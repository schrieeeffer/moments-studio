"""Trace the AI-extracted alpha into genuine scalable SVG contours."""
from pathlib import Path
from PIL import Image
from scipy.ndimage import gaussian_filter
from skimage.measure import find_contours
import numpy as np
import json, shutil

root=Path(__file__).resolve().parent.parent
sources=root/'source-assets/like-icon-v2'
dest=root/'public/assets/icons';dest.mkdir(parents=True,exist_ok=True)
meta=json.loads((sources/'prompt.json').read_text(encoding='utf-8'))
original=sources/meta.get('originalFile','ai-heart-original.png')
if not original.exists():shutil.copy2(meta['generatedPath'],original)
img=Image.open(original).convert('RGBA')
alpha=np.array(img.getchannel('A'))
assert alpha.min()==0 and alpha.max()==255
paths=find_contours(gaussian_filter(alpha.astype(float)/255,1),.5)
paths=sorted(paths,key=len,reverse=True)[:2]
assert len(paths)==2 and all(len(p)>500 for p in paths),'Expected outer outline and transparent inner hole'
points=np.concatenate(paths)
ymin,xmin=points.min(axis=0);ymax,xmax=points.max(axis=0)
margin=2.;w=xmax-xmin+2*margin;h=ymax-ymin+2*margin
def cubic_path(points):
    # Resample each closed contour by arc length, then convert Catmull-Rom
    # segments to cubic Beziers. The alpha, not a hand-designed heart, defines it.
    xy=points[:,::-1].copy();xy[:,0]-=xmin-margin;xy[:,1]-=ymin-margin
    if np.linalg.norm(xy[0]-xy[-1])>0.01:xy=np.vstack([xy,xy[0]])
    distance=np.r_[0,np.cumsum(np.linalg.norm(np.diff(xy,axis=0),axis=1))]
    steps=max(64,round(distance[-1]/7))
    t=np.linspace(0,distance[-1],steps,endpoint=False)
    q=np.column_stack([np.interp(t,distance,xy[:,i]) for i in [0,1]])
    fmt=lambda p:f'{p[0]:.3f} {p[1]:.3f}'
    commands=['M '+fmt(q[0])]
    for i in range(len(q)):
        p0,p1,p2,p3=[q[j%len(q)] for j in [i-1,i,i+1,i+2]]
        commands.append('C '+fmt(p1+(p2-p0)/6)+' '+fmt(p2-(p3-p1)/6)+' '+fmt(p2))
    return ' '.join(commands)+' Z'
rgb=np.array(img)[:,:,:3][alpha>240]
color='#'+''.join(f'{round(v):02x}' for v in np.median(rgb,axis=0))
data=' '.join(cubic_path(p) for p in paths)
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.3f}" height="{h:.3f}" viewBox="0 0 {w:.3f} {h:.3f}"><path fill="{color}" fill-rule="evenodd" d="{data}"/></svg>\n'
(dest/'like-heart-v2.svg').write_text(svg,encoding='utf-8')
bbox=(int(np.floor(xmin))-2,int(np.floor(ymin))-2,int(np.ceil(xmax))+3,int(np.ceil(ymax))+3)
cropped=img.crop(bbox);cropped.save(dest/'like-heart-v2.png',optimize=True)
details={'tool':'built-in image_gen, followed by alpha contour tracing','svg':'/assets/icons/like-heart-v2.svg','png':'/assets/icons/like-heart-v2.png','color':color,'viewBox':[w,h],'logicalSize':[18.2,18.2*h/w],'contours':2,'reference':'user-provided original Moments screenshot, like icon','tracing':'closed cubic Bezier contours; true vector paths, no embedded raster'}
(sources/'asset.json').write_text(json.dumps(details,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(details))
