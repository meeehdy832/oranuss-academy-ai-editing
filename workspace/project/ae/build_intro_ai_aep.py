# Developed by Mehdi ORANUSS | Powered by Claude
"""Builds the After Effects project for the intro (output/intro-ai/AE/Intro-AI-Editing.aep).
Reads the HyperFrames source (camera layouts, zooms, keywords, scene exits), the OrcaXV cue list
(work/intro-ai/sfx_orcaxv.json) and the plates rendered by intro_ai_plates.py, copies the footage into
output/intro-ai/AE/Footage, makes a polished voice stem, and writes work/intro-ai/ae/build_intro_ai.jsx,
which After Effects runs (DoScriptFile) to create the project.

Layer stack in the main comp (top -> bottom), same order as the HTML z-index:
  TOP plate (ring + wipes) / Camera circle copy (on top during circle beats) / keyword precomps (editable text)
  / GFX plate (scene graphics, alpha) / RAW clip (0-3.12 s) / Camera (real footage, layout + zoom keyframes)
  / BG plate / Voice / 56 SFX layers / final mix (reference, off) / approved video (guide, off)."""
import html as H, json, os, re, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HF = os.path.join(ROOT, "hf", "intro-ai")
WK = os.path.join(ROOT, "work", "intro-ai")
AE = os.path.abspath(os.path.join(ROOT, "..", "output", "intro-ai", "AE"))
FOOT = os.path.join(AE, "Footage")
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
FPS = 30
DUR = 3425 / FPS                      # frames of the approved video
FACE = (1000, 430)
INDEX = open(os.path.join(HF, "index.html"), encoding="utf-8").read()

# ---------- camera: layout + zoom tweens, simulated like GSAP so interrupted tweens start where they really are ----------
def inset(s):
    t, r, b, l, rad = map(float, re.findall(r"[-0-9.]+", s))
    return [t, r, b, l, rad]
cam_tw = [(float(m[5]), float(m[4]), inset(m[0]) + [float(m[1]), float(m[2]), float(m[3])])
          for m in re.findall(r"tl\.to\('#cam',\{clipPath:'(inset\([^']*\))',x:([-0-9.]+),y:([-0-9.]+),scale:([-0-9.]+),duration:([0-9.]+),ease:'power3\.inOut'\},([0-9.]+)\)", INDEX)]
zoom_tw = [(float(m[2]), float(m[1]), [float(m[0])]) for m in re.findall(r"tl\.to\('#camz',\{scale:([0-9.]+),duration:([0-9.]+),ease:'power2\.inOut'\},([0-9.]+)\)", INDEX)]
zsets = [(float(m[1]), int(m[0])) for m in re.findall(r"tl\.set\('#cam',\{zIndex:(\d+)\},([0-9.]+)\)", INDEX)]

def inout(p, k):
    return (2 ** (k - 1)) * p ** k if p < 0.5 else 1 - ((-2 * p + 2) ** k) / 2
def keys(tweens, start, k):
    """[(t, value, kind)] where kind 'a' = tween start, 'b' = tween end."""
    out, cur, prev = [], list(start), None
    for t, d, target in sorted(tweens, key=lambda x: x[0]):
        if prev and t < prev[0] + prev[1]:             # interrupted: value where the previous tween is now
            p0, d0, a, b = prev
            e = inout((t - p0) / d0, k)
            cur = [x + (y - x) * e for x, y in zip(a, b)]
            out = [o for o in out if not (o[2] == "b" and o[0] > t)]
        out.append((round(t, 3), list(cur), "a"))
        out.append((round(t + d, 3), list(target), "b"))
        prev, cur = (t, d, list(cur), list(target)), list(target)
    return out
CAM = keys(cam_tw, [0, 0, 0, 0, 0, 0, 0, 1.0], 3)
ZOOM = keys(zoom_tw, [1.0], 2)
over, on = [], None                                 # circle beats: camera drawn above the scene graphics
for t, z in sorted(zsets):
    if z == 7 and on is None:
        on = t
    elif z != 7 and on is not None:
        over.append([on, t]); on = None
if on is not None:
    over.append([on, DUR])

# ---------- scenes and keywords ----------
scenes = {}
for sid, st, du in re.findall(r'<div id="(s\d\d)" data-composition-id="s\d\d" data-composition-src="[^"]*" data-start="([0-9.]+)" data-duration="([0-9.]+)"', INDEX):
    comp = open(os.path.join(HF, "compositions", f"{sid}.html"), encoding="utf-8").read()
    m = re.search(rf"tl\.to\('#{sid}-w',\{{opacity:0,(x:-180|y:-120|scale:\.965|scale:1\.25),filter:'blur\((\d+)px\)',duration:([.0-9]+),ease:'power3\.in'\}},([0-9.]+)\)", comp)
    ex = None
    if m:
        kind = {"x:-180": "left", "y:-120": "up", "scale:.965": "blur", "scale:1.25": "zoom"}[m[1]]
        ex = {"kind": kind, "blur": int(m[2]), "d": float(m[3]), "t": round(float(st) + float(m[4]), 3)}
    scenes[sid] = {"id": sid, "start": float(st), "end": round(float(st) + float(du), 3), "exit": ex, "comp": comp}

