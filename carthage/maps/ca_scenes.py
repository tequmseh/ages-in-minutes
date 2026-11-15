from ca_base import *

def sc(name, dur, cam, masks=None, active=None, rivers=True):
    return scene(name, dur, cam, masks or {}, res="10", active=active, rivers=rivers)
def lerp(a, b, p): return (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)
def keyed(t, keys):
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t0: return v0
        if t < t1: return v0 + (v1 - v0) * (t - t0) / (t1 - t0)
    return keys[-1][1]
def garrow(fr, path, frac=1.0, a=1.0, width=4.5):
    gline(fr, path, color=INK, width=width, frac=frac, a=a, arrow=True)
def frac_at(path, lon, lat):
    p = np.asarray(path) * np.array([engine.K, 1.0]); L = path_len(p)
    i = int(np.argmin(np.hypot(p[:, 0] - lon * engine.K, p[:, 1] - lat))); return L[i] / L[-1]
def dim(fr, a, b, txt, a_=1.0, off=(0, -34), size=24):
    if a_ <= 0: return
    x0, y0 = P(fr.cam, *a); x1, y1 = P(fr.cam, *b)
    pline(fr, [(x0, y0), (x1, y1)], width=2.5, a=a_)
    v = np.array([x1 - x0, y1 - y0]); v = v / np.hypot(*v); o = np.array([-v[1], v[0]]) * 9
    for x, y in ((x0, y0), (x1, y1)): pline(fr, [(x - o[0], y - o[1]), (x + o[0], y + o[1])], width=2.5, a=a_)
    fr.plaque((x0 + x1) / 2 + off[0], (y0 + y1) / 2 + off[1], txt, size=size, a=a_, pad=(12, 8))

WEST = cam_box(-10, 19, 31, 45.5)
MED = cam_box(-9.5, 37.5, 29.5, 46)
LEB = cam_box(33.8, 37.2, 32.6, 34.9)
TUN = cam_box(9.3, 11.4, 36.4, 37.35)
WAIST = cam_box(6, 17, 34.5, 39.5)
EAST = cam_box(24, 46, 28.5, 39)
NET = cam_box(-11, 17, 31, 44)
ATL = cam_box(-44, 60, 12, 52.5)
SICC = cam_box(11.6, 16.2, 36.3, 38.75)
STRAIT = cam_box(14.9, 16.3, 37.75, 38.55)
AFR = cam_box(8.6, 11.8, 36.0, 37.6)
SARD = cam_box(5.5, 16.5, 35.5, 43.5)
SPAF = cam_box(-8, 12, 34, 41.5)
SPAINC = cam_box(-9.8, 4.5, 35.6, 43.9)
W9 = cam_box(-6.5, 19, 36, 47.3)
ITA9 = cam_box(2.2, 18.8, 39.8, 46.6)
W10 = cam_box(-9.5, 19, 34, 46.5)
AFRW = cam_box(5.5, 12.5, 34.3, 38.0)

# ================= 0a. Cold open, the encirclement: 2 s (VO 0:11-0:13)
@sc("00a_cold_open", 2, WEST, active=[(0, 2)])
def _(fr, t):
    blank(fr, LAND)
    cx, cy, hw, hh = 960, 450, 300, 120
    poly(fr, [(cx - hw, cy - hh), (cx + hw, cy - hh), (cx + hw, cy + hh), (cx - hw, cy + hh)], ROME)
    T(fr, cx, cy, "ROME", size=54, sp=22, anchor="m", w="b", color=WHITE)
    # the ring: starts as a line under the Roman block, both ends run round the flanks and meet behind it
    g = 62; x0, x1, y0, y1 = cx - hw - g, cx + hw + g, cy - hh - g, cy + hh + g
    half = [(cx, y1), (x1, y1), (x1, y0), (cx, y0)]
    k = 0.30 + 0.70 * ease(t / 1.45)
    for sg in (1, -1):
        pts = [(cx + sg * (x - cx), y) for x, y in half]
        pline(fr, pts, color=PURPLE, width=40, frac=k)
    T(fr, cx, y1 + 74, "HANNIBAL", size=40, sp=16, anchor="m", w="b", color=PURPLE_D)

# ================= 0b. Cold open, one dot on the sea: 7 s (VO 0:37-0:44)
@sc("00b_cold_open", 7, WEST, active=[(0.3, 3.2)])
def _(fr, t):
    a = fr.r(0.2, 0.5)
    if 0.3 <= t <= 3.2: fr.pulse(*C["CARTHAGE"], t, 0.3, color=PURPLE, n=2, rmax=54, width=3.5)
    carthage(fr, a, r=11, side="t", size=30)
    x, y = P(fr.cam, *C["CARTHAGE"])
    fr.plaque(x, y + 62, "MORE THAN 600 YEARS", size=28, a=fr.r(0.9, 0.5))

# ================= 1a. The Purple People, the coast: 20 s (VO 0:00-0:20)
STRIP_P = [(34.8, 34.75), (36.6, 34.75), (36.2, 32.95), (34.8, 32.95)]
LEBR = [(35.50, 33.18), (35.68, 33.55), (35.88, 33.95), (36.10, 34.32), (36.30, 34.62)]
@sc("01a_the_purple_people", 20, LEB, dict(strip=COAST(STRIP_P, 0.17)))
def _(fr, t):
    fr.fill(fr.masks["strip"], PURPLE_L, fr.r(0.3, 1.2))
    modern(fr, 36.62, 33.9, "NOW LEBANON", a=fr.r(1.6, 0.6), size=24)
    mounts(fr, LEBR, a=fr.r(3.0, 0.7), rows=2, step=34, size=12, gap=20)
    TL(fr, 36.02, 33.5, "MOUNTAINS", size=22, sp=5, a=fr.r(3.4, 0.5), color=SAND_D, w="b")
    for i, n in enumerate(["TYRE", "SIDON", "BYBLOS"]):
        a = fr.r(10.0 + i * 1.0, 0.4); pdot(fr, n, a, r=9)
        x, y = P(fr.cam, *C[n]); T(fr, x - 22, y, n, size=30, anchor="r", a=a, w="b")
    fr.plaque(520, 170, "PHOENICIANS", size=34, a=fr.r(16.6, 0.5))

# ================= 1b. The Purple People, the route west: 30 s (VO 1:05-1:35)
ROUTE = smooth([(35.2, 33.27), (33.5, 32.6), (31, 32.3), (27.5, 32.2), (24.5, 32.7), (22, 33.25), (19.9, 31.9), (18, 31.1), (16, 31.7), (14.6, 32.85),
                (12.5, 33.25), (11.5, 34.2), (11.35, 35.6), (11.4, 36.7), (11.2, 37.3), (10.5, 37.5), (9.6, 37.6), (7.8, 37.2), (5.5, 37.15), (3.1, 37.05),
                (0.5, 36.4), (-2.2, 35.75), (-4.2, 35.6), (-5.5, 35.95), (-6.3, 36.45)], 10)
STOPS = ["LEPTIS", "SABRATHA", "HADRUMETUM", "CARTHAGE", "UTICA", "HIPPO", "ICOSIUM", "RUSADDIR", "LIXUS", "MALACA", "GADES"]
_c1, _a1 = mover([(0, LEB), (0.4, LEB), (3.6, MED), (30, MED)])
@sc("01b_the_purple_people", 30, _c1, dict(strip=COAST(STRIP_P, 0.17)), active=_a1 + [(27, 30)])
def _(fr, t):
    fr.fill(fr.masks["strip"], PURPLE_L)
    near = 1 - fr.r(0.4, 1.2); far = fr.r(2.6, 1.0)
    for n in ["TYRE", "SIDON", "BYBLOS"]:
        pdot(fr, n, near, r=9); x, y = P(fr.cam, *C[n]); T(fr, x - 22, y, n, size=30, anchor="r", a=near, w="b")
    for n in ["TYRE", "SIDON", "BYBLOS"]: pdot(fr, n, far, r=5)
    TL(fr, 35.0, 34.95, "PHOENICIANS", size=18, sp=3, anchor="r", a=far, w="b", color=PURPLE_D)
    gline(fr, ROUTE, color=PURPLE, width=4 + 1.5 * fr.r(25.0, 1.0), frac=fr.r(2.8, 3.4), arrow=True)
    region(fr, -3.6, 39.9, "SPAIN", a=fr.r(5.0, 0.5), size=30, sp=10, w="b")
    fr.plaque(P(fr.cam, -3.6, 39.9)[0], P(fr.cam, -3.6, 39.9)[1] + 56, "SILVER  ·  TIN", size=24, a=fr.r(5.5, 0.5), pad=(13, 8))
    for i, n in enumerate(STOPS): pdot(fr, n, fr.r(9.0 + 0.35 * i, 0.3), r=6)
    pa = fr.r(17.0, 0.6) * (1 - fr.r(22.5, 0.8))
    gline(fr, [(35.9, 33.5), (38.3, 34.1)], color=SLATE, width=4.5, a=pa, arrow=True)
    TL(fr, 36.4, 35.0, "TO PERSIA", size=17, sp=3, anchor="m", a=pa, color=(70, 82, 90), w="b")
    fr.plaque(960, 120, "NOT AN EMPIRE. A ROUTE.", size=30, a=fr.r(24.6, 0.5))
    h = fr.r(27.0, 0.6)
    if 27 <= t <= 30: fr.pulse(*C["CARTHAGE"], t, 27.0, color=PURPLE, n=2, rmax=44, width=3.5)
    pdot(fr, "CARTHAGE", h, r=11)

