from pathlib import Path
from PIL import Image,ImageOps
import requests,io,json,hashlib
r=Path(__file__).resolve().parent.parent;stage=r/'source-assets/japanese-anime'
rows=json.loads((stage/'records.json').read_text(encoding='utf-8'));seen={a['sourceId'] for a in rows}
q='query { Media(idMal:50265,type:ANIME) { characters(perPage:25,sort:[FAVOURITES_DESC]) { nodes { id name { full } image { large } siteUrl } } } }'
resp=requests.post('https://graphql.anilist.co',json={'query':q},timeout=25);resp.raise_for_status()
c=next(a for a in resp.json()['data']['Media']['characters']['nodes'] if a['id'] not in seen and a['image']['large'])
url=c['image']['large'];resp=requests.get(url,timeout=25);resp.raise_for_status()
original=Image.open(io.BytesIO(resp.content)).convert('RGB');im=ImageOps.fit(original,(256,256),method=Image.Resampling.LANCZOS,centering=(.5,.28))
file=stage/'322.jpg';im.save(file,quality=92,optimize=True)
a=rows[21];a.update(label=c['name']['full'],sourceId=c['id'],source=c['siteUrl'],imageUrl=url,sha256=hashlib.sha256(file.read_bytes()).hexdigest(),originalSize=list(original.size))
(stage/'records.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'replaced':322,'name':a['label'],'source':a['source']},ensure_ascii=True))
