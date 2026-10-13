from pathlib import Path
import re, json

root=Path(__file__).resolve().parent.parent
s=(root/'public/status-bars.js').read_text(encoding='utf-8')
rows=re.findall(r"\{id:'([^']+)',label:'([^']+)',description:'([^']+)',family:'([^']+)'\}",s)
assert len(rows)==14
groups=[]
for family in dict.fromkeys(r[3] for r in rows):
    options=''.join(f'<option value="{r[0]}">{r[1]}</option>' for r in rows if r[3]==family)
    groups.append(f'<optgroup label="{dict(ios="iOS",xiaomi="小米",huawei="华为 HarmonyOS",oppo="OPPO ColorOS",vivo="vivo OriginOS",honor="荣耀 MagicOS")[family]}">{options}</optgroup>')
p=root/'public/index.html';html=p.read_text(encoding='utf-8')
html=re.sub(r'(<select id="status-style">).*?(</select>)',lambda m:m[1]+'\n'+''.join(groups)+'\n'+m[2],html,flags=re.S)
html=html.replace('12 款','14 款').replace('查看官方参考来源','查看截图与参考来源').replace('参考官方系统图标资料制作，不是原机截图。','参考大陆常见系统截图制作；不同版本和设置会有差异。')
p.write_text(html,encoding='utf-8')
print(json.dumps({'styles':len(rows)}))
