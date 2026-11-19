# География, маски и помощники для карт «The Aztecs in 20 Minutes». Движок и стиль — из rome/maps (Look A + рельеф, Меркатор, 60 кадров/с).
# Отличия от современной карты (намеренно): озёра Долины Мехико около 1519 г. (Тескоко, Шалтокан, Сумпанго, Чалько, Сочимилько) и острова на них
# обведены по карте Wikimedia «Basin of Mexico 1519» (CC BY-SA), привязка по 20 городам (lakes.json, georef.py); плотина и дамбы — схема по той же карте.
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../rome/maps"))
import engine
import numpy as np
from PIL import Image, ImageDraw
# ---- lakes: cut the water out of the land, then put the islands back
_LK = json.load(open(os.path.join(HERE, "lakes.json")))
LAKE_RINGS = [np.asarray(o["ring"], float) for o in _LK if not o["hole"]]
ISLANDS = [np.asarray(o["ring"], float) for o in _LK if o["hole"]]
for _r in LAKE_RINGS: engine.HOLES.append(engine._chaikin(_r, 1))
_lm0 = engine.land_mask
def _land_mask(cam, res=None):
    m = _lm0(cam, res)
    if cam[2] > 250: engine._draw_polys(ImageDraw.Draw(m), cam, [engine._chaikin(r, 1) for r in ISLANDS], 255, minpx=1.0)
    return m
engine.land_mask = _land_mask
def _inside(p, poly):
    x, y = p; n = len(poly); c = False
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c
engine.RIVER_NAMES |= {"Río Balsas", "Rio Balsas", "Río Grande de Santiago", "Rio Grande de Santiago", "Río Papaloapan", "Río Grijalva", "Río Usumacinta", "Pánuco", "Panuco"}
engine.RIVERS = engine._rivers()
import ro_base
from ro_base import *
HERE = os.path.dirname(os.path.abspath(__file__))
ro_base.RANGES[:] = [
    ([(-109.0, 31.0), (-107.6, 28.6), (-106.2, 26.4), (-105.0, 24.5), (-104.0, 22.8), (-103.2, 21.4)], 1.3, 1.0),                        # Sierra Madre Occidental
    ([(-101.0, 27.8), (-100.2, 26.0), (-99.6, 24.2), (-99.2, 22.6), (-98.6, 20.8)], 0.9, 0.9),                                           # Sierra Madre Oriental
    ([(-105.0, 19.6), (-103.4, 19.5), (-102.0, 19.6), (-100.6, 19.4), (-99.6, 19.2), (-98.6, 19.15), (-97.4, 19.1), (-96.6, 19.0)], 0.75, 1.0),   # Trans-Mexican Volcanic Belt
    ([(-103.5, 18.2), (-101.8, 17.8), (-100.2, 17.4), (-98.4, 17.1), (-96.8, 16.9)], 0.8, 0.9),                                          # Sierra Madre del Sur
    ([(-94.0, 16.4), (-92.4, 16.0), (-91.2, 15.5), (-90.2, 15.2)], 0.7, 0.8),                                                            # Chiapas / Guatemala highlands
    ([(-98.75, 19.0), (-98.65, 19.6)], 0.22, 0.9), ([(-99.35, 19.1), (-99.15, 19.5)], 0.25, 0.8),                                         # Sierra Nevada, Sierra de las Cruces
    ([(-99.15, 19.7), (-99.0, 19.45)], 0.18, 0.7)]                                                                                       # Sierra de Guadalupe

