"""Mesopotamia: chapter specs built from ../layout.json (the only source of windows), ../maps.json (map clips), ../clips.json (clip entry points), ../timing.json.
On-screen words are the English part of each layout segment; every item is timed to the voice-over phrase it repeats (found automatically, WORDS overrides)."""
from gfxlib import *
from gfxlib import _load
from PIL import ImageFilter
import os, json, re
R = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(R); cx = W // 2
GR = dict(color=GRAY, bold=False)
LAY = json.load(open(f"{C}/layout.json")); MAPS = json.load(open(f"{C}/maps.json")); TIM = json.load(open(f"{C}/timing.json")); CLIPS = json.load(open(f"{C}/clips.json"))["clips"]
TAIL = 17.6          # black tail after the outro, s: the film must not be shorter than 20:00
def card(n): return [f"{C}/out/{f}" for f in sorted(os.listdir(f"{C}/out")) if f.startswith(f"mesopotamia_chapter_{n:02d}_")][0]

# ---------------------------------------------------------------- words on screen -> voice-over time
def norm(s): return re.sub(r"[^a-z0-9 ]+", " ", s.lower().replace("’", "'").replace("'", "")).split()
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
WORDS = {"60 SECONDS": "sixty seconds", "60 MINUTES": "sixty minutes", "4,000 YEARS AGO": "four thousand", "69,000 GUESTS": "sixty-nine thousand", "69,574 GUESTS": "sixty-nine thousand", "3100 BC": "3100", "50,000 PEOPLE": "fifty thousand",
         "3,000 YEARS": "three thousand", "29,086": "twenty-nine thousand", "37 MONTHS": "thirty-seven", "2450 BC": "2450", "2200 BC": "2200", "2112 BC": "2112", "300 YEARS BEFORE HAMMURABI": "three hundred years", "48 YEARS": "forty-eight",
         "1792 BC": "1792", "2 METRES": "two metres", "282 LAWS": "282", "1750 BC": "1750", "360°": "360", "10,000 JARS OF BEER": "ten thousand jars", "10,000 SKINS OF WINE": "ten thousand skins", "668 BC": "668", "30,000+ TABLETS": "thirty thousand",
         "1872": "1872", "AD 79": "79", "APRIL 2003": "April 2003", "15,000 OBJECTS": "fifteen thousand", "5,000 YEARS": "five thousand", "2,000 YEARS": "two thousand", "1,000+ YEARS LATER": "thousand years", "A TOOTH = 2 SHEKELS OF SILVER": "tooth",
         "√2 = 1.414213": "square root", "91 M × 91 M × 91 M": "ninety-one", "1 MINA OF SILVER": "one mina", "40 MINAS": "forty minas", "NOT EVEN 10": "not even ten", "3300 BC": "3300", "TABLET XI": "tablet eleven", "THE 1850s": "1850s",
         "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "10": "ten", "12": "twelve", "15": "fifteen", "20": "twenty", "30": "thirty", "60": "sixty"}
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
def column(d, t, x, its, ts, A, wmax, y0=None, big=150, ghost=0.0):
    """a centred column: first item large, last on a plaque, the rest grey; returns nothing"""
    rows = []
    for i, s in enumerate(its):
        kind = "T" if i == 0 else ("P" if i == len(its) - 1 and len(its) >= 3 else "G")
        if len(its) == 2 and i == 1: kind = "P"
        top = big if kind == "T" else (60 if kind == "P" else 46)
        if kind == "T" and len(its) == 1: top = big
        ls = wrap(s, 30 if kind == "T" else 38) if len(s) > 26 else [s]; size = min(tsize(l, wmax, top) for l in ls)
        for l in ls: rows.append((kind, l, size, ts[i], size * (1.3 if kind == "T" else 2.3 if kind == "P" else 1.9)))
    tot = sum(r_[4] for r_ in rows); y = (y0 if y0 is not None else 540) - tot / 2
    for kind, l, size, t0, hh in rows:
        a = max(r(t, t0), ghost) * A; yy = y + hh / 2
        if kind == "T": text(d, x, yy, l, size, a, sp=max(2, size // 14), dy=18)
        elif kind == "P": plaque(d, x, yy, l, size, a, sp=max(2, size // 9))
        else: text(d, x, yy, l, size, a, sp=max(2, size // 9), **GR)
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

PLATE_OBJ = {"p3b": "V32"}          # a plate with an object beside the words
GHOST = 0.3          # a plate is never an empty screen: every line is there from the first frame, dim, and lights up when it is spoken
G = {}          # (chapter, window start) -> draw(im, d, t)
def mk_plate(n, a, b, i, txt):
    its = parse(txt); ts = times(n, its, a, b, first_now=True)
    def f(im, d, t):
        A = fade(t, a, b) * r(t, a, 0.25)
        if i == "p7a":          # sixty and what divides it
            text(d, cx, 300, its[0], 260, A, sp=10, dy=18)
            for k, s in enumerate(its[1:]): text(d, 330 + k * 140, 720, s, 90, max(r(t, ts[k + 1]), GHOST) * A, color=WHITE if k % 2 == 0 else GRAY)
        elif i == "p1c":          # eighteen temples, one on top of another
            step = (b - a - 3.0) / 18          # all eighteen layers are on screen from the first frame, they light up one by one through the window
            for k in range(18):
                aa = max(r(t, a + 0.5 + k * step, 0.4), GHOST) * A; y = 860 - k * 34; w = 760 - k * 22
                if aa > 0: d.rectangle([cx - w / 2, y - 12, cx + w / 2, y + 12], fill=col(GRAY if k < 17 else WHITE, aa))
            plaque(d, cx, 960, its[-1], 54, A, sp=6)
        elif i in ("p7c", "p11c", "p12b"):
            la, lb = {"p7c": ("1800 BC", "PYTHAGORAS"), "p11c": ("NARAM-SIN ~2250 BC", "NABONIDUS ~550 BC"), "p12b": ("3300 BC · URUK", "AD 79 · URUK")}[i]
            tscale(d, t, 360, 1560, 470, la, lb, a + 0.3, min(3.0, (b - a) * 0.5), A)
            rest = {"p7c": its[2:], "p11c": its[2:], "p12b": []}[i]; rt = ts[len(its) - len(rest):]
            if rest: column(d, t, cx, rest, rt, A, 1500, y0=760, big=70, ghost=GHOST)
        elif i in PLATE_OBJ: obj(im, PLATE_OBJ[i], 560, 540, h=1000, a=A); d = ImageDraw.Draw(im); column(d, t, 1300, its, ts, A, 900, ghost=GHOST)
        else: column(d, t, cx, its, ts, A, 1650, ghost=GHOST)
    G[(n, a)] = f
def _has(n, ph, a, b):
    try: at(n, ph, lo=a, hi=b); return True
    except KeyError: return False
USE = {}
def mk_ins(n, a, b, i, txt):
    its = parse(txt); ts = times(n, its, a, b); k = USE[i] = USE.get(i, 0) + 1
    name = {"V05": "V05a"}.get(i, i); top = (i == "V05" and k == 2)          # second showing of the stele: its upper part, the phalanx
    wide = asp(name) > 1.25; photo_ = name in ("V09", "V26", "V31", "V29")
    def f(im, d, t):
        A = fade(t, a, b) * r(t, a, 0.3)
        if photo_ and name != "V29":
            photo(im, name, A); d = ImageDraw.Draw(im); vis = [k for k in range(len(its)) if t >= ts[k]]
            if vis: plaque(d, cx, 970, its[vis[-1]], 44 if len(its[vis[-1]]) < 30 else 34, r(t, ts[vis[-1]]) * A, sp=5)
        elif top: obj(im, name, cx, 400, h=660, a=A, crop=(0.0, 0.0, 1.0, 0.44)); d = ImageDraw.Draw(im); column(d, t, cx, its, ts, A, 1600, y0=900, big=64)
        elif i == "V13" and n == 6 and k == 1:          # the top of the stele: the king before Shamash
            obj(im, name, 560, 540, h=940, a=A, crop=(0.0, 0.0, 1.0, 0.27)); d = ImageDraw.Draw(im); column(d, t, 1340, its, ts, A, 800)
        elif i == "V13" and n == 6:          # the whole stele, passing from top to bottom
            o = _load(name); w = 640; hh = int(o.height * w / o.width); q = ease((t - a - 0.8) / (b - a - 2.2)) if b - a > 3 else 0
            key = ("pan", w)
            if key not in _PAN: _PAN[key] = o.resize((w, hh), Image.LANCZOS)
            oo = _PAN[key]; y = int(60 - q * (hh - 960)); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); lay.paste(oo, (560 - w // 2, y), oo)
            if A < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * A)))
            im.paste(lay, (0, 0), lay); d = ImageDraw.Draw(im); column(d, t, 1340, its, ts, A, 800)
        elif wide:
            (framed if name in ("V29",) else obj_)(im, name, cx, 400 if its else 540, min(600, int(1400 / asp(name))) if its else min(900, int(1700 / asp(name))), A); d = ImageDraw.Draw(im)
            if its: column(d, t, cx, its, ts, A, 1600, y0=880, big=64)
        elif not its: obj(im, name, cx, 540, h=980, a=A)
        else:
            h = min(940, int(720 / asp(name)), int(_load(name).height * 1.45)); (framed if name in ("V27",) else obj_)(im, name, 540, 540, h, A); d = ImageDraw.Draw(im); column(d, t, 1340, its, ts, A, 800, big=110)
    G[(n, a)] = f
_PAN = {}
def obj_(im, name, x, y, h, a): obj(im, name, x, y, h=h, a=a)
def mk_outro(n, a, b):
    def f(im, d, t):
        A = min(1.0, max(0.0, (b - t) / 1.2))
        text(d, cx, 300, "AGES", 150, A * r(t, a + 0.3), sp=14); text(d, cx, 440, "IN MINUTES", 70, A * r(t, a + 0.6), sp=22, color=ACC)
        text(d, cx, 620, "THAT WAS MESOPOTAMIA IN TWENTY MINUTES", 36, A * r(t, at(12, "That was Mesopotamia")), sp=4, **GR)
        plaque(d, cx, 780, "SUBSCRIBE", 60, A * r(t, at(12, "subscribe", -0.1)), sp=7); text(d, cx, 900, "WHICH CIVILIZATION SHOULD WE COVER NEXT?", 34, A * r(t, at(12, "which civilization")), sp=4, **GR)
    G[(n, a)] = f

# ---------------------------------------------------------------- captions on reconstruction clips, title
def cap(key, line, size=40, y=960, sp=3):
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); sz = size if len(line) <= 40 else 34; f = font(True, sz); px, py = sz * 0.45, sz * 0.32; w = tw(d, line, f, sp)
        d.rectangle([cx - w / 2 - px, y - sz * 0.6 - py, cx + w / 2 + px, y + sz * 0.6 + py], fill=WHITE + (255,)); xx = cx - w / 2
        for ch in line: d.text((xx, y - sz * 0.6), ch, font=f, fill=BG + (255,)); xx += d.textlength(ch, font=f) + sp
        p = f"{R}/tmp_panel_{key}.png"; im.save(p); return p
    return mk
def title_still():
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = Image.linear_gradient("L").resize((W, 520)); m = Image.new("L", (W, H), 0); m.paste(g.point(lambda v: int(v * 0.85)), (0, H - 520))
        im.paste(BG + (255,), (0, 0), m); d = ImageDraw.Draw(im); f = font(True, 150); s = "MESOPOTAMIA"; w = tw(d, s, f, 10); x = cx - w / 2
        for ch in s: d.text((x, 730), ch, font=f, fill=WHITE + (255,)); x += d.textlength(ch, font=f) + 10
        f2 = font(True, 56); s2 = "IN 20 MINUTES"; w = tw(d, s2, f2, 16); x = cx - w / 2
        for ch in s2: d.text((x, 920), ch, font=f2, fill=ACC + (255,)); x += d.textlength(ch, font=f2) + 16
        p = f"{R}/tmp_panel_title.png"; im.save(p); return p
    return mk
def clip_caps(n, a, b, txt, k):
    its = parse(txt)
    if n == 0 and a > 37: its = [x for x in its if x not in ("MESOPOTAMIA", "IT TAKES TWENTY MINUTES")]
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
    if n == 0: stills.append((title_still(), at(0, "It takes twenty", -0.3), segs[-1][1]))
    def gfx(t):
        im, d = blank()
        for a, b in wins:
            if a <= t < b: G[(n, a)](im, d, t)
        return im
    mus = f"{C}/music/{n:02d}.wav"
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
