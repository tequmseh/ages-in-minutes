"""Ancient Rome in 20 Minutes: map scenes, timed to the recorded voiceover (chapter seconds). Windows come from ../layout.json (one source of numbers).
usage: python3 ro_scenes.py list | still name@t,t (chapter seconds) | sheet tag [prefixes] | render names..."""
from ro_base import *
BLACK = (17, 17, 17); PAPER = (250, 247, 240)
_LAY = json.load(open(os.path.join(HERE, "../layout.json")))
WIN = {}
for _ch, _v in _LAY.items():
    if not isinstance(_v, dict) or "segs" not in _v: continue
    for _s in _v["segs"]:
        if _s[2] == "MAP": WIN.setdefault(_s[3], []).append((int(_ch), _s[0], _s[1]))
def win(i): w = WIN[i]; return w[0][0], min(a for _, a, _b in w), max(b for _, _a, b in w)
def sc(i, tag, cam, masks, **kw): ch, a, b = win(i); return scene(f"{i}_{tag}", ch, a, b, cam, masks, **kw)

# ---------------------------------------------------------------- helpers
def blank(fr, color=BLACK):
    fr.im.paste(color, (0, 0, fr.im.size[0], fr.im.size[1])); fr.d = ImageDraw.Draw(fr.im)
def rect(fr, x0, y0, x1, y1, color, a=1.0):
    alpha_draw(fr, lambda d, c: d.rectangle([s(x0), s(y0), s(x1), s(y1)], fill=c), color, a)
def poly(fr, pts, color, a=1.0):
    alpha_draw(fr, lambda d, c: d.polygon([(s(x), s(y)) for x, y in pts], fill=c), color, a)
def lship(fr, x, y, k=1.0, a=1.0, color=INK, sail=PAPER, flip=False, stripes=NOR):
    """small longship glyph: curved hull, mast, striped square sail; x, y = middle of the waterline"""
    if a <= 0: return
    f = -1 if flip else 1
    hull = [(-24, -9), (-21, -11), (-17, -3), (-9, 1), (9, 1), (17, -3), (22, -12), (25, -10), (21, 1), (13, 6), (-13, 6), (-20, 1)]
    poly(fr, [(x + f * px * k, y + py * k) for px, py in hull], color, a)
    rect(fr, x - 1.1 * k, y - 26 * k, x + 1.1 * k, y + 1 * k, color, a)
    rect(fr, x - 12 * k, y - 25 * k, x + 12 * k, y - 8 * k, sail, a)
    if k >= 0.8:
        for i in (-8, 0, 8): rect(fr, x + (i - 2) * k, y - 25 * k, x + (i + 2) * k, y - 8 * k, stripes, a)
    alpha_draw(fr, lambda d, c: d.rectangle([s(x - 12 * k), s(y - 25 * k), s(x + 12 * k), s(y - 8 * k)], outline=c, width=max(1, s(1.2 * k))), color, a)
def gship(fr, lon, lat, dx=0, dy=0, **kw):
    x, y = P(fr.cam, lon, lat); lship(fr, x + dx, y + dy, **kw)
def sail_along(fr, path, q, k=0.8, a=1.0, **kw):
    """ship glyph at fraction q of a lon/lat path"""
    if a <= 0 or q <= 0: return
    p = partial(proj(fr.cam, path, 1), min(q, 1.0))[-1]; lship(fr, p[0], p[1] - 4, k=k, a=a, **kw)
def tline(fr, a, k, left="", right="", title="", x0=210, w=1500, y0=1012, ra=1.0):
    """timeline strip in the bottom safe band: black strip, yellow bar growing with k"""
    if a <= 0: return
    rect(fr, x0 - 60, y0 - 52, x0 + w + 60, y0 + 52, BLACK, a * 0.94)
    rect(fr, x0, y0 - 4, x0 + w, y0 + 4, (70, 72, 75), a)
    rect(fr, x0, y0 - 9, x0 + w * max(0.0, min(1.0, k)), y0 + 9, YELLOW, a)
    for xx in (x0, x0 + w * max(0.0, min(1.0, k))): rect(fr, xx - 2, y0 - 18, xx + 2, y0 + 18, YELLOW, a)
    if left: T(fr, x0, y0 - 32, left, size=22, w="b", sp=2, color=WHITE, a=a)
    if right: T(fr, x0 + w, y0 - 32, right, size=22, w="b", sp=2, color=WHITE, a=a * ra, anchor="r")
    if title: T(fr, x0 + w / 2, y0 + 33, title, size=17, w="s", sp=4, color=WHITE, a=a * ra, anchor="m")
def scatter(fr, key, n, seed=3, box=None):
    """n random lon/lat points inside mask `key` (fixed camera only); cached on the scene"""
    c = getattr(fr.scene, "_sc", None)
    if c is None: c = fr.scene._sc = {}
    k = (key, n, seed, fr.cam)
    if k not in c:
        m = np.asarray(fr.masks[key]); ys, xs = np.nonzero(m[::4, ::4] > 200); rng = np.random.default_rng(seed); out = []
        if len(xs):
            idx = rng.choice(len(xs), size=min(n, len(xs)), replace=False)
            out = [((xs[i] * 4 + 2) / SS, (ys[i] * 4 + 2) / SS) for i in idx]
        c[k] = out
    return c[k]
def dots_px(fr, pts, a_fn, r=3.2, color=INK, ring=WHITE):
    for i, (x, y) in enumerate(pts):
        a = a_fn(i)
        if a <= 0: continue
        if ring: circ(fr, x, y, r + 1.6, ring, a)
        circ(fr, x, y, r, color, a)
def circ(fr, x, y, r, color=None, a=1.0, outline=None, width=2):
    if a <= 0: return
    if color is not None: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=c), color, a)
    if outline is not None: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], outline=c, width=s(width)), outline, a)
def col(fr, x, y, items, size=22, gap=58, anchor="l", light=True, first_dark=False, dim=1.0):
    """column of plaques: items = [(text, t0)]"""
    for i, (txt, t0) in enumerate(items):
        PQ(fr, x, y + i * gap, txt, a=fr.R(t0, 0.4) * dim, size=size, anchor=anchor, light=light and not (first_dark and i == 0), pad=(12, 8))
def arrow(fr, pts, t0, d=1.4, width=4.2, a=1.0, n=10, **kw):
    gline(fr, smooth(pts, n) if len(pts) > 2 else pts, width=width, frac=fr.R(t0, d), arrow=True, halo=kw.pop("halo", WHITE), a=a, **kw)
def out(fr, t0, d=0.5): return 1 - fr.R(t0, d)

def rome(fr, a=1.0, label=True, r=7, side="r", size=22, **kw):
    x, y = P(fr.cam, *C["ROME"]); circ(fr, x, y, r + 3, WHITE, a); circ(fr, x, y, r, ROM_D, a)
    if label: city(fr, "ROME", a=a, r=r, side=side, size=size, dot=None, ring=None, icon=False, **kw)
def town(fr, name, a=1.0, r=5, color=INK, **kw): city(fr, name, a=a, r=r, dot=color, icon=False, **kw)
def tdot(fr, ll, a=1.0, r=4.2, color=INK, ring=WHITE):
    x, y = P(fr.cam, *ll); circ(fr, x, y, r + 1.8, ring, a); circ(fr, x, y, r, color, a)
def xmark(fr, name, a=1.0, **kw): cross(fr, *C[name], a=a, **kw)

# ---------------------------------------------------------------- the city plan (schematic: hills, river, walls)
TIBER = [(12.4850, 41.9480), (12.4760, 41.9420), (12.4669, 41.9355), (12.4655, 41.9290), (12.4690, 41.9240), (12.4745, 41.9180), (12.4742, 41.9120), (12.4760, 41.9055),
         (12.4720, 41.9035), (12.4665, 41.9017), (12.4630, 41.8990), (12.4640, 41.8965), (12.4665, 41.8935), (12.4705, 41.8922), (12.4745, 41.8910), (12.4777, 41.8905),
         (12.4795, 41.8888), (12.4790, 41.8855), (12.4762, 41.8832), (12.4735, 41.8790), (12.4715, 41.8745), (12.4750, 41.8690), (12.4740, 41.8640)]
