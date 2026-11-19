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
    PQL(fr, -101.6, 22.0, "MEXICA", a=fr.R(word(1, "They called", "Mesheeka"), 0.4), size=36)
    modern(fr, -100.1, 25.3, "MEXICO", a=fr.R(word(1, "And yes", "Mexico"), 0.5), size=44, color=(70, 60, 46))
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
    PQ(fr, 960, 960, "FIVE CONNECTED LAKES", a=fr.R(word(1, "On its floor", "five"), 0.4), size=28)
    lake_t(fr, -98.97, 19.52, "LAKE TEXCOCO", word(1, "No river", "Texcoco"), size=22)
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
    if ll: PQL(fr, *ll, "MEXICA", dx=-120, dy=0, a=fr.R(ta + 1.0, 0.4), size=24)
    PQL(fr, -99.07, 19.74, "THEY ARE LATE", a=fr.R(cue(1, "They are late"), 0.4), size=30)
    cities1(fr, ta)
    PQL(fr, -99.31, 19.33, "THE LAND NOBODY ELSE WANTS", a=fr.R(word(1, "So they take", "land nobody"), 0.4), size=24)

@sc("01d", "wander", VAL, {}, ch=2)
def _(fr, t):
    valley_rivers(fr, a=0.9)
    for n, c in (("CULHUACAN", TAR), ("AZCAPOTZALCO", TEP), ("TEXCOCO", ACO)): city(fr, n, a=1.0, side={"AZCAPOTZALCO": "l"}.get(n, "r"), r=7, size=22, dot=c, icon=False, dy=-24 if n == "CULHUACAN" else 0)
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
    city(fr, "TEXCOCO", a=1.0, side="b", r=7, size=22, dot=ACO, icon=False, dy=4)
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
    city(fr, "AZCAPOTZALCO", a=1.0, side="l", r=9, size=26, dot=TEP, icon=False, dx=-14)
    city(fr, "TLACOPAN", a=1.0, side="l", r=8, size=24, dot=TEP, icon=False, dy=26); city(fr, "TEXCOCO", a=1.0, side="r", r=8, size=24, dot=ACO, icon=False)
    city(fr, "TENOCHTITLAN", a=1.0, side="r", r=8, size=24, dot=AZ, icon=False, ll=C["TENOCH_ISL"], dy=24)
    ti = cue(4, "The Mesheeka choose")
    PQL(fr, *C["TENOCH_ISL"], "ITZCOATL", dx=130, dy=88, a=fr.R(ti, 0.4), size=28)
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

# ================= city plan helpers (schematic island)
def plan(fr, a=1.0, canals=True, grid_a=1.0, precinct=True, palace=True, market=False):
    """the island of Tenochtitlan with Tlatelolco: land colour over the lake, a canal grid, the Great Temple precinct, the king's palace"""
    p = [tuple(q) for q in proj(fr.cam, engine._chaikin(np.asarray(CITY_P, float), 2), 1)]
    poly(fr, p, ISLAND_C, a)
    pline(fr, p + [p[0]], color=ISLAND_E, width=2.4, a=a)
    if canals and grid_a > 0:
        ang = math.radians(17.0); ux, uy = math.sin(ang), math.cos(ang); vx, vy = uy, -ux       # canal axes: along the temple axis and across it
        for ax, bx in ((ux, uy), (vx, vy)):
            for k in np.arange(-0.040, 0.0401, 0.0042):
                ptsl = []; run = []
                for t_ in np.linspace(-0.07, 0.07, 280):
                    ll = (TEMPLE[0] + k * (vx if ax == ux else ux) / 1.0 + t_ * ax, TEMPLE[1] + k * (vy if ax == ux else uy) + t_ * bx)
                    ins = _inside(ll, CITY_P)
                    if ins: run.append(ll)
                    elif run: ptsl.append(run); run = []
                if run: ptsl.append(run)
                for r_ in ptsl:
                    if len(r_) > 3: pline(fr, proj(fr.cam, np.asarray(r_, float), 1), color=CAN, width=1.8, a=a * grid_a * 0.9)
    if precinct:
        x, y = P(fr.cam, *TEMPLE); hw = abs(P(fr.cam, TEMPLE[0] + 0.0014, TEMPLE[1])[0] - x); hh = abs(P(fr.cam, TEMPLE[0], TEMPLE[1] + 0.0014)[1] - y)
        poly(fr, [(x - hw, y - hh), (x + hw, y - hh), (x + hw, y + hh), (x - hw, y + hh)], AZ_L, a)
        pline(fr, [(x - hw, y - hh), (x + hw, y - hh), (x + hw, y + hh), (x - hw, y + hh), (x - hw, y - hh)], color=AZ_D, width=2.6, a=a)
        circ(fr, x, y, max(4, hw * 0.28), AZ, a)
    if palace:
        x, y = P(fr.cam, *PALACE); hw = abs(P(fr.cam, PALACE[0] + 0.0011, PALACE[1])[0] - x); hh = abs(P(fr.cam, PALACE[0], PALACE[1] + 0.0007)[1] - y)
        poly(fr, [(x - hw, y - hh), (x + hw, y - hh), (x + hw, y + hh), (x - hw, y + hh)], TAR, a)
    if market:
        x, y = P(fr.cam, *MARKET); hw = abs(P(fr.cam, MARKET[0] + 0.0016, MARKET[1])[0] - x); hh = abs(P(fr.cam, MARKET[0], MARKET[1] + 0.0011)[1] - y)
        poly(fr, [(x - hw, y - hh), (x + hw, y - hh), (x + hw, y + hh), (x - hw, y + hh)], PAPER, a)
        pline(fr, [(x - hw, y - hh), (x + hw, y - hh), (x + hw, y + hh), (x - hw, y + hh), (x - hw, y - hh)], color=AZ_D, width=2.6, a=a)
