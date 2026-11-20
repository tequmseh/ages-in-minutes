"""Aztecs cover picture: source -> 3840x1764, title AZTECS centred across the top like the other covers, in front of the picture
(the headdress fills the right 60 % of the upper frame: letters behind it would lose C and S, so they lie over the feathers; the face stays clear).
usage: SIZE=600 python3 mk_aztecs_picture.py 3360 250 238   (title width at 4K; vertical centre of the letters; opacity 0-255; SIZE = font size)"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); A = sys.argv[1:]; SPAN = int(A[0]) if A else 3440; Y = int(A[1]) if len(A) > 1 else 1400; AL = int(A[2]) if len(A) > 2 else 205
src = Image.open(f"{HERE}/src/aztecs_picture_source.jpg").convert("RGB"); W, Hh = 3840, 1764
big = src.resize((W, round(src.height * W / src.width)), Image.LANCZOS); im = big.crop((0, 0, W, Hh)).filter(ImageFilter.UnsharpMask(radius=2.2, percent=60, threshold=2))          # the extra rows go from the bottom: the headdress touches the top
a = np.asarray(im).astype(np.float32); yy = np.linspace(0, 1, Hh)[:, None, None]
grad = np.clip(0.72 + 0.28 * (yy / 0.36), 0.72, 1.0)          # darker sky at the top: the white title reads over the sunset
base = ImageEnhance.Contrast(Image.fromarray(np.clip(a * grad, 0, 255).astype(np.uint8))).enhance(1.05)
txt = os.environ.get("TITLE", "AZTECS"); ov = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); do = ImageDraw.Draw(ov); size = int(os.environ.get("SIZE", 900))
while True:
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", size); ws = [do.textlength(c, font=fnt) for c in txt]; sp = (SPAN - sum(ws)) / (len(txt) - 1)
    if sp >= size * 0.10: break
    size -= 4
x = (W - SPAN) / 2
for c, w in zip(txt, ws): do.text((x, Y), c, font=fnt, fill=(246, 244, 238, AL), anchor="lm"); x += w + sp
sh = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); sh.putalpha(ov.getchannel("A").filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.30)))
o = base.convert("RGBA"); o.alpha_composite(sh); o.alpha_composite(ov); o.convert("RGB").save(f"{HERE}/src/aztecs_picture.png"); print("size", size, "ink", ov.getchannel("A").getbbox())