HILLS = dict(CAPITOLINE=(12.4829, 41.8934, .0022, .0019, 30), PALATINE=(12.4873, 41.8890, .0031, .0026, 0), AVENTINE=(12.4815, 41.8823, .0046, .0030, 20),
             CAELIAN=(12.4968, 41.8850, .0056, .0026, -15), ESQUILINE=(12.5012, 41.8950, .0052, .0040, 0), VIMINAL=(12.4968, 41.8996, .0042, .0017, -25), QUIRINAL=(12.4905, 41.9022, .0058, .0019, -30))
WALL = [(12.4790, 41.8890), (12.4805, 41.8945), (12.4840, 41.8975), (12.4870, 41.9025), (12.4925, 41.9060), (12.4990, 41.9075), (12.5030, 41.9030), (12.5050, 41.8975), (12.5055, 41.8935),
        (12.5030, 41.8890), (12.5000, 41.8850), (12.4985, 41.8825), (12.4930, 41.8800), (12.4880, 41.8790), (12.4830, 41.8775), (12.4775, 41.8795), (12.4760, 41.8830), (12.4775, 41.8865), (12.4790, 41.8890)]
CLOACA = [(12.4895, 41.8950), (12.4870, 41.8934), (12.4853, 41.8922), (12.4835, 41.8908), (12.4818, 41.8898), (12.4797, 41.8888)]
FORUM = (12.4853, 41.8922); MILVIAN = (12.4669, 41.9355)
PLAN = cam_box(12.452, 12.518, 41.872, 41.912); PLANW = cam_box(12.43, 12.56, 41.868, 41.95)
def ell(lon, lat, rx, ry, ang, k=1.0, n=40):
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang)); out = []
    for i in range(n):
        t = 2 * math.pi * i / n; u, v = rx * k * math.cos(t), ry * k * math.sin(t) * (1 + 0.12 * math.sin(3 * t + lon * 900))
        out.append((lon + u * c - v * s_, lat + (u * s_ + v * c)))
    return out
def gpoly(fr, lonlat, color, a=1.0):
    p = proj(fr.cam, lonlat, 1); poly(fr, [tuple(q) for q in p], color, a)
def plan(fr, hi=None, hi_a=0.0, hills_a=1.0):
    """river, island and the seven hills; hi = hill name to highlight"""
    for nm, (lon, lat, rx, ry, ang) in HILLS.items():
        gpoly(fr, ell(lon + rx * 0.10, lat - ry * 0.14, rx, ry, ang, 1.12), (150, 132, 98), 0.34 * hills_a)
        gpoly(fr, ell(lon, lat, rx, ry, ang), (236, 222, 184), 0.80 * hills_a)
        gpoly(fr, ell(lon - rx * 0.08, lat + ry * 0.10, rx, ry, ang, 0.62), (246, 236, 206), 0.75 * hills_a)
        if nm == hi and hi_a > 0: gpoly(fr, ell(lon, lat, rx, ry, ang), ROM, 0.62 * hi_a)
    gline(fr, smooth(TIBER, 6), color=(62, 104, 126), width=max(7.0, 0.00105 * fr.cam[2]))
    gline(fr, smooth(TIBER, 6), color=(104, 160, 184), width=max(5.0, 0.00085 * fr.cam[2]))
    gpoly(fr, ell(12.4777, 41.8905, .0013, .00042, -18), (236, 222, 184), 1.0)
ALLIES = [(12.71, 41.80), (12.89, 41.84), (12.80, 41.96), (12.40, 42.02), (12.10, 42.0), (14.25, 41.08), (14.25, 40.84), (11.76, 42.25), (14.05, 40.85), (13.61, 41.65), (12.63, 41.45),
          (13.41, 42.08), (12.74, 42.73), (13.25, 41.29), (14.78, 41.13), (12.11, 43.11), (13.02, 43.58)]
APPIA = [C["ROME"], (12.72, 41.72), (13.02, 41.47), (13.25, 41.29), (13.60, 41.26), (13.83, 41.16), C["CAPUA"]]
ROADS = [[C["ROME"], C["CAPUA"], (15.6, 41.1), C["BRUNDISIUM"]], [C["ROME"], (12.6, 43.0), C["ARIMINUM"], (11.3, 44.5), C["MEDIOLANUM"]],
         [C["ROME"], (10.4, 43.7), (8.93, 44.41), C["MASSILIA"], C["NARBO"], C["TARRACO"], C["SAGUNTUM"], C["NEWCARTHAGE"], C["CORDUBA"], C["GADES"]],
         [C["MASSILIA"], C["LUGDUNUM"], C["LUTETIA"], (1.6, 50.7)], [C["LUGDUNUM"], C["TRIER"], C["COLONIA"]], [(1.3, 51.1), C["LONDINIUM"], C["EBORACUM"]],
         [C["MEDIOLANUM"], C["AQUILEIA"], C["SIRMIUM"], (21.9, 43.3), (23.3, 42.7), C["ADRIANOPLE"], C["CONSTANTINOPLE"]], [C["DYRRACHIUM"], C["THESSALONICA"], C["CONSTANTINOPLE"]],
         [(29.2, 40.9), C["NICAEA"], C["ANCYRA"], (35.5, 38.7), C["ANTIOCH"], C["DAMASCUS"], C["JERUSALEM"], C["PELUSIUM"], C["ALEXANDRIA"]],
         [C["ALEXANDRIA"], C["CYRENE"], C["LEPTIS"], C["CARTHAGE"], C["CAESAREA"], C["TINGIS"]], [C["NARBO"], C["BURDIGALA"]], [C["TARRACO"], (-0.88, 41.65), (-5.57, 42.6)],
         [C["AQUILEIA"], C["CARNUNTUM"]], [C["EPHESUS"], (30.5, 38.8), C["ANCYRA"]], [C["THESSALONICA"], C["ATHENS"], C["CORINTH"]], [C["COLONIA"], C["MOGONTIACUM"], (7.6, 47.56), C["MEDIOLANUM"]]]
LEGIONS = [(-1.08, 53.96), (-2.89, 53.19), (-3.0, 51.6), (6.1, 51.75), (7.1, 50.73), (8.27, 50.0), (7.75, 48.58), (16.37, 48.21), (16.87, 48.11), (18.1, 47.73), (19.04, 47.5),
           (20.46, 44.82), (21.2, 44.7), (25.35, 43.62), (27.26, 44.12), (28.1, 45.2), (23.58, 46.07), (22.8, 45.5), (38.35, 38.35), (39.3, 39.9), (37.9, 37.05), (36.6, 36.4), (38.0, 35.3),
           (35.22, 31.78), (35.2, 32.6), (36.48, 32.52), (29.95, 31.15), (31.2, 30.0), (6.0, 35.42), (-5.57, 42.6)]
HANNIBAL = [C["NEWCARTHAGE"], C["SAGUNTUM"], (0.6, 40.8), (2.2, 41.6), (2.9, 42.45), (3.6, 43.5), (4.75, 44.1), (5.3, 45.0), (6.0, 45.3), (6.9, 45.1), (7.7, 45.07), (9.6, 45.05), (10.9, 44.4),
            (11.4, 43.7), (12.1, 43.14), (13.3, 42.6), (14.6, 42.0), (15.6, 41.5), C["CANNAE"]]
SPART = [C["CAPUA"], (14.43, 40.82), (15.3, 40.4), (16.2, 40.0), (16.6, 40.9), (15.2, 41.7), (13.6, 42.6), (12.4, 43.6), C["MUTINA"], (12.2, 43.5), (13.8, 42.0), (15.4, 40.9), (16.4, 39.6),
         (15.9, 38.3), (16.5, 39.4), (15.6, 40.2), (15.2, 40.6)]
FRONT_RHINE = [(4.3, 52.0), (6.0, 51.85), (6.7, 51.2), (7.0, 50.7), (7.6, 50.3), (8.3, 50.0), (8.3, 49.2), (7.9, 48.5), (7.6, 47.6)]
FRONT_DAN = [(11.6, 48.9), (12.1, 49.0), (13.4, 48.55), (14.3, 48.3), (15.6, 48.4), (16.4, 48.2), (17.2, 48.1), (18.1, 47.75), (18.9, 47.8), (19.05, 47.4), (18.95, 46.2), (19.0, 45.5),
             (20.4, 44.8), (21.4, 44.7), (22.6, 44.5), (22.9, 43.85), (24.8, 43.75), (25.4, 43.65), (26.1, 43.95), (27.3, 44.15), (28.0, 45.2), (28.3, 45.45), (29.7, 45.2)]
