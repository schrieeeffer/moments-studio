"""Import generated originals named by their separate per-asset prompts.

input JSON: [{index, name, prompt, path}], ordered by index 0..19.
Resizes assets for web delivery; original outputs and prompts remain local.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import json, shutil, hashlib, sys

root=Path(__file__).resolve().parent.parent
specs=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
assert [s['index'] for s in specs]==list(range(20))
originals=root/'source-assets/generated-avatars';originals.mkdir(parents=True,exist_ok=True)
records=[]
sheet=Image.new('RGB',(10*128,2*148),'white');draw=ImageDraw.Draw(sheet)
for i,s in enumerate(specs):
    file=Path(s['path']);assert file.is_file()
    target=originals/(s['name']+'.png')
    shutil.copy2(file,target)
    img=ImageOps.fit(Image.open(file).convert('RGB'),(256,256),method=Image.Resampling.LANCZOS)
    id=280+i;filename=f'{id+1:03}.jpg';destination=root/'public/assets/avatars'/filename
    img.save(destination,quality=90,optimize=True)
    records.append({'id':id,'category':'写真人像' if i<10 else '二次元','src':'/assets/avatars/'+filename,
      'style':'AI 原创 · 写实虚构人物' if i<10 else 'AI 原创 · 二次元插画','collection':'expanded',
      'generated':True,'label':s['name'],'source':'AI original · built-in image_gen',
      'author':'圈图素材库','license':'AI-generated original asset','sha256':hashlib.sha256(destination.read_bytes()).hexdigest()})
    sheet.paste(img.resize((120,120)),(i%10*128+4,i//10*148+4))
    draw.text((i%10*128+4,i//10*148+127),filename,fill='#222')
    s['path']=str(target)
(originals/'prompts.json').write_text(json.dumps(specs,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'public/assets/generated-avatars.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
sheet.save(root/'test-output/ai-avatar-contact-sheet.jpg',quality=92)
print('Imported 20 originals as lightweight square JPEG avatars.')
