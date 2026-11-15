import sys, os
from functools import reduce
from engine import *
from PIL import ImageChops as IC

WHITE = (255, 255, 255)
def cam_at(lon, lat, S): return (lon, lat - 55.0 / S, S)
FULL = cam_full()

# ------------------------------------------------------------------ geography (lon, lat)
HELL = [(26.1, 39.95), (26.19, 40.025), (26.33, 40.10), (26.39, 40.15), (26.41, 40.20), (26.52, 40.28), (26.68, 40.38), (26.9, 40.47), (27.5, 40.7)]
BOSP = [(28.6, 40.85), (28.99, 41.0), (29.05, 41.08), (29.07, 41.14), (29.13, 41.24), (29.5, 41.5)]
AEG_COAST = [(27.9, 36.45), (27.25, 36.55), (27.15, 37.0), (27.1, 37.55), (26.95, 38.0), (26.25, 38.15), (26.3, 38.7), (26.7, 38.9), (26.6, 39.3), (26.0, 39.5)]
EMPIRE_CORE = (AEG_COAST + HELL + BOSP + [(31, 41.7), (33, 42.5), (35.2, 42.4), (37, 41.7), (39.5, 41.5), (41.3, 41.9), (41.2, 42.9),
    (42, 43.2), (45, 42.7), (47.5, 42.2), (48.6, 42.0), (53, 42), (56, 43), (59, 43.3), (61, 42.8), (64, 42.3), (67, 42), (69.5, 41.2), (71, 40.8),
    (72, 39), (72, 37), (73.5, 36), (74.5, 34.5), (74, 32), (73, 30), (71.5, 28), (70, 26), (69.5, 24.5), (68.5, 23.2), (66, 24.6), (62, 23), (57, 24),
    (56.6, 26.1), (54, 26), (51, 27), (49.6, 29.2), (48.4, 29.4), (47, 29.5), (44.5, 30.5), (42, 32), (39.5, 32.5), (37.5, 31), (36, 29.3), (35, 29),
    (34.6, 27.6), (36.2, 23.9), (35.3, 23.5), (30.5, 23.5), (28.5, 25), (25, 28), (22, 30), (20, 30.5), (19.8, 33.3), (24, 32.9), (29, 32.1), (32, 32.2),
    (31.6, 34), (31.6, 35.9), (29.5, 35.9)])
MEDIA = [(35.3, 42.4), (41.3, 42.5), (45, 42.7), (48.6, 42), (49.5, 38.5), (50, 37.2), (54, 37.2), (57, 38.5), (61, 37.5), (61.5, 34.5), (58.5, 31.8), (55.5, 31.6),
         (51, 33.5), (48, 33.5), (46, 35), (44, 36.5), (41.5, 37), (38.5, 37.2), (36.5, 38), (35, 39.5)]
ELAM = [(47.2, 33.3), (48, 33.5), (51, 33.5), (51.5, 31.5), (50.2, 30.2), (49.6, 29.2), (48.4, 29.4), (48.2, 31.5)]
PARSA = [(50.2, 30.2), (51.5, 31.5), (54, 31.2), (55.5, 29.5), (55.5, 27.3), (54, 26), (51, 27), (49.6, 29.2)]
LYDIA = AEG_COAST[1:] + HELL + BOSP + [(31, 41.7), (33, 42.5), (35.2, 42.4), (35, 39.5), (34.3, 38), (33.2, 37.2), (31, 37.1), (29, 36.9), (28.2, 36.85)]
BABYLON = [(48.2, 29.8), (48.2, 31.5), (47.2, 33.3), (46, 35), (44, 36.5), (41.5, 37), (38.5, 37.2), (36.4, 37.1), (35.6, 36.7), (35.2, 35), (34.6, 32.5),
           (34.0, 31.2), (34.9, 29.4), (36, 29.3), (37.5, 31), (39.5, 32.5), (42, 32), (44.5, 30.5), (47, 29.5)]
EGYPT = [(25, 32.2), (29, 32.2), (32.5, 32.0), (34.0, 31.25), (34.9, 29.4), (34.6, 27.6), (36.2, 23.9), (35.3, 23.4), (30.5, 23.4), (28.5, 25), (25, 28)]
EGSEL = [(18, 34.5), (29, 32.2), (32.5, 32.0), (34.0, 31.25), (34.9, 29.4), (34.6, 27.6), (37, 23), (18, 22)]
ANATSEL = [(24, 35.2), (36.3, 35.7), (36.4, 37.1), (38.5, 37.2), (36.5, 38), (35, 39.5), (35.3, 43), (24, 43)]
IONIA = [(26.0, 40.3), (27.2, 40.45), (27.6, 39.5), (27.95, 38.6), (28.05, 37.6), (28.4, 36.95), (28.0, 36.4), (27.0, 36.4), (26.9, 37.6), (25.9, 38.1), (25.8, 39.6)]
THRACE = ([(29.6, 41.7)] + BOSP[::-1] + HELL[::-1] + [(26.0, 40.0), (26.08, 40.27), (25.4, 40.62), (24.9, 40.87), (24.4, 40.86), (23.9, 40.78), (23.5, 41.2),
          (23.4, 41.6), (24.5, 42.6), (27, 43.6), (28.6, 44.2), (29.4, 43.5), (28.7, 42.3)])
MACEDON = [(22.55, 40.0), (21.6, 40.2), (21.2, 40.9), (22.0, 41.4), (23.4, 41.6), (23.5, 41.2), (23.9, 40.78), (23.75, 40.65), (23.4, 40.75), (23.05, 40.75),
           (22.9, 40.6), (22.7, 40.4), (22.62, 40.1)]
THESSALY = [(21.5, 39.2), (21.6, 39.95), (22.55, 40.0), (22.75, 39.85), (23.4, 39.3), (23.0, 38.95), (22.3, 38.87), (21.6, 39.0)]
BOEOTIA = [(22.85, 38.2), (22.85, 38.6), (23.3, 38.72), (23.72, 38.42), (23.7, 38.2), (23.2, 38.13)]

C = dict(BABYLON=(44.42, 32.54), SUSA=(48.26, 32.19), SARDIS=(28.04, 38.49), ECBATANA=(48.52, 34.80), PERSEPOLIS=(52.89, 29.93), MEMPHIS=(31.25, 29.85),
         ATHENS=(23.73, 37.98), SPARTA=(22.43, 37.07), MILETUS=(27.28, 37.53), MARATHON=(23.97, 38.15), THERMOPYLAE=(22.54, 38.80), PLATAEA=(23.27, 38.22),
         THEBES=(23.32, 38.32), HALICARNASSUS=(27.42, 37.04), JERUSALEM=(35.22, 31.78), ASHUR=(43.26, 35.46), DER=(46.3, 33.6), OPIS=(44.55, 33.3),
         BACTRA=(66.9, 36.76), CUNAXA=(44.2, 33.3), TRAPEZUS=(39.72, 41.0), EPHESUS=(27.34, 37.94), PELLA=(22.52, 40.76), ISTANBUL=(29.0, 41.02),
         ABYDOS=(26.40, 40.19), ATHOS=(23.92, 40.37))
