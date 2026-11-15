"""Graphics and timelines for chapters 1-12 (chapter 11 lives in ch11.py)."""
from gfxlib import *
import os, math
R = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(R); cx = W // 2
def card(n): return [f"{C}/out/{f}" for f in sorted(os.listdir(f"{C}/out")) if f.startswith(f"carthage_chapter_{n:02d}_")][0]
def M(n): return f"{C}/maps/out_look/{n}.mp4"
def RC(n): return f"{R}/rec/{n}.mp4"
def g(s, b=False, **k): return dict(color=GRAY, bold=b, **k)
GR = dict(color=GRAY, bold=False)

def g1(t):
    im, d = blank()
    a = win(t, 30.6, 37.2)
    if a > 0:
        obj(im, "murex_a", 700, 440, 470, a * r(t, 30.7)); obj(im, "murex_c", 1220, 440, 470, a * r(t, 31.0))
        plaque(d, cx, 800, "WORTH MORE THAN GOLD", 64, a * r(t, 31.3), sp=4)
        text(d, cx, 940, "LATER, THE COLOUR OF ROMAN EMPERORS", 34, a * r(t, 34.3), sp=7, **GR)
    a = win(t, 37.2, 41.6)
    if a > 0:
        text(d, cx, 170, "THEY SELL", 34, a * r(t, 37.4), sp=8, **GR)
        obj(im, "glass_tall", 430, 520, 440, a * r(t, 38.9)); obj(im, "glass_round", 640, 600, 220, a * r(t, 39.0)); obj(im, "glass_mid", 830, 560, 340, a * r(t, 39.1))
        obj(im, "bowl", 1380, 520, 470, a * r(t, 39.8))
        text(d, 640, 900, "GLASS", 60, a * r(t, 39.0), sp=8); text(d, 1380, 900, "FINE METALWORK", 60, a * r(t, 39.9), sp=8)
    a = win(t, 41.6, 58.7)
    if a > 0:
        text(d, cx, 150, "AND ONE THING BY ACCIDENT", 34, a * r(t, 41.9), sp=8, **GR)
        obj(im, "ahiram", cx, 330, None, a * r(t, 45.0, 0.6), w=1640)
        plaque(d, cx, 540, "22 SIGNS", 96, a * r(t, 46.6), sp=4); text(d, cx, 680, "ONE FOR EACH SOUND", 36, a * r(t, 48.3), sp=8, **GR)
        text(d, 520, 850, "PHOENICIAN", 54, a * r(t, 49.0), sp=5)
        text(d, 800, 850, "→", 54, a * r(t, 50.5), **GR); text(d, 960, 850, "GREEK", 54, a * r(t, 50.6), sp=5)
        text(d, 1120, 850, "→", 54, a * r(t, 53.2), **GR); text(d, 1290, 850, "LATIN", 54, a * r(t, 53.3), sp=5)
        text(d, 960, 915, "+ VOWELS", 24, a * r(t, 51.8), sp=6, **GR)
        text(d, cx, 1000, "YOU ARE READING ITS GRANDCHILD", 30, a * r(t, 55.6), sp=8, **GR)
    a = win(t, 58.7, 64.8, fo=0.2)
    if a > 0:
        text(d, cx, 300, "THE GREEK WORD FOR BOOK", 36, a * r(t, 58.9), sp=8, **GR)
        text(d, cx, 470, "BYBLOS", 170, a * r(t, 60.3), sp=14, dy=18)
        plaque(d, cx, 720, "BIBLE", 96, a * r(t, 63.2), sp=6)
    return im
S1 = dict(n=1, gfx=g1, gfx_windows=[(30.5, 64.9)], overlays=[(M("01a_the_purple_people"), 0, 20.7, False), (RC("R01"), 20.7, 30.6, True), (M("01b_the_purple_people"), 64.8, 96, False)])

