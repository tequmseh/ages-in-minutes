"""Look A (accepted 14 Nov): same vector maps, natural land tones anchored to the terrain, deeper sea with pale shallows,
soft coast shadow, grain and vignette. Import BEFORE ca_scenes; the original engine and scenes are not edited."""
import numpy as np, engine
from PIL import Image, ImageFilter, ImageChops
W, H, SS = engine.W, engine.H, engine.SS
_OLD_LAND = engine.LAND
LAND_N = (220, 207, 168); LAND_G = (200, 201, 152); SEA_DEEP = (118, 163, 186); SEA_SHALLOW = (192, 219, 227)
engine.LAND = LAND_N; engine.SEA = (160, 195, 209); engine.RIVER = (104, 158, 182)
for fn in (engine.Frame.label, engine.Frame.text, engine.Frame.line):
    if fn.__defaults__: fn.__defaults__ = tuple(LAND_N if d == _OLD_LAND else d for d in fn.__defaults__)
_TAB = np.random.default_rng(11).random((256, 256)).astype(np.float32)
def _vnoise(u, v):
    """value noise on a lattice, smooth-interpolated; u, v in lattice units"""
    i = np.floor(u).astype(np.int64); j = np.floor(v).astype(np.int64); fu = u - i; fv = v - j
    fu = fu * fu * (3 - 2 * fu); fv = fv * fv * (3 - 2 * fv)
    a = _TAB[i & 255, j & 255]; b = _TAB[(i + 1) & 255, j & 255]; c = _TAB[i & 255, (j + 1) & 255]; d = _TAB[(i + 1) & 255, (j + 1) & 255]
    return (a + (b - a) * fu) * (1 - fv) + (c + (d - c) * fu) * fv
def terrain(cam, q=4):
    """(mottle, green) fields for the frame, anchored to longitude and latitude so they travel with the land when the camera moves"""
    w, h = W * SS // q, H * SS // q; clon, clat, S = cam
    x = (np.arange(w, dtype=np.float32) + 0.5) * q; y = (np.arange(h, dtype=np.float32) + 0.5) * q
    lon = clon + (x - W * SS / 2) / (S * SS * engine.K); lat = clat - (y - H * SS / 2) / (S * SS)
    LON, LAT = np.meshgrid(lon, lat)
    mot = np.zeros((h, w), np.float32)
    for cell, amp in ((5.0, 0.030), (1.6, 0.024), (0.5, 0.016), (0.15, 0.010), (0.045, 0.008)):
        px = cell * S                                   # size of one cell on screen
        k = float(np.clip((px - 5) / 12, 0, 1)) * float(np.clip((2600 - px) / 900, 0, 1))
        if k > 0: mot += (_vnoise(LON / cell + 37.0, LAT / cell + 11.0) - 0.5) * 2 * amp * k
    grn = np.clip((_vnoise(LON / 3.2 + 91.0, LAT / 3.2 + 53.0) * 0.6 + _vnoise(LON / 0.9 + 13.0, LAT / 0.9 + 71.0) * 0.4 - 0.32) * 2.2, 0, 1)
    up = lambda a: np.asarray(Image.fromarray(a).resize((W * SS, H * SS), Image.BICUBIC), np.float32)
    return 1.0 + up(mot), up(grn.astype(np.float32))
def style(lm, mot, grn):
    """lm: L mask of land at SS scale -> styled RGB array"""
    w, h = lm.size; q = 4
    small = lm.resize((w // q, h // q), Image.BILINEAR)
    near = np.asarray(small.filter(ImageFilter.GaussianBlur(16)).resize((w, h), Image.BILINEAR), np.float32) / 255
    wide = np.asarray(small.filter(ImageFilter.GaussianBlur(70)).resize((w, h), Image.BILINEAR), np.float32) / 255
    L = np.asarray(lm, np.float32)[..., None] / 255
    k = np.clip(near * 1.9 + wide * 0.9, 0, 1)[..., None]
    sea = np.array(SEA_DEEP, np.float32) + (np.array(SEA_SHALLOW, np.float32) - np.array(SEA_DEEP, np.float32)) * k
    sh = np.asarray(ImageChops.offset(small, 2, 3).filter(ImageFilter.GaussianBlur(3.5)).resize((w, h), Image.BILINEAR), np.float32)[..., None] / 255
    sea = sea * (1 - 0.22 * sh)
    rim = np.clip((1 - near) * 2.0, 0, 1)[..., None]
    g = (grn * 0.55)[..., None]
    land = (np.array(LAND_N, np.float32) * (1 - g) + np.array(LAND_G, np.float32) * g) * mot[..., None] * (1 - 0.07 * rim)
    return sea * (1 - L) + land * L, L
def base_image(cam, lm, desert=None):
    mot, grn = terrain(cam); a, _ = style(lm, mot, grn)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
engine.base_image = base_image
_fill0 = engine.Frame.fill
def fill(self, mask, color, a=1.0): _fill0(self, mask, color, a * 0.86)       # territory colours stay translucent
engine.Frame.fill = fill
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
_VIG = (1 - 0.16 * np.clip((((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2 - 0.55) / 1.45, 0, 1))[..., None]
_GRAIN = (np.random.default_rng(5).normal(0, 2.6, (H, W, 1))).astype(np.float32)
def out(self):
    a = np.asarray(self.im.resize((W, H), Image.LANCZOS), np.float32)
    return Image.fromarray(np.clip(a * _VIG + _GRAIN, 0, 255).astype(np.uint8), "RGB")
engine.Frame.out = out

# ---- schemes (city plan, harbour, encirclement) get the same sea and land treatment
_SCR = terrain((10.0, 36.8, 300.0))
def restyle_flat(im, sea_color):
    """a flat hand-drawn scheme: every pixel of the flat sea colour becomes styled water, everything else gets the land mottle"""
    a = np.asarray(im, np.float32); sea = (np.abs(a - np.array(sea_color, np.float32)).max(-1) < 4)
    lm = Image.fromarray(((~sea) * 255).astype(np.uint8), "L")
    styled, L = style(lm, _SCR[0], _SCR[1] * 0)
    return Image.fromarray(np.clip(np.where(sea[..., None], styled, a * _SCR[0][..., None]), 0, 255).astype(np.uint8), "RGB")
def install(cs):
    """cs = the imported ca_scenes module"""
    from PIL import ImageDraw
    cs.NUM = (213, 188, 142)
    p0 = cs.plan_image
    def plan_image():
        if "styled" not in cs._PLAN: p0(); cs._PLAN["im"] = restyle_flat(cs._PLAN["im"], cs.SEA); cs._PLAN["styled"] = True
        return cs._PLAN["im"]
    cs.plan_image = plan_image
    land_tex = Image.fromarray(np.clip(np.array(LAND_N, np.float32) * _SCR[0][..., None], 0, 255).astype(np.uint8), "RGB")
    def blank(fr, color):
        fr.im.paste(land_tex if color == cs.LAND else color, (0, 0)) if color == cs.LAND else fr.im.paste(color, (0, 0, fr.im.size[0], fr.im.size[1]))
        fr.d = ImageDraw.Draw(fr.im)
    cs.blank = blank
