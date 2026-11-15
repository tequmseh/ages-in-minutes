"""Assemble one chapter: card + (graphics base, maps and reconstruction clips on their windows) + voiceover + quiet clip sound."""
import subprocess, json, sys, os, re, importlib
FPS = 30; CARD = 3.5; BED = 0.07          # clip sound ceiling: 7 % of the levelled clip
# Master quality (standard since episode 2): everything is composed at 1920x1080, then the finished chapter is scaled to 2560x1440 and
# encoded near-transparently. YouTube gives uploads above 1080p a better codec and several times the bitrate, so 1080p playback is cleaner too.
OUT_W, OUT_H = 2560, 1440; CRF = "14"; PRESET = "slow"
ROOT = os.path.dirname(os.path.abspath(__file__))
def run(a, **k): return subprocess.run(a, capture_output=True, text=True, **k)
def dur(f): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).stdout)
def loud(f):
    e = run(["ffmpeg", "-hide_banner", "-i", f, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr
    return json.loads(e[e.rindex("{"):e.rindex("}") + 1])
def build(spec):
    n = spec["n"]; vo = f"{ROOT}/vo/{n:02d}.mp3"; D = dur(vo); out = f"{ROOT}/out/ch{n:02d}.mp4"; os.makedirs(f"{ROOT}/out", exist_ok=True)
    # 1. graphics base
    gfx = f"{ROOT}/tmp_gfx_{n:02d}.mp4"; nfr = int(round(D * FPS)); import gfxlib
    if spec.get("gfx") is None:
        assert run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x111111:s=1920x1080:r={FPS}:d={D + 0.2}", "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", gfx]).returncode == 0
    else: _render_gfx(spec, gfx, D, nfr)
    _mux(spec, gfx, D, vo, out)
def _render_gfx(spec, gfx, D, nfr):
    import gfxlib
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", gfx], stdin=subprocess.PIPE)
    black = gfxlib.blank()[0].tobytes(); act = spec.get("gfx_windows", [(0, D)])
    for i in range(nfr):
        t = i / FPS
        p.stdin.write(spec["gfx"](t).tobytes() if any(a <= t <= b for a, b in act) else black)
    p.stdin.close(); assert p.wait() == 0
def _mux(spec, gfx, D, vo, out):
    n = spec["n"]
    ins = ["-i", spec["card"], "-i", gfx]; fc = []; last = "[1:v]"; aud = []
    for k, (f, t0, t1, snd) in enumerate(spec["overlays"]):
        t1 = min(t1, D); i = k + 2; ins += ["-i", f]
        fc.append(f"[{i}:v]fps={FPS},scale=1920:1080:flags=lanczos,setsar=1,tpad=stop_mode=clone:stop_duration=2,setpts=PTS-STARTPTS+{t0}/TB[v{k}]")
        fc.append(f"{last}[v{k}]overlay=enable='between(t,{t0},{t1 - 1 / FPS:.3f})':eof_action=pass[o{k}]"); last = f"[o{k}]"
        if snd:
            I = float(loud(f)["input_i"]); g = min(18.0, -23.0 - I)          # level the clips to each other, never boost more than 18 dB
            L = t1 - t0
            fc.append(f"[{i}:a]aresample=48000,atrim=0:{L:.3f},volume={g:.2f}dB,volume={BED},afade=t=in:d=0.3,afade=t=out:st={max(0, L - 0.4):.3f}:d=0.4,"
                      f"adelay={int((CARD + t0) * 1000)}:all=1[a{k}]"); aud.append(f"[a{k}]")
    for j, (mk, t0, t1) in enumerate(spec.get("stills", [])):
        i = len([x for x in ins if x == "-i"]); L = t1 - t0; ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{L}", "-i", mk()]
        ins_extra = None
        fc.append(f"[{i}:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st={L - 0.35:.2f}:d=0.3:alpha=1,setpts=PTS-STARTPTS+{t0}/TB[s{j}]")
        fc.append(f"{last}[s{j}]overlay=enable='between(t,{t0},{t1})':eof_action=pass[so{j}]"); last = f"[so{j}]"
    fo = spec.get("fade_out", 0.5)
    fc.append(f"{last}fade=t=out:st={D - fo:.3f}:d={fo},format=yuv420p[body]")
    fc.append(f"[0:v]fps={FPS},scale=1920:1080,setsar=1,format=yuv420p[card]"); fc.append(f"[card][body]concat=n=2:v=1:a=0,scale={OUT_W}:{OUT_H}:flags=lanczos,setsar=1,format=yuv420p[v]")
    m = loud(vo); vi = len([x for x in ins if x == "-i"]); ins += ["-i", vo]
    fc.append(f"[{vi}:a]loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
              f"offset={m['target_offset']}:linear=true,aresample=48000,adelay={int(CARD * 1000)}:all=1[vo]")
    fc.append(f"[vo]{''.join(aud)}amix=inputs={len(aud) + 1}:normalize=0:duration=longest,alimiter=limit=0.84,aformat=channel_layouts=stereo[a]")
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
        while not all(os.path.exists(o[0]) for o in s["overlays"]): time.sleep(10)
        build(s)