def g2(t):
    im, d = blank()
    a = win(t, 34.4, 41.0)
    if a > 0:
        obj(im, "dido", cx, 420, 600, a * r(t, 34.5))
        plaque(d, cx, 820, "A GREAT STORY", 60, a * r(t, 35.0), sp=4)
        text(d, cx, 950, "WRITTEN DOWN ABOUT 900 YEARS LATER", 34, a * r(t, 38.6), sp=7, **GR)
    a = win(t, 41.0, 52.1)
    if a > 0:
        obj(im, "virgil", 560, 540, 800, a * r(t, 41.1))
        text(d, 1300, 300, "THE ROMAN POET", 32, a * r(t, 41.3), sp=8, **GR); text(d, 1300, 420, "VIRGIL", 130, a * r(t, 41.9), sp=10, dy=18)
        text(d, 1300, 600, "ELISSA  →  DIDO", 64, a * r(t, 43.6), sp=5)
        text(d, 1300, 700, "A DOOMED LOVE AFFAIR", 30, a * r(t, 45.0), sp=7, **GR); text(d, 1300, 748, "WITH THE ANCESTOR OF ROME", 30, a * r(t, 45.9), sp=7, **GR)
        plaque(d, 1300, 900, "ROMAN LITERATURE", 54, a * r(t, 50.4), sp=4)
    a = win(t, 52.1, 62.0)
    if a > 0:
        text(d, cx, 200, "WHAT WE CAN CHECK", 36, a * r(t, 52.4), sp=8, **GR)
        text(d, cx, 330, "FOUNDED, SAY THE GREEK HISTORIANS", 30, a * r(t, 54.6), sp=7, **GR)
        plaque(d, cx, 560, "814 BC", 150, a * r(t, 56.3), sp=6)
        text(d, cx, 780, "OLDEST FINDS ON THE SITE: THE 700s BC", 44, a * r(t, 58.6), sp=5)
        text(d, cx, 900, "CLOSE ENOUGH", 34, a * r(t, 60.9), sp=8, **GR)
    a = win(t, 62.0, 76.8, fo=0.2)
    if a > 0:
        text(d, cx, 230, "THE NAME IS REAL", 36, a * r(t, 62.2), sp=8, **GR)
        text(d, cx, 400, "QART-HADASHT", 160, a * r(t, 63.6), sp=10, dy=18)
        plaque(d, cx, 640, "NEW CITY", 84, a * r(t, 65.4), sp=6)
        text(d, cx, 790, "NEWTOWN", 54, a * r(t, 66.7), sp=10, **GR)
        text(d, cx, 930, "FOR CENTURIES IT SENDS GIFTS TO THE TEMPLE IN TYRE", 30, a * r(t, 71.0), sp=7, **GR)
    return im
S2 = dict(n=2, gfx=g2, gfx_windows=[(34.3, 76.9)], overlays=[(RC("R02"), 0, 8.0, True), (RC("R03"), 8.0, 14.0, True), (M("02a_new_city"), 14.0, 34.4, False), (M("02b_new_city"), 76.7, 96, False)])

def panel(key, box, items, caption=None):
    """inset over a map: the cut-out objects sit directly on the map with a soft shadow, NO black panel behind them
    (rule from 15 Nov: a black box on a map looks ugly). items = [(name, cx, cy, h)] in box coordinates; the caption goes on a small plaque."""
    from PIL import ImageFilter
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); x0, y0, x1, y1 = box
        for n, px, py, h in items:
            o = Image.open(f"{R}/cut/{n}.png").convert("RGBA"); o = o.resize((max(2, int(o.width * h / o.height)), h), Image.LANCZOS)
            pos = (int(x0 + px - o.width / 2), int(y0 + py - o.height / 2))
            sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); a = Image.new("L", (W, H), 0); a.paste(o.getchannel("A").point(lambda v: int(v * 0.45)), (pos[0] + 6, pos[1] + 10))
            sh.putalpha(a.filter(ImageFilter.GaussianBlur(12))); im.alpha_composite(sh); im.alpha_composite(o, pos)
        if caption:
            d = ImageDraw.Draw(im); f = font(True, 26); w = tw(d, caption, f, 5); cx_ = (x0 + x1) / 2; yb = y1 - 40
            d.rectangle([cx_ - w / 2 - 14, yb - 22, cx_ + w / 2 + 14, yb + 22], fill=BG + (255,)); xx = cx_ - w / 2
            for ch in caption: d.text((xx, yb - 16), ch, font=f, fill=WHITE + (255,)); xx += d.textlength(ch, font=f) + 5
        p = f"{R}/tmp_panel_{key}.png"; im.save(p); return p
    return mk
