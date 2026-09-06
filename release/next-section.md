# Continue with Level 2: The Night Watchman

```text
Document:    Agent Handoff — Level 2: The Night Watchman
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      0b485d7d9a9761669743af9ac6fbf25778859d5a5bcc83bfa737785dc7e0355a
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

## Resume here

The next course section is **Level 2: The Night Watchman**. This handoff prepares the next implementation task; it does not start a watcher, create a schedule, or publish another release. Keep the course at five levels and 90 minutes per meeting, with required preparation before class.

Canonical repository: [Zero-to-Agent-Course-Material](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material). The original website and private Rails platform are generated consumers, not authoring locations. The repository root used for this work is the isolated checkout named `Zero-to-Agent-Course-Material` under the website workspace's `.worktrees/` directory.

### Starting state, checked 2026-09-06

| Item | Exact state | Consequence for the next agent |
| --- | --- | --- |
| Local authoring branch | `codex/level-1-documents`; latest application change `0904c94` | Continue from this branch's current tip, including this handoff commit. |
| Published source | Remote `main`, remote `codex/level-1-documents`, and tag `v1.0.0-rc.1` all resolve to `3203f04` | The public release does not contain the later readability fixes or this handoff. Recheck remote refs before a future push. |
| Local `main` | Still points to the initialization commit `f38ccdc` | Do not use this stale local branch as the Level 2 base. |
| Unpublished app fixes | `7c291a4`, `f0949d1`, `0904c94` | Preserve the final shared cream/sage palette, paired widget colors, and readable source cards. Do not restore the earlier mixed light/dark styling. |
| Website review checkout | Sibling `../course-material-site`, branch `codex/course-material-source`, commit `f4cf49b` | Committed locally; not merged or deployed. Its generated copy identifies source `3203f04`. |
| Private-platform review checkout | Sibling `../course-material-platform`, branch `codex/course-material-canonical`, commit `a83611aa` | Committed locally; not merged or deployed. Preserve submissions and the guarded source/hash checks. Never copy its private source into this repository. |

The sibling paths above describe this maintainer workspace, not a learner installation. The parent website's checkout and unrelated uncommitted files were preserved. Do not copy, clean, reset, or merge them as part of resuming.

From the canonical checkout, inspect status and create the next worktree from the current authoring branch:

```sh
git status --short
git fetch origin
git worktree add ../Zero-to-Agent-Level-02 -b codex/level-2-night-watchman codex/level-1-documents
```

Run these only when starting Level 2 implementation. If that branch or destination already exists, inspect and reuse the correct worktree; do not overwrite it. Install its own locked environment with `uv sync --frozen`; do not symlink another worktree's environment. Use graft before inspecting or changing code.

## What Level 1 already provides

- Runnable Python/Streamlit document helper under `projects/documents/`, with SQLite search, source receipts, Ollama/Claude/OpenAI adapters, persistent private progress, and Markdown evidence export.
- Working `zta setup`, `zta doctor documents`, `zta start documents`, and `zta test documents` commands. No watcher CLI command exists yet; do not document one as available before implementing and testing it.
- Shared Windows/macOS preparation, assistant choices, manual editing route, learner/instructor materials, five decks, generated PDFs, saved examples, and versioned download tooling.
- Thirty-six deterministic app checks passed. The recorded Ollama pilot passed all five questions. Hosted Windows/macOS checks passed for the published candidate; later UI changes were checked locally.
- The final UI uses a fixed course palette across all screens, including labels, buttons, menus, source cards, alerts, and inline code. Browser checks with both light and dark framework defaults found a minimum checked text contrast of 6.12:1; passage text was 13.43:1. Source cards were visually checked at 887 × 1087.

At this handoff the document app was running at `http://127.0.0.1:8501/` from the authoring checkout. Treat this as a transient session, not an always-on service. Check port ownership before stopping or restarting it. Local `.zta/` contains maintainer pilot progress; preserve it and keep it out of Git. It is not a real student submission receipt.

The published [release candidate](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material/releases/tag/v1.0.0-rc.1) is not classroom-certified. [Level 1 verification](verification.md) still requires actual minimum-hardware Windows/Mac setup, fresh assistant-login/edit paths, live Claude/OpenAI pilots, and authenticated student upload/reopen. Do not mark those complete based on unit tests or this handoff. Do not rewrite the existing tag to include later fixes.

## Read these Level 2 sources first

1. [Level contract](../courses/project-lab/level-02/level.yml).
2. [Learner lesson](../courses/project-lab/level-02/student.md), [instructor run sheet](../courses/project-lab/level-02/instructor.md), and [worksheet](../courses/project-lab/level-02/worksheet.md).
3. [Starter map](../courses/project-lab/level-02/assets/starter/README.md), [watcher](../courses/project-lab/level-02/assets/starter/watch.py), [workflow template](../courses/project-lab/level-02/assets/starter/watch.yml), and [existing tests](../courses/project-lab/level-02/assets/starter/test_watch.py). Audit the code through graft before adopting or moving it; it was migrated, not re-piloted in the Level 1 release.
4. [Controlled practice page](../courses/project-lab/level-02/assets/practice-page.html) and [saved three-run packet](../courses/project-lab/level-02/assets/fallback-three-runs.md).
5. [Shared course manifest](../courses/project-lab/course.yml) and [maintainer build/release instructions](maintaining.md).

