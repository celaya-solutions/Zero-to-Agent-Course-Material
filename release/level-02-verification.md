# Level 2 Candidate Verification

```text
Document:    Level 2 Candidate Verification
Version:     v1.0.1
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      c1f98c196155e89409aaed2fd618161472c6ad9338af211b9f7f89224809ebb7
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Status: **local review candidate; not a published or classroom-certified release**. Scope is Level 2 only; existing Level 1 readability fixes are retained. Source starts from `codex/level-1-documents` at `1c50b67`, with work on isolated branch `codex/level-2-night-watchman`.

## Gaps resolved from the inherited starter

The old setup required a second repository and root-level files, silently skipped a missing issue token, had no failure receipt, used unbounded page reads, and could duplicate an issue after a failed state commit. The new maintained project uses the existing learner fork, guarded default-branch execution, bounded input, saved pending intent, explicit failure receipts, and a tested local rehearsal. Legacy file paths now direct maintainers to one implementation.

The lesson separates the allowed same-fork practice issue from the prohibition on posting elsewhere. It explains daily UTC scheduling, new manual runs versus old reruns, public state versus private evidence, and disabling versus cancelling existing work. Preparation, worksheet, manual/assistant card, answer key, and complete authored fallback examples align with those controls.

## Verification record

Local deterministic tests cover stable/nested text, missing/empty/duplicate/unknown signals, baseline, unchanged, change, repeat, irrelevant footer, return transitions, fetch failure, state-write failure, issue rejection, uncertain delivery, lost issue response, reconciliation, corrupt state, scoped workflow, disabled/branch/trigger guards, bounded response, and secret-safe errors. All 43 watcher checks and 36 Level 1 regression checks passed on the maintainer Mac. The command rehearsal produced baseline saved, no change, changed, no change with exactly one local alert file and no hosted issue; see `release/evidence/watchman-local-macos.json`. A fresh local clone installed into its own environment from the lockfile with network disabled; its doctor and all 43 watcher tests also passed. Both course validators passed. Built 62 PDFs and five 20-slide decks; inspected 34 changed handout pages with no clipped text, and checked all 20 Level 2 slides at 1280x900 and 390x844 with keyboard/button navigation, focus, hidden-state, and horizontal-overflow checks.

Authored fallback logs are teaching material, not execution evidence. Machine/API fixtures use temporary local data and do not contact GitHub. Local terminal checks do not prove hosted permissions or the course upload path.

## Required live gates

| Gate | Current state | Evidence needed |
| --- | --- | --- |
| Fresh Windows setup and local rehearsal | Not performed on a Windows device | Exact OS, command versions, install, tests, three local rounds |
| Fresh Mac learner-fork setup | Maintainer local verification only | Independent learner setup, tools, expected outcomes and time |
| Hosted baseline/unchanged/changed/repeat | Pending designated practice-fork authorization | Four real run URLs, one real issue, state and artifact receipts |
| Hosted failure and recovery | Not performed | Controlled failure log, preserved state, repaired run without duplicate issue |
| Actual daily scheduled event | Not observed | A real `schedule` event receipt with intended and actual time; disable afterward |
| Browser stop controls | Not performed in a designated fork | Disabled state, false variable, no queued/active run, attempted trigger evidence |
| Claude Code/Codex fresh assistant edit | Not performed | Actual login and bounded edit, same local before/after expectation |
| Test-student Level 2 upload/reopen | Not performed | Authenticated student navigation, correct private file and receipt |
| Published version/download links | Not published | Reviewed source tag, generated packets, matching checksums and links |

The public v1.0.0-rc.1 tag belongs to Level 1 and must not be rewritten. PDF source links target the proposed v1.1.0-rc.1 tag so they remain usable when the platform serves a standalone PDF. That tag is not yet published: source URLs remain a release gate. For local review, use the matching Markdown files included in the packets. The canonical workflow template is not installed or enabled by maintenance builds.

## Integration boundary

Refresh course copies into separate website and private-platform review worktrees only after canonical source is committed. Keep consumer provenance and hash checks. Do not merge, push a release, deploy, reset a course, seed a database, or alter learner submissions as part of validation. Record actual consumer results in the final verification note.

## Official facts checked 2026-09-06

- [Manual execution](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow): `workflow_dispatch`, default-branch presence, write access, branch picker.
- [Schedules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule): default branch, delays/dropped jobs, UTC default and optional timezone support. This template deliberately uses UTC, daily 13:17.
- [Disable/enable](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows) and [cancel](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/cancel-a-workflow-run): stop future triggers and outstanding work separately.
- [Permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions): job-level contents/issues writes and unspecified scopes set to none.
- [Contents](https://docs.github.com/en/rest/repos/contents#create-or-update-file-contents), [Issues](https://docs.github.com/en/rest/issues/issues), and [artifacts](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts): state persistence, practice issue, and inspectable per-run receipts.
