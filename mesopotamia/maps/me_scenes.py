"""Mesopotamia in 20 Minutes: map scenes, timed to the recorded voiceover (chapter seconds). Windows come from ../layout.json (one source of numbers).
usage: python3 me_scenes.py list | still name@t,t (chapter seconds) | sheet tag [prefixes] | render names... | json"""
from me_base import *
HERE = os.path.dirname(os.path.abspath(__file__))
import me_base; _inside = me_base._inside
_LAY = json.load(open(os.path.join(HERE, "../layout.json")))
WIN = {}
for _ch, _v in _LAY.items():
    if not isinstance(_v, dict) or "segs" not in _v: continue
    for _s in _v["segs"]:
        if _s[2] == "MAP": WIN.setdefault((_s[3], int(_ch)), []).append((_s[0], _s[1]))
def sc(i, tag, cam, masks, ch=None, **kw):
    """one clip per map id and chapter: it covers the first window's start to the last window's end"""
    chs = [c for (j, c) in WIN if j == i]; ch = ch if ch is not None else chs[0]; w = WIN[(i, ch)]
    return scene(f"{i}_{tag}", ch, min(a for a, b in w), max(b for a, b in w), cam, masks, **kw)

# ---------------------------------------------------------------- helpers
def rect(fr, x0, y0, x1, y1, color, a=1.0):
    alpha_draw(fr, lambda d, c: d.rectangle([s(x0), s(y0), s(x1), s(y1)], fill=c), color, a)
def poly(fr, pts, color, a=1.0):
    alpha_draw(fr, lambda d, c: d.polygon([(s(x), s(y)) for x, y in pts], fill=c), color, a)
def circ(fr, x, y, r, color=None, a=1.0, outline=None, width=2):
    if a <= 0: return
    if color is not None: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=c), color, a)
    if outline is not None: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], outline=c, width=s(width)), outline, a)
def arrow(fr, pts, t0, d=1.4, width=4.2, a=1.0, n=10, **kw):
    gline(fr, smooth(pts, n) if len(pts) > 2 else pts, width=width, frac=fr.R(t0, d), arrow=True, halo=kw.pop("halo", WHITE), a=a, **kw)
def out(fr, t0, d=0.5): return 1 - fr.R(t0, d)
_gline0 = gline
def gline(fr, lonlat, halo=None, **kw):
    """dashed lines need a dense path (the base dash routine drops a dash that lies inside one segment)"""
    if kw.get("dash"):
        a = np.asarray(lonlat, float); L = path_len(proj(fr.cam, a, 1)); n = max(2, int(L[-1] / 3.0))
        lonlat = np.stack([np.interp(np.linspace(0, L[-1], n), L, a[:, 0]), np.interp(np.linspace(0, L[-1], n), L, a[:, 1])], 1)
    _gline0(fr, lonlat, halo=halo, **kw)
def tdot(fr, ll, a=1.0, r=4.2, color=INK, ring=WHITE):
    x, y = P(fr.cam, *ll); circ(fr, x, y, r + 1.8, ring, a); circ(fr, x, y, r, color, a)
def town(fr, name, a=1.0, r=5.5, color=INK, size=22, **kw): city(fr, name, a=a, r=r, dot=color, icon=False, size=size, **kw)
def gpoly(fr, lonlat, color, a=1.0):
    p = proj(fr.cam, lonlat, 1); poly(fr, [tuple(q) for q in p], color, a)
def rivers_bold(fr, width=5.0, a=1.0, color=(74, 128, 156)):
    """the two rivers drawn heavier than the base (same geometry, so no double line)"""
    for arr in engine.RIVERS:
        p = proj(fr.cam, arr, 1)
        if p[:, 0].max() < 0 or p[:, 0].min() > W or p[:, 1].max() < 0 or p[:, 1].min() > H: continue
        pline(fr, p, color=color, width=width, a=a)
def mover_dot(fr, path, t0, d, r=7, color=INK, hold=0.0):
    """a dot travelling along a lon/lat path between chapter seconds t0 and t0+d"""
    live(fr, t0, t0 + d + hold)
    if fr.v < t0 or fr.v > t0 + d + hold: return None
    ll = along(path, ease((fr.v - t0) / d)); tdot(fr, ll, r=r, color=color); return ll
def villages(fr, t0=None, color=(110, 84, 50), r=3.4):
    for i, ll in enumerate(VILLAGES): tdot(fr, ll, a=1.0 if t0 is None else fr.R(t0 + i * 0.07, 0.4), r=r, color=color)
CANALS = []
_rg = np.random.default_rng(21)
for _base in (OLD_EUPHRATES[3:], [(44.5, 33.4), (45.0, 32.9), (45.6, 32.5), (46.2, 32.3), (46.7, 32.0), (47.1, 31.6)], [(44.3, 32.7), (44.4, 32.2), (44.7, 31.8), (45.2, 31.4), (45.7, 31.1)]):
    _b = smooth(_base, 8)
    for _k in range(6, len(_b) - 4, 7):
        _p = _b[_k]; _v = _b[_k + 2] - _b[_k - 2]; _v = _v / np.hypot(*_v)
        for _sg in (1, -1):
            _n = np.array([-_v[1], _v[0]]) * _sg; _L = _rg.uniform(0.12, 0.34); _q = _p + (_n * 0.9 + _v * 0.45) * _L
            if not _inside(tuple(_q), GULF): CANALS.append([tuple(_p), tuple(_p + (_n * 0.9 + _v * 0.2) * _L * 0.5), tuple(_q)])
def canals(fr, t0=None, a=1.0):
    for i, c in enumerate(CANALS): gline(fr, c, color=(84, 142, 166), width=2.2, frac=1.0 if t0 is None else fr.R(t0 + (i % 17) * 0.12, 1.3), a=a)
def green(fr, a): terr(fr, "plain", GRN, a * 0.6, border=False)

MESO = cam_box(37.2, 51.6, 28.4, 38.7); SOUTHC = cam_box(43.4, 48.6, 30.1, 33.7); SUMERC = cam_box(44.1, 47.7, 30.45, 32.95); NEAR = cam_box(27, 54, 22.5, 41.5)
TOP = cam_box(36.5, 46.5, 35.0, 41.0)

# ================= chapter 1
@sc("01a", "two_rivers", mover([(0, TOP), (1.6, TOP), (9.4, MESO), (20, MESO)]), {})
def _(fr, t):
    rivers_bold(fr, 4.6)
    modern(fr, 38.6, 39.3, "TURKEY", a=fr.R(3.0, 0.5) * out(fr, 12.0), size=22)
    modern(fr, 39.55, 35.2, "EUPHRATES", a=fr.R(word(1, "Two rivers", "the Euphrates"), 0.4), size=21, color=SEA_T, anchor="r")
    modern(fr, 44.2, 35.3, "TIGRIS", a=fr.R(word(1, "Two rivers", "Tigris"), 0.4), size=21, color=SEA_T, anchor="l")
    sea(fr, 50.2, 28.95, "PERSIAN GULF", a=fr.R(word(1, "They run", "Persian"), 0.5), size=19)
    PQ(fr, 560, 760, "MESOPOTAMIA", a=fr.R(word(1, "The Greeks", "Mesopotamia"), 0.4), size=40); PQ(fr, 560, 842, "BETWEEN THE RIVERS", a=fr.R(word(1, "The Greeks", "between the rivers"), 0.4), size=28, light=True)
    a = fr.R(word(1, "Today", "mostly"), 0.6)
    modern(fr, 42.3, 32.9, "IRAQ", a=a, size=40, color=(70, 60, 46)); modern(fr, 42.3, 32.9, "TODAY", a=a, size=17, color=(70, 60, 46), dy=40)

@sc("01b", "canals", SOUTHC, dict(plain=SOUTH))
def _(fr, t):
    green(fr, fr.R(53.4, 2.6)); canals(fr, 53.0); rivers_bold(fr, 4.0)
    PQ(fr, 520, 180, "THE RICHEST FARMLAND ON EARTH", a=fr.R(word(1, "Irrigated", "some of"), 0.4), size=30)