There is no `level-02/README.md`; `student.md` is the learner entry. Keep the existing `courses/project-lab/level-02/` URLs. Put the maintained runnable watcher under `projects/watchman/`; make old starter paths generated copies or clear links so there are not two editable implementations.

## Required Level 2 outcome

Build a small watcher using **GitHub Actions** for the hosted route. It reads the supplied public practice page, extracts the stable `watch-value` status, compares it with saved state, records a dated decision, and creates one useful repository issue for a meaningful change. Keep the existing baseline → unchanged → `OPEN` to `PAUSED` exercise. A learner must use the off switch and show what happened after disabling the workflow. Railway remains a written optional extension, not a deployment requirement.

The six-line learner spec names the address, signal, meaningful-change rule, trigger, alert, and never list. Required evidence is the spec, predictions written before each run, baseline/unchanged/changed receipts, old/new values in the issue, dated logs, an honest verdict for each run, and the observed disabled state. Use a private `PROJECT-LAB-02.md` submission through the course platform; public code belongs in the learner's own fork. A repository issue is the assessed alert; email delivery is not a pass requirement.

Resolve inherited inconsistencies before teaching: the starter map currently says to create a separate practice repository and put files at its root, while the approved course uses a shared learner fork and separate project folders. Choose the actual learner-fork paths, explain the full workflow installation and default-branch steps, and update every matching lesson, template, test, and saved example. Clearly distinguish the explicitly allowed practice issue from the never-list prohibition on posting elsewhere.

Each learner needs their own suitable computer for the live course route. Partner, paper, and saved-run participation must be labeled as fallback evidence, not proof that the learner launched their own project. Reuse the shared GitHub/assistant preparation instead of requiring another set of accounts.

## Implementation and teaching sequence

| Where | Action | Why | Expected result | Recovery if it fails |
| --- | --- | --- | --- | --- |
| New isolated Level 2 checkout | Audit the inherited watcher, workflow, tests, persistence, and starter map. | Determine what already works before changing it. | A concrete gap list and one maintained project layout. | Record the failing case; keep the inherited files until the replacement is reviewed. |
| Official GitHub documentation | Verify current fork/Actions setup, default-branch requirements, permissions, scheduling delays/UTC, issue behavior, and disable controls. | These product details can change. | Exact URLs and accurate UI steps with a verification date. | Record access or policy limits and provide the saved-run route. |
| `projects/watchman/` and workflow template | Implement and test stable extraction, persisted baseline, bounded fetches, change handling, failure logging, and duplicate-alert prevention. | A failed fetch must not become a false change or erase good state. | Deterministic baseline/unchanged/changed/failure/repeat behavior. | Repair the specific failure before claiming the hosted route passes. |
| Learner fork setup | Make workflow installation and enabling explicit; use scoped `GITHUB_TOKEN` permissions and no pasted personal token. | Keep authority understandable and confined to the practice repository. | Learner can identify what may read, write state, and create an issue. | Explain the exact policy/permission block; do not silently broaden permissions. |
| Level 2 teaching files | Expand preparation and the 90-minute walkthrough using Where → Action → Why → Expected result → Recovery for each step. | A new learner must not need an unwritten instruction. | OS-specific folder/edit/run steps, both assistant prompts, a manual card, worksheet, rubric, instructor answer key, and complete saved examples. | Walk the instructions literally and fill the missing step. |
| Controlled local tests and approved practice fork | Test baseline, unchanged, meaningful change, irrelevant page change, missing signal, fetch failure, state/issue failure, rerun, and stop behavior. | Check useful alerts and reliable boundaries. | Redacted evidence clearly separates local fixtures from real hosted results. | Save the failure and diagnose it; do not call an error “no change.” |
| Browser and course test account | Verify the real run, issue/log views, off switch, and private Markdown upload/reopen. | Source files alone do not prove the learner workflow. | Exact controls, screenshots where useful, and a real submission receipt. | Keep blocked gates explicit and provide saved examples after two attempts or five minutes. |
| Course build and separate consumer worktrees | Regenerate affected decks/PDFs/downloads, run validators, and review generated consumer changes. | Keep one canonical course with five 90-minute levels. | A committed, versioned candidate with matching artifacts. | Fix source first; do not hand-edit generated copies or merge/deploy as cleanup. |

Watch only the supplied page or a page the learner controls. Keep the schedule conservative and documented; do not promise exact scheduled execution times. No private-page access, personal tracking, login bypass, arbitrary action execution, or automatic purchases/replies/spending. Hosted pilots and schedules must be intentionally started in the designated practice fork and disabled after the test. Do not add autonomous messaging outside that project.

## Checks and stopping point

Follow [the release commands](maintaining.md) after course edits: update headers, regenerate slides/PDFs, run both material validators, and package from the allowlist. Keep `uv run --frozen zta test documents` passing as the Level 1 regression check. Define and document the watcher test command only after the actual project layout is settled; the inherited starter currently uses `python -m unittest test_watch.py` from its own folder.

Level 2 is ready for review when a fresh learner can follow one supported route through setup, all three runs, the alert and log, a tested off switch, and private submission without an unwritten instruction. Record setup/run timing without grading machine speed. Saved examples must identify themselves as saved examples. Keep unperformed pilots open and do not claim a release complete solely because its code checks pass.

Commit the finished implementation and a brief change note. Refresh generated consumers separately and preserve student data. Merging, changing the public release, and live deployment remain separate release actions requiring the user's instruction. Do not start Level 3, revive retired curricula, or rewrite the alternative-project catalog as part of Level 2.
