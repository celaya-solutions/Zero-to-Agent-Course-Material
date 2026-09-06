#!/usr/bin/env python3
# Document:    Night Watchman Runtime
# Version:     v1.0.0
# Author:      Celaya Solutions
# Contact:     hello@celayasolutions.com
# Date:        2026-09-06
# SHA256:      dc4ac67c210eabcf806ff98c94add574c2da9524922d445204aa358eac9aaf69
# Chain:       n/a
# Tx:          [not anchored]
# License:     All Rights Reserved / Celaya Solutions

"""One controlled status, persistent decisions, and one issue per transition."""
from __future__ import annotations

import argparse
import base64
import copy
import datetime as dt
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
PAGE = "courses/project-lab/level-02/assets/practice-page.html"
STATE = ".watch-state/watchman.json"
MAX_PAGE = 128 * 1024
MAX_RESPONSE = 2 * 1024 * 1024
ALLOWED_VALUES = {"OPEN", "PAUSED"}


class WatchError(Exception):
    """A safe, learner-readable failure; never includes a token or response body."""


class ApiError(WatchError):
    def __init__(self, status):
        self.status = status
        super().__init__(f"GitHub HTTP {status}. Check Issues, Actions policy, and branch rules; no success recorded.")


class SignalParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.values = []
        self.active = None

    def handle_starttag(self, tag, attrs):
        # The practice signal is deliberately a simple text element.
        if dict(attrs).get("id") == "watch-value":
            if self.active is not None:
                raise WatchError("Duplicate watch-value marker.")
            self.active = (tag, len(self.stack))
            self.values.append("")
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        if dict(attrs).get("id") == "watch-value":
            raise WatchError("Empty watch-value marker.")

    def handle_endtag(self, tag):
        if self.active and (not self.stack or self.stack[-1] != tag):
            raise WatchError("Malformed watch-value markup.")
        if self.active == (tag, len(self.stack) - 1):
            self.active = None
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_data(self, data):
        if self.active:
            self.values[-1] += data


def extract_value(page):
    parser = SignalParser()
    parser.feed(page)
    parser.close()
    if len(parser.values) != 1 or parser.active:
        raise WatchError("Need exactly one closed element with id=watch-value.")
    value = " ".join(parser.values[0].split())
    if value not in ALLOWED_VALUES:
        raise WatchError("watch-value must be OPEN or PAUSED. Unknown or empty text is a failure.")
    return value


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise WatchError("Redirect refused. Check the approved practice address.")


def request_bytes(url, *, method="GET", data=None, token=None, limit=MAX_RESPONSE):
    headers = {"User-Agent": "ZTA-Night-Watchman/1.1", "Accept": "application/vnd.github+json"}
    if token:
        headers.update(Authorization=f"Bearer {token}", **{"X-GitHub-Api-Version": "2022-11-28"})
    if data is not None:
        data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(urllib.request.Request(url, data=data, headers=headers, method=method), timeout=15) as response:
            payload = response.read(limit + 1)
            if len(payload) > limit:
                raise WatchError("Response exceeds the size limit. No value saved.")
            return payload
    except urllib.error.HTTPError as exc:
        raise ApiError(exc.code) from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise WatchError("Network request failed or timed out. No automatic retry; inspect the receipt.") from None


def fetch_page(url):
    if not url.startswith("https://raw.githubusercontent.com/"):
        raise WatchError("Only the supplied public GitHub practice page is supported.")
    return request_bytes(url, limit=MAX_PAGE).decode("utf-8")


def validate_state(state, source):
    if state is None:
        return
    if not isinstance(state, dict) or state.get("schema") != 1 or state.get("source") != source:
        raise WatchError("State is invalid or belongs to another source. Preserve it and ask the instructor.")
    if state.get("current") not in ALLOWED_VALUES or type(state.get("sequence")) is not int or state["sequence"] < 0:
        raise WatchError("Saved value or sequence is invalid. Do not reset the baseline.")
    pending = state.get("pending")
    if pending is not None:
        if not isinstance(pending, dict) or pending.get("old") != state["current"] or pending.get("new") not in ALLOWED_VALUES or pending["new"] == pending["old"]:
            raise WatchError("Pending transition is invalid. Preserve state for review.")
        expected = transition(source, state["sequence"] + 1, pending["old"], pending["new"])
        if pending.get("id") != expected["id"] or type(pending.get("attempted")) is not bool:
            raise WatchError("Pending transition identity is invalid.")


