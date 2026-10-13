from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import shutil,json,hashlib
root=Path(__file__).resolve().parent.parent
stage=root/'source-assets/avatar-replacement';originals=stage/'generated';out=stage/'generated-jpg'
originals.mkdir(exist_ok=True);out.mkdir(exist_ok=True)
rows=[]
for file in sorted(stage.glob('completed-*.json')):rows.extend(json.loads(file.read_text(encoding='utf-8')))
records=[]
for row in rows:
    if row.get('error'):continue
    id=row['id'];name=f'{id+1:03}'
    original=originals/(name+'.png')
    if not original.exists():shutil.copy2(row['path'],original)
    dest=out/(name+'.jpg')
    if not dest.exists():
        img=ImageOps.fit(Image.open(original).convert('RGB'),(256,256),method=Image.Resampling.LANCZOS)
        img.save(dest,quality=91,optimize=True)
    records.append({'id':id,'category':row['category'],'src':f'/assets/avatars/{name}.jpg','style':row['style'],
      'collection':'replacement','generated':True,'source':'AI original · built-in image_gen','author':'圈图素材库',
      'license':'AI-generated original asset','promptId':id,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
records.sort(key=lambda a:a['id']);assert len({a['id'] for a in records})==len(records)
(stage/'ai-records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for offset in range(0,len(records),20):
    group=records[offset:offset+20]
    sheet=Image.new('RGB',(5*168,4*188),'white');draw=ImageDraw.Draw(sheet)
    for i,a in enumerate(group):
        x,y=i%5*168,i//5*188;sheet.paste(Image.open(out/f'{a["id"]+1:03}.jpg').resize((160,160)),(x+4,y+4));draw.text((x+4,y+167),f'#{a["id"]+1}',fill='#222')
    sheet.save(root/f'test-output/replacement-ai-{offset//20+1}.jpg',quality=94)
print(json.dumps({'staged':len(records),'errors':[r['id'] for r in rows if r.get('error')]}))
