# Developed by Mehdi ORANUSS | Powered by Claude
"""After Effects plates for the intro: splits hf/intro-ai/index.html into three render passes so AE can rebuild the
layer stack with the real camera footage and editable keywords in between.
  bg  : background world + split card frame (opaque, MP4)            -> under the camera
  gfx : all scene graphics, keywords hidden (ProRes 4444 with alpha)  -> over the camera
  top : circle ring + purple wipes (ProRes 4444 with alpha)          -> over the circle camera
Writes work/intro-ai/ae/<pass>/index.html (assets + compositions linked) and renders into output/intro-ai/AE/Footage/Plates.
usage: python3 -I project/ae/intro_ai_plates.py [bg gfx top]"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HF = os.path.join(ROOT, "hf", "intro-ai")
WK = os.path.join(ROOT, "work", "intro-ai", "ae")
OUT = os.path.join(ROOT, "..", "output", "intro-ai", "AE", "Footage", "Plates")
SRC = open(os.path.join(HF, "index.html"), encoding="utf-8").read()

CAM = re.compile(r'\s*<div id="cam".*?</div></div>', re.S)
def drop(html, *ids):
    for i in ids:
        if i == "cam":
            html = CAM.sub("", html)
        elif i == "scenes":
            html = re.sub(r'\s*<div id="s\d\d"[^>]*></div>', "", html)
        else:
            html = re.sub(rf'\s*<(div|video|audio) id="{i}"[^>]*>(</\1>)?', "", html)
    return html

CLEAR = "\n      html, body { background: transparent !important; }\n"
PASSES = {
    "bg":  (drop(SRC, "cam", "ring", "rawclip", "scenes", "fx", "mix"), "", "mp4"),
    "gfx": (drop(SRC, "bg", "cardframe", "cam", "ring", "rawclip", "fx", "mix"), CLEAR + "      .kword { visibility: hidden !important; }\n", "mov"),
    "top": (drop(SRC, "bg", "cardframe", "cam", "rawclip", "scenes", "mix"), CLEAR, "mov"),
}

os.makedirs(OUT, exist_ok=True)
HTML_ONLY = "--html-only" in sys.argv
for name in ([a for a in sys.argv[1:] if not a.startswith("--")] or list(PASSES)):
    html, css, fmt = PASSES[name]
    d = os.path.join(WK, name)
    os.makedirs(d, exist_ok=True)
    for sub in ("assets", "compositions", "hyperframes.json", "package.json"):
        link = os.path.join(d, sub)
        if not os.path.lexists(link):
            os.symlink(os.path.join(HF, sub), link)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html.replace("    </style>", css + "    </style>", 1))
    if HTML_ONLY:
        continue
    final = os.path.join(OUT, f"Intro-AI-{name.upper()}-plate.{fmt}")
    if os.path.exists(final):
        print("skip (exists)", final); continue
    part = os.path.join(d, f"rendering-{name}.{fmt}")
    cmd = ["npx", "--yes", "hyperframes@0.9.9", "render", "--quality", "delivery", "-o", part, "--quiet"]
    if fmt == "mov":
        cmd += ["--format", "mov"]
    print("render", name, flush=True)
    subprocess.run(cmd, cwd=d, check=True)
    os.replace(part, final)
    print("PLATE_OK", name, final, flush=True)
