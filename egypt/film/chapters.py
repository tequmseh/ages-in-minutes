"""Ancient Egypt, chapters 1-12: graphics on black (g1..g12), stills laid over maps and clips, and the per-chapter layout (SPECS)."""
from gfxlib import *
from PIL import ImageFilter
import os, math
R = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(R); cx = W // 2
os.makedirs(f"{R}/tmp", exist_ok=True)
def card(n): return f"{R}/cards/card{n - 1}.mp4"
def M(n): return f"{C}/maps/out_look/{n}.mp4"
def RC(n): return f"{R}/rec/{n}.mp4"
GR = dict(color=GRAY, bold=False); LIGHT = (205, 205, 200); RED = (186, 62, 40)
LOGO = Image.open(f"{C}/../channel/logo_mark_transparent.png").convert("RGBA")

# ---------- stills: transparent 1920x1080 layers that sit on top of a map or a clip
def still(key, fn):
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fn(im, ImageDraw.Draw(im)); p = f"{R}/tmp/st_{key}.png"; im.save(p); return p
    return mk
def T(d, x, y, s, size, fill=WHITE, bold=True, sp=3, anchor="m"):
    f = font(bold, size); w = tw(d, s, f, sp); x0 = x - w / 2 if anchor == "m" else (x - w if anchor == "r" else x)
    for ch in s: d.text((x0, y - size * 0.6), ch, font=f, fill=fill + (255,)); x0 += d.textlength(ch, font=f) + sp
def PL(d, x, y, s, size, fg=BG, bg=WHITE, sp=3, anchor="m"):
    f = font(True, size); w = tw(d, s, f, sp); px, py = size * 0.45, size * 0.32; x0 = x - w / 2 if anchor == "m" else x
    d.rectangle([x0 - px, y - size * 0.6 - py, x0 + w + px, y + size * 0.6 + py], fill=bg + (255,))
    for ch in s: d.text((x0, y - size * 0.6), ch, font=f, fill=fg + (255,)); x0 += d.textlength(ch, font=f) + sp
def BP(d, x, y, s, size=30, **k): PL(d, x, y, s, size, fg=WHITE, bg=BG, **k)         # black plaque, the map's own label style
def band(im, h=560, k=0.96):
    g = Image.linear_gradient("L").resize((W, h)).point(lambda v: int(v * k)); b = Image.new("RGBA", (W, h), BG + (0,)); b.putalpha(g); im.alpha_composite(b, (0, H - h))
def put(im, n, x, y, h=None, w=None, shadow=True):
    """museum cut-out straight on the map, with a soft shadow (no dark panel)"""
    s = Image.open(f"{R}/cut/{n}.png").convert("RGBA")
    if h is None: h = int(s.height * w / s.width)
    o = s.resize((max(2, int(s.width * h / s.height)), int(h)), Image.LANCZOS)
    if shadow:
        pad = 60; sh = Image.new("RGBA", (o.width + 2 * pad, o.height + 2 * pad), (0, 0, 0, 0))
        sh.paste(Image.new("RGBA", o.size, (0, 0, 0, 150)), (pad + 10, pad + 14), o.getchannel("A")); sh = sh.filter(ImageFilter.GaussianBlur(18))
        im.alpha_composite(sh, (int(x - o.width / 2 - pad), int(y - o.height / 2 - pad)))
    im.alpha_composite(o, (int(x - o.width / 2), int(y - o.height / 2)))
def lt(key, main=None, small=None, plq=False, y=955, size=62, under=None):
    """lower third over footage: dark band, small light line above, main line (plain or plaque), optional line under"""
    def fn(im, d):
        band(im)
        if small: T(d, cx, y - 85, small, 34, WHITE, bold=False, sp=7)
        if main:
            sz = size
            while tw(d, main, font(True, sz), 3) > 1720: sz -= 2
            (PL if plq else T)(d, cx, y, main, sz)
        if under: T(d, cx, y + 70, under, 32, WHITE, bold=False, sp=6)
    return still(key, fn)
def only(key, fn): return still(key, fn)

# ---------- crowns, drawn
def crown_white(d, x, y, s, a, fill=WHITE):
    if a <= 0: return
    pts = [(-0.26, 0), (-0.23, -0.22), (-0.16, -0.50), (-0.11, -0.70), (-0.13, -0.80), (-0.10, -0.92), (0, -0.98), (0.10, -0.92), (0.13, -0.80), (0.11, -0.70), (0.16, -0.50), (0.23, -0.22), (0.26, 0)]
    d.polygon([(x + px * s, y + py * s) for px, py in pts], fill=col(fill, a))
def crown_red(d, x, y, s, a):
    if a <= 0: return
    c = col(RED, a)
    d.polygon([(x - 0.30 * s, y), (x - 0.35 * s, y - 0.36 * s), (x + 0.10 * s, y - 0.44 * s), (x + 0.25 * s, y - 1.0 * s), (x + 0.33 * s, y - 1.0 * s), (x + 0.30 * s, y)], fill=c)
    x0, y0 = x - 0.02 * s, y - 0.42 * s; x1, y1 = x - 0.27 * s, y - 0.78 * s; pts = [(x0, y0), (x1, y1)]
    ccx, ccy = x1 - 0.085 * s, y1 + 0.015 * s; a0 = math.atan2(y1 - ccy, x1 - ccx)
    for i in range(1, 70):                                                 # the curl ends in a small spiral
        u = i / 69; ang = a0 - u * math.pi * 3.4; rad = 0.086 * s * (1 - u * 0.8); pts.append((ccx + math.cos(ang) * rad, ccy + math.sin(ang) * rad))
    d.line(pts, fill=c, width=max(4, int(s * 0.024)), joint="curve")

# ================= 1. The Gift
def _palermo(im, d): put(im, "palermo", 230, 400, h=480); BP(d, 70, 690, "THE OLDEST ROYAL ANNALS", 28, anchor="l")
def _herod(im, d): put(im, "herod", 230, 400, h=480); BP(d, 70, 690, "HERODOTUS", 30, sp=6, anchor="l")
S1 = dict(n=1, gfx=None, overlays=[(M("01_the_gift"), 0, 86.6, False), (RC("R03"), 35.4, 42.3, True, 1.0), (RC("R04"), 76.2, 86.6, True)], stills=[
    (lt("1a", "THE GIFT IS NOT RELIABLE", plq=True), 35.5, 37.4), (lt("1b", "TOO LOW A FLOOD, AND PEOPLE STARVE"), 37.5, 39.8), (lt("1c", "TOO HIGH, AND IT SWEEPS VILLAGES AWAY"), 39.9, 42.2),
    (still("1p", _palermo), 42.7, 51.4), (only("1p2", lambda im, d: PL(d, 74, 780, "HOW HIGH THE RIVER ROSE", 38, anchor="l")), 49.6, 51.4),
    (still("1h", _herod), 70.9, 76.1), (only("1h2", lambda im, d: PL(d, 74, 780, "THE GIFT OF THE RIVER", 38, anchor="l")), 72.9, 76.1),
    (lt("1d", "A GIFT LIKE THIS NEEDS MANAGING"), 76.4, 78.2), (lt("1e", "MEASURE THE FLOOD  ·  STORE THE GRAIN  ·  SETTLE THE FIELDS", size=48), 78.4, 84.1),
    (lt("1f", "THAT SOMEONE IS ABOUT TO APPEAR", plq=True), 84.4, 86.5)])