def causeways(fr, a=1.0, which=("N", "W", "S"), width=5.0):
    for nm, cw in (("N", CW_TEPEYAC), ("W", CW_TLACOPAN), ("S", CW_IZTAP)):
        if nm in which: gline(fr, smooth(cw, 6), color=AZ, width=width, a=a, halo=WHITE)
def fillemp(fr, a=1.0, color=AZ, k=0.62): terr(fr, "EMP", color, a * k)
def onland(fr, ll, key="EMP"):
    x, y = P(fr.cam, *ll); m = fr.masks[key]; k = m.size[0] / W; xi, yi = int(x * k), int(y * k)
    return 0 <= xi < m.size[0] and 0 <= yi < m.size[1] and m.getpixel((xi, yi)) > 100
def PW(fr, x, y, txt, t_in, t_out=None, size=28, **kw):
    """a plaque shown from chapter second t_in until t_out"""
    a = fr.R(t_in, 0.4) * (1 - (fr.R(t_out - 0.4, 0.4) if t_out else 0.0))
    PQ(fr, x, y, txt, a=a, size=size, **kw)

# ================= chapter 5
CORE_C = cam_box(-101.3, -94.2, 16.2, 20.9)
@sc("05a", "1440", CORE_C, {})
def _(fr, t):
    t0 = cue(5, "In 1440")
    PQ(fr, 400, 150, "1440", a=fr.R(t0, 0.4), size=44)
    PQ(fr, 1650, 230, "THE FIRST MOCTEZUMA", a=fr.R(word(5, "In 1440", "first Moctezuma"), 0.4), size=30)
    PQ(fr, 1650, 290, "NOT THE FAMOUS ONE", a=fr.R(cue(5, "This is not the famous"), 0.4), size=24)
    PQ(fr, 1650, 345, "HIS GREAT-GRANDFATHER", a=fr.R(cue(5, "This is his great"), 0.4), size=24)
    city(fr, "TENOCHTITLAN", a=1.0, side="l", r=8, size=24, dot=AZ, icon=False, ll=C["TENOCH_ISL"])
    tu = cue(5, "Under him")
    pulse(fr, C["TENOCH_ISL"], tu, 2.4, color=AZ)
    te = word(5, "They march east", "east"); ts_ = word(5, "They march east", "south")
    EAST = [C["TENOCH_ISL"], (-98.0, 19.25), (-96.9, 19.0), (-96.25, 18.85)]
    SOUTH = [C["TENOCH_ISL"], (-98.7, 18.6), (-97.9, 18.0), (-97.33, 17.69)]
    arrow(fr, EAST, te - 0.6, d=2.4, color=AZ, width=5.2); arrow(fr, SOUTH, ts_ - 0.6, d=2.4, color=AZ, width=5.2)
    sea(fr, -95.6, 20.75, "GULF OF MEXICO", a=fr.R(word(5, "They march east", "Gulf"), 0.5), size=22)
    region(fr, -98.9, 17.25, "OAXACA", a=fr.R(word(5, "They march east", "Oaxaca"), 0.5), size=26)
    tk = cue(5, "The kings after him")
    PQ(fr, 1650, 400, "THE KINGS AFTER HIM KEEP GOING", a=fr.R(tk, 0.4), size=24)
    arrow(fr, [(-96.25, 18.85), (-95.6, 18.2), (-94.7, 17.4)], tk + 0.2, d=1.4, color=AZ_D, width=4.2, dash=(10, 8))
    arrow(fr, [(-97.33, 17.69), (-96.6, 16.9), (-95.6, 16.4)], tk + 0.4, d=1.4, color=AZ_D, width=4.2, dash=(10, 8))

EMPC = cam_box(-102.8, -90.6, 13.6, 22.7)
def empire_tint(fr, a):
    """Tarascans and Tlaxcala in the neighbours' grey"""
    if a > 0:
        for k in ("TAR", "TLX", "HUEX"):
            if k in fr.masks: fr.fill(fr.masks[k], ENM, a * 0.5)
