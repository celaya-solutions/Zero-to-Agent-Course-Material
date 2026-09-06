# Course Repository Instructions

```text
Document:    Course Repository Instructions
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      bd623a5a3879f601ce6e25b065e9725f5181081e97e9dc1ef6fd156fc8be7a17
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

This repository is the canonical authoring home for five 90-minute levels. Teaching files stay under `courses/project-lab/level-01` through `level-05`; runnable applications stay under `projects/`. The website and private platform consume generated copies.

## Work rules

Use an isolated `codex/` branch/worktree. Keep changes small and commit completed work; do not merge or deploy without a direct instruction. If graft is available, use its context graph before searching source. Graft is an optional maintainer tool, not a learner prerequisite.

Read `courses/project-lab/level-01/manual-edit.md` before a learner edit. Explain the likely cause before changing one rule or retrieval setting. Preserve supplied documents, expected results, tests, provider selection, local-only binding, and evidence privacy. Do not publish on the learner's behalf.

Keys, imported files, indexes, progress, and learner exports belong only in ignored local storage. Never read or include a learner key in a prompt, commit, screenshot, log, or answer. Do not add automatic cloud switching or paid retries.

## Validation and documentation

Run `uv run --frozen zta test documents`. After a course edit, update document hashes, regenerate slides and PDFs, run `LANG=en_US.UTF-8 ruby scripts/validate_project_lab.rb`, then `uv run --frozen python scripts/validate_materials.py`. See `release/maintaining.md` for exact commands.

Every new document receives the standard metadata header. Canonical content is the UTF-8 text below that header, with leading/trailing blank space removed and one final newline; SHA256 covers those bytes. Preserve existing licenses and source attribution. Recheck public facts and provider prices before class. Saved examples are authored examples, never live test proof.

Summaries use plain language and describe verified results. Unperformed device, cloud, and authenticated upload pilots remain open release gates. Do not infer classroom readiness from unit tests.

## Change notes

- 2026-09-06: Added and committed the Level 1 starter and five-level teaching pack. Browser review confirmed source checks, the controlled improvement, private export, and persistence; added a fixed light theme and bounded CI diagnostics. Device, cloud, and authenticated-student gates are tracked in `release/verification.md`.
