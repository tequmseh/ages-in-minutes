"""Persia in 20 Minutes: map scenes, timed to the recorded voiceover (chapter seconds).
usage: python3 pe_scenes.py list | still name@t,t (chapter seconds) | sheet [names] | render names..."""
from pe_base import *

A_EGEAN = cam_box(19.5, 31.5, 35.2, 41.8)
# ================= 0. Cold open, VO 42.8-59.0: the size of it, then the timeline
_c = mover([(42.8, cam_at(26.5, 39.2, 120)), (43.4, cam_at(26.5, 39.2, 120)), (47.6, FULL)])
@scene("00_cold_open", 0, 42.8, 59.2, _c, dict(emp=MAXE), res="50")
def _(fr, t):
    terr(fr, "emp", PER)
    empire_label(fr, fr.R(47.8, 0.8))
    region(fr, 24.6, 43.9, "THE BALKANS", a=fr.R(46.5, 0.6), size=18, sp=4)
    TL(fr, 71.3, 30.6, "THE INDUS", size=18, sp=4, a=fr.R(47.4, 0.6), anchor="l", dx=14)
    dim_line(fr, 22.5, 71.5, 44.9, fr.R(50.6, 1.0), "3,000 MILES")
    # timeline strip
    a1 = fr.R(53.4, 0.6); a2 = fr.R(56.4, 0.6)
    if a1 > 0:
        x0, y0 = 150, 850; u = 2.6                          # px per year
        alpha_draw(fr, lambda d, c: d.rectangle([s(x0 - 40), s(y0 - 62), s(x0 + 250 * u + 330), s(y0 + 120)], fill=c), INK, a1 * 0.92)
        k1 = fr.R(53.6, 1.2); k2 = fr.R(56.6, 1.4)
        alpha_draw(fr, lambda d, c: d.rectangle([s(x0), s(y0 - 22), s(x0 + 220 * u * k1), s(y0 + 22)], fill=c), YELLOW, a1)
        T(fr, x0, y0 - 42, "PERSIAN EMPIRE", size=17, sp=4, color=WHITE, a=a1); T(fr, x0 + 220 * u + 22, y0, "220 YEARS", size=30, w="b", sp=2, color=WHITE, a=fr.R(54.2, 0.5))
        alpha_draw(fr, lambda d, c: d.rectangle([s(x0), s(y0 + 58), s(x0 + 250 * u * k2), s(y0 + 102)], fill=c), (150, 150, 150), a2)
        T(fr, x0, y0 + 40, "UNITED STATES", size=17, sp=4, color=WHITE, a=a2); T(fr, x0 + 250 * u + 22, y0 + 80, "250 YEARS", size=30, w="b", sp=2, color=WHITE, a=fr.R(57.5, 0.5))

# ================= 1a. VO 0-25.6: four old kingdoms and a nobody
@scene("01a_nobody", 1, 0.0, 25.8, FULL, dict(bab=BAB, lyd=I(CORE, LYDIA), egy=EGY, med=I(CORE, MEDIA), parsa=I(CORE, PARSA)), res="50")
def _(fr, t):
    K4 = (("bab", BAB_C, 5.6, (41.2, 34.2), "BABYLON", "TOWERS AND BANKERS"), ("lyd", LYD_C, 8.5, (30.2, 39.5), "LYDIA", "WHERE COINS WERE INVENTED"),
          ("egy", EGY_C, 10.8, (27.6, 28.6), "EGYPT", "ALREADY ANCIENT"), ("med", MED_C, 13.2, (51.5, 36.3), "THE MEDES", "HORSE LORDS"))
    for key, col, t0, ll, name, tag in K4: terr(fr, key, col, fr.R(t0, 0.9))
    terr(fr, "parsa", PER, fr.R(18.4, 1.0))
    PQ(fr, 250, 110, "550 BC", a=fr.R(0.3, 0.5), size=32)
    for key, col, t0, ll, name, tag in K4:
        region(fr, *ll, name, a=fr.R(t0 + 0.1, 0.7), size=26, sp=6, color=WHITE, w="b")
        region(fr, *ll, tag, a=fr.R(t0 + 0.7, 0.7), size=13, sp=3, color=WHITE, dy=30)
    region(fr, 56.5, 33.4, "IRANIAN PLATEAU", a=fr.R(14.8, 0.7), size=14, sp=5, color=WHITE)
    pulse(fr, (52.6, 29.3), 16.5, 2.4, color=PER_D, rmax=40)
    PQL(fr, 52.6, 29.3, "PARSA", dy=4, a=fr.R(23.2, 0.5), size=22, pad=(12, 8))
    modern(fr, 58.6, 29.6, "TODAY'S IRAN", a=fr.R(21.5, 0.7), size=16)
    gline(fr, arc((52.6, 30.9), (51.2, 34.6), -0.18), width=3.2, frac=fr.R(24.3, 1.0), arrow=True, halo=WHITE)

