# Windows - Install and Open the Course

```text
Document:    Windows - Install and Open the Course
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      a77146aacfe2494a33f56deb9d3681a40b716d717668b17ac22634b388e82589
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Start with [Preparation](README.md). Keep one copy of this guide open until the app runs.

| Step / where | Action | Why | Expected result | Recovery |
| --- | --- | --- | --- | --- |
| 1 / settings | Start > Settings > System > About: record Windows version, System type, and Installed RAM. File Explorer > This PC: record free disk space. Use Windows 10 22H2 or newer on a supported 64-bit computer. | Checks the planned local-model target | Record OS, RAM, chip, and storage | Cloud generation reduces model hardware needs; installation still requires an unrestricted computer |
| 2 / browser and installer | Install [GitHub Desktop](https://desktop.github.com/download/), choose the installer matching your OS/chip, open it, and sign in | Manages your fork and changes | Correct GitHub username appears | Complete the browser authorization, then return to Desktop |
| 3 / terminal | Open Start, type PowerShell, and open Windows PowerShell. Use PowerShell, not Command Prompt. | Opens the command tool | A prompt is visible | Ask the helper to point to the app; keep control of the keyboard |
| 4 / terminal | Run the installer below; wait for completion; close and reopen the terminal | Installs uv and refreshes PATH | `uv --version` prints a version | If blocked by device policy, use the setup clinic; do not change machine-wide policy |
| 5 / clone folder | In GitHub Desktop choose Repository > Show in Explorer. In File Explorer, click the address bar, type `powershell`, and press Enter. Run `Get-Location` and `Get-ChildItem`. | Places commands at the repository root | Listing includes `pyproject.toml` and `uv.lock` | If they are missing, open the clone itself, not its parent or projects subfolder |
| 6 / same terminal | Run `uv sync --frozen` | Downloads managed Python and installs the release's packages | No error; local .venv exists | Check internet, storage, and permissions. Keep uv.lock unchanged |
| 7 / browser and terminal | Complete [model setup](models.md) and [coding-assistant setup](coding-assistants.md) | Configures the selected routes | Doctor passes and assistant can inspect README | Follow [Recovery](recovery.md) |
| 8 / same terminal | Run `uv run --frozen zta start documents`, then open http://127.0.0.1:8501 | Starts the local interface | Start, Binder, Five questions, Improve, and Proof tabs appear | Keep the terminal open; check its error if the page fails |
| 9 / terminal | Press Ctrl+C; refresh the browser | Demonstrates the stop | Browser disconnects; the terminal prompt returns | Closing only the browser does not stop the app |

## uv installer

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Reopen the terminal, then run:

```sh
uv --version
uv sync --frozen
uv run --frozen zta setup
uv run --frozen zta doctor documents
uv run --frozen zta start documents
```

Run each line separately; read its result before continuing. Installer source: [official uv instructions](https://docs.astral.sh/uv/getting-started/installation/). Ollama requirements: [official Windows guide](https://docs.ollama.com/windows).

## Command not found

If a newly installed command is missing, completely close and reopen the terminal, then try its `--version` check again. If it still fails, use the [official installer troubleshooting](https://docs.astral.sh/uv/getting-started/installation/) and the setup clinic. Do not paste random fixes or private account information into chat.

## Visual guide

[Open the illustrated setup map](setup-map.svg). It distinguishes the browser, GitHub Desktop, terminal, and local app. It is an instructional diagram, not a screenshot claiming a device pilot occurred.