@sc("01c", "villages_eridu", SOUTHC, dict(plain=SOUTH))
def _(fr, t):
    green(fr, 1.0); canals(fr); rivers_bold(fr, 4.0); villages(fr, 58.4)
    PQ(fr, 420, 180, "5000 BC", a=fr.R(word(1, "By about", "5000"), 0.4), size=36)
    te = cue(1, "Eridu"); tdot(fr, C["ERIDU"], a=fr.R(te, 0.3), r=8, color=AKK); pulse(fr, C["ERIDU"], te, 2.2, color=AKK)
    PQL(fr, *C["ERIDU"], "ERIDU", dx=-110, dy=10, a=fr.R(te, 0.4), size=32)
    sea(fr, 48.05, 30.45, "THE GULF", a=fr.R(te + 1.0, 0.4), size=18)

# ================= chapter 2
URUKZ = cam_at(45.638, 31.324, 520)
@sc("02a", "uruk", mover([(0, SOUTHC), (1.2, SOUTHC), (6.6, URUKZ), (9, URUKZ)]), dict(plain=SOUTH))
def _(fr, t):
    green(fr, 1.0); canals(fr); rivers_bold(fr, 4.0); villages(fr)
    PQ(fr, 420, 180, "3500 BC", a=fr.R(0.9, 0.4), size=36)
    tu = cue(2, "Uruk, on"); tdot(fr, C["URUK"], a=fr.R(1.0, 0.4), r=9, color=AKK); pulse(fr, C["URUK"], tu, 1.9, color=AKK)
    PQL(fr, *C["URUK"], "URUK", dx=140, dy=-10, a=fr.R(tu, 0.4), size=36)

# ---- schematic plan of Uruk
UC = (45.6385, 31.3225)
def ring(lon, lat, rx, ry, ang=0, n=72, wob=0.07, seed=0):
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang)); pts = []
    for i in range(n):
        t = 2 * math.pi * i / n; k = 1 + wob * math.sin(3 * t + seed) + wob * 0.6 * math.sin(5 * t + 1.7 * seed)
        u, v = rx * k * math.cos(t), ry * k * math.sin(t); pts.append((lon + u * c - v * s_, lat + u * s_ + v * c))
    return pts + [pts[0]]
UWALL = ring(UC[0], UC[1], 0.0162, 0.0138, 12, wob=0.06, seed=1.3)
UCITY = ring(UC[0], UC[1], 0.0150, 0.0127, 12, wob=0.06, seed=1.3)
EANNA = [(45.6392, 31.3248), (45.6442, 31.3243), (45.6447, 31.3206), (45.6396, 31.3210)]
ANU = [(45.6318, 31.3236), (45.6352, 31.3240), (45.6357, 31.3206), (45.6322, 31.3202)]
UCANAL = [(45.600, 31.352), (45.618, 31.346), (45.636, 31.3405), (45.652, 31.339), (45.662, 31.330), (45.667, 31.318), (45.664, 31.305), (45.672, 31.292)]
UPLAN = cam_box(45.607, 45.670, 31.3035, 31.3415)
_rb = np.random.default_rng(5); UBLOCKS = []
while len(UBLOCKS) < 420:
    p = (float(_rb.uniform(45.620, 45.657)), float(_rb.uniform(31.307, 31.338)))
    if _inside(p, UCITY) and not _inside(p, [(45.6305, 31.3250), (45.6460, 31.3253), (45.6460, 31.3196), (45.6308, 31.3192)]): UBLOCKS.append((p, float(_rb.uniform(0.6, 1.25)), float(_rb.uniform(-25, 25))))
def uruk_plan(fr, wall=0.0, wall_a=1.0):
    c = getattr(fr.scene, "_plan", None)
    if c is None:
        S = fr.cam[2] * SS; lay = Image.new("RGBA", fr.im.size, (0, 0, 0, 0))
        m = Image.new("L", fr.im.size, 0); ImageDraw.Draw(m).polygon([tuple(q) for q in proj(fr.cam, UCITY)], fill=255)
        lay.paste((206, 188, 150), (0, 0), m.filter(ImageFilter.GaussianBlur(0.0009 * S)).point(lambda v: int(v * 0.9)))
        d = ImageDraw.Draw(lay)
        for (lon, lat), k, ang in UBLOCKS:
            w_, h_ = 0.00062 * k, 0.00040 * k; ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            pts = [(lon + u * ca - v * sa, lat + u * sa + v * ca) for u, v in ((-w_, -h_), (w_, -h_), (w_, h_), (-w_, h_))]
            d.polygon([tuple(q) for q in proj(fr.cam, pts)], fill=(170, 148, 110, 255))
        c = fr.scene._plan = lay
    gline(fr, smooth(UCANAL, 8), color=(62, 104, 126), width=15); gline(fr, smooth(UCANAL, 8), color=(104, 160, 184), width=11)
    fr.im.paste(c, (0, 0), c); fr.d = ImageDraw.Draw(fr.im)
    for blk, col in ((EANNA, (236, 226, 200)), (ANU, (236, 226, 200))):
        gpoly(fr, [(x + 0.00035, y - 0.00035) for x, y in blk], (96, 84, 60), 0.45); gpoly(fr, blk, col, 1.0)
    if wall > 0: gline(fr, UWALL, color=ASY_D, width=9, frac=wall, halo=WHITE, a=wall_a)
    modern(fr, 45.6625, 31.3368, "EUPHRATES", size=18, color=SEA_T)
def temples(fr, ta=None, ti=None):
    a1 = 1.0 if ta is None else fr.R(ta, 0.4); a2 = 1.0 if ti is None else fr.R(ti, 0.4)
    gpoly(fr, [(45.6327, 31.3229), (45.6345, 31.3231), (45.6347, 31.3214), (45.6329, 31.3212)], WHITE, a1)
    gpoly(fr, EANNA, BAB, 0.55 * a2)
    return a1, a2
@sc("02b", "uruk_plan", UPLAN, {}, ch=2, rivers=False)
def _(fr, t):
    uruk_plan(fr); a1, a2 = temples(fr, word(2, "In the middle", "sky god"), word(2, "In the middle", "goddess"))
    PQL(fr, 45.6337, 31.3221, "AN", dx=-150, dy=-80, a=a1, size=34); T(fr, P(fr.cam, 45.6337, 31.3221)[0] - 150, P(fr.cam, 45.6337, 31.3221)[1] - 30, "SKY GOD", size=18, sp=4, anchor="m", a=a1)
    PQL(fr, 45.6420, 31.3226, "INANNA", dx=230, dy=-80, a=a2, size=34); T(fr, P(fr.cam, 45.6420, 31.3226)[0] + 230, P(fr.cam, 45.6420, 31.3226)[1] - 30, "GODDESS", size=18, sp=4, anchor="m", a=a2)
    x, y = P(fr.cam, 45.6337, 31.3221); circ(fr, x, y, 40, outline=INK, a=fr.R(word(2, "In the middle", "one of them"), 0.4), width=4)
    PQ(fr, 330, 150, "URUK", size=36)
@sc("02b", "uruk_wall3", UPLAN, {}, ch=3, rivers=False)
def _(fr, t):
    tw = word(3, "But the Sumerians", "built Uruk"); uruk_plan(fr, wall=fr.R(tw, 3.0)); temples(fr)
    PQ(fr, 330, 150, "URUK", size=36)
    PQ(fr, 400, 860, "URUK'S GREAT WALL", a=fr.R(tw + 0.8, 0.4), size=30); PQ(fr, 400, 935, "≈ 9 KM", a=fr.R(tw + 1.6, 0.4), size=26, light=True)
    PQ(fr, 1460, 860, "THE OLDEST GREAT STORY", a=fr.R(word(3, "But the Sumerians", "the hero"), 0.4), size=28); PQ(fr, 1460, 935, "GILGAMESH", a=fr.R(word(3, "But the Sumerians", "the hero"), 0.4), size=28, light=True)
@sc("02b", "uruk_wall10", UPLAN, {}, ch=10, rivers=False)
def _(fr, t):
    uruk_plan(fr, wall=1.0); temples(fr)
    PQ(fr, 330, 150, "URUK", size=36)
    PQ(fr, 1460, 860, "ENKIDU", a=fr.R(word(10, "In it, the king", "Enkidu"), 0.4), size=30); PQ(fr, 1460, 935, "NEVER TO DIE", a=fr.R(word(10, "In it, the king", "never"), 0.4), size=28, light=True)