# ================= 2. Two Lands
def g2(t):
    im, d = blank()
    a = win(t, 16.5, 31.9)
    if a > 0:
        text(d, cx, 80, "HIS VICTORY POSTER", 34, a * r(t, 16.8), sp=8, **GR)
        obj(im, "narmer_a", 540, 545, 760, a * r(t, 16.8)); obj(im, "narmer_b", 1380, 545, 760, a * (0.3 * r(t, 17.0) + 0.7 * r(t, 26.6)))
        text(d, 540, 1000, "THE WHITE CROWN OF THE SOUTH", 34, a * r(t, 22.6), sp=4); text(d, 1380, 1000, "THE RED CROWN OF THE NORTH", 34, a * r(t, 27.6), sp=4)
    a = win(t, 32.0, 46.3)
    if a > 0:
        obj(im, "crown_w", 430, 640 - 0.34 * 911 / 2, int(0.34 * 911), a * r(t, 32.2)); text(d, 430, 760, "THE SOUTH", 34, a * r(t, 32.6), sp=8, **GR)
        text(d, 690, 470, "+", 90, a * r(t, 33.2), **GR)
        obj(im, "crown_r", 950, 700 - 0.34 * 1262 / 2, int(0.34 * 1262), a * r(t, 33.2)); text(d, 950, 760, "THE NORTH", 34, a * r(t, 33.6), sp=8, **GR)
        text(d, 1220, 470, "=", 90, a * r(t, 34.3), **GR)
        obj(im, "crownfig", 1500, 520, 800, a * r(t, 34.3))
        text(d, 690, 200, "EVERY KING WEARS BOTH CROWNS", 40, a * r(t, 32.4), sp=6)
        plaque(d, 690, 880, "LORD OF THE TWO LANDS", 60, a * r(t, 36.6), sp=4)
        text(d, 690, 1000, "TWO COUNTRIES HELD TOGETHER BY ONE MAN", 32, a * r(t, 39.4), sp=6, **GR)
    a = win(t, 51.5, 64.2)
    if a > 0:
        text(d, cx, 90, "A NEW TOOL", 36, a * r(t, 51.7), sp=10, **GR)
        obj(im, "labels", cx, 460, None, a * r(t, 53.6), w=1180)
        text(d, cx, 850, "LABELS TIED TO GOODS IN ROYAL TOMBS", 38, a * r(t, 57.4), sp=6)
        text(d, cx - 400, 975, "HIEROGLYPHS BEGIN AS", 38, a * r(t, 61.8), sp=6, **GR); plaque(d, cx + 230, 975, "STOCK CONTROL", 56, a * r(t, 62.7), sp=4)
    a = win(t, 64.4, 82.3)
    if a > 0:
        obj(im, "maat", 480, 540, 820, a * r(t, 64.5, 0.6))
        text(d, 1250, 130, "THE KING IS A GOD ON EARTH", 36, a * r(t, 66.4), sp=7, **GR); text(d, 1250, 210, "WITH ONE JOB: TO KEEP", 36, a * r(t, 68.0), sp=7, **GR)
        text(d, 1250, 390, "MAAT", 190, a * r(t, 69.5), sp=14, dy=18)
        text(d, 1250, 560, "ORDER  ·  BALANCE  ·  THE FLOOD ON TIME", 34, a * r(t, 70.9), sp=5)
        text(d, 1100, 740, "THE OPPOSITE:", 36, a * r(t, 75.3), sp=7, **GR); plaque(d, 1480, 740, "CHAOS", 60, a * r(t, 76.3), sp=6)
        text(d, 1250, 930, "THE OPERATING MANUAL FOR THE NEXT 3,000 YEARS", 30, a * r(t, 78.9), sp=6, **GR)
    return im
S2 = dict(n=2, gfx=g2, gfx_windows=[(16.4, 46.5), (51.3, 82.4)], overlays=[(M("02a_two_lands"), 0, 16.5, False), (M("02b_two_lands"), 46.4, 51.5, False)])

# ================= 3. The Pyramid Age
def g3(t):
    im, d = blank(); a = win(t, 0.1, 4.6, fo=0.2)
    text(d, cx, 380, "IF THE KING IS A GOD", 44, a * r(t, 0.2), sp=8, **GR); text(d, cx, 520, "HIS TOMB IS", 80, a * r(t, 1.6), sp=5); plaque(d, cx, 690, "A PUBLIC WORKS PROJECT", 72, a * r(t, 2.4), sp=4)
    return im
def _merer(im, d): put(im, "merer", 1500, 500, h=600); BP(d, 1500, 850, "THE OLDEST INSCRIBED PAPYRI IN THE WORLD", 24)
S3 = dict(n=3, gfx=g3, gfx_windows=[(0, 4.8)], overlays=[(M("03_the_pyramid_age"), 4.6, 98.6, False), (RC("R05"), 15.7, 25.9, True), (RC("R01"), 50.4, 62.6, True),
                                                       (RC("R06a"), 62.8, 71.5, True, 0.5), (RC("R06b"), 71.5, 78.4, True, 1.5)], stills=[
    (lt("3a", "IMHOTEP BUILDS ONE IN STONE", under="THEN STACKS FIVE MORE ON TOP"), 16.8, 21.0),
    (lt("3b", "THE STEP PYRAMID", under="THE OLDEST BIG STONE BUILDING WE KNOW OF"), 21.3, 25.8),
    (lt("3c", "THE GREAT PYRAMID"), 52.6, 54.0), (lt("3d", "2.3 MILLION BLOCKS", plq=True), 54.2, 56.4), (lt("3e", "146 METRES HIGH", plq=True), 56.5, 58.6),
    (lt("3f", "NOTHING ON EARTH IS TALLER", small="FOR NEARLY 4,000 YEARS"), 58.9, 62.4),
    (lt("3g", "NOT SLAVES", small="WHO BUILT IT?", plq=True), 63.2, 66.6), (lt("3h", "BAKERIES  ·  BARRACKS FOR 2,000 MEN  ·  CATTLE BONES BY THE TON", small="THEIR TOWN NEXT DOOR", size=46), 67.0, 71.4),
    (lt("3i", "FED LIKE SOLDIERS", small="A KIND OF LABOUR TAX"), 73.6, 78.2),
    (still("3m", _merer), 78.6, 88.2), (only("3m2", lambda im, d: BP(d, 1500, 915, "INSPECTOR MERER", 30, sp=6)), 85.9, 88.2)])

