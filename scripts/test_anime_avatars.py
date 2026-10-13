from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,zipfile,io,sys
r=Path(__file__).resolve().parent.parent;out=r/'test-output'
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:17888'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page(accept_downloads=True,viewport={'width':1440,'height':1000})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.add_init_script("""if(!localStorage.getItem('avatar-migration-tested')){localStorage.setItem('moments-studio-draft-v1',JSON.stringify({fields:{post:'旧草稿保留检查', 'avatar-pool':'original'},poster:'/assets/avatars/005.svg',likerIds:[1,2,3,4,5,6]}));localStorage.setItem('avatar-migration-tested','1');}""")
 page.goto(url,wait_until='networkidle');page.wait_for_function('window.MomentsStudio')
 assert page.evaluate('MomentsStudio.getConfig().poster')=='/assets/avatars/005.jpg'
 assert page.locator('#post').input_value()=='旧草稿保留检查'
 assert page.locator('#avatar-pool').input_value()=='replacement'
 page.locator('#open-library').click();page.get_by_role('button',name='日本动漫',exact=True).click()
 assert page.locator('.avatar-item').count()==60
 page.screenshot(path=str(out/'japanese-anime-library.png'))
 page.locator('.avatar-item').first.click();assert '/301.jpg' in page.evaluate('MomentsStudio.getConfig().poster')
 page.locator('#avatar-pool').select_option('anime');page.locator('#batch-count').fill('50');page.locator('#generate').click()
 rows=page.evaluate('MomentsStudio.getVariants()');assert len(rows)==50 and len({a['poster'] for a in rows})==50
 assert all(all(300<=id<360 for id in a['likerIds']) for a in rows)
 page.locator('#batch-count').fill('5');page.locator('#generate').click()
 with page.expect_download(timeout=60000) as d:page.locator('#export-batch').click()
 d.value.save_as(str(out/'japanese-anime-batch.zip'))
 with zipfile.ZipFile(out/'japanese-anime-batch.zip') as z:
  names=[n for n in z.namelist() if n.endswith('.png')];assert len(names)==5
  for name in names:assert Image.open(io.BytesIO(z.read(name))).height>2000
 assert not errors,errors;browser.close()
print(json.dumps({'passed':True,'total':360,'anime':60,'checks':['legacy SVG draft migration','custom copy preserved','anime filter','50 unique anime posters','anime liker pool','5 PNG ZIP'],'url':url}))
