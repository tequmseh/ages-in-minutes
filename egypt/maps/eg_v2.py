"""Egypt maps, second edition: the accepted map look + scenes re-timed to the new voiceover (v2 script).
The original scenes are not rewritten: each is played through a piecewise-linear time warp (old scene time -> new chapter time).
usage: python3 eg_v2.py list | still name@t,t (new clip time) | sheet | render names..."""
import sys, os, numpy as np, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.append(os.path.join(HERE, "../../carthage/maps"))
import look, engine
engine.FPS = 60                      # series standard since episode 2: maps in true 60 fps
from PIL import Image
# the Sahara stays sand: green mottle only outside the desert polygon
_style0 = look.style
def base_image(cam, lm, desert=None):
    mot, grn = look.terrain(cam)
    if desert is not None:
        dz = np.asarray(desert.resize(lm.size), np.float32) / 255
        grn = grn * (1 - dz) * 1.25 + grn * dz * 0.10
    a, _ = look.style(lm, mot, np.clip(grn, 0, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
engine.base_image = base_image
src = open(os.path.join(HERE, "eg_scenes.py")).read().split('if __name__ == "__main__":')[0]
for a, b in (('"WARDING OFF THE BOWS"', '"SUBDUER OF THE NUBIANS"'), ('fr.plaque(x - 236, y + 34,', 'fr.plaque(x - 250, y + 34,'), ('"24 AUGUST AD 394"', '"AD 394"'),
             ('site("MEIDUM", 27.5, 7, "1", 20)', 'site("MEIDUM", 27.5, 7, "RUIN", 18)'), ('"2 · BENT"', '"BENT"'), ('site("REDP", 38.5, 7, "3", 20, -9)', 'site("REDP", 38.5, 7, "THE THIRD", 18, -9)')):
    assert src.count(a) == 1, a; src = src.replace(a, b)
ns = {"__name__": "eg_scenes_v2"}; exec(compile(src, "eg_scenes_v2", "exec"), ns); SC0 = ns["SC"]
FPS, W, H = engine.FPS, engine.W, engine.H

# name: (chapter, [(old scene t, new voiceover t), ...]); equal old values in a row = hold
A = {
 "00_cold_open": (0, [(0, 10.4), (6.2, 18.0), (17, 23.0)]),
 "01_the_gift": (1, [(0, 0), (0.5, 1.7), (7.0, 5.9), (12.0, 10.6), (14.6, 12.9), (16.8, 15.0), (20.4, 17.2), (24.0, 20.0), (27.6, 21.4), (30.2, 25.0), (33.0, 27.5), (34.2, 30.3),
                     (38.0, 33.3), (39.2, 34.6), (39.2, 53.0), (42.0, 53.8), (44.0, 55.4), (46.0, 56.7), (49.2, 60.6), (50.0, 61.5), (51.2, 62.6), (54.0, 67.0), (56.8, 70.5), (79, 86.5)]),
 "02a_two_lands": (2, [(0, 0), (4, 4.1), (8, 7.0), (12, 11.1), (15, 14.0), (17, 16.5)]),
 "02b_two_lands": (2, [(0, 46.4), (5, 51.4)]),
 "03_the_pyramid_age": (3, [(0, 4.6), (17, 21.2), (27.5, 31.7), (36, 35.9), (38.5, 41.7), (44, 47.0), (47, 50.5), (48, 52.7), (49.5, 54.2), (53, 56.4), (61, 62.5), (62, 63.5), (62, 79.6),
                            (82.5, 80.3), (86.5, 83.0), (88, 84.0), (90.4, 86.0), (93.4, 88.2), (94, 89.0), (99, 91.6), (106, 98.5)]),
 "04_the_first_collapse": (4, [(0, 39.8), (3, 43.0), (9, 49.5), (14, 53.4), (15.6, 55.0), (35.2, 72.3), (38, 84.75)]),
 "05_the_reboot": (5, [(0, 8.8), (1, 12.5), (5, 14.5), (7.2, 16.6), (10.2, 17.7), (15.2, 23.5), (16, 24.5), (16, 52.3), (41.0, 52.8), (44.2, 55.6), (45.2, 57.0), (47.8, 60.0), (52, 62.5), (54, 65.6)]),
 "06_foreign_kings": (6, [(0, 0), (0.8, 4.9), (7.4, 9.6), (14.6, 12.3), (15, 12.6), (18, 16.9), (22.4, 20.6), (23, 22.3), (30, 28.9), (31, 30.0), (31, 46.7), (49, 47.2), (51.4, 49.4), (51.6, 51.0),
                          (52.2, 51.5), (55, 53.7), (56.85, 55.6), (57.5, 56.5), (57.5, 76.9), (68.2, 77.4), (70.4, 79.5), (72.0, 83.0), (73.2, 84.3), (86, 94.5)]),
 "07_the_empire": (7, [(0, 0), (11, 10.2), (14.2, 14.0), (16, 15.0), (23.4, 22.6), (24.3, 23.8), (25, 25.2), (26, 26.5), (26, 43.0), (43.2, 43.5), (46.4, 46.6), (47, 47.5), (47, 56.6),
                       (60, 57.0), (62.4, 59.4), (65, 62.0), (66, 63.0), (66, 76.5), (83.5, 77.2), (85, 79.0), (85, 92.18)]),
 "08a_the_heretic": (8, [(0, 23.9), (1.2, 25.8), (5, 28.3)]),
 "08b_the_heretic": (8, [(0, 53.6), (3.2, 58.0), (11, 64.9)]),
 "09a_the_superpower": (9, [(0, 15.0), (6.2, 21.3), (10.5, 27.4), (12.5, 28.9), (15, 29.4), (17, 30.8), (20, 32.2), (22, 33.7)]),
 "09b_the_superpower": (9, [(0, 59.4), (9, 66.3)]),
 "09c_the_superpower": (9, [(0, 66.3), (1.9, 69.9), (3.6, 71.5), (6, 74.0)]),
 "10a_the_long_decline": (10, [(0, 2.7), (5, 8.5), (10, 10.9), (14.2, 15.2), (26, 26.2), (28, 28.2)]),
 "10b_the_long_decline": (10, [(0, 63.4), (7, 70.6)]),
 "10c_the_long_decline": (10, [(0, 74.9), (3.2, 78.2), (4.6, 81.5), (5.8, 82.7), (15.2, 88.5), (17.3, 90.2), (19, 92.5)]),
 "11a_other_peoples_egypt": (11, [(0, 7.1), (7, 10.4), (15, 16.0), (19.5, 21.0), (26, 27.8)]),
 "11b_other_peoples_egypt": (11, [(0, 44.9), (3, 46.6), (11, 51.0), (13, 53.8)]),
 "12a_what_remains": (12, [(0, 19.3), (0.6, 21.5), (3, 24.0), (9, 26.6), (13.2, 31.5), (16, 34.1)]),
 "12b_what_remains": (12, [(0, 53.8), (1.8, 56.4), (5.2, 58.8), (6.4, 60.5), (8, 62.5), (37, 89.6)]),
}
class Warp:
    def __init__(s, name):
        s.name = name; s.sc = SC0[name]; s.ch, an = A[name]; s.t0 = an[0][1]; s.dur = round(an[-1][1] - an[0][1], 2)
        s.old = [a for a, _ in an]; s.new = [b - s.t0 for _, b in an]
        assert all(b2 >= b1 for b1, b2 in zip(s.new, s.new[1:])) and all(a2 >= a1 for a1, a2 in zip(s.old, s.old[1:])), name
    def w(s, t):
        for (a1, b1), (a2, b2) in zip(zip(s.old, s.new), zip(s.old[1:], s.new[1:])):
            if t <= b2: return a1 if b2 == b1 else a1 + (a2 - a1) * (t - b1) / (b2 - b1)
        return s.old[-1]
    def frame(s, t): return s.sc.frame(round(s.w(t), 4))
    def still(s, t, path, scale=0.5):
        im = s.frame(t); im.resize((int(W * scale), int(H * scale)), Image.LANCZOS).save(path)
    def render(s, outdir):
        n = int(round(s.dur * FPS)); final = os.path.join(outdir, s.name + ".mp4"); tmp = final[:-4] + ".tmp.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an", tmp], stdin=subprocess.PIPE)
        s.sc.frame(0.0); ps, pb = None, None
        for k in range(n):
            to = round(s.w(k / FPS), 4); sig = s.sc.sig(to)
            if sig == ps: p.stdin.write(pb); continue
            pb = s.frame(k / FPS).tobytes(); ps = sig; p.stdin.write(pb)
        p.stdin.close()
        if p.wait() == 0: os.rename(tmp, final)
