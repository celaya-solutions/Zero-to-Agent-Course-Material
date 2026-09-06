"""A local document helper with an evidence worksheet that survives refresh."""
import json
import uuid
from pathlib import Path
import streamlit as st
from zta import __version__
from zta.documents import CLASS_FILES, build_index, inventory, retrieve
from zta.evidence import QUESTIONS, checks, export_markdown, valid_revision
from zta.providers import ProviderError, request_answer, request_estimate, RATES
from zta.storage import config, data_dir, now, progress, root, save_progress, settings

st.set_page_config(page_title="Your Documents Answer Back | Zero to Agent", page_icon="📄", layout="wide")
# Keep foregrounds and backgrounds in Streamlit's theme so a saved dark-mode
# preference cannot put white widget text on a custom light background.
st.markdown("""<style>
.stAppDeployButton {display:none;}
h1,h2,h3 {font-family: Georgia,serif;}
.stButton>button {border-radius:3px;}
/* Pair these course surfaces explicitly: nested Markdown must not inherit
   a saved theme's white text while the label or tab has a pale background. */
.stTabs [role="tablist"],
[data-testid="stFileUploader"] > [data-testid="stWidgetLabel"] {
    background-color:#f6f2e9 !important;
    color:#192a25 !important;
    opacity:1 !important;
}
.stTabs [role="tab"] {
    background-color:transparent !important;
    color:#192a25 !important;
    opacity:1 !important;
}
.stTabs [role="tab"] p,
[data-testid="stFileUploader"] > [data-testid="stWidgetLabel"] p {
    color:inherit !important;
    opacity:1 !important;
}
.stTabs [role="tab"][aria-selected="true"] {
    color:#236346 !important;
    font-weight:600;
}
</style>""", unsafe_allow_html=True)
try:
    cfg = config()
    options = settings()
    state = progress()
except (ValueError,OSError) as exc:
    st.error(str(exc)); st.stop()
index_path = data_dir()/"index.sqlite3"
assets = root()/"courses/project-lab/level-01/assets"

# Every callback reloads the most recent disk state, then updates just its field.
def field_change(key):
    current = progress()
    current["fields"][key] = st.session_state[key]
    save_progress(current)

def field(label, key, area=False):
    if key not in st.session_state:
        st.session_state[key] = state["fields"].get(key, "")
    fn = st.text_area if area else st.text_input
    return fn(label,key=key,on_change=field_change,args=(key,))

def set_class(name):
    current = progress(); current["classifications"][name] = st.session_state["class_"+name]; save_progress(current)

def set_verdict(run_id):
    current = progress()
    for run in current["runs"]:
        if run["id"] == run_id:
            run["verdict"] = st.session_state["verdict_"+run_id]
    save_progress(current)

def show_passages(passages, run=None):
    for passage in passages:
        label = f"{passage['source']} / {passage['heading']}"
        with st.expander(label):
            st.caption(f"{passage['class']} | Receipt {passage['id']} | Page {passage['page'] or 'not applicable'}")
            st.text(passage["text"])
            if run:
                if st.button("I opened and checked this source", key=f"open_{run['id']}_{passage['id']}"):
                    current=progress()
                    receipt={"at":now(),"run":run["id"],"number":run["number"],"source":passage["source"],"heading":passage["heading"],"quote":passage["text"]}
                    current["opened"].append(receipt); save_progress(current)
                    st.success("Source check recorded. Explain your comparison in Proof.")

