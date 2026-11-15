import json, math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "../../maps/data"))
W, H, FPS, SS = 1920, 1080, 30, 2
SAFE = 110                       # bottom strip kept free of labels (timeline goes there)
SEA = (220, 238, 243); LAND = (243, 226, 188); INK = (17, 17, 17)
OCHRE = (217, 164, 65); OCHRE_L = (243, 223, 178); GRAY = (154, 165, 171)
YELLOW = (241, 194, 46); RIVER = (128, 190, 212); COAST = (190, 208, 214)
K = math.cos(math.radians(35))
SAND = (243, 223, 178); GREEN = (59, 143, 124); GREEN_L = (158, 206, 192); SLATE = (118, 132, 140); SLATE_L = (203, 211, 215); BROWN = (150, 120, 96)
FLOOD = (112, 178, 205)
FD = "/usr/share/fonts/opentype/inter/"
_fc = {}
def font(w, size):
    key = (w, size)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(FD + {"r": "Inter-Regular.otf", "m": "Inter-Medium.otf", "s": "Inter-SemiBold.otf", "b": "Inter-Bold.otf"}[w], size)
    return _fc[key]

# ---------------- data ----------------
HOLES = []
def _rings(path, box=(0, 6, 98, 58), holes=False):
    out = []
    for f in json.load(open(path))["features"]:
        g = f["geometry"]
        polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for p in polys:
            a = np.asarray(p[0], dtype=np.float64)[:, :2]
            if a[:, 0].max() < box[0] or a[:, 0].min() > box[2] or a[:, 1].max() < box[1] or a[:, 1].min() > box[3]:
                continue
            out.append(a)
            if holes:
                for h in p[1:]:
                    hh = np.asarray(h, dtype=np.float64)[:, :2]
                    if hh[:, 0].max() - hh[:, 0].min() > 1.5 and 20 < hh[:, 0].mean() < 80: HOLES.append(hh)
    return out
LAND50 = _rings(DATA + "/land50.geojson")
LAND10 = _rings(DATA + "/ne_10m_land.geojson", holes=True)
def _chaikin(a, n=2):
    for _ in range(n):
        b = np.roll(a, -1, axis=0)
        a = np.stack([0.75 * a + 0.25 * b, 0.25 * a + 0.75 * b], 1).reshape(-1, 2)
    return a
def _lakes():
    keep = ("Caspian", "Aral", "Van", "Urmia", "Dead Sea", "Sevan", "Tuz")
    out = []
    for f in json.load(open(DATA + "/ne_10m_lakes.geojson"))["features"]:
        n = f["properties"].get("name") or ""; g = f["geometry"]
        if not g or not any(k in n for k in keep): continue
        polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for p in polys:
            a = np.asarray(p[0], dtype=np.float64)[:, :2]
            if 20 < a[:, 0].mean() < 80 and 20 < a[:, 1].mean() < 50: out.append(a)
    return out
LAKES = _lakes()
RIVER_NAMES = {"Nile", "Rosetta Branch", "Damietta Branch", "Indus", "Firat", "Al Furat", "Euphrates", "Dicle", "Tigris", "Shatt al Arab", "Danube", "Donau", "Dunaj", "Duna", "Dunav", "Dunărea",
               "Amu Darya", "Syr Darya", "Kizilirmak", "Kızılırmak", "Karun", "Helmand", "Kura", "Aras", "Jordan"}
def _rivers():
    out = []
    for f in json.load(open(DATA + "/ne_10m_rivers_lake_centerlines.geojson"))["features"]:
        g = f["geometry"]
        if not g or f["properties"].get("name") not in RIVER_NAMES: continue
        for l in ([g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]):
            a = np.asarray(l, dtype=np.float64)[:, :2]
            if 10 < a[:, 0].mean() < 82 and 15 < a[:, 1].mean() < 50 and len(a) > 2: out.append(a)
    return out