ROYAL_ROAD = smooth([C["SARDIS"], (30.2, 38.9), (31.99, 39.65), (32.85, 39.93), (34.6, 40.0), (36.4, 39.3), (38.3, 38.35), (40.2, 37.9), (42.2, 37.2),
                     (43.5, 36.4), (44.3, 35.3), (45.6, 34.2), (47.0, 33.1), C["SUSA"]])
TEN_IN = smooth([C["SARDIS"], (30.3, 37.95), (32.5, 37.87), (34.9, 36.92), (36.2, 36.85), (38.3, 35.9), (40.5, 34.8), (42.5, 34.0), C["CUNAXA"]])
TEN_OUT = smooth([C["CUNAXA"], (43.9, 34.5), (43.3, 36.3), (42.3, 37.6), (41.5, 39.0), (40.5, 40.2), C["TRAPEZUS"]])
ALEX = smooth([C["PELLA"], (24.5, 40.9), (26.4, 40.25), (27.3, 40.3), C["SARDIS"], C["MILETUS"], C["HALICARNASSUS"], (30.5, 37.0), (31.99, 39.65), (34.9, 36.92),
               (36.2, 36.85), (35.2, 33.27), (34.45, 31.5), C["MEMPHIS"], (34.45, 31.5), (35.6, 33.4), (38.3, 35.9), (41.0, 37.0), (43.25, 36.56), C["BABYLON"],
               C["SUSA"], C["PERSEPOLIS"]])
BATTLES = [(27.3, 40.3), (36.2, 36.85), (43.25, 36.56)]
DARIUS_FLIGHT = smooth([(43.25, 36.56), C["ECBATANA"], (51.4, 35.6), (54.3, 35.9)])
XERXES = smooth([C["SARDIS"], (27.2, 39.6), (26.42, 40.2), (26.6, 40.75), (25.5, 40.95), (24.3, 40.95), (23.6, 40.7), (22.95, 40.63), (22.5, 40.0), (22.4, 39.4), (22.45, 38.95), C["THERMOPYLAE"]])
SCYTH = smooth([(29.0, 41.3), (28.2, 43.5), (28.6, 45.3), (31.5, 47.2), (35.5, 48.2), (39.5, 48.6)])
CANAL = smooth([(31.52, 30.57), (31.9, 30.56), (32.28, 30.56), (32.36, 30.3), (32.55, 29.95)], 8)
GRID = [[(30.5, 35.5), (30.5, 42.5)], [(34.6, 35.5), (34.6, 43)], [(25.5, 38.8), (34.6, 38.8)], [(34.6, 37.7), (38.9, 37.4)], [(38.9, 43), (38.9, 36.8)],
        [(38.9, 37.4), (44.6, 37.4)], [(45.2, 43), (44.6, 37.4), (46, 34.5), (48.2, 30.3), (48.3, 29)], [(40.6, 37.4), (40.1, 33.5), (39.4, 31.8)],
        [(40.1, 34.6), (45.9, 34.6)], [(34.0, 31.6), (34.95, 29.2)], [(25, 33), (25, 27.5)], [(53, 38.2), (53, 33.3)], [(50.3, 33.3), (50.0, 29.6)],
        [(46.6, 33.3), (60.5, 33.3)], [(55.6, 33.3), (55.6, 25.5)], [(52.5, 40.2), (63, 40.2)], [(60.5, 44), (60.5, 24)], [(55.6, 28.8), (69.5, 28.8)],
        [(60.5, 38), (72.5, 38)], [(60.5, 33), (69.5, 33)], [(69.5, 41.5), (69.5, 23)]]

# ------------------------------------------------------------------ masks
def M(poly): return lambda cam, lm: IC.multiply(poly_mask(cam, poly), lm)
def I(f, poly): return lambda cam, lm: IC.multiply(f(cam, lm), poly_mask(cam, poly))
def U(*fs): return lambda cam, lm: reduce(IC.lighter, [f(cam, lm) for f in fs])
def Dm(a, *bs): return lambda cam, lm: reduce(IC.subtract, [b(cam, lm) for b in bs], a(cam, lm))
CORE = M(EMPIRE_CORE)
EGY = I(CORE, EGSEL); BAB = I(CORE, BABYLON)
STAGE1 = U(I(CORE, MEDIA), I(CORE, ELAM), I(CORE, PARSA))
WEST = Dm(I(CORE, ANATSEL), STAGE1)
CYRUS = Dm(CORE, BAB, EGY)
EAST = Dm(CYRUS, STAGE1, WEST)
NOEGY = Dm(CORE, EGY)
THR = M(THRACE); MAC = M(MACEDON); ION = I(CORE, IONIA)
MAXE = U(CORE, THR)
def GRIDM(cam, lm):
    m = Image.new("L", (W * SS, H * SS), 0); d = ImageDraw.Draw(m)
    for l in GRID: d.line(list(map(tuple, proj(cam, smooth(l, 4) if len(l) > 2 else l))), fill=255, width=s(2.2))
    return IC.multiply(m, CORE(cam, lm))

# ------------------------------------------------------------------ small drawing helpers
def alpha_draw(fr, fn, color, a):
    if a <= 0: return
    if a >= 1: fn(fr.d, color); return
    m = Image.new("L", fr.im.size, 0); fn(ImageDraw.Draw(m), 255)
    fr.im.paste(color, (0, 0), m.point(lambda v: int(v * a))); fr.d = ImageDraw.Draw(fr.im)
def T(fr, x, y, txt, size=20, w="s", color=INK, anchor="l", sp=1.2, a=1.0):
    """text at output-pixel position"""
    f = font(w, s(size))
    alpha_draw(fr, lambda d, c: text_spaced(d, (s(x), s(y)), txt, f, c, sp, anchor), color, a)
def TL(fr, lon, lat, txt, dx=0, dy=0, **kw):
    x, y = P(fr.cam, lon, lat); T(fr, x + dx, y + dy, txt, **kw)
def region(fr, lon, lat, txt, a=1.0, size=23, color=INK, sp=3.5, dx=0, dy=0):
    TL(fr, lon, lat, txt, dx=dx, dy=dy, size=size, w="s", color=color, anchor="m", sp=sp, a=a)
def modern(fr, lon, lat, txt, a=1.0, size=17, dx=0, dy=0, anchor="m", on=0.0):
    """grey modern-name label; on=1 switches it to white for use over the ochre fill"""
    TL(fr, lon, lat, txt, dx=dx, dy=dy, size=size, w="m", color=mix(WHITE, GRAY, on), anchor=anchor, sp=4.5, a=a)
def city(fr, name, a=1.0, side="r", r=5, size=19, label=None, dx=0, dy=0, ll=None):
    if a <= 0: return
    lon, lat = ll or C[name]; x, y = P(fr.cam, lon, lat)
    alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=c), INK, a)
    txt = label if label is not None else name
    if not txt: return
    off = r + 8
    if side == "r": T(fr, x + off + dx, y + dy, txt, size=size, anchor="l", a=a)
    elif side == "l": T(fr, x - off + dx, y + dy, txt, size=size, anchor="r", a=a)
    elif side == "t": T(fr, x + dx, y - off - size * 0.45 + dy, txt, size=size, anchor="m", a=a)
    else: T(fr, x + dx, y + off + size * 0.5 + dy, txt, size=size, anchor="m", a=a)
