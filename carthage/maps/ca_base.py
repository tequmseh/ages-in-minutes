# География, маски и помощники для карт «Carthage in 20 Minutes»
import sys, os, json
from functools import reduce
import engine
from engine import *
from PIL import ImageChops as IC, ImageFilter

WHITE = (255, 255, 255)
PURPLE = (138, 74, 120); PURPLE_L = (212, 181, 203); PURPLE_D = (92, 44, 80)
ROME = (104, 128, 154); ROME_L = (188, 202, 216); ROME_D = (62, 82, 106)
GREEK = (252, 251, 247); SAND_D = (168, 142, 96); MOUNT = (176, 150, 108)
NUM = (224, 199, 150); CHAR = (58, 50, 54); SEA_D = (84, 128, 146)

def cam_at(lon, lat, S): return (lon, lat - 55.0 / S, S)
def cam_box(lon0, lon1, lat0, lat1, mx=40, my=45):
    S = min((H - SAFE - 2 * my) / (lat1 - lat0), (W - 2 * mx) / ((lon1 - lon0) * engine.K))
    return cam_at((lon0 + lon1) / 2, (lat0 + lat1) / 2, S)

C = dict(TYRE=(35.20, 33.27), SIDON=(35.37, 33.56), BYBLOS=(35.65, 34.12), CARTHAGE=(10.32, 36.85), UTICA=(10.06, 37.06), HIPPACRA=(9.87, 37.27),
         TUNES=(10.18, 36.80), GADES=(-6.29, 36.53), MOTYA=(12.45, 37.87), PANORMUS=(13.36, 38.12), LILYBAEUM=(12.44, 37.80), SYRACUSE=(15.29, 37.07),
         HIMERA=(13.82, 37.97), MESSANA=(15.555, 38.19), RHEGIUM=(15.65, 38.11), ECNOMUS=(13.93, 37.10), NORA=(9.02, 38.98), THARROS=(8.44, 39.87),
         IBIZA=(1.43, 38.91), MALACA=(-4.42, 36.72), LIXUS=(-6.11, 35.20), MOGADOR=(-9.77, 31.51), ROME=(12.48, 41.89), NEWCARTHAGE=(-0.98, 37.60),
         SAGUNTUM=(-0.28, 39.68), TREBIA=(9.59, 45.05), TRASIMENE=(12.10, 43.14), CANNAE=(16.15, 41.30), CAPUA=(14.25, 41.08), ZAMA=(9.25, 36.0),
         METAURUS=(13.0, 43.78), ASPIS=(11.10, 36.84), CAPEBON=(11.0, 37.07), SICCA=(8.71, 36.18), HADRUMETUM=(10.64, 35.83), CROTON=(17.12, 39.08),
         LEPTIS=(14.29, 32.64), HIPPO=(7.75, 36.90), ICOSIUM=(3.06, 36.80), RUSADDIR=(-2.94, 35.30), SABRATHA=(12.48, 32.80), SALAMIS=(23.5, 37.95),
         CASTULO=(-3.62, 38.04), RIOTINTO=(-6.6, 37.7), CAMARINA=(14.45, 36.87), PASS=(9.75, 36.40))

# ---------------------------------------------------------------- rings and regions
def _inside(a, x, y):
    x0, y0 = a[:-1, 0], a[:-1, 1]; x1, y1 = a[1:, 0], a[1:, 1]
    c = ((y0 > y) != (y1 > y)) & (x < (x1 - x0) * (y - y0) / (y1 - y0 + 1e-15) + x0)
    return bool(c.sum() % 2)
def ring_at(lon, lat):
    best = None
    for a in engine.LAND10:
        if a[:, 0].min() <= lon <= a[:, 0].max() and a[:, 1].min() <= lat <= a[:, 1].max() and _inside(a, lon, lat):
            if best is None or len(a) < len(best): best = a
    return best
