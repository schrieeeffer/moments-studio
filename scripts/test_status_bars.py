from playwright.sync_api import sync_playwright
from pathlib import Path
from PIL import Image, ImageDraw
import base64, hashlib, io, json, sys, zipfile

out = Path(__file__).resolve().parent.parent / 'test-output'
out.mkdir(exist_ok=True)
url = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:17888'

def png(data):
    return Image.open(io.BytesIO(base64.b64decode(data.split(',')[1]))).convert('RGBA')

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000},accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(url,wait_until='networkidle')
    page.wait_for_function('window.MomentsStudio && document.querySelector("#preview").height>100')
    styles=page.evaluate('StatusBars.styles')
    assert len(styles)>=10 and len(styles)==page.locator('#status-style option').count()
    results=page.evaluate('''async () => {
      const base=MomentsStudio.getConfig(), rows=[];
      for (const style of StatusBars.styles) {
        const canvas=document.createElement('canvas');
        await MomentsStudio.render({...base,statusStyle:style.id},canvas);
        const small=document.createElement('canvas');
        StatusBars.preview(small,{...base,statusStyle:style.id});
        rows.push({id:style.id,label:style.label,image:canvas.toDataURL(),small:small.toDataURL()});
      }
      return rows;
    }''')
    hashes=set(); body=None
    sheet=Image.new('RGB',(960, len(styles)//2*112),'white')
    draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(results):
        image=png(r['image']); assert image.size==(1080,2340)
        header=image.crop((0,0,1080,128))
        hashes.add(hashlib.sha256(header.tobytes()).hexdigest())
        tail=image.crop((0,130,1080,2340)).tobytes()
        if body is None:body=tail
        assert tail==body, 'Style change affected post content'
        assert image.getextrema()[3]==(255,255), 'Unexpected transparent pixels'
        small=png(r['small'])
        sheet.paste(small.resize((456,54)).convert('RGB'),(i%2*480+12,i//2*112+35))
        draw.text((i%2*480+12,i//2*112+12),r['id'],fill='#222')
    assert len(hashes)==len(styles), 'Duplicate status-bar styles'
    sheet.save(out/'status-styles.png')
    # Every preset responds to the same time and battery inputs, including endpoints.
    values=page.evaluate('''() => StatusBars.styles.map(s=>{
      const a=document.createElement('canvas'),b=document.createElement('canvas');
      StatusBars.preview(a,{statusStyle:s.id,statusTime:'11:00',battery:1});
      StatusBars.preview(b,{statusStyle:s.id,statusTime:'22:00',battery:100});
      return [a.toDataURL(),b.toDataURL()];
    })''')
    assert all(a!=b for a,b in values)
    page.locator('#open-status-styles').click()
    assert page.locator('.status-option').count()==len(styles)
    page.screenshot(path=str(out/'status-gallery.png'))
    page.get_by_role('button',name='选择 小米 · 网速与通知',exact=True).click()
    page.wait_for_timeout(350)
    assert page.evaluate('MomentsStudio.getConfig().statusStyle')=='hyperos-speed'
    page.reload(wait_until='networkidle')
    page.wait_for_function('window.MomentsStudio')
    assert page.locator('#status-style').input_value()=='hyperos-speed'
    page.locator('#random-status').uncheck()
    page.locator('#generate').click()
    page.locator('#status-style').select_option('coloros-ring')
    page.wait_for_timeout(350)
    assert all(c['statusStyle']=='coloros-ring' for c in page.evaluate('MomentsStudio.getVariants()'))
    page.locator('.variant').nth(2).click()
    assert page.locator('#status-style').input_value()=='coloros-ring'
    with page.expect_download(timeout=60000) as d:page.locator('#export-batch').click()
    d.value.save_as(str(out/'status-batch.zip'))
    with zipfile.ZipFile(out/'status-batch.zip') as z:
        records=json.loads(z.read('方案信息.json'))['items']
        assert len(records)==5 and all(c['statusStyle']=='coloros-ring' for c in records)
        for rec,name in zip(records,[n for n in z.namelist() if n.endswith('.png')]):
            exported=Image.open(io.BytesIO(z.read(name))).convert('RGBA')
            data=page.evaluate('''c=>{const canvas=document.createElement('canvas');canvas.width=c.width;canvas.height=Math.ceil(c.width*50/420);const ctx=canvas.getContext('2d');ctx.scale(c.width/420,c.width/420);ctx.fillStyle='#eee';ctx.fillRect(0,0,420,50);StatusBars.draw(ctx,{statusStyle:c.statusStyle,statusTime:c.clock,battery:c.battery});return canvas.toDataURL();}''',rec)
            expected=png(data)
            # Compare full pixels above the last partially covered boundary row.
            actual=exported.crop((0,0,exported.width,int(exported.width*50/420)))
            expected=expected.crop((0,0,expected.width,actual.height))
            assert actual.tobytes()==expected.tobytes(), 'Exported style/time/battery mismatch'
            assert actual.getextrema()[3]==(255,255)
            assert expected.getextrema()[3]==(255,255)
    with page.expect_download() as d:page.locator('#export-current').click()
    d.value.save_as(str(out/'status-current.png'))
    # UI includes live preview, keyboard-compatible native select, and mobile gallery.
    for width in [1024,768,390]:
        page.set_viewport_size({'width':width,'height':844})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('#open-status-styles').click()
    page.screenshot(path=str(out/'status-mobile.png'))
    page.get_by_role('button',name='选择 iOS · 简洁',exact=True).click()
    assert page.locator('#status-style').input_value()=='ios-classic'
    page.goto(url+'/statusbar-sources.html',wait_until='networkidle')
    assert page.locator('section').count()==6 and page.locator('section a').count()>=11
    assert not errors,errors
    browser.close()
print(json.dumps({'passed':True,'styles':len(styles),'checks':['unique headers','unchanged post content','opaque output','dynamic time and battery','visual gallery','saved choice','global batch setting','ZIP metadata','PNG export','responsive layout','official sources','no runtime errors'],'url':url},ensure_ascii=False))
