from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from collections import Counter
import hashlib, io, json, sys, zipfile

root=Path(__file__).resolve().parent.parent
out=root/'test-output';out.mkdir(exist_ok=True)
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:17888'
manifest=json.loads((root/'public/assets/avatars.json').read_text(encoding='utf-8'))
assert len(manifest)==360
new=[a for a in manifest if a.get('collection')=='expanded']
assert len(new)==100
assert len([a for a in new if a.get('generated')])==20
hashes=set()
for a in new:
 file=root/'public'/a['src'].lstrip('/')
 assert file.is_file()
 im=Image.open(file);assert im.size==(256,256)
 hashes.add(hashlib.sha256(im.tobytes()).hexdigest())
 assert a.get('source') and a.get('license')
assert len(hashes)==100

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':1440,'height':1000},accept_downloads=True)
 errors=[];failed=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:failed.append(r.url) if r.status>=400 else None)
 page.goto(url,wait_until='networkidle')
 page.wait_for_function('window.MomentsStudio && document.querySelector("#preview").height>100')
 assert page.evaluate('MomentsStudio.getLibrary().length')==360
 assert page.locator('#avatar-pool').input_value()=='all'
 page.locator('#avatar-pool').select_option('expanded')
 page.locator('#open-library').click()
 assert page.locator('.avatar-item').count()==360
 first_categories=page.locator('.avatar-item').evaluate_all('(els)=>els.slice(0,7).map(el=>el.querySelector("img").alt.split(" ")[0])')
 assert len(set(first_categories))==7,first_categories
 page.screenshot(path=str(out/'avatar-library-desktop.png'))
 for category,n in Counter(a['category'] for a in manifest).items():
  page.get_by_role('button',name=category,exact=True).click()
  assert page.locator('.avatar-item').count()==n
  page.locator('.avatar-item').first.click()
  page.wait_for_timeout(250)
  selected=page.evaluate('MomentsStudio.getConfig().poster')
  page.reload(wait_until='networkidle');page.wait_for_function('window.MomentsStudio')
  assert page.evaluate('MomentsStudio.getConfig().poster')==selected,category
  page.locator('#open-library').click()
 page.get_by_role('button',name='全部',exact=True).click()
 assert page.locator('.avatar-item').count()==360
 page.locator('#close-library').click()
 page.locator('#batch-count').fill('50')
 page.locator('#generate').click()
 configs=page.evaluate('MomentsStudio.getVariants()')
 assert len(configs)==50
 for c in configs:
  assert manifest[next(a['id'] for a in manifest if a['src']==c['poster'])]['collection']=='expanded'
  assert all(id>=200 for id in c['likerIds'])
  assert len(c['likerIds'])==len(set(c['likerIds']))==c['likes']
  cats={manifest[id]['category'] for id in c['likerIds']}
  assert len(cats)>=min(5,c['likes'])
 page.locator('#avatar-pool').select_option('replacement')
 page.locator('#batch-count').fill('5')
 page.locator('#generate').click()
 assert all(all(id<200 for id in c['likerIds']) for c in page.evaluate('MomentsStudio.getVariants()'))
 page.locator('#avatar-pool').select_option('expanded')
 page.locator('#generate').click()
 with page.expect_download(timeout=60000) as d:page.locator('#export-batch').click()
 d.value.save_as(str(out/'expanded-avatar-batch.zip'))
 with zipfile.ZipFile(out/'expanded-avatar-batch.zip') as z:
  records=json.loads(z.read('方案信息.json'))['items']
  assert len(records)==5
  assert all(c['avatarSources'] and all(a.get('source') for a in c['avatarSources']) for c in records)
  for name in z.namelist():
   if name.endswith('.png'):assert Image.open(io.BytesIO(z.read(name))).width in (1080,1170,1200)
 page.set_viewport_size({'width':390,'height':844})
 page.locator('#open-library').click()
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 close=page.locator('#close-library').bounding_box()
 assert close['y']>=0 and close['y']+close['height']<=844
 page.screenshot(path=str(out/'avatar-library-mobile.png'))
 page.locator('#close-library').click()
 page.goto(url+'/credits.html',wait_until='networkidle')
 assert page.locator('.credits-item').count()==232
 assert not errors,errors
 assert not failed,failed
 browser.close()
print(json.dumps({'passed':True,'total':360,'new':100,'categories':dict(Counter(a['category'] for a in new)),'checks':['100 unique square JPEGs','source records','mixed gallery','category filters','JPEG draft persistence','balanced random pool','50 plan generation','original pool','ZIP source metadata','mobile gallery','no HTTP or JS errors'],'url':url},ensure_ascii=False))
