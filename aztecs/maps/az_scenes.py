"""The Aztecs in 20 Minutes: map scenes, timed to the recorded voiceover (chapter seconds). Windows come from ../layout.json (one source of numbers).
usage: python3 az_scenes.py list | still name@t,t (chapter seconds) | sheet tag [prefixes] | render names... | json"""
from az_base import *
HERE = os.path.dirname(os.path.abspath(__file__))
import az_base; _inside = az_base._inside
from functools import partial
_LAY = json.load(open(os.path.join(HERE, "../layout.json")))
WIN = {}
for _ch, _v in _LAY.items():
    if not isinstance(_v, dict) or "segs" not in _v: continue
    for _s in _v["segs"]:
        if _s[2] == "MAP": WIN.setdefault((_s[3], int(_ch)), []).append((_s[0], _s[1]))
def sc(i, tag, cam, masks, ch=None, **kw):
    """one clip per map id and chapter: it covers the first window's start to the last window's end"""
    chs = [c for (j, c) in WIN if j == i]; ch = ch if ch is not None else chs[0]; w = WIN[(i, ch)]
    return scene(f"{i}_{tag}" + ("" if ch == chs[0] else f"_c{ch}"), ch, min(a for a, b in w), max(b for a, b in w), cam, masks, **kw)

# ---------------------------------------------------------------- helpers
def rect(fr, x0, y0, x1, y1, color, a=1.0):
    alpha_draw(fr, lambda d, c: d.rectangle([s(x0), s(y0), s(x1), s(y1)], fill=c), color, a)
def poly(fr, pts, color, a=1.0):
    alpha_draw(fr, lambda d, c: d.polygon([(s(x), s(y)) for x, y in pts], fill=c), color, a)
def circ(fr, x, y, r, color=None, a=1.0, outline=None, width=2):
    if a <= 0: return
    if color is not None: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=c), color, a)
    if outline is not None: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], outline=c, width=s(width)), outline, a)
def arrow(fr, pts, t0, d=1.4, width=4.2, a=1.0, n=10, **kw):
    gline(fr, smooth(pts, n) if len(pts) > 2 else pts, width=width, frac=fr.R(t0, d), arrow=True, halo=kw.pop("halo", WHITE), a=a, **kw)
def out(fr, t0, d=0.5): return 1 - fr.R(t0, d)
_gline0 = gline
def gline(fr, lonlat, halo=None, **kw):
    """dashed lines need a dense path (the base dash routine drops a dash that lies inside one segment)"""
    if kw.get("dash"):
        a = np.asarray(lonlat, float); L = path_len(proj(fr.cam, a, 1)); n = max(2, int(L[-1] / 3.0))
        lonlat = np.stack([np.interp(np.linspace(0, L[-1], n), L, a[:, 0]), np.interp(np.linspace(0, L[-1], n), L, a[:, 1])], 1)
    _gline0(fr, lonlat, halo=halo, **kw)
def tdot(fr, ll, a=1.0, r=4.2, color=INK, ring=WHITE):
    x, y = P(fr.cam, *ll); circ(fr, x, y, r + 1.8, ring, a); circ(fr, x, y, r, color, a)
def town(fr, name, a=1.0, r=5.5, color=INK, size=22, **kw): city(fr, name, a=a, r=r, dot=color, icon=False, size=size, **kw)
def gpoly(fr, lonlat, color, a=1.0):
    p = proj(fr.cam, lonlat, 1); poly(fr, [tuple(q) for q in p], color, a)
def rivers_bold(fr, width=5.0, a=1.0, color=(74, 128, 156)):
    """the two rivers drawn heavier than the base (same geometry, so no double line)"""
    for arr in engine.RIVERS:
        p = proj(fr.cam, arr, 1)
        if p[:, 0].max() < 0 or p[:, 0].min() > W or p[:, 1].max() < 0 or p[:, 1].min() > H: continue
        pline(fr, p, color=color, width=width, a=a)
