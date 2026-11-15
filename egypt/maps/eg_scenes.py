from eg_base import *

CAM_ETH = cam_box(10.5, 55.5, 13.2, 32.3)
CAM_JOIN = cam_box(30.2, 32.3, 29.35, 30.75)
CAM_MEM = cam_box(30.4, 32.1, 29.30, 30.08)
CAM_RED = cam_box(30.75, 33.15, 28.6, 30.2)
CAM_NUB = cam_box(27.4, 36.6, 21.15, 25.25)
CAM_F6 = cam_box(18, 48, 17.5, 33.2)

# ================= 0. Cold open: 17 s (VO 0:46-1:03)
@scene("00_cold_open", 17, COUNTRY, dict(egy=EGY))
def _(fr, t):
    egypt(fr, fr.r(0.2, 1.2))
    region(fr, 27.6, 28.45, "EGYPT", a=fr.r(1.0, 0.8), size=34, sp=12)
    fr.plaque(P(fr.cam, 27.6, 28.45)[0], P(fr.cam, 27.6, 28.45)[1] + 70, "3,000 YEARS", size=34, a=fr.r(6.2, 0.6))

# ================= 1. The Gift: 79 s (VO 0:00-1:19, freeze 1:02-1:08)
_c1, _a1 = mover([(0, COUNTRY), (17.6, COUNTRY), (20.4, CAM_ETH), (30.2, CAM_ETH), (33.0, COUNTRY)])
@scene("01_the_gift", 79, _c1, dict(egy=EGY, wide=U(B("ASWAN", "APEX", wk=2.6), DEL)), rivers=False, active=_a1)
def _(fr, t):
    appear = fr.r(7.0, 1.2)
    out1 = 1 - fr.r(16.8, 0.6)                      # things that leave before the camera opens southwards
    flood = fr.r(24.0, 1.8) * (1 - fr.r(27.6, 2.2))
    fr.fill(fr.masks["wide"], FLOOD, flood * 0.85)
    egypt(fr, appear); river(fr, appear)
    region(fr, 25.9, 27.9, "SAHARA", a=fr.r(0.5, 0.8) * out1, size=40, sp=22, color=SAND_D, w="b")
    TL(fr, 33.05, 26.85, "THE NILE", size=19, sp=3, a=fr.r(7.8, 0.6) * out1)
    dim_v(fr, 29.75, 24.09, 31.55, fr.r(12.0, 1.0) * out1, "1,000 KM")
    a20 = fr.r(14.6, 0.6) * out1
    if a20 > 0:
        x, y = P(fr.cam, on_river(27.95), 27.95)
        pline(fr, [(x - 10, y), (x + 10, y)], width=2.5, a=a20)
        for xx in (x - 10, x + 10): pline(fr, [(xx, y - 9), (xx, y + 9)], width=2.5, a=a20)
        pline(fr, [(x + 16, y), (x + 62, y)], width=2, a=a20)
        fr.plaque(x + 118, y, "20 KM", size=24, a=a20, pad=(12, 8))
    # the source: rain far to the south, the flood runs north
    eth = fr.r(20.4, 0.6) * (1 - fr.r(29.6, 0.6))
    modern(fr, 37.3, 13.72, "NOW ETHIOPIA", a=eth, size=18)
    rain(fr, 37.3, 14.6, eth)
    fp = fr.r(21.4, 5.2); fa = 1 - fr.r(27.0, 1.6)
    gline(fr, FLOODPATH, color=FLOOD, width=6, frac=fp, a=fa)
    # the names of the two lands
    TL(fr, 31.13, 31.02, "KEMET", size=30, w="b", color=WHITE, sp=5, anchor="m", a=fr.r(34.2, 0.7))
    TL(fr, 31.13, 31.02, "THE BLACK LAND", dy=27, size=13, w="s", color=WHITE, sp=2.5, anchor="m", a=fr.r(34.8, 0.7))
    region(fr, 26.6, 26.9, "DESHRET", a=fr.r(38.0, 0.7), size=30, sp=12, color=SAND_D, w="b")
    region(fr, 26.6, 26.9, "THE RED LAND", a=fr.r(38.5, 0.7), size=15, sp=4, color=SAND_D, dy=30, w="m")
    region(fr, 32.7, 27.9, "DESHRET", a=fr.r(38.0, 0.7), size=18, sp=5, color=SAND_D, w="b")
    # the walls: desert on both sides, sea on top, cataracts at the bottom
    dimw = 1 - 0.7 * fr.r(49.2, 0.8)
    gline(fr, WALL_L, width=4.5, frac=fr.r(42.0, 1.2), a=dimw); gline(fr, WALL_R, width=4.5, frac=fr.r(42.0, 1.2), a=dimw)
    gline(fr, [(29.3, 31.97), (33.1, 31.97)], width=4.5, frac=fr.r(44.0, 0.7), a=dimw)
    TL(fr, 31.2, 32.13, "SEA", size=16, sp=5, anchor="m", a=fr.r(44.3, 0.5) * dimw, color=(70, 110, 125))
    gline(fr, [(32.3, 24.0), (33.5, 24.0)], width=6, frac=fr.r(46.0, 0.6), a=dimw)
    TL(fr, 33.6, 24.0, "CATARACTS", size=16, sp=4, a=fr.r(46.3, 0.5) * dimw)
    # current north, wind south
    seg = axis_part("ASYUT", "MEIDUM")[::30]
    cur = smooth([tuple(p + np.array([0.34, 0.0])) for p in seg], 8); wnd = smooth([tuple(p + np.array([-0.34, 0.0])) for p in seg[::-1]], 8)
    wb = 4.5 + 2.2 * fr.r(54.0, 0.5) * (1 - fr.r(56.2, 0.6))
    gline(fr, cur, color=(52, 124, 156), width=wb, frac=fr.r(50.0, 1.4), arrow=True)
    gline(fr, wnd, color=(88, 88, 88), width=wb, frac=fr.r(51.2, 1.4), arrow=True)
    x, y = P(fr.cam, on_river(28.55) + 0.34, 28.55)
    T(fr, x + 18, y, "CURRENT", size=17, sp=3, a=fr.r(50.4, 0.6), color=(40, 104, 134))
    x, y = P(fr.cam, on_river(28.55) - 0.34, 28.55)
    T(fr, x - 18, y, "WIND", size=17, sp=3, a=fr.r(51.6, 0.6), anchor="r", color=(70, 70, 70))

