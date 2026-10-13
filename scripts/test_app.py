from playwright.sync_api import sync_playwright
from pathlib import Path
from PIL import Image
import zipfile,json,sys

out=Path(__file__).resolve().parent.parent/'test-output'
out.mkdir(exist_ok=True)
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:17888'
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1,accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.goto(url,wait_until='networkidle')
    page.wait_for_function('window.MomentsStudio && document.querySelector("#preview").height > 100')
    assert page.evaluate('MomentsStudio.getLibrary().length')==360
    page.screenshot(path=str(out/'desktop.png'),full_page=True)
    page.locator('#open-library').click()
    page.get_by_role('button',name='全部',exact=True).click()
    assert page.locator('.avatar-item').count()==360
    page.get_by_role('button',name='二次元',exact=True).click()
    assert page.locator('.avatar-item').count()==18
    page.locator('.avatar-item').nth(3).click()
    assert not page.locator('#avatar-dialog').is_visible()
    page.locator('#post').fill('测试文案：中文标点、⑤、12345678901 均应保持原样。')
    page.wait_for_timeout(400)
    assert page.evaluate('MomentsStudio.getConfig().post')=='测试文案：中文标点、⑤、12345678901 均应保持原样。'
    with page.expect_download() as d:
        page.locator('#export-current').click()
    d.value.save_as(str(out/'current.png'))
    assert Image.open(out/'current.png').size==(1080,2340)
    page.locator('#generate').click()
    configs=page.evaluate('MomentsStudio.getVariants()')
    assert len(configs)==5
    def minute(t):
        h,m=map(int,t.split(':'));return 60*h+m
    for c in configs:
        assert 660<=minute(c['statusTime'])<=1320
        assert 660<=minute(c['commentTime'])<minute(c['commentTime'])+c['gap']<=1320
        assert c['gap'] in (1,2)
        assert c['likes']>=6 and len(c['likerIds'])==c['likes']==len(set(c['likerIds']))
    with page.expect_download(timeout=60000) as d:
        page.locator('#export-batch').click()
    d.value.save_as(str(out/'batch.zip'))
    with zipfile.ZipFile(out/'batch.zip') as z:
        assert len([n for n in z.namelist() if n.endswith('.png')])==5
        metadata=json.loads(z.read('方案信息.json'))
        assert len(metadata['items'])==5
        for item in metadata['items']:
            assert all(t.startswith('昨天 ') for t in item['commentTimes'])
    page.locator('#time-start').fill('22:00')
    page.locator('#time-end').fill('11:00')
    before=page.evaluate('MomentsStudio.getVariants()')
    page.locator('#generate').click()
    assert '时间范围' in page.locator('#toast').inner_text()
    assert page.evaluate('MomentsStudio.getVariants()')==before
    page.locator('#reset').click()
    page.locator('#post').fill('这是测试自动换行与长截图扩展的内容。'*30)
    page.wait_for_timeout(500)
    assert page.locator('#preview').evaluate('(el)=>el.height')>2340
    page.locator('#reset').click()
    page.wait_for_timeout(500)
    page.screenshot(path=str(out/'desktop.png'),full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    page.wait_for_timeout(360)
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    page.screenshot(path=str(out/'mobile.png'),full_page=True)
    assert not errors, errors
    browser.close()
print(json.dumps({'passed':True,'tests':['360 avatars','category filter','avatar selection','verbatim text','PNG dimensions','random rules','unique liker IDs','5 PNG ZIP','invalid range handling','long text expansion','mobile overflow','no runtime errors'],'url':url},ensure_ascii=False))
