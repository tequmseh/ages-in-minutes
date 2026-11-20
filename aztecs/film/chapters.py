"""Aztecs: chapter specs built from ../layout.json (the only source of windows), ../maps.json (map clips), ../clips.json (clip entry points), ../timing.json.
On-screen words are the English part of each layout segment; every item is timed to the voice-over phrase it repeats (found automatically, WORDS overrides)."""
from gfxlib import *
from gfxlib import _load
from PIL import ImageFilter
import os, json, re
R = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(R); cx = W // 2
GR = dict(color=GRAY, bold=False)
LAY = json.load(open(f"{C}/layout.json")); MAPS = json.load(open(f"{C}/maps.json")); TIM = json.load(open(f"{C}/timing.json")); CLIPS = json.load(open(f"{C}/clips.json"))["clips"]
TAIL = 15.0          # quiet dark tail after the outro for the YouTube end screen (Rustam, 20 Nov)
def card(n): return [f"{C}/out/{f}" for f in sorted(os.listdir(f"{C}/out")) if f.startswith(f"aztecs_chapter_{n:02d}_")][0]

# ---------------------------------------------------------------- words on screen -> voice-over time
import unicodedata
def norm(s): s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode(); return re.sub(r"[^a-z0-9 ]+", " ", s.lower().replace("’", "'").replace("'", "")).split()
def _rows(n):
    out = []
    for r_ in TIM[str(n)]["rows"]:
        ws = [(m.start(), norm(m.group())) for m in re.finditer(r"\S+", r_["text"])]; L = max(1, len(r_["text"]))
        out += [(r_["start"] + (r_["end"] - r_["start"]) * p / L, w[0]) for p, w in ws if w]
    return out
ROWS = {n: _rows(n) for n in range(13)}
def at(n, phrase, d=0.0, lo=0.0, hi=1e9):
    ws = norm(phrase); rw = ROWS[n]
    for i in range(len(rw) - len(ws) + 1):
        if lo - 0.5 <= rw[i][0] <= hi and all(rw[i + k][1] == ws[k] for k in range(len(ws))): return rw[i][0] + d
    raise KeyError(phrase)
# on-screen item -> the spoken words it stands for (numbers and symbols are spoken differently)
WORDS = {"200,000 PEOPLE": "two hundred thousand", "4× LONDON": "four times", "EVERY 52 YEARS": "fifty-two years", "NOT WON BY 500 SPANIARDS": "five hundred Spaniards", "19TH CENTURY": "nineteenth century",
         "60,000?": "sixty thousand", "1 BEAN": "one bean", "1 TOMATO": "one tomato", "38 PROVINCES": "thirty-eight", "365": "three hundred and sixty-five", "260": "two hundred and sixty", "52": "fifty-two",
         "13 AUGUST 1521": "thirteenth of August", "500 SPANIARDS": "five hundred Spaniards", "80 DAYS": "eighty days", "UP TO 80%": "eighty per cent", "1.5 MILLION SPEAK NAHUATL": "one and a half million", "365 DAYS": "three hundred and sixty-five", "260 DAYS": "two hundred and sixty", "52 YEARS": "fifty-two years",
         "MAY 1520": "In May", "MALINTZIN": "~", "21 FEBRUARY 1978": "twenty-first of February", "MOCTEZUMA": "Moctezuma was", "THEIR HOSTAGE": "their hostage", "1502": "1502", "FIRST APPEARS 1552": "first appears", "2/5 TENOCHTITLAN": "two fifths", "2/5 TEXCOCO": "Texcoco", "1/5 TLACOPAN": "one fifth", "80,400": "eighty thousand", "QUETZALCOATL?": "Quetzalcoatl", "TOMATOES": "tomatoes", "CHILI": "chili", "AVOCADO": "avocados"}
def parse(txt):
    txt = re.sub(r"\([^)]*\)\.?", "", txt); tk = txt.split(" "); k = max([i for i, w in enumerate(tk) if re.search("[А-Яа-яЁё]", w)], default=-1)
    tk = [w for w in tk[k + 1:] if w]
    for j in (0, 1):          # a Latin tail of the Russian description ("Ур III.", "YBC 7289.")
        if j < len(tk) - 1 and tk[j].endswith(".") and not tk[j].endswith("…"): tk = tk[j + 1:]; break
    return [x.strip() for x in re.split(r" · | → | ↔ | ← ", " ".join(tk).strip()) if x.strip()]