# ================= 2a. New City, the hill and the oxhide: 20 s (VO 0:15-0:35)
LAND_IN = smooth([(14.6, 36.0), (12.6, 36.75), (11.5, 37.3), (10.85, 37.3), (10.5, 37.05), (10.37, 36.9)], 10)
_c2, _a2 = mover([(0, WAIST), (0.3, WAIST), (3.3, TUN), (20, TUN)])
@sc("02a_new_city", 20, _c2, active=_a2)
def _(fr, t):
    region(fr, 9.75, 36.62, "NORTH AFRICA", a=fr.r(0.3, 0.5), size=26, sp=9, color=SAND_D, w="b")
    gline(fr, LAND_IN, color=PURPLE, width=4.5, frac=fr.r(0.3, 3.0), arrow=True)
    x, y = P(fr.cam, *C["CARTHAGE"]); h = fr.r(3.3, 0.5)
    circ(fr, x, y, 30, (226, 204, 160), h)
    pline(fr, [(x - 17, y + 9), (x - 3, y - 11), (x + 4, y - 1), (x + 9, y - 8), (x + 19, y + 9)], color=SAND_D, width=3.5, a=h)
    ring(fr, *C["CARTHAGE"], 47, color=PURPLE_D, width=3, frac=fr.r(4.0, 9.6))
    T(fr, x + 68, y - 14, "ONE OXHIDE,", size=21, sp=2.5, a=fr.r(9.4, 0.5), w="b")
    T(fr, x + 68, y + 14, "CUT INTO STRIPS", size=21, sp=2.5, a=fr.r(9.9, 0.5), w="b")
    fr.plaque(x + 200, y + 86, "DIDO'S PROBLEM", size=28, a=fr.r(17.6, 0.5))

# ================= 2b. New City, the narrow waist: 16 s (VO 1:17-1:33)
EB = smooth([(6.9, 38.3), (9.6, 37.95), (11.55, 37.33), (13.4, 36.2), (16.3, 35.5)], 10)
WB = smooth([(16.6, 36.0), (13.7, 36.65), (11.9, 37.62), (9.8, 38.3), (7.0, 38.75)], 10)
@sc("02b_new_city", 16, WAIST, active=[(14, 16)])
def _(fr, t):
    region(fr, 7.4, 35.95, "AFRICA", a=fr.r(3.6, 0.5), size=32, sp=14, color=SAND_D, w="b")
    modern(fr, 9.35, 35.35, "NOW TUNISIA", a=fr.r(2.2, 0.5), size=19)
    region(fr, 14.25, 37.55, "SICILY", a=fr.r(4.6, 0.5), size=28, sp=9, w="b")
    gline(fr, EB, color=SEA_D, width=4.5, frac=fr.r(8.3, 1.8), arrow=True)
    gline(fr, WB, color=SEA_D, width=4.5, frac=fr.r(9.6, 1.8), arrow=True)
    dim(fr, (11.09, 37.10), (12.40, 37.74), "145 KM", fr.r(6.0, 0.6), off=(-52, -44))
    if 14 <= t <= 16: fr.pulse(*C["CARTHAGE"], t, 14.0, color=PURPLE, n=2, rmax=50, width=3.5)
    x, y = P(fr.cam, *C["CARTHAGE"])
    carthage(fr, fr.r(0.2, 0.5), r=11, label="", size=26)
    T(fr, x - 24, y - 4, "QART-HADASHT", size=27, anchor="r", a=fr.r(0.2, 0.5), w="b")
    T(fr, x - 24, y + 25, "NEW CITY", size=17, anchor="r", sp=3, a=fr.r(0.6, 0.5), color=PURPLE_D, w="b")
    fr.plaque(x - 118, y + 78, "THE TOLLBOOTH", size=26, a=fr.r(14.0, 0.5), pad=(13, 8))

# ================= 3. The Trading Empire: 97 s (VO 0:00-1:37, still 0:55-1:08)
ASSY = smooth([(43.0, 36.5), (39.6, 35.7), (36.9, 34.5), (35.75, 33.75)], 10)
BABY = smooth([(44.3, 32.6), (40.6, 33.25), (36.25, 33.32)], 10)
PERS = smooth([(48.6, 30.5), (43.0, 30.5), (38.6, 31.5), (35.8, 32.85)], 10)
L_SIC = smooth([(10.4, 36.95), (10.75, 37.3), (11.6, 37.6), (12.42, 37.86)], 8)
L_SAR = smooth([(10.4, 36.95), (10.6, 37.4), (9.9, 38.2), (9.05, 38.93)], 8)
L_IBI = smooth([(10.4, 36.95), (10.55, 37.45), (9.4, 37.95), (6.0, 38.35), (1.5, 38.88)], 8)
L_SPA = smooth([(1.4, 38.85), (-0.3, 37.3), (-2.0, 36.45), (-4.4, 36.62), (-5.5, 35.98), (-6.3, 36.5)], 8)
L_MOR = smooth([(-5.6, 35.95), (-6.45, 35.25), (-7.7, 34.1), (-9.3, 32.9), (-10.0, 31.6)], 8)
HANNO = smooth([(-5.5, 35.95), (-6.7, 35.2), (-8.6, 33.6), (-10.3, 31.0), (-10.7, 29.2), (-13.5, 27.2), (-15.7, 24.6), (-17.5, 21.2), (-16.9, 18.5),
                (-17.5, 15.6), (-18.0, 14.5), (-17.4, 12.6), (-16.2, 11.2)], 10)
