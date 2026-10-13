from pathlib import Path
from collections import Counter
from PIL import Image
from playwright.sync_api import sync_playwright
import json, zipfile, io, base64, sys, time

root=Path(__file__).resolve().parent.parent
out=root/'test-output';out.mkdir(exist_ok=True)
url=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:17888').rstrip('/')
def minute(t):
    h,m=map(int,t.replace('昨天 ','').split(':'));return h*60+m
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1100},accept_downloads=True)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(url,wait_until='networkidle');page.wait_for_function('window.MomentsStudio')
    assert page.locator('#batch-count').get_attribute('max')=='50'
    page.locator('#post').fill('自定义文案保持原样：中文、⑤、123456。')
    page.locator('#batch-count').fill('7')
    with page.expect_download(timeout=120000) as d:page.locator('#generate-download').click()
    d.value.save_as(str(out/'flexible-seven.zip'))
    configs=page.evaluate('MomentsStudio.getVariants()')
    assert len(configs)==7
    for key in ['poster','nickname','battery','statusStyle','statusTime']:
        assert len({c[key] for c in configs})==7,key
    assert all(c['post']=='自定义文案保持原样：中文、⑤、123456。' for c in configs)
    for c in configs:
        assert c['gap'] in [1,2] and 660<=minute(c['commentTime'])<minute(c['commentTime'])+c['gap']<=1320
        assert len(c['likerIds'])==len(set(c['likerIds']))==c['likes']>=6
    # ZIP uses each variant's style, time and battery rather than a global override.
    with zipfile.ZipFile(out/'flexible-seven.zip') as z:
        names=[n for n in z.namelist() if n.endswith('.png')]
        records=json.loads(z.read('方案信息.json'))['items'];assert len(names)==len(records)==7
        for name,c in zip(names,configs):
            png=Image.open(io.BytesIO(z.read(name))).convert('RGBA')
            rec=records[names.index(name)];assert rec['statusStyle']==c['statusStyle'] and rec['battery']==c['battery']
            expected=page.evaluate('''c=>{const canvas=document.createElement('canvas');canvas.width=c.width;canvas.height=Math.ceil(c.width*50/420);const ctx=canvas.getContext('2d');ctx.scale(c.width/420,c.width/420);ctx.fillStyle='#eee';ctx.fillRect(0,0,420,50);StatusBars.draw(ctx,c);return canvas.toDataURL();}''',c)
            header=Image.open(io.BytesIO(base64.b64decode(expected.split(',')[1]))).convert('RGBA')
            h=int(c['width']*50/420);assert png.crop((0,0,c['width'],h)).tobytes()==header.crop((0,0,c['width'],h)).tobytes()
    page.locator('#batch-count').fill('50')
    started=time.perf_counter()
    with page.expect_download(timeout=180000) as d:page.locator('#generate-download').click()
    elapsed=time.perf_counter()-started
    d.value.save_as(str(out/'flexible-fifty.zip'))
    configs=page.evaluate('MomentsStudio.getVariants()');assert len(configs)==50
    for key in ['poster','nickname','battery']:assert len({c[key] for c in configs})==50,key
    for values,choices in [(Counter(c['statusStyle'] for c in configs),14),(Counter((c['width'],c['height']) for c in configs),5)]:
        assert len(values)==choices and max(values.values())-min(values.values())<=1
    assert len({tuple(c['likerIds']) for c in configs})==50
    with zipfile.ZipFile(out/'flexible-fifty.zip') as z:
        assert len([n for n in z.namelist() if n.endswith('.png')])==50
        assert len(json.loads(z.read('方案信息.json'))['items'])==50
    page.wait_for_function('!document.querySelector("#generate").disabled')
    before=page.evaluate('MomentsStudio.getVariants()')
    for value in ['','0','51','-1','3.5']:
        page.locator('#batch-count').fill(value);page.locator('#generate').click()
        assert '1–50' in page.locator('#toast').inner_text()
        assert page.evaluate('MomentsStudio.getVariants()')==before
    # Fixed modes and tiny time ranges stay valid; battery makes full combinations unique.
    for id in ['random-status','random-size','random-identity']:page.locator('#'+id).uncheck()
    page.locator('#time-start').fill('21:58');page.locator('#time-end').fill('22:00')
    page.locator('#batch-count').fill('50');page.locator('#generate').click()
    fixed=page.evaluate('MomentsStudio.getVariants()')
    for key in ['statusStyle','poster','nickname','width','height']:assert len({c[key] for c in fixed})==1,key
    assert len({c['battery'] for c in fixed})==50
    assert all(1318<=minute(c['commentTime'])<minute(c['commentTime'])+c['gap']<=1320 for c in fixed)
    # Single-image minimum and saved custom count.
    page.locator('#batch-count').fill('1');page.locator('#generate').click()
    assert len(page.evaluate('MomentsStudio.getVariants()'))==1
    page.reload(wait_until='networkidle');page.wait_for_function('window.MomentsStudio')
    assert page.locator('#batch-count').input_value()=='1' and not page.locator('#random-status').is_checked()
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(out/'flexible-batch-mobile.png'),full_page=True)
    assert not errors,errors
    browser.close()
print(json.dumps({'passed':True,'customCount':7,'maximumCount':50,'exportSeconds':round(elapsed,2),'zipMiB':round((out/'flexible-fifty.zip').stat().st_size/1048576,2),'url':url},ensure_ascii=False))
