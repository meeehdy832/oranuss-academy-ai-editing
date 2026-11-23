"""Sound design for the financial-freedom explainer.
Builds an SFX bus from beats.json (each hit on its animation frame, same timings as Explainer.tsx),
mixes it under the voice, and masters to YouTube loudness (-14 LUFS integrated, true peak <= -1 dBTP, two-pass).

    python3 sfx_mix.py bus                       -> sfx_bus.wav + cues.json
    python3 sfx_mix.py bus WORKDIR BEATS.json        -> WORKDIR/sfx_bus.wav + cues.json
    python3 sfx_mix.py master WORKDIR VIDEO.mp4 OUT.mp4  -> final video (WORKDIR/voice.wav + SFX), mastered
SFX library: env SFX_LIB (default: the user's "+50 Sound Effects" folder).
"""
import json, os, re, subprocess, sys

HERE = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()          # WORKDIR
BEATS = sys.argv[3] if len(sys.argv) > 3 and sys.argv[1] == "bus" else os.path.join(HERE, "beats.json")
BUS = "sfx_bus.wav"
LAND = int(os.environ.get("LAND", "36"))                            # frame where counters land (ExplainerDoc)
LIB = os.environ.get("SFX_LIB", "/Users/Apple/Downloads/motion-graphics-skills-main/reference/+50 Sound Effects")
FPS = 30
DUR = json.load(open(BEATS, encoding="utf-8"))["duration"]

# one sound per role: (file, measured peak dBFS, max length s)
SND = {
    "whoosh": ("Whooch/Whoosh 7 .wav", -3.0, 1.4),
    "deep":   ("Most used/Deep Whoosh   (5).wav", -6.9, 1.8),
    "pop":    ("+Gift/Vadi Sound - UI Clicks - Notification Pop.wav", -4.7, 0.35),
    "click":  ("Most used/Ui Click_Snap.mp3", -6.7, 0.35),
    "impact": ("+Gift/DSGNSrce_IMPACT-Element 13_Ocular_Quantum.wav", -1.0, 1.1),
    "count":  ("Most used/Countdown, Spin, Numbers (3).wav", -8.0, 0.73),
    "cash":   ("+Gift/DB studios - Old Cash Register Cha Ching Money.wav", -4.0, 1.8),
}
# target PEAK level of each hit in the mix (voice sits ~ -16 LUFS before mastering): effects stay well under the voice
TARGET = {"whoosh": -21, "deep": -18, "pop": -17, "click": -19, "impact": -21, "count": -23, "cash": -15}


def fx_cues(b, hit):
    """Hits for the idea animations (IdeaFx.tsx), on the same spoken-word times."""
    t0 = b["from"]
    for fx in b.get("fx", []):
        k, at = fx["k"], t0 + fx.get("at", 0.3)
        items = fx.get("items") or []
        its = [t0 + it["at"] if "at" in it else None for it in items]
        if fx.get("pos") in ("left", "right"):
            hit(at - 0.28, "whoosh", -4)                      # glass panel swings in
        if k == "stamp":
            hit(at, "impact", 2)
        elif k in ("chips", "globe", "tags"):
            for j, t in enumerate(its):
                hit(t if t is not None else at + (0.27 + j * 0.6 if k == "chips" else 0.33 + j * 0.67), "pop", -j * 0.5)
        elif k == "receipt":
            for j, t in enumerate(its):
                hit(t if t is not None else at + 0.33 + j * 0.53, "click", -1)
        elif k == "count":
            hit(at, "count"); hit(at + fx.get("dur", 2), "cash" if fx.get("suffix", "DH") == "DH" else "impact", -1)
        elif k == "calendar":
            n, dur = fx.get("n", 6), fx.get("dur", 4)
            for j in range(n):
                hit(at + j * dur / n, "click", -2)
            if fx.get("value"):
                hit(at + dur, "cash", -2)
        elif k == "clock":
            hit(at, "count", -1); hit(at + 0.7, "cash", -3)
        elif k == "flow":
            hit(at, "pop"); hit(at + 0.27, "pop", -1); hit(at + 0.55, "cash", -4)
        elif k == "scale":
            hit(at + 0.6, "impact", -4)
        elif k == "domino":
            st, gap = at + 0.2, 26 / 30
            for j in range(fx.get("n", 6)):
                hit(st + 0.15, "click", -j * 0.3); st += gap; gap = max(5 / 30, gap * 0.72)
        elif k in ("line", "meter"):
            hit(at, "count", -2)