# ================= 2a. Two Lands: 17 s (VO 0:00-0:17)
@scene("02a_two_lands", 17, COUNTRY, dict(up=UPPER, lo=LOWER))
def _(fr, t):
    fr.plaque(330, 150, "3100 BC", size=32, a=fr.r(0.2, 0.5))
    fr.fill(fr.masks["up"], GREEN, fr.r(4.0, 1.0))
    fr.fill(fr.masks["lo"], GREEN_L, fr.r(12.0, 1.0)); fr.fill(fr.masks["lo"], GREEN, fr.r(15.0, 1.6))
    x, y = P(fr.cam, on_river(26.6), 26.6)
    T(fr, x - 34, y, "UPPER EGYPT", size=24, sp=4, anchor="r", a=fr.r(4.4, 0.7))
    fr.plaque(x - 150, y + 56, "UPPER = SOUTH", size=24, a=fr.r(8.0, 0.6), pad=(14, 9))
    TL(fr, 29.55, 30.75, "LOWER EGYPT", size=24, sp=4, anchor="r", a=fr.r(12.3, 0.7))

# ================= 2b. Two Lands, the join: 5 s (VO 0:58-1:03)
@scene("02b_two_lands", 5, CAM_JOIN, dict(egy=EGY))
def _(fr, t):
    egypt(fr)
    TL(fr, 31.05, 30.52, "DELTA", size=26, sp=8, anchor="m", color=WHITE, w="b")
    x, y = P(fr.cam, on_river(29.52), 29.52)
    T(fr, x + 78, y, "VALLEY", size=22, sp=7, color=GREEN_D, w="b")
    city(fr, "MEMPHIS", a=fr.r(0.4, 0.5), side="l", r=9, size=30, ring=WHITE, dx=-4)

# ================= 3. The Pyramid Age: 106 s (VO 0:05-1:51, freeze 1:08-1:26 = clip 63-81)
_c3, _a3 = mover([(0, CAM_MEM), (82.5, CAM_MEM), (86.5, CAM_RED), (90.4, CAM_RED), (93.4, CAM_MEM)])
@scene("03_the_pyramid_age", 106, _c3, dict(egy=EGY), active=_a3)
def _(fr, t):
    egypt(fr)
    near = 1 - fr.r(82.3, 0.7) * (1 - fr.r(92.9, 0.6))          # labels that only make sense in the close-up
    fr.plaque(250, 120, "2650 BC", size=32, a=fr.r(0.2, 0.5) * (1 - fr.r(44.0, 0.8)))
    city(fr, "MEMPHIS", side="r", r=6, size=18, dot=WHITE, a=near, dx=64)
    def site(name, t0, r, txt, size, dy=0):
        a = fr.r(t0, 0.5); city(fr, name, a=a, r=r, label="")
        x, y = P(fr.cam, *C[name]); T(fr, x - r - 8, y + dy, txt, size=size, anchor="r", a=a * near)
    site("SAQQARA", 17.0, 8, "STEP PYRAMID", 24); site("MEIDUM", 27.5, 7, "1", 20)
    site("BENT", 36.0, 7, "2 · BENT", 20, 9); site("REDP", 38.5, 7, "3", 20, -9)
    city(fr, "GIZA", a=fr.r(47.0, 0.5), side="l", r=10, size=30, label="GIZA")
    gx, gy = P(fr.cam, *C["GIZA"])
    T(fr, gx - 22, gy + 34, "GREAT PYRAMID", size=18, sp=3, anchor="r", a=fr.r(48.0, 0.6) * near)
    pl = 1 - fr.r(61.0, 0.8)
    fr.plaque(1480, 300, "2.3 MILLION BLOCKS", size=30, a=fr.r(49.5, 0.6) * pl)
    fr.plaque(1480, 372, "146 M", size=30, a=fr.r(53.0, 0.6) * pl)
    # the diary: a cave on the Red Sea, stone ferried down the Nile to Giza
    far = fr.r(86.6, 0.6) * (1 - fr.r(90.2, 0.5))
    modern(fr, 32.95, 28.75, "RED SEA", a=far, size=17, color=(110, 150, 165))
    city(fr, "JARF", a=fr.r(88.0, 0.4) * (1 - fr.r(90.2, 0.5)), side="l", r=8, size=20, label="THE DIARY")
    route = smooth([(31.325, 29.938), (31.285, 29.935), (31.262, 29.95), (31.238, 29.972), (31.20, 29.977), (31.152, 29.978)], 8)
    gline(fr, route, width=4.5, frac=fr.r(94.0, 2.4), arrow=True)
    rx, ry = P(fr.cam, 31.325, 29.938)
    alpha_draw(fr, lambda d, c: d.ellipse([s(rx - 6), s(ry - 6), s(rx + 6), s(ry + 6)], fill=c), INK, fr.r(93.6, 0.4))
    fr.plaque(rx + 190, ry, "200 BLOCKS A MONTH", size=24, a=fr.r(99.0, 0.6), pad=(13, 8))