R_SIC = ring_at(14.0, 37.6); R_SAR = ring_at(9.0, 40.0); R_COR = ring_at(9.1, 42.1); R_IBI = ring_at(1.42, 38.98)
def RING(a): return lambda cam, lm: IC.multiply(poly_mask(cam, a, soft=False), lm)
def M(poly, soft=True): return lambda cam, lm: IC.multiply(poly_mask(cam, poly, soft), lm)
def U(*fs): return lambda cam, lm: reduce(IC.lighter, [f(cam, lm) for f in fs])
def Dm(a, *bs): return lambda cam, lm: reduce(IC.subtract, [b(cam, lm) for b in bs], a(cam, lm))
def X(a, b): return lambda cam, lm: IC.multiply(a(cam, lm), b(cam, lm))
def COAST(poly, wdeg):
    """coastal band of the given width inside a polygon"""
    def f(cam, lm):
        q = 4; small = lm.resize((W * SS // q, H * SS // q), Image.BILINEAR)
        r = max(1.0, wdeg * cam[2] * SS / q)
        band = IC.invert(small).filter(ImageFilter.GaussianBlur(r * 0.6)).point(lambda v: 255 if v > 26 else 0).filter(ImageFilter.GaussianBlur(1.2))
        return IC.multiply(IC.multiply(band.resize(lm.size, Image.BILINEAR), lm), poly_mask(cam, poly, True))
    return f
SIC = RING(R_SIC); SAR = RING(R_SAR); COR = RING(R_COR); IBI = RING(R_IBI)
SICW_P = [(11.8, 38.7), (13.62, 38.7), (13.3, 37.15), (11.8, 36.8)]
SICW = X(SIC, M(SICW_P)); SICE = Dm(SIC, SICW)
AFR_HOME_P = [(8.5, 37.6), (11.5, 37.6), (11.5, 35.2), (10.9, 34.6), (9.0, 35.1), (8.3, 36.2)]
AFR_SMALL_P = [(9.35, 37.6), (11.5, 37.6), (11.5, 36.1), (10.5, 35.85), (9.6, 36.2)]
AFR_COAST_P = [(-5.95, 35.9), (-5.2, 35.95), (-2, 36.2), (3, 37.3), (8.5, 37.7), (11.6, 37.7), (11.6, 34), (16, 33.0), (16, 30), (-5.95, 33)]
MOR_COAST_P = [(-7.2, 35.9), (-5.2, 35.95), (-5.0, 34.5), (-8, 32), (-11, 30), (-11, 36)]
NUMIDIA_P = [(-1.8, 35.6), (-1.0, 36.6), (3, 37.4), (8.5, 37.7), (8.3, 36.2), (9.0, 35.1), (10.9, 34.6), (10.6, 33.4), (5, 33.3), (-1.8, 33.6)]
SPAIN_P = [(-7.5, 35.96), (-5.61, 35.96), (-5.3, 36.02), (-2, 36.3), (0.6, 37.5), (1.3, 40.2), (0.9, 40.72), (0.2, 41.0), (-1.5, 40.6), (-3.0, 39.8),
           (-4.8, 39.2), (-6.5, 38.6), (-7.5, 37.2)]
ITA_P = [(10.0, 43.95), (12.6, 44.25), (14.5, 43.9), (19.0, 41.0), (19.0, 37.7), (15.75, 37.7), (15.60, 38.0), (15.60, 38.22), (15.70, 38.31), (15.0, 38.9),
         (13.0, 40.5), (11.5, 41.6), (10.6, 42.5), (10.0, 43.3)]
EMPIRE_P = [(-25, 50), (40, 50), (40, 31.2), (34, 29.5), (25, 30.2), (20, 30.0), (15, 30.6), (11, 31.6), (8, 33.6), (0, 33.9), (-8, 31.5), (-25, 31.5)]
AFR_HOME = M(AFR_HOME_P); AFR_SMALL = M(AFR_SMALL_P); NUMIDIA = M(NUMIDIA_P); SPAIN = M(SPAIN_P); ITALY = Dm(M(ITA_P), SIC)
AFR_COAST = COAST(AFR_COAST_P, 0.32); EMPIRE = M(EMPIRE_P)

def _named(name):
    out = []
    for f in json.load(open(engine.DATA + "/ne_10m_rivers_lake_centerlines.geojson"))["features"]:
        g = f["geometry"]
        if g and f["properties"].get("name") == name:
            for l in ([g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]):
                out.append(np.asarray(l, dtype=np.float64)[:, :2])
    return out
EBRO = _named("Ebro")

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

# ---------------------------------------------------------------- Carthage-specific helpers
def blank(fr, color):
    fr.im.paste(color, (0, 0, fr.im.size[0], fr.im.size[1])); fr.d = ImageDraw.Draw(fr.im)
def poly(fr, pts, color, a=1.0, outline=None, width=2):
    def fn(d, c):
        q = [(s(x), s(y)) for x, y in pts]; d.polygon(q, fill=c)
    alpha_draw(fr, fn, color, a)
    if outline: pline(fr, list(pts) + [pts[0]], color=outline, width=width, a=a)
def circ(fr, x, y, r, color=None, a=1.0, outline=None, width=2):
    if a <= 0: return
    if color is not None: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=c), color, a)
    if outline is not None: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], outline=c, width=s(width)), outline, a)