st.caption("CELAYA SOLUTIONS LEARNING / ZERO TO AGENT / LEVEL 01")
st.title("Your Documents Answer Back")
st.write("Find the page. Check the answer. Show the proof.")
with st.sidebar:
    st.header("Your workspace")
    st.write(f"**Engine:** {cfg['provider']}")
    st.code(cfg["model"],language=None)
    st.caption(f"Course {__version__} · {options['max_passages']} passages per question")
    st.write("Local search stays on this computer.")
    if cfg["provider"] != "ollama":
        st.warning("Cloud answers send your question and selected passages to the chosen provider.")
        st.checkbox("I understand and will use only public or synthetic files",key="cloud_consent")
        incoming,outgoing=RATES[cfg["provider"]]
        st.caption(f"Model rate: ${incoming:g} per million input tokens / ${outgoing:g} per million output tokens. Check the current provider price before use.")
        st.caption("One request per click. No automatic retries. API billing is separate from coding-assistant access.")
    total=sum(r['result'].get('estimated_usd',0) for r in state["runs"])
    st.caption(f"Recorded API estimate: ${total:.4f}. Provider billing is authoritative. Rates checked 2026-09-06.")
    st.write("Stop the app: press **Ctrl+C** in its terminal.")
    st.caption("Private progress is saved in .zta/ and excluded from Git.")
    st.markdown("[Course materials](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material) · [Course sign in](https://learn.zerotoagent.org/auth/users/sign_in)")

start,binder,questions,improve,proof=st.tabs(["1 · Start", "2 · Binder", "3 · Five questions", "4 · Improve", "5 · Proof"])
with start:
    st.subheader("Three tasks. Ninety minutes.")
    st.write("Build a binder from four safe documents. Test five questions. Make one change and rerun.")
    st.info("Preparation comes first: fork the repo, install with uv, choose your coding assistant and answer engine, then run doctor.")
    field("Course nickname (not your legal name)","nickname")
    field("Coding assistant: Claude Code, Codex, or manual card","assistant")
    st.markdown("**Public facts are real. Training records are invented.** Never call a classroom rule a CSR policy.")
    st.write("A source receipt can be valid while the answer is wrong. Open the source and compare the claim yourself.")
    st.caption("Encuentra la página y después responde. Si falta información, detente.")
with binder:
    st.subheader("Build your binder")
    st.write("Load the four class documents, then build the searchable index. Only selected document text is indexed; lessons and answer keys are excluded.")
    if st.button("Load class binder",type="primary"):
        folder=data_dir()/"binder"; folder.mkdir(exist_ok=True)
        # Only replace documents within the app-owned binder folder.
        for old in folder.iterdir():
            if old.is_file(): old.unlink()
        for name in CLASS_FILES: (folder/name).write_bytes((assets/name).read_bytes())
        if index_path.exists(): index_path.unlink()
        st.success("Four documents loaded. Choose Build index next.")
    uploads=st.file_uploader("Or add approved documents (10 MB each; text PDF, Markdown, or UTF-8 text)",type=["md","txt","pdf"],accept_multiple_files=True)
    if st.button("Use uploaded binder",disabled=not uploads):
        # Parse before replacing any existing binder or index.
        from zta.documents import extract
        try:
            if len(uploads)>20: raise ValueError("Use at most 20 files.")
            if len({f.name for f in uploads})!=len(uploads): raise ValueError("Use distinct filenames.")
            for upload in uploads:
                if Path(upload.name).name!=upload.name or "\\" in upload.name: raise ValueError("Invalid filename.")
                extract(upload.name,upload.getvalue())
            folder=data_dir()/"binder"; folder.mkdir(exist_ok=True)
            for old in folder.iterdir():
                if old.is_file(): old.unlink()
            for upload in uploads: (folder/upload.name).write_bytes(upload.getvalue())
            if index_path.exists(): index_path.unlink()
            st.success("Uploaded binder saved. Build its index next.")
        except ValueError as exc: st.error(str(exc))
    folder=data_dir()/"binder"
    files=sorted(folder.iterdir()) if folder.exists() else []
    if st.button("Build index",disabled=not files):
        try:
            passages=build_index(index_path,[(p.name,p.read_bytes()) for p in files if p.is_file()])
            st.success(f"Indexed {len(files)} documents and {len(passages)} passages.")
        except (ValueError,OSError) as exc: st.error(str(exc))
    if files:
        st.write("Open each original below. Classify it before asking questions.")
        for path in files:
            key="class_"+path.name
            choices=["Choose","public","training-only","unclassified"]
            if key not in st.session_state: st.session_state[key]=state["classifications"].get(path.name,"Choose")
            st.selectbox(f"Classify {path.name}",choices,key=key,on_change=set_class,args=(path.name,))
            st.download_button(f"Open original: {path.name}",path.read_bytes(),file_name=path.name,key="original_"+path.name)
    current_passages=inventory(index_path)
    if current_passages:
        st.caption(f"Current index: {len({p['source'] for p in current_passages})} documents / {len(current_passages)} passages")
        show_passages(current_passages)