S3 = dict(n=3, gfx=None, overlays=[(M("03_the_trading_empire"), 0, 99, False)], stills=[(panel("amph", (30, 170, 290, 650), [("amphora2", 130, 165, 290), ("entella", 130, 395, 110)]), 30.9, 42.4),
                  (panel("gor", (1130, 480, 1450, 990), [("gorilla2", 160, 215, 400)], "GORILLAI"), 56.2, 67.2),
                  (panel("wolf", (820, 650, 1300, 1030), [("wolf2", 240, 160, 290)], "ROME"), 81.5, 93.2)])

def g4(t):
    im, d = blank()
    photo(im, "selinunte2", win(t, 30.0, 33.1, fi=0.25, fo=0.25), band=False)
    a = win(t, 33.0, 39.7)
    if a > 0:
        text(d, cx, 170, "THE GREEKS OF SYRACUSE", 34, a * r(t, 33.2), sp=8, **GR)
        obj(im, "syr_head", 500, 480, 400, a * r(t, 33.2)); obj(im, "syr_horse", 930, 480, 400, a * r(t, 33.4)); obj(im, "greek", 1400, 480, 470, a * r(t, 33.6))
        plaque(d, cx, 840, "THEY WRITE IT DOWN", 64, a * r(t, 37.0), sp=4)
        text(d, cx, 970, "AND THEIR BOOKS SURVIVE", 34, a * r(t, 38.1), sp=8, **GR)
    a = win(t, 39.7, 44.7)
    if a > 0:
        text(d, cx, 250, "IN THOSE BOOKS, CARTHAGINIANS ARE", 36, a * r(t, 39.9), sp=8, **GR)
        text(d, cx, 440, "CRUEL", 110, a * r(t, 41.7), sp=8, dy=14); text(d, cx, 600, "GREEDY", 110, a * r(t, 42.4), sp=8, dy=14); text(d, cx, 760, "CANNOT BE TRUSTED", 110, a * r(t, 43.1), sp=8, dy=14)
    a = win(t, 44.7, 54.5, fo=0.2)
    if a > 0:
        text(d, cx, 270, "THE ROMANS MAKE IT A PROVERB", 36, a * r(t, 44.9), sp=8, **GR)
        plaque(d, cx, 480, "PUNIC FAITH", 130, a * r(t, 46.9), sp=6)
        text(d, cx, 700, "THEIR PHRASE FOR TREACHERY", 54, a * r(t, 48.4), sp=5)
        text(d, cx, 860, "A LITTLE RICH, COMING FROM ROME", 34, a * r(t, 50.6), sp=8, **GR)
    return im
S4 = dict(n=4, gfx=g4, gfx_windows=[(29.9, 54.6)], overlays=[(M("04a_the_sicilian_wars"), 0, 25.0, False), (RC("R04"), 25.0, 30.0, True), (M("04b_the_sicilian_wars"), 54.4, 96, False)])

