# ZERO TO AGENT: Project Lab

Five ninety-minute meetings. Four required projects. One final presentation.

This is a standalone, shorter course for a room that may include a person opening a chat tool for the first time and a person who already writes software. Everyone completes the same core proof. Experienced builders may complete the builder extension, but extra code never replaces clear evidence.

## Course map

| Level | Project | What leaves the room |
| --- | --- | --- |
| 1 | Your Documents Answer Back | A forked custom document app, five tests, two source checks, one committed improvement, and private proof |
| 2 | The Night Watchman | A scheduled page check, a log, an alert, and a tested off switch |
| 3 | Nothing Leaves the Building | A local model that answers offline, a benchmark, and a named rule set |
| 4 | The Front Desk, Attacked and Locked | A tested business desk, message card, ten-attack before-and-after sheet, four applied defenses, and one-minute pitch |
| 5 | Choose, Improve, and Present | One improved project, costed, presented to the class with normal, failure, and fallback proof |

Before Level 1, complete [Preparation](../../preparation/README.md). Use your own Windows or Mac computer. Choose Claude Code or Codex for editing and Ollama, Claude API, or OpenAI API for answers. A manual card and saved runs cover blocked accounts.

## Required files in every level

- level.yml: the contract for the level.
- student.md: the learner lesson and three tasks.
- instructor.md: the 90-minute run sheet, grading guide, and recovery routes.
- worksheet.md: the fillable evidence trail.
- slides.html: an accessible, printable 20-slide deck in the Zero to Agent visual system.
- assets/: safe practice material and an outage route.

## Mixed-experience rule

The core route is the passing route. It can be completed with templates, a browser, and a partner where noted. The builder extension exposes more of the code, hosting, or automation. A learner does not fail because another learner wrote more code.

Helpers use three moves: ask what the learner expects, point to one next step, then give the controls back. A helper never takes over the keyboard, account, or decision.

## Language release

English is the source edition. Phase 1 includes Spanish anchors, safety stops, and navigation in every learner-facing level. Full Spanish learner lessons and worksheets are Phase 2. Spanish instructor materials and decks follow a bilingual pilot in Phase 3. See _shared/language-plan.md.

## Real case study, safe records

Celaya Solutions Research is the shared case. Its identity, location, public contact route, and public work are taken from its official website. The class never invents internal policies, client facts, prices, or promises and presents them as real. Any record written for an exercise is headed TRAINING-ONLY SYNTHETIC RECORD.

Learners may replace the case with their own business or an owner-approved business only after the instructor confirms the public/private boundary. Cloud practice uses only public or synthetic records. Private records stay local.

## Teaching and release boundary

This is the one course. The earlier twelve-level and eight-week drafts are kept under archive/ for history and are not taught.
The canonical authoring home is https://github.com/celaya-solutions/Zero-to-Agent-Course-Material. This directory is the source for generated website and private-platform copies.
The platform copies this directory with its `zta:sync_content` task, then checks
the copy before it can be committed. Syncing files does not change the live
course database or the Course Edge service. A public release may deploy this
repository only to the Railway Landing Page service after a local pilot, merge
approval, and a fresh browser check.

## Build and validation

Run:

    ruby scripts/build_project_lab_pdfs.rb
    ruby scripts/build_project_lab_slides.rb
    LANG=en_US.UTF-8 ruby scripts/validate_project_lab.rb
    python3 -m http.server 4173

Then open /courses/project-lab/ and at least one lesson PDF and slide deck in a browser.
