"""Vikings cold open (52 s): reconstruction footage with lower-third text, the map, the title. 1920x1080, 60 fps."""
import sys, subprocess, os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
W, H, FPS, DUR = 1920, 1080, 60, 52.0
BG = (17, 17, 17); WHITE = (242, 240, 235); GRAY = (128, 132, 136); DIM = (70, 72, 75); ACC = (242, 194, 48); LIGHT = (205, 205, 200)
HERE = os.path.dirname(os.path.abspath(__file__)); REC = f"{HERE}/../rec"
FB = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"; FR = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
_f = {}
def font(b, s):
    k = (b, int(s))
    if k not in _f: _f[k] = ImageFont.truetype(FB if b else FR, int(s))
    return _f[k]
def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
def r(t, t0, d=0.35): return ease((t - t0) / d)
def win(t, a, b, fi=0.3, fo=0.3): return max(0.0, min(1.0, (t - a) / fi, (b - t) / fo))
def tw(d, s, f, sp=0): return sum(d.textlength(ch, font=f) + sp for ch in s) - sp
def text(d, x, y, s, size, a=1.0, bold=True, color=WHITE, anchor="m", sp=0):
    if a <= 0: return
    f = font(bold, size); w = tw(d, s, f, sp); x0 = x - w / 2 if anchor == "m" else (x - w if anchor == "r" else x)
    for ch in s:
        d.text((x0, y - size * 0.6), ch, font=f, fill=color + (int(255 * a),)); x0 += d.textlength(ch, font=f) + sp
def plaque(d, x, y, s, size, a=1.0, sp=2):
    if a <= 0: return
    f = font(True, size); w = tw(d, s, f, sp); px, py = size * 0.45, size * 0.32
    d.rectangle([x - px, y - size * 0.6 - py, x + w + px, y + size * 0.6 + py], fill=WHITE + (int(255 * a),))
    xx = x
    for ch in s:
        d.text((xx, y - size * 0.6), ch, font=f, fill=BG + (int(255 * a),)); xx += d.textlength(ch, font=f) + sp
LOGO = Image.open(f"{HERE}/../../channel/logo_mark_transparent.png").convert("RGBA")
# file, start inside the file, window on the timeline, dark band under text, playback speed (windows from ../layout_clips.json, chapter 0)
SEG = [("R01", 0.0, 0.0, 10.5, True, 0.95), ("R05", 0.0, 10.5, 16.1, True, 1.0), ("R02", 0.0, 16.1, 21.9, True, 1.0), ("R03", 0.0, 21.9, 29.3, True, 1.0),
       ("R04", 0.0, 29.3, 45.1, True, 0.949), ("MAP", 0.0, 45.1, 52.0, False, 1.0)]
T_TITLE = 49.0
_g = np.linspace(0, 1, 520)[:, None, None] ** 1.05 * 0.93
class Reader:
    def __init__(s, name, ss, n, sp=1.0):
        f = f"{HERE}/../maps/out_look/00_cold_open.mp4" if name == "MAP" else f"{REC}/{name}.mp4"
        if name == "MAP": ss = min(ss, 4.6)          # the map file is 4.7 s; its last frame is held under the title
        s.p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", str(ss), "-i", f, "-vf", f"setpts=PTS/{sp},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1",
                                "-frames:v", str(n + 3), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE); s.last = None
    def get(s):
        b = s.p.stdout.read(W * H * 3)
        if len(b) == W * H * 3: s.last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        return s.last
_rd = {}
def base(t):
    for k, (n, ss, a, b, band, sp) in enumerate(SEG):
        if a <= t < b:
            if k not in _rd: _rd[k] = Reader(n, ss + (t - a) * sp, int((b - t) * FPS), sp)
            f = _rd[k].get().astype(np.float32)
            if band: f[H - 520:] = f[H - 520:] * (1 - _g) + np.array(BG, np.float32) * _g
            k2 = min(1.0, (t + 0.001) / 0.4 if a == 0 else 1.0, 1 - ease((t - T_TITLE) / 0.5) if n == "MAP" else 1.0)
            if k2 < 1: f = f * k2 + np.array(BG, np.float32) * (1 - k2)
            return Image.fromarray(f.astype(np.uint8))
    return Image.new("RGB", (W, H), BG)