def times(n, its, a, b, first_now=False):
    """voice-over second for every item: the phrase itself, a shorter start of it, one of its longer words; otherwise spaced evenly between its neighbours"""
    ts = []; cur = a - 0.4
    for s in its:
        t = None; ws = norm(WORDS.get(s, s)); cands = [ws[:k] for k in range(len(ws), 1, -1)] + [[w] for w in ws if len(w) >= 4 or s in WORDS]
        for c in cands:
            try: t = at(n, " ".join(c), -0.12, max(cur + 0.3, a - 0.4), b - 0.3); break
            except KeyError: pass
        ts.append(t); cur = t if t is not None else cur
    for i, t in enumerate(ts):
        if t is None:
            p = max([x for x in ts[:i] if x is not None], default=a); q = min([x for x in ts[i + 1:] if x is not None], default=b - 0.6); k = sum(1 for x in ts[i:] if x is None) if q == b - 0.6 else 1
            ts[i] = p + (q - p) / (k + 1) if i else a + 0.15
    ts = [min(max(t, a + 0.1), b - 0.5) for t in ts]
    if first_now and ts: ts[0] = a + 0.12
    if b - a > 2:          # a label must not wait dim for most of its window, and the last one must have time to be read
        if ts and ts[0] > a + 0.25 * (b - a): ts[0] = a + 0.15
        ts = [min(t, b - min(1.5, 0.3 * (b - a))) for t in ts]
    return ts

# ---------------------------------------------------------------- drawing
def wrap(s, maxc):
    if len(s) <= maxc: return [s]
    ws = s.split(" "); best = None
    for i in range(1, len(ws)):
        l1, l2 = " ".join(ws[:i]), " ".join(ws[i:])
        if best is None or abs(len(l1) - len(l2)) < abs(len(best[0]) - len(best[1])): best = (l1, l2)
    return list(best) if best else [s]
