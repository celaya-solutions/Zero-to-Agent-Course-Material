"""Private Markdown evidence; a valid receipt does not prove a claim is correct."""
import json
import re
from . import __version__
from .storage import now, redact

QUESTIONS = [
    "Where is Celaya Solutions Research based?",
    "What kind of systems does the lab build?",
    "Which public contact route should I use for a research collaboration, and what work does the lab focus on?",
    "What is the price of a custom deployment?",
    "Which routing label and review target should be used for a research collaboration in this exercise?",
]

def valid_revision(state):
    revision=state.get("revision",{})
    runs=state.get("runs",[])
    ids=[run["id"] for run in runs]
    before,after=revision.get("before"),revision.get("after")
    if before not in ids or after not in ids or ids.index(before)>=ids.index(after):return False
    a,b=runs[ids.index(before)],runs[ids.index(after)]
    return a["number"]==b["number"] and a["question"]==b["question"] and all(str(revision.get(k,"")).strip() for k in ("change","reason"))

def valid_fork_links(fields):
    fork=fields.get("fork_url","").rstrip("/")
    commit=fields.get("commit_url","")
    return bool(re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",fork) and re.fullmatch(re.escape(fork)+r"/commit/[0-9a-fA-F]{7,40}",commit))

def checks(state):
    fields = state.get("fields", {})
    runs = state.get("runs", [])
    latest = {r["number"]: r for r in runs}
    from .documents import CLASS_FILES
    classes = state.get("classifications", {})
    return {
        "Four documents classified correctly": all(classes.get(n)==("public" if n.startswith("public-") else "training-only") for n in CLASS_FILES),
        "Five expectations saved before asking": all(latest.get(i,{}).get("expected") for i in range(1,6)),
        "Five test rows have learner verdicts": all(latest.get(i,{}).get("verdict") in {"Pass", "Miss"} for i in range(1,6)),
        "Both public sources opened for question 3": {"public-identity-and-work.md", "public-contact-and-method.md"}.issubset({o["source"] for o in state.get("opened",[]) if o.get("number")==3}),
        "Same-question before and after recorded": valid_revision(state),
        "Fork and commit links recorded": valid_fork_links(fields),
        "Identity and exit ticket complete": all(fields.get(k, "").strip() for k in ["nickname", "assistant", "source_check", "data_boundary", "exit_ticket"]),
    }

def export_markdown(state, config):
    f = state.get("fields", {})
    lines = ["# Level 1 - Your Documents Answer Back", "", "```text", "Document:    Level 1 - Learner Evidence", "Version:     v1.0.0", "Author:      Celaya Solutions", "Contact:     hello@celayasolutions.com", f"Date:        {now()[:10]}", "SHA256:      [pending]", "Chain:       n/a", "Tx:          [not anchored]", "License:     All Rights Reserved / Celaya Solutions", "```", "", f"Course release: {__version__}", f"Nickname: {f.get('nickname','')}", f"Coding assistant: {f.get('assistant','')}", f"Answer engine: {config['provider']} / {config['model']}", f"Fork: {f.get('fork_url','')}", f"Commit: {f.get('commit_url','')}", "", "## Completion checks"]
    for name, passed in checks(state).items():
        lines.append(f"- {'Complete' if passed else 'Incomplete'}: {name}")
    lines += ["", "## Document classification"]
    for name, kind in state.get("classifications",{}).items():
        lines.append(f"- {name}: {kind}")
    for n, r in enumerate(state.get("runs",[]),1):
        lines += ["", f"## Run {n} - Question {r['number']}", f"Run ID: {r['id']}", f"Time: {r['at']}", f"Route: {r.get('route','live')}", f"Question: {r['question']}", f"Expected BEFORE asking: {r['expected']}", f"Engine: {r['provider']} / {r['model']}", f"Settings: {json.dumps(r['settings'])}", f"Status: {r['result']['status']}", f"Learner verdict: {r.get('verdict','Not recorded')}", "", "### Observed answer", r['result']['answer'], "", "### Retrieved passages"]
        for p in r['passages']:
            lines += [f"- {p['id']}: {p['source']} / {p['heading']} / page {p['page'] or 'n/a'} / {p['class']}", "> "+p['text'].replace("\n","\n> ")]
        lines += ["", "### Citation quotes", *[f"- {c['id']}: {c['quote']}" for c in r['result']['citations']]]
    lines += ["", "## Sources opened by the learner", json.dumps(state.get("opened",[]), indent=2), "", "## Before, change, after", json.dumps(state.get("revision",{}), indent=2), "", "## Source check", f.get("source_check",""), "", "## Data boundary", f.get("data_boundary",""), "", "## Unresolved misses or fallback", f.get("unresolved","None recorded"), "", "## Exit ticket", f.get("exit_ticket",""), "", "## Submission receipt", "After upload, record the receipt time in the platform. Exporting this file does not submit it.", ""]
    content = redact("\n".join(lines), config.get("api_key",""))
    import hashlib
    body = content.split("```",2)[2].strip()+"\n"
    return content.replace("SHA256:      [pending]", "SHA256:      "+hashlib.sha256(body.encode()).hexdigest(), 1)
