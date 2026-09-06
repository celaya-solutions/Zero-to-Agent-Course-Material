# Level 2 Assistant and Manual Card

```text
Document:    Level 2 Assistant and Manual Card
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      420eca03033235ddac0490900704202aa988b5ff4545324b85189761d8cb47f3
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Complete the main lesson first. This optional exercise shows that changing unrelated page text does not deserve an alert. It changes a supplied synthetic page, makes no external request, and needs no model or paid API. Use a separate local rehearsal from hosted proof.

## Common starting point

Open the same clone in GitHub Desktop; fetch/pull so local page edits are current. Open its root terminal using the Level 2 preparation card. Run `uv run --frozen zta test watchman`. Close any other local rehearsal terminal before continuing.

Open the supplied practice page in your editor. It may say PAUSED after class; either valid status is fine. Do not change `watch-value` or reset any state. Write your expected local decision before running:

```sh
uv run --frozen zta start watchman
```

This makes one local round and exits. The first local run may save a baseline. Run it again after predicting `no change`. Receipts appear in `.zta/watchman/rounds.jsonl`. These are **LOCAL REHEARSAL**, not a GitHub issue, hosted run, or scheduled job.

## Claude Code route

Reuse your installed Claude Code and sign-in from [shared assistant preparation](../../../preparation/coding-assistants.md). In the root terminal open `claude`, then send the bounded prompt below. Do not attach `.zta/`; paste only the safe local decision and a copy of the public footer sentence.

## Codex route

Reuse Codex from shared preparation. Open this course clone and send the same prompt in a task. Verify the selected folder before accepting any change. Follow the assistant's repository rules for a review branch/worktree and do not authorize publication.

## Bounded prompt for either assistant

> Read AGENTS.md, the Level 2 manual card, and projects/watchman/README.md. Explain why editing the paragraph after the marked status should leave the signal unchanged. Change only that paragraph in courses/project-lab/level-02/assets/practice-page.html by adding the sentence "Footer wording changed for the quiet-alert test." Preserve the watch-value element, current status, tests, watcher code, workflow permissions, state, and expected result. Do not read .zta/, send requests, create issues, enable workflows, or publish. Show the one-file diff and the local test and rehearsal commands. My prediction is that the marked value stays the same and the next completed local round says no change.

**Expected result:** One paragraph edit and an explanation. **Recovery:** Reject edits to the parser, signal, workflow, or private data. Use the manual route if access or limits block the assistant. No assistant subscription is required for this exercise.

## Manual route

**Where:** Your text editor. **Action:** Open `courses/project-lab/level-02/assets/practice-page.html`. Find the paragraph after the status line and append `Footer wording changed for the quiet-alert test.` before that paragraph's closing `</p>`. Save in UTF-8 with the `.html` extension unchanged.

**Why:** This is a controlled irrelevant change. **Expected result:** Only one paragraph changes; OPEN/PAUSED and `id="watch-value"` are untouched. **Recovery:** Review Desktop's diff. Undo only your paragraph edit if the file type or signal was changed; preserve unrelated edits.

## Check the same prediction

Save the before receipt and your prediction time in the private worksheet, then run:

```sh
uv run --frozen zta test watchman
uv run --frozen zta start watchman
```

Expected: tests pass; `decision: no change`; same previous/current value; no new local alert file. Record the after receipt and explain why the footer is ignored. If it fails, read the safe error and preserve the local state. Do not ask an assistant to rewrite expected results to fit the output.

Each command starts a fresh process, so there is no app server to restart. Review and commit the page edit on your own learner branch only if you want to keep it; publishing is your action. Keep the hosted workflow disabled. This extension cannot replace the lesson's actual issue or off-switch proof.
