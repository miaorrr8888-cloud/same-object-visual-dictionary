"""Record human same-object/quality review with hashes; no automatic identity claim."""
import argparse,hashlib,json
from pathlib import Path

def review(manifest,decisions):
    path=Path(manifest).resolve();data=json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(decisions,dict) or not isinstance(decisions.get('reviews'),list):raise ValueError('reviews array required')
    by_image={}
    for r in decisions['reviews']:
        if r.get('image') in by_image:raise ValueError('duplicate review image')
        by_image[r.get('image')]=r
    rows=[]
    for variant in data['variants']:
        name=variant['image'];raw=path.parent/name;image=raw.resolve()
        if raw.is_symlink() or not image.is_relative_to(path.parent) or not image.is_file():raise ValueError('image outside manifest directory')
        r=by_image.get(name,{})
        if r.get('decision') not in {None,'accept','reject','needs_review'}:raise ValueError('invalid decision')
        accepted=r.get('decision')=='accept'
        if accepted and not (r.get('same_object') is True and r.get('text_checked') is True and isinstance(r.get('reviewer'),str) and r['reviewer'].strip()):raise ValueError('accept requires reviewer, same_object and text_checked')
        rows.append({'image':name,'sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'decision':r.get('decision','needs_review'),
                     'reviewer':r.get('reviewer'),'notes':r.get('notes'),'identity_origin':'HUMAN_DECLARATION','auto_verified':False})
    extra=set(by_image)-{v['image'] for v in data['variants']}
    if extra:raise ValueError('review refers to unknown image')
    return {'variants':rows,'accepted':sum(r['decision']=='accept' for r in rows)}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest');p.add_argument('reviews');a=p.parse_args()
    try:r=review(a.manifest,json.load(open(a.reviews,encoding='utf-8-sig')))
    except (ValueError,OSError,KeyError,TypeError) as e:p.exit(2,'Review error: '+str(e)+'\n')
    print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