def g5(t):
    im, d = blank()
    a = win(t, 6.0, 14.9)
    if a > 0:
        obj(im, "aristotle", 560, 560, 800, a * r(t, 6.1), crop=(0, 0, 1, 0.84))
        text(d, 1300, 250, "A GREEK WITNESS", 32, a * r(t, 6.2), sp=8, **GR); text(d, 1300, 370, "ARISTOTLE", 120, a * r(t, 6.5), sp=8, dy=18)
        text(d, 1300, 500, "ONE OF THE BEST CONSTITUTIONS IN THE WORLD", 26, a * r(t, 9.0), sp=5, **GR)
        text(d, 1300, 640, "KINGSHIP", 64, a * r(t, 11.9), sp=8); text(d, 1300, 750, "ARISTOCRACY", 64, a * r(t, 12.7), sp=8); text(d, 1300, 860, "DEMOCRACY", 64, a * r(t, 13.6), sp=8)
    a = win(t, 24.8, 33.0)
    if a > 0:
        plaque(d, cx, 380, "104 JUDGES", 130, a * r(t, 24.9), sp=6)
        text(d, cx, 580, "THEIR JOB: WATCH THE GENERALS", 36, a * r(t, 25.2), sp=8, **GR)
        text(d, cx, 740, "IT KEEPS THE GENERALS HONEST", 58, a * r(t, 29.3), sp=5)
        text(d, cx, 860, "AND NERVOUS", 58, a * r(t, 31.3), sp=5)
    a = win(t, 66.2, 68.7, fi=0.15, fo=0.2)
    if a > 0:
        plaque(d, cx, 430, "MAGO", 130, a * r(t, 66.2), sp=8)
        text(d, cx, 630, "A MANUAL ON AGRICULTURE · 28 BOOKS", 44, a * r(t, 66.4), sp=6)
        text(d, cx, 770, "KEEP HIM IN MIND", 34, a * r(t, 67.5), sp=8, **GR)
    a = win(t, 68.7, 100, fo=0.01)
    if a > 0:
        text(d, cx, 130, "THE HARDEST QUESTION", 40, a * r(t, 69.4), sp=10)
        obj(im, "stele", cx, 400, 400, a * r(t, 71.3))
        xl, xr = 400, 1520
        text(d, xl, 340, "THE ACCUSERS", 60, a * r(t, 71.5), sp=6); text(d, xl, 430, "GREEK AND ROMAN AUTHORS", 28, a * r(t, 72.0), sp=6, **GR)
        text(d, xr, 340, "THE URNS", 60, a * r(t, 77.4), sp=6); text(d, xr, 430, "THOUSANDS, IN A SACRED PRECINCT", 28, a * r(t, 79.0), sp=6, **GR)
        text(d, cx, 670, "ONE TEAM: DIED BEFORE OR SOON AFTER BIRTH", 36, a * r(t, 84.4), sp=5)
        text(d, cx, 750, "ANOTHER: THE AGES POINT TO SACRIFICE", 36, a * r(t, 89.8), sp=5)
        text(d, cx, 830, "THE ARGUMENT IS NOT OVER", 30, a * r(t, 92.8), sp=8, **GR)
        text(d, xl, 500, "WERE ENEMIES", 40, a * r(t, 95.0), sp=6); text(d, xr, 500, "ARE REAL", 40, a * r(t, 96.9), sp=6)
        plaque(d, cx, 970, "HOLD BOTH", 60, a * r(t, 98.4), sp=8)
    return im
S5 = dict(n=5, gfx=g5, gfx_windows=[(5.9, 15.0), (24.7, 33.1), (66.1, 100)], fade_out=0.6,
          overlays=[(RC("R05"), 0, 6.0, True), (RC("R06"), 14.9, 24.8, True), (RC("R07"), 33.0, 43.0, True), (RC("R08"), 43.0, 53.9, True),
                    (M("05_round_harbour"), 53.9, 60.4, False), (RC("R09"), 60.4, 66.2, True)])

def hull(d, x0, x1, y, a, flip=False):
    c = col(WHITE, a); pts = [(x0, y), (x0 + 50, y + 70), (x1 - 70, y + 70), (x1, y - 30), (x1 - 40, y)]
    if flip: pts = [(x0 + x1 - px, py) for px, py in pts]
    d.line(pts + [pts[0]], fill=c, width=5); m = (x0 + x1) / 2
    d.line([(m, y), (m, y - 260)], fill=c, width=5); d.line([(m - 110, y - 235), (m + 110, y - 235)], fill=c, width=5)
