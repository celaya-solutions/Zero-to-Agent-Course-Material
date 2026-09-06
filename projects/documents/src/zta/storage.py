"""Local configuration and atomic evidence saves. No network or Git writes."""
import json
import os
import re
import tempfile
import tomllib
from datetime import datetime, timezone
from pathlib import Path

MODELS = {"ollama": "gemma3:4b", "claude": "claude-haiku-4-5-20251001", "openai": "gpt-4.1-mini-2025-04-14"}

def root():
    if os.environ.get("ZTA_ROOT"):
        return Path(os.environ["ZTA_ROOT"]).resolve()
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "courses/project-lab").is_dir():
            return parent
    raise RuntimeError("Open a terminal in the course clone and run uv sync --frozen.")

def data_dir():
    path = Path(os.environ.get("ZTA_DATA_DIR", str(root() / ".zta")))
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path

def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ValueError(f"{path.name} is unreadable. Keep a backup and ask the instructor to recover it.") from exc

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".save-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def config():
    result = read_json(data_dir() / "config.json", {})
    provider = result.get("provider", "ollama")
    if provider not in MODELS:
        raise ValueError("Unknown provider. Run uv run --frozen zta setup.")
    result.setdefault("provider", provider)
    result.setdefault("model", MODELS[provider])
    keyname = {"claude": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY"}.get(provider)
    if keyname and os.environ.get(keyname):
        result["api_key"] = os.environ[keyname]
    return result

def settings():
    with (root() / "projects/documents/settings.toml").open("rb") as stream:
        result = tomllib.load(stream)
    if type(result.get("max_passages")) is not int or not 1 <= result["max_passages"] <= 8:
        raise ValueError("max_passages must be a whole number from 1 to 8. Restore 4 for class.")
    if type(result.get("show_source_quotes")) is not bool:
        raise ValueError("show_source_quotes must be true or false.")
    return result

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def progress():
    return read_json(data_dir() / "progress.json", {"fields": {}, "runs": [], "opened": [], "classifications": {}, "revision": {}})

def save_progress(value):
    write_json(data_dir() / "progress.json", value)

def redact(text, key=""):
    if key:
        text = text.replace(key, "[REDACTED]")
    return re.sub(r"\bsk-[A-Za-z0-9_-]{12,}", "[REDACTED]", text)
