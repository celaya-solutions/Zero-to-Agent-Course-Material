"""Export the canonical course into an isolated WEBSITE checkout, never a live service."""
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('destination',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    dest=args.destination.resolve()
    if not (dest/'course/landing.html').is_file():parser.error('Destination must be a website checkout containing course/landing.html')
    if dest==ROOT:parser.error('Destination must differ from the canonical repository')
    paths=[*sorted((ROOT/'courses/project-lab').rglob('*')),*sorted((ROOT/'preparation').rglob('*'))]
    paths += [ROOT/'scripts'/name for name in ['build_project_lab_slides.rb','build_project_lab_pdfs.rb','build_pdfs.py','validate_project_lab.rb']]
    files=[p for p in paths if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
    manifest={'repository':'https://github.com/celaya-solutions/Zero-to-Agent-Course-Material','source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    if args.check:
        bad=[name for name,digest in manifest['files'].items() if not (dest/name).is_file() or hashlib.sha256((dest/name).read_bytes()).hexdigest()!=digest]
        if bad:raise SystemExit('Generated course mismatch: '+', '.join(bad))
        print(f'Generated website copy matches {len(files)} files.');return
    for p in files:
        target=dest/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    (dest/'course-material-source.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Exported {len(files)} source/generated files. Review and commit the destination worktree; no deployment performed.')
if __name__=='__main__':main()
