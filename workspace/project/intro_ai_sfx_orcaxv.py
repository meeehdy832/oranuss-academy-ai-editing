# Developed by Mehdi ORANUSS | Powered by Claude
"""Intro AI editing, OrcaXV SFX version: same voice chain as intro_ai_audio.py, but the sound effects come from the
orcaxv-sfx skill (OrcaXV Essentials 100). Every cue sits on a visual event of hf/gen_intro_ai.py (scene wipes, keyword
slams, card pops, logo reveals). Writes hf/intro-ai/assets/mix-orcaxv.wav, work/intro-ai/sfx_orcaxv.json and
output/intro-ai/sfx-cue-sheet-orcaxv.md, then muxes the mix onto the approved FINAL picture as a preview."""
import csv, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WK = os.path.join(ROOT, "work", "intro-ai")
SK = os.path.join(ROOT, "..", ".claude", "skills", "orcaxv-sfx")
MIX = os.path.join(ROOT, "hf", "intro-ai", "assets", "mix-orcaxv.wav")
OUTDIR = os.path.join(ROOT, "..", "output", "intro-ai")
PICTURE = os.path.join(OUTDIR, "Intro-AI-Editing-FINAL.mp4")
VERSION = sys.argv[1] if len(sys.argv) > 1 else "v1"
OUT = os.path.join(OUTDIR, f"Intro-AI-Editing-SFX-PREVIEW-{VERSION}.mp4")
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
TOTAL = round(json.load(open(os.path.join(WK, "edl.json")))["total"], 2)
CAT = {r["id"]: r for r in csv.DictReader(open(os.path.join(SK, "scripts", "catalog.tsv"), encoding="utf-8"), delimiter="\t")}
# talking-head YouTube: SFX sit 6-12 dB under the voice (orcaxv defaults loud -8 / normal -5 / quiet -2, then -4 more)
LEVEL_GAIN = {"loud": -12.0, "normal": -9.0, "quiet": -6.0}

# (time on screen, id, align, extra dB, trim s, what happens on screen)
CUES = [
    (2.96, "WH-163", "peak", 0, None, "raw clip wipes into the AI edit"),
    (3.68, "RS-006", "end", -3, None, "riser lands on AI EDITING"),
    (3.68, "IM-003", "peak", -5, 2.2, "AI EDITING keyword slam"),
    (6.68, "WH-166", "peak", 0, None, "timeline panel tilts in"),
    (7.70, "WH-004", "peak", 0, None, "one long clip splits into shots"),
    (9.10, "UI-019", "peak", 0, None, "shots shift into place"),
    (11.61, "CA-001", "peak", 0, None, "blade cuts the bad take"),
    (12.62, "PO-006", "peak", 0, None, "keyframes and caption blocks pop in"),
    (14.11, "DA-002", "start", -2, None, "playhead sweeps, sparkles"),
    (15.46, "IM-029", "peak", -5, 1.6, "keyword: automatic"),
    (17.39, "PO-019", "peak", 0, None, "check mark: done"),
    (20.51, "WH-156", "peak", 0, None, "full screen: Claude"),
    (20.80, "PO-003", "peak", -2, 2.0, "Claude mark spins in"),
    (22.60, "CI-014", "peak", -5, 2.2, "Claude wordmark reveal"),
    (24.68, "PO-006", "peak", 0, None, "update card 1 NEW"),
    (25.32, "PO-008", "peak", 0, None, "update card 2 NEW"),
    (26.14, "PO-009", "peak", 0, None, "update card 3 NEW"),
    (28.74, "LO-003", "peak", -5, 2.4, "ORANUSS ACADEMY wordmark"),
    (29.96, "WH-012", "peak", 0, None, "full screen: wall of content"),
    (31.45, "WH-158", "peak", -2, None, "one video multiplies into the wall"),
    (33.24, "IM-025", "peak", -5, 1.6, "keyword: content"),
    (35.44, "IM-012", "peak", -7, 2.0, "gem + keyword: value of content"),
    (36.90, "PO-008", "peak", 0, None, "chip: needed in every project"),
    (39.86, "PO-009", "peak", 0, None, "project tiles pop in"),
    (42.05, "PO-006", "peak", 0, None, "play badges on every project"),
    (45.59, "WH-091", "peak", 0, None, "zoom to the social feed"),
    (47.65, "UI-006", "peak", -7, 1.4, "likes on the feed"),
    (49.29, "WH-174", "peak", -2, None, "full screen: learn with me"),
    (52.53, "PO-016", "peak", 0, None, "step 01 learn"),
    (52.53, "PA-005", "start", -4, None, "path draws between the steps"),
    (56.27, "UI-041", "peak", 0, None, "step 02 understand"),
    (57.08, "RW-001", "peak", 0, None, "step 03 work"),
    (58.55, "PO-008", "peak", 0, None, "chip: your project"),
    (59.72, "PO-009", "peak", 0, None, "chip: other projects"),
    (61.92, "WH-158", "peak", 0, None, "full screen: offer it as a service"),
    (64.98, "IM-020", "peak", -7, 2.0, "keyword: service"),
    (66.50, "PO-022", "peak", 0, None, "clients pop in around"),
    (68.49, "PO-006", "peak", 0, None, "row: no project"),
    (70.99, "PO-008", "peak", 0, None, "row: want to start"),
    (73.47, "PO-009", "peak", 0, None, "row: thinking about it"),
    (75.79, "WH-175", "peak", 0, None, "you + client appear"),
    (77.86, "RW-010", "peak", 0, 1.8, "coins: work together"),
    (80.60, "WH-176", "peak", 0, None, "push in on the face"),
    (83.99, "IM-029", "peak", -5, 1.6, "keyword: intro"),
    (84.67, "PO-008", "peak", 0, None, "keyword: and a guide"),
    (86.29, "IM-025", "peak", -7, 1.6, "keyword: VIDEO EDITING"),
    (87.55, "PO-009", "peak", -2, None, "chip: with AI"),
    (88.95, "WH-156", "peak", 0, None, "full screen: the series"),
    (89.82, "PO-006", "peak", 0, None, "title AI EDITING SERIES"),
    (92.00, "UI-029", "peak", -3, None, "chip: everything new on YouTube"),
    (95.82, "WH-012", "peak", 0, None, "back to split: calendar"),
    (97.26, "PO-013", "peak", -3, 2.0, "Friday lights up"),
    (97.83, "PO-008", "peak", -3, None, "chip: one session a month"),
    (102.04, "PO-022", "peak", 0, None, "question bubbles"),
    (104.32, "PO-003", "peak", -2, 2.0, "more questions"),
    (108.76, "CI-002", "peak", -9, 3.0, "last push on the face"),
]

