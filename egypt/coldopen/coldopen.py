"""Egypt cold open (48.27 s): reconstruction footage + the cold-open map, text in the lower third, 60 fps.
python3 coldopen.py still 2 7 ...   -> contact sheet;   python3 coldopen.py   -> ../film/out/ch00.mp4 (2560x1440, voice + music)"""
import sys, subprocess, os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
W, H, FPS, DUR = 1920, 1080, 60, 48.27
BG = (17, 17, 17); WHITE = (242, 240, 235); LIGHT = (205, 205, 200); ACC = (242, 194, 48)
FB = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"; FR = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
HERE = os.path.dirname(os.path.abspath(__file__)); REC = f"{HERE}/../film/rec"; MAP = f"{HERE}/../maps/out_look/00_cold_open.mp4"
LOGO = Image.open(f"{HERE}/../../channel/logo_mark_transparent.png").convert("RGBA")
_f = {}
def font(b, s):
    k = (b, int(s))
    if k not in _f: _f[k] = ImageFont.truetype(FB if b else FR, int(s))
    return _f[k]
def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
def r(t, t0, d=0.35): return ease((t - t0) / d)
def win(t, a, b, fi=0.25, fo=0.25): return max(0.0, min(1.0, (t - a) / fi, (b - t) / fo))
def tw(d, s, f, sp=0): return sum(d.textlength(ch, font=f) + sp for ch in s) - sp
def text(d, x, y, s, size, a=1.0, bold=True, color=WHITE, anchor="m", sp=0):
    if a <= 0: return
    f = font(bold, size); w = tw(d, s, f, sp); x0 = x - w / 2 if anchor == "m" else (x - w if anchor == "r" else x)
    for ch in s:
        d.text((x0, y - size * 0.6), ch, font=f, fill=color + (int(255 * a),)); x0 += d.textlength(ch, font=f) + sp
def plaque(d, x, y, s, size, a=1.0, sp=2, anchor="m", fg=BG, bg=WHITE):
    if a <= 0: return
    f = font(True, size); w = tw(d, s, f, sp); px, py = size * 0.45, size * 0.32; x0 = x - w / 2 if anchor == "m" else x
    d.rectangle([x0 - px, y - size * 0.6 - py, x0 + w + px, y + size * 0.6 + py], fill=bg + (int(255 * a),))
    for ch in s:
        d.text((x0, y - size * 0.6), ch, font=f, fill=fg + (int(255 * a),)); x0 += d.textlength(ch, font=f) + sp

# (source, start inside the source, window in the voice track, dark band for text)
SEG = [("R02", 0.4, 0.0, 5.18, True), ("R01", 6.4, 5.18, 10.5, True), ("MAP", 0.0, 10.5, 23.03, False),
       ("R03", 1.0, 23.03, 26.30, True), ("R13", 2.0, 26.30, 28.71, True), ("R08", 3.0, 28.71, 30.71, True),
       ("R10", 1.0, 30.71, 33.41, True), ("R06a", 1.0, 33.41, 35.91, True), ("R06b", 0.6, 35.91, 42.51, True), ("R05", 1.5, 42.51, DUR + 0.1, True)]
BAND = 520; _g = (np.linspace(0, 1, BAND)[:, None, None] ** 1.05 * 0.93).astype(np.float32); _bg = np.array(BG, np.float32)
class Reader:
    def __init__(s, name, ss, n):
        src = MAP if name == "MAP" else f"{REC}/{name}.mp4"
        s.p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", f"{ss:.3f}", "-i", src, "-vf",
                                f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1",   # 24 fps -> 60 by frame repetition
                                "-frames:v", str(n + 3), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE); s.last = None
    def get(s):
        b = s.p.stdout.read(W * H * 3)
        if len(b) == W * H * 3: s.last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        return s.last
_rd = {}
def base(i):
    t = i / FPS
    for k, (n, ss, a, b, band) in enumerate(SEG):
        if a <= t < b:
            if k not in _rd: _rd[k] = Reader(n, ss + (t - a), int((b - t) * FPS))
            f = _rd[k].get().astype(np.float32)
            if band: f[H - BAND:] = f[H - BAND:] * (1 - _g) + _bg * _g
            k2 = min(1.0, (t + 0.001) / 0.35, (DUR - t) / 0.5)
            if k2 < 1: f = f * k2 + _bg * (1 - k2)
            return Image.fromarray(f.astype(np.uint8)).convert("RGBA")
