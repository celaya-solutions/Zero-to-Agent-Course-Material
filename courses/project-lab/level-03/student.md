# Project Lab Level 3: Nothing Leaves the Building

## Goal

Run a local model with the network off, compare two supported local models, verify one answer, and create a named model with a useful rule set.

By the end of class, you can:

- explain that a local model is a file run on your hardware;
- prove an answer works with wifi off;
- compare speed, file size, and usefulness;
- verify one fact instead of trusting fluency; and
- build a named model from a short rules file.

## Earlier setup

Ollama may already be installed from Level 1. Keep that installation. Cloud-route learners complete the shared [Ollama setup](../../../preparation/models.md) before Level 3. This meeting focuses on offline verification, fair model comparison, and named rules rather than repeating installation.

## Start here

Bring your own computer. The model runs on your machine, so your machine is the limit: the command card lists a model for 8 GB laptops and a larger one for 16 GB, and you run whichever fits. A slower answer on your own hardware is the lesson, not a failure. There is no shared class machine for this level.

The instructor chooses and tests the small and medium models during the week of class. The command card must show the exact names and file sizes. Do not download an unknown model during class.

No laptop? Pair as test operator. You choose the prompts, run the stopwatch, check the source, and complete your own benchmark.

Experienced builder? Connect the Level 1 binder to local retrieval, or open a phone window only on the classroom router. Close it before leaving.

## Anchors / Anclas

- Nothing leaves the building. / Nada sale del edificio.
- The model is a file. / El modelo es un archivo.
- Local first, cloud when needed. / Primero local, nube cuando haga falta.

## The garage toolbox

A cloud model works in someone else's building. A local model is downloaded once and opened by a runner on your machine. RAM is the workbench: the file and the current job must fit. A smaller quantized file is the same tool made from lighter material. It may be faster and a little less exact.

Private does not mean accurate. Small models can guess. The source check remains.

## Safety stop / Alto de seguridad

Use only instructor-approved model files. Keep the local service on localhost unless the instructor provides the isolated classroom router. Never expose its port to the public internet. Private records stay out of the cloud comparison.

Usa solamente archivos aprobados. Mantén el servicio en tu propia computadora. No abras la puerta a internet.

## Task 1: Run the airplane test

1. Record the small model's exact name and file size.
2. Start it with the command card.
3. Ask it to rewrite the supplied rough message.
4. Turn wifi off in view of a partner.
5. Ask the second supplied question.
6. Record that the answer completed offline, then turn wifi back on.

Success check: a partner observed the network off and the local answer finish.

## Task 2: Benchmark two models

Run the same three prompts on the small and medium models:

1. Rewrite a rough message, firm and polite.
2. State one checkable public fact from the CSR case.
3. Solve the supplied three-quote cost problem.

Record model name, file size, seconds to first useful answer, quality from 1 to 3, and notes. Open the public source and verify prompt 2.

Success check: the comparison uses the same prompts and includes one checked fact.

## Task 3: Build your named model

Fill the supplied model template with a safe job, three to six rules, a stop rule, and a low temperature. Create it under your chosen name. Run one normal request and one question whose price or date is not provided.

Success check: the named model performs the normal job and says it is unsure instead of inventing the missing price or date.

Builder extension: use local embeddings with the Level 1 binder, or load the supplied phone page on the classroom router. Prove the port is closed again before class ends.

## Quick check before proof

1. What does RAM limit?
2. Why does wifi-off prove location but not accuracy?
3. Which model would you keep for daily writing, and why?
4. When would the cloud be the safer or more useful choice?

## Pass this level

One offline answer; a two-model benchmark with time, size, and quality; one fact checked against a source; a named custom model; and a written local-versus-cloud choice.

Save the worksheet as PROJECT-LAB-03.md or keep the paper copy.

## If something fails

- Not enough memory: use the prepared small model.
- Runner not available: open it using the operating-system card.
- Model missing: use the USB copy; do not improvise a new download.
- Model too slow: record the honest result and use the saved medium-model run.
- No laptop: remain the operator in a pair and complete the benchmark.
- Power failure: use the printed output packet and compare from evidence.

## Resumen en español

Tarea 1: demuestra una respuesta con wifi apagado. Tarea 2: compara dos modelos con las mismas tres preguntas y verifica un dato. Tarea 3: crea un modelo con nombre, reglas y una forma de detenerse cuando falta información.

## Words for Level 3

- Local model: a model file running on your machine.
- Runner: the program that opens the model file.
- RAM: the memory workbench where the model must fit.
- Quantization: a smaller representation of the model weights.
- Localhost: your machine reached from itself.