def cross(fr, lon, lat, a=1.0, r=9, width=4, color=INK):
    if a <= 0: return
    x, y = P(fr.cam, lon, lat); rr = r * min(1.0, a * 1.2)
    def fn(d, c):
        d.line([s(x - rr), s(y - rr), s(x + rr), s(y + rr)], fill=c, width=s(width)); d.line([s(x - rr), s(y + rr), s(x + rr), s(y - rr)], fill=c, width=s(width))
    alpha_draw(fr, fn, color, a)
def bar(fr, lon, lat, ang, length=18, width=5, a=1.0, frac=1.0, color=INK):
    """short thick bar centred on a point (bridge / canal symbol); ang in degrees, screen space"""
    if a <= 0 or frac <= 0: return
    x, y = P(fr.cam, lon, lat); dx = math.cos(math.radians(ang)) * length / 2; dy = -math.sin(math.radians(ang)) * length / 2
    x0, y0 = x - dx, y - dy; x1, y1 = x0 + 2 * dx * frac, y0 + 2 * dy * frac
    alpha_draw(fr, lambda d, c: d.line([s(x0), s(y0), s(x1), s(y1)], fill=c, width=s(width)), color, a)
def dim_line(fr, lon0, lon1, lat, a, txt):
    if a <= 0: return
    x0, y = P(fr.cam, lon0, lat); x1, _ = P(fr.cam, lon1, lat); xm = (x0 + x1) / 2
    xa = xm - (xm - x0) * a; xb = xm + (x1 - xm) * a
    fr.d.line([s(xa), s(y), s(xb), s(y)], fill=INK, width=s(2.5))
    for x in (xa, xb): fr.d.line([s(x), s(y - 11), s(x), s(y + 11)], fill=INK, width=s(2.5))
    fr.plaque(xm, y, txt, size=32, a=min(1, a * 1.3))
def empire_label(fr, a):
    region(fr, 49.5, 36.2, "PERSIAN EMPIRE", a=a, size=30, sp=9)

# ================================================================== SCENES
SC = {}
def scene(name, dur, cam, masks, res=None, active=None, rivers=True):
    def deco(fn):
        SC[name] = Scene(name, dur, cam if callable(cam) else (lambda t, c=cam: c), fn, masks, rivers=rivers, res=res, active=active)
        return fn
    return deco
def mover(keys):
    """keys: [(t, cam)], camera eases between consecutive keys that differ; returns (cam_fn, active intervals)"""
    def fn(t):
        for (t0, c0), (t1, c1) in zip(keys, keys[1:]):
            if t <= t0: return c0
            if t < t1: return c0 if c0 == c1 else lerp_cam(c0, c1, (t - t0) / (t1 - t0))
        return keys[-1][1]
    act = [(t0, t1) for (t0, c0), (t1, c1) in zip(keys, keys[1:]) if c0 != c1]
    return fn, act

# ---------- 0. Cold open: 25 s (VO 0:49-1:14)
_c0, _a0 = mover([(0, cam_at(25.6, 38.6, 135)), (0.4, cam_at(25.6, 38.6, 135)), (4.6, FULL)])
@scene("00_cold_open", 25, _c0, dict(emp=MAXE, mac=MAC), res="50", active=_a0)
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE); fr.fill(fr.masks["mac"], OCHRE_L)
    empire_label(fr, fr.r(4.8, 0.8))
    dim_line(fr, 22.5, 71.5, 46.0, fr.r(8.0, 1.0), "3,000 MILES")

# ---------- 12. What the tablet says: 28 s (VO 1:15-1:43)
@scene("12_what_the_tablet_says", 28, FULL, dict(emp=MAXE, mac=MAC), res="50")
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE); fr.fill(fr.masks["mac"], OCHRE_L)
    empire_label(fr, 1.0)
    for k, (lon, lat, n) in enumerate([(19.5, 44.6, "EUROPE"), (23.5, 26.3, "AFRICA"), (75.2, 37.2, "ASIA")]):
        modern(fr, lon, lat, n, a=fr.r(3.0 + 0.5 * k, 0.6), size=20)
    dim_line(fr, 22.5, 71.5, 46.0, fr.r(11.0, 1.0), "3,000 MILES")

# ---------- 1. Nobody from nowhere: 82 s
@scene("01_nobody_from_nowhere", 82, FULL, dict(bab=BAB, lyd=I(CORE, LYDIA), egy=M(EGYPT), med=I(CORE, MEDIA), parsa=I(CORE, PARSA), st1=STAGE1, west=WEST, east=EAST), res="50",
       active=[(80, 82)])
def _(fr, t):
    k = fr.masks
    fr.fill(k["bab"], OCHRE_L, fr.r(6, 0.8)); fr.fill(k["lyd"], OCHRE_L, fr.r(9, 0.8)); fr.fill(k["egy"], OCHRE_L, fr.r(11, 0.8)); fr.fill(k["med"], OCHRE_L, fr.r(14, 0.8))
    fr.fill(k["parsa"], OCHRE, fr.r(17, 0.8))
    fr.fill(k["st1"], OCHRE, fr.r(40, 1.6)); fr.fill(k["west"], OCHRE, fr.r(47, 2.6)); fr.fill(k["east"], OCHRE, fr.r(57, 2.4))
    region(fr, 41.5, 34.0, "BABYLON", fr.r(6, 0.8)); region(fr, 29.8, 39.3, "LYDIA", fr.r(9, 0.8)); region(fr, 29.5, 27.0, "EGYPT", fr.r(11, 0.8))
    region(fr, 50.5, 36.0, "THE MEDES", fr.r(14, 0.8))
    region(fr, 53.0, 29.2, "PARSA", fr.r(17, 0.8), size=19, sp=2.5)
    modern(fr, 57.5, 31.6, "NOW IRAN", fr.r(18.2, 0.8), on=fr.r(57, 2.4)); modern(fr, 35.2, 39.1, "NOW TURKEY", fr.r(48.5, 0.8), on=1)
    for i, ll in enumerate([(27.28, 37.53), (27.34, 37.94), (27.14, 38.42), (26.75, 38.67)]):
        city(fr, "", a=fr.r(53 + 0.2 * i, 0.4), r=3.2, ll=ll, label="")
    TL(fr, 26.4, 38.1, "GREEK CITIES", dx=-10, dy=0, size=15, anchor="r", sp=1.5, a=fr.r(53.3, 0.6))
    city(fr, "BABYLON", a=fr.r(79.6, 0.5), side="b", label="", r=6)
    if t >= 80: fr.pulse(*C["BABYLON"], t, 80.0)

