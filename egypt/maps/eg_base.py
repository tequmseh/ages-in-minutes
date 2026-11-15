# География, маски и общие помощники для карт «Ancient Egypt in 20 Minutes»
import sys, os, json
from functools import reduce
import engine
from engine import *
from PIL import ImageChops as IC

WHITE = (255, 255, 255)
GREEN_D = (28, 92, 79)            # тёмный зелёный для подписей по песку
SAND_D = (170, 142, 92)           # подписи пустыни
NILE = engine.NILE

def cam_at(lon, lat, S): return (lon, lat - 55.0 / S, S)
def cam_box(lon0, lon1, lat0, lat1, mx=40, my=45):
    S = min((H - SAFE - 2 * my) / (lat1 - lat0), (W - 2 * mx) / ((lon1 - lon0) * engine.K))
    return cam_at((lon0 + lon1) / 2, (lat0 + lat1) / 2, S)
COUNTRY = cam_full()

# ---------------------------------------------------------------- places (lon, lat)
C = dict(MEMPHIS=(31.255, 29.849), THEBES=(32.645, 25.705), GIZA=(31.134, 29.979), SAQQARA=(31.216, 29.871), MEIDUM=(31.157, 29.388),
         BENT=(31.209, 29.790), REDP=(31.206, 29.812), AVARIS=(31.82, 30.79), ASWAN=(32.875, 24.09), PHILAE=(32.880, 24.025), APEX=(31.233, 30.10),
         ASYUT=(31.18, 27.18), CUSAE=(30.82, 27.44), AMARNA=(30.90, 27.65), HIBA=(30.93, 28.78), ABYDOS=(31.92, 26.18), SEMNA=(30.97, 21.50),
         BUHEN=(31.28, 21.91), ABU_SIMBEL=(31.625, 22.337), KERMA=(30.41, 19.60), NAPATA=(31.83, 18.53), KURGUS=(33.35, 19.50), MEROE=(33.75, 16.94),
         KHARTOUM=(32.49, 15.63), MEGIDDO=(35.18, 32.58), KADESH=(36.52, 34.56), ALEXANDRIA=(29.92, 31.20), KARNAK=(32.657, 25.719),
         KINGS=(32.601, 25.740), DEIR=(32.601, 25.727), JARF=(32.66, 28.89), GAZA=(34.45, 31.5), PELUSIUM=(32.55, 31.04), HATTUSA=(34.62, 40.02),
         DENDERA=(32.67, 26.14), ESNA=(32.55, 25.29), EDFU=(32.87, 24.98), KOMOMBO=(32.93, 24.45), TANA=(37.3, 11.9))
def on_river(lat):
    """lon of the Nile at a latitude (first crossing from the north)"""
    for (x0, y0), (x1, y1) in zip(NILE[::-1][:-1], NILE[::-1][1:]):
        if (y0 - lat) * (y1 - lat) <= 0 and y0 != y1: return float(x0 + (x1 - x0) * (lat - y0) / (y1 - y0))
    return None

# ---------------------------------------------------------------- desert (drawn into the base)
engine.DESERT_POLY = [(-3, 37.6), (10.9, 37.6), (11.6, 35.3), (20, 33.7), (26, 33.1), (31.5, 32.7), (33.9, 31.65), (34.25, 31.32), (34.75, 31.25), (35.35, 31.08),
    (35.78, 31.3), (36.15, 32.0), (36.6, 32.6), (36.75, 33.3), (37.3, 34.2), (38.2, 34.9), (39.6, 35.4), (40.6, 34.85), (41.6, 34.2), (42.8, 33.5), (43.8, 32.5),
    (44.6, 31.5), (46.0, 30.7), (47.5, 29.95), (48.5, 29.3), (50.0, 27.5), (52.5, 25.9), (56.4, 26.6), (57.6, 25.0), (60.5, 22.5), (58, 16), (52, 13.6), (45, 11.9),
    (43.4, 12.55), (42.3, 14.0), (40.9, 15.6), (39.7, 15.3), (38.0, 16.2), (36.5, 15.8), (34, 15.3), (30, 15.0), (22, 15.5), (14, 15.5), (-3, 16.5)]

