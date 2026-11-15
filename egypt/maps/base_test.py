from eg_base import *
@scene("t_country", 1, COUNTRY, dict(egy=EGY))
def _(fr, t): egypt(fr)
@scene("t_wide", 1, cam_box(8, 59, 15.5, 37.5), dict(egy=EGY, lev=LEV, hat=HAT))
def _(fr, t):
    fr.fill(fr.masks["lev"], GREEN_L); fr.fill(fr.masks["hat"], SLATE_L); egypt(fr)
@scene("t_mem", 1, cam_box(30.4, 32.1, 29.30, 30.08), dict(egy=EGY))
def _(fr, t):
    egypt(fr)
    for n in ("MEMPHIS", "GIZA", "SAQQARA", "MEIDUM", "BENT", "REDP"): city(fr, n, side="l")
@scene("t_thebes", 1, cam_box(32.4, 32.9, 25.60, 25.88), dict(egy=EGY))
def _(fr, t):
    egypt(fr)
    for n in ("KARNAK", "KINGS", "DEIR"): city(fr, n, side="l")
@scene("t_eth", 1, cam_box(5, 62, 8.5, 32.5), dict(egy=EGY))
def _(fr, t): egypt(fr)
for n, sc in SC.items(): sc.still(0, f"test/{n}.png", 0.5)
