# География, маски и помощники для карт «The Vikings in 20 Minutes» (вид Look A + рельеф, как в последних картах Персии; проекция Меркатора; 60 кадров/с)
import sys, os, json, math
from functools import reduce
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.append(os.path.join(HERE, "../../carthage/maps"))
import engine
import look
engine.FPS = 60
from engine import *
from PIL import ImageChops as IC, ImageFilter, Image, ImageDraw
import numpy as np

WHITE = (255, 255, 255)
NOR = (150, 52, 46); NOR_L = (214, 160, 146); NOR_D = (98, 30, 28)             # the Norse: dark red
FRK = (86, 112, 158); FRK_L = (172, 190, 216); FRK2 = (122, 104, 150); FRK3 = (92, 138, 128)    # Franks and the three-way split
ENG1 = (104, 124, 150); ENG2 = (140, 108, 148); ENG3 = (72, 140, 118); ENG4 = (176, 132, 70)    # four English kingdoms
BYZ = (120, 72, 132); RUS = (184, 122, 52); RUS_L = (226, 190, 140)
MOUNT = (150, 128, 100); SEA_T = (66, 104, 124); CHAR = (60, 60, 60); GOLD = (196, 150, 40); ICE = (238, 241, 240); FOREST = (150, 168, 120)

def cam_at(lon, lat, S): return (lon, float(MY(lat)) - 55.0 / S, S)
def cam_box(lon0, lon1, lat0, lat1, mx=40, my=45):
    y0, y1 = float(MY(lat0)), float(MY(lat1))
    S = min((H - SAFE - 2 * my) / (y1 - y0), (W - 2 * mx) / (lon1 - lon0))
    return ((lon0 + lon1) / 2, (y0 + y1) / 2 - 55.0 / S, S)