@sc("05b", "empire", EMPC, {"EMP": EMP, "TAR": TARM, "TLX": TLXM, "HUEX": HUEXM})
def _(fr, t):
    t0 = cue(5, "By 1502")
    terr(fr, "EMP", AZ, 0.62 * fr.R(t0 + 0.2, 7.0))
    PQ(fr, 400, 150, "1502", a=fr.R(t0, 0.4), size=44)
    PQ(fr, 400, 215, "AHUITZOTL", a=fr.R(word(5, "By 1502", "Ahuitzotl"), 0.4), size=28)
    city(fr, "TENOCHTITLAN", a=1.0, side="l", r=7, size=22, dot=AZ_D, icon=False, ll=C["TENOCH_ISL"], dy=-30)
    sea(fr, -94.0, 21.4, "GULF OF MEXICO", a=fr.R(word(5, "By 1502", "Gulf"), 0.5), size=24)
    sea(fr, -98.5, 14.4, "PACIFIC OCEAN", a=fr.R(word(5, "By 1502", "Pacific"), 0.5), size=24)
    ts = word(5, "By 1502", "Soconusco")
    tdot(fr, C["TAPACHULA"], a=fr.R(ts, 0.4), r=7, color=AZ_D); PQL(fr, *C["TAPACHULA"], "SOCONUSCO", dx=-120, dy=34, a=fr.R(ts, 0.4), size=24)
    modern(fr, -90.6, 15.35, "GUATEMALA", a=fr.R(word(5, "By 1502", "Guatemala"), 0.5), size=22)
    PQ(fr, 430, 800, "400–500 SMALL STATES", a=fr.R(cue(5, "Four to five"), 0.4), size=28)
    PQ(fr, 430, 865, "5–6 MILLION PEOPLE", a=fr.R(cue(5, "Five or six"), 0.4), size=28)
    PW(fr, 960, 960, "A DEFEATED KING USUALLY KEEPS HIS THRONE", cue(5, "A defeated king"), cue(5, "The rule is simple"), size=26)
    tr = cue(5, "The rule is simple"); tp = word(5, "The rule is simple", "pay")
    SRC = [C["TOCHTEPEC"], C["COIXTLAHUACA"], C["TAPACHULA"], C["CUERNAVACA"], (-93.5, 17.4), (-97.0, 20.6)]
    tx_ = cue(5, "Pay, and you are left alone")
    for i, src in enumerate(SRC):
        arrow(fr, [src, C["TENOCH_ISL"]], tp + 0.15 * i, d=2.2, color=AZ_D, width=3.6, halo=WHITE, a=out(fr, tx_, 0.8))
    PW(fr, 960, 960, "PAY · TWICE A YEAR · SEND SOLDIERS WHEN ASKED", tp, tx_, size=26)
    tg = cue(5, "And some neighbours")
    for i, ll in enumerate(((-96.6, 17.6), (-94.0, 17.3), (-98.3, 16.9), (-92.6, 15.8), (-97.2, 20.6))):
        pulse(fr, ll, cue(5, "Every Aztec king") + 0.25 * i, 2.8, color=AZ_D, rmax=40)
    PQ(fr, 960, 960, "EVERY AZTEC KING HAS TO PUT DOWN REBELLIONS", a=fr.R(cue(5, "Every Aztec king"), 0.4) * (1 - fr.R(tg - 0.4, 0.4)), size=26)
    empire_tint(fr, fr.R(tg, 1.4))
    PQ(fr, 960, 960, "SOME NEIGHBOURS NEVER GIVE IN", a=fr.R(tg, 0.4), size=26)

WESTC = cam_box(-103.9, -96.4, 17.3, 21.3)
@sc("05c", "neighbours", WESTC, {"EMP": EMP, "TAR": TARM, "TLX": TLXM, "HUEX": HUEXM})
def _(fr, t):
    terr(fr, "EMP", AZ, 0.30); empire_tint(fr, 1.0)
    city(fr, "TENOCHTITLAN", a=1.0, side="l", r=7, size=22, dot=AZ_D, icon=False, ll=C["TENOCH_ISL"], dy=34)
    tt = cue(5, "To the west")
    region(fr, -102.1, 20.1, "TARASCANS", a=fr.R(word(5, "To the west", "Tarascans"), 0.5), size=26)
    arrow(fr, [C["TENOCH_ISL"], (-99.9, 19.5), TAXIMAROA], tt + 1.2, d=2.0, color=AZ, width=5)
    cross(fr, *TAXIMAROA, a=fr.R(tt + 3.0, 0.4), r=16, width=6, color=AZ_D)
    PQ(fr, 400, 150, "LATE 1470s", a=fr.R(tt + 0.2, 0.4), size=40)
    PQ(fr, 960, 960, "THE EMPIRE'S ONE GREAT DEFEAT", a=fr.R(cue(5, "It is the empire"), 0.4), size=28)
    tl = cue(5, "To the east, the small")
    region(fr, -98.15, 19.95, "TLAXCALA", a=fr.R(tl, 0.5), size=26)
    pulse(fr, C["TLAXCALA"], tl + 0.5, 3.0, color=TLX, rmax=48)
    PQ(fr, 1480, 150, "AZTEC LAND ON EVERY SIDE", a=fr.R(word(5, "To the east, the small", "Aztec land"), 0.4), size=26)
    PQ(fr, 960, 880, "REMEMBER TLAXCALA", a=fr.R(cue(5, "Remember Tlaxcala"), 0.4), size=34)