with questions:
    st.subheader("Predict, ask, inspect")
    st.write("Fill all five expected results before your first test. For each answer, inspect its passages and record Pass or Miss. A Miss is useful evidence.")
    for i,q in enumerate(QUESTIONS,1):
        field(f"{i}. {q} — expected behavior",f"expected_{i}",True)
    ready=all(st.session_state.get(f"expected_{i}","").strip() for i in range(1,6))
    if not ready: st.info("Save an expected result for all five questions to enable live tests.")
    for i,q in enumerate(QUESTIONS,1):
        st.markdown(f"#### Question {i}")
        st.write(q)
        preview=retrieve(index_path,q,options["max_passages"]) if index_path.exists() else []
        with st.expander(f"Preview retrieved evidence for question {i}"):
            for p in preview: st.text(f"{p['source']} / {p['heading']}\n{p['text']}")
        if cfg["provider"] != "ollama":
            estimate=request_estimate(cfg["provider"],q,preview)
            st.caption(f"Before you run: planning estimate ${estimate['usd']:.4f} for about {estimate['input_tokens']} input tokens and up to 800 output tokens. Actual tokenization and billing can differ; this is not a spending cap.")
        if st.button(f"Run question {i}",disabled=not ready or not index_path.exists(),key=f"run_{i}"):
            if cfg["provider"]!="ollama" and not st.session_state.get("cloud_consent"):
                st.error("Read the cloud notice and confirm the public/synthetic boundary in the sidebar.")
            else:
                try:
                    with st.spinner("Finding evidence and asking your selected model…"):
                        result=request_answer(cfg,q,preview) if preview else {"status":"not_found","answer":"Not in the documents.","citations":[],"seconds":0,"estimated_usd":0}
                    current=progress()
                    run={"id":uuid.uuid4().hex[:12],"at":now(),"number":i,"question":q,"expected":st.session_state[f"expected_{i}"],"provider":cfg["provider"],"model":cfg["model"],"settings":options,"passages":preview,"result":result,"verdict":"Choose","route":"live"}
                    current["runs"].append(run); save_progress(current); st.rerun()
                except ProviderError as exc: st.error(str(exc))
        runs=[r for r in state["runs"] if r["number"]==i]
        if runs:
            run=runs[-1]; result=run["result"]
            if result["status"]=="needs_review": st.warning("Needs review")
            else: st.caption(result["status"].replace("_"," ").title())
            st.text(result["answer"])
            if options["show_source_quotes"]:
                for c in result["citations"]: st.text(f"Source quote [{c['id']}]: {c['quote']}")
            st.caption(f"Run {run['id']} · {run['at']} · {result.get('seconds',0)} seconds · {run['route']}")
            cited={c['id'] for c in result['citations']}
            st.write("Source receipts used by this answer:")
            show_passages([p for p in run['passages'] if p['id'] in cited],run)
            key="verdict_"+run['id']
            if key not in st.session_state: st.session_state[key]=run.get('verdict','Choose')
            st.selectbox("My verdict",["Choose","Pass","Miss"],key=key,on_change=set_verdict,args=(run['id'],))
    with st.expander("Service unavailable? Use a labeled saved example"):
        st.write("This imports an authored classroom example. It is not a live model result. You still write expectations, inspect sources, and judge each answer.")
        if st.button("Load five saved examples",disabled=not ready):
            saved=json.loads((assets/'saved-runs.json').read_text(encoding="utf-8"))
            current=progress()
            for r in saved:
                r.update({"id":uuid.uuid4().hex[:12],"at":now(),"expected":st.session_state[f"expected_{r['number']}"],"verdict":"Choose","route":"saved classroom example"})
                current['runs'].append(r)
            save_progress(current); st.rerun()
