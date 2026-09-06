# Project Lab Level 1: Your Documents Answer Back

```text
Document:    Project Lab Level 1: Your Documents Answer Back
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      e35720402b4172f25b5e4641e296bba5c0e06ef63bfeb246d420f5148367c84b
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

## Goal

Build and test a custom document helper that searches supplied public and synthetic files, shows exact source receipts, stops on missing facts, and flags conflicts for human review.

By the end of class, you can explain local retrieval, distinguish public from synthetic evidence, test missing/conflicting answers, open exact sources, and connect a small project change to a rerun.

## Before the 90-minute class

Complete [Preparation](../../../preparation/README.md). You need your own Windows or Mac computer, a fork, a working uv environment, one coding assistant (Claude Code or Codex, or the manual card), one answer engine (Ollama, Claude API, or OpenAI API), and course-platform access. No coding experience is required. Preparation takes 45-90 minutes plus download time.

Open this lesson and [the app](http://127.0.0.1:8501) side by side. To start it, open a terminal in the fork's root and run:

```sh
uv run --frozen zta doctor documents
uv run --frozen zta start documents
```

Doctor checks readiness. Start runs the app. Keep the terminal open; Ctrl+C stops it. If anything fails, follow [Recovery](../../../preparation/recovery.md). Your worksheet saves locally as you finish each field and move to the next one; press Tab or click outside a text field before refreshing.

## Anchors / Anclas

- Find the page, then answer. / Encuentra la página y después responde.
- Confidence is not accuracy. / La confianza no es exactitud.
- A citation is a receipt to inspect, not proof by itself.

## The binder and clerk

The binder contains approved documents. A clerk finds passages containing useful words. The model reads those passages and writes an answer. This is retrieval-augmented generation (RAG): retrieve first, then generate. Our small app uses SQLite keyword search, not embeddings or model training. A file does not become learned model knowledge when you load it.

## Safety stop / Alto de seguridad

Use only supplied public or TRAINING-ONLY SYNTHETIC RECORD files. Never add client records, private messages, account data, contracts, keys, or unpublished work. Both cloud routes send selected passages to the provider; local Ollama keeps generation on this computer. Neither route guarantees a correct answer.

Solo usa archivos públicos o sintéticos. No compartas claves, datos privados ni información de clientes. Si falta información, detente.

## Task 1: Run the app and build the binder (0-23 minutes)

| Step / where | Action | Why | Expected result | Recovery |
| --- | --- | --- | --- | --- |
| 1 / Start tab, 0-5 | Enter your course nickname and coding assistant. Read the provider/model in the sidebar | Records the actual route | Your name, tool, and model are visible | Rerun setup if the provider is wrong; record Manual card if needed |
| 2 / demonstration, 5-10 | Follow question > search > passages > answer > citation | Separates evidence finding from fluent writing | You can name each stage | Ask the instructor to repeat the same question with its source open |
| 3 / Binder tab, 10-15 | Click Load class binder. Open all four originals; classify each public or training-only | Prevents synthetic policy claims | Two public files and two synthetic files are correctly classified | Read each file's status/disclaimer, not its filename alone |
| 4 / Binder tab, 15-23 | Click Build index. Open an extracted passage and compare it with the original | Confirms the text was read correctly | Four documents are indexed with headings and readable text | Use text copies if PDF extraction fails; rebuild the correct binder |

The four files are Public Identity and Work, Public Contact and Method, Training Record A, and Training Record B. A rules card or answer key is not a fifth source. The app loads only the four named files.

## Task 2: Predict and test five questions (23-50 minutes)

| # | Question | Expected behavior |
| --- | --- | --- |
| 1 | Where is Celaya Solutions Research based? | El Paso, Texas; public identity file; exact heading |
| 2 | What kind of systems does the lab build? | Only the supplied description; public work heading |
| 3 | Which public contact route should I use for a research collaboration, and what work does the lab focus on? | Public email and work description, with one citation to each public document |
| 4 | What is the price of a custom deployment? | Not in the documents. No number or guessed range |
| 5 | Which routing label and review target should be used for a research collaboration in this exercise? | Both synthetic records: RESEARCH / two classroom days and COLLABORATION / three classroom days; human review; no chosen winner |


| Step / where | Action | Why | Expected result | Recovery |
| --- | --- | --- | --- | --- |
| 5 / Five questions, 23-28 | Fill all five Expected fields before clicking any Run button | Makes your prediction independent of the model answer | All five Run buttons become available | Complete each field and press Tab; build index if buttons stay disabled |
| 6 / Five questions, 28-43 | Preview the retrieved evidence, then run each question once. For cloud, first acknowledge the sidebar data notice | Shows what the model actually receives | Each question has an answer/status, passages, time, and route | Read service errors once; do not retry billing failures repeatedly |
| 7 / each result | Read the source receipts and choose My verdict: Pass or Miss | You grade support and safe behavior, not confidence | Five verdicts are saved | Mark Miss if a citation is valid but the claim is unsupported |
| 8 / question 3, 43-50 | Open the two cited public source panels. Compare their original text with the two claims. Click I opened and checked this source for each | Verifies a real two-document answer | Both public sources are recorded as opened | If one source is absent, record the miss; examine retrieval before revising |

Question 4 must stop. Question 5 must show both synthetic routes and targets and ask a person. A model that picks one target has missed the conflict. A Needs review status means the app could not validate the answer format or source receipts; it is not a successful supported answer.

## Task 3: Improve, rerun, save, and submit (50-90 minutes)

| Step / where | Action | Why | Expected result | Recovery |
| --- | --- | --- | --- | --- |
| 9 / Improve tab, 50-55 | Choose the weakest row; write the suspected cause and the change you expect to help | Makes the edit purposeful | One observable problem is named | If all tests pass, use the controlled exercise below |
| 10 / Claude Code or Codex, 55-67 | Open your fork. Paste the bounded prompt in Improve with the safe question, expectation, answer, and passages. Review its proposed edit | Changes one cause while preserving the test | Only intended source/settings changes appear | Use [Manual edit](manual-edit.md) if assistant access is blocked |
| 11 / same file | Save the edit; refresh the browser to reload settings. Run the SAME question | Connects the change to its effect | A second run of the same question is saved | Undo an unrelated edit and try the documented change |
| 12 / Improve | Choose Before and After runs of the same question. Explain one change and its observed effect; Save before and after | Creates an inspectable revision trail | Revision evidence saved | Two different questions or empty explanations are rejected |
| 13 / Five questions, 67-75 | Rerun all five; judge each latest result | Checks that one improvement did not break another behavior | Five final verdicts exist | Keep unresolved misses visible; do not relabel a failure as Pass |
| 14 / terminal, 75-80 | Run `uv run --frozen zta test documents` | Checks parsing, retrieval, adapter failures, and evidence without paid API calls | Tests pass | Read the failed check and restore the intended edit; ask instructor if needed |
| 15 / GitHub Desktop | Review the diff. Commit the intended project change with summary Show source quotes for Level 1. Click Push origin (or Publish branch). Open the commit in your fork and copy its URL | Saves a reproducible code version | GitHub shows your change | Do not commit .zta, keys, or evidence; see [commit guide](manual-edit.md) |
| 16 / Proof tab, 80-87 | Paste fork and commit links. Explain source check, data boundary, unresolved misses, and exit ticket. Review completion checks; click Export PROJECT-LAB-01.md | Builds the private evidence file | Browser downloads the complete Markdown packet | Incomplete items remain labeled; finish or explain the block |
| 17 / [course platform](https://learn.zerotoagent.org/auth/users/sign_in) | Open course > Level 1 > upload file; choose PROJECT-LAB-01.md; complete the displayed acknowledgment; Submit; reopen Submission History and inspect the file/time | Proves receipt | Correct content and timestamp appear | Keep local file if platform is down; [submission guide](../../../preparation/submission.md) |
| 18 / terminal and exit ticket, 87-90 | Press Ctrl+C; refresh the browser. Explain one missing-information rule and one conflict rule | Demonstrates stopping and understanding | App disconnects; exit ticket is complete | Closing the browser alone does not stop the process |

### If all five pass: controlled retrieval exercise

In `projects/documents/settings.toml`, change `max_passages = 4` to `max_passages = 1`. Save, refresh, and rerun question 5. Inspect which record is missing. Restore 4, save, refresh, and rerun. Compare retrieved evidence even if the model safely refuses; do not force a hallucination.

Then keep one useful change: set `show_source_quotes = true`. Save, refresh, and rerun the selected question. Quotes now appear below the answer, so a reader can check support faster. Commit this improvement and leave `max_passages = 4`.

Builder extension: inspect retrieval in `projects/documents/src/zta/documents.py` after core proof. Compare counts using the same questions. Extra code does not replace the five-question record.

## Quick check before proof

1. Why is a model answer not its own source?
2. What is the difference between a valid receipt and a correct claim?
3. What should happen when a price is missing?
4. Why must both training records appear?
5. Which data left your computer on your selected route?

## Pass this level

Four classified documents; five predicted and judged tests; two public source checks; one same-question improvement; a fork commit; and a private evidence upload receipt.

Save the private packet as PROJECT-LAB-01.md. The app checks completeness, not truth. The instructor grades your predictions, source checks, honest verdicts, and explanation. An unresolved model miss stays visible. A saved example is always labeled saved; it does not claim a successful live build.

## If something fails

After two tries or five minutes, open the saved examples section in Five questions and load the five authored examples. Write expectations first and judge each result. For a full outage use [the printable packet](assets/fallback-grounded-run.md) and [worksheet](worksheet.md). Use the manual repair explanation; mark live-only fields Not applicable: saved run. Keep the same decision trail.

## Resumen en español

Ejecuta la aplicación. Clasifica cuatro archivos. Escribe lo esperado antes de hacer cinco preguntas. Verifica dos fuentes públicas. Cambia una regla, repite la misma pregunta y guarda la evidencia. Sube el archivo al curso y confirma que llegó. Los ejemplos guardados siempre se marcan como guardados.

## After editing Python rules

Settings-only edits take effect after saving and refreshing the browser. If the edit changes a `.py` file, return to the app's terminal, press Ctrl+C, run `uv run --frozen zta start documents` again, and refresh the browser before rerunning the same question. This starts the changed code. Your saved expectations and runs remain in `.zta/`. If a stale-import error appears, use this same restart sequence; do not delete progress or reinstall packages.
