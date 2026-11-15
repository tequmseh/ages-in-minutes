"""Persia map scenes, chapters 9-12"""
from pe_base import *
from pe_s2 import tag, mover_dot
def ship(fr, lon, lat, fill, a=1.0, r=8, ring=INK):
    if a <= 0: return
    x, y = P(fr.cam, lon, lat)
    alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=c), fill, a)
    alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], outline=c, width=s(2.2)), ring, a)
def lerp2(a, b, q): return (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)

# ================= 9a. VO 0-47.3: Athens burns; the trap at Salamis; Artemisia
CAM_SAL = cam_at(23.60, 37.935, 4300)
_GRK = [(23.577 + 0.0072 * i, 37.9362 - 0.0016 * (i % 2)) for i in range(7)]
_PER = [((23.635 + 0.016 * (i % 4), 37.872 - 0.015 * (i // 4)), (23.581 + 0.011 * (i % 4), 37.9235 - 0.0075 * (i // 4))) for i in range(16)]
_ART0 = (23.60, 37.905); _VIC = (23.635, 37.915); _CHASE0 = (23.555, 37.925)
@scene("09a_salamis", 9, 0.0, 47.3, CAM_SAL, dict(), res="10")
def _(fr, t):
    live(fr, 18.5, 24.6); live(fr, 32.6, 39.2)
    battle = 1 - fr.R(24.9, 1.0)
    region(fr, 23.46, 37.935, "SALAMIS", size=26, sp=8, a=fr.R(6.9, 0.6))
    city(fr, "ATHENS", side="r", r=9, size=30, a=fr.R(0.6, 0.4)); pulse(fr, C["ATHENS"], 1.2, 4.2, color=PER_D, rmax=64, width=4, n=3)
    PQL(fr, *C["ATHENS"], "THE ACROPOLIS BURNS", dx=60, dy=-56, a=fr.R(1.6, 0.4) * (1 - fr.R(8.0, 0.5)), size=20, pad=(10, 7))
    for ll in _GRK: ship(fr, *ll, WHITE, a=fr.R(7.0, 0.6) * battle)
    TL(fr, 23.60, 37.9362, "THE GREEK FLEET", dx=0, dy=-34, size=16, sp=2, anchor="m", a=fr.R(8.4, 0.5) * battle)
    PQL(fr, 23.50, 37.99, "THEMISTOCLES", dx=-120, dy=-78, a=fr.R(9.0, 0.4) * battle, size=20, pad=(10, 7))
    gline(fr, smooth([(23.605, 37.929), (23.625, 37.905), (23.645, 37.880)]), color=CHAR, width=3, frac=fr.R(10.2, 1.6), dash=(9, 7), arrow=True, a=battle * (1 - fr.R(18.2, 0.5)))
    q = ease((t - 18.5) / 3.6); dead = fr.R(23.2, 1.2)
    for a0, a1 in _PER: ship(fr, *lerp2(a0, a1, q), mix((150, 150, 150), PER, dead), a=fr.R(7.4, 0.6) * battle, ring=WHITE)
    TL(fr, 23.66, 37.845, "XERXES' FLEET", dx=0, dy=44, size=16, sp=2, anchor="m", a=fr.R(7.6, 0.5) * (1 - fr.R(18.4, 0.5)))
    PQ(fr, 330, 104, "THE TRAP", a=fr.R(6.9, 0.4) * battle, size=34)
    PQ(fr, 1540, 470, "A FALSE MESSAGE:", a=fr.R(11.7, 0.4) * (1 - fr.R(17.0, 0.4)), size=20)
    PQ(fr, 1540, 532, "“THE GREEKS WILL SLIP AWAY TONIGHT.", a=fr.R(13.2, 0.4) * (1 - fr.R(17.0, 0.4)), size=22, light=True)
    PQ(fr, 1540, 588, "BLOCK THE STRAIT.”", a=fr.R(15.7, 0.4) * (1 - fr.R(17.0, 0.4)), size=22, light=True)
    PQ(fr, 1540, 470, "THE NARROW CHANNEL", a=fr.R(19.7, 0.4) * battle, size=22)
    PQ(fr, 1540, 532, "NUMBERS ARE USELESS", a=fr.R(21.4, 0.4) * battle, size=22, light=True)
    PQ(fr, 1540, 588, "THE GREEKS WRECK IT", a=fr.R(23.4, 0.4) * battle, size=22, light=True)
    # Artemisia
    art = fr.R(26.6, 0.8)
    if art > 0:
        qa = ease((t - 34.0) / 0.9); apos = lerp2(_ART0, (23.628, 37.913), qa)
        qc = ease((t - 32.8) / 1.6); back = ease((t - 38.2) / 1.2); cpos = lerp2(lerp2(_CHASE0, (23.585, 37.912), qc), (23.545, 37.935), back)
        ship(fr, *_VIC, (150, 150, 150), a=art, ring=WHITE, r=12)
        cross(fr, *_VIC, a=fr.R(34.9, 0.3), r=13, width=5)
        ship(fr, *cpos, WHITE, a=art * fr.R(32.4, 0.5), r=12)
        ship(fr, *apos, PER, a=art, r=14, ring=WHITE)
        TL(fr, *cpos, "A GREEK SHIP", dx=-18, dy=0, size=15, sp=2, anchor="r", a=fr.R(32.8, 0.4) * (1 - fr.R(38.4, 0.4)))
        TL(fr, *_VIC, "HER OWN SIDE", dx=20, dy=0, size=15, sp=2, anchor="l", a=fr.R(34.9, 0.4))
        x, y = P(fr.cam, *_ART0)
        PQ(fr, x - 20, y + 62, "ARTEMISIA", a=fr.R(26.9, 0.4), size=24); PQ(fr, x - 20, y + 114, "QUEEN OF HALICARNASSUS", a=fr.R(27.7, 0.4), size=16, pad=(10, 6), light=True)
        city(fr, "", ll=(23.60, 37.985), a=fr.R(39.5, 0.4), r=7, label="")
        PQL(fr, 23.60, 37.985, "XERXES, WATCHING FROM THE SHORE", dx=60, dy=-46, a=fr.R(39.6, 0.4), size=18, pad=(10, 6))
        PQ(fr, 1400, 830, "“MY MEN HAVE BECOME WOMEN,", a=fr.R(43.5, 0.4), size=26, light=True)
        PQ(fr, 1400, 894, "AND MY WOMEN, MEN!”", a=fr.R(46.1, 0.4), size=26, light=True)

# ================= 9b. VO 47.9-55.8: Xerxes goes home; Plataea
@scene("09b_plataea", 9, 47.9, 55.9, cam_box(22.5, 25.3, 37.45, 38.95), dict(), res="10")
def _(fr, t):
    city(fr, "ATHENS", side="r", r=7, size=24)
    gline(fr, smooth([(23.78, 38.02), (24.1, 38.35), (24.5, 38.75), (25.0, 39.1)]), color=PER_D, width=5.5, frac=fr.R(48.0, 1.6), arrow=True, halo=WHITE)
    PQL(fr, 24.45, 38.62, "XERXES GOES HOME", dx=150, dy=30, a=fr.R(48.2, 0.4), size=22, pad=(11, 7))
    city(fr, "PLATAEA", a=fr.R(51.9, 0.4), side="l", r=9, size=30); cross(fr, 23.30, 38.235, a=fr.R(50.9, 0.4), r=13, width=5.5)
    PQL(fr, *C["PLATAEA"], "THE NEXT YEAR", dx=-90, dy=52, a=fr.R(51.3, 0.4), size=18, pad=(10, 6), light=True)
    PQ(fr, 960, 940, "FOR THE GREEKS: THE MOMENT THAT DEFINES THEM", a=fr.R(53.2, 0.5), size=24)

# ================= 9c. VO 60.6-77.6: the same events, seen from Susa
_c = mover([(60.6, cam_at(24.3, 38.3, 170)), (60.9, cam_at(24.3, 38.3, 170)), (63.4, FULL)])
@scene("09c_from_susa", 9, 60.6, 77.7, _c, dict(emp=CORE, thr=THR, ion=ION), res="50")
def _(fr, t):
    lost = fr.R(66.4, 1.6)
    terr(fr, "emp", PER); terr(fr, "thr", PER, 1 - lost, border=False); terr(fr, "ion", (226, 208, 170), lost, border=False)
    a = fr.R(62.6, 0.6)
    city(fr, "SUSA", a=fr.R(62.0, 0.5), side="r", r=10, size=32, color=WHITE)
    city(fr, "ATHENS", a=a, side="b", r=4, size=13, label="")
    PQL(fr, 22.6, 38.6, "THE FAR WESTERN EDGE", dx=40, dy=-150, a=fr.R(64.9, 0.5), size=20, pad=(10, 7))
    PQL(fr, 27.2, 38.2, "A STRIP OF COASTLINE", dx=60, dy=170, a=fr.R(67.4, 0.5), size=17, pad=(10, 6), light=True)
    PQ(fr, 1180, 104, "NOT A SINGLE PROVINCE THAT MATTERS", a=fr.R(69.2, 0.5), size=26)
    PQ(fr, 1180, 170, "ANOTHER 150 YEARS", a=fr.R(72.7, 0.5), size=30)
    PQ(fr, 1180, 236, "NO PERSIAN ACCOUNT OF THE WAR SURVIVES", a=fr.R(75.1, 0.5), size=19, light=True)

# ================= 10a. VO 16.8-40.8: Persian gold and the Spartan fleet
CAM_PEL = cam_box(20.6, 30.4, 35.7, 41.1)
ATHP = [(23.35, 37.6), (23.45, 38.33), (23.2, 38.75), (24.3, 39.05), (24.9, 39.9), (25.6, 40.35), (26.3, 39.9), (25.8, 38.9), (26.5, 38.15), (27.3, 37.95), (27.6, 36.6), (26.0, 36.1), (24.3, 36.4)]
PELP = [(21.0, 38.33), (22.9, 38.12), (23.25, 37.5), (23.2, 36.3), (21.5, 36.5), (21.0, 37.5)]
_FL0 = (27.05, 37.95)
@scene("10a_persian_gold", 10, 16.8, 40.9, CAM_PEL, dict(emp=CORE, ath=M(ATHP, False), spa=M(PELP)), res="10")
def _(fr, t):
    live(fr, 32.2, 35.6)
    terr(fr, "emp", PER); terr(fr, "ath", GREEK, fr.R(16.9, 0.8) * (1 - 0.75 * fr.R(39.2, 1.4)), border=False); terr(fr, "spa", MACE, fr.R(17.4, 0.8))
    city(fr, "ATHENS", side="t", r=7, size=24, a=fr.R(16.9, 0.4)); city(fr, "SPARTA", side="b", r=7, size=24, a=fr.R(17.4, 0.4), color=WHITE)
    gline(fr, arc(C["SARDIS"], _FL0, 0.25), width=5, frac=fr.R(21.0, 1.4), arrow=True, halo=WHITE)
    city(fr, "", ll=C["SARDIS"], r=8, label="", a=fr.R(20.6, 0.4))
    tag(fr, *C["SARDIS"], "CYRUS THE YOUNGER", "A PERSIAN PRINCE", a=fr.R(25.7, 0.4), au=fr.R(23.6, 0.4), dx=160, dy=-34, size=20)
    PQL(fr, *C["SARDIS"], "PERSIAN GOLD", dx=160, dy=-34, a=fr.R(20.9, 0.4) * (1 - fr.R(23.4, 0.3)), size=22, pad=(11, 7))
    q = ease((t - 32.2) / 3.0)
    for i in range(8):
        p0 = (_FL0[0] - 0.09 * (i % 4), _FL0[1] - 0.07 * (i // 4)); p1 = (26.56 + 0.05 * (i % 4), 40.27 + 0.04 * (i // 4))
        path = smooth([p0, (26.2, 38.6), (25.75, 39.5), (26.1, 40.02), p1], 8)
        pt = partial(path, q)[-1] if q > 0 else p0
        ship(fr, pt[0], pt[1], MACE, a=fr.R(21.9, 0.5), r=6.5, ring=WHITE)
    PQL(fr, *_FL0, "THE SPARTAN FLEET", dx=-150, dy=62, a=fr.R(22.0, 0.4) * (1 - fr.R(32.0, 0.4)), size=17, pad=(10, 6), light=True)
    PQL(fr, *_FL0, "LYSANDER", dx=-150, dy=18, a=fr.R(28.1, 0.4) * (1 - fr.R(32.0, 0.4)), size=20, pad=(10, 7))
    cross(fr, *C["AEGOSPOTAMI"], a=fr.R(35.0, 0.4), r=12, width=5)
    TL(fr, *C["AEGOSPOTAMI"], "AEGOSPOTAMI", dx=-20, dy=-26, size=22, anchor="r", a=fr.R(33.7, 0.4))
    PQ(fr, 420, 104, "THE PELOPONNESIAN WAR", a=fr.R(19.2, 0.4) * (1 - fr.R(32.0, 0.3)), size=28)
    PQ(fr, 420, 104, "405 BC", a=fr.R(32.3, 0.4), size=34)
    PQ(fr, 420, 172, "THE ATHENIAN FLEET, CAUGHT ON THE BEACH", a=fr.R(35.7, 0.5), size=18, light=True)
    PQL(fr, *C["ATHENS"], "SURRENDERS THE NEXT YEAR", dx=-40, dy=60, a=fr.R(39.3, 0.4), size=18, pad=(10, 6), light=True)
    PQ(fr, 1380, 940, "THE CREWS GET A PAY RISE", a=fr.R(30.4, 0.4) * (1 - fr.R(32.0, 0.3)), size=20, light=True)

# ================= 10b. VO 41.4-58.6: the Ten Thousand
@scene("10b_ten_thousand", 10, 41.4, 58.6, cam_at(35.6, 36.4, 64), dict(emp=CORE), res="50")
def _(fr, t):
    terr(fr, "emp", PER)
    gline(fr, TEN_IN, width=4.2, frac=fr.R(43.9, 6.4), halo=WHITE)
    city(fr, "", ll=C["SARDIS"], a=fr.R(43.6, 0.4), r=6, label="")
    region(fr, 34.0, 39.6, "ASIA", a=fr.R(44.5, 0.5), size=22, sp=10, color=WHITE)
    cross(fr, *C["CUNAXA"], a=fr.R(50.4, 0.4), r=12, width=5, color=WHITE)
    TL(fr, *C["CUNAXA"], "CUNAXA", dx=18, dy=-22, size=22, color=WHITE, a=fr.R(50.8, 0.4))
    PQL(fr, *C["CUNAXA"], "THE PRINCE IS KILLED", dx=120, dy=40, a=fr.R(50.0, 0.4), size=17, pad=(10, 6), light=True)
    gline(fr, TEN_OUT, color=WHITE, width=4.2, frac=fr.R(53.2, 3.0), arrow=True)
    TL(fr, 42.9, 38.4, "THE WAY HOME", dx=22, size=15, sp=3, color=WHITE, a=fr.R(54.1, 0.5), w="m")
    PQ(fr, 400, 104, "10,000 GREEK SOLDIERS", a=fr.R(41.6, 0.4), size=28)
    PQ(fr, 400, 170, "HIRED SPEARS IN A PERSIAN CIVIL WAR", a=fr.R(45.1, 0.4), size=17, light=True)
    PQ(fr, 1560, 104, "401 BC", a=fr.R(51.6, 0.4), size=34)
    PQ(fr, 1560, 172, "XENOPHON WROTE THE BOOK", a=fr.R(57.2, 0.4), size=18, light=True)

# ================= 10c. VO 59.2-83.5: the King's Peace
CAM_KP = cam_box(19.6, 52.0, 28.8, 42.2)
@scene("10c_kings_peace", 10, 59.2, 83.5, CAM_KP, dict(emp=CORE, ion=ION, x_gr=M(GREECE)), res="50")
def _(fr, t):
    won = fr.R(74.4, 1.8)
    terr(fr, "emp", PER); terr(fr, "ion", (226, 208, 170), 1 - won, border=False)
    mfill(fr, fr.masks["x_gr"], GREEK, 0.75)
    for i, ll in enumerate(((23.73, 37.98), (22.43, 37.07), (23.32, 38.32), (22.93, 37.94))): pulse(fr, ll, 61.3 + 0.3 * i, 4.0, color=INK, n=1, rmax=20, width=2.5)
    region(fr, 21.3, 39.9, "THE GREEK CITIES", a=fr.R(61.1, 0.5), size=15, sp=3, dy=-40)
    gline(fr, arc(C["SUSA"], (24.3, 38.3), 0.16), width=4.6, frac=fr.R(67.3, 1.8), arrow=True, halo=WHITE)
    city(fr, "SUSA", side="r", r=9, size=28, color=WHITE, a=fr.R(66.8, 0.4))
    PQL(fr, 37.0, 37.2, "TERMS SENT DOWN FROM SUSA", dy=-20, a=fr.R(67.3, 0.5), size=18, pad=(10, 6), light=True)
    PQ(fr, 330, 104, "387 BC", a=fr.R(59.4, 0.4), size=34)
    PQ(fr, 960, 104, "THE KING'S PEACE", a=fr.R(71.5, 0.4), size=36)
    PQ(fr, 960, 176, "THE GREEK CITIES OF ASIA BELONG TO HIM", a=fr.R(74.2, 0.5), size=20, light=True)
    PQ(fr, 600, 940, "LOST WITH AN ARMY", a=fr.R(77.2, 0.4), size=26); PQ(fr, 1240, 940, "WON BACK WITH A PURSE", a=fr.R(79.9, 0.4), size=26)

# ================= 11a. VO 16.8-42.4: full treasury, working roads, and Macedon
_BT = [(C["GRANICUS"], 34.4), (C["ISSUS"], 35.0), (C["GAUGAMELA"], 35.6)]
_ALEX1 = ALEX
@scene("11a_alexander", 11, 16.8, 42.4, FULL, dict(emp=NOEGY, egy=EGY, mac=MAC), res="50")
def _(fr, t):
    live(fr, 31.8, 41.2)
    terr(fr, "emp", PER); k = fr.R(18.5, 1.8); terr(fr, "egy", EGY_C, 1 - k, border=k < 1); terr(fr, "egy", PER, k, border=False); terr(fr, "mac", MACE, fr.R(27.8, 0.8))
    region(fr, 27.6, 28.6, "EGYPT", size=22, sp=6, color=WHITE, w="b")
    gline(fr, ROYAL_ROAD, color=WHITE, width=3, frac=fr.R(24.0, 1.2), a=1 - fr.R(30.0, 0.6))
    pulse(fr, (22.3, 40.9), 28.8, 2.6, color=INK, rmax=46, width=3.5)
    TL(fr, 22.3, 41.0, "MACEDON", dx=-10, dy=-34, size=20, anchor="m", a=fr.R(29.0, 0.4))
    q = min(1.0, max(0.0, (t - 31.8) / 9.4))
    gline(fr, _ALEX1, width=4.4, frac=q, arrow=True, halo=WHITE)
    for ll, t0 in _BT: cross(fr, *ll, a=fr.R(t0, 0.35), r=11, width=5, color=WHITE)
    gline(fr, DARIUS_FLIGHT, color=WHITE, width=3, frac=fr.R(39.1, 2.0), dash=(9, 7), arrow=True)
    cross(fr, 54.5, 35.95, a=fr.R(41.4, 0.4), r=9, width=4, color=WHITE)
    PQL(fr, 54.5, 35.95, "MURDERED BY HIS OWN SATRAP", dx=140, dy=-42, a=fr.R(40.9, 0.4), size=17, pad=(10, 6), light=True)
    PQL(fr, 49.0, 35.6, "DARIUS III RUNS EAST", dx=40, dy=46, a=fr.R(37.9, 0.4), size=18, pad=(10, 6))
    PQ(fr, 800, 104, "340 BC", a=fr.R(16.8, 0.4) * (1 - fr.R(29.9, 0.3)), size=34); PQ(fr, 800, 104, "334 BC", a=fr.R(30.2, 0.4), size=34)
    PQ(fr, 800, 172, "EGYPT RECONQUERED AFTER 60 YEARS", a=fr.R(18.5, 0.4) * (1 - fr.R(29.9, 0.3)), size=17, light=True)
    PQ(fr, 800, 172, "ALEXANDER LEADS IT INTO ASIA", a=fr.R(31.8, 0.4), size=17, light=True)
    PQ(fr, 1500, 104, "THE TREASURY IS FULL", a=fr.R(22.6, 0.4) * (1 - fr.R(29.9, 0.3)), size=24); PQ(fr, 1500, 166, "THE ROADS WORK", a=fr.R(24.0, 0.4) * (1 - fr.R(29.9, 0.3)), size=24)
    PQ(fr, 1500, 104, "3 GREAT BATTLES IN 3 YEARS", a=fr.R(34.1, 0.4), size=24)

# ================= 11b. VO 42.8-61.8: Persepolis burns; the funeral; the hunt
CAM_E = cam_box(40.5, 72.5, 25.6, 41.6)
@scene("11b_persepolis_burns", 11, 42.8, 61.8, CAM_E, dict(emp=CORE), res="50")
def _(fr, t):
    terr(fr, "emp", PER)
    city(fr, "PERSEPOLIS", side="l", r=10, size=30, color=WHITE, a=fr.R(43.5, 0.4))
    pulse(fr, C["PERSEPOLIS"], 44.6, 8.0, color=(255, 214, 150), rmax=70, width=4.5, n=3, period=1.2)
    PQL(fr, *C["PERSEPOLIS"], "THE PALACE BURNS", dx=150, dy=-50, a=fr.R(44.6, 0.4) * (1 - fr.R(55.0, 0.4)), size=22, pad=(11, 7))
    PQ(fr, 960, 104, "REVENGE FOR THE ACROPOLIS", a=fr.R(49.7, 0.4) * (1 - fr.R(53.4, 0.4)), size=28)
    PQ(fr, 960, 170, "150 YEARS LATE", a=fr.R(51.4, 0.4) * (1 - fr.R(53.4, 0.4)), size=20, light=True)
    PQ(fr, 520, 104, "WATCH WHAT HE DOES NEXT", a=fr.R(53.8, 0.4), size=28)
    PQL(fr, *C["PERSEPOLIS"], "A ROYAL FUNERAL FOR DARIUS", dx=170, dy=-50, a=fr.R(55.6, 0.4), size=20, pad=(10, 7), light=True)
    gline(fr, smooth([C["HECATOMPYLOS"], (58.5, 36.6), (62.0, 35.6), (65.0, 36.2), C["BACTRA"], C["MARACANDA"]]), width=4.4, frac=fr.R(57.8, 2.4), arrow=True, halo=WHITE)
    PQL(fr, 62.0, 35.6, "HUNTS DOWN THE KILLER", dy=52, a=fr.R(57.8, 0.4), size=20, pad=(10, 7))
    PQL(fr, *C["MARACANDA"], "A SATRAP WHO DECLARED HIMSELF KING", dx=-90, dy=-46, a=fr.R(59.4, 0.4), size=15, pad=(9, 6), light=True)

# ================= 11c. VO 62.4-67.5: what he keeps
@scene("11c_keeps", 11, 62.4, 67.5, FULL, dict(emp=CORE, x_grid=GRIDM), res="50")
def _(fr, t):
    terr(fr, "emp", PER); mfill(fr, fr.masks["x_grid"], WHITE, fr.R(62.6, 0.9))
    gline(fr, np.vstack([ROYAL_ROAD, ROAD_EXT]), color=INK, width=4, frac=fr.R(64.7, 1.2), halo=WHITE)
    for i, n in enumerate(("SARDIS", "BABYLON", "MEMPHIS", "ECBATANA", "BACTRA", "SUSA")): city(fr, "", ll=C[n], a=fr.R(66.0 + 0.08 * i, 0.4), r=7, label="")
    PQ(fr, 960, 104, "HE KEEPS:", a=fr.R(62.4, 0.3), size=30)
    for i, (txt, t0) in enumerate((("THE PROVINCES", 62.9), ("THE TAXES", 63.9), ("THE ROADS", 64.8), ("THE PERSIAN GOVERNORS", 66.4))):
        PQ(fr, 330 + 400 * i + (60 if i == 3 else 0), 176, txt, a=fr.R(t0, 0.35), size=22, light=True)

# ================= 11d. VO 94.0-107.3: carved up, machinery kept
_P1 = [(18, 34.6), (29, 32.3), (32.5, 32.0), (34.4, 31.2), (35.2, 29.3), (34.6, 27.6), (37, 23), (18, 22)]                      # Egypt
_P2 = [(24, 34.3), (36.3, 35.9), (37.2, 37.6), (39.5, 39.0), (41.0, 41.0), (41.5, 43.5), (24, 44.5)]                           # Anatolia and Thrace
@scene("11d_carved_up", 11, 94.0, 107.3, FULL, dict(emp=MAXE, mac=MAC, x_gr=M(GREECE), x_p1=I(MAXE, _P1), x_p2=I(MAXE, _P2)), res="50")
def _(fr, t):
    live(fr, 100.7, 104.0)
    k = fr.R(96.0, 1.6)
    terr(fr, "emp", PER); terr(fr, "mac", PER, border=False); mfill(fr, fr.masks["x_gr"], PER, 0.9)
    mfill(fr, fr.masks["x_p1"], EGY_C, k); mfill(fr, fr.masks["x_p2"], LYD_C, k); terr(fr, "mac", MACE, k); mfill(fr, fr.masks["x_gr"], MACE, k)
    PQ(fr, 960, 104, "HIS GENERALS CARVED IT UP", a=fr.R(96.0, 0.4), size=30)
    PQ(fr, 960, 172, "AND KEPT THE MACHINERY", a=fr.R(97.3, 0.4), size=20, light=True)
    road = np.vstack([ROYAL_ROAD, ROAD_EXT])
    gline(fr, road, color=INK, width=4, frac=fr.R(99.6, 1.2), halo=WHITE)
    if 100.7 <= t <= 104.0: mover_dot(fr, proj(fr.cam, road, 1), (t - 100.7) / 3.2, r=9, fill=INK, ring=WHITE)
    for i, (txt, t0) in enumerate((("PROVINCES", 98.8), ("ROYAL ROADS", 99.6), ("A STATE COURIER SERVICE", 100.7))):
        PQ(fr, 1180 + 0 * i, 760 + 62 * i, txt, a=fr.R(t0, 0.35), size=24, anchor="l")
    gline(fr, [(21.5, 41.6), (15.2, 41.9)], width=4.4, frac=fr.R(105.4, 0.9), arrow=True, halo=WHITE)
    PQ(fr, 190, 420, "ROME INCLUDED", a=fr.R(105.8, 0.4), size=22)

# ================= 12a. VO 10.8-25.9: Parsa, Persia, Iran
IRANP = [(44.3, 39.4), (46.5, 38.9), (48.9, 38.4), (53.9, 37.4), (56.0, 38.1), (61.2, 36.6), (60.6, 33.6), (61.8, 31.4), (61.0, 29.8), (63.3, 27.2), (61.6, 25.2), (57.3, 25.4),
         (56.4, 27.1), (54.2, 26.6), (51.6, 27.8), (50.0, 30.2), (48.6, 30.0), (47.7, 31.0), (46.1, 33.2), (45.5, 34.6), (46.1, 35.8), (44.8, 37.2)]
@scene("12a_the_name", 12, 10.8, 25.9, cam_box(36, 70, 22.5, 42), dict(iran=M(IRANP), parsa=I(CORE, PARSA)), res="50")
def _(fr, t):
    terr(fr, "iran", PER, fr.R(12.9, 1.4)); terr(fr, "parsa", PER_D, fr.R(15.7, 0.8))
    lab = 1 - fr.R(24.9, 0.5)
    region(fr, 54.6, 34.2, "PERSIA", a=fr.R(12.9, 0.6) * lab, size=64, sp=30, color=WHITE, w="b")
    region(fr, 54.6, 34.2, "WHAT THE GREEKS CALLED THE WHOLE COUNTRY", a=fr.R(13.6, 0.6) * lab, size=15, sp=4, color=WHITE, dy=62)
    region(fr, 54.6, 34.2, "IRAN", a=fr.R(25.3, 0.5), size=84, sp=44, color=WHITE, w="b")
    PQL(fr, 52.7, 29.2, "PARSA", a=fr.R(17.1, 0.4), size=24, pad=(12, 8)); PQL(fr, 52.7, 29.2, "ONE PROVINCE", dy=50, a=fr.R(15.9, 0.4), size=15, pad=(9, 6), light=True)
    PQ(fr, 330, 104, "1935", a=fr.R(21.7, 0.4), size=36)
    PQ(fr, 330, 172, "A DIFFERENT AND VERY OLD NAME", a=fr.R(19.3, 0.5), size=17, light=True)

# ================= 12b. VO 45.3-75.8: three continents, and how you rule them
@scene("12b_the_answer", 12, 45.3, 75.8, FULL, dict(emp=MAXE, x_grid=GRIDM, x_egy=EGY, x_bab=I(CORE, [(41.5, 35.2), (46.2, 34.4), (48.2, 31.2), (47.2, 29.8), (44.6, 30.6), (42.0, 32.2)]), x_jud=M(JUDEA), x_ion=ION, x_east=I(CORE, [(60.5, 44), (75, 44), (75, 22), (60.5, 22)]), x_med=I(CORE, MEDIA)), res="50")
def _(fr, t):
    terr(fr, "emp", PER)
    d = fr.R(65.1, 1.2)
    for key, col in (("x_egy", EGY_C), ("x_bab", BAB_C), ("x_jud", GOLD), ("x_ion", GREEK), ("x_east", LYD_C), ("x_med", MED_C)): mfill(fr, fr.masks[key], col, d * 0.7)
    mfill(fr, fr.masks["x_grid"], WHITE, fr.R(67.1, 1.4))
    for k, (lon, lat) in enumerate([(19.0, 44.4), (22.5, 26.3), (76.0, 40.5)]):
        region(fr, lon, lat, ("EUROPE", "AFRICA", "ASIA")[k], a=fr.R(50.6 + 0.25 * k, 0.5), size=24, sp=10, color=(96, 84, 60), w="b")
    city(fr, "", ll=C["PERSEPOLIS"], a=fr.R(52.1, 0.4), r=8, label=""); pulse(fr, C["PERSEPOLIS"], 52.1, 5.4, color=WHITE, rmax=44, n=2)
    PQL(fr, *C["PERSEPOLIS"], "A CLERK KNEW", dx=40, dy=52, a=fr.R(52.2, 0.4) * (1 - fr.R(58.2, 0.4)), size=20, pad=(10, 7))
    PQL(fr, *C["PERSEPOLIS"], "THE KING OWED HER AN EXTRA RATION", dx=40, dy=100, a=fr.R(56.0, 0.4) * (1 - fr.R(58.2, 0.4)), size=16, pad=(10, 6), light=True)
    PQ(fr, 330, 104, "25 CENTURIES AGO", a=fr.R(47.5, 0.4) * (1 - fr.R(58.2, 0.4)), size=28)
    dim_line(fr, 22.5, 71.5, 44.9, fr.R(59.9, 1.0) * (1 - fr.R(68.9, 0.5)), "3,000 MILES")
    for i, (txt, t0, lt) in enumerate((("NOT BY MAKING EVERYONE THE SAME", 62.9, False), ("BY LETTING THEM STAY DIFFERENT", 65.1, True), ("AND WRITING EVERYTHING DOWN", 67.1, True))):
        PQ(fr, 960, 820 + 62 * i, txt, a=fr.R(t0, 0.4) * (1 - fr.R(68.9, 0.5)), size=24, light=lt)
    PQ(fr, 960, 850, "THE GREEKS WON THE STORY", a=fr.R(69.3, 0.4), size=30)
    PQ(fr, 960, 922, "THE PERSIANS BUILT THE SYSTEM", a=fr.R(71.1, 0.4), size=30, light=True)
