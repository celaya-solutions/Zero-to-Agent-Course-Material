"""Browser controls for the fixed classroom desk. Drafts never trigger actions."""
import json
import streamlit as st
import httpx
import desk

st.set_page_config(page_title='The Front Desk | Zero to Agent', page_icon='📋', layout='centered')
st.title('The Front Desk')
st.caption('ZERO TO AGENT · LEVEL 4 · TRAINING ONLY')
st.write('Build a desk, test its limits, then show what changed. Use the supplied fictional messages. Every reply is a draft for a person to check.')
st.info('Local Ollama · gemma3:4b · No sending or booking tools')
try:
    desk.prepare()
    state = desk.control()
    st.subheader('1. Set the boundary')
    st.write(f"Phase: **{state['phase']}** · Desk: **{'ready' if state['enabled'] else 'paused'}**")
    left, right = st.columns(2)
    if left.button('Pause desk' if state['enabled'] else 'Resume desk', width='stretch'):
        desk.change('pause' if state['enabled'] else 'resume')
        st.rerun()
    if right.button('Apply four defenses', disabled=state['phase']=='locked', width='stretch'):
        desk.change('lock')
        st.rerun()
    st.caption('Lock removes fake private values from new requests, marks visitor text, retains draft-only access, and records controls. It cannot guarantee that every answer is correct.')
    st.write('During a long run, pause from a second terminal: `uv run --frozen zta pause front-desk`. An in-flight calculation may finish; its reply will be withheld.')
    st.subheader('2. Write expected, then run')
    group = st.radio('Practice set', ['callers', 'attacks'], format_func=lambda x: 'Five callers' if x=='callers' else 'Ten fixed attacks', horizontal=True)
    with st.expander('Read the test card before running'):
        for task in desk.tasks(group):
            st.markdown(f"**{task['id']} · {task['name']}**")
            st.text(task['prompt'])
            st.caption('Expected: '+task['expected'])
    if st.button('Run selected set', type='primary'):
        with st.status('Running locally. Completed replies are saved as they arrive.', expanded=True) as progress:
            with desk.client() as api:
                path = desk.run(group, api, on_row=lambda row: st.text(f"{row['id']}: {row['answer']}"))
            result = desk.read_json(path, {})
            progress.update(label=result['status'], state='complete')
            st.session_state['receipt_choice'] = path.name
    st.subheader('3. Read the receipts')
    files = sorted(desk.LOCAL.glob('run-*.json'), key=lambda p:p.stat().st_mtime, reverse=True)
    if files:
        chosen_name = st.selectbox('Saved run', [p.name for p in files], key='receipt_choice')
        chosen = desk.LOCAL/chosen_name
        result = desk.read_json(chosen, {})
        st.write(f"{result['phase']} · {result['group']} · {result['status']}")
        st.caption('An exact-match flag is a clue. It misses hints, translations, invented values, and other unsafe replies. Grade every row yourself.')
        for row in result['rows']:
            with st.expander(f"{row['id']} · {row['status']}"):
                st.text('Visitor: '+row['input'])
                st.text(row.get('answer', 'No reply delivered.'))
                st.write('Flags: '+', '.join(row['flags']))
        st.download_button('Download this run receipt', chosen.read_bytes(), file_name=chosen.name, mime='application/json')
    else:
        st.write('Your first run will appear here.')
    st.subheader('4. Make a message card')
    st.write('Use this supplied fictional request: River asks about an industrial document project, this week, afternoons. The public follow-up route is hello@celayasolutions.com. No reply time is promised.')
    st.code('Alias: River\nPublic route: hello@celayasolutions.com\nNeed: Industrial document project conversation\nUrgency: This week\nPreferred follow-up time: Afternoons (request, not a promise)', language=None)
    st.write('Complete your own worksheet in `.zta/front-desk/PROJECT-LAB-04.md`. Keep receipt names, verdicts, your repair, and pitch there. Upload to Level 4 and reopen it, or write “Not submitted.”')
except (httpx.HTTPError, ValueError, OSError):
    st.error('The desk stopped. Earlier rows are saved. Check Ollama and the preparation guide; no cloud retry was made.')
