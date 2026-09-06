"""Versioned offline learner/instructor packets. Never package a whole checkout."""
import hashlib,json,zipfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION='v1.0.0-rc.1'

def main():
    out=ROOT/'dist';out.mkdir(exist_ok=True)
    learner=[ROOT/'LICENSE',ROOT/'release/attribution.md',ROOT/'README.md',ROOT/'README.pdf',*sorted((ROOT/'preparation').rglob('*'))]
    for p in (ROOT/'courses/project-lab').rglob('*'):
        if not p.is_file():continue
        if p.name.startswith(('instructor.','answer-key.')):continue
        if p.suffix in {'.md','.pdf','.html','.yml','.txt','.json','.template','.py'}:learner.append(p)
    teacher=learner+[p for p in (ROOT/'courses/project-lab').rglob('*') if p.is_file() and p.name.startswith(('instructor.','answer-key.'))]
    teacher += [p for p in (ROOT/'release').rglob('*') if p.is_file()]
    checks={}
    for name,files in [('learner-materials',learner),('instructor-materials',teacher)]:
        target=out/f'{name}-{VERSION}.zip'
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(set(files)):
                if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.pyc':continue
                z.write(p,p.relative_to(ROOT))
        checks[target.name]=hashlib.sha256(target.read_bytes()).hexdigest()
    for name,source in [('level-01-lesson','student.pdf'),('level-01-saved-examples','assets/fallback-grounded-run.pdf'),('level-01-slides','slides.html')]:
        target=out/f'{name}-{VERSION}{Path(source).suffix}'
        shutil.copy2(ROOT/'courses/project-lab/level-01'/source,target)
        checks[target.name]=hashlib.sha256(target.read_bytes()).hexdigest()
    (out/'SHA256SUMS.txt').write_text(''.join(f'{v}  {k}\n' for k,v in checks.items()))
    print(json.dumps(checks,indent=2))
if __name__=='__main__':main()