FRONT_EAST = [(41.5, 41.5), (41.0, 40.2), (40.2, 39.4), (39.0, 38.6), (38.5, 37.5), (39.6, 36.9), (41.2, 37.1), (41.6, 36.3), (40.4, 35.2), (39.5, 34.2), (38.0, 33.2), (37.2, 32.0), (36.6, 30.0), (35.0, 29.5)]

ITA = cam_box(6.3, 19.5, 36.3, 47.2); CENT = cam_box(9.6, 17.4, 39.9, 44.5); MED = cam_box(-10.5, 41, 29, 48.5); EMPC = cam_box(-11, 50, 23.5, 56.5)

# ================= chapter 1
@sc("01a", "italy_tiber", mover([(0, ITA), (5.0, ITA), (11.5, cam_box(11.3, 13.7, 41.35, 42.45)), (21, cam_box(11.3, 13.7, 41.35, 42.45))]), {})
def _(fr, t):
    z = fr.cam[2] > ITA[2] * 2.2
    region(fr, 12.6, 43.4, "ITALY", a=fr.R(2.2, 0.5) * (0 if z else 1), size=34)
    if z:
        modern(fr, 12.47, 42.20, "TIBER", a=fr.R(10.6, 0.5), size=20, color=SEA_T, dx=58)
        x, y = P(fr.cam, *C["ROME"])
        for i, (dx, dy) in enumerate(((-10, -30), (16, -34), (34, -16), (36, 8), (20, 28), (-6, 30), (-4, 0))): circ(fr, x + dx + 22, y + dy, 13, (236, 222, 184), fr.R(11.6 + i * 0.1, 0.4) * 0.9, outline=(150, 132, 98), width=1.6)
        rome(fr, a=fr.R(13.1, 0.4), label=False, r=8)
        PQ(fr, x - 150, y - 4, "ROME", a=fr.R(13.3, 0.4), size=34)
        PQ(fr, 1380, 330, "21 APRIL 753 BC", a=fr.R(15.2, 0.4), size=30, light=True); PQ(fr, 1380, 400, "ROMULUS", a=fr.R(18.3, 0.4), size=30)
        pulse(fr, C["ROME"], 13.1, 2.4, color=ROM_D)

@sc("01c", "hills_plan", PLAN, {}, rivers=False)
def _(fr, t):
    plan(fr, hi="PALATINE", hi_a=fr.R(49.3, 0.6))
    modern(fr, 12.4648, 41.8905, "TIBER", size=20, color=PAPER)
    gline(fr, [(12.4848, 41.8906), (12.4862, 41.8914), (12.4880, 41.8915), (12.4896, 41.8908)], color=INK, width=6, frac=fr.R(51.0, 1.2), halo=WHITE)
    PQL(fr, 12.4873, 41.8890, "PALATINE HILL", dx=330, dy=10, a=fr.R(49.5, 0.4) * out(fr, 60), size=28); PQL(fr, 12.4873, 41.8890, "MID-700s BC", dx=330, dy=74, a=fr.R(52.6, 0.4) * out(fr, 60), size=26, light=True)
    a = fr.R(72.2, 0.6); x, y = P(fr.cam, *FORUM)
    if a > 0: gpoly(fr, ell(FORUM[0], FORUM[1], .0016, .0008, 28), ROM, 0.75 * a)
    gline(fr, smooth(CLOACA, 6), color=(40, 78, 110), width=6, frac=fr.R(67.2, 3.4), halo=WHITE, dash=(16, 9))
    PQL(fr, *CLOACA[0], "CLOACA MAXIMA", dx=250, dy=-40, a=fr.R(70.2, 0.4), size=26); PQL(fr, *FORUM, "FORUM", dx=-150, dy=-60, a=fr.R(73.0, 0.4), size=26, light=True)

@sc("01d", "etruria", CENT, dict(etr=ETR))
def _(fr, t):
    terr(fr, "etr", ETRC, fr.R(62.9, 0.8)); region(fr, 11.35, 43.05, "ETRUSCANS", a=fr.R(63.3, 0.5), size=26)
    rome(fr); PQL(fr, *C["ROME"], "SEVEN KINGS", dx=250, dy=70, a=fr.R(59.7, 0.4), size=30)

# ================= chapter 2
@sc("02a", "plebs_walk_out", PLANW, {}, rivers=False)
def _(fr, t):
    plan(fr); gline(fr, WALL, color=(110, 96, 74), width=3, a=0.7)
    live(fr, 39.0, 46.0); rng = np.random.default_rng(4)
    for i in range(46):
        o = rng.normal(0, 1, 4); st = (12.488 + o[0] * .004, 41.891 + o[1] * .003); en = (12.531 + o[2] * .0035, 41.937 + o[3] * .0022)
        q = ease(min(1.0, max(0.0, (fr.v - 40.2 - i * 0.05) / 3.6))); mid = (st[0] + (en[0] - st[0]) * q, st[1] + (en[1] - st[1]) * q + 0.004 * math.sin(math.pi * q))
        tdot(fr, mid, r=4.0, color=ROM_D)
    PQ(fr, 330, 160, "494 BC", a=fr.R(39.1, 0.4), size=34); PQ(fr, 330, 250, "TRIBUNES", a=fr.R(46.2, 0.4), size=30, light=True)
    PQ(fr, 330, 330, "VETO", a=fr.R(51.3, 0.4), size=34); PQ(fr, 330, 410, "I FORBID", a=fr.R(52.6, 0.3), size=30, light=True)

@sc("02b", "gauls", cam_box(9.4, 15.0, 41.2, 45.4), dict(lat=LAT))
def _(fr, t):
    terr(fr, "lat", ROM); rome(fr)
    PQ(fr, 330, 170, "390 BC", a=fr.R(64.6, 0.4), size=34)
    arrow(fr, [(10.6, 44.9), (11.4, 44.2), C["CLUSIUM"], (12.45, 42.25), (12.5, 42.0)], 66.6, 3.4, color=GAU, width=7)
    region(fr, 10.75, 45.15, "GAULS", a=fr.R(68.6, 0.4), size=28, color=GAU)
    pulse(fr, C["ROME"], 72.4, 2.6, color=ROM_D); PQL(fr, *C["ROME"], "CAPITOLINE HILL", dx=270, dy=70, a=fr.R(72.9, 0.4), size=28)

@sc("02c", "wall", PLAN, {}, rivers=False)
def _(fr, t):
    plan(fr); gline(fr, WALL, color=ROM_D, width=8, frac=fr.R(97.3, 3.6), halo=WHITE)
    PQ(fr, 330, 170, "ELEVEN KILOMETRES", a=fr.R(99.6, 0.4), size=30); PQ(fr, 330, 250, "EIGHT HUNDRED YEARS", a=fr.R(104.2, 0.4), size=30, light=True)

# ================= chapter 3
@sc("03a", "neighbours", CENT, dict(lat=LAT, etr=ETR, sam=SAMN))
def _(fr, t):
    terr(fr, "lat", ROM, fr.R(5.6, 0.6)); terr(fr, "etr", ETRC, fr.R(6.8, 0.6)); terr(fr, "sam", SAM, fr.R(8.2, 0.6))
    region(fr, 13.05, 41.47, "LATINS", a=fr.R(5.9, 0.4), size=20, dy=30); region(fr, 11.35, 43.05, "ETRUSCANS", a=fr.R(7.0, 0.4), size=26); region(fr, 14.55, 41.45, "SAMNITES", a=fr.R(8.4, 0.4), size=24)
    rome(fr)

@sc("03b", "allies", CENT, dict(lat=LAT))
def _(fr, t):
    terr(fr, "lat", ROM); k = fr.R(16.4, 1.4)
    for i, ll in enumerate(ALLIES):
        tdot(fr, ll, r=6, color=mix(ALLY, (120, 120, 120), min(1.0, max(0.0, k * 1.6 - i * 0.03))))
        if fr.v >= 23.4: gline(fr, arc(ll, C["ROME"], 0.12), color=ROM_D, width=3.4, frac=fr.R(23.8 + i * 0.07, 1.2), arrow=True, halo=WHITE)
    rome(fr)
    PQ(fr, 1500, 200, "ALLIES", a=fr.R(16.9, 0.4), size=34); PQ(fr, 1500, 285, "NO TRIBUTE", a=fr.R(22.4, 0.4), size=30, light=True); PQ(fr, 1500, 365, "SOLDIERS", a=fr.R(24.4, 0.4), size=30)

