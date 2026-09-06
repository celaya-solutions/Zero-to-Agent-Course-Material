# Level 4 Preparation - The Front Desk

```text
Document:    Level 4 Preparation - The Front Desk
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      fbee5efe166fa3b5e658323a1330978e97bb07c354315f44638262a0e1812e2b
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Prepare before the 90-minute meeting. Each learner needs their own Ollama-capable computer. Reuse the course fork, Python environment, and Ollama from Levels 1-3. A phone can read the packet but does not replace the prepared computer. Saved examples support an outage; they do not prove that a phone ran the lab.

## Tools and downloads

Use the [course repository](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material), [Ollama download](https://ollama.com/download), and [Gemma 3 library page](https://ollama.com/library/gemma3). See [Mac setup](../../../preparation/macos.md) or [Windows setup](../../../preparation/windows.md) if starting fresh. Use the instructor's reviewed course candidate: unpublished local changes are not yet available from the public main branch.

No new API key, subscription, cloud model, or hosting account is needed. Use local gemma3:4b for both phases. Download size and runtime vary; check the model page and Level 3 preparation. Do not start a large download during class. If the computer cannot complete a set in its class block, use the saved packet.

## From the course folder

Open the cloned course folder in GitHub Desktop, then open its terminal. Run one line at a time; these commands work on the prepared Mac and Windows routes.

```sh
uv sync --frozen
ollama pull gemma3:4b
uv run --frozen zta prepare front-desk
uv run --frozen zta doctor front-desk
uv run --frozen zta test front-desk
uv run --frozen zta start front-desk
```

Pull downloads only if needed; do it during preparation. Open [the local desk](http://127.0.0.1:8504). The terminal stays open. Doctor should name the local model and digest; it does not generate an answer. Tests use fake responses; the five callers check real generation. Stop the browser server with Ctrl+C.

Prepare creates only the private Level 4 instructions, worksheet, and control file. It preserves existing edits, receipts, and phase. Data stays in ignored .zta/front-desk/. The desk does not read the Level 1 provider configuration or keys, does not upload files, and does not fall back to a cloud model.

## Readiness check

Open the desk and the [caller card](assets/caller-card.md). Run Five callers before class; confirm replies and a saved run. Keep the receipt as preparation evidence. The first source rule is weak on purpose. A refusal, missing citation, or honest model error is useful evidence, not a reason to invent a pass.

If Ollama is missing, open its app and rerun doctor. If a model is missing, run the supplied pull command during preparation. After two attempts or five minutes, switch to the [saved callers](assets/fallback-caller-run.md) and [saved attacks](assets/fallback-before-after.md). Keep earlier failed receipts.

## Pause and recovery

Click Pause desk when idle. During a run, open a second terminal in this same course folder and run `uv run --frozen zta pause front-desk`. Run a set while paused: its new receipt must say paused and have zero rows. Resume with `uv run --frozen zta resume front-desk`. A request already sent may finish computing; the program withholds that reply and sends no next request. Ctrl+C ends the current terminal process, while the pause setting survives a restart.

Only one run can use a desk folder at a time. If the process crashed and a new run reports it is still active, first close every Front Desk terminal and tab. Keep all run receipts. Then remove only .zta/front-desk/running.lock in the file manager. Ask the instructor if unsure. Never delete the whole private folder to clear an error.

Lock is one-way for this lesson. It prevents accidentally adding the bait again. If you locked before saving Before, keep that fact and use the labeled saved Before set; do not rewrite a receipt. Review the frozen prompts and model digest before claiming a matched comparison.
