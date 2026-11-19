"""Mesopotamia cover picture: source -> 3840x1764, title MESOPOTAMIA centred BEHIND the figures (the king, his guard, the bow, the horses and the lion stay in front of the letters).
usage: python3 mk_mesopotamia_picture.py [SPAN] [Y]   (title width in px at 4K, default 3440; vertical centre of the letters, default 195: the letters sit above the figures, only the crown, the bow tip and the spear cut into them)"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from scipy import ndimage as ndi
import numpy as np, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); SPAN = int(sys.argv[1]) if len(sys.argv) > 1 else 3440; Y = int(sys.argv[2]) if len(sys.argv) > 2 else 195
src = Image.open(f"{HERE}/src/mesopotamia_picture_source.jpg").convert("RGB"); W, Hh = 3840, 1764
big = src.resize((W, round(src.height * W / src.width)), Image.LANCZOS); im = big.crop((0, big.height - Hh, W, big.height)).filter(ImageFilter.UnsharpMask(radius=2.2, percent=60, threshold=2))          # the extra rows go from the sky
a = np.asarray(im).astype(np.float32)
# foreground = everything that differs from the smooth sky: the sky is estimated by a wide median on a small copy, so thin things (bow string, arrow, spear) survive
sm = im.resize((W // 16, Hh // 16), Image.BILINEAR); bg = np.stack([ndi.median_filter(np.asarray(sm)[..., c], size=(7, 71)) for c in range(3)], 2)
bg = np.asarray(Image.fromarray(bg).resize((W, Hh), Image.BICUBIC).filter(ImageFilter.GaussianBlur(12))).astype(np.float32)
fg = np.abs(a - bg).max(2) > 26; fg = ndi.binary_closing(fg, iterations=2); lab, n = ndi.label(fg); sz = ndi.sum(fg, lab, range(1, n + 1)); fg = np.isin(lab, [i + 1 for i, v in enumerate(sz) if v > 900])
fgm = np.asarray(Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32) / 255
yy = np.linspace(0, 1, Hh)[:, None, None]; grad = np.clip(0.70 + 0.30 * (yy / 0.40), 0.70, 1.0)          # darker sky at the top: a white title reads over it
base = ImageEnhance.Contrast(Image.fromarray(np.clip(a * grad, 0, 255).astype(np.uint8))).enhance(1.05)
txt = os.environ.get("TITLE", "MESOPOTAMIA"); ov = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); do = ImageDraw.Draw(ov); size = 900
while True:
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", size); ws = [do.textlength(c, font=fnt) for c in txt]; sp = (SPAN - sum(ws)) / (len(txt) - 1)
    if sp >= size * 0.10: break
    size -= 4
x = (W - SPAN) / 2
for c, w in zip(txt, ws): do.text((x, Y), c, font=fnt, fill=(246, 244, 238, 232), anchor="lm"); x += w + sp
al = np.asarray(ov).astype(np.float32); al[..., 3] *= (1 - fgm); ov = Image.fromarray(al.astype(np.uint8), "RGBA")
bb = Image.fromarray((np.asarray(do._image)[..., 3] if False else np.asarray(ov)[..., 3])).getbbox(); print("size", size, "title ink", bb)
o = base.convert("RGBA"); o.alpha_composite(ov); o.convert("RGB").save(f"{HERE}/src/mesopotamia_picture.png")