# ---------------------------------------------------------------- terrain: ice caps, northern forest, mountain relief
ICECAPS = [
    [(-48, 61.4), (-45.0, 60.9), (-43.6, 62), (-41.5, 64), (-38, 66), (-31, 68.6), (-25.5, 70.6), (-24, 73), (-22.5, 76), (-22, 80), (-32, 82.3), (-50, 81.8), (-62, 80.6),
     (-66, 78.3), (-60, 76.2), (-56.5, 73), (-53.5, 70), (-51.6, 67.5), (-50.6, 65), (-49.6, 63)],
    [(-18.3, 64.15), (-17.6, 64.75), (-16.1, 64.72), (-15.6, 64.3), (-16.8, 63.98)], [(-20.6, 64.55), (-19.9, 64.9), (-19.4, 64.6), (-20.1, 64.4)],
    [(-19.1, 64.7), (-18.6, 64.98), (-18.2, 64.75), (-18.7, 64.6)], [(-19.4, 63.55), (-18.9, 63.75), (-18.5, 63.6), (-19.0, 63.48)],
]
FORESTS = [[(4, 58), (10, 57.2), (13, 56.2), (20, 54.4), (26, 53), (34, 52), (46, 52.5), (64, 54), (64, 71), (20, 71), (12, 67), (4, 62)]]
RANGES = [  # (polyline lon/lat, width in degrees of longitude, strength)
    ([(6.2, 59.0), (7.6, 60.4), (8.4, 61.6), (9.6, 62.4), (12.4, 63.4), (13.6, 65.2), (15.6, 66.8), (17.8, 68.2), (20.5, 69.2), (23.5, 69.8)], 1.5, 1.0),   # Scandinavian mountains
    ([(7.0, 58.6), (8.0, 59.6), (9.2, 61.0)], 1.3, 0.8), ([(6.2, 60.6), (7.2, 61.6), (8.0, 62.3)], 1.0, 0.8),
    ([(6.6, 44.4), (7.2, 45.6), (8.6, 46.3), (10.4, 46.7), (12.4, 47.0), (14.4, 47.3)], 1.1, 1.0),                                                         # Alps
    ([(-1.6, 43.0), (0.4, 42.7), (2.4, 42.45)], 0.6, 0.9),                                                                                                 # Pyrenees
    ([(-5.4, 56.6), (-4.6, 57.2), (-3.6, 57.1)], 0.9, 0.7), ([(-2.4, 54.2), (-2.2, 54.9), (-2.4, 55.4)], 0.5, 0.45), ([(-3.9, 52.2), (-3.9, 53.05)], 0.5, 0.5),   # Highlands, Pennines, Wales
    ([(18.5, 49.3), (20.5, 49.2), (23.0, 48.6), (25.0, 47.4), (26.2, 45.9), (24.6, 45.4), (22.8, 45.3)], 0.9, 0.8),                                         # Carpathians
    ([(22.6, 42.9), (25.0, 42.7), (27.0, 42.75)], 0.5, 0.6), ([(20.6, 41.6), (21.0, 40.0), (21.8, 38.8)], 0.5, 0.6),                                         # Balkan, Pindus
    ([(37.8, 43.9), (40.5, 43.3), (43.2, 42.7), (46.0, 41.9), (48.6, 41.0)], 0.8, 1.0),                                                                    # Caucasus
    ([(59.0, 52.0), (58.8, 56), (59.6, 60), (60.5, 64)], 1.0, 0.6),                                                                                        # Urals
    ([(30.0, 37.0), (32.0, 36.75), (34.0, 37.1), (36.0, 37.6), (40.5, 38.3)], 0.9, 0.7), ([(31.5, 41.2), (34.5, 41.3), (37.5, 40.7), (40.5, 40.6)], 0.7, 0.6),   # Taurus, Pontic
    ([(-21.5, 64.9), (-19.5, 64.7), (-17.5, 64.6), (-15.6, 64.9)], 1.2, 0.8), ([(-23.0, 65.8), (-22.0, 65.9)], 0.7, 0.5), ([(-19.0, 65.6), (-17.6, 65.7)], 0.8, 0.5),   # Iceland highlands
    ([(-4.9, 37.0), (-3.2, 37.05), (-2.0, 37.3)], 0.5, 0.6), ([(11.0, 44.2), (12.6, 43.2), (13.8, 42.2), (15.2, 40.9)], 0.5, 0.6),                           # Sierra Nevada, Apennines
    ([(-57.6, 49.0), (-56.9, 50.2), (-56.2, 51.2)], 0.5, 0.5),                                                                                             # Long Range, Newfoundland
]
def _blur_lines(cam, lines, q=4):
    w, h = W * SS // q, H * SS // q; acc = np.zeros((h, w), np.float32)
    for pts, wd, k in lines:
        if k <= 0: continue
        m = Image.new("L", (w, h), 0); p = proj(cam, smooth(pts, 8)) / q
        if p[:, 0].max() < -200 or p[:, 0].min() > w + 200 or p[:, 1].max() < -200 or p[:, 1].min() > h + 200: continue
        px = max(2.0, wd * cam[2] * SS / q)
        ImageDraw.Draw(m).line(list(map(tuple, p)), fill=255, width=max(1, int(px * 0.55)), joint="curve")
        acc = np.maximum(acc, np.asarray(m.filter(ImageFilter.GaussianBlur(px * 0.42)), np.float32) / 255 * k)
    return acc
