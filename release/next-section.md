# Continue After Level 3

```text
Document:    Continue After Level 3
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      746c915bd1baea0fb8c09d4a7566da951ad2096fb8d9339970f9218382ae79a4
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Level 3: Nothing Leaves the Building has a maintained local lab and full teaching package. Start from the merged canonical main after verifying its branch status, and preserve Level 1/2 fixes. Read [Level 3 verification](level-03-verification.md) for measured results and unperformed classroom pilots.

## Authoring and checks

Use a new isolated codex worktree. Edit canonical course source first. Run the three project suites: `uv run --frozen zta test documents`, `uv run --frozen zta test watchman`, and `uv run --frozen zta test local-models`. Refresh headers, slides, and PDFs, then run both material validators and build the versioned download package.

Level 3 learner edits may access only `.zta/local-models/Modelfile` under the exact manual-card scope. Do not read other learner state or keys. Keep the two supplied models, local endpoint, prompts, limits, and prior receipts intact. Named rules are not fine-tuning or enforced security.

## Next work

Begin Level 4 only under a new instruction. Before a classroom/public release, finish the open device, observed-offline, assistant-route, and student-upload pilots. Preserve older Level 1 and Level 2 gates, including the exact approved repository requirement for hosted Watchman work. A manual job does not prove a daily scheduled tick.

## Generated consumers

Use `scripts/export_course.py` for the separate website checkout and guarded `zta:sync_content` / `zta:check_content` for the separate private platform. Never copy Rails source, database, keys, or student submissions into public course source. Do not seed/reset courses during a content export. Keep website and private main status, source receipts, and deployment state distinct.

The current instruction authorizes merging the finished Level 3 work and its prerequisite course copies. Public push, release publication, deployment, and live student-data changes remain separate actions. Package/source links marked v1.2.0-rc.1 need that actual release before they are advertised as public downloads.
