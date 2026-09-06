#!/usr/bin/env ruby
# frozen_string_literal: true

require "cgi"
require "fileutils"
require "yaml"

ROOT = File.expand_path("..", __dir__)
COURSE = File.join(ROOT, "courses", "project-lab")

DECKS = {
  1 => {
    routes: "<p>Own Windows/Mac computer; completed preflight; Claude Code or Codex for edits; Ollama, Claude API, or OpenAI API for answers.</p>",
    anchors: "<p>Find the page, then answer. Encuentra la p\u00e1gina y despu\u00e9s responde. Confidence is not accuracy.</p>",
    idea: "<p>Four source files become local searchable passages. The selected model writes from the retrieved evidence. This is keyword retrieval, not model training.</p>",
    fence: "<p>Only public or synthetic files. Cloud routes send selected passages. Keys and learner proof stay out of Git. A receipt still needs human checking.</p>",
    demo: "<p>Launch with uv run --frozen zta start documents. Open 127.0.0.1:8501. Trace a question through passages, answer, and source check.</p>",
    task1: "<p>Load class binder. Classify two public and two synthetic files. Build index. Compare extracted text with originals.</p>",
    task1_check: "<p>Four correctly classified documents with readable headings. The app reports the selected provider and model.</p>",
    task2: "<p>Write all five expectations before running. Test location, systems, contact plus work, missing price, and conflicting training rules.</p>",
    task2_check: "<p>Open BOTH public sources for question 3. Missing price stops. Both synthetic labels and targets appear with human review.</p>",
    task3: "<p>Choose one miss. Change one setting or rule with Claude Code, Codex, or the manual card. Rerun the SAME question.</p>",
    task3_check: "<p>Before, one change, after, and explanation are saved. Rerun all five questions and judge each result.</p>",
    extension: "<p>All five pass? Change max_passages from 4 to 1, test conflict, restore 4, and compare evidence. Keep show_source_quotes = true as the useful edit.</p>",
    outage: "<p>Load five saved examples after predictions. Mark the route saved classroom example. Paper and manual editing preserve the decision trail.</p>",
    partner: "<p>Check source labels, both public receipts, missing/conflict behavior, and the same-question rerun.</p>",
    spanish: "<p>Clasifica cuatro archivos. Predice y prueba cinco preguntas. Verifica dos fuentes. Cambia una regla y repite. Guarda la evidencia.</p>",
    next: "<p>Run zta test documents. Review, commit, and push only the project change to your fork. Export private PROJECT-LAB-01.md and upload it to Level 1.</p>",
    exit: "<p>Reopen the upload receipt. Stop the app with Ctrl+C. Explain one missing-information rule and one conflict rule.</p>",
  },
  2 => {
    routes: "<ul><li>Core: supplied watcher and GitHub Actions</li><li>Partner: spec, predictions, and log review</li><li>Outage: saved three-run packet</li></ul>",
    anchors: "<ul><li>Look, compare, tell.</li><li>Mira, compara y avisa.</li><li>If it cannot be turned off, it is not finished.</li></ul>",
    idea: "<p>A good guard follows the same route, reads one stable signal, compares it with the last round, and alerts only when a written rule says it matters.</p>",
    fence: "<ul><li>One approved page</li><li>One stable value</li><li>No buy, reply, delete, post, or spend</li><li>One log and one switch</li></ul>",
    demo: "<p>Run baseline. Run unchanged. Change OPEN to PAUSED. Read the alert and every log line.</p>",
    task1: "<p>Write address, signal, meaningful-change rule, trigger, alert, and never list.</p>",
    task1_check: "<p>A partner can predict exactly when an alert appears.</p>",
    task2: "<p>Run baseline, unchanged, and controlled-change tests. Record expected and actual results.</p>",
    task2_check: "<p>One change creates one issue. No change creates no issue. Failure is not called no change.</p>",
    task3: "<p>Disable the workflow. Try the control again. Record the stopped state and who owns the switch.</p>",
    task3_check: "<p>The switch was used, not merely named.</p>",
    extension: "<p>Narrow the parser, then write a Railway contract: start, environment, health, state, persistence, schedule, stop, and cost.</p>",
    outage: "<p>Use the saved baseline, unchanged, and changed logs. Identify the same receipts and switch.</p>",
    partner: "<ul><li>Spec predicts behavior</li><li>Three states are distinct</li><li>Old and new values are visible</li><li>Switch is proved</li></ul>",
    spanish: "<p>Escribe la regla. Ejecuta tres pruebas. Lee el registro. Usa el interruptor.</p>",
    next: "<p>The warehouse computer worked while your laptop was closed. Next, bring the model onto your machine.</p>",
    exit: "<p>What may your watcher do? Where is its off switch?</p>",
  },
  3 => {
    routes: "<ul><li>Core: reuse earlier Ollama setup; prepare small and medium models</li><li>Partner: prompt, stopwatch, source, verdict</li><li>Outage: dated benchmark packet</li></ul>",
    anchors: "<ul><li>The model is a file.</li><li>El modelo es un archivo.</li><li>Local first, cloud when needed.</li></ul>",
    idea: "<p>The cloud is a shop across town. A local model is a toolbox in your garage. RAM is the workbench where the file must fit.</p>",
    fence: "<ul><li>Local does not mean accurate.</li><li>Approved model files only.</li><li>Localhost stays closed to the internet.</li><li>Private records stay out of cloud comparison.</li></ul>",
    demo: "<p>Point to the model file. Run it. Turn wifi off. Ask again. Then compare the same three prompts.</p>",
    task1: "<p>Record the small model name and size. Run it. Turn wifi off and complete a second answer.</p>",
    task1_check: "<p>A partner observed the network off and the answer finish.</p>",
    task2: "<p>Run writing, public-fact, and arithmetic prompts on two models. Time and score each.</p>",
    task2_check: "<p>Same prompts, exact model names, file sizes, timing, ratings, and one checked public fact.</p>",
    task3: "<p>Fill the model template with a safe job, three rules, and a missing-price-or-date stop. Create and run it by name.</p>",
    task3_check: "<p>Normal job works. Missing fact does not become a confident guess.</p>",
    extension: "<p>Connect the Level 1 binder locally, or open a phone window only on the class router. Close the door before leaving.</p>",
    outage: "<p>Use the dated saved benchmark. Record what a real wifi-off test would prove and what it would not.</p>",
    partner: "<ul><li>Offline observation</li><li>Fair two-model comparison</li><li>Fact checked outside model</li><li>Network door closed</li></ul>",
    spanish: "<p>Demuestra una respuesta sin wifi. Compara dos modelos. Verifica un dato. Crea un modelo con nombre.</p>",
    next: "<p>You own the toolbox. Next, build a front desk for a real business and try to break it before anyone else does.</p>",
    exit: "<p>Which job stays local? When is the cloud the better tool?</p>",
  },
  4 => {
    routes: "<ul><li>Core: public CSR case in a chat project, attacked in the same project</li><li>Alternate business: owner and instructor approval</li><li>Partner attacks: only after a clear yes</li><li>Outage: saved caller packet and saved before-and-after packet</li></ul>",
    anchors: "<ul><li>Sell the outcome, not the robot. / Vende el resultado, no el robot.</li><li>Fences, not promises. / Barreras, no promesas.</li><li>A secret it never saw cannot leak.</li></ul>",
    idea: "<p>A good front desk answers approved facts, takes a complete message, stops on unsafe work, and leaves action to a person.</p><p>A stranger's note and the owner's rules land on that desk as words. The model may follow the note. That is prompt injection.</p>",
    fence: "<ul><li>No invented price, timing, private contact, or high-stakes advice</li><li>No send, book, spend, or delete</li><li>Test only what you own or have permission to test</li><li>Use fake secrets. Never target a real outside system.</li></ul>",
    demo: "<p>Run a public fact and a missing price. Then run a hidden instruction and watch it land. Remove the fake secret. Show the message card, the log, and the switch.</p>",
    task1: "<p>Answer the case interview. Write trigger, steps, checks, failure routes, access list, and never list. Never list first.</p>",
    task1_check: "<p>A partner can tell what the desk does, cannot do, and hands to a human.</p>",
    task2: "<p>Build from approved files plus one fake code. Run five callers. Fix every miss and make one five-part message card.</p>",
    task2_check: "<p>Supported answers have receipts. Missing and high-stakes routes stop. The card has five fields.</p>",
    task3: "<p>Run all ten attacks and count. Mark untrusted text, remove the secret, require human action, name the log and switch. Rerun the same ten.</p>",
    task3_check: "<p>Same test, honest counts, fake secret absent, switch used. Then a sixty-second pitch with no AI, agent, or model.</p>",
    extension: "<p>Automate the same attacks only after manual proof; keep the key in an environment variable and inspect the log. Write a Vercel server-function boundary that keeps the secret out of browser code.</p>",
    outage: "<p>Use saved caller replies and the saved before-and-after packet. Rewrite each miss, complete the message card, and label the run not live.</p>",
    partner: "<ul><li>Six-part spec</li><li>Five test rows and a five-part card</li><li>Consent before attack</li><li>Same ten tests, fake secret absent</li><li>Switch used, outcome pitch</li></ul>",
    spanish: "<p>Escribe el trabajo y sus límites. Prueba cinco llamadas. Prueba diez ataques, aplica cuatro barreras y repite. Presenta el resultado en un minuto.</p>",
    next: "<p>You built all four projects and locked the last one. Next, choose one, improve it, cost it, and present it to the class.</p>",
    exit: "<p>What outcome does the owner receive? Which fence did the most?</p>",
  },
  5 => {
    routes: "<ul><li>Live build</li><li>Dated saved run</li><li>Recorded or partner-read presentation</li><li>Same eight proof items for every route</li></ul>",
    anchors: "<ul><li>Show the work, the miss, the fix, and the switch.</li><li>Working is not the same as proven.</li><li>El público debe poder repetir la prueba.</li></ul>",
    idea: "<p>The strongest project is not the one with the most code. It is the one whose claim, failure, repair, fence, and stop another person can inspect.</p>",
    fence: "<ul><li>Public or synthetic screen only</li><li>No keys, notifications, private tabs, or client data</li><li>Saved material is labeled saved</li><li>Deployment status is not browser proof</li></ul>",
    demo: "<p>Show a green deploy with no user result. Then show the eight-item proof board and one repeatable test.</p>",
    task1: "<p>Choose Documents, Watchman, Local Model, or Front Desk. Assemble all eight proof items and fill the cost sheet.</p>",
    task1_check: "<p>A partner can find ownership, before, change, normal, failure, fence, stop, cost, and reflection.</p>",
    task2: "<p>Run one fresh normal input, one fresh failure input, and the switch or fallback. Record expected and actual.</p>",
    task2_check: "<p>For deployed work, browser behavior, service health, and persistence claims are checked separately.</p>",
    task3: "<p>Rehearse and present: 30 seconds outcome, 60 normal, 45 miss and fix, 30 fence and stop, 15 cost and next step.</p>",
    task3_check: "<p>Three minutes. The class can follow the receipts. Works, honest, and theirs.</p>",
    extension: "<p>Show a Vercel frontend or Railway service only when the three separate checks are visible and safe.</p>",
    outage: "<p>State the unavailable dependency, last verified time, saved receipt, and exact check you would run now.</p>",
    partner: "<ul><li>All eight items</li><li>Repeatable normal test</li><li>Visible failure route</li><li>Used switch or fallback</li><li>Safe screen</li></ul>",
    spanish: "<p>Reúne ocho pruebas. Ejecuta una prueba normal y una falla. Usa el interruptor. Presenta durante tres minutos.</p>",
    next: "<p>Keep the project that solves a real job. Keep the test sheet beside it.</p>",
    exit: "<p>What will you keep using? What must a person still own?</p>",
  },
}.freeze

