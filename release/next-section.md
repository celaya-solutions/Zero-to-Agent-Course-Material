# Release and Verify the Five-Level Course

```text
Document:    Release and Verify the Five-Level Course
Version:     v1.1.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      096f5e257a2494ba7da1b3b811c1cd99d11f222a50ac6a7994e771793fd2011a
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

## Active user direction

On 2026-09-06 the user requested the remaining publishing, deployment, and real learner checks, and explicitly excluded Spanish work. Perform the work below as the next maintenance task. The instruction-update task records this handoff; it does not itself claim those actions were executed.

Levels 4 and 5 are already merged into the canonical course and website main branches. Their private course copy is merged into the existing canonical-course integration branch, not yet released to the live Rails checkout. All five lesson packs are complete. Start from the current merged state and verify exact branch, remote, service, and source receipt before acting.

This user direction supplies the scoped release instruction mentioned by older no-push/no-deploy notes. Those dated notes remain historical evidence, not a reason to ask again for the same release permission. Work in isolated branches, validate fixes, and carry the requested release through to live verification. Ask only for a specific missing account, device, required owner action, or action beyond this scope; continue independent work while blocked.

## 1. Prepare and publish the downloads

Use [the release runbook](maintaining.md). Recheck [Level 1 verification](verification.md) and each Level 2-5 verification record; keep measured results and unfinished checks distinct. Run all four project suites and both course validators. Rebuild slides/PDFs if teaching content or release URLs change. Rebuild learner/instructor ZIPs and individual downloads, inspect the rendered outputs, and verify every SHA256.

Publish the reviewed canonical source and matching downloads to celaya-solutions/Zero-to-Agent-Course-Material. The current candidate is v1.4.0-rc.1. Inspect remote tags first; never rewrite a published tag. If a new version is needed, align the package, PDF links/footer, course manifest, and downloads before publication. Mark the release prerelease while required live checks remain open; do not call it classroom-certified. Download the published files anonymously, verify checksums, open PDFs/slides offline, and check PDF source links against the actual tag.

## 2. Publish the website

Export the committed canonical source into the public website with scripts/export_course.py and run --check; preserve course-material-source.json. Commit/integrate the generated changes, push the correct website remote, and deploy the public site only to Railway Landing Page. Confirm the exact Railway project, environment, and service before deploying. Preserve Course Edge for the Rails tunnel.

Wait for that deployment ID to reach SUCCESS, then verify zerotoagent.org, the five-level materials, versioned downloads, and the learn.zerotoagent.org sign-in links. Inspect desktop/phone and light/dark rendering, PDF opening, and slide navigation. A successful upload or root HTTP 200 is not enough; record the served content and relevant URLs.

## 3. Release the private course update

Use the separate private repository and its existing canonical-course integration branch. Push private Rails source only to its private fork remote, never its public upstream origin. Confirm the current launchd service working directory and deployment branch before integrating into the live checkout. Follow the private deployment runbook; keep Railway Course Edge as the tunnel, not a static-site upload target.

Sync/check from the exact committed canonical source, review the bundle receipt, run focused platform checks, and prove repeat-sync stability. Preserve the database, existing courses, submissions, scores, credentials, and unrelated local work. Do not seed/reset, recreate courses, or replace learner records. Verify the actual five-level pages, resources, sign-in flow, and course behavior after release; record runtime/source/deployment identity.

## 4. Complete real learner and control checks

Use the gate rows in release/verification.md and release/level-02-verification.md through release/level-05-verification.md. Perform the checks, fix observed problems, and retest; do not merely restate the checklist.

- On fresh Windows and Mac learner setups, follow the written account/fork/install/launch steps, then test each supported bounded assistant-edit route and the manual fallback. Record real device details and time; CI runners or the maintainer's existing Mac are not substitutes for missing learner-device checks.
- With a designated test learner and synthetic evidence, sign in, open each of the five levels, upload its correct worksheet, reopen the submission and file, and verify saved contents. Keep other learners' data unchanged and test-account details private.
- In a designated user-owned Watchman practice fork, verify baseline, unchanged, changed, repeat without a duplicate issue, controlled failure/recovery, and an actual daily schedule event. Record real run/issue/state receipts. Disable the workflow, set WATCHMAN_ENABLED=false, cancel queued/active runs, wait for final states, and verify the stop controls. Do not substitute local rehearsal or manually triggered events for hosted/scheduled proof.
- Verify document refresh/export/shutdown, partner-observed local-model network isolation where safe, and Front Desk pause during a real request plus a paused zero-request attempt. Keep already-sent request limits explicit. Retain failed/truncated results. Test only supplied public/synthetic inputs and owned targets.
- Rehearse the Level 5 project paths, three-minute presentation and table timing, evidence review, and saved/accessibility fallbacks. Test live cloud routes only when already selected and funded for the pilot; do not add purchases, paid retries, or automatic provider switching.

Record each result as passed, failed, or blocked, with date, exact version, safe receipt, and remaining action. Never invent an observer, device, receipt, schedule tick, cost, or upload. If a physical device, test account, observer, or funded provider is unavailable, name that exact gap and finish the other work. Keep private raw evidence out of public commits.

## Done means

Published source/downloads match their tag and hashes; the website and private course serve the intended version; all available learner/control checks have actual evidence; observed failures are repaired and retested; and any truly unavailable checks are explicitly documented with their required owner action. Update the verification records and short agent change notes. Report what is live separately from what is locally merged or still blocked.

## Out of scope

Do not translate, expand Spanish materials, or require Spanish delivery pilots for this task. Preserve existing Spanish anchors and safety text. Do not add a sixth level, revive retired game/Spellbreaker material, change pricing/paid plans, or reset learner data. The active follow-up is release and verification of the existing five-level English course.