# ---------- 2a. The Cylinder, first piece: 15 s
_c2a = cam_at(45.2, 33.2, 150)
@scene("02a_the_cylinder", 15, _c2a, dict(per=CYRUS, bab=BAB), res="10")
def _(fr, t):
    fr.fill(fr.masks["per"], OCHRE); fr.fill(fr.masks["bab"], OCHRE_L); fr.fill(fr.masks["bab"], OCHRE, fr.r(13.0, 1.8))
    region(fr, 42.2, 34.6, "BABYLONIA", size=22)
    x, y = P(fr.cam, *C["BABYLON"]); wa = fr.r(0.3, 1.2); g = fr.r(13.0, 1.2); R = 30
    if wa > 0:
        col = mix(INK, OCHRE_L, wa)
        for (x0, y0, x1, y1) in [(x - R, y + R, x + R, y + R), (x - R, y - R, x - R, y + R), (x + R, y - R, x + R, y + R)]:
            fr.d.line([s(x0), s(y0), s(x1), s(y1)], fill=col, width=s(5))
        gap = R * 0.75 * g       # the north wall opens
        fr.d.line([s(x - R), s(y - R), s(x - gap), s(y - R)], fill=col, width=s(5)); fr.d.line([s(x + gap), s(y - R), s(x + R), s(y - R)], fill=col, width=s(5))
    city(fr, "BABYLON", a=fr.r(0.2, 0.6), side="b", r=7, size=22, dy=30)
    fr.plaque(960, 110, "539 BC", size=34, a=fr.r(8.0, 0.6))
    fr.line(smooth([(48.6, 35.6), (47.2, 34.9), (45.8, 34.1), C["OPIS"]]), width=4.5, frac=fr.r(9.4, 1.6), arrow=True, bgc=OCHRE)
    cross(fr, *C["OPIS"], a=fr.r(11.0, 0.4), r=11, width=5); TL(fr, *C["OPIS"], "OPIS", dx=-18, dy=-4, size=18, anchor="r", a=fr.r(11.0, 0.5))
    fr.line([(44.5, 33.15), (44.43, 32.86)], width=4.5, frac=fr.r(13.2, 1.2), arrow=True, bgc=OCHRE)

# ---------- 2b. The Cylinder, second piece: 11 s (VO 0:41-0:52)
@scene("02b_the_cylinder", 11, cam_at(42.5, 33.6, 95), dict(per=NOEGY), res="10")
def _(fr, t):
    fr.fill(fr.masks["per"], OCHRE)
    city(fr, "BABYLON", side="b", r=7, size=22)
    for i, (n, side) in enumerate([("ASHUR", "t"), ("SUSA", "r"), ("DER", "t")]):
        fr.line(arc(C["BABYLON"], C[n], 0.12 if n != "SUSA" else -0.12), color=(70, 70, 70), width=2.6, frac=fr.r(1.0 + 0.9 * i, 1.4), arrow=True, bgc=OCHRE)
        city(fr, n, a=fr.r(1.6 + 0.9 * i, 0.6), side=side, r=4, size=17)
    fr.line(arc(C["BABYLON"], (35.55, 31.85), 0.10), width=5.5, frac=fr.r(7.0, 2.0), arrow=True, bgc=OCHRE)
    city(fr, "JERUSALEM", a=fr.r(7.6, 0.7), side="l", r=6, size=21, dx=-2)
    region(fr, 35.3, 30.9, "JUDEA", fr.r(8.2, 0.7), size=17, sp=3, dx=-52)

# ---------- 3a. Control the story, first piece: 6 s
@scene("03a_control_the_story", 6, FULL, dict(per=NOEGY, egy=EGY), res="50")
def _(fr, t):
    fr.fill(fr.masks["per"], OCHRE); fr.fill(fr.masks["egy"], OCHRE_L); fr.fill(fr.masks["egy"], OCHRE, fr.r(0.4, 1.8))
    region(fr, 29.5, 27.0, "EGYPT"); empire_label(fr, 1.0)

# ---------- 3b. Control the story, second piece: 12 s (VO 1:07-1:19)
_REB = [("BABYLON", C["BABYLON"], 2.0, 44.42, 32.54), ("MEDIA", C["ECBATANA"], 3.0, 0, 0), ("ELAM", C["SUSA"], 4.0, 0, 0), ("EGYPT", C["MEMPHIS"], 5.0, 0, 0)]
_REB2 = [((52.9, 29.9), 5.8), ((43.5, 36.3), 6.1), ((56.0, 36.6), 6.4), ((61.8, 37.6), 6.7), ((41.5, 39.6), 7.0), ((65.7, 31.6), 7.3)]
@scene("03b_control_the_story", 12, FULL, dict(emp=CORE), res="50", active=[(0, 12)])
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE)
    for ll, t0 in _REB2:
        if t >= t0: fr.pulse(*ll, t, t0, n=1, rmax=22, width=2.5); fr.dot(*ll, r=3.5)
    for n, ll, t0, _, _ in _REB:
        if t >= t0: fr.pulse(*ll, t, t0, n=2, rmax=40, width=3.5); fr.dot(*ll, r=6)
    off = {"BABYLON": (-64, 34), "MEDIA": (0, -36), "ELAM": (70, 20), "EGYPT": (0, -36)}
    for n, ll, t0, _, _ in _REB:
        fr.plaque_at(*ll, n, dx=off[n][0], dy=off[n][1], size=19, a=ramp(t, t0, 0.4), pad=(10, 7))
    fr.plaque(960, 108, "19 BATTLES  ·  9 KINGS", size=32, a=ramp(t, 8.0, 0.6))

# ---------- 4. The operating system: 38 s (VO 0:05-0:43)
@scene("04_the_operating_system", 38, FULL, dict(emp=CORE, grid=GRIDM), res="50")
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE); fr.fill(fr.masks["grid"], WHITE, fr.r(0.2, 2.6))
    fr.plaque(960, 108, "20 SATRAPIES", size=32, a=fr.r(8.0, 0.6))
    fr.dot(*C["BABYLON"], r=6, a=fr.r(24.0, 0.5)); fr.plaque_at(*C["BABYLON"], "BABYLON  ·  1,000 TALENTS", dx=-150, dy=54, size=22, a=fr.r(24.3, 0.6))
    fr.dot(70.6, 30.2, r=6, a=fr.r(30.0, 0.5)); fr.plaque_at(70.6, 30.2, "INDIA  ·  360 TALENTS", dx=-90, dy=-48, size=22, a=fr.r(30.3, 0.6))
    fr.dot(*C["PERSEPOLIS"], r=6, a=fr.r(34.0, 0.5)); fr.plaque_at(*C["PERSEPOLIS"], "PERSIA  ·  NOTHING", dx=40, dy=52, size=22, a=fr.r(34.3, 0.6))

# ---------- 5. Beating distance: 86 s (freeze 43-51)
_VA = cam_at(38.5, 36.4, 70); _VE = cam_at(32.25, 30.1, 235); _VC = cam_at(47.2, 33.4, 120)
def _c5(t):
    if t < 51: return _VA
    if t < 66: return _VE
    if t < 69: return lerp_cam(_VE, _VC, (t - 66) / 3.0)
    return _VC