# ================= 4. The First Collapse
def g4(t):
    im, d = blank()
    a = win(t, 0.1, 14.2)
    if a > 0:
        obj(im, "pepipyr", cx, 400, None, a * r(t, 0.2, 0.6), w=900)
        text(d, cx, 830, "SMALLER AND SHODDIER", 54, a * r(t, 1.8), sp=5)
        text(d, cx, 915, "EVERY DEAD KING NEEDS PRIESTS AND ESTATES, FOREVER, TAX-FREE", 30, a * r(t, 6.5), sp=5, **GR)
        plaque(d, cx, 1005, "FOREVER TURNS OUT TO BE EXPENSIVE", 44, a * r(t, 11.8), sp=4)
    a = win(t, 14.4, 23.6)
    if a > 0:
        text(d, cx, 260, "POWER DRAINS OUT OF THE CAPITAL", 40, a * r(t, 14.6), sp=8, **GR)
        text(d, cx, 420, "PROVINCIAL GOVERNORS PASS THEIR JOBS", 56, a * r(t, 16.9), sp=4); plaque(d, cx, 580, "FROM FATHER TO SON", 84, a * r(t, 18.6), sp=5)
        text(d, cx, 780, "AND BUILD GRAND TOMBS AT HOME, NOT NEXT TO THE KING", 34, a * r(t, 20.6), sp=6, **GR)
    a = win(t, 23.8, 39.7, fo=0.25)
    if a > 0:
        obj(im, "pepi", 540, 540, 860, a * r(t, 23.9, 0.6))
        text(d, 1320, 200, "THE LAST GREAT KING OF THE AGE", 34, a * r(t, 24.0), sp=7, **GR); text(d, 1320, 350, "PEPI II", 160, a * r(t, 26.0), sp=10, dy=18)
        text(d, 1320, 500, "ON THE THRONE AS A SMALL BOY", 34, a * r(t, 27.6), sp=6, **GR)
        plaque(d, 1320, 660, "MORE THAN 90 YEARS", 68, a * r(t, 30.0), sp=4); text(d, 1320, 765, "BY TRADITION", 30, a * r(t, 29.2), sp=8, **GR)
        text(d, 1320, 900, "AN OLD KING", 46, a * r(t, 36.5), sp=5); text(d, 1320, 975, "AND HEIRS WHO DIE WAITING", 46, a * r(t, 37.6), sp=5)
    return im
def _mirror(im, d): put(im, "mirror", 700, 540, w=300); BP(d, 700, 700, "NOW OWNS A MIRROR", 28)
S4 = dict(n=4, gfx=g4, gfx_windows=[(0, 39.9)], overlays=[(M("04_the_first_collapse"), 39.8, 84.9, False)], stills=[
    (only("4u", lambda im, d: BP(d, 520, 900, "THE WORLD TURNED UPSIDE DOWN", 34)), 59.2, 62.8), (still("4m", _mirror), 65.6, 72.0),
    (only("4n", lambda im, d: PL(d, 620, 790, "NOTE WHO IS COMPLAINING", 32)), 70.2, 72.0), (only("4w", lambda im, d: PL(d, 520, 900, "WARLORDS WITH GOOD PR", 38)), 75.1, 77.1)])

# ================= 5. The Reboot
def g5(t):
    im, d = blank()
    a = win(t, 0.1, 8.9, fo=0.2)
    if a > 0:
        text(d, cx, 200, "THE FIRST CLUE TO OUR QUESTION", 36, a * r(t, 0.3), sp=8, **GR)
        y = 600; k = r(t, 0.4, 1.0)
        d.rectangle([260, y - 7, 260 + 600 * k, y + 7], fill=col(ACC, a))
        if t > 3.2:
            for x in range(880, 1050, 34): d.rectangle([x, y - 3, x + 18, y + 3], fill=col(GRAY, a * r(t, 3.3)))
            text(d, 960, y - 60, "COLLAPSE", 30, a * r(t, 3.4), sp=8, **GR)
        k2 = r(t, 7.6, 0.8)
        if k2 > 0: d.rectangle([1060, y - 7, 1060 + 600 * k2, y + 7], fill=col(ACC, a))
        text(d, cx, 370, "EGYPT HAS COLLAPSED", 76, a * r(t, 3.4), sp=5)
        text(d, cx, 760, "IT DOES NOT TURN INTO SOMETHING ELSE", 38, a * r(t, 5.2), sp=7, **GR); plaque(d, cx, 900, "IT REBOOTS", 84, a * r(t, 7.7, 0.25), sp=6)
    a = win(t, 65.5, 84.6)
    if a > 0:
        text(d, cx, 90, "EGYPT WRITES ITS CLASSICS", 38, a * r(t, 65.7), sp=9, **GR)
        obj(im, "sinuhe", 640, 400, None, a * r(t, 68.4, 0.6), w=940); obj(im, "palette", 1500, 400, None, a * r(t, 66.2, 0.6), w=600)
        text(d, 640, 720, "THE TALE OF SINUHE", 48, a * r(t, 71.2), sp=5); text(d, 1500, 720, "STORIES  ·  ADVICE  ·  COMPLAINTS", 30, a * r(t, 68.4), sp=5, **GR)
        plaque(d, cx, 875, "THE GOLDEN AGE", 80, a * r(t, 81.0), sp=6); text(d, cx, 1000, "THE TIME WHEN THE LANGUAGE WAS PERFECT", 32, a * r(t, 82.4), sp=7, **GR)
    a = win(t, 84.7, 89.0, fo=0.1)
    if a > 0:
        text(d, cx, 330, "IT LASTS", 44, a * r(t, 84.8), sp=10, **GR); text(d, cx, 500, "400 YEARS", 180, a * r(t, 85.4), sp=8, dy=18)
        plaque(d, cx, 760, "THEN THE PATTERN REPEATS", 60, a * r(t, 87.2), sp=4)
    return im
