import json
import pytest


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setenv("ZTA_DATA_DIR", str(tmp_path / "state"))
    from zta import app as module
    return module


def prepare(app):
    """The class binder, indexed, with all five expectations saved."""
    app.load_class_binder()
    app.build_binder_index()
    for i in range(1, 6):
        app.save_field(f"expected_{i}", "Check supplied sources; stop if missing.")


def test_binder_loads_indexes_and_survives_reload(app):
    assert "Four documents loaded" in app.load_class_binder()
    assert {p.name for p in app.binder_files()} == set(app.CLASS_FILES)
    assert "Indexed 4 documents" in app.build_binder_index()
    assert {p["source"] for p in app.inventory(app.index_path())} == set(app.CLASS_FILES)


def test_saved_fields_survive_a_fresh_read(app):
    app.save_field("nickname", "Pilot learner")
    assert app.field_value("nickname") == "Pilot learner"
    assert app.progress()["fields"]["nickname"] == "Pilot learner"


def test_run_is_blocked_until_every_expectation_is_saved(app):
    app.load_class_binder()
    app.build_binder_index()
    assert not app.expectations_ready()
    for i in range(1, 5):
        app.save_field(f"expected_{i}", "Stops if missing.")
    assert not app.expectations_ready()
    with pytest.raises(ValueError, match="all five questions"):
        app.run_question(1, True)
    app.save_field("expected_5", "Shows both records.")
    assert app.expectations_ready()


def test_run_is_blocked_before_the_index_exists(app):
    for i in range(1, 6):
        app.save_field(f"expected_{i}", "Stops if missing.")
    with pytest.raises(ValueError, match="index"):
        app.run_question(1, True)


def test_cloud_route_refuses_to_send_without_consent(app, monkeypatch):
    prepare(app)
    monkeypatch.setattr(app, "config", lambda: {"provider": "claude", "model": "m", "api_key": "k"})
    sent = []
    monkeypatch.setattr(app, "request_answer", lambda *a: sent.append(a))
    with pytest.raises(ValueError, match="cloud notice"):
        app.run_question(1, False)
    assert sent == []


def test_a_run_records_its_question_expectation_and_route(app, monkeypatch):
    prepare(app)
    monkeypatch.setattr(app, "request_answer", lambda cfg, q, passages: {
        "status": "answered", "answer": "El Paso, Texas.",
        "citations": [{"id": passages[0]["id"], "quote": "El Paso"}], "seconds": 1, "estimated_usd": 0})
    app.run_question(1, False)
    run = app.progress()["runs"][-1]
    assert run["number"] == 1 and run["route"] == "live"
    assert run["question"] == app.QUESTIONS[0]
    assert run["expected"] == "Check supplied sources; stop if missing."
    assert run["passages"] and run["verdict"] == "Choose"


def test_saved_examples_are_labeled_saved_not_live(app):
    prepare(app)
    app.load_saved_examples()
    runs = app.progress()["runs"]
    assert len(runs) == 5
    assert {r["route"] for r in runs} == {"saved classroom example"}
    assert [r["number"] for r in runs] == [1, 2, 3, 4, 5]


def test_verdicts_and_classifications_persist(app):
    prepare(app)
    app.load_saved_examples()
    run_id = app.progress()["runs"][0]["id"]
    app.set_verdict(run_id, "Miss")
    assert app.progress()["runs"][0]["verdict"] == "Miss"
    app.set_classification("training-record-a.md", "training-only")
    assert app.progress()["classifications"]["training-record-a.md"] == "training-only"


def test_opening_a_source_records_a_receipt(app):
    prepare(app)
    app.load_saved_examples()
    run = next(r for r in app.progress()["runs"] if r["number"] == 3)
    for passage in run["passages"]:
        app.record_open(run, passage)
    opened = app.progress()["opened"]
    assert {o["number"] for o in opened} == {3}
    assert {o["source"] for o in opened} >= {"public-identity-and-work.md"}