EGW = cam_box(27.5, 50.5, 23.0, 36.5); ABYDOS = (31.92, 26.18)
@sc("02c", "uruk_egypt", EGW, {})
def _(fr, t):
    rivers_bold(fr, 3.6)
    tdot(fr, C["URUK"], r=8, color=AKK); PQL(fr, *C["URUK"], "URUK", dx=0, dy=-52, size=30)
    te = word(2, "Along with", "Egypt"); tdot(fr, ABYDOS, a=fr.R(te, 0.4), r=8, color=EGY); pulse(fr, ABYDOS, te, 2.4, color=INK); pulse(fr, C["URUK"], te + 0.5, 2.4, color=AKK)
    PQL(fr, *ABYDOS, "EGYPT", dx=0, dy=-52, a=fr.R(te, 0.4), size=30)
    T(fr, P(fr.cam, *ABYDOS)[0], P(fr.cam, *ABYDOS)[1] + 40, "HIEROGLYPHS", size=18, sp=4, anchor="m", a=fr.R(te + 0.5, 0.4)); T(fr, P(fr.cam, *C["URUK"])[0], P(fr.cam, *C["URUK"])[1] + 40, "CUNEIFORM", size=18, sp=4, anchor="m", a=fr.R(te + 0.5, 0.4))
    PQ(fr, 960, 170, "THE OLDEST WRITING ON EARTH", a=fr.R(word(2, "Along with", "the oldest"), 0.4), size=32); PQ(fr, 960, 250, "TO KEEP ACCOUNTS", a=fr.R(word(2, "It was invented", "to keep"), 0.4), size=30, light=True)

# ================= chapter 3
@sc("03a", "sumer_cities", SUMERC, dict(sum=SUMER))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "sum", SUM, fr.R(10.2, 1.0) * 0.55)
    PQ(fr, 380, 170, "2900 BC", a=fr.R(0.5, 0.4), size=36)
    town(fr, "URUK", r=7, color=AKK, side="l", size=24)
    for nm, side in (("UR", "b"), ("LAGASH", "r"), ("UMMA", "t"), ("KISH", "t"), ("NIPPUR", "r")):
        tt = word(3, "Ur, Lagash", nm.capitalize()); town(fr, nm, a=fr.R(tt, 0.35), r=7, color=AKK, side=side, size=24); pulse(fr, C[nm], tt, 1.2, color=AKK, n=1)
    PQ(fr, 1480, 250, "SUMERIAN", a=fr.R(word(3, "Most of them", "Sumerian"), 0.4), size=34); PQ(fr, 1480, 330, "ONE LANGUAGE · MANY CITIES", a=fr.R(word(3, "Most of them", "but not"), 0.4), size=24, light=True)

GUC = cam_box(45.35, 47.05, 30.98, 32.12)
BORDER = [(46.00, 31.74), (46.05, 31.64), (46.03, 31.56), (46.08, 31.47)]
@sc("03b", "lagash_umma", GUC, dict(lag=LAGASHM, umm=UMMAM, gue=GUEDENA))
def _(fr, t):
    rivers_bold(fr, 4.0)
    terr(fr, "lag", LAG, fr.R(36.2, 0.6)); terr(fr, "umm", UMM, fr.R(37.0, 0.6))
    tg = word(3, "Between Lagash", "a strip"); terr(fr, "gue", GRN, fr.R(tg, 0.6)); 
    town(fr, "LAGASH", a=fr.R(36.2, 0.4), r=7, side="r", size=26); town(fr, "GIRSU", a=fr.R(36.2, 0.4), r=4.5, side="r", size=17); town(fr, "UMMA", a=fr.R(37.0, 0.4), r=7, side="l", size=26)
    v1 = fr.v < 60
    PQ(fr, 960, 150, "GU'EDENA — THE EDGE OF THE PLAIN", a=fr.R(word(3, "Between Lagash", "called"), 0.4) * (1 if v1 else 0), size=30)
    # the fight: short arrows into the strip from both sides
    for k in range(3):
        t0 = 42.6 + k * 0.9
        arrow(fr, [(45.93, 31.67), (46.07, 31.65)], t0, 0.5, color=UMM, width=6, a=out(fr, t0 + 0.9, 0.3) if k < 2 else out(fr, 60)); arrow(fr, [(46.27, 31.58), (46.15, 31.67)], t0 + 0.45, 0.5, color=(128, 82, 30), width=6, a=out(fr, t0 + 1.35, 0.3) if k < 2 else out(fr, 60))
    PQ(fr, 960, 930, "THE EARLIEST WAR BETWEEN STATES", a=fr.R(cue(3, "It is the earliest"), 0.4) * (1 if v1 else 0), size=28, light=True)
    # second window: the border, broken twice
    tb = cue(3, "Eannatum marks"); gline(fr, smooth(BORDER, 8), color=INK, width=6, frac=fr.R(tb + 0.3, 1.8), halo=WHITE, dash=(10, 7))
    for i, ll in enumerate(BORDER): tdot(fr, ll, a=fr.R(tb + 0.3 + i * 0.4, 0.3), r=6, color=PAPER, ring=INK)
    PQ(fr, 960, 150, "BORDER: STONES AND A DITCH", a=fr.R(tb + 0.5, 0.4) * (0 if v1 else 1), size=28)
    for txt, ph, y in (("AGAIN", "Umma breaks", 31.66), ("AND AGAIN", "And again", 31.58)):
        t0 = word(3, ph, "again"); arrow(fr, [(45.93, y + 0.02), (46.14, y)], t0, 0.6, color=UMM, width=7)
    PQ(fr, 560, 860, "AGAIN", a=fr.R(word(3, "Umma breaks", "again"), 0.3), size=32); PQ(fr, 560, 940, "AND AGAIN", a=fr.R(cue(3, "And again"), 0.3), size=32, light=True)

# ================= chapter 4
NORTH = cam_box(43.0, 46.6, 31.75, 34.3); KUN = cam_box(43.5, 47.5, 30.55, 33.5)
@sc("04a", "kish_akkad", NORTH, dict(akk=AKKAD))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "akk", AKK, fr.R(2.2, 1.0) * 0.6)
    PQ(fr, 380, 170, "2334 BC", a=fr.R(0.6, 0.4), size=36)
    region(fr, 44.55, 33.3, "AKKAD", a=fr.R(2.6, 0.5), size=34, color=WHITE); T(fr, P(fr.cam, 44.55, 33.3)[0], P(fr.cam, 44.55, 33.3)[1] + 44, "THE NORTH", size=18, sp=4, anchor="m", color=WHITE, a=fr.R(3.2, 0.5))
    town(fr, "KISH", r=7, side="b", size=24)
@sc("04b", "sargon_rise", KUN, dict(akk=AKKAD, sum=SUMER))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "akk", AKK, 0.6)
    town(fr, "KISH", r=7, side="t", size=24); town(fr, "URUK", r=7, side="l", size=24); town(fr, "NIPPUR", r=7, side="r", size=24)
    PQL(fr, *C["KISH"], "CUPBEARER", dx=-190, dy=20, a=fr.R(word(4, "The gardener", "cupbearer"), 0.4) * out(fr, 33.2), size=28)
    PQL(fr, *C["KISH"], "KING", dx=-150, dy=20, a=fr.R(word(4, "Then, somehow", "king"), 0.4), size=30)
    t1 = cue(4, "He defeats"); arrow(fr, [C["KISH"], (45.0, 32.0), (45.5, 31.5)], t1, 1.6, color=AKK, width=8)
    PQL(fr, *C["URUK"], "LUGALZAGESI", dx=-40, dy=62, a=fr.R(word(4, "He defeats", "Lugalzagesi"), 0.4), size=26, light=True)
    t2 = word(4, "He defeats", "leads him"); arrow(fr, [(45.62, 31.42), (45.5, 31.8), (45.28, 32.06)], t2, 1.6, color=INK, width=5, dash=None)
    PQL(fr, *C["NIPPUR"], "THE GATE OF ENLIL", dx=250, dy=-56, a=fr.R(word(4, "He defeats", "the gate"), 0.4), size=26)