_STN = np.linspace(0, 1, 111)
_COURT = [(69.5, "BABYLON"), (73.4, "SUSA"), (75.6, "ECBATANA"), (79.0, "BABYLON"), (81.8, "SUSA"), (84.2, "ECBATANA")]
@scene("05_beating_distance", 86, _c5, dict(emp=CORE), active=[(66, 69), (27.5, 34.2), (73.4, 86)])
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE)
    if t < 51:
        road = ROYAL_ROAD[::-1]                      # drawn from Susa towards Sardis
        fr.line(road, width=4, frac=fr.r(7.0, 3.6), bgc=OCHRE)
        sa = fr.r(25.0, 2.6)
        if sa > 0:
            pr = proj(fr.cam, road); L = path_len(pr)
            for q in _STN[:int(round(111 * sa))]:
                p = partial(pr, q)[-1]; fr.d.ellipse([p[0] - s(3.4), p[1] - s(3.4), p[0] + s(3.4), p[1] + s(3.4)], fill=WHITE, outline=INK, width=s(1.3))
        city(fr, "SUSA", a=fr.r(6.8, 0.5), side="r", r=7, size=23); city(fr, "SARDIS", a=fr.r(10.0, 0.5), side="l", r=7, size=23)
        if 27.5 <= t <= 34.2:                        # the relay: a message running Sardis -> Susa
            q = ease((t - 27.5) / 6.5); p = partial(proj(fr.cam, ROYAL_ROAD), q)[-1]
            fr.d.ellipse([p[0] - s(10), p[1] - s(10), p[0] + s(10), p[1] + s(10)], fill=INK, outline=WHITE, width=s(3))
        fr.plaque(960, 96, "2,500 KM", size=32, a=fr.r(10.4, 0.6))
        fr.plaque(960, 164, "90 DAYS ON FOOT", size=26, a=fr.r(13.0, 0.6))
        fr.plaque(960, 226, "7 DAYS BY RELAY", size=26, a=fr.r(34.0, 0.6))
        fr.plaque(960, 288, "111 STATIONS", size=22, a=fr.r(26.0, 0.6))
    else:
        ea = 1 - ramp(t, 66.0, 0.8)                  # Egypt elements fade as the camera leaves
        ca = ramp(t, 68.6, 0.8)
        if ea > 0:
            fr.line(CANAL, width=5, frac=fr.r(51.2, 3.6), bgc=OCHRE, a=ea)
            city(fr, "MEMPHIS", a=ea, side="l", r=6, size=21)
            TL(fr, 31.05, 29.2, "NILE", size=17, w="m", color=(120, 160, 175), sp=4, anchor="r", a=ea)
            modern(fr, 30.2, 31.95, "MEDITERRANEAN", a=ea, size=17); modern(fr, 33.2, 28.75, "RED SEA", a=ea, size=17, dx=6)
            fr.plaque_at(31.95, 30.56, "DARIUS' CANAL", dx=0, dy=-46, size=24, a=fr.r(54.6, 0.6) * ea)
            modern(fr, 32.62, 30.75, "NOW SUEZ CANAL", a=fr.r(63.0, 0.8) * ea, size=16, anchor="l", dx=14)
            if ea >= 1 and t >= 63: fr.line([(32.33, 31.25), (32.36, 30.6), (32.55, 29.95)], color=GRAY, width=2.2, dash=(7, 6), a=ramp(t, 63.0, 0.8), bgc=OCHRE)
        if ca > 0:
            for n, side in (("BABYLON", "l"), ("SUSA", "r"), ("ECBATANA", "r")): city(fr, n, a=ca, side=side, r=6, size=22)
            lab = {"BABYLON": ("WINTER", -70, 46, 72.0), "SUSA": ("SPRING", 66, 46, 74.3), "ECBATANA": ("SUMMER", 0, -46, 76.5)}
            for n, (txt, dx, dy, t0) in lab.items(): fr.plaque_at(*C[n], txt, dx=dx, dy=dy, size=20, a=ramp(t, t0, 0.5), pad=(10, 7))
            # the court: a ringed dot moving between the three capitals
            pos = np.array(C[_COURT[0][1]], float)
            for (ta, na), (tb, nb) in zip(_COURT, _COURT[1:]):
                if t >= tb: pos = np.array(C[nb], float)
                elif t >= tb - 1.2 and t < tb:
                    q = ease((t - (tb - 1.2)) / 1.2); pos = np.array(C[na], float) + (np.array(C[nb], float) - np.array(C[na], float)) * q
            x, y = P(fr.cam, *pos); rr = 15
            alpha_draw(fr, lambda d, c: d.ellipse([s(x - rr), s(y - rr), s(x + rr), s(y + rr)], outline=c, width=s(4.5)), INK, ca)

# ---------- 6. The receipts: 16 s (VO 0:41-0:57)
_MAT = [("CEDAR", "LEBANON", (35.9, 34.0), 4.0, 0.16, (-6, -34)), ("GOLD", "SARDIS", C["SARDIS"], 5.0, 0.14, (0, -34)), ("GOLD", "BACTRIA", C["BACTRA"], 6.2, -0.16, (0, -34)),
        ("IVORY", "AFRICA", (32.6, 23.9), 7.2, 0.14, (-78, 0)), ("IVORY", "INDIA", (70.4, 28.6), 8.2, -0.14, (-10, 38))]
_CRAFT = [("STONECUTTERS", (27.3, 37.3), 10.0, "r", (-12, 22)), ("GOLDSMITHS", (31.2, 30.0), 10.7, "r", (-12, 0)), ("BRICKMAKERS", C["BABYLON"], 11.4, "b", (-30, 26))]
@scene("06_the_receipts", 16, FULL, dict(emp=CORE), res="50")
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE)
    for word, place, ll, t0, bend, off in _MAT:
        fr.line(arc(ll, C["SUSA"], bend), width=3.2, frac=fr.r(t0, 1.3), arrow=True, bgc=OCHRE)
        fr.dot(*ll, r=5, a=fr.r(t0, 0.4))
        fr.plaque_at(*ll, f"{word}  ·  {place}", dx=off[0], dy=off[1], size=18, a=fr.r(t0 + 0.2, 0.5), pad=(9, 6))
    for word, ll, t0, side, off in _CRAFT:
        fr.line(arc(ll, C["SUSA"], 0.06), color=(60, 60, 60), width=1.8, frac=fr.r(t0, 1.0), dash=(6, 5), bgc=OCHRE)
        fr.dot(*ll, r=3.5, a=fr.r(t0, 0.4))
        TL(fr, *ll, word, dx=off[0], dy=off[1], size=16, w="s", sp=1.5, anchor={"r": "r", "b": "m"}[side], a=fr.r(t0 + 0.1, 0.5))
    city(fr, "SUSA", side="b", r=8, size=24, dy=4)