HIMIL = smooth([(-6.4, 36.5), (-9.4, 36.9), (-10.0, 39.5), (-9.9, 42.6), (-8.7, 44.2), (-6.2, 46.6), (-5.6, 48.6), (-5.4, 49.9)], 10)
TREATY = smooth([(10.35, 37.3), (10.25, 38.2), (9.85, 39.05)], 10)
_c3, _a3 = mover([(0, EAST), (11, EAST), (14.5, NET), (44, NET), (47, ATL), (74.5, ATL), (77.5, NET), (97, NET)])
@sc("03_the_trading_empire", 97, _c3, active=_a3 + [(94, 97)])
def _(fr, t):
    # Tyre squeezed from the east
    fade = fr.r(8.6, 2.0); east = 1 - fr.r(13.4, 1.0)
    for path, lab, pos, t0, anc in ((ASSY, "ASSYRIANS", (43.2, 37.0), 3.0, "m"), (BABY, "BABYLONIANS", (44.5, 33.2), 5.2, "l"), (PERS, "PERSIANS", (45.6, 29.75), 7.4, "m")):
        gline(fr, path, color=SLATE, width=5, frac=fr.r(t0, 1.4), arrow=True, a=east)
        TL(fr, *pos, lab, size=21, sp=4, anchor=anc, a=fr.r(t0, 0.5) * east, w="b", color=(60, 72, 80))
    city(fr, "TYRE", a=fr.r(0.2, 0.5) * east, side="l", r=9, size=28, ring=WHITE, dot=mix(GRAY, PURPLE, fade), color=mix(GRAY, INK, fade))
    # the network
    net = fr.r(14.4, 0.6); nl = max(0.0, min(1.0, 1 - fr.r(44.0, 1.0) + fr.r(76.6, 1.0)))
    gone = 1 - fr.r(43.4, 0.5)
    date(fr, "500 BC", fr.r(15.0, 0.5) * gone)
    for path, t0 in ((L_SIC, 19.0), (L_SAR, 20.4), (L_IBI, 21.6), (L_SPA, 22.8), (L_MOR, 24.6)):
        gline(fr, path, color=PURPLE, width=3, frac=fr.r(t0, 1.0))
    for n, t0 in (("MOTYA", 19.6), ("PANORMUS", 19.8), ("NORA", 21.0), ("THARROS", 21.2), ("IBIZA", 22.4), ("MALACA", 23.4), ("GADES", 23.8), ("LIXUS", 25.2), ("MOGADOR", 25.5)):
        pdot(fr, n, fr.r(t0, 0.3), r=6)
    TL(fr, 12.55, 37.28, "WESTERN SICILY", size=18, sp=2.5, anchor="l", a=fr.r(19.0, 0.5) * nl, w="b")
    TL(fr, 8.0, 40.25, "SARDINIA", size=18, sp=2.5, anchor="r", a=fr.r(20.4, 0.5) * nl, w="b")
    TL(fr, 1.45, 39.55, "IBIZA", size=18, sp=2.5, anchor="m", a=fr.r(21.6, 0.5) * nl, w="b")
    region(fr, -3.6, 39.9, "SPAIN", a=fr.r(22.8, 0.5) * nl, size=26, sp=9, w="b")
    TL(fr, -3.6, 38.0, "SILVER", size=17, sp=4, anchor="m", a=fr.r(23.6, 0.5) * nl, w="b", color=(90, 90, 90))
    modern(fr, -4.3, 33.4, "NOW MOROCCO", a=fr.r(24.6, 0.5) * nl, size=18)
    fr.plaque(960, 112, "HARBOURS, NOT PROVINCES", size=30, a=fr.r(28.0, 0.5) * gone)
    sunk = fr.r(40.4, 0.4) * gone
    if sunk > 0:
        x, y = P(fr.cam, 5.4, 40.7); boat(fr, x, y, 0.5, (95, 105, 112), sunk, k=1.5); cross(fr, 5.4, 40.7, a=sunk, r=13, width=4.5)
    # Hanno and Himilco
    gline(fr, HANNO, color=PURPLE_D, width=3.5, frac=fr.r(47.2, 6.2), arrow=True, dash=(13, 8), a=1 - fr.r(74.6, 0.8))
    TL(fr, -20.5, 22.0, "HANNO", size=22, sp=4, anchor="r", a=fr.r(48.6, 0.5) * (1 - fr.r(74.6, 0.8)), w="b", color=PURPLE_D)
    region(fr, -5.0, 19.5, "WEST AFRICA", a=fr.r(50.0, 0.6) * (1 - fr.r(74.6, 0.8)), size=22, sp=8, color=SAND_D, w="b")
    gline(fr, HIMIL, color=PURPLE_D, width=3.5, frac=fr.r(68.6, 3.2), arrow=True, dash=(13, 8), a=1 - fr.r(74.6, 0.8))
    TL(fr, -13.0, 42.5, "HIMILCO", size=22, sp=4, anchor="r", a=fr.r(69.0, 0.5) * (1 - fr.r(74.6, 0.8)), w="b", color=PURPLE_D)
    region(fr, -1.6, 52.7, "BRITAIN", a=fr.r(70.6, 0.5) * (1 - fr.r(74.6, 0.8)), size=22, sp=7, w="b")
    fr.plaque(P(fr.cam, -5.4, 50.2)[0] - 78, P(fr.cam, -5.4, 50.2)[1] + 2, "TIN", size=22, a=fr.r(71.4, 0.5) * (1 - fr.r(74.6, 0.8)), pad=(11, 7))
    # the first treaty with Rome
    date(fr, "509 BC", fr.r(81.0, 0.5))
    ra = fr.r(83.0, 0.5)
    city(fr, "ROME", a=ra, side="r", r=5, size=18, label="", dot=ROME_D, ring=WHITE)
    x, y = P(fr.cam, *C["ROME"]); T(fr, x + 15, y - 2, "ROME", size=18, a=fr.r(87.4, 0.5), color=ROME_D, w="b")
    gline(fr, TREATY, color=PURPLE_D, width=4, frac=fr.r(88.6, 1.4), dash=(10, 7))
    TL(fr, 5.3, 39.7, "NO ROMAN SHIPS", size=19, sp=3, anchor="m", a=fr.r(89.6, 0.5), w="b", color=PURPLE_D)
    if 94 <= t <= 97: fr.pulse(*C["CARTHAGE"], t, 94.0, color=PURPLE, n=2, rmax=46, width=3.5)
    x, y = P(fr.cam, *C["CARTHAGE"])
    carthage(fr, net, r=10, label="")
    T(fr, x - 6, y + 34, "CARTHAGE", size=24, anchor="m", a=net * nl, w="b")

# ================= 4a. The Sicilian Wars, Himera: 25 s (VO 0:00-0:25)
BACK = smooth([(12.5, 37.95), (12.95, 38.3), (13.5, 38.3), (13.8, 38.03)], 10)
@sc("04a_the_sicilian_wars", 25, SICC, dict(sw=SICW, se=SICE))
def _(fr, t):
    fr.fill(fr.masks["sw"], PURPLE, fr.r(1.8, 1.0)); fr.fill(fr.masks["se"], GREEK, fr.r(4.0, 1.0))
    region(fr, 13.3, 38.62, "SICILY", a=fr.r(0.2, 0.5), size=34, sp=14, w="b")
    TL(fr, 12.83, 37.86, "CARTHAGINIAN", size=17, sp=3, anchor="m", a=fr.r(2.2, 0.6), color=WHITE, w="b")
    TL(fr, 14.45, 37.62, "GREEK", size=22, sp=8, anchor="m", a=fr.r(4.4, 0.6), w="b")
    sy = fr.r(6.6, 0.4); gdot(fr, "SYRACUSE", sy, r=9)
    x, y = P(fr.cam, *C["SYRACUSE"]); T(fr, x + 20, y, "SYRACUSE", size=28, a=sy, w="b")
    him = fr.r(9.6, 0.4) * (1 - fr.r(23.0, 0.9)); gdot(fr, "HIMERA", him, r=8)
    x, y = P(fr.cam, *C["HIMERA"]); T(fr, x + 4, y - 30, "HIMERA", size=24, anchor="m", a=him, w="b")
    date(fr, "480 BC", fr.r(11.0, 0.5) * (1 - fr.r(20.6, 0.5)))
    mv = fr.r(11.3, 1.5); pos = lerp(C["PANORMUS"], (13.72, 37.93), mv)
    block(fr, *pos, PURPLE_D, a=fr.r(11.0, 0.4) * (1 - fr.r(13.8, 0.7)), w=38, h=19)
    cross(fr, 13.72, 37.9, a=fr.r(13.2, 0.4) * (1 - fr.r(20.6, 0.6)), r=13, width=5)
    sa = fr.r(16.2, 0.5) * (1 - fr.r(20.3, 0.5))
    T(fr, 1850, 142, "THE SAME DAY: SALAMIS", size=21, sp=3, anchor="r", a=sa, w="b")
    pline(fr, [(1560, 180), (1850, 180)], width=4, a=sa, arrow=True)
    gline(fr, BACK, color=PURPLE_D, width=5, frac=fr.r(21.2, 1.7), arrow=True)

