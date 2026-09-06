"""Text extraction and inspectable SQLite FTS5 keyword retrieval."""
import hashlib
import io
import json
import re
import sqlite3
from pathlib import Path
from pypdf import PdfReader

CLASS_FILES = ["public-identity-and-work.md", "public-contact-and-method.md", "training-record-a.md", "training-record-b.md"]
STOP = set("a an the is are was were what which where who how why do does did of to for in on at by and or with should i we you it its this that from be used use kind give me tell about celaya solutions research".split())

def extract(name, data):
    if len(data) > 10 * 1024 * 1024:
        raise ValueError(f"{name}: exceeds the 10 MB limit.")
    suffix = Path(name).suffix.lower()
    if suffix not in {".md", ".txt", ".pdf"}:
        raise ValueError(f"{name}: use Markdown, UTF-8 text, or a text-based PDF.")
    sections = []
    if suffix == ".pdf":
        try:
            pdf = PdfReader(io.BytesIO(data))
            if pdf.is_encrypted:
                raise ValueError("password-protected PDF")
            if len(pdf.pages) > 100:
                raise ValueError("PDF exceeds 100 pages")
            for number, page in enumerate(pdf.pages, 1):
                text = (page.extract_text() or "").strip()
                if not text:
                    raise ValueError(f"page {number} has no readable text; use the supplied text alternative")
                sections.append((f"Page {number}", number, text))
        except Exception as exc:
            raise ValueError(f"{name}: cannot read this PDF ({str(exc)[:140]}).") from exc
    else:
        try:
            text = data.decode("utf-8-sig")
        except UnicodeError as exc:
            raise ValueError(f"{name}: save a UTF-8 text copy.") from exc
        # Document metadata is not evidence. The canonical body follows this header.
        text = re.sub(r"```(?:text)?\s*\nDocument:.*?```\s*", "", text, count=1, flags=re.S)
        heading = "Document text"
        lines = []
        for line in text.splitlines():
            if re.match(r"^#{1,6} ", line):
                if "\n".join(lines).strip():
                    sections.append((heading, None, "\n".join(lines).strip()))
                heading = line.lstrip("# ").strip()
                lines = []
            else:
                lines.append(line)
        if "\n".join(lines).strip():
            sections.append((heading, None, "\n".join(lines).strip()))
    if sum(len(s[2]) for s in sections) > 250_000:
        raise ValueError(f"{name}: exceeds 250,000 extracted characters; use a smaller document.")
    full = "\n".join(s[2] for s in sections)
    source_class = "training-only" if "not a real Celaya Solutions Research policy" in full else "unclassified"
    if name.startswith("public-") and "PUBLIC SOURCE" in full:
        source_class = "public"
    passages = []
    for heading, page, text in sections:
        for offset in range(0, len(text), 1200):
            body = text[offset:offset+1200]
            digest = hashlib.sha256(f"{name}|{heading}|{page}|{offset}|{body}".encode()).hexdigest()[:12]
            passages.append({"id": digest, "source": name, "heading": heading, "page": page, "text": body, "class": source_class})
    if not passages:
        raise ValueError(f"{name}: no readable text; use the supplied text copy.")
    return passages

def build_index(path, files):
    passages = []
    if not files or len(files) > 20:
        raise ValueError("Load between 1 and 20 documents before building the index.")
    names = set()
    for name, data in files:
        if name in names or name != Path(name).name or "/" in name or "\\" in name:
            raise ValueError("Use distinct filenames without folder paths.")
        names.add(name)
        passages.extend(extract(name, data))
    if sum(len(p["text"]) for p in passages) > 500_000:
        raise ValueError("Binder exceeds 500,000 characters. Use a smaller binder.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as db:
        db.execute("BEGIN")
        db.execute("DROP TABLE IF EXISTS chunks")
        db.execute("DROP TABLE IF EXISTS passages")
        db.execute("CREATE VIRTUAL TABLE chunks USING fts5(source, heading, body, tokenize='porter unicode61')")
        db.execute("CREATE TABLE passages (rowid INTEGER PRIMARY KEY, data TEXT NOT NULL)")
        for p in passages:
            cursor = db.execute("INSERT INTO chunks VALUES (?,?,?)", (p["source"], p["heading"], p["text"]))
            db.execute("INSERT INTO passages VALUES (?,?)", (cursor.lastrowid, json.dumps(p)))
    return passages

def retrieve(path, question, count=4):
    if not path.exists():
        raise ValueError("Build the document index before asking a question.")
    tokens = list(dict.fromkeys(t for t in re.findall(r"[a-z0-9]+", question.lower()) if t not in STOP))[:40]
    if not tokens:
        return []
    match = " OR ".join('"'+t+'"' for t in tokens)
    with sqlite3.connect(path) as db:
        rows = db.execute("SELECT p.data FROM chunks c JOIN passages p ON p.rowid=c.rowid WHERE chunks MATCH ? ORDER BY bm25(chunks,0.1,2.0,1.0), c.rowid LIMIT ?", (match, count)).fetchall()
    return [json.loads(row[0]) for row in rows]

def inventory(path):
    if not path.exists():
        return []
    with sqlite3.connect(path) as db:
        return [json.loads(row[0]) for row in db.execute("SELECT data FROM passages ORDER BY rowid")]