# ---------- 7. The price: 50 s (VO 0:26-1:16)
_V7a = cam_at(29.0, 41.15, 250); _V7b = cam_at(31.5, 44.3, 60); _V7c = cam_at(24.8, 40.9, 170); _V7d = cam_at(26.2, 38.75, 170)
_c7, _a7 = mover([(0, _V7a), (11.3, _V7a), (13.2, _V7b), (20.8, _V7b), (23.0, _V7c), (32.0, _V7c), (34.0, _V7d)])
@scene("07_the_price", 50, _c7, dict(emp=CORE, thr=THR, mac=MAC), res="10", active=_a7 + [(30, 33), (34, 50)])
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE); fr.fill(fr.masks["thr"], OCHRE, fr.r(23.0, 1.6)); fr.fill(fr.masks["mac"], OCHRE_L, fr.r(26.0, 1.6))
    S = fr.cam[2]
    if t < 13.2:
        a = 1 - ramp(t, 11.6, 0.8)
        bar(fr, 29.03, 41.07, 12, length=30, width=6, frac=fr.r(6.0, 1.4), a=a)
        fr.plaque_at(29.03, 41.07, "BRIDGE OF BOATS", dx=190, dy=-78, size=24, a=fr.r(7.0, 0.6) * a)
        modern(fr, 28.75, 41.02, "NOW ISTANBUL", a=fr.r(9.0, 0.8) * a, anchor="r", dx=-14, size=18)
        modern(fr, 30.6, 42.1, "BLACK SEA", a=a, size=18); region(fr, 27.6, 41.7, "EUROPE", a=a * 0.9, size=22, color=GRAY); region(fr, 31.2, 40.45, "ASIA", a=a, size=22)
        TL(fr, 29.1, 41.14, "BOSPORUS", dx=22, dy=2, size=15, w="m", color=(110, 150, 165), sp=3, a=a)
    if 11.5 <= t < 23.2:
        a = ramp(t, 12.6, 0.8) * (1 - ramp(t, 21.0, 0.8))
        col = mix(GRAY, INK, ramp(t, 19.0, 1.2))
        fr.line(SCYTH, color=col, width=5, frac=fr.r(12.8, 3.6), dash=(16, 9), arrow=True, a=a)
        region(fr, 34.5, 49.4, "SCYTHIANS", a=a * ramp(t, 13.4, 0.8), size=24, color=GRAY, sp=6)
        modern(fr, 34.5, 43.4, "BLACK SEA", a=a, size=18)
        fr.plaque_at(39.5, 48.6, "HIS ONE FAILURE", dx=-60, dy=44, size=22, a=ramp(t, 19.0, 0.6) * a)
    if t >= 21.5:
        a = ramp(t, 22.6, 0.8)
        region(fr, 26.3, 41.75, "THRACE", a=fr.r(23.4, 0.8), size=22)
        ma = fr.r(26.4, 0.8); pa = fr.r(30.0, 0.6)
        if pa > 0: fr.plaque_at(22.25, 40.95, "MACEDON", dx=0, dy=0, size=24, a=pa)
        elif ma > 0: region(fr, 22.25, 40.95, "MACEDON", a=ma, size=20)
        if 30 <= t <= 33: fr.pulse(22.25, 40.95, t, 30.0, n=2, rmax=70, width=3.5)
    if t >= 33.0:
        a = ramp(t, 34.0, 0.6)
        modern(fr, 29.6, 39.35, "NOW TURKEY", a=fr.r(35.0, 0.8), size=18, on=1)
        fr.plaque(960, 104, "IONIAN REVOLT  ·  499 BC", size=28, a=fr.r(34.0, 0.6))
        for n in ("MILETUS", "EPHESUS"):
            if t >= 34.4: fr.pulse(*C[n], t, 34.4, n=1, rmax=26, width=2.5)
        city(fr, "ATHENS", a=a, side="l", r=5, size=19)
        fr.line(arc(C["ATHENS"], (26.9, 37.7), -0.16), color=(60, 60, 60), width=2.4, frac=fr.r(37.0, 1.6), dash=(8, 6), arrow=True, bgc=SEA)
        city(fr, "SARDIS", a=a, side="r", r=6, size=21); city(fr, "MILETUS", a=a, side="l", r=6, size=21, dy=14)
        if t >= 40.0: fr.pulse(*C["SARDIS"], t, 40.0, n=2, rmax=44, width=3.5)
        fr.plaque_at(*C["SARDIS"], "BURNED", dx=0, dy=-44, size=20, a=fr.r(40.2, 0.5), pad=(10, 7))
        fr.plaque_at(*C["MILETUS"], "SACKED", dx=78, dy=10, size=20, a=fr.r(46.0, 0.5), pad=(10, 7))

# ---------- 8a. Xerxes goes west, first piece: 47 s
_V8a = cam_at(23.95, 38.02, 700); _V8b = cam_at(29.5, 34.6, 62); _V8c = cam_at(25.15, 40.3, 330)
_c8a, _a8a = mover([(0, _V8a), (7.5, _V8a), (10.8, _V8b), (21.5, _V8b), (25.2, _V8c)])
@scene("08a_xerxes_goes_west", 47, _c8a, dict(emp=CORE, thr=THR, mac=MAC), res="10", active=_a8a + [(16, 21.5), (45, 47)])
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE); fr.fill(fr.masks["thr"], OCHRE); fr.fill(fr.masks["mac"], OCHRE_L)
    if t < 10.8:
        a = 1 - ramp(t, 7.7, 0.8)
        fr.plaque(960, 104, "490 BC", size=32, a=a)
        fr.line(smooth([(23.82, 38.37), (23.97, 38.28), (24.01, 38.175)]), width=5, frac=fr.r(0.4, 1.8), arrow=True, bgc=SEA, a=a)
        city(fr, "MARATHON", a=fr.r(0.2, 0.5) * a, side="r", r=8, size=26, dy=8); city(fr, "ATHENS", a=a, side="l", r=8, size=26)
        fr.line([C["MARATHON"], (23.85, 38.06), C["ATHENS"]], color=(60, 60, 60), width=3, frac=fr.r(2.2, 1.4), dash=(10, 8), a=a)
        TL(fr, 23.9, 38.05, "A DAY'S MARCH", dx=24, dy=10, size=19, w="m", color=(60, 60, 60), sp=2.5, a=fr.r(2.8, 0.7) * a)
    if 9.5 <= t < 25.2:
        a = ramp(t, 10.4, 0.8) * (1 - ramp(t, 21.6, 0.8))
        empire_a = a
        region(fr, 29.5, 26.6, "EGYPT", a=a, size=22); city(fr, "ATHENS", a=a, side="l", r=5, size=19)
        region(fr, 41.0, 36.2, "PERSIAN EMPIRE", a=a, size=26, sp=7)
        if 16 <= t < 21.5: fr.pulse(*C["MEMPHIS"], t, 16.0, n=2, rmax=52, width=3.5)
        fr.plaque_at(*C["MEMPHIS"], "EGYPT REVOLTS", dx=0, dy=-52, size=22, a=ramp(t, 16.0, 0.5) * a)
    if t >= 23.5:
        a = ramp(t, 24.6, 0.8)
        modern(fr, 26.05, 40.07, "HELLESPONT", a=a, size=16, anchor="r", dx=-22, dy=22)
        bar(fr, 26.385, 40.185, 150, length=30, width=5, frac=fr.r(28.0, 1.6)); bar(fr, 26.43, 40.225, 150, length=30, width=5, frac=fr.r(30.6, 1.6))
        fr.plaque_at(26.41, 40.2, "TWO BRIDGES OF BOATS", dx=40, dy=-62, size=22, a=fr.r(29.0, 0.6))
        region(fr, 25.6, 41.25, "THRACE", a=a, size=22); region(fr, 22.45, 41.0, "MACEDON", a=a, size=20)
        bar(fr, 23.93, 40.375, 62, length=24, width=5, frac=fr.r(34.0, 1.8))
        TL(fr, 24.25, 40.2, "ATHOS", dx=14, dy=20, size=18, a=a)
        fr.plaque_at(23.93, 40.375, "CANAL  ·  2 KM", dx=-20, dy=-52, size=22, a=fr.r(35.2, 0.6))
        if t >= 45.0: fr.pulse(23.93, 40.375, t, 45.0, n=2, rmax=46, width=3.5)

