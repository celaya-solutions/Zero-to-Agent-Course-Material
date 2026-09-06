# Course Repository Instructions

```text
Document:    Course Repository Instructions
Version:     v1.5.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      35c56abaef6394fb4a40c4227df373af3aea7b9108ac8d47873b7658d2ed9832
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

This repository is the canonical authoring home for five 90-minute levels. Teaching files stay under `courses/project-lab/level-01` through `level-05`; runnable applications stay under `projects/`. The website and private platform consume generated copies.

## Next maintainer task

Execute [the release and learner-verification handoff](release/next-section.md): publish matching course downloads, deploy the website and private course update, and complete the real learner/setup/upload/schedule/stop checks. Levels 4-5 are already merged locally. The user's 2026-09-06 direction authorizes this scoped follow-through; older no-release notes describe earlier turns. Exclude all new Spanish work and Spanish delivery pilots; preserve existing text. Record actual results and specific external blockers rather than asking again for the same release permission.

## Work rules

Use an isolated `codex/` branch/worktree. Keep changes small and commit completed work. The active release handoff records the user-directed integration/publication/deployment scope; unrelated merges or deployments still need a direct instruction. If graft is available, use its context graph before searching source. Graft is an optional maintainer tool, not a learner prerequisite.

For a Level 1 learner edit, read `courses/project-lab/level-01/manual-edit.md`. Explain the likely cause before changing one rule or retrieval setting. Preserve supplied documents, expected results, tests, provider selection, local-only binding, and evidence privacy. Do not publish on the learner's behalf.

Keys, imported files, indexes, progress, and learner exports belong only in ignored local storage. Never read or include a learner key in a prompt, commit, screenshot, log, or answer. Do not add automatic cloud switching or paid retries.

For a Level 2 learner exercise, read `courses/project-lab/level-02/manual-edit.md`. The bounded edit changes only unrelated practice-page text; preserve the marked status, workflow, tests, state, and expectations. Never enable workflows, create issues, or publish on the learner's behalf without their explicit request.

For a Level 3 learner edit, follow `courses/project-lab/level-03/manual-edit.md`. Only the private `.zta/local-models/Modelfile` is authorized for the one-rule edit; all other private files remain out of scope. Preserve the local base, endpoint, tests, prompts, settings, and before receipts. The learner judges both after answers.

For a Level 4 learner edit, follow `courses/project-lab/level-04/manual-edit.md`. Open only `.zta/front-desk/desk-instructions.md` for the one Source rule; do not read other private state, keys, or receipts. Preserve fixed tests, public records, model, endpoint, logs, controls, and earlier proof. The learner runs C1/C2 again and judges the replies.

For Level 5, reuse one earlier tested change using courses/project-lab/level-05/manual-edit.md. Keep private proof in .zta/showcase/PROJECT-LAB-05.md. Do not read or rewrite learner receipts, create fake results, reset locks/state, or publish. Authored examples cannot close personal live gates.

## Validation and documentation

Run `uv run --frozen zta test documents`, `uv run --frozen zta test watchman`, `uv run --frozen zta test local-models`, and `uv run --frozen zta test front-desk`. Refresh the legacy workflow with `uv run --frozen python scripts/sync_watchman_starter.py`. After a course edit, update document hashes, regenerate slides and PDFs, run `LANG=en_US.UTF-8 ruby scripts/validate_project_lab.rb`, then `uv run --frozen python scripts/validate_materials.py`. See `release/maintaining.md` for exact commands.

Every new document receives the standard metadata header. Canonical content is the UTF-8 text below that header, with leading/trailing blank space removed and one final newline; SHA256 covers those bytes. Preserve existing licenses and source attribution. Recheck public facts and provider prices before class. Saved examples are authored examples, never live test proof.

Summaries use plain language and describe verified results. Unperformed device, cloud, and authenticated upload pilots remain open release gates. Do not infer classroom readiness from unit tests.

## Change notes

- 2026-09-06: Committed instructions for publication, website/private-course deployment, and real learner/control verification as the next agent task; Spanish work is excluded. The earlier Level 4-5 merges are complete.


- 2026-09-06: Committed Level 5's final proof board, project-specific checks, cost examples, accessible presentation routes, full handouts, and 20 slides. All 116 project tests and course/render/package checks pass; classroom gates are in release/level-05-verification.md. Source and consumers remain isolated; no merge or deployment.


- 2026-09-06: Committed Level 4 local desk, full learner/teacher pack, fixed caller/attack sets, source-rule retests, private log and pause control. All 116 project tests plus live model, browser, slides, and PDF checks pass; remaining classroom gates and actual model failures are recorded in release/level-04-verification.md. No merge or deployment was performed.

- 2026-09-06: Completed and committed Level 3 local lab, six-row comparison, named-rule retests, and the learner/teacher pack. All 96 project tests and course/render checks pass; the committed Level 3 suite is included in the Windows/Mac CI matrix; actual model failures and open device/network/upload pilots are recorded in release/level-03-verification.md.


- 2026-09-06: Built the maintained Level 2 watcher, failure/recovery checks, full learner/teacher pack, and candidate downloads; 79 app checks, fresh-clone installation, and document/slide/PDF review pass locally. Hosted, device, schedule, and student-upload gates remain in release/level-02-verification.md.

- 2026-09-06: Built the Level 1 release candidate and five-level teaching pack, then fixed readability across the app. All 36 app checks and browser contrast checks pass; remaining classroom pilots are recorded in `release/verification.md`.
- 2026-09-06: Updated both assistant entry files and added the Level 2 continuation handoff, including unpublished fixes and separate integration boundaries.