# ================= 4b. The Sicilian Wars, Agathocles: 30 s (VO 0:55-1:25)
AGA = smooth([(15.36, 37.0), (15.35, 36.55), (14.3, 36.45), (12.8, 36.7), (11.7, 36.95), (11.22, 36.98)], 10)
AGB = smooth([(11.0, 36.92), (10.72, 36.62), (10.42, 36.68), (10.32, 36.8)], 10)
@sc("04b_the_sicilian_wars", 30, WAIST, dict(sw=SICW, se=SICE, home=AFR_HOME))
def _(fr, t):
    k = fr.masks
    fr.fill(k["home"], PURPLE_L); fr.fill(k["sw"], PURPLE); fr.fill(k["se"], GREEK)
    region(fr, 14.1, 37.62, "SICILY", size=24, sp=9, w="b")
    date(fr, "310 BC", fr.r(0.3, 0.5))
    carthage(fr, 1.0, r=10, side="l", size=24)
    gdot(fr, "SYRACUSE", r=8); x, y = P(fr.cam, *C["SYRACUSE"])
    T(fr, x + 30, y - 14, "SYRACUSE", size=23, w="b"); T(fr, x + 30, y + 14, "AGATHOCLES", size=17, sp=3, a=fr.r(1.6, 0.5), color=(70, 70, 70), w="b")
    ring(fr, *C["SYRACUSE"], 20, color=PURPLE_D, width=4.5, frac=fr.r(4.0, 1.2))
    garrow(fr, AGA, frac=fr.r(7.0, 4.0))
    fr.plaque(P(fr.cam, 13.5, 36.05)[0], P(fr.cam, 13.5, 36.05)[1], "14,000 MEN", size=24, a=fr.r(7.6, 0.5), pad=(13, 8))
    b = fr.r(11.6, 0.5)
    if b > 0:
        x, y = P(fr.cam, 11.32, 36.98)
        for i in range(3): boat(fr, x + 4 + i * 5, y - 16 + i * 15, 3.3, CHAR, b, k=1.0)
    TL(fr, 11.62, 37.32, "BURNS HIS SHIPS", size=17, sp=2.5, a=b, w="b")
    garrow(fr, AGB, frac=fr.r(14.0, 2.0))
    TL(fr, 10.3, 38.45, "GIANT AT SEA", size=24, sp=7, anchor="m", a=fr.r(21.0, 0.6), w="b", color=SEA_D)
    TL(fr, 9.75, 36.2, "SOFT AT HOME", size=20, sp=5, anchor="m", a=fr.r(22.4, 0.6), w="b", color=PURPLE_D)

# ================= 5. How It Worked, the round harbour: 6 s (VO 0:56-1:02)
QUAY = (229, 209, 168)
@sc("05_round_harbour", 6, WEST, active=[(0.3, 2.9)])
def _(fr, t):
    blank(fr, LAND)
    cx, cy, R, Rb, Ri = 960, 462, 372, 300, 124
    circ(fr, cx, cy, R, QUAY); circ(fr, cx, cy, R, None, outline=SAND_D, width=3)
    circ(fr, cx, cy, Rb, SEA)
    poly(fr, [(cx - 30, cy + Rb - 14), (cx + 30, cy + Rb - 14), (cx + 30, 1080), (cx - 30, 1080)], SEA)
    pline(fr, [(cx - 30, cy + R - 2), (cx - 30, 1080)], color=SAND_D, width=3); pline(fr, [(cx + 30, cy + R - 2), (cx + 30, 1080)], color=SAND_D, width=3)
    circ(fr, cx, cy, Ri, QUAY); circ(fr, cx, cy, Ri, None, outline=SAND_D, width=3)
    circ(fr, cx, cy, 50, (214, 190, 146)); poly(fr, [(cx - 20, cy - 20), (cx + 20, cy - 20), (cx + 20, cy + 20), (cx - 20, cy + 20)], SAND_D)
    k = keyed(t, [(0.3, 0.0), (2.9, 1.0)])
    n1, n2 = 190, 30; g = math.radians(8)
    for i in range(int(round(n1 * k))):
        ang = math.pi / 2 + g + (2 * math.pi - 2 * g) * (i + 0.5) / n1
        ca, sa = math.cos(ang), math.sin(ang)
        pline(fr, [(cx + ca * (Rb + 5), cy + sa * (Rb + 5)), (cx + ca * (Rb + 54), cy + sa * (Rb + 54))], color=PURPLE, width=4.2)
    for i in range(int(round(n2 * k))):
        ang = math.pi / 2 + 2 * math.pi * (i + 0.5) / n2; ca, sa = math.cos(ang), math.sin(ang)
        pline(fr, [(cx + ca * (Ri - 5), cy + sa * (Ri - 5)), (cx + ca * (Ri - 44), cy + sa * (Ri - 44))], color=PURPLE, width=4.2)
    T(fr, 150, 130, "CARTHAGE", size=30, sp=8, a=fr.r(0.2, 0.5), w="b")
    T(fr, 150, 172, "THE NAVAL HARBOUR", size=19, sp=4, a=fr.r(0.2, 0.5), color=(80, 80, 80), w="b")
    ca = fr.r(1.6, 0.5)
    pline(fr, [(1310, 250), (1400, 190), (1470, 190)], width=2.5, a=ca); T(fr, 1484, 190, "COVERED DOCKS", size=21, sp=3, a=ca, w="b")
    fr.plaque(1640, 300, "220 WARSHIPS", size=32, a=fr.r(3.0, 0.5))

# ================= 6a. The First War with Rome, the strait: 22 s (VO 0:00-0:22)
@sc("06a_the_first_war_with_rome", 22, STRAIT, dict(it=ITALY))
def _(fr, t):
    fr.fill(fr.masks["it"], ROME_L, fr.r(8.0, 1.0))
    region(fr, 15.2, 37.98, "SICILY", size=30, sp=12, w="b"); region(fr, 16.0, 38.33, "ITALY", size=30, sp=12, w="b", a=fr.r(8.0, 1.0))
    date(fr, "264 BC", fr.r(0.3, 0.5))
    m = fr.r(2.2, 0.5); city(fr, "MESSANA", a=m, side="l", r=9, size=28, ring=WHITE, dot=INK)
    p1 = fr.r(5.0, 5.0); pos = lerp((15.22, 38.46), (15.60, 38.31), p1); ca = fr.r(4.8, 0.5)
    fleet(fr, *pos, 6, PURPLE, ang=0.5, a=ca, k=1.25)
    x, y = P(fr.cam, *pos); T(fr, x, y - 44, "CARTHAGINIAN FLEET", size=20, sp=3, anchor="m", a=fr.r(5.6, 0.5), color=PURPLE_D, w="b")
    p2 = fr.r(7.5, 5.0); pos = lerp((15.74, 37.86), (15.685, 38.09), p2); rb = fr.r(7.3, 0.5)
    block(fr, *pos, ROME_D, a=rb, w=34, h=17, ang=-1.2)
    x, y = P(fr.cam, *pos); T(fr, x + 34, y + 2, "ROMAN ARMY", size=20, sp=3, anchor="l", a=fr.r(8.0, 0.5), color=ROME_D, w="b")
    dim(fr, (15.578, 38.235), (15.648, 38.235), "3 KM", fr.r(14.4, 0.6), off=(86, -2))

# ================= 6b. The First War with Rome, Ecnomus to the peace: 52 s (VO 0:48-1:40)
INV = smooth([(13.95, 36.95), (12.9, 36.75), (11.9, 36.75), (11.3, 36.82)], 10)
@sc("06b_the_first_war_with_rome", 52, WAIST, dict(sw=SICW, se=SICE, sic=SIC, home=AFR_HOME), active=[(25, 28.4)])
def _(fr, t):
    k = fr.masks
    fr.fill(k["home"], PURPLE_L); fr.fill(k["sw"], PURPLE); fr.fill(k["se"], ROME_L); fr.fill(k["sic"], ROME_L, fr.r(34.0, 3.0))
    region(fr, 14.2, 37.62, "SICILY", size=24, sp=9, w="b")
    carthage(fr, 1.0, r=10, side="l", size=24)
    date(fr, "256 BC", fr.r(0.3, 0.5) * (1 - fr.r(33.4, 0.4))); date(fr, "241 BC", fr.r(34.0, 0.5))
    off = 1 - fr.r(11.4, 0.7)
    TL(fr, 13.93, 37.32, "CAPE ECNOMUS", size=18, sp=2.5, anchor="m", a=fr.r(1.0, 0.5) * off, w="b")
    # the fleets
    go = fr.r(12.3, 3.2); back = fr.r(23.6, 2.0)
    rp = lerp((14.9, 36.72), (14.22, 36.88), fr.r(0.5, 2.5))
    if go > 0: rp = tuple(partial(INV, go)[-1])
    if back > 0: rp = lerp((11.3, 36.82), (14.2, 36.62), back)
    gline(fr, INV, color=ROME, width=4, frac=go, a=1 - fr.r(23.0, 1.0))
    fleet(fr, *rp, 6, ROME_D, ang=math.pi if back == 0 else 0.0, a=1 - fr.r(25.8, 1.2), k=1.1, dy=22)
    fleet(fr, *rp, 3, ROME_D, ang=math.pi if back == 0 else 0.0, k=1.1, cols=3, dy=0)
    cp = lerp((12.95, 37.05), (13.62, 36.92), fr.r(0.5, 2.5))
    fleet(fr, *cp, 9, PURPLE, ang=0.0, a=1 - fr.r(10.4, 0.9), k=1.1, dy=10)
    cross(fr, 13.93, 36.93, a=fr.r(3.1, 0.4) * off, r=13, width=5)
    fr.plaque(P(fr.cam, 13.93, 36.3)[0], P(fr.cam, 13.93, 36.3)[1], "680 SHIPS", size=28, a=fr.r(3.5, 0.5) * off)
    fr.plaque(P(fr.cam, 13.93, 36.3)[0], P(fr.cam, 13.93, 36.3)[1] + 62, "290,000 MEN", size=24, a=fr.r(6.2, 0.5) * off, pad=(13, 8))
    # the invasion of Africa
    arm = fr.r(15.4, 0.4) * (1 - fr.r(23.0, 0.8)); ap = lerp((11.0, 36.86), (10.5, 36.66), fr.r(17.0, 2.5))
    block(fr, *ap, ROME_D, a=arm, w=28, h=14)
    cross(fr, 10.5, 36.66, a=fr.r(22.4, 0.4) * (1 - fr.r(24.4, 0.8)), r=12, width=5)
    # the storm
    if 25 <= t <= 28.4: fr.pulse(14.2, 36.66, t, 25.0, color=SEA_D, n=3, period=1.1, rmax=70, width=4)
    fr.plaque(P(fr.cam, 14.2, 36.05)[0] + 40, P(fr.cam, 14.2, 36.05)[1], "384 SHIPS LOST", size=26, a=fr.r(25.8, 0.5) * (1 - fr.r(33.4, 0.5)), pad=(13, 8))
    fleet(fr, 15.85, 37.5, 6, ROME_D, ang=math.pi / 2, a=fr.r(29.4, 0.5), k=1.0)
    fleet(fr, 15.95, 36.95, 6, ROME_D, ang=math.pi / 2, a=fr.r(30.9, 0.5), k=1.0)
    fr.plaque(250, 186, "3,200 TALENTS", size=26, a=fr.r(38.4, 0.5), pad=(14, 9))

