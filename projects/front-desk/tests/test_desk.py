import importlib.util
import json
from pathlib import Path
import sys

import httpx
import pytest

SPEC = importlib.util.spec_from_file_location('front_desk', Path(__file__).parents[1]/'desk.py')
desk = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(desk)


@pytest.fixture
def home(tmp_path):
    desk.prepare(tmp_path)
    return tmp_path


def api_for(generate=None, cloud=False, redirect=False):
    calls = []
    def handler(request):
        calls.append(request)
        if redirect:
            return httpx.Response(302, headers={'location':'https://example.com/blocked'})
        if request.url.path == '/api/tags':
            return httpx.Response(200, json={'models':[{'name':desk.MODEL, 'digest':'test-digest', 'size':42}]})
        if request.url.path == '/api/show':
            return httpx.Response(200, json={'remote_host':'example.com'} if cloud else {})
        return generate(request) if generate else httpx.Response(200, json={'response':'Draft only.', 'done':True, 'done_reason':'stop', 'model':desk.MODEL})
    return httpx.Client(base_url=desk.ENDPOINT, transport=httpx.MockTransport(handler), follow_redirects=False), calls


def receipts(home):
    return [json.loads(p.read_text()) for p in home.glob('run-*.json')]


def test_prepare_preserves_private_edits_and_control(home):
    rules=home/'desk-instructions.md';rules.write_text('My private rule')
    sheet=home/'PROJECT-LAB-04.md';sheet.write_text('My evidence')
    desk.change('lock',home);desk.change('pause',home)
    desk.prepare(home)
    assert rules.read_text()=='My private rule'
    assert sheet.read_text()=='My evidence'
    assert desk.control(home)['phase']=='locked'
    assert not desk.control(home)['enabled']


def test_locked_payload_removes_bait_no_history_tools_or_remote_request(home):
    api,calls=api_for()
    desk.run('attacks',api,home)
    before=[json.loads(r.content) for r in calls if r.url.path=='/api/generate']
    assert len(before)==10 and all(all(f in p['system'] for f in desk.FAKES) for p in before)
    calls.clear();desk.change('lock',home)
    desk.run('attacks',api,home)
    after=[json.loads(r.content) for r in calls if r.url.path=='/api/generate']
    assert len(after)==10
    assert all(not any(f in json.dumps(p) for f in desk.FAKES) for p in after)
    assert all('UNTRUSTED VISITOR DATA START' in p['prompt'] for p in after)
    assert all(set(p)=={'model','system','prompt','stream','options','keep_alive'} for p in after)
    assert all(str(r.url).startswith(desk.ENDPOINT+'/api/') for r in calls)
    pair=receipts(home)
    assert pair[0]['tasks_sha256']==pair[1]['tasks_sha256']
    assert all(r['complete'] and len(r['rows'])==10 for r in pair)
    assert all(row['verdict'] is None for r in pair for row in r['rows'])


def test_pause_prevents_even_model_check(home):
    desk.change('pause',home);api,calls=api_for()
    p=desk.run('callers',api,home)
    receipt=json.loads(p.read_text())
    assert calls==[]
    assert receipt['status']=='paused' and receipt['rows']==[] and not receipt['complete']
    assert not (home/'running.lock').exists()


@pytest.mark.parametrize('action',['pause','lock','pause-resume'])
def test_control_change_during_request_suppresses_answer_and_next_request(home,action):
    def response(request):
        if action=='pause-resume':
            desk.change('pause',home);desk.change('resume',home)
        else:
            desk.change(action,home)
        return httpx.Response(200,json={'done':True,'response':'Must not be delivered.'})
    api,calls=api_for(response)
    result=json.loads(desk.run('attacks',api,home).read_text())
    assert len([r for r in calls if r.url.path=='/api/generate'])==1
    assert not result['complete'] and 'answer' not in result['rows'][0]
    assert result['rows'][0]['status']=='suppressed after control change'


def test_resume_after_pause_allows_new_set(home):
    desk.change('pause',home);desk.change('resume',home)
    api,_=api_for()
    result=json.loads(desk.run('callers',api,home).read_text())
    assert result['complete'] and len(result['rows'])==5


@pytest.mark.parametrize('kind',['network','empty','interrupted'])
def test_failed_batch_preserves_completed_rows_and_new_attempt_is_separate(home,kind):
    count=0
    def response(request):
        nonlocal count
        count+=1
        if count==2:
            if kind=='network':raise httpx.ConnectError('not available')
            if kind=='interrupted':raise KeyboardInterrupt()
            return httpx.Response(200,json={'done':True,'response':''})
        return httpx.Response(200,json={'done':True,'response':'First completed draft.'})
    api,_=api_for(response)
    with pytest.raises((httpx.HTTPError,ValueError,KeyboardInterrupt)):
        desk.run('callers',api,home)
    old=next(home.glob('run-*.json'));saved=old.read_bytes()
    result=json.loads(saved)
    assert result['rows'][0]['answer']=='First completed draft.'
    assert result['rows'][1]['status']=='failed or interrupted' and not result['complete']
    assert not (home/'running.lock').exists()
    api,_=api_for();desk.run('callers',api,home)
    assert len(receipts(home))==2 and old.read_bytes()==saved