def _zone(cam, polys, blur_deg, q=4):
    dm = Image.new("L", (W * SS // q, H * SS // q), 0); dd = ImageDraw.Draw(dm)
    for poly in polys: dd.polygon(list(map(tuple, proj(cam, engine._chaikin(np.asarray(poly, float), 2)) / q)), fill=255)
    return np.asarray(dm.filter(ImageFilter.GaussianBlur(max(2.0, blur_deg * cam[2] * SS / q))).resize((W * SS, H * SS), Image.BILINEAR), np.float32) / 255
def base_image(cam, lm, desert=None):
    mot, grn = look.terrain(cam); q = 4
    fz = _zone(cam, FORESTS, 1.2); iz = _zone(cam, ICECAPS, 0.35)
    grn = np.clip(grn * (1 + 0.5 * fz) + 0.22 * fz, 0, 1)
    a, L = look.style(lm, mot, grn)
    land = a * (1 - 0.16 * fz[..., None]) + np.array(FOREST, np.float32) * mot[..., None] * (0.16 * fz[..., None])
    r = _blur_lines(cam, RANGES, q)
    if r.max() > 0:
        hh, ww = r.shape; clon, clat, S = cam
        x = (np.arange(ww, dtype=np.float32) + 0.5) * q; y = (np.arange(hh, dtype=np.float32) + 0.5) * q
        LON, LAT = np.meshgrid(clon + (x - W * SS / 2) / (S * SS * engine.K), clat - (y - H * SS / 2) / (S * SS))
        rough = 0.55 + 0.45 * (look._vnoise(LON / 0.22 + 5, LAT / 0.22 + 9) * 0.6 + look._vnoise(LON / 0.07 + 3, LAT / 0.07 + 7) * 0.4) * 2
        hgt = r * rough
        gy, gx = np.gradient(hgt); shade = np.clip((-gx - gy) * 9.0, -1, 1)
        up = lambda v: np.asarray(Image.fromarray(v.astype(np.float32)).resize((W * SS, H * SS), Image.BICUBIC), np.float32)
        R = up(r)[..., None]; SH = up(shade)[..., None]
        land = land * (1 - 0.30 * R) + np.array(MOUNT, np.float32) * (0.30 * R)
        land = land * (1 + 0.16 * SH * np.clip(R * 2.5, 0, 1))
    if iz.max() > 0:
        I_ = np.clip(iz * 1.25, 0, 1)[..., None]
        land = land * (1 - 0.92 * I_) + np.array(ICE, np.float32) * (0.985 + 0.5 * (mot[..., None] - 1)) * (0.92 * I_)
    a = a * (1 - L) + land * L
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
engine.base_image = base_image

# ---------------------------------------------------------------- places (lon, lat)
C = dict(LINDISFARNE=(-1.80, 55.68), YORK=(-1.08, 53.96), DUBLIN=(-6.26, 53.35), PARIS=(2.35, 48.86), ROUEN=(1.10, 49.44), CHARTRES=(1.49, 48.45), HEDEBY=(9.57, 54.49),
         BIRKA=(17.55, 59.33), JELLING=(9.42, 55.76), ROSKILDE=(12.08, 55.64), OSEBERG=(10.44, 59.31), CONSTANTINOPLE=(28.98, 41.01), KYIV=(30.52, 50.45), LADOGA=(32.30, 59.99),
         NOVGOROD=(31.28, 58.52), MOSCOW=(37.62, 55.75), BAGHDAD=(44.37, 33.31), BULGAR=(49.05, 54.98), CORDOBA=(-4.78, 37.89), REYKJAVIK=(-21.90, 64.14),
         THINGVELLIR=(-21.12, 64.26), BRATTAHLID=(-45.52, 61.15), HVALSEY=(-45.63, 60.83), LANSE=(-55.53, 51.60), EDINGTON=(-2.14, 51.28), ATHELNEY=(-2.93, 51.06),
         GRIMSBY=(-0.08, 53.57), DERBY=(-1.48, 52.92), WHITBY=(-0.62, 54.49), STAMFORD=(-0.91, 53.99), HASTINGS=(0.49, 50.91), SPILLINGS=(18.87, 57.75), ORKNEY=(-3.0, 59.0),
         SHETLAND=(-1.3, 60.35), FAROE=(-6.9, 62.0), GNEZDOVO=(31.87, 54.78), UPPLAND=(17.9, 59.75), LONDON=(-0.10, 51.51), CHESTER=(-2.89, 53.19), TRONDHEIM=(10.4, 63.43),
         BERGEN=(5.3, 60.4), GJERMUNDBU=(10.1, 60.1), WINCHESTER=(-1.31, 51.06), RIPON=(-1.5, 54.1), VIK=(10.6, 59.2), SMOLENSK=(32.05, 54.78))

# ---------------------------------------------------------------- regions
DENMARK_P = [(7.9, 54.85), (7.9, 57.9), (10.9, 57.95), (11.5, 56.75), (12.4, 56.65), (13.4, 56.4), (14.7, 56.15), (14.5, 55.25), (12.9, 54.45), (10.5, 54.45), (9.4, 54.78)]
NORWAY_P = [(3.5, 57.7), (7.5, 57.7), (10.4, 58.85), (11.5, 58.9), (12.3, 60.2), (12.6, 61.5), (12.2, 63.3), (14.0, 64.5), (14.6, 66.2), (16.4, 68.0), (20.0, 69.05), (25, 69.0),
            (29, 69.9), (31.5, 70.0), (31, 71.6), (3.5, 71.6)]
SWEDEN_BIG = [(10.9, 55.2), (10.9, 59), (11.5, 69.6), (21, 69.6), (23.6, 67.8), (24.15, 65.8), (22.4, 63.6), (20.2, 60.5), (19.8, 59.6), (20.2, 57), (17, 55.2)]
ENGLAND_P = [(-5.9, 49.85), (1.9, 50.6), (2.1, 53.2), (-0.9, 55.9), (-2.05, 55.82), (-2.6, 55.25), (-3.1, 54.98), (-3.9, 54.5), (-3.2, 53.4), (-3.05, 52.9), (-3.15, 52.3),
             (-2.7, 51.62), (-3.4, 51.3), (-5.9, 50.4)]
NORTHUMBRIA_P = [(-3.3, 53.35), (-2.0, 53.42), (-0.25, 53.68), (0.6, 53.7), (0.4, 56.15), (-3.6, 56.05), (-5.4, 54.8), (-3.9, 54.0)]
MERCIA_P = [(-3.1, 53.33), (-2.0, 53.42), (-0.25, 53.68), (0.45, 53.4), (0.2, 52.75), (-0.2, 52.3), (0.2, 51.75), (-0.5, 51.5), (-2.65, 51.62), (-3.15, 52.3), (-3.05, 52.95)]
EASTANGLIA_P = [(0.2, 52.75), (0.45, 53.2), (2.0, 53.1), (2.0, 51.8), (0.2, 51.75), (-0.2, 52.3)]
WESSEX_P = [(-5.9, 49.85), (1.7, 50.5), (1.7, 51.5), (0.2, 51.75), (-0.5, 51.5), (-2.65, 51.62), (-3.1, 51.2), (-4.5, 51.3), (-5.9, 50.4)]
DANELAW_P = [(-0.05, 51.5), (-0.9, 52.0), (-1.5, 52.5), (-2.1, 52.9), (-2.9, 53.22), (-3.35, 54.0), (-2.6, 54.7), (-1.35, 54.68), (0.6, 54.65), (2.3, 53), (2.1, 51.65), (0.7, 51.45)]
CAROL_P = [(-1.8, 43.35), (0.7, 42.7), (1.5, 41.3), (3.3, 41.8), (3.2, 43.2), (7.5, 43.7), (10.2, 43.9), (12.5, 41.7), (14.0, 41.5), (14.2, 42.5), (13.5, 45.6), (16.5, 46.5),
           (17, 48.2), (14, 49), (12.3, 50.3), (13, 51.5), (11, 53.8), (10.7, 54.3), (8.9, 54.4), (8.3, 53.6), (4.5, 53.6), (1.5, 51.0), (-1.4, 48.75), (-2.0, 47.3), (-1.2, 45.5)]
WFRANK_SEL = [(-12, 40), (3.4, 40), (4.7, 43.2), (4.7, 45.6), (5.2, 47.6), (4.9, 49.8), (3.6, 51.5), (2.0, 52.5), (-12, 52.5)]
EFRANK_SEL = [(7.1, 54.8), (7.3, 51.0), (8.1, 49.5), (7.7, 47.6), (9.5, 47.3), (11.5, 46.95), (13.8, 46.6), (20, 46), (20, 56)]
NORMANDY_P = [(-1.62, 48.5), (-2.05, 49.78), (-1.2, 49.78), (0.1, 49.52), (1.42, 50.1), (1.78, 49.3), (1.72, 48.92), (0.9, 48.42), (-0.6, 48.42)]
RUSLAND_P = [(28.2, 59.6), (30.0, 60.2), (33.5, 60.9), (37, 60.2), (40.5, 58.2), (42.0, 56.0), (39.5, 54.0), (36.0, 51.5), (34.0, 49.4), (31.5, 48.6), (28.0, 49.2), (25.2, 50.6),
             (24.4, 52.6), (26.5, 55.2), (27.6, 57.5)]
GOTLAND_P = [(17.9, 56.85), (19.5, 56.85), (19.5, 58.05), (17.9, 58.05)]
ICELAND_P = [(-25, 63.2), (-13, 63.2), (-13, 66.7), (-25, 66.7)]
GREENSET_P = [(-49.5, 59.7), (-43.2, 59.7), (-43.6, 61.2), (-46.5, 61.9), (-49.0, 62.2), (-52.5, 65.2), (-54.5, 65.2), (-52, 62)]
BYZ_P = [(19.3, 41.9), (19.8, 39.6), (21.0, 37.5), (22.0, 36.2), (24, 34.6), (27, 34.9), (28, 36.3), (30.5, 35.9), (33, 35.9), (36.2, 35.8), (37.5, 37.2), (40.5, 38.5),
         (41.6, 41.6), (39, 41.2), (36, 42.2), (33, 42.2), (30, 41.4), (28.6, 43.8), (25, 43.9), (22.6, 44.3), (21.0, 43.0)]

# ---------------------------------------------------------------- masks
def M(poly, soft=True): return lambda cam, lm: IC.multiply(poly_mask(cam, poly, soft), lm)
def I(f, poly): return lambda cam, lm: IC.multiply(f(cam, lm), poly_mask(cam, poly))
def U(*fs): return lambda cam, lm: reduce(IC.lighter, [f(cam, lm) for f in fs])
def Dm(a, *bs): return lambda cam, lm: reduce(IC.subtract, [b(cam, lm) for b in bs], a(cam, lm))
def COAST(poly, wdeg):
    """coastal band of the given width (degrees of longitude) inside a polygon"""
    def f(cam, lm):
        q = 4; small = lm.resize((W * SS // q, H * SS // q), Image.BILINEAR)
        r = max(1.0, wdeg * cam[2] * SS / q)
        band = IC.invert(small).filter(ImageFilter.GaussianBlur(r * 0.6)).point(lambda v: 255 if v > 26 else 0).filter(ImageFilter.GaussianBlur(1.2))
        return IC.multiply(IC.multiply(band.resize(lm.size, Image.BILINEAR), lm), poly_mask(cam, poly, True))
    return f
def EDGE(f, px=3.2):
    def g(cam, lm):
        m = f(cam, lm); q = 2; sm = m.resize((m.size[0] // q, m.size[1] // q), Image.BILINEAR)
        e = IC.subtract(sm, sm.filter(ImageFilter.MinFilter(2 * int(px * SS / q / 2) + 1)))
        return e.resize(m.size, Image.BILINEAR)
    return g
DENMARK = M(DENMARK_P); NORWAY = M(NORWAY_P); SWEDEN = Dm(M(SWEDEN_BIG), NORWAY, DENMARK)
ENGLAND = M(ENGLAND_P); NORTHUMBRIA = I(ENGLAND, NORTHUMBRIA_P); MERCIA = I(ENGLAND, MERCIA_P); EASTANGLIA = I(ENGLAND, EASTANGLIA_P); WESSEX = I(ENGLAND, WESSEX_P)
DANELAW = I(ENGLAND, DANELAW_P); NOTDANE = Dm(ENGLAND, DANELAW)
CAROL = M(CAROL_P); WFRANK = I(CAROL, WFRANK_SEL); EFRANK = I(CAROL, EFRANK_SEL); MFRANK = Dm(CAROL, WFRANK, EFRANK)
NORMANDY = M(NORMANDY_P); RUSLAND = M(RUSLAND_P); GOTLAND = M(GOTLAND_P, False); ICELAND = M(ICELAND_P, False); GREENSET = COAST(GREENSET_P, 0.9); BYZANT = M(BYZ_P)

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
def sea(fr, lon, lat, txt, a=1.0, size=17, dx=0, dy=0, anchor="m"):
    TL(fr, lon, lat, txt, dx=dx, dy=dy, size=size, w="m", color=SEA_T, anchor=anchor, sp=5, a=a)
def modern(fr, lon, lat, txt, a=1.0, size=17, dx=0, dy=0, anchor="m", color=(120, 108, 84)):
    TL(fr, lon, lat, txt, dx=dx, dy=dy, size=size, w="m", color=color, anchor=anchor, sp=4.5, a=a)
import glob as _glob, os as _os
ICONS = {_os.path.basename(f)[:-4].upper(): f for f in _glob.glob(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "icons", "cities", "png", "*.png"))}
_ICO = {}
def city(fr, name, a=1.0, side="r", r=5, size=19, label=None, dx=0, dy=0, ll=None, color=INK, dot=INK, ring=WHITE, icon=True):
    if a <= 0: return
    lon, lat = ll or C[name]; x, y = P(fr.cam, lon, lat)
    if icon and name in ICONS and r >= 7 and label in (None, ""):
        # city icon from the shared library (icons/cities) instead of a dot; the label keeps its side
        hpx = int(s(r * 10)); k = (name, hpx)
        if k not in _ICO: _ICO[k] = Image.open(ICONS[name]).convert("RGBA").resize((hpx, hpx), Image.LANCZOS).getchannel("A")
        m = _ICO[k]; pos = (int(s(x) - hpx / 2), int(s(y) - hpx / 2))
        if ring:
            halo = m.filter(ImageFilter.MaxFilter(2 * int(s(1.6)) + 1)).filter(ImageFilter.GaussianBlur(s(1.0)))
            fr.im.paste(ring, pos, halo.point(lambda v: int(v * 0.55 * min(1, a))))
        fr.im.paste(dot, pos, m if a >= 1 else m.point(lambda v: int(v * a))); fr.d = ImageDraw.Draw(fr.im)
        r = r * 5.4; ring = None; dot = None
    if ring: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r - 2.5), s(y - r - 2.5), s(x + r + 2.5), s(y + r + 2.5)], fill=c), ring, a)
    if dot: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=c), dot, a)
    txt = label if label is not None else name
    if not txt: return
    off = r + 9
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
def gline(fr, lonlat, halo=None, **kw):
    """polyline in lon/lat; halo = light casing under the line so it reads over any fill"""
    p = proj(fr.cam, lonlat, 1)
    if halo: pline(fr, p, color=halo, width=kw.get("width", 3) + 3.2, a=kw.get("a", 1.0) * 0.9, frac=kw.get("frac", 1.0), dash=kw.get("dash"))
    pline(fr, p, **kw)
