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
"V05a": ("V05", "full", {"crop": (0.52, 0.0, 0.95, 1.0)}),
"V05b": ("V05", "full", {"crop": (0.57, 0.08, 0.80, 0.50)}),
"V06": ("V06", "cut", {"crop": (0.0, 0.0, 0.47, 1.0)}),
"V07": ("V07", "cut", {"crop": (0.27, 0.12, 0.73, 0.85), "fill": True}),
"V08": ("V08", "cut", {"fill": True}),
"V09": ("V09", "full", {}),
"V10": ("V10", "cut", {"fill": True}),
"V11": ("V11", "cut", {}),
"V12": ("V12", "cut", {"fill": True}),
"V13": ("V13", "cut", {"fill": True}),
"V14": ("V14", "cut", {"fill": True}),
"V15": ("V15", "cut", {"fill": True}),
"V16": ("V16", "cut", {"fill": True}),
"V17": ("V17", "cut", {"crop": (0.30, 0.03, 0.95, 0.40), "fill": True}),
"V18": ("V18", "cut", {"fill": True}),
"V19": ("V19", "cut", {"crop": (0.15, 0.25, 0.80, 1.0), "fill": True}),
"V20": ("V20", "cut", {"fill": True}),
"V21": ("V21", "cut", {"fill": True}),
"V23": ("V23", "full", {"crop": (0.63, 0.13, 0.965, 0.685)}),
"V24": ("V24", "full", {"crop": (0.03, 0.04, 0.985, 0.955)}),
"V25": ("V25", "cut", {"fill": True}),
"V26": ("V26", "full", {"crop": (0.37, 0.10, 0.97, 0.673)}),
"V27": ("V27", "full", {}),
"V28": ("V28", "cut", {"fill": True}),
"V29": ("V29", "full", {"crop": (0.004, 0.01, 0.996, 0.99)}),
"V30": ("V30", "cut", {"fill": True}),
"V31": ("V31", "full", {}),
}
Image.MAX_IMAGE_PIXELS = None
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(FULL, exist_ok=True); ses = None
    for k in (sys.argv[1:] or J):
        s, m, o = J[k]; im = Image.open(glob.glob(f"{HERE}/src/{s}.*")[0]).convert("RGB")
        if o.get("crop"): c = o["crop"]; im = im.crop((int(c[0] * im.width), int(c[1] * im.height), int(c[2] * im.width), int(c[3] * im.height)))
        if max(im.size) > MAXS: im.thumbnail((MAXS, MAXS), Image.LANCZOS)
        if m == "full": im.save(f"{FULL}/{k}.jpg", quality=95); print(k, "full", im.size, flush=True); continue
        ses = ses or new_session("isnet-general-use"); r = cut(im, ses, o); r.save(f"{OUT}/{k}.png"); print(k, "cut", r.size, "LOW" if max(r.size) < 1000 else "", flush=True)
