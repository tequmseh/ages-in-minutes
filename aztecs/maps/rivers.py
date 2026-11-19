"""Trace the rivers of the Basin of Mexico 1519 map (blue lines outside the lakes) -> rivers.json (lon/lat polylines)"""
import json, numpy as np, cv2
from PIL import Image
from skimage.morphology import skeletonize
from scipy import ndimage as ndi
from georef import CTRL, fit, to_ll
a=np.asarray(Image.open('/mnt/user-data/uploads/2f220e33-image.webp').convert('RGB')).astype(int)
m=(a[...,2]-a[...,0]>70)&(a[...,0]<90)&(a[...,2]>110)&(a[...,1]>70)
m[:520,1100:]=False; m[2250:,:]=False
lk=cv2.imread('/tmp/lakemask.png',0)>0
lk=cv2.dilate(lk.astype(np.uint8),np.ones((9,9),np.uint8))>0
m&=~lk
m=cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))>0
sk=skeletonize(m)
lab,n=ndi.label(sk,structure=np.ones((3,3)))
px,py=fit(CTRL); out=[]
nb=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
for i in range(1,n+1):
    ys,xs=np.nonzero(lab==i)
    if len(xs)<70: continue
    pts=set(zip(ys.tolist(),xs.tolist()))
    def deg(p): return sum((p[0]+d[0],p[1]+d[1]) in pts for d in nb)
    seen=set(); ends=[p for p in pts if deg(p)==1]
    starts=ends if ends else [next(iter(pts))]
    for s0 in starts:
        if s0 in seen: continue
        path=[s0]; seen.add(s0); cur=s0
        while True:
            nxt=[(cur[0]+d[0],cur[1]+d[1]) for d in nb if (cur[0]+d[0],cur[1]+d[1]) in pts and (cur[0]+d[0],cur[1]+d[1]) not in seen]
            if not nxt: break
            cur=nxt[0]; seen.add(cur); path.append(cur)
        if len(path)<60: continue
        p=np.array(path)[:,::-1].astype(float)
        p=p[::10] if len(p)>20 else p
        out.append([ [round(v,4) for v in to_ll(px,py,x,y)] for x,y in p])
json.dump(out,open('rivers.json','w')); print(len(out),sum(len(o) for o in out))