# ================= 4. The First Collapse: 38 s (VO 0:34-1:12, freeze 0:59-1:09 = clip 25-35)
def gauge(fr, x, y0, y1, level, a):
    if a <= 0: return
    w = 34
    yl = y1 - (y1 - y0) * level
    alpha_draw(fr, lambda d, c: d.rectangle([s(x - w / 2), s(yl), s(x + w / 2), s(y1)], fill=c), FLOOD, a)
    alpha_draw(fr, lambda d, c: d.rectangle([s(x - w / 2), s(y0), s(x + w / 2), s(y1)], outline=c, width=s(3)), INK, a)
    for k in range(1, 8):
        yy = y1 - (y1 - y0) * k / 8
        pline(fr, [(x + w / 2, yy), (x + w / 2 + (16 if k % 2 == 0 else 9), yy)], width=2.2, a=a)
    T(fr, x, y0 - 30, "NILE FLOOD", size=17, sp=4, anchor="m", a=a)
@scene("04_the_first_collapse", 38, COUNTRY, dict(south=B("ASWAN", "ASYUT"), north=U(B("ASYUT", "APEX"), FAY, DEL), gap=B("ABYDOS", "HIBA", wk=1.25)))
def _(fr, t):
    k = fr.masks
    fr.fill(k["south"], GREEN); fr.fill(k["north"], GREEN)
    fr.fill(k["north"], GREEN_L, fr.r(14.0, 1.6))
    fr.fill(k["gap"], SAND, fr.r(35.2, 1.4))
    lvl = 0.86 - 0.58 * fr.r(3.0, 6.0)
    gauge(fr, 430, 330, 700, lvl, fr.r(0.3, 0.6))
    fr.plaque(430, 232, "2200 BC", size=30, a=fr.r(3.0, 0.5))
    TL(fr, 29.6, 30.75, "NORTH", size=22, sp=6, anchor="r", a=fr.r(15.0, 0.7))
    x, y = P(fr.cam, on_river(25.2), 25.2)
    T(fr, x - 34, y, "SOUTH", size=22, sp=6, anchor="r", a=fr.r(15.6, 0.7))

# ================= 5. The Reboot: 54 s (VO 0:10-1:04, freeze 0:26-0:48 = clip 16-38)
_c5, _a5 = mover([(0, COUNTRY), (41.0, COUNTRY), (44.2, CAM_NUB)])
FORTS = [23.16, 22.67, 22.21, 21.91, 21.80, 21.63, 21.55, 21.50]
@scene("05_the_reboot", 54, _c5, dict(south=B("ASWAN", "ASYUT"), north=U(B("ASYUT", "APEX"), FAY, DEL), dl=DEL), active=_a5)
def _(fr, t):
    k = fr.masks
    fr.fill(k["north"], GREEN_L); fr.fill(k["south"], GREEN)
    sweep(fr, "ASYUT", "APEX", fr.r(5.0, 2.2), GREEN); fr.fill(k["dl"], GREEN, fr.r(6.8, 1.2))
    sweep(fr, "ASWAN", "SEMNA", fr.r(41.4, 2.8), GREEN_L)
    fr.plaque(330, 150, "2055 BC", size=32, a=fr.r(0.2, 0.5) * (1 - fr.r(40.6, 0.4)))
    city(fr, "THEBES", a=fr.r(1.0, 0.5), side="l", r=8, size=26, ring=WHITE)
    tx, ty = P(fr.cam, *C["THEBES"]); m = fr.r(10.2, 0.6) * (1 - fr.r(15.2, 0.6))
    T(fr, tx - 20, ty + 38, "MENTUHOTEP", size=20, sp=3, anchor="r", a=m)
    T(fr, tx - 20, ty + 64, "FOUNDER NO. 2", size=15, sp=3, anchor="r", a=m, color=(90, 90, 90), w="m")
    region(fr, 33.9, 22.7, "NUBIA", a=fr.r(44.0, 0.7), size=30, sp=12, color=SAND_D, w="b")
    TL(fr, 33.9, 22.7, "GOLD", dy=36, size=17, sp=6, anchor="m", a=fr.r(44.4, 0.7), color=SAND_D)
    for i, lat in enumerate(FORTS):
        a = fr.r(45.2 + i * 0.32, 0.3); lon = on_river(lat)
        city(fr, "", a=a, ll=(lon, lat), r=6, label="", ring=WHITE)
    lon = on_river(FORTS[-1]); x, y = P(fr.cam, lon, FORTS[-1]); a = fr.r(52.0, 0.5)
    pline(fr, [(x - 12, y + 6), (x - 60, y + 30)], width=2, a=a)
    fr.plaque(x - 236, y + 34, "WARDING OFF THE BOWS", size=22, a=a, pad=(12, 8))