# timeline of the opening line: pyramid ... Cleopatra ... Moon landing, to scale (2560 BC, 69 BC, AD 1969)
TX0, TX1, TY = 300, 1620, 930; TXC = TX0 + (2560 - 69) / (2560 + 1969) * (TX1 - TX0)
LIST = [(24.52, 26.30, "A RIVER THAT BUILDS A COUNTRY"), (26.30, 28.71, "THREE COLLAPSES, THREE COMEBACKS"), (28.71, 30.71, "A WOMAN WHO MAKES HERSELF KING"),
        (30.71, 33.41, "A PHARAOH WHO TRIES TO ABOLISH THE OLD GODS"), (33.41, 35.91, "THE PEOPLE WHO REALLY BUILT THE PYRAMIDS")]
SAME = [(12.92, "ONE STATE"), (13.9, "THE SAME GODS"), (15.1, "THE SAME SCRIPT"), (16.3, "THE SAME IDEA OF A KING")]
def frame(i):
    t = i / FPS; im = base(i); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); cx = W // 2
    a = win(t, 0.15, 10.35)
    if a > 0:                                                   # 1. the comparison
        def dot(x, k):
            if k > 0: d.ellipse([x - 11, TY - 11, x + 11, TY + 11], fill=ACC + (int(255 * a * k),))
        k_m = r(t, 2.3, 0.9); k_p = r(t, 3.5, 1.0)
        if k_m > 0: d.rectangle([TXC, TY - 3, TXC + (TX1 - TXC) * k_m, TY + 3], fill=ACC + (int(255 * a),))
        if k_p > 0: d.rectangle([TXC - (TXC - TX0) * k_p, TY - 3, TXC, TY + 3], fill=ACC + (int(255 * a),))
        dot(TXC, r(t, 0.2)); dot(TX1, r(t, 3.0)); dot(TX0, r(t, 4.3))
        text(d, TXC, TY - 62, "CLEOPATRA", 44, a * r(t, 0.2), sp=3)
        text(d, TX1, TY - 62, "MOON LANDING", 44, a * r(t, 2.6), sp=3)
        text(d, TX0, TY - 62, "GREAT PYRAMID", 44, a * r(t, 4.0), sp=3)
        text(d, (TXC + TX1) / 2, TY + 48, "CLOSER", 30, a * r(t, 1.2) * (1 if t < 8.3 else 1), bold=False, color=LIGHT, sp=6)
        text(d, (TX0 + TXC) / 2, TY + 48, "ALREADY ANCIENT HISTORY", 30, a * r(t, 6.6), bold=False, color=LIGHT, sp=6)
    for k, (t0, s) in enumerate(SAME):                          # 2. over the map
        a = r(t, t0, 0.3) * win(t, 12.5, 22.85)
        plaque(d, 150, 590 + k * 92, s, 40, a, sp=3, anchor="l", fg=WHITE, bg=BG)
    a = win(t, 23.1, 24.42, fo=0.15)
    if a > 0:                                                   # 3. the promise
        f = font(True, 76); w = tw(d, "IN THE NEXT 20 MINUTES", f, 2); x0 = cx - (150 + w) / 2
        lg = LOGO.resize((120, 120), Image.LANCZOS); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a))); ov.alpha_composite(lg, (int(x0), 880))
        text(d, x0 + 150, 940, "IN THE NEXT 20 MINUTES", 76, a, anchor="l", sp=2)
    for k, (t0, t1, s) in enumerate(LIST):
        a = win(t, t0, t1, fi=0.18, fo=0.15 if k < 4 else 0.25)
        if a > 0:
            sz = 60 if len(s) < 36 else 54; f = font(True, sz); w = tw(d, s, f, 3); x0 = cx - (105 + w) / 2
            text(d, x0, 950, f"0{k + 1}", sz, a, anchor="l", color=LIGHT); text(d, x0 + 105, 950, s, sz, a, anchor="l", sp=3)
    a = win(t, 35.95, 42.35)
    if a > 0:                                                   # 4. the builders
        f = font(True, 60); w1 = tw(d, "THEY WERE", f, 3); w2 = tw(d, "NOT SLAVES", f, 3); x0 = cx - (w1 + 50 + w2) / 2
        k1 = a * (1 - r(t, 39.75, 0.25))
        text(d, x0, 890, "THEY WERE", 60, k1 * r(t, 35.95, 0.25), anchor="l", sp=3); plaque(d, x0 + w1 + 50, 890, "NOT SLAVES", 60, k1 * r(t, 36.3, 0.2), sp=3, anchor="l")
        text(d, cx, 985, "THEY ATE BEEF, AND THEY NAMED THEIR WORK GANGS", 38, k1 * r(t, 37.3), bold=False, color=LIGHT, sp=5)
        k2 = a * r(t, 40.0, 0.3)
        text(d, cx, 880, "ONE WAS CALLED", 38, k2, bold=False, color=LIGHT, sp=6); text(d, cx, 965, "THE DRUNKARDS OF MENKAURE", 66, k2 * r(t, 40.7, 0.3), sp=3)
    a = win(t, 42.6, 45.95)
    if a > 0:                                                   # 5. the question, then the title
        text(d, cx, 885, "HOW DO YOU MAKE A COUNTRY LAST", 58, a * r(t, 42.6), sp=3); plaque(d, cx, 985, "3,000 YEARS?", 62, a * r(t, 44.4, 0.25), sp=3)
    a = r(t, 46.1, 0.3)
    if a > 0:
        f = font(True, 84); s = "ANCIENT EGYPT"; w = tw(d, s, f, 4); x0 = cx - (165 + w) / 2
        lg = LOGO.resize((135, 135), Image.LANCZOS); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a))); ov.alpha_composite(lg, (int(x0), 862))
        text(d, x0 + 165, 905, s, 84, a, anchor="l", sp=4); text(d, x0 + 169, 990, "IN 20 MINUTES", 44, a * r(t, 47.1), anchor="l", sp=8, color=LIGHT, bold=False)
    k2 = min(1.0, (t + 0.001) / 0.35, (DUR - t) / 0.5)
    if k2 < 1: ov.putalpha(ov.getchannel("A").point(lambda v: int(v * k2)))
    im.alpha_composite(ov); return im.convert("RGB")