def rot(pts, ang, cx=0.0, cy=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]
def boat(fr, x, y, ang, color, a=1.0, k=1.0):
    L, Wd = 11 * k, 4.2 * k
    poly(fr, rot([(L, 0), (L * 0.45, -Wd), (-L, -Wd), (-L, Wd), (L * 0.45, Wd)], ang, x, y), color, a)
def fleet(fr, lon, lat, n, color, ang=0.0, a=1.0, k=1.0, cols=3, dx=0, dy=0, gap=(26, 13)):
    if a <= 0: return
    x, y = P(fr.cam, lon, lat); x += dx; y += dy; rows = (n + cols - 1) // cols
    for i in range(n):
        r, c = divmod(i, cols)
        ox = (c - (cols - 1) / 2) * gap[0] * k + (gap[0] * 0.5 * k if r % 2 else 0); oy = (r - (rows - 1) / 2) * gap[1] * k
        (px, py), = rot([(ox, oy)], ang, x, y); boat(fr, px, py, ang, color, a, k)
def block(fr, lon, lat, color, a=1.0, w=26, h=13, ang=0.0, dx=0, dy=0, outline=WHITE):
    if a <= 0: return
    x, y = P(fr.cam, lon, lat); x += dx; y += dy
    if outline: poly(fr, rot([(-w / 2 - 2.5, -h / 2 - 2.5), (w / 2 + 2.5, -h / 2 - 2.5), (w / 2 + 2.5, h / 2 + 2.5), (-w / 2 - 2.5, h / 2 + 2.5)], ang, x, y), outline, a)
    poly(fr, rot([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)], ang, x, y), color, a)
def mounts(fr, lonlat, a=1.0, step=30, size=10, color=MOUNT, width=3, rows=1, gap=15):
    if a <= 0: return
    p = np.asarray(proj(fr.cam, smooth(lonlat, 8), 1)); L = path_len(p); n = max(2, int(L[-1] / step))
    for r in range(rows):
        for i in range(n + 1):
            q = partial(p, min(1.0, (i + (0.5 if r % 2 else 0)) / n))[-1]; x, y = q[0], q[1] + (r - (rows - 1) / 2) * gap
            if not (-40 < x < W + 40 and -40 < y < H + 40): continue
            pline(fr, [(x - size, y + size * 0.6), (x, y - size * 0.6), (x + size, y + size * 0.6)], color=color, width=width, a=a)
def ring(fr, lon, lat, r, color=INK, a=1.0, width=3, frac=1.0, start=-90, dash=None):
    if a <= 0 or frac <= 0: return
    x, y = P(fr.cam, lon, lat); n = max(8, int(64 * frac))
    ang = np.radians(start + np.linspace(0, 360 * min(frac, 1.0), n))
    pline(fr, np.stack([x + r * np.cos(ang), y + r * np.sin(ang)], 1), color=color, width=width, a=a, dash=dash)
def pdot(fr, name, a=1.0, r=6, color=PURPLE, ringc=WHITE, ll=None):
    if a <= 0: return
    x, y = P(fr.cam, *(ll or C[name]))
    if ringc: circ(fr, x, y, r + 3, ringc, a)
    circ(fr, x, y, r, color, a)
def gdot(fr, name, a=1.0, r=6, ll=None):
    """Greek city: white with a dark outline"""
    if a <= 0: return
    x, y = P(fr.cam, *(ll or C[name])); circ(fr, x, y, r + 2.5, INK, a); circ(fr, x, y, r, GREEK, a)