def transition(source, sequence, old, new):
    identity = hashlib.sha256(json.dumps([source, sequence, old, new]).encode()).hexdigest()[:24]
    return {"id": identity, "old": old, "new": new, "attempted": False}


def issue_text(pending, source):
    title = f"Change spotted: {pending['old']} to {pending['new']}"
    body = (f"TRAINING-ONLY: Night Watchman\n\nSource: {source}\n\n"
            f"Old value: **{pending['old']}**\n\nNew value: **{pending['new']}**\n\n"
            "Meaningful change: the marked status changed. Check the practice page; no other action was taken.\n\n"
            f"<!-- zta-watchman:{pending['id']} -->")
    return title, body


class GitHubStore:
    def __init__(self, repository, branch, token):
        self.repository, self.branch, self.token = repository, branch, token
        self.sha = None
        self.base = f"https://api.github.com/repos/{repository}"
        self.source = f"https://raw.githubusercontent.com/{repository}/{urllib.parse.quote(branch, safe='')}/{PAGE}"

    def api(self, path, *, method="GET", data=None):
        return json.loads(request_bytes(self.base + path, method=method, data=data, token=self.token))

    def load(self):
        # Confirm access before interpreting a missing state file as the first run.
        info = self.api("")
        if info.get("private") or info.get("default_branch") != self.branch or not info.get("has_issues"):
            raise WatchError("Use a public learner fork with Issues enabled and its default branch selected.")
        try:
            item = self.api(f"/contents/{STATE}?ref={urllib.parse.quote(self.branch, safe='')}")
        except ApiError as exc:
            if exc.status == 404:
                return None
            raise
        self.sha = item["sha"]
        state = json.loads(base64.b64decode(item["content"], validate=False).decode("utf-8"))
        if state is None:
            raise WatchError("Saved state is null. Preserve it for instructor review.")
        return state

    def save(self, state):
        payload = {"message": "Record watchman decision", "branch": self.branch,
                   "content": base64.b64encode((json.dumps(state, indent=2) + "\n").encode()).decode()}
        if self.sha:
            payload["sha"] = self.sha
        item = self.api(f"/contents/{STATE}", method="PUT", data=payload)
        self.sha = item["content"]["sha"]

    def find_issue(self, pending):
        marker = f"<!-- zta-watchman:{pending['id']} -->"
        for page in range(1, 11):
            issues = self.api(f"/issues?state=all&sort=created&direction=desc&per_page=100&page={page}")
            for item in issues:
                if not item.get("pull_request") and item.get("user", {}).get("login") == "github-actions[bot]" and marker in (item.get("body") or ""):
                    return f"https://github.com/{self.repository}/issues/{int(item['number'])}"
            if len(issues) < 100:
                return None
        raise WatchError("Issue search limit reached. Instructor review required; no issue sent.")

    def create_issue(self, pending):
        title, body = issue_text(pending, self.source)
        item = self.api("/issues", method="POST", data={"title": title, "body": body})
        return f"https://github.com/{self.repository}/issues/{int(item['number'])}"


class LocalStore:
    """File-backed rehearsal; never makes a request or creates a GitHub issue."""
    def __init__(self, directory):
        self.directory = directory
        self.source = "local rehearsal / supplied practice-page.html"

    def load(self):
        path = self.directory / "state.json"
        if not path.exists():
            return None
        state = json.loads(path.read_text(encoding="utf-8"))
        if state is None:
            raise WatchError("Saved state is null. Preserve it for instructor review.")
        return state

    def save(self, state):
        self.directory.mkdir(parents=True, exist_ok=True)
        path = self.directory / "state.json"
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)

    def find_issue(self, pending):
        path = self.directory / f"local-alert-{pending['id']}.md"
        return str(path) if path.exists() else None

    def create_issue(self, pending):
        path = self.directory / f"local-alert-{pending['id']}.md"
        title, body = issue_text(pending, self.source)
        with path.open("x", encoding="utf-8") as output:
            output.write(f"# LOCAL REHEARSAL - no hosted issue\n\n{title}\n\n{body}\n")
        return str(path)


