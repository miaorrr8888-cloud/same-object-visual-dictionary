"""Build a local gallery from an explicit manifest; this never generates images."""
import argparse
import html
import json
from pathlib import Path
import shutil
from PIL import Image, UnidentifiedImageError


def build(manifest, output):
    manifest=Path(manifest).resolve(); root=manifest.parent
    data=json.loads(manifest.read_text(encoding='utf-8'))
    if not isinstance(data,dict) or not isinstance(data.get('anchor'),str) or not isinstance(data.get('variants'),list):
        raise ValueError('manifest requires anchor text and variants array')
    anchor=data['anchor']; cards=data['variants']
    if not cards: raise ValueError('at least one variant is required')
    prepared=[]
    for card in cards:
        if not isinstance(card,dict) or not isinstance(card.get('image'),str) or not isinstance(card.get('prompt'),str):
            raise ValueError('variant requires image and prompt text')
        if card.get('anchor')!=anchor:
            raise ValueError('every variant must identify the same anchor')
        if card.get('status') not in {'GENERATED','REFERENCE','UNKNOWN'}:
            raise ValueError('explicit provenance status required')
    for entry in [{'image':anchor,'prompt':'Anchor','status':'REFERENCE'},*cards]:
        image=(root/entry['image']).resolve()
        if not image.is_relative_to(root) or image.suffix.lower() not in {'.png','.jpg','.jpeg','.webp'} or not image.is_file():
            raise ValueError('images must be existing raster files within the manifest directory')
        try:
            with Image.open(image) as decoded: decoded.verify()
        except (OSError,UnidentifiedImageError,ValueError):
            raise ValueError('image cannot be decoded: '+image.name)
        prepared.append((entry,image))
    out=Path(output).resolve()
    if out.exists(): raise ValueError('output must be a new directory')
    (out/'images').mkdir(parents=True)
    body=[]
    for index,(entry,image) in enumerate(prepared):
        name=f'{index:03d}{image.suffix.lower()}'
        shutil.copyfile(image,out/'images'/name)
        body.append(f'<article><img src="images/{name}" alt="{html.escape(entry["prompt"],quote=True)}"><p>{html.escape(entry["status"])}</p><pre>{html.escape(entry["prompt"])}</pre><button onclick="navigator.clipboard.writeText(this.previousElementSibling.textContent)">Copy prompt</button></article>')
    page='<!doctype html><meta charset="utf-8"><title>Prompt comparison</title><style>body{font:16px system-ui;margin:32px;background:#fafafa}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}img{width:100%;height:280px;object-fit:contain}pre{white-space:pre-wrap}article{background:white;padding:16px}</style><h1>Prompt comparison</h1><p>Same declared anchor. Visual consistency and generation settings require human review.</p><main>'+''.join(body)+'</main>'
    (out/'index.html').write_text(page,encoding='utf-8')
    return out/'index.html'


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('manifest'); p.add_argument('output')
    a=p.parse_args()
    try: print(build(a.manifest,a.output))
    except (ValueError,KeyError,OSError,json.JSONDecodeError) as exc: p.exit(2,'Input error: '+str(exc)+'\n')