# ================= 1b. VO 33.1-75.2: Cyrus starts winning; the oracle
_c = mover([(33.1, FULL), (54.4, FULL), (57.0, A_EGEAN), (70.6, A_EGEAN), (73.4, FULL)])
@scene("01b_cyrus", 1, 33.1, 75.2, _c, dict(bab=BAB, lyd=I(CORE, LYDIA), egy=EGY, st1=STAGE1, west=WEST, east=EAST, parsa=I(CORE, PARSA), med=I(CORE, MEDIA)), active=[(54.4, 57.0), (70.6, 73.4)])
def _(fr, t):
    wide = 1 - fr.R(54.6, 0.8) * (1 - fr.R(72.6, 0.8)); near = 1 - wide
    terr(fr, "bab", BAB_C); terr(fr, "egy", EGY_C); terr(fr, "med", MED_C, 1 - fr.R(37.6, 1.6)); terr(fr, "lyd", LYD_C)
    terr(fr, "parsa", PER, border=t < 37.6); terr(fr, "st1", PER, fr.R(37.6, 1.8), border=False)
    back = fr.R(55.0, 1.4) * (1 - fr.R(69.4, 1.8))                     # the story steps back before the conquest of Lydia
    terr(fr, "west", PER, fr.R(44.7, 2.4) * (1 - back), border=False); terr(fr, "east", PER, fr.R(52.2, 2.2), border=False)
    region(fr, 41.2, 34.2, "BABYLON", size=26, sp=6, color=WHITE, w="b", a=wide); region(fr, 27.6, 28.6, "EGYPT", size=26, sp=6, color=WHITE, w="b", a=wide)
    region(fr, 51.5, 36.3, "THE MEDES", size=26, sp=6, color=WHITE, w="b", a=wide); region(fr, 30.2, 39.5, "LYDIA", size=26, sp=6, color=WHITE, w="b", a=wide)
    PQL(fr, 52.6, 29.3, "CYRUS", dy=4, a=fr.R(34.7, 0.5) * wide, size=24, pad=(12, 8))
    gline(fr, arc((52.2, 30.6), C["ECBATANA"], -0.2), width=4.2, frac=fr.R(36.9, 1.2), arrow=True, halo=WHITE, a=wide)
    gline(fr, smooth([C["ECBATANA"], (44.5, 36.8), (40.2, 38.0), (36.2, 39.2), (32.5, 39.4), (28.6, 38.6)]), width=4.2, frac=fr.R(42.0, 2.8), arrow=True, halo=WHITE, a=wide)
    region(fr, 34.5, 40.4, "ANATOLIA", a=fr.R(43.6, 0.6) * wide, size=14, sp=5, color=WHITE)
    PQL(fr, 30.2, 39.5, "CROESUS", dy=44, a=fr.R(46.0, 0.5) * wide, size=20, pad=(11, 7))
    for i, ll in enumerate([(27.28, 37.53), (27.34, 37.94), (27.14, 38.42), (26.75, 38.67), (26.9, 39.1)]):
        city(fr, "", a=fr.R(49.2 + 0.12 * i, 0.4) * wide, r=3.4, ll=ll, label="")
    TL(fr, 26.3, 38.2, "GREEK CITIES", dx=-12, size=15, anchor="r", sp=2, a=fr.R(49.4, 0.6) * wide)
    modern(fr, 33.5, 37.9, "NOW TURKEY", a=fr.R(50.8, 0.7) * wide, size=14, color=(240, 226, 214))
    gline(fr, smooth([(54.5, 35.2), (58.5, 36.6), (62.5, 37.8), (66.3, 39.4)]), width=4.2, frac=fr.R(52.0, 1.6), arrow=True, halo=WHITE, a=wide)
    region(fr, 63.5, 40.6, "CENTRAL ASIA", a=fr.R(53.0, 0.6) * wide, size=16, sp=5, color=WHITE)
    # the oracle
    if near > 0:
        region(fr, 30.3, 39.35, "LYDIA", size=30, sp=9, color=WHITE, w="b", a=near)
        city(fr, "SARDIS", a=near * fr.R(57.6, 0.5), side="r", r=8, size=22, label="CROESUS", color=WHITE)
        gline(fr, arc(C["SARDIS"], C["DELPHI"], 0.16), width=3.2, frac=fr.R(58.3, 1.4), dash=(12, 8), arrow=True, a=near, color=CHAR)
        city(fr, "DELPHI", a=near * fr.R(59.3, 0.5), side="l", r=7, size=24)
        TL(fr, *C["DELPHI"], "THE ORACLE", dx=-16, dy=28, size=14, sp=3, anchor="r", a=near * fr.R(59.0, 0.5), w="m")
        gline(fr, arc(C["DELPHI"], C["SARDIS"], 0.16), width=3.2, frac=fr.R(62.9, 1.4), dash=(12, 8), arrow=True, a=near, color=PER_D)
        PQ(fr, 960, 250, "HE WILL DESTROY A GREAT EMPIRE", a=fr.R(64.6, 0.6) * near, size=32)
        PQ(fr, 960, 322, "THE EMPIRE HE DESTROYS IS HIS OWN", a=fr.R(69.0, 0.6) * near, size=24, light=True)

