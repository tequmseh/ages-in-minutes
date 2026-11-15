import sys, glob
from PIL import Image, ImageDraw
out = sys.argv[1]; files = []
for pat in sys.argv[2:]: files += sorted(glob.glob(pat))
cols = 2 if len(files) <= 4 else 3
w, h = (960, 540) if cols == 2 else (640, 360)
rows = (len(files) + cols - 1) // cols
sh = Image.new("RGB", (cols * w + (cols + 1) * 8, rows * (h + 8) + 8), (40, 42, 46))
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS)
    d = ImageDraw.Draw(im); d.rectangle([0, h - 110 * h // 1080, w, h], outline=(255, 0, 255))
    d.text((6, 4), f.split("/")[-1][:-4], fill=(255, 0, 255))
    sh.paste(im, (8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 8)))
sh.save(out)