@sc("03c", "via_appia", cam_box(11.9, 14.9, 40.65, 42.25), dict(lat=LAT))
def _(fr, t):
    gline(fr, smooth(APPIA, 8), color=INK, width=7, frac=fr.R(32.6, 4.6), halo=WHITE)
    rome(fr); town(fr, "CAPUA", a=fr.R(36.4, 0.4), r=6, size=24, side="b")
    PQ(fr, 420, 170, "312 BC", a=fr.R(32.6, 0.4), size=34); PQ(fr, 420, 255, "VIA APPIA", a=fr.R(34.4, 0.4), size=30, light=True)

@sc("03d", "road_network", EMPC, dict(emp=EMP117), res="50")
def _(fr, t):
    terr(fr, "emp", ROM, 0.55, border=False)
    for i, rd in enumerate(ROADS): gline(fr, smooth(rd, 6), color=PAPER, width=3.6, frac=fr.R(51.2 + i * 0.12, 2.6), halo=ROM_D)
    rome(fr, label=False); PQ(fr, 960, 130, "EIGHTY THOUSAND KILOMETRES", a=fr.R(53.6, 0.4), size=32)

@sc("03e", "pyrrhus", cam_box(13.2, 22.6, 37.6, 42.6), dict(ep=EPIRUS, lat=M(PEN_P)))
def _(fr, t):
    terr(fr, "ep", GRK, fr.R(60.4, 0.6)); region(fr, 20.6, 39.75, "EPIRUS", a=fr.R(60.6, 0.4) * 0 , size=22)
    town(fr, "TARENTUM", a=fr.R(58.4, 0.4), r=6, size=24, side="t"); pulse(fr, C["TARENTUM"], 59.0, 2.4, color=GRK)
    arrow(fr, arc((20.2, 39.6), (17.6, 40.25), -0.18), 60.6, 1.5, color=GRK, width=7)
    PQ(fr, 330, 170, "280 BC", a=fr.R(57.0, 0.4) * out(fr, 62.3), size=34); PQL(fr, 20.6, 39.75, "PYRRHUS", dy=70, a=fr.R(61.5, 0.4), size=28)
    for nm, ll, t0 in (("", (16.67, 40.22), 70.3), ("", (15.56, 41.2), 71.0)): cross(fr, *ll, a=fr.R(t0, 0.4), color=GRK, r=13, width=6)
    PQ(fr, 960, 820, "ONE MORE VICTORY LIKE THAT,", a=fr.R(72.4, 0.4), size=28, light=True); PQ(fr, 960, 890, "AND WE ARE FINISHED", a=fr.R(74.2, 0.4), size=28)

@sc("03f", "peninsula", ITA, dict(core=U(LAT, ETR, SAMN), pen=PEN))
def _(fr, t):
    terr(fr, "core", ROM, out(fr, 80.0, 3.0)); terr(fr, "pen", ROM, fr.R(79.4, 4.4)); rome(fr)
    PQ(fr, 420, 200, "275 BC", a=fr.R(79.2, 0.4), size=34); PQ(fr, 420, 290, "THE WHOLE ITALIAN PENINSULA", a=fr.R(84.4, 0.4), size=26, light=True, anchor="m")

# ================= chapter 4
@sc("04a", "sicily_carthage", cam_box(4.5, 19.5, 33.4, 43.6), dict(pen=PEN, car=CARTH, sic=SICILY))
def _(fr, t):
    terr(fr, "pen", ROM); terr(fr, "car", CAR, fr.R(5.4, 0.8)); terr(fr, "sic", ROM, fr.R(30.4, 1.4)); rome(fr)
    region(fr, 14.1, 37.55, "SICILY", a=fr.R(3.6, 0.4), size=26, color=mix(WHITE, INK, fr.R(30.4, 1.4)))
    town(fr, "CARTHAGE", a=fr.R(5.6, 0.4), r=6.5, size=26, side="b", color=INK)
    PQ(fr, 330, 170, "264 BC", a=fr.R(12.4, 0.4) * out(fr, 20), size=34); pulse(fr, C["MESSANA"], 13.6, 3.0, color=ROM_D)
    PQ(fr, 330, 170, "TWENTY-THREE YEARS", a=fr.R(29.8, 0.4), size=28, anchor="m"); PQ(fr, 330, 250, "FIRST PROVINCE", a=fr.R(32.4, 0.4), size=28, light=True)

@sc("04c", "hannibal", cam_box(-7.5, 19.5, 35.6, 47.2), dict(it=U(PEN, SICILY, SARD, CORS), car=CARTH218))
def _(fr, t):
    terr(fr, "it", ROM); terr(fr, "car", CAR); rome(fr); town(fr, "CARTHAGE", r=5.5, size=20, side="b")
    gline(fr, smooth(HANNIBAL, 8), color=CAR, width=7, frac=fr.R(40.4, 5.0), halo=WHITE, arrow=fr.v < 45.6)
    PQ(fr, 330, 170, "218 BC", a=fr.R(35.7, 0.4) * out(fr, 45.7), size=34); PQ(fr, 330, 255, "HANNIBAL", a=fr.R(37.4, 0.4) * out(fr, 45.7), size=30, light=True)
    region(fr, 7.3, 46.2, "ALPS", a=fr.R(42.4, 0.4), size=22, dy=-34)
    PQ(fr, 330, 170, "2 AUGUST 216 BC", a=fr.R(46.3, 0.4), size=30, anchor="m"); xmark(fr, "CANNAE", a=fr.R(48.6, 0.4), color=INK, r=13, width=6)
    PQL(fr, *C["CANNAE"], "CANNAE", dx=110, dy=-44, a=fr.R(48.8, 0.4), size=28); pulse(fr, C["CANNAE"], 48.8, 3.0)

@sc("04e", "alliance_holds", ITA, dict(it=U(PEN, SICILY)))
def _(fr, t):
    terr(fr, "it", ROM); rome(fr)
    for i, ll in enumerate(ALLIES + [(16.87, 41.12), (15.8, 40.64), (14.78, 41.13), (16.6, 39.3), (13.9, 42.35), (13.5, 43.6), (11.9, 43.46), (10.4, 43.72)]): tdot(fr, ll, r=5, color=mix(PAPER, ALLY, min(1.0, max(0.0, fr.R(65.3, 2.6) * 1.8 - i * 0.03))), ring=ROM_D)
    PQ(fr, 420, 200, "THE ALLIANCE SYSTEM HOLDS", a=fr.R(68.8, 0.4), size=28, anchor="m")

@sc("04f", "zama", cam_box(5.6, 17.2, 34.4, 39.7), dict(it=U(PEN, SICILY, SARD), car=U(COAST(NAFR_COAST, 1.1), M(CARTH_HOME))))
def _(fr, t):
    terr(fr, "it", ROM); terr(fr, "car", CAR); town(fr, "CARTHAGE", r=6.5, size=24, side="r")
    arrow(fr, [C["LILYBAEUM"], (11.2, 37.6), C["UTICA"], (9.7, 36.6), C["ZAMA"]], 71.2, 3.0, color=ROM_D, width=7)
    xmark(fr, "ZAMA", a=fr.R(74.3, 0.4), r=13, width=6); PQL(fr, *C["ZAMA"], "ZAMA", dx=-110, dy=50, a=fr.R(74.5, 0.4), size=30); PQL(fr, *C["ZAMA"], "202 BC", dx=-110, dy=116, a=fr.R(75.7, 0.4), size=28, light=True)

@sc("04g", "carthage_corinth", cam_box(4, 27.5, 33, 43.2), dict(rm=ROME146))
def _(fr, t):
    terr(fr, "rm", ROM); rome(fr)
    PQ(fr, 960, 130, "146 BC", a=fr.R(89.5, 0.4), size=36)
    for nm, t0, dx, dy in (("CARTHAGE", 93.1, 0, 64), ("CORINTH", 95.6, 0, 64)):
        x, y = P(fr.cam, *C[nm]); k = fr.R(t0, 0.9); circ(fr, x, y, 11, WHITE); circ(fr, x, y, 8, mix(BLACK, PAPER, k)); pulse(fr, C[nm], t0, 2.2, color=BLACK)
        PQ(fr, x + dx, y + dy, nm, a=fr.R(t0 + 0.2, 0.4), size=28)
        cross(fr, *C[nm], a=k, r=20, width=6, color=BLACK)

