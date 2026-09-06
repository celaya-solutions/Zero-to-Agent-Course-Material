# Level 2 Instructor Answer Key

```text
Document:    Level 2 Instructor Answer Key
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      6a27cd1c01a41c20f5f83d03cf18d759686a190234d3a0f7e60bee594dd5ecf6
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Do not show this page until predictions are recorded. It is a teaching key, not evidence that any hosted pilot ran.

## Six-line model spec

Address is the learner's own raw practice-page URL; execution uses the run's immutable commit version. Signal is the one closed `watch-value` element. A meaningful change is a transition between OPEN and PAUSED; missing/empty/duplicate/unknown text fails. Trigger is manual during class and daily at 13:17 UTC only while enabled. Alert is one issue in that same fork with old/new values and source. Never list forbids buying, replying, deleting, posting elsewhere, private access, people tracking, and automatic spending; it explicitly permits the practice issue.

## Expected evidence

| Case | Decision and state | New issue |
| --- | --- | --- |
| No previous state, OPEN | baseline saved; current OPEN; pending null | 0 |
| OPEN again | no change; current OPEN | 0 |
| OPEN to PAUSED | changed; current PAUSED; pending null after completion | 1 |
| PAUSED again | no change; current PAUSED | 0 |
| Only footer changes | no change; current untouched | 0 |
| Page missing/invalid or fetch fails | failed; last good state unchanged | 0 |
| State write fails before send | failed; no success claimed | 0 |
| Issue denied definitively | failed; pending remains retryable after repair | 0 |
| Issue created, last state write fails | failed; next run finds same issue, records alert recovered | 0 additional |
| Issue delivery uncertain and not found | failed; attempted pending remains, human reconciliation needed | No automatic resend |
| Disabled, variable false, no outstanding jobs | disabled state observed; no new manual run | 0 |

The changed issue is `Change spotted: OPEN to PAUSED`, with both values and the practice source in its body. GitHub supplies the creation time; the round receipt supplies time, source commit, run, previous/current values, decision, transition ID, and issue URL when known. If a pending alert is recovered, that round finishes the older pending transition before a later round observes the page again.

## Exit answers

1. A GitHub-hosted runner runs each job; the learner laptop need not remain open.
2. No change means a successful valid observation matched the baseline. Failed means no successful decision was completed; it may need issue/state recovery.
3. State lets a new runner compare with the last confirmed value. Deleting it discards memory and may hide a change.
4. The token has repository-wide contents/issues write scopes. The reviewed code writes one state file and one practice issue per transition, within the learner fork.
5. A fresh manual run selects the latest default-branch commit. Re-running an older job uses that older commit and can observe an old status.
6. The learner observed a disabled workflow, false variable, unavailable trigger, and no queued/active work. That is not proof of an unobserved future schedule tick.

## Grade understanding fairly

An honest failure is useful evidence when the learner identifies the stage and proposes a bounded recovery. Do not call a blocked hosted build complete. A saved route can demonstrate sound evaluation and a correctly explained stop, but cannot satisfy an individual live issue or operated switch claim.

The local footer exercise passes when before/after status remains equal, the next decision is no change, and the diff changes only the unrelated paragraph. Do not require an assistant or model-generated mistake.

## Instructor recovery boundary

See [the project README](../../../projects/watchman/README.md) before repairing uncertain delivery. Keep the workflow disabled while investigating. Check the pending ID against open and closed issues. Never delete good state, delete an issue to force a test, or automatically reset the send flag. Keep a separate private note of any manual repair and rerun the same expectation after review.
