"""clips.json: точка входа каждого показа ролика. Окна — из layout.json. Показы одного ролика идут по исходнику подряд; если исходника не хватает, куски делят его равномерно (перекрываются)."""
import json, os, subprocess
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); L = json.load(open(f"{C}/layout.json")); HEAD = 0.3
OVR = {}          # (ролик, глава, t0) -> секунда входа, если показ надо сдвинуть после просмотра
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
uses = {}
for n in range(13):
    for a, b, kind, i, _ in L[str(n)]["segs"]:
        if kind == "CLIP": uses.setdefault(i, []).append((n, a, round(b - a, 3)))
out = {}
for nm in sorted(uses):
    D = round(dur(f"{C}/clips/{nm}.mp4"), 2); us = uses[nm]; tot = sum(u[2] for u in us); free = D - HEAD - 0.15; pos = HEAD; lst = []
    for k, (n, a, ln) in enumerate(us):
        t = pos if tot <= free else HEAD + (free - ln) * (k / max(1, len(us) - 1)); t = OVR.get((nm, n, a), max(0.0, min(t, D - ln - 0.1)))
        lst.append(dict(ch=n, t0=a, len=ln, **{"in": round(t, 2)}, speed=1.0)); pos += ln
        assert t + ln <= D + 0.01, (nm, n, a, "ролик короче окна")
    out[nm] = dict(file=f"{nm}.mp4", dur=D, uses=lst)
json.dump(dict(_note="Точки входа роликов по показам: in — секунда исходника, speed — скорость. Окна из layout.json. Собирается tools/clips_src.py.", clips=out), open(f"{C}/clips.json", "w"), indent=1, ensure_ascii=False)
print(len(out), "роликов", sum(len(v["uses"]) for v in out.values()), "показов", round(sum(u["len"] for v in out.values() for u in v["uses"]), 1), "с")
