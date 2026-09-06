# Level 4 Manual Edit - A Source Receipt

```text
Document:    Level 4 Manual Edit - A Source Receipt
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      8508c976903ce40ad5496d508084dee3105461cfdfd2a963df340df9917673eb
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

The initial rule can produce a smooth public answer with no source. Repair one citation rule. Do this before the first ten-attack run, then keep it unchanged for both attack phases.

## Predict and preserve

Run Five callers. In your worksheet keep the run name and C1/C2 replies. A C1 answer needs the supplied file and heading. C2 must still avoid an invented price. If both already pass, record that honestly and make the rule explicit anyway.

## One allowed edit

Open only .zta/front-desk/desk-instructions.md in your editor. Replace exactly:

```text
Source rule: Give a helpful public answer.
```

with:

```text
Source rule: For a public fact, name csr-public-brief.md and its exact heading. For a missing fact, say Not in the public source; do not invent a citation or answer.
```

Save the file. The app reads it for the next request; no rebuild is needed. The metadata hash in this private learner copy is not a security control and need not be edited for the exercise. Do not change the supplied brief, test prompts, expected answers, fixed defenses, model, endpoint, log, or earlier evidence.

## Retest

Run Five callers again, or `uv run --frozen zta callers front-desk`. Keep all rows and compare C1 and C2 before and after the edit. Verify each claim against the brief yourself. A file name alone is not proof. The rule is a wording improvement, not a permission boundary. If it still fails, record the failure and use the answer key to explain a safe rewrite.

## Coding-assistant prompt

Use one assistant from [the preparation guide](../../../preparation/coding-assistants.md), or make the edit yourself. No assistant subscription is required for the manual route.

```text
I am doing the Level 4 classroom edit. Explain why a public answer might omit a source. Read only .zta/front-desk/desk-instructions.md and replace the single Source rule with the exact replacement from courses/project-lab/level-04/manual-edit.md. Do not read other .zta files, provider keys, receipts, or private documents. Preserve all other rules, source files, tests, model, endpoint, limits, log, and controls. Show the one-line diff and the callers command. I will run it and judge C1 and C2 myself. Do not publish or submit anything.
```
