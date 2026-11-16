"""Persia: graphics, museum inserts and overlay lists for chapters 1-12 (the cold open is built separately once the clips exist).
All seconds are voice-over seconds of the chapter. Plaque text repeats the voice-over wording."""
from gfxlib import *
from gfxlib import _load
from PIL import ImageFilter
import os
R = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(R); cx = W // 2
def card(n): return [f"{C}/out/{f}" for f in sorted(os.listdir(f"{C}/out")) if f.startswith(f"persia_chapter_{n:02d}_")][0]
def M(n): return f"{C}/maps/out_look/{n}.mp4"
def RC(n): return f"{R}/rec/{n}.mp4"
GR = dict(color=GRAY, bold=False)

def panel(key, items, caption=None, cap_xy=None):
    """inset over a map: objects or photographs lie directly on the map with a soft shadow (no black panel).
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
        if caption:
            d = ImageDraw.Draw(im); f = font(True, 24); w = tw(d, caption, f, 4); x, y = cap_xy
            d.rectangle([x - w / 2 - 14, y - 21, x + w / 2 + 14, y + 21], fill=BG + (255,)); xx = x - w / 2
            for ch in caption: d.text((xx, y - 15), ch, font=f, fill=WHITE + (255,)); xx += d.textlength(ch, font=f) + 4
        p = f"{R}/tmp_panel_{key}.png"; im.save(p); return p
    return mk

# ---------------------------------------------------------------- 1. Nobody from nowhere
S1 = dict(n=1, gfx=None, overlays=[(M("01a_nobody"), 0, 26.0, False), (RC("R01"), 26.0, 33.1, True), (M("01b_cyrus"), 33.1, 75.3, False), (M("01c_twenty_years"), 75.3, 83, False)],
          stills=[(panel("vase", [("V01_croesus_vase", 1560, 700, 620, False)]), 68.8, 74.9)])

# ---------------------------------------------------------------- 2. Babylon and the cylinder
def g2(t):
    im, d = blank()
    a = win(t, 28.5, 37.7)
    if a > 0:
        obj(im, "V03_cyrus_cylinder", cx, 470, 620, a * r(t, 28.7, 0.6))
        text(d, cx, 880, "A CLAY CYLINDER", 60, a * r(t, 29.2), sp=8)
        text(d, cx, 970, "IN THE BABYLONIANS' OWN LANGUAGE", 32, a * r(t, 31.6), sp=7, **GR)
    a = win(t, 56.5, 75.2)
    if a > 0:
        obj(im, "V03_cyrus_cylinder", 520, 520, 500, a * r(t, 56.7, 0.6))
        text(d, 1380, 250, "A REPLICA AT THE", 32, a * r(t, 57.6), sp=8, **GR)
        text(d, 1380, 340, "UNITED NATIONS", 84, a * r(t, 59.2), sp=5)
        text(d, 1380, 470, "“THE FIRST CHARTER", 46, a * r(t, 61.2), sp=5); text(d, 1380, 530, "OF HUMAN RIGHTS”", 46, a * r(t, 61.2), sp=5)
        strike(d, 1380, 470, "“THE FIRST CHARTER", 46, r(t, 64.1, 0.3), a, sp=5); strike(d, 1380, 530, "OF HUMAN RIGHTS”", 46, r(t, 64.25, 0.3), a, sp=5)
        text(d, 1380, 640, "IT ISN'T", 40, a * r(t, 64.2), sp=10, **GR)
        text(d, 1380, 730, "THE CURATORS AT THE BRITISH MUSEUM SAY SO PLAINLY", 24, a * r(t, 69.4), sp=5, **GR)
        plaque(d, 1380, 880, "ROYAL PR", 110, a * r(t, 72.6), sp=6)
    return im
S2 = dict(n=2, gfx=g2, gfx_windows=[(28.4, 37.8), (56.4, 75.3)],
          overlays=[(M("02a_babylon"), 0, 14.8, False), (RC("R02"), 0, 7.6, True), (M("02b_terror"), 14.9, 28.6, False), (M("02c_going_home"), 37.6, 56.6, False), (M("02d_new_idea"), 75.1, 88, False)])

# ---------------------------------------------------------------- 3. Darius takes control of the story
def g3(t):
    im, d = blank()
    a = win(t, 14.0, 38.6)
    if a > 0:
        text(d, cx, 130, "WE KNOW IT MAINLY FROM ONE MAN", 34, a * r(t, 14.4), sp=8, **GR)
        text(d, cx, 200, "AND HE IS NOT NEUTRAL", 34, a * r(t, 17.3), sp=8)
        d.line([(cx, 300), (cx, 900)], fill=col(DIM, a * r(t, 19.3)), width=2)
        plaque(d, 500, 340, "ACCORDING TO DARIUS", 40, a * r(t, 19.5), sp=4)
        text(d, 500, 480, "A PRIEST STOLE THE THRONE", 40, a * r(t, 20.9), sp=4)
        text(d, 500, 545, "PRETENDING TO BE CYRUS' OTHER SON", 26, a * r(t, 22.6), sp=5, **GR)
        text(d, 500, 680, "DARIUS KILLS THE IMPOSTER", 40, a * r(t, 27.9), sp=4)
        text(d, 500, 745, "WITH SIX FRIENDS", 26, a * r(t, 29.1), sp=5, **GR)
        text(d, 500, 850, "AND TAKES THE CROWN", 40, a * r(t, 30.2), sp=4)
        plaque(d, 1420, 340, "SOME HISTORIANS SUSPECT", 40, a * r(t, 32.0), sp=4)
        text(d, 1420, 480, "THE IMPOSTER", 40, a * r(t, 34.7), sp=4); text(d, 1420, 545, "WAS THE REAL PRINCE", 40, a * r(t, 35.2), sp=4)
        text(d, 1420, 720, "AND DARIUS", 40, a * r(t, 36.4), sp=4); text(d, 1420, 785, "WAS THE USURPER", 40, a * r(t, 36.9), sp=4)
    a = win(t, 72.6, 83.0)
    if a > 0:
        photo(im, "V06_behistun", a); d = ImageDraw.Draw(im)
        text(d, 520, 905, "HIS ENEMIES FOLLOWED THE LIE", 34, a * r(t, 73.4), sp=6)
        text(d, 520, 975, "HE SERVES THE TRUTH", 34, a * r(t, 76.3), sp=6)
        plaque(d, 1340, 930, "A PRESS RELEASE CARVED IN STONE", 44, a * r(t, 78.6), sp=3)
    a = win(t, 83.0, 93.3, fo=0.5)
    if a > 0:
        obj(im, "V07_rawlinson", 520, 540, 860, a * r(t, 83.2, 0.6))
        text(d, 1320, 260, "THE 1830s AND 40s", 34, a * r(t, 83.6), sp=8, **GR)
        text(d, 1320, 380, "HENRY RAWLINSON", 88, a * r(t, 86.0), sp=4)
        text(d, 1320, 480, "A BRITISH OFFICER", 32, a * r(t, 85.2), sp=8, **GR)
        text(d, 1320, 640, "THREE PARALLEL TEXTS", 44, a * r(t, 89.0), sp=5)
        plaque(d, 1320, 800, "THE KEY TO READING CUNEIFORM", 46, a * r(t, 90.6), sp=3)
    return im
S3 = dict(n=3, gfx=g3, gfx_windows=[(13.9, 38.7), (72.5, 94)],
          overlays=[(M("03a_cambyses"), 0, 14.0, False), (M("03b_explodes"), 38.7, 57.4, False), (M("03c_behistun"), 57.5, 72.7, False), (RC("R03"), 57.5, 64.4, True)],
          stills=[(panel("tomb", [("V05_tomb_cyrus", 1480, 800, 380, True)]), 0.6, 4.7)])

# ---------------------------------------------------------------- 4. The operating system
def g4(t):
    im, d = blank()
    a = win(t, 0.0, 4.5, fi=0.01)
    if a > 0:
        text(d, cx, 430, "CYRUS BUILT THE EMPIRE", 54, a * r(t, 0.1), sp=7, **GR)
        plaque(d, cx, 600, "DARIUS TURNS IT INTO A MACHINE", 72, a * r(t, 2.2), sp=3)
    a = win(t, 36.4, 42.6)
    if a > 0:
        obj(im, "V08_daric", cx, 440, 480, a * r(t, 36.6, 0.5))
        text(d, cx, 790, "A GOLD COIN WITH A ROYAL ARCHER ON IT", 36, a * r(t, 38.0), sp=7, **GR)
        plaque(d, cx, 920, "THE HARD CURRENCY OF ITS AGE", 56, a * r(t, 40.3), sp=3)
    return im
S4 = dict(n=4, gfx=g4, gfx_windows=[(0, 4.7), (36.3, 42.8)],
          overlays=[(M("04a_satrapies"), 4.6, 25.8, False), (M("04b_kings_eyes"), 26.0, 36.5, False), (M("04c_languages"), 42.7, 57.8, False), (M("04d_stay_different"), 58.2, 73, False)],
          stills=[(panel("tab4", [("V17b_tablet_user", 420, 780, 420, False)]), 51.0, 57.5),
                  (panel("stat", [("V10b_darius_statue_full", 1620, 640, 700, False)]), 63.2, 66.4)])

# ---------------------------------------------------------------- 5. Beating distance
def g5(t):
    im, d = blank()
    a = win(t, 34.4, 45.3)
    if a > 0:
        obj(im, "V11_herodotus", 470, 560, 900, a * r(t, 34.6, 0.6))
        text(d, 1300, 200, "HERODOTUS", 96, a * r(t, 34.9), sp=8)
        text(d, 1300, 300, "NOT EASILY IMPRESSED BY PERSIANS", 28, a * r(t, 36.2), sp=6, **GR)
        plaque(d, 1300, 480, "NOTHING MORTAL TRAVELS FASTER", 48, a * r(t, 38.6), sp=2)
        for i, (s, t0) in enumerate((("NEITHER SNOW", 40.6), ("NOR RAIN", 41.4), ("NOR HEAT", 42.0), ("NOR DARKNESS", 42.6))):
            text(d, 1300, 630 + i * 70, s, 46, a * r(t, t0), sp=7)
        text(d, 1300, 950, "STOPS THESE COURIERS", 32, a * r(t, 43.6), sp=8, **GR)
    a = win(t, 45.3, 51.7)
    if a > 0:
        photo(im, "V13_farley", a); d = ImageDraw.Draw(im)
        plaque(d, cx, 960, "THE OLD MAIN POST OFFICE IN NEW YORK", 46, a * r(t, 48.4), sp=3)
    return im
S5 = dict(n=5, gfx=g5, gfx_windows=[(34.3, 51.9)],
          overlays=[(M("05a_the_road"), 0, 34.5, False), (RC("R04"), 22.2, 34.3, True), (M("05c_canal"), 51.8, 70, False)],
          stills=[(panel("stele", [("V12_shaluf_stele", 300, 760, 520, True)]), 56.0, 64.8)])

# ---------------------------------------------------------------- 6. Persepolis and the receipts
def g6(t):
    im, d = blank()
    a = win(t, 8.6, 20.7)
    if a > 0:
        photo(im, "V14_apadana", a); d = ImageDraw.Draw(im)
        b = a * (1 - r(t, 17.7, 0.3))
        text(d, cx, 890, "ASSYRIAN PALACES WERE DECORATED WITH", 28, b * r(t, 12.4), sp=6)
        text(d, 400, 975, "SIEGES", 40, b * r(t, 14.2), sp=6); text(d, 960, 975, "IMPALED PRISONERS", 40, b * r(t, 15.0), sp=6); text(d, 1540, 975, "PILES OF HEADS", 40, b * r(t, 16.2), sp=6)
        plaque(d, cx, 950, "HERE, NOT ONE BATTLE SCENE", 54, a * r(t, 18.1), sp=3)
    a = win(t, 20.7, 32.8)
    if a > 0:
        photo(im, "V15a_delegation", a); d = ImageDraw.Draw(im)
        plaque(d, cx, 930, "23 DELEGATIONS", 64, a * r(t, 21.6) * (1 - r(t, 26.0, 0.3)), sp=4)
        b = a * r(t, 26.4)
        for s_, t0, t1 in (("LYDIANS WITH FINE VESSELS", 26.5, 28.3), ("ARABS LEADING A CAMEL", 28.5, 30.0), ("AFRICANS CARRYING AN ELEPHANT TUSK", 30.2, 33.0)):
            text(d, cx, 950, s_, 46, a * win(t, t0, t1, 0.25, 0.2), sp=5)
    a = win(t, 32.8, 41.5)
    if a > 0:
        photo(im, "V15b_pesce", a); d = ImageDraw.Draw(im)
        text(d, cx, 950, "AN USHER TAKES EACH LEADER BY THE HAND", 40, a * r(t, 32.9) * (1 - r(t, 35.1, 0.25)), sp=5)
        text(d, cx, 890, "THE MESSAGE IS NOT “WE CRUSHED YOU”", 30, a * r(t, 35.5), sp=6)
        plaque(d, cx, 970, "EVERYONE HAS A PLACE, AND HERE IT IS", 50, a * r(t, 38.1), sp=3)
    a = win(t, 58.6, 85.4)
    if a > 0:
        obj(im, "V17b_tablet_user", 500, 540, 760, a * r(t, 58.8, 0.6))
        b = a * (1 - r(t, 74.0, 0.35))
        text(d, 1380, 170, "AND WE CAN CHECK HIM", 30, b * r(t, 58.9), sp=8, **GR)
        text(d, 1380, 290, "1933", 130, b * r(t, 60.4), sp=8, dy=16)
        text(d, 1380, 400, "AN OFFICE ARCHIVE INSIDE THE", 26, b * r(t, 62.6), sp=6, **GR); text(d, 1380, 440, "FORTIFICATION WALL OF PERSEPOLIS", 26, b * r(t, 63.6), sp=6, **GR)
        plaque(d, 1380, 580, "20,000 TABLETS", 64, b * r(t, 66.6), sp=3); text(d, 1380, 665, "AND FRAGMENTS", 24, b * r(t, 68.0), sp=7, **GR)
        text(d, 1380, 780, "AROUND 15,000 DOCUMENTS", 44, b * r(t, 70.4), sp=4)
        text(d, 1380, 880, "COVERING JUST 16 YEARS", 44, b * r(t, 72.2), sp=4)
        c = a * r(t, 74.4)
        plaque(d, 1380, 250, "THEY ARE RECEIPTS", 60, c, sp=4)
        for i, (s, t0) in enumerate((("BARLEY FOR A GANG OF FOREIGN WORKERS", 75.9), ("WINE FOR A TRAVELLER ON HIS WAY FROM INDIA", 77.9), ("FEED FOR HORSES", 80.5), ("OFFERINGS FOR THE GODS", 82.0))):
            text(d, 1380, 440 + i * 110, s, 30, a * r(t, t0), sp=5)
        text(d, 1380, 440 + 3 * 110 + 46, "AND NOT ONLY THE PERSIAN ONES", 22, a * r(t, 83.4), sp=6, **GR)
    a = win(t, 85.4, 98.7)
    if a > 0:
        text(d, cx, 300, "NOT FREE IN OUR SENSE", 36, a * r(t, 85.9), sp=8, **GR)
        text(d, cx, 380, "MANY WERE PROBABLY DEPORTED THERE", 30, a * r(t, 88.5), sp=7, **GR)
        plaque(d, cx, 560, "COUNTED, FED AND PAID", 84, a * r(t, 90.6), sp=4)
        text(d, cx, 690, "DOWN TO THE LAST JUG", 36, a * r(t, 92.6), sp=8)
        text(d, cx, 860, "THE MOST POWERFUL MAN ON EARTH RAN HIS CAPITAL LIKE AN ACCOUNTANT", 28, a * r(t, 94.8), sp=5, **GR)
    a = win(t, 98.7, 104, fo=0.01)
    if a > 0:
        text(d, cx, 430, "THE GREEKS REMEMBERED THE WHIPS", 50, a * r(t, 99.1), sp=6, **GR)
        plaque(d, cx, 610, "THE TABLETS SHOW THE SPREADSHEETS", 64, a * r(t, 101.1), sp=3)
    return im
S6 = dict(n=6, gfx=g6, gfx_windows=[(8.5, 41.6), (58.5, 104)],
          overlays=[(M("06a_persepolis"), 0, 8.7, False), (RC("R05"), 20.8, 29.0, True), (M("06b_materials"), 41.7, 58.6, False), (RC("R06"), 85.4, 98.6, True)])

# ---------------------------------------------------------------- 7. The price
def g7(t):
    im, d = blank()
    a = win(t, 0.0, 6.7, fi=0.01)
    if a > 0:
        text(d, cx, 360, "NONE OF THIS MAKES PERSIA GENTLE", 44, a * r(t, 0.1), sp=7, **GR)
        plaque(d, cx, 540, "IT IS AN EMPIRE", 96, a * r(t, 2.6), sp=5)
        text(d, cx, 720, "IT TAKES YOUR SILVER AND YOUR SONS", 44, a * r(t, 4.2), sp=7)
    a = win(t, 6.7, 19.9)
    if a > 0:
        obj(im, "V06_behistun", cx, 360, None, a * r(t, 6.9, 0.6), w=1700, crop=(0.33, 0.30, 0.99, 0.57))
        text(d, cx, 730, "DARIUS TELLS US HIMSELF WHAT HE DID TO A REBEL KING", 28, a * r(t, 8.6), sp=6, **GR)
        for s, x, t0 in (("NOSE", 400, 11.9), ("EARS", 730, 12.5), ("TONGUE", 1110, 13.0), ("ONE EYE", 1530, 14.3)):
            text(d, x, 850, s, 60, a * r(t, t0), sp=8)
        text(d, cx, 970, "CHAINED AT THE PALACE GATE FOR EVERYONE TO SEE", 28, a * r(t, 15.6), sp=6, **GR)
    a = win(t, 19.9, 24.8)
    if a > 0:
        plaque(d, cx, 470, "TOLERANCE IS THE OFFER", 84, a * r(t, 20.3), sp=4)
        text(d, cx, 650, "THAT IS WHAT REFUSING IT LOOKS LIKE", 40, a * r(t, 22.3), sp=7, **GR)
    return im
S7 = dict(n=7, gfx=g7, gfx_windows=[(0, 25.0)],
          overlays=[(M("07a_ionian_revolt"), 25.0, 65.0, False), (RC("R07"), 37.0, 44.8, True), (M("07b_mardonius"), 65.6, 97, False)])

# ---------------------------------------------------------------- 8. Xerxes goes west
def g8(t):
    im, d = blank()
    a = win(t, 70.1, 97.0)
    if a > 0:
        photo(im, "V16_archers", a); d = ImageDraw.Draw(im)
        b = a * (1 - r(t, 82.2, 0.3))
        plaque(d, 520, 940, "10,000", 84, b * r(t, 73.6), sp=5); text(d, 1280, 925, "THE IMMORTALS", 76, b * r(t, 75.9), sp=7)
        text(d, 1280, 1005, "ALWAYS EXACTLY 10,000", 28, b * r(t, 79.8), sp=7)
        c = a * (1 - r(t, 88.9, 0.3))
        text(d, cx, 895, "WHEN A MAN DIES OR FALLS SICK", 32, c * r(t, 82.6), sp=6)
        plaque(d, cx, 980, "A REPLACEMENT STEPS IN AT ONCE", 48, c * r(t, 84.6), sp=3)
        text(d, cx, 895, "AROUND THEM, A CROWD OF OTHER PEOPLES", 32, a * r(t, 89.3), sp=6)
        text(d, cx, 980, "EACH IN ITS OWN DRESS, WITH ITS OWN WEAPONS", 40, a * r(t, 91.4), sp=5)
    return im
S8 = dict(n=8, gfx=g8, gfx_windows=[(70.0, 97.2)],
          overlays=[(M("08a_marathon"), 0, 27.3, False), (M("08b_engineering"), 27.4, 57.6, False), (RC("R08"), 27.4, 41.2, True), (RC("R09"), 41.5, 50.9, True),
                    (M("08c_the_army"), 57.9, 70.2, False), (RC("R10"), 70.2, 80.4, True), (M("08d_thermopylae"), 97.1, 129, False), (RC("R11"), 97.1, 110.8, True)],
          stills=[(panel("canal", [("V18_xerxes_canal", 1380, 760, 400, True)]), 51.3, 57.4)])

# ---------------------------------------------------------------- 9. The same war, seen from Susa
def g9(t):
    im, d = blank()
    a = win(t, 55.7, 60.6)
    if a > 0:
        text(d, cx, 430, "THEY WILL WRITE ABOUT IT FOR CENTURIES", 46, a * r(t, 55.9), sp=6, **GR)
        plaque(d, cx, 610, "THAT IS WHY YOU HAVE HEARD OF IT", 64, a * r(t, 58.2), sp=3)
    return im
S9 = dict(n=9, gfx=g9, gfx_windows=[(55.6, 60.8)],
          overlays=[(M("09a_salamis"), 0, 47.6, False), (RC("R12"), 0, 3.9, True), (RC("R13"), 17.1, 24.5, True), (M("09b_plataea"), 47.9, 55.9, False), (M("09c_from_susa"), 60.6, 79, False)])

# ---------------------------------------------------------------- 10. If you can't beat them, rent them
def g10(t):
    im, d = blank()
    a = win(t, 0.0, 4.5, fi=0.01)
    if a > 0:
        text(d, cx, 420, "AND PERSIA LEARNS", 54, a * r(t, 0.1), sp=8, **GR)
        plaque(d, cx, 600, "IF YOU CAN'T BEAT THE GREEKS, RENT THEM", 60, a * r(t, 2.0), sp=2)
    a = win(t, 4.5, 16.7)
    if a > 0:
        obj(im, "V19_themistocles", 470, 560, 900, a * r(t, 4.7, 0.6))
        text(d, 1300, 220, "THEMISTOCLES", 92, a * r(t, 4.8), sp=6)
        text(d, 1300, 330, "THE ATHENIAN WHO PLANNED THE VICTORY AT SALAMIS", 24, a * r(t, 6.2), sp=5, **GR)
        text(d, 1300, 480, "DRIVEN OUT BY HIS OWN CITY", 42, a * r(t, 8.5), sp=5)
        text(d, 1300, 600, "FLEES TO THE PERSIAN COURT", 42, a * r(t, 10.9), sp=5)
        text(d, 1300, 700, "LEARNS PERSIAN", 42, a * r(t, 12.4), sp=5)
        plaque(d, 1300, 880, "A GOVERNOR FOR THE GREAT KING", 46, a * r(t, 14.2), sp=3)
    return im
S10 = dict(n=10, gfx=g10, gfx_windows=[(0, 16.9)],
           overlays=[(RC("R14"), 4.5, 10.6, True), (M("10a_persian_gold"), 16.8, 41.2, False), (M("10b_ten_thousand"), 41.4, 58.9, False), (RC("R15"), 41.4, 47.4, True), (M("10c_kings_peace"), 59.2, 84, False)])

# ---------------------------------------------------------------- 11. The last Achaemenid
def g11(t):
    im, d = blank()
    a = win(t, 0.0, 16.7, fi=0.01)
    if a > 0:
        text(d, cx, 200, "THE GREEKS ALSO TELL A STORY", 34, a * r(t, 0.2), sp=8, **GR)
        text(d, cx, 380, "PERSIA IS ROTTING", 130, a * r(t, 3.7), sp=6, dy=16)
        for s, x, t0 in (("SOFT KINGS", 440, 5.5), ("SCHEMING QUEENS", 960, 6.5), ("TOO MUCH LUXURY", 1500, 7.6)):
            text(d, x, 590, s, 44, a * r(t, t0), sp=5)
        text(d, cx, 730, "HISTORIANS REPEATED IT FOR 2,000 YEARS", 30, a * r(t, 11.0), sp=7, **GR)
        strike(d, cx, 380, "PERSIA IS ROTTING", 130, r(t, 14.1, 0.4), a, sp=6)
        plaque(d, cx, 900, "THE EVIDENCE SAYS OTHERWISE", 64, a * r(t, 14.3), sp=3)
    a = win(t, 67.7, 82.6)
    if a > 0:
        obj(im, "V20b_alexander", 470, 540, 940, a * r(t, 67.9, 0.6))
        b = a * (1 - r(t, 75.6, 0.3))
        text(d, 1300, 300, "HE STARTS WEARING", 32, b * r(t, 68.0), sp=8, **GR)
        plaque(d, 1300, 420, "PERSIAN ROYAL DRESS", 60, b * r(t, 68.8), sp=3)
        text(d, 1300, 620, "HE ASKS HIS MACEDONIANS TO BOW", 36, b * r(t, 70.7), sp=5); text(d, 1300, 680, "THE PERSIAN WAY", 36, b * r(t, 72.4), sp=5)
        text(d, 1300, 820, "THEY ARE APPALLED", 44, b * r(t, 73.8), sp=8, **GR)
        text(d, 1300, 300, "AT SUSA", 32, a * r(t, 75.9), sp=8, **GR)
        text(d, 1300, 420, "HE MARRIES A DAUGHTER OF DARIUS", 38, a * r(t, 76.8), sp=4)
        plaque(d, 1300, 620, "ABOUT 80 OFFICERS", 64, a * r(t, 78.6), sp=3)
        text(d, 1300, 740, "MARRY PERSIAN NOBLEWOMEN", 34, a * r(t, 80.0), sp=6); text(d, 1300, 800, "IN THE SAME CEREMONY", 28, a * r(t, 81.2), sp=7, **GR)
    a = win(t, 82.6, 94.0)
    if a > 0:
        text(d, cx, 200, "THE FRENCH HISTORIAN PIERRE BRIANT", 34, a * r(t, 83.0), sp=8, **GR)
        text(d, cx, 330, "ALEXANDER ACTED AS", 44, a * r(t, 85.8), sp=7)
        plaque(d, cx, 500, "THE LAST OF THE ACHAEMENIDS", 80, a * r(t, 87.4), sp=3)
        text(d, cx, 740, "HE DID NOT DESTROY THE PERSIAN EMPIRE", 40, a * r(t, 90.4), sp=6, **GR)
        text(d, cx, 850, "HE TOOK IT OVER", 76, a * r(t, 92.3), sp=8)
    return im
S11 = dict(n=11, gfx=g11, gfx_windows=[(0, 16.9), (67.6, 94.1)],
           overlays=[(M("11a_alexander"), 16.8, 42.7, False), (M("11b_persepolis_burns"), 42.8, 62.2, False), (RC("R16"), 42.8, 53.2, True), (M("11c_keeps"), 62.4, 67.8, False),
                     (RC("R17"), 67.8, 75.5, True), (RC("R18"), 75.7, 82.4, True), (M("11d_carved_up"), 94.0, 108, False)],
           stills=[(panel("mosaic", [("V20a_mosaic", 1030, 850, 380, True)]), 36.0, 42.5)])

# ---------------------------------------------------------------- 12. What the tablet says
LOGO = Image.open(f"{C}/../channel/logo_mark_transparent.png").convert("RGBA")
def g12(t):
    im, d = blank()
    a = win(t, 0.0, 10.7, fi=0.01)
    if a > 0:
        photo(im, "V21_pasargadae_channel", a); d = ImageDraw.Draw(im)
        text(d, cx, 880, "THEIR WALLED ROYAL PARKS", 28, a * r(t, 2.7), sp=7)
        text(d, 420, 960, "PAIRIDAEZA", 50, a * r(t, 5.0), sp=7); text(d, 700, 960, "→", 50, a * r(t, 6.8), **GR)
        text(d, 990, 960, "PARADEISOS", 50, a * r(t, 7.4), sp=7); text(d, 1270, 960, "→", 50, a * r(t, 9.0), **GR)
        plaque(d, 1540, 960, "PARADISE", 56, a * r(t, 9.3), sp=5)
    a = win(t, 26.1, 45.2)
    if a > 0:
        obj(im, "V17b_tablet_user", 500, 540, 720, a * r(t, 26.3, 0.6))
        text(d, 1380, 180, "THE BEST ANSWER TO OUR QUESTION", 28, a * r(t, 26.5), sp=7, **GR)
        text(d, 1380, 270, "ONE OF THOSE CLAY TABLETS", 44, a * r(t, 28.0), sp=4); text(d, 1380, 330, "FROM PERSEPOLIS", 44, a * r(t, 29.4), sp=4)
        text(d, 1380, 500, "WOMEN ON A WORK TEAM HAVE GIVEN BIRTH", 28, a * r(t, 34.0), sp=5, **GR)
        text(d, 1380, 600, "EXTRA RATIONS", 56, a * r(t, 36.9), sp=6)
        text(d, 1380, 680, "WINE OR BEER, AND GRAIN", 30, a * r(t, 38.3), sp=7, **GR)
        plaque(d, 1380, 830, "TWICE AS MUCH IF THE BABY IS A BOY", 40, a * r(t, 40.3), sp=2)
        text(d, 1380, 960, "NOBODY SAID THIS WAS A FAIR WORLD", 26, a * r(t, 42.9), sp=6, **GR)
    a = win(t, 76.3, 100, fo=0.01)
    if a > 0:
        plaque(d, cx, 330, "THAT WAS PERSIA", 96, a * r(t, 76.9), sp=5)
        b = a * r(t, 80.6, 0.4)
        if b > 0:
            lg = LOGO.resize((int(LOGO.width * 100 / LOGO.height), 100), Image.LANCZOS); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * b)))
            wt = tw(d, "SUBSCRIBE", font(True, 70), 8); x0 = cx - (lg.width + 30 + wt) / 2
            im.paste(lg, (int(x0), 560), lg); text(d, x0 + lg.width + 30, 610, "SUBSCRIBE", 70, b, anchor="l", sp=8)
        text(d, cx, 800, "WHICH CIVILIZATION DO YOU WANT TO SEE NEXT?", 40, a * r(t, 82.4), sp=5)
        text(d, cx, 880, "TELL US IN THE COMMENTS", 30, a * r(t, 81.6), sp=8, **GR)
    return im
S12 = dict(n=12, gfx=g12, gfx_windows=[(0, 10.8), (26.0, 45.3), (76.2, 100)], fade_out=1.0,
           overlays=[(M("12a_the_name"), 10.8, 26.1, False), (RC("R19"), 30.6, 39.9, True), (M("12b_the_answer"), 45.3, 76.3, False)])

SPECS = {1: S1, 2: S2, 3: S3, 4: S4, 5: S5, 6: S6, 7: S7, 8: S8, 9: S9, 10: S10, 11: S11, 12: S12}
for k, s in SPECS.items(): s.setdefault("card", card(k))

SHOTS = {2: [33, 62, 70, 74], 3: [24, 37, 80, 92], 4: [3.8, 41.5], 5: [39, 44, 50], 6: [16.8, 19.5, 24, 31, 40, 64, 73, 83.5, 93, 102], 7: [5.5, 15, 23], 8: [78, 86, 93],
         9: [59.5], 10: [3.5, 15.5], 11: [8, 15.5, 74, 81.8, 89, 93.5], 12: [9.8, 32, 43.5, 84]}
if __name__ == "__main__":
    import sys
    ims = [(k, t, SPECS[k]["gfx"](t).resize((640, 360))) for k in SHOTS for t in SHOTS[k]]
    os.makedirs(f"{R}/chk", exist_ok=True); n = 0
    for p in range(0, len(ims), 16):
        part = ims[p:p + 16]; sh = Image.new("RGB", (4 * 640, ((len(part) + 3) // 4) * 360))
        for i, (k, t, im) in enumerate(part):
            ImageDraw.Draw(im).text((8, 6), f"ch{k} {t}", fill=(242, 194, 48)); sh.paste(im, (i % 4 * 640, i // 4 * 360))
        sh.save(f"{R}/chk/gfx_{n}.jpg", quality=86); n += 1
    for k in SPECS:
        for m, _, _ in SPECS[k].get("stills", []): m()
    print(len(ims), n)
