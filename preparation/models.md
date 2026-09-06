# Choose an Answer Engine

```text
Document:    Choose an Answer Engine
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      0cf8c917b380b49f4e33d69879072c58914564b650febac5facd6a24dca6e0b1
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Choose one engine. Document extraction and search remain local in every route. Ollama also generates the answer locally. Claude API and OpenAI API receive the question plus selected passages. Only supplied public or synthetic documents belong in cloud practice.

## Local Ollama

| Where | Action | Why | Expected result | Recovery |
| --- | --- | --- | --- | --- |
| Browser | Open https://ollama.com/download and choose Windows or Mac | Downloads the local model runner | Installer matches your OS | Check [Windows](https://docs.ollama.com/windows) or [Mac](https://docs.ollama.com/macos) requirements |
| Computer | Install and open Ollama; keep it running | Starts the service on 127.0.0.1:11434 | Ollama appears in the menu/task area | Open it again if doctor cannot connect |
| Terminal | Run `ollama --version`, then `ollama pull gemma3:4b` | Downloads the exact starting model | Download completes; `ollama list` includes gemma3:4b | Allow more time/storage; do not switch to an unknown model during class |
| Course root | Run `uv run --frozen zta setup`; enter 1 | Selects local inference | Ollama / gemma3:4b is reported | Rerun setup if the wrong provider was selected |
| Course root | Run doctor, then start; complete the practice question | Confirms the model actually answers | An answer and valid source receipt appear | Slow or failed generation: use cloud or the labeled saved run |

The model download is about 3.3 GB ([model card](https://ollama.com/library/gemma3)); working memory and dependencies need extra space. 16 GB RAM and 10 GB free disk are provisional planning targets, not a promise about every device. See the release pilot report. No Ollama account, payment card, or API key is needed for this local model. Keep the service on localhost. Exit the app with Ctrl+C; optionally unload the model with `ollama stop gemma3:4b` after class.

## Claude API

1. **Where:** [Claude Console](https://platform.claude.com/). **Action:** sign in or create the developer account and complete its required verification. **Why:** API billing is separate from Claude chat/coding access. **Expected:** you can open account Settings. **Recovery:** use account support or the local route if access is unavailable.
2. **Where:** Console Settings > Billing. **Action:** read the current required funding amount and enable billing only if you accept that amount; turn off automatic credit replenishment for class if offered. **Why:** a valid key without funds may still fail. **Expected:** credits or billing access show as active. **Recovery:** use Ollama if you cannot fund the account. This guide does not promise a fixed minimum charge.
3. **Where:** [API keys](https://platform.claude.com/settings/keys). **Action:** create a key named Zero to Agent class. Copy it once. **Why:** a separate key can be revoked after class. **Expected:** the provider displays the key. **Recovery:** create a replacement if you missed the one-time display; do not send the key to the instructor.
4. **Where:** course root terminal. **Action:** `uv run --frozen zta setup`; enter 2; paste the key at the hidden prompt and press Enter. **Why:** keeps it out of shell history. **Expected:** `claude-haiku-4-5-20251001` appears without a key. **Recovery:** rerun setup for a typo.
5. **Where:** terminal and local app. **Action:** run doctor; start; read the cloud notice and confirm use of public/synthetic files; run the practice question. **Why:** confirms generation and billing beyond the model-list check. **Expected:** answer, receipt, and usage estimate. **Recovery:** use the reported key, quota, or network recovery route; no automatic retry occurs.

## OpenAI API

1. **Where:** [OpenAI Platform](https://platform.openai.com/). **Action:** sign in or create a developer account, complete verification, and choose/create the project for class. **Why:** API access and billing are separate from ChatGPT/Codex access. **Expected:** the selected project appears. **Recovery:** resolve account access or use Ollama.
2. **Where:** platform Settings > Billing. **Action:** inspect current minimum funding, add funds if acceptable, and disable automatic recharge for class if offered. **Why:** chat subscriptions do not fund this app. **Expected:** active API billing. **Recovery:** choose the local route if funding is unavailable.
3. **Where:** [API keys](https://platform.openai.com/api-keys). **Action:** create a key named Zero to Agent class in your selected project; copy its one-time value. **Why:** scopes class use to a recognizable credential. **Expected:** key is displayed once. **Recovery:** revoke/recreate if needed; never paste it into a lesson or chat.
4. **Where:** course root terminal. **Action:** `uv run --frozen zta setup`; enter 3; paste into the hidden prompt. **Why:** stores the credential outside tracked source. **Expected:** `gpt-4.1-mini-2025-04-14` appears. **Recovery:** rerun setup after correcting the key.
5. **Where:** terminal and local app. **Action:** doctor, start, acknowledge cloud data transfer, and complete the practice question. **Why:** checks the actual answer path. **Expected:** source-backed answer. **Recovery:** follow the error category; do not repeatedly click after a billing failure.

## Cost and privacy check before a cloud question

Rates checked 2026-09-06: Claude Haiku 4.5 is $1 input / $5 output per million tokens; GPT-4.1 mini is $0.40 input / $1.60 output per million tokens. These are model API charges, excluding account minimum funding and any coding-assistant subscription. Sources: [Claude models/pricing](https://platform.claude.com/docs/en/models/overview) and [OpenAI model pricing](https://developers.openai.com/api/docs/models/gpt-4.1-mini).

For comparison, 20 calls using 6,000 input and 800 output tokens each would cost about $0.20 with Haiku or $0.074 with GPT-4.1 mini. This is an example, not a hard spending cap. The app displays recorded token-based estimates; the provider dashboard is authoritative. Failed calls or other apps may create usage absent from this local total. The app has no paid retries, background generation, or automatic provider fallback.

Keys live in ignored `.zta/config.json` with owner-only creation permissions where supported. Environment keys are also accepted for instructors. Do not open this file in a coding-assistant task. Do not commit it. After class, revoke an unused class key in the provider console; deleting a local file alone does not revoke it.
