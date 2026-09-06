# Zero to Agent - Course Material

```text
Document:    Zero to Agent - Course Material
Version:     v1.4.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      4e3bb672d1b8a7a2346c0811971151808d876b0722f1abb9f7ba0fd7d3fb5f2e
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Five 90-minute meetings. Four projects. One final presentation. Beginners start from a working application, inspect its evidence, make one change, and show the result.

## Start here

1. Open [Preparation](preparation/README.md). Choose [Windows](preparation/windows.md) or [Mac](preparation/macos.md), then one coding assistant and one answer engine. This catches account and installation problems before class.
2. Open [Level 1](courses/project-lab/level-01/student.md). Follow its numbered steps. Each names the action, reason, expected result, and recovery route.
3. Keep [the manual edit card](courses/project-lab/level-01/manual-edit.md) and [saved examples](courses/project-lab/level-01/assets/fallback-grounded-run.md) available offline.
4. [Sign in to the course](https://learn.zerotoagent.org/auth/users/sign_in) before class and confirm you can open Level 1's upload form.

## Run the document helper

From this repository's root, after installing uv:

```sh
uv sync --frozen
uv run --frozen zta setup
uv run --frozen zta doctor documents
uv run --frozen zta start documents
```

Open http://127.0.0.1:8501. Keep the terminal open. Stop with Ctrl+C. Python and package versions come from the included lockfile. The app does not install a cloud key or model for you; [model setup](preparation/models.md) explains both paths.

## Course map

| Level | Project | Proof |
| --- | --- | --- |
| [1 - Your Documents Answer Back](courses/project-lab/level-01/student.md) | [Document helper](projects/documents/README.md) | Five tests, source checks, change, private submission |
| [2 - The Night Watchman](courses/project-lab/level-02/student.md) | [Page watcher](projects/watchman/README.md) | Baseline, unchanged, changed, off switch |
| [3 - Nothing Leaves the Building](courses/project-lab/level-03/student.md) | [Local model lab](projects/local-models/README.md) | Observed offline result or labeled fallback, six rows, named-rule retest |
| [4 - The Front Desk, Attacked and Locked](courses/project-lab/level-04/student.md) | [Local front desk](projects/front-desk/README.md) | Five callers, one edit, fixed attacks, four defenses, log and pause |
| [5 - Choose, Improve, and Present](courses/project-lab/level-05/student.md) | An earlier project | Improved outcome, cost, presentation |

Level 2 now has a maintained watcher and full [preparation guide](courses/project-lab/level-02/preparation.md). Levels 3 and 4 have maintained local labs and full preparation guides; both reuse earlier setup. Level 5 has a full [preparation guide](courses/project-lab/level-05/preparation.md), eight-item proof board, project-specific final checks, worked cost sheet, and labeled presentation fallback. The alternative-project catalog remains on [the course website](https://zerotoagent.org/course/catalog.html); it is not a second required course.

## Downloads and status

Download the versioned learner and instructor ZIP files from [Releases](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material/releases). Each includes PDFs and offline instructions. Learner code comes from your fork; a materials ZIP is not a Git working copy.

The published Level 1 package remains **v1.0.0-rc.1**. The current Level 5 work is a local **v1.4.0-rc.1 review candidate**, including Levels 1-4; see [Level 5 verification](release/level-05-verification.md). Use its matching complete course checkout, not an older download. A merge does not publish the tag or its downloads. Earlier classroom gates remain in their verification records.

## What goes where

- `courses/project-lab/`: canonical five-level teaching source and generated handouts.
- `preparation/`: shared installation, account, model, and recovery guides.
- `projects/documents/`: the custom app, editable settings, and deterministic tests.
- `projects/watchman/`: the scheduled watcher, local rehearsal, workflow template, and tests.
- `.zta/`: private credentials, imported files, search index, and evidence. Git ignores it.
- `scripts/`: course builds, validation, releases, and export to the website or private platform.

Never put keys, private documents, learner evidence, or private platform source in this public repository. The app is a local single-user teaching tool. It has no public-host authentication layer.

## Maintain and publish

Run `uv run --frozen zta test documents`, `uv run --frozen zta test watchman`, and `uv run --frozen python scripts/validate_materials.py`. Build PDFs and slides with the commands in [Maintaining the course](release/maintaining.md). Commit a reviewed branch; merges and live deployments are separate actions.

Questions and access blocks: hello@celayasolutions.com. Share the command and error category, never an API key or private file. Code inherited from the existing course retains its MIT notice in LICENSE; third-party applications and model weights retain their own licenses. New course documents carry the required Celaya Solutions header.
