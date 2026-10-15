"""Register existing generated outputs with prompt and actual provider record."""
import argparse,hashlib,json,shutil,tempfile,os
from pathlib import Path
from datetime import datetime
from PIL import Image

def register(anchor,image,record,output):
    anchor=Path(anchor).resolve();image=Path(image).resolve();output=Path(output).resolve()
    if output.exists():raise ValueError('output must be a new directory')
    for field in ('prompt','provider','generated_at'):
        if not isinstance(record.get(field),str) or not record[field].strip():raise ValueError(field+' required')
    time=datetime.fromisoformat(record['generated_at'].replace('Z','+00:00'))
    if time.tzinfo is None:raise ValueError('generated_at requires timezone')
    for p in (anchor,image):
        if p.suffix.lower() not in {'.png','.jpg','.jpeg','.webp'}:raise ValueError('supported raster image required')
        with Image.open(p) as decoded:decoded.verify()
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='generation-',dir=output.parent) as temp:
        temp=Path(temp);a='anchor'+anchor.suffix.lower();v='variant'+image.suffix.lower()
        shutil.copyfile(anchor,temp/a);shutil.copyfile(image,temp/v)
        manifest={'anchor':a,'variants':[{'anchor':a,'image':v,'prompt':record['prompt'],'status':'GENERATED',
                    'provider':record['provider'],'generated_at':record['generated_at'],'model':record.get('model','UNDISCLOSED'),
                    'generation_record_origin':'SUPPLIED_DECLARATION','visual_identity_verified':False}]}
        (temp/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
        (temp/'reviews.json').write_text('{"reviews": []}\n',encoding='utf-8')
        evidence={'anchor_sha256':hashlib.sha256(anchor.read_bytes()).hexdigest(),'variant_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),
                  'provider':record['provider'],'provider_job_id':record.get('provider_job_id'),'record_verified':False}
        (temp/'generation-record.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
        # Reserve directory name without replacing existing data.
        output.mkdir()
        for p in temp.iterdir():shutil.copyfile(p,output/p.name)
    return output/'manifest.json'

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('anchor');p.add_argument('image');p.add_argument('record');p.add_argument('output');a=p.parse_args()
    try:result=register(a.anchor,a.image,json.loads(Path(a.record).read_text(encoding='utf-8-sig')),a.output)
    except (OSError,ValueError,TypeError) as e:p.exit(2,'Registration error: '+str(e)+'\n')
    print(result)
if __name__=='__main__':main()
