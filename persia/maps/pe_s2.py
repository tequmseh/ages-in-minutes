"""Persia map scenes, chapters 4-8"""
from pe_base import *
def tag(fr, lon, lat, top, under=None, a=1.0, au=None, dx=0, dy=0, size=20):
    """black name plaque with a light line under it"""
    x, y = P(fr.cam, lon, lat)
    PQ(fr, x + dx, y + dy, top, a=a, size=size, pad=(11, 7))
    if under: PQ(fr, x + dx, y + dy + size * 2.15, under, a=a if au is None else au, size=size * 0.8, pad=(10, 6), light=True)
def mover_dot(fr, path_px, q, r=8, a=1.0, fill=WHITE, ring=INK):
    p = partial(np.asarray(path_px, float), min(max(q, 0.0), 1.0))[-1]
    alpha_draw(fr, lambda d, c: d.ellipse([s(p[0] - r - 2.5), s(p[1] - r - 2.5), s(p[0] + r + 2.5), s(p[1] + r + 2.5)], fill=c), ring, a)
    alpha_draw(fr, lambda d, c: d.ellipse([s(p[0] - r), s(p[1] - r), s(p[0] + r), s(p[1] + r)], fill=c), fill, a)

# ================= 4a. VO 4.6-25.5: provinces, satraps, silver
_SRC = [(28.5, 38.6), (33.5, 39.5), (38.5, 35.2), (31.0, 28.5), (42.0, 39.5), (44.4, 32.6), (56.5, 37.0), (60.5, 30.5), (66.5, 37.0), (70.5, 30.0), (63.5, 41.0), (36.0, 32.5)]
@scene("04a_satrapies", 4, 4.6, 25.6, FULL, dict(emp=CORE, x_grid=GRIDM), res="50")
def _(fr, t):
    terr(fr, "emp", PER); mfill(fr, fr.masks["x_grid"], WHITE, fr.R(4.8, 2.6))
    live(fr, 15.0, 21.2)
    hub = C["SUSA"]
    for i, ll in enumerate(_SRC):                                   # silver travelling to the centre
        a = fr.R(15.0 + 0.1 * i, 0.4)
        if a <= 0: continue
        path = proj(fr.cam, arc(ll, hub, 0.12 if i % 2 else -0.12), 1)
        pline(fr, path, color=WHITE, width=1.8, a=0.55 * a * (1 - fr.R(20.6, 0.6)))
        for k in range(3):
            q = ((t - 15.0 - 0.1 * i) / 2.4 + k / 3.0) % 1.0
            if t < 20.9: mover_dot(fr, path, q, r=4.5, a=a * min(1.0, (1 - q) * 4), fill=(226, 226, 230), ring=INK)
    city(fr, "", ll=hub, a=fr.R(15.0, 0.4), r=8, label="")
    PQ(fr, 960, 104, "SATRAP", a=fr.R(8.0, 0.5), size=36)
    PQ(fr, 960, 170, "A GOVERNOR FOR EVERY PROVINCE", a=fr.R(8.4, 0.5), size=20, light=True)
    PQ(fr, 330, 104, "20 PROVINCES", a=fr.R(13.4, 0.5), size=30)
    PQ(fr, 1560, 104, "A FIXED AMOUNT OF SILVER", a=fr.R(15.4, 0.5), size=26)
    PQ(fr, 1560, 166, "A NUMBER, WRITTEN DOWN", a=fr.R(19.4, 0.5), size=20, light=True)
    PQ(fr, 700, 930, "CYRUS: A FATHER", a=fr.R(22.3, 0.5), size=28); PQ(fr, 1220, 930, "DARIUS: A SHOPKEEPER", a=fr.R(24.0, 0.5), size=28)

# ================= 4b. VO 26.0-36.3: who watches the satraps
CAM_W = cam_box(24.5, 52.5, 28.6, 42.4)
_SEATS = [("SARDIS", (29.3, 37.75)), ("BABYLON", (43.5, 33.6)), ("MEMPHIS", (30.6, 28.9)), ("ECBATANA", (49.6, 35.6))]
@scene("04b_kings_eyes", 4, 26.0, 36.4, CAM_W, dict(emp=CORE, x_grid=GRIDM), res="50")
def _(fr, t):
    terr(fr, "emp", PER); mfill(fr, fr.masks["x_grid"], WHITE, 0.55)
    live(fr, 31.4, 34.0)
    for i, (n, fort) in enumerate(_SEATS):
        gline(fr, [fort, C["SUSA"]], color=INK, width=3.4, frac=fr.R(29.9 + 0.12 * i, 0.9), halo=WHITE)
        x, y = P(fr.cam, *fort); a = fr.R(28.4 + 0.1 * i, 0.4)
        alpha_draw(fr, lambda d, c, x=x, y=y: d.rectangle([s(x - 8), s(y - 8), s(x + 8), s(y + 8)], fill=c), INK, a)
        alpha_draw(fr, lambda d, c, x=x, y=y: d.rectangle([s(x - 8), s(y - 8), s(x + 8), s(y + 8)], outline=c, width=s(2.5)), WHITE, a)
        city(fr, n, r=7, label="", a=fr.R(26.4, 0.4))
        if t >= 31.4:                                                # inspectors leave the king
            path = proj(fr.cam, arc(C["SUSA"], C[n], 0.2), 1); q = ease((t - 31.4 - 0.15 * i) / 2.0)
            if 0 < q < 1.0 or t < 36.4: mover_dot(fr, path, q, r=6, a=fr.R(31.4, 0.3), fill=WHITE, ring=INK)
    city(fr, "SUSA", r=10, label="", ring=WHITE)
    tag(fr, *C["SUSA"], "THE KING", dx=96, dy=40, size=22)
    tag(fr, *C["SARDIS"], "SATRAP", dx=-10, dy=-44, a=fr.R(26.4, 0.4), size=20)
    tag(fr, *_SEATS[0][1], "FORTRESS COMMANDER", dx=10, dy=44, a=fr.R(28.4, 0.4), size=18)
    PQ(fr, 960, 104, "STRAIGHT TO THE KING", a=fr.R(29.9, 0.5) * (1 - fr.R(34.6, 0.4)), size=28)
    PQ(fr, 960, 104, "THE KING'S EYES", a=fr.R(35.0, 0.5), size=34)
    PQ(fr, 960, 172, "ROYAL INSPECTORS, WITHOUT WARNING", a=fr.R(31.6, 0.5), size=20, light=True)

