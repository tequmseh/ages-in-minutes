# География, маски и помощники для карт «Ancient Rome in 20 Minutes» (вид Look A + рельеф, как в последних картах Персии; проекция Меркатора; 60 кадров/с)
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

ROM = (156, 44, 40); ROM_L = (214, 150, 138); ROM_D = (100, 26, 26)            # Rome: crimson
CAR = (70, 100, 150); GRK = (60, 132, 110); ETRC = (176, 128, 60); SAM = (120, 110, 84); GAU = (86, 128, 84); PAR = (196, 126, 48)
GOT = (98, 112, 122); HUN = (120, 84, 60); VAN = (116, 78, 136); EST = (120, 72, 132); PALM = (190, 140, 50); GALC = (70, 110, 150); ALLY = (196, 120, 96)
# ---------------------------------------------------------------- terrain: deserts stay sand, mountain belts get soft relief
DESERTS = [
    [(-17, 28), (-10, 29.3), (-5.5, 31.3), (-1, 32.6), (3, 33.6), (7.5, 34.0), (9.8, 33.6), (10.8, 32.9), (13, 32.3), (15.4, 31.6), (18, 30.6), (20, 31.0), (21.5, 32.0), (23, 31.6),
     (25, 31.2), (29.3, 30.6), (30.2, 29.0), (30.6, 26.5), (32.2, 24.0), (33.4, 24.0), (32.4, 26.6), (31.6, 29.2), (32.3, 30.9), (33.9, 31.0), (34.25, 31.2), (35.2, 30.9),
     (35.9, 31.4), (36.3, 32.2), (36.9, 33.3), (37.6, 34.4), (38.8, 35.2), (40.2, 35.0), (41.4, 34.3), (42.8, 33.4), (43.7, 32.4), (44.5, 31.4), (46.0, 30.5), (47.5, 29.95),
     (48.5, 29.3), (50, 27.5), (52.5, 25.9), (56.4, 26.6), (60, 22), (58, 14), (45, 12), (40, 14), (30, 13), (10, 13), (-17, 14)],
    [(51.5, 35.2), (54, 35.6), (57.5, 35.2), (59.5, 33.5), (60.3, 31.0), (60.0, 28.6), (58.6, 27.8), (57.2, 29.4), (55.5, 31.4), (53.2, 32.6), (51.8, 33.9)],
]
RANGES = [  # (polyline lon/lat, width in degrees of longitude, strength)
    ([(6.9, 44.2), (7.0, 45.3), (8.2, 46.1), (10.2, 46.6), (12.2, 47.0), (14.4, 47.3)], 1.1, 1.0),                                                    # Alps
    ([(8.6, 44.45), (10.0, 44.4), (11.5, 43.95), (12.8, 43.0), (13.5, 42.4), (14.4, 41.6), (15.6, 40.6), (16.2, 39.6), (16.3, 38.6)], 0.5, 0.7),      # Apennines
    ([(-1.6, 43.0), (0.4, 42.7), (2.4, 42.45)], 0.6, 0.9), ([(-7, 43.0), (-4, 43.1), (-2, 43.0)], 0.5, 0.6), ([(-6.5, 40.3), (-3.5, 41.0)], 0.5, 0.5),  # Pyrenees, Cantabrian, Central
    ([(-4.9, 37.0), (-3.2, 37.05), (-2.0, 37.3)], 0.5, 0.6), ([(2.6, 45.4), (3.4, 44.5)], 0.7, 0.4),                                                  # Sierra Nevada, Massif Central
    ([(-8, 31), (-5, 32.3), (-2, 33.8), (2, 35.2), (6, 35.6), (9, 35.6)], 0.9, 0.8),                                                                  # Atlas
    ([(14.5, 45.4), (16.5, 44.0), (18.5, 43.0), (19.8, 42.3)], 0.7, 0.7), ([(20.6, 41.6), (21.0, 40.0), (21.8, 38.8)], 0.5, 0.6),                     # Dinaric, Pindus
    ([(22.6, 42.9), (25.0, 42.7), (27.0, 42.75)], 0.5, 0.6), ([(18.5, 49.3), (20.5, 49.2), (23.0, 48.6), (25.0, 47.4), (26.2, 45.9), (24.6, 45.4), (22.8, 45.3)], 0.9, 0.8),
    ([(30.0, 37.0), (32.0, 36.75), (34.0, 37.1), (36.0, 37.6), (38.2, 38.1), (40.5, 38.3), (43.2, 38.0)], 0.9, 0.8), ([(31.5, 41.2), (34.5, 41.3), (37.5, 40.7), (40.5, 40.6)], 0.7, 0.6),
    ([(37.8, 43.9), (40.5, 43.3), (43.2, 42.7), (46.0, 41.9), (48.6, 41.0)], 0.8, 1.0), ([(35.85, 33.4), (36.1, 34.2), (36.2, 35.6)], 0.35, 0.7),      # Caucasus, Lebanon
    ([(45.3, 37.2), (46.6, 35.2), (48.0, 33.5), (50.0, 31.8), (51.8, 30.2)], 1.3, 0.9),                                                               # Zagros
    ([(-4.6, 57.2), (-3.6, 57.1)], 0.9, 0.5), ([(-2.3, 54.2), (-2.3, 55.2)], 0.5, 0.4),
]
def _blur_lines(cam, lines, q=4):
    w, h = W * SS // q, H * SS // q; acc = np.zeros((h, w), np.float32)
    for pts, wd, k in lines:
        px = max(2.0, wd * cam[2] * SS / q)
        if k <= 0 or px > 600: continue
        m = Image.new("L", (w, h), 0); p = proj(cam, smooth(pts, 8)) / q
        if p[:, 0].max() < -200 or p[:, 0].min() > w + 200 or p[:, 1].max() < -200 or p[:, 1].min() > h + 200: continue
        ImageDraw.Draw(m).line(list(map(tuple, p)), fill=255, width=max(1, int(px * 0.55)), joint="curve")
        acc = np.maximum(acc, np.asarray(m.filter(ImageFilter.GaussianBlur(px * 0.42)), np.float32) / 255 * k)
    return acc
