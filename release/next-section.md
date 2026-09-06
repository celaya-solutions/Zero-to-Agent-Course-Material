# Continue the Level 2 Candidate

```text
Document:    Continue the Level 2 Candidate
Version:     v1.1.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      c9e1319c5c2c032d3e25a843fcb6c9532de0b49b036aa65d9952d2ebc97784f6
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

## Current work

Level 2: The Night Watchman is implemented on isolated branch `codex/level-2-night-watchman` in sibling worktree `Zero-to-Agent-Level-02`. This branch starts from the Level 1 handoff at `1c50b67`, preserving its unpublished readability fixes. Do not start from stale local main or the older published v1.0.0-rc.1 tag.

Read [Level 2 verification](level-02-verification.md) for actual test evidence and open gates. The [learner lesson](../courses/project-lab/level-02/student.md), [preparation](../courses/project-lab/level-02/preparation.md), and [project map](../projects/watchman/README.md) are the next review entry points. All five levels remain 90 minutes.

## Continue in this order

1. Inspect branch/worktree status and preserve unrelated work. Start a new isolated worktree from this branch's current tip if making a new coding change. Install its own locked environment; do not symlink `.venv`.
2. Finish any explicitly approved hosted pilot in the designated public practice repository. The canonical course repository is blocked by the watcher and must not get an installed active workflow. Obtain the exact repository approval before creating issues or enabling scheduled work.
3. Follow the learner route: baseline OPEN, unchanged OPEN, change to PAUSED, repeat unchanged, one useful issue, state, logs/artifact, then disable/false variable/cancel outstanding work. Observe an actual daily scheduled event separately before claiming scheduled execution tested. A manual job or local fixture is not that evidence.
4. Finish fresh Windows/Mac learner setup, each assistant edit path, and a test-student Level 2 upload/reopen. Keep credentials and student evidence private. Existing Level 1 live gates remain in [its verification record](verification.md).
5. Before a separately requested release, rebuild from canonical source, rerun checks, refresh the separate consumer branches, inspect source/download links, and publish a new version. Never rewrite the existing Level 1 tag or merge/deploy as cleanup.

## Build and validation commands

From the canonical root:

```sh
uv sync --frozen
uv run --frozen zta test documents
uv run --frozen zta test watchman
uv run --frozen python scripts/sync_watchman_starter.py
uv run --frozen python scripts/update_headers.py
ruby scripts/build_project_lab_slides.rb
uv run --frozen python scripts/build_pdfs.py
LANG=en_US.UTF-8 ruby scripts/validate_project_lab.rb
uv run --frozen python scripts/validate_materials.py
uv run --frozen python scripts/package_release.py
```

The two old starter Python files are compatibility entry points, not a second implementation. Update the maintained watcher under `projects/watchman/`; regenerate the old workflow copy after template changes. Do not delete `.watch-state` or clear a pending send flag to force a passing demonstration. Uncertain delivery intentionally stops until a human can establish the result.

## Consumer boundaries

Website updates belong in the separate `course-material-site-level02` review checkout on `codex/course-material-level02`, based on the prior Level 1 website review branch. Private Rails updates belong in `course-material-platform-level02` on `codex/course-material-level02`, based on its prior canonical-source review branch. Verify these actual states before reusing them; final results are recorded in their agent notes.

Use the existing exporter and guarded `zta:sync_content` / `zta:check_content` tasks. The Rails source, database, and student submissions must never be copied into public course source. Keep the original website main, live service, private runtime configuration, and earlier review worktrees intact.

## Stopping point

This task prepares a review candidate, not automatic permission to publish or deploy. Keep unperformed hosted/device/schedule/student pilots explicit. Do not begin Level 3, revive retired curricula, or change the alternative-project catalog without a new instruction.
