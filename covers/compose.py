"""Cover = picture above the band + timeline overlay + slogan in the band + channel logo.
usage: python3 compose.py PICTURE overlay_NAME.png OUT.jpg "220 |YEARS, |3,000 |MILES"   (parts split by |, odd parts yellow: start with | to begin white)"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys, os
K = 2 if os.environ.get("COVER_4K") else 1          # COVER_4K=1: 3840x2160, picture area 3840x1764
W, H = 1920 * K, 1080 * K; LINE = 882 * K; YEL = (242, 194, 48); WHITE = (244, 242, 236)
HERE = os.path.dirname(os.path.abspath(__file__)); FB = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
pic, ov, out, slogan = sys.argv[1:5]; logo_h = (int(sys.argv[5]) if len(sys.argv) > 5 else 0) * K          # no logo on covers by default (Rustam, 20 Nov: "опять лого"); pass a height to add one
im = Image.new("RGB", (W, H), (17, 17, 17)); p = Image.open(pic).convert("RGB")
k = max(W / p.width, (LINE + 2 * K) / p.height); p = p.resize((round(p.width * k), round(p.height * k)), Image.LANCZOS)
im.paste(p.crop(((p.width - W) // 2, 0, (p.width - W) // 2 + W, LINE + 2 * K)), (0, 0))
im.paste(Image.open(f"{HERE}/{ov}").convert("RGBA"), (0, 0), Image.open(f"{HERE}/{ov}").convert("RGBA"))
d = ImageDraw.Draw(im); parts = slogan.split("|"); txt = "".join(parts); X0, X1 = 66 * K, 1854 * K
def width(f, sp): return sum(d.textlength(c, font=f) + sp for c in txt) - sp
size = 150 * K
while True:
    f = ImageFont.truetype(FB, size); sp = size * 0.07
    if width(f, sp) <= X1 - X0 and size <= 128 * K: break
    size -= 1
x = (W - width(f, sp)) / 2; y = (LINE + 14 * K + H) / 2
for i, part in enumerate(parts):
    for c in part:
        d.text((x, y), c, font=f, fill=YEL if i % 2 == 0 else WHITE, anchor="lm"); x += d.textlength(c, font=f) + sp
if logo_h == 0: im.save(f"{HERE}/out/{out}", quality=95); print(out, size, "no logo"); sys.exit()
lg = Image.open(f"{HERE}/../channel/logo_mark_transparent.png").convert("RGBA"); lg = lg.resize((round(lg.width * logo_h / lg.height), logo_h), Image.LANCZOS)
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([40 - 14, 40 - 14, 40 + lg.width + 14, 40 + logo_h + 14], fill=(17, 17, 17, 215))
im.paste(sh.filter(ImageFilter.GaussianBlur(10)), (0, 0), sh.filter(ImageFilter.GaussianBlur(10))); im.paste(lg, (40, 40), lg)
im.save(f"{HERE}/out/{out}", quality=95); print(out, size)
