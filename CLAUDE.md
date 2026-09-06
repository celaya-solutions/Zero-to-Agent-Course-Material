# Claude Code Course Instructions

```text
Document:    Claude Code Course Instructions
Version:     v1.1.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      2bcfc5b27a107942850eaf14984d1a9e1c747ba3587fe2323545ff19a33ea53f
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Read [AGENTS.md](AGENTS.md) first. Codex and Claude Code use the same scope and checks.

For **course maintenance**, Level 3 now has a local lab and teaching package. Follow [the handoff](release/next-section.md) and [verification](release/level-03-verification.md). Preserve earlier work and separate consumers. Do not begin Level 4 or publish as cleanup.

For a **Level 3 learner exercise**, follow [the manual card](courses/project-lab/level-03/manual-edit.md). Edit only the named private Modelfile rule. Do not open other `.zta/` files or keys. Keep the base, endpoint, prompts, limits, tests, and earlier evidence. Show the diff and create/check commands; the learner runs them and judges both answers.

For a **Level 2 learner exercise**, read [the manual card](courses/project-lab/level-02/manual-edit.md). Explain why unrelated footer text should stay quiet, then make only the requested paragraph edit. Preserve the status, watcher, workflow, state, tests, and predictions. Do not read private `.zta/`, enable workflows, create issues, or publish. Run `uv run --frozen zta test watchman`; the learner runs the local rehearsal and judges the result.

For a **Level 1 learner edit**, read the [manual edit card](courses/project-lab/level-01/manual-edit.md) and [learner lesson](courses/project-lab/level-01/student.md). Explain the observed miss before editing. Change one rule or retrieval setting. Preserve supplied documents, expected results, and tests. Show the diff and the exact rerun command. Keep credentials and learner work private. Do not publish anything unless the learner separately requests that action.

Use `uv run --frozen zta test documents` from the repository root to check a change without paid API calls. Do not run a live cloud request to test an edit without the learner selecting that route and accepting its cost/data notice.