@sc("04h", "mare_nostrum", MED, dict(a=ROME146, b=Dm(EMP14, ROME146)), res="50")
def _(fr, t):
    terr(fr, "a", ROM, border=False); terr(fr, "b", ROM, fr.R(98.9, 2.6), border=False); rome(fr, label=False)
    TL(fr, 18.6, 34.4, "MARE NOSTRUM", size=40, w="b", color=PAPER, anchor="m", sp=8, a=fr.R(100.4, 0.5)); PQ(fr, 960, 880, "OUR SEA", a=fr.R(102.5, 0.3), size=34)

# ================= chapter 5
@sc("05a", "silver_slaves", MED, dict(a=ROME146), res="50")
def _(fr, t):
    terr(fr, "a", ROM); rome(fr, label=False)
    for i, st in enumerate(((-3.5, 38.5), (9.8, 36.4), (22.6, 38.6), (27.5, 38.4), (5.0, 43.6), (9.0, 39.8))): arrow(fr, arc(st, (12.6 + (i % 3 - 1) * 0.5, 41.6), 0.16 * (1 if i % 2 else -1)), 0.5 + i * 0.25, 1.6, color=GOLD, width=6)
    PQ(fr, 960, 130, "SILVER AND SLAVES", a=fr.R(1.4, 0.4), size=34)

@sc("05b", "capitol", PLAN, {}, rivers=False)
def _(fr, t):
    plan(fr, hi="CAPITOLINE", hi_a=fr.R(29.0, 0.6)); gline(fr, WALL, color=(110, 96, 74), width=3, a=0.7)
    pulse(fr, HILLS["CAPITOLINE"][:2], 29.2, 3.0, color=ROM_D)
    PQL(fr, *HILLS["CAPITOLINE"][:2], "THE CAPITOL", dx=-330, dy=-30, a=fr.R(29.3, 0.4), size=30); PQL(fr, *HILLS["CAPITOLINE"][:2], "THREE HUNDRED", dx=-330, dy=40, a=fr.R(30.6, 0.4), size=28, light=True)
    PQL(fr, *HILLS["CAPITOLINE"][:2], "GAIUS", dx=-330, dy=130, a=fr.R(37.4, 0.4), size=30)

@sc("05c", "sulla", cam_box(11.4, 15.6, 40.2, 42.5), dict(it=PEN))
def _(fr, t):
    terr(fr, "it", ROM, 0.75); rome(fr, size=26)
    PQ(fr, 420, 170, "88 BC", a=fr.R(56.0, 0.4), size=34); PQ(fr, 420, 255, "SULLA", a=fr.R(57.4, 0.4), size=30, light=True)
    arrow(fr, smooth([C["NOLA"], C["CAPUA"], (13.6, 41.3), (12.9, 41.65), (12.58, 41.84)], 8), 61.4, 2.8, color=INK, width=8)

@sc("05d", "spartacus", ITA, dict(it=U(PEN, SICILY, CISALP)))
def _(fr, t):
    terr(fr, "it", ROM, 0.75); rome(fr); town(fr, "CAPUA", a=fr.R(79.2, 0.4), r=6, size=24, side="l")
    gline(fr, smooth(SPART, 8), color=INK, width=5.5, frac=fr.R(80.8, 6.0), halo=WHITE, dash=None)
    cross(fr, 15.2, 40.6, a=fr.R(86.6, 0.4), r=12, width=6)
    PQ(fr, 420, 200, "73 BC", a=fr.R(74.9, 0.4), size=34); PQ(fr, 420, 285, "SPARTACUS", a=fr.R(76.8, 0.4), size=30, light=True)

# ================= chapter 6
@sc("06a", "gaul", cam_box(-6.5, 14, 41.3, 52.6), dict(rm=U(ITALY, NARBON, HISP), g=Dm(GAUL, HISP, ITALY)))
def _(fr, t):
    terr(fr, "rm", ROM); terr(fr, "g", ROM, fr.R(16.8, 5.4)); rome(fr)
    region(fr, 2.3, 47.4, "GAUL", a=fr.R(14.9, 0.4), size=40); PQ(fr, 1560, 200, "58–50 BC", a=fr.R(18.2, 0.4), size=34)

@sc("06b", "parthians", cam_box(25, 58, 26.5, 43.5), dict(rm=Dm(EMP14, M(EGY_P, False)), pa=PARTHIA), res="50")
def _(fr, t):
    terr(fr, "rm", ROM); terr(fr, "pa", PAR, fr.R(35.4, 0.8)); region(fr, 50.5, 33.6, "PARTHIANS", a=fr.R(35.8, 0.4), size=34)
    PQ(fr, 420, 170, "53 BC", a=fr.R(33.6, 0.4), size=34); xmark(fr, "CARRHAE", a=fr.R(34.6, 0.4), r=13, width=6)
    PQ(fr, 960, 880, "NOW THERE ARE TWO", a=fr.R(38.1, 0.3), size=32)

RUBICON = [(12.05, 43.93), (12.2, 44.03), (12.32, 44.12), (12.40, 44.17)]
@sc("06c", "rubicon", cam_box(10.3, 14.4, 43.0, 45.3), dict(it=PEN, ci=CISALP))
def _(fr, t):
    terr(fr, "it", ROM); terr(fr, "ci", ROM_L); gline(fr, smooth(RUBICON, 6), color=(40, 96, 130), width=8, halo=WHITE)
    PQL(fr, 12.2, 44.03, "RUBICON", dx=-150, dy=-10, a=fr.R(40.2, 0.4), size=30)
    arrow(fr, [(11.9, 44.42), (12.2, 44.3), (12.45, 44.12), (12.75, 43.9)], 57.6, 1.5, color=INK, width=9)
    PQ(fr, 960, 880, "THE DIE IS CAST", a=fr.R(55.6, 0.4), size=34)

@sc("06d", "pompey_egypt", cam_box(9.5, 37, 27.5, 45.2), dict(rm=Dm(EMP14, M(EGY_P, False)), eg=I(CONT, EGY_P)), res="50")
def _(fr, t):
    terr(fr, "rm", ROM); terr(fr, "eg", PALM, fr.R(61.8, 0.6)); rome(fr)
    arrow(fr, smooth([C["PHARSALUS"], (24.2, 38.4), (26.8, 36.4), (29.5, 34.2), (31.6, 32.2), C["PELUSIUM"]], 8), 61.4, 2.0, color=INK, width=6)
    region(fr, 30.6, 28.6, "EGYPT", a=fr.R(62.2, 0.4), size=32); xmark(fr, "PELUSIUM", a=fr.R(63.2, 0.4), r=12, width=6)
    PQL(fr, *C["ROME"], "DICTATOR", dx=-150, dy=10, a=fr.R(65.0, 0.4), size=30)

# ================= chapter 7
@sc("07a", "pax_romana", EMPC, dict(emp=EMP14), res="50")
def _(fr, t):
    terr(fr, "emp", ROM); rome(fr, label=False); PQ(fr, 960, 130, "PAX ROMANA", a=fr.R(55.4, 0.4), size=40)

@sc("07b", "rhine", cam_box(1.5, 16.5, 46.3, 55.2), dict(emp=EMP14))
def _(fr, t):
    terr(fr, "emp", ROM); region(fr, 10.6, 51.6, "GERMANY", a=fr.R(68.9, 0.4) * 0 + fr.R(67.9, 0.4), size=34)
    PQ(fr, 1560, 200, "AD 9", a=fr.R(67.9, 0.4) * out(fr, 80), size=34); xmark(fr, "KALKRIESE", a=fr.R(68.4, 0.4), r=13, width=6); PQL(fr, *C["KALKRIESE"], "ARMINIUS", dx=150, dy=-50, a=fr.R(68.4, 0.4) * out(fr, 80), size=28)
    gline(fr, smooth(FRONT_RHINE, 6), color=ROM_D, width=9, frac=fr.R(93.1, 1.6), halo=WHITE)
    PQL(fr, 7.0, 50.7, "THE RHINE", dx=-170, dy=0, a=fr.R(93.3, 0.4), size=30); PQ(fr, 1560, 200, "AD 14", a=fr.R(96.4, 0.4), size=34)

