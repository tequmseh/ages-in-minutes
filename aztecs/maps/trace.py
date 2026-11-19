"""Trace lake polygons (lon/lat) from the georeferenced Basin of Mexico 1519 map -> lakes.json"""
import json, numpy as np, cv2
from PIL import Image
from georef import CTRL, fit, to_ll
a=np.asarray(Image.open('/mnt/user-data/uploads/2f220e33-image.webp').convert('RGB')).astype(int)
tgt=np.array([200,236,255]); m=(np.abs(a-tgt).sum(2)<40).astype(np.uint8)*255
# fill the text labels and the thin lines inside the lakes, then clean specks
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
m[:520,1100:]=0; m[2250:,:700]=0; m[2380:,:]=0           # title box, legend, scale bar
m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
cv2.imwrite('/tmp/lakemask.png',m)
cs,h=cv2.findContours(m,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
px,py=fit(CTRL); out=[]
for i,c in enumerate(cs):
    A=cv2.contourArea(c)
    if A<600: continue
    eps=2.2; c2=cv2.approxPolyDP(c,eps,True)[:,0,:]
    ring=[to_ll(px,py,float(x),float(y)) for x,y in c2]
    out.append({"hole": bool(h[0][i][3]>=0), "area_px": A, "ring": [(round(a_,4),round(b,4)) for a_,b in ring]})
json.dump(out,open('lakes.json','w'))
print(len(out),[(o['hole'],int(o['area_px'])) for o in out])
