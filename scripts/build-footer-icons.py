"""Calibrate vector glyphs to the original screenshot, including ridge branch.

AI candidates are retained for review. Production vector geometry comes from
the user's original contours after the generated ridge topology was rejected.
"""
from pathlib import Path
from PIL import Image
from scipy.ndimage import gaussian_filter
from skimage.measure import find_contours
import numpy as np
import json

root=Path(__file__).resolve().parent.parent
source=root/'source-assets/comment-footer-v2'
dest=root/'public/assets/icons';dest.mkdir(parents=True,exist_ok=True)
inputs=[('comment-smile-v2','toolbar-reference.png',(10,12,80,82),6),('comment-image-v2','picture-reference.png',None,3)]
assets=[]
for id,filename,box,expected in inputs:
    img=Image.open(source/filename).convert('RGB')
    if box:img=img.crop(box)
    rgb=np.array(img).astype(float);gray=rgb.mean(axis=2)
    edges=np.r_[gray[0],gray[-1],gray[:,0],gray[:,-1]]
    background=float(np.median(edges));ink=float(np.percentile(gray,1))
    alpha=np.clip((background-gray)/(background-ink),0,1)
    curves=[p for p in find_contours(gaussian_filter(alpha,.25),.5) if len(p)>12]
    assert len(curves)==expected,(id,len(curves))
    allpoints=np.concatenate(curves);ymin,xmin=allpoints.min(axis=0);ymax,xmax=allpoints.max(axis=0)
    margin=.3;w=xmax-xmin+2*margin;h=ymax-ymin+2*margin
    def path(points):
        xy=points[:,::-1].copy();xy[:,0]-=xmin-margin;xy[:,1]-=ymin-margin
        if np.linalg.norm(xy[0]-xy[-1])>.001:xy=np.vstack([xy,xy[0]])
        d=np.r_[0,np.cumsum(np.linalg.norm(np.diff(xy,axis=0),axis=1))]
        n=max(32,round(d[-1]/.35));t=np.linspace(0,d[-1],n,endpoint=False)
        q=np.column_stack([np.interp(t,d,xy[:,i]) for i in [0,1]])
        fmt=lambda v:f'{v[0]:.4f} {v[1]:.4f}'
        commands=['M '+fmt(q[0])]
        for i in range(n):
            p0,p1,p2,p3=[q[j%n] for j in [i-1,i,i+1,i+2]]
            commands.append('C '+fmt(p1+(p2-p0)/6)+' '+fmt(p2-(p3-p1)/6)+' '+fmt(p2))
        return ' '.join(commands)+' Z'
    data=' '.join(path(p) for p in curves)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="{512*h/w:.4f}" viewBox="0 0 {w:.4f} {h:.4f}"><path fill="#242424" fill-rule="evenodd" d="{data}"/></svg>\n'
    (dest/(id+'.svg')).write_text(svg,encoding='utf-8')
    assets.append({'id':id,'svg':f'/assets/icons/{id}.svg','png':f'/assets/icons/{id}.png','dimensions':[w,h],'contours':len(curves),'color':'#242424','geometrySource':filename,'method':'original screenshot contour calibration; cubic Bezier vector paths','aiRedraw':'rejected after visual comparison'})
(source/'assets.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(assets))
