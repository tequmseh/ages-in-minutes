# Шапка канала Ages in Minutes: 2560x1440, единая шкала 3500 BC -> сегодня в безопасной зоне 1546x423.
from PIL import Image, ImageDraw, ImageFont
import sys
W,H,SS=2560,1440,2
SAFE=(507,508,2053,931)                      # зона, видимая на всех устройствах
X0,X1=527,2033; Y0,Y1=-3500,2000             # шкала внутри безопасной зоны
YEL=(242,194,48); WHITE=(244,242,236); GREY=(150,156,164); BLACK=(17,17,17)
B="/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"; R="/usr/share/fonts/opentype/inter/Inter-Medium.otf"
def F(p,s): return ImageFont.truetype(p,int(s*SS))
def X(y): return X0+(y-Y0)/(Y1-Y0)*(X1-X0)
# год, подпись даты, подпись события (2 строки), объект для слота (рус., только в схеме)
MARKS=[(-3200,"3200 BC",("Writing","begins"),"глиняная табличка"),
       (-2560,"2560 BC",("Great","Pyramid"),"пирамида"),
       (-1754,"1754 BC",("Hammurabi's","laws"),"стела Хаммурапи"),
       (-1200,"1200 BC",("Bronze Age","collapse"),"бронзовый меч"),
       (-550,"550 BC",("Persian","Empire"),"золотой дарик"),
       (-27,"27 BC",("Roman","Empire"),"бюст Августа"),
       (537,"AD 537",("Hagia","Sophia"),"золотой солид"),
       (1206,"AD 1206",("Mongol","Empire"),"монгольский шлем")]
def banner(objects=True, guide=False):
    im=Image.new("RGB",(W*SS,H*SS),BLACK); d=ImageDraw.Draw(im,"RGBA")
    s=lambda v:int(round(v*SS))
    if objects: line=752; dsize=34; csize=20; obj_bottom=716; obj_h=170
    else:       line=664; dsize=35; csize=21
    def seg(xa,xb,y,h,col,a=255): d.rectangle([s(xa),s(y-h/2),s(xb),s(y+h/2)],fill=col+(a,))
    # линия: в безопасной зоне сплошная, слева уходит в прошлое с засечками, справа пунктир в будущее
    step=8
    for x in range(0,X0,step): seg(x,x+step,line,3,WHITE,int(40+215*(x/X0)))
    seg(X0,X1,line,3,WHITE)
    for x in range(X1,W,26):
        a=int(255*(1-(x-X1)/(W-X1))*0.9)
        seg(x,min(x+13,W),line,3,WHITE,max(a,0))
    pxy=(X1-X0)/(Y1-Y0)
    y=Y0
    while X(y)>0:                                   # засечки каждые 500 лет, включая «до шкалы»
        x=X(y); big=(y%1000==0); h=22 if big else 12
        a=255 if x>=X0 else int(40+215*(x/X0))
        d.rectangle([s(x-1.5),s(line-h/2),s(x+1.5),s(line+h/2)],fill=WHITE+(a,))
        y-=500
    for y in range(Y0+500,Y1,500):
        x=X(y); h=22 if y%1000==0 else 12
        if min(abs(x-X(m[0])) for m in MARKS)<20: continue
        d.rectangle([s(x-1.5),s(line-h/2),s(x+1.5),s(line+h/2)],fill=WHITE+(255,))
    fd=F(B,dsize); fc=F(R,csize)
    boxes=[]
    for yr,lab,cap,obj in MARKS:
        x=X(yr)
        d.rectangle([s(x-2.5),s(line-17),s(x+2.5),s(line+17)],fill=YEL+(255,))
        d.ellipse([s(x-8),s(line-8),s(x+8),s(line+8)],fill=YEL+(255,))
        ty=line+34
        d.text((s(x),s(ty)),lab,font=fd,fill=YEL+(255,),anchor="mt")
        tw=d.textlength(lab,font=fd)/SS; boxes.append((x-tw/2,x+tw/2,lab))
        for i,c in enumerate(cap):
            d.text((s(x),s(ty+dsize+12+i*(csize+6))),c,font=fc,fill=GREY+(255,),anchor="mt")
        if objects and guide:
            d.rounded_rectangle([s(x-62),s(obj_bottom-obj_h),s(x+62),s(obj_bottom)],radius=s(10),outline=(120,126,134,255),width=s(2))
            fo=F(R,15); words=obj.split(" ")
            for i,wd in enumerate(words):
                d.text((s(x),s(obj_bottom-obj_h/2-10*len(words)+i*20)),wd,font=fo,fill=(170,176,184,255),anchor="mt")
    # «TODAY» на правом конце шкалы
    d.rectangle([s(X1-1.5),s(line-17),s(X1+1.5),s(line+17)],fill=WHITE+(255,))
    d.text((s(X1+2),s(line+34)),"TODAY",font=fd,fill=WHITE+(255,),anchor="rt")
    tw=d.textlength("TODAY",font=fd)/SS; boxes.append((X1-tw,X1,"TODAY"))
    boxes.sort()
    for a,b in zip(boxes,boxes[1:]):
        gap=b[0]-a[1]
        if gap<12: print("TIGHT",objects,a[2],b[2],round(gap,1))
    if guide:
        for gi,(w,col,name) in enumerate(((1546,(242,194,48,255),"телефон 1546x423"),(1855,(120,170,255,255),"планшет 1855x423"),(2560,(120,220,150,255),"компьютер 2560x423"))):
            xa=(W-w)/2; d.rectangle([s(xa+1),s(508),s(xa+w-1),s(931)],outline=col,width=s(2))
            d.text((s(517),s(931+10+gi*30)),name,font=F(R,20),fill=col,anchor="lt")
        d.text((s(40),s(40)),"Весь кадр 2560x1440 виден только на телевизоре",font=F(R,24),fill=(170,176,184,255))
    return im.resize((W,H),Image.LANCZOS)
if __name__=="__main__":
    banner(True,True).save("banner_guide.png")
    banner(True,False).save("banner_base_for_objects.png")
    banner(False,False).save("banner_text_only.png")
    # проверочные кадры: полоса компьютера и телефон
    for name in ("banner_text_only","banner_base_for_objects","banner_guide"):
        im=Image.open(name+".png")
        im.crop((0,508,2560,931)).save(f"chk_{name}_desktop.png")
        im.crop((507,508,2053,931)).resize((430,118),Image.LANCZOS).save(f"chk_{name}_mobile.png")
