# Document:    Night Watchman Behavior Checks
# Version:     v1.0.0
# Author:      Celaya Solutions
# Contact:     hello@celayasolutions.com
# Date:        2026-09-06
# SHA256:      690ad94d2f56a4afd37752edbd62b40e8e4191d49a1a40daf6a8ca514a9bba74
# Chain:       n/a
# Tx:          [not anchored]
# License:     All Rights Reserved / Celaya Solutions

"""Behavior checks with temporary files and a fake GitHub API; no external writes."""
import base64
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import urllib.error

import pytest
import yaml

PROJECT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("night_watchman", PROJECT / "watch.py")
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)
spec = importlib.util.spec_from_file_location("watchman_manage", PROJECT / "manage.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def page(value="OPEN", footer="one"):
    return f'<html><body><p>Status: <strong id="watch-value">{value}</strong></p><footer>{footer}</footer></body></html>'


class Store(w.LocalStore):
    def __init__(self, path):
        super().__init__(path)
        self.saves = 0
        self.fail_save = None
        self.issue_failure = None
        self.lose_issue_response = False
        self.sent = 0

    def save(self, state):
        self.saves += 1
        if self.saves == self.fail_save:
            raise w.WatchError("State write rejected")
        super().save(state)

    def create_issue(self, pending):
        if self.issue_failure:
            raise self.issue_failure
        result = super().create_issue(pending)
        self.sent += 1
        if self.lose_issue_response:
            raise w.WatchError("Response lost")
        return result


def run(store, value="OPEN", **kwargs):
    code = w.execute(store, kwargs.get("read", lambda: page(value, kwargs.get("footer", "one"))), store.directory,
                     route="local fixture", run_id="test")
    receipt = json.loads((store.directory / "rounds.jsonl").read_text().splitlines()[-1])
    return code, receipt


@pytest.mark.parametrize("markup", [page(), page("<b>OPEN</b>"), page(" \nOPEN\t"), page("O&#80;EN")])
def test_stable_extraction(markup):
    assert w.extract_value(markup) == "OPEN"


@pytest.mark.parametrize("markup", ["<p>OPEN</p>", page(""), page("UNKNOWN"), page("OPEN") + page("PAUSED"), '<b id="watch-value">OPEN', '<b id="watch-value"/>', '<b id="watch-value"><i>OPEN</b>', page("OPEN PAUSED")])
def test_invalid_signals_fail(markup):
    with pytest.raises(w.WatchError):
        w.extract_value(markup)


def test_baseline_unchanged_changed_and_repeat(tmp_path):
    store = Store(tmp_path)
    assert run(store)[1]["decision"] == "baseline saved"
    assert run(store)[1]["decision"] == "no change"
    code, changed = run(store, "PAUSED")
    assert code == 0 and changed["decision"] == "changed"
    assert changed["previous"] == "OPEN" and changed["current"] == "PAUSED"
    assert "Old value: **OPEN**" in Path(changed["issue"]).read_text()
    assert run(store, "PAUSED")[1]["decision"] == "no change"
    assert store.sent == 1 and store.load()["current"] == "PAUSED"
    assert len((tmp_path / "rounds.jsonl").read_text().splitlines()) == 4


def test_irrelevant_footer_does_not_alert(tmp_path):
    store = Store(tmp_path)
    run(store)
    assert run(store, footer="a different date")[1]["decision"] == "no change"
    assert store.sent == 0


def test_back_and_forth_is_a_new_transition(tmp_path):
    store = Store(tmp_path)
    for value in ["OPEN", "PAUSED", "OPEN", "PAUSED"]:
        assert run(store, value)[0] == 0
    assert store.sent == 3 and store.load()["sequence"] == 3


@pytest.mark.parametrize("read", [lambda: "no marker", lambda: page(""), lambda: (_ for _ in ()).throw(w.WatchError("Fetch timed out"))])
def test_page_failure_preserves_baseline_and_logs(tmp_path, read):
    store = Store(tmp_path)
    run(store)
    saved = store.load()
    code, receipt = run(store, read=read)
    assert code == 1 and receipt["decision"] == "failed" and receipt["time"]
    assert store.load() == saved and store.sent == 0


@pytest.mark.parametrize("save_number", [1, 2, 3])
def test_no_issue_before_durable_state(tmp_path, save_number):
    store = Store(tmp_path)
    store.fail_save = save_number
    if save_number != 1:
        run(store)
    code, _ = run(store, "PAUSED")
    assert code == 1 and store.sent == 0


def test_alert_success_state_failure_reconciles_without_duplicate(tmp_path):
    store = Store(tmp_path)
    run(store)
    store.fail_save = 4
    assert run(store, "PAUSED")[0] == 1
    assert store.load()["current"] == "OPEN" and store.load()["pending"]["attempted"]
    assert run(store, "PAUSED")[1]["decision"] == "alert recovered"
    assert store.load()["current"] == "PAUSED" and store.sent == 1


def test_lost_issue_response_reconciles(tmp_path):
    store = Store(tmp_path)
    run(store)
    store.lose_issue_response = True
    assert run(store, "PAUSED")[0] == 1
    assert run(store, "PAUSED")[1]["decision"] == "alert recovered"
    assert store.sent == 1


def test_uncertain_issue_absent_stops_without_resend(tmp_path):
    store = Store(tmp_path)
    run(store)
    store.issue_failure = w.WatchError("Network failed")
    assert run(store, "PAUSED")[0] == 1
    store.issue_failure = None
    code, receipt = run(store, "PAUSED")
    assert code == 1 and "No second issue sent" in receipt["error"] and store.sent == 0


def test_definite_issue_denial_can_retry_after_repair(tmp_path):
    store = Store(tmp_path)
    run(store)
    store.issue_failure = w.ApiError(403)
    assert run(store, "PAUSED")[0] == 1
    assert store.load()["pending"]["attempted"] is False
    store.issue_failure = None
    assert run(store, "PAUSED")[0] == 0 and store.sent == 1


@pytest.mark.parametrize("bad", ["null", "{invalid", "{}", '{"schema": 1,"current":"OPEN","source":"elsewhere","sequence":0}'])
def test_corrupt_state_is_not_a_new_baseline(tmp_path, bad):
    store = Store(tmp_path)
    (tmp_path / "state.json").write_text(bad)
    assert run(store)[0] == 1
    assert (tmp_path / "state.json").read_text() == bad and store.sent == 0


def environment():
    return {"WATCHMAN_ENABLED": "true", "GITHUB_REPOSITORY": "learner/course", "WATCH_BRANCH": "main",
            "GITHUB_SHA": "a" * 40, "GITHUB_REF": "refs/heads/main", "GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_TOKEN": "fake-test-only"}


@pytest.mark.parametrize("key,value", [("WATCHMAN_ENABLED", "false"), ("GITHUB_REPOSITORY", "celaya-solutions/Zero-to-Agent-Course-Material"), ("GITHUB_REF", "refs/heads/other"), ("GITHUB_EVENT_NAME", "pull_request"), ("GITHUB_TOKEN", ""), ("GITHUB_SHA", "branch-name")])
def test_hosted_guards(key, value):
    env = environment(); env[key] = value
    with pytest.raises(w.WatchError):
        w.hosted_context(env)


def test_hosted_fetch_uses_immutable_run_commit():
    store, url = w.hosted_context(environment())
    assert "/" + "a" * 40 + "/" in url and url.endswith(w.PAGE)
    assert "/main/" in store.source


def test_github_state_cas_and_closed_issue_lookup(monkeypatch):
    store, _ = w.hosted_context(environment())
    state = {"schema": 1, "source": store.source, "current": "OPEN", "sequence": 0, "pending": None}
    calls = []
    pending = w.transition(store.source, 1, "OPEN", "PAUSED")
    def api(path, *, method="GET", data=None):
        calls.append((path, method, data))
        if path == "": return {"private": False, "has_issues": True, "default_branch": "main"}
        if path.startswith("/issues"):
            if "page=2" in path:
                return [{"number": 42,"state":"closed","user":{"login":"github-actions[bot]"},"body":w.issue_text(pending, store.source)[1]}]
            return [{"number":1,"body":"unrelated","user":{"login":"learner"}}] * 100
        if method == "PUT": return {"content":{"sha":"next-sha"}}
        return {"sha":"old-sha","content":base64.b64encode(json.dumps(state).encode()).decode()}
    monkeypatch.setattr(store, "api", api)
    assert store.load() == state
    store.save(state)
    assert calls[-1][2]["sha"] == "old-sha" and store.sha == "next-sha"
    assert store.find_issue(pending).endswith("/issues/42")


def test_api_denial_does_not_expose_response_or_token(monkeypatch):
    class Opener:
        def open(self, *args, **kwargs):
            raise urllib.error.HTTPError("https://example.com/secret",403,"secret-token",{},None)
    monkeypatch.setattr(w.urllib.request,"build_opener",lambda *a:Opener())
    with pytest.raises(w.ApiError) as error:
        w.request_bytes("https://api.github.com/repos/learner/course",token="secret-token")
    assert "secret" not in str(error.value) and "403" in str(error.value)


def test_bounded_response_and_timeout(monkeypatch):
    class Response:
        def __enter__(self): return self
        def __exit__(self,*a): pass
        def read(self, count): assert count == 6; return b"abcdef"
    class Opener:
        def open(self,*a,**kw): assert kw["timeout"] == 15; return Response()
    monkeypatch.setattr(w.urllib.request,"build_opener",lambda *a:Opener())
    with pytest.raises(w.WatchError,match="size limit"):
        w.request_bytes("https://api.github.com",limit=5)


def test_redirect_refused():
    with pytest.raises(w.WatchError,match="Redirect"):
        w.NoRedirect().redirect_request(None,None,302,"",{},"http://127.0.0.1")


def test_installer_keeps_existing_files_and_private_evidence(tmp_path):
    for rel in ["projects/watchman/workflow.template.yml","courses/project-lab/level-02/worksheet.md"]:
        target=tmp_path/rel; target.parent.mkdir(parents=True,exist_ok=True); target.write_text("source")
    m.prepare(tmp_path)
    evidence=tmp_path/".zta/PROJECT-LAB-02.md"; evidence.write_text("my predictions")
    m.prepare(tmp_path)
    assert evidence.read_text()=="my predictions"
    assert (tmp_path/".github/workflows/watchman.yml").read_text()=="source"


def test_workflow_is_scoped_and_keeps_failure_receipts():
    data=yaml.safe_load((PROJECT/"workflow.template.yml").read_text())
    trigger=data.get("on",data.get(True)) # YAML 1.1 treats on as bool.
    assert set(trigger)=={"workflow_dispatch","schedule"}
    assert trigger["schedule"]==[{"cron":"17 13 * * *"}]
    job=data["jobs"]["watch"]
    assert job["permissions"]=={"contents":"write","issues":"write"}
    assert "WATCHMAN_ENABLED" in job["if"] and data["concurrency"]["cancel-in-progress"] is False
    artifact=job["steps"][-1]
    assert artifact["if"]=="always()" and artifact["with"]["path"]==".zta/watchman-run/rounds.jsonl"


def test_doctor_works_without_model_configuration():
    result=subprocess.run([str(Path(sys.executable).parent/("zta.exe" if sys.platform=="win32" else "zta")),"doctor","watchman"],capture_output=True,text=True,cwd=PROJECT.parents[1])
    assert result.returncode==0 and "PASS: local watcher" in result.stdout