# ================= 7a. The Truceless War, the mutiny: 30 s (VO 0:00-0:30)
MERC = smooth([(12.4, 37.75), (11.6, 37.55), (10.85, 37.32), (10.45, 37.0)], 10)
TOWNS = [C["UTICA"], C["HIPPACRA"], (9.55, 36.78), (9.2, 36.52), (9.85, 36.42), (10.2, 36.38), (10.62, 36.42), (9.4, 37.05), (10.72, 36.72)]
_c7, _a7 = mover([(0, WAIST), (9, WAIST), (12, AFR), (30, AFR)])
@sc("07a_the_truceless_war", 30, _c7, dict(sic=SIC, home=AFR_HOME), active=_a7)
def _(fr, t):
    k = fr.masks; fr.fill(k["home"], PURPLE_L); fr.fill(k["sic"], ROME_L)
    w = 1 - fr.r(9.0, 0.8)
    region(fr, 14.2, 37.62, "SICILY", size=24, sp=9, w="b", a=w, color=ROME_D)
    date(fr, "241 BC", fr.r(0.3, 0.5) * w)
    gline(fr, MERC, color=CHAR, width=5, frac=fr.r(4.5, 3.0), arrow=True, a=w)
    TL(fr, 11.5, 38.0, "MERCENARIES", size=20, sp=3, anchor="m", a=fr.r(5.2, 0.5) * w, w="b", color=CHAR)
    for i, ll in enumerate(TOWNS):
        pdot(fr, None, fr.r(11.0, 0.8), r=6, ll=ll); pdot(fr, None, fr.r(17.0 + 0.35 * i, 0.4), r=6, ll=ll, color=CHAR)
    TL(fr, 9.5, 36.1, "AFRICAN TOWNS", size=18, sp=3, anchor="m", a=fr.r(17.0, 0.5), w="b", color=CHAR)
    mp = lerp((9.7, 36.62), (10.14, 36.78), fr.r(14.0, 2.2))
    block(fr, *mp, CHAR, a=fr.r(12.4, 0.5), w=30, h=15, ang=-0.3)
    ring(fr, *C["CARTHAGE"], 62, color=CHAR, width=5.5, frac=0.56 * fr.r(21.0, 1.6), start=80)
    carthage(fr, 1.0, r=11, side="r", size=26)
    x, y = P(fr.cam, *C["CARTHAGE"]); fr.plaque(x + 96, y - 64, "UNDER SIEGE", size=26, a=fr.r(22.4, 0.5), pad=(13, 8))

# ================= 7b. The Truceless War, the pass and the islands: 36 s (VO 0:52-1:28)
_c7b, _a7b = mover([(0, AFR), (7.3, AFR), (9.6, SARD), (36, SARD)])
@sc("07b_the_truceless_war", 36, _c7b, dict(sic=SIC, sar=SAR, cor=COR, home=AFR_HOME, it=ITALY), active=_a7b)
def _(fr, t):
    k = fr.masks
    fr.fill(k["home"], PURPLE_L); fr.fill(k["sic"], ROME_L); fr.fill(k["it"], ROME_L)
    fr.fill(k["sar"], PURPLE_L); fr.fill(k["sar"], ROME_L, fr.r(11.3, 1.2)); fr.fill(k["cor"], ROME_L, fr.r(12.0, 1.2))
    near = 1 - fr.r(7.3, 0.8)
    mounts(fr, [(9.42, 36.53), (10.06, 36.51)], a=near, step=30, size=11); mounts(fr, [(9.42, 36.29), (10.06, 36.27)], a=near, step=30, size=11)
    hp = lerp((10.2, 36.78), (10.13, 36.40), fr.r(0.8, 2.6))
    block(fr, 9.74, 36.40, CHAR, a=fr.r(0.4, 0.5) * (1 - fr.r(6.6, 0.9)) * near, w=34, h=15)
    block(fr, *hp, PURPLE, a=near, w=18, h=40)
    block(fr, 9.36, 36.40, PURPLE, a=fr.r(3.5, 0.5) * near, w=18, h=40)
    x, y = P(fr.cam, *hp); T(fr, x + 24, y, "HAMILCAR BARCA", size=22, sp=2.5, a=fr.r(0.6, 0.5) * near, w="b", color=PURPLE_D)
    cross(fr, 9.74, 36.40, a=fr.r(6.0, 0.4) * near, r=13, width=5)
    carthage(fr, 1.0, r=10, side="r", size=24)
    far = fr.r(9.2, 0.6)
    city(fr, "ROME", a=far, side="r", r=7, size=24, dot=ROME_D, ring=WHITE, color=ROME_D)
    TL(fr, 8.05, 40.1, "SARDINIA", size=22, sp=3, anchor="r", a=fr.r(11.3, 0.5), w="b")
    TL(fr, 8.45, 42.2, "CORSICA", size=22, sp=3, anchor="r", a=fr.r(12.0, 0.5), w="b")
    fr.plaque(250, 120, "+1,200 TALENTS", size=30, a=fr.r(16.3, 0.5))

# ================= 8a. The Barcas in Spain, Hamilcar leaves: 6 s (VO 0:00-0:06)
HAM = smooth([(9.9, 36.75), (7.5, 36.55), (4.5, 36.35), (1.5, 35.85), (-1.5, 35.15), (-4.0, 35.1), (-5.35, 35.7), (-5.85, 36.2), (-6.1, 36.6)], 10)
@sc("08a_the_barcas_in_spain", 6, SPAF, dict(home=AFR_HOME))
def _(fr, t):
    fr.fill(fr.masks["home"], PURPLE_L)
    date(fr, "237 BC", fr.r(0.2, 0.5))
    region(fr, -3.3, 39.6, "SPAIN", size=32, sp=12, w="b")
    carthage(fr, 1.0, r=10, side="t", size=24)
    gline(fr, HAM, color=PURPLE, width=5.5, frac=fr.r(3.0, 2.6), arrow=True)
    TL(fr, 4.6, 35.55, "HAMILCAR", size=22, sp=4, anchor="m", a=fr.r(1.2, 0.5), w="b", color=PURPLE_D)

# ================= 8b. The Barcas in Spain, the kingdom: 57 s (VO 0:21-1:18)
def mine(fr, lon, lat, a):
    if a <= 0: return
    x, y = P(fr.cam, lon, lat)
    poly(fr, [(x, y - 13), (x + 13, y), (x, y + 13), (x - 13, y)], WHITE, a); poly(fr, [(x, y - 9), (x + 9, y), (x, y + 9), (x - 9, y)], (96, 100, 106), a)
