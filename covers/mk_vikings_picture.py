"""Vikings cover picture: source -> 3840x1764, prow sheen tamed, darker top, title VIKINGS centred with the prow in front of the letters.
usage: python3 mk_vikings_picture.py [SPAN]   (title width in px at 4K, default 3360)"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); SPAN = int(sys.argv[1]) if len(sys.argv) > 1 else 3360
src = Image.open(f"{HERE}/src/vikings_picture_source.jpg").convert("RGB")
W, Hh = 3840, 1764; k = Hh / src.height; im = src.resize((round(src.width * k), Hh), Image.LANCZOS); x0 = (im.width - W) // 2; im = im.crop((x0, 0, x0 + W, Hh))
im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=2))
a = np.asarray(im).astype(np.float32); f = lambda x, y: ((x * k - x0), (y * k))
m = Image.new("L", (W, Hh), 0); d = ImageDraw.Draw(m)
d.polygon([f(900, 560), f(925, 330), f(960, 200), f(915, 150), f(925, 70), f(1000, 55), f(1050, 120), f(1040, 330), f(1010, 470), f(1130, 650), f(1330, 800), f(1600, 830), f(1600, 900), f(1250, 960), f(1020, 1010), f(930, 850)], fill=255)
m = np.asarray(m.filter(ImageFilter.GaussianBlur(40))).astype(np.float32)[..., None] / 255
g = a.mean(axis=2, keepdims=True); warm = np.clip((a[..., 0:1] - a[..., 2:3]) / 90, 0, 1)
t = m * warm * 0.42; a = a * (1 - t) + (g * 0.5 + a * 0.5 * 0.9) * t          # brassy sheen on the prow -> wet wood
clean = np.clip(a, 0, 255)
yy = np.linspace(0, 1, Hh)[:, None, None]; grad = np.clip(0.50 + 0.50 * (yy / 0.46), 0.50, 1.0)          # darker sky at the top: a white title reads over pale fog and sail
base = ImageEnhance.Contrast(Image.fromarray((clean * grad).astype(np.uint8))).enhance(1.06)
txt = "VIKINGS"; size = 556; ov = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); do = ImageDraw.Draw(ov)
fnt = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", size); ws = [do.textlength(c, font=fnt) for c in txt]; sp = (SPAN - sum(ws)) / (len(txt) - 1)
x = (W - SPAN) / 2; y = 330
for c, w in zip(txt, ws): do.text((x, y), c, font=fnt, fill=(246, 244, 238, 212), anchor="lm"); x += w + sp
lum = clean.mean(axis=2); sat = clean.max(axis=2) - clean.min(axis=2)
pm = np.zeros((Hh, W), np.float32); bx = slice(int(f(880, 0)[0]), int(f(1080, 0)[0])); by = slice(0, 640)
pm[by, bx] = ((lum[by, bx] < 132) | ((sat[by, bx] > 38) & (lum[by, bx] < 185))).astype(np.float32)          # dark or brown pixels = the stem and its spiral
pmi = Image.fromarray((pm * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2))
al = np.asarray(ov).astype(np.float32); al[..., 3] *= (1 - np.asarray(pmi).astype(np.float32) / 255); ov = Image.fromarray(al.astype(np.uint8), "RGBA")
bb = Image.fromarray(np.asarray(ov)[..., 3]).getbbox(); print("title ink", bb[0], bb[2], "margins", bb[0], W - bb[2])
o = base.convert("RGBA"); o.alpha_composite(ov); o.convert("RGB").save(f"{HERE}/src/vikings_picture.png")