def bar(fr, lon, lat, ang, length=18, width=5, a=1.0, frac=1.0, color=INK):
    if a <= 0 or frac <= 0: return
    x, y = P(fr.cam, lon, lat); dx = math.cos(math.radians(ang)) * length / 2; dy = -math.sin(math.radians(ang)) * length / 2
    x0, y0 = x - dx, y - dy; x1, y1 = x0 + 2 * dx * frac, y0 + 2 * dy * frac
    alpha_draw(fr, lambda d, c: d.line([s(x0), s(y0), s(x1), s(y1)], fill=c, width=s(width)), color, a)
def dim_line(fr, lon0, lon1, lat, a, txt, size=32):
    if a <= 0: return
    x0, y = P(fr.cam, lon0, lat); x1, _ = P(fr.cam, lon1, lat); xm = (x0 + x1) / 2
    xa = xm - (xm - x0) * a; xb = xm + (x1 - xm) * a
    pline(fr, [(xa, y), (xb, y)], width=2.8)
    for x in (xa, xb): pline(fr, [(x, y - 12), (x, y + 12)], width=2.8)
    fr.plaque(xm, y, txt, size=size, a=min(1, a * 1.3))
def live(fr, a, b):
    """mark chapter seconds a..b as animated (so frames are not reused there)"""
    off = fr.t - fr.v; fr.scene.auto.add((round(a + off, 3), round(b + off, 3)))