def carthage(fr, a=1.0, r=9, label="CARTHAGE", side="r", size=24, color=INK, dot=PURPLE, **kw):
    city(fr, "CARTHAGE", a=a, r=r, label=label, side=side, size=size, ring=WHITE, dot=dot, color=color, **kw)
def date(fr, txt, a=1.0, x=250, y=120, size=32): fr.plaque(x, y, txt, size=size, a=a)

def cannae(fr, x0, y0, w, h, p, a=1.0, labels=True, frame=True, la=1.0):
    """Encirclement scheme. p: 0 lines drawn up, 0.5 centre bent back, 1 ring closed."""
    if a <= 0: return
    if frame:
        poly(fr, [(x0 - 3, y0 - 3), (x0 + w + 3, y0 - 3), (x0 + w + 3, y0 + h + 3), (x0 - 3, y0 + h + 3)], INK, a)
        poly(fr, [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], (247, 240, 224), a)
    cx = x0 + w / 2; u = w / 600.0
    e = lambda v: ease(max(0.0, min(1.0, v)))
    adv = e(p / 0.62); bend = 1 - 2 * e((p - 0.12) / 0.45); close = e((p - 0.55) / 0.3); rear = e((p - 0.68) / 0.32); cavoff = e((p - 0.1) / 0.3)
    yc = y0 + h * 0.60
    # Roman infantry: deep block, pushes down into the pocket and gets squeezed
    rw = (300 - 70 * close) * u; rd = (74 + 34 * close) * u; ry = y0 + h * 0.20 + adv * h * 0.24
    R = lambda xa, ya, xb, yb, col: poly(fr, [(xa, ya), (xb, ya), (xb, yb), (xa, yb)], col, a)
    R(cx - rw / 2, ry, cx + rw / 2, ry + rd, ROME)
    # Roman cavalry on the wings: driven off early
    ca = a * (1 - cavoff)
    if ca > 0:
        for sg in (-1, 1):
            xx = cx + sg * (215 + 60 * cavoff) * u; poly(fr, [(xx - 24 * u, ry - 40 * u * cavoff), (xx + 24 * u, ry - 40 * u * cavoff), (xx + 24 * u, ry + 30 * u - 40 * u * cavoff), (xx - 24 * u, ry + 30 * u - 40 * u * cavoff)], ROME_L, ca)
    # Carthaginian centre: thin crescent, bulging forward, then bending back
    n = 9; half = 150 * u; amp = 46 * u
    for i in range(n):
        xi = -half + 2 * half * (i + 0.5) / n; yy = yc - bend * amp * (1 - (xi / half) ** 2) + (1 - bend) * 0.5 * 26 * u
        R(cx + xi - half / n + 2 * u, yy - 9 * u, cx + xi + half / n - 2 * u, yy + 9 * u, PURPLE)
    # African infantry at both ends: wheel inwards on the Roman flanks
    for sg in (-1, 1):
        xx = cx + sg * (half + 30 * u - close * 42 * u); y1 = yc - 16 * u - close * 60 * u; y2 = yc + 46 * u - close * 16 * u
        R(xx - 15 * u, y1, xx + 15 * u, y2, PURPLE_D)
    # cavalry: sweeps round and closes the rear
    for sg in (-1, 1):
        ax, ay = cx + sg * 250 * u, yc + 6 * u
        bx, by = cx + sg * (255 - 0 * u) * u, y0 + h * 0.17
        ex, ey = cx + sg * 76 * u, ry - 22 * u
        q = cavoff * 0.5 + rear * 0.5
        if q < 0.5: xx, yy = ax + (bx - ax) * q * 2, ay + (by - ay) * q * 2
        else: xx, yy = bx + (ex - bx) * (q - 0.5) * 2, by + (ey - by) * (q - 0.5) * 2
        wv = (26 + 44 * rear) * u
        R(xx - wv, yy - 10 * u, xx + wv, yy + 10 * u, PURPLE)
    if labels and la > 0:
        T(fr, x0 + 18 * u, y0 + 26 * u, "ROME", size=17 * u, w="b", color=ROME_D, sp=3, a=a * la)
        T(fr, x0 + 18 * u, y0 + h - 24 * u, "HANNIBAL", size=17 * u, w="b", color=PURPLE_D, sp=3, a=a * la)

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
