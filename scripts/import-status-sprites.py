from pathlib import Path
from PIL import Image
import json, shutil

root=Path(__file__).resolve().parent.parent
src=root/'source-assets/statusbar-generated'
dest=root/'public/assets/status-bars-v2'
dest.mkdir(parents=True,exist_ok=True)
rows=json.loads((src/'prompts.json').read_text(encoding='utf-8'))
manifest=[]
for row in rows:
    original=src/(row['id']+'-original.png')
    shutil.copy2(row['generatedPath'],original)
    img=Image.open(original).convert('RGBA')
    alpha=img.getchannel('A'); assert alpha.getextrema()==(0,255), 'Expected real transparency'
    bbox=alpha.point(lambda v:255 if v>32 else 0).getbbox(); img=img.crop(bbox)
    # Trim only transparent storage padding; retain AI pixels and their alpha.
    target=img.resize((round(img.width/img.height*96),96),Image.Resampling.LANCZOS)
    target.save(dest/(row['id']+'.png'),optimize=True)
    occupied=[any(v>32 for v in img.getchannel('A').crop((x,0,x+1,img.height)).getdata()) for x in range(img.width)]
    runs=[];start=None
    for x,v in enumerate(occupied+[False]):
        if v and start is None:start=x
        if not v and start is not None:runs.append([start,x]);start=None
    print(json.dumps({'id':row['id'],'bbox':bbox,'cropSize':img.size,'xRuns':runs}))
    # Extract a single-SIM variant from the same intact glyph groups.
    if row['id']=='xiaomi':
        crop=img.crop((round(img.width*.35),0,img.width,img.height))
        crop=crop.crop(crop.getchannel('A').point(lambda v:255 if v>32 else 0).getbbox())
        crop.resize((round(crop.width/crop.height*96),96),Image.Resampling.LANCZOS).save(dest/'xiaomi-single.png',optimize=True)
    if row['id']=='huawei':
        crop=img.crop((0,0,round(img.width*.67),img.height))
        crop=crop.crop(crop.getchannel('A').point(lambda v:255 if v>32 else 0).getbbox())
        crop.resize((round(crop.width/crop.height*96),96),Image.Resampling.LANCZOS).save(dest/'huawei-single.png',optimize=True)
    manifest.append({'id':row['id'],'source':'one-time AI generation, screenshot reference only','reference':row['ref'],'image':f'/assets/status-bars-v2/{row["id"]}.png','size':target.size})
(dest/'sprite-sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