# ---------------------------------------------------------------- relief and streams of the valley, taken from the Wikimedia map (same georeference)
from georef import CTRL, fit, to_ll
_px, _py = fit(CTRL)
def _src(pts): return [to_ll(_px, _py, x * 1.158, y * 1.158) for x, y in pts]       # pixel of the displayed map -> lon/lat
VALLEY_RANGES = [
    (_src([(500, 790), (590, 860), (640, 930), (625, 1000)]), 0.12, 1.0),                 # Sierra de Guadalupe
    (_src([(60, 2150), (150, 1960), (250, 1760), (330, 1590), (400, 1330)]), 0.16, 1.0),   # Sierra de las Cruces
    (_src([(60, 240), (130, 390), (210, 520)]), 0.14, 0.8),                                # hills west of Zumpango
    (_src([(1520, 1560), (1600, 1400), (1655, 1250), (1650, 1100)]), 0.2, 1.0),            # Sierra Nevada (east edge of the valley)
    (_src([(1230, 1450), (1300, 1620), (1250, 1760)]), 0.12, 0.8),                         # hills of Ixtapaluca
    (_src([(640, 1860), (770, 1810), (900, 1780)]), 0.08, 0.7),                            # Star's Hill and the Iztapalapa peninsula
    (_src([(1250, 470), (1400, 590), (1500, 700)]), 0.1, 0.6),                             # hills near Teotihuacan
    (_src([(600, 2150), (900, 2100), (1250, 2150)]), 0.15, 0.8)]                           # south wall of the valley (Chichinautzin)
ro_base.RANGES.extend(VALLEY_RANGES)
VALLEY_RIVERS = [np.asarray(r, float) for r in json.load(open(os.path.join(HERE, "rivers.json")))]       # streams of the valley: drawn only in valley scenes (the source map is cut at its frame)
ro_base.DESERTS[:] = [[(-114.8, 32.6), (-108.5, 31.8), (-104.2, 31.0), (-101.6, 29.4), (-101.4, 27.0), (-103.0, 25.4), (-105.4, 25.3), (-107.6, 28.0), (-110.5, 30.2), (-113.0, 31.4)]]

# ---------------------------------------------------------------- colours
AZ = (176, 70, 48); AZ_L = (222, 170, 150); AZ_D = (110, 38, 28)         # the Mexica: dark brick red
ACO = (86, 128, 150); TEP = (122, 96, 150); TLX = (60, 132, 122); TAR = (190, 142, 60); MIX = (110, 100, 90); MAY = (86, 128, 84)
TRI_T = (176, 70, 48); TRI_X = (70, 110, 150); TRI_P = (150, 110, 70); ENM = (110, 100, 90); SPA = (60, 60, 60); GRN = (104, 150, 84)
LKC = (150, 214, 236)
PAPER = (250, 247, 240); BLACK = (17, 17, 17)

# ---------------------------------------------------------------- places (lon, lat); town centres, the places are not displaced against modern coordinates
C = ro_base.C; C.clear()
C.update(TENOCHTITLAN=(-99.1316, 19.4350), TLATELOLCO=(-99.135, 19.452), TEXCOCO=(-98.882, 19.512), TLACOPAN=(-99.189, 19.459), AZCAPOTZALCO=(-99.186, 19.487),
         CULHUACAN=(-99.110, 19.336), CHAPULTEPEC=(-99.182, 19.420), COYOACAN=(-99.162, 19.350), XOCHIMILCO=(-99.104, 19.257), CHALCO=(-98.897, 19.264),
         IZTAPALAPA=(-99.056, 19.357), TEPEYAC=(-99.118, 19.485), CUAUTITLAN=(-99.178, 19.671), TEOTIHUACAN=(-98.844, 19.692), TENAYUCA=(-99.170, 19.528),
         XALTOCAN=(-99.0, 19.72), MIXCOAC=(-99.187, 19.375), HUEXOTLA=(-98.885, 19.481), COATLINCHAN=(-98.89, 19.44), ECATEPEC=(-99.061, 19.601), IXTAPALUCA=(-98.883, 19.319),
         TLAXCALA=(-98.240, 19.314), CHOLULA=(-98.301, 19.063), VERACRUZ=(-96.134, 19.174), HAVANA=(-82.367, 23.114), COZUMEL=(-86.92, 20.42), CEMPOALA=(-96.407, 19.447),
         TZINTZUNTZAN=(-101.58, 19.63), OAXACA=(-96.72, 17.06), TAPACHULA=(-92.26, 14.90), TABASCO=(-92.70, 18.40), CUERNAVACA=(-99.23, 18.92), TOLLAN=(-99.34, 20.06),
         TEOTITLAN=(-97.08, 18.13), COIXTLAHUACA=(-97.33, 17.69), TOCHTEPEC=(-96.12, 18.10), HUEXOTZINCO=(-98.42, 19.03), ATLIXCO=(-98.43, 18.91), CAMPECHE=(-90.53, 19.85),
         TENOCH_ISL=(-99.13, 19.43), STARHILL=(-99.06, 19.33), CHAPULT=(-99.182, 19.420), TLAHUAC=(-99.01, 19.27), ZUMPANGO=(-99.10, 19.80), TEXMELUCAN=(-98.43, 19.28))
