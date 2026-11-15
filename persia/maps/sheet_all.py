"""contact sheets of every scene: python3 sheet_all.py -> test_look/all_1.jpg, all_2.jpg (two frames per scene, VO second in the corner)"""
import pe_scenes
from pe_base import *
names = list(SC); half = (len(names) + 1) // 2
for part, grp in enumerate((names[:half], names[half:]), 1):
    ims = []
    for n in grp:
        sc = SC[n]; sc.frame(0.0)
        for f in (0.55, 0.985):
            im = sc.frame(sc.dur * f).resize((768, 432), Image.LANCZOS); d = ImageDraw.Draw(im); d.rectangle([0, 0, 300, 20], fill=(17, 17, 17))
            d.text((6, 4), f"{n}  ch{sc.ch} VO {sc.t0 + sc.dur * f:5.1f}", fill=(255, 255, 255)); ims.append(im)
        sc.masks = {}; sc._cam = None; sc.base = None; sc.rmask = None; sc.rm = None; sc.lm = None; sc.desert = None
    cols = 4; sh = Image.new("RGB", (cols * 768, ((len(ims) + cols - 1) // cols) * 432), (17, 17, 17))
    for i, im in enumerate(ims): sh.paste(im, (i % cols * 768, i // cols * 432))
    sh.save(f"{HERE}/test_look/all_{part}.jpg", quality=88)
