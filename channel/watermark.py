# Логотип-значок для видео (YouTube Studio -> Брендинг -> «Логотип канала»): квадрат >=150 px, <1 МБ.
from PIL import Image, ImageDraw
import math
YEL=(242,194,48,255); WHITE=(244,242,236,255); BLACK=(17,17,17,255)
def pt(c,r,deg):
    a=math.radians(deg-90); return (c+r*math.cos(a), c+r*math.sin(a))
def mark(size=600, disc=True, bold=True):
    k=4*size/800; N=int(800*k); c=N/2
    im=Image.new("RGBA",(N,N),(0,0,0,0)); d=ImageDraw.Draw(im)
    if disc: d.ellipse([0,0,N-1,N-1],fill=BLACK)
    R=(268 if bold else 262)*k; tw=(34 if bold else 24)*k
    d.pieslice([c-R,c-R,c+R,c+R],-90,30,fill=YEL)
    for i in range(12):
        deg=i*30; col=YEL if deg<=120 else WHITE
        a=pt(c,(304 if bold else 300)*k,deg); b=pt(c,(352 if i%3==0 else 340)*k,deg)
        d.line([a,b],fill=col,width=int(tw))
        for p in (a,b): d.ellipse([p[0]-tw/2,p[1]-tw/2,p[0]+tw/2,p[1]+tw/2],fill=col)
    return im.resize((size,size),Image.LANCZOS)
if __name__=="__main__":
    badge=mark(600,True); badge.save("watermark_badge.png")
    plain=mark(600,False); plain.save("logo_mark_transparent.png")
    # проверка: на светлой карте и на чёрной заставке, примерный размер и место значка YouTube
    base="/tmp/claude-0/-home-claude/6766839a-4a89-5481-9872-a3381d71ea5c/scratchpad/"
    a=Image.open(base+"maps/out/base_map_full.png").convert("RGBA").resize((960,540),Image.LANCZOS)
    b=Image.open(base+"cards/test_1.png").convert("RGBA").resize((960,540),Image.LANCZOS)
    sheet=Image.new("RGB",(960*2+60,540*2+60),(40,42,46))
    for row,wm in enumerate((badge,plain)):
        for col,fr in enumerate((a,b)):
            f=fr.copy(); w=wm.resize((46,46),Image.LANCZOS)
            f.alpha_composite(w,(960-46-14,540-46-58))
            sheet.paste(f.convert("RGB"),(20+col*980,20+row*560))
    sheet.save("watermark_check.png")
    sheet.crop((20+980+700,20+330,20+980+960,20+540)).resize((780,630),Image.LANCZOS).save("watermark_zoom.png")