# ================= chapter 6
ISLP = cam_box(-99.158, -99.102, 19.405, 19.470)
@sc("06a", "plan", ISLP, {}, rivers=False)
def _(fr, t):
    plan(fr); causeways(fr)
    PQL(fr, -99.112, 19.425, "TENOCHTITLAN", dx=150, dy=0, a=1.0, size=28)
    tp = cue(6, "Most estimates")
    PQ(fr, 400, 150, "200,000", a=fr.R(tp, 0.4), size=48)
    PQ(fr, 400, 215, "SOME SCHOLARS SAY FEWER, SOME SAY MANY MORE", a=fr.R(cue(6, "Some scholars"), 0.4), size=22, anchor="l")
    PQ(fr, 960, 960, "THE LARGEST CITY ANCIENT MEXICO EVER SAW", a=fr.R(cue(6, "Either way"), 0.4), size=28)

MKTC = cam_box(-99.152, -99.114, 19.428, 19.470)
@sc("06b", "tlatelolco", MKTC, {}, rivers=False)
def _(fr, t):
    plan(fr, market=True, palace=False)
    gline(fr, smooth([MARKET] + CW_TEPEYAC[3:], 6), color=AZ, width=5.0, halo=WHITE)          # the causeway beyond the market; the route temple -> market is the arrow only (no double stroke)
    tg = cue(6, "Then go north")
    arrow(fr, [TEMPLE, (-99.1335, 19.4430), MARKET], tg + 0.2, d=1.8, color=AZ, width=4.6)
    PQL(fr, *MARKET, "TLATELOLCO", dx=-250, dy=-18, a=fr.R(word(6, "Then go north", "Tlatelolco"), 0.4), size=34)
    PQ(fr, 1480, 150, "CORTES CLAIMS 60,000 A DAY", a=fr.R(cue(6, "Cort"), 0.4), size=26)
    PQ(fr, 1480, 215, "OTHER WITNESSES: 20,000–40,000", a=fr.R(cue(6, "Other witnesses"), 0.4), size=26)

# ================= chapter 8
TEMPC = cam_box(-99.150, -99.112, 19.419, 19.452)
@sc("08a", "temple", TEMPC, {}, rivers=False)
def _(fr, t):
    plan(fr, canals=True, palace=False)
    ts = cue(8, "Then, in 2015")
    x, y = P(fr.cam, *TEMPLE)
    PQ(fr, x + 190, y + 40, "GREAT TEMPLE", a=fr.R(word(8, "Then, in 2015", "Great Temple"), 0.4), size=30)
    PQ(fr, 400, 150, "2015", a=fr.R(ts, 0.4), size=44)
    ta = word(8, "Then, in 2015", "tower")
    tdot(fr, SKULLS, a=fr.R(ta, 0.3), r=9, color=AZ_D); pulse(fr, SKULLS, ta, 2.4, color=AZ_D)
    PQL(fr, *SKULLS, "A TOWER OF HUMAN SKULLS", dx=-190, dy=-70, a=fr.R(ta, 0.4), size=26)
    PQ(fr, 1480, 150, "MORE THAN 600 SO FAR", a=fr.R(cue(8, "More than six hundred"), 0.4), size=28)
    PQ(fr, 960, 960, "A CONQUISTADOR HAD DESCRIBED EXACTLY SUCH A TOWER", a=fr.R(cue(8, "A conquistador"), 0.4), size=26)

# ================= chapter 9
FLOWC = cam_box(-99.5, -96.9, 18.7, 20.1)
@sc("09a", "tlaxcala", FLOWC, {"EMP": EMP, "TLX": TLXM, "HUEX": HUEXM}, rivers=False)
def _(fr, t):
    terr(fr, "EMP", AZ, 0.34); terr(fr, "TLX", TLX, 0.9 * fr.R(0.5, 1.0)); fr.fill(fr.masks["HUEX"], ENM, 0.45)
    city(fr, "TENOCHTITLAN", a=1.0, side="l", r=8, size=24, dot=AZ, icon=False, ll=C["TENOCH_ISL"])
    city(fr, "TLAXCALA", a=fr.R(0.3, 0.4), side="r", r=8, size=26, dot=TLX, icon=False); pulse(fr, C["TLAXCALA"], 0.6, 2.4, color=TLX)
    tf = cue(9, "The Aztecs fought")
    for i in range(3): arrow(fr, [C["TENOCH_ISL"], (-98.7, 19.40), C["TLAXCALA"]], tf + 0.5 + 0.8 * i, d=1.6, color=AZ, width=4.4)
    PQ(fr, 960, 140, "THE FLOWER WAR", a=fr.R(word(9, "The Aztecs fought", "flower war"), 0.4), size=40)
    PQ(fr, 960, 960, "AT AN AGREED PLACE AND TIME", a=fr.R(cue(9, "A flower war was"), 0.4) * (1 - fr.R(cue(9, "The warriors arrived") - 0.4, 0.4)), size=28)
    PQ(fr, 960, 960, "THE POINT WAS TO TAKE PRISONERS", a=fr.R(cue(9, "The point was to take"), 0.4) * (1 - fr.R(cue(9, "These wars began") - 0.4, 0.4)), size=28)
    PQ(fr, 400, 215, "UNDER THE FIRST MOCTEZUMA", a=fr.R(cue(9, "These wars began"), 0.4), size=26)
    PQ(fr, 960, 960, "TRAINING · RELIGION · A SHOW OF STRENGTH", a=fr.R(cue(9, "For the Aztecs"), 0.4) * (1 - fr.R(cue(9, "For Tlaxcala") - 0.4, 0.4)), size=28)
    tk = cue(9, "Year after year")
    arrow(fr, [C["TLAXCALA"], (-98.7, 19.40), C["TENOCH_ISL"]], tk, d=2.4, color=TLX, width=5.4)
    PQ(fr, 960, 960, "CARRIED OFF TO DIE IN TENOCHTITLAN", a=fr.R(tk, 0.4), size=28)

