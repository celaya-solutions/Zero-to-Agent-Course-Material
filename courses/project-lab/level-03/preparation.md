# Prepare Level 3 on Your Own Computer

```text
Document:    Prepare Level 3 on Your Own Computer
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      bf54ebb445f4da677c44964821cfbde20ae54204bc256c9a8c4fee42ea31f06a
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Do this online before the 90-minute class. Keep the existing course folder and installed Ollama from Level 1. You need your own supported Windows or Mac computer for independent practice. A partner/saved route helps you learn when a device is unavailable, but does not prove your device works.

## Get ready

| Where | Action | Expected result | Recovery |
| --- | --- | --- | --- |
| Your course root | Open the folder containing `pyproject.toml`; run `uv sync --frozen` | The locked environment installs without a changed lockfile | Follow the shared [Windows](../../../preparation/windows.md) or [Mac](../../../preparation/macos.md) guide |
| Browser | New local users open [Ollama download](https://ollama.com/download); choose the installer for their OS | Ollama installed and open | Read the official [Windows guide](https://docs.ollama.com/windows) or [Mac guide](https://docs.ollama.com/macos) |
| Terminal | Run `ollama --version` | A version number | Open Ollama; reopen the terminal after installation |
| Terminal, online | Run `ollama pull gemma3:1b` | Small model finishes downloading | Make disk space or allow more time before class |
| Terminal, online | Run `ollama pull gemma3:4b` | Larger model finishes; Level 1 users may already have it | Do not try a larger model to fix a memory failure |
| Terminal | Run `ollama list` | Both exact names appear with sizes and IDs | Finish the missing download while online |
| Course root | Run `uv run --frozen zta prepare local-models`, then `uv run --frozen zta doctor local-models` | Private files prepared and two LOCAL model rows | See recovery below |
| Course root | Run `uv run --frozen zta offline local-models` while still connected for a setup rehearsal | One local answer and a receipt | Label this connected rehearsal, never offline proof |

The small download is about 815 MB and the larger about 3.3 GB, checked 2026-09-06 on the official [1B model card](https://ollama.com/library/gemma3:1b) and [4B model card](https://ollama.com/library/gemma3:4b). Working memory needs extra space. 8 GB RAM for the small route and 16 GB for the larger route are planning targets, not tested minimums or speed promises. Keep at least 8 GB free disk for downloads and working space, more if your system needs it. Record your actual size/digest; tags can change.

These local downloads require no API key or paid generation. Model terms are separate from the course license; read the [Gemma terms](https://ai.google.dev/gemma/terms). The course contains templates and prompts, not model weights. Reuse the downloaded models instead of bundling someone else's model folder into your fork.

## Local connection check

Keep the default loopback address. The lab always calls `http://127.0.0.1:11434`, ignores proxy variables, refuses cloud metadata, and never follows HTTP redirects. It does not read the Level 1 provider configuration or use its API key. Do not select a `cloud` model or enable web search. Ollama's [FAQ](https://docs.ollama.com/faq) explains the default local bind and optional cloud-disable setting; do not replace existing settings blindly.

Check your own listener before class if you have changed Ollama networking. On Mac, run `lsof -nP -iTCP:11434 -sTCP:LISTEN`; on Windows PowerShell, run `Get-NetTCPConnection -LocalPort 11434 -State Listen`. Expect `127.0.0.1` (loopback); `0.0.0.0`, `*`, or a LAN address needs instructor help before class. Do not stop an unknown process. Doctor checks model availability, not the listener's bind or all system traffic.

## Recovery

- **Cannot connect:** open Ollama; use the listener check to identify the service. Keep the terminal in the course root. Do not switch the endpoint to a public service.
- **Missing model:** reconnect intentionally and finish the exact download before restarting offline proof. The lab will not download on your behalf.
- **Slow or out of memory:** close your own unused applications, retry once, then use the supplied saved rows for the larger model. Label each row's source. Never claim those times came from your computer.
- **No installer or network:** use a previously working local installation. If absent, work through the saved packet. A USB file alone is not a tested cross-platform model installer; do not copy unknown model stores into your account.
- **Course command missing:** confirm the reviewed Level 3 checkout and rerun `uv sync --frozen` while online. Do not guess a branch or overwrite uncommitted work.
- **Interrupted benchmark:** keep the partial receipt, mark missing rows Not performed, stop the matching course model if needed, then start a new receipt. Do not edit a failed receipt into a success.
- **Cannot disconnect access links:** use the connected rehearsal or saved route and explain the missing observation. Never sever a remote or assistive session to earn a check mark.

Bring the downloaded files, charger, your private worksheet, and a copy of the saved packet. Do not download models during the timed lesson.
