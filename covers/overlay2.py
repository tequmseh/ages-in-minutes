# Обложки серии, v2: подписи дат НАД шкалой. mode "A": плашка выше, шкала внутри; "B": шкала на кромке, даты на чёрных плашках
from PIL import Image, ImageDraw, ImageFont
import sys
W,H,SS=1280,720,2
X0,X1=44,1236; Y0,Y1=-3500,2000
YEL=(242,194,48,255); WHITE=(244,242,236,255); GREY=(150,156,164,255); BLACK=(17,17,17,255)
B="/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"; R="/usr/share/fonts/opentype/inter/Inter-Medium.otf"
def F(p,s): return ImageFont.truetype(p,s*SS)
def X(y): return X0+(y-Y0)/(Y1-Y0)*(X1-X0)
def lab(y): return f"{-y} BC" if y<0 else f"AD {y}"
def overlay(big,small,a,b,mode="A"):
    im=Image.new("RGBA",(W*SS,H*SS),(0,0,0,0)); d=ImageDraw.Draw(im)
    s=lambda v:int(round(v*SS))
    if mode=="A": top=H-166; line=top+56
    else: top=H-132; line=top
    d.rectangle([0,s(top),s(W),s(H)],fill=BLACK)
    d.rectangle([s(X0),s(line-1.5),s(X1),s(line+1.5)],fill=WHITE)
    for y in range(Y0,Y1+1,500):
        if min(abs(X(y)-X(a)),abs(X(y)-X(b)))<12: continue
        h=11 if y%1000==0 else 6
        d.rectangle([s(X(y)-1.5),s(line-h),s(X(y)+1.5),s(line+h)],fill=WHITE)
    xa,xb=X(a),X(b)
    d.rectangle([s(xa),s(line-5),s(xb),s(line+5)],fill=YEL)
    for x in (xa,xb): d.rectangle([s(x-2),s(line-14),s(x+2),s(line+14)],fill=YEL)
    f=F(R,19); ly=line-24   # низ текста
    def text(x,t,fill,anchor):
        tw=d.textlength(t,font=f)/SS
        l={"l":x,"r":x-tw,"m":x-tw/2}[anchor[0]]
        if mode=="B": d.rectangle([s(l-8),s(ly-24),s(l+tw+8),s(ly+6)],fill=BLACK)
        d.text((s(l),s(ly)),t,font=f,fill=fill,anchor="ls")
    if xb-xa<230:
        t=f"{lab(a).replace(' BC','')}–{lab(b)}"
        tw=d.textlength(t,font=f)/SS; cx=min(max((xa+xb)/2,X0+tw/2),X1-tw/2)
        text(cx,t,YEL,"m"); occ=(cx-tw/2-24,cx+tw/2+24)
    else:
        text(xa,lab(a),YEL,"l"); text(xb,lab(b),YEL,"r"); occ=(xa-24,xb+24)
    for x,t,anc in ((X0,"3500 BC","l"),(X1,"TODAY","r")):
        tw=d.textlength(t,font=f)/SS; l,r=(x,x+tw) if anc=="l" else (x-tw,x)
        if r<occ[0] or l>occ[1]: text(x,t,GREY,anc)
    fb=F(B,84); d.text((s(X0-4),s(H-6)),big,font=fb,fill=WHITE,anchor="ls")
    bw=d.textlength(big,font=fb)/SS
    d.text((s(X0+bw+28),s(H-17)),small,font=F(B,46),fill=YEL,anchor="ls")
    return im.resize((W,H),Image.LANCZOS)
SERIES=[("egypt","EGYPT",-3100,-30),("persia","PERSIA",-550,-330),("greece","GREECE",-800,-146),("rome","ROME",-753,476)]
if __name__=="__main__":
    if sys.argv[1]=="test":
        sheet=Image.new("RGB",(1280*2+60,720*2+60),(40,42,46))
        for j,m in enumerate("AB"):
            for i,k in enumerate((0,1)):
                key,name,a,b=SERIES[k]
                bg=Image.new("RGBA",(W,H),(214,205,180,255)); bg.alpha_composite(overlay(name,"IN 20 MINUTES",a,b,m))
                sheet.paste(bg.convert("RGB"),(20+i*1300,20+j*740))
        sheet.save("v2_test.png")
    else:
        m=sys.argv[1]
        sheet=Image.new("RGB",(1280*2+60,720*2+60+260),(40,42,46))
        for i,(key,name,a,b) in enumerate(SERIES):
            o=overlay(name,"IN 20 MINUTES",a,b,m)
            if key in("egypt","persia"): o.save(f"overlay_{key}_v2.png")
            bg=Image.new("RGBA",(W,H),(214,205,180,255)); bg.alpha_composite(o)
            sheet.paste(bg.convert("RGB"),(20+(i%2)*1300,20+(i//2)*740))
            sheet.paste(bg.convert("RGB").resize((336,189),Image.LANCZOS),(20+i*356,1520))
        sheet.save("v2_check.png")