# ---------------------------------------------------------------- regions
DELTA = [(31.233, 30.06), (30.86, 30.42), (30.40, 30.85), (29.98, 31.10), (29.85, 31.25), (30.3, 31.6), (31.0, 31.8), (31.9, 31.75), (32.45, 31.45),
         (32.45, 31.05), (32.15, 30.75), (31.75, 30.45), (31.45, 30.2)]
FAYUM = [(30.79 + 0.27 * math.cos(a), 29.37 + 0.165 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 28, endpoint=False)]
FAYNECK = [(30.90, 29.44), (31.05, 29.36), (31.24, 29.33), (31.24, 29.16), (31.05, 29.21), (30.90, 29.26)]
LEVANT = [(32.4, 31.3), (33.2, 31.45), (34.2, 31.9), (34.6, 32.9), (35.0, 33.9), (35.5, 34.9), (35.6, 35.9), (36.2, 36.4), (37.3, 36.7), (38.1, 36.5), (38.4, 35.9),
          (37.8, 35.0), (37.1, 34.2), (36.7, 33.3), (36.3, 32.3), (35.9, 31.3), (35.3, 30.2), (35.0, 29.5), (34.3, 28.9), (33.6, 28.5), (33.0, 29.2), (32.6, 29.9),
          (32.5, 30.6), (32.3, 31.0)]
HATTI = [(30.5, 39.8), (31, 41.2), (34, 41.9), (37.5, 41.0), (39.5, 39.5), (39.6, 37.8), (38.6, 36.5), (37.4, 35.4), (36.7, 34.75), (36.0, 35.0), (35.9, 36.3),
         (35.0, 36.6), (33.0, 36.3), (31.0, 36.9), (30.2, 37.8)]
PERSIA = [(32.4, 31.3), (33.2, 31.45), (34.2, 31.9), (34.6, 32.9), (35.0, 33.9), (35.5, 34.9), (35.6, 36.0), (33, 36.0), (27, 36.3), (26, 39.5), (27, 41.2), (31, 42),
          (36, 42.3), (41.5, 42), (45, 42.5), (49, 40), (55, 40), (58, 30), (56, 26.5), (52.5, 26.5), (50, 28), (48.3, 29.4), (46, 30.8), (44.6, 31.6), (43, 32.8),
          (41, 33.2), (39, 32.3), (37.2, 31.2), (36.0, 30.0), (35.0, 29.5), (34.3, 30.4), (33.3, 30.9), (32.5, 31.0)]
EGYPT_BOX = [(25.0, 31.9), (29.0, 31.5), (32.4, 31.5), (34.3, 31.35), (34.95, 29.5), (34.4, 27.9), (35.6, 24.0), (35.9, 23.2), (34.0, 22.0), (25.0, 22.0)]

def M(poly, soft=True): return lambda cam, lm: IC.multiply(poly_mask(cam, poly, soft), lm)
def U(*fs): return lambda cam, lm: reduce(IC.lighter, [f(cam, lm) for f in fs])
def Dm(a, *bs): return lambda cam, lm: reduce(IC.subtract, [b(cam, lm) for b in bs], a(cam, lm))
def B(a, b, **kw): return lambda cam, lm: band_mask(cam, C[a], C[b], **kw)
DEL = M(DELTA); FAY = U(M(FAYUM), M(FAYNECK))
VAL = U(B("ASWAN", "APEX"), FAY)                      # the valley, First Cataract to the Delta apex
EGY = U(VAL, DEL)
UPPER = U(B("ASWAN", "MEMPHIS"), FAY); LOWER = U(DEL, B("MEMPHIS", "APEX"))
LEV = M(LEVANT); HAT = M(HATTI); PER = M(PERSIA); EGB = M(EGYPT_BOX)

# ---------------------------------------------------------------- drawing helpers
def alpha_draw(fr, fn, color, a):
    if a <= 0: return
    if a >= 1: fn(fr.d, color); return
    m = Image.new("L", fr.im.size, 0); fn(ImageDraw.Draw(m), 255)
    fr.im.paste(color, (0, 0), m.point(lambda v: int(v * a))); fr.d = ImageDraw.Draw(fr.im)
