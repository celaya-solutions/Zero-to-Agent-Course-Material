"""Opt-in real-provider acceptance. No API request unless --live is supplied."""
import argparse,json,platform,tempfile
from pathlib import Path
from zta.documents import CLASS_FILES,build_index,retrieve
from zta.evidence import QUESTIONS
from zta.providers import request_answer
from zta.storage import config,root,now

def main():
    p=argparse.ArgumentParser();p.add_argument('--live',action='store_true',required=True);args=p.parse_args()
    cfg=config();r=root();assets=r/'courses/project-lab/level-01/assets';runs=[]
    print('Selected engine:',cfg['provider'],cfg['model'],'Five requests; cloud may incur charges. Only bundled public/synthetic data is sent.')
    with tempfile.TemporaryDirectory() as t:
        index=Path(t)/'index.sqlite3';build_index(index,[(n,(assets/n).read_bytes()) for n in CLASS_FILES])
        for i,q in enumerate(QUESTIONS,1):
            passages=retrieve(index,q,4);answer=request_answer(cfg,q,passages)
            runs.append({'number':i,'question':q,'at':now(),'result':answer,'passages':passages})
            print(i,answer['status'],answer['answer'])
    dest=r/'.zta'/f'live-pilot-{cfg["provider"]}.json';dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps({'recorded_at':now(),'os':platform.platform(),'provider':cfg['provider'],'model':cfg['model'],'runs':runs},indent=2))
    print('Saved locally:',dest.name,'Review semantic results before copying a sanitized record into release/evidence.')
if __name__=='__main__':main()