CITIES9 = [C[k] for k in ("CUERNAVACA", "TEOTITLAN", "COIXTLAHUACA", "TOCHTEPEC", "OAXACA", "TAPACHULA", "CEMPOALA", "TOLLAN", "TABASCO")]
EMPD = cam_box(-102.8, -91.5, 14.4, 22.4)
@sc("09b", "weakness", EMPD, {"EMP": EMP, "TAR": TARM, "TLX": TLXM, "HUEX": HUEXM})
def _(fr, t):
    terr(fr, "EMP", AZ, 0.58)
    ti = cue(9, "Inside its borders")
    rng = np.random.RandomState(7)
    k = 0
    for ll in CITIES9:
        for j in range(5):
            q = (ll[0] + rng.uniform(-0.55, 0.55), ll[1] + rng.uniform(-0.45, 0.45))
            if _inside(q, EMP_P) and not _inside(q, TLX_P) and not _inside(q, TUT_P) and onland(fr, q):
                tdot(fr, q, a=fr.R(ti + 0.045 * k, 0.3), r=3.6, color=AZ_D); k += 1
    tdot(fr, C["TENOCH_ISL"], r=8, color=AZ_D); PQL(fr, *C["TENOCH_ISL"], "TENOCHTITLAN", dx=-70, dy=-60, size=22)
    PQ(fr, 960, 960, "HUNDREDS OF CITIES · THEY PAY ONLY BECAUSE THEY MUST", a=fr.R(ti, 0.4) * (1 - fr.R(cue(9, "Next door") - 0.4, 0.4)), size=26)
    tn = cue(9, "Next door")
    empire_tint(fr, fr.R(tn, 1.2))
    region(fr, -97.4, 19.9, "TLAXCALA", a=fr.R(tn + 0.6, 0.5), size=24); region(fr, -102.1, 20.35, "TARASCANS", a=fr.R(tn + 0.3, 0.5), size=24)
    PQ(fr, 960, 960, "ENEMIES WITH EVERY REASON TO WANT REVENGE", a=fr.R(tn, 0.4) * (1 - fr.R(cue(9, "All that holds") - 0.4, 0.4)), size=26)
    tf = cue(9, "All that holds")
    pulse(fr, C["TENOCH_ISL"], tf, 3.4, color=AZ_D, n=3, rmax=70, width=4, period=1.0)
    PQ(fr, 960, 960, "FEAR OF ONE CITY ON A LAKE", a=fr.R(tf, 0.4) * (1 - fr.R(cue(9, "In 1502") - 0.4, 0.4)), size=28)
    t19 = cue(9, "As the year 1519")
    PQ(fr, 400, 150, "1519", a=fr.R(t19, 0.4), size=44)
    pulse(fr, C["TENOCH_ISL"], t19 + 1.0, 4.0, color=AZ, n=3, rmax=80, width=4, period=1.1)
    PQ(fr, 960, 960, "NO POWER CAN CHALLENGE TENOCHTITLAN", a=fr.R(word(9, "As the year 1519", "no power"), 0.4), size=28)

# ================= chapter 10
SEAC = cam_box(-97.6, -79.6, 16.4, 24.2)
@sc("10a", "voyage", SEAC, {})
def _(fr, t):
    t0 = cue(10, "In February")
    PQ(fr, 440, 150, "FEBRUARY 1519", a=fr.R(t0, 0.4), size=40)
    region(fr, -80.7, 22.35, "CUBA", a=fr.R(t0 - 0.2, 0.5), size=26)
    tdot(fr, C["HAVANA"], r=7, color=AZ_D)
    VOY = [C["HAVANA"], (-83.4, 23.45), (-84.8, 22.55), (-85.4, 21.75), C["COZUMEL"], (-86.45, 21.25), (-86.6, 21.95), (-88.2, 21.85), (-90.3, 21.6), (-91.2, 20.3), (-92.0, 19.0), C["TABASCO"], (-93.2, 18.9), (-94.6, 19.0), C["VERACRUZ"]]
    arrow(fr, VOY, t0 + 0.4, d=9.0, color=AZ, width=5.0, n=12)
    for i, (txt, w) in enumerate((("11 SHIPS", "eleven"), ("ABOUT 500 SOLDIERS", "five hundred"), ("16 HORSES", "sixteen"))):
        PQ(fr, 440, 230 + 62 * i, txt, a=fr.R(word(10, "In February", w), 0.4), size=28)
    PQ(fr, 960, 960, "THE GOVERNOR OF CUBA HAS TRIED TO REPLACE HIM", a=fr.R(cue(10, "The governor"), 0.4), size=26)

