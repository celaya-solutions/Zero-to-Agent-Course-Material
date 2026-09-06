# Course Access and Private Submission

```text
Document:    Course Access and Private Submission
Version:     v1.1.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      567a3d114191e99b563de8c09e183872e4ab35be0960d480662856689ee498ad
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Code changes go to your GitHub fork. Evidence goes to the course platform. The export is one Markdown file; no ZIP or public chat link is needed.

| Where | Action | Why | Expected result | Recovery |
| --- | --- | --- | --- | --- |
| Browser | Open https://learn.zerotoagent.org/auth/users/sign_in | Uses the branded course entry | Sign-in form appears | If unavailable, keep local work and report the access block |
| Sign-in form | Use your existing course login; if invited for the first time, finish the password-setup link from the enrollment email | Activates the correct learner identity | Course dashboard appears | Use password recovery or ask the instructor to resend enrollment; never share a password |
| Course list | Open Zero to Agent / ZTA; if absent, complete the course join flow with the code the instructor gives privately | Enrolls the correct account | The five-level course is visible | The instructor resolves missing enrollment; no course access code is published in this repo |
| Course assessments | Open Level 1 - Your Documents Answer Back | Opens the graded activity | File-upload control and submission instructions appear | Tell instructor if the assignment is closed or the title is from a retired course |
| Local app / Proof | Complete the checklist and click Export PROJECT-LAB-01.md | Creates a portable record of the work | Browser downloads a nonempty Markdown file | Allow this download or export again; it does not upload automatically |
| Level 1 upload | Choose file; select PROJECT-LAB-01.md; read/complete any displayed integrity acknowledgment; click Submit | Sends evidence privately | Confirmation and submission-history entry appear | Read the error; keep the local file if the service is unavailable |
| Submission history | Open the latest entry and view/download the submitted file; compare the nickname, final commit, and last run | Verifies receipt and contents | Correct file and timestamp are visible | Resubmit the corrected file if needed; a download alone is not a receipt |

The private platform is maintained separately. A real student-account upload pilot is a release gate; screenshots and the exact observed navigation are recorded in release/verification.md. Do not use an instructor-only page as proof that students can upload. Personal enrollment links/codes and student files never belong in this public repo.

## Level 2 submission

Use the same sign-in and course-list steps, then open **Level 2 - The Night Watchman**. Its evidence file is `.zta/PROJECT-LAB-02.md`, created by `zta prepare watchman` and completed in a text editor. Use the upload control's file picker, navigate to the course clone's `.zta` folder, and select that file. On Mac the file picker can open the folder with Command+Shift+G and the actual folder path; never paste a sample path. On Windows type the actual `.zta` folder path in the file picker's address bar.

Submit, open the resulting entry, and view/download the file. Compare your nickname, final run link, and off-switch evidence. Record the receipt privately. A missing Level 2 form or inaccessible student account remains a block, not a reason to publish the worksheet. A real Level 2 student-account upload/reopen pilot remains required in `release/level-02-verification.md`.
