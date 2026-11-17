"""Vikings: overlay lists, text frames, museum inserts and clip captions for chapters 1-12 (the cold open is built in ../coldopen).
All seconds are voice-over seconds of the chapter. Numbers come from ../layout_clips.json (clips), ../layout_inserts.json (inserts)
and scenes.json (map scene windows, dumped from maps/vk_scenes.py list). Plaque text repeats the voice-over wording."""
from gfxlib import *
from gfxlib import _load
from PIL import ImageFilter
import os, json, subprocess
R = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(R); cx = W // 2
GR = dict(color=GRAY, bold=False)
def card(n): return [f"{C}/out/{f}" for f in sorted(os.listdir(f"{C}/out")) if f.startswith(f"vikings_chapter_{n:02d}_")][0]
def M(n): return f"{C}/maps/out_look/{n}.mp4"
def RC(n): return f"{R}/rec/{n}.mp4"

def scenes():
    p = f"{R}/scenes.json"
    if not os.path.exists(p) or os.path.getmtime(p) < os.path.getmtime(f"{C}/maps/vk_scenes.py"):
        o = subprocess.run(["python3", f"{C}/maps/vk_scenes.py", "list"], capture_output=True, text=True).stdout
        sc = [[l.split()[0], int(l.split()[1][2:]), float(l.split()[3]), float(l.split()[5])] for l in o.splitlines() if l and not l.startswith("total")]
        json.dump(sc, open(p, "w"), indent=0)
    return json.load(open(p))
SCN = scenes(); CLIPS = json.load(open(f"{C}/layout_clips.json"))["clips"]; INS = json.load(open(f"{C}/layout_inserts.json"))["inserts"]

# which part of the file a repeated clip shows: (clip, chapter, window start) -> (file, start inside the file)
PART = {("R01", 10, 73.3): ("R01", 0.5), ("R02", 8, 50.5): ("R02", 0.6), ("R03", 6, 93.9): ("R03", 5.8), ("R04", 2, 0.0): ("R04b", 2.0), ("R04", 12, 97.8): ("R04", 1.1),
        ("R15", 6, 41.7): ("R15", 5.1), ("R17", 7, 91.7): ("R17", 0.0)}
SPEED = {("R17", 7, 91.7): 0.99}          # R17 is 8.96 s for a 9.0 s window

def panel(key, items):
    """inset over a map: cut-outs or photographs lie directly on the map with a soft shadow (no black panel).
    items = [(name, cx, cy, h, frame)]; frame=True puts a thin light border round a rectangular photograph."""
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
    """white plaques as a transparent still, for captions that lie on top of a reconstruction clip; lines stack upwards from y"""
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = font(True, size); px, py = size * 0.45, size * 0.32
        for k, txt in enumerate(lines):
            yy = y - (len(lines) - 1 - k) * size * 1.95; w = tw(d, txt, f, sp)
            d.rectangle([cx - w / 2 - px, yy - size * 0.6 - py, cx + w / 2 + px, yy + size * 0.6 + py], fill=WHITE + (255,)); xx = cx - w / 2
            for ch in txt: d.text((xx, yy - size * 0.6), ch, font=f, fill=BG + (255,)); xx += d.textlength(ch, font=f) + sp
        p = f"{R}/tmp_panel_{key}.png"; im.save(p); return p
    return mk

# ---------------------------------------------------------------- text frames
def g1(t):
    im, d = blank()
    a = win(t, 0.0, 7.0, fi=0.01)
    if a > 0:
        text(d, cx, 260, "START WITH THE WORD", 30, a * r(t, 0.3), sp=8, **GR)
        text(d, cx, 470, "VIKINGR", 210, a * r(t, 2.6), sp=10)
        text(d, cx, 650, "A PERSON WHO GOES ON AN EXPEDITION OVERSEAS", 38, a * r(t, 4.2), sp=6, **GR)
    a = win(t, 7.1, 12.7, fo=0.01)
    if a > 0:
        text(d, cx, 300, "VIKING", 170, a * r(t, 7.3), sp=10); text(d, cx, 440, "THE EXPEDITION ITSELF", 38, a * r(t, 8.2), sp=7, **GR)
        text(d, cx, 660, "NOT A NATION", 72, a * r(t, 9.9), sp=6); plaque(d, cx, 840, "AN ACTIVITY", 92, a * r(t, 11.3), sp=6)
    return im
