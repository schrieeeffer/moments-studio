from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
import sys,json
url=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:17888/moments-studio/').rstrip('/')+'/'
prefix=urlsplit(url).path
out=Path(__file__).resolve().parent.parent/'test-output';out.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page(accept_downloads=True)
 errors=[];bad=[];escaped=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
 page.on('request',lambda r:escaped.append(r.url) if urlsplit(r.url).netloc==urlsplit(url).netloc and not urlsplit(r.url).path.startswith(prefix) else None)
 page.goto(url,wait_until='networkidle');page.wait_for_function('window.MomentsStudio')
 assert page.evaluate('MomentsStudio.getLibrary().length')==360
 assert page.locator('#poster-avatar').evaluate('(img)=>img.complete&&img.naturalWidth>0')
 page.locator('#open-library').click();page.get_by_role('button',name='日本动漫',exact=True).click()
 assert page.locator('.avatar-item').count()==60
 page.wait_for_function('Array.from(document.querySelectorAll(".avatar-item img")).filter(img=>img.getBoundingClientRect().top<innerHeight).every(img=>img.complete&&img.naturalWidth>0)')
 page.locator('.avatar-item').first.click()
 page.screenshot(path=str(out/'static-pages-desktop.png'),full_page=True)
 page.goto(url+'credits.html',wait_until='networkidle')
 assert page.locator('.credits-item').count()==232 and page.locator('.anime-source').count()==60
 page.locator('.credits-item img').first.scroll_into_view_if_needed()
 page.wait_for_function('document.querySelector(".credits-item img").complete&&document.querySelector(".credits-item img").naturalWidth>0')
 assert page.locator('.credits-item img').first.evaluate('(img)=>img.complete&&img.naturalWidth>0')
 page.get_by_role('link',name='← 返回工作台',exact=True).click()
 page.wait_for_function('window.MomentsStudio')
 assert page.url==url
 page.goto(url+'statusbar-sources.html',wait_until='networkidle')
 assert page.locator('a[href="assets/status-bars-v2/inter-OFL.txt"]').count()==1
 assert not bad,bad
 assert not escaped,escaped
 assert not errors,errors
 browser.close()
print(json.dumps({'passed':True,'url':url,'checks':['project subpath','360 avatars','60 anime thumbnails','status fonts and sprites','credits sources and return link','no root path requests','no HTTP or JavaScript errors']}))
