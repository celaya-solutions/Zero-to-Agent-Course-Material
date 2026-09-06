# Project Lab Level 2: The Night Watchman

## Goal

Specify, run, and test a scheduled page watcher that records each round, alerts only on a meaningful change, and stops through a tested switch.

By the end of class, you can:

- write a watchman spec another person can follow;
- explain look, compare, tell;
- run a prepared watcher in GitHub Actions;
- read its log and alert; and
- disable it and prove the next run does not happen.

## Start here

The core route uses the supplied practice page and starter files. You may use a coding assistant to explain a line, but the test sheet is yours. Phone-only learners own the spec, prediction, and log review while a partner operates the browser.

Experienced builder? Inspect or revise the extraction rule and write a Railway always-on contract. Do not deploy to Railway in this level.

## Anchors / Anclas

- Look, compare, tell. / Mira, compara y avisa.
- If it cannot be turned off, it is not finished. / Si no se puede apagar, no está terminado.
- Autonomy is earned, not granted. / La autonomía se gana, no se concede.

## The guard's rounds

A useful watcher is boring. It visits one address on a schedule, reads one stable value, compares that value with the last round, writes a log line, and alerts only when the change matches a written rule. The clock is its trigger. The log is its receipt.

Tonight it may create a repository issue. It may not buy, reply, delete, post elsewhere, or spend money.

## Safety stop / Alto de seguridad

Watch only the supplied page or a page you own. Respect site terms and rate limits. Use no private page, login, bypass, or personal tracking. A repository token stays in the host's secret store and never appears in code or a log.

Vigila solamente la página de práctica o una página tuya. No uses páginas privadas, cuentas ajenas ni claves en el código.

## Task 1: Write the watchman spec

Fill six lines:

1. Address: the supplied practice page.
2. Signal: the text inside the element marked watch-value.
3. Meaningful change: the status text changes.
4. Trigger: a manual run now; daily schedule after class.
5. Alert: one GitHub issue naming old and new values.
6. Never list: no purchase, reply, deletion, public post, or spending.

Success check: a partner can predict exactly when an alert should and should not appear.

## Task 2: Run, change, and inspect

1. Use the supplied starter map: watch.py and practice-page.html go at the repository root; watch.yml goes at .github/workflows/watch.yml.
2. Run the workflow once. Record the baseline line.
3. Run it again without changing the page. Record no change.
4. Change the practice status from OPEN to PAUSED.
5. Run it again. Inspect the issue and log.
6. Match each run to the expected result you wrote first.

Success check: one controlled change creates one useful alert. An unchanged run creates no alert.

## Task 3: Use the switch

Disable the workflow. Try to reach the Run workflow control again and record what changed. Write where the switch lives and who may use it. Enable it only if the instructor asks.

Builder extension: narrow the parser so a moving date or footer cannot trigger an alert. Then write the start command, environment, health check, state, persistence, schedule, stop, and monthly cost a Railway version would require.

## Quick check before proof

1. Where does the watcher run while the laptop is closed?
2. What is the difference between an unchanged run and a failed run?
3. Which action can the watcher take?
4. Where is the off switch?

## Pass this level

A complete watchman spec; baseline, unchanged, and changed runs; one useful alert and log trail; a never list; and proof that the learner used the off switch.

Save the worksheet as PROJECT-LAB-02.md or keep the paper copy.

## If something fails

- Workflow missing: compare the exact folder path with the starter card.
- Red run: read the last ten log lines and record the first useful error.
- No issue: check that the workflow may write issues and that the signal changed.
- No email: the issue and log are still proof; notification settings are separate.
- GitHub unavailable: use the saved three-run packet and complete the same verdicts.
- Platform unavailable: keep local proof and submit later.

## Resumen en español

Tarea 1: escribe qué vigila, qué cambio importa y qué nunca puede hacer. Tarea 2: ejecuta una línea base, una prueba sin cambio y una prueba con cambio. Tarea 3: usa el interruptor y demuestra que se detuvo.

## Words for Level 2

- Schedule: the clock rule that starts a run.
- Workflow: the host's file describing the job.
- Log: one dated receipt for each round.
- Alert: a message created only for a meaningful change.
- Kill switch: the tested action that stops future runs.
