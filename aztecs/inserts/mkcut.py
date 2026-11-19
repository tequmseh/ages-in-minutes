"""Aztecs: вырезки предметов и подготовка вставок. python3 mkcut.py [ключи]. Вход src/Vnn.* (присылает Рустам, в git нет), выход ../film/cut/*.png и ../film/full/*.jpg.
V01 и V17 — rembg (isnet-general-use; pip install --break-system-packages rembg onnxruntime). Остальные предметы на ровном фоне — ключ (key, из mesopotamia/inserts/mkcut.py; rembg для них не нужен). Плоские листы кодексов, портреты и фото идут как есть (full)."""
import sys, os, glob
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f"{HERE}/../film/cut"; FULL = f"{HERE}/../film/full"; MAXS = 3000
Image.MAX_IMAGE_PIXELS = None
J = {  # ключ: (исходник, режим, opts)
"V01": ("V01", "rembg", {"fill": True}), "V12": ("V12", "key", {"const": True, "thr": 26, "shadows": False}),
"V13": ("V13", "key", {"const": True, "thr": 26, "shadows": False}), "V14": ("V14", "key", {"const": True, "thr": 26, "shadows": False}),
"V17": ("V17", "rembg", {}), "V23": ("V23", "key", {"const": True, "thr": 26, "shadows": False}),
}
for k in ["V02","V03","V04","V05","V06","V07","V08","V08.1","V08.2","V09","V10","V11","V15","V16","V18","V19","V20","V21","V22","V24","V25"]: J[k] = (k, "full", {})
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
    os.makedirs(OUT, exist_ok=True); os.makedirs(FULL, exist_ok=True)
    for k in (sys.argv[1:] or J):
        s, m, o = J[k]; im = Image.open(glob.glob(f"{HERE}/src/{s}.*")[0]).convert("RGB")
        if o.get("crop"): c = o["crop"]; im = im.crop((int(c[0] * im.width), int(c[1] * im.height), int(c[2] * im.width), int(c[3] * im.height)))
        if max(im.size) > MAXS: im.thumbnail((MAXS, MAXS), Image.LANCZOS)
        if m == "full": im.save(f"{FULL}/{k}.jpg", quality=95); print(k, "full", im.size, flush=True); continue
        if m == "rembg":
            import importlib.util; sp = importlib.util.spec_from_file_location("rome_mkcut", f"{HERE}/../../rome/inserts/mkcut.py"); rm = importlib.util.module_from_spec(sp); sp.loader.exec_module(rm)
            r = rm.cut(im, rm.new_session("isnet-general-use"), o); r.save(f"{OUT}/{k}.png"); print(k, "rembg", r.size, flush=True); continue
        r = key(im, o.get("thr", 16), o.get("const", False), o.get("shadows", True), o.get("warm", 0), o.get("corner", "tl"), o.get("sh", 60)); r.save(f"{OUT}/{k}.png"); print(k, "key", r.size, "LOW" if max(r.size) < 1000 else "", flush=True)
