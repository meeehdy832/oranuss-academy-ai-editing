# Developed by Mehdi ORANUSS | Powered by Claude
"""Intro AI editing, step 1: tighten the talking-head take by cutting pauses (no word is cut).
Silences from silencedetect (-32 dB, >= 0.28 s) are shortened to 0.2 s (0.1 s kept on each side).
Writes work/intro-ai/edl.json (kept segments + word times mapped to the tight timeline) and work/intro-ai/tight.mp4."""
import json, os, re, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
WK = os.path.join(ROOT, "work", "intro-ai")
SRC = os.path.join(os.path.dirname(ROOT), "input", "recordings", "introduction editing ai.mp4")
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
PAD = 0.10
END = 118.40   # after "tahiyati", before the tail noise

log = subprocess.run([FF, "-hide_banner", "-i", os.path.join(WK, "vo16.wav"), "-af", "silencedetect=n=-32dB:d=0.28", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
cuts = [(s + PAD, e - PAD) for s, e in zip(starts, ends) if e - s >= 0.28 and s < END]

keep, t = [], 0.0
for a, b in cuts:
    if a > t:
        keep.append((round(t, 3), round(a, 3)))
    t = b
if END - t > 0.05:
    keep.append((round(t, 3), END))
keep = [(a, min(b, END)) for a, b in keep if a < END]

def to_tight(x):
    """Original time -> tight-timeline time (times inside a cut snap to the cut point)."""
    acc = 0.0
    for a, b in keep:
        if x < a:
            return round(acc, 3)
        if x <= b:
            return round(acc + x - a, 3)
        acc += b - a
    return round(acc, 3)

words = []
for s in json.load(open(os.path.join(WK, "words.json")))["transcription"]:
    txt = s["text"].strip()
    if txt:
        words.append({"t0": to_tight(s["offsets"]["from"] / 1000), "t1": to_tight(s["offsets"]["to"] / 1000),
                      "o0": s["offsets"]["from"] / 1000, "text": txt})
total = round(sum(b - a for a, b in keep), 3)
json.dump({"keep": keep, "total": total, "words": words}, open(os.path.join(WK, "edl.json"), "w"), ensure_ascii=False, indent=1)

# render the tight A-roll: each segment trimmed, 8 ms audio fades at every join (no clicks)
parts, labels = [], []
for i, (a, b) in enumerate(keep):
    d = b - a
    parts.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]")
    parts.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={d - 0.008:.3f}:d=0.008[a{i}]")
    labels.append(f"[v{i}][a{i}]")
parts.append(f"{''.join(labels)}concat=n={len(keep)}:v=1:a=1[v][a]")
fg = os.path.join(WK, "cut_filter.txt")
open(fg, "w").write(";\n".join(parts))
tmp = os.path.join(WK, "rendering-tight.mp4")
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", SRC, "-/filter_complex", fg, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "pcm_s16le", tmp.replace(".mp4", ".mov")], check=True)
os.replace(tmp.replace(".mp4", ".mov"), os.path.join(WK, "tight.mov"))
print(f"{len(keep)} segments, {len(cuts)} pauses cut, 118.58 s -> {total} s")