# ================= 1c. VO 75.3-82.05: twenty years later
@scene("01c_twenty_years", 1, 75.3, 82.2, FULL, dict(bab=BAB, egy=EGY, per=CYRUS), res="50")
def _(fr, t):
    terr(fr, "per", PER); terr(fr, "bab", BAB_C); terr(fr, "egy", EGY_C)
    region(fr, 27.6, 28.6, "EGYPT", size=22, sp=6, color=WHITE, w="b"); region(fr, 53.5, 35.4, "PERSIA", size=34, sp=12, color=WHITE, w="b")
    PQ(fr, 960, 110, "ABOUT 20 YEARS", a=fr.R(75.4, 0.5), size=32)
    region(fr, 40.8, 34.6, "BABYLON", size=26, sp=6, color=WHITE, w="b")
    city(fr, "BABYLON", a=fr.R(80.0, 0.4), r=7, label=""); pulse(fr, C["BABYLON"], 80.0, 2.2, color=WHITE, rmax=46, width=3.5)

# ================= 2a. VO 0-14.6: Babylon opens its gates
CAM_BAB = cam_box(40.6, 49.4, 31.0, 35.9)
@scene("02a_babylon", 2, 0.0, 14.7, CAM_BAB, dict(per=CYRUS, bab=BAB, x_all=NOEGY), res="10")
def _(fr, t):
    k_ = fr.R(13.0, 1.6); terr(fr, "per", PER, border=False); terr(fr, "bab", BAB_C, border=k_ <= 0); mfill(fr, fr.masks["x_all"], PER, k_ / FILL_A / 0.86 if k_ >= 1 else k_)
    region(fr, 42.3, 34.9, "BABYLONIA", size=24, sp=8, color=WHITE, w="b", a=0.9)
    x, y = P(fr.cam, *C["BABYLON"]); wa = fr.R(2.6, 1.0); g = fr.R(12.2, 1.0)
    for R_, wd in ((46, 6), (34, 3)):                                 # double wall, north gate opens
        gap = R_ * 0.6 * g
        for (x0, y0, x1, y1) in [(x - R_, y + R_, x + R_, y + R_), (x - R_, y - R_, x - R_, y + R_), (x + R_, y - R_, x + R_, y + R_), (x - R_, y - R_, x - gap, y - R_), (x + gap, y - R_, x + R_, y - R_)]:
            if abs(x1 - x0) + abs(y1 - y0) > 0.5: pline(fr, [(x0, y0), (x1, y1)], width=wd, a=wa, color=WHITE)
    city(fr, "BABYLON", a=fr.R(0.0, 0.5), side="b", r=8, size=28, dy=46, color=WHITE)
    PQ(fr, 960, 110, "THE BIGGEST CITY ON EARTH", a=fr.R(1.0, 0.5) * (1 - fr.R(7.6, 0.5)), size=30)
    PQ(fr, 960, 110, "539 BC", a=fr.R(8.1, 0.5), size=34)
    gline(fr, smooth([(48.6, 35.6), (47.2, 34.9), (45.8, 34.1), C["OPIS"]]), width=4.5, frac=fr.R(9.6, 1.4), arrow=True, halo=WHITE)
    cross(fr, *C["OPIS"], a=fr.R(10.5, 0.4), r=11, width=5, color=WHITE)
    TL(fr, *C["OPIS"], "BATTLE IN THE FIELD", dx=-18, dy=-4, size=15, anchor="r", sp=2, a=fr.R(10.8, 0.5), color=WHITE)
    gline(fr, [(44.5, 33.15), (44.43, 32.86)], width=4.5, frac=fr.R(12.8, 1.0), arrow=True, halo=WHITE)
    PQL(fr, *C["BABYLON"], "NO SIEGE", dx=150, dy=-6, a=fr.R(13.4, 0.5), size=22, pad=(11, 7))

