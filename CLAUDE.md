# Claude Code Course Instructions

```text
Document:    Claude Code Course Instructions
Version:     v1.1.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      c30110eccef9d86f9d736cf102de4436e7be40d145c888b7a80e51f33a991068
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Read [AGENTS.md](AGENTS.md) first. Codex and Claude Code use the same scope and checks.

For **course maintenance**, Level 2 now has a local implementation and teaching candidate. Follow [the continuation handoff](release/next-section.md) and [verification gates](release/level-02-verification.md). Preserve Level 1 readability fixes and keep canonical source, generated website copies, and the private platform separate. Do not begin Level 3 or publish as cleanup.

For a **Level 2 learner exercise**, read [the manual card](courses/project-lab/level-02/manual-edit.md). Explain why unrelated footer text should stay quiet, then make only the requested paragraph edit. Preserve the status, watcher, workflow, state, tests, and predictions. Do not read private `.zta/`, enable workflows, create issues, or publish. Run `uv run --frozen zta test watchman`; the learner runs the local rehearsal and judges the result.

For a **Level 1 learner edit**, read the [manual edit card](courses/project-lab/level-01/manual-edit.md) and [learner lesson](courses/project-lab/level-01/student.md). Explain the observed miss before editing. Change one rule or retrieval setting. Preserve supplied documents, expected results, and tests. Show the diff and the exact rerun command. Keep credentials and learner work private. Do not publish anything unless the learner separately requests that action.

Use `uv run --frozen zta test documents` from the repository root to check a change without paid API calls. Do not run a live cloud request to test an edit without the learner selecting that route and accepting its cost/data notice.
