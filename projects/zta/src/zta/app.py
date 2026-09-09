"""A local document helper with an evidence worksheet that survives refresh."""
import json
import uuid
import warnings
from pathlib import Path
import gradio as gr
from zta import __version__
from zta.documents import CLASS_FILES, build_index, extract, inventory, retrieve
from zta.evidence import QUESTIONS, checks, export_markdown, valid_revision
from zta.providers import ProviderError, request_answer, request_estimate, RATES
from zta.storage import config, data_dir, now, progress, root, save_progress, settings
from zta.ui import blocks

CLASSES = ["Choose", "public", "training-only", "unclassified"]
VERDICTS = ["Choose", "Pass", "Miss"]
PROMPT = ("Read the Level 1 instructions and inspect my recorded miss. Explain its likely cause before editing. "
          "Change one rule or retrieval setting that addresses it. Preserve the supplied documents, expected results, "
          "and tests. Show the change, explain why it should help, and tell me how to rerun the same question. "
          "Do not publish anything.")



def state_and_context():
    """Every callback reloads the most recent disk state before it reads or writes."""
    return progress(), config(), settings()


def index_path():
    return data_dir() / "index.sqlite3"


def assets_dir():
    return root() / "courses/project-lab/level-01/assets"


def binder_dir():
    folder = data_dir() / "binder"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def binder_files():
    folder = data_dir() / "binder"
    return sorted(p for p in folder.iterdir() if p.is_file()) if folder.exists() else []


def save_field(key, value):
    current = progress()
    current["fields"][key] = value or ""
    save_progress(current)


def field_value(key):
    return progress()["fields"].get(key, "")


def set_classification(name, value):
    current = progress()
    current["classifications"][name] = value
    save_progress(current)


def set_verdict(run_id, value):
    current = progress()
    for run in current["runs"]:
        if run["id"] == run_id:
            run["verdict"] = value
    save_progress(current)


def record_open(run, passage):
    current = progress()
    current["opened"].append({"at": now(), "run": run["id"], "number": run["number"],
                              "source": passage["source"], "heading": passage["heading"],
                              "quote": passage["text"]})
    save_progress(current)


def replace_binder(files):
    """Parse everything before replacing any existing binder or index."""
    if not files:
        raise ValueError("Choose at least one document.")
    if len(files) > 20:
        raise ValueError("Use at most 20 files.")
    named = []
    for path in files:
        name = Path(path).name
        if name != Path(name).name or "\\" in name:
            raise ValueError("Invalid filename.")
        named.append((name, Path(path).read_bytes()))
    if len({n for n, _ in named}) != len(named):
        raise ValueError("Use distinct filenames.")
    for name, data in named:
        extract(name, data)
    folder = binder_dir()
    for old in folder.iterdir():
        if old.is_file():
            old.unlink()
    for name, data in named:
        (folder / name).write_bytes(data)
    if index_path().exists():
        index_path().unlink()
    return len(named)


def load_class_binder():
    replace_binder([str(assets_dir() / name) for name in CLASS_FILES])
    return "Four documents loaded. Choose Build index next."


def build_binder_index():
    files = binder_files()
    if not files:
        raise ValueError("Load a binder before building the index.")
    passages = build_index(index_path(), [(p.name, p.read_bytes()) for p in files])
    return f"Indexed {len(files)} documents and {len(passages)} passages."


def expectations_ready(state=None):
    state = state or progress()
    return all(str(state["fields"].get(f"expected_{i}", "")).strip() for i in range(1, 6))


def preview_for(number, options=None):
    options = options or settings()
    if not index_path().exists():
        return []
    return retrieve(index_path(), QUESTIONS[number - 1], options["max_passages"])


def run_question(number, consented):
    """One request per click. No automatic retries."""
    state, cfg, options = state_and_context()
    if not expectations_ready(state):
        raise ValueError("Save an expected result for all five questions first.")
    if not index_path().exists():
        raise ValueError("Build the document index before asking a question.")
    if cfg["provider"] != "ollama" and not consented:
        raise ValueError("Read the cloud notice and confirm the public/synthetic boundary in the sidebar.")
    passages = preview_for(number, options)
    result = (request_answer(cfg, QUESTIONS[number - 1], passages) if passages else
              {"status": "not_found", "answer": "Not in the documents.", "citations": [], "seconds": 0, "estimated_usd": 0})
    current = progress()
    current["runs"].append({"id": uuid.uuid4().hex[:12], "at": now(), "number": number,
                            "question": QUESTIONS[number - 1], "expected": current["fields"].get(f"expected_{number}", ""),
                            "provider": cfg["provider"], "model": cfg["model"], "settings": options,
                            "passages": passages, "result": result, "verdict": "Choose", "route": "live"})
    save_progress(current)


