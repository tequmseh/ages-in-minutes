"""The Vikings in 20 Minutes: map scenes, timed to the recorded voiceover (chapter seconds).
usage: python3 vk_scenes.py list | still name@t,t (chapter seconds) | sheet [names] | render names..."""
from vk_base import *
BLACK = (17, 17, 17); PAPER = (250, 247, 240)

# ---------------------------------------------------------------- helpers
def blank(fr, color=BLACK):
    fr.im.paste(color, (0, 0, fr.im.size[0], fr.im.size[1])); fr.d = ImageDraw.Draw(fr.im)
def rect(fr, x0, y0, x1, y1, color, a=1.0):
    alpha_draw(fr, lambda d, c: d.rectangle([s(x0), s(y0), s(x1), s(y1)], fill=c), color, a)
def poly(fr, pts, color, a=1.0):
    alpha_draw(fr, lambda d, c: d.polygon([(s(x), s(y)) for x, y in pts], fill=c), color, a)
def lship(fr, x, y, k=1.0, a=1.0, color=INK, sail=PAPER, flip=False, stripes=NOR):
    """small longship glyph: curved hull, mast, striped square sail; x, y = middle of the waterline"""
    if a <= 0: return
    f = -1 if flip else 1
    hull = [(-24, -9), (-21, -11), (-17, -3), (-9, 1), (9, 1), (17, -3), (22, -12), (25, -10), (21, 1), (13, 6), (-13, 6), (-20, 1)]
    poly(fr, [(x + f * px * k, y + py * k) for px, py in hull], color, a)
    rect(fr, x - 1.1 * k, y - 26 * k, x + 1.1 * k, y + 1 * k, color, a)
    rect(fr, x - 12 * k, y - 25 * k, x + 12 * k, y - 8 * k, sail, a)
    if k >= 0.8:
        for i in (-8, 0, 8): rect(fr, x + (i - 2) * k, y - 25 * k, x + (i + 2) * k, y - 8 * k, stripes, a)
    alpha_draw(fr, lambda d, c: d.rectangle([s(x - 12 * k), s(y - 25 * k), s(x + 12 * k), s(y - 8 * k)], outline=c, width=max(1, s(1.2 * k))), color, a)
def gship(fr, lon, lat, dx=0, dy=0, **kw):
    x, y = P(fr.cam, lon, lat); lship(fr, x + dx, y + dy, **kw)
def sail_along(fr, path, q, k=0.8, a=1.0, **kw):
    """ship glyph at fraction q of a lon/lat path"""
    if a <= 0 or q <= 0: return
    p = partial(proj(fr.cam, path, 1), min(q, 1.0))[-1]; lship(fr, p[0], p[1] - 4, k=k, a=a, **kw)
def tline(fr, a, k, left="", right="", title="", x0=210, w=1500, y0=1012, ra=1.0):
    """timeline strip in the bottom safe band: black strip, yellow bar growing with k"""
    if a <= 0: return
    rect(fr, x0 - 60, y0 - 52, x0 + w + 60, y0 + 52, BLACK, a * 0.94)
    rect(fr, x0, y0 - 4, x0 + w, y0 + 4, (70, 72, 75), a)
    rect(fr, x0, y0 - 9, x0 + w * max(0.0, min(1.0, k)), y0 + 9, YELLOW, a)
    for xx in (x0, x0 + w * max(0.0, min(1.0, k))): rect(fr, xx - 2, y0 - 18, xx + 2, y0 + 18, YELLOW, a)
    if left: T(fr, x0, y0 - 32, left, size=22, w="b", sp=2, color=WHITE, a=a)
    if right: T(fr, x0 + w, y0 - 32, right, size=22, w="b", sp=2, color=WHITE, a=a * ra, anchor="r")
    if title: T(fr, x0 + w / 2, y0 + 33, title, size=17, w="s", sp=4, color=WHITE, a=a * ra, anchor="m")
def scatter(fr, key, n, seed=3, box=None):
    """n random lon/lat points inside mask `key` (fixed camera only); cached on the scene"""
    c = getattr(fr.scene, "_sc", None)
    if c is None: c = fr.scene._sc = {}
    k = (key, n, seed, fr.cam)
    if k not in c:
        m = np.asarray(fr.masks[key]); ys, xs = np.nonzero(m[::4, ::4] > 200); rng = np.random.default_rng(seed); out = []
        if len(xs):
            idx = rng.choice(len(xs), size=min(n, len(xs)), replace=False)
            out = [((xs[i] * 4 + 2) / SS, (ys[i] * 4 + 2) / SS) for i in idx]
        c[k] = out
    return c[k]
def dots_px(fr, pts, a_fn, r=3.2, color=INK, ring=WHITE):
    for i, (x, y) in enumerate(pts):
        a = a_fn(i)
        if a <= 0: continue
        if ring: circ(fr, x, y, r + 1.6, ring, a)
        circ(fr, x, y, r, color, a)
def circ(fr, x, y, r, color=None, a=1.0, outline=None, width=2):
    if a <= 0: return
    if color is not None: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=c), color, a)
    if outline is not None: alpha_draw(fr, lambda d, c: d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], outline=c, width=s(width)), outline, a)
def col(fr, x, y, items, size=22, gap=58, anchor="l", light=True, first_dark=False, dim=1.0):
    """column of plaques: items = [(text, t0)]"""
    for i, (txt, t0) in enumerate(items):
        PQ(fr, x, y + i * gap, txt, a=fr.R(t0, 0.4) * dim, size=size, anchor=anchor, light=light and not (first_dark and i == 0), pad=(12, 8))
def arrow(fr, pts, t0, d=1.4, width=4.2, a=1.0, n=10, **kw):
    gline(fr, smooth(pts, n) if len(pts) > 2 else pts, width=width, frac=fr.R(t0, d), arrow=True, halo=kw.pop("halo", WHITE), a=a, **kw)
def out(fr, t0, d=0.5): return 1 - fr.R(t0, d)

SCAND = cam_box(2, 30, 53.8, 71.3)
EUR = cam_box(-27, 50, 31, 68.5)
WORLD = cam_box(-62, 56, 34, 72)
WEUR = cam_box(-13, 22, 42, 62.5)
EAST = cam_box(9, 57, 39.5, 66.5)

# ================= 0. Cold open, VO 45.1-49.7: the edge of the map, then all over it
_c = mover([(45.1, cam_box(-2, 34, 53, 71.5)), (45.5, cam_box(-2, 34, 53, 71.5)), (48.6, WORLD)])
@scene("00_cold_open", 0, 45.1, 49.8, _c, dict(sc=U(NORWAY, SWEDEN, DENMARK)), res="50")
def _(fr, t):
    terr(fr, "sc", NOR)
    for i, (ll, bend) in enumerate((((-6.3, 53.3), 0.12), ((2.3, 48.9), 0.1), ((-21.9, 64.1), -0.1), ((-45.5, 61), -0.12), ((-55.5, 51.6), -0.16), ((30.5, 50.4), -0.1),
                                    ((29, 41), -0.14), ((48, 46.5), -0.18))):
        gline(fr, arc((9 if ll[0] < 9 else 17, 60), ll, bend), width=3.6, frac=fr.R(46.6 + 0.12 * i, 1.6), arrow=True, halo=WHITE)

# ================= 1a. VO 21.6-74.9: Scandinavia, three lands, water as the road, runes
COASTN = COAST(NORWAY_P, 0.5)
SEAWAYS = [[(10.6, 59.0), (9.5, 58.0), (7.0, 57.7), (5.2, 59.0), (4.6, 61.0), (5.6, 62.6), (8.6, 63.9), (11.2, 65.2), (12.6, 67.2), (15.5, 68.9), (19.0, 70.2)],
           [(10.6, 59.0), (11.0, 57.6), (11.4, 56.4), (12.6, 55.9), (12.7, 55.0), (14.5, 55.0), (16.6, 56.2), (17.4, 58.0), (18.6, 59.2), (19.0, 60.6), (18.0, 62.2), (20.6, 63.6), (22.2, 65.2)],
           [(12.6, 55.9), (11.0, 55.4), (10.6, 54.6)], [(7.0, 57.7), (8.2, 57.0), (8.0, 55.4)], [(17.4, 58.0), (18.6, 57.5)], [(18.6, 59.2), (21.5, 59.6), (24.5, 59.8)]]
@scene("01a_scandinavia", 1, 21.6, 74.9, SCAND, dict(dk=DENMARK, sw=SWEDEN, no=NORWAY, x_fj=COASTN), res="10")
def _(fr, t):
    PQ(fr, 330, 110, "SCANDINAVIA", a=fr.R(22.8, 0.5) * out(fr, 40.0), size=34)
    terr(fr, "dk", NOR_L, fr.R(24.4, 0.8) * (1 - 0.45 * fr.R(40.2, 0.8))); terr(fr, "sw", (176, 186, 140), fr.R(29.9, 0.8) * (1 - 0.45 * fr.R(40.2, 0.8)))
    terr(fr, "no", (178, 170, 158), fr.R(32.3, 0.8) * (1 - 0.45 * fr.R(40.2, 0.8)))
    mfill(fr, fr.masks["x_fj"], NOR_D, fr.R(34.2, 1.0) * 0.55 * out(fr, 40.2, 0.8))
    region(fr, 9.4, 56.25, "DENMARK", a=fr.R(24.5, 0.5), size=22, sp=5, w="b"); region(fr, 16.0, 60.6, "SWEDEN", a=fr.R(30.0, 0.5), size=26, sp=8, w="b")
    region(fr, 8.6, 61.0, "NORWAY", a=fr.R(32.4, 0.5), size=26, sp=8, w="b")
    sea(fr, 4.2, 56.6, "NORTH SEA", a=fr.R(27.4, 0.5), size=19); sea(fr, 19.4, 56.2, "BALTIC", a=fr.R(28.6, 0.5), size=19)
    gline(fr, [(10.9, 57.6), (12.4, 55.2)], width=3, frac=fr.R(26.6, 0.8), dash=(9, 7), color=CHAR, a=out(fr, 31.0))
    TL(fr, 4.2, 62.6, "HUNDREDS OF FJORDS", size=16, sp=2, anchor="r", dx=-6, a=fr.R(34.4, 0.5) * out(fr, 40.0))
    PQ(fr, 1560, 150, "AROUND 800", a=fr.R(40.4, 0.5) * out(fr, 52.9), size=32)
    PQ(fr, 1560, 214, "NO COUNTRIES AS WE KNOW THEM", a=fr.R(41.6, 0.5) * out(fr, 52.9), size=20, light=True, pad=(12, 8))
    col(fr, 1352, 300, [("KINGS", 44.4), ("CHIEFTAINS", 46.6), ("FAMILY FARMS", 48.0), ("LOCAL ASSEMBLIES", 49.4)], size=19, gap=50, dim=out(fr, 52.9))
    for i, ll in enumerate(((9.57, 54.49), (17.55, 59.33), (10.2, 59.0), (9.9, 55.35))):
        city(fr, "", ll=ll, label="", r=4.2, a=fr.R(51.0 + 0.2 * i, 0.5) * out(fr, 65.0))
    # water holds it together
    w = fr.R(53.3, 0.6) * out(fr, 65.3)
    for i, l in enumerate(SEAWAYS): gline(fr, smooth(l, 10), width=3.4, frac=fr.R(53.6 + 0.5 * i, 2.6), color=WHITE, a=w * 0.95)
    for i, (l, t0) in enumerate(((SEAWAYS[0], 59.6), (SEAWAYS[1], 60.2))): sail_along(fr, smooth(l, 10), 0.08 + 0.5 * ease((t - t0) / 5.5), k=0.75, a=fr.R(t0, 0.4) * w)
    live(fr, 59.6, 65.8)
    PQ(fr, 1560, 150, "WATER", a=fr.R(54.6, 0.4) * w, size=32); PQ(fr, 1560, 214, "THE SEA IS THE MOTORWAY", a=fr.R(59.5, 0.4) * w, size=22, light=True, pad=(12, 8))
    # runes: the Rök stone cut-out stands on the right (insert V01)
    PQ(fr, 420, 150, "RUNES", a=fr.R(69.0, 0.4), size=34); PQ(fr, 420, 216, "SIXTEEN SIGNS", a=fr.R(69.9, 0.4), size=22, light=True, pad=(12, 8))
    col(fr, 262, 290, [("STONE, WOOD AND BONE", 71.0), ("NOT BOOKS", 73.6)], size=18, gap=48)

# ================= 1b. VO 74.9-91.1: other people write about them; the sagas
@scene("01b_writers", 1, 74.9, 91.2, EUR, dict(sc=U(NORWAY, SWEDEN, DENMARK), ice=ICELAND), res="50")
def _(fr, t):
    terr(fr, "sc", NOR_L)
    w = out(fr, 81.4)
    for i, (ll, txt, t0, dx, dy) in enumerate((((-1.5, 53.0), "ENGLISH MONKS", 78.2, -190, 40), ((3.0, 47.6), "FRANKISH ANNALISTS", 79.2, -120, 80), ((44.4, 33.3), "ARAB TRAVELLERS", 80.2, -150, -64))):
        gline(fr, arc(ll, (12 + 3 * i, 59), 0.12 if i < 2 else -0.16), width=3, frac=fr.R(t0, 1.2), dash=(10, 7), arrow=True, color=CHAR, a=w)
        city(fr, "", ll=ll, label="", r=5, a=fr.R(t0, 0.4) * w); PQL(fr, *ll, txt, dx=dx, dy=dy, a=fr.R(t0, 0.4) * w, size=22, pad=(12, 8))
    PQ(fr, 960, 110, "OTHER PEOPLE WRITE ABOUT THEM", a=fr.R(75.4, 0.5) * w, size=28)
    terr(fr, "ice", NOR, fr.R(83.6, 0.8)); pulse(fr, (-18.5, 64.9), 83.8, 2.6, color=NOR_D, rmax=60, width=4)
    region(fr, -18.5, 67.6, "ICELAND", a=fr.R(83.9, 0.5), size=24, sp=7, w="b")
    PQ(fr, 520, 330, "THE SAGAS", a=fr.R(82.2, 0.4), size=32); PQ(fr, 520, 394, "TWO OR THREE HUNDRED YEARS AFTER", a=fr.R(84.6, 0.4), size=19, light=True, pad=(12, 8))
    PQ(fr, 520, 470, "GREAT STORIES.", a=fr.R(87.7, 0.4), size=24, light=True); PQ(fr, 520, 532, "NOT EXACTLY RECORDS.", a=fr.R(89.0, 0.4), size=24)