# the lake system: dike of Nezahualcoyotl (pixel path on the source map -> lon/lat) and the three causeways (schematic)
DIKE = [to_ll(_px, _py, x * 1.158, y * 1.158) for x, y in [(655, 1140), (661, 1230), (662, 1290), (668, 1330), (655, 1360), (660, 1440), (675, 1500), (678, 1531)]]
CW_TEPEYAC = [C["TENOCHTITLAN"], (-99.134, 19.4435), C["TLATELOLCO"], (-99.127, 19.468), C["TEPEYAC"]]
CW_TLACOPAN = [C["TENOCHTITLAN"], (-99.150, 19.4430), (-99.170, 19.4515), C["TLACOPAN"]]
CW_IZTAP = [C["TENOCHTITLAN"], (-99.1315, 19.405), (-99.120, 19.378), (-99.095, 19.360), C["IZTAPALAPA"]]
CW_COYO = [(-99.1265, 19.372), (-99.14, 19.362), C["COYOACAN"]]
CW_TLAHUAC = [(-99.04, 19.285), (-99.015, 19.27), (-98.99, 19.252)]
AQUEDUCT = [C["CHAPULTEPEC"], (-99.172, 19.425), (-99.158, 19.4325), (-99.139, 19.4345)]
# the Triple Alliance / empire polygons are drawn in az_scenes.py (schematic borders, provinces by the voiceover)

# ---------------------------------------------------------------- voiceover cues
_ROWS = json.load(open(os.path.join(HERE, "../timing.json")))
def cue(ch, phrase, frac=None):
    for r in _ROWS[str(ch)]["rows"]:
        if r["text"].lower().startswith(phrase.lower()): return r["start"] + ((r["end"] - r["start"]) * frac if frac else 0.0)
    raise KeyError((ch, phrase))
def word(ch, phrase, w):
    """second at which word `w` is spoken inside the sentence starting with `phrase` (linear inside the sentence, as in the layout)"""
    for r in _ROWS[str(ch)]["rows"]:
        if r["text"].lower().startswith(phrase.lower()):
            i = r["text"].lower().index(w.lower()); return r["start"] + (r["end"] - r["start"]) * i / max(1, len(r["text"]))
    raise KeyError((ch, phrase))
def along(path, q):
    """lon/lat point at fraction q of a lon/lat path"""
    return tuple(partial(np.asarray(path, float), max(0.0, min(1.0, q)))[-1])

# ---------------------------------------------------------------- stronger relief than the Rome look (the Basin of Mexico map is the model for detail)
import inspect, textwrap
_src_bi = textwrap.dedent(inspect.getsource(ro_base.base_image))
_src_bi = _src_bi.replace("a * (1 - 0.30 * R) + np.array(MOUNT, np.float32) * (0.30 * R)", "a * (1 - RK * R) + np.array(MOUNT, np.float32) * (RK * R)").replace("(1 + 0.16 * SH", "(1 + SK * SH").replace("* 9.0, -1, 1)", "* 14.0, -1, 1)")
RK, SK = 0.62, 0.42
_ns = dict(ro_base.__dict__); _ns.update(RK=RK, SK=SK)
exec(_src_bi, _ns); engine.base_image = _ns["base_image"]; ro_base.base_image = _ns["base_image"]
_FR = (-99.337, -98.731, 19.155, 19.844)          # frame of the source map (lon0, lon1, lat0, lat1)
def valley_rivers(fr, a=1.0, width=2.6, color=(74, 128, 156), frac=1.0, fade=0.05):
    """streams of the valley; the source map ends at its frame, so every stream fades out toward it"""
    for arr in VALLEY_RIVERS:
        p = proj(fr.cam, arr, 1)
        if p[:, 0].max() < 0 or p[:, 0].min() > W or p[:, 1].max() < 0 or p[:, 1].min() > H: continue
        n = len(arr); k = max(1, int(n * frac))
        for i in range(0, k - 1, 3):
            q = arr[i:min(i + 4, k)]; m = q.mean(0)
            d = min(m[0] - _FR[0], _FR[1] - m[0], m[1] - _FR[2], _FR[3] - m[1]); f = max(0.0, min(1.0, d / fade))
            if f > 0: pline(fr, proj(fr.cam, q, 1), color=color, width=width, a=a * f)

