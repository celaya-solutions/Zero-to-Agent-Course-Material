# Preparation - Before Level 1

```text
Document:    Preparation - Before Level 1
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      72b5682e7ea619ba2ddb37da3f8de6a8cfa70af6b0160a042de6eaed4892a494
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Allow 45-90 minutes plus download time. Finish before the 90-minute lesson or attend the setup clinic. You need your own Windows or Mac computer, power, permission to install software, and internet for setup. A phone can read the lesson but cannot run this starter.

## Choose one route at each layer

| Layer | Choices | Why |
| --- | --- | --- |
| Coding helper | [Claude Code or Codex](coding-assistants.md); manual card if access is blocked | Helps you understand and edit the project |
| App answer engine | [Ollama, Claude API, or OpenAI API](models.md) | Answers document questions while the app runs |

A coding-assistant subscription does not automatically supply API credits for this app. You only need the accounts for your selected route. Local Ollama has no per-answer API fee; hardware and electricity still have costs.

## Follow this order

| Step / where | Action | Why | Expected result | Recovery |
| --- | --- | --- | --- | --- |
| 1 / computer settings | Follow your [Windows](windows.md) or [Mac](macos.md) hardware check | Finds incompatible or locked devices early | OS, RAM, disk, and permissions recorded | Use cloud generation if local model cannot run; ask for the setup clinic if installation is blocked |
| 2 / browser | Open [GitHub signup](https://github.com/signup); create or sign into your account; verify the email | A verified account can create a fork | GitHub shows your username | Complete verification or use account recovery before class |
| 3 / GitHub Desktop | [Download](https://desktop.github.com/download/), install, launch, and choose Sign in to GitHub.com; authorize in the browser | Connects the local project to your account | Desktop shows the same username as the browser | Sign out of the wrong account and sign back in |
| 4 / browser | Open [the course repo](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material); Fork; select your personal owner; keep the name; Create fork | Your changes belong to you | Owner is your username and the parent is celaya-solutions | If it says repository not found, the course release is not public yet; contact instructor |
| 5 / Desktop | File > Clone Repository; GitHub.com; select YOUR fork; choose a local folder; Clone. Choose For my own purposes if prompted | Downloads files and keeps pushes aimed at your fork | Local README, pyproject.toml, uv.lock, and projects folder exist | Refresh the repo list or use the URL tab with your fork URL |
| 6 / terminal | Follow your OS guide to install uv, reopen the terminal, and open the clone's root | Commands need the course folder | uv --version works; directory listing contains pyproject.toml | Follow the matching PATH or folder recovery step |
| 7 / terminal | Run `uv sync --frozen` | Creates the locked Python environment | Dependencies install; no lockfile changes | Recheck network and free disk; copy the error category for the instructor |
| 8 / chosen assistant | Complete [coding-assistant setup](coding-assistants.md) and open this clone | Makes a guided edit possible | Assistant explains README without edits | Use the manual edit card if account access is blocked |
| 9 / terminal | Complete [model setup](models.md), then `uv run --frozen zta setup` | Selects the app's one answer engine | Provider and model are shown, key is never printed | Rerun setup to correct the selection |
| 10 / terminal | `uv run --frozen zta doctor documents` | Checks parsing and provider reachability | PASS lines; any NOTE is read | Match the issue in [Recovery](recovery.md) |
| 11 / terminal and browser | `uv run --frozen zta start documents`; open http://127.0.0.1:8501; load binder, build index, fill predictions, run question 1 | Confirms real generation and billing, beyond connectivity | Answer cites El Paso source; no service error | Use provider recovery; never infer billing access from model-list access alone |
| 12 / course platform | Follow [submission setup](submission.md); find Level 1 upload control | Avoids last-minute enrollment problems | Assignment opens as a student | Resolve sign-in, enrollment, or closed assignment before class |
| 13 / browser | From [Releases](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material/releases), download learner-materials ZIP; extract it using Finder or Explorer; open lesson and saved-example PDFs | Keeps teaching material available offline | Both PDFs open with network off | Use included Markdown/text if a PDF reader fails |

## Preparation receipt

Write your OS, RAM, free disk, coding assistant, provider, model, doctor result, practice-answer result, and assignment access in the setup clinic sheet. Do not write a key. Preparation is complete only after an actual answer and access to the upload control.

The 16 GB RAM / 10 GB free-storage target is a planning target, not a tested guarantee for every device. Use the release verification report to see the actual pilot hardware. Hardware and download delays do not lower your learning grade.