# ================= 2h. VO 13.6-26.3: the hull (scheme on black)
@scene("02h_hull", 2, 13.6, 26.4, SCAND, dict(), res="50", active=[(13.6, 26.4)])
def _(fr, t):
    blank(fr); cx, cy = 960, 560; a0 = fr.R(13.6, 0.5); rock = math.radians(2.6 * math.sin((t - 13.6) * 1.35)); bob = 6 * math.sin((t - 13.6) * 1.35 + 0.8)
    def tr(pts): return [(cx + x * math.cos(rock) - y * math.sin(rock), cy + bob + x * math.sin(rock) + y * math.cos(rock)) for x, y in pts]
    # clinker hull, cross-section: each plank laps over the one below it
    n = 8; prof = [(0, 150), (70, 138), (150, 112), (228, 76), (296, 30), (348, -22), (388, -76), (414, -128), (430, -176)]
    for sg in (-1, 1):
        for i in range(n):
            (x0, y0), (x1, y1) = prof[i], prof[i + 1]; dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; ox, oy = uy * 20, -ux * 20
            lap = 26; step = 7 * (i % 2)                                           # every plank overlaps the one below and sits a little proud of it
            q = [(x0 - ux * lap - ox * 0.0 + uy * step, y0 - uy * lap - ux * step), (x1 + uy * step, y1 - ux * step), (x1 + ox + uy * step, y1 + oy - ux * step), (x0 - ux * lap + ox + uy * step, y0 - uy * lap + oy - ux * step)]
            pa = a0 * (0.3 + 0.7 * fr.R(18.4 + 0.22 * i, 0.4))
            poly(fr, tr([(sg * x, y) for x, y in q]), (236, 232, 222) if i % 2 == 0 else (176, 170, 158), pa)
    poly(fr, tr([(-13, 138), (13, 138), (9, 196), (-9, 196)]), PAPER, a0)                                      # keel
    for yb, hw in ((-60, 378), (60, 262)): poly(fr, tr([(-hw, yb - 5), (hw, yb - 5), (hw, yb + 5), (-hw, yb + 5)]), (150, 150, 146), a0 * 0.8)   # cross-beams
    poly(fr, tr([(-6, -330), (6, -330), (6, 140), (-6, 140)]), (150, 150, 146), a0 * 0.8)                          # mast
    wl = fr.R(23.7, 0.6); yw = cy - 104                                                                         # waterline: high on the hull
    if wl > 0:
        pts = [(x, yw + 7 * math.sin(x / 70.0 + (t - 13.6) * 2.2)) for x in range(120, 1801, 20)]
        pline(fr, pts, color=(118, 163, 186), width=5, a=wl, frac=wl)
    PQ(fr, 400, 150, "CROSS THE OPEN SEA", a=fr.R(14.2, 0.4) * out(fr, 18.0), size=30); PQ(fr, 400, 214, "AND STILL ROW", a=fr.R(15.9, 0.4) * out(fr, 18.0), size=22, light=True, pad=(12, 8))
    PQ(fr, 400, 150, "OVERLAPPING OAK PLANKS", a=fr.R(18.6, 0.4), size=30); PQ(fr, 400, 214, "IT FLEXES WITH THE WAVES", a=fr.R(21.2, 0.4), size=22, light=True, pad=(12, 8))
    PQ(fr, 1500, 150, "VERY LOW IN THE WATER", a=fr.R(24.2, 0.4), size=30)
    T(fr, cx, cy + 250, "KEEL", size=18, sp=5, w="s", color=(170, 170, 166), anchor="m", a=a0)

# ================= 2a. VO 26.3-37.9: the Dublin warship
IRISH = cam_box(-11.5, 0.5, 51.2, 55.7)
@scene("02a_dublin_ship", 2, 26.3, 38.0, IRISH, dict(), res="10")
def _(fr, t):
    city(fr, "DUBLIN", a=fr.R(28.6, 0.5), side="l", r=8, size=28); pulse(fr, C["DUBLIN"], 28.8, 2.4, color=NOR_D, rmax=46, width=3.5)
    PQL(fr, *C["DUBLIN"], "AROUND 1042", dx=-110, dy=58, a=fr.R(29.6, 0.4), size=22, pad=(12, 8))
    x, y = P(fr.cam, -4.6, 53.55); lship(fr, x, y + 30, k=5.2, a=fr.R(26.5, 0.6))
    PQ(fr, 1500, 150, "ONE OF THE LARGEST WARSHIPS EVER FOUND", a=fr.R(26.6, 0.5), size=22)
    a1 = fr.R(31.0, 0.6)
    if a1 > 0:
        pline(fr, [(x - 130 * a1, y + 82), (x + 130 * a1, y + 82)], width=2.8)
        for xx in (x - 130 * a1, x + 130 * a1): pline(fr, [(xx, y + 70), (xx, y + 94)], width=2.8)
        PQ(fr, x, y + 82, "30 METRES", size=24, a=min(1, a1 * 1.3), pad=(12, 8))
    PQ(fr, x, y + 150, "ONE METRE OF WATER", a=fr.R(32.8, 0.4), size=22, light=True, pad=(12, 8))
    PQ(fr, x, y + 212, "65 TO 70 MEN", a=fr.R(35.2, 0.4), size=26)

# ================= 2b. VO 46.6-55.6: any beach or riverbank
_HITS = [(-1.8, 55.7), (-6.3, 53.3), (-5.6, 56.3), (-3.0, 59.0), (1.1, 49.45), (2.3, 48.9), (-1.6, 47.2), (0.7, 47.4), (-0.6, 44.85), (4.3, 51.9), (6.95, 50.9), (8.8, 53.1), (-1.1, 53.95),
         (1.3, 52.6), (-9.1, 38.7), (-6.0, 37.4), (-8.5, 51.9), (-2.7, 51.5), (0.1, 51.5), (-4.1, 47.95), (10.0, 53.55), (3.2, 51.2), (-8.6, 42.9), (-7.3, 55.0), (1.9, 47.9)]
@scene("02b_any_beach", 2, 46.6, 55.7, WEUR, dict(sc=U(NORWAY, DENMARK)), res="50", active=[(46.6, 55.7)])
def _(fr, t):
    terr(fr, "sc", NOR)
    PQ(fr, 400, 130, "A NEW KIND OF ENEMY", a=fr.R(46.8, 0.4), size=30)
    col(fr, 208, 204, [("ANY BEACH OR RIVERBANK", 49.6), ("STRIKE", 52.2), ("AND BE GONE", 53.0)], size=21, gap=54)
    for i, ll in enumerate(_HITS):
        t0 = 47.4 + (i * 7 % len(_HITS)) * 0.27
        gline(fr, arc((7.5 if ll[1] < 57 else 5.5, 57.4 if ll[1] < 57 else 60.5), ll, 0.1 * (1 if i % 2 else -1)), width=2.2, frac=ease((t - t0) / 0.9), color=NOR_D, a=max(0.0, min(1.0, (t0 + 1.9 - t) / 0.6)) * 0.9)
        x, y = P(fr.cam, *ll); ph = (t - t0 - 0.8) / 1.0
        if 0 <= ph <= 1: circ(fr, x, y, 5 + 26 * ph, outline=NOR_D, a=1 - ph, width=3)
        circ(fr, x, y, 4.6, WHITE, ease((t - t0 - 0.8) / 0.3)); circ(fr, x, y, 3.2, NOR_D, ease((t - t0 - 0.8) / 0.3))

# ================= 2c. VO 55.6-74.2: the Oseberg burial
SNOR = cam_box(3.5, 15.5, 57.4, 61.6)
@scene("02c_oseberg", 2, 55.6, 74.3, SNOR, dict(no=NORWAY), res="10")
def _(fr, t):
    terr(fr, "no", (178, 170, 158), 0.8)
    region(fr, 8.4, 60.7, "NORWAY", size=30, sp=10, w="b", a=fr.R(60.6, 0.5))
    PQ(fr, 400, 130, "THE ELITE TOOK THEM TO THE GRAVE", a=fr.R(56.2, 0.4) * out(fr, 59.8), size=24)
    PQ(fr, 330, 130, "834", a=fr.R(60.1, 0.4), size=36)
    city(fr, "OSEBERG", a=fr.R(61.4, 0.5), side="l", r=7, size=24, label="" if t < 70.3 else "OSEBERG", icon=False); pulse(fr, C["OSEBERG"], 61.6, 2.4, color=NOR_D, rmax=44, width=3.5)
    col(fr, 208, 204, [("TWO WOMEN, BURIED INSIDE A SHIP", 61.8), ("A CART, SLEDGES, FINE TEXTILES", 64.6), ("THE CLAY PRESERVED THE WOOD", 67.6)], size=19, gap=50, dim=out(fr, 70.0))
    PQ(fr, 400, 204, "THE OSEBERG SHIP", a=fr.R(70.4, 0.4), size=26); PQ(fr, 400, 266, "ALMOST WHOLE, IN A MUSEUM", a=fr.R(71.8, 0.4), size=19, light=True, pad=(12, 8))

# ================= 2d. VO 74.2-93.4: the 2007 voyage; one ship, three jobs
STALLION = smooth([(12.08, 55.72), (11.9, 56.1), (11.3, 56.9), (10.9, 57.95), (8.0, 58.0), (3.0, 58.8), (-2.2, 59.15), (-5.2, 58.85), (-6.7, 57.8), (-7.1, 56.4), (-6.4, 55.55), (-5.45, 54.7),
                   (-5.3, 53.9), (-6.0, 53.4)], 14)
NSEA = cam_box(-13, 16, 50.2, 62.2)
@scene("02d_sea_stallion", 2, 74.2, 93.5, NSEA, dict(dk=DENMARK), res="10", active=[(77.0, 84.0)])
def _(fr, t):
    terr(fr, "dk", NOR_L, 0.9)
    PQ(fr, 330, 130, "2007", a=fr.R(74.4, 0.4) * out(fr, 85.0), size=36)
    PQ(fr, 330, 196, "A FULL-SIZE COPY", a=fr.R(77.0, 0.4) * out(fr, 85.0), size=21, light=True, pad=(12, 8))
    region(fr, 9.6, 56.35, "DENMARK", size=20, sp=5, w="b", a=fr.R(79.6, 0.4)); region(fr, -8.2, 53.3, "IRELAND", size=22, sp=6, w="b", a=fr.R(80.6, 0.4))
    q = ease((t - 77.2) / 6.2)
    gline(fr, STALLION, width=4, frac=q, color=INK, halo=WHITE)
    city(fr, "ROSKILDE", label="", r=5.5, icon=False); city(fr, "DUBLIN", label="", r=6, a=fr.R(82.6, 0.4), icon=False)
    sail_along(fr, STALLION, max(q, 0.001), k=1.5, a=fr.R(77.0, 0.4))
    PQ(fr, 330, 262, "A CREW OF SIXTY-FIVE", a=fr.R(81.6, 0.4) * out(fr, 85.0), size=21, light=True, pad=(12, 8))
    PQL(fr, *C["DUBLIN"], "IT WORKED.", dx=-30, dy=70, a=fr.R(84.0, 0.3), size=26)
    col(fr, 1330, 150, [("A LANDING CRAFT", 86.9), ("A LORRY", 87.9), ("A FAMILY CAR", 88.6)], size=24, gap=62)
    PQ(fr, 1600, 350, "SEATS SIXTY-FIVE, ALL ARMED", a=fr.R(90.6, 0.4), size=24, anchor="r")