def load_saved_examples():
    """Imports authored classroom examples. These are never live model results."""
    state = progress()
    if not expectations_ready(state):
        raise ValueError("Save an expected result for all five questions first.")
    saved = json.loads((assets_dir() / "saved-runs.json").read_text(encoding="utf-8"))
    for run in saved:
        run.update({"id": uuid.uuid4().hex[:12], "at": now(),
                    "expected": state["fields"].get(f"expected_{run['number']}", ""),
                    "verdict": "Choose", "route": "saved classroom example"})
        state["runs"].append(run)
    save_progress(state)
    return f"Loaded {len(saved)} saved classroom examples. They are labeled saved, not live."


def save_revision(before, after, change, reason):
    state = progress()
    runs = state["runs"]
    candidate = {"before": before, "after": after, "change": change or "", "reason": reason or "", "valid": True}
    match = next((r for r in runs if r["id"] == before), None)
    candidate["question"] = match["number"] if match else None
    if not valid_revision({"runs": runs, "revision": candidate}):
        raise ValueError("Choose an earlier BEFORE and a later AFTER run of the SAME question, "
                         "and explain the change and result.")
    state["revision"] = candidate
    save_progress(state)
    return "Revision evidence saved."


def export_packet():
    state, cfg, _ = state_and_context()
    target = data_dir() / "PROJECT-LAB-01.md"
    target.write_text(export_markdown(state, cfg), encoding="utf-8")
    return str(target)


def run_label(run):
    return f"Q{run['number']} · {run['at']} · {run['id']} · {run['route']}"


def passage_caption(passage):
    return f"{passage['class']} | Receipt {passage['id']} | Page {passage['page'] or 'not applicable'}"


def workspace_text(cfg, options):
    return (f"### Your workspace\n**Engine:** {cfg['provider']}\n\n`{cfg['model']}`\n\n"
            f"Course {__version__} · {options['max_passages']} passages per question\n\n"
            "Local search stays on this computer.")


def cloud_text(cfg):
    if cfg["provider"] == "ollama":
        return ""
    incoming, outgoing = RATES[cfg["provider"]]
    return ("**Cloud answers send your question and selected passages to the chosen provider.**\n\n"
            f"Model rate: ${incoming:g} per million input tokens / ${outgoing:g} per million output tokens. "
            "Check the current provider price before use.\n\n"
            "One request per click. No automatic retries. API billing is separate from "
            "coding-assistant access.")


def guard(fn):
    """Turn an expected failure into a visible message instead of a stack trace."""
    def wrapped(*args):
        try:
            return fn(*args)
        except (ValueError, OSError, ProviderError) as exc:
            raise gr.Error(str(exc)) from exc
    return wrapped


def bump(tick):
    return tick + 1


def show_passages(passages, run=None, tick=None):
    for passage in passages:
        with gr.Accordion(f"{passage['source']} / {passage['heading']}", open=False):
            gr.Markdown(passage_caption(passage), elem_classes="zta-kicker")
            gr.Textbox(passage["text"], label=None, show_label=False, container=False,
                       lines=min(12, passage["text"].count("\n") + 3), interactive=False,
                       elem_classes="zta-passage")
            if run is not None:
                opened = gr.Button("I opened and checked this source", size="sm")
                opened.click(guard(lambda r=run, p=passage: record_open(r, p)), None, None).then(
                    lambda: gr.Info("Source check recorded. Explain your comparison in Proof."), None, None
                ).then(bump, tick, tick)


