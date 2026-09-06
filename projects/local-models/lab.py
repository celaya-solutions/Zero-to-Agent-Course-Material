"""Level 3: a fixed local endpoint, supplied prompts, and private run receipts."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid

import httpx

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'courses/project-lab/level-03/assets'
LOCAL = ROOT / '.zta/local-models'
MODELS = ('gemma3:1b', 'gemma3:4b')
CUSTOM = 'zta-desk:latest'
ENDPOINT = 'http://127.0.0.1:11434'
OPTIONS = {'temperature': 0.2, 'seed': 42, 'num_ctx': 4096, 'num_predict': 256}


def client():
    # Never inherit a proxy or redirect to a remote provider.
    return httpx.Client(base_url=ENDPOINT, timeout=httpx.Timeout(180, connect=5),
                        trust_env=False, follow_redirects=False)


def request(api, method, path, **kwargs):
    response = api.request(method, path, **kwargs)
    response.raise_for_status()
    return response.json()


def installed(api, names):
    entries = request(api, 'GET', '/api/tags').get('models', [])
    found = {m['name']: m for m in entries}
    for name in names:
        if name not in MODELS + (CUSTOM,):
            raise ValueError('Use only the two course models or zta-desk:latest.')
        if name not in found:
            raise ValueError(f'{name} is missing. Complete preparation before disconnecting; no download was attempted.')
        details = request(api, 'POST', '/api/show', json={'model': name})
        if any(details.get(k) or found[name].get(k) for k in ('remote_host', 'remote_model')):
            raise ValueError('Cloud-backed models are not allowed in the local lab.')
    return {name: found[name] for name in names}


def prepare(directory=LOCAL):
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    for source, name in [(ASSETS/'Modelfile.template', 'Modelfile'),
                         (ASSETS.parent/'worksheet.md', 'PROJECT-LAB-03.md')]:
        target = directory/name
        try:
            with target.open('x', encoding='utf-8') as f:
                f.write(source.read_text(encoding='utf-8'))
            target.chmod(0o600)
        except FileExistsError:
            pass
    print('Private worksheet and Modelfile ready in .zta/local-models/. Existing work preserved.')


def prompts():
    data = json.loads((ASSETS/'prompts.json').read_text(encoding='utf-8'))
    source = (ASSETS.parent.parent/'level-01/assets/public-identity-and-work.md').read_text(encoding='utf-8')
    return [{**p, 'prompt': p['prompt'].replace('{PUBLIC_SOURCE}', source)} for p in data]


def generate(api, model, prompt, metadata):
    start = time.perf_counter()
    result = request(api, 'POST', '/api/generate', json={
        'model': model, 'prompt': prompt, 'stream': False,
        'options': OPTIONS, 'keep_alive': 0,
    })
    elapsed = time.perf_counter() - start
    answer = result.get('response', '')
    if not result.get('done') or not isinstance(answer, str) or not answer.strip():
        raise ValueError('No complete non-empty response. Record a failed attempt, not a benchmark score.')
    return {'model': model, 'digest': metadata.get('digest'), 'size_bytes': metadata.get('size'),
            'prompt': prompt, 'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
            'seconds_to_complete': round(elapsed, 3), 'options': OPTIONS.copy(),
            'answer': answer, 'done_reason': result.get('done_reason'),
            'truncated': result.get('done_reason') == 'length',
            'quality_score': None, 'source_verdict': None}


def run(mode, api, directory=LOCAL):
    tasks = prompts()
    names = MODELS if mode == 'benchmark' else ((CUSTOM,) if mode == 'check' else (MODELS[0],))
    metadata = installed(api, names)
    if mode == 'offline':
        tasks = [{'id': 'offline', 'prompt': 'TRAINING ONLY: Rewrite politely in one sentence: Clear the shared workbench by 4 p.m. today. Do not invent a policy.'}]
    elif mode == 'check':
        tasks = [p for p in tasks if p['id'] in ('writing', 'missing')]
    else:
        tasks = [p for p in tasks if p['id'] != 'missing']
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    target = directory/f'{mode}-{uuid.uuid4().hex}.json'
    receipt = {'route': 'live local endpoint', 'mode': mode,
               'created_at': datetime.now(timezone.utc).isoformat(),
               'network_disconnect_observed': None,
               'timing_method': 'total request seconds including load; unload after every request',
               'runs': [], 'complete': False}
    def save():
        temp = target.with_suffix('.tmp')
        temp.write_text(json.dumps(receipt, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
        temp.chmod(0o600)
        temp.replace(target)
    save()
    try:
        for name in names:
            # Normalize the first run as well: unload any already warm course model.
            request(api, 'POST', '/api/generate', json={'model': name, 'keep_alive': 0})
            for task in tasks:
                print(f"Running {name}: {task['id']} (up to 180 seconds)...", flush=True)
                row = generate(api, name, task['prompt'], metadata[name])
                row['id'] = task['id']
                receipt['runs'].append(row)
                save()
                print(f"{row['seconds_to_complete']} seconds | {row['answer']}", flush=True)
                if row['truncated']:
                    print('Output hit the limit. Mark incomplete; do not award a full quality score.')
        receipt['complete'] = True
    except (httpx.HTTPError, ValueError, KeyboardInterrupt):
        receipt['error'] = 'Run interrupted or failed. Completed earlier rows are preserved; do not mark this run complete.'
        raise
    finally:
        save()
        print(f'Saved private receipt: {target.relative_to(ROOT) if target.is_relative_to(ROOT) else target.name}')
    print('Judge each answer yourself. This receipt does not prove network disconnection or submit your worksheet.')
    return target


def create(api, directory=LOCAL):
    installed(api, [MODELS[0]])
    # Only an explicitly prepared course-owned name can be replaced.
    path = directory/'Modelfile'
    text = path.read_text(encoding='utf-8')
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith('#')]
    if not lines or lines[0] != 'FROM gemma3:1b':
        raise ValueError('Keep FROM gemma3:1b. Edit only the writing rule inside SYSTEM.')
    if sum(line.upper().startswith('FROM ') for line in lines) != 1:
        raise ValueError('Only one local base model is allowed.')
    env = os.environ.copy()
    env['OLLAMA_HOST'] = ENDPOINT
    env['OLLAMA_NO_CLOUD'] = '1'
    for key in ('HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','http_proxy','https_proxy','all_proxy'):
        env.pop(key, None)
    print('Creating/replacing only the course model zta-desk:latest.', flush=True)
    subprocess.run(['ollama', 'create', CUSTOM, '-f', str(path)], env=env, check=True, timeout=180)
    print('Run uv run --frozen zta check local-models. Named rules are not training or a security barrier.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare','doctor','start','offline','benchmark','create','check'])
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            prepare()
        elif args.command == 'start':
            print('Read courses/project-lab/level-03/student.md. Commands: prepare, doctor, offline, benchmark, create, check.')
        else:
            with client() as api:
                if args.command == 'doctor':
                    for name, entry in installed(api, MODELS).items():
                        print(f"LOCAL: {name} | {entry.get('size')} bytes | {entry.get('digest')}")
                    print('No generation made. No cloud fallback. The learner must observe all external network links being disconnected.')
                elif args.command == 'create':
                    create(api)
                else:
                    run(args.command, api)
    except (httpx.HTTPError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print('Local lab stopped. Check Ollama, installed models, and preparation. No cloud retry.', file=sys.stderr)
        if not isinstance(exc, httpx.HTTPError):
            print(str(exc), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print('Stopped. Earlier receipt rows remain private in .zta/local-models/.')
        return 130
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