def _sen(im, d): put(im, "sen3", 270, 590, h=480); BP(d, 270, 880, "SENUSRET III", 30, sp=5)
def _sah(im, d): put(im, "sahure", 650, 590, h=520); BP(d, 650, 880, "A PYRAMID KING", 30, sp=5)
S5 = dict(n=5, gfx=g5, gfx_windows=[(0, 9.0), (65.4, 89.0)], overlays=[(M("05_the_reboot"), 8.8, 65.7, False)], stills=[
    (still("5s", _sen), 32.2, 50.2), (still("5k", _sah), 34.8, 50.2), (only("5t", lambda im, d: BP(d, 460, 280, "HEAVY EYELIDS  ·  A LINED FACE  ·  BIG EARS", 28)), 39.8, 45.9),
    (only("5j", lambda im, d: PL(d, 460, 280, "THIS IS A HARD JOB", 44)), 46.3, 50.2)])

# ================= 6. Foreign Kings
ROUTE = [(905, 215), (800, 300), (730, 420), (710, 540), (730, 680), (790, 800), (835, 880)]
def _dash(d, pts, on=16, off=12, width=5, fill=BG + (255,)):
    acc = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0); s = 0.0
        while s < L:
            ph = (acc + s) % (on + off)
            if ph < on:
                e = min(L, s + on - ph); d.line([(x0 + (x1 - x0) * s / L, y0 + (y1 - y0) * s / L), (x0 + (x1 - x0) * e / L, y0 + (y1 - y0) * e / L)], fill=fill, width=width); s = e
            else: s += on + off - ph
        acc += L
def _mess(im, d):
    _dash(d, ROUTE[:4]); _dash(d, ROUTE[3:], on=4, off=14, width=4, fill=BG + (120,))
    x, y = ROUTE[3]; d.line([(x - 20, y - 20), (x + 20, y + 20)], fill=BG + (255,), width=8); d.line([(x - 20, y + 20), (x + 20, y - 20)], fill=BG + (255,), width=8)
    BP(d, x - 185, y, "A MESSENGER", 28, sp=5)
def _quote(im, d): PL(d, 400, 800, "ATTACK FROM THE SOUTH,", 36); PL(d, 400, 868, "AND WE WILL SHARE EGYPT", 36)
def _axe(im, d): put(im, "axe", 400, 600, h=400); BP(d, 400, 860, "WEAPONS OF A LEVANTINE TYPE", 26)
S6 = dict(n=6, gfx=None, overlays=[(M("06_foreign_kings"), 0, 94.6, False), (RC("R07"), 36.1, 46.2, True)], stills=[
    (lt("6a", "THE HORSE AND CHARIOT", small="NEW TECHNOLOGY"), 38.3, 39.8), (lt("6b", "A STRONGER BOW", small="NEW TECHNOLOGY"), 39.9, 41.1), (lt("6c", "NEW BRONZE WEAPONS", small="NEW TECHNOLOGY"), 41.2, 42.8),
    (lt("6d", "EGYPT HAS FALLEN BEHIND", plq=True), 43.1, 46.1), (still("6x", _axe), 58.8, 65.6), (still("6m", _mess), 68.2, 77.3), (still("6q", _quote), 74.1, 77.3)])

# ================= 7. The Empire
def g7(t):
    im, d = blank(); a = win(t, 79.4, 92.3, fo=0.1)
    if a > 0:
        text(d, cx, 150, "THE KING GETS A NICKNAME", 38, a * r(t, 79.6), sp=9, **GR)
        text(d, 330, 460, "PER-AA", 90, a * r(t, 85.2), sp=6); text(d, 330, 570, "THE PALACE, NOT THE MAN", 26, a * r(t, 82.0), sp=5, **GR)
        text(d, 575, 455, "→", 50, a * r(t, 85.8), **GR); text(d, 920, 460, "THE GREAT HOUSE", 60, a * r(t, 85.8), sp=4)
        text(d, 920, 570, "LIKE “THE WHITE HOUSE”", 26, a * r(t, 86.8), sp=5, **GR)
        text(d, 1270, 455, "→", 50, a * r(t, 90.6), **GR); plaque(d, 1560, 460, "PHARAOH", 70, a * r(t, 90.8), sp=5)
        text(d, cx, 800, "IT REACHES US THROUGH THE BIBLE", 34, a * r(t, 89.2), sp=8, **GR)
    return im
def _hat(im, d): put(im, "hat", 330, 560, h=760); BP(d, 330, 985, "HATSHEPSUT", 32, sp=6)
S7 = dict(n=7, gfx=g7, gfx_windows=[(79.3, 92.4)], overlays=[(M("07_the_empire"), 0, 79.5, False), (RC("R08"), 46.5, 56.4, True), (RC("R09"), 69.4, 79.4, True)], stills=[
    (still("7h", _hat), 29.4, 41.0), (only("7k", lambda im, d: (BP(d, 640, 420, "NOT QUEEN:", 40), PL(d, 640, 520, "KING", 80, sp=8))), 34.9, 41.0),
    (only("7b", lambda im, d: BP(d, 640, 650, "WITH THE ROYAL FALSE BEARD", 26)), 38.2, 41.0),
    (lt("7a", "ONE OF THE MOST ELEGANT TEMPLES IN EGYPT"), 46.7, 49.4), (lt("7c", "HER NAME IS CHISELLED OFF THE WALLS"), 49.9, 53.1),
    (lt("7d", "WE'RE TALKING ABOUT HER", small="IT DIDN'T WORK", plq=True), 53.5, 56.3),
    (lt("7e", "HIDDEN TOMBS IN A DESERT VALLEY"), 73.9, 76.7), (lt("7f", "THE VALLEY OF THE KINGS", plq=True), 77.1, 79.3)])