def tsize(s, wmax, top): return int(max(30, min(top, wmax / (max(1, len(s)) * 0.64))))
def column(d, t, x, its, ts, A, wmax, y0=None, big=100, ghost=0.0, align="m"):
    """one text block for every plate and insert: headline (fixed size, shrunk only if too wide), grey lines, the last line on a plaque; align "l" = left edge at x"""
    rows = []
    for i, s in enumerate(its):
        kind = "T" if i == 0 else ("P" if i == len(its) - 1 and len(its) >= 3 else "G")
        if len(its) == 2 and i == 1: kind = "P"
        top = big if kind == "T" else (round(big * 0.56) if kind == "P" else round(big * 0.46))
        ls = wrap(s, 30 if kind == "T" else 38) if len(s) > 26 else [s]; size = min(tsize(l, wmax, top) for l in ls)
        for l in ls: rows.append((kind, l, size, ts[i], size * (1.3 if kind == "T" else 2.3 if kind == "P" else 1.9)))
    tot = sum(r_[4] for r_ in rows); y = (y0 if y0 is not None else 540) - tot / 2
    for kind, l, size, t0, hh in rows:
        a = max(r(t, t0), ghost) * A; yy = y + hh / 2
        if kind == "T": text(d, x, yy, l, size, a, sp=max(2, size // 14), dy=18, anchor=align)
        elif kind == "P": plaque(d, x + (size * 0.45 if align == "l" else 0), yy, l, size, a, sp=max(2, size // 9), anchor=align)
        else: text(d, x, yy, l, size, a, sp=max(2, size // 9), anchor=align, **GR)
        y += hh
def fade(t, a, b): return min(1.0, max(0.0, (b - t) / 0.25))
def tscale(d, t, x0, x1, y, la, lb, t0, dur=1.6, A=1.0):
    k = ease((t - t0) / dur); d.line([(x0, y), (x1, y)], fill=col(DIM, A), width=3)
    if k > 0: d.rectangle([x0, y - 7, x0 + (x1 - x0) * k, y + 7], fill=col(ACC, A))
    text(d, x0, y + 50, la, 30, A, anchor="l", **GR); text(d, x1, y + 50, lb, 30, A * r(t, t0 + dur * 0.8), anchor="r", **GR)
def asp(name): o = _load(name); return o.width / o.height
def framed(im, name, x, y, h, a):
    o = _load(name); w = int(o.width * h / o.height)
    if a > 0: ImageDraw.Draw(im).rectangle([x - w / 2 - 6, y - h / 2 - 6, x + w / 2 + 6, y + h / 2 + 6], fill=col(WHITE, a))
    obj(im, name, x, y, h=h, a=a)

GHOST = 0.3          # a plate is never an empty screen: every line is there from the first frame, dim, and lights up when it is spoken
G = {}          # (chapter, window start) -> draw(im, d, t)
PITEMS = {"p4b": ["THE WINNERS EDIT THE PAST", "THE OLD PAINTED HISTORIES WERE BURNED", "A NEW STORY", "A CHOSEN PEOPLE"], "p11a": ["MAY 1520", "THE CITY RISES", "CORTÉS RETURNS", "MOCTEZUMA DIES"],
          "p12a": ["1545", "UP TO 80%", "UNTIL THE TWENTIETH CENTURY"], "p10a": ["QUETZALCOATL?", "FIRST APPEARS 1552", "INVENTED AFTER THE CONQUEST"]}          # long plates carry more of the spoken words than the layout line (never one line on black)
def T(n, ph, a, b, d=-0.12, dflt=None):
    try: return at(n, ph, d, a - 0.4, b)
    except KeyError:
        if dflt is None: raise
        return dflt
def mk_plate(n, a, b, i, txt):
    its = PITEMS.get(i, parse(txt)) if i not in ("p6a", "p8a") else []; ts = times(n, its, a, b, first_now=True)
    if i == "p4a": ts = [T(n, "Two fifths go", a, b), T(n, "two fifths to Texcoco", a, b), T(n, "one fifth", a, b)]
    def f(im, d, t):
        A = fade(t, a, b) * r(t, a, 0.25)
        if i == "p4a":          # the split of the tribute: a bar in fifths, three shares
            x0, x1, y = 260, 1660, 430; u = (x1 - x0) / 5; xs = [x0, x0 + 2 * u, x0 + 4 * u, x1]
            for k, sname in enumerate(its):
                fr, nm = sname.split(" ", 1); aa = max(r(t, ts[k]), GHOST) * A; c = (xs[k] + xs[k + 1]) / 2
                d.rectangle([xs[k] + 5, y - 46, xs[k + 1] - 5, y + 46], fill=col(WHITE if k < 2 else GRAY, aa))
                text(d, c, y + 150, fr, 120, aa, sp=4); text(d, c, y + 270, nm, 44 if k < 2 else 34, aa, sp=5, **GR)
        elif i == "p6a":          # what cacao beans buy
            rows = [("1", "TOMATO", "one bean buys"), ("3", "TURKEY EGG", "three buy"), ("100", "TURKEY HEN", "hundred buy")]
            text(d, cx, 200, "CACAO BEANS", 40, A, sp=10, **GR)
            for k, (num, what, ph) in enumerate(rows):
                aa = max(r(t, T(n, ph, a, b, dflt=a + 0.2 + k * 3)), GHOST) * A; y = 400 + k * 200
                text(d, 760, y, num, 150, aa, anchor="r", sp=4); text(d, 860, y, "→", 80, aa, anchor="l", color=GRAY); text(d, 1010, y, what, 84, aa, anchor="l", sp=6)
        elif i == "p7a":          # Nahuatl words, one size, lit as they are spoken
            for k, w_ in enumerate(its):
                text(d, cx, 220 + k * 160, w_, 120, max(r(t, ts[k]), GHOST) * A, sp=14)
        elif i == "p8a":          # two phases of one plate: the debt, then the disputed number
            m1 = T(n, "Second, the numbers", a, b) - 0.3
            if t < m1:
                A1 = A * min(1.0, max(0.0, (m1 - t) / 0.25))
                its1 = ["THE DEBT TO THE GODS", "PAID IN LIVES", "PRACTISED ACROSS ANCIENT MEXICO"]; ph = ["owed them a debt", "paid in lives", "practised across"]
                obj(im, "V01", 500, 540, h=800, a=A1); d = ImageDraw.Draw(im); column(d, t, TX, its1, [a + 0.12] + [T(n, p, a, b) for p in ph[1:]], A1, 800, big=76, ghost=GHOST, align="l")
            else:
                A2 = A * r(t, m1, 0.25); t1 = T(n, "1487", a, b); t2 = T(n, "eighty thousand four hundred", a, b); t3 = T(n, "four days", a, b); t4 = T(n, "inflated", a, b); t5 = T(n, "in the thousands", a, b)
                obj(im, "V13", 500, 540, w=860, a=A2); d = ImageDraw.Draw(im); X = 1420
                text(d, X, 200, "THE GREAT TEMPLE · 1487", 44, max(r(t, t1), GHOST) * A2, sp=8, **GR)
                text(d, X, 420, "80,400", 200, max(r(t, t2), GHOST) * A2, sp=10, dy=18); strike(d, X, 420, "80,400", 200, ease((t - t4) / 0.6), A2, sp=10, color=GRAY)
                text(d, X, 610, "PRISONERS IN FOUR DAYS", 46, max(r(t, t3), GHOST) * A2, sp=8, **GR)
                plaque(d, X, 820, "THOUSANDS", 90, max(r(t, t5), GHOST) * A2, sp=10)
        elif i == "p10b":          # the chain of translation
            xs = [330, 960, 1590]
            for k, w_ in enumerate(its):
                aa = max(r(t, ts[k]), GHOST) * A; text(d, xs[k], 500, w_, 88, aa, sp=6)
                if k: text(d, 655 if k == 1 else 1235, 500, "→", 70, aa, color=GRAY)
            for k, (nm, ph) in enumerate([("CORTÉS", "Cortes speaks"), ("AGUILAR", "Aguilar speaks"), ("MALINTZIN", "Malintzin speaks")]):
                text(d, xs[k], 640, nm, 40, max(r(t, T(n, ph, a, b, dflt=ts[k])), GHOST) * A, sp=8, **GR)
        else: column(d, t, cx, its, ts, A, 1650, big=100, ghost=GHOST)
    G[(n, a)] = f
def _has(n, ph, a, b):
    try: at(n, ph, lo=a, hi=b); return True
    except KeyError: return False
USE = {}
ITEMS = {(9, "V18"): ["1502", "THE SECOND MOCTEZUMA", "EIGHTEEN YEARS"], (10, "V20"): ["MALINTZIN", "SPEAKS BOTH MAYA AND NAHUATL", "THE SPANISH BAPTIZE HER MARINA"],
         (10, "V18"): ["MOCTEZUMA", "HE KEPT THEM CLOSE", "THEIR HOSTAGE"], (12, "V23"): ["21 FEBRUARY 1978", "COYOLXAUHQUI", "AT THE FOOT OF THE GREAT TEMPLE"],
         (7, "V17"): ["EAGLE WARRIORS", "JAGUAR WARRIORS", "BLADES OF OBSIDIAN"], (4, "V10"): ["TLACAELEL", "THE POWER BEHIND THE THRONE"], (6, "V13"): ["THE GREAT TEMPLE", "HUITZILOPOCHTLI", "TLALOC"],
         (12, "V22"): ["FLORENTINE CODEX", "1.5 MILLION SPEAK NAHUATL"], (8, "V01"): ["365 DAYS", "260 DAYS", "52 YEARS"]}          # on-screen words where the layout order differs from the spoken order
TX = 1010          # left edge of the text beside an object
PHOTO = ("V08", "V08.1", "V08.2", "V25")          # photographs shown full frame
FRAMED = ()          # rectangular pictures on a white mat
def mk_ins(n, a, b, i, txt):
    its = ITEMS.get((n, i), parse(txt)); ts = times(n, its, a, b); name = i; wide = asp(name) > 1.25; rect = _load(name).getextrema()[3][0] == 255
    def f(im, d, t):
        A = fade(t, a, b) * r(t, a, 0.3)
        if name in PHOTO:
            photo(im, name, A); d = ImageDraw.Draw(im); vis = [k for k in range(len(its)) if t >= ts[k]]
            if vis: plaque(d, cx, 960, its[vis[-1]], 34 if len(its[vis[-1]]) <= 40 else 30, r(t, ts[vis[-1]]) * A, sp=5)
        elif (n, i) == (8, "V01"):          # two calendars and their common cycle: three equal lines
            obj_(im, name, 500, 540, 800, A); d = ImageDraw.Draw(im)
            for k, w_ in enumerate(its): text(d, TX, 380 + k * 160, w_, 96, max(r(t, ts[k]), GHOST) * A, sp=7, color=WHITE, anchor="l")
        elif wide:
            obj_(im, name, cx, 420 if its else 540, min(680, int(1500 / asp(name))) if its else min(940, int(1700 / asp(name))), A); d = ImageDraw.Draw(im)
            if its: column(d, t, cx, its, ts, A, 1600, y0=930, big=60, ghost=GHOST)
        elif not its: obj_(im, name, cx, 540, 980, A)
        else:
            h = min(960, int(760 / asp(name)), int(_load(name).height * 1.45)); (framed if name in FRAMED else obj_)(im, name, 500, 540, h, A); d = ImageDraw.Draw(im); column(d, t, TX, its, ts, A, 800, big=76, ghost=GHOST, align="l")
    G[(n, a)] = f
_PAN = {}
def obj_(im, name, x, y, h, a): obj(im, name, x, y, h=h, a=a)
def mk_outro(n, a, b):
    def f(im, d, t):
        A = min(1.0, max(0.0, (b - t) / 1.2))
        text(d, cx, 300, "AGES", 150, A * r(t, a + 0.3), sp=14); text(d, cx, 440, "IN MINUTES", 70, A * r(t, a + 0.6), sp=22, color=ACC)
        text(d, cx, 620, "THAT WAS THE AZTECS IN TWENTY MINUTES", 36, A * r(t, at(12, "That was the Aztecs")), sp=4, **GR)
        plaque(d, cx, 780, "SUBSCRIBE", 60, A * r(t, at(12, "subscribe", -0.1)), sp=7); text(d, cx, 900, "WHICH CIVILIZATION SHOULD WE COVER NEXT?", 34, A * r(t, at(12, "which civilization")), sp=4, **GR)
    G[(n, a)] = f

# ---------------------------------------------------------------- captions on reconstruction clips, title
def cap(key, line, size=40, y=960, sp=3):
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); sz = 34 if len(line) <= 40 else 30; f = font(True, sz); px, py = sz * 0.45, sz * 0.32; w = tw(d, line, f, sp)
        d.rectangle([cx - w / 2 - px, y - sz * 0.6 - py, cx + w / 2 + px, y + sz * 0.6 + py], fill=WHITE + (255,)); xx = cx - w / 2
        for ch in line: d.text((xx, y - sz * 0.6), ch, font=f, fill=BG + (255,)); xx += d.textlength(ch, font=f) + sp
        p = f"{R}/tmp_panel_{key}.png"; im.save(p); return p
    return mk
def title_still():
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = Image.linear_gradient("L").resize((W, 520)); m = Image.new("L", (W, H), 0); m.paste(g.point(lambda v: int(v * 0.85)), (0, H - 520))
        im.paste(BG + (255,), (0, 0), m); d = ImageDraw.Draw(im); f = font(True, 150); s = "THE AZTECS"; w = tw(d, s, f, 10); x = cx - w / 2
        for ch in s: d.text((x, 730), ch, font=f, fill=WHITE + (255,)); x += d.textlength(ch, font=f) + 10
        f2 = font(True, 56); s2 = "IN 20 MINUTES"; w = tw(d, s2, f2, 16); x = cx - w / 2
        for ch in s2: d.text((x, 920), ch, font=f2, fill=ACC + (255,)); x += d.textlength(ch, font=f2) + 16
        p = f"{R}/tmp_panel_title.png"; im.save(p); return p
    return mk
def clip_caps(n, a, b, txt, k):
    its = parse(txt)
    if n == 0 and a > 44: its = [x for x in its if x not in ("THE AZTECS", "IT TAKES TWENTY MINUTES")]
    ts = times(n, its, a, b); out = []
    for j, s in enumerate(its):
        t1 = ts[j + 1] - 0.05 if j + 1 < len(its) else b - 0.15
        if t1 - ts[j] > 0.6: out.append((cap(f"c{n:02d}_{k}_{j}", s), ts[j], t1))
    return out

# ---------------------------------------------------------------- spec
def clip_use(nm, n, a):
    u = [x for x in CLIPS[nm]["uses"] if x["ch"] == n and abs(x["t0"] - a) < 0.05][0]; return f"{C}/clips/{nm}.mp4", u["in"], u.get("speed", 1.0)
def map_clip(n, i, a):
    for nm, m in MAPS.items():
        if m["ch"] == n and m["id"] == i and m["t0"] - 0.01 <= a < m["t1"]: return f"{C}/maps/out_look/{nm}.mp4", a - m["t0"]
    raise KeyError((n, i, a))
def spec(n):
    segs = LAY[str(n)]["segs"]; ov = []; wins = []; stills = []
    for k, (a, b, kind, i, txt) in enumerate(segs):
        if kind == "MAP": f, ss = map_clip(n, i, a); ov.append((f, a, b, False, ss, 1.0))
        elif kind == "CLIP": f, ss, sp = clip_use(i, n, a); ov.append((f, a, b, True, ss, sp)); stills += clip_caps(n, a, b, txt, k)
        else:
            if (n, a) not in G: (mk_outro(n, a, b) if kind == "CARD" else mk_plate(n, a, b, i, txt) if kind == "PLATE" else mk_ins(n, a, b, i, txt))
            wins.append((a, b))
    if n == 0: stills.append((title_still(), at(0, "So who were", 0.3), segs[-1][1]))
    def gfx(t):
        im, d = blank()
        for a, b in wins:
            if a <= t < b: G[(n, a)](im, d, t)
        return im
    import glob as _g; mus = (_g.glob(f"{C}/music/{n:02d}.*") + [""])[0]
    return dict(n=n, gfx=gfx, gfx_windows=wins, overlays=ov, stills=stills, card=card(n) if n else None, fade_out=1.2 if n == 12 else 0.5, dur=(LAY["12"]["dur"] + TAIL) if n == 12 else 0,
                music=(mus, None, -27.0 if n == 0 else None) if os.path.exists(mus) else None)
class _S(dict):
    def __missing__(s, k):
        USE.clear()
        for m in range(k): [USE.__setitem__(x[3], USE.get(x[3], 0) + 1) for x in LAY[str(m)]["segs"] if x[2] == "INS"]          # which showing of an insert this is
        s[k] = spec(k); return s[k]
SPECS = _S()
if __name__ == "__main__":      # check: everything is found; sheets of plates and inserts, two moments each
    os.makedirs("/tmp/chk", exist_ok=True); ims = []
    for n in range(13):
        s = SPECS[n]; print(n, len(s["overlays"]), "clips+maps", len(s["stills"]), "captions", len(s["gfx_windows"]), "plates/inserts", [o[0] for o in s["overlays"] if not os.path.exists(o[0])])
        for a, b in s["gfx_windows"]:
            for q in (0.5, 0.96):
                t = a + (b - a) * q - (0.3 if q > 0.9 else 0); im = s["gfx"](t).resize((480, 270)); ImageDraw.Draw(im).text((4, 3), f"ch{n} {t:.1f}", fill=(255, 255, 0)); ims.append(im)
    for k in range(0, len(ims), 48):
        part = ims[k:k + 48]; S = Image.new("RGB", (8 * 480, ((len(part) + 7) // 8) * 270))
        for j, im in enumerate(part): S.paste(im, (j % 8 * 480, j // 8 * 270))
        S.save(f"/tmp/chk/plates_{k // 48}.jpg", quality=85)
