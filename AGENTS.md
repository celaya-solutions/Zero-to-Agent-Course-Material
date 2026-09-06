# Course Repository Instructions

```text
Document:    Course Repository Instructions
Version:     v1.0.3
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      e5f276218b2bbdac1f1b684bc3ffecd1835103cc91f82a49847ea4ab9eb7cc80
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

- 2026-09-06: Added and committed the Level 1 starter and five-level teaching pack. Browser review confirmed source checks, the controlled improvement, private export, and persistence; added a fixed light theme and bounded CI diagnostics with short test-case labels and explicit UTF-8 reads for Windows. Windows and Mac hosted checks pass. Physical-device, cloud, and authenticated-student gates are tracked in `release/verification.md`.

- 2026-09-06: Removed fixed app colors that mixed pale backgrounds with dark-mode white text. Verified sidebar, tabs, and upload controls in light and dark browser previews; all 36 app checks pass.

- 2026-09-06: Added explicit paired colors for course tabs and the upload label, including nested text. Browser checks at 874 x 1087 measured 13.43:1 text contrast and 6.38:1 on the active tab; all 36 app checks pass.

- 2026-09-06: Unified the fixed course palette across passage cards, labels, controls, menus, alerts, and code; increased passage spacing. All five screens passed browser contrast checks with light and dark defaults (minimum checked text 6.12:1, passages 13.43:1), with source cards reviewed at 887 x 1087; all 36 app checks pass.
