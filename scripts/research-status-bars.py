"""Save source screenshots for visual study; never publish third-party captures."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw,ImageOps
import requests,json,io

root=Path(__file__).resolve().parent.parent
out=root/'source-assets/statusbar-research';out.mkdir(parents=True,exist_ok=True)
samples=[
 {'id':'xiaomi-community','system':'小米澎湃 OS','source':'https://web.vip.miui.com/page/info/mio/mio/detail?postId=52332496','image':'https://cdn.cnbj1.fds.api.mi-img.com/middle.community.vip.bkt/6ba242865b929e098b6f628113df3f8a?f=webp&q=80&thumb=1&w=1080'},
 {'id':'xiaomi-review','system':'小米澎湃 OS','source':'https://zhongce.sina.com.cn/article/view/180408','image':'https://zhongces3.sina.com.cn/product/20240310/1e8f7df2426deb578ec86cf3865fce0f.jpeg'},
 {'id':'oppo-community','system':'OPPO ColorOS','source':'https://www.oppo.cn/thread-399423032-1','image':'https://imgfs.oppo.cn/uploads/thread/attachment/2022/07/07/1657142681038583400.jpg'},
 {'id':'vivo-sdk','system':'vivo OriginOS','source':'https://help.aliyun.com/zh/document_detail/3030718.html','image':'https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2540457771/p1071047.png'},
 {'id':'vivo-community','system':'vivo OriginOS 对比','source':'https://bbs.vivo.com/in/thread/161651','image':'https://in-exstatic-vivofs.vivo.com/bCy1HLzT9bUXp6Mb/IN-VIVO/threadResource/20250218/38211ba4c93d46ea861d88370e078a4f_w3264_h3264.png'},
 {'id':'honor-community','system':'荣耀 MagicOS','source':'https://club.honor.com/cn/thread-28094158-1-1.html','image':'https://res1-cn.c.hihonor.com/data/attachment/forum/202311/13/4d2a287c1a87c14252a2e61e141501bab324e2da7231c7c8ca43c5998d0f432a.jpg'},
 {'id':'huawei-guide','system':'华为 HarmonyOS 2 / P40','source':'https://jingyan.baidu.com/article/e4511cf32061ed6a855eaf20.html','image':'https://exp-picture.cdn.bcebos.com/0d55dc7bd2828689c6e44f0765f97fbd4d7c3739.jpg'},
 {'id':'huawei-official','system':'华为官方应用展示','source':'https://consumer.huawei.com/cn/myhuawei-app/','image':'https://consumer.huawei.com/content/dam/huawei-cbg-site/greate-china/cn/mkt/myhuawei-app-download/img/250520/4.png'},
]
def download(s):
 try:
  r=requests.get(s['image'],timeout=25);r.raise_for_status()
  im=Image.open(io.BytesIO(r.content)).convert('RGB')
  path=out/(s['id']+'.png');im.save(path)
  return {**s,'path':str(path),'width':im.width,'height':im.height}
 except Exception as e:return {**s,'error':str(e)}
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=4) as executor:records=list(executor.map(download,samples))
 (out/'sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
 for r in records:print(json.dumps({k:v for k,v in r.items() if k not in ('image','source')},ensure_ascii=False),flush=True)
