import sys, subprocess, os
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1920,1080,60
BG=(17,17,17); WHITE=(242,240,235); GRAY=(120,124,128); DIM=(70,72,75); ACC=(242,194,48)
def font(bold,size):
    cands = (["/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf","/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else
             ["/usr/share/fonts/opentype/inter/Inter-Regular.otf","/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
    for c in cands:
        if os.path.exists(c): return ImageFont.truetype(c,size)
    raise SystemExit("no font")
F_T=font(True,150); F_CH=font(False,30); F_TICK=font(False,24); F_RANGE=font(True,40); F_END=font(False,24)
X0,X1,Y=160,1760,840
Y0,YE=1250,1521
def xof(y): return X0+(y-Y0)/(YE-Y0)*(X1-X0)
# chapter, title, from, to (None = before / beyond the scale), label. Years set from script.md (ch. 7 has no dates of its own: the imperial period).
CH=[("CHAPTER 1","THE PEOPLE WITH THE WRONG NAME",1250,1325,"1250–1325"),
    ("CHAPTER 2","THE EAGLE AND THE CACTUS",1325,1427,"1325–1427"),
    ("CHAPTER 3","A CITY BUILT ON WATER",1325,1449,"1325–1449"),
    ("CHAPTER 4","THREE CITIES AGAINST ONE",1427,1428,"1427–1428"),
    ("CHAPTER 5","AN EMPIRE OF TRIBUTE",1440,1502,"1440–1502"),
    ("CHAPTER 6","THE CITY ON THE LAKE",1519,1519,"1519"),
    ("CHAPTER 7","GROWING UP AZTEC",1428,1519,"1428–1519"),
    ("CHAPTER 8","FEEDING THE SUN",1487,1507,"1487–1507"),
    ("CHAPTER 9","WARS OF FLOWERS",1502,1519,"1502–1519"),
    ("CHAPTER 10","STRANGERS FROM THE SEA",1519,1519,"1519"),
    ("CHAPTER 11","THE FALL",1520,1521,"1520–1521"),
    ("CHAPTER 12","WHAT REMAINS",1521,None,"1521 → TODAY")]
def fmt(y): return str(y)
TICKS=sorted({y for _,_,a_,b_,_ in CH for y in (a_,b_) if y}|{Y0,YE})
SLUG=["the_people_with_the_wrong_name","the_eagle_and_the_cactus","a_city_built_on_water","three_cities_against_one","an_empire_of_tribute","the_city_on_the_lake","growing_up_aztec","feeding_the_sun","wars_of_flowers","strangers_from_the_sea","the_fall","what_remains"]
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
                s=fmt(y)
                w=d.textlength(s,font=F_TICK)
                tx = x if y==Y0 else (x-w if y==YE else x-w/2)
                d.text((tx,Y+26),s,font=F_TICK,fill=(ACC if y in (a,b) else GRAY))
    sp=ease((t-0.4)/0.9)
    if a is None:                      # before the scale: bar runs left from its start, arrow pointing left
        xr=xof(b); xl=xr-(xr-70)*sp
        xr=X0; xl=xr-(xr-70)*sp
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
        name=f"out/aztecs_chapter_{i+1:02d}_{SLUG[i]}"; tmp=name+".tmp.mp4"
        p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p",tmp],stdin=subprocess.PIPE)
        for k in range(n): p.stdin.write(frame(i,k/FPS,i==0).tobytes())
        p.stdin.close()
        if p.wait()==0: os.rename(tmp,name+".mp4")
