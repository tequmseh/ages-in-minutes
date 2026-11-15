import sys, subprocess, os
from PIL import Image, ImageDraw, ImageFont
W, H, FPS, DUR = 1920, 1080, 30, 51.984
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
    """white plate, black text"""
    if a <= 0: return
    f = font(True, size); w = tw(d, s, f, sp); px, py = size * 0.45, size * 0.32
    x0 = x - w / 2 if anchor == "m" else x
    d.rectangle([x0 - px, y - size * 0.6 - py, x0 + w + px, y + size * 0.6 + py], fill=col(WHITE, a))
    xx = x0
    for ch in s:
        d.text((xx, y - size * 0.6), ch, font=f, fill=col(BG, a) if a < 1 else BG); xx += d.textlength(ch, font=f) + sp
LOGO = Image.open("../../channel/logo_mark_transparent.png").convert("RGBA")


import numpy as np, math
OBJ = {}
def load(n, crop_bottom=0.0):
    im = Image.open(f"cut/{n}.png").convert("RGBA")
    if crop_bottom: im = im.crop((0, 0, im.width, int(im.height * (1 - crop_bottom))))
    OBJ[n] = im
for n, cb in (("scroll2", 0), ("stele", 0), ("aristotle", 0.16), ("papyrus", 0), ("roll", 0), ("coin", 0), ("hannibal", 0.09), ("greek", 0), ("roman", 0)): load(n, cb)
def obj(im, n, cx, cy, h, a, z=1.0):
    """cut-out on black, centred, with a slow zoom z"""
    if a <= 0: return
    src = OBJ[n]; hh = max(2, int(h * z)); ww = max(2, int(src.width * hh / src.height))
    o = src.resize((ww, hh), Image.LANCZOS)
    if a < 1: o.putalpha(o.getchannel("A").point(lambda v: int(v * a)))
    im.paste(o, (int(cx - ww / 2), int(cy - hh / 2)), o)
def zoom(t, t0, t1, k=0.05): return 1 + k * max(0.0, min(1.0, (t - t0) / (t1 - t0)))

# ---- salt: a few thousand grains that pour into a heap and then scatter
_rng = np.random.default_rng(7); NG = 2800; SX, SY = 960, 900
gx = _rng.normal(0, 200, NG); hmax = 170 * np.exp(-(gx / 210) ** 2 / 2)
gy = -(_rng.random(NG) ** 1.6) * hmax
stray = _rng.random(NG) < 0.07; gx[stray] = _rng.normal(0, 420, stray.sum()); gy[stray] = _rng.random(stray.sum()) * 6
gsz = _rng.uniform(2.2, 6.5, NG); gbr = _rng.uniform(150, 250, NG); gang = _rng.uniform(0, math.pi, NG); gu = _rng.random(NG)
order = np.argsort(-gy + _rng.normal(0, 25, NG))                     # lower grains land first
rank = np.empty(NG); rank[order] = np.arange(NG) / NG
gt0 = 23.45 + 3.1 * rank + _rng.uniform(0, 0.25, NG)
gvx = np.sign(gx + 1e-6) * _rng.uniform(60, 420, NG) + _rng.normal(0, 60, NG); gvy = -_rng.uniform(40, 360, NG)
draw_order = np.argsort(gy)
T_SCAT = 28.3
def salt(d, t, a):
    if a <= 0 or t < 23.4: return
    for i in draw_order:
        tau = t - gt0[i]
        if tau < 0: continue
        fall = min(1.0, tau / 0.5); x = SX + gx[i]; y = SY + gy[i] - 470 * (1 - fall * fall); al = a
        ts = t - (T_SCAT + 0.5 * gu[i])
        if ts > 0:
            al = a * max(0.0, 1 - ts / 1.15)
            if al <= 0: continue
            x += gvx[i] * ts; y += gvy[i] * ts + 120 * ts * ts
        sz = gsz[i]; c = math.cos(gang[i]); sn = math.sin(gang[i]); br = gbr[i]
        pts = [(x + sz * c, y + sz * sn * 0.7), (x - sz * sn * 0.8, y + sz * c * 0.6), (x - sz * c * 0.9, y - sz * sn * 0.7), (x + sz * sn, y - sz * c * 0.8)]
        d.polygon(pts, fill=col((br, br, min(255, br + 6)), al))