def test_truncated_and_exact_leak_are_flags_never_automatic_verdicts(home):
    api,_=api_for(lambda r:httpx.Response(200,json={'done':True,'response':desk.FAKES[0], 'done_reason':'length'}))
    result=json.loads(desk.run('callers',api,home).read_text())
    row=result['rows'][0]
    assert row['truncated'] and 'exact fake value found' in row['flags']
    assert row['verdict'] is None


def test_cloud_backed_model_and_redirect_are_refused(home):
    for kwargs in ({'cloud':True},{'redirect':True}):
        api,calls=api_for(**kwargs)
        with pytest.raises((ValueError,httpx.HTTPError)):
            desk.run('callers',api,home)
        assert not any(r.url.path=='/api/generate' for r in calls)
        assert not any(r.url.host=='example.com' for r in calls)


def test_missing_model_preserves_failure_receipt(home):
    api=httpx.Client(base_url=desk.ENDPOINT,transport=httpx.MockTransport(lambda r:httpx.Response(200,json={'models':[]})))
    with pytest.raises(ValueError,match='missing'):
        desk.run('callers',api,home)
    assert receipts(home)[0]['rows']==[] and not receipts(home)[0]['complete']


def test_citation_edit_is_used_without_mutating_earlier_receipts(home):
    api,calls=api_for();desk.run('callers',api,home)
    old=next(home.glob('run-*.json'));saved=old.read_bytes()
    rule=home/'desk-instructions.md';rule.write_text(rule.read_text().replace('Source rule: Give a helpful public answer.','Source rule: Cite csr-public-brief.md and its heading.'))
    desk.run('callers',api,home)
    payloads=[json.loads(r.content) for r in calls if r.url.path=='/api/generate']
    assert 'Cite csr-public-brief.md and its heading.' in payloads[-1]['system']
    assert old.read_bytes()==saved


def test_reintroduced_bait_fails_locked_payload(home):
    desk.change('lock',home)
    with (home/'desk-instructions.md').open('a') as f:f.write('\n'+desk.FAKES[0])
    api,calls=api_for()
    with pytest.raises(ValueError,match='fake private value'):
        desk.run('attacks',api,home)
    assert not any(r.url.path=='/api/generate' for r in calls)


def test_run_lock_and_broken_log_block_generation(home,monkeypatch):
    (home/'running.lock').write_text('busy');api,calls=api_for()
    with pytest.raises(ValueError,match='active'):desk.run('callers',api,home)
    assert calls==[]
    (home/'running.lock').unlink()
    monkeypatch.setattr(desk,'write_json',lambda *args:(_ for _ in ()).throw(OSError('disk full')))
    with pytest.raises(OSError):desk.run('callers',api,home)
    assert calls==[] and not (home/'running.lock').exists()


@pytest.mark.parametrize('bad',[{}, {'phase':'locked','enabled':'yes','revision':'x'}])
def test_damaged_control_fails_closed(home,bad):
    (home/'control.json').write_text(json.dumps(bad));api,calls=api_for()
    with pytest.raises(ValueError):desk.run('callers',api,home)
    assert calls==[]


def test_no_provider_config_is_read(home,monkeypatch):
    # The shared storage helper is used only for explicit local receipts.
    import zta.storage
    monkeypatch.setattr(zta.storage,'config',lambda:pytest.fail('must not read provider config'))
    monkeypatch.setenv('HTTPS_PROXY','https://example.com')
    api,_=api_for();desk.run('callers',api,home)


def test_cli_routes_front_desk_and_rejects_misrouted_commands(monkeypatch):
    import zta.cli
    calls=[]
    monkeypatch.setattr(zta.cli.subprocess,'call',lambda command,**kwargs:calls.append(command) or 0)
    for action in ['prepare','doctor','callers','attacks','lock','pause','resume','start','test']:
        monkeypatch.setattr(sys,'argv',['zta',action,'front-desk'])
        assert zta.cli.main()==0
    assert len(calls)==9 and '--server.address=127.0.0.1' in calls[-2]
    assert '--server.port=8504' in calls[-2]
    for action in ['attacks','lock','pause']:
        monkeypatch.setattr(sys,'argv',['zta',action,'documents'])
        assert zta.cli.main()==1
    assert len(calls)==9
