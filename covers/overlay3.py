"""Cover overlay, v3: black band + one universal timeline 3500 BC -> today, labels above the line on black plaques, no title.
usage: python3 overlay3.py universal            -> the same file for every cover (millennia labelled, nothing highlighted)
       python3 overlay3.py span NAME -814 -146  -> the same scale with one period highlighted in yellow
Output: 1920x1080 transparent PNG; set COVER_4K=1 for 3840x2160."""
from PIL import Image, ImageDraw, ImageFont
import sys, os
import os as _os
W, H = (3840, 2160) if _os.environ.get("COVER_4K") else (1920, 1080); SS = 2
K = W / 1280
X0, X1 = 44 * K, 1236 * K; Y0, Y1 = -3500, 2000
YEL = (242, 194, 48, 255); WHITE = (244, 242, 236, 255); GREY = (176, 180, 186, 255); BLACK = (17, 17, 17, 255)
FONT = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
def X(y): return X0 + (y - Y0) / (Y1 - Y0) * (X1 - X0)
def lab(y): return f"{-y} BC" if y < 0 else f"AD {y}"
def overlay(span=None):
    im = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im); s = lambda v: int(round(v * SS))
    line = H - 132 * K; f = ImageFont.truetype(FONT, s(19 * K)); ly = line - 24 * K
    d.rectangle([0, s(line), s(W), s(H)], fill=BLACK)
    d.rectangle([s(X0), s(line - 1.5 * K), s(X1), s(line + 1.5 * K)], fill=WHITE)
    def text(x, t, fill, anchor):
        tw = d.textlength(t, font=f) / SS; l = {"l": x, "r": x - tw, "m": x - tw / 2}[anchor]
        d.rectangle([s(l - 8 * K), s(ly - 24 * K), s(l + tw + 8 * K), s(ly + 6 * K)], fill=BLACK); d.text((s(l), s(ly)), t, font=f, fill=fill, anchor="ls"); return l - 8 * K, l + tw + 8 * K
    for y in range(Y0, Y1 + 1, 500):
        if span and min(abs(X(y) - X(span[0])), abs(X(y) - X(span[1]))) < 12 * K: continue
        h = (11 if y % 1000 == 0 else 6) * K
        d.rectangle([s(X(y) - 1.5 * K), s(line - h), s(X(y) + 1.5 * K), s(line + h)], fill=WHITE)
    occ = []
    if span:
        a, b = span; xa, xb = X(a), X(b)
        d.rectangle([s(xa), s(line - 5 * K), s(xb), s(line + 5 * K)], fill=YEL)
        for x in (xa, xb): d.rectangle([s(x - 2 * K), s(line - 14 * K), s(x + 2 * K), s(line + 14 * K)], fill=YEL)
        t = f"{lab(a).replace(' BC', '') if b < 0 else lab(a)}–{b if a > 0 else lab(b)}"; tw = d.textlength(t, font=f) / SS
        cx = min(max((xa + xb) / 2, X0 + tw / 2), X1 - tw / 2); occ.append(text(cx, t, YEL, "m"))
        marks = [(X0, "3500 BC", "l"), (X1, "TODAY", "r")]
    else:
        marks = [(X0, "3500 BC", "l"), (X(-2000), "2000 BC", "m"), (X(-1000), "1000 BC", "m"), (X(0), "AD 1", "m"), (X(1000), "AD 1000", "m"), (X1, "TODAY", "r")]
    for x, t, anc in marks:
        tw = d.textlength(t, font=f) / SS; l = {"l": x, "r": x - tw, "m": x - tw / 2}[anc]
        if all(l + tw + 30 * K < o[0] or l - 30 * K > o[1] for o in occ): text(x, t, GREY, anc)
    return im.resize((W, H), Image.LANCZOS)
if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__)); SUF = "_4k" if W == 3840 else ""
    if sys.argv[1] == "universal": overlay().save(f"{out}/overlay_universal{SUF}.png")
    else: overlay((int(sys.argv[3]), int(sys.argv[4]))).save(f"{out}/overlay_{sys.argv[2]}{SUF}.png")
