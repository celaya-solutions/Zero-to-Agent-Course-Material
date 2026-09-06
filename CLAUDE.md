# Claude Code Course Instructions

```text
Document:    Claude Code Course Instructions
Version:     v1.3.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      1d1d70fa2abdeb0ebde61070e409d8b992bb2008ca363816903f43736626d607
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Read [AGENTS.md](AGENTS.md) first. Codex and Claude Code use the same scope and checks.

For **course maintenance**, Level 4 now has a local front desk and teaching package. Follow [the handoff](release/next-section.md) and [verification](release/level-04-verification.md). Preserve earlier work and separate consumers. Do not begin Level 5, merge, or publish as cleanup.

For a **Level 4 learner exercise**, follow [the manual card](courses/project-lab/level-04/manual-edit.md). Edit only the one Source rule in `.zta/front-desk/desk-instructions.md`; do not read other private files or keys. Preserve test inputs, records, model, endpoint, logs, and controls. Show the diff and callers command; the learner runs it and judges C1/C2.

For a **Level 3 learner exercise**, follow [the manual card](courses/project-lab/level-03/manual-edit.md). Edit only the named private Modelfile rule. Do not open other `.zta/` files or keys. Keep the base, endpoint, prompts, limits, tests, and earlier evidence. Show the diff and create/check commands; the learner runs them and judges both answers.

For a **Level 2 learner exercise**, read [the manual card](courses/project-lab/level-02/manual-edit.md). Explain why unrelated footer text should stay quiet, then make only the requested paragraph edit. Preserve the status, watcher, workflow, state, tests, and predictions. Do not read private `.zta/`, enable workflows, create issues, or publish. Run `uv run --frozen zta test watchman`; the learner runs the local rehearsal and judges the result.

For a **Level 1 learner edit**, read the [manual edit card](courses/project-lab/level-01/manual-edit.md) and [learner lesson](courses/project-lab/level-01/student.md). Explain the observed miss before editing. Change one rule or retrieval setting. Preserve supplied documents, expected results, and tests. Show the diff and the exact rerun command. Keep credentials and learner work private. Do not publish anything unless the learner separately requests that action.

Use `uv run --frozen zta test documents` from the repository root to check a change without paid API calls. Do not run a live cloud request to test an edit without the learner selecting that route and accepting its cost/data notice.