def g6(t):
    im, d = blank()
    a = win(t, 38.7, 48.1, fo=0.2)
    if a > 0:
        text(d, cx, 150, "SO THEY CHEAT", 36, a * r(t, 39.4), sp=8, **GR)
        Y = 700; d.line([(140, Y + 95), (1780, Y + 95)], fill=col(DIM, a), width=3)
        hull(d, 260, 900, Y, a * r(t, 38.9)); hull(d, 1010, 1650, Y, a * r(t, 38.9), flip=True)
        text(d, 580, Y + 150, "ROMAN SHIP", 28, a * r(t, 39.0), sp=7, **GR); text(d, 1330, Y + 150, "CARTHAGINIAN SHIP", 28, a * r(t, 39.0), sp=7, **GR)
        b = a * r(t, 40.8)
        if b > 0:
            px, py = 840, Y - 6; d.line([(px, py), (px, py - 300)], fill=col(WHITE, b), width=6)       # pole at the bow
            k = ease((t - 44.2) / 0.5); k = k * k; ang = math.radians(78 * (1 - k) + 2 * k); L = 330
            ex, ey = px + L * math.cos(ang), py - 20 - L * math.sin(ang)
            d.line([(px, py - 20), (ex, ey)], fill=col(WHITE, b), width=12)
            d.line([(px, py - 300), (ex, ey)], fill=col(GRAY, b), width=2)                               # rope
            nx, ny = math.sin(ang), math.cos(ang)                                                        # spike under the far end
            d.polygon([(ex - 12 * math.cos(ang), ey + 12 * math.sin(ang)), (ex + 12 * math.cos(ang), ey - 12 * math.sin(ang)), (ex + 34 * nx, ey + 34 * ny)], fill=col(WHITE, b))
            text(d, 600, 360, "HINGED BRIDGE", 34, b * r(t, 41.0) * (1 - r(t, 44.0, 0.3)), sp=7)
            text(d, 1080, 330, "SPIKE", 34, a * r(t, 42.7) * (1 - r(t, 44.0, 0.3)), sp=7)
        plaque(d, cx, 960, "A SEA BATTLE BECOMES A LAND BATTLE", 46, a * r(t, 45.6), sp=4)
    return im
S6 = dict(n=6, gfx=g6, gfx_windows=[(38.6, 48.2)], overlays=[(M("06a_the_first_war_with_rome"), 0, 22.8, False), (RC("R10"), 22.8, 30.8, True), (RC("R11"), 30.8, 38.7, True),
                                                           (M("06b_the_first_war_with_rome"), 48.0, 101, False)])

def g7(t):
    im, d = blank()
    a = win(t, 34.0, 41.5, fi=0.2)
    if a > 0:
        obj(im, "libyan", cx, 250, 280, a * r(t, 34.1))
        text(d, cx, 480, "THE HISTORIAN POLYBIUS CALLS IT", 36, a * r(t, 34.0), sp=8, **GR)
        plaque(d, cx, 650, "THE TRUCELESS WAR", 116, a * r(t, 34.3), sp=5)
        text(d, cx, 860, "NEITHER SIDE TAKES PRISONERS", 50, a * r(t, 35.8), sp=6)
    return im
S7 = dict(n=7, gfx=g7, gfx_windows=[(33.9, 41.6)], overlays=[(M("07a_the_truceless_war"), 0, 30.0, False), (RC("R12"), 30.0, 34.0, True), (RC("R13"), 41.5, 51.5, True),
                                                           (M("07b_the_truceless_war"), 51.5, 96, False)])

def g8(t):
    im, d = blank()
    a = win(t, 15.6, 18.1, fo=0.2)
    if a > 0:
        obj(im, "hannibal", 520, 580, 860, a * r(t, 15.7), crop=(0, 0, 1, 0.91))
        text(d, 1400, 400, "THE SON'S NAME", 36, a * r(t, 15.9), sp=8, **GR)
        text(d, 1400, 560, "HANNIBAL", 140, a * r(t, 16.6), sp=10, dy=18)
    a = win(t, 18.1, 20.8, fi=0.2, fo=0.2)
    if a > 0:
        text(d, cx, 140, "SPAIN", 40, a * r(t, 18.3), sp=14, **GR)
        obj(im, "elche", 760, 590, 720, a * r(t, 18.2)); obj(im, "falcata", 1330, 590, 760, a * r(t, 18.5))
    return im