# ================= chapter 8
AQUA = [[(13.05, 41.93), (12.9, 41.95), (12.75, 41.9), (12.6, 41.87), C["ROME"]], [(13.10, 41.90), (12.92, 41.88), (12.72, 41.84), (12.6, 41.85), C["ROME"]],
        [(12.98, 41.99), (12.82, 41.98), (12.68, 41.93), (12.57, 41.9), C["ROME"]], [(12.95, 42.03), (12.78, 42.0), (12.64, 41.95), C["ROME"]],
        [(12.86, 41.92), (12.7, 41.88), (12.58, 41.88), C["ROME"]], [(12.62, 41.89), (12.55, 41.885), C["ROME"]], [(12.66, 41.905), (12.57, 41.895), C["ROME"]],
        [(12.67, 41.80), (12.6, 41.84), (12.54, 41.87), C["ROME"]], [(12.70, 41.78), (12.62, 41.82), (12.55, 41.86), C["ROME"]],
        [(12.25, 42.08), (12.33, 42.0), (12.42, 41.93), C["ROME"]], [(12.33, 42.10), (12.38, 42.02), (12.45, 41.94), C["ROME"]]]
@sc("08a", "aqueducts", cam_box(12.1, 13.3, 41.62, 42.2), {})
def _(fr, t):
    for i, aq in enumerate(AQUA): gline(fr, smooth(aq, 8), color=(40, 96, 130), width=4.5, frac=fr.R(11.6 + i * 0.4, 2.4), halo=WHITE)
    rome(fr, r=10, size=28, side="b")
    PQ(fr, 420, 170, "ELEVEN AQUEDUCTS", a=fr.R(19.6, 0.4), size=30, anchor="m"); PQ(fr, 420, 255, "AD 226", a=fr.R(18.0, 0.4), size=30, light=True)

@sc("08b", "circus", PLAN, {}, rivers=False)
def _(fr, t):
    plan(fr); gline(fr, WALL, color=(110, 96, 74), width=3, a=0.7)
    c = (12.4853, 41.8861); ang = math.radians(-33); L, Wd = .0037, .00062; pts = []
    for i in range(41):
        th = math.pi * i / 40 - math.pi / 2; pts.append((L + Wd * math.cos(th), Wd * math.sin(th)))
    pts += [(-L, Wd), (-L, -Wd)]
    ring = [(c[0] + u * math.cos(ang) - v * 1.34 * math.sin(ang), c[1] + (u * math.sin(ang) + v * 1.34 * math.cos(ang)) / 1.34) for u, v in pts]; ring.append(ring[0])
    a = fr.R(46.2, 0.6); gpoly(fr, ring, ROM, 0.85 * a); gline(fr, ring, color=ROM_D, width=4, a=a)
    PQL(fr, *c, "CIRCUS MAXIMUS", dx=20, dy=110, a=fr.R(46.8, 0.4), size=30); PQL(fr, *c, "MORE THAN A HUNDRED THOUSAND", dx=20, dy=180, a=fr.R(48.6, 0.4), size=26, light=True)

# ================= chapter 9
@sc("09a", "largest", EMPC, dict(emp=EMPH, ex=I(EMP117, EASTX_P)), res="50")
def _(fr, t):
    terr(fr, "emp", ROM); terr(fr, "ex", mix(ROM, ROM_L, fr.R(18.8, 1.6)), 1 - 0.55 * fr.R(18.8, 1.6), border=False); rome(fr, label=False)
    PQ(fr, 960, 110, "AD 117", a=fr.R(0.4, 0.4) * out(fr, 15.0), size=38)
    PQ(fr, 960, 890, "FIVE MILLION SQUARE KILOMETRES", a=fr.R(9.4, 0.4) * out(fr, 15.0), size=28); PQ(fr, 960, 955, "60–70 MILLION PEOPLE", a=fr.R(12.2, 0.4) * out(fr, 15.0), size=28, light=True)
    PQ(fr, 960, 110, "HADRIAN", a=fr.R(16.0, 0.4) * out(fr, 28.5), size=36)
    gline(fr, smooth(FRONT_EAST, 6), color=ROM_D, width=6, frac=fr.R(19.6, 1.4), halo=WHITE)
    for i, ll in enumerate(LEGIONS):
        x, y = P(fr.cam, *ll); a = fr.R(29.3 + i * 0.05, 0.3); rect(fr, x - 6.5, y - 6.5, x + 6.5, y + 6.5, WHITE, a); rect(fr, x - 4.5, y - 4.5, x + 4.5, y + 4.5, BLACK, a)
    PQ(fr, 960, 110, "THIRTY LEGIONS", a=fr.R(29.6, 0.4), size=36)

@sc("09d", "spain_libya", MED, dict(emp=EMPH), res="50")
def _(fr, t):
    terr(fr, "emp", ROM); rome(fr, label=False)
    tdot(fr, C["ITALICA"], a=fr.R(36.2, 0.4), r=7, color=BLACK); pulse(fr, C["ITALICA"], 36.4, 2.6, color=BLACK); PQL(fr, *C["ITALICA"], "SPAIN", dx=150, dy=-60, a=fr.R(36.6, 0.4), size=32)
    tdot(fr, C["LEPTIS"], a=fr.R(40.8, 0.4), r=7, color=BLACK); pulse(fr, C["LEPTIS"], 41.0, 2.4, color=BLACK); PQL(fr, *C["LEPTIS"], "LIBYA", dx=0, dy=70, a=fr.R(41.3, 0.4), size=32)

@sc("09e", "citizens_plague", EMPC, dict(emp=EMPH), res="50")
def _(fr, t):
    terr(fr, "emp", ROM); rome(fr, label=False)
    pts = scatter(fr, "emp", 240, seed=7); x0, y0 = P(fr.cam, *C["ROME"]); k = fr.R(46.0, 5.0) * 1500; o = out(fr, 56.8, 0.8)
    dots_px(fr, pts, lambda i: o * min(1.0, max(0.0, (k - math.hypot(pts[i][0] - x0, pts[i][1] - y0)) / 90)), r=3.6, color=PAPER, ring=ROM_D)
    PQ(fr, 960, 110, "AD 212", a=fr.R(43.6, 0.4) * o, size=36); PQ(fr, 960, 185, "CARACALLA", a=fr.R(45.2, 0.4) * o, size=30, light=True)
    PQ(fr, 960, 900, "I AM A ROMAN CITIZEN", a=fr.R(54.7, 0.3) * o, size=34)
    p2 = scatter(fr, "emp", 300, seed=11); k2 = fr.R(59.2, 2.8) * 2200
    dots_px(fr, p2, lambda i: min(1.0, max(0.0, (k2 - (1900 - p2[i][0])) / 120)), r=4.2, color=BLACK, ring=None)
    PQ(fr, 960, 110, "THE 160s", a=fr.R(59.0, 0.4), size=36); PQ(fr, 960, 185, "PLAGUE", a=fr.R(60.3, 0.4), size=32, light=True)

@sc("09g", "danube", cam_box(8, 25, 42.6, 51.2), dict(emp=EMPH))
def _(fr, t):
    terr(fr, "emp", ROM); gline(fr, smooth(FRONT_DAN[:14], 6), color=ROM_D, width=9, frac=fr.R(64.6, 1.6), halo=WHITE)
    for i, st in enumerate(((14.8, 50.2), (17.4, 49.9), (19.6, 49.4))): arrow(fr, [st, (st[0] + 0.5, st[1] - 1.3)], 65.6 + i * 0.25, 0.9, color=GOT, width=7)
    PQ(fr, 420, 170, "MARCUS AURELIUS", a=fr.R(63.4, 0.4), size=30, anchor="m"); PQL(fr, 16.4, 48.2, "THE DANUBE", dx=40, dy=74, a=fr.R(65.0, 0.4), size=30, light=True)

