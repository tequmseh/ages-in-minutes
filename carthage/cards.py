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
Y0,YE=814,146
def xof(y): return X0+(Y0-y)/(Y0-YE)*(X1-X0)
TICKS=[814,650,480,306,264,241,237,218,216,201,146]
CH=[("CHAPTER 1","THE PURPLE PEOPLE",None,814),
    ("CHAPTER 2","NEW CITY",814,650),
    ("CHAPTER 3","THE TRADING EMPIRE",650,480),
    ("CHAPTER 4","THE SICILIAN WARS",480,306),
    ("CHAPTER 5","HOW IT WORKED",306,264),
    ("CHAPTER 6","THE FIRST WAR WITH ROME",264,241),
    ("CHAPTER 7","THE TRUCELESS WAR",241,237),
    ("CHAPTER 8","THE BARCAS IN SPAIN",237,218),
    ("CHAPTER 9","HANNIBAL",218,216),
    ("CHAPTER 10","THE LONG DEFEAT",216,201),
    ("CHAPTER 11","CARTHAGE MUST BE DESTROYED",201,146),
    ("CHAPTER 12","WHAT REMAINS",146,None)]
SLUG=["the_purple_people","new_city","the_trading_empire","the_sicilian_wars","how_it_worked","the_first_war_with_rome","the_truceless_war","the_barcas_in_spain","hannibal","the_long_defeat","carthage_must_be_destroyed","what_remains"]
CH=[(l,t,a,b,("BEFORE 814 BC" if a is None else (f"{a}–{b} BC" if b else "146 BC → TODAY"))) for l,t,a,b in CH]
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
        name=f"out/carthage_chapter_{i+1:02d}_{SLUG[i]}"; tmp=name+".tmp.mp4"
        p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p",tmp],stdin=subprocess.PIPE)
        for k in range(n): p.stdin.write(frame(i,k/FPS,i==0).tobytes())
        p.stdin.close()
        if p.wait()==0: os.rename(tmp,name+".mp4")
