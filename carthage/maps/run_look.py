import sys, time, look, ca_scenes
look.install(ca_scenes)
mode = sys.argv[1]
if mode == "still":
    for spec in sys.argv[2:]:
        n, ts = spec.split("@")
        for tt in ts.split(","): ca_scenes.SC[n].still(float(tt), f"test_look/{n}_{float(tt):05.1f}.png", 0.5)
else:
    for n in sys.argv[2:]:
        t0 = time.time(); ca_scenes.SC[n].render("out_look"); print(n, round(time.time() - t0, 1), flush=True)