def mover_dot(fr, path, t0, d, r=7, color=INK, hold=0.0):
    """a dot travelling along a lon/lat path between chapter seconds t0 and t0+d"""
    live(fr, t0, t0 + d + hold)
    if fr.v < t0 or fr.v > t0 + d + hold: return None
    ll = along(path, ease((fr.v - t0) / d)); tdot(fr, ll, r=r, color=color); return ll
def villages_dummy(): pass
def lbl(fr, name, t0, side="r", color=INK, dot=INK, r=6, size=22, dx=0, dy=0, label=None, pul=None):
    """a town dot with its label fading in at chapter second t0"""
    a = fr.R(t0, 0.4); city(fr, name, a=a, side=side, r=r, size=size, color=color, dot=dot, icon=False, dx=dx, dy=dy, label=label)
    if pul: pulse(fr, C[name], t0, 2.0, color=pul)
def lake_t(fr, lon, lat, txt, t0, size=18): sea(fr, lon, lat, txt, a=fr.R(t0, 0.5), size=size)
def bridges(fr, pts, a=1.0, n=6, seed=1):
    """short white gaps along a causeway = bridges"""
    p = np.asarray(pts, float)
    for q in np.linspace(0.18, 0.88, n):
        ll = along(p, q); x, y = P(fr.cam, *ll); alpha_draw(fr, lambda d, c: d.ellipse([s(x - 4.5), s(y - 4.5), s(x + 4.5), s(y + 4.5)], fill=c), WHITE, a)
        alpha_draw(fr, lambda d, c: d.ellipse([s(x - 2.2), s(y - 2.2), s(x + 2.2), s(y + 2.2)], fill=c), INK, a)

NORTHC = cam_box(-118, -91, 15, 33.5); ROUTEC = cam_box(-114, -96, 17.5, 33.5)
VAL = cam_box(-99.42, -98.72, 19.18, 19.86); ISL = cam_box(-99.27, -99.02, 19.36, 19.52); LAKEW = cam_box(-99.30, -98.84, 19.30, 19.62); ISL3 = cam_box(-99.26, -99.02, 19.33, 19.52); DIKEC = cam_box(-99.27, -98.82, 19.24, 19.60)
AZTLAN_PT = (-109.5, 31.0)
ROUTE = [AZTLAN_PT, (-108.2, 28.6), (-106.6, 26.2), (-104.7, 23.9), (-102.6, 22.0), (-100.6, 20.4), (-99.19, 19.46)]

# ================= chapter 1
@sc("01a", "name", NORTHC, {})
def _(fr, t):
    PQL(fr, -101.6, 22.0, "MESHEEKA", a=fr.R(word(1, "They called", "Mesheeka"), 0.4), size=36)
    modern(fr, -102.0, 25.0, "MEXICO", a=fr.R(word(1, "And yes", "Mexico"), 0.5), size=44, color=(70, 60, 46))
    ta = word(1, "Aztec comes", "Aztlan")
    arrow(fr, [(-101.5, 23.0), (-104.5, 27.0), (-108.4, 30.4)], ta - 0.3, d=2.4, dash=(10, 8), color=AZ_D, width=4)
    PQL(fr, *AZTLAN_PT, "AZTLAN", dy=-6, a=fr.R(ta, 0.4), size=38)
    PQL(fr, AZTLAN_PT[0], AZTLAN_PT[1], "SOMEWHERE FAR TO THE NORTH", dy=52, a=fr.R(word(1, "Aztec comes", "somewhere"), 0.4), size=22)
    PQL(fr, -104.0, 18.7, "NOBODY KNOWS WHERE IT WAS", a=fr.R(cue(1, "Nobody knows"), 0.4), size=28)

