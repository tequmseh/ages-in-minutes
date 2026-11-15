from gfxlib import *
import os
R = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(R)
def gfx(t):
    im, d = blank(); cx = W // 2
    a = win(t, 0.0, 5.0, fi=0.15, fo=0.25)
    if a > 0:
        text(d, cx, 440, "THE PART THE ROMANS DID NOT EXPECT", 40, a * r(t, 0.15), sp=8, color=GRAY, bold=False)
        plaque(d, cx, 580, "CARTHAGE RECOVERS", 96, a * r(t, 3.33), sp=4)
    a = win(t, 13.0, 18.0, fi=0.2, fo=0.2)
    if a > 0:
        text(d, cx, 470, "EXILE", 150, a * r(t, 14.0), sp=14, dy=18)
        plaque(d, cx, 650, "183 BC", 70, a * r(t, 16.9), sp=4)
    a = win(t, 25.0, 27.0, fi=0.15, fo=0.15)
    if a > 0:
        text(d, cx, 440, "A ROMAN SENATOR", 40, a * r(t, 25.05), sp=8, color=GRAY, bold=False)
        text(d, cx, 580, "CATO", 170, a * r(t, 25.9), sp=14, dy=18)
    a = win(t, 37.0, 50.0, fi=0.2, fo=0.01)
    if a > 0:
        text(d, cx, 300, "EVERY VOTE, ON ANY SUBJECT, ENDS THE SAME WAY", 36, a * r(t, 37.1), sp=7, color=GRAY, bold=False)
        plaque(d, cx, 480, "CARTHAGE MUST BE DESTROYED", 92, a * r(t, 41.26, 0.25), sp=4)
        s2 = "CARTHAGE MUST BE SPARED"; a2 = a * r(t, 46.29)
        text(d, cx, 680, s2, 70, a2 * (1 - 0.5 * r(t, 48.3)), sp=4, color=GRAY)
        strike(d, cx, 680, s2, 70, ease((t - 48.3) / 0.45), a, sp=4, color=GRAY)
        text(d, cx, 820, "CATO WINS", 44, a * r(t, 48.5), sp=10)
    return im
SPEC = dict(n=11, card=f"{C}/out/carthage_chapter_11_carthage_must_be_destroyed.mp4", gfx=gfx,
            gfx_windows=[(0, 5.1), (12.9, 18.1), (24.9, 27.1), (36.9, 50.1)],
            overlays=[(f"{R}/rec/R19.mp4", 5.0, 13.0, True), (f"{R}/rec/R20.mp4", 18.0, 25.0, True), (f"{R}/rec/R21.mp4", 27.0, 37.0, True),
                      (f"{C}/maps/out/11_carthage_must_be_destroyed.mp4", 50.0, 89.0, False), (f"{R}/rec/R22.mp4", 89.0, 96.84, True)])
