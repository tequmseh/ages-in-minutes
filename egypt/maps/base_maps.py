from eg_base import *
@scene("base_map_country", 1, COUNTRY, dict(egy=EGY))
def _(fr, t): egypt(fr)
@scene("base_map_wide", 1, cam_box(8, 59, 16.2, 37.3), dict(egy=EGY))
def _(fr, t): egypt(fr)
for n, sc in SC.items(): sc.still(0, f"out/{n}.png", 1.0)
