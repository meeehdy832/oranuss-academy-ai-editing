# Developed by Mehdi ORANUSS | Powered by Claude
"""Intro AI editing, audio: voice from the tightened take (work/intro-ai/tight.mov) + SFX cues written by
hf/gen_intro_ai.py (work/intro-ai/sfx_cues.json), no music (user's choice). Voice polish: highpass, light denoise,
presence, compression; then the sum to -14 LUFS / -1.5 dBTP. Writes hf/intro-ai/assets/mix.wav."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from styles.base import place_sfx

ROOT = os.path.dirname(os.path.abspath(__file__))
WK = os.path.join(ROOT, "work", "intro-ai")
KIT = os.path.join(ROOT, "work", "sfx", "kit")
OUT = os.path.join(ROOT, "hf", "intro-ai", "assets", "mix.wav")
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
TOTAL = round(json.load(open(os.path.join(WK, "edl.json")))["total"], 2)

sfx = place_sfx([tuple(c) for c in json.load(open(os.path.join(WK, "sfx_cues.json")))], KIT)
g = [f"[0:a]aresample=48000,pan=mono|c0=0.5*c0+0.5*c1,highpass=f=80,afftdn=nf=-30:tn=1,equalizer=f=200:t=q:w=1:g=-1.5,"
     f"equalizer=f=3500:t=q:w=1.2:g=2.5,acompressor=threshold=-22dB:ratio=3:attack=6:release=120:makeup=3,apad=whole_dur={TOTAL}[vo]"]
labels = ["[vo]"]
for i, (st, path, gain) in enumerate(sfx):
    g.append(f"[{i + 1}:a]aresample=48000,pan=mono|c0=c0,volume={gain}dB,adelay={int(round(st * 1000))}:all=1[s{i}]")
    labels.append(f"[s{i}]")
g.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,atrim=0:{TOTAL},loudnorm=I=-14:TP=-1.5:LRA=11,"
         f"alimiter=limit=0.84:level=0,aresample=48000,pan=stereo|c0=c0|c1=c0[a]")
fg = os.path.join(WK, "audio_filter.txt")
open(fg, "w").write(";\n".join(g))
cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", "-i", os.path.join(WK, "tight.mov")]
for _, p, _ in sfx:
    cmd += ["-i", p]
tmp = OUT.replace(".wav", ".rendering.wav")
cmd += ["-/filter_complex", fg, "-map", "[a]", "-c:a", "pcm_s24le", tmp]
subprocess.run(cmd, check=True)
# second pass: loudnorm's one-pass mode lands a little hot on speech-only mixes, so trim to exactly -14 LUFS
import re
meas = subprocess.run([FF, "-hide_banner", "-i", tmp, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
i_lufs = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", meas)[-1])
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", tmp, "-af", f"volume={-14 - i_lufs:.2f}dB,alimiter=limit=0.84:level=0",
                "-c:a", "pcm_s24le", OUT], check=True)
os.remove(tmp)
print("mix ok", len(sfx), "sfx", TOTAL, "s")