ROUTEB = cam_box(-99.7, -95.7, 18.4, 20.1)
@sc("10b", "inland", ROUTEB, {"EMP": EMP, "TLX": TLXM, "HUEX": HUEXM})
def _(fr, t):
    terr(fr, "EMP", AZ, 0.30); fr.fill(fr.masks["HUEX"], ENM, 0.45)
    city(fr, "TENOCHTITLAN", a=1.0, side="l", r=8, size=24, dot=AZ_D, icon=False, ll=C["TENOCH_ISL"], dy=-30)
    t0 = cue(10, "Cort" + "\u00e9s destroys")
    tdot(fr, C["VERACRUZ"], r=7, color=INK); cross(fr, *C["VERACRUZ"], a=fr.R(t0, 0.4), r=14, width=6, color=AZ_D)
    PQ(fr, 400, 150, "SHIPS DESTROYED", a=fr.R(word(10, "Cort" + "és destroys", "ships"), 0.4), size=30)
    ta = word(10, "Cort" + "és destroys", "August")
    PQ(fr, 400, 215, "AUGUST", a=fr.R(ta, 0.4), size=30)
    ROUTE1 = [C["VERACRUZ"], (-96.6, 19.5), (-97.1, 19.55), (-97.7, 19.5), C["TLAXCALA"]]
    arrow(fr, ROUTE1, ta - 0.4, d=4.0, color=AZ, width=5.0)
    tt = cue(10, "Tlaxcala fights")
    city(fr, "TLAXCALA", a=fr.R(tt, 0.4), side="l", r=8, size=26, dot=TLX, icon=False, dy=44); pulse(fr, C["TLAXCALA"], tt, 2.6, color=TLX, rmax=40)
    fr.fill(fr.masks["TLX"], TLX, 0.6 * fr.R(tt, 1.2))
    PQ(fr, 960, 960, "THEN IT MAKES A DECISION", a=fr.R(cue(10, "Then it makes"), 0.4) * (1 - fr.R(cue(10, "These strangers") - 0.4, 0.4)), size=28)
    tw = cue(10, "These strangers")
    ROUTE2 = [C["TLAXCALA"], C["CHOLULA"], (-98.75, 19.17), (-99.0, 19.30), C["IZTAPALAPA"], C["TENOCH_ISL"]]
    arrow(fr, ROUTE2, tw, d=2.8, color=TLX, width=5.4)
    PQ(fr, 960, 960, "A WEAPON AGAINST TENOCHTITLAN", a=fr.R(tw, 0.4), size=28)

# ================= chapter 11
RTC = cam_box(-99.7, -95.9, 18.7, 20.1)
ISL4 = cam_box(-99.19, -99.07, 19.385, 19.485)
LAKEC = cam_box(-99.32, -98.15, 19.18, 19.72)
W2 = cam_box(-99.5, -97.9, 19.0, 19.95)
CAM11 = mover([(0, RTC), (9.5, RTC), (13.0, ISL4), (30.0, ISL4), (37.0, LAKEW), (49.0, LAKEW), (53.0, W2), (60.0, W2)])
@sc("11a", "alvarado", CAM11, {"TLX": TLXM})
def _(fr, t):
    live(fr, 0, 60)
    pa = fr.R(10.5, 2.0) * (1 - fr.R(35.0, 3.0))
    if pa > 0: plan(fr, a=pa); causeways(fr, a=pa)
    city(fr, "TENOCHTITLAN", a=1.0, side="r", r=8, size=24, dot=AZ, icon=False, ll=C["TENOCH_ISL"], dy=34)
    t1 = cue(11, "Then, in the spring")
    PQ(fr, 400, 150, "SPRING 1520", a=fr.R(t1, 0.4) * (1 - fr.R(cue(11, "On the night of the thirtieth") - 0.4, 0.4)), size=40)
    COAST = (-96.4, 19.45)
    arrow(fr, [C["TENOCH_ISL"], (-98.4, 19.55), (-97.3, 19.5), COAST], t1 + 0.4, d=3.4, color=AZ, width=5.0, a=out(fr, 14.0, 1.0))
    t2 = cue(11, "A second Spanish")
    arrow(fr, [(-95.3, 19.65), COAST], t2 + 0.2, d=1.8, color=SPA, width=5.0, a=out(fr, 14.0, 1.0))
    PQ(fr, 1480, 150, "800+ SOLDIERS FROM CUBA TO ARREST HIM", a=fr.R(t2, 0.4) * (1 - fr.R(cue(11, "He leaves about") - 0.4, 0.4)), size=24)
    t3 = cue(11, "He leaves about")
    PW(fr, 960, 960, "ABOUT 80 MEN UNDER PEDRO DE ALVARADO", t3, 29.0, size=28)
    t4 = cue(11, "On the night of the thirtieth")
    gline(fr, smooth(CW_TLACOPAN, 6), color=AZ, width=5.0, a=fr.R(t4 - 2.0, 0.6), halo=WHITE)
    PQ(fr, 400, 150, "30 JUNE 1520", a=fr.R(t4, 0.4), size=40)
    ESC = [C["TENOCH_ISL"], (-99.150, 19.4430), (-99.170, 19.4515), C["TLACOPAN"]]
    arrow(fr, ESC, t4 + 1.0, d=3.0, color=SPA, width=5.4)
    tc = cue(11, "They are caught")
    cross(fr, -99.163, 19.449, a=fr.R(tc, 0.4), r=16, width=6, color=AZ_D); pulse(fr, (-99.163, 19.449), tc, 2.6, color=AZ_D, rmax=44)
    PQ(fr, 960, 960, "MORE THAN HALF HIS MEN", a=fr.R(cue(11, "Cort" + "és loses"), 0.4) * (1 - fr.R(cue(11, "The Spanish call it") - 0.4, 0.4)), size=28)
    PQ(fr, 960, 960, "THE NIGHT OF SORROWS", a=fr.R(cue(11, "The Spanish call it"), 0.4) * (1 - fr.R(cue(11, "And Tlaxcala") - 0.4, 0.4)), size=34)
    ts = cue(11, "The survivors")
    FLEE = [C["TLACOPAN"], (-99.15, 19.55), (-99.05, 19.66), (-98.75, 19.70), (-98.50, 19.62), C["TLAXCALA"]]
    arrow(fr, FLEE, ts, d=2.4, color=SPA, width=5.4)
    tk = cue(11, "And Tlaxcala")
    city(fr, "TLAXCALA", a=fr.R(ts + 1.4, 0.4), side="l", r=8, size=26, dot=TLX, icon=False, dy=40)
    fr.fill(fr.masks["TLX"], TLX, 0.6 * fr.R(tk, 1.0)); pulse(fr, C["TLAXCALA"], tk, 2.4, color=TLX, rmax=40)
    PQ(fr, 960, 960, "TLAXCALA TAKES THEM IN", a=fr.R(tk, 0.4), size=28)