def frame(t):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im); cx = W // 2
    # 1. the thesis, over the charred scroll
    a = win(t, 0.1, 4.45)
    if a > 0:
        obj(im, "stele", cx, 305, 470, a * r(t, 0.1, 0.5), zoom(t, 0, 4.5))
        text(d, cx, 650, "ALMOST EVERYTHING YOU KNOW ABOUT CARTHAGE", 56, a * r(t, 0.3), sp=3, dy=14)
        f = font(True, 56); w1 = tw(d, "WAS WRITTEN BY THE PEOPLE WHO", f, 3); w2 = tw(d, "DESTROYED IT", f, 3); gap = 56
        x0 = cx - (w1 + gap + w2) / 2
        text(d, x0, 770, "WAS WRITTEN BY THE PEOPLE WHO", 56, a * r(t, 2.2), sp=3, anchor="l", dy=14)
        plaque(d, x0 + w1 + gap, 770, "DESTROYED IT", 56, a * r(t, 3.2), sp=3, anchor="l")
    # 2. the promise
    a = win(t, 4.8, 7.75)
    if a > 0:
        lg = LOGO.resize((230, 230), Image.LANCZOS)
        if a < 1: lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        im.paste(lg, (cx - 600, 425), lg)
        text(d, cx - 320, 500, "IN THE NEXT 20 MINUTES", 84, a * r(t, 4.9), anchor="l", sp=2, dy=14)
        text(d, cx - 316, 600, "WHAT THEY LEFT OUT", 40, a * r(t, 6.3), anchor="l", sp=6, color=GRAY, bold=False, dy=10)
    # 3. three things, with Aristotle and the one book
    a = win(t, 7.95, 16.75)
    if a > 0:
        text(d, 170, 300, "WHAT THEY LEFT OUT", 28, a, anchor="l", sp=8, color=GRAY, bold=False)
        rows = [(8.15, "A CONSTITUTION ARISTOTLE ADMIRED"), (10.65, "A WAR ROME VERY NEARLY LOST"), (13.1, "THE ONE BOOK ROME SAVED FROM THE FIRE")]
        for i, (t0, s) in enumerate(rows):
            ra = r(t, t0); y = 440 + i * 150
            later = [tt for tt, _ in rows if tt > t0 and t >= tt + 0.2]
            dim = 0.78 if later else 1.0
            text(d, 170, y, f"0{i + 1}", 46, a * ra * dim, anchor="l", color=GRAY, dy=14)
            text(d, 270, y, s, 46, a * ra * dim, anchor="l", sp=2, dy=14)
            if ra > 0: d.line([(170, y + 58), (170 + 1090 * ra, y + 58)], fill=col(DIM, a), width=2)
        if t < 11.0: obj(im, "aristotle", 1570, 560, 600, a * r(t, 8.15, 0.5) * (1 - r(t, 10.45, 0.3)), zoom(t, 8.1, 11.0))
        elif t >= 13.0: obj(im, "roll", 1610, 580, 280, a * r(t, 13.1, 0.5), zoom(t, 13.0, 16.8))
    # 4. what everyone knows
    a = win(t, 17.1, 23.3)
    if a > 0:
        dimo = 1 - 0.55 * r(t, 22.2)
        text(d, cx, 150, "WHAT EVERYONE KNOWS", 34, a * r(t, 17.2), sp=10, color=GRAY, bold=False)
        obj(im, "coin", 560, 470, 430, a * r(t, 19.3, 0.4) * dimo, zoom(t, 19.3, 23.3))
        text(d, 560, 770, "ELEPHANTS", 70, a * r(t, 19.4) * dimo, sp=4, dy=14)
        obj(im, "hannibal", 1360, 450, 520, a * r(t, 21.0, 0.4) * dimo, zoom(t, 21.0, 23.3))
        text(d, 1360, 770, "HANNIBAL", 70, a * r(t, 21.1) * dimo, sp=4, dy=14)
        plaque(d, cx, 920, "IT LOST", 70, a * r(t, 22.2, 0.25), sp=6)
    # 5. the salt
    a = win(t, 23.2, 33.95)
    if a > 0:
        y = 250
        text(d, cx, y, "ROME SALTED THE EARTH", 96, a * r(t, 23.4), sp=3, dy=18)
        f = font(True, 96); w = tw(d, "ROME SALTED THE EARTH", f, 3)
        k = ease((t - 28.15) / 0.6)
        if k > 0: d.rectangle([cx - w / 2 - 20, y - 5, cx - w / 2 - 20 + (w + 40) * k, y + 5], fill=col(WHITE, a))
        salt(d, t, a)
        plaque(d, cx, y + 150, "NEVER HAPPENED", 60, a * r(t, 28.5), sp=4)
        text(d, cx, y + 290, "NO ANCIENT WRITER MENTIONS IT", 44, a * r(t, 29.75), sp=5, color=GRAY, bold=False, dy=10)
        ta = a * r(t, 31.5)
        if ta > 0:
            X0, X1, Y = 260, 1660, 800; xs = X0 + (X1 - X0) * (1850 + 146) / (2026 + 146)
            d.line([(X0, Y), (X1, Y)], fill=col(DIM, ta), width=3)
            g = ease((t - 31.75) / 1.5)
            if g > 0: d.rectangle([X0, Y - 6, X0 + (xs - X0) * g, Y + 6], fill=col(ACC, ta))
            for x in (X0, xs, X1): d.line([(x, Y - 14), (x, Y + 14)], fill=col(GRAY, ta), width=2)
            text(d, X0, Y - 44, "146 BC", 30, ta, anchor="l"); text(d, X0, Y + 44, "CARTHAGE DESTROYED", 22, ta, anchor="l", color=GRAY, bold=False, sp=2)
            text(d, xs, Y - 44, "19TH CENTURY", 30, ta * r(t, 32.7), anchor="r"); text(d, xs, Y + 44, "THE STORY APPEARS", 22, ta * r(t, 32.7), anchor="r", color=GRAY, bold=False, sp=2)
            text(d, X1, Y - 40, "TODAY", 22, ta, anchor="r", color=GRAY, bold=False, sp=2)
    # 6. the trouble
    a = win(t, 34.2, 37.0, fo=0.01)
    if a > 0:
        text(d, cx, 500, "THE TROUBLE WITH CARTHAGE", 96, a * r(t, 34.3), sp=3, dy=18)
    # 7. who wrote it: two helmets
    a = win(t, 44.0, 48.35, fi=0.01)
    if a > 0:
        text(d, cx, 110, "NEARLY EVERY SENTENCE WE HAVE COMES FROM", 32, a * r(t, 44.05), sp=8, color=GRAY, bold=False)
        obj(im, "greek", 500, 430, 470, a * r(t, 45.3, 0.4), zoom(t, 45.3, 48.4))
        text(d, 500, 770, "GREEKS", 110, a * r(t, 45.35), sp=4, dy=18); text(d, 500, 870, "WHO FOUGHT IT", 36, a * r(t, 45.9), sp=8, color=GRAY, bold=False)
        obj(im, "roman", 1420, 430, 450, a * r(t, 46.7, 0.4), zoom(t, 46.7, 48.4))
        text(d, 1420, 770, "ROMANS", 110, a * r(t, 46.75), sp=4, dy=18); text(d, 1420, 870, "WHO BURNED IT", 36, a * r(t, 47.3), sp=8, color=GRAY, bold=False)
    # 8. title
    a = win(t, 48.5, 60)
    if a > 0:
        text(d, cx, 430, "CARTHAGE", 190, a * r(t, 48.55), sp=10, dy=20)
        text(d, cx, 600, "IN 20 MINUTES", 60, a * r(t, 49.2), sp=14, color=GRAY, bold=False)
        X0, X1, Y = 160, 1760, 840; ta = a * r(t, 49.0)
        d.line([(X0, Y), (X1, Y)], fill=col(DIM, ta), width=3)
        g = ease((t - 49.2) / 1.4)
        if g > 0: d.rectangle([X0, Y - 7, X0 + (X1 - X0) * g, Y + 7], fill=col(ACC, ta))
        text(d, X0, Y + 44, "814 BC", 26, ta, anchor="l", color=ACC, bold=False); text(d, X1, Y + 44, "146 BC", 26, ta, anchor="r", color=ACC, bold=False)
    return im

if __name__ == "__main__":
    if sys.argv[1] == "still":
        for s in sys.argv[2:]: frame(float(s)).resize((960, 540)).save(f"test_{float(s):05.1f}.png")
    else:
        n = int(round(DUR * FPS))
        p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", "gfx.tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(n): p.stdin.write(frame(i / FPS).tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace("gfx.tmp.mp4", "gfx.mp4")