@sc("04c", "akkad_sumer", KUN, dict(akk=AKKAD, sum=SUMER))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "akk", AKK, 0.6); terr(fr, "sum", AKK, fr.R(word(4, "For the first", "north and south"), 1.6) * 0.6)
    town(fr, "KISH", r=6, side="t", size=22); town(fr, "URUK", r=6, side="l", size=22); town(fr, "NIPPUR", r=6, side="r", size=22); town(fr, "UR", r=6, side="b", size=22)
    region(fr, 44.5, 33.42, "AKKAD", a=fr.R(word(4, "For the first", "Akkad"), 0.4), size=28, color=WHITE); region(fr, 46.2, 31.75, "SUMER", a=fr.R(word(4, "For the first", "Sumer"), 0.4), size=28, color=WHITE)
    PQ(fr, 1480, 200, "ONE KING", a=fr.R(word(4, "For the first", "answer"), 0.4), size=34)
    tq = word(4, "Sargon builds", "Akkad"); x, y = P(fr.cam, 44.22, 33.02)
    circ(fr, x, y, 30, color=PAPER, a=fr.R(tq, 0.4)); circ(fr, x, y, 30, outline=INK, a=fr.R(tq, 0.4), width=4); T(fr, x, y - 2, "?", size=40, w="b", anchor="m", a=fr.R(tq, 0.4))
    PQ(fr, x - 250, y - 10, "THE CITY OF AKKAD", a=fr.R(tq, 0.4), size=26); PQ(fr, x - 250, y + 62, "NEVER FOUND", a=fr.R(cue(4, "Archaeologists have never"), 0.4), size=26, light=True)
GUTC = cam_box(42.2, 49.4, 30.4, 36.2)
@sc("04d", "gutians", GUTC, dict(emp=U(AKKAD, SUMER)))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "emp", AKK, 0.6 - 0.25 * fr.R(86.0, 1.6))
    for i, pts in enumerate(([(46.9, 35.3), (45.9, 34.5), (44.9, 33.6)], [(47.7, 34.2), (46.7, 33.4), (45.6, 32.6)], [(48.4, 33.1), (47.3, 32.5), (46.3, 31.9)])): arrow(fr, pts, 85.1 + i * 0.25, 1.3, color=GUT, width=8)
    region(fr, 47.9, 34.75, "GUTIANS", a=fr.R(word(4, "Raiders", "Gutians"), 0.4), size=30); modern(fr, 47.2, 35.6, "ZAGROS MOUNTAINS", a=1.0, size=17)

# ================= chapter 5
@sc("05a", "ur", SUMERC, dict(sum=SOUTH))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "sum", UR3, fr.R(1.2, 1.6) * 0.55)
    tu = word(5, "Out of the", "Ur"); tdot(fr, C["UR"], r=9, color=AKK, a=fr.R(0.4, 0.4)); pulse(fr, C["UR"], tu, 1.8, color=AKK); PQL(fr, *C["UR"], "UR", dx=-90, dy=6, a=fr.R(tu, 0.4), size=38)
    for nm, side in (("URUK", "l"), ("NIPPUR", "r"), ("LAGASH", "r")): town(fr, nm, r=5, side=side, size=19)
RUNC = cam_box(44.3, 47.3, 30.45, 32.65); RUN = [C["NIPPUR"], (45.40, 31.90), (45.55, 31.62), (45.72, 31.36), (45.92, 31.14), C["UR"]]
@sc("05b", "shulgi_run", RUNC, dict(sum=SOUTH))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "sum", UR3, 0.55)
    town(fr, "NIPPUR", r=7, side="t", size=24); town(fr, "UR", r=7, side="b", size=24)
    PQ(fr, 420, 180, "SHULGI", size=34); PQ(fr, 420, 262, "A GOD", a=fr.R(word(5, "Shulgi also", "a god"), 0.4), size=30, light=True)
    t1 = word(5, "One hymn", "ran from"); t2 = word(5, "One hymn", "and back"); rp = smooth(RUN, 8)
    gline(fr, rp, color=INK, width=6, frac=fr.R(t1, 3.4), halo=WHITE); mover_dot(fr, rp, t1, 3.4, r=9, color=AKK)
    PQL(fr, 45.62, 31.52, "160 KM", dx=170, dy=-10, a=fr.R(word(5, "One hymn", "about a hundred"), 0.4), size=32)
    gline(fr, [(x + 0.05, y + 0.03) for x, y in rp[::-1]], color=AKK, width=5, frac=fr.R(t2, 1.6), halo=WHITE, arrow=True); mover_dot(fr, [(x + 0.05, y + 0.03) for x, y in rp[::-1]], t2, 1.6, r=9, color=AKK)
    PQL(fr, 45.62, 31.52, "AND BACK", dx=170, dy=62, a=fr.R(t2, 0.4), size=28, light=True); PQ(fr, 420, 344, "ONE DAY", a=fr.R(word(5, "One hymn", "in a single"), 0.4), size=30)
FALLC = cam_box(39.6, 51.4, 28.9, 35.6)
@sc("05c", "fall_of_ur", FALLC, dict(sum=SOUTH, ela=ELAM))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "sum", UR3, 0.55 * out(fr, 79.6, 1.6) + 0.12 * fr.R(79.6, 1.6))
    town(fr, "UR", r=7, side="b", size=24, color=INK)
    ta = word(5, "Nomads", "Amorites")
    for i, pts in enumerate(([(41.0, 34.4), (42.2, 33.9), (43.5, 33.3)], [(41.2, 32.9), (42.6, 32.6), (43.9, 32.2)], [(42.4, 31.2), (43.6, 31.3), (44.8, 31.3)])): arrow(fr, pts, ta - 0.4 + i * 0.25, 1.4, color=AMO, width=8)
    region(fr, 41.4, 33.55, "AMORITES", a=fr.R(ta, 0.4), size=28)
    PQ(fr, 440, 860, "GRAIN ×60", a=fr.R(word(5, "Under the last", "the price"), 0.4) * out(fr, 73.6), size=34)
    PQ(fr, 440, 860, "2004 BC", a=fr.R(cue(5, "In 2004"), 0.4), size=36)
    te = word(5, "In 2004", "Elam"); terr(fr, "ela", ELA, fr.R(te - 0.5, 0.8)); region(fr, 50.2, 31.6, "ELAM", a=fr.R(te, 0.4), size=30, color=WHITE); modern(fr, 50.6, 33.9, "IRAN", a=fr.R(word(5, "In 2004", "Iran"), 0.4), size=22)
    town(fr, "SUSA", a=fr.R(te, 0.4), r=5.5, side="t", size=20)
    arrow(fr, [C["SUSA"], (47.6, 31.75), (46.9, 31.3), (46.2, 31.02)], word(5, "In 2004", "sacks"), 1.6, color=ELA, width=8); pulse(fr, C["UR"], word(5, "In 2004", "sacks") + 1.4, 2.2, color=ELA)

# ================= chapter 6
BABC = cam_box(42.9, 46.7, 31.2, 33.85); HAMC = cam_box(41.6, 49.2, 29.7, 35.0)
@sc("06a", "babylon", BABC, dict(sou=SOUTH))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "sou", AMO, fr.R(0.4, 1.4) * 0.45)
    region(fr, 45.6, 31.75, "AMORITES", a=fr.R(0.6, 0.5), size=30)
    for nm, side in (("KISH", "r"), ("NIPPUR", "r")): town(fr, nm, r=4.5, side=side, size=18)
    tb = cue(6, "Its name"); tdot(fr, C["BABYLON"], a=fr.R(3.6, 0.4), r=7, color=BAB_D); pulse(fr, C["BABYLON"], tb, 1.8, color=BAB_D); PQL(fr, *C["BABYLON"], "BABYLON", dx=-170, dy=4, a=fr.R(tb, 0.4), size=36)
@sc("06b", "hammurabi", HAMC, dict(core=BABCORE, sou=SOUTH))
def _(fr, t):
    rivers_bold(fr, 4.0); k = fr.R(cue(6, "By the end") - 1.6, 3.0)
    terr(fr, "core", BAB, 1.0 - k); terr(fr, "sou", BAB, k)
    tdot(fr, C["BABYLON"], r=8, color=BAB_D); PQL(fr, *C["BABYLON"], "BABYLON", dx=-150, dy=-6, size=30)
    PQ(fr, 1380, 190, "HAMMURABI", size=34)
    PQ(fr, 1380, 272, "ALL OF SOUTHERN MESOPOTAMIA", a=fr.R(word(6, "By the end", "all of"), 0.4), size=24, light=True); PQ(fr, 1380, 346, "CAPITAL FOR 1,000+ YEARS", a=fr.R(word(6, "By the end", "its capital"), 0.4), size=24)

