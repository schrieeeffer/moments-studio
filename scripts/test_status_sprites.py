from playwright.sync_api import sync_playwright
from pathlib import Path
from PIL import Image
import io, base64, json, sys

root=Path(__file__).resolve().parent.parent
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:17888'
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page()
    bad=[]
    page.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
    page.goto(url,wait_until='networkidle');page.wait_for_function('window.MomentsStudio')
    assert page.evaluate("document.fonts.check('650 20px StatusInter') && document.fonts.check('550 17px StatusRoboto')")
    assets=page.evaluate("performance.getEntriesByType('resource').map(r=>r.name).filter(n=>/status-bars-v2.*\\.(png|woff2)$/.test(n))")
    assert len(assets)==10,assets
    # Changing time must leave network/battery pixels intact. Battery must leave time/network intact.
    rows=page.evaluate('''()=>StatusBars.styles.map(style=>{
        function image(time,battery){const c=document.createElement('canvas');StatusBars.preview(c,{statusStyle:style.id,statusTime:time,battery});return c.toDataURL();}
        return {id:style.id,base:image('11:00',50),clock:image('22:00',50),low:image('11:00',1),full:image('11:00',100)};
    })''')
    def read(data):return Image.open(io.BytesIO(base64.b64decode(data.split(',')[1]))).convert('RGB')
    for row in rows:
        a,b,c,d=[read(row[k]) for k in ['base','clock','low','full']]
        assert a.crop((240,0,840,100)).tobytes()==b.crop((240,0,840,100)).tobytes(),row['id']
        assert a.crop((0,0,480,100)).tobytes()==c.crop((0,0,480,100)).tobytes()==d.crop((0,0,480,100)).tobytes(),row['id']
        assert a.tobytes()!=b.tobytes() and a.tobytes()!=c.tobytes() and c.tobytes()!=d.tobytes(),row['id']
        assert all(im.crop((0,85,840,100)).getextrema()==((238,238),)*3 for im in [a,b,c,d]),'Status content exceeds strip'
    for old,new in {'android-stock':'harmony-clean','android-notify':'origin-standard','oneui-standard':'magic-pure','oneui-dnd':'magic-notify'}.items():
        page.evaluate('''old=>localStorage.setItem('moments-studio-draft-v1',JSON.stringify({fields:{'status-style':old,nickname:'保留我的昵称',post:'迁移前的文案'}}))''',old)
        page.reload(wait_until='networkidle');page.wait_for_function('window.MomentsStudio')
        assert page.locator('#status-style').input_value()==new
        assert page.locator('#nickname').input_value()=='保留我的昵称'
        assert page.locator('#post').input_value()=='迁移前的文案'
    assert not bad,bad
    browser.close()
print(json.dumps({'passed':True,'styles':len(rows),'loadedRasterAndFonts':len(assets),'legacyDrafts':4,'url':url}))
