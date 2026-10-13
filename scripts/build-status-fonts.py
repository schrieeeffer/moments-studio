"""Bundle OFL fonts with only status-bar characters; no runtime font service."""
from pathlib import Path
import requests, json
from fontTools.ttLib import TTFont
from fontTools import subset

root=Path(__file__).resolve().parent.parent
dest=root/'public/assets/status-bars-v2'
dest.mkdir(parents=True,exist_ok=True)
rows=[]
for name,filename in [('inter','Inter[opsz,wght].ttf'),('roboto','Roboto[wdth,wght].ttf')]:
    base=f'https://raw.githubusercontent.com/google/fonts/main/ofl/{name}/'
    response=requests.get(base+filename,timeout=30); response.raise_for_status()
    source=root/'source-assets/statusbar-fonts'/filename
    source.parent.mkdir(parents=True,exist_ok=True); source.write_bytes(response.content)
    license_response=requests.get(base+'OFL.txt',timeout=30); license_response.raise_for_status()
    (dest/f'{name}-OFL.txt').write_text(license_response.text,encoding='utf-8')
    font=TTFont(source)
    options=subset.Options(); options.flavor='woff2'
    sub=subset.Subsetter(options=options); sub.populate(text='0123456789:% .KB/sGAVPNHD'); sub.subset(font)
    font.flavor='woff2'; target=dest/f'{name}-status.woff2'; font.save(target)
    rows.append({'name':name,'source':base+filename,'license':'SIL Open Font License 1.1','bytes':target.stat().st_size})
(dest/'font-sources.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows))