EBRO_L = EBRO[0] if EBRO[0][0][0] > EBRO[0][-1][0] else EBRO[0][::-1]
@sc("08b_the_barcas_in_spain", 57, SPAINC, dict(sp=SPAIN), active=[(22.5, 25.2), (55, 57)])
def _(fr, t):
    fr.fill(fr.masks["sp"], PURPLE_L, fr.r(5.5, 6.0))
    region(fr, -4.6, 40.75, "SPAIN", size=36, sp=14, w="b", a=fr.r(0.2, 0.5))
    for i, ll in enumerate([C["CASTULO"], C["RIOTINTO"], (-1.75, 37.45)]): mine(fr, *ll, fr.r(0.6 + 0.5 * i, 0.4))
    TL(fr, -3.62, 38.47, "SILVER", size=20, sp=5, anchor="m", a=fr.r(0.8, 0.5), w="b", color=(70, 74, 80))
    TL(fr, -3.9, 39.25, "THE BARCA FAMILY", size=19, sp=4, anchor="m", a=fr.r(8.0, 0.6), w="b", color=PURPLE_D)
    gline(fr, EBRO_L, color=ROME_D, width=5.5, frac=fr.r(33.6, 1.8))
    TL(fr, 0.75, 42.3, "RIVER EBRO", size=22, sp=3, anchor="m", a=fr.r(34.2, 0.5), w="b", color=ROME_D)
    TL(fr, 0.75, 42.0, "ROME'S LINE", size=16, sp=3, anchor="m", a=fr.r(35.0, 0.5), w="b", color=ROME_D)
    nc = fr.r(22.5, 0.4)
    if 22.5 <= t <= 25.2: fr.pulse(*C["NEWCARTHAGE"], t, 22.5, color=PURPLE, n=2, rmax=44, width=3.5)
    pdot(fr, "NEWCARTHAGE", nc, r=10)
    x, y = P(fr.cam, *C["NEWCARTHAGE"])
    T(fr, x + 24, y + 6, "QART-HADASHT", size=26, a=fr.r(24.0, 0.5), w="b")
    T(fr, x + 24, y + 38, "NEW CARTHAGE", size=21, sp=2, a=fr.r(26.4, 0.5), w="b", color=PURPLE_D)
    T(fr, x + 24, y + 66, "NOW CARTAGENA", size=16, sp=4, a=fr.r(28.6, 0.5), w="m", color=GRAY)
    date(fr, "221 BC", fr.r(39.0, 0.5))
    fr.plaque(250, 186, "HANNIBAL, 26", size=26, a=fr.r(42.6, 0.5), pad=(14, 9))
    sg = fr.r(49.0, 0.4)
    city(fr, "SAGUNTUM", a=sg, side="r", r=8, size=24, dot=ROME_D, ring=WHITE, dx=14)
    x, y = P(fr.cam, *C["SAGUNTUM"]); T(fr, x + 34, y + 27, "FRIEND OF ROME", size=15, sp=3, a=fr.r(52.4, 0.5), w="b", color=ROME_D)
    ring(fr, *C["SAGUNTUM"], 19, color=PURPLE_D, width=4.5, frac=fr.r(54.6, 1.0))
    if 55.6 <= t <= 57: fr.pulse(*C["SAGUNTUM"], t, 55.6, color=PURPLE_D, n=1, rmax=40, width=3)
    fr.plaque(x + 96, y - 52, "8 MONTHS", size=24, a=fr.r(55.4, 0.5), pad=(13, 8))

# ================= 9. Hannibal: 98 s (VO 0:00-1:38)
HR = smooth([(-0.98, 37.6), (-0.6, 38.6), (-0.3, 39.65), (0.5, 40.75), (2.0, 41.55), (2.85, 42.45), (3.1, 43.25), (4.1, 43.7), (4.75, 44.05), (4.95, 44.85),
             (5.75, 45.2), (6.9, 45.1), (7.68, 45.05), (9.55, 45.0), (10.4, 44.6), (11.0, 44.1), (11.3, 43.6), (12.05, 43.2), (12.9, 42.75), (14.1, 42.3),
             (15.3, 41.65), (16.1, 41.32)], 12)
_HK = [(9.0, 0.0), (12.0, frac_at(HR, 2.85, 42.45)), (14.0, frac_at(HR, 4.75, 44.05)), (17.6, frac_at(HR, 6.9, 45.1)), (22.0, frac_at(HR, 7.68, 45.05)),
       (38.0, frac_at(HR, 7.68, 45.05)), (41.0, frac_at(HR, 9.55, 45.0)), (43.6, frac_at(HR, 12.05, 43.2)), (53.0, 1.0)]
PLAN_SP = smooth([(11.9, 42.0), (10.4, 42.75), (7.0, 42.7), (4.2, 42.35), (2.4, 41.5), (1.1, 41.0)], 10)
PLAN_AF = smooth([(12.55, 41.5), (12.95, 39.6), (12.4, 38.3), (11.3, 37.55), (10.55, 37.15)], 10)
TOROME = smooth([(16.0, 41.32), (14.9, 41.3), (13.6, 41.6), (12.72, 41.85)], 10)
PYR = [(-1.6, 42.98), (0.5, 42.72), (2.75, 42.45)]
ALPS = [(7.0, 43.95), (6.85, 44.6), (6.95, 45.3), (7.7, 45.95), (9.3, 46.4), (11.5, 46.75), (13.6, 46.5)]
_c9, _a9 = mover([(0, W9), (27, W9), (30.5, ITA9), (98, ITA9)])
@sc("09_hannibal", 98, _c9, dict(it=ITALY, sp=SPAIN, sic=SIC, sar=SAR, cor=COR, home=AFR_HOME), active=_a9 + [(9, 22.2), (38, 53.2), (55, 72.5)])
def _(fr, t):
    k = fr.masks
    for n in ("it", "sic", "sar", "cor"): fr.fill(k[n], ROME_L)
    fr.fill(k["sp"], PURPLE_L); fr.fill(k["home"], PURPLE_L)
    wide = 1 - fr.r(26.6, 0.5); ital = fr.r(30.0, 0.6)
    mounts(fr, PYR, step=30, size=11); mounts(fr, ALPS, step=30, size=11, rows=2, gap=16)
    pa = 1 - fr.r(5.6, 1.0)
    gline(fr, PLAN_SP, color=ROME_D, width=4, frac=fr.r(1.6, 1.6), a=pa, arrow=True, dash=(12, 8))
    gline(fr, PLAN_AF, color=ROME_D, width=4, frac=fr.r(1.6, 1.6), a=pa, arrow=True, dash=(12, 8))
    TL(fr, 7.3, 40.9, "ROME'S PLAN", size=19, sp=3, anchor="m", a=fr.r(2.0, 0.5) * pa, w="b", color=ROME_D)
    gline(fr, HR, color=PURPLE, width=5.5, frac=keyed(t, _HK), arrow=True)
    city(fr, "ROME", side="l", r=7, size=24, dot=ROME_D, ring=WHITE, color=ROME_D)
    pdot(fr, "NEWCARTHAGE", wide, r=8)
    x, y = P(fr.cam, *C["NEWCARTHAGE"]); T(fr, x - 18, y + 26, "HANNIBAL", size=24, sp=3, anchor="r", a=fr.r(6.6, 0.5) * wide, w="b", color=PURPLE_D)
    TL(fr, 0.3, 43.42, "PYRENEES", size=19, sp=4, anchor="m", a=fr.r(11.6, 0.5) * wide, w="b")
    TL(fr, 4.2, 44.85, "RHÔNE", size=19, sp=4, anchor="r", a=fr.r(13.6, 0.5) * wide, w="b", color=SEA_D)
    TL(fr, 7.9, 46.72, "ALPS", size=24, sp=12, anchor="m", a=fr.r(15.8, 0.5), w="b")
    date(fr, "218 BC", fr.r(14.8, 0.5) * (1 - fr.r(51.4, 0.5))); date(fr, "216 BC", fr.r(52.0, 0.5))
    x, y = P(fr.cam, 7.68, 45.05)
    fr.plaque(x + 110, y + 78, "20,000 INFANTRY", size=24, a=fr.r(23.0, 0.5) * wide, pad=(13, 8))
    fr.plaque(x + 110, y + 132, "6,000 CAVALRY", size=24, a=fr.r(24.6, 0.5) * wide, pad=(13, 8))
    # the three battles
    x, y = P(fr.cam, *C["TRASIMENE"]); alpha_draw(fr, lambda d, c: d.ellipse([s(x - 4), s(y - 13), s(x + 16), s(y + 3)], fill=c), SEA, ital)
    cross(fr, 9.62, 44.88, a=fr.r(41.0, 0.4), r=11, width=4.5)
    TL(fr, 9.62, 44.55, "TREBIA", size=21, sp=3, anchor="m", a=fr.r(41.0, 0.5), w="b")
    cross(fr, 12.02, 43.3, a=fr.r(43.8, 0.4), r=11, width=4.5)
    TL(fr, 12.45, 43.52, "LAKE TRASIMENE", size=21, sp=3, anchor="l", a=fr.r(43.6, 0.5), w="b")
    cn = fr.r(53.0, 0.4); x, y = P(fr.cam, *C["CANNAE"])
    cross(fr, *C["CANNAE"], a=cn, r=14, width=5.5); T(fr, x + 26, y - 2, "CANNAE", size=30, a=cn, w="b")
    fr.plaque(x + 96, y + 62, "48,000 ROMAN DEAD", size=24, a=fr.r(69.0, 0.5), pad=(13, 8))
    # the encirclement, inset in the left third
    ia = fr.r(55.0, 0.6) * (1 - fr.r(71.6, 0.8))
    cannae(fr, 50, 480, 580, 440, keyed(t, [(57.6, 0.0), (61.5, 0.52), (65.0, 0.62), (68.0, 1.0)]), a=ia)
    T(fr, 612, 506, "86,000", size=17, anchor="r", a=ia, w="b", color=ROME_D); T(fr, 612, 896, "50,000", size=17, anchor="r", a=ia, w="b", color=PURPLE_D)
    # the march that did not happen
    off = fr.r(86.4, 1.0)
    gline(fr, TOROME, color=mix(GRAY, PURPLE_D, off), width=4, frac=fr.r(83.0, 2.0), arrow=True, dash=(11, 8))
    TL(fr, 14.25, 41.72, "MARCH ON ROME?", size=17, sp=3, anchor="m", a=fr.r(83.4, 0.5), w="b", color=mix(GRAY, PURPLE_D, off))

