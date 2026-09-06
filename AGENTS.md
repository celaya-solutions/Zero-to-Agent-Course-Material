# Course Repository Instructions

```text
Document:    Course Repository Instructions
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      488517c4f323afeceb7c2ab51cdcf18533de6cf76b571e6eee38f72578616e01
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

- 2026-09-06: Added the custom Level 1 app, shared setup guides, source exercises, teaching pack, locked runtime, and release checks. Migrated the five active levels; retained later project scope and license notices.