# ---------------------------------------------------------------- empire and neighbours (schematic, borders "very approximate" even in the sources: Barlow 1949 / Berdan 1996)
# Triple Alliance tribute provinces about 1502-1519; coast and sea are cut by the land mask, so the polygon may run out into the water.
# Not conquered: Tlaxcala, Huexotzinco, the Tarascan state (Taximaroa = Ciudad Hidalgo was the frontier), the Mixtec coast (Tututepec, Yopes).
EMP_P = [(-100.2, 20.75), (-99.5, 21.6), (-98.9, 22.4), (-97.5, 22.4), (-96.0, 22.5), (-91.5, 20.5), (-91.5, 18.0), (-92.8, 17.3), (-92.7, 16.0), (-91.6, 14.9), (-91.0, 13.8),
         (-95.0, 13.8), (-99.0, 15.5), (-101.9, 16.6), (-101.8, 17.9), (-100.9, 18.3), (-100.55, 19.2), (-100.45, 19.9)]
TLX_P = [(-98.47, 19.5), (-98.22, 19.6), (-97.96, 19.5), (-97.92, 19.3), (-98.06, 19.16), (-98.36, 19.18), (-98.5, 19.3)]
HUEX_P = [(-98.6, 19.15), (-98.35, 19.2), (-98.25, 18.95), (-98.5, 18.85)]
TUT_P = [(-99.3, 15.8), (-99.3, 17.0), (-97.0, 17.0), (-96.4, 15.8)]
TAR_P = [(-103.3, 19.9), (-102.2, 20.45), (-101.0, 20.3), (-100.55, 19.9), (-100.5, 19.0), (-100.9, 18.3), (-101.8, 17.8), (-102.6, 18.0), (-103.4, 18.7)]
EMP = Dm(M(EMP_P), M(TLX_P), M(HUEX_P), M(TUT_P), M(TAR_P))
TLXM = M(TLX_P); TARM = M(TAR_P); HUEXM = M(HUEX_P)
DRY_C = (206, 194, 150)           # dry lake bed
TAXIMAROA = (-100.57, 19.69)
# ---------------------------------------------------------------- the city plan (schematic): the island of Tenochtitlan and Tlatelolco, canals, the Great Temple precinct, the palace
def _isl(c, w, h, ang=17.0, seed=3, n=9, jit=0.07):
    """a slightly irregular quadrilateral island (km -> lon/lat), turned to the temple axis"""
    rng = np.random.RandomState(seed); a = math.radians(ang); pts = []
    cs = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    for k in range(4):
        (x0, y0), (x1, y1) = cs[k], cs[(k + 1) % 4]
        for q in range(n):
            f = q / n; x = x0 + (x1 - x0) * f; y = y0 + (y1 - y0) * f
            if q: x += rng.uniform(-jit, jit); y += rng.uniform(-jit, jit)
            xr = x * math.cos(a) + y * math.sin(a); yr = -x * math.sin(a) + y * math.cos(a)
            pts.append((c[0] + xr / 104.9, c[1] + yr / 111.0))
    return pts
TEN_P = _isl((-99.1315, 19.4285), 3.3, 3.1, seed=3)
TLA_P = _isl((-99.1352, 19.4535), 1.7, 1.5, seed=5)
TEMPLE = C["TENOCHTITLAN"]; PALACE = (-99.1285, 19.4328); MARKET = (-99.1352, 19.4515); SKULLS = (-99.1330, 19.4364)
CAN = (150, 214, 236); ISLAND_C = (236, 226, 192); ISLAND_E = (150, 128, 90)
