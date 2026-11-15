# География, маски и помощники для карт «Persia in 20 Minutes» (вид Look A, 60 кадров/с)
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
PER = (164, 72, 56); PER_L = (218, 170, 150); PER_D = (112, 42, 32)          # Persia: brick red
BAB_C = (104, 124, 150); LYD_C = (140, 108, 148); EGY_C = (72, 140, 118); MED_C = (150, 118, 84)   # the four old powers
GREEK = (84, 120, 160); GREEK_L = (176, 196, 218); MACE = (96, 96, 112)
SAND_D = (168, 142, 96); MOUNT = (150, 124, 88); SEA_T = (72, 112, 132); CHAR = (60, 60, 60); GOLD = (196, 150, 40)

def cam_at(lon, lat, S): return (lon, lat - 55.0 / S, S)
def cam_box(lon0, lon1, lat0, lat1, mx=40, my=45):
    S = min((H - SAFE - 2 * my) / (lat1 - lat0), (W - 2 * mx) / ((lon1 - lon0) * engine.K))
    return cam_at((lon0 + lon1) / 2, (lat0 + lat1) / 2, S)
FULL = cam_full()

# ---------------------------------------------------------------- terrain: deserts stay sand, mountain belts get soft relief
DESERTS = [
    [(-3, 37.6), (10.9, 37.6), (11.6, 35.3), (20, 33.7), (25, 31.4), (29.3, 30.6), (30.2, 29.0), (30.6, 26.5), (32.2, 24.0), (33.4, 24.0), (32.4, 26.6), (31.6, 29.2), (32.3, 30.9),
     (33.9, 31.0), (34.25, 31.2), (35.2, 30.9), (35.9, 31.4), (36.3, 32.2), (36.9, 33.3), (37.6, 34.4), (38.8, 35.2), (40.2, 35.0), (41.4, 34.3), (42.8, 33.4), (43.7, 32.4),
     (44.5, 31.4), (46.0, 30.5), (47.5, 29.95), (48.5, 29.3), (50.0, 27.5), (52.5, 25.9), (56.4, 26.6), (57.6, 25.0), (60.5, 22.5), (58, 16), (52, 13.6), (45, 11.9),
     (43.4, 12.55), (42.3, 14.0), (40.9, 15.6), (39.7, 15.3), (38.0, 16.2), (36.5, 15.8), (34, 15.3), (30, 15.0), (22, 15.5), (14, 15.5), (-3, 16.5)],
    [(51.5, 35.2), (54, 35.6), (57.5, 35.2), (59.5, 33.5), (60.3, 31.0), (60.0, 28.6), (58.6, 27.8), (57.2, 29.4), (55.5, 31.4), (53.2, 32.6), (51.8, 33.9)],       # Kavir + Lut
    [(54.5, 41.8), (58, 43.5), (63, 44.2), (66.5, 42.5), (66.0, 39.6), (63.5, 37.6), (60.5, 37.4), (57.0, 38.6), (54.2, 39.4)],                                   # Karakum + Kyzylkum
    [(60.5, 31.0), (64.5, 31.2), (66.5, 29.4), (65.5, 27.2), (62.5, 26.0), (60.6, 27.4)],                                                                          # Sistan / Registan
    [(69.5, 29.6), (72.5, 29.8), (73.5, 27.0), (71.5, 24.6), (69.2, 25.2), (69.0, 27.6)],                                                                          # Thar
]
RANGES = [  # (polyline lon/lat, width in degrees, strength)
    ([(45.3, 37.2), (46.6, 35.2), (48.0, 33.5), (50.0, 31.8), (51.8, 30.2), (53.6, 28.6), (55.6, 27.6)], 1.3, 1.0),            # Zagros
    ([(46.9, 36.0), (48.6, 34.3), (50.6, 32.6), (52.4, 31.0)], 0.9, 0.7),
    ([(48.6, 37.6), (50.4, 36.5), (52.4, 36.0), (54.6, 36.6), (56.8, 37.4), (59.0, 36.6)], 0.8, 1.0),                              # Elburz / Kopet Dag
    ([(30.0, 37.0), (32.0, 36.75), (34.0, 37.1), (36.0, 37.6), (38.2, 38.1), (40.5, 38.3), (43.2, 38.0)], 0.9, 0.9),               # Taurus
    ([(31.5, 41.2), (34.5, 41.3), (37.5, 40.7), (40.5, 40.6), (42.2, 41.2)], 0.7, 0.7),                                            # Pontic
    ([(37.8, 43.9), (40.5, 43.3), (43.2, 42.7), (46.0, 41.9), (48.6, 41.0)], 0.8, 1.0),                                            # Caucasus
    ([(40.8, 40.2), (43.0, 39.6), (45.4, 39.2)], 0.8, 0.6),                                                                        # Armenian highland
    ([(62.5, 34.6), (65.5, 34.9), (68.5, 35.4), (71.2, 36.3), (73.6, 36.6)], 1.2, 1.0),                                            # Hindu Kush
    ([(66.6, 30.2), (67.8, 32.2), (69.6, 33.6)], 0.8, 0.7),                                                                        # Sulaiman
    ([(70.5, 38.6), (72.6, 38.4), (74.5, 37.6)], 1.2, 0.9),                                                                        # Pamir
    ([(20.4, 41.6), (21.0, 40.0), (21.6, 38.9), (22.2, 38.3)], 0.5, 0.7),                                                          # Pindus
    ([(23.0, 42.8), (25.0, 42.7), (27.0, 42.75)], 0.5, 0.6), ([(23.3, 41.75), (24.6, 41.6), (25.6, 41.45)], 0.5, 0.6),            # Balkan, Rhodope
    ([(35.85, 33.4), (36.1, 34.2), (36.2, 35.6)], 0.35, 0.7), ([(53.0, 26.9), (57.0, 26.0)], 0.0, 0.0),                           # Lebanon
    ([(36.6, 14.5), (38.5, 12.5), (39.2, 10)], 1.6, 0.7),
    ([(22.28, 38.745), (22.5, 38.755), (22.74, 38.735)], 0.05, 0.9),                                                               # Kallidromo, above Thermopylae                                                                          # Ethiopian highland
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
def base_image(cam, lm, desert=None):
    mot, grn = look.terrain(cam); q = 4
    dz = np.zeros((H * SS, W * SS), np.float32)
    dm = Image.new("L", (W * SS // q, H * SS // q), 0); dd = ImageDraw.Draw(dm)
    for poly in DESERTS: dd.polygon(list(map(tuple, proj(cam, engine._chaikin(np.asarray(poly, float), 2)) / q)), fill=255)
    dz = np.asarray(dm.filter(ImageFilter.GaussianBlur(max(2.0, 0.5 * cam[2] * SS / q))).resize((W * SS, H * SS), Image.BILINEAR), np.float32) / 255
    grn = np.clip(grn * (1 - dz) * 1.2 + grn * dz * 0.08, 0, 1)
    a, L = look.style(lm, mot, grn)
    # relief: ridge field -> hillshade (light from the north-west) + a brown tint on the heights
    r = _blur_lines(cam, RANGES, q)
    if r.max() > 0:
        tex = look._vnoise if hasattr(look, "_vnoise") else None
        hh, ww = r.shape; clon, clat, S = cam
        x = (np.arange(ww, dtype=np.float32) + 0.5) * q; y = (np.arange(hh, dtype=np.float32) + 0.5) * q
        LON, LAT = np.meshgrid(clon + (x - W * SS / 2) / (S * SS * engine.K), clat - (y - H * SS / 2) / (S * SS))
        rough = 0.55 + 0.45 * (look._vnoise(LON / 0.22 + 5, LAT / 0.22 + 9) * 0.6 + look._vnoise(LON / 0.07 + 3, LAT / 0.07 + 7) * 0.4) * 2
        hgt = r * rough
        gy, gx = np.gradient(hgt); shade = np.clip((-gx - gy) * 9.0, -1, 1)
        up = lambda v: np.asarray(Image.fromarray(v.astype(np.float32)).resize((W * SS, H * SS), Image.BICUBIC), np.float32)
        R = up(r)[..., None]; SH = up(shade)[..., None]
        land = a * (1 - 0.30 * R) + np.array(MOUNT, np.float32) * (0.30 * R)
        land = land * (1 + 0.16 * SH * np.clip(R * 2.5, 0, 1))
        a = a * (1 - L) + land * L
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
engine.base_image = base_image

# ---------------------------------------------------------------- places (lon, lat)
C = dict(BABYLON=(44.42, 32.54), SUSA=(48.26, 32.19), SARDIS=(28.04, 38.49), ECBATANA=(48.52, 34.80), PERSEPOLIS=(52.89, 29.93), PASARGADAE=(53.17, 30.19), MEMPHIS=(31.25, 29.85),
         ATHENS=(23.73, 37.98), SPARTA=(22.43, 37.07), MILETUS=(27.28, 37.53), MARATHON=(23.97, 38.15), THERMOPYLAE=(22.54, 38.80), PLATAEA=(23.27, 38.22),
         THEBES=(23.32, 38.32), HALICARNASSUS=(27.42, 37.04), JERUSALEM=(35.22, 31.78), OPIS=(44.55, 33.3), BEHISTUN=(47.44, 34.39), ELEPHANTINE=(32.89, 24.09),
         BACTRA=(66.9, 36.76), CUNAXA=(44.2, 33.3), TRAPEZUS=(39.72, 41.0), EPHESUS=(27.34, 37.94), PELLA=(22.52, 40.76), DELPHI=(22.50, 38.48),
         ABYDOS=(26.40, 40.19), ATHOS=(23.92, 40.37), LADE=(27.27, 37.52), SAMOS=(26.95, 37.75), AEGOSPOTAMI=(26.63, 40.33), ERETRIA=(23.79, 38.39),
         GORDION=(31.99, 39.65), TYRE=(35.20, 33.27), GAZA=(34.45, 31.5), DAMASCUS=(36.30, 33.51), NINEVEH=(43.15, 36.36), ARBELA=(44.01, 36.19),
         GRANICUS=(27.3, 40.3), ISSUS=(36.2, 36.85), GAUGAMELA=(43.25, 36.56), MARACANDA=(66.97, 39.65), TAXILA=(72.8, 33.75), SIDON=(35.37, 33.56),
         PELUSIUM=(32.55, 31.04), SALAMIS=(23.50, 37.95), LEBANON=(35.9, 34.0), AMPE=(47.9, 30.6), HECATOMPYLOS=(54.6, 36.1))

# ---------------------------------------------------------------- regions (from the pilot, tightened)
HELL = [(26.1, 39.95), (26.19, 40.025), (26.33, 40.10), (26.39, 40.15), (26.41, 40.20), (26.52, 40.28), (26.68, 40.38), (26.9, 40.47), (27.5, 40.7)]
BOSP = [(28.6, 40.85), (28.99, 41.0), (29.05, 41.08), (29.07, 41.14), (29.13, 41.24), (29.5, 41.5)]
AEG_COAST = [(27.9, 36.45), (27.25, 36.55), (27.15, 37.0), (27.1, 37.55), (26.95, 38.0), (26.25, 38.15), (26.3, 38.7), (26.7, 38.9), (26.6, 39.3), (26.0, 39.5)]
EMPIRE_CORE = (AEG_COAST + HELL + BOSP + [(31, 41.7), (33, 42.5), (35.2, 42.4), (37, 41.7), (39.5, 41.5), (41.3, 41.9), (41.2, 42.9),
    (42, 43.2), (45, 42.7), (47.5, 42.2), (48.6, 42.0), (52.5, 41.6), (54.5, 41.4), (57, 42.6), (59.5, 43.2), (61.5, 42.6), (64, 42.0), (66.5, 41.9), (68.6, 41.6), (70.4, 40.9),
    (71.2, 39.6), (70.8, 38.2), (71.6, 37.0), (73.0, 35.8), (73.6, 34.3), (73.3, 32.5), (72.4, 30.6), (71.2, 28.4), (70.0, 26.2), (69.2, 24.6), (68.4, 23.4), (66, 24.6), (62, 23), (57, 24),
    (56.6, 26.1), (54, 26), (51, 27), (49.6, 29.2), (48.4, 29.4), (47, 29.5), (44.5, 30.5), (42, 32), (39.5, 32.5), (37.5, 31), (36, 29.3), (35, 29),
    (34.6, 27.6), (36.2, 23.9), (35.3, 23.6), (33.4, 23.7), (31.4, 23.9), (30.3, 25.6), (29.4, 27.6), (28.2, 29.2), (26.0, 30.2), (23.0, 30.5), (20.6, 30.6), (19.9, 31.4), (19.8, 33.3),
    (24, 32.9), (29, 32.1), (32, 32.2), (31.6, 34), (31.6, 35.9), (29.5, 35.9)])
MEDIA = [(35.3, 42.4), (41.3, 42.5), (45, 42.7), (48.6, 42), (49.5, 38.5), (50, 37.2), (54, 37.2), (57, 38.5), (61, 37.5), (61.5, 34.5), (58.5, 31.8), (55.5, 31.6),
         (51, 33.5), (48, 33.5), (46, 35), (44, 36.5), (41.5, 37), (38.5, 37.2), (36.5, 38), (35, 39.5)]
ELAM = [(47.2, 33.3), (48, 33.5), (51, 33.5), (51.5, 31.5), (50.2, 30.2), (49.6, 29.2), (48.4, 29.4), (48.2, 31.5)]
PARSA = [(50.2, 30.2), (51.5, 31.5), (54, 31.2), (55.5, 29.5), (55.5, 27.3), (54, 26), (51, 27), (49.6, 29.2)]
LYDIA = AEG_COAST[1:] + HELL + BOSP + [(31, 41.7), (33, 42.5), (35.2, 42.4), (35, 39.5), (34.3, 38), (33.2, 37.2), (31, 37.1), (29, 36.9), (28.2, 36.85)]
BABYLONIA = [(48.2, 29.8), (48.2, 31.5), (47.2, 33.3), (46, 35), (44, 36.5), (41.5, 37), (38.5, 37.2), (36.4, 37.1), (35.6, 36.7), (35.2, 35), (34.6, 32.5),
           (34.0, 31.2), (34.9, 29.4), (36, 29.3), (37.5, 31), (39.5, 32.5), (42, 32), (44.5, 30.5), (47, 29.5)]
EGYPT = [(25, 32.2), (29, 32.2), (32.5, 32.0), (34.0, 31.25), (34.9, 29.4), (34.6, 27.6), (36.2, 23.9), (35.3, 23.4), (30.5, 23.4), (28.5, 25), (25, 28)]
EGSEL = [(18, 34.5), (29, 32.2), (32.5, 32.0), (34.0, 31.25), (34.9, 29.4), (34.6, 27.6), (37, 23), (18, 22)]
ANATSEL = [(24, 34.3), (34.9, 34.3), (35.3, 35.6), (36.2, 36.3), (36.4, 37.1), (38.5, 37.2), (36.5, 38), (35, 39.5), (35.3, 43), (24, 43)]
IONIA = [(26.0, 40.3), (27.2, 40.45), (27.6, 39.5), (27.95, 38.6), (28.05, 37.6), (28.4, 36.95), (28.0, 36.4), (27.0, 36.4), (26.9, 37.6), (25.9, 38.1), (25.8, 39.6)]
THRACE = ([(29.6, 41.7)] + BOSP[::-1] + HELL[::-1] + [(26.0, 40.0), (26.08, 40.27), (25.4, 40.62), (24.9, 40.87), (24.4, 40.86), (23.9, 40.78), (23.5, 41.2),
          (23.4, 41.6), (24.5, 42.6), (27, 43.6), (28.6, 44.2), (29.4, 43.5), (28.7, 42.3)])
MACEDON = [(22.55, 40.0), (21.6, 40.2), (21.2, 40.9), (22.0, 41.4), (23.4, 41.6), (23.5, 41.2), (23.9, 40.78), (23.75, 40.65), (23.4, 40.75), (23.05, 40.75),
           (22.9, 40.6), (22.7, 40.4), (22.62, 40.1)]
THESSALY = [(21.5, 39.2), (21.6, 39.95), (22.55, 40.0), (22.75, 39.85), (23.4, 39.3), (23.0, 38.95), (22.3, 38.87), (21.6, 39.0)]
BOEOTIA = [(22.85, 38.2), (22.85, 38.6), (23.3, 38.72), (23.72, 38.42), (23.7, 38.2), (23.2, 38.13)]
JUDEA = [(34.5, 31.3), (34.85, 32.2), (35.6, 32.3), (35.6, 31.2), (35.2, 30.9)]
GREECE = [(19.3, 40.0), (22.6, 40.05), (24.5, 38.9), (24.6, 37.4), (23.4, 36.2), (21.4, 36.5), (20.5, 38.0), (19.8, 39.3)]
# 20 tribute districts, drawn as soft borders inside the empire (schematic: Herodotus gives peoples, not frontiers)
GRID = [[(30.5, 35.5), (30.5, 42.5)], [(34.6, 35.5), (34.6, 43)], [(25.5, 38.8), (34.6, 38.8)], [(34.6, 37.7), (38.9, 37.4)], [(38.9, 43), (38.9, 36.8)],
        [(38.9, 37.4), (44.6, 37.4)], [(45.2, 43), (44.6, 37.4), (46, 34.5), (48.2, 30.3), (48.3, 29)], [(40.6, 37.4), (40.1, 33.5), (39.4, 31.8)],
        [(40.1, 34.6), (45.9, 34.6)], [(34.0, 31.6), (34.95, 29.2)], [(25, 33), (25, 27.5)], [(53, 38.2), (53, 33.3)], [(50.3, 33.3), (50.0, 29.6)],
        [(46.6, 33.3), (60.5, 33.3)], [(55.6, 33.3), (55.6, 25.5)], [(52.5, 40.2), (63, 40.2)], [(60.5, 44), (60.5, 24)], [(55.6, 28.8), (69.5, 28.8)],
        [(60.5, 38), (72.5, 38)], [(60.5, 33), (69.5, 33)], [(69.5, 41.5), (69.5, 23)]]

ROYAL_ROAD = smooth([C["SARDIS"], (30.2, 38.9), (31.99, 39.65), (32.85, 39.93), (34.6, 40.0), (36.4, 39.3), (38.3, 38.35), (40.2, 37.9), (42.2, 37.2),
                     (43.5, 36.4), (44.3, 35.3), (45.6, 34.2), (47.0, 33.1), C["SUSA"]])
ROAD_EXT = smooth([C["SUSA"], (50.2, 31.0), (51.6, 30.4), C["PERSEPOLIS"]])
TEN_IN = smooth([C["SARDIS"], (30.3, 37.95), (32.5, 37.87), (34.9, 36.92), (36.2, 36.85), (38.3, 35.9), (40.5, 34.8), (42.5, 34.0), C["CUNAXA"]])
TEN_OUT = smooth([C["CUNAXA"], (43.9, 34.5), (43.3, 36.3), (42.3, 37.6), (41.5, 39.0), (40.5, 40.2), C["TRAPEZUS"]])
ALEX = smooth([C["PELLA"], (24.5, 40.9), (26.4, 40.25), (27.3, 40.3), C["SARDIS"], C["MILETUS"], C["HALICARNASSUS"], (30.5, 37.0), (31.99, 39.65), (34.9, 36.92),
               (36.2, 36.85), (35.2, 33.27), (34.45, 31.5), C["MEMPHIS"], (34.45, 31.5), (35.6, 33.4), (38.3, 35.9), (41.0, 37.0), (43.25, 36.56), C["BABYLON"],
               C["SUSA"], C["PERSEPOLIS"]])
DARIUS_FLIGHT = smooth([(43.25, 36.56), C["ECBATANA"], (51.4, 35.6), (54.3, 35.9)])
XERXES = smooth([C["SARDIS"], (27.2, 39.6), (26.42, 40.2), (26.6, 40.75), (25.5, 40.95), (24.3, 40.95), (23.6, 40.7), (22.95, 40.63), (22.5, 40.0), (22.4, 39.4), (22.45, 38.95), C["THERMOPYLAE"]])
CANAL = smooth([(31.52, 30.57), (31.9, 30.56), (32.28, 30.56), (32.36, 30.3), (32.55, 29.95)], 8)

# ---------------------------------------------------------------- masks
def M(poly, soft=True): return lambda cam, lm: IC.multiply(poly_mask(cam, poly, soft), lm)
def I(f, poly): return lambda cam, lm: IC.multiply(f(cam, lm), poly_mask(cam, poly))
def U(*fs): return lambda cam, lm: reduce(IC.lighter, [f(cam, lm) for f in fs])
def Dm(a, *bs): return lambda cam, lm: reduce(IC.subtract, [b(cam, lm) for b in bs], a(cam, lm))
CORE = M(EMPIRE_CORE)
EGY = I(CORE, EGSEL); BAB = I(CORE, BABYLONIA)
STAGE1 = U(I(CORE, MEDIA), I(CORE, ELAM), I(CORE, PARSA))
WEST = Dm(I(CORE, ANATSEL), STAGE1)
CYRUS = Dm(CORE, BAB, EGY)
EAST = Dm(CYRUS, STAGE1, WEST)
NOEGY = Dm(CORE, EGY)
THR = M(THRACE); MAC = M(MACEDON); ION = I(CORE, IONIA)
MAXE = U(CORE, THR)
def GRIDM(cam, lm):
    m = Image.new("L", (W * SS, H * SS), 0); d = ImageDraw.Draw(m)
    for l in GRID: d.line(list(map(tuple, proj(cam, smooth(l, 4) if len(l) > 2 else l))), fill=255, width=s(2.4))
    return IC.multiply(m, CORE(cam, lm))
def EDGE(f, px=3.2):
    """outline of a mask (drawn darker than the fill, gives territories a crisp border)"""
    def g(cam, lm):
        m = f(cam, lm); q = 2; sm = m.resize((m.size[0] // q, m.size[1] // q), Image.BILINEAR)
        e = IC.subtract(sm, sm.filter(ImageFilter.MinFilter(2 * int(px * SS / q / 2) + 1)))
        return e.resize(m.size, Image.BILINEAR)
    return g

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
def city(fr, name, a=1.0, side="r", r=5, size=19, label=None, dx=0, dy=0, ll=None, color=INK, dot=INK, ring=WHITE):
    if a <= 0: return
    lon, lat = ll or C[name]; x, y = P(fr.cam, lon, lat)
    if ring: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r - 2.5), s(y - r - 2.5), s(x + r + 2.5), s(y + r + 2.5)], fill=c), ring, a)
    alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=c), dot, a)
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
def empire_label(fr, a, lon=49.5, lat=36.2, size=30):
    region(fr, lon, lat, "PERSIAN EMPIRE", a=a, size=size, sp=9, color=WHITE, w="b")

# ---------------------------------------------------------------- voiceover cues
_WORDS = json.load(open(os.path.join(HERE, "../words.json")))
def _norm(w): return "".join(ch for ch in w.lower() if ch.isalnum())
def cue(ch, phrase, nth=1, after=0.0):
    """start time (chapter seconds) of the nth occurrence of a word or phrase in the recorded voiceover"""
    ws = _WORDS[str(ch)]; want = [_norm(x) for x in phrase.split()]; k = 0
    for i in range(len(ws) - len(want) + 1):
        if ws[i][1] < after: continue
        if all(_norm(ws[i + j][0]) == want[j] for j in range(len(want))):
            k += 1
            if k == nth: return float(ws[i][1])
    raise KeyError((ch, phrase, nth))

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