KW = []
for sid, sc in sorted(scenes.items()):
    for kid, cls, style, inner in re.findall(r'<div id="(s\d\d-k[a-z0-9]*)" class="(kword[^"]*)" style="([^"]*)">(.*?)</div>', sc["comp"]):
        st = dict(re.findall(r"([a-z-]+):([^;]+)", style))
        left, top, w, h, fs = (float(re.sub("px", "", st[k])) for k in ("left", "top", "width", "height", "font-size"))
        spans = [(H.unescape(txt), c == "grad") for c, txt in re.findall(r'<span class="([^"]*)">(.*?)</span>', inner)]
        tin = float(re.search(rf"tl\.fromTo\('#{kid}',\{{opacity:0,scale:1\.35.*?\}},([0-9.]+)\);", sc["comp"])[1])
        out = re.search(rf"tl\.to\(\[?'#{kid}'[^;]*?blur\((\d+)px\)',duration:([.0-9]+),ease:'power3\.in'\}},([0-9.]+)\);", sc["comp"])
        KW.append({"id": kid, "scene": sid, "text": " ".join(s for s, _ in spans), "spans": spans, "ar": " ar" in cls,
                   "cx": left + w / 2, "cy": top + h / 2, "fs": fs, "tin": round(sc["start"] + tin, 3),
                   "out": {"t": round(sc["start"] + float(out[3]), 3), "d": float(out[2]), "blur": int(out[1])} if out else None,
                   "end": sc["end"]})

# ---------- footage ----------
os.makedirs(os.path.join(FOOT, "SFX"), exist_ok=True)
os.makedirs(os.path.join(FOOT, "Audio"), exist_ok=True)
os.makedirs(os.path.join(FOOT, "Camera"), exist_ok=True)
def copy(src, dst):
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
    return dst
AROLL = copy(os.path.join(HF, "assets", "aroll.mp4"), os.path.join(FOOT, "Camera", "Intro-AI-camera-tight.mp4"))
RAW = copy(os.path.join(HF, "assets", "raw.mp4"), os.path.join(FOOT, "Camera", "Intro-AI-raw-opening.mp4"))
MIX = copy(os.path.join(HF, "assets", "mix-orcaxv.wav"), os.path.join(FOOT, "Audio", "Intro-AI-final-mix-orcaxv.wav"))
rows = json.load(open(os.path.join(WK, "sfx_orcaxv.json")))
for r in rows:
    r["local"] = copy(r["file"], os.path.join(FOOT, "SFX", os.path.basename(r["file"])))

# voice stem: same polish chain as the mix; gain G = what the mix's loudness pass added, so stems + SFX gains add up
fg = open(os.path.join(WK, "audio_filter_orcaxv.txt")).read().split(";\n")
pre = fg[:-1] + [fg[-1].split(",loudnorm")[0] + ",aresample=48000,ebur128[a]"]
open(os.path.join(WK, "ae", "pre_sum.txt"), "w").write(";\n".join(pre))
cmd = [FF, "-hide_banner", "-i", os.path.join(WK, "tight.mov")] + sum([["-i", r["file"]] for r in rows], [])
meas = subprocess.run(cmd + ["-/filter_complex", os.path.join(WK, "ae", "pre_sum.txt"), "-map", "[a]", "-f", "null", "-"],
                      capture_output=True, text=True).stderr
G = round(-14.0 - float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", meas)[-1]), 2)
VOICE = os.path.join(FOOT, "Audio", "Intro-AI-voice-polished.wav")
if not os.path.exists(VOICE):
    vchain = fg[0].replace(f",apad=whole_dur=", f",volume={G}dB,alimiter=limit=0.84:level=0,apad=whole_dur=").replace("[vo]", ",pan=stereo|c0=c0|c1=c0[a]")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", os.path.join(WK, "tight.mov"), "-filter_complex", vchain,
                    "-map", "[a]", "-c:a", "pcm_s24le", VOICE + ".part.wav"], check=True)
    os.replace(VOICE + ".part.wav", VOICE)
SFX = [{"id": r["id"], "name": r["name"], "note": r["note"], "file": r["local"], "start": round(r["start"], 3), "skip": round(r["skip"], 3),
        "trim": r["trim"], "gain": round(r["gain"] + G, 2), "t": r["t"]} for r in rows]

PL = os.path.join(FOOT, "Plates")
DATA = {
    "fps": FPS, "dur": DUR, "face": FACE, "cam": CAM, "zoom": ZOOM, "over": over, "kw": KW,
    "scenes": [{k: v for k, v in s.items() if k != "comp"} for s in scenes.values()], "sfx": SFX,
    "files": {"bg": os.path.join(PL, "Intro-AI-BG-plate.mp4"), "gfx": os.path.join(PL, "Intro-AI-GFX-plate.mov"),
              "top": os.path.join(PL, "Intro-AI-TOP-plate.mov"), "aroll": AROLL, "raw": RAW, "voice": VOICE, "mix": MIX,
              "ref": os.path.abspath(os.path.join(AE, "..", "Intro-AI-Editing-FINAL-v2.mp4")),
              "aep": os.path.join(AE, "Intro-AI-Editing.aep"), "log": os.path.join(WK, "ae", "build_log.txt")},
}
missing = [f for f in DATA["files"].values() if f.endswith((".mp4", ".mov", ".wav")) and not os.path.exists(f)]
if missing:
    raise SystemExit("missing: " + ", ".join(missing))
jsx = "var D = " + json.dumps(DATA, ensure_ascii=False) + ";\n" + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "intro_ai_build.jsx"), encoding="utf-8").read()
out = os.path.join(WK, "ae", "build_intro_ai.jsx")
open(out, "w", encoding="utf-8").write("\ufeff" + jsx)
print("jsx", out, "| cam keys", len(CAM), "| zoom keys", len(ZOOM), "| over", over, "| keywords", len(KW), "| sfx", len(SFX), "| G", G)
