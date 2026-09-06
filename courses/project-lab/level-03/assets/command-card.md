# Level 3 Command Card

```text
Document:    Level 3 Command Card
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      2a77a6d7b132c8a01c9405c042fd2f13018eba492c405341f0432ebe9b928196
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Run from the course root, where `pyproject.toml` lives. Mac Terminal and Windows PowerShell use the same commands. Use `uv sync --frozen` online before class. Do not type square-bracket placeholders.

| Command | What it does | Expected result |
| --- | --- | --- |
| `ollama list` | Lists already downloaded models | `gemma3:1b` and `gemma3:4b` with IDs and sizes |
| `uv run --frozen zta prepare local-models` | Copies the worksheet and rules without replacing existing work | Files in private `.zta/local-models/` |
| `uv run --frozen zta doctor local-models` | Checks the fixed local endpoint and both models | Two LOCAL rows; no answer generated |
| `uv run --frozen zta offline local-models` | Runs one supplied prompt | Answer, total seconds, receipt; human observes disconnection |
| `uv run --frozen zta benchmark local-models` | Runs the same three prompts on both models | Six rows; you score quality |
| `uv run --frozen zta create local-models` | Creates/replaces the course name from your private rules | `zta-desk:latest` appears in `ollama list` |
| `uv run --frozen zta check local-models` | Tests normal writing and missing price/date | Two actual answers for your verdict |
| `uv run --frozen zta test local-models` | Runs code checks without a model request | Passing tests; not model-quality proof |

Need to stop? Press Ctrl+C. On your own machine run `ollama stop gemma3:1b`, `ollama stop gemma3:4b`, or `ollama stop zta-desk:latest` for the course model still loaded. Unloading keeps its files. Avoid deleting models as a classroom shortcut.

[Preparation](../preparation.md) includes exact downloads, hardware planning, sources, and recovery. [Manual edit](../manual-edit.md) shows the one-rule change. [Ollama Modelfile reference](https://docs.ollama.com/modelfile) explains FROM, SYSTEM, and PARAMETER.