S8 = dict(n=8, gfx=g8, gfx_windows=[(15.5, 20.8)], fade_out=0.8, overlays=[(M("08a_the_barcas_in_spain"), 0, 5.4, False), (RC("R14"), 5.4, 15.6, True),
                                                                          (M("08b_the_barcas_in_spain"), 20.7, 78.0, False), (RC("R15_16"), 78.0, 96, True)])
S9 = dict(n=9, gfx=None, overlays=[(M("09_hannibal"), 0, 99, False)], stills=[(panel("plate", (300, 580, 700, 980), [("capena", 200, 200, 370)]), 30.6, 37.0)])

def g10(t):
    im, d = blank()
    a = win(t, 7.6, 10.9, fi=0.2, fo=0.2)
    if a > 0: text(d, cx, 540, "ROME CHANGES TACTICS", 90, a * r(t, 8.4), sp=6, dy=14)
    a = win(t, 18.6, 25.3, fi=0.2)
    if a > 0:
        text(d, cx, 340, "THE ROMANS NICKNAME HIM", 36, a * r(t, 18.7), sp=8, **GR)
        plaque(d, cx, 530, "THE DELAYER", 130, a * r(t, 19.7), sp=6)
        text(d, cx, 750, "NOT A COMPLIMENT. YET.", 50, a * r(t, 21.6), sp=6)
    return im
S10 = dict(n=10, gfx=g10, gfx_windows=[(7.5, 11.0), (18.5, 25.4)], overlays=[(RC("R17"), 0, 7.6, True), (RC("R18"), 10.9, 18.6, True), (M("10_the_long_defeat"), 25.3, 96, False)],
           stills=[(panel("scipio", (580, 30, 820, 440), [("scipio", 120, 175, 320)], "SCIPIO"), 33.4, 40.6)])