# ================= chapter 10
@sc("10a", "goths_sasanians", cam_box(17, 50, 29.5, 48.6), dict(emp=EMPH, sa=PARTHIA), res="50")
def _(fr, t):
    terr(fr, "emp", ROM); terr(fr, "sa", PAR, fr.R(25.0, 0.8))
    for i, st in enumerate(((27.0, 46.9), (28.2, 46.7), (29.3, 46.4))): arrow(fr, [st, (st[0] - 0.3, st[1] - 2.9)], 23.2 + i * 0.2, 1.2, color=GOT, width=8)
    region(fr, 28.4, 47.6, "GOTHS", a=fr.R(23.2, 0.4), size=30, color=GOT); region(fr, 46.6, 34.6, "SASANIANS", a=fr.R(26.4, 0.4), size=28, dy=-40)
    arrow(fr, smooth([C["CTESIPHON"], (41.5, 34.9), (39.0, 36.0), (36.9, 36.2)], 8), 27.4, 1.8, color=PAR, width=8, halo=BLACK)
    PQ(fr, 420, 170, "260", a=fr.R(30.2, 0.4), size=36); xmark(fr, "EDESSA", a=fr.R(31.0, 0.4), r=13, width=6); PQL(fr, *C["EDESSA"], "EDESSA", dx=-10, dy=-56, a=fr.R(31.2, 0.4), size=28)
    PQ(fr, 420, 255, "SHAPUR", a=fr.R(32.9, 0.4), size=30, light=True); PQ(fr, 420, 335, "VALERIAN", a=fr.R(34.2, 0.4), size=30)

@sc("10c", "three_parts", EMPC, dict(g=GALLIC, p=PALMYR, c=CENTRAL, emp=EMP3), res="50")
def _(fr, t):
    k = fr.R(57.2, 2.0); q = 1.0 if k < 1 else 0.0
    terr(fr, "c", ROM, q); terr(fr, "g", mix(GALC, ROM, fr.R(46.0, 1.4)), q * (1 - k)); terr(fr, "p", mix(PALM, ROM, fr.R(46.0, 1.4)), q * (1 - k))
    terr(fr, "emp", ROM, k); rome(fr, label=False)
    o = out(fr, 57.0, 0.6)
    PQL(fr, 1.5, 47.0, "GALLIC EMPIRE", a=fr.R(48.6, 0.4) * o, size=28); PQL(fr, *C["PALMYRA"], "PALMYRA", dx=120, dy=-30, a=fr.R(51.6, 0.4) * o, size=28); tdot(fr, C["PALMYRA"], a=fr.R(51.4, 0.4) * o, r=6, color=BLACK)
    PQL(fr, *C["ROME"], "ROME", dx=70, dy=70, a=fr.R(55.2, 0.4) * o, size=28, light=True); PQ(fr, 960, 110, "AURELIAN", a=fr.R(57.6, 0.4), size=36)

@sc("10d", "diocletian", cam_box(7.5, 25, 38.6, 47.8), dict(emp=EMP3))
def _(fr, t):
    terr(fr, "emp", ROM); rome(fr); tdot(fr, C["SALONA"], a=fr.R(66.8, 0.4), r=7, color=BLACK); pulse(fr, C["SALONA"], 67.0, 2.6, color=BLACK)
    region(fr, 17.2, 43.9, "DALMATIA", a=fr.R(67.0, 0.4), size=24, color=WHITE, dy=-36)
    PQ(fr, 420, 170, "284", a=fr.R(65.6, 0.4), size=36); PQ(fr, 420, 255, "DIOCLETIAN", a=fr.R(68.2, 0.4), size=30, light=True)

