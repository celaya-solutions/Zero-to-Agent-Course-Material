# Course Repository Instructions

```text
Document:    Course Repository Instructions
Version:     v1.1.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      a03102e2bdc91288403bdb0f1d44f81a19a9ab1e551739fbbc5e5911b20e6a4f
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

This repository is the canonical authoring home for five 90-minute levels. Teaching files stay under `courses/project-lab/level-01` through `level-05`; runnable applications stay under `projects/`. The website and private platform consume generated copies.

## Next maintainer task

Continue from the merged Level 3 source. Read [the handoff](release/next-section.md) and [Level 3 verification](release/level-03-verification.md). Begin Level 4 or publish only under a new instruction. Preserve earlier live gates.

## Work rules

Use an isolated `codex/` branch/worktree. Keep changes small and commit completed work; do not merge or deploy without a direct instruction. If graft is available, use its context graph before searching source. Graft is an optional maintainer tool, not a learner prerequisite.

For a Level 1 learner edit, read `courses/project-lab/level-01/manual-edit.md`. Explain the likely cause before changing one rule or retrieval setting. Preserve supplied documents, expected results, tests, provider selection, local-only binding, and evidence privacy. Do not publish on the learner's behalf.

Keys, imported files, indexes, progress, and learner exports belong only in ignored local storage. Never read or include a learner key in a prompt, commit, screenshot, log, or answer. Do not add automatic cloud switching or paid retries.

For a Level 2 learner exercise, read `courses/project-lab/level-02/manual-edit.md`. The bounded edit changes only unrelated practice-page text; preserve the marked status, workflow, tests, state, and expectations. Never enable workflows, create issues, or publish on the learner's behalf without their explicit request.

For a Level 3 learner edit, follow `courses/project-lab/level-03/manual-edit.md`. Only the private `.zta/local-models/Modelfile` is authorized for the one-rule edit; all other private files remain out of scope. Preserve the local base, endpoint, tests, prompts, settings, and before receipts. The learner judges both after answers.

## Validation and documentation

Run `uv run --frozen zta test documents`, `uv run --frozen zta test watchman`, and `uv run --frozen zta test local-models`. Refresh the legacy workflow with `uv run --frozen python scripts/sync_watchman_starter.py`. After a course edit, update document hashes, regenerate slides and PDFs, run `LANG=en_US.UTF-8 ruby scripts/validate_project_lab.rb`, then `uv run --frozen python scripts/validate_materials.py`. See `release/maintaining.md` for exact commands.

Every new document receives the standard metadata header. Canonical content is the UTF-8 text below that header, with leading/trailing blank space removed and one final newline; SHA256 covers those bytes. Preserve existing licenses and source attribution. Recheck public facts and provider prices before class. Saved examples are authored examples, never live test proof.

Summaries use plain language and describe verified results. Unperformed device, cloud, and authenticated upload pilots remain open release gates. Do not infer classroom readiness from unit tests.

## Change notes

- 2026-09-06: Completed and committed Level 3 local lab, six-row comparison, named-rule retests, and the learner/teacher pack. All 96 project tests and course/render checks pass; actual model failures and open device/network/upload pilots are recorded in release/level-03-verification.md.


- 2026-09-06: Built the maintained Level 2 watcher, failure/recovery checks, full learner/teacher pack, and candidate downloads; 79 app checks, fresh-clone installation, and document/slide/PDF review pass locally. Hosted, device, schedule, and student-upload gates remain in release/level-02-verification.md.

- 2026-09-06: Built the Level 1 release candidate and five-level teaching pack, then fixed readability across the app. All 36 app checks and browser contrast checks pass; remaining classroom pilots are recorded in `release/verification.md`.
- 2026-09-06: Updated both assistant entry files and added the Level 2 continuation handoff, including unpublished fixes and separate integration boundaries.