def cues():
    beats = json.load(open(BEATS, encoding="utf-8"))["beats"]
    out = []
    def hit(t, role, db_shift=0.0):
        if 0 <= t < DUR - 0.2:
            out.append({"t": round(t, 3), "role": role, "db": TARGET[role] + db_shift})
    for i, b in enumerate(beats):
        t0, ty = b["from"], b["type"]
        f = lambda frames: t0 + frames / FPS
        # scene change: whoosh peaks as the scene emerges (starts 3 f early); images get the deeper one
        if ty in ("image", "cutout", "video"):
            hit(t0 - 0.15, "deep")
        else:
            hit(t0 - 0.10, "whoosh", -2 if i % 2 else 0)        # small level variation, same family
        full = any(x.get("pos") == "full" for x in b.get("fx", []))
        fx_cues(b, hit)
        if full:
            continue
        if ty == "title":
            hit(f(4), "pop"); hit(f(12), "impact", -3)
        elif ty == "icons":
            for k, _ in enumerate(b.get("items", [])):
                hit(f(10 + k * 8 + 4), "pop", -k * 1.0)
        elif ty == "steps":
            n = max(1, len(b.get("items", [])))
            per = max(10, min(40, int(((b["to"] - b["from"]) * FPS - 40) / n)))
            for k in range(n):
                hit(f(10 + k * per), "click")
        elif ty == "stat":
            hit(f(6), "count")
            money = "DH" in (b.get("suffix") or "") or "درهم" in (b.get("title") or "")
            hit(f(LAND), "cash" if money else "impact", 0 if money else -2)
        elif ty == "vs":
            hit(f(12), "pop"); hit(f(26), "pop", -1)
            hit(f(24), "click", -2); hit(f(38), "click")          # the ✕ and ✓ marks
        elif ty == "quote":
            hit(f(2), "pop", -2)
        elif ty == "cutout":
            hit(f(8), "impact", -2)
        elif ty == "flow":
            half = max(60, (b["to"] - b["from"]) * FPS / 2 - 10)
            for k in range(len(b.get("rows", []))):
                st = 6 + k * half
                hit(f(st), "pop"); hit(f(st + 10), "click", -2); hit(f(st + 20), "pop", -2)
        elif ty == "equation":
            dur = (b["to"] - b["from"]) * FPS; end = min(dur - 30, 150)
            hit(f(14), "count", -2); hit(f(14 + (end - 14) * (0.72 - 0.12) / (0.86 - 0.12)), "impact", 1)
        elif ty == "bars":
            hit(f(10), "count", -3); hit(f(40), "pop", -2)
        elif ty == "chain":
            st, gap = 8, 70
            for k in range(b.get("n", 5)):
                hit(f(st), "pop", -k * 0.5); st += gap; gap = max(14, gap * 0.6)
        if ty in ("image", "video"):                      # soft tick on each 2.5 s punch-in
            k = 1
            while f(75 * k) < b["to"] - 0.3:
                hit(f(75 * k), "click", -7); k += 1
    return sorted(out, key=lambda c: c["t"])


def build_bus():
    cs = cues()
    json.dump(cs, open(os.path.join(HERE, "cues.json"), "w"), indent=1)
    roles = sorted({c["role"] for c in cs})
    args = ["ffmpeg", "-v", "error", "-y"]
    for r in roles:
        args += ["-i", os.path.join(LIB, SND[r][0])]
    fl, labels = [], []
    for ri, r in enumerate(roles):
        mine = [c for c in cs if c["role"] == r]
        fl.append(f"[{ri}:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit={len(mine)}" + "".join(f"[{r}{k}]" for k in range(len(mine))))
        _, peak, ln = SND[r]
        for k, c in enumerate(mine):
            ms = int(c["t"] * 1000)
            gain = c["db"] - peak
            fl.append(f"[{r}{k}]atrim=0:{ln},afade=t=out:st={max(0, ln - 0.12):.2f}:d=0.12,volume={gain:.1f}dB,adelay={ms}|{ms}[o{r}{k}]")
            labels.append(f"[o{r}{k}]")
    fl.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,apad=whole_dur={DUR},atrim=0:{DUR}[bus]")
    script = os.path.join(HERE, ".sfx_filter.txt")
    open(script, "w").write(";\n".join(fl))
    subprocess.run(args + ["-/filter_complex", script, "-map", "[bus]", "-c:a", "pcm_s16le", os.path.join(HERE, BUS)], check=True)
    print(f"{len(cs)} hits · roles: " + ", ".join(f"{r}={sum(1 for c in cs if c['role']==r)}" for r in roles))


def voice_gain(path, target=-16.0):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return round(target - float(m[-1]), 1) if m else 0.0


def master(video, out):
    voice, bus = os.path.join(HERE, "voice.wav"), os.path.join(HERE, BUS)
    gain = voice_gain(voice)
    pre = os.path.join(HERE, "premix.wav")
    # voice to ~-16 LUFS (+1.7 dB from -17.7), SFX bus under it, gentle limiter for safety
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", bus, "-filter_complex",
                    f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={gain}dB[v];"
                    "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[s];"
                    "[v][s]amix=inputs=2:normalize=0:duration=first[m]", "-map", "[m]", "-c:a", "pcm_s24le", pre], check=True)
    # loudnorm pass 1 (measure)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))
    print("measured:", {k: m[k] for k in ("input_i", "input_tp", "input_lra")})
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", pre, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", ln, "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    summ = r.stderr[r.stderr.rfind("Summary"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", summ); tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ)
    print(f"final: {i.group(1) if i else '?'} LUFS integrated · true peak {tp.group(1) if tp else '?'} dBTP → {out}")


if __name__ == "__main__":
    if sys.argv[1] == "bus":
        build_bus()
    else:
        master(sys.argv[3], sys.argv[4])