# ================= 6. Foreign Kings: 86 s (VO 0:00-1:26, freeze 0:37-0:49 and 0:57-1:08)
CAM_F6A = cam_box(25.0, 40.0, 27.0, 33.4)
CAM_F6B = cam_box(16, 49, 19.3, 33.2)
_c6, _a6 = mover([(0, CAM_F6A), (49.0, CAM_F6A), (51.4, CAM_F6B), (68.2, CAM_F6B), (70.4, CAM_F6A)])
@scene("06_foreign_kings", 86, _c6, dict(egy=EGY, hyk=U(DEL, B("CUSAE", "APEX"), FAY), dl=DEL, nub=B("ASWAN", "KERMA")), active=_a6 + [(55.0, 56.85)])
def _(fr, t):
    k = fr.masks
    fr.fill(k["nub"], BROWN, fr.r(51.6, 1.0))
    egypt(fr)
    fr.fill(k["hyk"], SLATE, fr.r(15.0, 1.2) * (1 - fr.r(70.8, 1.2)))
    sweep(fr, "CUSAE", "APEX", fr.r(69.4, 1.6), GREEN)
    for i, src in enumerate([(35.7, 33.1), (35.4, 31.9), (35.0, 30.6)]):
        tgt = (32.25 - 0.12 * i, 30.98 - 0.14 * i)
        gline(fr, arc(src, tgt, 0.14 - 0.1 * i), color=SLATE, width=4, frac=fr.r(0.8 + 1.6 * i, 3.4), arrow=True, dash=(10, 7), a=1 - fr.r(14.6, 0.8))
    region(fr, 31.15, 32.35, "HEQA KHASUT", a=fr.r(18.0, 0.5) * (1 - fr.r(22.4, 0.5)), size=30, sp=7, w="b")
    region(fr, 31.15, 32.35, "RULERS OF FOREIGN LANDS", a=fr.r(18.6, 0.5) * (1 - fr.r(22.4, 0.5)), size=15, sp=4, dy=34, color=(90, 90, 90), w="m")
    region(fr, 31.15, 32.35, "HYKSOS", a=fr.r(23.0, 0.5) * (1 - fr.r(70.8, 1.0)), size=34, sp=14, w="b")
    city(fr, "AVARIS", a=fr.r(30.0, 0.5), side="r", r=8, size=24, ring=WHITE, dx=2)
    city(fr, "THEBES", a=fr.r(50.2, 0.5), side="l", r=8, size=24, ring=WHITE)
    if 55.0 <= t <= 56.8: fr.pulse(*C["THEBES"], t, 55.0, color=GREEN_D, n=2, rmax=44, width=3.5)
    region(fr, 33.3, 21.3, "NUBIA", a=fr.r(52.2, 0.6), size=26, sp=9, color=(110, 84, 62), w="b")
    fr.plaque(330, 150, "1550 BC", size=32, a=fr.r(70.6, 0.5))
    chase = smooth([(31.95, 30.83), (32.8, 30.98), (33.8, 31.12), (34.5, 31.42)], 8)
    gline(fr, chase, width=4.6, frac=fr.r(72.0, 2.0), arrow=True)
    region(fr, 35.2, 31.95, "PALESTINE", a=fr.r(73.2, 0.6), size=20, sp=5)


def front(fr, mask, lat):
    """the part of a mask that lies south of a latitude"""
    y = int(round(proj(fr.cam, [(fr.cam[0], lat)])[0][1]))
    m = Image.new("L", mask.size, 0); ImageDraw.Draw(m).rectangle([0, max(0, y), mask.size[0], mask.size[1]], fill=255)
    return IC.multiply(mask, m)
