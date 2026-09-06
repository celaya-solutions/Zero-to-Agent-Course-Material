# Level 1 Release Verification

```text
Document:    Level 1 Release Verification
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      3098870f59e9cf9630d07b29238f81b27726fd1cd410f10fdfe5fcdff6450e67
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Status: **release candidate; classroom readiness is not yet certified**. A working app and passing fixture checks are useful evidence, but do not replace physical-device and authenticated student pilots.

## Evidence recorded on 2026-09-06

| Check | Observed result | Evidence or limitation |
| --- | --- | --- |
| Locked Python setup on this Mac | Passed: Python 3.12.13 and `uv sync --frozen`. | Existing developer Mac: macOS 27.0, Apple M5 Max, 128 GB RAM; not a new learner account. This does not verify a 16 GB minimum. |
| Deterministic application checks | 36 checks passed at the final application review. | Parsing, retrieval, PDFs, provider fixtures, receipts, private export, refresh state. Includes chronology, commit-link matching, and canonical export hashes. |
| Ollama live five-question pilot | All five expected behaviors passed. | [Recorded responses and passages](evidence/ollama-macos.json); Ollama 0.33.2, gemma3:4b. Human checked the claims, missing-price stop, and both synthetic records. |
| Answer time | 0.26–1.33 seconds in that recorded local pilot. | One machine/run; do not grade learners on this. |
| Hardware recommendation | Provisional 16 GB RAM / 10 GB free disk. | Minimum supported hardware has not been measured on actual Windows and Mac learner devices. |
| Claude and OpenAI adapters | Fixture checks only. | No live course API credentials were supplied to this workspace. Live billing/access/model behavior remains unverified. |
| Hosted Windows and Mac checks | Passed on both runners: locked install, 36 application tests, material validation, and clean working tree. | [GitHub run 34055813619](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material/actions/runs/34055813619); [machine-readable receipt](evidence/ci-macos-windows.json). Physical-device installer and learner-account pilots remain open. |
| Mac browser workflow | Passed for this maintainer pilot: binder, five live answers, classifications, two source checks, one/four-passage comparison, revision record, refresh/restart persistence, and Markdown download event. | The exported draft remains private; it is not a learner fork or course receipt. Theme contrast was corrected and visually checked. |
| Shutdown | Passed: Ctrl+C ended the app process and its health URL refused connections. | Private progress survived restart. |
| Generated website/platform copies | Course validator and platform standalone contracts pass in isolated worktrees. | No seed/reset, live deployment, or student-data mutation occurred. |
| Fresh public clone on this Mac | Passed: clone, `uv sync --frozen`, interactive local setup, doctor, and unchanged tracked files. | Existing uv/model cache was reused; dependency setup took under one second. This is not the proposed 45–90 minute learner preparation measurement. |
| Controlled retrieval exercise | Passed: reducing four passages to one omitted Record A; restoring four exposed both conflicting records. | [Before/after evidence](evidence/controlled-retrieval-macos.json). The one-passage answer was correctly judged a miss. |
| Course page and slides | Passed: existing entry page, preparation/lesson links, next-slide control, End key, and slide 20; layout inspected. | Generated website preview, not a production deployment. |
| Coding-assistant alternatives | Codex used to implement the project; manual change is specified. | Fresh learner Claude Code and Codex install/sign-in/edit pilots remain required. |
| Course sign-in | Public sign-in route responds. | An authenticated test-student upload-and-reopen run remains required. |

## Gate checklist and recording form

Complete each row on the actual selected platform; keep private student evidence and keys out of public records. Add a dated, redacted summary and exact release/commit. A failed test is a recorded result, not a reason to hide a row.

| Where | Action | Why | Expected result | Recovery if it fails |
| --- | --- | --- | --- | --- |
| Fresh Windows learner fork | Follow every Windows preparation step, including account, folder, uv, sync, setup, doctor, and launch. Record OS, RAM, free disk, uv/Python/app versions, setup time excluding downloads and download time separately. | Validate written instructions and runtime. | A question runs without an unwritten instruction. | Record the missing step; update guide; restart from a clean path. |
| Fresh Mac learner fork | Repeat the Mac guide and the same recorded fields. | Validate Mac-specific installation/folder steps. | Same observable outcome. | Fix the Mac guide and repeat. |
| Each coding assistant | Follow installation/sign-in, open project, use read-only prompt, apply one bounded edit, inspect diff. | Validate both supported editing routes. | One intended change, preserved tests, no publication by the assistant. | Record account block; use manual card; keep assistant gate open. |
| Each answer engine | Configure the named model; inspect consent/cost notice; run all five exact questions. Save retrieved passages, actual citations, elapsed time, and human verdicts. | Prove the shared evidence contract on real models. | Five correct behaviors; no invented price or silently chosen conflict winner. | Record miss, diagnose one cause, rerun all five after correction. |
| App on both OSes | Refresh after writing expectations and tests; export; stop with Ctrl+C; verify URL no longer responds. | Prove persistence, download, and shutdown. | Work survives refresh, file opens, process ends. | Fix the observed failure before marking pass. |
| GitHub Desktop/fork | Commit and push the deliberate settings change; inspect changed files online. | Prove reproducibility and private-data exclusion. | Public commit contains intended code only. | Unstage private files and use the recovery card. |
| Course test student | Sign in, open course, select Level 1, choose the exported Markdown file, submit, reopen Submission History and attached file. Capture controls with a non-personal test nickname. | Prove the actual private submission path. | Correct file, timestamp, receipt, and downloaded content. | Record exact auth/enrollment/upload block; preserve the local file and do not claim pass. |
| Release downloads | Download both ZIPs anonymously, compare SHA256, open lesson PDF, saved packet, and slides offline. | Prove learners receive usable materials. | Files and links match the published tag. | Replace/rebuild the candidate before sharing. |

A live pilot can be recorded from the canonical repository with `uv run --frozen python scripts/live_pilot.py --live` after `zta setup`. That command makes exactly five requests to the chosen provider and can incur charges. It writes `.zta/live-pilot-PROVIDER.json`; review/redact before copying a public-only result into `release/evidence/`. Human verdicts remain mandatory.

No minimum-funding figure is promised: check the provider's checkout during each pilot. Record any required deposit and the displayed price before the first paid request. Do not automatically fund accounts or retry paid requests.