SIEGE = mover([(69.75, LAKEC), (78.0, LAKEC), (83.0, LAKEW), (90.0, LAKEW)])
@sc("11b", "siege", SIEGE, {"TLX": TLXM})
def _(fr, t):
    live(fr, 69.75, 90)
    valley_rivers(fr, a=0.7)
    city(fr, "TENOCHTITLAN", a=1.0, side="l", r=8, size=24, dot=AZ, icon=False, ll=C["TENOCH_ISL"], dx=-30, dy=-95)
    city(fr, "TLAXCALA", a=1.0, side="l", r=7, size=24, dot=TLX, icon=False, dy=40)
    t0 = cue(11, "In May 1521")
    PQ(fr, 400, 150, "MAY 1521", a=fr.R(t0, 0.4), size=44)
    t1 = cue(11, "He has thirteen")
    for i in range(13):
        tdot(fr, (-99.03 + 0.012 * (i % 7) - 0.006 * (i // 7), 19.47 - 0.010 * (i // 7)), a=fr.R(t1 + 0.12 * i, 0.3), r=5, color=INK)
    PQ(fr, 1480, 150, "13 SHIPS BUILT FOR THE LAKE", a=fr.R(t1, 0.4), size=26)
    PQ(fr, 1480, 215, "ABOUT 1,000 SPANIARDS", a=fr.R(t1 + 2.0, 0.4), size=26)
    t2 = cue(11, "With them march")
    for i, src in enumerate((C["TLAXCALA"], C["TEXCOCO"], C["CHALCO"], C["COYOACAN"])):
        arrow(fr, [src, C["TENOCH_ISL"]], t2 + 0.3 * i, d=2.0, color=TLX, width=4.2, dash=(10, 8))
    PQ(fr, 1480, 280, "ALLIES: TENS OF THOUSANDS", a=fr.R(t2, 0.4), size=26)
    PQ(fr, 1480, 345, "SOME COUNTS SAY 200,000", a=fr.R(cue(11, "Some counts"), 0.4), size=24)
    t3 = cue(11, "They cut the aqueduct")
    ax_, ay_ = along(AQUEDUCT, 0.5); cross(fr, ax_, ay_, a=fr.R(t3, 0.3), r=14, width=6, color=AZ_D)
    PQ(fr, 960, 960, "THEY CUT THE AQUEDUCT", a=fr.R(t3, 0.3) * (1 - fr.R(t3 + 1.2, 0.3)), size=28)
    t4 = cue(11, "They block")
    for k, cw in enumerate((CW_TEPEYAC, CW_TLACOPAN, CW_IZTAP)):
        q = along(cw, 0.7); cross(fr, *q, a=fr.R(t4 + 0.25 * k, 0.3), r=14, width=6, color=AZ_D)
    PQ(fr, 960, 960, "THEY BLOCK THE CAUSEWAYS", a=fr.R(t4, 0.3) * (1 - fr.R(cue(11, "The siege lasts") - 0.3, 0.3)), size=28)
    PQ(fr, 960, 960, "THE SIEGE LASTS ABOUT THREE MONTHS", a=fr.R(cue(11, "The siege lasts"), 0.3), size=28)

# ================= chapter 12
HOND = cam_box(-100.2, -86.5, 13.6, 20.6)
CAM12 = mover([(0, ISL4), (6.5, ISL4), (10.0, HOND), (16.0, HOND)])
@sc("12a", "ruins", CAM12, {})
def _(fr, t):
    live(fr, 0, 16)
    pa = 1 - fr.R(6.5, 1.5)
    if pa > 0: plan(fr, a=pa); causeways(fr, a=pa)
    t0 = 0.2
    PQ(fr, 960, 960, "ON TOP OF THE RUINS", a=fr.R(word(12, "Cort" + "és builds", "on top"), 0.4) * (1 - fr.R(cue(12, "It is Mexico City") - 0.4, 0.4)), size=28)
    tm = cue(12, "It is Mexico City")
    PQL(fr, *C["TENOCH_ISL"], "MEXICO CITY", dx=0, dy=-60, a=fr.R(tm, 0.4) * (1 - fr.R(8.4, 1.0)), size=36)
    tdot(fr, C["TENOCH_ISL"], r=8, color=AZ_D)
    tc = cue(12, "Cuauhtemoc stays")
    PQ(fr, 960, 140, "CUAUHTEMOC STAYS A PRISONER", a=fr.R(tc, 0.4) * (1 - fr.R(9.0, 0.6)), size=30)
    th = cue(12, "In 1525")
    PQ(fr, 400, 150, "1525", a=fr.R(th, 0.4), size=44)
    MARCH = [C["TENOCH_ISL"], (-97.0, 18.7), (-94.4, 18.15), (-92.7, 17.9), (-91.0, 17.6), (-89.2, 16.4), (-88.5, 15.7)]
    arrow(fr, MARCH, th + 0.3, d=3.4, color=AZ, width=5.0, n=10)
    modern(fr, -88.0, 14.9, "HONDURAS", a=fr.R(word(12, "In 1525", "Honduras"), 0.5), size=22)
    cross(fr, -91.0, 17.6, a=fr.R(th + 3.2, 0.4), r=16, width=6, color=AZ_D)
    PQ(fr, 960, 960, "CORTES HAS HIM HANGED", a=fr.R(word(12, "In 1525", "has him"), 0.4), size=28)

DRYC = cam_box(-99.32, -98.82, 19.20, 19.82)
def LAKES_M(cam, lm):
    return reduce(IC.lighter, [engine.poly_mask(cam, r, True) for r in LAKE_RINGS])
@sc("12b", "drained", DRYC, {"LAKES": LAKES_M})
def _(fr, t):
    valley_rivers(fr, a=0.8)
    td = cue(12, "The lake goes too"); tn = cue(12, "The new rulers")
    dry = fr.R(td + 0.4, 6.0) * 0.96
    if dry > 0: fr.fill(fr.masks["LAKES"], DRY_C, dry)
    PQ(fr, 960, 140, "THE LAKE GOES TOO", a=fr.R(td, 0.4) * (1 - fr.R(tn - 0.4, 0.4)), size=40)
    PQ(fr, 960, 960, "FINISHED IN THE LATE 19TH CENTURY", a=fr.R(word(12, "The new rulers", "late nineteenth"), 0.4), size=28)
    modern(fr, -99.13, 19.43, "MEXICO CITY", dx=135, dy=-8, a=fr.R(tn + 2.0, 0.6), size=24, color=(70, 60, 46))

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
    elif mode == "sweep":       # six stills spread over each layout window, one strip per scene (dense check)
        pref = sys.argv[3:]
        for n, s_ in SC.items():
            if pref and not any(n.startswith(p) for p in pref): continue
            s_.frame(0.0); ims = []
            wins = WIN[(n.split("_")[0], s_.ch)]; a0, b1 = wins[0][0], wins[-1][1]
            for k in range(6):
                tt = a0 + (b1 - a0) * (0.08 + 0.84 * k / 5)
                if not any(a <= tt <= b for a, b in wins): tt = min((x for w in wins for x in w), key=lambda x: abs(x - tt))
                im = s_.frame(tt - s_.t0).resize((640, 360), Image.LANCZOS); d = ImageDraw.Draw(im); d.rectangle([0, 0, 250, 16], fill=(17, 17, 17))
                d.text((4, 3), f"{n} VO {tt:5.1f}", fill=(255, 255, 255)); ims.append(im)
            clear(s_)
            sh = Image.new("RGB", (3 * 640, 2 * 360), (17, 17, 17))
            for i, im in enumerate(ims): sh.paste(im, (i % 3 * 640, i // 3 * 360))
            sh.save(f"{HERE}/test_look/sweep_{n}.jpg", quality=84); print(n, flush=True)
    elif mode == "still":
        for spec in sys.argv[2:]:
            n, ts = spec.split("@"); s_ = SC[n]; s_.frame(0.0)
            for tt in ts.split(","): s_.still(float(tt) - s_.t0, f"{HERE}/test_look/{n}_{float(tt):05.1f}.jpg", 0.75)
    else:
        os.makedirs(f"{HERE}/out_look", exist_ok=True)
        for n in sys.argv[2:]:
            t0 = time.time(); SC[n].render(f"{HERE}/out_look"); clear(SC[n]); print(n, round(time.time() - t0, 1), flush=True)