def tri(fr, lon, lat, a=1.0, r=9, color=INK):
    if a <= 0: return
    x, y = P(fr.cam, lon, lat)
    alpha_draw(fr, lambda d, c: d.polygon([(s(x), s(y - r)), (s(x + r), s(y + r * 0.8)), (s(x - r), s(y + r * 0.8))], fill=c), color, a)

# ================= 7. The Empire: 85 s (VO 0:00-1:25, freeze 0:27-0:43 and 0:50-1:00)
CAM_EMP = cam_box(8, 59, 16.2, 37.3)
CAM_TH = cam_box(32.35, 32.95, 25.60, 25.88)
_c7, _a7 = mover([(0, CAM_EMP), (60.0, CAM_EMP), (62.4, CAM_TH)])
@scene("07_the_empire", 85, _c7, dict(egy=EGY, lev=LEV, nub0=B("ASWAN", "BUHEN")), active=_a7)
def _(fr, t):
    k = fr.masks
    lat = 31.25 + (32.75 - 31.25) * fr.r(11.0, 3.6) + (37.2 - 32.75) * fr.r(16.0, 7.0)
    fr.fill(front(fr, k["lev"], lat), GREEN_L)
    fr.fill(k["nub0"], GREEN_L); sweep(fr, "BUHEN", "KURGUS", fr.r(17.0, 7.0), GREEN_L)
    egypt(fr)
    fr.plaque(330, 150, "17 CAMPAIGNS · 20 YEARS", size=30, a=fr.r(11.3, 0.6) * (1 - fr.r(23.4, 0.6)))
    city(fr, "MEGIDDO", a=fr.r(14.2, 0.4) * (1 - fr.r(60.2, 0.5)), side="r", r=6, size=19, ring=WHITE)
    region(fr, 38.9, 36.9, "SYRIA", a=fr.r(24.3, 0.6) * (1 - fr.r(60.2, 0.5)), size=20, sp=6, dx=30)
    modern(fr, 27.6, 19.4, "NOW SUDAN", a=fr.r(25.0, 0.6) * (1 - fr.r(60.2, 0.5)), size=17)
    punt = [(34.3, 26.55), (35.2, 25.0), (36.6, 22.8), (37.9, 20.6), (38.7, 18.9), (38.95, 17.75)]
    gline(fr, smooth(punt, 8), color=(52, 124, 156), width=3.6, frac=fr.r(43.2, 3.2), arrow=True, dash=(9, 6), a=1 - fr.r(60.2, 0.5))
    region(fr, 37.3, 17.25, "PUNT", a=fr.r(45.4, 0.6) * (1 - fr.r(60.2, 0.5)), size=22, sp=8, w="b")
    near = fr.r(62.0, 0.6)
    city(fr, "KARNAK", a=near, side="r", r=11, size=34, label="THEBES", ring=WHITE, dx=4)
    kx, ky = P(fr.cam, *C["KARNAK"])
    T(fr, kx + 24, ky + 38, "KARNAK", size=22, sp=4, a=fr.r(65.0, 0.5) * near)
    city(fr, "KINGS", a=fr.r(83.5, 0.4), side="l", r=9, size=24, label="VALLEY OF THE KINGS", ring=WHITE)

# ================= 8a. The Heretic, the new capital: 5 s (VO 0:26-0:31)
@scene("08a_the_heretic", 5, COUNTRY, dict(egy=EGY), active=[(1.2, 3.6)])
def _(fr, t):
    egypt(fr)
    city(fr, "MEMPHIS", side="l", r=5, size=17, ring=WHITE); city(fr, "THEBES", side="l", r=5, size=17, ring=WHITE)
    a = fr.r(1.2, 0.4)
    if 1.2 <= t <= 3.6: fr.pulse(*C["AMARNA"], t, 1.2, color=INK, n=2, rmax=46, width=3.5)
    city(fr, "AMARNA", a=a, side="l", r=9, size=26, label="", ring=WHITE)
    x, y = P(fr.cam, *C["AMARNA"])
    fr.plaque(x - 150, y, "NEW CAPITAL", size=26, a=fr.r(1.5, 0.5), pad=(14, 9))

# ================= 8b. The Heretic, the inbox: 11 s (VO 0:57-1:08)
CAM_LET = cam_box(21, 47.5, 25.6, 37.6)
LETTERS = [((34.3, 37.9), 0.10), ((39.6, 37.0), 0.10), ((45.6, 33.4), -0.08), ((35.65, 34.1), 0.14), ((35.25, 31.9), 0.2), ((33.3, 35.0), -0.12), ((43.4, 36.3), 0.05)]
@scene("08b_the_heretic", 11, CAM_LET, dict(egy=EGY, lev=LEV))
def _(fr, t):
    fr.fill(fr.masks["lev"], GREEN_L); egypt(fr)
    tgt = np.array(C["AMARNA"])
    for i, (src, bend) in enumerate(LETTERS):
        v = tgt - np.array(src); end = tuple(tgt - v / np.hypot(*v) * 0.42)
        gline(fr, arc(src, end, bend), width=3.2, frac=fr.r(0.5 + 0.55 * i, 2.2), arrow=True, dash=(9, 6), color=(40, 40, 40))
    city(fr, "AMARNA", side="l", r=8, size=22, label="", ring=WHITE)
    fr.plaque(330, 150, "350 LETTERS", size=32, a=fr.r(3.2, 0.6))