# ================= 4c. VO 42.7-57.6: three languages, three jobs
@scene("04c_languages", 4, 42.7, 57.7, FULL, dict(emp=CORE, x_grid=GRIDM, x_parsa=I(CORE, PARSA)), res="50")
def _(fr, t):
    terr(fr, "emp", PER); mfill(fr, fr.masks["x_grid"], WHITE, 0.45)
    mfill(fr, fr.masks["x_parsa"], PER_D, fr.R(51.0, 0.8))
    region(fr, 46.0, 36.6, "ARAMAIC", a=fr.R(45.5, 0.7), size=64, sp=34, color=WHITE, w="b")
    region(fr, 46.0, 36.6, "PAPERWORK ACROSS THE PROVINCES", a=fr.R(43.0, 0.7), size=17, sp=6, color=WHITE, dy=-58)
    region(fr, 46.0, 36.6, "THE LANGUAGE MOST CLERKS ALREADY KNOW", a=fr.R(48.3, 0.7), size=17, sp=6, color=WHITE, dy=58)
    city(fr, "PERSEPOLIS", a=fr.R(51.3, 0.4), r=8, label=""); pulse(fr, C["PERSEPOLIS"], 51.3, 2.0, color=WHITE, rmax=40)
    tag(fr, *C["PERSEPOLIS"], "THE CAPITAL", dx=0, dy=-46, a=fr.R(51.3, 0.4), size=20)
    PQL(fr, *C["PERSEPOLIS"], "ELAMITE: THE ACCOUNTS", dx=210, dy=24, a=fr.R(53.0, 0.5), size=22, anchor="m", light=True)
    PQL(fr, *C["PERSEPOLIS"], "PERSIAN: FOR MONUMENTS", dx=210, dy=78, a=fr.R(56.7, 0.5), size=22, anchor="m", light=True)

# ================= 4d. VO 58.2-72.1: nobody is asked to become Persian
@scene("04d_stay_different", 4, 58.2, 72.2, FULL, dict(emp=CORE, x_egy=EGY, x_bab=I(CORE, BABCORE_W := [(41.5, 35.2), (46.2, 34.4), (48.2, 31.2), (47.2, 29.8), (44.6, 30.6), (42.0, 32.2)]), x_jud=M(JUDEA), x_ion=ION), res="50")
def _(fr, t):
    terr(fr, "emp", PER)
    for key, col, t0 in (("x_egy", EGY_C, 61.4), ("x_bab", BAB_C, 66.5), ("x_jud", GOLD, 68.2), ("x_ion", GREEK, 69.6)): mfill(fr, fr.masks[key], col, fr.R(t0, 0.8) * 0.8)
    PQ(fr, 960, 104, "NOBODY IS ASKED TO BECOME PERSIAN", a=fr.R(58.5, 0.5), size=30)
    tag(fr, 29.4, 27.8, "EGYPT", "KEEPS ITS PHARAOH", a=fr.R(61.4, 0.4), dx=-40, dy=-10, size=22)
    PQL(fr, 29.4, 27.8, "DARIUS, IN EGYPTIAN DRESS", dx=-40, dy=76, a=fr.R(63.9, 0.5), size=15, pad=(9, 6), light=True)
    tag(fr, 45.2, 32.6, "BABYLON", "KEEPS ITS TEMPLES", a=fr.R(66.5, 0.4), dx=20, dy=30, size=22)
    tag(fr, 35.1, 31.7, "JUDEA", "ITS LAW", a=fr.R(68.2, 0.4), dx=84, dy=-40, size=22)
    tag(fr, 27.0, 38.2, "THE GREEK CITIES", "THEIR OWN LOCAL RULERS", a=fr.R(69.6, 0.4), dx=-96, dy=-78, size=20)

