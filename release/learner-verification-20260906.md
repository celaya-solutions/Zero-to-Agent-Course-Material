# English Learner Verification Follow-through

```text
Document:    English Learner Verification Follow-through
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      cdd59f5700f6cd521f7e29812f5fbb4d55904961d53f5860af077194b9527d8c
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

## Scope and version

This is a maintainer verification run dated 2026-09-06 America/Denver (2026-09-07 UTC). The published course remains v1.4.0-rc.1 at 8492461afdc7e852c3a0f042461e4e8a5c988ac1. Its tag, attached downloads, website export receipt, and teaching files were not replaced. Later commits record maintenance evidence only. The user asked to continue the instruction files and directed the agent to use best judgment when choosing dedicated test resources.

## Results

| Check | Result | Evidence and limit |
| --- | --- | --- |
| Live learner sign-in | Passed | Created one new synthetic, confirmed, non-admin student with a new enrollment. Generated credentials and browser storage remain private. No existing account was impersonated or reset. |
| Level 1 upload/reopen | Passed | Uploaded the published worksheet plus an explicit synthetic verification note, observed Handin received, reopened Source and downloaded the file in a new browser context. SHA256 4753bf98ce05fcafee223f0e1971b778462dbf3b532ef0aa2f84717369f95067 matched. This proves file delivery, not completion of learner exercises. |
| Levels 2-5 authenticated access/upload | Blocked by actual course dates | Student requests redirected to the assessments hub with an authorization message. Start times are September 12, 19, 26 and October 3, 2026 at 06:00 UTC. No course dates, staff roles, or access rules were changed to bypass them. |
| Existing records | Passed | Every pre-existing row in users, courses, assessments, problems, submissions, scores, enrollments and assessment-user data retained its checksum. Additions are the dedicated test user, its enrollment, five assessment-user rows and one Level 1 submission. Detailed counts/hashes remain private. |
| Source viewer on phone | Failed, repaired, retested live | Initial rendered source was below a large empty region, with black code on a dark panel and cramped side panels. Private runtime fix 0c9e4822 keeps the viewer in the normal content panel, uses readable text and a full-width phone stack with separate saved layouts. Sass and Rails ERB compile; live 390px and 1280px views, hide/show comments, refresh and horizontal bounds pass with zero page errors. Public Rails runtime was restarted through its existing launchd service; Railway Course Edge stayed unchanged. |
| Live Front Desk pause | Passed maintainer control test | One real local gemma3:4b generation was sent. Pause was saved while waiting for response headers. The returned answer was suppressed and the batch stopped; a second paused run sent zero requests and recorded zero rows. [Redacted trace](evidence/live-pause-20260906.json). Already-sent model computation continued; this does not claim request cancellation or human observation. |
| Hosted Watchman | Passed six manual rounds and interim stop | Baseline, unchanged, OPEN-to-PAUSED change, repeat, invalid-signal failure and restored-input recovery completed. Exactly one practice issue; failure preserved PAUSED state, sequence 1, pending null. [Actual receipts](evidence/watchman-hosted-20260906.json). |
| Actual daily schedule | Blocked; no event observed | The reviewed template remains daily at 13:17 UTC. After recovery the workflow was disabled, WATCHMAN_ENABLED set false, all six runs were final, and a new dispatch was rejected with HTTP 422. An hourly unattended follow-up was rejected by automatic approval review because it could later mutate repositories and cancel runs. No automation was created and the workflow remains disabled. Explicit owner approval is required to enable the daily pilot and create that follow-up. |
| Project regression checks | Passed | Documents 36, Watchman 43, Local Models 17, Front Desk 20: 116 total. These are deterministic maintainer checks. |

## Watchman receipts

Dedicated repository: [Zero-to-Agent-Watchman-Pilot-20260906](https://github.com/celaya-solutions/Zero-to-Agent-Watchman-Pilot-20260906). This is a separate public synthetic practice copy of the published tag, not a GitHub network fork: the signed-in owner also owns the canonical repository. Only this practice repository was enabled or changed.

| Round | Run | Observed decision |
| --- | --- | --- |
| Baseline | [34069339344](https://github.com/celaya-solutions/Zero-to-Agent-Watchman-Pilot-20260906/actions/runs/34069339344) | baseline saved, OPEN |
| Unchanged | [34069421255](https://github.com/celaya-solutions/Zero-to-Agent-Watchman-Pilot-20260906/actions/runs/34069421255) | no change |
| Change | [34069482873](https://github.com/celaya-solutions/Zero-to-Agent-Watchman-Pilot-20260906/actions/runs/34069482873) | changed; practice issue 1 |
| Repeat | [34069532084](https://github.com/celaya-solutions/Zero-to-Agent-Watchman-Pilot-20260906/actions/runs/34069532084) | no change; no duplicate issue |
| Controlled failure | [34069596969](https://github.com/celaya-solutions/Zero-to-Agent-Watchman-Pilot-20260906/actions/runs/34069596969) | failed: signal must be OPEN or PAUSED |
| Recovery | [34069692678](https://github.com/celaya-solutions/Zero-to-Agent-Watchman-Pilot-20260906/actions/runs/34069692678) | no change; state preserved |

## Remaining owner and learner work

- For the actual daily event, approve enabling this dedicated pilot and one bounded hourly follow-up. The follow-up should watch for event=schedule, retain the artifact, then disable the workflow, set the variable false, cancel/wait for any active runs and verify shutdown. Stop and report failure if no event arrives by a stated deadline. Do not use a manual dispatch as schedule evidence.
- Continue the synthetic student's remaining uploads when each level opens. Keep its private credentials, browser state, screenshots and raw table checks outside public commits. Do not change class dates or existing learner work to force a pass.
- Fresh physical Windows/Mac learners, supported assistant install/sign-in/edit routes, partner-observed network disconnection, and actual Level 5 learner presentations/table timing remain unperformed. The maintainer Mac and automated browser are not substitutes.
- The local-model host's previously noted shared listener boundary still needs a separate owner-reviewed preflight before an observed isolation test. This run did not disconnect network links, change the shared model service or claim isolation.
- No funded cloud provider was selected for this pilot. No purchase, paid request/retry or provider switch occurred. New Spanish work and Spanish delivery pilots remain excluded.

Private evidence is retained only in the ignored .zta/learner-pilot-20260906 folder of the learner-verification worktree. It includes the dedicated test credentials; never print or publish that file. The public evidence files contain only supplied synthetic inputs, safe control metadata and public run links.