RIVERS = _rivers()
# ---------------- camera ----------------
def cam_full():            # whole country, same framing everywhere
    return (47.0, 32.4, 35.0)
def proj(cam, pts, ss=SS):
    clon, clat, S = cam
    a = np.asarray(pts, dtype=np.float64).reshape(-1, 2)
    x = (a[:, 0] - clon) * K * S + W / 2
    y = (clat - a[:, 1]) * S + H / 2
    return np.stack([x, y], 1) * ss
def P(cam, lon, lat):
    x, y = proj(cam, [(lon, lat)], 1)[0]
    return float(x), float(y)
def lerp_cam(a, b, p):
    p = ease(p)
    S = math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * p)
    # move the centre in screen-proportional way so zoom feels steady
    q = 0 if abs(b[2] - a[2]) < 1e-6 else (1 / a[2] - 1 / S) / (1 / a[2] - 1 / b[2])
    q = p if abs(b[2] - a[2]) < 1e-6 else q
    return (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q, S)
def ease(p):
    p = max(0.0, min(1.0, p)); return p * p * (3 - 2 * p)
def ramp(t, t0, d=0.6):
    return ease((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)

# ---------------- base raster ----------------
def _draw_polys(d, cam, rings, fill, minpx=3.0):
    for a in rings:
        p = proj(cam, a)
        if p[:, 0].max() < -50 or p[:, 0].min() > W * SS + 50 or p[:, 1].max() < -50 or p[:, 1].min() > H * SS + 50: continue
        if (p[:, 0].max() - p[:, 0].min()) < minpx * SS and (p[:, 1].max() - p[:, 1].min()) < minpx * SS: continue
        d.polygon(list(map(tuple, p)), fill=fill)
def _chaikin_open(a, n=2):
    for _ in range(n):
        p, q = a[:-1], a[1:]
        mid = np.stack([0.75 * p + 0.25 * q, 0.25 * p + 0.75 * q], 1).reshape(-1, 2)
        a = np.vstack([a[:1], mid, a[-1:]])
    return a
_SM = {}
def smooth_rings():
    if "r" not in _SM:
        out = []
        for a in LAND10:
            if a[:, 0].max() < 19 or a[:, 0].min() > 30 or a[:, 1].max() < 34.5 or a[:, 1].min() > 42.5: continue
            if len(a) < 20000: out.append(_chaikin(a)); continue
            m = (a[:, 0] > 18) & (a[:, 0] < 31) & (a[:, 1] > 34) & (a[:, 1] < 43)
            parts = []; i = 0; n = len(a)
            while i < n:
                j = i
                while j < n and m[j] == m[i]: j += 1
                seg = a[i:min(j + 1, n)]
                parts.append(_chaikin_open(seg) if m[i] and len(seg) > 3 else seg)
                i = j
            out.append(np.vstack(parts))
        _SM["r"] = out
    return _SM["r"]
def land_mask(cam, res=None):
    m = Image.new("L", (W * SS, H * SS), 0); d = ImageDraw.Draw(m)
    use10 = (cam[2] >= 70) if res is None else (res == "10")
    rings = smooth_rings() if (cam[2] >= 400 and use10) else (LAND10 if use10 else LAND50)
    _draw_polys(d, cam, rings, 255)
    _draw_polys(d, cam, HOLES, 0, minpx=1.5)
    _draw_polys(d, cam, LAKES, 0, minpx=1.5)
    return m
def poly_mask(cam, poly, soft=True):
    m = Image.new("L", (W * SS, H * SS), 0)
    a = np.asarray(poly, dtype=np.float64)
    if soft: a = _chaikin(a, 2)
    ImageDraw.Draw(m).polygon(list(map(tuple, proj(cam, a))), fill=255)
    return m
def river_mask(cam, others=True):
    m = Image.new("L", (W * SS, H * SS), 0); d = ImageDraw.Draw(m); w = int(round(2.6 * SS))
    for a in RIVERS:
        p = proj(cam, a)
        if p[:, 0].max() < 0 or p[:, 0].min() > W * SS or p[:, 1].max() < 0 or p[:, 1].min() > H * SS: continue
        d.line(list(map(tuple, p)), fill=255, width=w, joint="curve")
    return m
def base_image(cam, lm, desert=None):
    im = Image.new("RGB", (W * SS, H * SS), SEA)
    im.paste(LAND, (0, 0), lm)
    if desert is not None: im.paste(SAND, (0, 0), desert)
    return im

# ---------------- drawing helpers (all at SS scale) ----------------
def s(v): return int(round(v * SS))
def text_spaced(d, xy, txt, f, fill, sp=0.0, anchor="l"):
    """anchor: l / m / r horizontally; xy is the left/mid/right point of the text's vertical middle."""
    widths = [d.textlength(c, font=f) for c in txt]
    tot = sum(widths) + sp * SS * (len(txt) - 1)
    x, y = xy
    if anchor == "m": x -= tot / 2
    elif anchor == "r": x -= tot
    asc, desc = f.getmetrics()
    y0 = y - (asc + desc) / 2
    for c, w in zip(txt, widths):
        d.text((x, y0), c, font=f, fill=fill); x += w + sp * SS
    return tot
def text_w(txt, f, sp=0.0):
    d = ImageDraw.Draw(Image.new("L", (4, 4)))
    return sum(d.textlength(c, font=f) for c in txt) + sp * SS * (len(txt) - 1)
def mix(c, bg, a):
    return tuple(int(round(bg[i] + (c[i] - bg[i]) * a)) for i in range(3))
def path_len(pts):
    a = np.asarray(pts, dtype=np.float64); return np.concatenate([[0], np.cumsum(np.hypot(*(a[1:] - a[:-1]).T))])
def partial(pts, frac):
    a = np.asarray(pts, dtype=np.float64)
    if frac >= 1: return a
    L = path_len(a); tgt = L[-1] * max(frac, 0)
    i = int(np.searchsorted(L, tgt, side="right")) - 1
    i = min(i, len(a) - 2)
    seg = L[i + 1] - L[i]
    q = 0 if seg == 0 else (tgt - L[i]) / seg
    return np.vstack([a[:i + 1], a[i] + (a[i + 1] - a[i]) * q])
def smooth(lonlat, n=12):
    """Catmull-Rom densify of a lon/lat polyline."""
    a = np.asarray(lonlat, dtype=np.float64)
    if len(a) < 3: return a
    pts = np.vstack([a[0], a, a[-1]]); out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for k in range(n):
            t = k / n
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(a[-1]); return np.asarray(out)
def arc(a, b, bend=0.18, n=40):
    a = np.asarray(a, float); b = np.asarray(b, float); m = (a + b) / 2; dv = b - a
    c = m + np.array([-dv[1], dv[0]]) * bend
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * a + 2 * (1 - t) * t * c + t ** 2 * b

class Frame:
    """One frame being drawn at SS scale on top of a base image."""
    def __init__(self, base, cam):
        self.im = base.copy(); self.d = ImageDraw.Draw(self.im); self.cam = cam
    def xy(self, lon, lat):
        x, y = proj(self.cam, [(lon, lat)])[0]; return float(x), float(y)
    def fill(self, mask, color, a=1.0):
        if a <= 0: return
        m = mask if a >= 1 else mask.point(lambda v: int(v * a))
        self.im.paste(color, (0, 0), m)
        if getattr(self, "rm", None) is not None: self.im.paste(RIVER, (0, 0), self.rm)
        self.d = ImageDraw.Draw(self.im)
    def line(self, lonlat, color=INK, width=3, frac=1.0, dash=None, arrow=False, a=1.0, bgc=LAND):
        if frac <= 0 or a <= 0: return
        p = partial(proj(self.cam, lonlat), frac)
        col = mix(color, bgc, a)
        if dash:
            L = path_len(p); on, off = dash[0] * SS, dash[1] * SS; pos = 0.0
            while pos < L[-1]:
                q0 = partial(p, pos / L[-1]); q1 = partial(p, min(pos + on, L[-1]) / L[-1])
                seg = q1[len(q0) - 1:]; seg[0] = q0[-1]
                if len(seg) >= 2: self.d.line(list(map(tuple, seg)), fill=col, width=s(width))
                pos += on + off
        else:
            self.d.line(list(map(tuple, p)), fill=col, width=s(width), joint="curve")
            r = s(width) / 2
            for q in (p[0], p[-1]): self.d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=col)
        if arrow and len(p) >= 2:
            e = p[-1]; k = len(p) - 2
            while k > 0 and np.hypot(*(e - p[k])) < 6 * SS: k -= 1
            v = e - p[k]; n = np.hypot(*v)
            if n > 0:
                v /= n; o = np.array([-v[1], v[0]]); hl = s(width * 4.2); hw = s(width * 2.2)
                self.d.polygon([tuple(e + v * hl * 0.55), tuple(e - v * hl * 0.45 + o * hw), tuple(e - v * hl * 0.45 - o * hw)], fill=col)
    def dot(self, lon, lat, r=5, color=INK, a=1.0, ring=None):
        if a <= 0: return
        x, y = self.xy(lon, lat); rr = s(r)
        if ring: self.d.ellipse([x - rr - s(3), y - rr - s(3), x + rr + s(3), y + rr + s(3)], fill=ring)
        self.d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=color if a >= 1 else mix(color, LAND, a))
    def pulse(self, lon, lat, t, t0, color=INK, n=2, period=0.9, rmax=34, width=3):
        for k in range(n):
            ph = (t - t0 - k * period * 0.5) / period
            if ph < 0: continue
            ph = ph % 1.0
            x, y = self.xy(lon, lat); r = s(6 + rmax * ph)
            col = mix(color, LAND, 1 - ph)
            self.d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=s(width))
    def label(self, lon, lat, txt, size=20, w="s", color=INK, dx=10, dy=0, anchor="l", sp=1.2, a=1.0, bgc=LAND, halo=True):
        if a <= 0: return
        x, y = self.xy(lon, lat); f = font(w, s(size))
        pos = (x + s(dx), y + s(dy))
        if halo:
            tw = text_w(txt, f, sp); x0 = pos[0] - (tw / 2 if anchor == "m" else tw if anchor == "r" else 0)
        text_spaced(self.d, pos, txt, f, mix(color, bgc, a), sp, anchor)
    def text(self, x, y, txt, size=20, w="s", color=INK, anchor="l", sp=1.2, a=1.0, bgc=LAND):
        if a <= 0: return
        text_spaced(self.d, (s(x), s(y)), txt, font(w, s(size)), mix(color, bgc, a), sp, anchor)
    def plaque(self, x, y, txt, size=30, a=1.0, anchor="m", strike=0.0, pad=(18, 11), bg=INK, fg=(255, 255, 255)):
        """Black plaque with white text; x,y in output px (centre for anchor m)."""
        if a <= 0: return
        f = font("b", s(size)); tw = text_w(txt, f, 1.5); asc, desc = f.getmetrics(); th = asc + desc
        cx, cy = s(x), s(y)
        x0 = cx - tw / 2 if anchor == "m" else (cx if anchor == "l" else cx - tw)
        box = [x0 - s(pad[0]), cy - th / 2 - s(pad[1]), x0 + tw + s(pad[0]), cy + th / 2 + s(pad[1])]
        if a < 1:
            ov = Image.new("RGB", self.im.size, bg); m = Image.new("L", self.im.size, 0)
            ImageDraw.Draw(m).rectangle(box, fill=int(255 * a)); self.im.paste(ov, (0, 0), m); self.d = ImageDraw.Draw(self.im)
            fgc = mix(fg, bg, a)
        else:
            self.d.rectangle(box, fill=bg); fgc = fg
        text_spaced(self.d, (x0, cy), txt, f, fgc, 1.5, "l")
        if strike > 0:
            self.d.line([(x0 - s(6), cy), (x0 - s(6) + (tw + s(12)) * min(strike, 1), cy)], fill=YELLOW, width=s(5))
        return box
    def plaque_at(self, lon, lat, txt, dx=0, dy=-40, **kw):
        x, y = P(self.cam, lon, lat); return self.plaque(x + dx, y + dy, txt, **kw)
    def out(self):
        return self.im.resize((W, H), Image.LANCZOS)

