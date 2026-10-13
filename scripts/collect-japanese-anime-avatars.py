"""Collect 60 character portraits; maintenance only, no AI or runtime scraping."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageOps,ImageDraw
import requests,json,io,time,hashlib
root=Path(__file__).resolve().parent.parent
stage=root/'source-assets/japanese-anime';stage.mkdir(parents=True,exist_ok=True)
series=[(20,'火影忍者'),(21,'海贼王'),(38000,'鬼灭之刃'),(50265,'间谍过家家'),(16498,'进击的巨人'),(11061,'全职猎人'),(1535,'死亡笔记'),(5114,'钢之炼金术师'),(40748,'咒术回战'),(20583,'排球少年')]
chosen=[];seen=set()
query='query ($id:Int) { Media(idMal:$id,type:ANIME) { title { romaji } characters(perPage:25,sort:[FAVOURITES_DESC]) { nodes { id name { full } image { large } siteUrl } } } }'
for aid,title in series:
 for retry in range(4):
  r=requests.post('https://graphql.anilist.co',json={'query':query,'variables':{'id':aid}},timeout=30)
  if r.status_code==429:time.sleep(3);continue
  r.raise_for_status();break
 media=r.json()['data']['Media'];rows=media['characters']['nodes']
 accepted=[]
 for a in rows:
  c=a;url=c['image']['large']
  if c['id'] in seen or not url or 'default' in url or c['name']['full']=='Narrator':continue
  seen.add(c['id']);accepted.append((300+len(chosen)+len(accepted),aid,title,c,url))
  if len(accepted)==6:break
 assert len(accepted)==6
 chosen+=accepted;print(f'{title}: 6 selected ({len(chosen)}/60)',flush=True);time.sleep(1.1)
def download(row):
 id,aid,title,c,url=row;r=requests.get(url,timeout=30);r.raise_for_status()
 original=Image.open(io.BytesIO(r.content)).convert('RGB')
 if min(original.size)<70:raise ValueError('Portrait too small')
 # Preserve the upper face in vertical portraits, without erasing any image marks.
 im=ImageOps.fit(original,(256,256),method=Image.Resampling.LANCZOS,centering=(.5,.28))
 name=f'{id+1:03}.jpg';file=stage/name;im.save(file,quality=92,optimize=True)
 return {'id':id,'category':'日本动漫','src':'/assets/avatars/'+name,'style':'动漫角色','collection':'anime','label':c['name']['full'],'series':title,'animeId':aid,'sourceId':c['id'],'source':c['siteUrl'],'imageUrl':url,'author':'原作品权利人','license':'Original character artwork; rights reserved','sourceProvider':'AniList','sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'originalSize':list(original.size)}
with ThreadPoolExecutor(max_workers=4) as executor:records=list(executor.map(download,chosen))
records.sort(key=lambda a:a['id']);assert len(records)==60 and len({a['sha256'] for a in records})==60
(stage/'records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for offset in range(0,60,30):
 sheet=Image.new('RGB',(6*152,5*175),'white');draw=ImageDraw.Draw(sheet)
 for i,a in enumerate(records[offset:offset+30]):
  x,y=i%6*152,i//6*175;sheet.paste(Image.open(stage/f'{a["id"]+1:03}.jpg').resize((144,144)),(x+4,y+4));draw.text((x+4,y+151),str(a['id']+1),fill='#222')
 sheet.save(root/f'test-output/japanese-anime-{offset//30+1}.jpg',quality=94)
print('60 portraits staged for visual review.',flush=True)