# ================= chapter 8
HITC = cam_box(30.5, 49.5, 29.3, 41.6)
MURSILI = [C["HATTUSA"], (35.6, 38.6), (36.6, 37.3), C["ALEPPO"], (38.3, 35.9), (39.6, 35.3), C["MARI"], (42.2, 34.0), (43.4, 33.4), C["BABYLON"]]
@sc("08a", "hittite_raid", HITC, dict(sou=SOUTH, core=BABYLONIA))
def _(fr, t):
    rivers_bold(fr, 3.6); k = fr.R(0.4, 2.8); terr(fr, "sou", BAB, 1 - k); terr(fr, "core", BAB, k * 0.75)
    tdot(fr, C["BABYLON"], r=7, color=BAB_D); TL(fr, *C["BABYLON"], "BABYLON", dx=14, dy=22, size=22)
    PQ(fr, 1500, 760, "1595 BC", a=fr.R(word(8, "Then, in 1595", "1595"), 0.4), size=36)
    tm = word(8, "Then, in 1595", "Mursili"); town(fr, "HATTUSA", a=fr.R(tm - 0.6, 0.4), r=6, side="t", size=22, color=INK); region(fr, 33.6, 38.9, "HITTITES", a=fr.R(tm - 0.6, 0.4), size=26)
    PQL(fr, *C["HATTUSA"], "MURSILI", dx=190, dy=0, a=fr.R(tm, 0.4), size=28, light=True)
    rp = smooth(MURSILI, 8); t1 = word(8, "Then, in 1595", "marches"); t2 = cue(8, "Then he simply")
    gline(fr, rp, color=HIT, width=7, frac=fr.R(t1, 3.4), halo=WHITE, arrow=fr.v < t2)
    pulse(fr, C["BABYLON"], word(8, "Then, in 1595", "sacks"), 2.2, color=HIT)
    PQL(fr, *C["BABYLON"], "MARDUK", dx=190, dy=-40, a=fr.R(word(8, "Then, in 1595", "the statue"), 0.4), size=28)
    back = [(x + 0.25, y + 0.3) for x, y in rp[::-1]]; gline(fr, back, color=HIT, width=5, frac=fr.R(t2, 1.5), halo=WHITE, arrow=True, dash=(12, 8)); mover_dot(fr, back, t2, 1.5, r=8, color=GOLD)
KASC = cam_box(40.8, 50.2, 29.7, 36.6)
@sc("08b", "kassites", KASC, dict(bab=BABYLONIA))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "bab", KAS, fr.R(cue(8, "Foreigners"), 1.6))
    for i, pts in enumerate(([(47.4, 34.9), (46.3, 34.3), (45.2, 33.6)], [(48.2, 33.9), (47.0, 33.3), (45.9, 32.7)])): arrow(fr, pts, 17.4 + i * 0.3, 1.5, color=KAS, width=8)
    region(fr, 48.2, 34.75, "KASSITES", a=fr.R(word(8, "Into the gap", "Kassites"), 0.4), size=30); modern(fr, 47.6, 35.75, "ZAGROS MOUNTAINS", size=17)
    tdot(fr, C["BABYLON"], r=7, color=BAB_D); PQL(fr, *C["BABYLON"], "BABYLON", dx=-150, dy=-6, size=28)
    PQ(fr, 420, 190, "400+ YEARS", a=fr.R(word(8, "Foreigners", "more than four"), 0.4), size=34); PQ(fr, 420, 270, "THE LONGEST DYNASTY", a=fr.R(word(8, "Foreigners", "the longest"), 0.4), size=24, light=True)
GKC = cam_box(28.0, 49.0, 25.6, 41.6)
CAPS = dict(EGYPT=C["AMARNA"], HITTITES=C["HATTUSA"], MITANNI=C["WASHUKANNI"], ASSYRIA=C["ASHUR"], BABYLON=C["BABYLON"])
@sc("08c", "great_kings", GKC, dict(egy=EGYPT, hit=HATTI, mit=MITANNI, asy=ASSYRIA14, bab=BABYLONIA))
def _(fr, t):
    rivers_bold(fr, 3.2); LAB = (("egy", "Egypt", EGY, (31.3, 29.2), "EGYPT"), ("hit", "the Hittites", HIT, (33.6, 38.6), "HITTITES"), ("mit", "Mitanni", MIT, (39.5, 37.35), "MITANNI"), ("asy", "Assyria", ASY, (43.5, 36.35), "ASSYRIA"), ("bab", "Babylon", BAB, (46.0, 32.0), "BABYLONIA"))
    for key, nm, col, ll, lab in LAB: terr(fr, key, col, fr.R(word(8, "Egypt, the Hittites", nm), 0.6))
    tl = word(8, "Egypt, the Hittites", "write to")
    for k, (i, j) in enumerate((("EGYPT", "HITTITES"), ("EGYPT", "MITANNI"), ("EGYPT", "ASSYRIA"), ("EGYPT", "BABYLON"), ("HITTITES", "BABYLON"))):
        gline(fr, arc(CAPS[i], CAPS[j], 0.10 if k % 2 else -0.10), color=INK, width=3.4, frac=fr.R(tl + k * 0.25, 1.1), halo=WHITE, dash=(10, 7))
    for nm in CAPS: tdot(fr, CAPS[nm], a=fr.R(tl, 0.4), r=5.5, color=PAPER, ring=INK)
    for key, nm, col, ll, lab in LAB: region(fr, ll[0], ll[1], lab, a=fr.R(word(8, "Egypt, the Hittites", nm), 0.4), size=17 if lab == "ASSYRIA" else 22 if lab in ("MITANNI", "BABYLONIA") else 26, color=WHITE)
    PQ(fr, 1500, 860, "GREAT KINGS · BROTHERS", a=fr.R(tl, 0.4), size=26); PQ(fr, 1500, 934, "AKKADIAN", a=fr.R(word(8, "Egypt, the Hittites", "in Akkadian"), 0.4), size=30, light=True)
ELC = cam_box(41.8, 51.0, 29.5, 34.7)
TROPHY = [C["SIPPAR"], (45.3, 33.0), (46.6, 32.7), (47.5, 32.4), C["SUSA"]]
def _ins(name, h):
    f = os.path.join(HERE, "../inserts", name + ".png")
    if not os.path.exists(f): return None
    im = Image.open(f).convert("RGBA"); return im.resize((max(1, int(im.size[0] * h * SS / im.size[1])), int(h * SS)), Image.LANCZOS)
_INS = {}
@sc("08d", "elam_trophies", ELC, dict(bab=BABYLONIA, ela=ELAM))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "bab", KAS, 1.0 - 0.75 * fr.R(word(8, "Around 1158", "the Kassite"), 2.0)); terr(fr, "ela", ELA, 1.0)
    region(fr, 50.0, 31.7, "ELAM", size=30, color=WHITE); town(fr, "SUSA", r=7, side="t", size=24); tdot(fr, C["BABYLON"], r=7, color=BAB_D); TL(fr, *C["BABYLON"], "BABYLON", dx=-14, dy=24, size=22, anchor="r")
    PQ(fr, 400, 180, "1158 BC", a=fr.R(word(8, "Around 1158", "1158"), 0.4), size=36)
    arrow(fr, [C["SUSA"], (47.2, 32.6), (46.0, 32.8), (44.9, 32.75)], word(8, "Around 1158", "Elam raids"), 1.8, color=ELA, width=8, a=out(fr, cue(8, "The Elamite") + 2.0, 1.0))
    PQ(fr, 400, 262, "SHUTRUK-NAHHUNTE", a=fr.R(word(8, "The Elamite", "Shutruk"), 0.4), size=26, light=True)
    tp = smooth(TROPHY, 8); t1 = word(8, "The Elamite", "the victory"); t2 = word(8, "The Elamite", "and the law"); te = cue(8, "That is why")
    gline(fr, tp, color=INK, width=5, frac=fr.R(word(8, "The Elamite", "carries"), 2.0), halo=WHITE, dash=(12, 8), arrow=True)
    for nm, lab, t0, off in (("V08", "STELE OF NARAM-SIN", t1, -1), ("V13", "LAWS OF HAMMURABI", t2, 1)):
        if fr.v < t0: continue
        live(fr, t0, t0 + 3.0); q = ease(min(1.0, (fr.v - t0) / 3.0)); ll = along(tp, q * 0.78); x, y = P(fr.cam, *ll); a = fr.R(t0, 0.4)
        if nm not in _INS: _INS[nm] = _ins(nm, 190)
        im = _INS[nm]
        if im is not None:
            px = (int(s(x + off * 105) - im.size[0] / 2), int(s(y - 120) - im.size[1] / 2)); fr.im.paste(im, px, im.getchannel("A").point(lambda v: int(v * a))); fr.d = ImageDraw.Draw(fr.im)
            T(fr, x + off * 105, y - (236 if off < 0 else 258), lab, size=15, sp=3, anchor="m", w="b", a=a)
        else: PQ(fr, x, y + off * 46, lab, a=a, size=22, light=(off > 0))
    modern(fr, 49.7, 33.75, "IRAN", a=fr.R(word(8, "That is why", "but in Iran"), 0.4), size=26); modern(fr, 44.4, 31.3, "IRAQ", a=fr.R(word(8, "That is why", "not in Iraq"), 0.4), size=26)
    PQ(fr, 400, 900, "FOUND AT SUSA · 1901–02", a=fr.R(word(8, "That is why", "three thousand"), 0.4), size=24, light=True); PQ(fr, 400, 974, "THE LOUVRE", a=fr.R(word(8, "Today both", "Louvre"), 0.4), size=30)

