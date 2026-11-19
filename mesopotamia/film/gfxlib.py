# text and plaque helpers shared by all chapters (same look as the chapter cards)
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1920, 1080, 60
BG = (17, 17, 17); WHITE = (242, 240, 235); GRAY = (128, 132, 136); DIM = (70, 72, 75); ACC = (242, 194, 48)
FB = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"; FR = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
_f = {}
def font(b, s):
    k = (b, int(s))
    if k not in _f: _f[k] = ImageFont.truetype(FB if b else FR, int(s))
    return _f[k]
def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
def col(c, a): a = max(0.0, min(1.0, a)); return tuple(int(BG[i] + (c[i] - BG[i]) * a) for i in range(3))
def r(t, t0, d=0.35): return ease((t - t0) / d)
def win(t, a, b, fi=0.3, fo=0.3): return max(0.0, min(1.0, (t - a) / fi, (b - t) / fo))
def tw(d, s, f, sp=0): return sum(d.textlength(ch, font=f) + sp for ch in s) - sp
def text(d, x, y, s, size, a=1.0, bold=True, color=WHITE, anchor="m", sp=0, dy=0):
    if a <= 0: return
    f = font(bold, size); w = tw(d, s, f, sp)
    x0 = x - w / 2 if anchor == "m" else (x - w if anchor == "r" else x)
    y0 = y - size * 0.6 + (1 - a) * dy
    for ch in s:
        d.text((x0, y0), ch, font=f, fill=col(color, a)); x0 += d.textlength(ch, font=f) + sp
def plaque(d, x, y, s, size, a=1.0, sp=2, anchor="m"):
    if a <= 0: return
    f = font(True, size); w = tw(d, s, f, sp); px, py = size * 0.45, size * 0.32
    x0 = x - w / 2 if anchor == "m" else x
    d.rectangle([x0 - px, y - size * 0.6 - py, x0 + w + px, y + size * 0.6 + py], fill=col(WHITE, a))
    xx = x0
    for ch in s:
        d.text((xx, y - size * 0.6), ch, font=f, fill=col(BG, a) if a < 1 else BG); xx += d.textlength(ch, font=f) + sp
def strike(d, x, y, s, size, k, a=1.0, sp=0, color=WHITE):
    if k <= 0: return
    w = tw(d, s, font(True, size), sp); d.rectangle([x - w / 2 - 16, y - 4, x - w / 2 - 16 + (w + 32) * k, y + 4], fill=col(color, a))
def blank(): 
    im = Image.new("RGB", (W, H), BG); return im, ImageDraw.Draw(im)

# ---- museum cut-outs
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _src = {}; _rs = {}
def _load(n):
    if n not in _src:
        for p in (f"{_R}/cut/{n}.png", f"{_R}/../inserts/full/{n}.jpg", f"{_R}/../inserts/src/{n}.jpg", f"{_R}/../inserts/src/{n}.png"):
            if _os.path.exists(p): _src[n] = Image.open(p).convert("RGBA"); break
    return _src[n]
def obj(im, n, cx, cy, h=None, a=1.0, w=None, crop=None):
    if a <= 0: return
    k = (n, h, w, crop)
    if k not in _rs:
        s = _load(n)
        if crop: s = s.crop((int(crop[0] * s.width), int(crop[1] * s.height), int(crop[2] * s.width), int(crop[3] * s.height)))
        if h is None: h = int(s.height * w / s.width)
        ww = w if w else int(s.width * h / s.height)
        _rs[k] = s.resize((max(2, int(ww)), max(2, int(h))), Image.LANCZOS)
    o = _rs[k]
    if a < 1: o = o.copy(); o.putalpha(o.getchannel("A").point(lambda v: int(v * a)))
    im.paste(o, (int(cx - o.width / 2), int(cy - o.height / 2)), o)
_ph = {}
def photo(im, n, a=1.0, band=True):
    """full-frame photograph (cover crop), optional dark band at the bottom for a caption"""
    if a <= 0: return
    if n not in _ph:
        s = _load(n).convert("RGB"); k = max(W / s.width, H / s.height); s = s.resize((int(s.width * k) + 1, int(s.height * k) + 1), Image.LANCZOS)
        x = (s.width - W) // 2; y = (s.height - H) // 2; s = s.crop((x, y, x + W, y + H))
        if band:
            g = Image.linear_gradient("L").resize((W, 420)); m = Image.new("L", (W, H), 0); m.paste(g.point(lambda v: int(v * 0.9)), (0, H - 420))
            s = Image.composite(Image.new("RGB", (W, H), BG), s, m)
        _ph[n] = s
    im.paste(_ph[n] if a >= 1 else Image.blend(Image.new("RGB", (W, H), BG), _ph[n], a))