# ================= 2b. VO 14.9-28.2: how empires ruled before
ASSYRIA = [(41.0, 37.3), (44.6, 37.3), (45.4, 35.8), (44.4, 34.5), (42.6, 34.3), (41.0, 35.4)]
BABCORE = [(43.2, 33.6), (45.6, 33.4), (47.4, 31.4), (46.6, 30.4), (44.6, 31.0), (43.2, 32.4)]
@scene("02b_terror", 2, 14.9, 28.3, cam_box(31.5, 50.5, 29.0, 38.6), dict(asy=M(ASSYRIA), bbc=M(BABCORE)), res="10")
def _(fr, t):
    terr(fr, "asy", SLATE, fr.R(18.7, 0.8)); terr(fr, "bbc", BAB_C, fr.R(19.4, 0.8))
    region(fr, 43.1, 36.1, "ASSYRIA", a=fr.R(18.9, 0.6), size=24, sp=6, color=WHITE, w="b"); region(fr, 45.2, 32.0, "BABYLON", a=fr.R(19.5, 0.6), size=22, sp=5, color=WHITE, w="b")
    PQ(fr, 420, 150, "RULED BY TERROR", a=fr.R(20.2, 0.5), size=30)
    dim = 1 - 0.65 * fr.R(24.8, 0.8)
    for i, (txt, t0) in enumerate((("BEAT A PEOPLE", 21.8), ("DEPORT THEM", 22.6), ("SMASH THEIR TEMPLES", 23.5))):
        PQ(fr, 235, 232 + i * 62, txt, a=fr.R(t0, 0.4) * dim, size=24, anchor="l", light=True)
    for k, (a_, b_, bend) in enumerate((((35.2, 32.4), (42.3, 36.0), -0.16), ((35.2, 31.7), (44.3, 32.5), 0.14), ((36.2, 34.3), (43.0, 35.2), -0.1))):
        cross(fr, *a_, a=fr.R(21.8 + 0.15 * k, 0.4) * dim, r=9, width=4)
        gline(fr, arc(a_, b_, bend), width=3, frac=fr.R(22.6 + 0.2 * k, 1.3), dash=(11, 8), arrow=True, color=CHAR, a=dim)
    PQ(fr, 960, 905, "CYRUS DOES THE OPPOSITE", a=fr.R(24.8, 0.5), size=32)
    PQ(fr, 960, 975, "AND HE PUTS IT IN WRITING", a=fr.R(26.8, 0.5), size=22, light=True)

