import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import httpx
import pytest

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('local_lab', ROOT/'projects/local-models/lab.py')
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


def api_for(handler):
    return httpx.Client(base_url=lab.ENDPOINT, transport=httpx.MockTransport(handler), follow_redirects=False)


def route(request):
    body = json.loads(request.content) if request.content else {}
    if request.url.path == '/api/tags':
        return httpx.Response(200, json={'models': [dict(name=n,size=123,digest='sha256:abc') for n in lab.MODELS+(lab.CUSTOM,)]})
    if request.url.path == '/api/show':
        return httpx.Response(200, json={'modelfile': 'FROM local-blob'})
    return httpx.Response(200, json={'done': True, 'response': 'Test answer.', 'done_reason': 'stop'})


def test_benchmark_uses_same_prompts_and_keeps_human_fields_blank(tmp_path):
    requests = []
    def handler(request):
        requests.append(request)
        return route(request)
    with api_for(handler) as api:
        path = lab.run('benchmark', api, tmp_path)
    result = json.loads(path.read_text())
    assert result['complete'] and len(result['runs']) == 6
    assert result['network_disconnect_observed'] is None
    for a,b in zip(result['runs'][:3],result['runs'][3:]):
        assert a['prompt_sha256'] == b['prompt_sha256']
        assert a['options'] == b['options']
        assert a['quality_score'] is None and a['source_verdict'] is None
        assert a['seconds_to_complete'] >= 0
        assert a['digest'] == 'sha256:abc'
    generated=[json.loads(r.content) for r in requests if r.url.path=='/api/generate']
    assert len(generated)==8  # 2 initial unloads and 6 measured requests
    assert all(r['keep_alive']==0 for r in generated)
    assert 'El Paso, Texas' in result['runs'][1]['prompt']
    assert all(str(r.url).startswith(lab.ENDPOINT+'/') for r in requests)


def test_prepare_does_not_overwrite_student_work(tmp_path):
    lab.prepare(tmp_path)
    (tmp_path/'PROJECT-LAB-03.md').write_text('private work')
    (tmp_path/'Modelfile').write_text('my edited rule')
    lab.prepare(tmp_path)
    assert (tmp_path/'PROJECT-LAB-03.md').read_text() == 'private work'
    assert (tmp_path/'Modelfile').read_text() == 'my edited rule'


def test_failed_later_request_preserves_partial_evidence(tmp_path):
    calls=0
    def handler(request):
        nonlocal calls
        if request.url.path=='/api/generate' and 'prompt' in json.loads(request.content):
            calls+=1
            if calls==2:
                return httpx.Response(500)
        return route(request)
    with api_for(handler) as api, pytest.raises(httpx.HTTPStatusError):
        lab.run('benchmark',api,tmp_path)
    result=json.loads(next(tmp_path.glob('*.json')).read_text())
    assert len(result['runs'])==1 and not result['complete'] and result['error']


@pytest.mark.parametrize('response', [{'done':False,'response':'partial'}, {'done':True,'response':''}])
def test_incomplete_answers_are_not_success(response):
    with api_for(lambda request:httpx.Response(200,json=response)) as api, pytest.raises(ValueError):
        lab.generate(api,lab.MODELS[0],'hello',{})


def test_token_cap_keeps_answer_but_marks_incomplete():
    with api_for(lambda request:httpx.Response(200,json={'done':True,'response':'cut off','done_reason':'length'})) as api:
        assert lab.generate(api,lab.MODELS[0],'hello',{})['truncated']


@pytest.mark.parametrize('location', ['show','tags'])
def test_cloud_metadata_refused(location):
    def handler(request):
        if request.url.path=='/api/'+location:
            data={'remote_host':'https://remote.invalid'}
            if location=='tags':data={'models':[dict(name=lab.MODELS[0],**data)]}
            return httpx.Response(200,json=data)
        return route(request)
    with api_for(handler) as api, pytest.raises(ValueError,match='Cloud'):
        lab.installed(api,[lab.MODELS[0]])


def test_missing_model_is_not_downloaded():
    calls=[]
    def handler(request):
        calls.append(request.url.path)
        return httpx.Response(200,json={'models':[]})
    with api_for(handler) as api, pytest.raises(ValueError,match='missing'):
        lab.installed(api,[lab.MODELS[0]])
    assert calls==['/api/tags']


def test_unknown_name_refused():
    with api_for(route) as api, pytest.raises(ValueError,match='only'):
        lab.installed(api,['remote-cloud'])


def test_redirect_not_followed():
    calls=[]
    def handler(request):
        calls.append(str(request.url))
        return httpx.Response(307,headers={'location':'https://remote.invalid/api/tags'})
    with api_for(handler) as api, pytest.raises(httpx.HTTPStatusError):
        lab.installed(api,[lab.MODELS[0]])
    assert len(calls)==1


def test_client_ignores_host_and_proxy_environment(monkeypatch):
    monkeypatch.setenv('HTTP_PROXY','http://remote.invalid:80')
    monkeypatch.setenv('OLLAMA_HOST','https://remote.invalid')
    with lab.client() as api:
        assert str(api.base_url)==lab.ENDPOINT
        assert not api.trust_env and not api.follow_redirects


def test_custom_create_has_fixed_name_local_host_and_no_proxy(tmp_path,monkeypatch):
    lab.prepare(tmp_path)
    called=[]
    monkeypatch.setenv('OLLAMA_HOST','https://remote.invalid')
    monkeypatch.setenv('HTTP_PROXY','http://remote.invalid')
    monkeypatch.setattr(lab.subprocess,'run',lambda args,**kwargs:called.append((args,kwargs)))
    with api_for(route) as api:
        lab.create(api,tmp_path)
    args,kwargs=called[0]
    assert args[:3]==['ollama','create',lab.CUSTOM]
    assert kwargs['env']['OLLAMA_HOST']==lab.ENDPOINT
    assert 'HTTP_PROXY' not in kwargs['env']
    assert kwargs['env']['OLLAMA_NO_CLOUD']=='1'


def test_custom_remote_base_refused(tmp_path):
    (tmp_path/'Modelfile').write_text('FROM remote-cloud\nSYSTEM hello')
    with api_for(route) as api, pytest.raises(ValueError,match='Keep FROM'):
        lab.create(api,tmp_path)


def test_repeat_runs_keep_distinct_receipts(tmp_path):
    with api_for(route) as api:
        a=lab.run('offline',api,tmp_path)
        b=lab.run('offline',api,tmp_path)
    assert a!=b and a.exists() and b.exists()


def test_named_check_uses_identical_before_after_prompts(tmp_path):
    with api_for(route) as api:
        path=lab.run('check',api,tmp_path)
    runs=json.loads(path.read_text())['runs']
    assert [r['id'] for r in runs]==['writing','missing']
    assert all(r['model']==lab.CUSTOM for r in runs)
    assert [r['prompt'] for r in runs]==[p['prompt'] for p in lab.prompts() if p['id'] in ('writing','missing')]


def test_level3_command_cannot_start_documents():
    # Exercise the installed entry point since cli.py deliberately has no module launch hook.
    result=subprocess.run([str(Path(sys.executable).parent/'zta'),'offline','documents'],cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==1 and 'requires the local-models project' in result.stderr
