"""Rome: chapter specs built from ../layout.json (windows), ../clips.json (clip entry points), ../layout_inserts.json and the map scene list.
All seconds are voice-over seconds of the chapter. Plaque text repeats the voice-over wording."""
from gfxlib import *
from gfxlib import _load
from PIL import ImageFilter, ImageFont
import os, json, subprocess, math
R = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(R); cx = W // 2
GR = dict(color=GRAY, bold=False)
LAY = json.load(open(f"{C}/layout.json")); CLIPS = json.load(open(f"{C}/clips.json"))["clips"]; INS = json.load(open(f"{C}/layout_inserts.json"))["inserts"]; TIM = json.load(open(f"{C}/timing.json"))
def card(n): return [f"{C}/out/{f}" for f in sorted(os.listdir(f"{C}/out")) if f.startswith(f"rome_chapter_{n:02d}_")][0]
def scenes():
    p = f"{R}/scenes.json"
    if not os.path.exists(p) or os.path.getmtime(p) < os.path.getmtime(f"{C}/maps/ro_scenes.py"):
        o = subprocess.run(["python3", f"{C}/maps/ro_scenes.py", "list"], capture_output=True, text=True).stdout
        json.dump({l.split()[0].split("_")[0]: [l.split()[0], float(l.split()[3])] for l in o.splitlines() if l and not l.startswith("total")}, open(p, "w"), indent=0)
    return json.load(open(p))
SCN = scenes()
def at(n, phrase, d=0.0):
    """voice-over second at which a phrase starts (linear inside its sentence)"""
    for r_ in TIM[str(n)]["rows"]:
        i = r_["text"].lower().find(phrase.lower())
        if i >= 0: return r_["start"] + (r_["end"] - r_["start"]) * i / max(1, len(r_["text"])) + d
    raise KeyError(phrase)
def clip_file(nm, n, t0):
    """entry point and speed of a clip showing; a clip made of parts is pre-cut once into rec/"""
    u = [x for x in CLIPS[nm]["uses"] if x["ch"] == n and abs(x["t0"] - t0) < 0.05][0]; src = f"{C}/clips/{nm}.mp4"
    if "parts" not in u: return src, u["in"], u["speed"]
    out = f"{R}/rec/{nm}_ch{n:02d}.mp4"
    if not os.path.exists(out):
        k = len(u["parts"]); fc = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];" for i, (a, b) in enumerate(u["parts"]))
        fc += "".join(f"[v{i}][a{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=1[v][a]"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-c:a", "aac", "-b:a", "192k", out], check=True)
    return out, 0.0, u["speed"]

def panel(key, items):
    """inset over a map: cut-outs or photographs lie directly on the map with a soft shadow; frame=True puts a thin light border round a photograph. items = [(name, cx, cy, h, frame)]"""
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for n, px, py, h, fr in items:
            o = _load(n); o = o.resize((max(2, int(o.width * h / o.height)), h), Image.LANCZOS)
            if fr:
                b = Image.new("RGBA", (o.width + 12, o.height + 12), WHITE + (255,)); b.paste(o, (6, 6)); o = b
            pos = (int(px - o.width / 2), int(py - o.height / 2))
            sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); a = Image.new("L", (W, H), 0); a.paste(o.getchannel("A").point(lambda v: int(v * 0.5)), (pos[0] + 6, pos[1] + 10))
            sh.putalpha(a.filter(ImageFilter.GaussianBlur(12))); im.alpha_composite(sh); im.alpha_composite(o, pos)
        p = f"{R}/tmp_panel_{key}.png"; im.save(p); return p
    return mk
def cap(key, lines, size=40, y=960, sp=3):
    """white plaques as a transparent still, for captions on top of a reconstruction clip; lines stack upwards from y"""
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = font(True, size); px, py = size * 0.45, size * 0.32
        for k, txt in enumerate(lines):
            yy = y - (len(lines) - 1 - k) * size * 1.95; w = tw(d, txt, f, sp)
            d.rectangle([cx - w / 2 - px, yy - size * 0.6 - py, cx + w / 2 + px, yy + size * 0.6 + py], fill=WHITE + (255,)); xx = cx - w / 2
            for ch in txt: d.text((xx, yy - size * 0.6), ch, font=f, fill=BG + (255,)); xx += d.textlength(ch, font=f) + sp
        p = f"{R}/tmp_panel_{key}.png"; im.save(p); return p
    return mk
def box(d, x0, y0, x1, y1, a=1.0, width=3, color=WHITE):
    if a > 0: d.rectangle([x0, y0, x1, y1], outline=col(color, a), width=width)
def line(d, pts, a=1.0, width=3, color=WHITE):
    if a > 0: d.line(pts, fill=col(color, a), width=width)

# ================================================================= plates and inserts: each function draws one segment, t = chapter seconds
G = {}
def seg(i):
    def deco(f): G[i] = f; return f
    return deco

# ---------------- chapter 2
@seg("p2a")
def _(im, d, t):
    o = 1 - r(t, at(2, "The Romans call it", -0.3), 0.4)          # the scheme gives way to the word
    for k, (x, name, sub, t0, t1) in enumerate(((430, "TWO CONSULS", "ELECTED EVERY YEAR", 9.4, 9.4), (960, "SENATE", "THE REAL POWER", 9.6, at(2, "the real power")),
                                                (1490, "ASSEMBLIES", "VOTE ON LAWS · ELECT THE OFFICIALS", at(2, "Assemblies"), at(2, "vote on laws")))):
        a = r(t, t0) * o; box(d, x - 235, 400, x + 235, 560, a); text(d, x, 480, name, 44, a, sp=4); text(d, x, 630, sub, 26 if len(sub) > 24 else 30, r(t, t1) * o, sp=2, **GR)
    a = r(t, at(2, "Assemblies", 0.3)) * o; line(d, [(665, 480), (725, 480)], a); line(d, [(1195, 480), (1255, 480)], a)
    b = r(t, at(2, "res publica", -0.1)); text(d, cx, 440, "RES PUBLICA", 150, b, sp=10, dy=30); text(d, cx, 610, "THE PUBLIC THING", 40, r(t, at(2, "the public thing")), sp=8, **GR)
    plaque(d, cx, 800, "REPUBLIC", 54, r(t, at(2, "republic comes from", -0.2)), sp=8)
