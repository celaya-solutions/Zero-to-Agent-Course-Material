# Five-Level Course Delivery Record

```text
Document:    Five-Level Course Delivery Record
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      6d44cba0179365263e0d9c3d6253841079fbfe418c0422fcc1f58fbb4c9fb929
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

The five-level English course was published and deployed on 2026-09-06. This record updates delivery status after publication; it does not replace the immutable release tag or its attached files.

## Published version

- Release: [v1.4.0-rc.1](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material/releases/tag/v1.4.0-rc.1), marked prerelease.
- Tagged source: 8492461afdc7e852c3a0f042461e4e8a5c988ac1. Export or reproduce this release from that tag; later documentation commits are maintenance records.
- All 18 attached downloads were fetched anonymously and matched SHA256SUMS.txt; both ZIPs passed integrity checks. Eleven individual PDFs opened successfully, and all 32 distinct embedded source links returned 200 at the versioned tag. All five downloaded slide decks opened and navigated with browser networking disabled.
- All four deterministic project suites passed: 36 document, 43 Watchman, 17 local-model, and 20 Front Desk tests. Both canonical course validators passed. GitHub Course checks also passed for the published commit ([run 34067259776](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material/actions/runs/34067259776)).

## Live delivery

- [Public website](https://zerotoagent.org/course/landing.html): website commit 5423ca918bd4a8262a34becd7ecf5747c2d57a13 reached Railway SUCCESS on deployment 5359a9a2-d763-4c56-acbb-1d7cdab76deb in Landing Page, production, project f2c87ae5-289d-4afa-91e3-9b4310e925b0. All 191 served export files matched the published source receipt.
- Desktop 1280px and phone 390px checks covered paper/night landing rendering and all five 20-slide decks. Keyboard navigation reached slide 20 in every deck; no horizontal overflow or browser errors occurred. Theme screenshots were captured with transitions finished.
- [Private course sign-in](https://learn.zerotoagent.org/auth/users/sign_in): the existing Mac-hosted Rails runtime was updated and restarted successfully; Course Edge was preserved as its tunnel. The runtime bundle identifies source 8492461 and content digest dd3d50c4df9b64e7e2c38815569ccf3dc1ae4d87242c3833810ea7d00ed9d5b6.
- Five old worksheet templates were backed up and replaced with the published worksheets. Existing lesson redirect files already matched. No seed/reset or database writes were performed. Before/after checksums matched for courses, assessments, problems, submissions, scores, and enrollments.
- Thirty-one focused Rails examples and eight standalone checks passed. The focused suite's retired six-level/120-minute expectations were corrected; test data used a separate database and isolated files.
- Live sign-in returned 200 and rendered at phone width; every protected level redirected anonymous requests to sign-in. This proves the access boundary, not authenticated learner behavior.

## Remaining learner gates

These checks are not completed by the deployment. The detailed gate rows in verification.md and level-02-verification.md through level-05-verification.md remain authoritative.

- Authenticated five-level upload/reopen checks: blocked pending a designated test learner account or signed-in test session. The browser was signed out; a username/session request was sent to the owner. Do not impersonate another learner or change passwords.
- Fresh physical Windows and Mac learner setup and assistant-edit routes: no fresh learner devices or pilot participants were supplied for this deployment. Maintainer tests and CI are not physical-device proof.
- Hosted Watchman baseline/change/repeat/failure/recovery, actual daily schedule event, and confirmed stop: no designated user-owned practice fork was supplied. Do not count local tests or manual workflow dispatch as a scheduled event.
- Partner-observed network isolation and the timed Level 5 classroom rehearsal: an observer and learner group are still required. The published saved examples remain authored examples.
- Live funded cloud routes and live-request pause pilots require the selected provider/test setup and actual receipts. This deployment introduced no purchase, paid retry, provider switch, or fabricated result.

Continue the remaining English learner gates when their specific resources are available. Preserve all learner records and existing Spanish anchors; no new Spanish work or Spanish delivery pilot is requested.