def run_round(store, read_page, receipt):
    """Persist intent before sending; reconcile uncertain sends without resending."""
    state = store.load()
    validate_state(state, store.source)
    previous = state["current"] if state else None
    receipt["previous"] = previous
    if state and state.get("pending"):
        pending = copy.deepcopy(state["pending"])
        receipt.update(current=pending["new"], transition=pending["id"], recovery=True)
    else:
        current = extract_value(read_page())
        receipt["current"] = current
        if state is None:
            store.save({"schema": 1, "source": store.source, "current": current, "sequence": 0, "pending": None})
            receipt["decision"] = "baseline saved"
            return
        if previous == current:
            receipt["decision"] = "no change"
            return
        pending = transition(store.source, state["sequence"] + 1, previous, current)
        state["pending"] = pending
        store.save(state)
        receipt["transition"] = pending["id"]

    issue = store.find_issue(pending)
    if not issue:
        if pending["attempted"]:
            raise WatchError("Alert delivery is uncertain. No second issue sent. Disable and ask the instructor to reconcile the pending ID.")
        pending["attempted"] = True
        state["pending"] = pending
        store.save(state)  # Durable send intent; a crash from here must never auto-resend.
        try:
            issue = store.create_issue(pending)
        except ApiError as exc:
            if exc.status in {400, 401, 403, 404, 410, 422}:
                pending["attempted"] = False  # Definitive rejection; repair permission, then retry.
                store.save(state)
            raise
    receipt["issue"] = issue
    store.save({**state, "current": pending["new"], "sequence": state["sequence"] + 1, "pending": None})
    receipt["decision"] = "alert recovered" if receipt.get("recovery") else "changed"


def hosted_context(env):
    if env.get("WATCHMAN_ENABLED") != "true":
        raise WatchError("WATCHMAN_ENABLED is not true. Watcher remains off.")
    repo, branch, sha = env.get("GITHUB_REPOSITORY", ""), env.get("WATCH_BRANCH", ""), env.get("GITHUB_SHA", "")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) or repo.lower() == "celaya-solutions/zero-to-agent-course-material":
        raise WatchError("Use your designated learner fork, not the canonical course repository.")
    if not branch or env.get("GITHUB_REF") != f"refs/heads/{branch}" or not re.fullmatch(r"[a-f0-9]{40}", sha):
        raise WatchError("Run the workflow on the default branch with a valid source commit.")
    if env.get("GITHUB_EVENT_NAME") not in {"workflow_dispatch", "schedule"} or not env.get("GITHUB_TOKEN"):
        raise WatchError("Hosted mode requires the course workflow and temporary GITHUB_TOKEN.")
    return GitHubStore(repo, branch, env["GITHUB_TOKEN"]), f"https://raw.githubusercontent.com/{repo}/{sha}/{PAGE}"


def execute(store, read_page, directory, *, route, run_id, source_commit="local"):
    directory.mkdir(parents=True, exist_ok=True)
    receipt = {"time": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "route": route,
               "run": run_id, "source_commit": source_commit, "decision": "failed"}
    code = 0
    try:
        run_round(store, read_page, receipt)
    except WatchError as exc:
        receipt.update(decision="failed", error=str(exc)); code = 1
    except (OSError, ValueError, KeyError, TypeError):
        receipt.update(decision="failed", error="Unreadable page, state, or API response. Preserve the last good state; ask the instructor."); code = 1
    serialized = json.dumps(receipt, sort_keys=True)
    with (directory / "rounds.jsonl").open("a", encoding="utf-8") as output:
        output.write(serialized + "\n")
    print(serialized)
    if os.environ.get("GITHUB_STEP_SUMMARY") and route == "GitHub Actions":
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
            summary.write("## Night Watchman receipt\n\n```json\n" + json.dumps(receipt, indent=2) + "\n```\n")
    return code


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--github", action="store_true", help="Only for the installed GitHub Actions workflow")
    args = parser.parse_args(argv)
    directory = ROOT / ".zta/watchman"
    if args.github:
        directory = ROOT / ".zta/watchman-run"
        try:
            store, url = hosted_context(os.environ)
        except WatchError as exc:
            directory.mkdir(parents=True, exist_ok=True)
            receipt = {"time": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "decision": "failed", "error": str(exc)}
            (directory / "rounds.jsonl").write_text(json.dumps(receipt) + "\n", encoding="utf-8")
            print(json.dumps(receipt)); return 1
        return execute(store, lambda: fetch_page(url), directory, route="GitHub Actions",
                       run_id=os.environ.get("GITHUB_RUN_ID", "unknown") + "/" + os.environ.get("GITHUB_RUN_ATTEMPT", "1"), source_commit=os.environ["GITHUB_SHA"])
    print("LOCAL REHEARSAL: one round; no network, hosted issue, or schedule. Files stay in .zta/watchman/.")
    return execute(LocalStore(directory), lambda: (ROOT / PAGE).read_text(encoding="utf-8"), directory,
                   route="local rehearsal", run_id="local")


if __name__ == "__main__":
    raise SystemExit(main())
