# Saved Three-Run Packet - Level 2

This is an outage route, not a live run.

## Run 1

    2026-09-04T13:00:03+00:00 | value=OPEN | decision=baseline saved

Expected: baseline, no alert.

## Run 2

    2026-09-04T13:04:12+00:00 | value=OPEN | decision=no change

Expected: no alert. This is success, not a failed run.

## Run 3

    2026-09-04T13:09:44+00:00 | value=PAUSED | decision=changed from OPEN to PAUSED

Saved issue title: Change spotted: OPEN to PAUSED

Expected: one useful alert.

## Learner job

Write the expected result for each run, judge the output, identify the receipt, and mark where the off switch would stop a fourth run. Mark live-only fields Not applicable: saved run.
