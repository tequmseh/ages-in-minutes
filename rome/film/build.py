"""Assemble one chapter: card + (graphics base, maps and reconstruction clips on their windows) + voiceover + quiet clip sound."""
import subprocess, json, sys, os, re, importlib
FPS = 60; CARD = 3.5; BED = 0.07; MUS = float(os.environ.get("MUS", "-34")); MUS_CARD = -21.0          # music bed: integrated loudness target, LUFS (voice is at -14)          # clip sound ceiling: 7 % of the levelled clip
# Master quality (standard since episode 2): everything is composed at 1920x1080, then the finished chapter is scaled to 2560x1440 and
# encoded near-transparently. YouTube gives uploads above 1080p a better codec and several times the bitrate, so 1080p playback is cleaner too.
# 60 fps: maps and graphics are rendered at a true 60; 24 fps reconstruction clips are brought up by frame repetition (2-3 cadence), never by interpolation.
OUT_W, OUT_H = 2560, 1440; CRF = "14"; PRESET = os.environ.get("PRESET", "medium")
DRAFT = bool(os.environ.get("DRAFT"))          # draft: 1080p, fast encode, missing clips are skipped and marked
if DRAFT: OUT_W, OUT_H, CRF, PRESET = 1920, 1080, "21", "veryfast"
ROOT = os.path.dirname(os.path.abspath(__file__))
def run(a, **k): return subprocess.run(a, capture_output=True, text=True, **k)
def dur(f): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).stdout)
def loud(f):
    e = run(["ffmpeg", "-hide_banner", "-i", f, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr
    return json.loads(e[e.rindex("{"):e.rindex("}") + 1])
VOICE = "volume={g:.2f}dB,aresample=48000,alimiter=limit=0.8:level=disabled:attack=3:release=60"
def voice_gain(f, target=-14.0):
    """gain that puts the limited voice at the target loudness (the limiter holds peaks under -1.5 dBTP and costs some level, so iterate)"""
    def meas(g):
        e = run(["ffmpeg", "-hide_banner", "-i", f, "-af", VOICE.format(g=g) + ",aformat=channel_layouts=stereo,ebur128", "-f", "null", "-"]).stderr          # measured as it is mixed: a mono voice reads about 1 dB higher in both channels
        return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1])
    g = target - meas(0.0)
    for _ in range(3): g += target - meas(g)
    return g
def build(spec):
    n = spec["n"]; import glob; vo = sorted(glob.glob(f"{ROOT}/../vo/vo{n:02d}.*"))[0]; D = max(dur(vo), spec.get("dur", 0)); od = "out_draft" if DRAFT else "out"; out = f"{ROOT}/{od}/ch{n:02d}.mp4"; os.makedirs(f"{ROOT}/{od}", exist_ok=True)
    spec = dict(spec); spec["missing"] = [(os.path.basename(o[0])[:-4], o[1], o[2]) for o in spec["overlays"] if not os.path.exists(o[0])]
    spec["overlays"] = [o for o in spec["overlays"] if os.path.exists(o[0])]
    if spec["missing"] and not DRAFT: sys.exit(f"missing clips: {spec['missing']}")
    # 1. graphics base
    gfx = f"{ROOT}/tmp_gfx_{n:02d}.mp4"; nfr = int(round(D * FPS)); import gfxlib
    if spec.get("gfx") is None and not spec["missing"]:
        assert run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x111111:s=1920x1080:r={FPS}:d={D + 0.2}", "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", gfx]).returncode == 0
    else:
        if spec.get("gfx") is None: spec["gfx"] = lambda t: gfxlib.blank()[0]; spec["gfx_windows"] = []
        _render_gfx(spec, gfx, D, nfr)
    _mux(spec, gfx, D, vo, out)
def _render_gfx(spec, gfx, D, nfr):
    import gfxlib
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", gfx], stdin=subprocess.PIPE)
    black = gfxlib.blank()[0].tobytes(); act = spec.get("gfx_windows", [(0, D)]); miss = spec.get("missing", [])
    for i in range(nfr):
        t = i / FPS; mm = [m for m in miss if m[1] <= t <= m[2]]
        if not mm and not any(a <= t <= b for a, b in act): p.stdin.write(black); continue
        im = spec["gfx"](t)
        if mm: gfxlib.text(gfxlib.ImageDraw.Draw(im), 60, 1040, f"{mm[0][0]} — CLIP PENDING", 22, anchor="l", sp=4, color=gfxlib.GRAY, bold=False)
        p.stdin.write(im.tobytes())
    p.stdin.close(); assert p.wait() == 0