def cells(fr, key, n, seed):
    c = getattr(fr.scene, "_cells", None)
    if c is None: c = fr.scene._cells = {}
    if (n, seed) not in c:
        pts = np.asarray(scatter(fr, key, n, seed=seed), np.float32) * SS / 4; h, w = H * SS // 4, W * SS // 4
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); best = np.full((h, w), 1e12, np.float32); lab = np.zeros((h, w), np.int32)
        for i, (px, py) in enumerate(pts):
            d = (xx - px) ** 2 + (yy - py) ** 2; m = d < best; best[m] = d[m]; lab[m] = i
        e = (lab != np.roll(lab, 1, 0)) | (lab != np.roll(lab, 1, 1))
        em = Image.fromarray((e * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).resize((W * SS, H * SS), Image.BILINEAR)
        c[(n, seed)] = IC.multiply(em, fr.masks[key])
    return c[(n, seed)]
@sc("10e", "provinces", EMPC, dict(emp=EMP3), res="50")
def _(fr, t):
    terr(fr, "emp", ROM); rome(fr, label=False)
    k = fr.R(78.4, 1.6); a1 = 1 - k
    if a1 > 0: fr.im.paste(PAPER, (0, 0), cells(fr, "emp", 48, 3).point(lambda v: int(v * 0.85 * a1)))
    if k > 0: fr.im.paste(PAPER, (0, 0), cells(fr, "emp", 100, 5).point(lambda v: int(v * 0.85 * k)))
    fr.d = ImageDraw.Draw(fr.im); PQ(fr, 960, 110, "A THOUSAND GOODS", a=fr.R(82.0, 0.4), size=34)

# ================= chapter 11
CHR = ["ANTIOCH", "DAMASCUS", "ALEXANDRIA", "EPHESUS", "EDESSA", "THESSALONICA", "CORINTH", "ROME", "CARTHAGE", "LUGDUNUM"]
@sc("11a", "christianity", cam_box(-6, 44, 28, 50), dict(emp=EMP3), res="50")
def _(fr, t):
    terr(fr, "emp", ROM); k = fr.R(9.8, 1.0)
    for i, nm in enumerate(CHR):
        gline(fr, arc(C["JERUSALEM"], C[nm], 0.14), color=PAPER, width=3.4, frac=fr.R(1.6 + i * 0.3, 1.4), halo=ROM_D, a=1 - 0.6 * k)
        tdot(fr, C[nm], a=fr.R(2.6 + i * 0.3, 0.4), r=6, color=mix(BLACK, PAPER, k), ring=mix(WHITE, ROM_D, k))
    tdot(fr, C["JERUSALEM"], r=7, color=PAPER, ring=ROM_D); region(fr, 35.3, 31.8, "JUDAEA", a=fr.R(2.4, 0.4), size=24, color=WHITE, dx=74, dy=40)
    PQ(fr, 960, 110, "CHRISTIANITY", a=fr.R(5.5, 0.4), size=36); PQ(fr, 960, 185, "DIOCLETIAN", a=fr.R(9.9, 0.4), size=30, light=True)

@sc("11b", "milvian", PLANW, {}, rivers=False)
def _(fr, t):
    plan(fr); gpoly(fr, ell(12.489, 41.891, .016, .0105, 0), ROM, 0.22)
    gline(fr, [(12.4790, 41.8960), (12.4764, 41.9113), (12.4700, 41.9260), MILVIAN, (12.4640, 41.9430)], color=INK, width=5, halo=WHITE)
    x, y = P(fr.cam, *MILVIAN); rect(fr, x - 26, y - 7, x + 26, y + 7, WHITE, fr.R(16.8, 0.4)); rect(fr, x - 23, y - 4.5, x + 23, y + 4.5, BLACK, fr.R(16.8, 0.4)); pulse(fr, MILVIAN, 17.2, 2.6)
    PQ(fr, 330, 170, "312", a=fr.R(13.6, 0.4), size=36); PQ(fr, 330, 255, "CONSTANTINE", a=fr.R(14.9, 0.4), size=30, light=True)
    PQL(fr, *MILVIAN, "MILVIAN BRIDGE", dx=250, dy=0, a=fr.R(17.3, 0.4), size=30); modern(fr, 12.489, 41.889, "ROME", size=30, color=ROM_D, a=1.0)

@sc("11c", "nicaea", cam_box(21.5, 36.5, 35.8, 43.8), dict(emp=EMP3))
def _(fr, t):
    terr(fr, "emp", ROM); tdot(fr, C["NICAEA"], a=fr.R(38.6, 0.4), r=8, color=PAPER, ring=BLACK); pulse(fr, C["NICAEA"], 39.0, 3.0, color=BLACK)
    PQ(fr, 420, 170, "325", a=fr.R(35.8, 0.4), size=36); PQL(fr, *C["NICAEA"], "NICAEA", dx=130, dy=40, a=fr.R(39.4, 0.4), size=32)

BOS = cam_box(28.3, 29.9, 40.72, 41.42); BOSW = cam_box(14, 47, 29.5, 48.6); BOS0 = cam_box(19, 39, 35.5, 46)
@sc("11d", "byzantium", mover([(44.7, BOS0), (46.6, BOS0), (48.8, BOS), (51.2, BOS), (53.2, BOSW), (56.0, BOSW)]), dict(emp=EMP3))
def _(fr, t):
    S = fr.cam[2]; near = S > BOS[2] * 0.6; terr(fr, "emp", ROM, 0.0 if near else 1.0)
    city(fr, "CONSTANTINOPLE", r=9 if near else 7, label="", icon=True)
    if S > BOS[2] * 0.25: PQL(fr, *C["BYZANTIUM"], "BYZANTIUM", dx=-170, dy=-30, a=fr.R(49.2, 0.4) * out(fr, 52.0), size=32)
    if near:
        region(fr, 28.62, 41.26, "EUROPE", a=fr.R(50.4, 0.4), size=30); region(fr, 29.45, 40.93, "ASIA", a=fr.R(51.0, 0.4), size=30); sea(fr, 29.12, 41.14, "BOSPORUS", a=fr.R(48.6, 0.4), size=20, dx=64)
    if fr.v > 53.0:
        gline(fr, smooth(FRONT_DAN, 6), color=PAPER, width=8, frac=fr.R(53.2, 1.0), halo=ROM_D); gline(fr, smooth(FRONT_EAST, 6), color=PAPER, width=8, frac=fr.R(54.6, 0.8), halo=ROM_D)
        PQL(fr, 22.6, 44.5, "THE DANUBE", dy=-50, a=fr.R(53.4, 0.3), size=26); PQL(fr, 40.4, 35.2, "THE EAST", dx=110, dy=0, a=fr.R(54.8, 0.3), size=26)

@sc("11e", "east_west", EMPC, dict(emp=EMP3, e=EAST395, w=WEST395), res="50")
def _(fr, t):
    terr(fr, "emp", ROM); k = fr.R(81.6, 1.6); terr(fr, "e", EST, k); terr(fr, "w", ROM, k)
    city(fr, "CONSTANTINOPLE", r=7, label="", a=fr.R(84.4, 0.4)); rome(fr, label=False)
    PQ(fr, 960, 110, "395", a=fr.R(80.4, 0.4), size=38); PQL(fr, 32.5, 38.6, "EAST", dy=0, a=fr.R(84.5, 0.4), size=36); PQL(fr, 4.5, 44.6, "WEST", a=fr.R(87.2, 0.4), size=36, light=True)

# ================= chapter 12
@sc("12a", "goths_huns", cam_box(15.5, 45, 36.3, 50.8), dict(emp=EMP3))
def _(fr, t):
    terr(fr, "emp", ROM); city(fr, "CONSTANTINOPLE", r=7, label="")
    PQ(fr, 330, 170, "376", a=fr.R(0.4, 0.4) * out(fr, 10.6), size=36); region(fr, 28.6, 47.3, "GOTHS", a=fr.R(1.4, 0.4), size=30, color=GOT)
    arrow(fr, arc((43.5, 48.3), (33.0, 47.6), 0.1), 2.6, 1.6, color=HUN, width=10); region(fr, 40.0, 49.3, "HUNS", a=fr.R(3.0, 0.4), size=30, color=HUN)
    for i, st in enumerate(((26.2, 46.6), (28.0, 46.5))): arrow(fr, [st, (st[0] - 0.2, 44.35)], 4.6 + i * 0.3, 1.4, color=GOT, width=8)
    gline(fr, smooth(FRONT_DAN[11:], 6), color=PAPER, width=6, halo=ROM_D)
    arrow(fr, smooth([(27.2, 43.9), (26.9, 42.9), (26.6, 41.95)], 6), 9.6, 1.2, color=GOT, width=8)
    PQ(fr, 330, 170, "378", a=fr.R(10.9, 0.4), size=36); xmark(fr, "ADRIANOPLE", a=fr.R(11.6, 0.4), r=13, width=6); PQL(fr, *C["ADRIANOPLE"], "ADRIANOPLE", dx=-190, dy=20, a=fr.R(11.8, 0.4), size=28)

@sc("12c", "vandals_476", cam_box(-1, 21, 33.2, 46.8), dict(w=Dm(WEST395, VANDAL, U(ITALY, SICILY)), v=VANDAL, it=U(ITALY, SICILY)))
def _(fr, t):
    terr(fr, "w", ROM, 0.8); terr(fr, "v", VAN); terr(fr, "it", mix(GOT, ROM, fr.R(44.2, 1.0)), 1.0); rome(fr)
    PQ(fr, 330, 170, "455", a=fr.R(36.1, 0.4) * out(fr, 43.8), size=36); region(fr, 8.2, 35.4, "VANDALS", a=fr.R(36.8, 0.4), size=28, color=WHITE)
    arrow(fr, smooth([C["CARTHAGE"], (11.2, 38.4), (12.0, 40.4), C["OSTIA"]], 8), 39.3, 2.2, color=VAN, width=8)
    town(fr, "CARTHAGE", r=6.5, size=24, side="b", a=fr.R(42.2, 0.4), color=WHITE)
    PQ(fr, 330, 170, "476", a=fr.R(44.1, 0.4), size=36); PQ(fr, 330, 255, "ODOACER", a=fr.R(45.6, 0.4), size=30, light=True)

@sc("12e", "east_remains", EMPC, dict(e=EAST395, w=WEST395), res="50")
def _(fr, t):
    terr(fr, "w", (128, 122, 112), 0.75, border=False); terr(fr, "e", EST); city(fr, "CONSTANTINOPLE", r=8, label="")
    PQL(fr, *C["CONSTANTINOPLE"], "CONSTANTINOPLE", dx=40, dy=-70, a=fr.R(71.2, 0.4), size=30); PQL(fr, *C["CONSTANTINOPLE"], "1453", dx=40, dy=74, a=fr.R(75.4, 0.4), size=36, light=True)

@sc("12f", "romance", cam_box(-118, 48, -52, 62), dict(r=ROMANCE), res="50", rivers=False)
def _(fr, t):
    terr(fr, "r", ROM, fr.R(80.4, 3.0)); PQ(fr, 960, 110, "NINE HUNDRED MILLION", a=fr.R(83.2, 0.4), size=36)

if __name__ == "__main__":
    import time
    mode = sys.argv[1]
    if mode == "list":
        tot = 0
        for n, s_ in SC.items(): print(f"{n:24s} ch{s_.ch:02d}  VO {s_.t0:6.1f} - {s_.t0 + s_.dur:6.1f}  ({s_.dur:5.1f} s)"); tot += s_.dur
        print("total", round(tot, 1), len(SC))
    elif mode == "sheet":       # one still per layout window, near its end
        pref = sys.argv[3:]; ims = []
        for n, s_ in SC.items():
            if pref and not any(n.startswith(p) for p in pref): continue
            s_.frame(0.0)
            for ch, a, b in WIN[n.split("_")[0]]:
                tt = a + (b - a) * 0.93
                im = s_.frame(tt - s_.t0).resize((960, 540), Image.LANCZOS); d = ImageDraw.Draw(im); d.rectangle([0, 0, 360, 22], fill=(17, 17, 17))
                d.text((6, 5), f"{n}  ch{ch} VO {tt:5.1f} ({a:.1f}-{b:.1f})", fill=(255, 255, 255)); ims.append(im)
            s_.masks = {}; s_._cam = None; s_.base = None; s_.rmask = None; s_.rm = None; s_.lm = None; s_.desert = None; s_._sc = None; s_._cells = None
        cols = 2; sh = Image.new("RGB", (cols * 960, ((len(ims) + cols - 1) // cols) * 540), (17, 17, 17))
        for i, im in enumerate(ims): sh.paste(im, (i % cols * 960, i // cols * 540))
        sh.save(f"{HERE}/test_look/sheet_{sys.argv[2]}.jpg", quality=86)
    elif mode == "still":
        for spec in sys.argv[2:]:
            n, ts = spec.split("@"); s_ = SC[n]; s_.frame(0.0)
            for tt in ts.split(","): s_.still(float(tt) - s_.t0, f"{HERE}/test_look/{n}_{float(tt):05.1f}.jpg", 0.75)
    else:
        os.makedirs(f"{HERE}/out_look", exist_ok=True)
        for n in sys.argv[2:]:
            t0 = time.time(); SC[n].render(f"{HERE}/out_look"); print(n, round(time.time() - t0, 1), flush=True)
