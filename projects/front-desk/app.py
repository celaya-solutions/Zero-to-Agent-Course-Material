"""Browser controls for the fixed classroom desk. Drafts never trigger actions."""
import queue
import threading
import warnings
import gradio as gr
import httpx
import desk

GROUPS = [("Five callers", "callers"), ("Ten fixed attacks", "attacks")]
STOPPED = ("The desk stopped. Earlier rows are saved. Check Ollama and the preparation guide; "
           "no cloud retry was made.")
CARD = ("Alias: River\nPublic route: hello@celayasolutions.com\n"
        "Need: Industrial document project conversation\nUrgency: This week\n"
        "Preferred follow-up time: Afternoons (request, not a promise)")

THEME = gr.themes.Base(
    primary_hue=gr.themes.colors.green,
    font=[gr.themes.GoogleFont("Source Sans 3"), "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("Source Code Pro"), "monospace"],
).set(
    body_background_fill="#f6f2e9",
    body_text_color="#192a25",
    body_text_color_subdued="#45594f",
    background_fill_primary="#f6f2e9",
    background_fill_secondary="#e7e9dd",
    block_background_fill="#f6f2e9",
    block_label_text_color="#192a25",
    block_title_text_color="#192a25",
    border_color_primary="#829285",
    input_background_fill="#e7e9dd",
    link_text_color="#236346",
    button_primary_background_fill="#236346",
    button_primary_text_color="#ffffff",
)
CSS = """
.zta-app {color-scheme: light;}
.zta-app h1, .zta-app h2, .zta-app h3 {font-family: Georgia, serif;}
.zta-kicker {letter-spacing: .08em; font-size: .8rem; color: #45594f;}
.zta-fixed {white-space: pre-wrap; font-family: var(--font-mono);
    background: #f6f2e9; border-left: 3px solid #236346; padding: .75rem 1rem; line-height: 1.65;}
"""


def boundary_text(state):
    return f"Phase: **{state['phase']}** · Desk: **{'ready' if state['enabled'] else 'paused'}**"


def pause_label(state):
    """The lesson names this control 'Pause desk'; it only becomes Resume once paused."""
    return "Pause desk" if state["enabled"] else "Resume desk"


def card_text(group):
    lines = []
    for task in desk.tasks(group):
        lines += [f"{task['id']} · {task['name']}", task["prompt"], "Expected: " + task["expected"], ""]
    return "\n".join(lines).strip()


def receipt_names():
    return [p.name for p in sorted(desk.LOCAL.glob("run-*.json"),
                                   key=lambda p: p.stat().st_mtime, reverse=True)]


def receipt_summary(name):
    if not name:
        return "Your first run will appear here.", ""
    try:
        result = desk.read_json(desk.LOCAL / name, {})
    except (ValueError, OSError):
        # One damaged receipt must not take the page down; the others still open.
        result = {}
    if not result:
        return f"{name} could not be read.", ""
    head = (f"{result['phase']} · {result['group']} · {result['status']}\n\n"
            "An exact-match flag is a clue. It misses hints, translations, invented values, and other "
            "unsafe replies. Grade every row yourself.")
    rows = []
    for row in result["rows"]:
        rows += [f"{row['id']} · {row['status']}",
                 "Visitor: " + row["input"],
                 row.get("answer", "No reply delivered."),
                 "Flags: " + ", ".join(row["flags"]), ""]
    return head, "\n".join(rows).strip()


def toggle_desk():
    state = desk.control()
    desk.change("pause" if state["enabled"] else "resume")


def apply_defenses():
    desk.change("lock")


def stream_run(group):
    """Rows are saved as they arrive, so a stopped run keeps everything already answered."""
    inbox = queue.Queue()

    def worker():
        try:
            with desk.client() as api:
                inbox.put(("done", desk.run(group, api, on_row=lambda row: inbox.put(("row", row)))))
        except (httpx.HTTPError, ValueError, OSError) as exc:
            inbox.put(("stopped", exc))

    threading.Thread(target=worker, daemon=True).start()
    lines = []
    while True:
        kind, value = inbox.get()
        if kind == "row":
            lines.append(f"{value['id']}: {value['answer']}")
            yield "Running locally. Completed replies are saved as they arrive.", "\n".join(lines)
        elif kind == "stopped":
            yield STOPPED, "\n".join(lines)
            return
        else:
            result = desk.read_json(value, {})
            yield result.get("status", "Run finished."), "\n".join(lines)
            return


def build():
    with gr.Blocks(theme=THEME, css=CSS, title="The Front Desk | Zero to Agent",
                   elem_classes="zta-app", analytics_enabled=False) as demo:
        tick = gr.State(0)
        gr.Markdown("ZERO TO AGENT · LEVEL 4 · TRAINING ONLY", elem_classes="zta-kicker")
        gr.Markdown("# The Front Desk\nBuild a desk, test its limits, then show what changed. Use the "
                    "supplied fictional messages. Every reply is a draft for a person to check.\n\n"
                    "> Local Ollama · gemma3:4b · No sending or booking tools")
        fatal = gr.Markdown("", visible=False)

        gr.Markdown("## 1. Set the boundary")
        boundary = gr.Markdown("")
        with gr.Row():
            pause_btn = gr.Button("Pause desk")
            lock_btn = gr.Button("Apply four defenses")
        gr.Markdown("Lock removes fake private values from new requests, marks visitor text, retains "
                    "draft-only access, and records controls. It cannot guarantee that every answer is "
                    "correct.\n\nDuring a long run, pause from a second terminal: "
                    "`uv run --frozen zta pause front-desk`. An in-flight calculation may finish; its "
                    "reply will be withheld.", elem_classes="zta-kicker")

        gr.Markdown("## 2. Write expected, then run")
        group = gr.Radio([g[0] for g in GROUPS], value=GROUPS[0][0], label="Practice set")
        with gr.Accordion("Read the test card before running", open=False):
            card = gr.Textbox(show_label=False, container=False, interactive=False, lines=18,
                              elem_classes="zta-fixed")
        run_btn = gr.Button("Run selected set", variant="primary")
        run_status = gr.Markdown("")
        run_log = gr.Textbox(label="Replies as they arrive", interactive=False, lines=8,
                             elem_classes="zta-fixed")

        gr.Markdown("## 3. Read the receipts")
        saved = gr.Dropdown([], label="Saved run", interactive=True)
        receipt_head = gr.Markdown("Your first run will appear here.")
        receipt_rows = gr.Textbox(show_label=False, container=False, interactive=False, lines=16,
                                  elem_classes="zta-fixed")
        receipt_file = gr.File(label="Download this run receipt", interactive=False)

        gr.Markdown("## 4. Make a message card")
        gr.Markdown("Use this supplied fictional request: River asks about an industrial document "
                    "project, this week, afternoons. The public follow-up route is "
                    "hello@celayasolutions.com. No reply time is promised.")
        gr.Textbox(CARD, show_label=False, container=False, interactive=False, lines=5,
                   elem_classes="zta-fixed")
        gr.Markdown("Complete your own worksheet in `.zta/front-desk/PROJECT-LAB-04.md`. Keep receipt "
                    "names, verdicts, your repair, and pitch there. Upload to Level 4 and reopen it, or "
                    "write “Not submitted.”")

        def value_for(label):
            return dict(GROUPS)[label]

        def refresh(chosen, label):
            """Re-read the desk from disk; a second terminal can pause it mid-class."""
            try:
                desk.prepare()
                state = desk.control()
            except (httpx.HTTPError, ValueError, OSError):
                return (gr.update(value=STOPPED, visible=True), "", gr.update(), gr.update(),
                        "", gr.update(), "", "", None)
            names = receipt_names()
            chosen = chosen if chosen in names else (names[0] if names else None)
            head, rows = receipt_summary(chosen)
            return (gr.update(visible=False), boundary_text(state),
                    gr.update(value=pause_label(state)),
                    gr.update(interactive=state["phase"] != "locked"),
                    card_text(value_for(label)),
                    gr.update(choices=names, value=chosen), head, rows,
                    str(desk.LOCAL / chosen) if chosen else None)

        outputs = [fatal, boundary, pause_btn, lock_btn, card, saved, receipt_head, receipt_rows,
                   receipt_file]

        def guarded(action):
            def wrapped(chosen, label):
                try:
                    action()
                except (httpx.HTTPError, ValueError, OSError) as exc:
                    raise gr.Error(str(exc)) from exc
                return refresh(chosen, label)
            return wrapped

        demo.load(refresh, [saved, group], outputs)
        pause_btn.click(guarded(toggle_desk), [saved, group], outputs)
        lock_btn.click(guarded(apply_defenses), [saved, group], outputs)
        group.change(refresh, [saved, group], outputs)
        saved.change(refresh, [saved, group], outputs)
        def run_selected(label):
            # This must stay a generator FUNCTION: a lambda returning the generator hands
            # Gradio one object instead of a stream, and no reply ever reaches the page.
            yield from stream_run(value_for(label))

        run_btn.click(run_selected, group, [run_status, run_log]).then(
            lambda label: refresh(None, label), group, outputs)
    return demo


def main():
    # A learner reads this terminal for the app URL. Library upgrade notices are not their business.
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    build().launch(server_name="127.0.0.1", server_port=8504, inbrowser=False,
                   show_api=False, quiet=True)


if __name__ == "__main__":
    main()
