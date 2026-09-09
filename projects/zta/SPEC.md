# One Project, Four Rooms: Merging the Project Lab into a Single Nested Build

```text
Document:    One Project, Four Rooms
Version:     v1.1.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-09
SHA256:      5d426e44a6f21812f9d670ed30ae7442f0163cb7695d20359201d6150d6b16f2
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

**Where this lives.** The plan was drafted from the website checkout, which holds a generated
copy of the course. The code it describes has only ever lived in this repository, the
canonical course repository, so this is where Phases A and B land. Read every "this
repository" below as this one.

**Status.** Phase A is landed and verified here. Phase B is written but not started; it is
held behind two decisions in section 11. Phase C is level material and belongs with the
lesson rewrites. Section 2 describes the tree before Phase A and is kept as the record of
what was wrong.

## 1. What was asked

Turn the Project Lab curriculum into one project with the others nested inside it,
as a single application, replacing the four standalone project apps, living in this
repository under `projects/`.

## 2. What is actually there today

The merge is roughly sixty percent built already, in a shape that will not scale.

One package, one command, one data directory already exist:

- `pyproject.toml` at the repository root builds one distribution, `zero-to-agent-course`.
- One console script, `zta`, dispatches every project.
- One ignored data directory, `.zta/`, holds all learner evidence.
- One provider layer in `zta.storage` and `zta.providers` is shared by all four.

Four things block calling it one project:

1. **The shared package lives inside one of the four projects.** It is at
   `projects/documents/src/zta/`. Documents is both a peer and the landlord. Every other
   project reaches into it, and `pyproject.toml` sets `where = ["projects/documents/src"]`.
2. **The other three are loose scripts, not modules.** `watchman/watch.py`,
   `local-models/lab.py`, and `front-desk/desk.py` are run as files by `subprocess`, each
   recomputing the repository root with `Path(__file__).resolve().parents[2]`. Moving any
   file breaks asset resolution silently.
3. **The command grammar grew per project.** `cli.py:main` accepts a flat verb list
   (`setup doctor start test prepare offline benchmark create check callers attacks lock
   pause resume`) and then guards each verb against the wrong project with hand-written
   errors. Every new capability adds a global verb and a new guard.
4. **There are two front doors.** Documents serves Streamlit on port 8501, the front desk
   on 8504, and the watchman and model lab are terminal only. A learner in Level 4 has no
   view of the work they did in Level 1.

The consequence in the classroom is Level 5. Its passing standard is "choose one course
project," because nothing joins them. The learner ends the course holding four artifacts
and no system.

## 3. The idea

The building metaphor is already in the course and was never named. Level 2 is The Night
Watchman. Level 3 is Nothing Leaves the Building. Level 4 is The Front Desk. Level 1
answers from the records. Those are four rooms of one small business, not four projects.

So: one application, one shell, four rooms.

| Room | Level | Nested module | What it does for the business |
|---|---|---|---|
| Records | 1 | `documents` | Answers questions from your own files, with page receipts |
| Night watch | 2 | `watchman` | Checks one thing on a schedule and only speaks when it matters |
| Private wing | 3 | `local-models` | Runs a model on your machine with the network off |
| Front desk | 4 | `front-desk` | Talks to outsiders, gets attacked, gets locked |
| Proof board | 5 | `proof` | Reads the workbook and shows what is proven and what is not |

Level 5 stops being "pick one of four" and becomes "improve one room of the shop you
built, and prove the whole building still runs." That is a stronger night and a better
demo, and the eight proof items already written for Level 5 become a screen instead of a
worksheet transcription exercise.

**Open decision for Chris.** The umbrella needs a course-facing name. Candidates: The
Shop, The Back Office, The Building. Package and command stay `zta` either way. Nothing
below depends on which is picked.

## 4. Target layout

```
projects/zta/                     the one project
  src/zta/
    __init__.py
    cli.py                        one dispatcher, uniform grammar
    shell.py                      one Streamlit app, one port, five pages
    registry.py                   module discovery and the Module contract
    core/
      storage.py                  promoted out of documents, unchanged behavior
      providers.py                promoted out of documents
      evidence.py                 one workbook, five sections
      controls.py                 pause, resume, stop, and the control log
      receipts.py                 one run-receipt schema for every room
    modules/
      documents.py
      watchman.py
      localmodels.py
      frontdesk.py
      proof.py
  tests/
    core/                         shared behavior
    modules/                      one folder per room, existing tests move here
