"""Validate course shape, local links, headers, generated files, and package boundaries."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
import yaml
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
COURSE=ROOT/'courses/project-lab'

def main():
    errors=[]
    course=yaml.safe_load((COURSE/'course.yml').read_text(encoding="utf-8"))
    if course['level_count']!=5 or course['duration_minutes_per_level']!=90:errors.append('Expected five 90-minute levels')
    for n in range(1,6):
        folder=COURSE/f'level-{n:02d}'
        m=yaml.safe_load((folder/'level.yml').read_text(encoding="utf-8"))
        for name in ['student','instructor','worksheet']:
            text=(folder/f'{name}.md').read_text(encoding="utf-8")
            if m['title'] not in text or m['passing_proof'] not in text:errors.append(f'{folder.name}/{name}: manifest mismatch')
            pdf=folder/f'{name}.pdf'
            if not pdf.exists():errors.append(f'Missing {pdf.relative_to(ROOT)}')
            elif not PdfReader(pdf).pages:errors.append(f'Empty PDF {pdf.name}')
        slides=(folder/'slides.html').read_text(encoding="utf-8")
        if len(re.findall(r'<section\b[^>]*class="slide',slides))!=20:errors.append(f'{folder.name}: needs 20 slides')
        text=(folder/'instructor.md').read_text(encoding="utf-8")
        section=text.split('## 90-minute schedule',1)[1].split('\n## ',1)[0]
        total=sum(int(x) for x in re.findall(r'^\| (?!\*\*Total).*? \| (\d+) \|$',section,re.M))
        if total!=90:errors.append(f'{folder.name}: schedule totals {total}')
    authored=[ROOT/'README.md',*sorted((ROOT/'preparation').glob('*.md')),*sorted((COURSE/'level-01').glob('*.md')),*sorted((COURSE/'level-02').rglob('*.md')),ROOT/'projects/watchman/README.md',ROOT/'release/level-02-verification.md']
    for path in authored:
        text=path.read_text(encoding="utf-8")
        for key in ['Document:','Version:','Author:','Contact:','Date:','SHA256:','Chain:','Tx:','License:']:
            if key not in text:errors.append(f'{path.name}: missing {key}')
        if '[pending]' in text:errors.append(f'{path.name}: unfinished hash')
        match=re.search(r'```(?:text)?\nDocument:.*?SHA256: +([0-9a-f]{64}).*?\n```(.*)',text,re.S)
        if not match or match[1]!=hashlib.sha256((match[2].strip()+'\n').encode()).hexdigest():errors.append(f'{path.name}: header hash mismatch')
    for path in [ROOT/'README.md',*sorted((ROOT/'preparation').glob('*.md')),*sorted(COURSE.rglob('*.md'))]:
        for link in re.findall(r'\]\(([^)\s]+)',path.read_text(encoding="utf-8")):
            if ':' in link or link.startswith('#'):continue
            target=(path.parent/link.split('#')[0]).resolve()
            if not target.exists():errors.append(f'{path.relative_to(ROOT)}: broken link {link}')
    saved=json.loads((COURSE/'level-01/assets/saved-runs.json').read_text(encoding="utf-8"))
    if len(saved)!=5 or any(r['route']!='saved classroom example' for r in saved):errors.append('Saved route must have five labeled examples')
    # Tracked-state only. Never inspect private .zta contents.
    tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
    for p in tracked:
        if p.startswith(('.zta/','.env','platform/')) or Path(p).name in {'PROJECT-LAB-01.md','PROJECT-LAB-02.md'}:errors.append(f'Private/generated learner data tracked: {p}')
    template=ROOT/'projects/watchman/workflow.template.yml'
    if template.read_bytes()!=(COURSE/'level-02/assets/starter/watch.yml').read_bytes():errors.append('Legacy workflow copy is stale; run scripts/sync_watchman_starter.py')
    if errors:
        print('\n'.join('ERROR: '+e for e in errors));return 1
    print('Course materials valid: five levels, 90 minutes each, links, PDFs, slides, and private-data boundary.');return 0
if __name__=='__main__':raise SystemExit(main())