@sc("01b", "march", ROUTEC, {})
def _(fr, t):
    t0 = cue(1, "According to their own")
    PQL(fr, *AZTLAN_PT, "AZTLAN", dx=-10, dy=-34, a=1.0, size=30)
    arrow(fr, ROUTE, t0 + 1.0, d=5.4, dash=(14, 9), color=AZ_D, width=5)
    tdot(fr, AZTLAN_PT, r=7, color=AZ_D)
    PQL(fr, -105.6, 29.0, "HUITZILOPOCHTLI", a=fr.R(word(1, "According to their own", "Huitzilopochtli"), 0.4), size=32)
    PQL(fr, -105.6, 29.0, "GOD OF THE SUN AND OF WAR", dy=46, a=fr.R(word(1, "According to their own", "god of the sun"), 0.4), size=22)

@sc("01c", "valley", VAL, {})
def _(fr, t):
    valley_rivers(fr, a=fr.R(53.0, 1.5) * 0.9)
    region(fr, -99.07, 19.83, "VALLEY OF MEXICO", a=fr.R(word(1, "So do many", "Valley of Mexico"), 0.5), size=30)
    PQL(fr, -98.78, 19.70, "MORE THAN 2,200 M", a=fr.R(word(1, "It is a high basin", "more than"), 0.4), size=30)
    PQL(fr, -98.78, 19.70, "ABOVE THE SEA", dy=46, a=fr.R(word(1, "It is a high basin", "above the sea"), 0.4), size=22, light=True)
    t5 = cue(1, "On its floor")
    for i, (n, ll) in enumerate((("ZUMPANGO", (-99.2, 19.795)), ("XALTOCAN", (-99.05, 19.72)), ("TEXCOCO", (-98.97, 19.52)), ("XOCHIMILCO", (-99.19, 19.215)), ("CHALCO", (-98.9, 19.215)))):
        lake_t(fr, ll[0], ll[1], "LAKE " + n, t5 + 0.35 * i, size=22)
    ts = word(1, "No river", "salty")
    PQL(fr, -98.97, 19.45, "SALTY", a=fr.R(ts, 0.4), size=30)

def cities1(fr, t0):
    lbl(fr, "CULHUACAN", word(1, "Culhuacan in the south", "Culhuacan"), side="r", color=INK, dot=TAR, r=7, size=22, pul=TAR)
    lbl(fr, "AZCAPOTZALCO", word(1, "Culhuacan in the south", "Azcapotzalco"), side="l", color=INK, dot=TEP, r=7, size=22, pul=TEP)
    lbl(fr, "TEXCOCO", word(1, "Culhuacan in the south", "Texcoco"), side="r", color=INK, dot=ACO, r=7, size=22, pul=ACO)
@sc("01d", "arrive", VAL, {})
def _(fr, t):
    valley_rivers(fr, a=0.9)
    ta = cue(1, "Around 1250")
    PQL(fr, -99.07, 19.80, "AROUND 1250", a=fr.R(ta, 0.4), size=38)
    ll = mover_dot(fr, [(-99.30, 19.72), (-99.25, 19.58), (-99.20, 19.47), C["CHAPULTEPEC"]], ta + 0.2, 2.6, r=8, color=AZ, hold=40.0)
    if ll: PQL(fr, *ll, "MESHEEKA", dx=-120, dy=0, a=fr.R(ta + 1.0, 0.4), size=24)
    PQL(fr, -99.07, 19.74, "THEY ARE LATE", a=fr.R(cue(1, "They are late"), 0.4), size=30)
    cities1(fr, ta)
    PQL(fr, -99.31, 19.33, "THE LAND NOBODY ELSE WANTS", a=fr.R(word(1, "So they take", "land nobody"), 0.4), size=24)

@sc("01d", "wander", VAL, {}, ch=2)
def _(fr, t):
    valley_rivers(fr, a=0.9)
    for n, c in (("CULHUACAN", TAR), ("AZCAPOTZALCO", TEP), ("TEXCOCO", ACO)): city(fr, n, a=1.0, side="r" if n != "AZCAPOTZALCO" else "l", r=7, size=22, dot=c, icon=False)
    path = [C["CHAPULTEPEC"], (-99.19, 19.49), (-99.15, 19.40), C["CULHUACAN"], (-99.0, 19.325), (-98.9, 19.40), C["TEXCOCO"]]
    gline(fr, smooth(path, 6), color=AZ, width=4, dash=(10, 8), frac=fr.R(0.2, 4.6), halo=WHITE)
    mover_dot(fr, smooth(path, 6), 0.2, 4.6, r=8, color=AZ, hold=40.0)
    PQL(fr, -99.07, 19.80, "A SIGN", a=fr.R(cue(2, "But their god"), 0.4), size=38)