# ================= 3a. VO 0-47.5: Lindisfarne
LIND = cam_box(-4.6, 1.4, 54.75, 56.45)
_SHIPS3 = [((1.9 + 0.33 * (i % 3), 56.05 - 0.2 * (i // 3) + 0.05 * (i % 2)), (-1.52 + 0.14 * (i % 3), 55.70 - 0.075 * (i // 3))) for i in range(6)]
@scene("03a_lindisfarne", 3, 0.0, 47.6, LIND, dict(), res="10", active=[(8.0, 13.5)])
def _(fr, t):
    PQ(fr, 400, 130, "THE EIGHTH OF JUNE, 793", a=fr.R(0.1, 0.5), size=30)
    city(fr, "LINDISFARNE", a=fr.R(3.1, 0.5), side="l", r=9, size=28); pulse(fr, C["LINDISFARNE"], 3.3, 2.6, color=NOR_D, rmax=50, width=3.5)
    TL(fr, *C["LINDISFARNE"], "A MONASTERY ON A TIDAL ISLAND", dx=-62, dy=40, size=15, sp=2, anchor="r", a=fr.R(4.4, 0.5) * out(fr, 16.4), w="m")
    region(fr, -2.3, 55.05, "NORTHERN ENGLAND", size=20, sp=6, a=fr.R(6.4, 0.5))
    q = ease((t - 8.1) / 5.0)
    for (a0, a1) in _SHIPS3:
        ll = (a0[0] + (a1[0] - a0[0]) * q, a0[1] + (a1[1] - a0[1]) * q); gship(fr, *ll, k=1.0, a=fr.R(8.1, 0.5), flip=True)
    PQ(fr, 1500, 150, "HEATHEN MEN", a=fr.R(11.8, 0.4) * out(fr, 16.4), size=30)
    PQ(fr, 400, 204, "RAIDERS HAD LANDED BEFORE", a=fr.R(16.8, 0.4) * out(fr, 24.8), size=20, light=True, pad=(12, 8))
    PQ(fr, 400, 266, "THE SHOCK IS THE TARGET", a=fr.R(19.6, 0.4) * out(fr, 24.8), size=22)
    PQ(fr, 400, 330, "ONE OF THE HOLIEST PLACES IN BRITAIN", a=fr.R(22.2, 0.4) * out(fr, 24.8), size=19, light=True, pad=(12, 8))
    PQ(fr, 400, 204, "ALCUIN", a=fr.R(25.1, 0.4) * out(fr, 31.2), size=28)
    PQ(fr, 400, 268, "“NO ONE HAD THOUGHT", a=fr.R(28.2, 0.4) * out(fr, 31.2), size=21, light=True, pad=(12, 8)); PQ(fr, 400, 324, "SUCH A VOYAGE POSSIBLE”", a=fr.R(29.4, 0.4) * out(fr, 31.2), size=21, light=True, pad=(12, 8))
    PQ(fr, 400, 204, "A PERFECT TARGET", a=fr.R(31.7, 0.4), size=26)
    col(fr, 208, 270, [("BY THE SEA", 35.0), ("SILVER, GOLD AND BOOKS", 36.8), ("NO WALLS, NO SOLDIERS", 40.3), ("PEOPLE: RANSOMED, OR SOLD", 43.0)], size=19, gap=50)

# ================= 3b. VO 47.5-55.0: the raids spread
BRIT = cam_box(-13, 13, 45.8, 62.6)
@scene("03b_raids_spread", 3, 47.5, 55.1, BRIT, dict(sc=U(NORWAY, DENMARK)), res="50")
def _(fr, t):
    terr(fr, "sc", NOR)
    PQ(fr, 330, 130, "WITHIN A FEW YEARS", a=fr.R(47.6, 0.4), size=28)
    for i, (pts, t0) in enumerate((([(4.6, 60.6), (0.5, 60.2), (-3.4, 58.9), (-5.6, 57.6)], 48.6), ([(4.6, 60.9), (-2, 60.6), (-6.4, 59.0), (-8.6, 56.6), (-8.4, 55.0)], 49.5),
                                   ([(7.6, 56.3), (5.0, 54.6), (3.0, 52.3), (1.7, 50.6)], 50.6), ([(7.6, 56.0), (4.2, 54.0), (2.0, 51.2), (-1.5, 50.0), (-5.6, 48.6), (-3.2, 47.2)], 51.2))):
        arrow(fr, pts, t0, 1.5, width=4.4, color=NOR_D)
    region(fr, -4.0, 56.9, "SCOTLAND", size=20, sp=6, w="b", a=fr.R(49.0, 0.4)); region(fr, -8.0, 53.3, "IRELAND", size=20, sp=6, w="b", a=fr.R(49.9, 0.4))
    region(fr, 3.0, 48.2, "FRANKISH KINGDOM", size=20, sp=6, w="b", a=fr.R(51.0, 0.4))
    for i in range(9): gship(fr, 2.2 + 0.9 * (i % 3) + 0.3 * (i // 3), 56.6 - 0.55 * (i // 3), k=0.7, a=fr.R(52.9 + 0.1 * i, 0.4) if i else fr.R(52.4, 0.4), flip=True)
    PQ(fr, 1560, 150, "A FEW SHIPS BECOME FLEETS", a=fr.R(53.0, 0.4), size=24)

# ================= 3c. VO 65.9-86.6: why now
_RICH = [(2.35, 48.86), (1.1, 49.44), (-1.55, 47.2), (0.69, 47.39), (4.9, 52.37), (5.34, 51.97), (6.96, 50.94), (-0.1, 51.5), (-1.08, 53.96), (-1.3, 51.06), (1.3, 52.63), (-6.26, 53.35),
         (-2.0, 48.65), (-0.57, 44.84), (3.72, 51.05), (8.8, 53.08), (-8.5, 42.88), (1.08, 51.28), (-1.4, 50.9), (4.4, 51.2), (-1.8, 55.68), (-6.4, 56.33), (2.83, 50.5)]
@scene("03c_why_now", 3, 65.9, 86.7, WEUR, dict(sc=U(NORWAY, SWEDEN, DENMARK)), res="50")
def _(fr, t):
    PQ(fr, 330, 130, "WHY NOW?", a=fr.R(65.9, 0.3), size=36)
    for i, ll in enumerate(_RICH):
        a = fr.R(68.8 + 0.1 * i, 0.5); x, y = P(fr.cam, *ll); circ(fr, x, y, 7.5, INK, a); circ(fr, x, y, 5.6, YELLOW if False else GOLD, a)
    PQ(fr, 330, 200, "RICHES SIT ON THE COASTS", a=fr.R(70.2, 0.4), size=21, light=True, pad=(12, 8))
    PQ(fr, 330, 258, "THE SHIPS ARE READY", a=fr.R(72.5, 0.4), size=21, light=True, pad=(12, 8))
    terr(fr, "sc", NOR, fr.R(74.0, 0.8))
    PQ(fr, 1530, 150, "YOUNG MEN NEED SILVER", a=fr.R(75.2, 0.4), size=24)
    PQ(fr, 1530, 212, "FOLLOWERS, LAND AND A GOOD MARRIAGE", a=fr.R(77.2, 0.4), size=18, light=True, pad=(12, 8))
    for i, (pts, t0) in enumerate((([(5, 60.5), (0, 59.5), (-4.5, 58.3)], 80.2), ([(7.5, 56.2), (4, 54), (1.6, 52.6)], 80.5), ([(7.5, 55.9), (3.6, 53.2), (1.9, 50.8)], 80.8), ([(5, 60.9), (-3, 60.4), (-8.6, 56)], 81.1))):
        arrow(fr, pts, t0, 1.6, width=4, color=NOR_D)
    tline(fr, fr.R(81.4, 0.5), fr.R(82.0, 3.6), left="793", title="TWO AND A HALF CENTURIES", ra=fr.R(82.6, 0.5))

# ================= 4a. VO 0-20.5: Charlemagne's empire, split three ways; the rivers
FRANCIA = cam_box(-6, 20, 41.2, 55.4)
def _river(name, box):
    out_ = []
    for f in json.load(open(engine.DATA + "/ne_10m_rivers_lake_centerlines.geojson"))["features"]:
        g = f["geometry"]
        if g and f["properties"].get("name") in name:
            for l in ([g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]):
                a = np.asarray(l, dtype=np.float64)[:, :2]
                if box[0] < a[:, 0].mean() < box[1] and box[2] < a[:, 1].mean() < box[3]: out_.append(a)
    return out_
R_SEINE = _river(("Seine",), (-2, 6, 46, 51)); R_LOIRE = _river(("Loire",), (-3, 6, 44, 49)); R_RHINE = _river(("Rhine", "Rhein"), (3, 11, 46, 53))
R_DNIPRO = _river(("Dnipro",), (28, 37, 45, 57)); R_VOLGA = _river(("Volga",), (30, 52, 44, 60)); R_VOLKHOV = _river(("Volkhov",), (30, 34, 57, 61))
def rivers_hl(fr, segs, a, color=(40, 96, 136), width=5):
    for sg in segs: gline(fr, sg, width=width, color=color, a=a)
_TOWNS4 = [(2.35, 48.86), (1.1, 49.44), (0.69, 47.39), (-1.55, 47.22), (1.9, 47.9), (6.96, 50.94), (7.6, 50.36), (8.27, 50.0), (5.12, 52.09), (4.08, 48.3), (-0.55, 47.47), (7.75, 48.58)]
@scene("04a_empire_split", 4, 0.0, 20.6, FRANCIA, dict(all=CAROL, w=WFRANK, m=MFRANK, e=EFRANK), res="50")
def _(fr, t):
    k = fr.R(4.6, 1.4)
    terr(fr, "all", FRK, 1 - k, border=k <= 0); terr(fr, "w", FRK, k); terr(fr, "m", FRK2, k); terr(fr, "e", FRK3, k)
    PQ(fr, 400, 130, "CHARLEMAGNE", a=fr.R(0.1, 0.4) * out(fr, 4.2), size=32)
    PQ(fr, 400, 196, "THE BIGGEST EMPIRE SINCE ROME", a=fr.R(1.6, 0.4) * out(fr, 4.2), size=19, light=True, pad=(12, 8))
    PQ(fr, 400, 130, "HIS GRANDSONS", a=fr.R(4.4, 0.4) * out(fr, 11.4), size=30)
    PQ(fr, 400, 196, "SPLIT IT THREE WAYS", a=fr.R(5.4, 0.4) * out(fr, 11.4), size=21, light=True, pad=(12, 8))
    PQ(fr, 400, 254, "AN INVITATION", a=fr.R(9.8, 0.4) * out(fr, 11.4), size=22)
    PQ(fr, 400, 130, "LOOK AT THE RIVERS", a=fr.R(11.7, 0.4), size=28)
    for segs, ll, txt, t0, dx, dy in ((R_SEINE, (0.2, 49.5), "SEINE", 13.0, -110, -40), (R_LOIRE, (-2.2, 47.2), "LOIRE", 13.7, -50, 30), (R_RHINE, (6.1, 51.8), "RHINE", 14.3, 60, -6)):
        rivers_hl(fr, segs, fr.R(t0, 0.6)); PQL(fr, *ll, txt, dx=dx, dy=dy, a=fr.R(t0 + 0.1, 0.4), size=20, light=True, pad=(10, 7))
    for i, (pts, t0) in enumerate((([(-1.5, 50.6), (-0.2, 49.9), (0.5, 49.5)], 15.5), ([(-4.6, 47.0), (-3.0, 47.15), (-2.1, 47.25)], 15.8), ([(3.2, 53.2), (3.8, 52.2), (4.6, 51.9)], 16.1))):
        arrow(fr, pts, t0, 1.0, width=4, color=NOR_D)
    for i, ll in enumerate(_TOWNS4):
        a = fr.R(17.4 + 0.1 * i, 0.4); x, y = P(fr.cam, *ll); circ(fr, x, y, 7, INK, a); circ(fr, x, y, 5.2, GOLD, a)
    PQ(fr, 400, 196, "RICH TOWNS AND ABBEYS ON THE BANKS", a=fr.R(17.6, 0.4), size=18, light=True, pad=(12, 8))

# ================= 4b. VO 29.4-52.2: Paris taken, paid off, besieged again
SEINEC = cam_box(-1.4, 4.6, 47.95, 50.45)
@scene("04b_paris", 4, 29.4, 52.3, SEINEC, dict(), res="10")
def _(fr, t):
    rivers_hl(fr, R_SEINE, 1.0, width=6)
    city(fr, "PARIS", side="r", r=10, size=32); city(fr, "ROUEN", label="", r=4.5, icon=False)
    for i in range(8): gship(fr, 1.55 + 0.085 * i, 49.02 - 0.012 * i + 0.06 * (i % 2), k=0.85, a=fr.R(29.5 + 0.06 * i, 0.4) * out(fr, 42.6, 1.2))
    PQ(fr, 400, 130, "EASTER 845", a=fr.R(29.6, 0.4) * out(fr, 44.5), size=32)
    PQ(fr, 400, 196, "THEY REACH PARIS AND TAKE IT", a=fr.R(30.4, 0.4) * out(fr, 44.5), size=20, light=True, pad=(12, 8))
    PQ(fr, 400, 262, "KING CHARLES THE BALD", a=fr.R(32.3, 0.4) * out(fr, 44.5), size=22)
    PQ(fr, 400, 322, "DOES NOT FIGHT THEM", a=fr.R(33.3, 0.4) * out(fr, 44.5), size=20, light=True, pad=(12, 8))
    PQ(fr, 400, 130, "PAYING BECOMES A HABIT", a=fr.R(44.8, 0.4), size=26); PQ(fr, 400, 196, "AND SO DO THE RAIDS", a=fr.R(46.2, 0.4), size=21, light=True, pad=(12, 8))
    PQ(fr, 1500, 150, "885", a=fr.R(47.7, 0.4), size=36); PQ(fr, 1500, 220, "A HUGE ARMY BESIEGES PARIS", a=fr.R(48.6, 0.4), size=20, light=True, pad=(12, 8))
    PQ(fr, 1500, 278, "FOR ALMOST A YEAR", a=fr.R(50.4, 0.4), size=22)
    ring_(fr, *C["PARIS"], 86, color=NOR_D, a=fr.R(48.4, 0.4), frac=fr.R(48.4, 2.4), width=7)
    for i in range(10):
        ang = math.radians(36 * i + 10); x, y = P(fr.cam, *C["PARIS"]); lship(fr, x + 128 * math.cos(ang), y + 110 * math.sin(ang), k=0.7, a=fr.R(48.6 + 0.15 * i, 0.4))
def ring_(fr, lon, lat, r, color=INK, a=1.0, width=3, frac=1.0, start=-90, dash=None):
    if a <= 0 or frac <= 0: return
    x, y = P(fr.cam, lon, lat); n = max(8, int(72 * frac)); ang = np.radians(start + np.linspace(0, 360 * min(frac, 1.0), n))
    pline(fr, np.stack([x + r * np.cos(ang), y + r * np.sin(ang)], 1), color=color, width=width, a=a, dash=dash)

# ================= 4c. VO 52.2-83.0: Rollo's deal; Normandy
NORMC = cam_box(-3.4, 4.4, 47.6, 50.7)
_CAST = [(-0.37, 49.18), (0.2, 48.9), (-1.1, 49.1), (0.6, 49.5), (1.15, 49.0), (-0.9, 48.75), (0.4, 49.75), (-1.45, 49.5)]
def castle(fr, x, y, k=1.0, a=1.0, color=INK):
    if a <= 0: return
    rect(fr, x - 9 * k, y - 12 * k, x + 9 * k, y + 6 * k, color, a)
    for i in (-9, -3, 3): rect(fr, x + i * k, y - 17 * k, x + (i + 4.4) * k, y - 12 * k, color, a)
    rect(fr, x - 2.4 * k, y - 2 * k, x + 2.4 * k, y + 6 * k, PAPER, a)
@scene("04c_normandy", 4, 52.2, 83.1, NORMC, dict(nm=NORMANDY), res="10")
def _(fr, t):
    rivers_hl(fr, R_SEINE, 1.0, width=6)
    hl = fr.R(80.2, 0.8)
    terr(fr, "nm", NOR, fr.R(61.6, 1.2))
    PQ(fr, 400, 130, "911", a=fr.R(52.4, 0.4) * out(fr, 80.0), size=36); PQ(fr, 400, 198, "THE FRANKS TRY SOMETHING NEW", a=fr.R(53.3, 0.4) * out(fr, 80.0), size=19, light=True, pad=(12, 8))
    city(fr, "PARIS", side="r", r=8, size=24, label="" , a=1.0)
    cross(fr, *C["CHARTRES"], a=fr.R(57.4, 0.4), r=11, width=5); TL(fr, *C["CHARTRES"], "CHARTRES", dx=20, dy=0, size=20, a=fr.R(57.5, 0.4))
    PQL(fr, *C["CHARTRES"], "ROLLO, JUST BEATEN", dx=40, dy=52, a=fr.R(56.0, 0.4) * out(fr, 68.8), size=19, pad=(11, 7))
    PQ(fr, 1500, 150, "KING CHARLES THE SIMPLE", a=fr.R(59.2, 0.4) * out(fr, 68.8), size=22); PQ(fr, 1500, 210, "OFFERS HIM A DEAL", a=fr.R(60.2, 0.4) * out(fr, 68.8), size=20, light=True, pad=(12, 8))
    city(fr, "ROUEN", a=fr.R(62.6, 0.4), side="t", r=7, size=24, color=WHITE, icon=False)
    col(fr, 1330, 290, [("THE LAND AROUND ROUEN", 62.0), ("HE IS BAPTISED", 64.8), ("KEEPS EVERY OTHER VIKING OUT", 66.2)], size=19, gap=50, dim=out(fr, 68.8))
    arrow(fr, [(-0.6, 50.35), (0.0, 49.85), (0.25, 49.6)], 66.4, 1.0, width=4, color=CHAR, a=out(fr, 73.6)); cross(fr, 0.05, 49.82, a=fr.R(67.6, 0.3) * out(fr, 73.6), r=10, width=5, color=WHITE)
    PQ(fr, 1500, 150, "THE RAIDERS BECOME THE GUARDS", a=fr.R(69.2, 0.4) * out(fr, 80.0), size=22)
    region(fr, -0.1, 48.98, "NORMANDY", a=fr.R(72.7, 0.5), size=34, sp=12, w="b", color=WHITE)
    TL(fr, -0.1, 48.98, "THE LAND OF THE NORTHMEN", dy=40, size=15, sp=4, anchor="m", color=WHITE, a=fr.R(71.4, 0.5) * out(fr, 79.6), w="m")
    for i, ll in enumerate(_CAST):
        x, y = P(fr.cam, *ll); castle(fr, x, y, 1.3, fr.R(75.6 + 0.25 * i, 0.4) * (1 - hl), color=WHITE)
    col(fr, 1330, 230, [("SPEAK FRENCH", 74.6), ("STONE CASTLES", 76.0), ("FIGHT ON HORSEBACK", 77.6)], size=19, gap=50, dim=out(fr, 80.0))
    PQ(fr, 960, 130, "REMEMBER NORMANDY", a=fr.R(80.2, 0.4), size=32)

# ================= 5a. VO 0-44.7: four kingdoms; the great heathen army
ENGC = cam_box(-8.2, 4.2, 49.6, 56.4)
@scene("05a_great_army", 5, 0.0, 44.8, ENGC, dict(nu=NORTHUMBRIA, me=MERCIA, ea=EASTANGLIA, we=WESSEX), res="10")
def _(fr, t):
    f1 = fr.R(23.3, 1.0); f2 = fr.R(24.8, 1.0); f3 = fr.R(26.2, 1.0)
    for k_, c_, ta, fall in (("nu", ENG1, 3.6, f1), ("me", ENG2, 4.6, f3 * 0.999), ("ea", ENG3, 5.4, f2), ("we", ENG4, 6.2, 0.0)):
        terr(fr, k_, mix(NOR, c_, fall), fr.R(ta, 0.6))
    PQ(fr, 330, 130, "865", a=fr.R(0.2, 0.4) * out(fr, 17.0), size=36); PQ(fr, 330, 198, "FOUR KINGDOMS", a=fr.R(1.6, 0.4) * out(fr, 17.0), size=22, light=True, pad=(12, 8))
    region(fr, -1.9, 54.85, "NORTHUMBRIA", a=fr.R(3.7, 0.4), size=20, sp=5, w="b", color=WHITE); region(fr, -1.7, 52.55, "MERCIA", a=fr.R(4.7, 0.4), size=22, sp=7, w="b", color=WHITE)
    region(fr, 1.05, 52.5, "EAST", a=fr.R(5.5, 0.4), size=17, sp=4, w="b", color=WHITE, dy=-11); region(fr, 1.05, 52.5, "ANGLIA", a=fr.R(5.5, 0.4), size=17, sp=4, w="b", color=WHITE, dy=11)
    region(fr, -2.0, 51.0, "WESSEX", a=fr.R(6.3, 0.4), size=22, sp=7, w="b", color=WHITE)
    arrow(fr, [(4.0, 54.4), (3.2, 53.3), (1.9, 52.6)], 8.2, 1.6, width=5.5, color=NOR_D)
    for i in range(6): gship(fr, 2.5 + 0.42 * (i % 3), 54.1 - 0.3 * (i // 3), k=0.8, a=fr.R(8.0 + 0.1 * i, 0.4) * out(fr, 16.8), flip=True)
    PQ(fr, 1500, 150, "THE GREAT HEATHEN ARMY", a=fr.R(11.2, 0.4) * out(fr, 28.2), size=26)
    PQ(fr, 1500, 212, "DOES NOT GO HOME FOR THE WINTER", a=fr.R(14.6, 0.4) * out(fr, 28.2), size=18, light=True, pad=(12, 8))
    arrow(fr, [(1.2, 52.6), (0.2, 53.1), (-0.7, 53.7), C["YORK"]], 17.4, 1.6, width=5, color=NOR_D)
    PQ(fr, 330, 130, "NOVEMBER 866", a=fr.R(17.3, 0.4) * out(fr, 38.2), size=30)
    city(fr, "YORK", a=fr.R(19.0, 0.4), side="l", r=8, size=26, color=WHITE, label="YORK" if t < 21.3 else "JORVIK")
    TL(fr, *C["YORK"], "A VIKING CAPITAL", dx=-56, dy=34, size=14, sp=3, anchor="r", color=WHITE, a=fr.R(20.6, 0.4) * out(fr, 28.2), w="m")
    arrow(fr, [C["YORK"], (-0.2, 53.2), (0.6, 52.7)], 24.6, 1.0, width=4, color=NOR_D, a=out(fr, 28.2)); arrow(fr, [(0.4, 52.5), (-0.6, 52.5), (-1.6, 52.7)], 26.0, 1.0, width=4, color=NOR_D, a=out(fr, 28.2))
    PQ(fr, 1500, 150, "SONS OF RAGNAR LOTHBROK?", a=fr.R(29.6, 0.4) * out(fr, 38.2), size=24)
    PQ(fr, 1500, 214, "IVAR THE BONELESS WAS REAL", a=fr.R(33.3, 0.4) * out(fr, 38.2), size=20, light=True, pad=(12, 8))
    PQ(fr, 1500, 270, "HIS FATHER MAY NOT HAVE BEEN", a=fr.R(36.3, 0.4) * out(fr, 38.2), size=20, light=True, pad=(12, 8))
    PQ(fr, 330, 130, "878", a=fr.R(38.5, 0.4), size=36); PQ(fr, 330, 198, "ONLY WESSEX IS LEFT", a=fr.R(39.6, 0.4), size=22, light=True, pad=(12, 8))
    arrow(fr, [(-1.3, 52.1), (-1.9, 51.75), (-2.1, 51.45)], 41.6, 1.2, width=5, color=NOR_D); PQ(fr, 330, 258, "TAKEN BY SURPRISE", a=fr.R(42.4, 0.4), size=20)

# ================= 5b. VO 55.0-84.8: Edington, the Danelaw, the names on the map
_BY = None
@scene("05b_danelaw", 5, 55.0, 84.9, ENGC, dict(dl=DANELAW, en=NOTDANE, x_dl=I(DANELAW, [(-3.2, 52.3), (0.9, 52.3), (0.6, 54.6), (-3.2, 54.6)])), res="10")
def _(fr, t):
    k = fr.R(66.6, 1.4)
    terr(fr, "dl", NOR, 1.0, border=k > 0.5); terr(fr, "en", mix(ENG4, NOR, k), 1.0, border=k > 0.5)
    x, y = P(fr.cam, *C["ATHELNEY"]); circ(fr, x, y, 16, outline=WHITE, a=out(fr, 61.0), width=3)
    TL(fr, *C["ATHELNEY"], "THE MARSHES", dx=-24, dy=0, size=15, sp=3, anchor="r", color=WHITE, a=out(fr, 61.0), w="m")
    PQ(fr, 330, 130, "MAY 878", a=fr.R(55.2, 0.4) * out(fr, 66.2), size=32)
    arrow(fr, [C["ATHELNEY"], (-2.6, 51.25), (-2.25, 51.28)], 56.8, 1.2, width=5, color=ENG4, halo=WHITE)
    cross(fr, *C["EDINGTON"], a=fr.R(58.9, 0.3), r=12, width=5, color=WHITE); TL(fr, *C["EDINGTON"], "EDINGTON", dx=20, dy=0, size=20, color=WHITE, a=fr.R(59.0, 0.4) * out(fr, 73.0))
    PQ(fr, 330, 198, "ALFRED WINS", a=fr.R(59.2, 0.4) * out(fr, 66.2), size=22, light=True, pad=(12, 8))
    PQ(fr, 1500, 150, "GUTHRUM IS BAPTISED", a=fr.R(61.2, 0.4) * out(fr, 66.2), size=24); PQ(fr, 1500, 212, "ALFRED IS HIS GODFATHER", a=fr.R(64.0, 0.4) * out(fr, 66.2), size=19, light=True, pad=(12, 8))
    gline(fr, smooth([C["LONDON"], (-0.9, 52.0), (-1.5, 52.5), (-2.1, 52.9), C["CHESTER"]], 10), width=6, frac=fr.R(66.5, 1.6), color=WHITE)
    region(fr, -0.6, 53.25, "DANELAW", a=fr.R(69.2, 0.5) * out(fr, 75.0), size=32, sp=11, w="b", color=WHITE)
    PQ(fr, 330, 130, "A LINE ACROSS ENGLAND", a=fr.R(66.6, 0.4) * out(fr, 73.0), size=24); PQ(fr, 330, 196, "LAND UNDER DANISH LAW", a=fr.R(70.6, 0.4) * out(fr, 73.0), size=20, light=True, pad=(12, 8))
    region(fr, -2.0, 51.0, "WESSEX", size=20, sp=6, w="b", color=WHITE, a=fr.R(68.0, 0.5) * out(fr, 75.0))
    pts = scatter(fr, "x_dl", 420, seed=8)
    dots_px(fr, pts, lambda i: fr.R(75.2 + 5.2 * i / max(1, len(pts)), 0.35), r=2.6, color=WHITE, ring=None)
    PQ(fr, 330, 130, "STILL ON THE MAP", a=fr.R(73.2, 0.4), size=26); PQ(fr, 330, 196, "MORE THAN SIX HUNDRED PLACE NAMES", a=fr.R(75.2, 0.4), size=18, light=True, pad=(12, 8))
    PQ(fr, 330, 252, "“BY”: A FARM OR VILLAGE", a=fr.R(78.4, 0.4), size=20)
    for n_, t0, side in (("GRIMSBY", 82.1, "r"), ("DERBY", 82.9, "l"), ("WHITBY", 83.6, "r")):
        a = fr.R(t0, 0.35); x, y = P(fr.cam, *C[n_]); circ(fr, x, y, 8, INK, a); circ(fr, x, y, 5.6, WHITE, a)
        PQL(fr, *C[n_], n_[:-2] + "BY", dx=(86 if side == "r" else -78), dy=0, a=a, size=20, pad=(10, 7))

# ================= 5k. VO 84.8-100.5: the words (text frame)
@scene("05k_words", 5, 84.8, 100.6, SCAND, dict(), res="50")
def _(fr, t):
    blank(fr)
    T(fr, 960, 190, "IT IS IN THE LANGUAGE", size=22, sp=7, w="s", color=(150, 152, 156), anchor="m", a=fr.R(84.9, 0.4))
    for i, (wd, t0) in enumerate((("SKY", 86.8), ("EGG", 87.2), ("KNIFE", 87.6), ("LEG", 88.0), ("SKIN", 88.4), ("TAKE", 89.8), ("THEY", 90.4))):
        PQ(fr, 330 + 210 * i, 330, wd, a=fr.R(t0, 0.3), size=34, light=True)
    PQ(fr, 660, 470, "WINDOW", a=fr.R(91.4, 0.3), size=38, light=True); T(fr, 840, 470, "=", size=38, w="b", color=WHITE, a=fr.R(92.2, 0.3))
    T(fr, 900, 470, "WIND-EYE", size=38, w="b", sp=3, color=WHITE, a=fr.R(92.4, 0.3)); T(fr, 960, 540, "A HOLE FOR THE WIND", size=20, sp=6, w="s", color=(150, 152, 156), anchor="m", a=fr.R(93.4, 0.4))
    # they took the knife from the window: the Norse words sit on plaques
    words = [("THEY", 1), ("TOOK", 1), ("THE", 0), ("KNIFE", 1), ("FROM", 0), ("THE", 0), ("WINDOW", 1)]; f = font("b", s(46)); gap = 26
    ws = [text_w(w_, f, 2.0) / SS for w_, _ in words]; x = 960 - (sum(ws) + gap * (len(words) - 1) + 0) / 2; a0 = fr.R(94.9, 0.4); hi = fr.R(97.2, 0.6)
    for (w_, norse), ww in zip(words, ws):
        if norse: rect(fr, x - 13, 760 - 40, x + ww + 13, 760 + 40, PAPER, a0 * hi)
        T(fr, x, 760, w_, size=46, w="b", sp=2.0, color=mix(BLACK, WHITE, hi) if norse else WHITE, a=a0); x += ww + gap
    T(fr, 960, 860, "FOUR OF THOSE SEVEN WORDS CAME ON VIKING SHIPS", size=20, sp=6, w="s", color=(150, 152, 156), anchor="m", a=fr.R(97.4, 0.5))

# ================= 6a. VO 46.6-76.6: women's rights; Ibrahim ibn Yaqub; Hedeby and Birka
TRADE = cam_box(-11, 25, 35.2, 62)
BALT = cam_box(2.5, 27, 52.6, 62.2)
_c6 = mover([(46.6, TRADE), (63.4, TRADE), (65.6, BALT)])
@scene("06a_hedeby", 6, 46.6, 76.7, _c6, dict(sc=U(NORWAY, SWEDEN, DENMARK)), res="50")
def _(fr, t):
    terr(fr, "sc", NOR_L, 0.85)
    w1 = out(fr, 63.2)
    PQ(fr, 400, 130, "A WOMAN CAN OWN PROPERTY", a=fr.R(46.7, 0.4) * out(fr, 50.2), size=24)
    PQ(fr, 400, 194, "AND DIVORCE HER HUSBAND", a=fr.R(48.4, 0.4) * out(fr, 50.2), size=21, light=True, pad=(12, 8))
    PQ(fr, 400, 130, "THE 960s", a=fr.R(50.5, 0.4) * w1, size=32)
    city(fr, "CORDOBA", a=fr.R(51.6, 0.4) * w1, side="r", r=6, size=22, icon=False); gline(fr, arc(C["CORDOBA"], C["HEDEBY"], -0.16), width=4, frac=fr.R(52.4, 2.0), arrow=True, halo=WHITE, a=w1)
    PQL(fr, *C["CORDOBA"], "IBRAHIM IBN YAQUB", dx=40, dy=52, a=fr.R(52.4, 0.4) * w1, size=20, pad=(11, 7))
    city(fr, "HEDEBY", a=fr.R(54.2, 0.4), side="l" if t < 64.5 else "b", r=6.5, size=24, icon=False)
    col(fr, 1290, 150, [("HE WRITES:", 55.9), ("THE RIGHT TO DIVORCE BELONGS TO THE WOMEN", 56.6), ("MEN AND WOMEN ALIKE WEAR EYE MAKE-UP", 59.4), ("IT MAKES THEM MORE BEAUTIFUL", 62.0)], size=17, gap=48, first_dark=True, dim=w1)
    w2 = fr.R(65.8, 0.5)
    city(fr, "BIRKA", a=w2, side="t", r=6.5, size=24, icon=False)
    PQ(fr, 330, 130, "A THOUSAND PEOPLE OR SO EACH", a=fr.R(66.4, 0.4) * w2, size=20); PQ(fr, 330, 190, "SMALL, BUT BUSY", a=fr.R(67.9, 0.4) * w2, size=20, light=True, pad=(12, 8))
    for i, (a_, b_, bend) in enumerate(((C["BIRKA"], (5.5, 54.6), 0.2), (C["HEDEBY"], (4.4, 53.2), -0.12), (C["BIRKA"], (26.2, 58.4), -0.14))):
        gline(fr, arc(a_, b_, bend), width=3.6, frac=fr.R(69.4 + 0.3 * i, 1.4), arrow=True, halo=WHITE, a=w2)
    for i, (a_, b_, bend) in enumerate((((4.2, 52.9), C["HEDEBY"], 0.16), ((26.4, 57.4), C["BIRKA"], -0.16), ((25.0, 53.4), (18.6, 57.5), 0.12))):
        gline(fr, arc(a_, b_, bend), width=3.6, frac=fr.R(73.6 + 0.3 * i, 1.4), arrow=True, halo=WHITE, color=GOLD, a=w2)
    col(fr, 1290, 150, [("OUT", 69.3), ("FURS · AMBER", 69.8), ("WALRUS IVORY · SLAVES", 71.2)], size=19, gap=50, first_dark=True, dim=w2)
    col(fr, 1290, 330, [("IN", 73.5), ("WINE · GLASS · SILK", 73.9), ("ABOVE ALL SILVER", 75.4)], size=19, gap=50, first_dark=True, dim=w2)

# ================= 6b. VO 76.6-101.3: Gotland's hoards; turn east
GOTC = cam_box(16.2, 21.4, 56.7, 58.15)
_c6b = mover([(76.6, GOTC), (97.9, GOTC), (101.0, cam_box(12, 44, 50, 62.5))])
@scene("06b_gotland", 6, 76.6, 101.4, _c6b, dict(go=GOTLAND), res="10")
def _(fr, t):
    w = out(fr, 97.8)
    terr(fr, "go", NOR_L, 0.9)
    if t < 98.2:
        region(fr, 17.25, 57.9, "GOTLAND", a=fr.R(78.0, 0.4) * w, size=30, sp=10, w="b", color=SEA_T)
        pts = scatter(fr, "go", 300, seed=5); dots_px(fr, pts, lambda i: fr.R(79.4 + 3.6 * i / max(1, len(pts)), 0.3) * w, r=3.4, color=(206, 208, 212), ring=INK)
        x, y = P(fr.cam, *C["SPILLINGS"]); a = fr.R(84.0, 0.4) * w; circ(fr, x, y, 14, INK, a); circ(fr, x, y, 11, YELLOW if False else (232, 234, 238), a); pulse(fr, C["SPILLINGS"], 84.2, 2.4, color=INK, rmax=50, width=3.5)
    PQ(fr, 400, 130, "MORE THAN SEVEN HUNDRED", a=fr.R(80.2, 0.4) * w, size=26); PQ(fr, 400, 194, "SILVER HOARDS", a=fr.R(81.8, 0.4) * w, size=22, light=True, pad=(12, 8))
    col(fr, 1330, 150, [("THE BIGGEST: DUG UP IN 1999", 84.0), ("67 KILOGRAMS OF SILVER", 86.2), ("OVER 14,000 COINS", 88.8), ("ALMOST ALL ISLAMIC DIRHAMS", 91.4)], size=19, gap=50, first_dark=True, dim=w)
    arrow(fr, [(20.5, 58.6), (25, 59.6), (30, 59.9), (36, 58.6)], 99.2, 1.8, width=5, color=INK)

# ================= 7a. VO 0-13.8: Sweden faces east; the river roads
ROAD_DN = smooth([(18.2, 59.4), (21, 59.7), (24.5, 59.8), (27.5, 60.0), (29.9, 59.93), (31.0, 59.93), (31.6, 60.12), (32.3, 60.05), (32.0, 59.4), (31.3, 58.5), (31.3, 57.6), (30.7, 56.4), (31.5, 55.4),
                  (32.0, 54.8), (30.9, 54.2), (30.3, 53.0), (30.55, 50.45), (31.6, 49.5), (33.5, 48.8), (35.0, 48.3), (35.1, 47.6), (33.6, 46.9), (32.3, 46.5), (31.3, 45.2), (30.0, 43.3), (29.2, 41.6),
                  (29.0, 41.1)], 10)
ROAD_VO = smooth([(31.3, 58.5), (33.4, 58.0), (35.9, 57.0), (37.6, 56.9), (39.8, 57.6), (41.9, 57.4), (44.0, 56.3), (46.6, 56.1), (49.1, 55.8), (49.0, 55.0), (48.4, 53.2), (46.0, 51.5), (45.4, 49.6),
                  (44.6, 48.7), (46.5, 47.2), (48.0, 46.3)], 10)
def _fa(path, lon, lat):
    p = np.asarray(path) * 1.0; L = path_len(p); i = int(np.argmin(np.hypot(p[:, 0] - lon, (p[:, 1] - lat) * 1.9))); return L[i] / L[-1]
@scene("07a_east", 7, 0.0, 13.9, EAST, dict(sw=SWEDEN), res="50")
def _(fr, t):
    terr(fr, "sw", NOR)
    region(fr, 15.6, 60.9, "SWEDEN", a=fr.R(0.1, 0.4), size=24, sp=7, w="b", color=WHITE)
    q1 = fr.R(2.4, 6.0) * 1.0; gline(fr, ROAD_DN, width=5, frac=min(1.0, 0.02 + q1), color=INK, halo=WHITE, arrow=True)
    gline(fr, ROAD_VO, width=5, frac=fr.R(10.6, 2.6), color=INK, halo=WHITE, arrow=True)
    sea(fr, 19.6, 57.0, "BALTIC", a=fr.R(2.4, 0.4), size=17)
    PQL(fr, 31.4, 60.9, "LAKE LADOGA", dx=30, dy=-34, a=fr.R(5.6, 0.4), size=18, light=True, pad=(10, 7)); PQL(fr, 31.9, 59.2, "VOLKHOV", dx=84, dy=10, a=fr.R(6.9, 0.4), size=18, light=True, pad=(10, 7))
    PQL(fr, 30.4, 52.0, "DNIEPER", dx=-80, dy=0, a=fr.R(8.4, 0.4), size=18, light=True, pad=(10, 7)); sea(fr, 34.5, 43.3, "BLACK SEA", a=fr.R(9.8, 0.4), size=19)
    PQL(fr, 45.4, 49.8, "VOLGA", dx=64, dy=0, a=fr.R(11.2, 0.4), size=18, light=True, pad=(10, 7)); sea(fr, 51.0, 42.6, "CASPIAN", a=fr.R(12.6, 0.4), size=18)
    PQ(fr, 330, 130, "RIVERS LEAD DEEP INLAND", a=fr.R(2.6, 0.4), size=24)

# ================= 7b. VO 25.1-83.8: Ruotsi, Rus, Kyiv, Rurik, the names
@scene("07b_rus", 7, 25.1, 83.9, EAST, dict(sw=SWEDEN, rus=RUSLAND), res="50")
def _(fr, t):
    terr(fr, "sw", NOR); terr(fr, "rus", RUS, fr.R(31.4, 1.2))
    region(fr, 15.6, 60.9, "SWEDEN", size=24, sp=7, w="b", color=WHITE, a=out(fr, 61.0))
    gline(fr, ROAD_DN, width=3.6, color=INK, halo=WHITE, a=0.85); gline(fr, ROAD_VO, width=3.6, color=INK, halo=WHITE, a=0.85 * out(fr, 39.2))
    w1 = out(fr, 39.2)
    PQL(fr, 25.5, 62.0, "THE FINNS", dx=0, dy=-30, a=fr.R(25.2, 0.4) * w1, size=18, light=True, pad=(10, 7)); gline(fr, arc((25.2, 61.6), (18.6, 60.6), 0.2), width=3, frac=fr.R(25.9, 1.0), dash=(9, 7), arrow=True, color=CHAR, a=w1)
    PQ(fr, 400, 130, "RUOTSI", a=fr.R(26.6, 0.4) * w1, size=34); PQ(fr, 400, 198, "AN OLD NORSE WORD FOR ROWING", a=fr.R(28.4, 0.4) * w1, size=19, light=True, pad=(12, 8))
    T(fr, 400, 262, "↓", size=30, w="b", anchor="m", a=fr.R(31.2, 0.3) * w1); PQ(fr, 400, 326, "RUS", a=fr.R(32.6, 0.4) * w1, size=34)
    region(fr, 33.2, 56.4, "RUS", a=fr.R(32.8, 0.5), size=40, sp=16, w="b", color=WHITE)
    modern(fr, 44.5, 59.6, "NOW RUSSIA", a=fr.R(36.6, 0.5) * out(fr, 48.0), size=19, color=(92, 80, 60)); modern(fr, 27.8, 53.4, "NOW BELARUS", a=fr.R(37.8, 0.5) * out(fr, 48.0), size=16, color=(250, 240, 224))
    city(fr, "KYIV", a=fr.R(41.3, 0.4), side="l", r=9, size=28, color=WHITE); pulse(fr, C["KYIV"], 41.5, 2.4, color=WHITE, rmax=48, width=3.5)
    PQL(fr, 31.9, 48.9, "DNIEPER", dx=76, dy=14, a=fr.R(42.0, 0.4) * out(fr, 48.0), size=18, light=True, pad=(10, 7))
    w2 = out(fr, 63.8)
    PQ(fr, 400, 130, "THE OLDEST EAST SLAVIC CHRONICLE", a=fr.R(43.2, 0.4) * out(fr, 48.2), size=19); PQ(fr, 400, 190, "WRITTEN AROUND 1113", a=fr.R(45.2, 0.4) * out(fr, 48.2), size=20, light=True, pad=(12, 8))
    PQ(fr, 400, 130, "862", a=fr.R(48.5, 0.4) * w2, size=36)
    gline(fr, arc((31.0, 58.6), (18.8, 59.9), 0.2), width=3.4, frac=fr.R(53.0, 1.6), dash=(10, 7), arrow=True, color=CHAR, a=w2 * out(fr, 61.2))
    col(fr, 208, 204, [("“OUR LAND IS GREAT AND RICH,", 55.0), ("BUT THERE IS NO ORDER IN IT.", 57.0), ("COME AND RULE OVER US.”", 59.3)], size=20, gap=52, dim=w2)
    gline(fr, arc((18.8, 59.6), (31.3, 58.5), 0.2), width=5, frac=fr.R(61.5, 1.6), arrow=True, halo=WHITE, a=w2)
    PQL(fr, 31.3, 58.5, "RURIK", dx=96, dy=-4, a=fr.R(62.6, 0.4) * out(fr, 75.2), size=26)
    city(fr, "MOSCOW", a=fr.R(66.6, 0.4) * out(fr, 75.2), side="r", r=6, size=22, color=WHITE, icon=False)
    tline(fr, fr.R(64.2, 0.5) * out(fr, 75.2), fr.R(64.8, 3.6), left="862", right="THE END OF THE 1500s", title="HIS DESCENDANTS RULE", ra=fr.R(67.6, 0.5))
    PQ(fr, 400, 130, "WRITTEN MUCH LATER", a=fr.R(70.0, 0.4) * out(fr, 75.2), size=24); PQ(fr, 400, 192, "HISTORIANS TREAT IT CAREFULLY", a=fr.R(72.6, 0.4) * out(fr, 75.2), size=19, light=True, pad=(12, 8))
    PQ(fr, 400, 130, "THE PRINCES' NAMES", a=fr.R(75.6, 0.4), size=26)
    for i, (a_, b_, t0) in enumerate((("OLEG", "HELGI", 78.8), ("IGOR", "INGVAR", 79.6), ("OLGA", "HELGA", 80.4))):
        PQ(fr, 300, 204 + 62 * i, a_, a=fr.R(t0, 0.3), size=24, light=True); T(fr, 400, 204 + 62 * i, "=", size=26, w="b", anchor="m", a=fr.R(t0 + 0.3, 0.3)); PQ(fr, 510, 204 + 62 * i, b_, a=fr.R(t0 + 0.6, 0.3), size=24)

# ================= 7c. VO 83.8-91.7: Ibn Fadlan on the Volga
VOLG = cam_box(22, 62, 30, 58.5)
@scene("07c_ibn_fadlan", 7, 83.8, 91.8, VOLG, dict(rus=RUSLAND), res="50")
def _(fr, t):
    terr(fr, "rus", RUS, 0.75); rivers_hl(fr, R_VOLGA, 0.9, width=4.5)
    PQ(fr, 330, 130, "922", a=fr.R(83.9, 0.4), size=36)
    city(fr, "BAGHDAD", a=fr.R(85.2, 0.4), side="r", r=8, size=26, icon=False)
    gline(fr, smooth([C["BAGHDAD"], (49.5, 36.5), (57, 39.5), (59.5, 43.5), (56, 48.5), (52, 52.5), C["BULGAR"]], 12), width=5, frac=fr.R(86.2, 2.6), arrow=True, halo=WHITE)
    PQL(fr, *C["BAGHDAD"], "AHMAD IBN FADLAN", dx=30, dy=56, a=fr.R(86.4, 0.4), size=22, pad=(12, 8))
    PQL(fr, *C["BULGAR"], "RUS TRADERS ON THE VOLGA", dx=-250, dy=-52, a=fr.R(88.4, 0.4), size=20, pad=(12, 8)); city(fr, "", ll=C["BULGAR"], label="", r=7, a=fr.R(88.6, 0.4))
    PQ(fr, 330, 198, "HE WRITES:", a=fr.R(90.6, 0.3), size=22, light=True, pad=(12, 8))

# ================= 8a. VO 0-32.3: the Great City
SOUTH = cam_box(17, 43, 39.3, 54)
@scene("08a_miklagard", 8, 0.0, 32.4, SOUTH, dict(byz=BYZANT, rus=RUSLAND), res="50")
def _(fr, t):
    terr(fr, "byz", BYZ, 0.85); terr(fr, "rus", RUS, 0.75)
    gline(fr, ROAD_DN, width=5, frac=0.42 + 0.58 * fr.R(0.2, 2.6), color=INK, halo=WHITE, arrow=True)
    city(fr, "CONSTANTINOPLE", a=fr.R(2.9, 0.4), side="l", r=11, size=30, color=WHITE); pulse(fr, C["CONSTANTINOPLE"], 3.0, 2.6, color=WHITE, rmax=60, width=4)
    PQ(fr, 400, 130, "MIKLAGARD", a=fr.R(5.4, 0.4) * out(fr, 25.0), size=34); PQ(fr, 400, 198, "THE GREAT CITY", a=fr.R(6.4, 0.4) * out(fr, 25.0), size=24, light=True, pad=(12, 8))
    PQ(fr, 400, 262, "THE RICHEST CITY IN CHRISTIAN EUROPE", a=fr.R(8.2, 0.4) * out(fr, 25.0), size=18, light=True, pad=(12, 8))
    PQ(fr, 400, 130, "TREATIES FOLLOW", a=fr.R(25.5, 0.4), size=28)
    PQ(fr, 400, 196, "IF THESE MEN ARE GOING TO FIGHT,", a=fr.R(28.4, 0.4), size=19, light=True, pad=(12, 8)); PQ(fr, 400, 250, "BETTER THAT THEY FIGHT FOR US", a=fr.R(30.2, 0.4), size=21)

# ================= 8b. VO 32.3-50.5: Basil and Vladimir
@scene("08b_vladimir", 8, 32.3, 50.6, SOUTH, dict(byz=BYZANT, rus=RUSLAND), res="50")
def _(fr, t):
    terr(fr, "byz", BYZ, 0.85); terr(fr, "rus", RUS, 0.75)
    city(fr, "CONSTANTINOPLE", side="l", r=11, size=30, color=WHITE); city(fr, "KYIV", a=fr.R(37.0, 0.4), side="l", r=10, size=28, color=WHITE)
    PQ(fr, 400, 130, "988", a=fr.R(32.4, 0.4), size=36)
    PQL(fr, *C["CONSTANTINOPLE"], "EMPEROR BASIL THE SECOND", dx=60, dy=70, a=fr.R(33.4, 0.4), size=20, pad=(12, 8)); PQL(fr, *C["CONSTANTINOPLE"], "NEEDS SOLDIERS", dx=60, dy=122, a=fr.R(35.4, 0.4) * out(fr, 44.8), size=18, light=True, pad=(10, 7))
    PQL(fr, *C["KYIV"], "VLADIMIR, PRINCE OF KYIV", dx=250, dy=-30, a=fr.R(36.9, 0.4), size=20, pad=(12, 8))
    gline(fr, ROAD_DN, width=6, frac=_fa(ROAD_DN, 30.55, 50.45) + (1 - _fa(ROAD_DN, 30.55, 50.45)) * fr.R(38.6, 2.2), color=INK, halo=WHITE, arrow=True, a=fr.R(38.4, 0.3))
    rect_cover = None
    PQL(fr, 33.6, 46.6, "SIX THOUSAND WARRIORS", dx=190, dy=-6, a=fr.R(39.2, 0.4), size=22)
    col(fr, 208, 204, [("VLADIMIR MARRIES THE EMPEROR'S SISTER", 41.0), ("AND IS BAPTISED", 43.4), ("THE RUS BECOME ORTHODOX CHRISTIANS", 45.2), ("THE SIX THOUSAND STAY", 48.6)], size=18, gap=50)

# ================= 8c. VO 59.9-81.1: Scandinavia goes south; the runes in Hagia Sophia
@scene("08c_go_south", 8, 59.9, 81.2, EAST, dict(sc=U(NORWAY, SWEDEN, DENMARK), byz=BYZANT), res="50")
def _(fr, t):
    terr(fr, "sc", NOR); terr(fr, "byz", BYZ, 0.85)
    region(fr, 14.6, 63.6, "SCANDINAVIA", a=fr.R(62.6, 0.4), size=22, sp=7, w="b", color=WHITE)
    PQ(fr, 400, 130, "FOR THE NEXT CENTURY", a=fr.R(60.0, 0.4) * out(fr, 74.5), size=26); PQ(fr, 400, 194, "YOUNG MEN GO SOUTH TO SERVE", a=fr.R(62.9, 0.4) * out(fr, 74.5), size=20, light=True, pad=(12, 8))
    for i, (st, bend) in enumerate((((10.5, 59.5), 0.05), ((17.6, 59.6), 0.0), ((10.0, 56.0), 0.1))):
        gline(fr, smooth([st, (22 + i, 57.8 - i), (30.0, 54.0 - 0.6 * i), (31.2 + 0.5 * i, 48.5), (30.4, 44.0), C["CONSTANTINOPLE"]], 12), width=4.2, frac=fr.R(60.4 + 0.4 * i, 2.6), arrow=True, halo=WHITE)
    city(fr, "CONSTANTINOPLE", side="r", r=10, size=26, color=WHITE)
    PQ(fr, 400, 130, "RUNES IN HAGIA SOPHIA", a=fr.R(74.8, 0.4), size=26); PQ(fr, 400, 194, "PROBABLY THE NAME HALFDAN", a=fr.R(75.6, 0.4), size=20, light=True, pad=(12, 8))
    PQ(fr, 400, 252, "STILL THERE, A THOUSAND YEARS LATER", a=fr.R(77.2, 0.4), size=18, light=True, pad=(12, 8))

# ================= 8d. VO 81.1-95.0: Harald
HAR = cam_box(-3, 38, 34.6, 66)
H1 = smooth([(10.4, 63.4), (13.5, 62.0), (17.0, 60.2), (21, 59.7), (27.5, 60.0), (31.3, 58.6), (31.6, 55.2), (30.55, 50.45), (33.5, 48.6), (32.3, 46.5), (30.0, 43.3), (29.0, 41.1)], 12)
H2 = smooth([(28.9, 40.9), (26.3, 40.1), (25.0, 38.0), (22.6, 36.0), (18.5, 36.4), (15.4, 37.2)], 12)
H3 = smooth([(29.0, 41.1), (30.0, 43.3), (32.3, 46.5), (33.5, 48.6), (30.55, 50.45), (31.6, 55.2), (31.3, 58.6), (27.5, 60.0), (21, 59.7), (17.0, 60.2), (13.5, 62.0), (10.4, 63.4)], 12)
@scene("08d_harald", 8, 81.1, 95.1, HAR, dict(no=NORWAY, byz=BYZANT), res="50")
def _(fr, t):
    terr(fr, "no", NOR); terr(fr, "byz", BYZ, 0.85)
    back = fr.R(89.4, 1.6)
    gline(fr, H1, width=5, frac=fr.R(81.4, 2.4), color=INK, halo=WHITE, arrow=back <= 0, a=1 - 0.45 * back)
    gline(fr, H2, width=4.5, frac=fr.R(85.3, 1.2), color=INK, halo=WHITE, arrow=True, a=1 - 0.45 * back)
    arrow(fr, [(28.6, 41.3), (27.0, 42.2), (25.4, 42.8)], 86.4, 0.9, width=4.5, a=1 - 0.45 * back)
    gline(fr, [(x + 0.9, y) for x, y in H3], width=6, frac=back, color=NOR_D, halo=WHITE, arrow=True)
    region(fr, 9.4, 61.2, "NORWAY", size=22, sp=7, w="b", color=WHITE); city(fr, "CONSTANTINOPLE", side="r", r=10, size=24, color=WHITE)
    PQ(fr, 330, 130, "1034", a=fr.R(82.6, 0.4), size=36); PQ(fr, 330, 198, "FIVE HUNDRED MEN", a=fr.R(83.6, 0.4), size=22, light=True, pad=(12, 8))
    PQL(fr, 14.2, 37.5, "SICILY", dx=0, dy=-46, a=fr.R(86.0, 0.4), size=20, light=True, pad=(10, 7)); PQL(fr, 25.2, 42.9, "BULGARIA", dx=-70, dy=-40, a=fr.R(87.0, 0.4), size=20, light=True, pad=(10, 7))
    PQ(fr, 330, 258, "RICH ENOUGH TO BECOME KING", a=fr.R(89.6, 0.4), size=19, light=True, pad=(12, 8))
    PQL(fr, 10.4, 63.4, "HARALD", dx=150, dy=-30, a=fr.R(92.4, 0.4), size=30); PQL(fr, 10.4, 63.4, "REMEMBER HIM", dx=150, dy=34, a=fr.R(94.0, 0.3), size=20, light=True, pad=(12, 8))

# ================= 9a. VO 0-16.3: west across the Atlantic
NATL = cam_box(-29, 14, 56.3, 67.6)
@scene("09a_go_west", 9, 0.0, 16.4, NATL, dict(no=NORWAY, ice=ICELAND), res="50")
def _(fr, t):
    terr(fr, "no", NOR); terr(fr, "ice", NOR, fr.R(13.8, 1.2))
    PQ(fr, 330, 130, "NOW GO WEST", a=fr.R(0.1, 0.3) * out(fr, 9.6), size=30)
    for i, (ll, nm, t0, dx, dy) in enumerate(((C["ORKNEY"], "ORKNEYS", 2.6, 0, 44), (C["SHETLAND"], "SHETLANDS", 3.3, 96, 0), (C["FAROE"], "FAROES", 4.0, 0, -42))):
        gline(fr, arc((5.0, 60.6 + 0.4 * i), ll, -0.1 - 0.04 * i), width=4, frac=fr.R(t0 - 0.6, 1.0), arrow=True, halo=WHITE, color=NOR_D)
        x, y = P(fr.cam, *ll); circ(fr, x, y, 9, WHITE, fr.R(t0, 0.3)); circ(fr, x, y, 6.5, NOR, fr.R(t0, 0.3)); PQL(fr, *ll, nm, dx=dx, dy=dy, a=fr.R(t0, 0.3), size=19, light=True, pad=(10, 7))
    gline(fr, arc(C["FAROE"], (-14.2, 64.6), -0.14), width=5, frac=fr.R(5.6, 1.8), arrow=True, halo=WHITE, color=NOR_D)
    PQ(fr, 400, 800, "A LARGE EMPTY ISLAND", a=fr.R(7.4, 0.4), size=26)
    PQ(fr, 400, 864, "IRISH MONKS HAD LIVED THERE", a=fr.R(9.9, 0.4), size=19, light=True, pad=(12, 8))
    PQ(fr, 820, 800, "874", a=fr.R(14.6, 0.4), size=34); PQ(fr, 820, 864, "THE TRADITIONAL DATE", a=fr.R(13.8, 0.4), size=17, light=True, pad=(12, 8))

# ================= 9s. VO 23.9-33.7: the ash layer (scheme on black)
@scene("09s_ash", 9, 23.9, 33.8, SCAND, dict(), res="50")
def _(fr, t):
    blank(fr); x0, x1 = 360, 1560; a0 = fr.R(23.9, 0.5); rng = np.random.default_rng(4)
    bands = [(560, 640, (74, 62, 50)), (640, 668, (196, 190, 176)), (668, 790, (60, 50, 42)), (790, 900, (46, 40, 36))]
    for i, (ya, yb, c_) in enumerate(bands):
        pts = [(x0, yb)] + [(x, ya + 5 * math.sin(x / 90.0 + i * 1.7)) for x in range(x0, x1 + 1, 30)] + [(x1, yb)]
        poly(fr, pts, c_, a0 * (fr.R(25.2, 0.6) if i == 1 else 1.0) if i == 1 else a0)
    rect(fr, x0, 558, x1, 564, (120, 132, 92), a0)                                                             # turf line
    ha = fr.R(28.6, 0.7)                                                                                       # the oldest houses, above the ash
    poly(fr, [(700, 560), (760, 480), (1160, 480), (1220, 560)], (150, 150, 146), ha); rect(fr, 930, 506, 990, 560, BLACK, ha)
    for xx in (800, 880, 1040, 1120): rect(fr, xx, 512, xx + 34, 536, BLACK, ha)
    T(fr, 960, 440, "THE OLDEST HOUSES", size=20, sp=6, w="s", color=(190, 190, 186), anchor="m", a=ha)
    pline(fr, [(1580, 654), (1650, 654)], color=WHITE, width=3, a=fr.R(25.4, 0.4))
    PQ(fr, 1660, 654, "VOLCANIC ASH", a=fr.R(25.4, 0.4), size=24, anchor="l", light=True); PQ(fr, 1660, 716, "FROM THE 870s", a=fr.R(26.8, 0.4), size=24, anchor="l")
    PQ(fr, 960, 190, "THE STORY AND THE SCIENCE AGREE", a=fr.R(31.2, 0.4), size=30, light=True)

# ================= 9b. VO 33.7-93.4: Iceland settled; the Althing; one law and one faith
ICEC = cam_box(-26.2, -11.8, 62.85, 66.95)
@scene("09b_iceland", 9, 33.7, 93.5, ICEC, dict(x_co=COAST(ICELAND_P, 0.42)), res="10")
def _(fr, t):
    region(fr, -18.4, 65.25, "ICELAND", a=fr.R(34.0, 0.4) * out(fr, 59.0), size=34, sp=14, w="b")
    city(fr, "REYKJAVIK", a=fr.R(33.8, 0.4), side="l", r=6, size=20, icon=False)
    pts = scatter(fr, "x_co", 230, seed=6); dots_px(fr, pts, lambda i: fr.R(34.2 + 3.4 * i / max(1, len(pts)), 0.3), r=3.2, color=NOR, ring=WHITE)
    PQ(fr, 400, 130, "WITHIN SIXTY YEARS", a=fr.R(33.9, 0.4) * out(fr, 38.2), size=28); PQ(fr, 400, 194, "FULLY SETTLED", a=fr.R(36.6, 0.4) * out(fr, 38.2), size=22, light=True, pad=(12, 8))
    PQ(fr, 400, 130, "NO KING", a=fr.R(38.9, 0.4) * out(fr, 58.9), size=34)
    PQ(fr, 400, 198, "930: THE ALTHING", a=fr.R(41.6, 0.4) * out(fr, 58.9), size=26)
    x, y = P(fr.cam, *C["THINGVELLIR"]); ta = fr.R(45.6, 0.4)
    circ(fr, x, y, 13, WHITE, ta); circ(fr, x, y, 9.5, INK, ta); pulse(fr, C["THINGVELLIR"], 45.8, 2.6, color=INK, rmax=52, width=3.5)
    PQL(fr, *C["THINGVELLIR"], "THINGVELLIR", dx=120, dy=-40, a=fr.R(46.4, 0.4), size=22)
    TL(fr, *C["THINGVELLIR"], "THE PLAIN OF THE ASSEMBLY", dx=24, dy=4, size=15, sp=3, a=fr.R(47.4, 0.4) * out(fr, 58.9), w="m")
    for i in range(12):
        ang = math.radians(30 * i + 8); x2, y2 = P(fr.cam, -21.12 + 3.4 * math.cos(ang) * (1.0 if i % 2 else 0.7), 64.26 + 1.25 * math.sin(ang) * (1.0 if i % 2 else 0.72))
        pline(fr, [(x2, y2), (x + (x2 - x) * 0.12, y + (y2 - y) * 0.12)], width=2.6, frac=fr.R(44.8 + 0.1 * i, 1.0), a=0.7 * out(fr, 58.9), arrow=True, color=CHAR)
    col(fr, 1330, 150, [("THE LAWSPEAKER RECITES", 49.5), ("A THIRD OF THE LAW EACH YEAR", 50.6), ("THE WHOLE CODE EVERY THREE YEARS", 52.4)], size=18, gap=48, first_dark=True, dim=out(fr, 58.9))
    PQ(fr, 400, 262, "STILL ICELAND'S PARLIAMENT", a=fr.R(54.7, 0.4) * out(fr, 58.9), size=20, light=True, pad=(12, 8))
    PQ(fr, 400, 318, "ONE OF THE OLDEST IN THE WORLD", a=fr.R(56.6, 0.4) * out(fr, 58.9), size=18, light=True, pad=(12, 8))
    PQ(fr, 400, 130, "THE YEAR 1000", a=fr.R(59.4, 0.4), size=32); PQ(fr, 400, 196, "ITS HARDEST CASE", a=fr.R(61.0, 0.4) * out(fr, 84.4), size=20, light=True, pad=(12, 8))
    merge = fr.R(84.6, 2.0); rng = np.random.default_rng(12)
    for i in range(34):
        sg = -1 if i % 2 else 1; ox = sg * (34 + 15 * (i // 2 % 5)) * (1 - 0.72 * merge) + rng.normal(0, 3); oy = (i // 10 - 1.2) * 15 + rng.normal(0, 3)
        a = fr.R(62.7 + 0.04 * i, 0.4); circ(fr, x + ox, y + 44 + oy, 6, WHITE, a); circ(fr, x + ox, y + 44 + oy, 4.4, mix(CHAR, NOR if sg < 0 else FRK, 1 - merge) if merge > 0 else (NOR if sg < 0 else FRK), a)
    PQL(fr, *C["THINGVELLIR"], "PAGANS", dx=-120, dy=112, a=fr.R(62.8, 0.4) * out(fr, 84.4), size=18, light=True, pad=(10, 7))
    PQL(fr, *C["THINGVELLIR"], "CHRISTIANS", dx=120, dy=112, a=fr.R(63.6, 0.4) * out(fr, 84.4), size=18, light=True, pad=(10, 7))
    PQ(fr, 1500, 150, "THE LAWSPEAKER, THORGEIR, DECIDES", a=fr.R(67.2, 0.4) * out(fr, 84.4), size=19)
    col(fr, 1330, 150, [("ONE LAW AND ONE FAITH", 84.5), ("PAGANS MAY STILL WORSHIP IN PRIVATE", 85.0), ("EVERYONE MAY KEEP EATING HORSE MEAT", 86.8)], size=18, gap=50, first_dark=True)
    PQ(fr, 400, 196, "BY COMMITTEE", a=fr.R(89.9, 0.4), size=26); PQ(fr, 400, 260, "AND NOBODY DIES.", a=fr.R(92.1, 0.3), size=22, light=True, pad=(12, 8))

# ================= 10a. VO 0-28.5: Erik the Red and the name
GRN = cam_box(-58, -10, 57.6, 69.4)
@scene("10a_greenland", 10, 0.0, 28.6, GRN, dict(ice=ICELAND, gs=GREENSET), res="10")
def _(fr, t):
    terr(fr, "ice", NOR); terr(fr, "gs", NOR, fr.R(27.4, 1.0))
    region(fr, -18.4, 67.5, "ICELAND", size=22, sp=7, w="b", a=fr.R(0.1, 0.4))
    PQ(fr, 1500, 150, "AROUND 982", a=fr.R(3.6, 0.4) * out(fr, 15.0), size=30); PQ(fr, 1500, 214, "ERIK THE RED", a=fr.R(4.8, 0.4), size=28)
    PQ(fr, 1500, 276, "OUTLAWED FOR THREE YEARS", a=fr.R(6.6, 0.4) * out(fr, 15.0), size=19, light=True, pad=(12, 8))
    gline(fr, smooth([(-23.6, 64.9), (-30, 65.2), (-36.5, 64.0), (-41.0, 61.4), (-43.6, 59.6), (-46.4, 60.2), (-47.6, 61.2)], 12), width=5, frac=fr.R(11.0, 3.2), arrow=True, halo=WHITE, color=NOR_D)
    region(fr, -43.5, 66.6, "GREENLAND", a=fr.R(16.6, 0.5), size=40, sp=16, w="b", color=(70, 96, 110))
    PQ(fr, 420, 880, "“AN ATTRACTIVE NAME”", a=fr.R(21.6, 0.4), size=26); PQ(fr, 420, 942, "THE OLDEST PROPERTY MARKETING ON RECORD", a=fr.R(24.2, 0.4), size=17, light=True, pad=(12, 8))
    PQ(fr, 900, 880, "IT WORKS.", a=fr.R(27.5, 0.3), size=26)

# ================= 10b. VO 37.4-39.6: Leif goes further
VIN = cam_box(-71, -34, 43.6, 64.6)
LEIF = smooth([(-46.0, 60.6), (-50.5, 60.8), (-55.5, 59.6), (-60.5, 57.4), (-59.5, 54.6), (-56.4, 52.6), (-55.5, 51.7)], 12)
@scene("10b_leif", 10, 37.4, 39.7, VIN, dict(gs=GREENSET), res="50")
def _(fr, t):
    terr(fr, "gs", NOR)
    region(fr, -44.0, 63.3, "GREENLAND", size=22, sp=7, w="b", color=(70, 96, 110))
    gline(fr, LEIF, width=5, frac=fr.R(37.6, 1.9), arrow=True, halo=WHITE, color=NOR_D)
    PQ(fr, 1500, 150, "ERIK'S SON LEIF", a=fr.R(37.5, 0.3), size=28)

# ================= 10c. VO 58.8-73.3: what the dig found; someone sailed further south
NFL = cam_box(-70, -49, 43.6, 53.4)
@scene("10c_lanse", 10, 58.8, 73.4, NFL, dict(), res="10")
def _(fr, t):
    x, y = P(fr.cam, *C["LANSE"]); circ(fr, x, y, 13, WHITE); circ(fr, x, y, 9.5, NOR)
    region(fr, -56.2, 48.7, "NEWFOUNDLAND", size=20, sp=6, w="b")
    col(fr, 1290, 150, [("THE EXCAVATIONS TURN UP", 58.9), ("NORSE BUILDINGS", 61.4), ("IRON NAILS", 62.6), ("A BRONZE CLOAK PIN", 63.6), ("BUTTERNUTS", 65.2)], size=20, gap=52, first_dark=True)
    PQ(fr, 400, 130, "BUTTERNUTS DO NOT GROW THAT FAR NORTH", a=fr.R(66.4, 0.4), size=19)
    gline(fr, smooth([(-56.2, 51.2), (-58.6, 49.9), (-61.5, 48.4), (-64.2, 47.4), (-65.3, 46.4)], 12), width=5, frac=fr.R(69.0, 2.0), arrow=True, halo=WHITE, color=NOR_D)
    PQ(fr, 400, 194, "SOMEONE HAD SAILED FURTHER SOUTH", a=fr.R(69.0, 0.4), size=19, light=True, pad=(12, 8))
    PQL(fr, -65.6, 46.3, "WHERE WILD GRAPES GROW", dx=30, dy=62, a=fr.R(71.0, 0.4), size=20, pad=(12, 8))

# ================= 10d. VO 85.0-106.6: 471 years before Columbus; America does not last; Hvalsey
@scene("10d_silence", 10, 85.0, 106.7, VIN, dict(gs=GREENSET), res="50")
def _(fr, t):
    fade = fr.R(105.8, 0.9)
    terr(fr, "gs", NOR, 1 - 0.75 * fade)
    region(fr, -44.0, 63.3, "GREENLAND", size=22, sp=7, w="b", color=(70, 96, 110))
    gone = fr.R(89.4, 1.6)
    gline(fr, LEIF, width=4.5, color=NOR_D, halo=WHITE, arrow=True, a=1 - gone)
    x, y = P(fr.cam, *C["LANSE"]); circ(fr, x, y, 12, WHITE, 1 - 0.7 * gone); circ(fr, x, y, 8.6, mix((160, 160, 160), NOR, gone), 1 - 0.5 * gone)
    tl = out(fr, 89.0)
    tline(fr, fr.R(85.0, 0.4) * tl, fr.R(85.4, 2.2), left="1021", right="COLUMBUS", title="471 YEARS", ra=fr.R(86.6, 0.5))
    PQ(fr, 400, 130, "AMERICA DOES NOT LAST", a=fr.R(89.3, 0.4) * out(fr, 96.6), size=26)
    col(fr, 208, 196, [("THE SETTLERS ARE FEW", 91.4), ("HOME IS FAR AWAY", 92.8), ("THE PEOPLE ALREADY THERE FIGHT BACK", 94.0)], size=18, gap=48, dim=out(fr, 96.6))
    PQ(fr, 400, 130, "GREENLAND LASTS", a=fr.R(96.9, 0.4) * (1 - fade), size=26); PQ(fr, 400, 194, "MORE THAN FOUR HUNDRED YEARS", a=fr.R(97.8, 0.4) * (1 - fade), size=19, light=True, pad=(12, 8))
    x2, y2 = P(fr.cam, *C["HVALSEY"]); ha = fr.R(100.6, 0.4) * (1 - 0.6 * fade); circ(fr, x2, y2, 10, WHITE, ha); circ(fr, x2, y2, 7, INK, ha)
    PQL(fr, *C["HVALSEY"], "HVALSEY CHURCH", dx=-170, dy=-12, a=fr.R(102.2, 0.4) * (1 - fade), size=22); PQL(fr, *C["HVALSEY"], "A WEDDING, SEPTEMBER 1408", dx=-170, dy=46, a=fr.R(103.4, 0.4) * (1 - fade), size=18, light=True, pad=(10, 7))
    PQ(fr, 960, 540, "AFTER THAT, SILENCE.", a=fr.R(105.9, 0.4), size=30)

# ================= 11a. VO 0-49.4: Jelling; kings and the new religion
SCS = cam_box(2.5, 23, 53.6, 65.2)
def xmark(fr, lon, lat, a=1.0, k=1.0, color=WHITE):
    if a <= 0: return
    x, y = P(fr.cam, lon, lat); rect(fr, x - 2.6 * k, y - 15 * k, x + 2.6 * k, y + 13 * k, color, a); rect(fr, x - 9 * k, y - 8 * k, x + 9 * k, y - 3 * k, color, a)
_CH_DK = [(9.42, 55.76), (12.08, 55.64), (10.2, 56.15), (9.9, 57.05), (10.4, 55.4), (13.2, 55.7), (8.77, 55.33)]
_CH_NO = [(10.4, 63.43), (5.3, 60.4), (10.75, 59.9), (5.7, 58.97), (7.9, 61.2), (11.1, 60.8)]
_CH_SE = [(17.64, 59.86), (13.2, 58.4), (15.6, 58.4)]
@scene("11a_jelling", 11, 0.0, 49.5, SCS, dict(dk=DENMARK, no=I(NORWAY, [(3, 57), (13, 57), (16, 66), (3, 66)]), sw=SWEDEN), res="10")
def _(fr, t):
    k = fr.R(11.4, 1.6)
    terr(fr, "dk", NOR, fr.R(0.8, 1.0)); terr(fr, "no", NOR, k * (1 - 0.0)); terr(fr, "sw", (176, 186, 140), 0.55)
    PQ(fr, 1500, 150, "CHIEFTAINS ARE TURNING INTO KINGS", a=fr.R(0.4, 0.4) * out(fr, 4.2), size=20)
    PQ(fr, 1500, 150, "AROUND 965", a=fr.R(4.4, 0.4) * out(fr, 22.5), size=30); PQ(fr, 1500, 214, "KING HARALD OF DENMARK", a=fr.R(5.6, 0.4) * out(fr, 22.5), size=21, light=True, pad=(12, 8))
    city(fr, "JELLING", a=fr.R(7.8, 0.4), side="l", r=7, size=24, color=WHITE, icon=False); pulse(fr, C["JELLING"], 8.0, 2.4, color=WHITE, rmax=46, width=3.5)
    col(fr, 1318, 290, [("THE RUNES SAY:", 9.8), ("ALL OF DENMARK AND NORWAY", 11.4), ("MADE THE DANES CHRISTIAN", 13.2), ("THEIR COUNTRY'S BIRTH CERTIFICATE", 15.6), ("IN EVERY DANISH PASSPORT", 18.4)], size=18, gap=48, first_dark=True, dim=out(fr, 22.5))
    region(fr, 8.8, 61.0, "NORWAY", size=24, sp=8, w="b", color=WHITE, a=fr.R(44.4, 0.4))
    region(fr, 15.8, 60.4, "SWEDEN", size=24, sp=8, w="b", a=fr.R(47.8, 0.4))
    PQ(fr, 1500, 150, "ONE GOD IN HEAVEN", a=fr.R(38.2, 0.4), size=26); PQ(fr, 1500, 214, "ONE KING ON EARTH", a=fr.R(39.4, 0.4), size=26, light=True)
    PQ(fr, 1500, 284, "THE CHURCH BRINGS WRITING", a=fr.R(41.0, 0.4), size=19, light=True, pad=(12, 8))
    for i, ll in enumerate(_CH_DK): xmark(fr, *ll, a=fr.R(36.6 + 0.2 * i, 0.4), k=1.1)
    for i, ll in enumerate(_CH_NO): xmark(fr, *ll, a=fr.R(44.5 + 0.2 * i, 0.4), k=1.1)
    for i, ll in enumerate(_CH_SE): xmark(fr, *ll, a=fr.R(48.4 + 0.3 * i, 0.4) * 0.8, k=1.1, color=INK)
    PQ(fr, 400, 130, "TWO KINGS NAMED OLAF", a=fr.R(45.4, 0.4), size=22); PQ(fr, 400, 192, "SWEDEN TAKES LONGER", a=fr.R(47.9, 0.4), size=20, light=True, pad=(12, 8))

# ================= 11k. VO 22.7-36.3: Bluetooth (text frame; the two runes are drawn apart, not as the trademark)
def rune(fr, x, y, kind, h=300, w=24, a=1.0, color=WHITE):
    if a <= 0: return
    pline(fr, [(x, y - h / 2), (x, y + h / 2)], color=color, width=w, a=a)
    if kind == "h":
        d = h * 0.2
        pline(fr, [(x - d, y - d), (x + d, y + d)], color=color, width=w, a=a); pline(fr, [(x - d, y + d), (x + d, y - d)], color=color, width=w, a=a)
    else:
        d = h * 0.3
        pline(fr, [(x, y - h / 2), (x + d, y - h / 4), (x, y), (x + d, y + h / 4), (x, y + h / 2)], color=color, width=w, a=a)
@scene("11k_bluetooth", 11, 22.7, 36.4, SCAND, dict(), res="50")
def _(fr, t):
    blank(fr)
    T(fr, 960, 170, "HARALD'S NICKNAME", size=22, sp=7, w="s", color=(150, 152, 156), anchor="m", a=fr.R(22.8, 0.4))
    PQ(fr, 960, 260, "BLUETOOTH", a=fr.R(23.7, 0.4), size=54, light=True)
    PQ(fr, 960, 372, "THE 1990s: A WIRELESS STANDARD NAMED AFTER HIM", a=fr.R(25.2, 0.4), size=20)
    T(fr, 960, 440, "THE KING WHO UNITED THE DANES", size=20, sp=6, w="s", color=(150, 152, 156), anchor="m", a=fr.R(30.0, 0.4))
    ra = fr.R(32.6, 0.5); rune(fr, 780, 690, "h", a=fr.R(33.8, 0.4)); rune(fr, 1110, 690, "b", a=fr.R(34.6, 0.4))
    T(fr, 960, 500, "HIS INITIALS IN RUNES", size=22, sp=7, w="s", color=WHITE, anchor="m", a=ra)
    T(fr, 780, 900, "H", size=44, w="b", color=WHITE, anchor="m", a=fr.R(34.0, 0.3)); T(fr, 1126, 900, "B", size=44, w="b", color=WHITE, anchor="m", a=fr.R(34.8, 0.3))

# ================= 11b. VO 49.4-92.6: England pays again; Canute's North Sea Empire
NSE = cam_box(-10, 19, 49.2, 65.2)
_NOS = I(NORWAY, [(3, 57), (13, 57), (16, 66), (3, 66)])
@scene("11b_north_sea_empire", 11, 49.4, 92.7, NSE, dict(en=ENGLAND, dk=DENMARK, no=_NOS), res="50")
def _(fr, t):
    gone = fr.R(88.6, 2.4)
    e1 = fr.R(59.6, 1.2); terr(fr, "dk", NOR, 1.0); terr(fr, "en", mix(NOR, ENG4, e1), 1 - 0.0); terr(fr, "no", NOR, fr.R(70.6, 1.0) * (1 - gone))
    if gone > 0: terr(fr, "en", ENG4, gone)
    region(fr, -1.5, 52.6, "ENGLAND", size=24, sp=8, w="b", color=WHITE); region(fr, 9.3, 56.3, "DENMARK", size=18, sp=5, w="b", color=WHITE)
    region(fr, 8.6, 61.0, "NORWAY", size=22, sp=7, w="b", color=WHITE, a=fr.R(70.8, 0.4) * (1 - gone))
    w1 = out(fr, 58.6)
    PQ(fr, 400, 130, "ENGLAND IS PAYING AGAIN", a=fr.R(49.5, 0.4) * w1, size=26)
    for i, pts in enumerate(([(7.4, 56.6), (4.0, 55.4), (1.2, 54.0), (0.2, 53.5)], [(7.6, 55.6), (4.4, 53.6), (2.4, 52.2), (1.6, 51.6)])):
        arrow(fr, pts, 52.4 + 0.5 * i, 1.6, width=5, color=NOR_D, a=out(fr, 63.4))
        gline(fr, [(x, y - 0.5) for x, y in smooth(pts[::-1], 10)], width=3.4, frac=fr.R(55.4 + 0.5 * i, 1.6), arrow=True, color=GOLD, halo=INK, a=w1)
    PQ(fr, 400, 194, "TENS OF THOUSANDS OF POUNDS OF SILVER", a=fr.R(55.6, 0.4) * w1, size=18, light=True, pad=(12, 8))
    PQ(fr, 400, 130, "1013", a=fr.R(58.9, 0.4) * out(fr, 63.4), size=36); PQ(fr, 400, 198, "SWEYN FORKBEARD TAKES THE THRONE", a=fr.R(60.6, 0.4) * out(fr, 63.4), size=18, light=True, pad=(12, 8))
    PQ(fr, 400, 130, "HIS SON CANUTE", a=fr.R(63.7, 0.4) * (1 - gone), size=28)
    for i, (txt, t0, ll) in enumerate((("ENGLAND 1016", 66.8, (-1.5, 51.6)), ("DENMARK 1018", 68.6, (10.8, 55.2)), ("NORWAY 1028", 70.4, (9.0, 59.9)))):
        PQL(fr, *ll, txt, dy=14, a=fr.R(t0, 0.4) * out(fr, 78.2), size=18, light=True, pad=(10, 7))
    lk = fr.R(74.6, 1.6) * (1 - gone)
    for a_, b_ in (((0.6, 53.4), (7.9, 56.0)), ((7.6, 57.6), (6.4, 58.6)), ((1.2, 54.4), (5.0, 59.6))): gline(fr, arc(a_, b_, 0.12), width=3.6, frac=lk, color=WHITE, a=0.95 * (1 - gone), dash=(12, 8))
    for i in range(5): gship(fr, 2.6 + 1.1 * (i % 3) + 0.5 * (i // 3), 56.6 - 0.9 * (i // 3), k=0.9, a=fr.R(75.4 + 0.15 * i, 0.4) * (1 - gone))
    sea(fr, 3.4, 58.0, "NORTH SEA", size=16, a=fr.R(73.2, 0.4))
    PQ(fr, 1500, 150, "THE NORTH SEA EMPIRE", a=fr.R(73.0, 0.4) * (1 - gone), size=28); PQ(fr, 1500, 214, "HELD TOGETHER BY NOTHING BUT SHIPS", a=fr.R(76.0, 0.4) * (1 - gone), size=18, light=True, pad=(12, 8))
    PQ(fr, 400, 130, "CANUTE DIES IN 1035", a=fr.R(88.5, 0.4), size=26); PQ(fr, 400, 194, "WITHIN SEVEN YEARS IT IS GONE", a=fr.R(90.4, 0.4), size=20, light=True, pad=(12, 8))

# ================= 12a. VO 0-31.0: 1066, three men, Stamford Bridge
E66 = cam_box(-9, 13, 49.5, 63.2)
@scene("12a_1066", 12, 0.0, 31.1, E66, dict(en=ENGLAND, no=_NOS, nm=NORMANDY), res="50")
def _(fr, t):
    terr(fr, "en", ENG4); terr(fr, "no", NOR, fr.R(8.9, 0.8)); terr(fr, "nm", FRK, fr.R(6.9, 0.8) * 0.9)
    PQ(fr, 330, 130, "1066", a=fr.R(0.0, 0.3), size=40)
    PQ(fr, 330, 202, "THE ENGLISH KING DIES WITHOUT A SON", a=fr.R(2.0, 0.4) * out(fr, 8.6), size=17, light=True, pad=(12, 8))
    PQL(fr, -1.4, 52.3, "HAROLD GODWINSON", dy=0, a=fr.R(4.6, 0.4), size=20)
    PQ(fr, 330, 202, "TWO OTHER MEN WANT IT", a=fr.R(7.0, 0.4) * out(fr, 19.0), size=20, light=True, pad=(12, 8))
    PQL(fr, 8.6, 61.2, "HARALD HARDRADA", dx=230, dy=-20, a=fr.R(9.4, 0.4), size=20); PQL(fr, 8.6, 61.2, "THE SAME HARALD, NOW KING OF NORWAY", dx=230, dy=30, a=fr.R(11.2, 0.4) * out(fr, 19.0), size=15, light=True, pad=(10, 6))
    HP = [(5.0, 60.6), (0.6, 60.3), (-2.4, 59.0), (-1.4, 57.0), (-0.6, 55.2), (0.1, 54.0), (-0.3, 53.72), (-0.85, 53.8)]
    arrow(fr, HP, 15.0, 2.8, width=5.5, color=NOR_D, a=1 - 0.6 * fr.R(27.4, 0.8))
    lost = fr.R(27.6, 1.6)
    for i in range(15):
        a = fr.R(16.4 + 0.05 * i, 0.4) * (1.0 if i < 2 else 1 - lost); gship(fr, 1.2 + 0.95 * (i % 5) + 0.3 * (i // 5 % 2), 56.9 - 0.62 * (i // 5), k=0.72, a=a, flip=True)
    PQ(fr, 1180, 700, "ABOUT THREE HUNDRED SHIPS", a=fr.R(17.4, 0.4) * out(fr, 27.2), size=22)
    cross(fr, *C["STAMFORD"], a=fr.R(21.4, 0.3), r=11, width=5, color=WHITE)
    PQL(fr, *C["STAMFORD"], "STAMFORD BRIDGE", dx=-150, dy=-34, a=fr.R(21.6, 0.4), size=18, light=True, pad=(10, 7))
    PQ(fr, 1180, 700, "ONLY TWENTY-FOUR SAIL HOME", a=fr.R(28.6, 0.4), size=22)

# ================= 12b. VO 38.5-50.1: Rollo's descendant; the Viking Age ends
CHAN = cam_box(-5.2, 4.6, 47.9, 52.3)
@scene("12b_william", 12, 38.5, 50.2, CHAN, dict(en=ENGLAND, nm=NORMANDY), res="10")
def _(fr, t):
    k = fr.R(46.6, 1.6)
    terr(fr, "nm", NOR); terr(fr, "en", mix(NOR, ENG4, k))
    region(fr, -0.1, 48.95, "NORMANDY", size=30, sp=10, w="b", color=WHITE); region(fr, -1.3, 51.75, "ENGLAND", size=30, sp=10, w="b", color=WHITE)
    arrow(fr, [(0.25, 49.7), (0.5, 50.3), (0.5, 50.8)], 38.6, 1.2, width=6, color=INK)
    cross(fr, *C["HASTINGS"], r=12, width=5, color=WHITE); TL(fr, *C["HASTINGS"], "HASTINGS", dx=22, dy=-2, size=20, color=WHITE)
    PQ(fr, 1500, 150, "WILLIAM", a=fr.R(38.5, 0.3), size=30); PQ(fr, 1500, 216, "ROLLO'S GREAT-GREAT-GREAT-GRANDSON", a=fr.R(39.4, 0.4), size=18, light=True, pad=(12, 8))
    col(fr, 1318, 300, [("A VIKING BEATEN IN ENGLAND", 43.4), ("ENGLAND CONQUERED BY THE DESCENDANTS OF VIKINGS", 45.6), ("WHO NOW SPEAK FRENCH", 48.2)], size=16, gap=46)
    tline(fr, fr.R(41.7, 0.5), 0.9 + 0.1 * fr.R(42.2, 1.0), left="793", right="1066", title="THE VIKING AGE ENDS", ra=fr.R(42.4, 0.5))

# ================= 12c. VO 50.1-81.1: no horns; the DNA
@scene("12c_who_they_were", 12, 50.1, 81.2, EUR, dict(sc=U(NORWAY, SWEDEN, DENMARK)), res="50")
def _(fr, t):
    terr(fr, "sc", NOR)
    w1 = out(fr, 63.0)
    PQ(fr, 400, 130, "WHAT DID THEY LEAVE BEHIND?", a=fr.R(50.1, 0.3) * w1, size=24); PQ(fr, 400, 196, "NOT HORNED HELMETS", a=fr.R(51.7, 0.4) * w1, size=26, light=True)
    col(fr, 208, 270, [("A COSTUME DESIGNER", 53.4), ("FOR WAGNER'S OPERAS, 1876", 55.2), ("THE ONE ALMOST COMPLETE HELMET: NO HORNS", 58.2)], size=18, gap=48, dim=w1)
    x, y = P(fr.cam, *C["GJERMUNDBU"]); circ(fr, x, y, 9, WHITE, fr.R(58.4, 0.3) * w1); circ(fr, x, y, 6, INK, fr.R(58.4, 0.3) * w1)
    PQ(fr, 400, 130, "2020", a=fr.R(63.4, 0.4), size=36); PQ(fr, 400, 198, "THE DNA OF 442 PEOPLE", a=fr.R(64.6, 0.4), size=22, light=True, pad=(12, 8))
    rng = np.random.default_rng(21); G = [(-21.5, 64.3), (-45.5, 61), (-3, 59), (-6.5, 57.4), (-6.3, 53.3), (-1.1, 54), (-1.3, 51.7), (10.5, 59.5), (5.6, 59), (10.4, 63.4), (9.5, 56), (12.1, 55.6), (17.6, 59.4),
                                          (18.5, 57.5), (16.5, 56.6), (24.5, 58.6), (32.3, 60), (31.3, 58.5), (31.9, 54.8), (30.5, 50.45), (18.6, 54.4), (1.1, 49.4), (14.3, 37.6), (-7, 62), (23.5, 60.4)]
    for i in range(110):
        g = G[i % len(G)]; ll = (g[0] + rng.normal(0, 0.9), g[1] + rng.normal(0, 0.45)); x, y = P(fr.cam, *ll); a = fr.R(65.0 + 0.03 * i, 0.3)
        dark = (i * 7 % 10) < 6; local = (i % len(G)) in (2, 3) and i % 3 == 0
        c_ = mix((92, 62, 40), (226, 196, 110), fr.R(69.0, 0.8)) if dark else (226, 196, 110)
        circ(fr, x, y, 6.2, INK if not local else WHITE, a); circ(fr, x, y, 4.6, mix(FRK, c_, fr.R(71.6, 0.8)) if local else c_, a)
    PQ(fr, 400, 260, "MANY WERE NOT BLOND", a=fr.R(69.0, 0.4), size=20, light=True, pad=(12, 8))
    PQ(fr, 400, 330, "BURIED AS VIKINGS IN SCOTLAND:", a=fr.R(70.8, 0.4), size=18); PQ(fr, 400, 388, "LOCAL PEOPLE, NO SCANDINAVIAN ANCESTRY", a=fr.R(73.0, 0.4), size=17, light=True, pad=(12, 8))
    PQ(fr, 1500, 150, "VIKING WAS NEVER A BLOODLINE", a=fr.R(76.6, 0.4), size=22); PQ(fr, 1500, 214, "A WAY OF LIFE YOU COULD JOIN", a=fr.R(79.0, 0.4), size=22, light=True)

# ================= 12d. VO 81.1-97.8: what is still on the map
@scene("12d_still_on_the_map", 12, 81.1, 97.9, WORLD, dict(sc=U(NORWAY, SWEDEN, DENMARK), rus=RUSLAND, nm=NORMANDY, ice=ICELAND), res="50")
def _(fr, t):
    terr(fr, "sc", NOR)
    PQ(fr, 960, 110, "STILL ON THE MAP", a=fr.R(81.6, 0.4) * out(fr, 93.0), size=30)
    terr(fr, "rus", RUS, fr.R(83.6, 0.8)); PQL(fr, 36.5, 55.5, "THE NAME OF RUSSIA", dy=-10, a=fr.R(83.8, 0.4), size=20)
    terr(fr, "nm", NOR, fr.R(86.5, 0.5)); PQL(fr, 0.0, 49.0, "NORMANDY", dx=10, dy=56, a=fr.R(86.6, 0.4), size=20)
    x, y = P(fr.cam, *C["DUBLIN"]); a = fr.R(87.8, 0.4); circ(fr, x, y, 9, WHITE, a); circ(fr, x, y, 6.4, NOR, a); PQL(fr, *C["DUBLIN"], "THE CITY OF DUBLIN", dx=-150, dy=4, a=a, size=18)
    terr(fr, "ice", NOR, fr.R(89.6, 0.5)); PQL(fr, -18.5, 65.0, "ICELAND AND ITS PARLIAMENT", dy=-56, a=fr.R(89.7, 0.4), size=18)
    for i, wd in enumerate(("SKY", "EGG", "WINDOW", "THEY")): PQ(fr, 560 + [0, 110, 262, 422][i], 900, wd, a=fr.R(91.3 + 0.3 * i, 0.3), size=24, light=True)
    for i, (ll, nm, t0, bend, dx, dy) in enumerate(((C["BULGAR"], "THE VOLGA", 94.6, -0.12, 40, -70), (C["CONSTANTINOPLE"], "CONSTANTINOPLE", 95.4, -0.14, 30, 44), (C["LANSE"], "AMERICA", 96.3, 0.2, 0, 44))):
        gline(fr, arc((14 if i < 2 else 6, 60), ll, bend), width=5, frac=fr.R(t0 - 0.9, 1.4), arrow=True, halo=WHITE)
        PQL(fr, *ll, nm, dx=dx, dy=dy, a=fr.R(t0, 0.3), size=20, light=True, pad=(10, 7))

if __name__ == "__main__":
    import time
    mode = sys.argv[1]
    if mode == "list":
        tot = 0
        for n, sc in SC.items(): print(f"{n:24s} ch{sc.ch:02d}  VO {sc.t0:6.1f} - {sc.t0 + sc.dur:6.1f}  ({sc.dur:5.1f} s)"); tot += sc.dur
        print("total", round(tot, 1), len(SC))
    elif mode == "still":
        for spec in sys.argv[2:]:
            n, ts = spec.split("@"); sc = SC[n]; sc.frame(0.0)
            for tt in ts.split(","): sc.still(float(tt) - sc.t0, f"{HERE}/test_look/{n}_{float(tt):05.1f}.jpg", 0.75)
    elif mode == "sheet":
        names = [n for n in SC if any(n.startswith(p) for p in sys.argv[3:])] if len(sys.argv) > 3 else list(SC); ims = []
        for n in names:
            sc = SC[n]; sc.frame(0.0)
            for f in (0.5, 0.985):
                im = sc.frame(sc.dur * f).resize((960, 540), Image.LANCZOS); ImageDraw.Draw(im).rectangle([0, 0, 330, 22], fill=(17, 17, 17))
                ImageDraw.Draw(im).text((6, 5), f"{n}  ch{sc.ch} VO {sc.t0 + sc.dur * f:5.1f}", fill=(255, 255, 255)); ims.append(im)
            sc.masks = {}; sc._cam = None; sc.base = None; sc.rmask = None; sc.rm = None; sc.lm = None; sc.desert = None; sc._sc = None
        cols = 2; sh = Image.new("RGB", (cols * 960, ((len(ims) + cols - 1) // cols) * 540), (17, 17, 17))
        for i, im in enumerate(ims): sh.paste(im, (i % cols * 960, i // cols * 540))
        sh.save(f"{HERE}/test_look/sheet_{sys.argv[2]}.jpg", quality=86)
    else:
        os.makedirs(f"{HERE}/out_look", exist_ok=True)
        for n in sys.argv[2:]:
            t0 = time.time(); SC[n].render(f"{HERE}/out_look"); print(n, round(time.time() - t0, 1), flush=True)