def pulse(fr, ll, t0, dur=2.6, color=INK, n=2, rmax=34, width=3, period=0.9):
    """expanding rings from chapter second t0 for dur seconds, true alpha"""
    live(fr, t0, t0 + dur); t = fr.v
    if not (t0 <= t <= t0 + dur): return
    x, y = P(fr.cam, *ll); fade = min(1.0, (t0 + dur - t) / 0.5)
    for k in range(n):
        ph = (t - t0 - k * period * 0.5) / period
        if ph < 0: continue
        ph = ph % 1.0; r = 6 + rmax * ph
        alpha_draw(fr, lambda d, c, r=r: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], outline=c, width=s(width)), color, (1 - ph) * fade)
def PQ(fr, x, y, txt, a=1.0, size=30, anchor="m", light=False, pad=None):
    """plaque at output px; light = white plaque with dark text (for use over the red fill)"""
    kw = dict(size=size, a=a, anchor=anchor)
    if pad: kw["pad"] = pad
    if light: kw.update(bg=(250, 247, 240), fg=INK)
    return fr.plaque(x, y, txt, **kw)
def PQL(fr, lon, lat, txt, dx=0, dy=0, **kw):
    x, y = P(fr.cam, lon, lat); return PQ(fr, x + dx, y + dy, txt, **kw)