# ================= chapter 2
ISLM = mover([(0, VAL), (1.2, VAL), (6.4, ISL)])
@sc("02a", "island", ISLM, {})
def _(fr, t):
    valley_rivers(fr, a=0.9 * (1 - fr.R(18.0, 3.0)))
    for n, c in (("AZCAPOTZALCO", TEP), ("TLACOPAN", TEP)): city(fr, n, a=1.0, side="l", r=7, size=20, dot=c, icon=False)
    ty = cue(2, "In the traditional")
    PQ(fr, 1480, 150, "1325", a=fr.R(ty, 0.4) * (1 - fr.R(26.0, 0.6)), size=44)
    tn = word(2, "They call the place", "Tenochtitlan")
    tdot(fr, C["TENOCH_ISL"], a=fr.R(tn, 0.3), r=9, color=AZ); pulse(fr, C["TENOCH_ISL"], tn, 2.2, color=AZ)
    PQL(fr, *C["TENOCH_ISL"], "TENOCHTITLAN", dx=165, dy=-4, a=fr.R(tn, 0.4), size=34)
    PQL(fr, *C["TENOCH_ISL"], "THE PLACE OF THE PRICKLY PEAR CACTUS", dx=165, dy=44, a=fr.R(word(2, "They call the place", "the place of"), 0.4), size=19)
    t3 = cue(2, "But it has three")
    PQ(fr, 1480, 150, "THREE ADVANTAGES", a=fr.R(t3, 0.4) * (1 - fr.R(cue(2, "A second group") - 0.4, 0.4)), size=38)
    for i, (txt, tw, (px_, py_)) in enumerate((("NOBODY ELSE WANTS IT", cue(2, "Nobody else wants it"), (1480, 240)), ("IT IS HARD TO ATTACK", cue(2, "It is hard to attack"), (1480, 310)), ("EVERYTHING TRAVELS BY CANOE", cue(2, "And it sits"), (1480, 380)))):
        PQ(fr, px_, py_, txt, a=fr.R(tw, 0.4) * (1 - fr.R(cue(2, "A second group") - 0.4, 0.4)), size=26)
    # tribute to Azcapotzalco
    tt = word(2, "For the next fifty", "Azcapotzalco")
    arrow(fr, [C["TENOCH_ISL"], (-99.17, 19.465), C["AZCAPOTZALCO"]], tt - 0.6, d=1.8, color=AZ, width=4.6)
    city(fr, "AZCAPOTZALCO", a=fr.R(tt - 0.6, 0.4), side="l", r=10, size=26, dot=TEP, icon=False, label="")
    PQL(fr, *C["AZCAPOTZALCO"], "TRIBUTE", dx=-60, dy=-50, a=fr.R(tt + 0.8, 0.4), size=28)

@sc("02b", "tlatelolco", ISL, {})
def _(fr, t):
    tdot(fr, C["TENOCH_ISL"], r=9, color=AZ); PQL(fr, *C["TENOCH_ISL"], "TENOCHTITLAN", dx=165, dy=30, size=26, a=1.0)
    tt = cue(2, "A second group")
    tdot(fr, C["TLATELOLCO"], a=fr.R(tt + 1.0, 0.3), r=9, color=TLX); pulse(fr, C["TLATELOLCO"], tt + 1.0, 2.2, color=TLX)
    PQL(fr, *C["TLATELOLCO"], "TLATELOLCO", dx=-170, dy=-6, a=fr.R(tt + 1.0, 0.4), size=34)
    PQL(fr, *C["TLATELOLCO"], "THE GREATEST MARKET IN THE LAND", dx=-300, dy=52, a=fr.R(cue(2, "It will have"), 0.4), size=22)