# ================= 5a. VO 0-34.2: distance, the road, the relay
_ROAD = ROYAL_ROAD[::-1]                       # Susa -> Sardis
_OLD = smooth([(44.3, 35.3), (43.5, 36.4), (42.2, 37.2), (40.2, 37.9), (38.3, 38.35)])
@scene("05a_the_road", 5, 0.0, 34.3, CAM_W, dict(emp=CORE), res="50")
def _(fr, t):
    terr(fr, "emp", PER)
    live(fr, 28.6, 33.6)
    gline(fr, _ROAD, width=5, frac=fr.R(6.9, 2.2), color=WHITE)
    gline(fr, _ROAD, width=2.2, frac=fr.R(6.9, 2.2), color=INK)
    gline(fr, _OLD, width=8, color=INK, a=fr.R(16.9, 0.6) * (1 - fr.R(21.8, 0.6)) * 0.85)
    PQL(fr, 41.6, 37.5, "MUCH OF IT OLDER THAN THE PERSIANS", dx=30, dy=-56, a=fr.R(17.4, 0.5) * (1 - fr.R(21.8, 0.5)), size=20, pad=(10, 7))
    sa = fr.R(24.3, 3.2)
    if sa > 0:
        pr = proj(fr.cam, _ROAD, 1)
        for q in np.linspace(0, 1, 111)[:int(round(111 * sa))]:
            p = partial(pr, q)[-1]
            fr.d.ellipse([s(p[0] - 4.2), s(p[1] - 4.2), s(p[0] + 4.2), s(p[1] + 4.2)], fill=WHITE, outline=INK, width=s(1.5))
    if 28.6 <= t <= 33.6:                                             # the message, Sardis -> Susa, station to station
        q = (t - 28.6) / 5.0; mover_dot(fr, proj(fr.cam, ROYAL_ROAD, 1), q, r=11, fill=INK, ring=WHITE)
    city(fr, "SUSA", a=fr.R(6.8, 0.5), side="r", r=9, size=28, color=WHITE); city(fr, "SARDIS", a=fr.R(8.3, 0.5), side="l", r=9, size=28, color=WHITE)
    TL(fr, *C["SUSA"], "THE CAPITAL", dx=20, dy=30, size=14, sp=3, color=WHITE, a=fr.R(6.4, 0.5), w="m")
    TL(fr, *C["SARDIS"], "THE WESTERN END", dx=-20, dy=30, size=14, sp=3, color=WHITE, a=fr.R(7.7, 0.5), anchor="r", w="m")
    PQ(fr, 960, 104, "DISTANCE", a=fr.R(5.0, 0.4) * (1 - fr.R(9.0, 0.4)), size=40)
    PQ(fr, 960, 104, "2,700 KM", a=fr.R(9.3, 0.5), size=36)
    PQ(fr, 960, 172, "3 MONTHS ON FOOT", a=fr.R(12.6, 0.5), size=24, light=True)
    PQ(fr, 1530, 104, "MORE THAN 100 STATIONS", a=fr.R(24.3, 0.5), size=26)
    PQ(fr, 1530, 166, "FRESH HORSES, FRESH RIDERS", a=fr.R(26.0, 0.5), size=19, light=True)
    PQ(fr, 1530, 228, "ABOUT 9 DAYS", a=fr.R(32.9, 0.5), size=30)

# ================= 5c. VO 51.8-69.3: the canal
CAM_SUEZ = cam_at(32.1, 30.25, 250)
_SHIP = np.vstack([CANAL, smooth([(32.55, 29.95), (32.7, 29.4), (33.1, 28.7), (33.7, 27.9)], 8)])
@scene("05c_canal", 5, 51.8, 69.4, CAM_SUEZ, dict(emp=CORE), res="10")
def _(fr, t):
    terr(fr, "emp", PER)
    live(fr, 61.7, 65.0)
    TL(fr, 31.05, 29.35, "THE NILE", size=20, sp=5, color=WHITE, anchor="r", a=fr.R(53.5, 0.5), w="b")
    TL(fr, 33.3, 28.75, "RED SEA", dx=16, size=20, sp=5, color=WHITE, a=fr.R(54.2, 0.5), w="b")
    region(fr, 29.6, 29.9, "EGYPT", a=fr.R(52.0, 0.5), size=30, sp=10, color=WHITE, w="b")
    gline(fr, CANAL, width=9, frac=fr.R(54.6, 2.4), color=WHITE); gline(fr, CANAL, width=5, frac=fr.R(54.6, 2.4), color=look_river())
    PQL(fr, 31.95, 30.56, "DARIUS' CANAL", dy=-48, a=fr.R(55.2, 0.5), size=26)
    for i, (txt, t0) in enumerate((("“I ORDERED THIS CANAL DUG.", 58.7), ("IT WAS DUG.", 60.7), ("SHIPS WENT FROM EGYPT TO PERSIA.”", 61.7))):
        PQ(fr, 120, 180 + 64 * i, txt, a=fr.R(t0, 0.4), size=26, anchor="l", light=True)
    if 61.7 <= t <= 65.0:
        for k in range(3): mover_dot(fr, proj(fr.cam, _SHIP, 1), (t - 61.7 - 0.5 * k) / 2.6, r=7, fill=WHITE, ring=INK, a=1.0 if (t - 61.7 - 0.5 * k) > 0 else 0)
    a2 = fr.R(65.3, 0.8)
    gline(fr, [(32.31, 31.27), (32.34, 30.6), (32.56, 29.95)], color=INK, width=3, dash=(9, 7), a=a2)
    PQL(fr, 32.34, 30.9, "SUEZ CANAL", dx=170, dy=70, a=fr.R(66.0, 0.5), size=22, pad=(11, 7))
    PQL(fr, 32.34, 30.9, "2,000 YEARS LATER", dx=170, dy=118, a=fr.R(67.3, 0.5), size=17, pad=(10, 6), light=True)