# ================= 8. The Heretic
def g8(t):
    im, d = blank()
    a = win(t, 0.1, 15.5, fo=0.2)
    if a > 0:
        obj(im, "reliefp", 520, 540, 900, a * r(t, 0.2, 0.7))
        text(d, 1400, 200, "ONE PHARAOH REWRITES", 36, a * r(t, 2.2), sp=7, **GR); text(d, 1400, 255, "THE OPERATING MANUAL", 36, a * r(t, 3.2), sp=7, **GR)
        text(d, 1400, 420, "AMENHOTEP IV", 84, a * r(t, 6.9), sp=4); text(d, 1400, 540, "ONLY ONE GOD WORTH WORSHIPPING", 30, a * r(t, 9.6), sp=6, **GR)
        plaque(d, 1400, 700, "THE ATEN", 96, a * r(t, 12.8), sp=6); text(d, 1400, 830, "THE DISC OF THE SUN", 36, a * r(t, 13.8), sp=8, **GR)
    a = win(t, 28.1, 36.4)
    if a > 0:
        text(d, cx, 330, "THE WORLD'S FIRST MONOTHEISM?", 70, a * r(t, 28.3), sp=4); text(d, cx, 460, "PERHAPS", 40, a * r(t, 30.7), sp=10, **GR)
        text(d, cx, 650, "CERTAINLY", 36, a * r(t, 31.9), sp=10, **GR); plaque(d, cx, 770, "A HOSTILE TAKEOVER", 84, a * r(t, 33.0), sp=5)
        text(d, cx, 920, "OF THE RICHEST INSTITUTION IN THE COUNTRY", 32, a * r(t, 34.3), sp=7, **GR)
    a = win(t, 36.6, 48.6)
    if a > 0:
        obj(im, "akh", 560, 540, 960, a * r(t, 36.7, 0.6))
        text(d, 1300, 200, "THE ART CHANGES OVERNIGHT", 38, a * r(t, 36.8), sp=8, **GR)
        text(d, 1300, 400, "AKHENATEN", 100, a * r(t, 41.4), sp=5)
        for k, (s, t0) in enumerate((("A LONG FACE", 43.6), ("A POT BELLY", 44.9), ("WIDE HIPS", 46.0))): text(d, 1300, 580 + k * 95, s, 56, a * r(t, t0), sp=5)
        text(d, 1300, 900, "KISSING HIS CHILDREN", 34, a * r(t, 47.1), sp=8, **GR)
    a = win(t, 48.7, 53.5, fo=0.2)
    if a > 0:
        obj(im, "nef", 620, 540, 960, a * r(t, 48.8, 0.5))
        text(d, 1340, 400, "HIS WIFE", 36, a * r(t, 48.9), sp=10, **GR); text(d, 1340, 540, "NEFERTITI", 120, a * r(t, 49.5), sp=6, dy=16)
        text(d, 1340, 700, "THE MOST FAMOUS PORTRAIT", 32, a * r(t, 50.6), sp=7, **GR); text(d, 1340, 750, "IN EGYPTIAN HISTORY", 32, a * r(t, 51.4), sp=7, **GR)
    a = win(t, 65.0, 73.9)
    if a > 0:
        text(d, cx, 250, "AKHENATEN DIES AFTER 17 YEARS", 44, a * r(t, 65.2), sp=7, **GR)
        text(d, cx - 330, 470, "WITHIN A FEW YEARS IT IS ALL", 52, a * r(t, 68.0), sp=4); plaque(d, cx + 440, 470, "REVERSED", 68, a * r(t, 69.4), sp=5)
        text(d, cx, 690, "THE NEW CITY IS ABANDONED", 56, a * r(t, 70.7), sp=5); text(d, cx, 800, "THE OLD GODS RETURN", 56, a * r(t, 72.4), sp=5)
    a = win(t, 74.1, 99.9, fo=0.1)
    if a > 0:
        obj(im, "tut", 560, 540, 900, a * r(t, 74.2, 0.7)); x = 1340
        k1 = a * (1 - r(t, 86.4, 0.4))
        text(d, x, 220, "THE BOY WHO SIGNS THE RESTORATION", 30, k1 * r(t, 74.3), sp=6, **GR); text(d, x, 370, "TUTANKHAMUN", 92, k1 * r(t, 76.0), sp=4)
        strike(d, x, 370, "TUTANKHAMUN", 92, r(t, 80.6, 0.9), k1, sp=4)
        text(d, x, 500, "DIES AT ABOUT NINETEEN", 32, k1 * r(t, 78.0), sp=7, **GR)
        text(d, x, 640, "SCRUBBED FROM THE KING LISTS", 40, k1 * r(t, 80.2), sp=5)
        plaque(d, x, 800, "WHICH IS WHY YOU KNOW HIS NAME", 40, k1 * r(t, 83.6), sp=3)
        k2 = a * r(t, 86.7, 0.4)
        text(d, x, 220, "A SMALL TOMB, FORGOTTEN", 36, k2, sp=7, **GR); text(d, x, 290, "THE ROBBERS MOSTLY MISS IT", 36, k2 * r(t, 89.0), sp=7, **GR)
        plaque(d, x, 480, "1922", 150, k2 * r(t, 92.4), sp=8); text(d, x, 640, "FOUND ALMOST INTACT", 44, k2 * r(t, 93.6), sp=6)
        text(d, x, 830, "THE MOST FAMOUS PHARAOH OF ALL", 34, k2 * r(t, 95.9), sp=6, **GR); text(d, x, 900, "IS THE ONE EGYPT TRIED TO DELETE", 40, k2 * r(t, 97.4), sp=4)
    return im
def _amarna(im, d): put(im, "amarna", 300, 720, h=400); BP(d, 300, 955, "LETTERS ON CLAY TABLETS", 26)
S8 = dict(n=8, gfx=g8, gfx_windows=[(0, 15.7), (28.0, 53.7), (64.8, 99.9)], overlays=[(RC("R10"), 15.6, 24.0, True, 1.0), (M("08a_the_heretic"), 23.9, 28.3, False), (M("08b_the_heretic"), 53.6, 65.0, False)], stills=[
    (lt("8a", "AKHENATEN", small="HE RENAMES HIMSELF"), 15.8, 18.0), (lt("8b", "HE SHUTS DOWN THE TEMPLES OF AMUN"), 18.3, 23.6),
    (still("8t", _amarna), 57.7, 64.8), (only("8g", lambda im, d: PL(d, 300, 1022, "THE KINGS WANT GOLD", 34)), 63.0, 64.8)])

