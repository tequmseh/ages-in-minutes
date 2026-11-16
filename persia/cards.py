import sys, subprocess, os
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1920,1080,30
BG=(17,17,17); WHITE=(242,240,235); GRAY=(120,124,128); DIM=(70,72,75); ACC=(242,194,48)
def font(bold,size):
    cands = (["/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf","/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else
             ["/usr/share/fonts/opentype/inter/Inter-Regular.otf","/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
    for c in cands:
        if os.path.exists(c): return ImageFont.truetype(c,size)
    raise SystemExit("no font")
F_T=font(True,150); F_CH=font(False,30); F_TICK=font(False,24); F_RANGE=font(True,40); F_END=font(False,24)
X0,X1,Y=160,1760,840
Y0,YE=550,323
def xof(y): return X0+(Y0-y)/(Y0-YE)*(X1-X0)
TICKS=[550,539,530,522,509,499,492,490,486,480,465,387,343,323]
CH=[("CHAPTER 1","NOBODY FROM NOWHERE",550,539),
    ("CHAPTER 2","BABYLON AND THE CYLINDER",539,530),
    ("CHAPTER 3","DARIUS TAKES CONTROL OF THE STORY",530,522),
    ("CHAPTER 4","THE OPERATING SYSTEM",522,486),
    ("CHAPTER 5","BEATING DISTANCE",522,486),
    ("CHAPTER 6","PERSEPOLIS AND THE RECEIPTS",509,493),
    ("CHAPTER 7","THE PRICE",499,492),
    ("CHAPTER 8","XERXES GOES WEST",490,480),
    ("CHAPTER 9","THE SAME WAR, SEEN FROM SUSA",480,465),
    ("CHAPTER 10","IF YOU CAN'T BEAT THEM, RENT THEM",465,387),
    ("CHAPTER 11","THE LAST ACHAEMENID",343,323),
    ("CHAPTER 12","WHAT THE TABLET SAYS",323,None)]
SLUG=["nobody_from_nowhere","babylon_and_the_cylinder","darius_takes_control","the_operating_system","beating_distance","persepolis_and_the_receipts","the_price","xerxes_goes_west","seen_from_susa","rent_them","the_last_achaemenid","what_the_tablet_says"]
CH=[(l,t,a,b,(f"{a}–{b} BC" if b else "323 BC → TODAY")) for l,t,a,b in CH]
def fit(d,text,maxw=1600,size=150):
    while True:
        f=font(True,size)
        if d.textlength(text,font=f)<=maxw or size<=80: return f
        size-=4
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def blend(c,a): return tuple(int(BG[i]+(c[i]-BG[i])*a) for i in range(3))
def spaced(d,xy,text,f,fill,sp=4):
    x,y=xy
    for ch in text:
        d.text((x,y),ch,font=f,fill=fill); x+=d.textlength(ch,font=f)+sp
def frame(i,t,first):
    lab,title,a,b,rng=CH[i]
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    lp=ease(t/0.7) if first else 1
    xe=X0+(X1-X0)*lp
    d.line([(X0,Y),(xe,Y)],fill=DIM,width=3)
    for y in TICKS:
        x=xof(y)
        if x<=xe:
            d.line([(x,Y-10),(x,Y+10)],fill=GRAY,width=2)
            wide = (a is not None and b is not None and abs(xof(b)-xof(a))>=110)
            if y in (Y0,YE) or (y in (a,b) and wide and min(abs(x-X0),abs(x-X1))>=100):
                s=f"{y} BC" if y in (Y0,YE) else str(y)
                w=d.textlength(s,font=F_TICK)
                tx = x if y==Y0 else x-w/2
                d.text((tx,Y+26),s,font=F_TICK,fill=(ACC if y in (a,b) else GRAY))
    sp=ease((t-0.4)/0.9)
    if a is None:                      # before the scale: bar runs left from its start, arrow pointing left
        xr=xof(b); xl=xr-(xr-70)*sp
        if sp>0:
            d.rectangle([xl,Y-7,xr,Y+7],fill=ACC)
            if sp>0.98: d.polygon([(xl,Y-22),(xl-34,Y),(xl,Y+22)],fill=ACC)
        cx=None
    elif b is not None:
        xa=xof(a); xb=xa+max(xof(b)-xa,8)*sp
        if sp>0: d.rectangle([xa,Y-7,xb,Y+7],fill=ACC)
        cx=(xa+xof(b))/2
    else:
        xa=xof(a); xb=xa+(W-60-xa)*sp
        if sp>0:
            d.rectangle([xa,Y-7,xb,Y+7],fill=ACC)
            if sp>0.98: d.polygon([(xb,Y-22),(xb+34,Y),(xb,Y+22)],fill=ACC)
        cx=(xa+W-60)/2
    ra=ease((t-0.9)/0.5)
    if ra>0:
        w=d.textlength(rng,font=F_RANGE); tx=(40 if cx is None else min(max(cx-w/2,X0),W-26-w if b is None else X1-w))
        d.text((tx,Y-78),rng,font=F_RANGE,fill=blend(ACC,ra))
    ta=ease((t-0.3)/0.6); off=int(30*(1-ta))
    spaced(d,(X0,250),lab,F_CH,blend(GRAY,ta),6)
    d.text((X0-6,310+off),title,font=fit(d,title),fill=blend(WHITE,ta))
    return im
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="test":
        for i,t in [(i,3.0) for i in range(12)]:
            frame(i,t,i==0).resize((960,540)).save(f"test_{i:02d}.png")
    else:
        i=int(mode); dur=3.5; n=int(dur*FPS)
        name=f"out/persia_chapter_{i+1:02d}_{SLUG[i]}"; tmp=name+".tmp.mp4"
        p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p",tmp],stdin=subprocess.PIPE)
        for k in range(n): p.stdin.write(frame(i,k/FPS,i==0).tobytes())
        p.stdin.close()
        if p.wait()==0: os.rename(tmp,name+".mp4")