# ================= 2c. VO 37.6-56.5: statues and exiles go home
_HOME = [((43.26, 35.46), 0.12), (C["SUSA"], -0.12), ((46.3, 33.6), 0.12), ((44.7, 33.7), 0.3), ((45.7, 31.3), -0.2)]
_PEOPLE = [((38.8, 36.9), 0.1), ((36.3, 35.2), 0.1), ((36.0, 33.4), 0.06), ((40.5, 37.9), -0.08)]
@scene("02c_going_home", 2, 37.6, 56.6, cam_at(41.8, 33.7, 95), dict(per=NOEGY, egy=EGY), res="10")
def _(fr, t):
    terr(fr, "per", PER); terr(fr, "egy", EGY_C)
    city(fr, "BABYLON", side="b", r=8, size=24, color=WHITE)
    pulse(fr, C["BABYLON"], 37.7, 1.6, color=WHITE, rmax=34)
    PQ(fr, 1500, 150, "TEMPLES REPAIRED", a=fr.R(37.9, 0.5), size=22, anchor="l")
    PQ(fr, 1500, 208, "GODS SENT BACK", a=fr.R(39.7, 0.5), size=22, anchor="l")
    PQ(fr, 1500, 266, "DEPORTED PEOPLES SENT HOME", a=fr.R(42.1, 0.5), size=22, anchor="l")
    for i, (ll, bend) in enumerate(_HOME):
        gline(fr, arc(C["BABYLON"], ll, bend), color=WHITE, width=2.6, frac=fr.R(39.5 + 0.25 * i, 1.2), arrow=True)
        city(fr, "", a=fr.R(40.2 + 0.25 * i, 0.5), r=4, ll=ll, label="")
    for i, (ll, bend) in enumerate(_PEOPLE):
        gline(fr, arc(C["BABYLON"], ll, bend), color=WHITE, width=2.6, frac=fr.R(42.2 + 0.25 * i, 1.6), dash=(10, 7), arrow=True)
    gline(fr, arc(C["BABYLON"], (35.55, 31.85), 0.10), width=5.5, frac=fr.R(45.3, 1.8), arrow=True, halo=WHITE)
    city(fr, "JERUSALEM", a=fr.R(46.4, 0.6), r=6, label="")
    PQL(fr, *C["JERUSALEM"], "THE JEWS GO HOME", dx=30, dy=62, a=fr.R(46.2, 0.5), size=22, pad=(11, 7))
    PQL(fr, *C["JERUSALEM"], "HALF A CENTURY IN EXILE", dx=30, dy=112, a=fr.R(47.9, 0.5), size=17, pad=(10, 6), light=True)
    T(fr, 960, 840, "THE BIBLE CALLS CYRUS", size=18, sp=5, anchor="m", color=WHITE, a=fr.R(51.8, 0.6) * 0)
    PQ(fr, 960, 880, "THE BIBLE:  “THE LORD'S ANOINTED”", a=fr.R(54.6, 0.6), size=30)

# ================= 2d. VO 75.1-87.25: the new idea
@scene("02d_new_idea", 2, 75.1, 87.4, FULL, dict(per=NOEGY, egy=EGY), res="50")
def _(fr, t):
    terr(fr, "per", PER); terr(fr, "egy", EGY_C)
    PQ(fr, 960, 110, "CHEAPER TO BE WELCOMED THAN FEARED", a=fr.R(79.7, 0.6), size=30)
    hub = (52.6, 29.6)
    for (ll, txt, t0, bend) in (((42.6, 33.6), "KEEP YOUR GODS", 82.5, -0.16), ((32.8, 39.0), "KEEP YOUR PRIESTS", 83.5, -0.12), ((64.5, 36.5), "KEEP YOUR LAWS", 84.5, 0.14)):
        gline(fr, arc((ll[0], ll[1] - 1.3), hub, bend), width=3.4, frac=fr.R(85.8, 1.2), arrow=True, color=WHITE)
    for (ll, txt, t0, bend) in (((42.6, 33.6), "KEEP YOUR GODS", 82.5, -0.16), ((32.8, 39.0), "KEEP YOUR PRIESTS", 83.5, -0.12), ((64.5, 36.5), "KEEP YOUR LAWS", 84.5, 0.14)):
        PQL(fr, *ll, txt, a=fr.R(t0, 0.4), size=22, pad=(11, 7), light=True)
    city(fr, "", ll=hub, a=fr.R(85.7, 0.4), r=8, label="")
    PQL(fr, *hub, "JUST SEND THE TAXES TO ME", dy=52, a=fr.R(85.8, 0.5), size=24)

