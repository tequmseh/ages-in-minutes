"""Mesopotamia: вырезки вставок V01–V31. python3 mkcut.py [ключи]. Вход src/Vnn.jpg|png (присылает Рустам, в git нет), выход ../film/cut/*.png и full/*.jpg.
Функция вырезки и её ключи (fill, cuty, cutline, keepbig) — из rome/inserts/mkcut.py. crop — доли исходника."""
import sys, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, f"{HERE}/../../rome/inserts")
from mkcut import cut, Image, new_session
OUT = f"{HERE}/../film/cut"; FULL = f"{HERE}/full"; MAXS = 3000
J = {  # ключ: (исходник, режим, opts)
"V01": ("V01", "cut", {}),
"V02": ("V02", "cut", {"fill": True}),
"V03": ("V03", "cut", {"fill": True}),
"V04": ("V04", "cut", {"fill": True}),
"V05a": ("V05", "key", {"crop": (0.56, 0.0, 1.0, 1.0), "warm": 9}),
"V06": ("V06", "cut", {"crop": (0.0, 0.0, 0.47, 1.0), "fill": True}),
"V07": ("V07", "cut", {"fill": True}),
"V08": ("V08", "cut", {"fill": True}),
"V09": ("V09", "full", {}),
"V10": ("V10", "cut", {"fill": True}),
"V11": ("V11", "cut", {}),
"V12": ("V12", "cut", {"fill": True}),
"V13": ("V13", "cut", {"fill": True}),
"V14": ("V14", "cut", {"fill": True}),
"V15": ("V15", "cut", {"fill": True}),
"V16": ("V16", "cut", {"fill": True}),
"V17": ("V17", "key", {"crop": (0.28, 0.03, 0.95, 0.44), "const": True, "thr": 26, "shadows": False}),
"V18": ("V18", "key", {"sh": 110}),
"V19": ("V19", "cut", {"fill": True}),
"V20": ("V20", "cut", {"fill": True}),
"V21": ("V21", "cut", {"fill": True}),
"V23": ("V23", "key", {"warm": 12}),
"V24": ("V24", "key", {"warm": 10}),
"V22": ("V22", "full", {"crop": (0.055, 0.045, 0.97, 0.975)}),
"V25": ("V25", "cut", {"fill": True}),
"V26": ("V26", "full", {"crop": (0.37, 0.17, 0.98, 0.76)}),
"V27": ("V27", "full", {}),
"V28": ("V28", "cut", {"fill": True}),
"V29": ("V29", "full", {"crop": (0.004, 0.01, 0.996, 0.99)}),
"V30": ("V30", "cut", {"fill": True}),
"V31": ("V31", "full", {}),
"V32": ("V32", "key", {"warm": 9}),          # герой со львом из Хорсабада — на плашке Гильгамеша (вне раскладки, добавлен Рустамом)
}
Image.MAX_IMAGE_PIXELS = None
def key(im, thr=16, const=False, shadows=True, warm=0, corner="tl", sh=60):
    """ровный серый фон (Рустам заменяет фоны сам): фон — плавная поверхность по краям кадра; тень под предметом (нейтральная, темнее фона) тоже считается фоном. Плоские плиты rembg рвёт, поэтому для них ключ."""
    import numpy as np
    from scipy import ndimage as ndi
    from PIL import ImageFilter
    a = np.asarray(im.convert("RGB")).astype(float); h, w = a.shape[:2]; b = max(4, int(0.025 * min(h, w)))
    m = np.zeros((h, w), bool); m[:b] = m[-b:] = True; m[:, :b] = m[:, -b:] = True
    yy, xx = np.mgrid[0:h, 0:w]; X = np.stack([np.ones(h * w), xx.ravel() / w, yy.ravel() / h, (xx.ravel() / w) ** 2, (yy.ravel() / h) ** 2, xx.ravel() * yy.ravel() / w / h], 1)
    bg = np.stack([(X @ np.linalg.lstsq(X[m.ravel()], a[..., c].ravel()[m.ravel()], rcond=None)[0]).reshape(h, w) for c in range(3)], 2)
    if const: bg = np.zeros_like(a) + np.median({'tl': a[:b, :b], 'br': a[-b:, -b:], 'bl': a[-b:, :b], 'tr': a[:b, -b:]}[corner].reshape(-1, 3), 0)          # предмет почти во весь кадр: фон — цвет угла
    d = np.abs(a - bg).max(2); neutral = (a.max(2) - a.min(2)) < 14; darker = (bg.mean(2) - a.mean(2)); shadow = neutral & (darker > 0) & (darker < sh)
    cand = (d > thr) & ~(shadow & shadows)
    if warm: cand = (a[..., 0] - a[..., 2]) > warm          # тёплый камень на нейтральном сером: тень нейтральна и в маску не попадает
    cand = ndi.binary_opening(cand, iterations=2); lab, n = ndi.label(~cand); edge = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1]); edge.discard(0)
    obj = ~np.isin(lab, list(edge)); lab, n = ndi.label(obj); sz = ndi.sum(obj, lab, range(1, n + 1)); obj = np.isin(lab, [i + 1 for i, v in enumerate(sz) if v >= 0.03 * sz.max()])
    obj = ndi.binary_fill_holes(ndi.binary_closing(obj, iterations=3)); A = Image.fromarray((obj * 255).astype("uint8")).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
    r = im.convert("RGBA"); r.putalpha(A); return r.crop(A.point(lambda v: 255 if v > 24 else 0).getbbox())
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(FULL, exist_ok=True); ses = None
    for k in (sys.argv[1:] or J):
        s, m, o = J[k]; im = Image.open(glob.glob(f"{HERE}/src/{s}.*")[0]).convert("RGB")
        if o.get("crop"): c = o["crop"]; im = im.crop((int(c[0] * im.width), int(c[1] * im.height), int(c[2] * im.width), int(c[3] * im.height)))
        if max(im.size) > MAXS: im.thumbnail((MAXS, MAXS), Image.LANCZOS)
        if m == "full": im.save(f"{FULL}/{k}.jpg", quality=95); print(k, "full", im.size, flush=True); continue
        if m == "key": r = key(im, o.get("thr", 16), o.get("const", False), o.get("shadows", True), o.get("warm", 0), o.get("corner", "tl"), o.get("sh", 60)); r.save(f"{OUT}/{k}.png"); print(k, "key", r.size, flush=True); continue
        ses = ses or new_session("isnet-general-use"); r = cut(im, ses, o); r.save(f"{OUT}/{k}.png"); print(k, "cut", r.size, "LOW" if max(r.size) < 1000 else "", flush=True)