def build():
    try:
        cfg, options = config(), settings()
    except (ValueError, OSError) as exc:
        with blocks("Zero to Agent · Level 1") as broken:
            gr.Markdown(f"## Setup problem\n\n{exc}\n\nFix this, then run `uv run --frozen zta start documents` again.")
        return broken

    with blocks("Your Documents Answer Back | Zero to Agent") as demo:
        tick = gr.State(0)
        with gr.Row():
            with gr.Column(scale=3):
                gr.Markdown("CELAYA SOLUTIONS LEARNING / ZERO TO AGENT / LEVEL 01", elem_classes="zta-kicker")
                gr.Markdown("# Your Documents Answer Back\nFind the page. Check the answer. Show the proof.")
            with gr.Column(scale=1, elem_classes="zta-side"):
                # Built once per process, so these must be refilled on every page load: the lesson
                # has learners edit settings.toml and refresh to read the new value here.
                workspace = gr.Markdown(workspace_text(cfg, options))
                consent = gr.Checkbox(label="I understand and will use only public or synthetic files",
                                      value=False, visible=cfg["provider"] != "ollama")
                cloud_notice = gr.Markdown(cloud_text(cfg), visible=cfg["provider"] != "ollama")

                @gr.render(inputs=tick)
                def spend(_):
                    total = sum(r["result"].get("estimated_usd", 0) for r in progress()["runs"])
                    gr.Markdown(f"Recorded API estimate: ${total:.4f}. Provider billing is authoritative. "
                                "Rates checked 2026-09-06.", elem_classes="zta-kicker")

                gr.Markdown("Stop the app: press **Ctrl+C** in its terminal.\n\n"
                            "Private progress is saved in `.zta/` and excluded from Git.\n\n"
                            "[Course materials](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material) · "
                            "[Course sign in](https://learn.zerotoagent.org/auth/users/sign_in)",
                            elem_classes="zta-kicker")

        def refresh_header():
            live_cfg, live_options = config(), settings()
            cloud = live_cfg["provider"] != "ollama"
            return (workspace_text(live_cfg, live_options),
                    gr.update(visible=cloud),
                    gr.update(value=cloud_text(live_cfg), visible=cloud))

        demo.load(guard(refresh_header), None, [workspace, consent, cloud_notice])

        with gr.Tabs():
            with gr.Tab("1 · Start"):
                gr.Markdown("### Three tasks. Ninety minutes.\n\nBuild a binder from four safe documents. "
                            "Test five questions. Make one change and rerun.\n\n"
                            "> Preparation comes first: fork the repo, install with uv, choose your coding assistant "
                            "and answer engine, then run doctor.")
                nickname = gr.Textbox(label="Course nickname (not your legal name)", value=field_value("nickname"))
                assistant = gr.Textbox(label="Coding assistant: Claude Code, Codex, or manual card",
                                       value=field_value("assistant"))
                nickname.blur(guard(lambda v: save_field("nickname", v)), nickname, None)
                assistant.blur(guard(lambda v: save_field("assistant", v)), assistant, None)
                gr.Markdown("**Public facts are real. Training records are invented.** Never call a classroom rule "
                            "a CSR policy.\n\nA source receipt can be valid while the answer is wrong. Open the "
                            "source and compare the claim yourself.\n\n"
                            "*Encuentra la página y después responde. Si falta información, detente.*")

            with gr.Tab("2 · Binder"):
                gr.Markdown("### Build your binder\n\nLoad the four class documents, then build the searchable "
                            "index. Only selected document text is indexed; lessons and answer keys are excluded.")
                with gr.Row():
                    load_btn = gr.Button("Load class binder", variant="primary")
                    index_btn = gr.Button("Build index")
                binder_status = gr.Markdown("")
                uploads = gr.File(label="Or add approved documents (10 MB each; text PDF, Markdown, or UTF-8 text)",
                                  file_count="multiple", file_types=[".md", ".txt", ".pdf"])
                upload_btn = gr.Button("Use uploaded binder")
                load_btn.click(guard(load_class_binder), None, binder_status).then(bump, tick, tick)
                index_btn.click(guard(build_binder_index), None, binder_status).then(bump, tick, tick)
                upload_btn.click(
                    guard(lambda files: f"Uploaded binder saved ({replace_binder(files or [])} documents). "
                                        "Build its index next."),
                    uploads, binder_status).then(bump, tick, tick)

                @gr.render(inputs=tick)
                def binder_view(_):
                    files = binder_files()
                    if not files:
                        gr.Markdown("No binder yet. Choose **Load class binder** above.")
                        return
                    state = progress()
                    gr.Markdown("Open each original below. Classify it before asking questions.")
                    for path in files:
                        with gr.Row():
                            choice = gr.Dropdown(CLASSES, label=f"Classify {path.name}",
                                                 value=state["classifications"].get(path.name, "Choose"))
                            # The Proof checklist reads this, so it must re-render when it changes.
                            choice.change(guard(lambda v, n=path.name: set_classification(n, v)),
                                          choice, None).then(bump, tick, tick)
                            gr.DownloadButton(f"Open original: {path.name}", value=str(path), size="sm")
                    current = inventory(index_path())
                    if current:
                        gr.Markdown(f"Current index: {len({p['source'] for p in current})} documents / "
                                    f"{len(current)} passages", elem_classes="zta-kicker")
                        show_passages(current)
                    else:
                        gr.Markdown("Index not built yet. Choose **Build index**.")

            with gr.Tab("3 · Five questions"):
                gr.Markdown("### Predict, ask, inspect\n\nFill all five expected results before your first test. "
                            "For each answer, inspect its passages and record Pass or Miss. A Miss is useful "
                            "evidence.")
                for number, question in enumerate(QUESTIONS, 1):
                    box = gr.Textbox(label=f"{number}. {question} — expected behavior", lines=2,
                                     value=field_value(f"expected_{number}"))
                    box.blur(guard(lambda v, n=number: save_field(f"expected_{n}", v)), box, None).then(bump, tick, tick)

                @gr.render(inputs=tick)
                def questions_view(_):
                    state, live_cfg, live_options = state_and_context()
                    ready = expectations_ready(state)
                    have_index = index_path().exists()
                    if not ready:
                        gr.Markdown("> Save an expected result for all five questions to enable live tests. "
                                    "Click outside a box to save it.")
                    if not have_index:
                        gr.Markdown("> Build the binder index on the Binder tab before running a question.")
                    for number, question in enumerate(QUESTIONS, 1):
                        gr.Markdown(f"#### Question {number}\n{question}")
                        preview = preview_for(number, live_options) if have_index else []
                        with gr.Accordion(f"Preview retrieved evidence for question {number}", open=False):
                            if preview:
                                show_passages(preview)
                            else:
                                gr.Markdown("No passages retrieved.")
                        if live_cfg["provider"] != "ollama" and preview:
                            estimate = request_estimate(live_cfg["provider"], question, preview)
                            gr.Markdown(f"Before you run: planning estimate ${estimate['usd']:.4f} for about "
                                        f"{estimate['input_tokens']} input tokens and up to 800 output tokens. "
                                        "Actual tokenization and billing can differ; this is not a spending cap.",
                                        elem_classes="zta-kicker")
                        run_btn = gr.Button(f"Run question {number}", variant="primary",
                                            interactive=ready and have_index)
                        run_btn.click(guard(lambda consented, n=number: run_question(n, consented)),
                                      consent, None).then(bump, tick, tick)
                        runs = [r for r in state["runs"] if r["number"] == number]
                        if not runs:
                            continue
                        run = runs[-1]
                        result = run["result"]
                        status = ("**Needs review**" if result["status"] == "needs_review"
                                  else result["status"].replace("_", " ").title())
                        gr.Markdown(status)
                        gr.Textbox(result["answer"], show_label=False, container=False, interactive=False,
                                   lines=max(3, result["answer"].count("\n") + 2), elem_classes="zta-answer")
                        if live_options["show_source_quotes"]:
                            for citation in result["citations"]:
                                gr.Markdown(f"Source quote [{citation['id']}]: {citation['quote']}")
                        gr.Markdown(f"Run {run['id']} · {run['at']} · {result.get('seconds', 0)} seconds · "
                                    f"{run['route']}", elem_classes="zta-kicker")
                        cited = {c["id"] for c in result["citations"]}
                        gr.Markdown("Source receipts used by this answer:")
                        show_passages([p for p in run["passages"] if p["id"] in cited], run, tick)
                        verdict = gr.Dropdown(VERDICTS, label="My verdict", value=run.get("verdict", "Choose"))
                        # The Proof checklist reads this, so it must re-render when it changes.
                        verdict.change(guard(lambda v, rid=run["id"]: set_verdict(rid, v)),
                                       verdict, None).then(bump, tick, tick)

                with gr.Accordion("Service unavailable? Use a labeled saved example", open=False):
                    gr.Markdown("This imports an authored classroom example. It is not a live model result. You "
                                "still write expectations, inspect sources, and judge each answer.")
                    saved_btn = gr.Button("Load five saved examples")
                    saved_status = gr.Markdown("")
                    saved_btn.click(guard(load_saved_examples), None, saved_status).then(bump, tick, tick)

            with gr.Tab("4 · Improve"):
                gr.Markdown("### One change. Same question.\n\nSelect a weak result and explain why it needs work. "
                            "Keep the question unchanged. Use Claude Code, Codex, or the manual card to make one "
                            "small edit.")
                gr.Code(PROMPT, label="Bounded prompt for your coding assistant", wrap_lines=True,
                        interactive=False)
                gr.Markdown(
                    "**If all five pass:** in `projects/documents/settings.toml`, change `max_passages = 4` to `1`. "
                    "Save, refresh the app, and rerun question 5. Inspect the missing evidence. Restore `4`, save, "
                    "refresh, and rerun the same question. Compare the passages, even if the model safely refused "
                    "both times.\n\n"
                    "**Keep a useful change:** set `show_source_quotes = true` in that same file. Save, refresh, and "
                    "rerun your selected question. Supporting quotes will now appear below its answer. Commit that "
                    "improvement; leave `max_passages = 4`.")

                @gr.render(inputs=tick)
                def revision_view(_):
                    state = progress()
                    runs = state["runs"]
                    if len(runs) < 2:
                        gr.Markdown("> Run the same question at least twice before recording your improvement.")
                        return
                    labels = [(run_label(r), r["id"]) for r in runs]
                    saved = state.get("revision", {})
                    before = gr.Dropdown(labels, label="Before run", value=saved.get("before") or labels[0][1])
                    after = gr.Dropdown(labels, label="After run", value=saved.get("after") or labels[-1][1])
                    change = gr.Textbox(label="One change I made", lines=2, value=saved.get("change", ""))
                    reason = gr.Textbox(label="What changed in the evidence or answer, and why?", lines=3,
                                        value=saved.get("reason", ""))
                    submit = gr.Button("Save before and after", variant="primary")
                    status = gr.Markdown("")
                    submit.click(guard(save_revision), [before, after, change, reason], status).then(bump, tick, tick)

            with gr.Tab("5 · Proof"):
                gr.Markdown("### Save the work. Confirm receipt.")
                proof_fields = [
                    ("fork_url", "Your fork URL", 1),
                    ("commit_url", "Your final commit URL", 1),
                    ("source_check", "What did you compare in the two public sources?", 3),
                    ("data_boundary", "What stays on this computer, and what leaves it on your route?", 3),
                    ("unresolved", "Unresolved misses, account blocks, or saved-run use", 3),
                    ("exit_ticket", "Exit ticket: one missing-information rule and one conflict rule", 3),
                ]
                for key, label, lines in proof_fields:
                    box = gr.Textbox(label=label, lines=lines, value=field_value(key))
                    box.blur(guard(lambda v, k=key: save_field(k, v)), box, None).then(bump, tick, tick)

                @gr.render(inputs=tick)
                def checklist(_):
                    results = checks(progress())
                    gr.Markdown("\n".join(("- Complete: " if passed else "- Incomplete: ") + label
                                          for label, passed in results.items()))
                    if not all(results.values()):
                        gr.Markdown("> This is a draft packet: finish the incomplete items before submitting, or "
                                    "explain the access block to your instructor.")

                export_btn = gr.Button("Export PROJECT-LAB-01.md", variant="primary")
                packet = gr.File(label="Your private evidence packet", interactive=False)
                export_btn.click(guard(export_packet), None, packet)
                gr.Markdown(
                    "In GitHub Desktop, review only your intended project change. Commit and push it to your own "
                    "fork. Keep `.zta/` and this evidence file private.\n\n"
                    "Sign in to the course platform, open Level 1, upload PROJECT-LAB-01.md, then reopen Submission "
                    "History and check the file and timestamp. Downloading here does not submit it.\n\n"
                    "*If the platform is down, keep the file and record the block. After two attempts or five "
                    "minutes, use the saved route and ask the instructor for the next submission check.*")

    return demo


def main():
    # A learner reads this terminal for the app URL. Library upgrade notices are not their business.
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    build().launch(server_name="127.0.0.1", server_port=8501, inbrowser=False,
                   show_api=False, quiet=True, max_file_size="10mb")


if __name__ == "__main__":
    main()