# ================= chapter 3
@sc("03a", "aqueduct", ISL3, {})
def _(fr, t):
    tdot(fr, C["TENOCH_ISL"], r=9, color=AZ); PQL(fr, *C["TENOCH_ISL"], "TENOCHTITLAN", dx=165, dy=30, size=26)
    ta = word(3, "The lake is salty", "Chapultepec")
    off = 0.0016
    for k, dl in enumerate((0.0, off)):
        gline(fr, [(x + dl, y) for x, y in smooth(AQUEDUCT, 6)], color=(66, 128, 170), width=4.4, frac=fr.R(ta - 1.4, 3.6), halo=WHITE)
    tdot(fr, C["CHAPULTEPEC"], a=fr.R(ta - 1.4, 0.4), r=8, color=INK); PQL(fr, *C["CHAPULTEPEC"], "CHAPULTEPEC", dx=-155, dy=0, a=fr.R(ta - 1.0, 0.4), size=28)
    PQL(fr, -99.11, 19.505, "TWO CHANNELS", a=fr.R(cue(3, "It has two channels"), 0.4) * (1 - fr.R(cue(3, "Three long") - 0.4, 0.4)), size=32)
    t3 = cue(3, "Three long")
    for nm, cw, w, (ox, oy) in (("NORTH", CW_TEPEYAC, "north", (24, -6)), ("WEST", CW_TLACOPAN, "west", (-30, -26)), ("SOUTH", CW_IZTAP, "south", (30, 4))):
        tw = word(3, "Three long", w)
        gline(fr, smooth(cw, 6), color=AZ, width=5.2, frac=fr.R(tw - 0.5, 1.6), halo=WHITE)
        x, y = P(fr.cam, *cw[-1]); PQ(fr, x + ox, y + oy, nm, a=fr.R(tw + 0.6, 0.4), size=22, anchor="l" if ox > 0 else "r")
    tb = cue(3, "Each is cut")
    for cw in (CW_TEPEYAC, CW_TLACOPAN, CW_IZTAP): bridges(fr, smooth(cw, 6), a=fr.R(tb, 0.5), n=5)
    PQL(fr, -99.15, 19.515, "EACH CUT BY BRIDGES", a=fr.R(tb, 0.4), size=26)

@sc("03b", "dike", DIKEC, {})
def _(fr, t):
    valley_rivers(fr, a=0.8)
    tdot(fr, C["TENOCH_ISL"], r=9, color=AZ); PQL(fr, *C["TENOCH_ISL"], "TENOCHTITLAN", dx=-170, dy=-6, size=26, a=1.0)
    tf = cue(3, "In 1449")
    PQ(fr, 400, 150, "1449", a=fr.R(tf, 0.4), size=44)
    flood = fr.R(tf, 1.0) * (1 - fr.R(cue(3, "It holds back"), 1.4))
    if flood > 0:
        for k in range(3): pulse(fr, C["TENOCH_ISL"], tf, 3.0, color=(66, 128, 170), n=3, rmax=60 + 40 * k, width=4, period=1.0 + 0.2 * k)
        PQL(fr, *C["TENOCH_ISL"], "FLOOD", dx=-150, dy=60, a=fr.R(tf + 0.4, 0.4) * (1 - fr.R(cue(3, "The king asks") - 0.4, 0.4)), size=30)
    te = word(3, "The king asks", "Nezahualcoyotl")
    city(fr, "TEXCOCO", a=fr.R(te, 0.4), side="r", r=8, size=26, dot=ACO, icon=False); pulse(fr, C["TEXCOCO"], te, 2.0, color=ACO)
    PQL(fr, *C["TEXCOCO"], "NEZAHUALCOYOTL", dx=-150, dy=-48, a=fr.R(te, 0.4), size=24)
    td = cue(3, "Nezahualcoyotl designs")
    gline(fr, DIKE, color=AZ_D, width=7.5, frac=fr.R(td + 1.2, 4.8), halo=WHITE)
    PQL(fr, -98.985, 19.43, "16 KM", a=fr.R(td + 4.8, 0.4), size=36)
    ts = cue(3, "It also keeps")
    PQL(fr, -98.93, 19.40, "SALT", a=fr.R(ts, 0.4), size=34); PQL(fr, -99.09, 19.545, "FRESHER", a=fr.R(ts + 0.8, 0.4), size=30)
    PQL(fr, -99.04, 19.30, "NO FLOODS UNTIL THE SPANISH ARRIVE", a=fr.R(cue(3, "There is no record"), 0.4), size=28)

