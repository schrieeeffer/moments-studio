"""Collect free Unsplash photography as local 256 px avatar assets.

This is a build-time tool, not a browser or server dependency. Downloads only
non-Plus images; stores the original source/author/license for each avatar.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageOps
import requests, json, io, hashlib, time

root=Path(__file__).resolve().parent.parent
out=root/'public/assets/avatars'
record_path=root/'public/assets/photo-avatars.json'
session=requests.Session()
session.headers.update({'User-Agent':'MomentsStudio/1.0 avatar asset curation'})
queries=[
 ('萌宠摄影','cat face',10),('萌宠摄影','dog puppy portrait',10),
 ('自然风景','mountain lake landscape',10),('自然风景','ocean sunset clouds',10),
 ('花草治愈','flower bouquet closeup',10),('花草治愈','green plants leaves',10),
 ('生活静物','coffee cup still life',10),('城市街景','city street night japan',10)
]

def candidates(q):
 r=session.get('https://unsplash.com/napi/search/photos',params={'query':q,'per_page':30,'page':1},timeout=25)
 r.raise_for_status()
 return [a for a in r.json()['results'] if not a.get('premium') and not a.get('plus') and not a.get('sponsorship')]

def download(item):
 id,category,a=item
 url=a['urls']['raw'].split('?')[0]+'?auto=format&fit=crop&w=384&h=384&q=85'
 response=requests.get(url,timeout=35);response.raise_for_status()
 image=ImageOps.fit(Image.open(io.BytesIO(response.content)).convert('RGB'),(256,256),method=Image.Resampling.LANCZOS)
 filename=f'{id+1:03}.jpg'
 image.save(out/filename,quality=88,optimize=True)
 return {'id':id,'category':category,'src':'/assets/avatars/'+filename,'style':'摄影素材','collection':'expanded',
   'label':a.get('alt_description') or a.get('description') or category,
   'source':a['links']['html'].split('?')[0],'sourceId':a['id'],
   'author':a['user']['name'],'authorUrl':a['user']['links']['html'],
   'license':'Unsplash License','licenseUrl':'https://unsplash.com/license',
   'imageUrl':url,'sha256':hashlib.sha256((out/filename).read_bytes()).hexdigest()}

if __name__=='__main__':
 chosen=[];seen=set()
 for category,q,n in queries:
  count=0
  for a in candidates(q):
   if a['id'] in seen:continue
   chosen.append((200+len(chosen),category,a));seen.add(a['id']);count+=1
   if count==n:break
  if count!=n:raise RuntimeError(f'Insufficient free results for {q}: {count}/{n}')
  print(f'Curated {category}: {q} ({n})',flush=True)
 records=[]
 with ThreadPoolExecutor(max_workers=6) as executor:
  for result in as_completed([executor.submit(download,a) for a in chosen]):
   records.append(result.result())
   if len(records)%10==0:print(f'Downloaded {len(records)}/{len(chosen)}',flush=True)
 records.sort(key=lambda a:a['id'])
 assert len(records)==80 and len({a['sha256'] for a in records})==80
 record_path.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
 sheet=Image.new('RGB',(10*112,8*112),'white')
 from PIL import ImageDraw
 draw=ImageDraw.Draw(sheet)
 for i,a in enumerate(records):
  x,y=i%10*112,i//10*112
  sheet.paste(Image.open(root/'public'/a['src'].lstrip('/')).resize((104,88)),(x+4,y+4))
  draw.text((x+4,y+94),str(a['id']+1),fill='#222')
 (root/'test-output').mkdir(exist_ok=True)
 sheet.save(root/'test-output/photo-contact-sheet.jpg',quality=92)
 print('Saved 80 photography avatars and their source records.',flush=True)