# ================= 9a. The Superpower, Kadesh: 22 s (VO 0:16-0:38)
CAM_KAD = cam_box(27.5, 42.5, 29.6, 37.6)
@scene("09a_the_superpower", 22, CAM_KAD, dict(egy=EGY, lev=LEV, hat=HAT))
def _(fr, t):
    k = fr.masks
    fr.fill(front(fr, k["lev"], 34.45), GREEN_L); fr.fill(k["hat"], SLATE_L); egypt(fr)
    fr.plaque(250, 130, "1274 BC", size=32, a=fr.r(0.3, 0.5))
    region(fr, 36.3, 37.3, "HATTI", size=30, sp=12, w="b", color=(60, 72, 80))
    region(fr, 36.3, 37.3, "THE HITTITES", size=15, sp=4, dy=32, color=(60, 72, 80), w="m")
    march = smooth([(31.85, 30.8), (32.7, 31.0), (34.3, 31.33), (34.85, 32.4), (35.2, 33.2), (35.9, 33.9), (36.38, 34.36)], 10)
    gline(fr, march, color=GREEN_D, width=5.5, frac=fr.r(0.6, 5.6), arrow=True)
    city(fr, "KADESH", a=fr.r(6.2, 0.4), side="t", r=8, size=26, ring=WHITE, dy=-4)
    gline(fr, arc((37.55, 35.25), (36.72, 34.42), -0.42), color=SLATE, width=5, frac=fr.r(10.5, 1.6), arrow=True)
    TL(fr, 37.72, 35.3, "AMBUSH", size=17, sp=3, a=fr.r(11.0, 0.5), color=(60, 72, 80))
    gline(fr, arc((35.7, 34.72), (36.3, 34.6), 0.18), color=GREEN_D, width=5, frac=fr.r(15.0, 1.4), arrow=True)
    TL(fr, 35.58, 34.74, "REINFORCEMENTS", size=17, sp=3, anchor="r", a=fr.r(15.4, 0.5), color=GREEN_D)
    x, y = P(fr.cam, *C["KADESH"])
    fr.plaque(x + 215, y + 66, "A DRAW", size=30, a=fr.r(20.0, 0.5))

# ================= 9b. The Superpower, Abu Simbel: 9 s (VO 1:14-1:23)
CAM_ABU = cam_box(28.6, 35.4, 21.5, 24.5)
@scene("09b_the_superpower", 9, CAM_ABU, dict(egy=EGY, nub=B("ASWAN", "SEMNA")), active=[(0.6, 3.0)])
def _(fr, t):
    fr.fill(fr.masks["nub"], GREEN_L); egypt(fr)
    x, y = P(fr.cam, *C["ASWAN"])
    pline(fr, [(x - 150, y), (x + 150, y)], width=2.4, dash=(10, 8), color=(90, 90, 90))
    T(fr, x + 170, y - 20, "EGYPT", size=20, sp=7, color=GREEN_D, w="b"); T(fr, x + 170, y + 22, "NUBIA", size=20, sp=7, color=SAND_D, w="b")
    if 0.6 <= t <= 3.0: fr.pulse(*C["ABU_SIMBEL"], t, 0.6, color=INK, n=2, rmax=46, width=3.5)
    city(fr, "ABU_SIMBEL", a=fr.r(0.6, 0.4), side="l", r=10, size=32, label="ABU SIMBEL", ring=WHITE, dx=-4)

# ================= 9c. The Superpower, the workmen's village: 6 s (VO 1:25-1:31)
_c9c, _a9c = mover([(0, cam_box(32.0, 33.3, 25.40, 26.05)), (1.8, CAM_TH)])
@scene("09c_the_superpower", 6, _c9c, dict(egy=EGY), active=_a9c)
def _(fr, t):
    egypt(fr)
    city(fr, "KARNAK", side="r", r=8, size=22, label="THEBES", ring=WHITE)
    city(fr, "KINGS", a=fr.r(1.6, 0.4), side="l", r=7, size=19, label="VALLEY OF THE KINGS", ring=WHITE, dy=-6)
    path = smooth([C["DEIR"], (32.596, 25.7335), C["KINGS"]], 6)
    gline(fr, path, width=2.6, frac=fr.r(3.6, 1.2), dash=(7, 6), color=(60, 60, 60))
    city(fr, "DEIR", a=fr.r(1.9, 0.4), side="b", r=10, size=30, label="DEIR EL-MEDINA", ring=WHITE, dy=6, dx=-40)