# ================= 3a. VO 0-13.6: Cyrus dies, Cambyses adds Egypt
@scene("03a_cambyses", 3, 0.0, 13.7, FULL, dict(per=NOEGY, egy=EGY), res="50")
def _(fr, t):
    live(fr, 11.7, 13.7)
    shake = 0.0 if t < 11.7 else 0.28 * (0.5 - 0.5 * math.cos((t - 11.7) * 7.0)) * min(1.0, (t - 11.7) / 0.5)
    terr(fr, "per", PER, 1 - shake); terr(fr, "egy", EGY_C, 1 - fr.R(7.4, 1.0)); terr(fr, "egy", PER, fr.R(6.6, 1.6) * (1 - shake))
    cross(fr, 64.5, 41.6, a=fr.R(0.3, 0.4), r=11, width=5, color=WHITE)
    PQL(fr, 64.5, 41.6, "CYRUS DIES", dx=-10, dy=-46, a=fr.R(0.3, 0.5), size=22, pad=(11, 7))
    region(fr, 62.0, 38.7, "CENTRAL ASIA", a=fr.R(3.7, 0.6), size=15, sp=5, color=WHITE)
    PQ(fr, 300, 110, "CAMBYSES", a=fr.R(5.7, 0.5), size=30)
    gline(fr, smooth([C["BABYLON"], (39.5, 34.6), (36.2, 33.4), (34.4, 31.4), (32.4, 30.9), C["MEMPHIS"]]), width=4.2, frac=fr.R(5.9, 1.8), arrow=True, halo=WHITE)
    region(fr, 27.6, 28.6, "EGYPT", a=fr.R(6.6, 0.7), size=26, sp=6, color=WHITE, w="b")
    region(fr, 27.6, 28.6, "THE LAST OF THE OLD GREAT POWERS", a=fr.R(7.6, 0.7), size=12, sp=2.5, color=WHITE, dy=30)
    gline(fr, smooth([(31.6, 30.3), (33.6, 31.3), (35.6, 32.6), (36.6, 34.6)]), width=3, frac=fr.R(9.9, 1.2), dash=(10, 7), arrow=True, color=WHITE)
    cross(fr, 36.6, 34.75, a=fr.R(11.0, 0.4), r=9, width=4, color=WHITE)
    PQL(fr, 36.6, 34.75, "DIES ON THE WAY HOME", dx=30, dy=-44, a=fr.R(10.6, 0.5), size=20, pad=(10, 7))

# ================= 3b. VO 38.7-56.6: the empire explodes
_REB = [("BABYLON", C["BABYLON"], 41.7, (-70, 40)), ("MEDIA", C["ECBATANA"], 42.4, (0, -40)), ("ELAM", C["SUSA"], 43.3, (78, 26)), ("EGYPT", C["MEMPHIS"], 43.7, (0, -40))]
_REB2 = [((52.9, 29.9), 44.5), ((43.5, 36.3), 44.8), ((56.0, 36.6), 45.1), ((61.8, 37.6), 45.4), ((41.5, 39.6), 45.7), ((65.7, 31.6), 46.0), ((58.5, 33.0), 46.3)]
@scene("03b_explodes", 3, 38.7, 56.7, FULL, dict(emp=CORE), res="50")
def _(fr, t):
    terr(fr, "emp", PER)
    calm = fr.R(52.6, 2.4)
    for ll, t0 in _REB2:
        pulse(fr, ll, t0, 52.4 - t0, color=WHITE, n=1, rmax=22, width=2.5)
        city(fr, "", ll=ll, a=fr.R(t0, 0.3), r=3.5, label="")
    for n, ll, t0, off in _REB:
        pulse(fr, ll, t0, 52.8 - t0, color=WHITE, n=2, rmax=40, width=3.5)
        city(fr, "", ll=ll, a=fr.R(t0, 0.3), r=6, label="")
        PQL(fr, *ll, n, dx=off[0], dy=off[1], size=20, a=fr.R(t0, 0.4), pad=(10, 7))
    PQ(fr, 960, 104, "THE EMPIRE EXPLODES", a=fr.R(39.6, 0.5) * (1 - fr.R(47.6, 0.5)), size=30)
    PQ(fr, 740, 104, "19 BATTLES IN A SINGLE YEAR", a=fr.R(48.1, 0.5), size=28); PQ(fr, 1260, 104, "9 KINGS CAPTURED", a=fr.R(50.6, 0.5), size=28)
    for i, (ll, t0) in enumerate([(x[1], 0) for x in _REB] + _REB2):
        cross(fr, *ll, a=fr.R(52.6 + 0.2 * i, 0.4), r=8, width=3.5, color=INK)