DESERT_POLY = None; DESERT_EXTRA = []
# ---------------- scene runner ----------------
class Scene:
    def __init__(self, name, dur, cam_fn, draw_fn, masks=None, rivers=True, res=None, active=None):
        self.name, self.dur, self.cam_fn, self.draw_fn, self.mask_polys, self.rivers = name, dur, cam_fn, draw_fn, masks or {}, rivers
        self._cam = None; self.res = res; self.active = list(active or []); self.auto = set()
    def prepare(self, cam):
        if cam == self._cam: return
        self._cam = cam
        lm = land_mask(cam, self.res)
        self.desert = ImageChops.multiply(poly_mask(cam, DESERT_POLY, soft=False), lm) if DESERT_POLY is not None else None
        if self.desert is not None:
            for extra in DESERT_EXTRA: self.desert = ImageChops.lighter(self.desert, ImageChops.multiply(poly_mask(cam, extra, soft=False), lm))
        self.base = base_image(cam, lm, self.desert)
        self.rmask = river_mask(cam)
        self.rm = self.rmask if self.rivers else None
        if self.rm is not None: self.base.paste(RIVER, (0, 0), self.rm)
        self.masks = {}
        for k, v in self.mask_polys.items():
            self.masks[k] = v(cam, lm) if callable(v) else ImageChops.multiply(poly_mask(cam, v), lm)
        self.lm = lm
    def frame(self, t):
        cam = tuple(round(v, 4) for v in self.cam_fn(t))
        self.prepare(cam)
        fr = Frame(self.base, cam); fr.t = t; fr.masks = self.masks; fr.scene = self; fr.rm = self.rm
        fr.r = lambda t0, d=0.6: (self.auto.add((round(t0, 3), round(t0 + d, 3))), ramp(t, t0, d))[1]
        self.draw_fn(fr, t)
        return fr.out()
    def sig(self, t):
        iv = list(self.auto) + self.active
        for a, b in iv:
            if a - 1e-6 <= t <= b + 1.0 / FPS + 1e-6: return ("a", round(t, 4))
        return ("s", sum(1 for a, b in iv if b < t), tuple(round(v, 4) for v in self.cam_fn(t)))
    def still(self, t, path, scale=1.0):
        im = self.frame(t)
        if scale != 1.0: im = im.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
        im.save(path)
    def render(self, outdir, t0=0.0, t1=None, suffix=""):
        t1 = self.dur if t1 is None else t1
        n = int(round((t1 - t0) * FPS))
        final = os.path.join(outdir, self.name + suffix + ".mp4"); tmp = final[:-4] + ".tmp.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an", tmp], stdin=subprocess.PIPE)
        self.frame(t0)          # dry pass registers animation intervals
        prev_sig, prev_bytes = None, None
        for k in range(n):
            t = t0 + k / FPS
            sig = self.sig(t)
            if sig is not None and sig == prev_sig:
                p.stdin.write(prev_bytes); continue
            b = self.frame(t).tobytes(); prev_sig, prev_bytes = sig, b
            p.stdin.write(b)
        p.stdin.close()
        if p.wait() == 0: os.rename(tmp, final)
        return final