```

`projects/documents`, `projects/watchman`, `projects/local-models`, and
`projects/front-desk` are removed. Their assets stay where they are, under
`courses/project-lab/level-0N/assets/`, resolved through `storage.root()` only. No module
computes a path from `__file__`.

`pyproject.toml` changes one line: `where = ["projects/zta/src"]`.

**What Phase A actually produced.** `projects/zta/src/zta/` and `projects/zta/tests/` exist
and are the package's home. The four room directories still hold their own scripts, tests,
READMEs and settings; removing them is Phase B, once each is a module.
`projects/documents/settings.toml` stays where the Level 1 lesson sends the learner, and
`storage.settings()` still reads it from there. Making that the documents module's own
config is a Phase B change, and it is the last piece of the landlord problem.

## 5. The nesting contract

A room is a Python module in `zta.modules` exposing one `Module` object. This is the whole
extension point. Nothing else in the system knows the room names.

```python
Module(
    slug="front-desk",
    title="The Front Desk",
    level=4,
    milestone="Sell the outcome, not the robot. Fences, not promises.",
    engines=("ollama",),          # which answer engines this room accepts
    network="local-only",         # local-only | scheduled | learner-choice
    prepare=...,                  # copy assets and worksheet, never overwrite
    doctor=...,                   # readiness checks, returns pass/note/fail rows
    page=...,                     # renders this room inside the shell
    tasks={"callers": ..., "attacks": ..., "lock": ...},
    evidence=(...,),              # proof items this room must produce
    stoppable=True,               # participates in the global stop switch
)
```

Three rules the registry enforces:

- **Isolation.** A room that fails to import, or whose doctor fails, is shown in the shell
  as unavailable with the reason. The other four keep working. This protects the
  instructor fallbacks: a broken Ollama on one night must not take the whole building down.
- **Engine capability is per room, not global.** Documents accepts Ollama, Claude, or
  OpenAI. The front desk and the model lab are local only. The watchman needs no model.
  The shell shows the engine each room will actually use, so "nothing leaves the building"
  stays a visible property rather than a claim.
- **One stop switch.** `controls.py` generalizes the existing `front-desk/control.json`
  (phase, enabled, revision, appended control log). `zta pause` with no argument pauses
  every stoppable room and writes one log line per room. Level 5 asks for a tested stop or
  fallback; this makes that one action and one receipt.

## 6. Command grammar

Universal verbs, every room, no guards:

```
zta setup                 choose the answer engine once
zta doctor [room]         readiness, all rooms or one
zta start [room]          open the shell; with a room, open on that page
zta prepare [room]        lay down assets and worksheets, never overwriting
zta test [room]           pytest for one room or all
zta status                what is running, what is paused, what is proven
zta pause  [room]         stop switch, all rooms or one
zta resume [room]
zta evidence              print the proof board to the terminal
```

Room-specific work moves behind one verb instead of growing the global list:

```
zta run front-desk attacks
zta run local-models benchmark
zta run watchman round
```

Old commands (`zta attacks front-desk`, `zta benchmark local-models`, and the rest) are
kept as deprecated aliases for one release, printing the new form. Printed commands appear
in worksheets and PDFs that learners already hold.

## 7. The shell

One Streamlit app, port 8501, five pages in the left nav plus a persistent header.

The header is the teaching surface and is visible on every page:

- Engine in use for the current room, and whether it is local or cloud.
- Network state: local only, or the named outbound host.
- Running or paused, with a Stop control that hits every room.
- Cost so far this session, from the existing usage and cost fields in the provider layer.

The Proof board page reads the workbook and renders the eight Level 5 items with the
labels the course already requires: live, saved, authored example, not performed. It never
invents a verdict. The learner types the verdict; the board shows what is missing.

Port 8504 disappears. Doctor's port check, the preparation guide, and every printed URL
must be updated in the same change.

## 8. Migration, in three shippable phases

**Phase A. Move the package. No learner-visible change. Done.**
Moved `projects/documents/src/zta` to `projects/zta/src/zta` and its tests to
`projects/zta/tests`. Repointed `pyproject.toml` and `testpaths`. Removed all four
`parents[2]` computations. Every command, port, worksheet path and evidence path is
unchanged. The 116 existing tests pass unchanged and 14 layout guards were added. Three
documents named a moved file and were corrected together with their PDFs and header
hashes: the Level 1 builder extension, `projects/documents/README.md`, and the repository
layout list in `README.md`. Section 12 records what was verified.

**Phase B. Nest the rooms.**
Introduce `registry.py`, the `Module` contract, `controls.py`, `receipts.py`, and
`shell.py`. Convert the four scripts into modules. Add the uniform grammar with aliases.
Merge the two Streamlit apps into one. Existing per-room tests move under
`tests/modules/` and keep asserting the same behavior; new tests cover isolation, the
global stop, and per-room engine capability.

**Phase C. Rewrite the levels.**
Level text moves from "tonight we build project X" to "tonight we open room X of the shop
you started in Level 1." Level 5 changes from choosing among four projects to improving one
room and proving the building. Slides and PDFs regenerate. Validators update.

Phases A and B are code in this repository. Phase C is course material and cannot be done
here. See the next section.

## 9. Traps and constraints, found while reviewing

1. **The website carries a generated copy of `courses/project-lab/`.** A level rewrite made
   in the website checkout is overwritten by the next export. Phase C lands here and
   reaches the website through `scripts/export_course.py`, which writes the
   `course-material-source.json` receipt. The prerequisite this section originally named -
   a canonical `main` that carried only `projects/documents` - is resolved: `859f6a6`
   carries all four rooms at version `1.4.0rc1`, and Phase A ran against it.
2. **v1.4.0-rc.1 is published with downloads and checksums, and its live gates are still
   open.** AGENTS.md forbids recreating the published tag, and learner setup, upload and
   reopen, watchman schedule, and Level 5 rehearsal checks are still outstanding. This work
   is v1.5.0. Recommendation: do not disturb the release candidate until its verification
   record is closed, or the open gates can never be attributed.
3. **`.zta/` layout changes break a cohort mid-course.** Today evidence sits at
   `.zta/PROJECT-LAB-02.md`, `.zta/front-desk/PROJECT-LAB-04.md`, `.zta/local-models/`, and
   `.zta/watchman/`. One workbook means either a migration step in `prepare`, or a clean
   cutover between cohorts. Cutover is cheaper and safer. Decide before Phase B.
4. **Assets are addressed by level, not by room.** `desk.py` reads
   `courses/project-lab/level-04/assets`. If a room is ever taught at a different level,
   that path is wrong. The `Module` should carry its asset directory explicitly.
5. **`scripts/validate_project_lab.rb` asserts the five-level shape and a fixed list of
   asset paths.** It does not assert `projects/` layout, so Phases A and B pass it
   untouched. Confirmed: it passed unchanged before and after Phase A, as did
   `scripts/validate_materials.py`.
6. **Fallbacks must survive the merge.** Every level ships paper and saved-run fallbacks
   for learners whose machine or network fails. The shell must render a room in fallback
   mode rather than hiding it.
7. **The published passing standard names four projects.** `course.yml` reads "Complete all
   four projects, then improve and present one project." Phase C changes that sentence, and
   it is quoted in the landing page, the rubric, and the certificate path. Grep before
   editing.
8. **`watch.py` must keep running with the standard library alone.** The installed workflow
   runs `python projects/watchman/watch.py --github` on a bare `actions/setup-python` job:
   no `uv sync`, no course package. Importing `zta` unconditionally there turns every
   scheduled round into a `ModuleNotFoundError`, and the learner sees a red run rather than
   a missed check. Phase A left it importing `zta.storage.root` when the package is present
   and falling back to the same marker walk when it is not;
   `tests/test_layout.py::test_watchman_runs_without_the_course_package` runs the file under
   `python -S` to hold that. A watchman module in Phase B inherits this constraint: the
   scheduled entry point cannot depend on the shell, the registry, or anything installed.

9. **Two engines, three privacy stories.** Documents may send selected passages to Claude or
   OpenAI. The private wing exists to prove nothing leaves. Putting both in one shell makes
   the contrast teachable, but only if the header never shows a stale engine. Treat the
   header as safety copy, not decoration.

## 10. What I recommend

Land Phase A now, as its own change, while the v1.4.0-rc.1 gates stay open. It is
invisible to learners, it removes the landlord problem and the four `parents[2]`
computations, and every later phase gets cheaper. Hold Phase B until the release candidate
closes. Start Phase C only in the canonical repository, and only after the umbrella name is
picked.

## 11. Open questions for Chris

1. Umbrella name: The Shop, The Back Office, The Building, or something else.
2. `.zta/` migration or clean cutover between cohorts.
3. Should Phase C wait for the v1.4.0-rc.1 verification gates to close, or run in parallel
   in the canonical repository.
4. Does the merged shell keep a terminal-only route for every room, for the venue-wifi and
   borrowed-laptop learners.

## 12. Phase A record

Landed on `codex/one-project-four-rooms` and merged to `main`. Reversible as one commit.

The merge met a concurrent rebuild of the Level 1 app on Gradio (`b6b4075`). Both sides
were kept: that rewrite's screen, launch command and tests, and this move's package
location. `projects/documents/README.pdf` was rebuilt, which also picked up the
Streamlit-to-Gradio wording that commit had left only in the Markdown.

Verified in the worktree, on macOS with Python 3.12.13:

- 130 tests pass: the 116 that existed before, unchanged, plus 14 new layout guards.
- `zta test documents`, `zta test watchman`, `zta test local-models` and
  `zta test front-desk` each pass, with the same counts as before the move
  (36, 43, 17, 20).
- `zta doctor watchman` passes. `zta doctor front-desk` passes against a live local
  `gemma3:4b`. `zta doctor local-models` reports `gemma3:1b` missing, which is true of this
  machine and was true before the move; reaching Ollama at all proves asset and endpoint
  resolution survived.
- `ruby scripts/validate_project_lab.rb` and `python scripts/validate_materials.py` both
  pass, including the header hashes of the three edited documents.
- `ruby scripts/build_project_lab_slides.rb` rebuilds all five decks byte for byte
  unchanged, so no deck quoted a moved path.
- Rebuilding every PDF changed the text of exactly the three edited documents; the other 72
  differed only in their embedded timestamps and were restored, so the commit carries no
  PDF churn.
- Upgrade path: a clone synced at `859f6a6`, then given this change, rebuilds its editable
  install on the next `uv run --frozen zta test` and passes. No manual re-sync, no
  instruction to add to the preparation guide.

Left open by Phase A, deliberately:

- The published v1.4.0-rc.1 downloads still carry the old wording of the Level 1 builder
  extension and the documents guide. The tag and its checksums are untouched, as required.
  Anyone closing the remaining v1.4.0-rc.1 learner gates should work from the published
  download and expect that one pointer to name `projects/documents/src/zta/documents.py`,
  which is where the file was at that tag.
- `storage.settings()` still reads `projects/documents/settings.toml`, so core still knows
  one room by name. Phase B removes that.
- `projects/documents/` now holds a README and a settings file and no code. It stays until
  Phase B turns it into `zta.modules.documents`.
- The distribution version is still `1.4.0rc1`. `zta doctor` prints it and the PDF footer
  carries it, so bumping it is a learner-visible change and belongs with the release that
  ships Phase B, not with a package move.
- The website's generated copy was not refreshed. It is pinned to the published
  v1.4.0-rc.1 content, and re-running `scripts/export_course.py` against it would put
  post-release material on the live site. The three edited documents reach the website
  with the next intended export, not with this change.
- A pull leaves ignored build artefacts behind at the old address:
  `projects/documents/src/zta/__pycache__` and the stale
  `zero_to_agent_course.egg-info`. Python will not import from them, since no `.py`
  file remains, and `uv run --frozen` rebuilds the editable install at the new
  address. They are safe to delete and need no learner instruction, but the layout
  guard asserts "no Python source under `projects/documents`" rather than "no
  directory", so a learner's leftovers never fail their test run.
