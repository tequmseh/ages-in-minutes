"""Align script sentences to a voiceover by its pauses (no speech recognition available).
usage: python3 align.py script.md vo_dir -> prints and saves timing.json: {chapter: [[t0, t1, sentence], ...]}"""
import re, sys, subprocess, json
def pauses(f, db=-33, d=0.16):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", f"silencedetect=noise={db}dB:d={d}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", o)]; en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", o)]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
    return list(zip(st, en + [dur] * (len(st) - len(en)))), dur
def units(text):
    text = re.sub(r"\[[a-z, ]+\]", "", text); text = " ".join(text.split())
    return [u.strip() for u in re.split(r"(?<=[.?!:;])\s+", text) if u.strip()]
def weight(u):   # spoken length: letters, digits read out longer, punctuation adds a little
    w = len(re.sub(r"[^A-Za-z]", "", u)) + 4.5 * len(re.findall(r"\d", u)) + 2
    return w
def align(us, ps, dur):
    # speech starts after a leading silence and ends before the trailing one
    t_start = ps[0][1] if ps and ps[0][0] < 0.05 else 0.0
    t_end = ps[-1][0] if ps and ps[-1][1] >= dur - 0.05 else dur
    inner = [p for p in ps if p[0] > t_start + 0.2 and p[1] < t_end - 0.05]
    W = [weight(u) for u in us]; n = len(us); m = len(inner)
    sil = sum(b - a for a, b in inner); rate = (t_end - t_start - sil) / sum(W)          # seconds of speech per weight unit
    # boundary k (after unit k) is either at pause j or unaligned; DP over (units used, pauses used)
    INF = 1e18; best = {(0, -1): (0.0, None)}
    cumW = [0]
    for w in W: cumW.append(cumW[-1] + w)
    def tstart(j): return t_start if j < 0 else inner[j][1]
    def tend(j): return t_end if j >= m else inner[j][0]
    def speech(j0, j1):  # speech time between end of pause j0 and start of pause j1, minus pauses inside
        return tend(j1) - tstart(j0) - sum(inner[k][1] - inner[k][0] for k in range(j0 + 1, j1))
    for i in range(n):
        for j in range(-1, m):
            if (i, j) not in best: continue
            c0 = best[(i, j)][0]
            for i2 in range(i + 1, min(n, i + 4) + 1):
                for j2 in range(j + 1, min(m, j + 9) + 1):
                    if (i2 == n) != (j2 == m): continue
                    exp = (cumW[i2] - cumW[i]) * rate; got = speech(j, j2)
                    pen = 0.0 if j2 == m else max(0.0, 0.35 - (inner[j2][1] - inner[j2][0])) * 0.8       # prefer long pauses as sentence ends
                    c = c0 + (got - exp) ** 2 / max(exp, 0.5) + pen + 0.15 * (i2 - i - 1)
                    if c < best.get((i2, j2), (INF,))[0]: best[(i2, j2)] = (c, (i, j))
    out = []; k = (n, m); chain = []
    while k != (0, -1): chain.append(k); k = best[k][1]
    chain.reverse(); pi, pj = 0, -1
    for (i2, j2) in chain:
        a, b = tstart(pj), tend(j2); tot = cumW[i2] - cumW[pi]; acc = 0
        for u in range(pi, i2):
            t0 = a + (b - a) * acc / tot; acc += W[u]; t1 = a + (b - a) * acc / tot
            out.append([round(t0, 2), round(t1, 2), us[u]])
        pi, pj = i2, j2
    return out
if __name__ == "__main__":
    script, vo = sys.argv[1], sys.argv[2]
    secs = re.split(r"^### ", open(script).read(), flags=re.M)[1:]; res = {}
    for k, s in enumerate(secs[:13]):
        ps, dur = pauses(f"{vo}/{k:02d}.mp3"); res[k] = align(units(s.split("\n", 1)[1]), ps, dur)
    json.dump(res, open("timing.json", "w"), indent=0)
    for k in ([int(x) for x in sys.argv[3:]] or res):
        print(f"== {k}")
        for t0, t1, u in res[k]: print(f"{t0:6.2f} {t1:6.2f}  {u[:110]}")