def slide(number, label, kicker, heading, body)
  <<~HTML
    <section class="slide#{number == 1 ? ' active' : ''}" tabindex="-1" aria-label="Slide #{number}: #{CGI.escapeHTML(label)}">
      <p class="kicker">#{kicker}</p>
      <h#{number == 1 ? 1 : 2}>#{heading}</h#{number == 1 ? 1 : 2}>
      #{body}
    </section>
  HTML
end

def render_deck(number, manifest, content)
  title = CGI.escapeHTML(manifest.fetch("title"))
  objective = CGI.escapeHTML(manifest.fetch("objective"))
  proof = CGI.escapeHTML(manifest.fetch("passing_proof"))
  slides = [
    slide(1, "Level #{number} title", "ZERO TO AGENT / PROJECT LAB / LEVEL #{number}", title, "<p class=\"muted\">Ninety minutes. Three tasks. One visible proof.</p>"),
    slide(2, "Class goal", "THE GOAL", "What leaves the room", "<p>#{objective}</p>"),
    slide(3, "Access routes", "START HERE", "Different devices. Same proof.", content.fetch(:routes)),
    slide(4, "Bilingual anchors", "ANCHORS / ANCLAS", "Say the lines together", content.fetch(:anchors)),
    slide(5, "Big idea", "THE BIG IDEA", "A picture before a term", content.fetch(:idea)),
    slide(6, "Safety stop", "SAFETY STOP / ALTO", "The fence comes first", content.fetch(:fence)),
    slide(7, "Live demonstration", "LIVE DEMO", "Watch the receipt, not the magic", content.fetch(:demo)),
    slide(8, "Task 1", "TASK 1", "Build the first piece", content.fetch(:task1)),
    slide(9, "Task 1 success check", "TASK 1 CHECK", "Success looks like this", content.fetch(:task1_check)),
    slide(10, "Task 2", "TASK 2", "Write expected. Then run.", content.fetch(:task2)),
    slide(11, "Task 2 success check", "TASK 2 CHECK", "Inspect the evidence", content.fetch(:task2_check)),
    slide(12, "Task 3", "TASK 3", "Change, stop, or present", content.fetch(:task3)),
    slide(13, "Task 3 success check", "TASK 3 CHECK", "Make the result visible", content.fetch(:task3_check)),
    slide(14, "Builder extension", "BUILDER EXTENSION", "More depth. Same passing proof.", content.fetch(:extension)),
    slide(15, "Outage route", "IF THE TOOL FAILS", "Use the saved route honestly", content.fetch(:outage)),
    slide(16, "Partner check", "PARTNER CHECK", "Can another person follow it?", content.fetch(:partner)),
    slide(17, "Passing proof", "PASSING PROOF", "Show the work", "<p>#{proof}</p>"),
    slide(18, "Spanish task summary", "RESUMEN EN ESPAÑOL", "Tres tareas. La misma evidencia.", content.fetch(:spanish)),
    slide(19, "Next level bridge", "NEXT", "Carry the proof forward", content.fetch(:next)),
    slide(20, "Exit ticket", "EXIT TICKET", "One answer before you leave", content.fetch(:exit)),
  ]

  <<~HTML
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="theme-color" content="#18221f">
      <title>Project Lab Level #{number} - #{title}</title>
      <style>
        :root { --bg:#121917; --panel:#19221f; --ink:#f2ede3; --muted:#bdc5bd; --signal:#e06a47; --line:#52605b; }
        * { box-sizing:border-box; }
        html, body { height:100%; }
        body { margin:0; overflow:hidden; background:var(--bg); color:var(--ink); font:clamp(18px,2vw,28px)/1.45 Manrope,system-ui,sans-serif; }
        .slide { position:absolute; inset:0; display:none; min-height:100vh; padding:7vh 8vw 14vh; flex-direction:column; justify-content:center; outline:none; }
        .slide.active { display:flex; }
        .kicker { margin:0 0 2vh; color:var(--signal); font:700 clamp(13px,1.2vw,18px)/1.4 "JetBrains Mono",ui-monospace,monospace; letter-spacing:.14em; text-transform:uppercase; }
        h1, h2 { max-width:20ch; margin:0 0 3vh; font-family:Fraunces,Georgia,serif; font-size:clamp(40px,6vw,90px); line-height:1.04; }
        h2 { font-size:clamp(34px,5vw,72px); }
        p, ul, ol { max-width:68ch; }
        p { margin:.35em 0; }
        ul, ol { margin:.5em 0; padding-left:1.3em; }
        li { margin:.35em 0; }
        .muted { color:var(--muted); }
        .signal { color:var(--signal); font-weight:800; }
        .controls { position:fixed; z-index:10; right:2vw; bottom:2vh; display:flex; align-items:center; gap:.7rem; padding:.45rem .65rem; border:1px solid var(--line); background:rgba(18,25,23,.96); }
        button { min-width:44px; min-height:44px; border:2px solid var(--muted); background:var(--panel); color:var(--ink); font:700 16px/1 system-ui,sans-serif; cursor:pointer; }
        button:hover, button:focus-visible { border-color:var(--signal); outline:3px solid transparent; }
        button:disabled { cursor:not-allowed; opacity:.35; }
        #counter { min-width:5.5em; text-align:center; font:14px/1.2 ui-monospace,monospace; }
        .help { position:fixed; left:2vw; bottom:3vh; color:var(--muted); font:13px/1.3 ui-monospace,monospace; }
        @media (max-width:720px) {
          .slide { width:100vw; max-width:100vw; overflow-y:auto; padding:5vh 6vw 20vh; }
          h1, h2, p, ul, ol { max-width:100%; overflow-wrap:anywhere; }
          h1 { font-size:clamp(36px,12vw,54px); }
          h2 { font-size:clamp(30px,10vw,46px); }
          .controls { left:6vw; right:6vw; justify-content:space-between; }
          #counter { min-width:auto; }
          .help { display:none; }
        }
        @media print {
          html, body { height:auto; overflow:visible; background:white; color:black; }
          .slide, .slide.active { position:relative; display:flex; min-height:7.5in; page-break-after:always; background:white; color:black; }
          .controls, .help { display:none; }
          .muted { color:#4d4944; }
        }
      </style>
    </head>
    <body>
      <main>
        #{slides.join("\n")}
      </main>
      <p class="help">Use Left/Right, Page Up/Page Down, Home/End, or the buttons.</p>
      <nav class="controls" aria-label="Slide controls">
        <button id="previous" type="button" aria-label="Previous slide">Back</button>
        <span id="counter" role="status" aria-live="polite">1 / 20</span>
        <button id="next" type="button" aria-label="Next slide">Next</button>
      </nav>
      <script>
        const slides = Array.from(document.querySelectorAll('.slide'));
        const previous = document.getElementById('previous');
        const next = document.getElementById('next');
        const counter = document.getElementById('counter');
        const requestedSlide = Number.parseInt(window.location.hash.slice(1), 10);
        let index = Number.isInteger(requestedSlide) ? requestedSlide - 1 : 0;
        function show(nextIndex) {
          index = Math.max(0, Math.min(slides.length - 1, nextIndex));
          slides.forEach(function (current, slideIndex) {
            const active = slideIndex === index;
            current.classList.toggle('active', active);
            current.setAttribute('aria-hidden', String(!active));
          });
          previous.disabled = index === 0;
          next.disabled = index === slides.length - 1;
          counter.textContent = (index + 1) + ' / ' + slides.length;
          history.replaceState(null, '', '#' + (index + 1));
          slides[index].focus({ preventScroll: true });
        }
        previous.addEventListener('click', function () { show(index - 1); });
        next.addEventListener('click', function () { show(index + 1); });
        document.addEventListener('keydown', function (event) {
          if (['ArrowRight','ArrowDown','PageDown',' '].includes(event.key)) { event.preventDefault(); show(index + 1); }
          if (['ArrowLeft','ArrowUp','PageUp'].includes(event.key)) { event.preventDefault(); show(index - 1); }
          if (event.key === 'Home') show(0);
          if (event.key === 'End') show(slides.length - 1);
        });
        show(index);
      </script>
    </body>
    </html>
  HTML
end

DECKS.each do |number, content|
  directory = File.join(COURSE, format("level-%02d", number))
  manifest = YAML.safe_load_file(File.join(directory, "level.yml"))
  FileUtils.mkdir_p(directory)
  File.write(File.join(directory, "slides.html"), render_deck(number, manifest, content))
end

puts "Built #{DECKS.length} Project Lab slide decks."
