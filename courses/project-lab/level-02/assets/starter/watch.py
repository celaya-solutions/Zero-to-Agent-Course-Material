#!/usr/bin/env python3
"""Watch one approved page value and leave a small, inspectable trail."""

from __future__ import annotations

import datetime as dt
import html
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request


STATE_DIR = Path(os.environ.get("WATCH_STATE_DIR", ".watch-state"))
PREVIOUS_FILE = STATE_DIR / "previous.txt"
LOG_FILE = STATE_DIR / "log.txt"
ALERT_FILE = STATE_DIR / "alert.txt"


def extract_value(page: str) -> str:
    """Return the text inside the one element marked watch-value."""
    match = re.search(
        r'<[^>]+id=["\']watch-value["\'][^>]*>(.*?)</[^>]+>',
        page,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        raise ValueError("The page has no element with id=watch-value")
    text = re.sub(r"<[^>]+>", "", match.group(1))
    return html.unescape(text).strip()


def fetch_page(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "ZTA-Project-Lab-Watchman/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8")


def create_issue(title: str, body: str) -> None:
    token = os.environ.get("GITHUB_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repository:
        print("Issue skipped: GITHUB_TOKEN or GITHUB_REPOSITORY is unavailable")
        return

    payload = json.dumps({"title": title, "body": body}).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repository}/issues",
        data=payload,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "ZTA-Project-Lab-Watchman/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        if response.status != 201:
            raise RuntimeError(f"Issue creation returned HTTP {response.status}")


def log_line(value: str, decision: str) -> None:
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    with LOG_FILE.open("a", encoding="utf-8") as log:
        log.write(f"{timestamp} | value={value} | decision={decision}\n")


def main() -> int:
    url = os.environ.get("WATCH_URL")
    if not url:
        print("WATCH_URL is required", file=sys.stderr)
        return 2

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        current = extract_value(fetch_page(url))
    except (OSError, ValueError, urllib.error.URLError) as error:
        print(f"Watch failed: {error}", file=sys.stderr)
        return 1

    previous = PREVIOUS_FILE.read_text(encoding="utf-8").strip() if PREVIOUS_FILE.exists() else None
    if previous is None:
        decision = "baseline saved"
        print(f"First look saved: {current}")
    elif previous == current:
        decision = "no change"
        print(f"No change: {current}")
    else:
        decision = f"changed from {previous} to {current}"
        alert = f"Controlled watch value changed from {previous} to {current}."
        ALERT_FILE.write_text(alert + "\n", encoding="utf-8")
        print(alert)
        create_issue(f"Change spotted: {previous} to {current}", alert)

    PREVIOUS_FILE.write_text(current + "\n", encoding="utf-8")
    log_line(current, decision)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
