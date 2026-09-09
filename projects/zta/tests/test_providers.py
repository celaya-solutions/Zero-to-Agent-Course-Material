import json
import httpx
import pytest
from zta.providers import request_answer,validate_answer,ProviderError
P=[{'id':'one','source':'a.md','heading':'Place','page':None,'class':'public','text':'The lab is based in El Paso, Texas.'}]
ANSWER={'status':'answered','answer':'El Paso, Texas.','citations':[{'id':'one','quote':'El Paso, Texas.'}]}

@pytest.mark.parametrize('provider',['ollama','claude','openai'])
def test_adapter_payload_and_receipts(provider):
    calls=[]
    def respond(request):
        body=json.loads(request.content);calls.append(body)
        assert 'selected' not in body # payload carries the actual passages via prompt
        if provider=='ollama': return httpx.Response(200,json={'message':{'content':json.dumps(ANSWER)}})
        if provider=='claude': return httpx.Response(200,json={'content':[{'type':'text','text':json.dumps(ANSWER)}],'usage':{'input_tokens':30,'output_tokens':20}})
        assert body['store'] is False
        assert body['text']['format']['strict'] is True
        return httpx.Response(200,json={'output':[{'content':[{'type':'output_text','text':json.dumps(ANSWER)}]}],'usage':{'input_tokens':30,'output_tokens':20}})
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        result=request_answer({'provider':provider,'model':'test','api_key':'class-test-only'},'Where?',P,client)
    assert result['answer']=='El Paso, Texas.'
    assert len(calls)==1

@pytest.mark.parametrize('code',[401,402,403,404,429,500])
def test_failure_has_no_retry_or_secret(code):
    calls=[]
    def respond(req):calls.append(req);return httpx.Response(code,json={'error':'SUPER_PRIVATE_KEY'})
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        with pytest.raises(ProviderError) as error:
            request_answer({'provider':'openai','model':'test','api_key':'SUPER_PRIVATE_KEY'},'Where?',P,client)
    assert len(calls)==1
    assert 'SUPER_PRIVATE_KEY' not in str(error.value)

def test_missing_key_never_sends():
    def respond(req):pytest.fail('Request sent without key')
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        with pytest.raises(ProviderError):request_answer({'provider':'claude','model':'test'},'Where?',P,client)

@pytest.mark.parametrize('data',[
    {'status':'answered','answer':'A guess','citations':[]},
    {'status':'answered','answer':'A guess','citations':[{'id':'invented','quote':'El Paso'}]},
    {'status':'answered','answer':'A guess','citations':[{'id':'one','quote':'A fake quote'}]},
    {'status':'conflict','answer':'A conflict','citations':[{'id':'one','quote':'El Paso'}]},
    [],{},None,
])
def test_invalid_receipts_fail_closed(data):
    assert validate_answer(data,P)['status']=='needs_review'

def test_not_found_cannot_smuggle_guessed_price():
    result=validate_answer({'status':'not_found','answer':'Maybe $1000','citations':[]},P)
    assert result['answer']=='Not in the documents.'
