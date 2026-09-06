"""Refresh standard document hashes without rewriting teaching content."""
import hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
pattern=re.compile(r"(?P<head>```(?:text)?\nDocument:.*?\n```)(?P<body>.*)",re.S)
for path in ROOT.rglob("*.md"):
    if any(part.startswith('.') or part in {'graft','dist'} for part in path.relative_to(ROOT).parts):continue
    text=path.read_text();match=pattern.search(text)
    if not match:continue
    digest=hashlib.sha256((match['body'].strip()+"\n").encode()).hexdigest()
    header=re.sub(r"SHA256:.*", "SHA256:      "+digest,match['head'])
    path.write_text(text[:match.start()]+header+match['body'])
print("Updated canonical document body hashes.")