def g6(t):
    im, d = blank()
    a = win(t, 5.9, 19.4)
    if a > 0:
        text(d, cx, 170, "THREE LAYERS", 32, a * r(t, 6.1), sp=9, **GR)
        text(d, cx, 330, "THE JARLS", 88, a * r(t, 8.0), sp=6); text(d, cx, 410, "THE CHIEFTAINS AT THE TOP", 28, a * r(t, 8.9), sp=6, **GR)
        text(d, cx, 540, "THE FREE FARMERS", 88, a * r(t, 10.4), sp=6); text(d, cx, 620, "IN THE MIDDLE", 28, a * r(t, 11.5), sp=6, **GR)
        text(d, cx, 750, "THE THRALLS", 88, a * r(t, 13.0), sp=6); plaque(d, cx, 850, "SLAVES", 46, a * r(t, 14.3), sp=6)
        text(d, cx, 980, "MANY OF THE CAPTIVES FROM THE RAIDS END UP HERE", 26, a * r(t, 15.5), sp=5, **GR)
    a = win(t, 19.6, 28.9)
    if a > 0:
        text(d, cx, 330, "THE THING", 170, a * r(t, 21.4), sp=10); text(d, cx, 470, "AN OPEN-AIR ASSEMBLY", 38, a * r(t, 22.3), sp=7, **GR)
        text(d, cx, 660, "NO WRITTEN LAW", 72, a * r(t, 23.9), sp=6); plaque(d, cx, 830, "A LAWSPEAKER", 64, a * r(t, 25.6), sp=6)
        text(d, cx, 950, "HOLDS IT IN HIS HEAD AND RECITES IT ALOUD", 26, a * r(t, 26.6), sp=5, **GR)
    a = win(t, 29.1, 41.7)
    if a > 0:
        x = 640
        text(d, x, 170, "THEIR GODS ARE MANY", 32, a * r(t, 29.2), sp=9, **GR)
        text(d, x, 340, "ODIN", 130, a * r(t, 30.8), sp=8); text(d, x, 435, "GOD OF WAR AND WISDOM", 28, a * r(t, 31.5), sp=6, **GR)
        text(d, x, 590, "THOR", 130, a * r(t, 33.3), sp=8); text(d, x, 685, "WHO PROTECTS ORDINARY FARMERS", 28, a * r(t, 34.6), sp=6, **GR)
        text(d, x, 850, "VALHALLA", 100, a * r(t, 40.0), sp=8); text(d, x, 935, "ODIN'S HALL", 28, a * r(t, 39.2), sp=6, **GR)
        obj(im, "V22_thor_hammer", 1400, 560, 600, a * r(t, 33.6, 0.6))
    return im
GFX = {1: (g1, [(0.0, 12.7)]), 6: (g6, [(5.8, 41.8)])}

# ---------------------------------------------------------------- museum inserts on maps: V## -> [(file, cx, cy, h, frame)], optional window override
PAN = {
 "V01": [("V14_roek_a", 1520, 600, 600, True)],
 "V03": [("V12_oseberg_dig", 1530, 680, 480, True)],
 "V02": [("V13_oseberg_ship", 1530, 680, 480, True)],
 "V05": [("V10_lindisfarne_stone", 1470, 640, 470, False)],
 "V04": [("V11_gospels_page", 1540, 610, 640, True)],
 "V06": [("V20_denier", 1440, 660, 300, False)],
 "V07": [("V03_alfred_jewel", 1500, 620, 600, False)],
 "V08": [("V09_key_lesecq", 1330, 640, 460, False), ("V04_oval_brooch", 1630, 640, 250, False)],
 "V10": [("V05c_scales", 1560, 610, 640, True)],
 "V11": [("V05_silver_bars", 1440, 420, 300, False), ("V05b_dirhams_case", 1440, 780, 330, True)],
 "V12": [("V06_pend1", 1250, 760, 330, False), ("V06_pend2", 1500, 760, 300, False), ("V06_pend3", 1730, 760, 290, False)],
 "V14": [("V07_hist_a", 1330, 700, 330, False), ("V07_hist_b", 1680, 700, 330, False)],
 "V15": [("V15_u112", 1440, 660, 460, True)],
 "V13": [("V08_halfdan_runes", 1300, 800, 380, True)],
 "V16": [("V18_hvalsey", 1380, 600, 520, True)],
 "V17": [("V17_jelling", 1500, 620, 640, False)],
 "V18": [("V16_cnut_a", 1330, 680, 340, False), ("V16_cnut_b", 1680, 680, 340, False)],
 "V19": [("V19_bayeux", 1380, 680, 500, True)],
 "V20": [("V02_valkyrie", 1500, 600, 700, False)],
 "V21": [("V01_helmet", 1500, 620, 520, False)],
}
WIN = {"V16": (99.8, 105.6)}          # the Hvalsey photograph leaves before "AFTER THAT, SILENCE."