# ================= 9. The Superpower
ABS = [("ILL", 80.5), ("STUNG BY A SCORPION", 81.9), ("EMBALMING HIS BROTHER", 84.1), ("BREWING BEER", 86.5)]
FLAKE = [(430, 250), (700, 190), (1050, 215), (1380, 180), (1540, 300), (1500, 520), (1560, 720), (1420, 860), (1100, 835), (820, 880), (520, 840), (380, 660), (420, 450)]
def g9(t):
    im, d = blank()
    a = win(t, 0.1, 14.9)
    if a > 0:
        obj(im, "ram", 520, 540, 940, a * r(t, 0.2, 0.7)); x = 1300
        text(d, x, 180, "A NEW DYNASTY, AND ITS STAR", 34, a * r(t, 2.4), sp=7, **GR); text(d, x, 330, "RAMESSES II", 120, a * r(t, 4.0), sp=5, dy=16)
        plaque(d, x, 540, "66 YEARS", 76, a * r(t, 6.6), sp=5); plaque(d, x, 690, "100 CHILDREN", 76, a * r(t, 8.6), sp=5)
        text(d, x, 870, "HIS NAME ON EVERYTHING", 44, a * r(t, 11.0), sp=5); text(d, x, 940, "EVEN OTHER KINGS' BUILDINGS", 32, a * r(t, 12.8), sp=7, **GR)
    a = win(t, 33.6, 42.2)
    if a > 0:
        obj(im, "kadesh", cx, 440, None, a * r(t, 33.7, 0.6), w=1800)
        text(d, cx - 330, 920, "CARVED ON TEMPLE WALLS AS", 40, a * r(t, 34.6), sp=5, **GR); plaque(d, cx + 420, 920, "A PERSONAL TRIUMPH", 52, a * r(t, 36.9), sp=4)
        text(d, cx, 1020, "RAMESSES ALONE IN HIS CHARIOT", 30, a * r(t, 38.6), sp=8, **GR)
    a = win(t, 42.3, 59.3, fo=0.2)
    if a > 0:
        obj(im, "treatyp", 540, 440, None, a * r(t, 42.5, 0.7), w=980); x = 1440
        text(d, x, 150, "FIFTEEN YEARS LATER", 34, a * r(t, 42.5), sp=8, **GR); text(d, x, 270, "A PEACE TREATY", 76, a * r(t, 46.4), sp=4)
        for k, (s, t0) in enumerate((("NO MORE WAR", 47.9), ("A DEFENCE PACT", 49.0), ("THE RETURN OF REFUGEES", 50.2))): text(d, x, 420 + k * 80, s, 44, a * r(t, t0), sp=5)
        text(d, x, 700, "BOTH SIDES' VERSIONS SURVIVE", 30, a * r(t, 52.4), sp=7, **GR)
        plaque(d, cx, 880, "THE OLDEST SURVIVING TREATY OF ITS KIND", 52, a * r(t, 54.6), sp=4); text(d, cx, 1000, "A COPY HANGS AT THE UNITED NATIONS", 32, a * r(t, 57.0), sp=8, **GR)
    a = win(t, 73.9, 92.0, fo=0.1)
    if a > 0:
        d.polygon(FLAKE, fill=col((222, 212, 190), a * r(t, 74.0, 0.6))); ink = (58, 44, 34)
        def ft(x, y, s, size, k, bold=True, sp=3):
            if k <= 0: return
            f = font(bold, size); w = tw(d, s, f, sp); xx = x
            c0 = col((222, 212, 190), a); c = tuple(int(c0[i] + (ink[i] * a + BG[i] * (1 - a) - c0[i]) * k) for i in range(3))
            for ch in s: d.text((xx, y - size * 0.6), ch, font=f, fill=c); xx += d.textlength(ch, font=f) + sp
        ft(500, 300, "AN ATTENDANCE REGISTER FOR 40 WORKERS", 34, r(t, 77.2), sp=5)
        for k, (s, t0) in enumerate(ABS):
            y = 410 + k * 100; ft(500, y, "ABSENT:", 42, r(t, t0 - 0.05), bold=False, sp=5); ft(730, y, s, 48, r(t, t0 + 0.35))
        text(d, cx, 960, "THE SICK NOTES OF THE MEN WHO BUILT", 34, a * r(t, 88.5), sp=7, **GR); text(d, cx, 1020, "THE VALLEY OF THE KINGS", 40, a * r(t, 90.0), sp=7)
        text(d, cx, 110, "THEY WROTE ON FLAKES OF STONE", 36, a * r(t, 74.8), sp=8, **GR)
    return im
S9 = dict(n=9, gfx=g9, gfx_windows=[(0, 15.1), (33.5, 59.5), (73.8, 92.1)], overlays=[(M("09a_the_superpower"), 15.0, 33.7, False), (RC("R11"), 59.4, 66.3, True), (M("09c_the_superpower"), 66.3, 74.0, False)], stills=[
    (lt("9a", "ABU SIMBEL", under="FOUR STATUES OF HIMSELF, TWENTY METRES HIGH"), 59.6, 64.9), (lt("9b", "SUBTLE IT IS NOT", plq=True), 65.2, 66.2)])

# ================= 10. The Long Decline
def g10(t):
    im, d = blank()
    a = win(t, 0.1, 2.8, fo=0.15); text(d, cx, 440, "THE THIRD COLLAPSE", 90, a * r(t, 0.2), sp=5); plaque(d, cx, 620, "THE SLOW ONE", 70, a * r(t, 1.3), sp=6)
    a = win(t, 70.6, 75.0, fo=0.15); text(d, cx, 440, "THEN COME THE OUTSIDERS", 80, a * r(t, 70.8), sp=5); plaque(d, cx, 620, "LIBYAN CHIEFS RULE AS PHARAOHS", 54, a * r(t, 72.7), sp=4)
    return im
def _meroe(im, d): put(im, "meroe", 430, 560, w=680); BP(d, 430, 800, "MORE PYRAMIDS IN SUDAN THAN IN EGYPT", 26)
S10 = dict(n=10, gfx=g10, gfx_windows=[(0, 2.9), (70.5, 75.1)], overlays=[(M("10a_the_long_decline"), 2.7, 29.7, False), (RC("R12a"), 29.7, 39.4, True), (RC("R12b"), 39.4, 50.2, True),
                                                                   (RC("R13"), 50.2, 63.4, True, 1.0), (M("10b_the_long_decline"), 63.4, 70.7, False), (M("10c_the_long_decline"), 74.9, 92.6, False)], stills=[
    (lt("10a", "THE TOMB BUILDERS DO NOT GET THEIR RATIONS", small="YEAR 29 OF RAMESSES III", size=54), 30.0, 35.8), (lt("10b", "THEY PUT DOWN THEIR TOOLS AND SIT DOWN"), 36.1, 39.2),
    (lt("10c", "WE ARE HUNGRY", small="THE SCRIBE WRITES DOWN WHAT THEY SHOUT", plq=True), 40.0, 43.1), (lt("10d", "THE FIRST RECORDED STRIKE IN HISTORY"), 43.4, 46.2),
    (lt("10e", "THEY GET PAID", small="IT WORKS"), 46.4, 48.1), (lt("10f", "THEN THE PAY IS LATE AGAIN", plq=True), 48.4, 50.1),
    (lt("10g", "A CONSPIRACY IN THE ROYAL HAREM", small="THE SIGNS PILE UP"), 52.6, 56.0), (lt("10h", "THE PRIESTS OF AMUN HIDE THE GREAT PHARAOHS", size=54, under="TOGETHER, FOR SAFETY"), 56.5, 63.2),
    (still("10m", _meroe), 85.1, 88.2)])

