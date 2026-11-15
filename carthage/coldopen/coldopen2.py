"""Cold open, variant A: the first 17 s run over reconstruction footage, text in the lower third."""
import sys, subprocess, os, numpy as np
from PIL import Image, ImageDraw
import coldopen as c
from coldopen import W, H, FPS, DUR, BG, WHITE, text, plaque, r, win, font, tw, LOGO
REC = "../film/rec"; LIGHT = (205, 205, 200)
SEG = [("R05", 0.5, 0.0, 3.1), ("R22", 0.8, 3.1, 7.95), ("R06", 4.0, 7.95, 10.55), ("R18", 7.2, 10.55, 13.0), ("R24", 1.0, 13.0, 17.1)]
T_END = 17.1
_g = np.linspace(0, 1, 520)[:, None, None] ** 1.05 * 0.93                      # dark band for the lower third
class Reader:
    def __init__(s, name, ss, n):
        s.p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", str(ss), "-i", f"{REC}/{name}.mp4", "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1", "-frames:v", str(n + 2),
                                "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE); s.last = None
    def get(s):
        b = s.p.stdout.read(W * H * 3)
        if len(b) == W * H * 3: s.last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        return s.last
_rd = {}
def base(i):
    t = i / FPS
    for k, (n, ss, a, b) in enumerate(SEG):
        if a <= t < b:
            if k not in _rd: _rd[k] = Reader(n, ss + (t - a), int((b - t) * FPS))
            f = _rd[k].get().astype(np.float32)
            f[H - 520:] = f[H - 520:] * (1 - _g) + np.array(BG, np.float32) * _g
            k2 = min(1.0, (T_END - t) / 0.35, (t + 0.001) / 0.3 if a == 0 else 1.0)       # fade in at the start, out to black at the end
            if k2 < 1: f = f * k2 + np.array(BG, np.float32) * (1 - k2)
            return Image.fromarray(f.astype(np.uint8))
def frame2(i):
    t = i / FPS
    if t >= T_END: return c.frame(t)
    im = base(i); d = ImageDraw.Draw(im); cx = W // 2
    a = win(t, 0.1, 4.45)
    if a > 0:
        text(d, cx, 860, "ALMOST EVERYTHING YOU KNOW ABOUT CARTHAGE", 56, a * r(t, 0.3), sp=3)
        f = font(True, 56); w1 = tw(d, "WAS WRITTEN BY THE PEOPLE WHO", f, 3); w2 = tw(d, "DESTROYED IT", f, 3); gap = 56; x0 = cx - (w1 + gap + w2) / 2
        text(d, x0, 965, "WAS WRITTEN BY THE PEOPLE WHO", 56, a * r(t, 2.2), sp=3, anchor="l")
        plaque(d, x0 + w1 + gap, 965, "DESTROYED IT", 56, a * r(t, 3.2, 0.2), sp=3, anchor="l")
    a = win(t, 4.8, 7.75)
    if a > 0:
        f = font(True, 76); w = tw(d, "IN THE NEXT 20 MINUTES", f, 2); x0 = cx - (150 + w) / 2
        lg = LOGO.resize((120, 120), Image.LANCZOS)
        if a < 1: lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        im.paste(lg, (int(x0), 835), lg)
        text(d, x0 + 150, 880, "IN THE NEXT 20 MINUTES", 76, a * r(t, 4.9), anchor="l", sp=2)
        text(d, x0 + 154, 970, "WHAT THEY LEFT OUT", 38, a * r(t, 6.3), anchor="l", sp=6, color=LIGHT, bold=False)
    for k, (t0, t1, s) in enumerate([(7.95, 10.55, "A CONSTITUTION ARISTOTLE ADMIRED"), (10.55, 13.0, "A WAR ROME VERY NEARLY LOST"), (13.0, 16.75, "THE ONE BOOK ROME SAVED FROM THE FIRE")]):
        a = win(t, t0, t1, fi=0.2, fo=0.2 if k < 2 else 0.3)
        if a > 0:
            f = font(True, 62); w = tw(d, s, f, 3); x0 = cx - (110 + w) / 2
            text(d, x0, 950, f"0{k + 1}", 62, a, anchor="l", color=LIGHT)
            text(d, x0 + 110, 950, s, 62, a, anchor="l", sp=3)
    return im
if __name__ == "__main__":
    if sys.argv[1] == "still":
        ims = []
        for s in sys.argv[2:]:
            _rd.clear(); ims.append(frame2(int(float(s) * FPS)).resize((640, 360)))
        sh = Image.new("RGB", (640 * 4, 360 * ((len(ims) + 3) // 4)))
        for j, im in enumerate(ims): sh.paste(im, (j % 4 * 640, j // 4 * 360))
        sh.save("test2.jpg", quality=88)
    else:
        n = int(round(DUR * FPS))
        p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", "gfx2.tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(n): p.stdin.write(frame2(i).tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace("gfx2.tmp.mp4", "gfx2.mp4")
