# Front Desk - Local Classroom Project

```text
Document:    Front Desk - Local Classroom Project
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      9624458892c07cf37e1b86c501b3e53eb36b87ec971917fc8bb9e012e779c9fa
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

The maintained Level 4 project serves the supplied public CSR snapshot and fictional test cards. It uses local gemma3:4b through Ollama on 127.0.0.1:11434. It does not read the Documents provider configuration or keys and never switches to a cloud model.

## Run

Complete [Level 4 preparation](../../courses/project-lab/level-04/preparation.md) from the full course repository. The website resource copy and PDF/ZIP packets alone are not an installable application.

```sh
uv run --frozen zta prepare front-desk
uv run --frozen zta doctor front-desk
uv run --frozen zta start front-desk
```

Open http://127.0.0.1:8504. The [student lesson](../../courses/project-lab/level-04/student.md) provides the sequence and proof. CLI equivalents:

```sh
uv run --frozen zta callers front-desk
uv run --frozen zta attacks front-desk
uv run --frozen zta lock front-desk
uv run --frozen zta attacks front-desk
uv run --frozen zta callers front-desk
uv run --frozen zta pause front-desk
uv run --frozen zta callers front-desk
uv run --frozen zta resume front-desk
uv run --frozen zta test front-desk
```

Make the one citation edit before the first attacks set. Keep the same model digest, prompts, and rules across attack phases. Lock is one-way. Repeated runs use fresh IDs; prepare preserves edits and earlier receipts.

## Boundaries

Only supplied test messages; no free-text uploads or real business records. Context is rebuilt from an allowlist for each request; previous answers are never fed back. The locked request omits fake bait and rejects known fake values if the learner's edited rule reintroduces them. Delimiters are only wording. No send, booking, browser, or spending tools exist in either phase. Every draft needs human review; a model can still hallucinate or ignore rules.

Control revision is checked before generation and after its response. Pause prevents new requests and suppresses a reply if control changed while it was running. It does not cancel already-started Ollama computation. A run made while paused records zero rows without calling Ollama. One run lock prevents overlapping batches in the same private folder; see preparation for crash recovery.

Private .zta/front-desk/ holds instructions, worksheet, run receipts, and control records. Each row stores input, expected behavior, answer, flags, request/rules hashes, and timing; each run stores model identity and test-set hash. Known fake leakage is intentionally visible for class grading. Verdict stays empty until the learner records their judgment in the worksheet. Logs are ordinary local files, not signed or tamper-proof evidence. Nothing is submitted automatically.

## Maintainer references

[Ollama generation API](https://docs.ollama.com/api/generate), [model listing](https://docs.ollama.com/api/tags), and [public case source](https://www.celayasolutions.com/) checked 2026-09-06. Tests use mocked HTTP and temporary private folders; a separate live run validates local generation. Existing device and upload gates remain in [Level 4 verification](../../release/level-04-verification.md).