# ---------- 8b. Xerxes goes west, second piece: 11 s (VO 1:04-1:15)
@scene("08b_xerxes_goes_west", 11, cam_at(25.2, 39.35, 150), dict(emp=CORE, thr=THR, mac=MAC), res="10")
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE); fr.fill(fr.masks["thr"], OCHRE); fr.fill(fr.masks["mac"], OCHRE_L)
    fr.line(XERXES, width=4.5, frac=fr.r(0.2, 2.6), arrow=True, bgc=OCHRE)
    city(fr, "SARDIS", side="r", r=6, size=20); city(fr, "ATHENS", side="b", r=5, size=19)
    fr.plaque(960, 110, "1,700,000", size=44, a=fr.r(3.0, 0.5), strike=fr.r(5.0, 0.7))
    fr.plaque(960, 196, "120,000–300,000", size=34, a=fr.r(8.0, 0.6))

# ---------- 8c. Xerxes goes west, third piece: 29 s (VO 1:40-2:09)
_V8d = cam_at(22.62, 38.84, 1050); _V8e = cam_at(24.6, 38.95, 190)
_c8c, _a8c = mover([(0, _V8d), (14.0, _V8d), (17.2, _V8e)])
@scene("08c_xerxes_goes_west", 29, _c8c, dict(emp=CORE, thr=THR, mac=MAC, the=M(THESSALY), boe=M(BOEOTIA)), res="10", active=_a8c)
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE); fr.fill(fr.masks["thr"], OCHRE)
    fr.fill(fr.masks["the"], OCHRE_L, fr.r(18.0, 0.8)); fr.fill(fr.masks["mac"], OCHRE_L, fr.r(18.8, 0.8)); fr.fill(fr.masks["boe"], OCHRE_L, fr.r(19.6, 0.8))
    if t < 17.2:
        a = 1 - ramp(t, 14.2, 0.8)
        fr.line(smooth([(22.2, 39.12), (22.36, 38.98), (22.47, 38.89), (22.515, 38.815)]), width=6, frac=fr.r(0.3, 2.0), arrow=True, a=a)
        bar(fr, 22.56, 38.795, 80, length=34, width=8, a=fr.r(0.2, 0.5) * a)
        TL(fr, 22.56, 38.795, "THERMOPYLAE", dx=30, dy=4, size=26, a=fr.r(0.4, 0.6) * a)
        fr.line(smooth([(22.45, 38.84), (22.47, 38.775), (22.55, 38.745), (22.63, 38.76), (22.635, 38.79)], 10), color=(60, 60, 60), width=3.2, frac=fr.r(10.5, 2.4),
                dash=(10, 7), arrow=True, a=a)
        TL(fr, 22.55, 38.745, "MOUNTAIN PATH", dx=0, dy=30, size=18, w="m", color=(60, 60, 60), sp=2.5, anchor="m", a=fr.r(11.4, 0.7) * a)
        modern(fr, 22.78, 38.9, "MALIAN GULF", a=a, size=16)
    if t >= 15.5:
        a = ramp(t, 16.6, 0.8)
        region(fr, 22.2, 39.5, "THESSALY", a=fr.r(18.2, 0.7), size=19); region(fr, 22.3, 40.98, "MACEDON", a=fr.r(19.0, 0.7), size=19)
        city(fr, "THEBES", a=fr.r(19.8, 0.7), side="l", r=5, size=19); city(fr, "ATHENS", a=a, side="r", r=5, size=19); city(fr, "SPARTA", a=a, side="b", r=5, size=19)
        city(fr, "THERMOPYLAE", a=a, side="l", r=4, size=15)
        city(fr, "HALICARNASSUS", a=fr.r(22.0, 0.6), side="b", r=6, size=17, label="HALICARNASSUS")
        fr.plaque_at(*C["HALICARNASSUS"], "QUEEN ARTEMISIA", dx=40, dy=-42, size=20, a=fr.r(22.6, 0.6), pad=(10, 7))
        la = fr.r(18.0, 0.8)
        if la > 0:
            x0, y0 = 150, 130
            alpha_draw(fr, lambda d, c: d.rectangle([s(x0), s(y0 - 14), s(x0 + 44), s(y0 + 14)], fill=c), OCHRE_L, la)
            alpha_draw(fr, lambda d, c: d.rectangle([s(x0), s(y0 - 14), s(x0 + 44), s(y0 + 14)], outline=c, width=s(2)), INK, la)
            T(fr, x0 + 60, y0, "GREEKS ON THE PERSIAN SIDE", size=22, sp=2.2, a=la)
            alpha_draw(fr, lambda d, c: d.rectangle([s(x0), s(y0 + 30), s(x0 + 44), s(y0 + 58)], fill=c), OCHRE, la)
            T(fr, x0 + 60, y0 + 44, "PERSIAN EMPIRE", size=22, sp=2.2, a=la)

