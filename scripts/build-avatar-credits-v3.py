from pathlib import Path
from collections import Counter
import json,html
root=Path(__file__).resolve().parent.parent
items=json.loads((root/'public/assets/avatars.json').read_text(encoding='utf-8'))
photos=[a for a in items if a.get('license')=='Unsplash License']
generated=[a for a in items if a.get('generated')]
anime=[a for a in items if a.get('collection')=='anime']
e=lambda x:html.escape(str(x),quote=True)
animecards=''.join(f'<div class="anime-source"><img src="{e(a["src"])}" alt="{e(a["label"])}" loading="lazy" width="80" height="80"><p>{e(a["series"])} · {e(a["label"])}</p><a href="{e(a["source"])}" target="_blank" rel="noopener">AniList 角色来源</a></div>' for a in anime)
cards=[]
for a in photos:
    cards.append(f'<div class="credits-item"><img src="{e(a["src"])}" alt="{e(a["category"])} {a["id"]+1}" loading="lazy"><p>#{a["id"]+1} · {e(a["category"])}</p><a href="{e(a["source"])}" target="_blank" rel="noopener">{e(a["author"])} · 原图来源</a></div>')
counts=Counter(a['category'] for a in generated)
page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>素材与开源说明 · 圈图</title><link rel="stylesheet" href="/style.css"></head><body><main class="sources-page"><a href="/">← 返回工作台</a><h1>素材与开源说明</h1>
<p>内置 {len(items)} 张头像：{len(photos)} 张摄影素材、{len(generated)} 张 AI 原创图片、{len(anime)} 张日本动漫角色头像。原来的 200 张统一模板头像已移除；新增 152 张摄影、48 张分别生成的 AI 图片，保留先前的 100 张素材。</p>
<h2>摄影素材</h2><p>包括萌宠、自然风景、花草、生活静物与城市街景。仅采用 Unsplash 免费图片，每张已保存作者、原图和许可。</p><p><a href="https://unsplash.com/license" target="_blank" rel="noopener">Unsplash 官方许可</a> · <a href="/assets/all-photo-avatars.json">全部摄影来源清单</a></p>
<h2>AI 原创素材</h2><p>{e('、'.join(f'{k} {v} 张' for k,v in counts.items()))}。AI 写真人像为虚构成年人，二次元为原创角色。每张使用独立题材和画风提示词，图片只在建库时生成。</p><p><a href="/assets/all-generated-avatars.json">全部 AI 素材清单</a> · <a href="/assets/replacement-avatars.json">本次替换 200 张清单</a></p>
<h2>使用方式</h2><p>全部图片保存在本站，预览、随机选取、单张导出、批量导出直接使用本地图片，不请求第三方图片服务，也不调用 AI。</p><p>旧头像编号保留，旧草稿中的 SVG 头像路径会映射到对应的新头像。</p>
<h2>日本动漫角色头像</h2><p>60 张，来自 AniList 角色资料库，涵盖 10 部作品。原角色及图片版权归相应权利人；来源记录不代表商业使用授权。未移除图片水印，仅选用原图没有明显水印的头像。</p><p><a href="/assets/anime-avatars.json">动漫头像来源清单</a></p><div class="credits-gallery">{animecards}</div>
<h2>程序与隐私</h2><p>JSZip 按 MIT 许可使用。<a href="/assets/dependencies.json">依赖版本与许可清单</a>。头像、封面和文案仅在浏览器中处理。</p>
<h2>摄影素材逐张来源</h2><div class="credits-gallery">{''.join(cards)}</div></main></body></html>'''
(root/'public/credits.html').write_text(page,encoding='utf-8')
for filename,rows in [('all-photo-avatars.json',photos),('all-generated-avatars.json',generated)]:
    (root/'public/assets'/filename).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Credits built for {len(items)} avatars: {len(photos)} photos, {len(generated)} AI images.')