def mfill(fr, mask, color, a):
    """fill with an ad-hoc mask (not through terr)"""
    if a > 0: fr.fill(mask, color, a * FILL_A)
FILL_A = 0.90          # x0.86 inside look.fill: the relief stays readable under the colour
def terr(fr, key, color, a=1.0, edge=None, border=True):
    """territory fill + darker border"""
    if a <= 0: return
    fr.fill(fr.masks[key], color, a * FILL_A)
    ek = key + "_e"
    if border and ek in fr.masks: fr.im.paste(edge or tuple(int(c * 0.72) for c in color), (0, 0), fr.masks[ek].point(lambda v: int(v * a * 0.9))); fr.d = ImageDraw.Draw(fr.im)


# ---------------------------------------------------------------- voiceover cues (sentence starts from timing.json)
_ROWS = json.load(open(os.path.join(HERE, "../timing.json")))
def cue(ch, phrase, frac=None):
    """chapter second at which the sentence starting with `phrase` begins (frac: 0..1 inside that sentence)"""
    for r in _ROWS[str(ch)]["rows"]:
        if r["text"].lower().startswith(phrase.lower()): return r["start"] + ((r["end"] - r["start"]) * frac if frac else 0.0)
    raise KeyError((ch, phrase))

SC = {}
def scene(name, ch, t0, t1, cam, masks, res=None, active=None, rivers=True):
    """ch = chapter, t0..t1 = voiceover seconds the clip covers; the draw function and fr.R work in chapter seconds"""
    dur = round(t1 - t0, 3)
    if isinstance(cam, tuple) and len(cam) == 2 and callable(cam[0]): cam, act0 = cam; active = (active or []) + act0
    if active: active = [(a - t0, b - t0) for a, b in active]
    if callable(cam): cam0 = cam; cam = lambda t, c=cam0: c(t + t0)
    def deco(fn0):
        def fn(fr, t):
            r_ = fr.r; fr.R = lambda a, d=0.6: r_(a - t0, d)          # no reference back to fr: a cycle would keep every 25 MB frame alive until the collector runs
            fr.v = t + t0
            fn0(fr, t + t0)
        mk = dict(masks)
        for k, v in list(masks.items()):
            if not k.endswith("_e") and not k.startswith("x_"): mk[k + "_e"] = EDGE(v)
        sc = Scene(name, dur, cam if callable(cam) else (lambda t, c=cam: c), fn, mk, rivers=rivers, res=res, active=active)
        sc.ch, sc.t0 = ch, t0; SC[name] = sc
        return fn0
    return deco
def mover(keys):
    def fn(t):
        for (t0, c0), (t1, c1) in zip(keys, keys[1:]):
            if t <= t0: return c0
            if t < t1: return c0 if c0 == c1 else lerp_cam(c0, c1, (t - t0) / (t1 - t0))
        return keys[-1][1]
    act = [(t0, t1) for (t0, c0), (t1, c1) in zip(keys, keys[1:]) if c0 != c1]
    return fn, act