@seg("V02")
def _(im, d, t):
    obj(im, "V02_arch_titus", cx, 540, h=1060, a=win(t, 24.0, 27.7, 0.3, 0.3)); d = ImageDraw.Draw(im)
    plaque(d, cx, 900, "SPQR", 64, r(t, at(2, "SPQR", -0.1)), sp=10); plaque(d, cx, 990, "THE SENATE AND THE PEOPLE OF ROME", 34, r(t, at(2, "the Senate and the People")), sp=4)
@seg("p2b")
def _(im, d, t):
    text(d, cx, 170, "THE PEOPLE ARE NOT EQUAL", 46, r(t, at(2, "But the people")), sp=6)
    a = r(t, at(2, "A small group")); b = r(t, at(2, "Everyone else", -0.2))
    for i in range(8): d.ellipse([368 + (i % 4) * 64 - 16, 420 + (i // 4) * 64 - 16, 368 + (i % 4) * 64 + 16, 420 + (i // 4) * 64 + 16], fill=col(WHITE, a))
    for i in range(160):
        x = 860 + (i % 20) * 44; y = 330 + (i // 20) * 44; k = min(1.0, max(0.0, b * 1.6 - i / 260)); d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=col(GRAY, k))
    text(d, 464, 580, "PATRICIANS", 44, r(t, at(2, "the patricians")), sp=4); text(d, 464, 650, "HOLD THE OFFICES", 30, r(t, at(2, "holds the offices")), sp=4, **GR)
    text(d, 1278, 740, "PLEBEIANS", 44, r(t, at(2, "a plebeian", -0.3)), sp=4); text(d, 1278, 810, "EVERYONE ELSE", 30, r(t, at(2, "Everyone else")), sp=4, **GR)
@seg("p2c")
def _(im, d, t):
    text(d, cx, 190, "AROUND 450 BC", 54, r(t, at(2, "Around 450 BC")), sp=8)
    t0 = at(2, "written down")
    for i in range(12):
        a = r(t, t0 + i * 0.16, 0.3); x = 330 + (i % 6) * 212; y = 330 + (i // 6) * 250; box(d, x, y, x + 150, y + 200, a, width=3)
        for k in range(6): line(d, [(x + 22, y + 34 + k * 26), (x + 128 - (k * 37 + i * 13) % 40, y + 34 + k * 26)], a * 0.5, width=3, color=GRAY)
    plaque(d, cx, 870, "TWELVE TABLETS", 50, r(t, at(2, "twelve tablets")), sp=6)
    text(d, cx, 970, "EVERYONE CAN READ WHAT THE RULES ARE", 34, r(t, at(2, "so everyone can read")), sp=5, **GR)
# ================================================================= generic plates: items = (kind, x, y, text, size, t0[, t1]); kind T white, G grey, P plaque, Y accent
SEG = {s[3]: (int(n), s[0], s[1]) for n, v in LAY.items() if n.isdigit() for s in v["segs"] if s[2] in ("PLATE", "INS", "CARD")}
def items(d, t, its, A=1.0):
    for it in its:
        k, x, y, s, size, t0 = it[:6]; a = r(t, t0) * A * ((1 - r(t, it[6], 0.3)) if len(it) > 6 else 1)
        if k == "P": plaque(d, x, y, s, size, a, sp=max(2, size // 9))
        elif k == "G": text(d, x, y, s, int(size * 1.15), a, sp=max(2, size // 8), **GR)
        elif k == "Y": text(d, x, y, s, size, a, sp=max(2, size // 12), color=ACC)
        else: text(d, x, y, s, size, a, sp=max(2, size // 14), dy=18)
def plate(i, *its, extra=None, pre=None):
    n, a, b = SEG[i]
    def f(im, d, t):
        A = min(1.0, max(0.0, (b - t) / 0.25))
        if pre: pre(im, d, t, A); d = ImageDraw.Draw(im)
        items(d, t, its, A)
        if extra: extra(im, d, t, A)
    G[i] = f
def O(name, x, y, h, t0=None, t1=None):
    def f(im, d, t, A):
        a = A * (r(t, t0, 0.4) if t0 is not None else 1) * ((1 - r(t, t1, 0.4)) if t1 is not None else 1); obj(im, name, x, y, h=h, a=a)
    return f
def PH(name):
    def f(im, d, t, A): photo(im, name, A)
    return f
def both(*fs):
    def f(im, d, t, A):
        for g in fs: g(im, d, t, A)
    return f
def arrow_r(d, x0, x1, y, a=1.0, color=WHITE, width=4):
    if a > 0: line(d, [(x0, y), (x1, y)], a, width, color); d.polygon([(x1, y - 12), (x1 + 22, y), (x1, y + 12)], fill=col(color, a))
def tscale(d, t, x0, x1, y, la, lb, t0, dur=1.6, A=1.0):
    """time scale: grey line, accent bar growing from la to lb"""
    k = ease((t - t0) / dur); line(d, [(x0, y), (x1, y)], A, 3, DIM)
    if k > 0: d.rectangle([x0, y - 7, x0 + (x1 - x0) * k, y + 7], fill=col(ACC, A))
    text(d, x0, y + 50, la, 30, A, anchor="l", **GR); text(d, x1, y + 50, lb, 30, A * r(t, t0 + dur * 0.8), anchor="r", **GR)

# ---------------- chapter 1
plate("p2d", ("G", cx, 250, "A RANSOM IN GOLD", 40, at(2, "a ransom in gold")), ("T", cx, 500, "VAE VICTIS", 220, at(2, "vae victis", -0.15)), ("P", cx, 760, "WOE TO THE DEFEATED", 60, at(2, "Woe to the defeated", -0.1)))
plate("V01", ("P", cx, 905, "ROMULUS AND REMUS", 44, at(1, "twin brother Remus", -0.2)), ("G", cx, 990, "NURSED BY A SHE-WOLF", 30, at(1, "nursed by"), at(1, "The brothers quarrelled")),
      ("G", cx, 990, "ROMULUS KILLED REMUS", 30, at(1, "Romulus killed")), pre=O("V01_wolf", cx, 450, 640, 21.0))
plate("p1a", ("T", cx, 400, "509 BC", 220, at(1, "509 BC", -0.2)), ("P", cx, 640, "TARQUIN THE PROUD", 54, at(1, "Tarquin")), ("G", cx, 760, "THEY WOULD NEVER HAVE ANOTHER", 32, at(1, "never have another", -0.3)))
plate("p1b", ("T", cx, 330, "FIVE HUNDRED YEARS", 96, at(1, "five hundred years", -0.2)), ("P", cx, 760, "THE WORD KING WAS AN INSULT", 44, at(1, "the word king")), ("G", cx, 900, "REMEMBER THAT", 34, at(1, "Remember that")),
      extra=lambda im, d, t, A: tscale(d, t, 360, 1560, 520, "509 BC", "", at(1, "For the next"), 3.2, A))
# ---------------- chapter 3
plate("V05", ("G", 1250, 380, "WON ALMOST EVERY BATTLE", 36, at(3, "won almost")), ("G", 1250, 460, "LOST THE WAR", 36, at(3, "lost the war")), ("P", 1250, 640, "A PYRRHIC VICTORY", 60, at(3, "a Pyrrhic", -0.2)), pre=O("V05_pyrrhus", 540, 560, 880))
# ---------------- chapter 4
plate("p4a", ("G", cx, 160, "SO IT BUILDS ONE", 34, 18.6, at(4, "the raven", -0.3)), ("P", cx, 300, "THE RAVEN", 80, at(4, "the raven", -0.2)), ("G", cx, 450, "A BOARDING BRIDGE WITH A SPIKE", 34, at(4, "a boarding bridge")), ("T", cx, 680, "A SEA BATTLE", 84, at(4, "A sea battle", -0.1)),
      ("T", cx, 800, "BECOMES A LAND BATTLE", 84, at(4, "becomes a land battle", -0.1)))
plate("V30", ("P", 1330, 330, "CATO", 60, at(4, "Cato is still", -0.2)), ("T", 1330, 540, "CARTHAGE", 76, at(4, "Carthage must be destroyed", -0.2)), ("T", 1330, 640, "MUST BE DESTROYED", 76, at(4, "Carthage must be destroyed", 0.3)),
      ("G", 1330, 800, "WHATEVER THE SUBJECT", 32, at(4, "whatever the subject")), pre=O("V30_cato", 520, 560, 900))
# ---------------- chapter 5
def _estates(im, d, t, A):
    k = ease((t - at(5, "huge estates")) / 1.6)
    for i in range(40):
        x = 420 + (i % 10) * 110; y = 380 + (i // 10) * 110; gone = (i % 10) < 7 * k + 0.01 and k > 0
        d.rectangle([x, y, x + 84, y + 84], outline=col(GRAY, A * (0.25 if gone else 1)), width=3)
    if k > 0: d.rectangle([408, 368, 408 + (7 * 110 + 0) * k + 12 * k, 368 + 4 * 110 - 2], outline=col(WHITE, A), width=6)
plate("p5a", ("T", cx, 220, "HUGE ESTATES", 80, at(5, "huge estates", -0.1)), ("G", cx, 920, "WORKED WITH SLAVES", 36, at(5, "work them with slaves")), extra=_estates)
plate("p5b", ("T", cx, 380, "133 BC", 200, at(5, "In 133 BC")), ("P", cx, 620, "TIBERIUS GRACCHUS", 54, at(5, "Tiberius Gracchus", -0.2)), ("G", cx, 750, "PUBLIC LAND TO THE POOR", 36, at(5, "public land")))
def _army(im, d, t, A):
    a = A * r(t, at(5, "These men expect"))
    box(d, 760, 470, 1080, 580, a); text(d, 920, 525, "SOLDIERS", 36, a, sp=4)
    b = A * r(t, at(5, "their general")); arrow_r(d, 1090, 1230, 480, b); box(d, 1262, 410, 1700, 520, b); text(d, 1481, 465, "THEIR GENERAL", 36, b, sp=4)
    c = A * r(t, at(5, "not the state")); arrow_r(d, 1090, 1230, 580, c, GRAY); box(d, 1262, 540, 1700, 650, c, color=GRAY); text(d, 1481, 595, "THE STATE", 36, c, sp=4, **GR)
    strike(d, 1481, 595, "THE STATE", 36, ease((t - at(5, "not the state") - 0.5) / 0.4), c, sp=4)
plate("p5c", ("T", 1230, 230, "THE ARMY CHANGES", 64, at(5, "Then the army")), ("P", 430, 960, "MARIUS", 44, at(5, "Marius", -0.1), 47.0),
      ("P", 1230, 800, "SOLDIERS NOW FOLLOW A MAN", 44, at(5, "Soldiers now follow")), ("G", 1230, 890, "NOT THE REPUBLIC", 32, at(5, "not the Republic")), pre=O("V33_marius", 430, 520, 760, 43.3, 47.0), extra=_army)
def _lists(im, d, t, A):
    t0 = at(5, "lists of enemies")
    for i in range(8):
        a = A * r(t, t0 + i * 0.12); y = 330 + i * 56; w = 300 + (i * 97) % 160; line(d, [(1180, y), (1180 + w, y)], a, 10, GRAY)
        k = ease((t - t0 - 1.2 - i * 0.3) / 0.3)
        if k > 0: line(d, [(1160, y), (1160 + (w + 40) * k, y)], A, 4)
plate("V06", ("P", 560, 760, "DICTATOR", 54, at(5, "as dictator", -0.2)), ("G", 1360, 240, "LISTS OF ENEMIES", 36, at(5, "lists of enemies")), ("G", cx, 940, "THEN HE STEPS DOWN", 36, at(5, "Then he steps down")),
      pre=O("V06_pompeius_rufus", 560, 480, 330), extra=_lists)
plate("p5d", ("T", cx, 520, "WHO CONTROLS THE ARMY?", 100, at(5, "who controls the army", -0.2)))
# ---------------- chapter 6
plate("V07+V29+V08", ("G", cx, 90, "THREE MEN DECIDE TO SHARE THE ANSWER", 30, 0.2), ("P", 400, 850, "POMPEY", 44, at(6, "Pompey")), ("G", 400, 930, "THE GREAT GENERAL", 28, at(6, "the great general")), ("P", 960, 850, "CRASSUS", 44, at(6, "Crassus")), ("G", 960, 930, "THE RICHEST MAN IN ROME", 28, at(6, "the richest man")),
      ("P", 1520, 850, "CAESAR", 44, at(6, "Gaius Julius Caesar")), ("G", 1520, 930, "DEEP IN DEBT", 28, at(6, "deep in debt")),
      pre=both(O("V07_pompey", 400, 450, 600, at(6, "Pompey", -0.2)), O("V29_crassus", 960, 450, 600, at(6, "Crassus", -0.2)), O("V08_caesar", 1520, 450, 600, at(6, "And Gaius", -0.2))))
plate("V09", ("P", 1300, 420, "THE THIRD PERSON", 54, at(6, "in the third person", -0.1)), ("G", 1300, 560, "PURE PROPAGANDA", 40, at(6, "pure propaganda")), pre=O("V09_caesar_1678", 520, 540, 1040))
def _cal(im, d, t, A):
    t1 = at(6, "then starts a new calendar"); k1 = ease((t - at(6, "last 445 days")) / 1.4); k2 = ease((t - t1) / 1.0); x0 = 300; full = 1320
    w = full * k1 * (1 - k2 * (1 - 365 / 445)); line(d, [(x0, 560), (x0 + full, 560)], A, 3, DIM)
    if w > 0: d.rectangle([x0, 548, x0 + w, 572], fill=col(ACC, A))
plate("p6a", ("T", cx, 380, "THE OLD ROMAN CALENDAR", 70, at(6, "The old Roman calendar"), at(6, "So Caesar makes", -0.2)), ("G", cx, 520, "MONTHS OUT OF STEP WITH THE SEASONS", 34, at(6, "months out of step"), at(6, "So Caesar makes", -0.2)), ("G", cx, 200, "46 BC", 44, at(6, "the year 46 BC")), ("T", cx, 380, "445 DAYS", 150, at(6, "445 days", -0.2), at(6, "then starts a new calendar")), ("T", cx, 380, "365 DAYS", 150, at(6, "365 days", -0.2)),
      ("G", cx, 680, "A LEAP YEAR EVERY FOURTH YEAR", 36, at(6, "a leap year")), ("P", cx, 870, "JULY", 80, at(6, "July.", -0.15)), extra=_cal)
plate("p6b", ("T", cx, 330, "FEBRUARY 44 BC", 96, at(6, "In February 44 BC")), ("P", cx, 580, "DICTATOR FOR LIFE", 64, at(6, "dictator for life", -0.2)), ("G", cx, 780, "THAT SOUNDS LIKE A KING", 38, at(6, "that sounds like a king")))
plate("V10", ("P", cx, 800, "TWENTY-THREE", 54, at(6, "twenty-three", -0.2)), ("G", cx, 910, "LIBERATORS", 44, at(6, "liberators", -0.1)), pre=O("V10_eid_mar", cx, 430, 440))
# ---------------- chapter 7
plate("V11", ("P", 1260, 380, "OCTAVIAN", 60, at(7, "Octavian", -0.2)), ("T", 1260, 560, "EIGHTEEN", 110, at(7, "eighteen years", -0.1)), ("G", 1260, 760, "THIRTEEN YEARS OF CIVIL WAR", 34, at(7, "Thirteen years")), pre=O("V11_octavian", 520, 560, 940))
plate("V12", ("P", 560, 800, "MARK ANTONY", 48, at(7, "Mark Antony", -0.1)), ("P", 1360, 800, "CLEOPATRA", 48, at(7, "Queen Cleopatra")), ("G", 1360, 885, "OF EGYPT", 30, at(7, "of Egypt")), pre=O("V12_antony_cleopatra", cx, 440, 460))
plate("V13", ("T", 1260, 330, "27 BC", 110, at(7, "In 27 BC")), ("P", 1260, 560, "AUGUSTUS", 70, at(7, "Augustus, the revered", -0.15)), ("G", 1260, 690, "THE REVERED ONE", 40, at(7, "the revered one")), pre=O("V13_prima_porta", 520, 550, 1040))
def _princeps(im, d, t, A):
    for x, name, ph in ((480, "CONSULS", "The consuls"), (960, "SENATE", "the senate and the elections"), (1440, "ELECTIONS", "the elections all")):
        a = A * r(t, at(7, ph)); box(d, x - 200, 560, x + 200, 680, a, color=GRAY); text(d, x, 620, name, 40, a, sp=4, **GR)
plate("p7a", ("G", cx, 150, "HE NEVER CALLS HIMSELF KING", 34, at(7, "He never calls")), ("T", cx, 310, "PRINCEPS", 130, at(7, "princeps", -0.15)), ("G", cx, 440, "THE FIRST CITIZEN", 40, at(7, "the first citizen")),
      ("P", cx, 850, "THE ARMY AND THE MONEY", 58, at(7, "the army and the money", -0.2)), extra=_princeps)
def _brick(im, d, t, A): arrow_r(d, 880, 1010, 330, A * r(t, at(7, "and left it")))
plate("p7b", ("G", 520, 330, "A CITY OF BRICK", 60, at(7, "a city of brick", -0.2)), ("T", 1400, 330, "A CITY OF MARBLE", 60, at(7, "a city of marble", -0.2)), ("G", 700, 740, "JULY", 70, at(7, "The month after July")), ("P", 1220, 740, "AUGUST", 80, at(7, "August.", -0.15)),
      extra=lambda im, d, t, A: (_brick(im, d, t, A), arrow_r(d, 860, 980, 740, A * r(t, at(7, "is renamed after him")))))
plate("p7c", ("G", cx, 290, "AUGUSTUS BEAT HIS HEAD AGAINST A DOOR", 32, at(7, "beat his head")), ("G", cx, 200, "ALL THREE ARE WIPED OUT", 36, at(7, "All three are wiped")), ("T", cx, 450, "VARUS, GIVE ME BACK", 100, at(7, "Varus, give me back", -0.2)), ("T", cx, 590, "MY LEGIONS!", 100, at(7, "Varus, give me back", 1.0)), ("G", cx, 800, "SUETONIUS", 30, at(7, "Suetonius says")))
plate("V14", ("T", 1280, 330, "XVII", 120, at(7, "seventeen", -0.1)), ("T", 1280, 500, "XVIII", 120, at(7, "eighteen and", -0.1)), ("T", 1280, 670, "XIX", 120, at(7, "nineteen", -0.1)), ("G", 1280, 850, "NEVER USED AGAIN", 36, at(7, "never used again")), pre=O("V14_caelius", 540, 545, 1030))
# ---------------- chapter 8
plate("V16", ("P", cx, 900, "AQUA VIRGO", 56, at(8, "the Aqua Virgo", -0.1)), ("P", cx, 990, "STILL FEEDS THE TREVI FOUNTAIN", 32, at(8, "still feeds")), pre=PH("V16_trevi"))
plate("p8a", ("G", cx, 200, "UNDER AUGUSTUS", 34, 30.2, at(8, "A century later")), ("G", cx, 400, "THE ROMAN PEOPLE NOW WANTED ONLY TWO THINGS", 32, at(8, "the Roman people now")), ("T", cx, 330, "TWO HUNDRED THOUSAND", 96, at(8, "two hundred thousand", -0.2), at(8, "A century later")), ("G", cx, 480, "FREE GRAIN EVERY MONTH", 40, at(8, "free grain"), at(8, "A century later")),
      ("G", cx, 300, "JUVENAL", 34, at(8, "the poet Juvenal")), ("T", cx, 520, "BREAD AND CIRCUSES", 120, at(8, "bread and circuses", -0.2)))
plate("p8b", ("G", cx, 200, "THE FAMOUS THUMBS DOWN", 36, at(8, "A word on the famous")), ("T", cx, 380, "POLLICE VERSO", 130, at(8, "pollice verso", -0.15)), ("G", cx, 560, "WITH A TURNED THUMB", 44, at(8, "with a turned thumb")), ("P", cx, 800, "NOBODY KNOWS WHICH WAY IT TURNED", 40, at(8, "Nobody knows")))
plate("V17", ("P", cx, 960, "A FRENCH PAINTING OF 1872", 44, at(8, "a French painting", -0.1)), pre=PH("V17_pollice_verso"))
def _vom(im, d, t, A):
    c = (cx, 560); k = ease((t - at(8, "It was an exit")) / 1.2)
    for i, (rx, ry) in enumerate(((150, 80), (240, 135), (330, 190), (420, 245))): d.ellipse([c[0] - rx, c[1] - ry, c[0] + rx, c[1] + ry], outline=col(WHITE if i in (0, 3) else GRAY, A), width=4 if i in (0, 3) else 2)
    for i in range(12):
        an = 2 * math.pi * i / 12 + 0.26; x0, y0 = c[0] + 430 * math.cos(an), c[1] + 252 * math.sin(an); x1, y1 = c[0] + (430 + 110 * k) * math.cos(an), c[1] + (252 + 64 * k) * math.sin(an)
        if k > 0: line(d, [(x0, y0), (x1, y1)], A, 5); d.ellipse([x1 - 9, y1 - 9, x1 + 9, y1 + 9], fill=col(WHITE, A))
plate("p8c", ("T", cx, 150, "VOMITORIUM", 90, at(8, "the vomitorium", -0.1)), ("G", cx, 240, "NEVER A ROOM FOR BEING SICK", 32, at(8, "never a room"), at(8, "It was an exit")), ("P", cx, 950, "AN EXIT", 60, at(8, "an exit", -0.1)), extra=_vom)
plate("p8d", ("T", cx, 520, "ROMAN CONCRETE", 130, at(8, "Roman concrete", -0.2)))
# ---------------- chapter 9
plate("p9a", ("T", cx, 330, "EVERY MORNING, REMIND YOURSELF", 62, at(9, "every morning", -0.1)), ("T", cx, 440, "THAT TODAY YOU WILL MEET PEOPLE", 62, at(9, "that today")), ("T", cx, 550, "WHO ARE RUDE AND UNGRATEFUL", 62, at(9, "who are rude")),
      ("G", cx, 760, "EIGHTEEN CENTURIES LATER", 34, at(9, "Eighteen centuries later")), ("P", cx, 860, "SOLD IN AIRPORT BOOKSHOPS", 44, at(9, "sold in airport", -0.1)))
plate("p9b", ("T", cx, 420, "180", 260, at(9, "dies in 180", 0.3)), ("G", cx, 680, "THE LONG PEACE STARTS TO END", 44, at(9, "the long peace")))
# ---------------- chapter 10
plate("p10a", ("T", cx, 300, "235", 200, 0.3), ("G", cx, 470, "MURDERED BY HIS OWN SOLDIERS", 36, at(10, "is murdered")), ("P", cx, 860, "FIFTY YEARS OF CHAOS", 60, at(10, "fifty years of chaos", -0.2)),
      extra=lambda im, d, t, A: tscale(d, t, 420, 1500, 640, "235", "285", at(10, "What follows"), 2.2, A))
def _emps(im, d, t, A):
    t0 = at(10, "more than twenty emperors", -0.4); t1 = at(10, "Most last a year")
    for i in range(24):
        x = 300 + (i % 12) * 120; y = 440 + (i // 12) * 130; a = A * r(t, t0 + i * 0.07); k = ease((t - t1 - i * 0.16) / 0.3)
        d.ellipse([x - 40, y - 40, x + 40, y + 40], fill=col(mix_(WHITE, DIM, k), a))
def mix_(c0, c1, k): return tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3))
plate("p10b", ("T", cx, 200, "235–284", 90, at(10, "Between 235")), ("P", cx, 760, "MORE THAN TWENTY EMPERORS", 50, at(10, "more than twenty emperors", -0.2)), ("G", cx, 880, "MOST LAST A YEAR OR TWO", 34, at(10, "Most last a year")),
      ("G", cx, 950, "KILLED BY THEIR OWN TROOPS", 34, at(10, "Most are killed")), extra=_emps)
plate("V22", ("P", cx, 910, "NEAR PERSEPOLIS", 50, at(10, "near Persepolis", -0.1)), ("P", cx, 995, "IT IS STILL THERE", 32, at(10, "It is still there")), pre=PH("V22_shapur"))
plate("V24", ("T", 1280, 420, "FOUR RULERS", 100, at(10, "four rulers", -0.2)), ("G", 1280, 600, "TWO SENIOR AND TWO JUNIOR", 38, at(10, "two senior")), pre=O("V24_tetrarchs", 540, 550, 1000))
plate("p10c", ("T", cx, 400, "305", 240, at(10, "In 305")), ("P", cx, 700, "HE RETIRES", 80, at(10, "He retires", -0.15)))
# ---------------- chapter 11
_XP = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 430)
def _sign(im, d, t, A):
    a = A * r(t, at(11, "the symbol of Christ", -0.4), 0.6)          # the Chi-Rho, set as a glyph
    if a > 0: bb = d.textbbox((0, 0), "\u2627", font=_XP); d.text((cx - (bb[0] + bb[2]) / 2, 530 - (bb[1] + bb[3]) / 2), "\u2627", font=_XP, fill=col(WHITE, a))
plate("p11a", ("G", cx, 110, "BEFORE THE BATTLE", 30, 20.4), ("T", cx, 210, "A SIGN", 80, at(11, "a sign from God", -0.1)), ("G", cx, 900, "THE SYMBOL OF CHRIST ON HIS SOLDIERS' SHIELDS", 32, at(11, "the symbol of Christ")), ("P", cx, 990, "HE WINS", 50, at(11, "He wins", -0.1)), extra=_sign)
plate("p11b", ("T", cx, 380, "313", 240, at(11, "In 313")), ("P", cx, 660, "FREEDOM OF WORSHIP", 64, at(11, "freedom of worship", -0.2)), ("G", cx, 800, "TO ALL, CHRISTIANS INCLUDED", 38, at(11, "to all, Christians")))
plate("V25", ("T", 1280, 420, "337", 200, at(11, "in 337", -0.1)), ("G", 1280, 640, "BAPTISED ONLY ON HIS DEATHBED", 34, at(11, "baptised only")), pre=O("V25_constantine", 540, 550, 980))
plate("V26", ("T", 1340, 360, "380", 170, at(11, "In 380")), ("P", 1340, 570, "THEODOSIUS", 56, at(11, "Theodosius", -0.1)), ("G", 1340, 700, "THE OFFICIAL RELIGION", 36, at(11, "the official religion")), pre=O("V26_missorium", 560, 550, 800))
plate("p11c", ("T", cx, 520, "THE OLD TEMPLES ARE CLOSED", 84, at(11, "The old temples")))
# ---------------- chapter 12
plate("p12a", ("T", cx, 330, "EIGHT HUNDRED YEARS", 100, at(12, "eight hundred years", -0.2)), ("G", cx, 800, "SINCE THE GAULS", 40, at(12, "since the Gauls")),
      extra=lambda im, d, t, A: tscale(d, t, 360, 1560, 560, "390 BC", "410", 23.6, 2.0, A))
plate("p12b", ("G", cx, 170, "IN BETHLEHEM", 30, 29.0), ("G", cx, 250, "JEROME", 40, at(12, "the scholar Jerome")), ("T", cx, 450, "THE CITY WHICH HAD TAKEN THE WHOLE WORLD", 62, at(12, "the city which had", -0.1)), ("T", cx, 580, "WAS ITSELF TAKEN", 100, at(12, "was itself taken", -0.1)))
plate("V27", ("G", cx, 790, "THE IMPERIAL REGALIA", 36, at(12, "the imperial regalia")), ("P", cx, 890, "CONSTANTINOPLE", 54, at(12, "to Constantinople", -0.1)), pre=O("V27_romulus_augustus", cx, 420, 440))
plate("p12c", ("T", 560, 400, "ROMULUS", 110, 61.9), ("G", 560, 530, "THE FOUNDER OF ROME", 36, at(12, "the founder of Rome")), ("T", 1380, 400, "AUGUSTUS", 110, 62.3), ("G", 1380, 530, "ITS FIRST EMPEROR", 36, at(12, "its first emperor")),
      ("P", cx, 820, "HISTORY HAS A SENSE OF HUMOUR", 44, at(12, "History has a sense")))
plate("p12d", ("T", cx, 250, "A B C D E F G H I K L M N O P Q R S T V X Y Z", 54, at(12, "The letters on this screen")), ("G", 760, 520, "JULY", 80, at(12, "down to July")), ("G", 1160, 520, "AUGUST", 80, at(12, "and August", -0.1)),
      ("P", 480, 800, "SENATE", 60, at(12, "Senate, republic")), ("P", 960, 800, "REPUBLIC", 60, at(12, "republic, veto", -0.1)), ("P", 1440, 800, "VETO", 60, at(12, "veto: all", -0.1)), ("G", cx, 940, "ALL LATIN", 36, at(12, "all Latin")))
plate("V28", ("P", cx, 940, "SPQR", 70, at(12, "still say SPQR", 0.3)), pre=PH("V28_spqr_cover"))
def _outro(im, d, t, A):
    text(d, cx, 300, "AGES", 150, A * r(t, 109.2), sp=14); text(d, cx, 440, "IN MINUTES", 70, A * r(t, 109.5), sp=22, color=ACC)
plate("outro", ("G", cx, 620, "THAT WAS ROME IN TWENTY MINUTES", 36, at(12, "That was Rome")), ("P", cx, 780, "SUBSCRIBE", 60, at(12, "subscribe", -0.1)), ("G", cx, 900, "WHICH CIVILIZATION SHOULD WE COVER NEXT?", 34, at(12, "which civilization")), extra=_outro)

# ================================================================= captions on clips and insets on maps: chapter -> [(still maker, t0, t1)]
def C_(n, key, lines, phrase, t1, d=-0.1, **kw): return (cap(f"c{n:02d}{key}", lines, **kw), phrase if isinstance(phrase, (int, float)) else at(n, phrase, d), t1)
def PN(v, x, y, h, t0, t1, frame=False): return (panel(f"{v}_{int(t0)}", [(INS[v]["files"][0].rsplit(".", 1)[0], x, y, h, frame)]), t0, t1)
def title_still():
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); g = Image.linear_gradient("L").resize((W, 520)); m = Image.new("L", (W, H), 0); m.paste(g.point(lambda v: int(v * 0.85)), (0, H - 520))
        im.paste(BG + (255,), (0, 0), m); d = ImageDraw.Draw(im); f = font(True, 150); s = "ANCIENT ROME"; w = tw(d, s, f, 10); x = cx - w / 2
        for ch in s: d.text((x, 730), ch, font=f, fill=WHITE + (255,)); x += d.textlength(ch, font=f) + 10
        f2 = font(True, 56); s2 = "IN 20 MINUTES"; w = tw(d, s2, f2, 16); x = cx - w / 2
        for ch in s2: d.text((x, 920), ch, font=f2, fill=ACC + (255,)); x += d.textlength(ch, font=f2) + 16
        p = f"{R}/tmp_panel_title.png"; im.save(p); return p
    return mk
def STILLS(n):
    if n == 0: return [C_(0, "a", ["NINETEEN HUNDRED YEARS OLD"], "nineteen hundred", 5.6), C_(0, "b", ["FROM NORTHERN BRITAIN TO THE EUPHRATES"], "from northern Britain", 16.5), C_(0, "c", ["ONE PERSON IN FIVE"], "one person in five", 20.1),
                       C_(0, "d", ["A FEW HUTS ON A HILL"], "a few huts", 23.9), C_(0, "e", ["A CITY THAT THROWS OUT ITS KINGS"], "a city that throws", 27.9), C_(0, "f", ["A SINGLE AFTERNOON"], "a single afternoon", 31.4),
                       C_(0, "g", ["A STREAM THAT CANNOT BE CROSSED"], "a stream that", 34.9), C_(0, "h", ["AN EMPEROR WHO RETIRES TO GROW CABBAGES"], "an emperor who retires", 37.7), C_(0, "i", ["THE LAST"], "the last.", 42.1, d=0.0),
                       C_(0, "j", ["WHY ROME NEVER QUITE ENDED"], "why Rome never", 46.3), (title_still(), 51.4, 53.9)]
    if n == 1: return [C_(1, "a", ["IRON AGE HUTS ON THE PALATINE HILL"], "Iron Age huts", 48.8)]
    if n == 2: return [C_(2, "a", ["WHO RULES INSTEAD?"], 0.2, 2.3), C_(2, "b", ["TWO CONSULS"], "two consuls", 7.4, d=-0.2), C_(2, "c", ["SAVED BY GEESE"], "saved by geese", 84.1), PN("V03", 1580, 600, 500, 97.4, 105.6, True)]
    if n == 3: return [PN("V04", 1560, 600, 600, 32.4, 39.9, True), C_(3, "a", ["THIRTY KILOMETRES A DAY"], "thirty kilometres", 50.8)]
    if n == 4: return [PN("V31", 1600, 640, 560, 35.6, 40.2), C_(4, "a", ["LIVY: FIFTY THOUSAND"], "fifty thousand", at(4, "Polybius", -0.15)), C_(4, "b", ["LIVY: FIFTY THOUSAND", "POLYBIUS: SEVENTY THOUSAND"], "Polybius", 58.1),
                       C_(4, "c", ["IN A SINGLE AFTERNOON"], "In a single afternoon", 60.1), PN("V32", 1640, 600, 600, 70.8, 77.1)]
    if n == 5: return [C_(5, "a", ["THEIR FARMS GONE"], "their farms gone", 18.4)]
    if n == 6: return [C_(6, "a", ["JANUARY 49 BC"], "In January 49 BC", at(6, "the Rubicon", -0.2), d=0.1), C_(6, "b", ["THE RUBICON"], "the Rubicon", 51.8), C_(6, "c", ["THE IDES OF MARCH"], "the Ides of March", 98.8), C_(6, "d", ["MORE THAN SIXTY MEN"], "More than sixty", 101.2)]
    if n == 7: return [C_(7, "a", ["31 BC"], "In 31 BC", at(7, "at Actium", -0.15), d=0.1), C_(7, "b", ["31 BC · ACTIUM"], "at Actium", 20.4), C_(7, "c", ["EGYPT BELONGS TO ROME"], "Egypt, with all", 25.6),
                       C_(7, "d", ["ARMINIUS"], "Arminius", 74.4), C_(7, "e", ["THREE LEGIONS"], "three legions", 78.0)]
    if n == 8: return [C_(8, "a", ["CLOSE TO A MILLION PEOPLE"], "close to a million", 7.2), C_(8, "b", ["FIVE OR SIX STOREYS HIGH"], "five or six storeys", 10.9), PN("V15", 420, 760, 420, 11.6, 17.4, True),
                       C_(8, "c", ["AD 80"], "In AD 80", at(8, "the Colosseum", -0.15), d=0.1), C_(8, "d", ["THE COLOSSEUM"], "the Colosseum", at(8, "fifty thousand", -0.15)), C_(8, "e", ["FIFTY THOUSAND"], "fifty thousand", 60.6),
                       C_(8, "f", ["AROUND AD 125"], "Around AD 125", at(8, "Hadrian", -0.15), d=0.1), C_(8, "g", ["HADRIAN"], "Hadrian rebuilds", 94.8), C_(8, "h", ["FORTY-THREE METRES"], "forty-three metres", 98.0)]
    if n == 9: return [PN("V18", 250, 620, 500, 0.4, 6.1), PN("V19", 250, 620, 500, 15.4, 21.3), C_(9, "a", ["AD 122"], "from AD 122", at(9, "a hundred and seventeen", -0.15)), C_(9, "b", ["A HUNDRED AND SEVENTEEN KILOMETRES"], "a hundred and seventeen", 28.8),
                       PN("V18", 300, 900, 320, at(9, "Trajan and Hadrian", -0.2), 42.9), PN("V19", 540, 900, 320, at(9, "and Hadrian", -0.1), 42.9), PN("V20", 1180, 900, 320, at(9, "Septimius Severus", -0.2), 42.9),
                       PN("V21", 1580, 640, 600, 62.5, 67.9), C_(9, "c", ["DUTY, DEATH AND STAYING CALM"], "duty, death", 75.3)]
    if n == 10: return [PN("V23", 1580, 840, 230, 50.6, 54.9), C_(10, "a", ["NINETEEN KILOMETRES OF BRICK"], "nineteen kilometres", 64.9), C_(10, "b", ["THE CABBAGES I HAVE GROWN WITH MY OWN HANDS"], "the cabbages", 99.7, size=34)]
    if n == 11: return [PN("V25", 1620, 640, 600, 13.4, 20.1), C_(11, "a", ["330"], "In 330", at(11, "Constantinople.", -0.1), d=0.1), C_(11, "b", ["330 · CONSTANTINOPLE"], "Constantinople.", at(11, "A new Rome", -0.1)), C_(11, "c", ["CONSTANTINOPLE — A NEW ROME"], "A new Rome", 61.1)]
    if n == 12: return [C_(12, "a", ["24 AUGUST 410"], "On the twenty-fourth", at(12, "Alaric", -0.15), d=0.1), C_(12, "b", ["24 AUGUST 410 · ALARIC"], "Alaric", 23.3), C_(12, "c", ["ROMULUS AUGUSTUS"], "Romulus Augustus", 52.2),
                        C_(12, "d", ["AUGUSTULUS — LITTLE AUGUSTUS"], "Augustulus", 55.7), C_(12, "e", ["A VILLAGE OF HUTS"], "A village of huts", 104.6), C_(12, "f", ["THE IDEA OF ROME NEVER DID"], "The idea of Rome", 108.7)]
    return []
# music: chapters 10 and 11 reuse tracks 4 and 7 until their own tracks arrive; chapter 12 has none
MUSIC = {n: f"{C}/music/{n:02d}.flac" for n in range(10)}; MUSIC.update({10: f"{C}/music/04.flac", 11: f"{C}/music/07.flac", 12: f"{C}/music/04.flac"}); STING = f"{R}/sting.wav"

def spec(n):
    segs = LAY[str(n)]["segs"]; ov = []; wins = []
    for a, b, kind, i, _ in segs:
        if kind == "MAP": nm, t0 = SCN[i]; ov.append((f"{C}/maps/out_look/{nm}.mp4", a, b, False, a - t0, 1.0))
        elif kind == "CLIP": f, ss, sp = clip_file(i, n, a); ov.append((f, a, b, True, ss, sp))
        elif i in G: wins.append((a, b, i))
        else: print("no graphics yet:", n, i)
    def gfx(t):
        im, d = blank()
        for a, b, i in wins:
            if a <= t < b or (t == b and b == segs[-1][1]): G[i](im, d, t)
        return im
    return dict(n=n, gfx=gfx, gfx_windows=[(a, b) for a, b, _ in wins], overlays=ov, stills=STILLS(n), card=card(n) if n else None, fade_out=1.2 if n == 12 else 0.5,
                music=(MUSIC[n], STING, -27.0 if n == 0 else None, 24.0 if n == 12 else None), music2=(f"{C}/music/01.flac", -32.0) if n == 12 else None)
class _S(dict):
    def __missing__(s, k): s[k] = spec(k); return s[k]
SPECS = _S()
if __name__ == "__main__":      # check: every segment has graphics, every phrase is found; sheet of plates
    import sys
    for n in range(13): s = spec(n); print(n, len(s["overlays"]), "overlays", len(s["stills"]), "stills", len(s["gfx_windows"]), "plates")
    ims = []
    for i, (n, a, b) in sorted(SEG.items(), key=lambda kv: (kv[1][0], kv[1][1])):
        for q in (0.55, 0.97):
            im, d = blank(); t = a + (b - a) * q - (0.3 if q > 0.9 else 0); G[i](im, d, t); im = im.resize((480, 270)); ImageDraw.Draw(im).text((4, 3), f"{i} ch{n} {t:.1f}", fill=(255, 255, 0)); ims.append(im)
    for k in range(0, len(ims), 48):
        part = ims[k:k + 48]; S = Image.new("RGB", (8 * 480, ((len(part) + 7) // 8) * 270))
        for j, im in enumerate(part): S.paste(im, (j % 8 * 480, j // 8 * 270))
        S.save(f"/tmp/chk/plates_{k // 48}.jpg", quality=85)
