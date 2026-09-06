# Saved Three-Run Packet - Level 2

```text
Document:    Saved Three-Run Packet - Level 2
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      69774dbe59015eb2686a581b6d605e350b371d032331519e0868727ee530e8c1
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

**AUTHORED CLASSROOM EXAMPLES. These are not live run logs or proof of a learner launch.** The times and run names below are illustrative. GitHub was not contacted to create this packet. No real issue, schedule, or submission receipt is claimed.

Use after two attempts or five minutes on a block. Cover each Actual section, write a prediction with your own time, then reveal it. Copy the same fields into the worksheet and label the route Saved example. Live-only URLs, switch operation, and upload fields remain Not performed unless you actually perform them.

## Source and written rule

Supplied page fragment before the edit:

```html
<p>Status: <strong id="watch-value">OPEN</strong></p>
<p>Footer revision one.</p>
```

Rule: compare exactly one valid OPEN/PAUSED status. First observation sets baseline; identical observations are quiet; a valid status transition creates one practice issue. A failure preserves the last confirmed value. Never buy, reply, delete, post elsewhere, track people, or spend. Only the practice issue is allowed.

## Run A - Predict before revealing

Page: OPEN. Prior state: absent. What should be saved? How many issues?

### Actual A - authored

```json
{"time":"2026-09-06T13:17:03+00:00","route":"authored saved example","run":"EXAMPLE-A","previous":null,"current":"OPEN","decision":"baseline saved"}
```

After state: current OPEN, sequence 0, pending null. Issue count: 0.

Verdict: Pass for this example, because no prior value exists to compare. This does not prove your own baseline run.

## Run B - Predict before revealing

Page: OPEN. State: OPEN. What counts as successful silence?

### Actual B - authored

```json
{"time":"2026-09-06T13:20:12+00:00","route":"authored saved example","run":"EXAMPLE-B","previous":"OPEN","current":"OPEN","decision":"no change"}
```

After state: still OPEN. Issue count: 0. Verdict: Pass; observation succeeded and values match.

## Run C - Predict before revealing

Change only OPEN to PAUSED inside the marked element. State: OPEN. What should the issue tell a person?

### Actual C - authored

```json
{"time":"2026-09-06T13:24:44+00:00","route":"authored saved example","run":"EXAMPLE-C","previous":"OPEN","current":"PAUSED","decision":"changed","issue":"EXAMPLE ISSUE 1 - no live URL"}
```

Example issue title: **Change spotted: OPEN to PAUSED**

Example body: TRAINING-ONLY: Night Watchman. Source: the learner's supplied public practice-page address. Old value: OPEN. New value: PAUSED. Meaningful change: the marked status changed. Check the practice page; no other action was taken. A transition marker ties it to pending state.

After state: current PAUSED, sequence 1, pending null. Issue count: 1. Verdict: Pass; both values and the source are visible.

## Run D - Repeat and noise check

Predict before revealing: page remains PAUSED; only footer wording changes. Should it create a second issue?

### Actual D - authored

```json
{"time":"2026-09-06T13:27:01+00:00","route":"authored saved example","run":"EXAMPLE-D","previous":"PAUSED","current":"PAUSED","decision":"no change"}
```

After state: PAUSED. Total issues: 1. Verdict: Pass; unrelated footer text is ignored.

## Failure card - an error is not silence

Predict before revealing: the request times out after the last confirmed PAUSED state.

### Actual failure - authored

```json
{"time":"2026-09-06T13:30:01+00:00","route":"authored saved example","run":"EXAMPLE-E","previous":"PAUSED","decision":"failed","error":"Network request failed or timed out. No automatic retry; inspect the receipt."}
```

Last good state remains PAUSED; no additional issue. Verdict: the run failed, while state preservation behaved correctly. Record those as separate facts. A sensible next step is one new manual run after network recovery, not deleting the state file.

## Off-switch card - distinguish a description from an action

Authored observation: an example learner selected Actions > Project Lab Watchman > three-dot menu > Disable workflow, set WATCHMAN_ENABLED to false, checked/cancelled outstanding work, refreshed, and saw the disabled state with the Run workflow control unavailable. No new manual run was created.

Your job: explain why closing the laptop is insufficient and why a queued/active run must also be checked. In your worksheet write **Not performed: saved switch example** for your own live switch action. Do not claim you waited through a real future daily tick.

## Evidence and exit

Complete all six spec lines, predictions, actuals, verdicts, example alert details, one failure explanation, and the six exit answers. Leave live URLs as Not performed. Keep your own course upload receipt only if you submit and reopen the worksheet; this packet supplies none. Ask for the missing live practice when service or access returns.
