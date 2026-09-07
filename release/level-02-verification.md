# Level 2 Candidate Verification

```text
Document:    Level 2 Candidate Verification
Version:     v1.0.3
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      d8a847e3028862c872bf670ff8f5b3a8cf4ebe71c56191c9eb80b3d20078cd5d
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

## Deployment update — 2026-09-06

Published v1.4.0-rc.1 and both live consumers are verified in [the delivery record](delivery-v1.4.0-rc.1.md). Anonymous downloads, hashes, offline slides, source links, and live delivery passed; remaining learner gates have specific missing resources. Earlier local-only delivery statements below describe the pre-publication review. New Spanish work and Spanish delivery pilots are excluded by the active user direction.

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
| Hosted baseline/unchanged/changed/repeat | Passed in dedicated synthetic practice copy | Four run receipts and one practice issue in the follow-through record |
| Hosted failure and recovery | Passed | Invalid-signal failure, unchanged last good state, repaired run and no duplicate issue |
| Actual daily scheduled event | Not observed | A real `schedule` event receipt with intended and actual time; disable afterward |
| Stop controls | Passed through GitHub API/CLI; browser-specific exercise remains open | Disabled state, false variable, zero active runs, HTTP 422 dispatch rejection |
| Claude Code/Codex fresh assistant edit | Not performed | Actual login and bounded edit, same local before/after expectation |
| Test-student Level 2 upload/reopen | Blocked until September 12 at 06:00 UTC | Dedicated student signed in; actual date gate refused access |
| Published version/download links | Passed v1.4.0-rc.1 | See delivery record; tag and attached downloads unchanged |

The public v1.0.0-rc.1 tag belongs to Level 1 and must not be rewritten. PDF source links target the proposed v1.1.0-rc.1 tag so they remain usable when the platform serves a standalone PDF. That tag is not yet published: source URLs remain a release gate. For local review, use the matching Markdown files included in the packets. The canonical workflow template is not installed or enabled by maintenance builds.

## Integration boundary

Refresh course copies into separate website and private-platform review worktrees only after canonical source is committed. Keep consumer provenance and hash checks. Do not merge, push a release, deploy, reset a course, seed a database, or alter learner submissions as part of validation. Record actual consumer results in the final verification note.

## Official facts checked 2026-09-06

- [Manual execution](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow): `workflow_dispatch`, default-branch presence, write access, branch picker.
- [Schedules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule): default branch, delays/dropped jobs, UTC default and optional timezone support. This template deliberately uses UTC, daily 13:17.
- [Disable/enable](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows) and [cancel](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/cancel-a-workflow-run): stop future triggers and outstanding work separately.
- [Permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions): job-level contents/issues writes and unspecified scopes set to none.
- [Contents](https://docs.github.com/en/rest/repos/contents#create-or-update-file-contents), [Issues](https://docs.github.com/en/rest/issues/issues), and [artifacts](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts): state persistence, practice issue, and inspectable per-run receipts.

## Follow-through on 2026-09-06

See [the live learner and control record](learner-verification-20260906.md). Level 1 synthetic learner upload/reopen, hosted Watchman manual rounds and interim shutdown, and a live local Front Desk pause now have actual evidence. Levels 2-5 uploads are date-gated; physical learners, observers and the actual scheduled event remain open. The published tag/downloads are unchanged.
