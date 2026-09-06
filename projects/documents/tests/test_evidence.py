import json
from zta.evidence import export_markdown,checks
from zta.storage import write_json,read_json

def test_atomic_progress_survives_reload(tmp_path):
    path=tmp_path/'progress.json'
    expected={'fields':{'nickname':'Class learner','expected_1':'Source-backed city'},'runs':[]}
    write_json(path,expected)
    assert read_json(path,{})==expected
    assert not list(tmp_path.glob('.save-*'))

def test_export_is_private_draft_without_fake_receipt():
    state={'fields':{'nickname':'sk-testsecret123456789012345'},'runs':[],'opened':[],'classifications':{},'revision':{}}
    text=export_markdown(state,{'provider':'openai','model':'test','api_key':'sk-testsecret123456789012345'})
    assert 'sk-testsecret' not in text
    assert '[REDACTED]' in text
    assert 'Incomplete:' in text
    assert 'Exporting this file does not submit it' in text
    assert '[pending]' not in text


def test_revision_requires_real_same_question_runs_in_order():
    from zta.evidence import valid_revision
    state={'runs':[{'id':'first','number':5,'question':'Conflict?'},{'id':'second','number':5,'question':'Conflict?'}], 'revision':{'before':'first','after':'second','change':'Restore evidence coverage','reason':'Both records now retrieved'}}
    assert valid_revision(state)
    state['revision']['after']='first'
    assert not valid_revision(state)
    state['revision'].update(before='second',after='first')
    assert not valid_revision(state)
    state['revision'].update(before='first',after='second')
    state['runs'][1]['question']='Different question'
    assert not valid_revision(state)


def test_commit_must_point_into_recorded_fork():
    from zta.evidence import valid_fork_links
    fields={'fork_url':'https://github.com/student/course','commit_url':'https://github.com/student/course/commit/abcdef1'}
    assert valid_fork_links(fields)
    fields['commit_url']='https://github.com/'
    assert not valid_fork_links(fields)
    fields['commit_url']='https://github.com/another/course/commit/abcdef1'
    assert not valid_fork_links(fields)


def test_export_hash_matches_canonical_body():
    import hashlib,re
    text=export_markdown({'fields':{},'runs':[]},{'provider':'ollama','model':'test'})
    digest=re.search(r'SHA256: +([0-9a-f]{64})',text).group(1)
    assert digest==hashlib.sha256((text.split('```',2)[2].strip()+'\n').encode()).hexdigest()