def T(fr, x, y, txt, size=20, w="s", color=INK, anchor="l", sp=1.2, a=1.0):
    f = font(w, s(size))
    alpha_draw(fr, lambda d, c: text_spaced(d, (s(x), s(y)), txt, f, c, sp, anchor), color, a)
def TL(fr, lon, lat, txt, dx=0, dy=0, **kw):
    x, y = P(fr.cam, lon, lat); T(fr, x + dx, y + dy, txt, **kw)
def region(fr, lon, lat, txt, a=1.0, size=23, color=INK, sp=3.5, dx=0, dy=0, w="s"):
    TL(fr, lon, lat, txt, dx=dx, dy=dy, size=size, w=w, color=color, anchor="m", sp=sp, a=a)
def modern(fr, lon, lat, txt, a=1.0, size=17, dx=0, dy=0, anchor="m", color=GRAY):
    TL(fr, lon, lat, txt, dx=dx, dy=dy, size=size, w="m", color=color, anchor=anchor, sp=4.5, a=a)
def city(fr, name, a=1.0, side="r", r=5, size=19, label=None, dx=0, dy=0, ll=None, color=INK, dot=INK, ring=None):
    if a <= 0: return
    lon, lat = ll or C[name]; x, y = P(fr.cam, lon, lat)
    if ring: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r - 3), s(y - r - 3), s(x + r + 3), s(y + r + 3)], fill=c), ring, a)
    alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=c), dot, a)
    txt = label if label is not None else name
    if not txt: return
    off = r + 8
    if side == "r": T(fr, x + off + dx, y + dy, txt, size=size, anchor="l", a=a, color=color)
    elif side == "l": T(fr, x - off + dx, y + dy, txt, size=size, anchor="r", a=a, color=color)
    elif side == "t": T(fr, x + dx, y - off - size * 0.45 + dy, txt, size=size, anchor="m", a=a, color=color)
    else: T(fr, x + dx, y + off + size * 0.5 + dy, txt, size=size, anchor="m", a=a, color=color)
def cross(fr, lon, lat, a=1.0, r=9, width=4, color=INK):
    if a <= 0: return
    x, y = P(fr.cam, lon, lat); rr = r * min(1.0, a * 1.2)
    def fn(d, c):
        d.line([s(x - rr), s(y - rr), s(x + rr), s(y + rr)], fill=c, width=s(width)); d.line([s(x - rr), s(y + rr), s(x + rr), s(y - rr)], fill=c, width=s(width))
    alpha_draw(fr, fn, color, a)
def pline(fr, pts_px, color=INK, width=3, a=1.0, frac=1.0, arrow=False, dash=None):
    """polyline in output px with alpha"""
    if a <= 0 or frac <= 0: return
    p = partial(np.asarray(pts_px, float) * SS, frac)
    def fn(d, c):
        if dash:
            L = path_len(p); on, off = dash[0] * SS, dash[1] * SS; pos = 0.0
            while pos < L[-1]:
                q0 = partial(p, pos / L[-1]); q1 = partial(p, min(pos + on, L[-1]) / L[-1])
                seg = q1[len(q0) - 1:].copy(); seg[0] = q0[-1]
                if len(seg) >= 2: d.line(list(map(tuple, seg)), fill=c, width=s(width))
                pos += on + off
        else:
            d.line(list(map(tuple, p)), fill=c, width=s(width), joint="curve"); r = s(width) / 2
            for q in (p[0], p[-1]): d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=c)
        if arrow and len(p) >= 2:
            e = p[-1]; k = len(p) - 2
            while k > 0 and np.hypot(*(e - p[k])) < 6 * SS: k -= 1
            v = e - p[k]; n = np.hypot(*v)
            if n > 0:
                v = v / n; o = np.array([-v[1], v[0]]); hl = s(width * 4.2); hw = s(width * 2.2)
                d.polygon([tuple(e + v * hl * 0.55), tuple(e - v * hl * 0.45 + o * hw), tuple(e - v * hl * 0.45 - o * hw)], fill=c)
    alpha_draw(fr, fn, color, a)
def gline(fr, lonlat, **kw):
    pline(fr, proj(fr.cam, lonlat, 1), **kw)