# ================= 3c. VO 57.5-72.6: Behistun and the copies
CAM_BEH = cam_box(42.6, 51.4, 31.4, 36.6)
_c = mover([(57.5, CAM_BEH), (66.2, CAM_BEH), (68.6, FULL)])
MAINROAD = smooth([C["BABYLON"], (44.6, 33.4), (45.4, 34.2), (46.3, 34.45), C["BEHISTUN"], (48.0, 34.55), C["ECBATANA"]])
_COPIES = [(C["BABYLON"], 0.1), (C["SUSA"], -0.1), (C["SARDIS"], 0.1), (C["PERSEPOLIS"], -0.12), (C["BACTRA"], 0.1), ((58.6, 37.0), 0.1), (C["DAMASCUS"], -0.08)]
@scene("03c_behistun", 3, 57.5, 72.7, _c, dict(emp=CORE), res="10")
def _(fr, t):
    terr(fr, "emp", PER)
    near = 1 - fr.R(66.2, 0.8); far = fr.R(67.6, 0.8)
    gline(fr, MAINROAD, width=3.2, dash=(12, 8), color=WHITE, a=near * fr.R(59.6, 0.8))
    TL(fr, 45.2, 33.75, "THE MAIN ROAD", size=15, sp=3, color=WHITE, a=near * fr.R(60.0, 0.6), anchor="r", dx=-10)
    city(fr, "BABYLON", a=near, side="b", r=5, size=17, color=WHITE); city(fr, "ECBATANA", a=near * 0, side="r", r=5, size=17, color=WHITE)
    city(fr, "BEHISTUN", a=fr.R(57.9, 0.4), side="t", r=9, size=26 - 8 * far, color=WHITE)
    pulse(fr, C["BEHISTUN"], 58.0, 2.2, color=WHITE, rmax=44, width=3.5)
    PQL(fr, *C["BEHISTUN"], "100 METRES ABOVE THE ROAD", dx=250, dy=6, a=fr.R(58.9, 0.5) * near, size=22, pad=(11, 7))
    PQL(fr, *C["BEHISTUN"], "HIS VERSION, IN 3 LANGUAGES", dx=250, dy=62, a=fr.R(62.1, 0.5) * near, size=22, pad=(11, 7), light=True)
    for i, (ll, bend) in enumerate(_COPIES):
        gline(fr, arc(C["BEHISTUN"], ll, bend), width=2.6, color=WHITE, frac=fr.R(67.6 + 0.12 * i, 1.4), arrow=True, a=far)
    PQ(fr, 960, 104, "COPIES GO OUT ACROSS THE EMPIRE", a=fr.R(67.2, 0.5), size=28)
    gline(fr, arc(C["BEHISTUN"], C["ELEPHANTINE"], 0.16), width=4.2, frac=fr.R(69.0, 1.4), arrow=True, halo=WHITE, a=far)
    region(fr, 27.6, 28.6, "EGYPT", a=fr.R(69.8, 0.5), size=22, sp=6, color=WHITE, w="b")
    PQL(fr, *C["ELEPHANTINE"], "ON PAPYRUS, IN A 4TH LANGUAGE", dx=-40, dy=58, a=fr.R(70.5, 0.5), size=20, pad=(10, 7))

import pe_s2, pe_s3

if __name__ == "__main__":
    import time
    mode = sys.argv[1]
    if mode == "list":
        tot = 0
        for n, sc in SC.items(): print(f"{n:24s} ch{sc.ch:02d}  VO {sc.t0:6.1f} - {sc.t0 + sc.dur:6.1f}  ({sc.dur:5.1f} s)"); tot += sc.dur
        print("total", round(tot, 1))
    elif mode == "still":
        for spec in sys.argv[2:]:
            n, ts = spec.split("@"); sc = SC[n]; sc.frame(0.0)
            for tt in ts.split(","): sc.still(float(tt) - sc.t0, f"{HERE}/test_look/{n}_{float(tt):05.1f}.png", 1.0)
    elif mode == "sheet":
        names = sys.argv[2:] or list(SC); ims = []
        for n in names:
            sc = SC[n]
            for f in (0.5, 0.985):
                im = sc.frame(sc.dur * f).resize((960, 540), Image.LANCZOS); ImageDraw.Draw(im).rectangle([0, 0, 330, 22], fill=(17, 17, 17))
                ImageDraw.Draw(im).text((6, 5), f"{n}  VO {sc.t0 + sc.dur * f:5.1f}", fill=(255, 255, 255)); ims.append(im)
        cols = 4; sh = Image.new("RGB", (cols * 960, ((len(ims) + cols - 1) // cols) * 540), (17, 17, 17))
        for i, im in enumerate(ims): sh.paste(im, (i % cols * 960, i // cols * 540))
        sh.save(f"{HERE}/test_look/sheet_{names[0][:2]}.jpg", quality=88)
    else:
        for n in sys.argv[2:]:
            t0 = time.time(); SC[n].render(f"{HERE}/out_look"); print(n, round(time.time() - t0, 1), flush=True)
