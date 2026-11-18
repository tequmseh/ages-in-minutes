"""Rome cover picture: source -> 3840x1764 (cover crop, bottom cut), darker top, title ROME centred with the eagle standard in front of the letters.
usage: python3 mk_rome_picture.py [SPAN] [Y]   (title width in px at 4K, default 3300; vertical centre of the letters, default 400)"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); SPAN = int(sys.argv[1]) if len(sys.argv) > 1 else 3300; Y = int(sys.argv[2]) if len(sys.argv) > 2 else 400
src = Image.open(f"{HERE}/src/rome_picture_source.jpg").convert("RGB")
W, Hh = 3840, 1764; k = W / src.width; im = src.resize((W, round(src.height * k)), Image.LANCZOS).crop((0, 0, W, Hh))          # keep the top: the eagle's wing tips; the soldiers at the bottom edge go
im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=60, threshold=2))
a = np.asarray(im).astype(np.float32)
yy = np.linspace(0, 1, Hh)[:, None, None]; grad = np.clip(0.62 + 0.38 * (yy / 0.42), 0.62, 1.0)          # darker sky at the top: a white title reads over it
base = ImageEnhance.Contrast(Image.fromarray(np.clip(a * grad, 0, 255).astype(np.uint8))).enhance(1.05)
txt = "ROME"; ov = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); do = ImageDraw.Draw(ov); size = 900
while True:
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", size); ws = [do.textlength(c, font=fnt) for c in txt]; sp = (SPAN - sum(ws)) / (len(txt) - 1)
    if sp >= size * 0.16: break
    size -= 4
x = (W - SPAN) / 2
for c, w in zip(txt, ws): do.text((x, Y), c, font=fnt, fill=(246, 244, 238, 225), anchor="lm"); x += w + sp
# the eagle and its pole stay in front of the letters: warm gold and dark bronze pixels against the blue sky, right part of the frame only
R, G, B = a[..., 0], a[..., 1], a[..., 2]; lum = a.mean(axis=2)
pm = np.zeros((Hh, W), np.float32); bx = slice(int(790 * k), W); by = slice(0, int(470 * k))
pm[by, bx] = (((R[by, bx] - B[by, bx]) > 34) | (lum[by, bx] < 70)).astype(np.float32)
pmi = Image.fromarray((pm * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(9)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2))
lab_ = np.asarray(pmi) > 128
from scipy import ndimage as ndi
lab, n = ndi.label(lab_); sz = ndi.sum(lab_, lab, range(1, n + 1)); keep = np.isin(lab, [i + 1 for i, v in enumerate(sz) if v > 0.02 * sz.max()]); pmf = np.asarray(pmi).astype(np.float32) / 255 * keep
xs = np.cumsum([0] + [w + sp for w in ws]); xe = (W - SPAN) / 2 + xs[3] - sp * 0.45          # the last letter stays whole: it lies over the right wing, the eagle covers only the M
ramp = np.clip((xe - np.arange(W)) / 60.0, 0, 1)[None, :]; pmf = pmf * ramp
sh = Image.new("L", (W, Hh), 0); dsh = ImageDraw.Draw(sh); dsh.text(((W - SPAN) / 2 + xs[3], Y + 6), txt[3], font=fnt, fill=150, anchor="lm"); sh = sh.filter(ImageFilter.GaussianBlur(22))          # soft shade under the E so it reads on the gold wing
base = Image.composite(Image.new("RGB", (W, Hh), (20, 16, 10)), base, sh.point(lambda v: int(v * 0.75)))
al = np.asarray(ov).astype(np.float32); al[..., 3] *= (1 - pmf); ov = Image.fromarray(al.astype(np.uint8), "RGBA")
bb = Image.fromarray(np.asarray(ov)[..., 3]).getbbox(); print("size", size, "title ink", bb, "margins", bb[0], W - bb[2])
o = base.convert("RGBA"); o.alpha_composite(ov); o.convert("RGB").save(f"{HERE}/src/rome_picture.png")
