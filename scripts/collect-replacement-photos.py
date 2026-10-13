"""Curate fresh free photography; stage assets until the full replacement is ready."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from PIL import Image,ImageOps,ImageDraw
import requests,json,io,hashlib,time

root=Path(__file__).resolve().parent.parent
stage=root/'source-assets/avatar-replacement'
out=stage/'photos';out.mkdir(parents=True,exist_ok=True)
old=json.loads((root/'public/assets/photo-avatars.json').read_text(encoding='utf-8'))
seen={a['sourceId'] for a in old}
queries=[
 ('萌宠摄影','cat sleeping window'),('萌宠摄影','shiba inu dog'),('萌宠摄影','puppy portrait'),('萌宠摄影','rabbit animal portrait'),
 ('自然风景','mist forest path'),('自然风景','rocky coast sea'),('自然风景','snow mountain sunrise'),('自然风景','aurora winter landscape'),
 ('花草治愈','tulip flowers'),('花草治愈','hydrangea flowers'),('花草治愈','succulent plant'),('花草治愈','autumn leaves branch'),
 ('城市街景','chongqing city'),('城市街景','shanghai street'),('城市街景','tokyo rainy street'),('城市街景','paris window architecture'),
 ('生活静物','coffee minimal table'),('生活静物','book reading still life'),('生活静物','vintage film camera'),('生活静物','tea ceramic table')]
session=requests.Session();session.headers.update({'User-Agent':'MomentsStudio/1.0 avatar curation'})
chosen=[]
for category,q in queries:
    accepted=[]
    for page in [1,2,3]:
        response=session.get('https://unsplash.com/napi/search/photos',params={'query':q,'per_page':30,'page':page},timeout=25)
        response.raise_for_status()
        for a in response.json()['results']:
            if a['id'] in seen or a.get('premium') or a.get('plus') or a.get('sponsorship'):continue
            accepted.append(a);seen.add(a['id'])
            if len(accepted)==6:break
        if len(accepted)==6:break
        time.sleep(.4)
    if len(accepted)!=6:raise RuntimeError(f'Insufficient free results for {q}')
    start_id=80+len(chosen)
    chosen.extend((start_id+i,category,a) for i,a in enumerate(accepted))
    print(f'Curated {q}: 6 ({len(chosen)}/120)',flush=True)
    time.sleep(.3)
assert [c[0] for c in chosen]==list(range(80,200))
def download(item):
    id,category,a=item
    url=a['urls']['raw'].split('?')[0]+'?auto=format&fit=crop&w=512&h=512&q=88'
    response=requests.get(url,timeout=35);response.raise_for_status()
    img=ImageOps.fit(Image.open(io.BytesIO(response.content)).convert('RGB'),(256,256),method=Image.Resampling.LANCZOS)
    name=f'{id+1:03}.jpg';dest=out/name;img.save(dest,quality=90,optimize=True)
    return {'id':id,'category':category,'src':'/assets/avatars/'+name,'style':'真实摄影','collection':'replacement',
        'label':a.get('alt_description') or category,'source':a['links']['html'].split('?')[0],'sourceId':a['id'],
        'author':a['user']['name'],'authorUrl':a['user']['links']['html'],'license':'Unsplash License',
        'licenseUrl':'https://unsplash.com/license','imageUrl':url,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
records=[]
with ThreadPoolExecutor(max_workers=6) as executor:
    for result in as_completed([executor.submit(download,a) for a in chosen]):
        records.append(result.result())
        if len(records)%12==0:print(f'Downloaded {len(records)}/120',flush=True)
records.sort(key=lambda a:a['id'])
assert len(records)==120 and len({a['sha256'] for a in records})==120
(stage/'photo-records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for offset in range(0,120,40):
    sheet=Image.new('RGB',(8*144,5*164),'white');draw=ImageDraw.Draw(sheet)
    for i,a in enumerate(records[offset:offset+40]):
        x,y=i%8*144,i//8*164;sheet.paste(Image.open(out/f'{a["id"]+1:03}.jpg').resize((136,136)),(x+4,y+4));draw.text((x+4,y+143),f'#{a["id"]+1}',fill='#222')
    sheet.save(root/f'test-output/replacement-photos-{offset//40+1}.jpg',quality=94)
print('Staged 120 new photo avatars and metadata.',flush=True)