# ================= 10a. The Long Decline, the collapse: 28 s (VO 0:03-0:31)
CAM_SEA = cam_box(19, 48, 28.6, 41.6)
RAID = [smooth([(26.6, 36.6), (29.5, 35.6), (32.2, 34.95), (34.2, 35.2)], 8),
        smooth([(34.9, 36.35), (35.45, 35.0), (35.2, 33.6), (34.55, 32.4), (33.7, 31.75), (32.35, 31.72)], 8),
        smooth([(36.6, 36.3), (36.35, 34.9), (35.75, 33.3), (35.2, 32.2), (34.55, 31.45)], 8)]
@scene("10a_the_long_decline", 28, CAM_SEA, dict(egy=EGY, lev=LEV, hat=HAT))
def _(fr, t):
    k = fr.masks
    fr.fill(k["lev"], GREEN_L, 1 - fr.r(26.0, 1.6)); fr.fill(k["hat"], SLATE_L, 1 - fr.r(5.0, 1.8)); egypt(fr)
    fr.plaque(330, 150, "1177 BC", size=32, a=fr.r(0.3, 0.5))
    region(fr, 34.6, 39.3, "HITTITE EMPIRE", a=1 - fr.r(5.0, 1.4), size=22, sp=6, color=(60, 72, 80), w="b")
    for i, pth in enumerate(RAID):
        gline(fr, pth, color=(40, 40, 40), width=4.6, frac=fr.r(10.0 + 0.5 * i, 3.0), arrow=True)
    region(fr, 29.6, 33.9, "PEOPLES OF THE SEA", a=fr.r(10.4, 0.6), size=20, sp=5, w="b", color=(40, 40, 40))
    x, y = P(fr.cam, 32.0, 31.72); a = fr.r(14.2, 0.4)
    pline(fr, [(x - 8, y - 20), (x - 8, y + 20)], width=7, a=a)
    fr.plaque(x - 132, y - 34, "RAMESSES III", size=22, a=fr.r(14.5, 0.5), pad=(12, 8))
    region(fr, 36.9, 35.9, "SYRIA", a=1 - fr.r(26.0, 1.2), size=17, sp=5, color=GREEN_D, dx=20)

# ================= 10b. The Long Decline, two crowns again: 7 s (VO 1:13-1:20)
@scene("10b_the_long_decline", 7, COUNTRY, dict(south=B("ASWAN", "HIBA"), north=U(B("HIBA", "APEX"), FAY, DEL)))
def _(fr, t):
    k = fr.masks
    fr.fill(k["south"], GREEN); fr.fill(k["north"], GREEN, 1 - fr.r(0.4, 1.2)); fr.fill(k["north"], GREEN_L, fr.r(0.4, 1.2))
    fr.plaque(330, 150, "1070 BC", size=32, a=fr.r(0.2, 0.5))
    city(fr, "THEBES", side="l", r=8, size=26, ring=WHITE)
    x, y = P(fr.cam, *C["THEBES"])
    T(fr, x - 20, y + 36, "HIGH PRIEST OF AMUN", size=16, sp=3, anchor="r", a=fr.r(1.0, 0.6), color=(70, 70, 70), w="m")

# ================= 10c. The Long Decline, Nubian kings and Assyria: 19 s (VO 1:26-1:45, freeze 1:33-1:41 = clip 7-15)
CAM_F10 = cam_box(17, 50, 16.2, 33.4)
ASSYR = smooth([(40.2, 34.6), (37.6, 33.6), (35.6, 32.6), (34.4, 31.35), (32.7, 31.0), (31.45, 30.2)], 8)
@scene("10c_the_long_decline", 19, CAM_F10, dict(egy=EGY, dl=DEL, kush=B("MEROE", "ASWAN")))
def _(fr, t):
    k = fr.masks
    egypt(fr, color=GREEN_L); fr.fill(k["kush"], BROWN)
    sweep(fr, "ASWAN", "APEX", fr.r(0.3, 2.3), BROWN); fr.fill(k["dl"], BROWN, fr.r(2.3, 0.9))
    region(fr, 34.9, 19.6, "NUBIA", size=26, sp=9, color=(110, 84, 62), w="b")
    tri(fr, 31.9, 18.62, fr.r(4.6, 0.4)); tri(fr, 33.72, 17.05, fr.r(5.2, 0.4))
    route = np.vstack([ASSYR, axis_part("APEX", "THEBES")[::25]])
    gline(fr, route, color=(30, 30, 30), width=5, frac=fr.r(15.2, 2.3), arrow=True)
    region(fr, 39.0, 33.2, "ASSYRIA", a=fr.r(15.3, 0.5), size=24, sp=8, w="b", dy=10)
    x, y = P(fr.cam, *C["THEBES"])
    fr.plaque(x - 122, y, "663 BC", size=28, a=fr.r(17.3, 0.5), pad=(13, 8))
    T(fr, x + 22, y, "THEBES", size=20, sp=2, a=fr.r(17.3, 0.5))