rows = []
for t, sid, align, extra, trim, note in CUES:
    s = CAT[sid]
    dur, peak = float(s["dur_s"]), float(s["peak_s"] or 0)
    eff = min(dur, trim) if trim else dur
    start = t - peak if align == "peak" else t - eff if align == "end" else t
    rows.append(dict(t=t, id=sid, name=s["name"], folder=s["folder"], align=align, start=max(start, 0), skip=max(-start, 0),
                     trim=trim, gain=LEVEL_GAIN[s["level"]] + extra, note=note, file=os.path.join(SK, "sounds", s["path"])))
json.dump(rows, open(os.path.join(WK, "sfx_orcaxv.json"), "w"), indent=1, ensure_ascii=False)

g = [f"[0:a]aresample=48000,pan=mono|c0=0.5*c0+0.5*c1,highpass=f=80,afftdn=nf=-30:tn=1,equalizer=f=200:t=q:w=1:g=-1.5,"
     f"equalizer=f=3500:t=q:w=1.2:g=2.5,acompressor=threshold=-22dB:ratio=3:attack=6:release=120:makeup=3,apad=whole_dur={TOTAL}[vo]"]
labels = ["[vo]"]
for i, r in enumerate(rows):
    c = f"[{i + 1}:a]aresample=48000,pan=mono|c0=0.5*c0+0.5*c1"
    if r["skip"]:
        c += f",atrim=start={r['skip']:.3f},asetpts=PTS-STARTPTS"
    if r["trim"]:
        c += f",atrim=0:{r['trim']},afade=t=out:st={max(r['trim'] - 0.25, 0):.3f}:d=0.25"
    c += f",volume={r['gain']}dB,adelay={int(round(r['start'] * 1000))}:all=1[s{i}]"
    g.append(c)
    labels.append(f"[s{i}]")
g.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,atrim=0:{TOTAL},loudnorm=I=-14:TP=-1.5:LRA=11,"
         f"alimiter=limit=0.84:level=0,aresample=48000,pan=stereo|c0=c0|c1=c0[a]")
fg = os.path.join(WK, "audio_filter_orcaxv.txt")
open(fg, "w").write(";\n".join(g))
cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", "-i", os.path.join(WK, "tight.mov")]
for r in rows:
    cmd += ["-i", r["file"]]
tmp = MIX.replace(".wav", ".rendering.wav")
subprocess.run(cmd + ["-/filter_complex", fg, "-map", "[a]", "-c:a", "pcm_s24le", tmp], check=True)
meas = subprocess.run([FF, "-hide_banner", "-i", tmp, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
i_lufs = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", meas)[-1])
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", tmp, "-af", f"volume={-14 - i_lufs:.2f}dB,alimiter=limit=0.84:level=0",
                "-c:a", "pcm_s24le", MIX], check=True)
os.remove(tmp)

# cue sheet for the editor (place clip at = where the sound file starts on the timeline)
def fmt(x):
    m, s = divmod(x, 60)
    return f"{int(m):02d}:{s:05.2f}"
md = ["# Intro AI editing: SFX cue sheet (OrcaXV Essentials 100)", "", "> Developed by Mehdi ORANUSS | Powered by Claude", "",
      f"{len(rows)} sounds from `.claude/skills/orcaxv-sfx/sounds/`, each on a visual event. Mix: voice + SFX, -14 LUFS.", "",
      "| Time | Place clip at | ID | Sound (folder / file) | Align | Gain | Trim | On screen |", "|---|---|---|---|---|---|---|---|"]
for r in rows:
    md.append(f"| {fmt(r['t'])} | {fmt(r['start'])} | {r['id']} | {r['folder']} / {r['id']} {r['name']} | {r['align']} | {r['gain']:+.0f} dB | "
              f"{str(r['trim']) + ' s' if r['trim'] else ''} | {r['note']} |")
open(os.path.join(OUTDIR, "sfx-cue-sheet-orcaxv.md"), "w").write("\n".join(md) + "\n\n---\n\nDeveloped by Mehdi ORANUSS | Powered by Claude\n")

# picture = the approved FINAL (unchanged), sound = new mix; never overwrite a delivered file
if os.path.exists(OUT):
    sys.exit(f"{OUT} exists: pass a new version, e.g. python3 intro_ai_sfx_orcaxv.py v2")
part = os.path.join(OUTDIR, f"rendering-sfx-{VERSION}.mp4")
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", PICTURE, "-i", MIX, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", part], check=True)
os.replace(part, OUT)
print("ok", len(rows), "sfx ->", OUT)
