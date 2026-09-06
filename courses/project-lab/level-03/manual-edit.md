# Level 3 One-Rule Edit

```text
Document:    Level 3 One-Rule Edit
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      61721cfd0e3be026bececf1de80086257bf6304efb2a67a7f39ed72fd3b7dfee
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Goal: make the same workbench reminder easier to read, without losing its deadline or request for a reply. Complete a before run first. A named rule set is not training and is not guaranteed to control the model.

## Manual route

1. Run `uv run --frozen zta prepare local-models` once. Create and check the original rules using the command card. Save both before answers.
2. In the editor, open `.zta/local-models/Modelfile`. Do not open a file called `Modelfile.txt` or the shared template by mistake.
3. Predict: exactly two short sentences should keep the reminder concise.
4. Replace only `Write one polite paragraph under 70 words.` with `Write exactly two short sentences under 50 words total. The first must keep the deadline; the second must ask the reader to reply when ready.`
5. Save. Preserve FROM, all other rules, temperature, context, output limit, supplied prompts, code, tests, and earlier receipts.
6. Run `uv run --frozen zta create local-models`, then `uv run --frozen zta check local-models`.
7. Compare the same normal and missing-information tests. Did it use two sentences, keep 4 p.m. and the reply request, and still stop on missing price/date? Record a failure if not. Keep all attempts.

## Claude Code or Codex route

Use the assistant setup you already completed in the [coding-assistant guide](../../../preparation/coding-assistants.md). Run the assistant online before/after the offline task. The assistant's own service is separate from the local model lab.

Give it this bounded request:

> Explain why the reminder may be too long. Edit only `.zta/local-models/Modelfile`: replace `Write one polite paragraph under 70 words.` with `Write exactly two short sentences under 50 words total. The first must keep the deadline; the second must ask the reader to reply when ready.` Preserve every other line, the base model, supplied prompts, tests, and earlier evidence. Do not open any other `.zta/` file, read keys, change provider settings, or publish. Show the one-line diff and the create/check commands. I will run them and judge both outputs.

Only the named Modelfile is in scope; the rest of `.zta/` stays private. If an assistant cannot access that ignored file, use the manual route. Do not weaken ignore rules or paste receipts into a prompt to get past that boundary.

## Stop and undo

If the new rule makes the result worse, restore the original sentence, create again, and retest. Record why. This edits a local private file; no public commit or remote model publication is needed.