# ---------- 9a. Seen from Susa, first piece: 13 s (VO 0:07-0:20)
_SHIPS = [((23.60 + 0.012 * (i % 4), 37.875 - 0.013 * (i // 4)), (23.555 + 0.006 * (i % 4), 37.953 + 0.004 * (i // 4) - 0.003 * (i % 4))) for i in range(12)]
@scene("09a_seen_from_susa", 13, cam_at(23.52, 37.95, 1500), dict(), res="10", active=[(2.8, 8.2)])
def _(fr, t):
    region(fr, 23.46, 37.93, "SALAMIS", size=24); city(fr, "ATHENS", side="r", r=8, size=26)
    fr.plaque(960, 104, "480 BC", size=32)
    TL(fr, 23.6, 37.975, "THE STRAIT", dx=0, dy=-58, size=17, w="m", color=(110, 150, 165), sp=4, anchor="m", a=fr.r(2.6, 0.7))
    for i in range(6):                                  # the Greek line, waiting inside
        x, y = P(fr.cam, 23.525 + 0.004 * (i % 2), 37.966 - 0.0085 * i + 0.02)
        fr.d.ellipse([s(x - 7), s(y - 7), s(x + 7), s(y + 7)], fill=WHITE, outline=INK, width=s(2.5))
    q = ease((t - 3.0) / 3.4); dead = ramp(t, 6.4, 1.6)
    for a0, a1 in _SHIPS:
        lon = a0[0] + (a1[0] - a0[0]) * q; lat = a0[1] + (a1[1] - a0[1]) * q; x, y = P(fr.cam, lon, lat)
        fr.d.ellipse([s(x - 7), s(y - 7), s(x + 7), s(y + 7)], fill=mix((165, 188, 197), INK, dead))
    TL(fr, 23.59, 37.86, "PERSIAN FLEET", dx=-14, dy=0, size=17, w="s", sp=2, anchor="r", a=1 - ramp(t, 6.4, 1.0))
    fr.line(smooth([(23.78, 37.99), (23.95, 38.02), (24.22, 38.03)]), width=4.5, frac=fr.r(8.0, 1.8), arrow=True)
    TL(fr, 24.0, 38.03, "XERXES GOES HOME", dx=0, dy=-26, size=18, sp=2, anchor="m", a=fr.r(8.6, 0.7))
    city(fr, "PLATAEA", a=fr.r(12.0, 0.4), side="l", r=7, size=22); fr.plaque_at(*C["PLATAEA"], "479 BC", dx=74, dy=-4, size=20, a=fr.r(12.2, 0.4), pad=(10, 7))

# ---------- 9b. Seen from Susa, second piece: 18 s (VO 0:43-1:01)
_c9b, _a9b = mover([(0, cam_at(24.3, 38.3, 170)), (0.5, cam_at(24.3, 38.3, 170)), (2.3, FULL)])
@scene("09b_seen_from_susa", 18, _c9b, dict(emp=CORE, thr=THR, ion=ION), res="50", active=_a9b)
def _(fr, t):
    lost = fr.r(7.0, 1.4)
    fr.fill(fr.masks["emp"], OCHRE); fr.fill(fr.masks["thr"], OCHRE, 1 - lost); fr.fill(fr.masks["ion"], LAND, lost)
    a = fr.r(2.2, 0.6)
    city(fr, "SUSA", a=a, side="r", r=9, size=30)
    city(fr, "ATHENS", a=a, side="b", r=4, size=15, label="GREECE", dx=-6)
    modern(fr, 21.0, 43.6, "THE FAR WESTERN EDGE", a=fr.r(4.0, 0.8), size=16, anchor="l", dx=-100)
    fr.plaque(960, 108, "150 MORE YEARS", size=34, a=fr.r(13.0, 0.6))

# ---------- 10. Rent them: 71 s (VO 0:19-1:30)
@scene("10_rent_them", 71, cam_at(35.6, 36.2, 64), dict(emp=CORE, ion=ION), res="50")
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE); fr.fill(fr.masks["ion"], LAND, 1 - fr.r(62.0, 2.0))
    gold = arc(C["SUSA"], C["SPARTA"], -0.13)
    gcol = mix(INK, mix((120, 120, 120), INK, ramp(t, 8.0, 1.2)), ramp(t, 55.0, 0.8))
    fr.line(gold, color=gcol, width=4, frac=fr.r(2.0, 2.2), arrow=True, bgc=OCHRE)
    city(fr, "SUSA", side="r", r=7, size=23); city(fr, "SPARTA", a=fr.r(3.6, 0.5), side="b", r=6, size=21); city(fr, "ATHENS", side="t", r=4, size=16)
    fr.plaque_at(35.8, 39.7, "PERSIAN GOLD", dx=0, dy=-112, size=22, a=fr.r(3.0, 0.6) * (1 - fr.r(8.0, 0.8)))
    fr.plaque(250, 110, "401 BC", size=30, a=fr.r(10.0, 0.6) * (1 - fr.r(45.0, 0.8)))
    fr.line(TEN_IN, width=3, frac=fr.r(10.4, 13.0), bgc=OCHRE)
    city(fr, "SARDIS", a=fr.r(10.0, 0.5), side="t", r=5, size=18); city(fr, "BABYLON", a=fr.r(23.0, 0.5), side="b", r=5, size=18)
    cross(fr, *C["CUNAXA"], a=fr.r(24.0, 0.4), r=10, width=4.5)
    fr.plaque_at(*C["CUNAXA"], "1,000 MILES FROM HOME", dx=-150, dy=-58, size=20, a=fr.r(27.0, 0.6) * (1 - fr.r(44.0, 0.8)), pad=(10, 7))
    fr.line(TEN_OUT, width=3, frac=fr.r(30.0, 4.6), arrow=True, bgc=OCHRE)
    modern(fr, 35.0, 43.0, "BLACK SEA", a=fr.r(33.0, 0.8), size=17)
    TL(fr, 38.6, 36.7, "THE TEN THOUSAND", dx=0, dy=0, size=16, w="s", sp=2.5, anchor="m", a=fr.r(14.0, 0.8))
    fr.plaque(960, 108, "THE KING'S PEACE  ·  387 BC", size=30, a=fr.r(55.0, 0.6))

# ---------- 11. The last Achaemenid: 15 s (VO 0:32-0:47)
@scene("11_the_last_achaemenid", 15, FULL, dict(emp=CORE, mac=MAC), res="50", active=[(13, 15)])
def _(fr, t):
    fr.fill(fr.masks["emp"], OCHRE); fr.fill(fr.masks["mac"], OCHRE_L)
    fr.plaque(250, 110, "334 BC", size=30, a=fr.r(0.2, 0.5))
    TL(fr, 22.3, 41.0, "MACEDON", dx=-14, dy=-30, size=17, anchor="m", sp=2.5)
    fr.line(ALEX, width=4, frac=fr.r(0.3, 12.4) if t < 0.3 else min(1.0, (t - 0.3) / 12.4), arrow=True, bgc=OCHRE)
    fr.scene.auto.add((0.3, 12.8))
    for i, ll in enumerate(BATTLES): cross(fr, *ll, a=fr.r(4.0 + 0.5 * i, 0.35), r=10, width=4.5)
    fr.line(DARIUS_FLIGHT, color=(70, 70, 70), width=2.8, frac=fr.r(8.0, 3.0), dash=(8, 6), arrow=True, bgc=OCHRE)
    fr.plaque_at(54.3, 35.9, "DARIUS III KILLED", dx=120, dy=-36, size=18, a=fr.r(11.0, 0.5), pad=(9, 6))
    city(fr, "PERSEPOLIS", a=fr.r(12.6, 0.5), side="r", r=7, size=22, dx=6)
    if t >= 13: fr.pulse(*C["PERSEPOLIS"], t, 13.0, n=2, rmax=44, width=3.5)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "still":
        for spec in sys.argv[2:]:
            n, ts = spec.split("@"); sc = SC[n]
            for tt in ts.split(","): sc.still(float(tt), f"test/{n}_{float(tt):05.1f}.png", 0.5)
    elif mode == "render":
        import time
        for n in sys.argv[2:]:
            t0 = time.time(); SC[n].render("out"); print(n, round(time.time() - t0, 1), flush=True)
    elif mode == "list":
        for n, sc in SC.items(): print(n, sc.dur)