# ================= 10. The Long Defeat: 67 s (VO 0:25-1:32)
SCIP = smooth([(1.25, 41.1), (0.5, 40.1), (-0.2, 38.95), (-0.85, 37.8)], 10)
HASD = smooth([(-1.5, 40.4), (1.6, 42.25), (4.4, 43.85), (6.9, 45.05), (9.5, 45.0), (11.5, 44.4), (12.85, 43.88)], 10)
SCAF = smooth([(12.4, 37.75), (11.5, 37.58), (10.6, 37.4), (10.12, 37.12)], 10)
HOME = smooth([(17.1, 39.0), (16.3, 37.5), (13.6, 35.85), (11.6, 35.55), (10.75, 35.8)], 10)
NUMC = smooth([(6.3, 35.5), (7.8, 35.6), (8.95, 35.92)], 8)
@sc("10_the_long_defeat", 67, W10, dict(it=ITALY, sic=SIC, sar=SAR, cor=COR, sp=SPAIN, home=AFR_HOME, coast=AFR_COAST))
def _(fr, t):
    k = fr.masks
    for n in ("it", "sic", "sar", "cor"): fr.fill(k[n], ROME_L)
    fr.fill(k["coast"], PURPLE_L, 1 - fr.r(56.0, 3.0)); fr.fill(k["home"], PURPLE_L)
    fr.fill(k["sp"], PURPLE_L); fr.fill(k["sp"], ROME_L, fr.r(18.6, 3.0))
    region(fr, -3.6, 39.6, "SPAIN", size=26, sp=9, w="b")
    city(fr, "ROME", side="l", r=7, size=24, dot=ROME_D, ring=WHITE, color=ROME_D)
    ha = 1 - fr.r(33.4, 1.0)
    block(fr, 16.35, 40.75, PURPLE, a=ha, w=30, h=15, ang=-0.5)
    TL(fr, 17.0, 41.45, "HANNIBAL", size=22, sp=3, anchor="l", a=fr.r(0.3, 0.5) * ha, w="b", color=PURPLE_D)
    fr.plaque(P(fr.cam, 17.0, 41.45)[0] + 70, P(fr.cam, 17.0, 41.45)[1] - 50, "15 YEARS", size=26, a=fr.r(1.2, 0.5) * ha, pad=(13, 8))
    cp = fr.r(6.2, 0.8); x, y = P(fr.cam, *C["CAPUA"])
    circ(fr, x, y, 9.5, WHITE, cp); circ(fr, x, y, 6.5, PURPLE, cp); T(fr, x - 14, y + 20, "CAPUA", size=20, anchor="l", a=cp, w="b")
    gline(fr, SCIP, color=ROME_D, width=5, frac=fr.r(18.0, 2.2), arrow=True, a=1 - fr.r(30.0, 1.0))
    TL(fr, 2.3, 40.6, "SCIPIO", size=22, sp=3, anchor="l", a=fr.r(18.0, 0.5) * (1 - fr.r(30.0, 0.6)), w="b", color=ROME_D)
    gline(fr, HASD, color=PURPLE, width=5.5, frac=fr.r(22.0, 2.6), arrow=True, a=1 - fr.r(29.0, 1.5))
    TL(fr, 4.3, 44.75, "HANNIBAL'S BROTHER", size=19, sp=3, anchor="r", a=fr.r(22.2, 0.5) * (1 - fr.r(29.0, 1.5)), w="b", color=PURPLE_D)
    cross(fr, *C["METAURUS"], a=fr.r(24.8, 0.4) * (1 - fr.r(29.0, 1.5)), r=14, width=5.5)
    gline(fr, SCAF, color=ROME_D, width=5, frac=fr.r(31.0, 1.8), arrow=True, a=1 - fr.r(54.6, 1.0))
    TL(fr, 11.9, 38.25, "SCIPIO", size=22, sp=3, anchor="l", a=fr.r(31.4, 0.5) * (1 - fr.r(54.6, 0.6)), w="b", color=ROME_D)
    gline(fr, HOME, color=PURPLE, width=4.5, frac=fr.r(33.6, 2.2), arrow=True, a=1 - fr.r(54.6, 1.0))
    date(fr, "202 BC", fr.r(35.0, 0.5) * (1 - fr.r(54.6, 0.5)))
    za = fr.r(36.0, 0.5) * (1 - fr.r(54.6, 1.0)); x, y = P(fr.cam, *C["ZAMA"])
    circ(fr, x, y, 9.5, WHITE, za); circ(fr, x, y, 6.5, INK, za); T(fr, x - 2, y + 30, "ZAMA", size=26, anchor="m", a=za, w="b")
    na = 1 - fr.r(54.6, 0.8)
    gline(fr, NUMC, color=(128, 98, 58), width=4.5, frac=fr.r(44.0, 1.6), arrow=True, a=na)
    TL(fr, 5.2, 34.75, "NUMIDIAN CAVALRY", size=17, sp=3, anchor="m", a=fr.r(44.3, 0.5) * na, w="b", color=(128, 98, 58))
    cross(fr, 9.25, 36.0, a=fr.r(50.0, 0.4) * (1 - fr.r(54.6, 0.8)), r=13, width=5)
    for i, (txt, t0) in enumerate((("NO OVERSEAS EMPIRE", 55.4), ("ALMOST NO FLEET", 57.4), ("NO WAR WITHOUT ROME", 59.4), ("10,000 TALENTS", 61.2))):
        fr.plaque(110, 110 + 60 * i, txt, size=25, a=fr.r(t0, 0.5), anchor="l", pad=(14, 9))
    carthage(fr, 1.0, r=10, side="l", size=24)
    TL(fr, 10.2, 35.0, "A CITY WITH A FARM", size=19, sp=3, anchor="m", a=fr.r(64.4, 0.5), w="b", color=PURPLE_D)

# ================= 11. Carthage Must Be Destroyed: 39 s (VO 0:50-1:29)
_PLAN = {}
PEN = [(-60, 318), (300, 330), (520, 262), (700, 150), (880, 96), (1060, 104), (1210, 190), (1290, 318), (1262, 470), (1206, 600), (1176, 716), (1150, 800), (1116, 900),
       (1090, 1140), (1030, 1140), (1052, 900), (1030, 800), (930, 770), (720, 750), (500, 712), (300, 650), (-60, 630)]