def loud(f):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    return json.loads(e[e.rindex("{"):e.rindex("}") + 1])
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "still":
        ims = []
        for s in sys.argv[2:]:
            _rd.clear(); ims.append(frame(int(float(s) * FPS)).resize((640, 360), Image.LANCZOS))
        sh = Image.new("RGB", (640 * 4, 360 * ((len(ims) + 3) // 4)))
        for j, im in enumerate(ims): sh.paste(im, (j % 4 * 640, j // 4 * 360))
        sh.save(f"{HERE}/test.jpg", quality=88); sys.exit()
    gfx = f"{HERE}/gfx.mp4"; n = int(round(DUR * FPS))
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", "scale=2560:1440:flags=lanczos", "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-profile:v", "high", "-bf", "2", "-g", "60", "-pix_fmt", "yuv420p", gfx + ".tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(gfx + ".tmp.mp4", gfx)
    vo = f"{HERE}/../film/vo/00.mp3"; mu = f"{HERE}/../film/music/coldopen.wav"; m = loud(vo); g = -28.0 - float(loud(mu)["input_i"])     # music 14 dB under the voice
    out = f"{HERE}/../film/out/ch00.mp4"
    fc = (f"[1:a]loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000[vo];"
          f"[2:a]aresample=48000,volume={g:.2f}dB,afade=t=in:d=0.4,afade=t=out:st={DUR - 1.6:.2f}:d=1.6[mu];[vo][mu]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.84,aformat=channel_layouts=stereo[a]")
    rr = subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", gfx, "-i", vo, "-i", mu, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                         "-t", f"{DUR:.3f}", "-movflags", "+faststart", out + ".tmp.mp4"], capture_output=True, text=True)
    assert rr.returncode == 0, rr.stderr[-2000:]
    os.replace(out + ".tmp.mp4", out); print(out, "music gain dB", round(g, 2))