def _mux(spec, gfx, D, vo, out):
    n = spec["n"]; CARD = globals()["CARD"] if spec.get("card") else 0.0
    ins = ["-i", spec["card"] or gfx, "-i", gfx]; fc = []; last = "[1:v]"; aud = []
    for k, (f, t0, t1, snd, *ex) in enumerate(spec["overlays"]):
        ss = ex[0] if ex else 0.0; sp = ex[1] if len(ex) > 1 else 1.0          # ss: start inside the clip, s; sp: playback speed (0.95 = 5 % slower)
        t1 = min(t1, D); i = k + 2; ins += ["-i", f]
        fc.append(f"[{i}:v]trim=start={ss},setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,setsar=1,"
                  f"tpad=stop_mode=clone:stop_duration=2,setpts=PTS-STARTPTS+{t0}/TB[v{k}]")
        fc.append(f"{last}[v{k}]overlay=enable='gte(t,{t0 - 0.004:.4f})*lt(t,{t1 - 0.004:.4f})':eof_action=pass[o{k}]"); last = f"[o{k}]"
        if snd:
            I = float(loud(f)["input_i"]); g = min(18.0, -23.0 - I)          # level the clips to each other, never boost more than 18 dB
            L = t1 - t0
            fc.append(f"[{i}:a]aresample=48000,atrim={ss}:{ss + L * sp:.3f},asetpts=PTS-STARTPTS,atempo={sp},volume={g:.2f}dB,volume={BED},afade=t=in:d=0.3,afade=t=out:st={max(0, L - 0.4):.3f}:d=0.4,"
                      f"adelay={int((CARD + t0) * 1000)}:all=1[a{k}]"); aud.append(f"[a{k}]")
    for j, (mk, t0, t1) in enumerate(spec.get("stills", [])):
        i = len([x for x in ins if x == "-i"]); L = t1 - t0; ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{L}", "-i", mk()]
        ins_extra = None
        fc.append(f"[{i}:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st={L - 0.35:.2f}:d=0.3:alpha=1,setpts=PTS-STARTPTS+{t0}/TB[s{j}]")
        fc.append(f"{last}[s{j}]overlay=enable='between(t,{t0},{t1})':eof_action=pass[so{j}]"); last = f"[so{j}]"
    fo = spec.get("fade_out", 0.5)
    fc.append(f"{last}fade=t=out:st={D - fo:.3f}:d={fo},format=yuv420p[body]")
    if CARD: fc.append(f"[0:v]fps={FPS},scale=1920:1080,setsar=1,format=yuv420p[card]"); fc.append(f"[card][body]concat=n=2:v=1:a=0,scale={OUT_W}:{OUT_H}:flags=lanczos,setsar=1,format=yuv420p[v]")
    else: fc.append(f"[body]scale={OUT_W}:{OUT_H}:flags=lanczos,setsar=1,format=yuv420p[v]")
    g = voice_gain(vo); m = {"input_i": f"gain {g:.2f} dB"}; vi = len([x for x in ins if x == "-i"]); ins += ["-i", vo]
    fc.append(f"[{vi}:a]{VOICE.format(g=g)},adelay={int(CARD * 1000)}:all=1[vo]")
    mu = spec.get("music")          # (file, sting, level): a track long enough starts on the card itself and drops under the voice; a shorter one starts with the body, the sting covers the card
    if mu and mu[0] and os.path.exists(mu[0]):
        f = mu[0]; I = float(loud(f)["input_i"]); L = dur(f); tp = 1.0; bed = (mu[2] if len(mu) > 2 and mu[2] is not None else MUS)
        on_card = bool(CARD) and L >= D + CARD - 0.1; need = D + (CARD if on_card else 0.0)
        if L < need + 0.2: tp = max(0.94, L / (need + 0.2))          # stretch up to 6 %, never cut mid-phrase
        gb = 10 ** ((bed - I) / 20); gc = 10 ** ((MUS_CARD - I) / 20); mi = len([x for x in ins if x == "-i"]); ins += ["-i", f]
        eq = "equalizer=f=2600:t=q:w=0.8:g=-4,"          # leave room for the voice
        if on_card:
            fc.append(f"[{mi}:a]aresample=48000,atempo={tp:.4f},atrim=0:{need:.3f},asetpts=PTS-STARTPTS,{eq}volume='if(lt(t,{CARD - 0.3}),{gc:.5f},if(lt(t,{CARD + 0.9}),{gc:.5f}+({gb:.5f}-{gc:.5f})*(t-{CARD - 0.3})/1.2,{gb:.5f}))':eval=frame,afade=t=in:d=0.05,afade=t=out:st={need - 2.5:.3f}:d=2.5[mus]")
        else:
            fc.append(f"[{mi}:a]aresample=48000,atempo={tp:.4f},atrim=0:{D:.3f},asetpts=PTS-STARTPTS,{eq}volume={gb:.5f},afade=t=in:d=0.8,afade=t=out:st={D - 2.5:.3f}:d=2.5,adelay={int(CARD * 1000)}:all=1[mus]")
        aud.append("[mus]")
        if CARD and not on_card and len(mu) > 1 and mu[1] and os.path.exists(mu[1]):
            si = len([x for x in ins if x == "-i"]); ins += ["-i", mu[1]]; I = float(loud(mu[1])["input_i"])
            fc.append(f"[{si}:a]aresample=48000,atrim=0:{CARD + 0.6},volume={MUS_CARD - I:.2f}dB,afade=t=in:d=0.05,afade=t=out:st={CARD - 0.5}:d=1.1[sting]"); aud.append("[sting]")
    fc.append(f"[vo]{''.join(aud)}amix=inputs={len(aud) + 1}:normalize=0:duration=longest,alimiter=limit=0.84:level=disabled,aformat=channel_layouts=stereo[a]")
    tmp = out.replace(".mp4", ".tmp.mp4")
    rr = run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", CRF, "-preset", PRESET, "-profile:v", "high", "-bf", "2", "-g", str(FPS // 2 * 2),
              "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{CARD + D:.3f}", "-movflags", "+faststart", tmp])
    if rr.returncode: print(rr.stderr[-3000:]); sys.exit(1)
    os.replace(tmp, out); os.remove(gfx); print(out, round(dur(out), 2), "vo", round(D, 2), "vo_in_LUFS", m["input_i"])
if __name__ == "__main__":
    sys.path.insert(0, ROOT)
    import chapters, time
    for c in sys.argv[1:]:
        s = chapters.SPECS[int(c)]
        build(s)