LOGO = Image.open(f"{C}/../channel/logo_mark_transparent.png").convert("RGBA")
def g12(t):
    im, d = blank()
    a = win(t, 27.3, 39.5)
    if a > 0:
        obj(im, "roll", 540, 540, None, a * r(t, 27.4), w=760)
        text(d, 1340, 300, "ROME KEEPS EXACTLY ONE WORK", 30, a * r(t, 27.7), sp=7, **GR)
        plaque(d, 1340, 470, "MAGO", 130, a * r(t, 30.1), sp=8)
        text(d, 1340, 650, "THE MANUAL ON FARMING", 48, a * r(t, 30.6), sp=5)
        text(d, 1340, 790, "TRANSLATED INTO LATIN", 30, a * r(t, 32.6), sp=7, **GR); text(d, 1340, 838, "BY ORDER OF THE SENATE", 30, a * r(t, 33.0), sp=7, **GR)
        text(d, 1340, 930, "QUOTED FOR CENTURIES", 30, a * r(t, 35.2), sp=7, **GR)
    a = win(t, 39.5, 49.7)
    if a > 0:
        text(d, cx, 260, "WHAT DO WE KNOW ABOUT CARTHAGE?", 70, a * r(t, 39.8), sp=4)
        text(d, cx, 460, "WHAT ITS ENEMIES WANTED US TO KNOW", 36, a * r(t, 42.3), sp=8, **GR)
        text(d, 330, 680, "CRUEL", 78, a * r(t, 44.5), sp=6, dy=14); text(d, 800, 680, "GREEDY", 78, a * r(t, 45.4), sp=6, dy=14); text(d, 1410, 680, "TREACHEROUS", 78, a * r(t, 46.2), sp=6, dy=14)
    a = win(t, 49.7, 59.3, fo=0.2)
    if a > 0:
        text(d, cx, 150, "AND WHAT THEY COULD NOT HIDE", 36, a * r(t, 49.9), sp=8, **GR)
        obj(im, "aristotle", 380, 380, 250, a * r(t, 50.2), crop=(0, 0, 1, 0.84)); text(d, 600, 380, "A CONSTITUTION A PHILOSOPHER ADMIRED", 48, a * r(t, 50.3), anchor="l", sp=3)
        obj(im, "ahiram", 380, 620, None, a * r(t, 53.1), w=330, crop=(0, 0, 0.3, 1)); text(d, 600, 620, "AN ALPHABET THE WEST STILL USES", 48, a * r(t, 53.2), anchor="l", sp=3)
        obj(im, "ram", 380, 860, None, a * r(t, 55.9), w=340); text(d, 600, 860, "A NAVY ROME HAD TO COPY PLANK BY PLANK", 48, a * r(t, 56.0), anchor="l", sp=3)
    a = win(t, 67.1, 71.1, fi=0.2, fo=0.2)
    if a > 0:
        photo(im, "baths", a); d = ImageDraw.Draw(im)
        text(d, cx, 880, "A CITY SO WELL PLACED", 56, r(t, 67.3), sp=5); text(d, cx, 970, "ITS DESTROYERS BUILT IT AGAIN", 56, r(t, 68.7), sp=5)
    a = win(t, 81.0, 100, fo=0.01)
    if a > 0:
        text(d, cx, 250, "THAT WAS CARTHAGE", 110, a * r(t, 81.3), sp=8, dy=18)
        plaque(d, cx, 440, "NEXT TIME: MESOPOTAMIA", 64, a * r(t, 83.1), sp=5)
        b = a * r(t, 84.9, 0.4)
        if b > 0:
            lg = LOGO.resize((int(LOGO.width * 100 / LOGO.height), 100), Image.LANCZOS); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * b)))
            wt = tw(d, "SUBSCRIBE", font(True, 70), 8); x0 = cx - (lg.width + 30 + wt) / 2
            im.paste(lg, (int(x0), 650), lg); text(d, x0 + lg.width + 30, 700, "SUBSCRIBE", 70, b, anchor="l", sp=8)
        text(d, cx, 860, "WHAT SHOULD WE COVER NEXT?", 44, a * r(t, 86.5), sp=6)
        text(d, cx, 940, "TELL US IN THE COMMENTS", 30, a * r(t, 87.6), sp=8, **GR)
    return im
S12 = dict(n=12, gfx=g12, gfx_windows=[(27.2, 59.4), (67.0, 71.2), (80.9, 100)], fade_out=1.0,
           overlays=[(M("12a_what_remains"), 0, 14.6, False), (RC("R23"), 14.6, 20.4, True), (RC("R24"), 20.4, 27.3, True), (RC("R25"), 59.3, 67.1, True), (M("12b_what_remains"), 71.0, 81.1, False)])

import ch11
S11 = dict(ch11.SPEC); S11["overlays"] = [(M("11_carthage_must_be_destroyed") if "maps/out/" in o[0] else o[0],) + tuple(o[1:]) for o in S11["overlays"]]
SPECS = {1: S1, 2: S2, 3: S3, 4: S4, 5: S5, 6: S6, 7: S7, 8: S8, 9: S9, 10: S10, 11: S11, 12: S12}
for k, s in SPECS.items(): s.setdefault("card", card(k))

if __name__ == "__main__":
    import sys
    shots = {12: [58]}
    ims = [(k, t, SPECS[k]["gfx"](t).resize((640, 360))) for k in shots for t in shots[k]]
    sh = Image.new("RGB", (4 * 640, ((len(ims) + 3) // 4) * 360))
    for i, (k, t, im) in enumerate(ims):
        ImageDraw.Draw(im).text((8, 6), f"ch{k} {t}", fill=(242, 194, 48)); sh.paste(im, (i % 4 * 640, i // 4 * 360))
    sh.save(f"{R}/chk/gfx_all.jpg", quality=88); [m() for k in (3, 9, 10) for m, _, _ in SPECS[k]['stills']]; print(len(ims))