# ================= chapter 9
ASC = cam_box(38.3, 48.3, 32.4, 38.6)
RAIDS = [[(43.2, 35.9), (41.6, 36.4), (39.9, 36.6), (38.6, 36.5)], [(43.3, 36.3), (43.0, 37.3), (42.4, 38.2)], [(43.5, 35.9), (45.0, 36.0), (46.4, 35.7)], [(43.4, 35.3), (44.0, 34.2), (44.5, 33.2)], [(43.0, 35.05), (41.8, 34.5), (40.6, 34.1)], [(43.6, 36.2), (44.8, 37.0), (45.9, 37.6)]]
@sc("09a", "assyria", ASC, dict(asy=ASSYRIA))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "asy", ASY, fr.R(cue(9, "Its people"), 1.0))
    ta = word(9, "Up the Tigris", "Ashur"); tdot(fr, C["ASHUR"], a=fr.R(1.6, 0.4), r=8, color=ASY_D); pulse(fr, C["ASHUR"], ta, 1.8, color=ASY_D)
    PQL(fr, *C["ASHUR"], "ASHUR", dx=-140, dy=-6, a=fr.R(ta, 0.4), size=34)
    region(fr, 43.45, 36.55, "ASSYRIANS", a=fr.R(word(9, "Its people", "Assyrians"), 0.4), size=24, color=WHITE)
    tdot(fr, C["BABYLON"], r=5, color=BAB_D); TL(fr, *C["BABYLON"], "BABYLON", dx=12, dy=20, size=18)
    PQ(fr, 400, 180, "900s BC", a=fr.R(word(9, "From the 900s", "900s"), 0.4), size=36); PQ(fr, 400, 262, "WAR ALMOST EVERY YEAR", a=fr.R(word(9, "From the 900s", "almost"), 0.4), size=24, light=True)
    for i, pts in enumerate(RAIDS): arrow(fr, pts, 9.4 + i * 0.5, 1.0, color=ASY_D, width=7, a=out(fr, 19.6, 0.8))
    tn = word(9, "Ashurnasirpal", "Nimrud"); tdot(fr, C["NIMRUD"], a=fr.R(tn - 0.3, 0.3), r=8, color=PAPER, ring=ASY_D); pulse(fr, C["NIMRUD"], tn, 1.6, color=ASY_D)
    PQL(fr, *C["NIMRUD"], "NIMRUD", dx=150, dy=-30, a=fr.R(tn, 0.4), size=32); PQL(fr, *C["NIMRUD"], "ASHURNASIRPAL II", dx=215, dy=-100, a=fr.R(cue(9, "Ashurnasirpal"), 0.4), size=24, light=True)
DEPC = cam_box(28.5, 52.5, 24.0, 41.0)
ASY8 = Dm(EMPIRE_ASY, M([(28, 22), (34.25, 22), (34.25, 31.2), (33.6, 31.45), (28, 32.5)], False))
MOVES = [[(35.6, 33.2), (38.5, 35.4), (42.0, 36.6)], [(46.4, 33.0), (42.5, 34.8), (38.0, 36.2)], [(37.0, 37.6), (41.0, 35.5), (45.6, 32.2)], [(44.6, 36.9), (40.0, 36.0), (36.2, 34.6)], [(36.4, 35.4), (41.0, 34.4), (47.4, 34.4)], [(45.2, 31.8), (41.4, 33.6), (36.4, 33.0)]]
@sc("09b", "deportations", DEPC, dict(emp=ASY8, isr=ISRAEL))
def _(fr, t):
    rivers_bold(fr, 3.2); terr(fr, "emp", ASY, 0.8)
    tdot(fr, C["NIMRUD"], r=6, color=ASY_D); TL(fr, *C["NIMRUD"], "ASSYRIA", dx=14, dy=-22, size=22, color=WHITE)
    for i, pts in enumerate(MOVES): gline(fr, smooth(pts, 10), color=PAPER, width=4.2, frac=fr.R(62.3 + i * 0.5, 1.6), halo=ASY_D, arrow=True, a=1.0 - 0.6 * fr.R(cue(9, "In the 720s"), 0.8))
    PQ(fr, 420, 180, "≈ 4,000,000 PEOPLE MOVED", a=fr.R(word(9, "One estimate", "some four"), 0.4) * out(fr, cue(9, "In the 720s")), size=28); PQ(fr, 420, 256, "OVER 250 YEARS", a=fr.R(word(9, "One estimate", "over two"), 0.4) * out(fr, cue(9, "In the 720s")), size=24, light=True)
    ti = cue(9, "In the 720s"); PQ(fr, 420, 180, "720s BC", a=fr.R(ti, 0.4), size=36)
    terr(fr, "isr", BAB, fr.R(ti + 0.6, 0.5)); tdot(fr, C["SAMARIA"], a=fr.R(ti + 0.6, 0.4), r=6, color=BAB_D); PQL(fr, *C["SAMARIA"], "ISRAEL", dx=-130, dy=0, a=fr.R(word(9, "In the 720s", "Israel"), 0.4), size=28, light=True)
    for i, pts in enumerate(([C["SAMARIA"], (37.6, 35.0), (40.0, 36.7)], [C["SAMARIA"], (38.5, 34.2), (43.0, 36.2)], [C["SAMARIA"], (40.0, 33.6), (44.5, 34.6), (48.0, 34.9)])): arrow(fr, pts, word(9, "In the 720s", "destroyed") + i * 0.3, 1.8, color=BAB_D, width=6)
    PQ(fr, 1420, 900, "THE TEN LOST TRIBES", a=fr.R(word(9, "Its deported", "the ten"), 0.4), size=30)
JUC = cam_box(33.2, 37.0, 30.55, 33.25)
LEV_P = [(34.2, 31.2), (34.6, 31.25), (34.75, 31.85), (35.1, 31.95), (35.55, 31.95), (35.9, 32.3), (36.2, 33.0), (36.6, 33.6), (36.6, 34.5), (33.0, 34.5), (33.0, 31.2)]
@sc("09c", "judah", JUC, dict(jud=JUDAH, emp=Dm(R(LEV_P, 0.05, 0.1), JUDAH)))
def _(fr, t):
    terr(fr, "emp", ASY, 0.8); terr(fr, "jud", BAB, 1.0)
    region(fr, 35.12, 31.42, "JUDAH", size=24, color=WHITE, dy=22); sea(fr, 33.85, 32.6, "MEDITERRANEAN", size=16)
    PQ(fr, 1480, 180, "701 BC", a=fr.R(0.0 + cue(9, "In 701"), 0.4), size=36); PQ(fr, 1480, 262, "SENNACHERIB", a=fr.R(word(9, "In 701", "Sennacherib"), 0.4), size=28, light=True)
    arrow(fr, [(35.6, 33.2), (35.1, 32.6), (34.8, 32.0), (34.85, 31.64)], word(9, "In 701", "invades"), 1.8, color=ASY_D, width=9)
    tl = word(9, "His palace reliefs", "Lachish") - 1.0; tdot(fr, C["LACHISH"], a=fr.R(77.2, 0.4), r=7, color=PAPER, ring=INK); PQL(fr, *C["LACHISH"], "LACHISH", dx=-150, dy=10, a=fr.R(77.4, 0.4), size=28)
    tj = cue(9, "Then he surrounds"); tdot(fr, C["JERUSALEM"], r=8, color=PAPER, ring=INK); PQL(fr, *C["JERUSALEM"], "JERUSALEM", dx=200, dy=-6, a=fr.R(82.7, 0.3), size=30)
    x, y = P(fr.cam, *C["JERUSALEM"]); k = fr.R(tj + 0.2, 1.4)
    if k > 0: alpha_draw(fr, lambda d, c: d.arc([s(x - 46), s(y - 46), s(x + 46), s(y + 46)], -90, -90 + 360 * k, fill=c, width=s(8)), ASY_D, 1.0)
    th = cue(9, "He never took"); PQ(fr, 1480, 760, "NEVER TOOK THE CITY", a=fr.R(th, 0.4), size=28); PQ(fr, 1480, 836, "TRIBUTE", a=fr.R(word(9, "He took tribute", "tribute"), 0.4), size=28, light=True)
    arrow(fr, [(35.45, 31.95), (35.9, 32.5), (36.5, 33.1)], cue(9, "He took tribute") + 0.4, 1.3, color=ASY_D, width=8)

