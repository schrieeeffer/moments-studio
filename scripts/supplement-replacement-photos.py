from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageOps,ImageDraw
import requests,json,io,hashlib
root=Path(__file__).resolve().parent.parent
stage=root/'source-assets/avatar-replacement'
records=json.loads((stage/'photo-records.json').read_text(encoding='utf-8'))
if len(records)==152:
 print('32 supplements already collected');raise SystemExit
old=json.loads((root/'public/assets/photo-avatars.json').read_text(encoding='utf-8'))
seen={a['sourceId'] for a in records+old}
queries=[('萌宠摄影','bird animal portrait'),('萌宠摄影','golden retriever portrait'),('自然风景','ocean waves sunset'),('自然风景','lake reflection mountain'),('花草治愈','orchid flower closeup'),('花草治愈','cherry blossom branch'),('生活静物','strawberry cake table'),('城市街景','hong kong street night')]
chosen=[]
for cat,q in queries:
 accepted=[]
 for page in (1,2,3):
  r=requests.get('https://unsplash.com/napi/search/photos',params={'query':q,'per_page':30,'page':page},timeout=25);r.raise_for_status()
  for a in r.json()['results']:
   if a['id'] in seen or a.get('premium') or a.get('plus') or a.get('sponsorship'):continue
   seen.add(a['id']);accepted.append(a)
   if len(accepted)==4:break
  if len(accepted)==4:break
 assert len(accepted)==4
 start=48+len(chosen);chosen.extend((start+i,cat,a) for i,a in enumerate(accepted))
 print(f'Curated {q}',flush=True)
def download(row):
 id,cat,a=row;url=a['urls']['raw'].split('?')[0]+'?auto=format&fit=crop&w=512&h=512&q=88'
 r=requests.get(url,timeout=35);r.raise_for_status()
 im=ImageOps.fit(Image.open(io.BytesIO(r.content)).convert('RGB'),(256,256),method=Image.Resampling.LANCZOS)
 name=f'{id+1:03}.jpg';file=stage/'photos'/name;im.save(file,quality=90,optimize=True)
 return {'id':id,'category':cat,'src':'/assets/avatars/'+name,'style':'真实摄影','collection':'replacement','label':a.get('alt_description') or cat,'source':a['links']['html'].split('?')[0],'sourceId':a['id'],'author':a['user']['name'],'authorUrl':a['user']['links']['html'],'license':'Unsplash License','licenseUrl':'https://unsplash.com/license','imageUrl':url,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
with ThreadPoolExecutor(max_workers=6) as executor:records+=list(executor.map(download,chosen))
records.sort(key=lambda a:a['id']);assert len(records)==152
(stage/'photo-records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
sheet=Image.new('RGB',(8*144,4*164),'white');draw=ImageDraw.Draw(sheet)
for i,a in enumerate(records[:32]):
 x,y=i%8*144,i//8*164;sheet.paste(Image.open(stage/'photos'/f'{a["id"]+1:03}.jpg').resize((136,136)),(x+4,y+4));draw.text((x+4,y+143),str(a['id']+1),fill='#222')
sheet.save(root/'test-output/replacement-supplements.jpg',quality=94)
print('Collected 32 additional licensed photos; no AI requests.',flush=True)
