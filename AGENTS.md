# Course Repository Instructions

```text
Document:    Course Repository Instructions
Version:     v1.0.4
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      7a76e263ac965b8d8dc7753a480a5ca0eded0ec1aae2e68ce7712dd512b76ea8
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

This repository is the canonical authoring home for five 90-minute levels. Teaching files stay under `courses/project-lab/level-01` through `level-05`; runnable applications stay under `projects/`. The website and private platform consume generated copies.

## Next maintainer task

Continue with **Level 2: The Night Watchman**. Read [the continuation handoff](release/next-section.md) before planning or editing. It records the exact starting branch, unpublished Level 1 fixes, existing Level 2 assets, required outcomes, review worktrees, and open release gates. Start the next isolated worktree from this branch's current tip so the local readability fixes are retained. These maintainer instructions do not expand a learner's bounded edit.

## Work rules

Use an isolated `codex/` branch/worktree. Keep changes small and commit completed work; do not merge or deploy without a direct instruction. If graft is available, use its context graph before searching source. Graft is an optional maintainer tool, not a learner prerequisite.

For a Level 1 learner edit, read `courses/project-lab/level-01/manual-edit.md`. Explain the likely cause before changing one rule or retrieval setting. Preserve supplied documents, expected results, tests, provider selection, local-only binding, and evidence privacy. Do not publish on the learner's behalf.

Keys, imported files, indexes, progress, and learner exports belong only in ignored local storage. Never read or include a learner key in a prompt, commit, screenshot, log, or answer. Do not add automatic cloud switching or paid retries.

## Validation and documentation

Run `uv run --frozen zta test documents`. After a course edit, update document hashes, regenerate slides and PDFs, run `LANG=en_US.UTF-8 ruby scripts/validate_project_lab.rb`, then `uv run --frozen python scripts/validate_materials.py`. See `release/maintaining.md` for exact commands.

Every new document receives the standard metadata header. Canonical content is the UTF-8 text below that header, with leading/trailing blank space removed and one final newline; SHA256 covers those bytes. Preserve existing licenses and source attribution. Recheck public facts and provider prices before class. Saved examples are authored examples, never live test proof.

Summaries use plain language and describe verified results. Unperformed device, cloud, and authenticated upload pilots remain open release gates. Do not infer classroom readiness from unit tests.

## Change notes

- 2026-09-06: Built the Level 1 release candidate and five-level teaching pack, then fixed readability across the app. All 36 app checks and browser contrast checks pass; remaining classroom pilots are recorded in `release/verification.md`.
- 2026-09-06: Updated both assistant entry files and added the Level 2 continuation handoff, including unpublished fixes and separate integration boundaries.