def river(fr, a=1.0):
    """paste the rivers by hand (for scenes created with rivers=False)"""
    if a <= 0: return
    m = fr.scene.rmask if a >= 1 else fr.scene.rmask.point(lambda v: int(v * a))
    fr.im.paste(RIVER, (0, 0), m); fr.d = ImageDraw.Draw(fr.im)
def nile_part(a, b):
    i, j = engine.nile_idx(*C[a]), engine.nile_idx(*C[b])
    return NILE[i:j + 1] if i <= j else NILE[j:i + 1][::-1]
def sweep(fr, a, b, frac, color, alpha=1.0, **kw):
    """valley strip growing from anchor a towards b"""
    if frac <= 0 or alpha <= 0: return
    fr.fill(band_mask(fr.cam, C[a], C[b], 0.0, min(frac, 1.0), **kw), color, alpha)
def dim_v(fr, lon, lat0, lat1, a, txt, side=-1):
    if a <= 0: return
    x, y0 = P(fr.cam, lon, lat0); _, y1 = P(fr.cam, lon, lat1); ym = (y0 + y1) / 2
    ya = ym - (ym - y1) * a; yb = ym + (y0 - ym) * a
    pline(fr, [(x, ya), (x, yb)], width=2.5)
    for y in (ya, yb): pline(fr, [(x - 11, y), (x + 11, y)], width=2.5)
    fr.plaque(x + side * 92, ym, txt, size=28, a=min(1, a * 1.3))

SC = {}
def scene(name, dur, cam, masks, res=None, active=None, rivers=True):
    def deco(fn):
        SC[name] = Scene(name, dur, cam if callable(cam) else (lambda t, c=cam: c), fn, masks, rivers=rivers, res=res, active=active)
        return fn
    return deco
def mover(keys):
    def fn(t):
        for (t0, c0), (t1, c1) in zip(keys, keys[1:]):
            if t <= t0: return c0
            if t < t1: return c0 if c0 == c1 else lerp_cam(c0, c1, (t - t0) / (t1 - t0))
        return keys[-1][1]
    act = [(t0, t1) for (t0, c0), (t1, c1) in zip(keys, keys[1:]) if c0 != c1]
    return fn, act
def egypt(fr, a=1.0, color=GREEN):
    fr.fill(fr.masks["egy"], color, a)

# ---------------------------------------------------------------- Blue Nile (for the flood pulse)
def _blue():
    segs = []
    for f in json.load(open(engine.DATA + "/ne_10m_rivers_lake_centerlines.geojson"))["features"]:
        g = f["geometry"]
        if g and f["properties"].get("name") in ("Abay", "El Bahr el Azraq"):
            for l in ([g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]):
                a = np.asarray(l, dtype=np.float64)[:, :2]
                if len(a) > 2: segs.append(a)
    p = engine._chain(segs)
    if np.hypot(*(p[0] - np.array(C["KHARTOUM"]))) < np.hypot(*(p[-1] - np.array(C["KHARTOUM"]))): p = p[::-1]
    return p
BLUE = _blue()
FLOODPATH = np.vstack([BLUE, NILE])
WALL_L = smooth([(32.2, 24.0), (32.0, 25.3), (31.35, 26.15), (30.55, 27.05), (30.1, 28.2), (30.3, 29.3), (30.05, 30.2), (29.6, 30.8), (29.3, 31.3)], 12)
WALL_R = smooth([(33.6, 24.0), (33.4, 25.4), (33.4, 26.25), (32.65, 26.85), (32.0, 27.4), (31.6, 28.2), (31.8, 29.2), (32.1, 30.0), (32.7, 30.6), (33.1, 31.25)], 12)
def axis_part(a, b):
    i, j = engine.nile_idx(*C[a]), engine.nile_idx(*C[b])
    return engine.AXIS[i:j + 1] if i <= j else engine.AXIS[j:i + 1][::-1]
def rain(fr, lon, lat, a, n=7):
    if a <= 0: return
    x, y = P(fr.cam, lon, lat)
    for k in range(n):
        xx = x + (k - n / 2) * 22; yy = y + (10 if k % 2 else -8)
        pline(fr, [(xx + 9, yy - 16), (xx - 9, yy + 16)], color=(72, 142, 172), width=3.2, a=a)
