# Documents - Custom Starter

```text
Document:    Documents - Custom Starter
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      8bafc26785872ffbea7576e83fb9008c8a81445038f8b6496f161f42efe5a1e7
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

A small Python/Streamlit app. SQLite FTS5 searches local text. Ollama, Claude API, or OpenAI API writes from the selected passages. No embeddings, vector database, Docker, web crawler, or public hosting account is required.

## Commands from the COURSE ROOT

```sh
uv sync --frozen
uv run --frozen zta setup
uv run --frozen zta doctor documents
uv run --frozen zta start documents
uv run --frozen zta test documents
```

Run the test command in a second terminal, or stop the app with Ctrl+C first. Open http://127.0.0.1:8501 while start runs. Doctor uses a free model-list check for cloud providers; the practice answer confirms generation and billing.

## Data flow

Load binder > validate files > extract page/heading passages > local SQLite keyword index > ranked passages > selected answer engine > JSON answer and verbatim source quotes > receipt validation > learner verdict > private Markdown export.

Input: Markdown/UTF-8 text/text PDFs, up to 20 files, 10 MB each, 100 PDF pages per file, and 500,000 total extracted characters. Scanned or encrypted PDFs require a text alternative. The app preserves exact filename, heading, and PDF page. It does not fetch websites from document links.

## Where to edit

Paths are from the course root. The shared `zta` package serves every level, so a change there affects more than Level 1.

- `projects/documents/settings.toml`: max_passages (default 4) and show_source_quotes (default false).
- `projects/zta/src/zta/documents.py`: extraction, index construction, keyword retrieval.
- `projects/zta/src/zta/providers.py`: fixed provider endpoints, prompt, API adapters, and receipt checks.
- `projects/zta/src/zta/evidence.py`: five questions, completion checks, private export.
- `projects/zta/src/zta/storage.py`: private local configuration/progress and atomic saves.
- `projects/zta/src/zta/app.py`: learner controls.
- `projects/zta/src/zta/cli.py`: setup, doctor, start, and test.

The provider contract returns status (`answered`, `not_found`, `conflict`, `needs_review`), answer text, citation ID/quote pairs, time, usage, and estimated cost. Receipt checks reject unknown IDs, absent quotes, and quotes not present in the retrieved text. These checks do not certify semantic correctness.

## Private state and limitations

.zta/config.json contains the selected provider and any API key. .zta/binder holds imported documents. .zta/index.sqlite3 is the search index. .zta/progress.json holds predictions, runs, verdicts, and source checks. All are ignored by Git. The export removes the configured key and common key-shaped strings, but still contains learner work and belongs in the private course platform.

This is a single-user local teaching app. No authentication, public network exposure, unattended actions, provider failover, or paid retries. Cloud use requires the explicit public/synthetic notice. Index rebuilding replaces the app's current search corpus, while earlier test records retain their original retrieved passages.

## Test and pilot distinction

Deterministic tests use HTTP fixtures and do not prove live provider behavior. Record live pilots separately with real provider/model/version/time. The saved-example route is intentionally labeled authored classroom material. See [release verification](../../release/verification.md).