# ================= 11. Other People's Egypt
BANDS = [(225, "HIEROGLYPHS", "FOR THE GODS", 61.7), (505, "EVERYDAY EGYPTIAN", "FOR THE CLERKS", 63.1), (820, "GREEK", "FOR THE GOVERNMENT", 64.7)]
def g11(t):
    im, d = blank()
    a = win(t, 0.1, 7.1, fo=0.2)
    if a > 0:
        text(d, cx, 330, "FROM HERE ON, EGYPT IS", 44, a * r(t, 0.2), sp=8, **GR); plaque(d, cx - 330, 500, "THE PRIZE", 96, a * r(t, 1.5), sp=5)
        text(d, cx + 380, 500, "NOT THE PLAYER", 76, a * r(t, 2.4), sp=4); strike(d, cx + 380, 500, "NOT THE PLAYER", 76, 0, a)
        text(d, cx, 760, "LOOK AT WHAT HAPPENS TO EVERYONE WHO WINS IT", 36, a * r(t, 3.6), sp=7, **GR)
    a = win(t, 27.8, 35.4, fo=0.2)
    if a > 0:
        obj(im, "ptol", 560, 540, 720, a * r(t, 27.9, 0.6)); x = 1340
        text(d, x, 300, "THE PTOLEMIES", 96, a * r(t, 28.0), sp=4); text(d, x, 420, "MACEDONIAN GREEKS", 40, a * r(t, 28.9), sp=8, **GR)
        text(d, x, 600, "THEY SPEAK GREEK", 44, a * r(t, 30.2), sp=5); text(d, x, 675, "AND MARRY THEIR SISTERS", 44, a * r(t, 31.2), sp=5)
        plaque(d, x, 850, "A FAMILY FIRM", 68, a * r(t, 33.8), sp=5)
    a = win(t, 53.9, 68.5, fo=0.2)
    if a > 0:
        obj(im, "rosetta", 520, 540, 900, a * r(t, 54.0, 0.7)); x = 1400
        k1 = a * (1 - r(t, 61.2, 0.3))
        plaque(d, x, 300, "196 BC", 110, k1 * r(t, 54.1), sp=6); text(d, x, 470, "A DECREE OF THE PRIESTS", 44, k1 * r(t, 55.3), sp=5)
        text(d, x, 550, "THANKING A TEENAGE PTOLEMY", 32, k1 * r(t, 56.6), sp=6, **GR); text(d, x, 600, "FOR HIS TAX BREAKS", 32, k1 * r(t, 58.2), sp=6, **GR)
        text(d, x, 780, "IN THREE SCRIPTS", 64, k1 * r(t, 59.8), sp=5)
        for y, s1, s2, t0 in BANDS:
            k = a * r(t, t0)
            if k > 0:
                d.line([(800, y), (1010, y)], fill=col(WHITE, k), width=3); d.ellipse([792, y - 8, 808, y + 8], fill=col(WHITE, k))
                text(d, 1040, y - 22, s1, 54, k, sp=4, anchor="l"); text(d, 1042, y + 42, s2, 30, k, sp=7, anchor="l", **GR)
        plaque(d, x + 40, 1000, "REMEMBER THAT STONE", 44, a * r(t, 66.7), sp=4)
    a = win(t, 76.1, 88.0, fo=0.1)
    if a > 0:
        obj(im, "cleo", 560, 440, 620, a * r(t, 76.2, 0.5)); obj(im, "antony", 1360, 440, 620, a * r(t, 77.2, 0.5))
        text(d, 560, 830, "CLEOPATRA VII", 44, a * r(t, 76.3), sp=6); text(d, 1360, 830, "TWO ROMANS IN A ROW", 44, a * r(t, 77.2), sp=5)
        text(d, 1360, 895, "THE SECOND ONE LOSES", 32, a * r(t, 78.8), sp=7, **GR)
        plaque(d, 560, 975, "30 BC", 70, a * r(t, 80.3), sp=6); text(d, 1360, 975, "EGYPT BECOMES THE PROPERTY OF OCTAVIAN", 30, a * r(t, 83.4), sp=5)
    return im
S11 = dict(n=11, gfx=g11, gfx_windows=[(0, 7.3), (27.7, 35.6), (53.8, 68.8), (76.0, 88.0)], overlays=[(M("11a_other_peoples_egypt"), 7.1, 27.9, False), (RC("R14"), 35.5, 45.0, True),
                                                                                                  (M("11b_other_peoples_egypt"), 44.9, 53.9, False), (RC("R02"), 68.7, 76.2, True, 0.3)], stills=[
    (lt("11a", "ALEXANDRIA", under="THE GREATEST CITY OF ITS AGE"), 35.7, 38.4), (lt("11b", "A LIGHTHOUSE A HUNDRED METRES TALL"), 38.7, 41.2),
    (lt("11c", "A LIBRARY THAT WANTS EVERY BOOK IN THE WORLD"), 41.4, 44.6),
    (lt("11d", "CLEOPATRA VII", small="THE LAST OF THE LINE"), 68.9, 71.3), (lt("11e", "THE FIRST OF HER FAMILY TO LEARN EGYPTIAN", small="CLEVER AND RUTHLESS", size=54), 71.6, 76.0)])