SC = {n: Warp(n) for n in A}
if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "list":
        for n, s in SC.items(): print(f"{n:28s} ch{s.ch:02d}  VO {s.t0:6.1f} - {s.t0 + s.dur:6.1f}  ({s.dur:5.1f} s)")
        print("total", round(sum(s.dur for s in SC.values()), 1))
    elif mode == "still":
        for spec in sys.argv[2:]:
            n, ts = spec.split("@")
            for tt in ts.split(","): SC[n].still(float(tt), f"{HERE}/test_look/{n}_{float(tt):05.1f}.png")
    elif mode == "sheet":
        from PIL import ImageDraw
        names = sys.argv[2:] or list(SC); ims = []
        for n in names:
            s = SC[n]
            for f in (0.45, 0.97):
                im = s.frame(s.dur * f).resize((640, 360), Image.LANCZOS); ImageDraw.Draw(im).rectangle([0, 0, 330, 24], fill=(17, 17, 17))
                ImageDraw.Draw(im).text((6, 5), f"{n}  VO {s.t0 + s.dur * f:5.1f}", fill=(255, 255, 255)); ims.append(im)
        cols = 6; sh = Image.new("RGB", (cols * 640, ((len(ims) + cols - 1) // cols) * 360), (17, 17, 17))
        for i, im in enumerate(ims): sh.paste(im, (i % cols * 640, i // cols * 360))
        sh.save(f"{HERE}/test_look/sheet.jpg", quality=86)
    else:
        import time
        for n in sys.argv[2:]:
            t0 = time.time(); SC[n].render(f"{HERE}/out_look"); print(n, round(time.time() - t0, 1), flush=True)