def test_revision_rejects_two_different_questions(app):
    prepare(app)
    app.load_saved_examples()
    runs = app.progress()["runs"]
    with pytest.raises(ValueError, match="SAME question"):
        app.save_revision(runs[0]["id"], runs[1]["id"], "changed a rule", "more evidence")
    assert app.progress()["revision"] == {}


def test_revision_accepts_a_before_and_after_of_one_question(app, monkeypatch):
    prepare(app)
    monkeypatch.setattr(app, "request_answer", lambda cfg, q, passages: {
        "status": "answered", "answer": "El Paso, Texas.", "citations": [], "seconds": 1, "estimated_usd": 0})
    app.run_question(1, False)
    app.run_question(1, False)
    runs = app.progress()["runs"]
    assert "saved" in app.save_revision(runs[0]["id"], runs[1]["id"], "showed quotes", "same answer, visible support")
    assert app.progress()["revision"]["question"] == 1


def test_uploaded_binder_is_parsed_before_the_old_one_is_replaced(app, tmp_path):
    app.load_class_binder()
    before = {p.name for p in app.binder_files()}
    bad = tmp_path / "notes.md"
    bad.write_bytes(b"\xff\xfe not utf-8")
    with pytest.raises(ValueError):
        app.replace_binder([str(bad)])
    assert {p.name for p in app.binder_files()} == before


def test_export_writes_a_packet_naming_the_incomplete_checks(app):
    prepare(app)
    path = app.export_packet()
    text = open(path, encoding="utf-8").read()
    assert path.endswith("PROJECT-LAB-01.md")
    assert "# Level 1 - Your Documents Answer Back" in text
    assert "Incomplete: Fork and commit links recorded" in text
    assert "SHA256:      [pending]" not in text


def test_export_redacts_an_api_key(app, monkeypatch):
    prepare(app)
    monkeypatch.setattr(app, "config", lambda: {"provider": "claude", "model": "m", "api_key": "sk-abcdefghijklmnop"})
    app.save_field("unresolved", "I pasted sk-abcdefghijklmnop by mistake")
    text = open(app.export_packet(), encoding="utf-8").read()
    assert "sk-abcdefghijklmnop" not in text
    assert "[REDACTED]" in text


def test_preview_respects_max_passages(app, monkeypatch):
    prepare(app)
    monkeypatch.setattr(app, "settings", lambda: {"max_passages": 1, "show_source_quotes": False})
    assert len(app.preview_for(5)) == 1
    monkeypatch.setattr(app, "settings", lambda: {"max_passages": 4, "show_source_quotes": False})
    assert len(app.preview_for(5)) > 1


def test_the_blocks_page_builds(app):
    prepare(app)
    app.load_saved_examples()
    page = app.build()
    assert page.title.startswith("Your Documents Answer Back")


def test_a_broken_settings_file_builds_a_readable_page(app, monkeypatch):
    monkeypatch.setattr(app, "settings", lambda: (_ for _ in ()).throw(ValueError("max_passages must be 1 to 8.")))
    page = app.build()
    assert page is not None


def test_saved_runs_asset_matches_the_five_questions(app):
    saved = json.loads((app.assets_dir() / "saved-runs.json").read_text(encoding="utf-8"))
    assert [r["number"] for r in saved] == [1, 2, 3, 4, 5]
    for record in saved:
        assert record["question"] == app.QUESTIONS[record["number"] - 1]


def test_header_text_reports_the_current_max_passages(app):
    """The lesson has learners edit settings.toml and refresh to read the new value here."""
    cfg = {"provider": "ollama", "model": "gemma3:4b"}
    assert "4 passages per question" in app.workspace_text(cfg, {"max_passages": 4, "show_source_quotes": False})
    assert "1 passages per question" in app.workspace_text(cfg, {"max_passages": 1, "show_source_quotes": False})


def test_the_local_route_shows_no_cloud_notice(app):
    assert app.cloud_text({"provider": "ollama", "model": "gemma3:4b"}) == ""
    notice = app.cloud_text({"provider": "claude", "model": "m"})
    assert "leave" not in notice.lower() or "send" in notice.lower()
    assert "No automatic retries" in notice
