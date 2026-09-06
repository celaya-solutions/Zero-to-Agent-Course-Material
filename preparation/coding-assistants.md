# Choose Claude Code or Codex

```text
Document:    Choose Claude Code or Codex
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      a304087429b720e25f33c0b1acf87bfcc1d11f7028b6c640b74bcf1a9e49ae64
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Choose one assistant. It edits the course app; it is separate from the engine that answers document questions. Account access and usage limits vary. Check the linked official account information before buying anything. If unavailable, use the manual edit card and keep the same evidence requirements.

## Claude Code

| Where | Action | Why | Expected result | Recovery |
| --- | --- | --- | --- | --- |
| Browser | Open [official quickstart](https://code.claude.com/docs/en/quickstart) and confirm your account has Claude Code access | Prevents assuming a free chat login includes coding access | You know which account you will sign into | Use manual card if account access is unavailable |
| Mac Terminal | Run `curl -fsSL https://claude.ai/install.sh | bash` | Installs the official native tool | Installation finishes | Use the official troubleshooting page if policy/network blocks it |
| Windows PowerShell | Run `irm https://claude.ai/install.ps1 | iex` | Installs the Windows native tool | Installation finishes | Use PowerShell; a Command Prompt window does not recognize irm |
| Reopened terminal | Run `claude --version` | Confirms the shell can find it | Claude Code version appears | Reopen terminal; follow official PATH recovery |
| Course root terminal | Run `claude`; follow the browser sign-in and return to the terminal | Attaches coding access to your project | You can send a prompt | Do not paste login codes or credentials into course evidence |
| Assistant | Send the inspection prompt below | Checks the project boundary before editing | Explanation only, no file changes | Reject edits and restate the read-only request |

## Codex

| Where | Action | Why | Expected result | Recovery |
| --- | --- | --- | --- | --- |
| Browser | Open [official desktop setup](https://learn.chatgpt.com/docs/app); choose the download for your OS/chip | Uses the supported installation route | The app installs and opens | Check official OS requirements if the installer refuses |
| Desktop app | Sign into your ChatGPT account and choose Codex | Opens the coding workspace | Codex task controls appear | Resolve account access or use the manual card |
| Project selector | Open the local course clone folder; select local work for this lesson | Keeps edits in the learner's fork | README and project folder belong to your clone | Remove an incorrectly selected folder and choose the right clone |
| Task | Send the inspection prompt below | Confirms what the assistant will edit | Explanation only | Reject unrelated edits; do not enable unattended publishing |

## First prompt - inspect only

> Read AGENTS.md, the course README, and projects/documents/README.md. Explain how the document helper runs and where I can change retrieval settings. Do not edit files, read .zta/, install software, send requests, or publish anything.

## Guided-edit prompt

> Read the Level 1 instructions and inspect my recorded miss. Explain its likely cause before editing. Change one rule or retrieval setting that addresses it. Preserve the supplied documents, expected results, and tests. Show the change, explain why it should help, and tell me how to rerun the same question. Do not publish anything.

Add your question, expected behavior, observed answer, and safe source excerpts. Never attach .zta/config.json. Read the diff before accepting it. Run the course checks after the edit. Use GitHub Desktop yourself to review and publish to your own fork.

If you used a coding assistant to make an edit, record its name in the app's Start tab. If you used the [manual card](../courses/project-lab/level-01/manual-edit.md), record Manual card.

## After editing Python rules

Settings-only edits take effect after saving and refreshing the browser. If the edit changes a `.py` file, return to the app's terminal, press Ctrl+C, run `uv run --frozen zta start documents` again, and refresh the browser before rerunning the same question. This starts the changed code. Your saved expectations and runs remain in `.zta/`. If a stale-import error appears, use this same restart sequence; do not delete progress or reinstall packages.
