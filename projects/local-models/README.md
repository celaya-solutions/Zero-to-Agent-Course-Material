# Local Model Lab Project

```text
Document:    Local Model Lab Project
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      7f04424be83e22fb21c785441ba809fdf122606087f404db990327895023bd8e
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

This is the maintained Level 3 helper. Read the [lesson](../../courses/project-lab/level-03/student.md) and [preparation](../../courses/project-lab/level-03/preparation.md) first. It uses the course's existing locked Python environment and Ollama, with no new account or API key.

| Part | Purpose |
| --- | --- |
| `lab.py` | Fixed loopback calls, model identity checks, timed runs, private receipts, named model creation |
| `tests/` | Deterministic safety/recovery checks; no real generation |
| `courses/project-lab/level-03/assets/prompts.json` | The same writing/source/arithmetic prompts and missing-information test |
| `courses/project-lab/level-03/assets/Modelfile.template` | Starting rules copied into the learner's private folder |
| `.zta/local-models/` | Ignored private worksheet, editable Modelfile, and separate receipts for each attempt |

From the course root, use `uv run --frozen zta prepare local-models`, `doctor`, `offline`, `benchmark`, `create`, `check`, or `test` in the same command position. [Command card](../../courses/project-lab/level-03/assets/command-card.md) lists the complete commands.

The lab calls only `127.0.0.1:11434`, uses fixed course names, rejects cloud metadata, ignores HTTP proxy variables, and refuses redirects. It never fetches missing models, reads Level 1 keys/config, auto-selects cloud, grades answer quality, or certifies network disconnection. `create` invokes the installed Ollama CLI with an explicit loopback host and a fixed course name; rerunning it replaces that course name only.

Receipts retain model digest/bytes, full supplied prompt and hash, answer, settings, total request seconds, and incomplete/truncated status. They do not contain arbitrary learner documents. Scores, source verdicts, and observed network state require human worksheet entries. Partial attempts remain available after a failure; new attempts have distinct files. Creation does not upload or train model weights. Unload course models after use without deleting their files.

Maintainers run `uv run --frozen zta test local-models`. Live checks and honest limits belong in [Level 3 verification](../../release/level-03-verification.md).
