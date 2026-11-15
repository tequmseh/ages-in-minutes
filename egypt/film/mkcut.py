import sys, os
from PIL import Image
from rembg import remove, new_session
ses = new_session("isnet-general-use")
J = {"mirror": ("B10_mirror.jpg", (0.05, 0.05, 0.64, 0.95)), "sen3": ("B11_senusret3_face_met.jpg", None), "sen3c": ("B11c_senusret3_white_crown.jpg", None), "sahure": ("B12_sahure.jpg", None),
     "palette": ("B14_scribe_palette.jpg", None), "axe": ("B15_duckbill_cleveland.jpg", None), "hat": ("B16_hatshepsut_kneeling.png", None), "akh": ("B18_akhenaten_colossus.jpg", None),
     "nef": ("B19_nefertiti.jpg", None), "amarna": ("B20_amarna_BM.jpg", None), "tut": ("B21_tut_mask.jpg", None), "ram": ("B22_ramesses2_turin.png", (0.1, 0.03, 0.9, 0.86)),
     "treaty": ("B24_treaty_hittite.jpg", (0.05, 0.0, 0.97, 0.78)), "ptol": ("B26_ptolemy1_erlangen.jpg", None), "rosetta": ("B27_rosetta.jpg", None), "cleo": ("B28_cleopatra_antony.jpg", (0.05, 0.03, 0.48, 0.97)),
     "antony": ("B28_cleopatra_antony.jpg", (0.52, 0.03, 0.97, 0.97)), "herod": ("B2_herodotus.png", (0, 0, 1, 0.95)), "narmer_a": ("B3_narmer_palette.jpg", (0.0, 0.0, 0.5, 1.0)), "narmer_b": ("B3_narmer_palette.jpg", (0.5, 0.0, 1.0, 1.0)),
     "maat": ("B6_maat_met.jpg", None), "pepi": ("B9_pepi2_mother.jpg", None), "palermo": ("B1_palermo_stone.jpg", None), "merer": ("B7_merer_papyrus.jpg", None), "relief": ("B17_akhenaten_family.jpg", (0.0, 0.0, 1.0, 0.86)),
     "crownfig": ("B4_pharaoh_double_crown_illustration.webp", None)}
for k in (sys.argv[1:] or J):
    f, c = J[k]; im = Image.open(f"ins/{f}").convert("RGB")
    if c: im = im.crop((int(c[0] * im.width), int(c[1] * im.height), int(c[2] * im.width), int(c[3] * im.height)))
    o = remove(im, session=ses); bb = o.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox(); o = o.crop(bb); o.save(f"cut/{k}.png"); print(k, o.size)