# ================= 12. What Remains
CONQ = ["LIBYANS", "NUBIANS", "PERSIANS", "GREEKS", "ROMANS"]
def g12(t):
    im, d = blank()
    a = win(t, 0.1, 5.9)
    if a > 0:
        obj(im, "august", 520, 540, 900, a * r(t, 0.2, 0.7))
        text(d, 1440, 400, "ROMAN EMPERORS", 68, a * r(t, 0.6), sp=4); text(d, 1440, 510, "WHO NEVER SET FOOT IN EGYPT", 32, a * r(t, 1.6), sp=7, **GR)
        plaque(d, 1440, 690, "AS PHARAOHS", 76, a * r(t, 4.3), sp=5)
    a = win(t, 6.3, 19.2, fo=0.2)
    if a > 0:
        text(d, cx, 180, "WHAT FINALLY ENDS ANCIENT EGYPT", 38, a * r(t, 6.5), sp=8, **GR)
        text(d, cx, 320, "NOT AN ARMY", 70, a * r(t, 8.4), sp=5); plaque(d, cx, 460, "A CHANGE OF MIND", 80, a * r(t, 10.3), sp=4)
        for k, (s, t0) in enumerate((("EGYPT BECOMES CHRISTIAN", 12.3), ("THE TEMPLES LOSE THEIR FUNDING", 14.0), ("THE PRIESTS WHO CAN READ THE OLD SCRIPT DIE OFF", 15.7))): text(d, cx, 660 + k * 100, s, 48, a * r(t, t0), sp=5)
    a = win(t, 34.2, 47.1)
    if a > 0:
        obj(im, "rosetta", 520, 540, 900, a * r(t, 34.3, 0.7)); x = 1400
        plaque(d, x, 250, "1799", 130, a * r(t, 34.4), sp=8); text(d, x, 410, "FRENCH SOLDIERS REBUILDING A FORT", 32, a * r(t, 35.3), sp=6, **GR)
        text(d, x, 540, "A BROKEN SLAB", 60, a * r(t, 37.6), sp=5); text(d, x, 620, "WITH THREE SCRIPTS ON IT", 40, a * r(t, 38.8), sp=5)
        text(d, x, 800, "ONE VERSION IS GREEK", 44, a * r(t, 43.4), sp=5); plaque(d, x, 920, "A KEY", 80, a * r(t, 45.6), sp=8)
    a = win(t, 47.1, 53.7, fo=0.2)
    if a > 0:
        obj(im, "champ", 560, 540, 900, a * r(t, 47.2, 0.6)); x = 1420
        plaque(d, x, 300, "1822", 150, a * r(t, 47.3), sp=8); text(d, x, 500, "CHAMPOLLION", 90, a * r(t, 48.9), sp=4); text(d, x, 600, "CRACKS IT", 40, a * r(t, 49.8), sp=10, **GR)
        text(d, x, 800, "EGYPT STARTS TALKING AGAIN", 46, a * r(t, 51.0), sp=4)
    a = win(t, 89.5, 99.9, fi=0.4, fo=0.1)
    if a > 0:
        lg = LOGO.resize((150, 150), Image.LANCZOS); k = a * r(t, 89.6, 0.5)
        if k < 1: lg.putalpha(lg.getchannel("A").point(lambda v: int(v * k)))
        im.paste(lg, (cx - 75, 110), lg)
        text(d, cx, 390, "THAT WAS EGYPT", 110, a * r(t, 89.8), sp=6, dy=16)
        text(d, cx, 520, "NEXT TIME", 36, a * r(t, 91.6), sp=10, **GR); text(d, cx, 610, "CARTHAGE", 76, a * r(t, 92.5), sp=6)
        plaque(d, cx, 770, "SUBSCRIBE", 80, a * r(t, 95.7), sp=8)
        text(d, cx, 920, "AND TELL US IN THE COMMENTS", 34, a * r(t, 96.7), sp=8, **GR); text(d, cx, 985, "WHICH CIVILIZATION YOU WANT TO SEE NEXT", 40, a * r(t, 97.6), sp=6)
    return im
def _three(k): return only(f"12p{k}", lambda im, d: BP(d, 110, 820 + k * 78, ["A RIVER THAT FEEDS YOU, DESERTS THAT GUARD YOU", "ONE IDEA: THERE IS AN ORDER, AND THE KING KEEPS IT", "WRITE EVERYTHING DOWN"][k], 30, anchor="l"))
def _conq(k):
    def fn(im, d):
        x = 60; f = font(True, 34)
        for j in range(k): x += tw(d, CONQ[j], f, 3) + 34 * 0.9 + 26
        BP(d, x + 34 * 0.45, 990, CONQ[k], 34, anchor="l")
    return only(f"12c{k}", fn)
def _dc(im, d): put(im, "crownfig", 300, 480, h=640); BP(d, 300, 850, "THE DOUBLE CROWN", 28, sp=5)
S12 = dict(n=12, gfx=g12, gfx_windows=[(0, 19.4), (34.1, 53.9), (89.4, 99.9)], overlays=[(M("12a_what_remains"), 19.3, 22.7, False, 1.5), (RC("R15m"), 22.7, 34.2, True), (M("12b_what_remains"), 53.8, 89.7, False)], stills=[
    (lt("12a", "A PRIEST CARVES A SHORT TEXT", small="THE ISLAND OF PHILAE, AD 394"), 22.9, 26.0), (lt("12b", "THE LAST HIEROGLYPHIC INSCRIPTION WE KNOW"), 26.5, 30.1),
    (lt("12c", "SILENT FOR 1,400 YEARS", plq=True), 30.5, 33.8),
    (_three(0), 58.2, 78.3), (_three(1), 62.1, 78.3), (_three(2), 70.0, 78.3),
    (_conq(0), 78.6, 88.0), (_conq(1), 79.4, 88.0), (_conq(2), 80.1, 88.0), (_conq(3), 80.9, 88.0), (_conq(4), 81.8, 88.0), (still("12d", _dc), 83.6, 88.0)])

SPECS = {1: S1, 2: S2, 3: S3, 4: S4, 5: S5, 6: S6, 7: S7, 8: S8, 9: S9, 10: S10, 11: S11, 12: S12}
for k, s in SPECS.items(): s.setdefault("card", card(k))

def preview(k, t):
    """what the finished frame looks like at voice time t of chapter k (graphics / overlay frame + stills)"""
    import subprocess, io
    s = SPECS[k]; im = None
    for f, t0, t1, snd, *rest in s["overlays"]:
        if t0 <= t < t1:
            ss = (rest[0] if rest else 0) + (t - t0)
            b = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{ss:.3f}", "-i", f, "-frames:v", "1", "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            if b: im = Image.open(io.BytesIO(b)).convert("RGBA")
    if im is None: im = (s["gfx"](t) if s.get("gfx") else blank()[0]).convert("RGBA")
    for mk, t0, t1 in s.get("stills", []):
        if t0 <= t <= t1: im.alpha_composite(Image.open(mk()).convert("RGBA"))
    return im.convert("RGB")
if __name__ == "__main__":
    import sys
    k = int(sys.argv[1]); ts = [float(x) for x in sys.argv[2:]]; ims = [preview(k, t).resize((640, 360), Image.LANCZOS) for t in ts]
    sh = Image.new("RGB", (4 * 640, ((len(ims) + 3) // 4) * 360))
    for i, (t, im) in enumerate(zip(ts, ims)): ImageDraw.Draw(im).text((8, 6), f"ch{k} {t}", fill=(255, 60, 60)); sh.paste(im, (i % 4 * 640, i // 4 * 360))
    sh.save(f"{R}/chk/pv_{k}.jpg", quality=86)