with improve:
    st.subheader("One change. Same question.")
    st.write("Select a weak result and explain why it needs work. Keep the question unchanged. Use Claude Code, Codex, or the manual card to make one small edit.")
    st.code("Read the Level 1 instructions and inspect my recorded miss. Explain its likely cause before editing. Change one rule or retrieval setting that addresses it. Preserve the supplied documents, expected results, and tests. Show the change, explain why it should help, and tell me how to rerun the same question. Do not publish anything.",language=None,wrap_lines=True)
    st.markdown("**If all five pass:** in `projects/documents/settings.toml`, change `max_passages = 4` to `1`. Save, refresh the app, and rerun question 5. Inspect the missing evidence. Restore `4`, save, refresh, and rerun the same question. Compare the passages, even if the model safely refused both times.")
    st.markdown("**Keep a useful change:** set `show_source_quotes = true` in that same file. Save, refresh, and rerun your selected question. Supporting quotes will now appear below its answer. Commit that improvement; leave `max_passages = 4`.")
    runs=state['runs']
    if len(runs)>=2:
        labels={r['id']:f"Q{r['number']} · {r['at']} · {r['id']} · {r['route']}" for r in runs}
        with st.form('revision'):
            before=st.selectbox('Before run',list(labels),format_func=labels.get)
            after=st.selectbox('After run',list(labels),index=len(labels)-1,format_func=labels.get)
            change=st.text_area('One change I made',value=state['revision'].get('change',''))
            reason=st.text_area('What changed in the evidence or answer, and why?',value=state['revision'].get('reason',''))
            if st.form_submit_button('Save before and after'):
                a=next(r for r in runs if r['id']==before); b=next(r for r in runs if r['id']==after)
                candidate={'before':before,'after':after,'question':a['number'],'change':change,'reason':reason,'valid':True}
                if not valid_revision({'runs':runs,'revision':candidate}):
                    st.error('Choose an earlier BEFORE and a later AFTER run of the SAME question, and explain the change and result.')
                else:
                    current=progress(); current['revision']=candidate; save_progress(current); st.success('Revision evidence saved.')
    else: st.info('Run the same question at least twice before recording your improvement.')
with proof:
    st.subheader("Save the work. Confirm receipt.")
    field('Your fork URL','fork_url')
    field('Your final commit URL','commit_url')
    field('What did you compare in the two public sources?','source_check',True)
    field('What stays on this computer, and what leaves it on your route?','data_boundary',True)
    field('Unresolved misses, account blocks, or saved-run use','unresolved',True)
    field('Exit ticket: one missing-information rule and one conflict rule','exit_ticket',True)
    current=progress()
    for label,passed in checks(current).items():
        st.write(('Complete: ' if passed else 'Incomplete: ')+label)
    text=export_markdown(current,cfg)
    st.download_button('Export PROJECT-LAB-01.md',text,file_name='PROJECT-LAB-01.md',mime='text/markdown')
    if not all(checks(current).values()): st.warning('This is a draft packet: finish the incomplete items before submitting, or explain the access block to your instructor.')
    st.write('In GitHub Desktop, review only your intended project change. Commit and push it to your own fork. Keep .zta/ and this evidence file private.')
    st.write('Sign in to the course platform, open Level 1, upload PROJECT-LAB-01.md, then reopen Submission History and check the file and timestamp. Downloading here does not submit it.')
    st.caption('If the platform is down, keep the file and record the block. After two attempts or five minutes, use the saved route and ask the instructor for the next submission check.')
