# Обложки серии: единая шкала 3500 BC -> сегодня, жёлтым закрашен отрезок цивилизации.
from PIL import Image, ImageDraw, ImageFont
W,H,SS=1280,720,2
BAND=132; X0,X1=44,1236; Y0,Y1=-3500,2000   # годы: BC отрицательные
YEL=(242,194,48,255); WHITE=(244,242,236,255); GREY=(150,156,164,255); BLACK=(17,17,17,255)
B="/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"; R="/usr/share/fonts/opentype/inter/Inter-Medium.otf"
def F(p,s): return ImageFont.truetype(p,s*SS)
def X(y): return X0+(y-Y0)/(Y1-Y0)*(X1-X0)
def lab(y): return f"{-y} BC" if y<0 else f"AD {y}"
def overlay(big,small,a,b,span_label=None):
    im=Image.new("RGBA",(W*SS,H*SS),(0,0,0,0)); d=ImageDraw.Draw(im)
    s=lambda v:int(round(v*SS)); top=H-BAND
    d.rectangle([0,s(top),s(W),s(H)],fill=BLACK)
    d.rectangle([s(X0),s(top-1.5),s(X1),s(top+1.5)],fill=WHITE)
    for y in range(Y0,Y1+1,500):
        if min(abs(X(y)-X(a)),abs(X(y)-X(b)))<12: continue
        big_t=(y%1000==0); h=11 if big_t else 6
        d.rectangle([s(X(y)-1.5),s(top-h),s(X(y)+1.5),s(top+h)],fill=WHITE)
    xa,xb=X(a),X(b)
    d.rectangle([s(xa),s(top-5),s(xb),s(top+5)],fill=YEL)
    for x in (xa,xb): d.rectangle([s(x-2),s(top-14),s(x+2),s(top+14)],fill=YEL)
    f=F(R,19); ly=top+22
    def text(x,t,fill,anchor): d.text((s(x),s(ly)),t,font=f,fill=fill,anchor=anchor)
    if xb-xa<230:
        t=span_label or f"{lab(a).replace(' BC','')}–{lab(b)}"
        tw=d.textlength(t,font=f)/SS; cx=min(max((xa+xb)/2,X0+tw/2),X1-tw/2)
        text(cx,t,YEL,"mt"); occ=(cx-tw/2-20,cx+tw/2+20)
    else:
        text(xa,lab(a),YEL,"lt"); text(xb,lab(b),YEL,"rt"); occ=(xa-20,xb+20)
    for x,t,anc in ((X0,"3500 BC","lt"),(X1,"TODAY","rt")):
        tw=d.textlength(t,font=f)/SS; l,r=(x,x+tw) if anc=="lt" else (x-tw,x)
        if r<occ[0] or l>occ[1]: text(x,t,GREY,anc)
    fb=F(B,84); d.text((s(X0-4),s(H-6)),big,font=fb,fill=WHITE,anchor="ls")
    bw=d.textlength(big,font=fb)/SS
    d.text((s(X0+bw+28),s(H-17)),small,font=F(B,46),fill=YEL,anchor="ls")
    return im.resize((W,H),Image.LANCZOS)
SERIES=[("egypt","EGYPT",-3100,-30),("persia","PERSIA",-550,-330),("greece","GREECE",-800,-146),("rome","ROME",-753,476)]
if __name__=="__main__":
    outs={}
    for key,name,a,b in SERIES:
        o=overlay(name,"IN 20 MINUTES",a,b); outs[key]=o
        if key in("egypt","persia"): o.save(f"overlay_{key}_universal.png")
    # лист-проверка: 4 обложки на сером фоне, полный размер + мобильный
    sheet=Image.new("RGB",(1280*2+60,720*2+60+260),(40,42,46))
    for i,(key,*_ ) in enumerate(SERIES):
        bg=Image.new("RGBA",(W,H),(96,101,110,255)); bg.alpha_composite(outs[key])
        sheet.paste(bg.convert("RGB"),(20+(i%2)*1300,20+(i//2)*740))
        sm=bg.convert("RGB").resize((336,189),Image.LANCZOS); sheet.paste(sm,(20+i*356,1500+20))
    sheet.save("universal_check.png")