def look_river(): return engine.RIVER

# ================= 6a. VO 0-8.3: a new capital in the homeland
CAM_PARSA = cam_box(48.6, 57.4, 27.3, 32.6)
_c = mover([(0.0, FULL), (1.6, FULL), (5.0, CAM_PARSA)])
@scene("06a_persepolis", 6, 0.0, 8.4, _c, dict(emp=CORE, x_parsa=I(CORE, PARSA)), res="10")
def _(fr, t):
    terr(fr, "emp", PER); mfill(fr, fr.masks["x_parsa"], PER_D, fr.R(1.6, 1.2) * 0.9)
    region(fr, 52.6, 28.6, "THE PERSIAN HOMELAND", a=fr.R(4.6, 0.6), size=22, sp=8, color=WHITE)
    city(fr, "PERSEPOLIS", a=fr.R(2.6, 0.4), r=11, label=""); pulse(fr, C["PERSEPOLIS"], 2.6, 3.0, color=WHITE, rmax=60, width=4)
    PQL(fr, *C["PERSEPOLIS"], "A NEW CEREMONIAL CAPITAL", dy=-62, a=fr.R(3.0, 0.5) * (1 - fr.R(6.9, 0.4)), size=24)
    PQL(fr, *C["PERSEPOLIS"], "PERSEPOLIS", dy=-66, a=fr.R(7.2, 0.4), size=40)

# ================= 6b. VO 41.7-58.1: the palace is a map of the empire
_MAT = [("CEDAR", "LEBANON", C["LEBANON"], 45.2, 0.16, (-10, -40)), ("GOLD", "SARDIS", C["SARDIS"], 47.0, 0.14, (0, -40)), ("GOLD", "BACTRIA", C["BACTRA"], 48.0, -0.16, (0, -40)),
        ("IVORY", "AFRICA", (32.6, 24.2), 49.4, 0.14, (-110, 0)), ("IVORY", "INDIA", (70.4, 28.6), 50.4, -0.14, (-20, 44))]
_CRAFT = [("GREEK STONECUTTERS", (27.3, 37.3), 51.2, (-20, 40)), ("EGYPTIAN GOLDSMITHS", (31.2, 30.0), 52.6, (-150, 4)), ("BABYLONIAN BRICKMAKERS", C["BABYLON"], 54.1, (-60, 44))]
@scene("06b_materials", 6, 41.7, 58.2, FULL, dict(emp=CORE), res="50")
def _(fr, t):
    terr(fr, "emp", PER)
    for word, place, ll, t0, bend, off in _MAT: gline(fr, arc(ll, C["SUSA"], bend), width=3.6, frac=fr.R(t0, 1.2), arrow=True, halo=WHITE)
    for word, ll, t0, off in _CRAFT: gline(fr, arc(ll, C["SUSA"], 0.07), color=WHITE, width=2.4, frac=fr.R(t0, 1.0), dash=(8, 6), arrow=True)
    for word, place, ll, t0, bend, off in _MAT:
        city(fr, "", ll=ll, a=fr.R(t0, 0.4), r=5, label=""); PQL(fr, *ll, f"{word} · {place}", dx=off[0], dy=off[1], size=19, a=fr.R(t0, 0.5), pad=(10, 6))
    for word, ll, t0, off in _CRAFT:
        city(fr, "", ll=ll, a=fr.R(t0, 0.4), r=4, label=""); PQL(fr, *ll, word, dx=off[0], dy=off[1], size=15, a=fr.R(t0, 0.5), pad=(9, 6), light=True)
    city(fr, "SUSA", side="b", r=9, size=26, dy=4, color=WHITE, a=fr.R(41.8, 0.4))
    PQ(fr, 960, 104, "WHO BUILT HIS PALACE", a=fr.R(43.2, 0.5) * (1 - fr.R(55.9, 0.4)), size=28)
    PQ(fr, 960, 104, "THE PALACE IS A MAP OF THE EMPIRE", a=fr.R(56.1, 0.5), size=30)

