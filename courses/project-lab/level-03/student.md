# Project Lab Level 3: Nothing Leaves the Building

```text
Document:    Project Lab Level 3: Nothing Leaves the Building
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      d7d015ad5595fa17b36dc777dd1fba917b0d55e0825297bd11e92a1d7900ca07
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

## Goal

Run a local model with external network links disconnected, compare two models using the same prompts, verify one answer, and test a named model with a missing-information rule.

By the end of class, you can explain where a model runs, compare results fairly, check a source, and improve one writing rule. A named configuration reuses downloaded weights; this exercise does not train new weights.

## Start here

Use your own computer. Complete [Level 3 preparation](preparation.md) before the 90-minute meeting. Reuse your course fork and Ollama installation from Level 1. Cloud-route learners need the local setup for this level. Each learner needs their own Ollama-capable computer for independent practice; there is no shared class machine.

If your device is unavailable, use a partner or the [saved packet](assets/fallback-benchmark.md) to practice judging evidence. Mark that route clearly. It does not show that your own computer ran offline.

Keep three windows ready: this lesson, your course folder in the editor, and a terminal opened at the course root. The root contains `pyproject.toml`. [Command card](assets/command-card.md) and [project map](../../../projects/local-models/README.md) explain each command.

## Anchors / Anclas

The model is a file. / El modelo es un archivo.
Local does not mean correct. / Local no significa correcto.
Check the answer, then choose the tool. / Verifica y después elige.

A model needs disk space for its weights and extra working memory for the job. File size is not the same as RAM use. A smaller model may fit more easily; it may also make more mistakes. The lab reads only supplied public or synthetic prompts. It sends them to `127.0.0.1:11434` and never switches to a cloud provider.

## Safety stop / Alto de seguridad

Use the supplied prompts. Keep Ollama on localhost. Do not open a router port, public tunnel, phone connection, or cloud comparison during this exercise. Shut down other course apps using Ollama before the timed run. Do not delete other people's models or stop unrelated services.

Wifi off is not enough if Ethernet, a USB tether, or another external connection is active. The partner watches all external links disconnect. A completed answer under that condition supports a limited offline claim; it does not audit the whole computer or prove accuracy. Never disconnect a shared workstation, remote-access session, or assistive connection needed for access. Use the fallback if disconnecting is not possible.

## Task 1: Prove one answer works offline

1. In the root terminal, run `uv run --frozen zta prepare local-models`. It creates your private worksheet and editable rules under `.zta/local-models/`. Running it again preserves existing work.
2. Run `uv run --frozen zta doctor local-models`. Expect two LOCAL rows with names, bytes, and full model digests. Copy those details to Task 1 of your worksheet. A missing model sends you back to preparation; this command never downloads it.
3. Before disconnecting, predict what will happen. A local model should answer; a cloud request cannot complete without its remote service.
4. With a partner watching, turn off wifi, unplug Ethernet, and disconnect any USB/phone tether. Record the time and which links were checked. Keep localhost available. Do not change system firewalls.
5. Run `uv run --frozen zta offline local-models`. Expect a short workbench reminder, elapsed seconds, and a new receipt filename. It may take up to three minutes on a slow machine.
6. Copy the answer, receipt name, time, and your partner's observation into the worksheet. The program leaves `network_disconnect_observed` blank: a program response cannot certify this human observation.
7. Restore the links you disconnected. Note the time. If the run failed, keep that result and follow recovery.

Success check: another person can distinguish what the terminal recorded from what your partner saw. Do not mark a saved or connected run as an offline success.

## Task 2: Compare the same three prompts

Before running, open the [benchmark card](assets/benchmark-card.md). Write your prediction and the expected answer for each prompt. The source prompt includes the complete dated [public source](../level-01/assets/public-identity-and-work.md); the model does not browse for it.

1. Run `uv run --frozen zta benchmark local-models` once. It runs writing, source, and arithmetic on `gemma3:1b`, then the same three prompts on `gemma3:4b`.
2. Wait for each row. The terminal shows its answer and total seconds to complete. A receipt is saved after every completed row, so a later failure cannot erase earlier work. Ctrl+C stops the learner command.
3. Enter all six rows in Task 2. Copy model size and digest from the receipt. Write each quality score yourself: 1 = wrong or unusable, 2 = useful with a specific correction, 3 = meets every check. An unfinished or capped answer cannot earn 3.
4. Read the original public source yourself. Compare the place, work, and both headings against the answer. Mark supported, unsupported, or incomplete, and give the line or heading that explains your verdict. The source is a dated classroom snapshot, not proof of today's live website.
5. Check the arithmetic independently: 84 is cheapest; 84 x 0.0825 = 6.93; 84 + 6.93 = 90.93 dollars. A confident wrong total earns 1.
6. Compare the models for this job on this computer. Each request starts after unloading that course model and includes loading in its time. It uses the same context limit, output cap, temperature, and seed. This is total completion time, not time to first word. Other running programs and hardware still affect it; one round cannot prove a universal winner.

Success check: six actual or clearly saved rows, fixed prompts, honest timing, human scores, and an independent source check. No model grades itself.

## Task 3: Name a helper, change one rule, and retest

1. Open `.zta/local-models/Modelfile` in the editor. Read its job, four writing rules, and missing-information stop. It starts from `gemma3:1b` already on disk.
2. Run `uv run --frozen zta create local-models`. This creates or replaces only the course name `zta-desk:latest`. It keeps the original base model.
3. Run `uv run --frozen zta check local-models`. Record the normal writing answer and the missing-price/date answer as **before**. A good missing answer says no price or delivery date is provided and asks a person to confirm.
4. Predict one useful change: two short sentences should make the reminder easier to read while keeping the deadline and reply request.
5. Follow the [manual edit card](manual-edit.md), or give its bounded prompt to Claude Code/Codex. Replace only `Write one polite paragraph under 70 words.` with `Write exactly two short sentences under 50 words total. The first must keep the deadline; the second must ask the reader to reply when ready.` Keep the missing-fact rule, base, limits, prompts, tests, and earlier receipts intact. Do not send private worksheet or receipts to an assistant.
6. Run create again, then check again. Both tests are identical to the before run. Record actual outputs and decide whether the new rule helped. A rule can still be ignored; report that failure, correct the one rule if time allows, and keep the earlier result.
7. Run `uv run --frozen zta test local-models`. These code tests check the lab's behavior, not the model's judgment. Save your rule text and comparison in the private worksheet.

Success check: named model, before outputs, prediction, one changed rule, after outputs, and a verdict for BOTH normal writing and missing information. Low temperature and a SYSTEM rule are not a security boundary.

Builder extension: run the unchanged benchmark a second time. Compare variation with the first round; keep separate receipts. Keep localhost and the supplied prompts. Finish core proof first.

## Quick check before proof

What does disk size tell you that RAM does not? Why is wifi-off alone sometimes weak evidence? Why can a model run offline and still invent a price? What changed when you created a named model?

## Pass this level

An observed offline answer or a labeled fallback; six benchmark rows with model identity, size, total time, and your quality verdict; one checked source; a named model tested before and after one rule edit; and a written local-versus-cloud choice.

Review `.zta/local-models/PROJECT-LAB-03.md`. Complete predictions, actual results, source checks, and before/after verdicts. Use [submission steps](../../../preparation/submission.md): sign in to the course, open Level 3, upload the private worksheet, and reopen the saved item to check its contents. A local receipt or exported file is not an upload receipt. If upload is unavailable, keep the file and record Not submitted; do not invent confirmation.

Stop any active learner command with Ctrl+C. Use `ollama stop gemma3:1b`, `ollama stop gemma3:4b`, and `ollama stop zta-desk:latest` if they remain loaded. Do not use `rm` for cleanup; keep downloads for next class. The private rules and worksheet stay in `.zta/`, which Git ignores. No public commit is needed for this local exercise.

## If something fails

After two attempts or five minutes on one problem, use [recovery](preparation.md#recovery) and the saved packet. Keep failures visible. A missing model needs online preparation before another airplane test. A slow or too-large model uses saved comparison rows with your own live rows labeled separately. If the named helper invents a fact, mark the test failed; a template is not guaranteed obedience. If a request is still running after cancellation, use the matching `ollama stop` command on your own course model.

## Resumen en español

Usa tu propia computadora. Prepara los dos modelos antes de clase. Desconecta wifi, Ethernet y cualquier conexión del teléfono frente a tu pareja; ejecuta y guarda una respuesta. Compara seis resultados con las mismas preguntas. Verifica la fuente y el cálculo. Crea `zta-desk`, cambia una sola regla y repite las dos pruebas. Entrega tu hoja privada en Nivel 3 y vuelve a abrirla. Marca los ejemplos guardados y las pruebas no realizadas con honestidad.

## Words for Level 3

Localhost means this computer talking to itself. A digest identifies the downloaded model content. A benchmark is a small comparison under recorded conditions. A Modelfile names a base and its rules; it is not training. RAM is working memory. Quantization stores weights with fewer bits, which changes size and can affect quality.