def base_image(cam, lm, desert=None):
    mot, grn = look.terrain(cam); q = 4
    dm = Image.new("L", (W * SS // q, H * SS // q), 0); dd = ImageDraw.Draw(dm)
    for poly in DESERTS: dd.polygon(list(map(tuple, proj(cam, engine._chaikin(np.asarray(poly, float), 2)) / q)), fill=255)
    dz = np.asarray(dm.filter(ImageFilter.GaussianBlur(min(60.0, max(2.0, 0.5 * cam[2] * SS / q)))).resize((W * SS, H * SS), Image.BILINEAR), np.float32) / 255
    grn = np.clip(grn * (1 - dz) * 1.2 + grn * dz * 0.08, 0, 1)
    a, L = look.style(lm, mot, grn)
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
        land = a * (1 - 0.30 * R) + np.array(MOUNT, np.float32) * (0.30 * R)
        land = land * (1 + 0.16 * SH * np.clip(R * 2.5, 0, 1))
        a = a * (1 - L) + land * L
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
engine.base_image = base_image

# ---------------------------------------------------------------- places (lon, lat)
C = dict(ROME=(12.483, 41.893), CAPUA=(14.25, 41.08), TARENTUM=(17.23, 40.47), CARTHAGE=(10.32, 36.85), SYRACUSE=(15.29, 37.07), CANNAE=(16.15, 41.31), ZAMA=(9.45, 36.1),
         CORINTH=(22.93, 37.91), NEWCARTHAGE=(-0.99, 37.60), ALEXANDRIA=(29.90, 31.20), PELUSIUM=(32.57, 31.04), EDESSA=(38.79, 37.16), PALMYRA=(38.27, 34.55),
         NICAEA=(29.72, 40.43), CONSTANTINOPLE=(28.98, 41.01), ADRIANOPLE=(26.56, 41.68), SALONA=(16.48, 43.54), KALKRIESE=(8.13, 52.41), RAVENNA=(12.20, 44.42),
         JERUSALEM=(35.22, 31.78), ANTIOCH=(36.16, 36.20), EPHESUS=(27.34, 37.94), THESSALONICA=(22.94, 40.64), LUGDUNUM=(4.83, 45.76), LONDINIUM=(-0.10, 51.51),
         ITALICA=(-6.04, 37.44), LEPTIS=(14.29, 32.64), CARRHAE=(39.03, 36.86), CTESIPHON=(44.58, 33.09), CARNUNTUM=(16.87, 48.11), ATHENS=(23.73, 37.98),
         MEDIOLANUM=(9.19, 45.46), TRIER=(6.64, 49.75), COLONIA=(6.96, 50.94), TARRACO=(1.25, 41.12), GADES=(-6.29, 36.53), NARBO=(3.0, 43.18), MASSILIA=(5.37, 43.30),
         ARIMINUM=(12.57, 44.06), BRUNDISIUM=(17.94, 40.63), DYRRACHIUM=(19.45, 41.32), ANCYRA=(32.85, 39.94), DAMASCUS=(36.30, 33.51), CYRENE=(21.86, 32.82),
         CAESAREA=(2.20, 36.60), TINGIS=(-5.80, 35.78), EBORACUM=(-1.08, 53.96), SIRMIUM=(19.61, 44.97), AQUILEIA=(13.37, 45.77), MOGONTIACUM=(8.27, 50.0),
         OSTIA=(12.29, 41.75), CLUSIUM=(11.95, 43.02), NOLA=(14.53, 40.93), MUTINA=(10.93, 44.65), PHARSALUS=(22.38, 39.30), DUROSTORUM=(27.26, 44.12), MESSANA=(15.55, 38.19),
         LILYBAEUM=(12.44, 37.80), UTICA=(10.06, 37.06), SAGUNTUM=(-0.27, 39.68), CORDUBA=(-4.78, 37.89), BURDIGALA=(-0.58, 44.84), LUTETIA=(2.35, 48.86), BYZANTIUM=(28.98, 41.01))

# ---------------------------------------------------------------- regions (sea-side points are free: every mask is cut by the land)
BRIT_P = [(-6.2, 49.7), (-5.6, 51.8), (-4.9, 53.2), (-4.6, 53.9), (-3.7, 54.75), (-3.0, 54.98), (-1.4, 55.02), (0.2, 54.9), (2.2, 52.8), (1.6, 51.2), (1.0, 50.6), (-1, 50.3), (-4, 49.75)]
CONT_P = [(4.2, 52.1), (6.0, 51.85), (6.7, 51.2), (7.0, 50.7), (7.6, 50.3), (8.3, 50.0), (8.7, 50.3), (9.0, 49.9), (9.4, 49.2), (9.7, 48.9), (10.6, 49.0), (11.6, 48.9), (12.1, 49.0),
          (13.4, 48.55), (14.3, 48.3), (15.6, 48.4), (16.4, 48.2), (17.2, 48.1), (18.1, 47.75), (18.9, 47.8), (19.05, 47.4), (18.95, 46.2), (19.0, 45.5), (20.4, 44.8),
          (21.4, 44.7), (22.6, 44.5), (22.9, 43.85), (24.8, 43.75), (25.4, 43.65), (26.1, 43.95), (27.3, 44.15), (28.0, 45.2),
          (28.3, 45.45), (29.7, 45.2), (31, 43.5), (35, 42.6), (38, 41.8), (41.6, 41.9), (43.5, 41.2), (45.5, 41.0), (46.6, 39.6), (46.0, 38.6), (46.4, 37.2), (46.2, 35.2),
          (46.6, 33.6), (47.6, 31.8), (48.4, 30.3), (48.5, 29.9), (47.0, 30.2), (45.0, 31.2), (43.4, 32.6), (41.5, 34.0), (39.5, 34.2), (38.0, 33.2), (37.2, 32.0), (37.5, 30.5),
          (37.6, 27.0), (36.0, 26.6), (34.8, 27.6), (35.2, 24.4), (33.6, 23.4), (32.3, 23.6), (31.2, 24.5), (30.2, 26.5), (29.6, 28.3), (29.4, 29.6), (28.5, 30.4), (26.5, 30.6),
          (25.0, 30.6), (23.5, 30.9), (21.5, 30.6), (20.0, 30.3), (19.0, 30.0), (17.0, 30.4), (15.0, 30.6), (13.0, 31.2), (11.0, 31.6), (9.6, 32.3), (8.6, 33.6), (7.0, 34.3),
          (5.0, 34.6), (3.0, 34.9), (1.0, 34.5), (-1.5, 34.2), (-3.5, 34.4), (-5.0, 33.7), (-6.2, 33.5), (-7.2, 33.6), (-8.5, 34), (-11, 36), (-11, 44), (-6, 47), (-6, 49.0),
          (-3, 49.5), (-1.5, 49.95), (0.5, 50.35), (1.4, 50.85), (2.2, 51.3), (3.2, 51.9)]
EASTX_P = [(41.5, 41.5), (41.0, 40.2), (40.2, 39.4), (39.0, 38.6), (38.5, 37.5), (38.0, 36.8), (38.3, 36.2), (39.2, 35.4), (39.5, 34.2), (41.5, 34.0), (43.4, 32.6), (45.0, 31.2),
           (47.0, 30.2), (50, 29), (50, 42), (43, 42.5)]
DACIA_P = [(20.4, 44.9), (21.6, 45.7), (22.9, 47.1), (24.0, 47.3), (25.1, 46.6), (25.6, 45.8), (25.3, 45.3), (24.9, 44.5), (24.8, 43.5), (22.9, 43.6), (22.6, 44.2), (21.4, 44.4), (20.4, 44.6)]
MAURET_P = [(-12, 30), (6.1, 30), (6.1, 37.3), (-2, 35.75), (-5.3, 35.95), (-5.9, 35.93), (-12, 35.5)]
ARABIA_P = [(35.0, 29.4), (35.5, 31.0), (35.7, 32.3), (36.6, 33.0), (38.0, 33.2), (37.2, 32.0), (37.5, 30.5), (37.6, 27.0), (36.0, 26.6), (34.8, 27.6)]
SIC_P = [(11.8, 36.4), (11.8, 38.5), (15.0, 38.5), (15.605, 38.32), (15.605, 37.9), (15.9, 37.0), (15.6, 36.4)]
SICW_P = [(11.8, 36.4), (11.8, 38.5), (13.9, 38.5), (14.2, 36.4)]
SARD_P = [(8, 38.7), (8, 41.3), (9.9, 41.3), (9.95, 38.7)]; CORS_P = [(8.4, 41.35), (8.4, 43.1), (9.7, 43.1), (9.7, 41.35)]
PEN_P = [(10.05, 44.0), (10.8, 44.1), (11.5, 44.0), (12.05, 43.93), (12.2, 44.03), (12.32, 44.12), (12.42, 44.19), (13.4, 44.2), (14.6, 43.5), (16.7, 42.3), (18.3, 41.2), (19.0, 40.2), (18.9, 39.0), (17.5, 37.4), (15.3, 37.3),
         (14.0, 40.0), (12.2, 41.0), (10.9, 42.2), (9.9, 42.6), (9.9, 43.5)]
CISALP_P = [(7.5, 43.75), (6.9, 44.3), (6.9, 45.1), (7.0, 45.9), (7.9, 46.0), (8.5, 46.4), (9.4, 46.4), (10.4, 46.6), (11.4, 47.0), (12.3, 46.8), (13.6, 46.5), (13.75, 45.6),
            (13.2, 45.3), (12.9, 44.4), (12.6, 43.6), (10.2, 43.5), (9.6, 43.9), (8.5, 43.9)]
HISP_P = [(-10, 35.6), (-5.9, 35.93), (-5.3, 36.02), (-2, 36.2), (1, 37.5), (4.6, 39), (4.6, 41), (3.2, 42.43), (1.7, 42.5), (0.7, 42.75), (-0.7, 42.9), (-1.75, 43.35), (-1.8, 44.5), (-10, 44.5)]
HISP146_SEL = [(4.6, 41), (3.2, 42.43), (0.7, 42.75), (-1.0, 42.6), (-2.0, 41.2), (-3.2, 39.8), (-5.0, 39.0), (-7.4, 38.0), (-7.4, 36.5), (-5.9, 35.93), (-2, 36.0), (1, 37.5), (4.6, 39)]
BARCID_SEL = [(-8.9, 36.9), (-7.0, 39.0), (-4.0, 40.0), (-1.5, 41.2), (0.9, 40.75), (1, 39), (-2, 36.2), (-5.3, 36.02), (-5.9, 35.93), (-9, 36)]
NARBON_P = [(3.2, 42.43), (1.7, 42.5), (0.9, 42.85), (1.0, 43.9), (2.5, 44.1), (4.0, 44.6), (4.8, 45.5), (6.0, 46.2), (6.9, 45.9), (6.9, 45.1), (6.9, 44.3), (7.5, 43.75), (7.4, 43.2), (4, 42.6)]
GAUL_P = [(-1.75, 43.35), (-0.7, 42.9), (0.7, 42.75), (1.5, 43.0), (3.5, 43.6), (5.5, 44.5), (6.5, 45.6), (6.9, 47.0), (7.6, 47.56), (7.6, 48.3), (8.1, 49.0),
          (8.4, 49.8), (7.9, 50.0), (7.6, 50.4), (7.1, 50.8), (6.8, 51.3), (6.2, 51.8), (4.3, 52.0), (2.5, 51.4), (1.5, 50.9), (0.3, 50.3), (-1.5, 49.95), (-3, 49.5), (-6, 49.0),
          (-6, 47), (-3, 45.5), (-2.2, 44)]
GREECE_P = [(19.2, 41.9), (20.5, 42.2), (22.3, 42.3), (23.6, 41.5), (24.8, 41.4), (24.9, 40.6), (26.3, 39.6), (26, 37), (24.5, 36.0), (22, 36.0), (20.5, 37), (19.3, 39.8)]
AFRICA_P = [(8.6, 37.6), (11.4, 37.6), (11.4, 35.0), (10.6, 34.3), (9.4, 35.2), (8.6, 36.4)]
CARTH_HOME = [(7.0, 37.6), (11.6, 37.6), (11.6, 33.4), (9.6, 33.4), (7.6, 35.2)]
NAFR_COAST = [(-6.5, 34.2), (-6.0, 36.2), (-2, 35.9), (3, 37.4), (9, 37.8), (11.6, 37.6), (11.6, 33.4), (15, 32.6), (19.6, 30.6), (19.6, 29.6), (14, 31.0), (9, 32.6), (3, 34.4), (-3, 33.8)]
SPAIN_COAST = [(-7.4, 36.0), (-7.4, 37.6), (-4, 37.6), (-1.6, 38.2), (-0.4, 39.3), (0.6, 38.4), (-2, 36.2), (-5.3, 36.02)]
ETR_P = [(10.2, 43.85), (11.2, 43.95), (12.0, 43.6), (12.35, 42.9), (12.55, 42.2), (12.42, 41.92), (12.2, 41.72), (11.5, 41.9), (10.6, 42.3), (9.9, 42.6), (9.9, 43.5)]
LAT_P = [(12.2, 41.72), (12.42, 41.92), (12.9, 42.0), (13.4, 41.75), (13.6, 41.25), (13.2, 41.1), (12.5, 41.3)]
SAM_P = [(13.7, 41.9), (14.4, 42.0), (15.1, 41.6), (15.3, 41.1), (14.7, 40.85), (14.0, 41.2), (13.6, 41.5)]
EPIRUS_P = [(19.6, 40.4), (20.0, 40.3), (21.2, 40.2), (21.4, 39.2), (20.9, 38.9), (20.0, 39.3), (19.6, 39.9)]
EAST395_P = [(19.5, 50), (19.4, 44.9), (19.3, 43.5), (19.3, 42.3), (19.15, 41.85), (18.7, 40.5), (18.9, 39), (18.9, 30.2), (19.2, 22), (52, 22), (52, 50)]
GALLIC_SEL = [(-1.75, 43.35), (-0.7, 42.9), (0.7, 42.75), (1.7, 42.5), (3.2, 42.43), (4, 42.4), (7.4, 43.2), (7.5, 43.75), (6.9, 44.3), (6.9, 45.1), (7.0, 45.9), (7.9, 46.0), (8.5, 46.5),
              (9.5, 47.3), (9.5, 49), (9, 50.5), (6, 52.5), (2.5, 51.6), (1.5, 50.9), (0.3, 50.3), (-1.5, 49.95), (-3, 49.5), (-6, 49.0), (-6, 47), (-2.2, 44)]
PALM_SEL = [(33.0, 42.3), (32.2, 40.0), (32.0, 37.6), (32.6, 36.3), (33, 36.05), (35.3, 36.0), (35.5, 35.0), (34.9, 33.5), (33.5, 31.9), (29, 31.6), (28.5, 31.3), (28.5, 22), (52, 22), (52, 42.3)]
PARTHIA_P = [(38.6, 37.3), (39.6, 35.2), (41.5, 34.0), (45.0, 31.0), (48.2, 29.8), (51, 27.5), (56, 26.8), (62, 25.3), (64, 30), (62, 36), (60, 38.5), (54, 39.5), (49.5, 38.5), (46.5, 39.2), (42.5, 38.6)]
GERMANIA_P = [(4.5, 53.6), (6.2, 51.9), (6.9, 51.2), (7.2, 50.7), (7.7, 50.3), (8.4, 50.0), (8.8, 50.3), (9.1, 49.9), (9.5, 49.2), (9.8, 48.95), (10.6, 49.05), (11.6, 48.95), (12.2, 49.05),
              (13.5, 48.6), (15, 48.6), (15, 55), (8, 55.5)]
VANDAL_AFR = [(5.0, 37.6), (11.6, 37.6), (11.6, 33.0), (9.4, 32.2), (7.0, 34.3), (5.0, 35.0)]
EGY_P = [(24.7, 22), (24.7, 31.9), (34.25, 31.35), (34.9, 29.5), (35.6, 22)]
BALEAR_P = [(1.0, 38.5), (1.0, 40.2), (4.5, 40.2), (4.5, 38.5)]
# modern Romance-speaking countries for the last map
FRANCE_P = [(-1.75, 43.35), (-0.7, 42.9), (0.7, 42.75), (1.7, 42.5), (3.2, 42.43), (4, 42.4), (7.4, 43.2), (7.5, 43.75), (6.9, 44.3), (6.9, 45.1), (7.0, 45.9), (6.1, 46.3), (6.9, 47.4),
            (7.6, 47.6), (8.2, 49.0), (6.4, 49.5), (5.8, 49.6), (4.2, 50.0), (2.6, 51.1), (1.5, 50.9), (0.3, 50.3), (-1.5, 49.95), (-3, 49.5), (-6, 49.0), (-6, 47), (-2.2, 44)]
ITALY_P = [(7.5, 43.75), (6.9, 44.3), (6.9, 45.1), (7.0, 45.9), (7.9, 46.0), (8.5, 46.4), (9.4, 46.4), (10.4, 46.6), (11.4, 47.0), (12.3, 46.8), (13.6, 46.5), (13.75, 45.6), (13.2, 45.3),
           (13.4, 44.2), (14.6, 43.5), (16.7, 42.3), (18.3, 41.2), (19.0, 40.2), (18.9, 39.0), (17.5, 37.4), (15.6, 36.4), (11.8, 36.4), (11.8, 38.5), (9.95, 38.7), (8, 38.7), (8, 41.3),
           (9.9, 41.3), (9.9, 43.5), (8.5, 43.9)]
ROMANIA_P = [(20.3, 46.1), (21.2, 46.3), (22.9, 48.0), (26.6, 48.3), (28.2, 48.2), (30.1, 46.4), (28.2, 45.45), (29.7, 45.2), (28.6, 43.75), (27.0, 44.1), (25.4, 43.65), (22.7, 44.2),
             (22.4, 44.7), (21.4, 44.85), (20.3, 45.3)]
LATAM_P = [(-117.1, 32.5), (-114.8, 32.5), (-111, 31.3), (-108.2, 31.3), (-108.2, 31.8), (-106.5, 31.8), (-104.5, 29.6), (-103, 29), (-101.4, 29.8), (-99.5, 27.5), (-97.2, 25.9), (-90, 24),
           (-85.5, 22.5), (-84.5, 24.2), (-80, 23.6), (-74, 20.6), (-68, 20), (-64.6, 18.0), (-66, 17.2), (-70, 16.5), (-72, 13.5), (-62.5, 11.3), (-60.5, 9.4), (-50, 6), (-33, -4),
           (-36, -20), (-50, -36), (-62, -57), (-78, -52), (-73, -20), (-83, -5), (-80, 5), (-92, 13), (-106, 17), (-119, 28)]
GUIANAS_P = [(-60.0, 8.6), (-61.3, 6.0), (-61.4, 5.2), (-60.7, 5.2), (-60.1, 4.5), (-59.9, 2.3), (-59.0, 1.3), (-56.5, 1.9), (-54.0, 2.3), (-54.4, 4.0), (-54.0, 5.9), (-56, 6.2), (-58, 7.5)]
BELIZE_P = [(-89.25, 15.9), (-89.2, 17.85), (-88.9, 18.5), (-87.6, 18.5), (-87.6, 15.9)]
JAMAICA_P = [(-78.5, 17.6), (-78.5, 18.6), (-76.1, 18.6), (-76.1, 17.6)]

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
BRIT = M(BRIT_P); CONT = M(CONT_P, False); DACIA = M(DACIA_P); EMP117 = U(BRIT, CONT, DACIA)
EASTX = M(EASTX_P); MAURET = I(CONT, MAURET_P)
EMPH = Dm(EMP117, EASTX)                                   # after Hadrian
EMP14 = Dm(CONT, EASTX, MAURET, M(ARABIA_P))        # Augustus (client kingdoms of Thrace and Cappadocia shown inside)
EMP3 = Dm(U(BRIT, CONT), EASTX)                                     # after Aurelian gave up Dacia
SICILY = M(SIC_P, False); SICW = I(SICILY, SICW_P); SARD = M(SARD_P, False); CORS = M(CORS_P, False)
PEN = Dm(M(PEN_P, False), SICILY); CISALP = Dm(M(CISALP_P), PEN); ITALY = U(PEN, CISALP)
HISP = M(HISP_P, False); HISP146 = I(HISP, HISP146_SEL); BARCID = I(HISP, BARCID_SEL)
NARBON = M(NARBON_P); GAUL = Dm(M(GAUL_P), NARBON); GREECE = M(GREECE_P); AFRICA = M(AFRICA_P)
CARTH = U(COAST(NAFR_COAST, 1.1), M(CARTH_HOME), SICW, SARD, COAST(SPAIN_COAST, 0.5))
CARTH218 = U(COAST(NAFR_COAST, 1.1), M(CARTH_HOME), BARCID)
ROME146 = U(ITALY, SICILY, SARD, CORS, HISP146, GREECE, AFRICA)
ETR = M(ETR_P); LAT = M(LAT_P); SAMN = M(SAM_P); EPIRUS = M(EPIRUS_P)
EAST395 = I(EMP3, EAST395_P); WEST395 = Dm(EMP3, EAST395)
GALLIC = U(BRIT, I(CONT, GALLIC_SEL), HISP); PALMYR = I(EMPH, PALM_SEL); CENTRAL = Dm(EMPH, GALLIC, PALMYR)
PARTHIA = M(PARTHIA_P); GERMANIA = M(GERMANIA_P)
VANDAL = U(I(CONT, VANDAL_AFR), SARD, CORS, M(BALEAR_P, False))
ROMANCE = U(HISP, M(FRANCE_P), M(ITALY_P), CORS, M(ROMANIA_P), Dm(M(LATAM_P), M(GUIANAS_P), M(BELIZE_P, False), M(JAMAICA_P, False)))

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