# ================= 7a. VO 25.0-64.8: the Ionian revolt
CAM_ION = cam_box(21.6, 30.4, 35.9, 40.7)
CAM_LADE = cam_box(26.3, 28.3, 37.0, 38.1)
_c = mover([(25.0, CAM_ION), (45.0, CAM_ION), (47.4, CAM_LADE), (57.2, CAM_LADE), (60.4, FULL)])
_GK = [(27.02 + 0.05 * (i % 4), 37.60 - 0.045 * (i // 4)) for i in range(12)]
@scene("07a_ionian_revolt", 7, 25.0, 64.9, _c, dict(emp=MAXE, ion=ION), res="10")
def _(fr, t):
    near = 1 - fr.R(57.2, 0.8); far = fr.R(59.6, 0.8); wide = 1 - fr.R(45.0, 0.6)
    reb = fr.R(27.0, 1.0) * (1 - fr.R(55.9, 1.4))
    terr(fr, "emp", PER); terr(fr, "ion", GREEK, reb, border=False)
    live(fr, 50.9, 53.4)
    gline(fr, arc(C["ATHENS"], (26.95, 37.9), -0.16), color=GREEK, width=4, frac=fr.R(37.0, 1.6), arrow=True, halo=WHITE, a=near * wide)
    PQL(fr, 25.2, 38.4, "20 SHIPS", dy=-30, a=fr.R(37.4, 0.4) * near * wide, size=20, pad=(10, 7))
    city(fr, "ATHENS", a=fr.R(36.8, 0.4) * near * wide, side="l", r=7, size=24)
    city(fr, "MILETUS", a=fr.R(30.9, 0.4) * near, side="r", r=8, size=24, color=WHITE, dy=18, dx=-4); pulse(fr, C["MILETUS"], 31.0, 2.4, color=WHITE, rmax=44)
    PQL(fr, *C["MILETUS"], "ARISTAGORAS", dx=150, dy=58, a=fr.R(32.6, 0.4) * (1 - fr.R(45.2, 0.4)) * near, size=18, pad=(10, 6))
    PQL(fr, *C["MILETUS"], "“NOW A DEMOCRACY”", dx=150, dy=100, a=fr.R(34.6, 0.4) * (1 - fr.R(45.2, 0.4)) * near, size=16, pad=(9, 6), light=True)
    city(fr, "SARDIS", a=fr.R(39.2, 0.4) * near, side="r", r=8, size=24, color=WHITE); pulse(fr, C["SARDIS"], 39.0, 3.0, color=(255, 226, 170), rmax=54, width=4)
    PQL(fr, *C["SARDIS"], "BURNED", dy=-44, a=fr.R(39.2, 0.4) * near * wide, size=20, pad=(10, 7))
    TL(fr, *C["SARDIS"], "THE PROVINCIAL CAPITAL", dx=20, dy=30, size=13, sp=3, color=WHITE, a=fr.R(40.5, 0.5) * near * wide, w="m")
    region(fr, 26.3, 39.25, "GREEK CITIES", a=fr.R(27.0, 0.5) * near * reb * wide, size=16, sp=4, color=INK, dx=-150)
    modern(fr, 29.0, 37.25, "THE TURKISH COAST", a=fr.R(27.9, 0.6) * near * wide, size=14, color=(240, 226, 214))
    # Lade
    la = fr.R(47.6, 0.5) * near
    for i, ll in enumerate(_GK):
        sam = i % 4 == 0 or i in (5, 10); q = ease((t - 50.9 - 0.08 * i) / 2.0) if sam else 0.0
        lon = ll[0] + (26.72 + 0.04 * (i % 3) - ll[0]) * q; lat = ll[1] + (37.64 + 0.03 * (i // 4) - ll[1]) * q; x, y = P(fr.cam, lon, lat)
        alpha_draw(fr, lambda d, c, x=x, y=y: d.ellipse([s(x - 9), s(y - 9), s(x + 9), s(y + 9)], fill=c), WHITE, la * (1 - fr.R(53.6, 0.6)))
        alpha_draw(fr, lambda d, c, x=x, y=y: d.ellipse([s(x - 9), s(y - 9), s(x + 9), s(y + 9)], outline=c, width=s(2.5)), INK, la * (1 - fr.R(53.6, 0.6)))
    cross(fr, 26.98, 37.50, a=la * fr.R(48.2, 0.4), r=14, width=5.5)
    TL(fr, 26.98, 37.50, "LADE", dx=-26, dy=6, size=30, anchor="r", a=fr.R(48.4, 0.4) * near)
    PQL(fr, 27.08, 37.42, "THE GREEK FLEET", dx=0, dy=0, a=fr.R(49.1, 0.4) * (1 - fr.R(53.6, 0.5)) * near, size=18, pad=(10, 6))
    TL(fr, 26.8, 37.93, "THE SAMIANS SAIL AWAY", dx=0, dy=0, size=20, sp=2, anchor="m", a=fr.R(50.9, 0.5) * (1 - fr.R(54.0, 0.5)) * near, w="m")
    PQL(fr, *C["MILETUS"], "TAKEN", dx=110, dy=62, a=fr.R(55.9, 0.4) * near, size=22, pad=(11, 7))
    PQ(fr, 300, 104, "499 BC", a=fr.R(25.3, 0.4) * (1 - fr.R(45.4, 0.3)), size=34); PQ(fr, 300, 104, "494 BC", a=fr.R(45.7, 0.4) * near, size=34)
    PQ(fr, 300, 172, "THE GREEK CITIES REFUSE", a=fr.R(27.0, 0.5) * (1 - fr.R(42.2, 0.3)), size=20, light=True)
    PQ(fr, 300, 172, "6 YEARS TO CRUSH THEM", a=fr.R(43.0, 0.5) * near, size=20, light=True)
    # the survivors
    path = smooth([C["MILETUS"], (30.5, 37.9), (34.5, 37.4), (38.5, 36.9), (42.0, 35.6), (44.6, 33.6), (46.6, 31.8), C["AMPE"]])
    gline(fr, path, color=WHITE, width=3.4, frac=fr.R(60.2, 2.6), dash=(11, 8), arrow=True, a=far)
    city(fr, "", ll=C["MILETUS"], a=far, r=5, label=""); TL(fr, *C["MILETUS"], "MILETUS", dx=-12, dy=-18, size=15, anchor="r", a=far)
    sea(fr, 51.2, 26.6, "PERSIAN GULF", a=fr.R(62.2, 0.5), size=16)
    PQL(fr, *C["AMPE"], "THE SURVIVORS", dx=0, dy=-46, a=fr.R(62.6, 0.5), size=20, pad=(10, 7))
    PQ(fr, 960, 104, "THE FAR END OF THE EMPIRE", a=fr.R(63.3, 0.5), size=26)

# ================= 7b. VO 65.6-96.2: Mardonius installs democracies; Athens is not forgotten
_ION6 = [((27.28, 37.53), "r"), ((27.34, 37.94), "r"), ((27.14, 38.42), "r"), ((26.75, 38.67), "l"), ((26.95, 39.10), "r"), ((26.14, 38.37), "l")]
@scene("07b_mardonius", 7, 65.6, 96.2, CAM_ION, dict(emp=MAXE), res="10")
def _(fr, t):
    terr(fr, "emp", PER)
    sw = fr.R(76.0, 1.0)
    for i, (ll, side) in enumerate(_ION6):
        a = fr.R(72.5 + 0.1 * i, 0.4)
        city(fr, "", ll=ll, a=a, r=6, label="", dot=mix(GREEK, INK, sw))
        x, y = P(fr.cam, *ll); dx = 70 if side == "r" else -70
        PQ(fr, x + dx, y, "TYRANT", a=a * (1 - sw), size=14, pad=(8, 5)); PQ(fr, x + dx + (14 if side == "r" else -14), y, "DEMOCRACY", a=a * sw, size=14, pad=(8, 5), light=True)
    city(fr, "SARDIS", a=fr.R(68.6, 0.4), side="r", r=7, size=20, label="", color=WHITE)
    tag(fr, *C["SARDIS"], "MARDONIUS", "THE PERSIAN GENERAL", a=fr.R(69.2, 0.4), au=fr.R(68.4, 0.4), dx=250, dy=-96, size=22)
    PQ(fr, 300, 104, "492 BC", a=fr.R(66.5, 0.4), size=34)
    PQ(fr, 300, 172, "THE TYRANTS REMOVED", a=fr.R(73.1, 0.5), size=20, light=True)
    PQ(fr, 300, 228, "DEMOCRACIES INSTEAD", a=fr.R(76.4, 0.5), size=20, light=True)
    PQ(fr, 1240, 940, "NO IDEOLOGY EXCEPT WHAT WORKS", a=fr.R(85.2, 0.5) * (1 - fr.R(88.6, 0.4)), size=28)
    city(fr, "ATHENS", a=fr.R(89.9, 0.4), side="l", r=9, size=30); pulse(fr, C["ATHENS"], 90.3, 5.6, color=PER_D, rmax=60, width=4, n=3, period=1.3)
    PQL(fr, *C["ATHENS"], "DARIUS HAS NOT FORGOTTEN", dx=-40, dy=62, a=fr.R(89.0, 0.5), size=20, pad=(10, 7))
    PQL(fr, *C["ATHENS"], "A REMINDER, 3 TIMES A DAY", dx=-40, dy=110, a=fr.R(93.6, 0.5), size=17, pad=(10, 6), light=True)

# ================= 8a. VO 0-27.0: Marathon; Darius dies; Xerxes
_V8a = cam_at(23.95, 38.02, 700); _V8b = cam_at(31.5, 34.2, 58)
_c = mover([(0.0, _V8a), (9.6, _V8a), (12.6, _V8b)])
@scene("08a_marathon", 8, 0.0, 27.0, _c, dict(emp=MAXE, mac=MAC), res="10")
def _(fr, t):
    terr(fr, "emp", PER); terr(fr, "mac", PER_L)
    near = 1 - fr.R(9.6, 0.8); far = fr.R(11.8, 0.8)
    gline(fr, smooth([(24.25, 38.42), (24.12, 38.3), (24.03, 38.19)]), color=PER_D, width=6, frac=fr.R(1.9, 1.4), arrow=True, a=near, halo=WHITE)
    TL(fr, 24.25, 38.42, "A PERSIAN FORCE LANDS", dx=14, dy=-18, size=18, sp=2, a=fr.R(1.9, 0.5) * near, color=PER_D)
    city(fr, "MARATHON", a=fr.R(3.0, 0.4) * near, side="l", r=9, size=30, dy=-6); city(fr, "ATHENS", a=fr.R(4.6, 0.4) * near, side="l", r=9, size=30)
    gline(fr, [C["MARATHON"], (23.85, 38.06), C["ATHENS"]], color=CHAR, width=3.4, frac=fr.R(4.0, 1.0), dash=(10, 8), a=near)
    TL(fr, 23.86, 38.07, "A DAY'S MARCH", dx=20, dy=14, size=19, w="m", color=CHAR, sp=2.5, a=fr.R(4.2, 0.5) * near)
    cross(fr, 24.0, 38.165, a=fr.R(5.6, 0.4) * near, r=12, width=5)
    PQ(fr, 300, 104, "490 BC", a=fr.R(0.3, 0.4), size=34)
    PQ(fr, 300, 172, "PERSIA LOSES", a=fr.R(5.6, 0.4) * near, size=22, light=True)
    PQ(fr, 1500, 104, "FOR ATHENIANS: A FOUNDING LEGEND", a=fr.R(7.1, 0.5) * near, size=22)
    # the view from Persia
    empire_label(fr, far, lon=40.5, lat=36.6, size=24)
    city(fr, "ATHENS", a=far, side="l", r=5, size=16)
    PQ(fr, 1500, 104, "FOR PERSIA: A DISTANT FRONTIER", a=fr.R(12.4, 0.5), size=22)
    pulse(fr, C["MEMPHIS"], 16.5, 6.0, color=WHITE, rmax=52, width=3.5); region(fr, 27.6, 28.6, "EGYPT", a=far, size=22, sp=6, color=WHITE, w="b")
    PQL(fr, *C["MEMPHIS"], "EGYPT REVOLTS", dx=40, dy=-52, a=fr.R(16.5, 0.4), size=22, pad=(11, 7))
    city(fr, "", ll=C["PERSEPOLIS"], a=fr.R(18.1, 0.4), r=7, label="")
    PQL(fr, *C["PERSEPOLIS"], "DARIUS DIES", dy=-44, a=fr.R(18.4, 0.4) * (1 - fr.R(19.9, 0.3)), size=22, pad=(11, 7))
    PQL(fr, *C["PERSEPOLIS"], "XERXES", dy=-44, a=fr.R(20.1, 0.4), size=26)
    PQ(fr, 1500, 166, "THE PREPARATIONS TAKE YEARS", a=fr.R(23.2, 0.5), size=19, light=True)

# ================= 8b. VO 27.4-57.3: two bridges and a canal
CAM_HEL = cam_at(26.40, 40.215, 2500); CAM_ATH = cam_at(23.97, 40.345, 1700)
_c = mover([(27.4, CAM_HEL), (41.0, CAM_HEL), (44.0, CAM_ATH)])
def _bridge(fr, lon, lat, frac, a=1.0):
    bar(fr, lon, lat, 128, length=74, width=11, frac=frac, a=a, color=WHITE); bar(fr, lon, lat, 128, length=70, width=6, frac=frac, a=a, color=INK)
@scene("08b_engineering", 8, 27.4, 57.4, _c, dict(emp=MAXE), res="10")
def _(fr, t):
    terr(fr, "emp", PER)
    h = 1 - fr.R(41.0, 0.8); at = fr.R(43.2, 0.8)
    T(fr, 770, 800, "HELLESPONT", size=24, sp=6, w="m", color=SEA_T, anchor="m", a=fr.R(27.9, 0.5) * h)
    region(fr, 26.30, 40.26, "EUROPE", a=h * 0, size=20, color=WHITE); 
    wreck = 1 - fr.R(34.0, 0.9)
    _bridge(fr, 26.392, 40.196, fr.R(30.9, 1.4), wreck * h); _bridge(fr, 26.404, 40.2035, fr.R(31.5, 1.4), wreck * h)
    pulse(fr, (26.40, 40.2), 34.0, 3.0, color=WHITE, rmax=90, width=4)
    _bridge(fr, 26.392, 40.196, fr.R(39.8, 1.0), h); _bridge(fr, 26.404, 40.2035, fr.R(40.2, 1.0), h)
    PQ(fr, 1380, 330, "TWO BRIDGES OF BOATS", a=fr.R(31.1, 0.5) * h, size=30)
    PQ(fr, 1380, 400, "MORE THAN A KILOMETRE OF OPEN WATER", a=fr.R(28.7, 0.5) * (1 - fr.R(33.4, 0.4)) * h, size=19, light=True)
    PQ(fr, 1380, 400, "THE FIRST PAIR: WRECKED BY A STORM", a=fr.R(34.0, 0.4) * (1 - fr.R(39.6, 0.4)) * h, size=19, light=True)
    PQ(fr, 1380, 400, "THE SECOND PAIR HOLDS", a=fr.R(39.9, 0.4) * h, size=19, light=True)
    TL(fr, 24.16, 40.25, "ATHOS", size=34, sp=8, a=fr.R(42.6, 0.5) * at, anchor="m")
    gline(fr, [(23.905, 40.392), (23.955, 40.357)], color=WHITE, width=11, frac=fr.R(45.9, 1.6), a=at); gline(fr, [(23.905, 40.392), (23.955, 40.357)], color=engine.RIVER, width=6, frac=fr.R(45.9, 1.6), a=at)
    PQ(fr, 560, 300, "A SHIP CANAL, 2 KM LONG", a=fr.R(46.3, 0.5) * at, size=30)
    PQ(fr, 560, 370, "A GREEK TALL TALE?", a=fr.R(49.4, 0.4) * (1 - fr.R(51.6, 0.4)) * at, size=19, light=True)
    PQ(fr, 560, 370, "FOUND IN THE 1990s, WHERE HERODOTUS PUT IT", a=fr.R(52.0, 0.4) * at, size=19, light=True)
    pulse(fr, (23.93, 40.375), 54.0, 3.2, color=INK, rmax=70, width=4)

# ================= 8c. VO 57.9-70.0: how big was the army
@scene("08c_the_army", 8, 57.9, 70.0, cam_at(25.2, 39.35, 150), dict(emp=MAXE, mac=MAC), res="10")
def _(fr, t):
    terr(fr, "emp", PER); terr(fr, "mac", PER_L)
    gline(fr, XERXES, width=5, frac=fr.R(57.9, 9.0), arrow=True, halo=WHITE)
    city(fr, "SARDIS", side="r", r=7, size=20, label="", color=WHITE); city(fr, "ATHENS", side="b", r=6, size=20)
    dimn = 1.0
    PQ(fr, 1380, 150, "1,700,000", a=fr.R(60.3, 0.4) * dimn, size=56)
    PQ(fr, 1380, 232, "HERODOTUS: FOOT SOLDIERS ALONE", a=fr.R(59.6, 0.4) * dimn, size=18, light=True)
    x0, x1, y = 1215, 1545, 150
    pline(fr, [(x0, y), (x0 + (x1 - x0) * fr.R(66.6, 0.5), y)], color=PER, width=7, a=1.0 if t >= 66.6 else 0)
    PQ(fr, 1380, 320, "A TENTH OF THAT, OR LESS", a=fr.R(67.1, 0.4), size=30)
    PQ(fr, 1380, 384, "STILL ENORMOUS", a=fr.R(68.9, 0.4), size=18, light=True)

# ================= 8d. VO 97.1-128.7: Thermopylae; Greeks on the Persian side
_V8d = cam_at(22.62, 38.84, 1050); _V8e = cam_at(24.6, 39.25, 180)
_c = mover([(97.1, _V8d), (110.8, _V8d), (113.8, _V8e)])
@scene("08d_thermopylae", 8, 97.1, 128.7, _c, dict(emp=MAXE, mac=MAC, the=M(THESSALY), boe=M(BOEOTIA)), res="10")
def _(fr, t):
    terr(fr, "emp", PER); terr(fr, "mac", PER_L, fr.R(117.9, 0.8)); terr(fr, "the", PER_L, fr.R(117.1, 0.8)); terr(fr, "boe", PER_L, fr.R(118.8, 0.8))
    near = 1 - fr.R(110.8, 0.8); far = fr.R(113.0, 0.8)
    gline(fr, smooth([(22.2, 39.12), (22.36, 38.98), (22.47, 38.89), (22.515, 38.815)]), color=PER_D, width=7, frac=fr.R(97.3, 1.6), arrow=True, a=near, halo=WHITE)
    bar(fr, 22.56, 38.795, 80, length=52, width=12, a=fr.R(97.2, 0.4) * near, color=GREEK)
    TL(fr, 22.56, 38.795, "THERMOPYLAE", dx=34, dy=4, size=30, a=fr.R(97.2, 0.5) * near)
    PQL(fr, 22.56, 38.795, "300 SPARTANS", dx=150, dy=58, a=fr.R(98.4, 0.4) * near, size=24)
    PQL(fr, 22.56, 38.795, "PLUS SEVERAL THOUSAND OTHER GREEKS", dx=150, dy=110, a=fr.R(99.9, 0.4) * near, size=16, pad=(10, 6), light=True)
    PQL(fr, 22.3, 39.05, "THE IMMORTALS", dx=-150, dy=0, a=fr.R(103.9, 0.4) * near, size=22, pad=(11, 7))
    PQ(fr, 300, 104, "3 DAYS", a=fr.R(106.4, 0.4) * near, size=36)
    gline(fr, smooth([(22.43, 38.86), (22.40, 38.77), (22.47, 38.70), (22.60, 38.69), (22.67, 38.74), (22.63, 38.785)], 10), color=CHAR, width=3.6, frac=fr.R(108.1, 2.2), dash=(10, 7), arrow=True, a=near)
    TL(fr, 22.53, 38.69, "A MOUNTAIN PATH", dy=30, size=18, w="m", color=CHAR, sp=2.5, anchor="m", a=fr.R(109.6, 0.5) * near)
    # the wider Greek world
    region(fr, 22.2, 39.5, "THESSALY", a=fr.R(117.1, 0.5), size=19, sp=3); region(fr, 22.3, 40.98, "MACEDON", a=fr.R(117.9, 0.5), size=19, sp=3)
    city(fr, "THEBES", a=fr.R(118.8, 0.5), side="l", r=6, size=20)
    city(fr, "SPARTA", a=fr.R(114.6, 0.4), side="b", r=6, size=20)
    PQL(fr, *C["SPARTA"], "AN EXILED KING RIDES WITH XERXES", dx=-60, dy=70, a=fr.R(114.2, 0.5), size=16, pad=(10, 6), light=True)
    city(fr, "", ll=C["HALICARNASSUS"], a=fr.R(122.2, 0.4), r=7, label="")
    tag(fr, *C["HALICARNASSUS"], "ARTEMISIA", "A QUEEN FROM A GREEK CITY", a=fr.R(123.9, 0.4), au=fr.R(122.2, 0.4), dx=60, dy=-80, size=22)
    PQ(fr, 620, 104, "XERXES IS NOT SHORT OF GREEK HELP", a=fr.R(112.2, 0.5) * far, size=26)
    la = fr.R(125.1, 0.6)
    if la > 0:
        x0, y0 = 150, 190
        alpha_draw(fr, lambda d, c: d.rectangle([s(x0), s(y0 - 14), s(x0 + 44), s(y0 + 14)], fill=c), PER_L, la)
        alpha_draw(fr, lambda d, c: d.rectangle([s(x0), s(y0 - 14), s(x0 + 44), s(y0 + 14)], outline=c, width=s(2)), INK, la)
        T(fr, x0 + 60, y0, "GREEKS ON THE PERSIAN SIDE", size=22, sp=2.2, a=la)