# ================= chapter 4
@sc("04a", "azcapotzalco", LAKEW, {})
def _(fr, t):
    valley_rivers(fr, a=0.8)
    for n, c, sd in (("TENOCHTITLAN", AZ, "r"), ("CULHUACAN", TAR, "r")):
        city(fr, n, a=1.0, side=sd, r=7, size=22, dot=c, icon=False, ll=C["TENOCH_ISL"] if n == "TENOCHTITLAN" else None)
    city(fr, "TEXCOCO", a=1.0, side="r", r=7, size=22, dot=ACO, icon=False)
    city(fr, "TLACOPAN", a=1.0, side="l", r=7, size=22, dot=TEP, icon=False, dy=26)
    t0 = cue(4, "Around 1427")
    PQ(fr, 400, 150, "1427", a=fr.R(t0, 0.4), size=44)
    city(fr, "AZCAPOTZALCO", a=1.0, side="l", r=10, size=28, dot=TEP, icon=False); pulse(fr, C["AZCAPOTZALCO"], t0, 2.4, color=TEP)
    PQL(fr, *C["AZCAPOTZALCO"], "TEZOZOMOC DIES", dx=-200, dy=-48, a=fr.R(t0 + 0.6, 0.4) * (1 - fr.R(cue(4, "His son Maxtla") - 0.4, 0.4)), size=24)
    tm = cue(4, "His son Maxtla")
    PQL(fr, *C["AZCAPOTZALCO"], "MAXTLA", dx=-150, dy=-48, a=fr.R(tm, 0.4), size=28)
    for i, tgt in enumerate((C["TENOCH_ISL"], C["TLACOPAN"], C["CULHUACAN"], C["TEXCOCO"])):
        arrow(fr, [C["AZCAPOTZALCO"], tgt], tm + 1.6 + 0.5 * i, d=1.2, color=TEP, width=3.6)
    tx = cue(4, "The prince of Texcoco")
    arrow(fr, [C["TEXCOCO"], (-98.80, 19.50)], tx + 0.4, d=1.6, color=ACO, width=5)
    PQL(fr, *C["TEXCOCO"], "NEZAHUALCOYOTL IN EXILE", dx=60, dy=-58, a=fr.R(tx + 0.4, 0.4), size=24)

