"""The four beginner commands used in the preparation guide."""
import argparse
import getpass
import json
import os
import socket
import sqlite3
import subprocess
import sys
from pathlib import Path
import httpx
from . import __version__
from .documents import CLASS_FILES, extract
from .storage import MODELS, config, data_dir, root, settings, write_json

def setup():
    print("Choose ONE answer engine. Coding-assistant access is separate.")
    print("1 Ollama (local)\n2 Claude API (selected passages leave this computer)\n3 OpenAI API (selected passages leave this computer)")
    print("Starting cloud rates per million input/output tokens: Claude Haiku $1/$5; OpenAI GPT-4.1 mini $0.40/$1.60 (checked 2026-09-06).")
    print("Check current prices and any required account funding at the provider checkout. Read preparation/models.md before choosing a paid route.")
    choices = {"1": "ollama", "2": "claude", "3": "openai"}
    selected = input("Route [1]: ").strip() or "1"
    if selected not in choices:
        raise ValueError("Enter 1, 2, or 3. No configuration changed.")
    provider = choices[selected]
    value = {"provider": provider, "model": MODELS[provider]}
    if provider != "ollama":
        print("Read preparation/models.md for pricing, billing, and privacy. API charges are separate from a chat subscription.")
        key = getpass.getpass("Paste your course API key (hidden; never paste it into a command or chat): ").strip()
        if not key:
            raise ValueError("No key entered. No configuration changed.")
        value["api_key"] = key
    write_json(data_dir()/"config.json", value)
    print(f"Saved {provider} / {value['model']}. Key stored only in ignored .zta/config.json.")
    if provider == "ollama":
        print("Open Ollama, then run: ollama pull gemma3:4b")
    print("Next: uv run --frozen zta doctor documents")

def doctor():
    cfg = config()
    settings()
    print(f"Zero to Agent {__version__} | Python {sys.version.split()[0]}")
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE VIRTUAL TABLE test USING fts5(text)")
    print("PASS: SQLite full-text search")
    assets = root()/"courses/project-lab/level-01/assets"
    for name in CLASS_FILES:
        extract(name, (assets/name).read_bytes())
    print("PASS: all four class documents extract")
    with socket.socket() as listener:
        try:
            listener.bind(("127.0.0.1",8501))
            print("PASS: local app port 8501 is free")
        except OSError:
            print("NOTE: port 8501 is occupied. If it is this app, use the existing browser tab; otherwise stop it before starting.")
    with httpx.Client(timeout=15, trust_env=False) as client:
        if cfg["provider"] == "ollama":
            response = client.get("http://127.0.0.1:11434/api/tags")
            response.raise_for_status()
            names = {m["name"] for m in response.json().get("models",[])}
            if cfg["model"] not in names:
                raise ValueError(f"Model missing. Run ollama pull {cfg['model']}.")
        else:
            key = cfg.get("api_key")
            if not key:
                raise ValueError("API key missing. Run zta setup.")
            url, headers = ("https://api.anthropic.com/v1/models", {"x-api-key":key,"anthropic-version":"2023-06-01"}) if cfg["provider"] == "claude" else ("https://api.openai.com/v1/models", {"Authorization":f"Bearer {key}"})
            response = client.get(url, headers=headers)
            if response.status_code != 200:
                raise ValueError(f"Provider access check failed (HTTP {response.status_code}). Recheck key and account access. Key not printed.")
            if cfg["model"] not in {m.get("id") for m in response.json().get("data",[])}:
                print("NOTE: selected model was not in this model-list page. The practice question must confirm access.")
    print(f"PASS: provider reachable ({cfg['provider']} / {cfg['model']}).")
    print("No paid generation was made. Complete the practice question in the app to confirm generation and billing access.")

def main():
    parser = argparse.ArgumentParser(prog="zta")
    parser.add_argument("command", choices=["setup","doctor","start","test","prepare","offline","benchmark","create","check","callers","attacks","lock","pause","resume"])
    parser.add_argument("project", nargs="?", choices=["documents","watchman","local-models","front-desk"])
    args = parser.parse_args()
    try:
        if args.project == "front-desk":
            project = root()/"projects/front-desk"
            if args.command == "test":
                command = [sys.executable,"-m","pytest",str(project/"tests"),"-q"]
            elif args.command == "start":
                command = [sys.executable,"-m","streamlit","run",str(project/"app.py"),"--server.address=127.0.0.1","--server.port=8504","--server.headless=true","--client.toolbarMode=minimal","--browser.gatherUsageStats=false"]
            elif args.command in {"prepare","doctor","callers","attacks","lock","pause","resume"}:
                command = [sys.executable,str(project/"desk.py"),args.command]
            else:
                raise ValueError("Read Level 4 preparation, then use zta prepare front-desk.")
            return subprocess.call(command, cwd=root())
        if args.command in {"callers","attacks","lock","pause","resume"}:
            raise ValueError("This command requires the front-desk project.")
        if args.project == "local-models":
            project = root()/"projects/local-models"
            if args.command == "test":
                command = [sys.executable,"-m","pytest",str(project/"tests"),"-q"]
            elif args.command == "setup":
                raise ValueError("Read Level 3 preparation, then use zta prepare local-models.")
            else:
                command = [sys.executable,str(project/"lab.py"),args.command]
            return subprocess.call(command, cwd=root())
        if args.command in {"offline","benchmark","create","check"}:
            raise ValueError("This command requires the local-models project.")
        if args.project == "watchman":
            project = root()/"projects/watchman"
            if args.command == "test":
                command = [sys.executable,"-m","pytest",str(project/"tests"),"-q"]
            elif args.command == "start":
                command = [sys.executable,str(project/"watch.py")]
            elif args.command in {"prepare","doctor"}:
                command = [sys.executable,str(project/"manage.py"),args.command]
            else:
                print("Watchman needs no model setup. Start with zta doctor watchman.")
                return 0
            return subprocess.call(command, cwd=root())
        elif args.command == "prepare":
            raise ValueError("Use zta prepare watchman for Level 2; follow the preparation guide for documents.")
        elif args.command == "setup":
            setup()
        elif args.command == "doctor":
            doctor()
        elif args.command == "test":
            return subprocess.call([sys.executable,"-m","pytest",str(root()/"projects/zta/tests"),"-q"], cwd=root())
        else:
            print("Open http://127.0.0.1:8501. Keep this terminal open. Stop with Ctrl+C.", flush=True)
            env = os.environ.copy()
            env["GRADIO_ANALYTICS_ENABLED"] = "False"
            return subprocess.call([sys.executable,str(Path(__file__).with_name("app.py"))],env=env,cwd=root())
    except KeyboardInterrupt:
        print("Stopped. Your evidence remains in .zta/.")
        return 130
    except (ValueError, OSError, sqlite3.Error, httpx.HTTPError) as exc:
        if isinstance(exc, httpx.HTTPError):
            print("Provider is unavailable. Open Ollama or check the cloud connection, then rerun doctor.", file=sys.stderr)
        else:
            print(str(exc), file=sys.stderr)
        return 1
    return 0
