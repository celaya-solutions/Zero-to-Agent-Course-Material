# Level 1 - Manual Edit and Commit Card

```text
Document:    Level 1 - Manual Edit and Commit Card
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      6e1ecc4b29b7bc430592e233072d44e6ee59d4579370318f0801f43a753a0c5b
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Use this card with Claude Code, Codex, or a plain-text editor. The learner owns the change and judgment.

| Where | Action | Why | Expected result | Recovery |
| --- | --- | --- | --- | --- |
| GitHub Desktop | Confirm the current repository is YOUR fork. Choose Current branch > New branch, name it codex/level-01, create it, and publish the branch to your fork | Keeps the class edit separate from the starting version | Branch name and your fork owner are visible | Switch back if you opened the course owner's repository |
| Finder/Explorer | Open projects > documents > settings.toml using a text editor | This is the small learner-editable configuration | You see max_passages and show_source_quotes | On Mac use TextEdit in plain-text mode; on Windows use Notepad; preserve .toml extension |
| Editor | For a controlled miss, replace only `max_passages = 4` with `max_passages = 1`; save | Hides some evidence in a measurable way | File contains one passage setting | If format error appears, restore the exact original line |
| Browser | Refresh the app; confirm sidebar shows 1 passage; rerun question 5; inspect retrieved records | Tests the changed evidence window | Only one passage is available | If sidebar still shows 4, save the file in the correct clone and refresh |
| Editor and browser | Restore `max_passages = 4`; save, refresh, rerun question 5 | Repairs evidence coverage | Both training records can appear | Compare actual retrieved passages rather than demanding one model wording |
| Editor | Change `show_source_quotes = false` to `show_source_quotes = true`; save | Leaves a useful visible improvement to commit | Supporting quotes will appear below answers | Use lowercase true without quotation marks |
| Browser | Refresh; rerun the same question; save Before and After in Improve | Records the effect | Same question with visible source quotes | Choose the correct runs by time and ID |
| Terminal at course root | `uv run --frozen zta test documents` | Checks application behavior without paid model calls | All deterministic tests pass | Record any failure and ask for help; do not weaken the tests |
| GitHub Desktop | Inspect Changes. Select only the intended project edit. Ensure max_passages is 4 and show_source_quotes is true | Keeps experiments and private files out of the commit | Small settings diff; no .zta or evidence | If .zta appears, stop and fix ignore rules before publishing |
| GitHub Desktop | Enter summary Show source quotes for Level 1. Click Commit to codex/level-01, then Push origin | Saves the improvement to your own account | Desktop reports no outgoing commits | Complete account authentication if requested |
| Desktop History | Select the new commit; use View on GitHub from its menu; copy the browser URL. Copy your fork's main repository URL too | Provides exact ownership and version receipts | URLs go into Proof fields | Verify owner is your username before submitting |

Do not open a pull request into the instructor's repository for routine homework. Do not merge your branch during the lesson. Your commit URL is the handoff. Never commit PROJECT-LAB-01.md or anything inside .zta/.

## After editing Python rules

Settings-only edits take effect after saving and refreshing the browser. If the edit changes a `.py` file, return to the app's terminal, press Ctrl+C, run `uv run --frozen zta start documents` again, and refresh the browser before rerunning the same question. This starts the changed code. Your saved expectations and runs remain in `.zta/`. If a stale-import error appears, use this same restart sequence; do not delete progress or reinstall packages.
