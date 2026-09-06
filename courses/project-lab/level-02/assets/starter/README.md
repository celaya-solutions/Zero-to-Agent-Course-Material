# Night Watchman Starter Map

```text
Document:    Night Watchman Starter Map
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      0255e75b6cf48120456bd96773e96061a956d0b7c8c6b99bcf7ba25137e0fb67
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Use the same complete learner course fork as Level 1. Do not create a second repository or place Python files at its root.

The maintained project is [projects/watchman](../../../../../projects/watchman/README.md). Follow [Level 2 preparation](../../preparation.md) for exact Windows/Mac folder, installation, GitHub controls, and recovery steps. Run these from the course root:

```sh
uv run --frozen zta doctor watchman
uv run --frozen zta test watchman
uv run --frozen zta prepare watchman
```

The last command copies the canonical workflow template to `.github/workflows/watchman.yml` and creates ignored `.zta/PROJECT-LAB-02.md`, keeping existing files. It does not publish or enable anything. Review and commit only the workflow to your own default branch. Enable the job deliberately during the lesson, then leave it disabled with WATCHMAN_ENABLED=false and no active/queued run.

`watch.py` and `test_watch.py` in this legacy folder are small compatibility entry points that require the complete clone. Edit and test the maintained project, not these wrappers. `watch.yml` is a generated copy of `projects/watchman/workflow.template.yml`; maintainers refresh it with `scripts/sync_watchman_starter.py`.

The same supplied practice page stays at `courses/project-lab/level-02/assets/practice-page.html`. Class checks are baseline OPEN, unchanged OPEN, controlled PAUSED change, repeat PAUSED, and the off switch. One same-fork practice issue is allowed; no posting elsewhere. The daily schedule is 13:17 UTC and may be delayed or dropped. Use new manual runs for the classroom test.