# ================= chapter 10
EMPC = cam_box(27.5, 52.5, 24.3, 39.6)
@sc("10a", "assyria_max", EMPC, dict(emp=EMPIRE_ASY))
def _(fr, t):
    rivers_bold(fr, 3.2); terr(fr, "emp", ASY, 0.3 + 0.7 * fr.R(5.4, 1.4))
    tdot(fr, C["NINEVEH"], r=7, color=PAPER, ring=ASY_D); TL(fr, *C["NINEVEH"], "NINEVEH", dx=14, dy=-20, size=22, color=WHITE)
    PQL(fr, 31.3, 28.6, "THE NILE", dx=-10, dy=150, a=fr.R(word(10, "At its height", "from the Nile"), 0.4), size=28); PQL(fr, 50.2, 33.2, "THE MOUNTAINS OF IRAN", dx=130, dy=-110, a=fr.R(word(10, "At its height", "to the mountains"), 0.4), size=26)
    PQ(fr, 400, 170, "ASHURBANIPAL · 668 BC", size=28, light=True)
NINC = cam_box(39.6, 47.0, 33.4, 38.2)
@sc("10b", "nineveh", NINC, dict(asy=ASSYRIA))
def _(fr, t):
    rivers_bold(fr, 4.0); terr(fr, "asy", ASY, 0.9)
    tn = word(10, "At Nineveh he built", "Nineveh"); tdot(fr, C["NINEVEH"], r=9, color=PAPER, ring=ASY_D); pulse(fr, C["NINEVEH"], tn, 2.0, color=ASY_D)
    PQL(fr, *C["NINEVEH"], "NINEVEH", dx=-170, dy=0, size=36)
    PQ(fr, 1330, 800, "THE GREATEST LIBRARY", a=fr.R(word(10, "At Nineveh he built", "the greatest"), 0.4), size=30); PQ(fr, 1330, 876, "OF THE ANCIENT NEAR EAST", a=fr.R(word(10, "At Nineveh he built", "of the ancient"), 0.4), size=26, light=True)
@sc("10c", "fall_of_nineveh", EMPC, dict(emp=EMPIRE_ASY, bab=BABYLONIA, med=MEDIA))
def _(fr, t):
    rivers_bold(fr, 3.2); t6 = cue(10, "In 612"); k = fr.R(cue(10, "Within twenty"), 6.0)
    terr(fr, "emp", ASY, 1.0 - 0.8 * k); terr(fr, "bab", BAB, fr.R(t6 - 0.6, 0.8)); terr(fr, "med", MED, fr.R(t6 - 0.3, 0.8))
    tdot(fr, C["NINEVEH"], r=7, color=PAPER, ring=ASY_D); TL(fr, *C["NINEVEH"], "NINEVEH", dx=-14, dy=-20, size=22, color=WHITE, anchor="r")
    PQ(fr, 420, 180, "631 BC", a=fr.R(word(10, "Ashurbanipal dies", "631"), 0.4) * out(fr, t6), size=36); PQ(fr, 420, 180, "612 BC", a=fr.R(t6, 0.4), size=36)
    arrow(fr, [C["BABYLON"], (44.2, 34.2), (43.6, 35.6), (43.25, 36.2)], word(10, "In 612", "Babylonians") , 1.6, color=BAB_D, width=8); arrow(fr, [C["ECBATANA"], (46.8, 35.6), (45.0, 36.3), (43.5, 36.4)], word(10, "In 612", "Medes"), 1.6, color=MED, width=8)
    PQL(fr, *C["BABYLON"], "BABYLONIANS", dx=-170, dy=30, a=fr.R(word(10, "In 612", "Babylonians"), 0.4), size=24); PQL(fr, *C["ECBATANA"], "MEDES", dx=150, dy=10, a=fr.R(word(10, "In 612", "Medes"), 0.4), size=24, light=True)
    tb = word(10, "In 612", "storms"); pulse(fr, C["NINEVEH"], tb, 2.6, color=(200, 90, 30)); cross(fr, *C["NINEVEH"], a=fr.R(word(10, "In 612", "burns"), 0.3), r=15, width=7, color=INK)

# ================= chapter 11
NBC = cam_box(31.0, 51.5, 26.3, 39.6)
@sc("11a", "babylon_max", NBC, dict(emp=EMPIRE_BAB))
def _(fr, t):
    rivers_bold(fr, 3.4); terr(fr, "emp", BAB, fr.R(0.3, 2.0))
    city(fr, "BABYLON", r=8, size=1, label="", dot=PAPER, ring=BAB_D, icon=False); PQL(fr, *C["BABYLON"], "BABYLON", dx=150, dy=40, size=32)
    PQ(fr, 420, 180, "NEBUCHADNEZZAR II", a=fr.R(word(11, "Under Nebuchadnezzar", "Nebuchadnezzar"), 0.4), size=28); PQ(fr, 420, 258, "605 BC", a=fr.R(word(11, "Under Nebuchadnezzar", "605"), 0.4), size=34, light=True)
GARC = cam_box(40.6, 47.6, 31.4, 37.3)
@sc("11b", "gardens", GARC, {})
def _(fr, t):
    rivers_bold(fr, 4.0)
    tdot(fr, C["BABYLON"], r=8, color=BAB_D); TL(fr, *C["BABYLON"], "BABYLON", dx=-16, dy=0, size=26, anchor="r")
    fr.plaque_at(*C["BABYLON"], "THE HANGING GARDENS", dx=250, dy=60, size=26, strike=fr.R(cue(11, "Babylon's most famous"), 1.2))
    tn = word(11, "Some scholars", "Sennacherib"); gline(fr, arc(C["BABYLON"], C["NINEVEH"], -0.14), color=INK, width=4.5, frac=fr.R(tn - 1.2, 1.6), halo=WHITE, dash=(12, 8), arrow=True)
    tdot(fr, C["NINEVEH"], a=fr.R(tn - 0.4, 0.4), r=8, color=ASY_D); TL(fr, *C["NINEVEH"], "NINEVEH", dx=-16, dy=0, size=26, anchor="r", a=fr.R(tn - 0.4, 0.4))
    PQL(fr, *C["NINEVEH"], "SENNACHERIB'S GARDENS?", dx=270, dy=60, a=fr.R(tn, 0.4), size=26, light=True)
EXC = cam_box(32.6, 47.4, 29.3, 37.6)
EXILE = [C["JERUSALEM"], (35.9, 33.0), (36.4, 34.4), (36.9, 35.8), (38.2, 36.2), (39.4, 35.6), C["MARI"], (42.3, 33.9), (43.5, 33.2), C["BABYLON"]]
@sc("11c", "exile", EXC, dict(emp=EMPIRE_BAB))
def _(fr, t):
    rivers_bold(fr, 3.8); terr(fr, "emp", BAB, 0.8)
    tdot(fr, C["BABYLON"], r=8, color=PAPER, ring=BAB_D); PQL(fr, *C["BABYLON"], "BABYLON", dx=150, dy=40, size=30)
    PQ(fr, 420, 180, "587 BC", a=fr.R(46.6, 0.4), size=36)
    tj = word(11, "In 587", "destroys"); tdot(fr, C["JERUSALEM"], r=8, color=PAPER, ring=INK); PQL(fr, *C["JERUSALEM"], "JERUSALEM", dx=-180, dy=30, size=28, light=True)
    pulse(fr, C["JERUSALEM"], tj, 2.4, color=(200, 90, 30)); cross(fr, *C["JERUSALEM"], a=fr.R(tj + 0.8, 0.3), r=14, width=7)
    te = word(11, "In 587", "takes its"); rp = smooth(EXILE, 8); gline(fr, rp, color=PAPER, width=6, frac=fr.R(te - 1.2, 2.2), halo=BAB_D, arrow=True)
