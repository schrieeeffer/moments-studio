from pathlib import Path
from PIL import Image
import json,shutil,zipfile,hashlib

root=Path(__file__).resolve().parent.parent
stage=root/'source-assets/avatar-replacement'
ai=json.loads((stage/'ai-records.json').read_text(encoding='utf-8'))
photos=json.loads((stage/'photo-records.json').read_text(encoding='utf-8'))
assert len(ai)==48 and [a['id'] for a in ai]==list(range(48)), 'Use completed AI assets only'
assert len(photos)==152 and [a['id'] for a in photos]==list(range(48,200))
items=sorted(ai+photos,key=lambda a:a['id']);assert len(items)==200
avatars=(root/'public/assets/avatars').resolve()
for a in items:
    file=stage/('generated-jpg' if a.get('generated') else 'photos')/f'{a["id"]+1:03}.jpg'
    assert Image.open(file).size==(256,256)
    assert hashlib.sha256(file.read_bytes()).hexdigest()==a['sha256']
backup=stage/'retired-prototypes.zip'
if not backup.exists():
    with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
        for id in range(200):
            file=avatars/f'{id+1:03}.svg'
            if file.exists():z.write(file,file.name)
for a in items:
    file=stage/('generated-jpg' if a.get('generated') else 'photos')/f'{a["id"]+1:03}.jpg'
    shutil.copy2(file,avatars/file.name)
(root/'public/assets/replacement-avatars.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
for id in range(200):
    file=avatars/f'{id+1:03}.svg';assert file.resolve().parent==avatars
    file.unlink(missing_ok=True)
print('Replaced 200 prototype SVG avatars with 200 curated JPEG avatars; private backup retained.')
