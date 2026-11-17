"""Rome: вырезки вставок V01–V33. python3 -I mkcut.py [ключи]. Вход — присланные файлы (хеш имени из чата), выход cut/*.png и full/*.jpg.
opts: crop=(x0,y0,x1,y1) доли; fill=True — залить дыры (плоские предметы); cutline=((x,y),...) — убрать всё ниже ломаной (координаты в пикселях кропа)."""
import sys, glob, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
from rembg import remove, new_session
U="/mnt/user-data/uploads/"; OUT=os.environ.get("OUT","/home/claude/work/inserts")
Image.MAX_IMAGE_PIXELS=None
def P(h): return glob.glob(U+h+"*")[0]
J={ # ключ: (хеш, режим, opts)
"V01_wolf":("9ce076f8","cut",{}),
"V02_arch_titus":("9494d41e","full",{}),
"V03_servian_wall":("73f59575","full",{}),
"V04_appia":("818354db","full",{}),
"V05_pyrrhus":("05eecf02","cut",{}),
"V06_pompeius_rufus":("7f3cc5a3","cut",{}),
"V07_pompey":("dd3b6af4","cut",{}),
"V08_caesar":("5554ceb3","cut",{"cuty":0.635}),
"V09_caesar_1678":("V09","full",{}),
"V10_eid_mar":("67a98db7","cut",{}),
"V11_octavian":("611e37b5","cut",{}),
"V12_antony_cleopatra":("769d25d3","cut",{}),
"V13_prima_porta":("5d195441","cut",{"cuty":0.93}),
"V14_caelius":("288524cb","cut",{"crop":(0,0,1700/2800,1),"fill":True}),
"V15_aqueduct":("490e490e","full",{}),
"V16_trevi":("468a9128","full",{}),
"V17_pollice_verso":("bb1f37f4","full",{}),
"V18_trajan":("24d97d18","cut",{"cuty":0.885}),
"V19_hadrian":("3317e3fc","cut",{"cutline":((0,1800),(560,1738),(1700,1738))}),
"V20_septimius":("bf823934","cut",{"cuty":0.80,"arc":0.02}),
"V21_marcus_aurelius":("8ef5929f","cut",{"keepbig":0.1}),
"V22_shapur":("aeebb1e6","full",{}),
"V23_zenobia":("c2e08988","cut",{}),
"V24_tetrarchs":("e375d29c","cut",{}),
"V25_constantine":("991dd6b8","cut",{"cuty":0.875}),
"V26_missorium":("007241e0","cut",{}),
"V27_romulus_augustus":("94411ee9","cut",{"stack":True}),
"V28_spqr_cover":("1961927c","full",{}),
"V29_crassus":("b56fb332","cut",{"cuty":0.855}),
"V30_cato":("cf9461bc","cut",{"cuty":0.80}),
"V31_hannibal":("a6db3266","cut",{"cuty":0.915}),
"V32_scipio":("96966685","cut",{"brightbottom":0.80,"cuty":0.93}),
"V33_marius":("79a5d0fd","cut",{}),
}
def load(h):
    p=P(h); im=Image.open(p)
    return im.convert("RGB")
def bbox(o): return o.getchannel("A").point(lambda v:255 if v>24 else 0).getbbox()
def cut(im,ses,o):
    r=remove(im,session=ses)
    A=np.array(r.getchannel("A")).astype(float); A=np.clip((A-100)/110.0,0,1)  # убрать полупрозрачные тени и ореол
    lab,n=ndi.label(A>0.5)
    if n>1:
        sz=ndi.sum(A>0.5,lab,range(1,n+1)); keep=[i+1 for i,v in enumerate(sz) if v>=0.02*sz.max()]; A=A*np.isin(lab,keep)
    A=np.array(Image.fromarray((A*255).astype("uint8")).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0)))
    r.putalpha(Image.fromarray(A)); a=A>24
    if o.get("fill"):
        lab,n=ndi.label(a); s=ndi.sum(a,lab,range(1,n+1)); a=ndi.binary_fill_holes(lab==(1+int(np.argmax(s))))
        r.putalpha(Image.fromarray((a*255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2)))
    if o.get("cutline"):
        bb=bbox(r); w,h=r.size; pts=[(x+bb[0],y+bb[1]) for x,y in o["cutline"]]  # координаты относительно габарита вырезки
        m=Image.new("L",(w,h),0); ImageDraw.Draw(m).polygon([(0,0),(w,0),(w,pts[-1][1])]+pts[::-1],fill=255)
        m=m.filter(ImageFilter.GaussianBlur(2)); r.putalpha(Image.fromarray(np.minimum(np.array(r.getchannel("A")),np.array(m))))
    if o.get("cuty") or o.get("brightbottom"):
        bb=bbox(r); a=np.array(r.getchannel("A")).astype(float)
        if o.get("cuty"):  # срез по дуге: центр ниже краёв, как основание бюста
            H=bb[3]-bb[1]; W=bb[2]-bb[0]; y0=bb[1]+o["cuty"]*H; cx=(bb[0]+bb[2])/2; hw=W/2
            yy=np.arange(a.shape[0])[:,None]; xx=np.arange(a.shape[1])[None,:]
            edge=y0-o.get("arc",0.03)*H*np.clip((xx-cx)/hw,-1,1)**2
            m=(yy<edge).astype(float)
            m=np.array(Image.fromarray((m*255).astype("uint8")).filter(ImageFilter.GaussianBlur(2)))/255.0; a=a*m
        if o.get("brightbottom"):  # светлое основание под тёмной бронзой (V32)
            y0=int(bb[1]+o["brightbottom"]*(bb[3]-bb[1])); px=np.array(r.convert("RGB")).astype(int)
            bad=(px.max(axis=2)>150); bad[:y0]=False; a[bad]=0
        r.putalpha(Image.fromarray(a.astype("uint8")))
    if o.get("keepbig"):
        a=np.array(r.getchannel("A"))>24; lab,n=ndi.label(a); sz=ndi.sum(a,lab,range(1,n+1)); keep=[i+1 for i,v in enumerate(sz) if v>=o["keepbig"]*sz.max()]
        r.putalpha(Image.fromarray((np.isin(lab,keep)*np.array(r.getchannel("A"))).astype("uint8")))
    return r.crop(bbox(r))
if __name__=="__main__":
    os.makedirs(OUT+"/cut",exist_ok=True); os.makedirs(OUT+"/full",exist_ok=True)
    ses=new_session("isnet-general-use")
    for k in (sys.argv[1:] or J):
        h,m,o=J[k]; im=load(h)
        if o.get("crop"): c=o["crop"]; im=im.crop((int(c[0]*im.width),int(c[1]*im.height),int(c[2]*im.width),int(c[3]*im.height)))
        if m=="full": im.save(f"{OUT}/full/{k}.jpg",quality=95); print(k,"full",im.size); continue
        if o.get("stack"): # две монеты друг над другом -> рядом
            hh=im.height//2; parts=[cut(im.crop((0,i*hh,im.width,(i+1)*hh)),ses,{}) for i in (0,1)]
            H=max(p.height for p in parts); r=Image.new("RGBA",(sum(p.width for p in parts)+40,H),(0,0,0,0)); x=0
            for p in parts: r.paste(p,(x,(H-p.height)//2)); x+=p.width+40
        else: r=cut(im,ses,o)
        r.save(f"{OUT}/cut/{k}.png"); print(k,"cut",r.size,"LOW" if max(r.size)<1000 else "")