# ================= 11a. Other People's Egypt, Persians and Alexander: 26 s (VO 0:08-0:34)
CAM_P = cam_box(18, 53, 22.6, 37.4)
ENTRY = smooth([(36.0, 33.9), (35.1, 32.6), (34.4, 31.35), (32.7, 31.0), (31.6, 30.4), (31.3, 29.9)], 8)
@scene("11a_other_peoples_egypt", 26, CAM_P, dict(egy=EGY, per=PER, egb=EGB))
def _(fr, t):
    k = fr.masks
    gone = 1 - fr.r(15.0, 1.4)
    fr.fill(k["per"], SLATE_L, fr.r(0.2, 1.2) * gone); fr.fill(k["egb"], SLATE_L, fr.r(7.0, 1.4) * gone)
    egypt(fr)
    fr.plaque(330, 150, "525 BC", size=32, a=fr.r(0.3, 0.5) * (1 - fr.r(15.0, 0.5)))
    fr.plaque(330, 150, "332 BC", size=32, a=fr.r(15.6, 0.5))
    region(fr, 41.5, 35.6, "PERSIAN EMPIRE", a=fr.r(0.8, 0.8) * gone, size=24, sp=8, w="b", color=(60, 72, 80))
    gline(fr, ENTRY, color=SLATE, width=5, frac=fr.r(1.2, 2.4), arrow=True, a=gone)
    gline(fr, ENTRY + np.array([0.0, 0.0]), color=(30, 30, 30), width=5, frac=fr.r(15.6, 2.6), arrow=True)
    TL(fr, 36.2, 34.05, "ALEXANDER", size=20, sp=4, a=fr.r(15.8, 0.5), w="b")
    city(fr, "ALEXANDRIA", a=fr.r(19.5, 0.4), side="l", r=8, size=24, ring=WHITE)

# ================= 11b. Other People's Egypt, temples up the river: 13 s (VO 0:53-1:06)
@scene("11b_other_peoples_egypt", 13, COUNTRY, dict(egy=EGY))
def _(fr, t):
    egypt(fr)
    city(fr, "ALEXANDRIA", side="l", r=6, size=19, ring=WHITE)
    for i, n in enumerate(["DENDERA", "ESNA", "EDFU", "KOMOMBO", "PHILAE"]):
        city(fr, n, a=fr.r(0.5 + 0.45 * i, 0.4), r=7, label="", ring=WHITE)
    x, y = P(fr.cam, *C["EDFU"])
    T(fr, x + 30, y - 12, "EGYPTIAN-STYLE TEMPLES", size=19, sp=3, a=fr.r(3.0, 0.6))
    T(fr, x + 30, y + 14, "BUILT UNDER GREEK KINGS", size=15, sp=3, a=fr.r(11.0, 0.6), color=(80, 80, 80), w="m")

# ================= 12a. What Remains, Philae: 16 s (VO 0:23-0:39)
CAM_PHI = cam_box(32.55, 33.2, 23.9, 24.2)
@scene("12a_what_remains", 16, CAM_PHI, dict(egy=EGY), active=[(0.6, 3.0)])
def _(fr, t):
    egypt(fr)
    for i in range(3):
        lat = 24.062 - i * 0.012; x, y = P(fr.cam, on_river(lat), lat)
        pline(fr, [(x - 30, y), (x + 30, y)], width=4, color=(40, 40, 40))
    fr.plaque(300, 150, "24 AUGUST AD 394", size=30, a=fr.r(0.3, 0.5))
    if 0.6 <= t <= 3.0: fr.pulse(*C["PHILAE"], t, 0.6, color=INK, n=2, rmax=50, width=3.5)
    city(fr, "PHILAE", a=fr.r(0.6, 0.4), side="l", r=11, size=36, ring=WHITE, dx=-6)
    x, y = P(fr.cam, *C["PHILAE"])
    T(fr, x - 26, y + 40, "THE LAST HIEROGLYPHS", size=18, sp=3, anchor="r", a=fr.r(9.0, 0.6), color=(60, 60, 60))
    fr.plaque(300, 216, "SILENT FOR 1,400 YEARS", size=24, a=fr.r(13.2, 0.6), pad=(13, 8))

# ================= 12b. What Remains, the ring closes: 37 s (VO 1:00-1:37)
@scene("12b_what_remains", 37, COUNTRY, dict(egy=EGY))
def _(fr, t):
    egypt(fr, fr.r(0.2, 1.2))
    region(fr, 27.6, 28.45, "EGYPT", a=fr.r(1.0, 0.8), size=34, sp=12)
    fr.plaque(P(fr.cam, 27.6, 28.45)[0], P(fr.cam, 27.6, 28.45)[1] + 70, "3,000 YEARS", size=34, a=fr.r(1.8, 0.6))
    region(fr, 26.6, 25.6, "DESHRET", a=fr.r(6.4, 0.8), size=26, sp=11, color=SAND_D, w="b")
    region(fr, 32.7, 27.9, "DESHRET", a=fr.r(6.4, 0.8), size=18, sp=5, color=SAND_D, w="b")
    TL(fr, 31.13, 31.02, "KEMET", size=30, w="b", color=WHITE, sp=5, anchor="m", a=fr.r(5.2, 0.8))

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