@sc("04b", "alliance", LAKEW, {})
def _(fr, t):
    valley_rivers(fr, a=0.8)
    city(fr, "AZCAPOTZALCO", a=1.0, side="l", r=9, size=26, dot=TEP, icon=False)
    city(fr, "TLACOPAN", a=1.0, side="l", r=8, size=24, dot=TEP, icon=False, dy=26); city(fr, "TEXCOCO", a=1.0, side="r", r=8, size=24, dot=ACO, icon=False)
    city(fr, "TENOCHTITLAN", a=1.0, side="r", r=8, size=24, dot=AZ, icon=False, ll=C["TENOCH_ISL"])
    ti = cue(4, "The Mesheeka choose")
    PQL(fr, *C["TENOCH_ISL"], "ITZCOATL", dx=130, dy=60, a=fr.R(ti, 0.4), size=28)
    tj = cue(4, "He joins forces")
    arrow(fr, [C["TENOCH_ISL"], C["TEXCOCO"]], tj, d=1.8, color=AZ, width=4.4); arrow(fr, [C["TENOCH_ISL"], C["TLACOPAN"]], tj + 1.0, d=1.4, color=AZ, width=4.4)
    tk = cue(4, "In 1428")
    arrow(fr, [C["TENOCH_ISL"], C["AZCAPOTZALCO"]], tk, d=1.2, color=AZ, width=5.4)
    cross(fr, *C["AZCAPOTZALCO"], a=fr.R(tk + 1.2, 0.4), r=16, width=6, color=AZ_D)
    PQL(fr, *C["AZCAPOTZALCO"], "1428", dx=-130, dy=-52, a=fr.R(tk, 0.4), size=32)
    th = cue(4, "Historians call them")
    pts = [C["TENOCH_ISL"], C["TEXCOCO"], C["TLACOPAN"], C["TENOCH_ISL"]]
    gline(fr, pts, color=AZ_D, width=5, frac=fr.R(th, 2.4), halo=WHITE)
    PQ(fr, 960, 130, "THE TRIPLE ALLIANCE", a=fr.R(th, 0.4), size=40)
    PQ(fr, 960, 190, "TENOCHTITLAN · TEXCOCO · TLACOPAN", a=fr.R(cue(4, "Tenochtitlan, Texcoco"), 0.4), size=24, light=True)
    PQ(fr, 960, 250, "IT IS NEVER ONE COUNTRY", a=fr.R(cue(4, "It is never one"), 0.4), size=26)

if __name__ == "__main__":
    import time
    mode = sys.argv[1]
    def clear(s_):
        s_.masks = {}; s_._cam = None; s_.base = None; s_.rmask = None; s_.rm = None; s_.lm = None; s_.desert = None; s_._plan = None
    os.makedirs(f"{HERE}/test_look", exist_ok=True)
    if mode == "list":
        tot = 0
        for n, s_ in SC.items(): print(f"{n:24s} ch{s_.ch:02d}  VO {s_.t0:6.1f} - {s_.t0 + s_.dur:6.1f}  ({s_.dur:5.1f} s)"); tot += s_.dur
        print("total", round(tot, 1), len(SC))
    elif mode == "json":
        json.dump({n: dict(ch=s_.ch, t0=s_.t0, t1=round(s_.t0 + s_.dur, 3), id=n.split("_")[0], windows=WIN[(n.split("_")[0], s_.ch)]) for n, s_ in SC.items()}, open(f"{HERE}/../maps.json", "w"), indent=1)
    elif mode == "sheet":       # one still per layout window, near its end
        pref = sys.argv[3:]; ims = []
        for n, s_ in SC.items():
            if pref and not any(n.startswith(p) for p in pref): continue
            s_.frame(0.0)
            for a, b in WIN[(n.split("_")[0], s_.ch)]:
                tt = a + (b - a) * 0.95
                im = s_.frame(tt - s_.t0).resize((960, 540), Image.LANCZOS); d = ImageDraw.Draw(im); d.rectangle([0, 0, 380, 22], fill=(17, 17, 17))
                d.text((6, 5), f"{n}  ch{s_.ch} VO {tt:5.1f} ({a:.1f}-{b:.1f})", fill=(255, 255, 255)); ims.append(im)
            clear(s_)
        cols = 2; sh = Image.new("RGB", (cols * 960, ((len(ims) + cols - 1) // cols) * 540), (17, 17, 17))
        for i, im in enumerate(ims): sh.paste(im, (i % cols * 960, i // cols * 540))
        sh.save(f"{HERE}/test_look/sheet_{sys.argv[2]}.jpg", quality=86)
    elif mode == "still":
        for spec in sys.argv[2:]:
            n, ts = spec.split("@"); s_ = SC[n]; s_.frame(0.0)
            for tt in ts.split(","): s_.still(float(tt) - s_.t0, f"{HERE}/test_look/{n}_{float(tt):05.1f}.jpg", 0.75)
    else:
        os.makedirs(f"{HERE}/out_look", exist_ok=True)
        for n in sys.argv[2:]:
            t0 = time.time(); SC[n].render(f"{HERE}/out_look"); clear(SC[n]); print(n, round(time.time() - t0, 1), flush=True)
