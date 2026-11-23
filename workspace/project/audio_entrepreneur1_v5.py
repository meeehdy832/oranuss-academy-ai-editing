# Developed by Mehdi ORANUSS | Powered by Claude
"""Entrepreneur short #1 v5 audio: cleaned voice (work/ytsave-entrepreneur/voice_v5_raw.wav) + music bed ducked under it + OrcaXV SFX from
work/ytsave-entrepreneur/sfx_cues_v5.json (hf/gen_entrepreneur1_v5.py). Two-pass to -14 LUFS. Writes hf/entrepreneur1-v5/assets/mix.wav."""
import csv, json, os, re, subprocess
ROOT = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.dirname(ROOT)
WK = os.path.join(ROOT, "work", "ytsave-entrepreneur")
SK = os.path.join(TOP, ".claude", "skills", "orcaxv-sfx")
MUSIC = os.path.join(TOP, "music", "sub_clair-background-music-591220 (2).mp3")
OUT = os.path.join(ROOT, "hf", "entrepreneur1-v5", "assets", "mix.wav")
VOICE = os.path.join(WK, "voice_v5_raw.wav")
CUEJ = json.load(open(os.path.join(WK, "sfx_cues_v5.json")))
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
TOTAL = CUEJ["total"]
CAT = {r["id"]: r for r in csv.DictReader(open(os.path.join(SK, "scripts", "catalog.tsv"), encoding="utf-8"), delimiter="\t")}
LEVEL = {"loud": -12.0, "normal": -9.0, "quiet": -6.0}
def lufs(args):
    m = subprocess.run([FF, "-hide_banner"] + args + ["-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", m)[-1])
VCH = ("aresample=48000,pan=mono|c0=c0,highpass=f=80,afftdn=nf=-28:tn=1,equalizer=f=250:t=q:w=1:g=-2,"
       "equalizer=f=3200:t=q:w=1.2:g=2.5,deesser=i=0.35,acompressor=threshold=-22dB:ratio=3:attack=6:release=120:makeup=2")
vg = -20.0 - lufs(["-i", VOICE, "-af", VCH + ",ebur128"])
rows = []
for t, sid, align, extra, trim in CUEJ["cues"]:
    s = CAT[sid]; dur, peak = float(s["dur_s"]), float(s["peak_s"] or 0)
    eff = min(dur, trim) if trim else dur
    st = t - peak if align == "peak" else t - eff if align == "end" else t
    rows.append((max(st, 0), max(-st, 0), trim, LEVEL[s["level"]] + extra, os.path.join(SK, "sounds", s["path"])))
g = [f"[0:a]{VCH},volume={vg:.2f}dB,apad=whole_dur={TOTAL},asplit=2[vo][vk]",
     f"[1:a]aresample=48000,pan=mono|c0=0.5*c0+0.5*c1,atrim=0:{TOTAL},asetpts=PTS-STARTPTS,volume=-24dB,"
     f"afade=t=in:d=1.0,afade=t=out:st={TOTAL - 1.8}:d=1.8[mu]",
     "[mu][vk]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=400:makeup=1[md]"]
labels = ["[vo]", "[md]"]
for i, (st, skip, trim, gain, path) in enumerate(rows):
    c = f"[{i + 2}:a]aresample=48000,pan=mono|c0=0.5*c0+0.5*c1"
    if skip: c += f",atrim=start={skip:.3f},asetpts=PTS-STARTPTS"
    if trim: c += f",atrim=0:{trim},afade=t=out:st={max(trim - 0.25, 0):.3f}:d=0.25"
    c += f",volume={gain}dB,adelay={int(round(st * 1000))}:all=1[s{i}]"
    g.append(c); labels.append(f"[s{i}]")
g.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,atrim=0:{TOTAL},alimiter=limit=0.7:level=0,pan=stereo|c0=c0|c1=c0[a]")
fg = os.path.join(WK, "audio_filter.txt"); open(fg, "w").write(";\n".join(g))
cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", "-i", VOICE, "-i", MUSIC] + sum([["-i", r[4]] for r in rows], [])
subprocess.run(cmd + ["-/filter_complex", fg, "-map", "[a]", "-c:a", "pcm_s24le", OUT + ".pre.wav"], check=True)
d = -14.0 - lufs(["-i", OUT + ".pre.wav", "-af", "ebur128"])
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", OUT + ".pre.wav", "-af", f"volume={d:.2f}dB,alimiter=limit=0.84:level=0",
                "-c:a", "pcm_s24le", OUT], check=True)
os.remove(OUT + ".pre.wav")
print("mix ok", len(rows), "sfx, voice gain", round(vg, 2), "trim", round(d, 2))