CITY = [(905, 372), (1262, 372), (1250, 470), (1200, 600), (1170, 716), (1146, 790), (1040, 786), (935, 758), (905, 640)]
def plan_image():
    if "im" not in _PLAN:
        class F: pass
        f = F(); f.im = Image.new("RGB", (W * SS, H * SS), SEA); f.d = ImageDraw.Draw(f.im)
        pen = [tuple(p) for p in engine._chaikin(np.asarray(PEN, float), 3)]
        poly(f, pen, LAND)
        m = Image.new("L", f.im.size, 0); ImageDraw.Draw(m).polygon([(s(x), s(y)) for x, y in pen], fill=255)
        inner = Image.new("L", f.im.size, 0); ImageDraw.Draw(inner).rectangle([s(452), 0, W * SS, H * SS], fill=255)
        f.im.paste(PURPLE_L, (0, 0), IC.multiply(m, inner))
        cm = Image.new("L", f.im.size, 0); ImageDraw.Draw(cm).polygon([(s(x), s(y)) for x, y in engine._chaikin(np.asarray(CITY, float), 2)], fill=255)
        _PLAN["city"] = IC.multiply(m, cm); f.im.paste((178, 128, 164), (0, 0), _PLAN["city"]); f.d = ImageDraw.Draw(f.im)
        for dx in (0, 13, 26): pline(f, [(428 + dx, 268), (440 + dx, 480), (432 + dx, 712)], color=PURPLE_D, width=4.5)     # triple wall across the isthmus
        circ(f, 1035, 520, 62, (150, 96, 136)); circ(f, 1035, 520, 62, None, outline=PURPLE_D, width=3); circ(f, 1035, 520, 34, None, outline=PURPLE_D, width=2.5)
        circ(f, 1118, 662, 36, SEA); circ(f, 1118, 662, 36, None, outline=PURPLE_D, width=3); circ(f, 1118, 662, 12, (178, 128, 164))
        poly(f, [(1100, 706), (1146, 706), (1146, 772), (1100, 772)], SEA, outline=PURPLE_D, width=3)
        poly(f, [(1112, 694), (1124, 694), (1124, 710), (1112, 710)], SEA); poly(f, [(1140, 752), (1190, 752), (1190, 768), (1140, 768)], SEA)
        T(f, 1035, 430, "CARTHAGE", size=30, sp=8, anchor="m", w="b", color=WHITE)
        T(f, 1035, 520, "CITADEL", size=14, sp=3, anchor="m", w="b", color=WHITE)
        T(f, 1080, 688, "HARBOURS", size=15, sp=3, anchor="r", w="b", color=WHITE)
        T(f, 470, 500, "WALLS", size=17, sp=4, anchor="l", w="b", color=PURPLE_D)
        _PLAN["im"] = f.im
    return _PLAN["im"]
NUMA = [smooth([(7.6, 36.55), (8.6, 36.5), (9.25, 36.55)], 8), smooth([(8.3, 35.1), (9.3, 35.3), (10.2, 35.5)], 8)]
ROMEL = smooth([(12.4, 37.75), (11.5, 37.62), (10.6, 37.42), (10.14, 37.12)], 10)
@sc("11_carthage_must_be_destroyed", 39, AFRW, dict(home=AFR_HOME, eat=Dm(AFR_HOME, AFR_SMALL), num=NUMIDIA, sic=SIC), active=[(11.0, 12.7)])
def _(fr, t):
    k = fr.masks
    fr.fill(k["num"], NUM); fr.fill(k["home"], PURPLE_L); fr.fill(k["eat"], NUM, fr.r(0.6, 5.0)); fr.fill(k["sic"], ROME_L)
    region(fr, 7.1, 35.75, "NUMIDIA", size=30, sp=12, w="b", color=(112, 84, 46), a=fr.r(0.2, 0.5))
    for p in NUMA: gline(fr, p, color=(128, 98, 58), width=5, frac=fr.r(1.0, 2.4), arrow=True)
    gline(fr, ROMEL, color=ROME_D, width=5.5, frac=fr.r(7.3, 2.2), arrow=True)
    TL(fr, 11.7, 38.0, "ROMAN ARMY", size=20, sp=3, anchor="l", a=fr.r(7.8, 0.5), w="b", color=ROME_D)
    carthage(fr, 1.0, r=10, side="r", size=24)
    pa = fr.r(11.0, 1.6)
    if pa > 0:
        fr.im = Image.blend(fr.im, plan_image(), pa) if pa < 1 else plan_image().copy(); fr.d = ImageDraw.Draw(fr.im)
        q = 1.0 if pa >= 1 else 0.0
        burn = fr.r(37.3, 1.5)
        if burn > 0:
            fr.im.paste(CHAR, (0, 0), _PLAN["city"].point(lambda v: int(v * 0.86 * burn))); fr.d = ImageDraw.Draw(fr.im)
            T(fr, 1035, 430, "CARTHAGE", size=30, sp=8, anchor="m", w="b", color=WHITE, a=burn)
        sg = fr.r(14.0, 1.2) * q
        pline(fr, [(352, 262), (366, 480), (356, 722)], color=ROME_D, width=7, frac=sg)
        for i, yy in enumerate((330, 480, 640)):
            poly(fr, [(250, yy - 22), (310, yy - 22), (310, yy + 22), (250, yy + 22)], ROME_D, fr.r(14.6 + 0.3 * i, 0.4) * q)
        fa = fr.r(15.4, 0.6) * q
        if fa > 0:
            for i in range(7): boat(fr, 1340 + (i % 2) * 34, 330 + i * 64, math.pi, ROME_D, fa, k=1.5)
        pline(fr, [(1196, 742), (1196, 784)], color=ROME_D, width=8, a=fr.r(16.0, 0.5) * q)
        fr.plaque(960, 150, "ROME:  ABANDON THE CITY", size=30, a=fr.r(17.0, 0.5) * (1 - fr.r(20.6, 0.4)) * q)
        fr.plaque(960, 150, "CARTHAGE REFUSES", size=30, a=fr.r(21.0, 0.5) * (1 - fr.r(28.6, 0.4)) * q)
        fr.plaque(960, 150, "3 YEARS", size=30, a=fr.r(29.0, 0.5) * (1 - fr.r(33.6, 0.5)) * q)
        pline(fr, engine.smooth([(1262, 800), (1186, 742), (1118, 640), (1052, 548)], 10), color=ROME_D, width=8, frac=fr.r(31.3, 1.8) * q, arrow=True)
    date(fr, "149 BC", fr.r(7.0, 0.5) * (1 - fr.r(30.6, 0.4))); date(fr, "146 BC", fr.r(31.0, 0.5))

# ================= 12a. What Remains, Roman Carthage: 16 s (VO 0:00-0:16)
@sc("12a_what_remains", 16, WEST, dict(emp=EMPIRE))
def _(fr, t):
    fr.fill(fr.masks["emp"], ROME_L, fr.r(0.6, 2.6))
    city(fr, "ROME", a=fr.r(0.6, 0.6), side="r", r=8, size=24, dot=ROME_D, ring=WHITE, color=ROME_D)
    x, y = P(fr.cam, *C["CARTHAGE"])
    ch = fr.r(1.2, 1.0)
    carthage(fr, 1.0, r=11, label="", dot=mix(ROME_D, PURPLE, ch))
    T(fr, x, y - 40, "CARTHAGE", size=30, anchor="m", w="b", a=1 - fr.r(1.2, 0.5))
    T(fr, x, y - 40, "ROMAN CARTHAGE", size=30, anchor="m", w="b", a=fr.r(1.8, 0.5), color=ROME_D)
    fr.plaque(x, y + 62, "2ND CITY OF THE ROMAN WEST", size=26, a=fr.r(8.0, 0.5), pad=(14, 9))

# ================= 12b. What Remains, the ring closes: 10 s (VO 1:11-1:21)
@sc("12b_what_remains", 10, WEST, active=[(0.3, 3.2)])
def _(fr, t):
    a = fr.r(0.2, 0.5)
    if 0.3 <= t <= 3.2: fr.pulse(*C["CARTHAGE"], t, 0.3, color=PURPLE, n=2, rmax=54, width=3.5)
    carthage(fr, a, r=11, side="t", size=30)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "still":
        for spec in sys.argv[2:]:
            n, ts = spec.split("@"); scn = SC[n]
            for tt in ts.split(","): scn.still(float(tt), f"test/{n}_{float(tt):05.1f}.png", 0.5)
    elif mode == "render":
        import time
        for n in sys.argv[2:]:
            t0 = time.time(); SC[n].render("out"); print(n, round(time.time() - t0, 1), flush=True)
    elif mode == "list":
        for n, scn in SC.items(): print(n, scn.dur)