EXA = cam_box(32.0, 49.0, 24.6, 35.0)
@sc("11d", "tema", EXA, dict(emp=EMPIRE_BAB))
def _(fr, t):
    rivers_bold(fr, 3.6); terr(fr, "emp", BAB, 0.8)
    tdot(fr, C["BABYLON"], r=8, color=PAPER, ring=BAB_D); TL(fr, *C["BABYLON"], "BABYLON", dx=16, dy=-22, size=24, color=WHITE)
    gline(fr, arc(C["BABYLON"], C["TEMA"], 0.14), color=INK, width=5, frac=fr.R(60.6, 1.4), halo=WHITE, arrow=True)
    tt = word(11, "He spends", "an oasis"); tdot(fr, C["TEMA"], a=fr.R(tt - 0.6, 0.4), r=8, color=GRN, ring=WHITE); pulse(fr, C["TEMA"], tt, 2.0, color=GRN)
    PQL(fr, *C["TEMA"], "TEMA", dx=-110, dy=0, a=fr.R(tt, 0.4), size=30); region(fr, 43.6, 26.0, "ARABIA", a=fr.R(word(11, "He spends", "Arabia"), 0.4), size=30)
    PQL(fr, *C["TEMA"], "TEN YEARS", dx=-110, dy=68, a=fr.R(word(11, "He spends", "ten years"), 0.4), size=26, light=True)
    PQL(fr, *C["BABYLON"], "BELSHAZZAR", dx=200, dy=40, a=fr.R(word(11, "He spends", "Belshazzar"), 0.4), size=28)
PERC = cam_box(36.0, 57.0, 26.0, 39.0)
PERS = PERSIA
@sc("11e", "cyrus", PERC, dict(emp=EMPIRE_BAB, per=PERS))
def _(fr, t):
    rivers_bold(fr, 3.4); tg = word(11, "In 539", "opens"); k = fr.R(tg, 2.6)
    terr(fr, "emp", BAB, 1.0 - k); terr(fr, "emp", PER, k); terr(fr, "per", PER, 1.0)
    region(fr, 52.4, 32.6, "PERSIANS", size=30, color=WHITE)
    tdot(fr, C["BABYLON"], r=8, color=PAPER, ring=BAB_D); PQL(fr, *C["BABYLON"], "BABYLON", dx=-150, dy=40, size=30)
    PQ(fr, 420, 180, "539 BC", a=fr.R(word(11, "In 539", "539"), 0.4), size=36); PQ(fr, 420, 262, "CYRUS", a=fr.R(word(11, "In 539", "Cyrus"), 0.4), size=30, light=True)
    arrow(fr, [C["ECBATANA"], (46.9, 34.3), (45.4, 33.7), (44.55, 33.3), (44.45, 32.75)], word(11, "In 539", "defeats"), 2.2, color=PER, width=9)
    PQ(fr, 1420, 900, "NEVER AGAIN KINGS OF ITS OWN", a=fr.R(word(11, "Mesopotamia will", "never"), 0.4), size=26)

# ================= chapter 12
ALC = cam_box(20.0, 50.5, 25.5, 43.2)
ALEX = [C["PELLA"], (25.5, 40.7), (26.6, 40.2), C["SARDIS"], (30.6, 37.9), (32.5, 37.9), (34.9, 37.0), C["ISSUS"], (36.0, 35.0), C["TYRE"], (34.4, 31.4), (32.4, 31.0), C["MEMPHIS"], (32.6, 31.05), (34.6, 31.6),
        (35.6, 33.4), (37.2, 35.6), (38.9, 36.6), (41.2, 37.0), C["GAUGAMELA"], (44.0, 35.0), (44.4, 33.6), C["BABYLON"]]
@sc("12a", "alexander", ALC, {})
def _(fr, t):
    rivers_bold(fr, 3.2); ta = word(12, "Alexander the Great", "Alexander"); rp = smooth(ALEX, 8)
    gline(fr, rp, color=MAC, width=6.5, frac=fr.R(ta, 4.2), halo=WHITE, arrow=True)
    region(fr, 23.3, 41.35, "MACEDON", a=fr.R(ta, 0.4), size=22); cross(fr, *C["GAUGAMELA"], a=fr.R(ta + 3.5, 0.3), r=11, width=6, color=MAC)
    tdot(fr, C["BABYLON"], r=8, color=PAPER, ring=BAB_D); PQL(fr, *C["BABYLON"], "BABYLON", dx=150, dy=44, size=30)
    PQ(fr, 420, 820, "ALEXANDER · 331 BC", a=fr.R(word(12, "Alexander the Great", "331"), 0.4), size=30); PQ(fr, 420, 898, "JUNE 323 BC", a=fr.R(word(12, "Alexander the Great", "June"), 0.4), size=30, light=True)
    pulse(fr, C["BABYLON"], word(12, "Alexander the Great", "dies"), 2.4, color=INK)
SELC = cam_box(42.6, 46.4, 31.75, 34.1)
@sc("12b", "seleucia", SELC, {})
def _(fr, t):
    rivers_bold(fr, 4.2); ts = word(12, "His successors", "Seleucia"); k = fr.R(word(12, "His successors", "slowly"), 2.5)
    tdot(fr, C["BABYLON"], r=9, color=mix(BAB_D, (150, 140, 120), k), ring=WHITE); T(fr, P(fr.cam, *C["BABYLON"])[0] - 22, P(fr.cam, *C["BABYLON"])[1], "BABYLON", size=32, w="b", anchor="r", color=mix(INK, (150, 140, 120), k * 0.85))
    tdot(fr, C["SELEUCIA"], a=fr.R(ts - 0.4, 0.4), r=9, color=MAC); pulse(fr, C["SELEUCIA"], ts, 2.0, color=MAC); PQL(fr, *C["SELEUCIA"], "SELEUCIA", dx=170, dy=0, a=fr.R(ts, 0.4), size=34)
    modern(fr, 45.35, 33.55, "TIGRIS", size=19, color=SEA_T); modern(fr, 43.55, 33.0, "EUPHRATES", size=19, color=SEA_T)
    T(fr, P(fr.cam, *C["SELEUCIA"])[0] + 170, P(fr.cam, *C["SELEUCIA"])[1] + 52, "A NEW GREEK CITY", size=18, sp=4, anchor="m", a=fr.R(ts, 0.4))

if __name__ == "__main__":
    import time
    mode = sys.argv[1]
    def clear(s_):
        s_.masks = {}; s_._cam = None; s_.base = None; s_.rmask = None; s_.rm = None; s_.lm = None; s_.desert = None; s_._plan = None
    if mode == "list":
        tot = 0
        for n, s_ in SC.items(): print(f"{n:24s} ch{s_.ch:02d}  VO {s_.t0:6.1f} - {s_.t0 + s_.dur:6.1f}  ({s_.dur:5.1f} s)"); tot += s_.dur
        print("total", round(tot, 1), len(SC))
    elif mode == "json":
        json.dump({n: dict(ch=s_.ch, t0=s_.t0, t1=round(s_.t0 + s_.dur, 3), id=n.split("_")[0], windows=WIN[(n.split("_")[0], s_.ch)]) for n, s_ in SC.items()}, open(f"{HERE}/../maps.json", "w"), indent=1)
    elif mode == "sheet":       # one still per layout window, near its end
        pref = sys.argv[3:]; ims = []
        for n, s_ in SC.items():
            if pref and not any(n.startswith(p) for p in pref): continue
            s_.frame(0.0)
            for a, b in WIN[(n.split("_")[0], s_.ch)]:
                tt = a + (b - a) * 0.95
                im = s_.frame(tt - s_.t0).resize((960, 540), Image.LANCZOS); d = ImageDraw.Draw(im); d.rectangle([0, 0, 380, 22], fill=(17, 17, 17))
                d.text((6, 5), f"{n}  ch{s_.ch} VO {tt:5.1f} ({a:.1f}-{b:.1f})", fill=(255, 255, 255)); ims.append(im)
            clear(s_)
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
            t0 = time.time(); SC[n].render(f"{HERE}/out_look"); clear(SC[n]); print(n, round(time.time() - t0, 1), flush=True)
