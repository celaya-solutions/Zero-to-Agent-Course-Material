# Claude Code Course Instructions

```text
Document:    Claude Code Course Instructions
Version:     v1.0.1
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      4110e190ac5d5bc2a828daa87037a758c09b6be4fd3399e9c8972ad7d3e2bd34
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Read [AGENTS.md](AGENTS.md) first. Codex and Claude Code use the same scope and checks.

For **course maintenance**, the next section is **Level 2: The Night Watchman**. Follow [the continuation handoff](release/next-section.md), including its starting branch and unpublished Level 1 fixes. The existing Level 2 starter and lessons are a starting point, not a verified new release. Keep source, generated website copies, and the private platform separate.

For a **Level 1 learner edit**, read the [manual edit card](courses/project-lab/level-01/manual-edit.md) and [learner lesson](courses/project-lab/level-01/student.md). Explain the observed miss before editing. Change one rule or retrieval setting. Preserve supplied documents, expected results, and tests. Show the diff and the exact rerun command. Keep credentials and learner work private. Do not publish anything unless the learner separately requests that action.

Use `uv run --frozen zta test documents` from the repository root to check a change without paid API calls. Do not run a live cloud request to test an edit without the learner selecting that route and accepting its cost/data notice.