def num(d, cx, y, k, s, a):
    f = font(True, 50); w = tw(d, s, f, 3); x0 = cx - (96 + w) / 2
    text(d, x0, y, f"0{k}", 50, a, anchor="l", color=LIGHT); text(d, x0 + 96, y, s, 50, a, anchor="l", sp=3)
LINES = [(0.3, 5.5, "THE YEAR 1021", "NEWFOUNDLAND"), (6.3, 10.3, "A STORM ON THE SUN LEFT A MARK INSIDE THE TREE", None),
         (11.2, 13.6, "THE PEOPLE LIVING THERE HAD NO IRON AXES", None), (13.9, 15.9, "THIS ONE HAD COME FROM GREENLAND", None),
         (17.6, 21.6, "THEY STOOD GUARD OVER THE EMPEROR", "CONSTANTINOPLE"), (24.6, 29.0, "MORE THAN FOURTEEN THOUSAND SILVER COINS", "A SWEDISH ISLAND"),
         (29.6, 34.3, "FARMERS FROM A LAND WITH NO REAL CITIES", "AND ALMOST NO BOOKS")]
def frame(t):
    im = base(t).convert("RGBA"); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); cx = W // 2
    for t0, t1, s1, s2 in LINES:
        a = win(t, t0, t1, fi=0.25, fo=0.25)
        if a > 0:
            text(d, cx, 930 if s2 else 960, s1, 54, a, sp=3)
            if s2: text(d, cx, 1010, s2, 32, a * r(t, t0 + 1.2), sp=6, color=LIGHT, bold=False)
    a = win(t, 34.8, 36.3)
    if a > 0:
        f = font(True, 70); s = "IN THE NEXT TWENTY MINUTES"; w = tw(d, s, f, 2); x0 = cx - (150 + w) / 2
        lg = LOGO.resize((120, 120), Image.LANCZOS); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        ov.paste(lg, (int(x0), 880), lg); text(d, x0 + 150, 940, s, 70, a * r(t, 34.9), anchor="l", sp=2)
    for k, (t0, t1, s) in enumerate([(36.5, 39.4, "THE TRADERS WHO PROBABLY GAVE RUSSIA ITS NAME"), (39.6, 41.9, "AN ISLAND THAT CHANGES ITS GODS BY LAW"),
                                     (42.1, 44.9, "THE FIRST EUROPEANS TO BUILD A HOUSE IN AMERICA")]):
        a = win(t, t0, t1, fi=0.25, fo=0.25)
        if a > 0: num(d, cx, 950, k + 1, s, a)
    a = win(t, T_TITLE, 99, fi=0.01)
    if a > 0:
        text(d, cx, 430, "THE VIKINGS", 190, a * r(t, T_TITLE + 0.15), sp=10)
        text(d, cx, 600, "IN 20 MINUTES", 60, a * r(t, T_TITLE + 0.9), sp=14, color=GRAY, bold=False)
        X0, X1, Y = 160, 1760, 840; ta = a * r(t, T_TITLE + 0.4)
        d.line([(X0, Y), (X1, Y)], fill=DIM + (int(255 * ta),), width=3)
        g = ease((t - T_TITLE - 0.6) / 1.4)
        if g > 0: d.rectangle([X0, Y - 7, X0 + (X1 - X0) * g, Y + 7], fill=ACC + (int(255 * ta),))
        text(d, X0, Y + 44, "793", 26, ta, anchor="l", color=ACC, bold=False); text(d, X1, Y + 44, "1066", 26, ta, anchor="r", color=ACC, bold=False)
    return Image.alpha_composite(im, ov).convert("RGB")
if __name__ == "__main__":
    if sys.argv[1] == "still":
        ims = []
        for s in sys.argv[2:]:
            _rd.clear(); ims.append(frame(float(s)).resize((640, 360)))
        sh = Image.new("RGB", (640 * 4, 360 * ((len(ims) + 3) // 4)))
        for j, im in enumerate(ims): sh.paste(im, (j % 4 * 640, j // 4 * 360))
        sh.save(f"{HERE}/test.jpg", quality=88)
    else:
        n = int(round(DUR * FPS)); out = f"{HERE}/gfx.mp4"
        p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", out + ".tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(n): p.stdin.write(frame(i / FPS).tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace(out + ".tmp.mp4", out)