# ---------------------------------------------------------------- captions on clips: chapter -> [(t0, t1, [lines])]
CAPS = {
 2: [(6.4, 13.4, ["THE 700s"]), (45.0, 46.5, ["NO HARBOUR NEEDED"])],
 3: [(11.6, 16.5, ["HEATHEN MEN"]), (55.1, 59.4, ["841"]), (59.8, 65.6, ["DUBLIN"])],
 4: [(35.9, 38.4, ["SEVEN THOUSAND POUNDS OF SILVER AND GOLD"]), (38.6, 40.8, ["MORE THAN TWO AND A HALF TONNES"]), (41.0, 42.4, ["IT WORKS."])],
 5: [(48.9, 54.4, ["A MUCH LATER LEGEND"])],
 6: [(2.5, 5.7, ["A FARM"])],
 7: [(13.9, 20.8, ["FROM THE 700s"]), (91.7, 94.9, ["“I HAVE NEVER SEEN BODIES MORE PERFECT THAN THEIRS.”"]), (95.1, 96.8, ["“THEY WERE LIKE PALM TREES.”"]), (98.4, 100.6, ["AN AXE, A SWORD AND A KNIFE"])],
 8: [(11.0, 17.5, ["THE EIGHTEENTH OF JUNE 860"]), (20.0, 22.0, ["LIKE A SWARM OF WASPS"]), (50.8, 54.3, ["THE VARANGIAN GUARD"]), (57.4, 59.7, ["THE EMPEROR PAYS VERY WELL"])],
 9: [(75.0, 77.7, ["A DAY AND A NIGHT"]), (80.0, 82.0, ["ONE LAW AND ONE FAITH"])],
 10: [(39.7, 43.5, ["AROUND THE YEAR 1000"]), (43.9, 45.4, ["VINLAND, WINE LAND"]), (47.4, 48.7, ["A LEGEND"]), (50.0, 54.8, ["1960"]), (55.4, 58.6, ["THE NORTHERN TIP OF NEWFOUNDLAND"]),
      (73.4, 75.4, ["2021"]), (75.8, 81.9, ["A SOLAR STORM FROM THE YEAR 993"])],
 11: [(84.0, 85.9, ["EVEN A KING HAS LIMITS"])],
 12: [(20.4, 25.2, ["STAMFORD BRIDGE"]), (25.4, 27.1, ["HARDRADA IS KILLED"]), (31.0, 33.4, ["NINETEEN DAYS LATER"]), (34.2, 36.3, ["HASTINGS"]), (36.5, 38.4, ["WILLIAM, DUKE OF NORMANDY"]),
      (97.9, 99.5, ["THEY STARTED AS RAIDERS."]), (99.7, 102.6, ["THEY ENDED AS FOUNDERS."])],
}

def spec(n):
    ov = [(M(nm), a, b, False) for nm, ch, a, b in SCN if ch == n]
    for nm, c in CLIPS.items():
        for u in c["use"]:
            if u[0] != n: continue
            f, ss = PART.get((nm, n, u[1]), (nm, 0.0)); sp = SPEED.get((nm, n, u[1]), float(u[3].split()[1]) if len(u) > 3 else 1.0)
            ov.append((RC(f), u[1], u[2], True, ss, sp))
    st = []
    for v, items in PAN.items():
        i = INS[v]
        if i["ch"] == n: a, b = WIN.get(v, (i["t0"], i["t1"])); st.append((panel(v, items), a, b))
    for k, (a, b, lines) in enumerate(CAPS.get(n, [])): st.append((cap(f"c{n:02d}_{k}", lines), a, b))
    g = GFX.get(n)
    return dict(n=n, gfx=g[0] if g else None, gfx_windows=g[1] if g else [], overlays=ov, stills=st, card=card(n), fade_out=0.5)
class _S(dict):
    def __missing__(s, k): s[k] = spec(k); return s[k]
SPECS = _S()

if __name__ == "__main__":
    tot = 0; files = set()
    for n in range(1, 13):
        s = spec(n)
        for o in s["overlays"]:
            if "/rec/" in o[0]: tot += o[2] - o[1]; files.add(os.path.basename(o[0]))
        print(n, len(s["overlays"]), "overlays,", len(s["stills"]), "stills")
    print("clip files", len(files), "clip seconds in chapters", round(tot, 1))
