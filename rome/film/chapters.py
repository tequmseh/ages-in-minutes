"""Rome: chapter specs built from ../layout.json (windows), ../clips.json (clip entry points), ../layout_inserts.json and the map scene list.
All seconds are voice-over seconds of the chapter. Plaque text repeats the voice-over wording."""
from gfxlib import *
from gfxlib import _load
from PIL import ImageFilter
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
@seg("p2d")
def _(im, d, t):
    ts = at(2, "throws his sword"); k = ease((t - ts - 0.9) / 0.5); ang = math.radians(9 * k); px, py = cx, 330; L = 360
    a = r(t, 84.4)
    line(d, [(px, py), (px, 760)], a, width=8); line(d, [(px - 150, 760), (px + 150, 760)], a, width=8)
    ex, ey = L * math.cos(ang), L * math.sin(ang); l = (px - ex, py - ey); rr = (px + ex, py + ey); line(d, [l, rr], a, width=8)
    for (x, y), lab in ((l, "GOLD"), (rr, "WEIGHTS")):
        line(d, [(x, y), (x - 90, y + 230)], a, width=3); line(d, [(x, y), (x + 90, y + 230)], a, width=3); line(d, [(x - 120, y + 230), (x + 120, y + 230)], a, width=8)
    for i in range(6): d.rectangle([l[0] - 66 + (i % 3) * 46, l[1] + 196 - (i // 3) * 30, l[0] - 66 + (i % 3) * 46 + 40, l[1] + 222 - (i // 3) * 30], fill=col(ACC, a * 0.0) if False else col(WHITE, a))
    for i in range(3): d.rectangle([rr[0] - 60 + i * 44, rr[1] + 186, rr[0] - 60 + i * 44 + 34, rr[1] + 222], fill=col(GRAY, a))
    s = ease((t - ts) / 0.9)          # the sword falls onto the weights
    if s > 0:
        sy = rr[1] + 150 - (1 - s) * 520; sx = rr[0]
        d.polygon([(sx - 150, sy - 6), (sx + 70, sy - 12), (sx + 120, sy), (sx + 70, sy + 12), (sx - 150, sy + 6)], fill=col(WHITE, s)); d.rectangle([sx - 160, sy - 30, sx - 148, sy + 30], fill=col(WHITE, s)); d.rectangle([sx - 215, sy - 8, sx - 160, sy + 8], fill=col(GRAY, s))
    text(d, cx, 190, "A RANSOM IN GOLD", 40, r(t, at(2, "a ransom in gold")) * (1 - r(t, at(2, "vae victis", -0.3))), sp=6, **GR)
    text(d, cx, 190, "VAE VICTIS", 110, r(t, at(2, "vae victis", -0.1)), sp=10, dy=20); plaque(d, cx, 930, "WOE TO THE DEFEATED", 46, r(t, at(2, "Woe to the defeated")), sp=6)

# captions on clips and insets on maps: chapter -> [(still maker, t0, t1)]
def STILLS(n):
    if n == 2: return [(cap("c02a", ["WHO RULES INSTEAD?"]), 0.2, 2.3), (cap("c02b", ["TWO CONSULS"]), at(2, "two consuls", -0.2), 7.4), (cap("c02c", ["SAVED BY GEESE"]), at(2, "saved by geese", -0.1), 84.1),
                       (panel("V03", [("V03_servian_wall", 1580, 600, 500, True)]), 97.4, 105.6)]
    return []
MUSIC = {n: f"{C}/music/{n:02d}.flac" for n in range(13)}; STING = f"{R}/sting.wav"

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
            if a <= t <= b: G[i](im, d, t)
        return im
    return dict(n=n, gfx=gfx, gfx_windows=[(a, b) for a, b, _ in wins], overlays=ov, stills=STILLS(n), card=card(n), fade_out=0.5, music=(MUSIC[n], STING))
class _S(dict):
    def __missing__(s, k): s[k] = spec(k); return s[k]
SPECS = _S()
