# Developed by Mehdi ORANUSS | Powered by Claude
"""YouTube intro "AI Editing" (16:9, 1080p): the presenter cut out of his room (assets/person.webm, alpha) over the
purple-3d-glass world, energetic edit: raw -> edited hook, camera moves on the cut-out, side panels and full-screen
3D glass beats, keywords only (no full captions), no music (voice + SFX in assets/mix.wav).
Plan: output/intro-ai/PLAN.md. Times are on the tightened timeline (project/work/intro-ai/edl.json).
Writes hf/intro-ai/index.html, compositions/*.html and work/intro-ai/sfx_cues.json."""
import json, os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hfkit import Scene, IC, icon, glass, gloss, sphere, chip, title, skel, phone, avatar, LEAD, is_ar

PROJ = os.path.join(HERE, "intro-ai")
COMP = os.path.join(PROJ, "compositions")
os.makedirs(COMP, exist_ok=True)
WK = os.path.join(HERE, "..", "work", "intro-ai")
EDL = json.load(open(os.path.join(WK, "edl.json")))
TOTAL = round(EDL["total"], 2)   # ends on his last word ("tahiyati"), no end card
LOGO = os.path.join(HERE, "..", "..", "brand")
CLAUDE_LOGO_UNUSED = next((f for f in sorted(os.listdir(LOGO)) if "claude" in f.lower() and f.lower().endswith((".png", ".svg", ".webp"))), None)

scenes, CUES, WIPES = [], [], []
def sfx(t, role, take=0, gain=-15):
    CUES.append((round(t, 3), role, take, gain))

def kword(S, name, x, y, text, t, fs=104, grad=None, align="center", w=1500):
    """Keyword lockup (the only on-screen 'captions'): blur-slam in on its word, holds dead still."""
    parts = text.split(" ")
    spans = " ".join(f'<span class="{"grad" if grad is not None and i in grad else ""}">{html.escape(p)}</span>' for i, p in enumerate(parts))
    S.box(name, x, y, w, int(fs * 1.5), "kword ar" if is_ar(text) else "kword", spans, f"font-size:{fs}px;text-align:{align}")
    S.tw(f"tl.fromTo('#{S.id(name)}',{{opacity:0,scale:1.35,filter:'blur(16px)'}},{{opacity:1,scale:1,filter:'blur(0px)',duration:.32,ease:'expo.out'}},{t});")

def fullbg(S):
    """Opaque world behind a full-screen beat (covers the presenter)."""
    S.raw(f'<div id="{S.id("fbg")}" class="full-bg"><div class="bg-base"></div><div class="bg-glow g1"></div><div class="bg-glow g2"></div><div class="bg-grid"></div></div>')
    S.tw(f"tl.fromTo('#{S.id('fbg')}',{{opacity:0}},{{opacity:1,duration:.22,ease:'power2.out'}},0);")

# ---------- camera on the cut-out presenter: (time, x, y, scale, duration) ----------
FACE = (1000, 430)          # his face in the source frame
# real footage (no background removal): full frame / split card on the left / small circle, plus punch-ins inside
LAYOUTS = {"full": ("inset(0px 0px 0px 0px round 0px)", 0, 0, 1.0),
           "split": ("inset(50px 500px 50px 580px round 44px)", -520, 0, 1.0),            # card 60-900 px, panels go right
           "circle": ("inset(100px 590px 320px 670px round 330px)", -730, 370, 0.42)}    # face circle bottom-left
CAM, ZOOM = [], []
def lay(t, state, d=0.6):
    CAM.append((round(t, 3), state, d))
def zoom(t, s=1.0, d=0.5):
    ZOOM.append((round(t, 3), s, d))

# S00 0-2.96 RAW: the untouched take (graded flat) with a RAW badge and a recording timecode
S = Scene("s00", 0.0, 4.2, "none"); scenes.append(S)
S.box("raw", 210, 90, 220, 70, "raw-badge", '<i class="rec"></i><span>RAW</span>', "border-radius:14px")
S.blurin(f"#{S.id('raw')}", 0.15)
S.box("tc", 1720, 90, 280, 60, "timecode", "00:00:00:00")
S.tw(f"(()=>{{const el=document.querySelector('#{S.id('tc')}');const o={{f:0}};tl.to(o,{{f:89,duration:2.96,ease:'none',onUpdate:()=>{{const f=Math.round(o.f);"
     f"el.textContent='00:00:0'+Math.floor(f/30)+':'+String(f%30).padStart(2,'0');}}}},0);}})();")
S.box("frm", 960, 540, 1880, 1040, "raw-frame")
S.blurin(f"#{S.id('frm')}", 0.1)
S.tw(f"tl.to(['#{S.id('raw')}','#{S.id('tc')}','#{S.id('frm')}'],{{opacity:0,duration:.15}},2.9);")
S.box("after", 260, 90, 380, 76, "after-badge", f'{icon("spark", 34)}<span class="ar">مونتاج بالـ AI</span>', "border-radius:38px")
S.pop(f"#{S.id('after')}", 3.05, 0.6, "back.out(1.6)", 0.45)
S.tw(f"tl.to('#{S.id('after')}',{{opacity:0,y:-30,filter:'blur(8px)',duration:.3,ease:'power3.in'}},3.9);")
sfx(2.96, "riser", 0, -16); sfx(2.96, "whoosh.long", 0, -10)
WIPES.append(2.96)
lay(2.96, "full", 0.01); zoom(3.05, 1.13, 0.5)

# S01 2.96-20.5 the edit assembles itself: timeline panel builds beside the presenter
S = Scene("s01", 3.6, 20.45, "left"); scenes.append(S)
S.box("kw1bg", 960, 880, 820, 170, "glass", "", "border-radius:85px"); S.pop(f"#{S.id('kw1bg')}", S.t(3.68), 0.7, "expo.out", 0.35)
kword(S, "kw1", 960, 880, "AI EDITING", S.t(3.68), 112, grad=[0]); sfx(3.68, "hit", 0, -12)
S.tw(f"tl.to(['#{S.id('kw1')}','#{S.id('kw1bg')}'],{{opacity:0,filter:'blur(10px)',duration:.25,ease:'power3.in'}},{S.t(6.25)});")
lay(6.5, "split", 0.6); zoom(6.5, 1.0, 0.6)
S.raw('<div class="persp" style="left:960px;top:150px;width:920px;height:700px">')
S.raw(f'<div id="{S.id("tlp")}" class="glass tl-panel" style="left:20px;top:40px;width:880px;height:620px;border-radius:40px">'
      f'<div class="tl-head"><span class="tl-dot"></span><span class="tl-dot"></span><span class="tl-dot"></span><b>AI EDITING</b></div>'
      f'<div class="tl-label" style="top:130px">V2</div><div class="tl-label" style="top:250px">V1</div><div class="tl-label" style="top:370px">A1</div><div class="tl-label" style="top:490px">T1</div>'
      + "".join(f'<div id="{S.id(f"seg{i}")}" class="clipseg" style="left:{110 + i * 148}px;top:220px;width:140px"><div class="cs-th"></div></div>' for i in range(5))
      + "".join(f'<div id="{S.id(f"kf{i}")}" class="kf" style="left:{150 + i * 120}px;top:118px"><i></i></div>' for i in range(6))
      + f'<div id="{S.id("wave")}" class="wave" style="left:110px;top:350px;width:740px;height:70px">' + "".join(
          f'<i style="height:{18 + (i * 37 % 50)}px"></i>' for i in range(46)) + "</div>"
      + "".join(f'<div id="{S.id(f"cap{i}")}" class="capseg" style="left:{120 + i * 180}px;top:475px;width:150px"></div>' for i in range(4))
      + f'<div id="{S.id("blade")}" class="blade"></div>'
      + f'<div id="{S.id("ph")}" class="playhead" style="left:110px;top:100px;height:450px"></div>'
      + "</div></div>")
S.tilt(f"#{S.id('tlp')}", S.t(6.68), -30, 12, -10, 4, 1.0); S.drift(f"#{S.id('tlp')}", S.t(6.68) + 1.0, "rotationY", 6)
sfx(6.68, "whoosh.short", 0, -13)
for i in range(5):     # one long clip...
    S.tw(f"tl.fromTo('#{S.id(f'seg{i}')}',{{opacity:0,scaleX:0}},{{opacity:1,scaleX:1,duration:.5,ease:'expo.out'}},{S.t(6.91) + i * 0.02:.3f});")
for i in range(5):     # ...splits into shots ("w-t9sim-ha", "l-l9atat")
    S.tw(f"tl.to('#{S.id(f'seg{i}')}',{{x:{(i - 2) * 14},duration:.35,ease:'power3.out'}},{S.t(7.70)});")
    S.tw(f"tl.to('#{S.id(f'seg{i}')}',{{y:{-8 if i % 2 else 8},duration:.3,ease:'power2.out'}},{S.t(9.10) + i * 0.05:.3f});")
sfx(7.70, "snap", 0, -14); sfx(9.10, "click", 0, -16)
S.tw(f"tl.fromTo('#{S.id('blade')}',{{opacity:0,y:-80}},{{opacity:1,y:0,duration:.25,ease:'power3.out'}},{S.t(11.61)});"
     f"tl.to('#{S.id('seg3')}',{{opacity:.25,scaleY:.7,duration:.25,ease:'power2.in'}},{S.t(11.61) + 0.2:.3f});"
     f"tl.to('#{S.id('blade')}',{{opacity:0,duration:.2}},{S.t(11.61) + 0.6:.3f});")
sfx(11.61, "snap", 1, -12)
for i in range(6):     # animation layer
    S.pop(f"#{S.id(f'kf{i}')}", S.t(12.62) + i * 0.06, 0.2, "back.out(2)", 0.4)
for i in range(4):
    S.tw(f"tl.fromTo('#{S.id(f'cap{i}')}',{{opacity:0,scaleX:0}},{{opacity:1,scaleX:1,duration:.4,ease:'expo.out'}},{S.t(12.62) + 0.2 + i * 0.06:.3f});")
S.tw(f"tl.fromTo('#{S.id('wave')}',{{opacity:0,scaleY:0}},{{opacity:1,scaleY:1,duration:.5,ease:'expo.out'}},{S.t(6.91) + 0.15:.3f});")
sfx(12.62, "pop", 0, -14)
S.tw(f"tl.fromTo('#{S.id('ph')}',{{opacity:0,x:0}},{{opacity:1,x:720,duration:2.6,ease:'none'}},{S.t(14.11)});")
sfx(14.11, "swell", 0, -18)
kword(S, "kw2", 1420, 918, "أوتوماتيك", S.t(15.46), 92, grad=[0], w=900); sfx(15.46, "hit", 1, -13)
zoom(12.6, 1.1, 0.5); zoom(17.4, 1.0, 0.45)
S.box("ok", 1760, 230, 92, 92, "okdot", icon("check", 50, "#fff", 3)); S.pop(f"#{S.id('ok')}", S.t(17.39), 0.3, "back.out(2)", 0.5)
sfx(17.39, "click.confirm", 0, -14)
for i, (x, y) in enumerate(((1100, 200), (1830, 640), (1250, 760))):
    S.box(f"sp{i}", x, y, 44, 44, "sparkle", icon("spark", 44, "#A78BFA")); S.pop(f"#{S.id(f'sp{i}')}", S.t(14.11) + 0.3 + i * 0.12, 0, "back.out(3)", 0.5)

# S02 20.5-23.4 full screen: Claude
S = Scene("s02", 20.45, 23.35, "zoom"); scenes.append(S)
fullbg(S); WIPES.append(20.45); sfx(20.51, "whoosh.long", 1, -11)
S.raw('<div class="persp" style="left:760px;top:170px;width:400px;height:400px">')
glass(S, "lc", 200, 200, 330, 330, f'<img id="{S.id("mark")}" src="assets/claude-mark.png" class="logo-img"/>', 70)
S.raw("</div>")
S.tilt(f"#{S.id('lc')}", 0.15, -50, 25, -12, 8, 1.1); S.drift(f"#{S.id('lc')}", 1.25, "rotationY", 14)
for i, d in enumerate((520, 640)):
    S.box(f"orb{i}", 960, 370, d, d, "orbit-ring", "", "border-radius:50%")
    S.tw(f"tl.fromTo('#{S.id(f'orb{i}')}',{{opacity:0,scale:.6,rotation:0}},{{opacity:1,scale:1,rotation:{90 if i else -90},duration:2.6,ease:'power2.out'}},{0.2 + i * 0.1:.2f});")
S.tw(f"tl.fromTo('#{S.id('mark')}',{{opacity:0,rotation:-200,scale:.2,x:-420,y:-260}},{{opacity:1,rotation:0,scale:1,x:0,y:0,duration:1.0,ease:'expo.out'}},0.35);")
S.tw(f"tl.to('#{S.id('mark')}',{{rotation:40,duration:{23.35 - 20.45 - 1.4:.2f},ease:'none'}},1.35);")
S.box("wm", 960, 720, 800, 172, "logo-wm", '<img src="assets/claude-logo.png"/>')
S.tw(f"tl.fromTo('#{S.id('wm')}',{{opacity:0,scale:1.25,filter:'blur(16px)'}},{{opacity:1,scale:1,filter:'blur(0px)',duration:.4,ease:'expo.out'}},{S.t(22.60)});")
sfx(22.60, "hit", 1, -11)
lay(20.3, "circle", 0.5)

# S03 23.4-27.9 AI keeps evolving: update cards cascade beside the presenter
S = Scene("s03", 23.35, 27.85, "left"); scenes.append(S)
lay(23.3, "split", 0.5); zoom(23.45, 1.08, 0.6)
for i, (t0, ic, kind) in enumerate(((24.68, "spark", ""), (25.32, "chip", "deep"), (26.14, "rocket", "violet"))):
    y = 300 + i * 170
    S.box(f"n{i}", 1400, y, 640, 140, "glass notif",
          f'<div class="gloss {kind}" style="left:22px;top:22px;width:96px;height:96px;border-radius:26px"><div class="gl-ic">{icon(ic, 46)}</div></div>'
          f'<div class="skel" style="position:absolute;left:146px;top:40px;width:300px;height:20px;border-radius:10px"></div>'
          f'<div class="skel" style="position:absolute;left:146px;top:80px;width:220px;height:14px;border-radius:7px"></div>'
          f'<div class="notif-new">NEW</div>', "border-radius:34px")
    S.side(f"#{S.id(f'n{i}')}", S.t(t0), 140, 0.7); sfx(t0, "pop", i, -16)
kword(S, "kw", 1400, 820, "الـ AI كيتطوّر", S.t(26.46), 88, grad=[1], w=1000)

# S04 27.9-29.9 Oranuss Academy
S = Scene("s04", 27.85, 29.95, "blur"); scenes.append(S)
zoom(27.9, 1.0, 0.35)
S.raw('<div class="persp" style="left:1050px;top:170px;width:300px;height:300px">')
gloss(S, "cap", 150, 150, 230, 230, "cap", 56, "", 116)
S.raw("</div>")
S.tilt(f"#{S.id('cap')}", S.t(28.64), -50, 25, -12, 8, 1.0); S.drift(f"#{S.id('cap')}", S.t(28.64) + 1.0, "rotationY", 10)
S.box("wm", 1440, 600, 900, 260, "wordmark-2", "ORANUSS<br>ACADEMY")
S.box("wma", 1440, 790, 900, 80, "label-t ar", "أورانوس أكاديمي", "font-size:56px;font-weight:700;color:#6D28D9;text-align:left")
S.up(f"#{S.id('wma')}", S.t(29.16), 20)
S.tw(f"tl.fromTo('#{S.id('wm')}',{{opacity:0,scale:1.15,filter:'blur(14px)'}},{{opacity:1,scale:1,filter:'blur(0px)',duration:.5,ease:'expo.out'}},{S.t(28.64) + 0.1:.3f});")
sfx(28.64, "bell", 2, -15)

# S05 29.95-34.0 full screen: one video multiplies into a wall of content (MO7TAWA)
S = Scene("s05", 29.95, 34.05, "zoom"); scenes.append(S)
lay(29.8, "circle", 0.5)
fullbg(S); WIPES.append(29.95); sfx(29.96, "whoosh.short", 2, -13)
S.raw(f'<div class="persp" style="left:0;top:0;width:1920px;height:1080px"><div id="{S.id("grid")}" class="wall">')
tints = ["#FFD9C2", "#CDE3FF", "#FFE9A8", "#C9F2DD", "#FFC9D2", "#D9D0FF", "#E2D8FF"]
k = 0
for r in range(5):
    for c in range(9):
        cx, cy = c - 4, r - 2
        S.raw(f'<div id="{S.id(f"g{k}")}" class="vcard glass" style="left:{960 + cx * 270 - 120}px;top:{540 + cy * 250 - 115}px">'
              f'<div class="thumb" style="background:{tints[(r * 9 + c) % 7]}"><div class="tplay">{icon("play", 26)}</div></div>'
              f'<div class="skel" style="position:absolute;left:18px;bottom:22px;width:140px;height:14px;border-radius:7px"></div></div>')
        d = abs(cx) + abs(cy)
        if d == 0:
            S.pop(f"#{S.id(f'g{k}')}", 0.15, 0.5, "expo.out", 0.6)
        else:
            S.tw(f"tl.fromTo('#{S.id(f'g{k}')}',{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.45,ease:'expo.out'}},{S.t(31.45) + d * 0.07:.3f});")
        k += 1
S.raw("</div></div>")
S.tw(f"tl.fromTo('#{S.id('grid')}',{{scale:2.6,rotationX:0,rotationZ:0}},{{scale:2.6,duration:.01}},0);"
     f"tl.to('#{S.id('grid')}',{{scale:.82,rotationX:24,rotationZ:-8,duration:1.3,ease:'power3.inOut'}},{S.t(31.45)});"
     f"tl.to('#{S.id('grid')}',{{rotationZ:-4,duration:{34.05 - 29.95 - S.t(31.45) - 1.6:.2f},ease:'none'}},{S.t(31.45) + 1.3:.3f});")
sfx(31.45, "whoosh.short", 0, -15)
S.box("kwbg", 960, 540, 760, 190, "glass", "", "border-radius:95px"); S.pop(f"#{S.id('kwbg')}", S.t(33.24), 0.7, "expo.out", 0.4)
kword(S, "kw", 960, 540, "المحتوى", S.t(33.24), 124, grad=[0], w=760); sfx(33.24, "hit", 2, -12)

# S06 34.05-39.5 value of content: keyword + gem beside the presenter
S = Scene("s06", 34.05, 39.48, "up"); scenes.append(S)
lay(33.95, "split", 0.5); zoom(34.1, 1.1, 0.6); zoom(36.9, 1.0, 0.5)
S.raw('<div class="persp" style="left:1240px;top:180px;width:420px;height:420px">')
gloss(S, "gem", 210, 210, 250, 250, "star", 70, "violet", 120)
S.raw("</div>")
S.tilt(f"#{S.id('gem')}", S.t(35.44), 50, 25, 14, 8, 1.0); S.drift(f"#{S.id('gem')}", S.t(35.44) + 1.0, "rotationY", -14)
kword(S, "kw", 1450, 720, "قيمة المحتوى", S.t(35.44), 96, grad=[0], w=900); sfx(35.44, "hit", 0, -13)
chip(S, "dar", 1450, 850, "ضروري ف كل مشروع", "check", "green", fs=34, h=80)
S.pop(f"#{S.id('dar')}", S.t(36.90), 0.6, "expo.out", 0.5); sfx(36.90, "pop", 3, -16)

# S07 39.5-45.5 any project needs content: project tiles get content
S = Scene("s07", 39.48, 45.55, "left"); scenes.append(S)
zoom(39.5, 1.06, 0.5)
for i, (ic, kind) in enumerate((("briefcase", ""), ("cart", "warm"), ("cap", "deep"))):
    x = 1130 + i * 250
    S.raw(f'<div class="persp" style="left:{x - 120}px;top:300px;width:240px;height:240px">')
    gloss(S, f"p{i}", 120, 120, 190, 190, ic, 48, kind, 92)
    S.raw("</div>")
    S.tilt(f"#{S.id(f'p{i}')}", S.t(39.86) + i * 0.1, -40, 20, -10, 6, 0.9)
    S.box(f"pl{i}", x + 70, 330, 64, 64, "tplay badge-play", icon("play", 26)); S.pop(f"#{S.id(f'pl{i}')}", S.t(42.05) + i * 0.08, 0.2, "back.out(2)", 0.45)
sfx(39.86, "pop", 0, -16); sfx(42.05, "pop", 1, -15)
kword(S, "kw", 1380, 700, "أي مشروع", S.t(39.86), 100, grad=[1], w=900)
chip(S, "c", 1380, 830, "خاصو المحتوى", "film", fs=34, h=80); S.pop(f"#{S.id('c')}", S.t(42.05), 0.6, "expo.out", 0.5)

# S08 45.5-49.3 our social pages: phone feed
S = Scene("s08", 45.55, 49.25, "blur"); scenes.append(S)
zoom(45.6, 1.0, 0.5); sfx(45.59, "whoosh.short", 1, -14)
feed = "".join(f'<div class="feed-card" style="top:{90 + i * 250}px"><div class="thumb" style="left:14px;right:14px;top:14px;height:150px;background:{tints[i % 7]}"><div class="tplay">{icon("play", 26)}</div></div>'
               f'<div class="skel" style="position:absolute;left:20px;bottom:24px;width:180px;height:14px;border-radius:7px"></div></div>' for i in range(8))
S.raw('<div class="persp" style="left:1220px;top:90px;width:440px;height:800px">')
phone(S, "ph", 220, 380, 700, f'<div id="{S.id("feed")}" class="feed">{feed}</div>')
S.raw("</div>")
S.tilt(f"#{S.id('ph')}", S.t(46.11), -40, 10, -14, 4, 1.0); S.drift(f"#{S.id('ph')}", S.t(46.11) + 1.0, "rotationY", 6)
S.tw(f"tl.fromTo('#{S.id('feed')}',{{y:0}},{{y:-900,duration:{49.25 - 45.55 - S.t(46.11) + 0.2:.2f},ease:'none'}},{S.t(46.11) + 0.3:.3f});")
for i, (x, y) in enumerate(((1640, 330), (1700, 520), (1610, 700))):
    S.box(f"h{i}", x, y, 70, 70, "heart-pop", icon("star", 40, "#fff")); S.pop(f"#{S.id(f'h{i}')}", S.t(47.65) + i * 0.18, 0.2, "back.out(2.2)", 0.45)
sfx(47.65, "tick", 0, -17)
kword(S, "kw", 1440, 920, "SOCIAL MEDIA", S.t(46.53), 66, grad=[0], w=900)

# S09 49.3-61.9 full screen: learn with me, 3 steps
S = Scene("s09", 49.25, 61.85, "zoom"); scenes.append(S)
lay(49.1, "circle", 0.5)
fullbg(S); WIPES.append(49.25); sfx(49.29, "whoosh.short", 2, -13)
steps = ((52.53, "cap", "تعلّم"), (56.27, "spark", "فهم"), (57.08, "play", "خدم"))
S.raw(f'<svg class="flow" viewBox="0 0 1920 1080" width="1920" height="1080"><path id="{S.id("ln")}" d="M1400 470 L 520 470"/></svg>')
S.tw(f"(()=>{{const p=document.querySelector('#{S.id('ln')}');const L=p.getTotalLength();gsap.set(p,{{strokeDasharray:L,strokeDashoffset:L}});"
     f"tl.to(p,{{strokeDashoffset:0,duration:4.6,ease:'none'}},{S.t(52.53)});}})();")
for i, (t0, ic, lab) in enumerate(steps):
    x = 1400 - i * 440   # Arabic reading order: step 01 on the right
    glass(S, f"c{i}", x, 470, 340, 400, "", 40)
    S.tw(f"tl.fromTo('#{S.id(f'c{i}')}',{{opacity:0,y:80,scale:.9}},{{opacity:.55,y:0,scale:.94,duration:.7,ease:'expo.out'}},{S.t(49.61) + i * 0.1:.3f});"
         f"tl.to('#{S.id(f'c{i}')}',{{opacity:1,scale:1,duration:.4,ease:'expo.out'}},{S.t(t0)});")
    S.raw(f'<div class="persp" style="left:{x - 110}px;top:290px;width:220px;height:220px">')
    gloss(S, f"i{i}", 110, 110, 170, 170, ic, 44, ["", "violet", "deep"][i], 84)
    S.raw("</div>")
    S.tilt(f"#{S.id(f'i{i}')}", S.t(t0), -40, 20, -10, 6, 0.8)
    S.box(f"n{i}", x + 130, 300, 70, 70, "step on", f"<span>{i + 1:02d}</span>", "border-radius:50%"); S.pop(f"#{S.id(f'n{i}')}", S.t(t0), 0.3, "back.out(1.8)", 0.5)
    S.box(f"l{i}", x, 590, 320, 80, "label-t ar", lab, "font-size:52px;font-weight:700"); S.up(f"#{S.id(f'l{i}')}", S.t(t0) + 0.1, 20)
    sfx(t0, "tick", i, -15)
p, n = title(S, "ttl", 960, 150, "تعلّم معايا", 84); S.words(p, n, S.t(52.53), 0.25)
chip(S, "m1", 1180, 820, "مشروعك", "briefcase", fs=38, h=84); S.pop(f"#{S.id('m1')}", S.t(58.55), 0.6, "expo.out", 0.5)
chip(S, "m2", 760, 820, "مشاريع أخرى", "layers", fs=38, h=84); S.pop(f"#{S.id('m2')}", S.t(59.72), 0.6, "expo.out", 0.5)
sfx(58.55, "pop", 1, -16); sfx(59.72, "pop", 2, -16)

# S10 61.9-68.0 full screen: offer it as a service (KHIDMA), people who need content
S = Scene("s10", 61.85, 67.95, "zoom"); scenes.append(S)
lay(61.7, "circle", 0.5)
fullbg(S); WIPES.append(61.85); sfx(61.92, "whoosh.long", 0, -12)
S.raw('<div class="persp" style="left:810px;top:230px;width:300px;height:300px">')
gloss(S, "bc", 150, 150, 240, 240, "briefcase", 60, "", 120)
S.raw("</div>")
S.tilt(f"#{S.id('bc')}", 0.2, -50, 25, -12, 8, 1.0); S.drift(f"#{S.id('bc')}", 1.2, "rotationY", 14)
kword(S, "kw", 960, 720, "خدمة", S.t(64.98), 150, grad=[0]); sfx(64.98, "hit", 0, -11)
import math
for i in range(8):
    a = math.radians(-90 + i * 45); x = 960 + 560 * math.cos(a); y = 400 + 300 * math.sin(a)
    if 520 < y < 760 and 640 < x < 1280:
        continue
    avatar(S, f"a{i}", round(x), round(y), 110, f"a{i % 6 + 1}")
    S.pop(f"#{S.id(f'a{i}')}", S.t(66.50) + i * 0.06, 0.3, "back.out(1.6)", 0.5)
    S.box(f"q{i}", round(x) + 60, round(y) - 60, 60, 60, "tplay badge-play", icon("play", 22)); S.pop(f"#{S.id(f'q{i}')}", S.t(67.30) + i * 0.05, 0.2, "back.out(2)", 0.4)
sfx(66.50, "pop", 3, -16)

# S11 68.0-75.5 people with no project / wanting to start
S = Scene("s11", 67.95, 75.45, "left"); scenes.append(S)
lay(67.85, "split", 0.5); zoom(68.0, 1.08, 0.6); zoom(72.0, 1.0, 0.5)
for i, (t0, ic, lab, kind) in enumerate(((68.49, "briefcase", "بلا مشروع", "deep"), (70.99, "rocket", "بغاو يبداو", "violet"), (73.47, "spark", "كيفكرو", ""))):
    y = 300 + i * 170
    S.box(f"r{i}", 1400, y, 680, 140, "glass notif",
          f'<div class="gloss {kind}" style="right:22px;top:22px;width:96px;height:96px;border-radius:26px"><div class="gl-ic">{icon(ic, 46)}</div></div>'
          f'<div class="row-t ar">{html.escape(lab)}</div>', "border-radius:34px")
    S.side(f"#{S.id(f'r{i}')}", S.t(t0), 140, 0.7); sfx(t0, "pop", i, -16)

# S12 75.5-78.6 propose the service, work together
S = Scene("s12", 75.45, 78.6, "blur"); scenes.append(S)
zoom(75.5, 1.06, 0.5); sfx(75.79, "whoosh.short", 0, -14)
avatar(S, "you", 1180, 400, 170, "me"); S.pop(f"#{S.id('you')}", S.t(75.79), 0.4, "back.out(1.6)", 0.55)
avatar(S, "cl", 1660, 400, 170, "a2"); S.pop(f"#{S.id('cl')}", S.t(76.64), 0.4, "back.out(1.6)", 0.55)
S.raw(f'<svg class="flow" viewBox="0 0 1920 1080" width="1920" height="1080"><path id="{S.id("lk")}" d="M1280 400 C 1360 330, 1480 330, 1560 400"/></svg>')
S.tw(f"(()=>{{const p=document.querySelector('#{S.id('lk')}');const L=p.getTotalLength();gsap.set(p,{{strokeDasharray:L,strokeDashoffset:L}});"
     f"tl.to(p,{{strokeDashoffset:0,duration:.6,ease:'power2.inOut'}},{S.t(77.11)});}})();")
S.raw('<div class="persp" style="left:1310px;top:480px;width:300px;height:300px">')
S.box("coins", 150, 150, 200, 200, "coins", "".join(f'<div class="coin" style="top:{110 - j * 26}px"></div>' for j in range(4)))
S.raw("</div>")
S.tilt(f"#{S.id('coins')}", S.t(77.86), -30, 30, -10, 20, 0.9); sfx(77.86, "bell", 4, -15)
kword(S, "kw", 1420, 880, "تعاونو", S.t(77.86), 100, grad=[0], w=900)

# S13 83.4-88.9 intro + proof: keyword stack beside the presenter
S = Scene("s13", 83.4, 88.9, "left"); scenes.append(S)
lay(78.6, "full", 0.55); zoom(78.6, 1.0, 0.55); zoom(80.6, 1.14, 0.4); lay(83.35, "split", 0.5); zoom(83.35, 1.0, 0.5)
sfx(80.6, "whoosh.short", 1, -16)
kword(S, "k1", 1400, 300, "مقدمة", S.t(83.99), 100, w=900); sfx(83.99, "hit", 1, -13)
kword(S, "k2", 1400, 450, "و دليل", S.t(84.67), 100, grad=[1], w=900); sfx(84.67, "pop", 1, -15)
kword(S, "k3", 1400, 640, "VIDEO EDITING", S.t(86.29), 104, grad=[0], w=1000); sfx(86.29, "hit", 2, -12)
chip(S, "ai", 1400, 790, "بالـ AI", "chip", fs=40, h=92); S.pop(f"#{S.id('ai')}", S.t(87.55), 0.6, "expo.out", 0.5)

# S14 88.9-93.7 full screen: more videos on the channel (series)
S = Scene("s14", 88.9, 93.7, "zoom"); scenes.append(S)
lay(88.75, "circle", 0.5)
fullbg(S); WIPES.append(88.9); sfx(88.95, "whoosh.long", 1, -12)
S.raw(f'<div id="{S.id("row")}" class="ep-row">' + "".join(
    f'<div id="{S.id(f"e{i}")}" class="ep glass" style="left:{i * 520}px"><div class="thumb ep-th" style="background:{tints[(i + 2) % 7]}"><div class="tplay big">{icon("play", 40)}</div></div>'
    f'<div class="ep-badge">EP {i + 1:02d}</div><div class="skel" style="position:absolute;left:28px;bottom:40px;width:260px;height:18px;border-radius:9px"></div></div>' for i in range(7)) + "</div>")
S.tw(f"tl.fromTo('#{S.id('row')}',{{x:700}},{{x:-1500,duration:{93.7 - 88.9 - 0.3:.2f},ease:'none'}},0.05);")
for i in range(7):
    S.tw(f"tl.fromTo('#{S.id(f'e{i}')}',{{opacity:0,y:60}},{{opacity:1,y:0,duration:.5,ease:'expo.out'}},{0.15 + i * 0.12:.2f});")
p, n = title(S, "ttl", 960, 170, "AI EDITING SERIES", 80); S.words(p, n, S.t(89.82), 0.1); sfx(89.82, "pop", 0, -15)
chip(S, "yt", 960, 860, "كل جديد ف YouTube", "play", fs=38, h=88); S.pop(f"#{S.id('yt')}", S.t(92.00), 0.6, "expo.out", 0.5)

# S15 95.8-108.6 practical sessions, one Friday a month: calendar + questions
S = Scene("s15", 95.75, 108.55, "left"); scenes.append(S)
lay(93.6, "full", 0.5); zoom(93.75, 1.12, 0.5); lay(95.75, "split", 0.55); zoom(95.75, 1.0, 0.55); sfx(95.82, "whoosh.short", 2, -14)
cells = ""
for r in range(5):
    for c in range(7):
        d = r * 7 + c + 1
        fri = (c == 4 and r == 1)
        cells += f'<div {"id=" + chr(34) + S.id("fri") + chr(34) if fri else ""} class="cal-cell{" fri" if fri else ""}" style="left:{30 + c * 92}px;top:{150 + r * 84}px">{d if d <= 30 else ""}</div>'
S.raw('<div class="persp" style="left:1060px;top:150px;width:760px;height:660px">')
glass(S, "cal", 380, 330, 700, 600, f'<div class="cal-head">{icon("cap", 40, "#7C3AED")}<b class="ar">جلسة تطبيقية</b></div>'
      + "".join(f'<div class="cal-dow" style="left:{30 + c * 92}px">{d}</div>' for c, d in enumerate("نثرخجسح")) + cells, 44)
S.raw("</div>")
S.tilt(f"#{S.id('cal')}", S.t(96.03), -35, 15, -10, 5, 1.0); S.drift(f"#{S.id('cal')}", S.t(96.03) + 1.0, "rotationY", 6)
S.tw(f"tl.to('#{S.id('fri')}',{{background:'radial-gradient(130% 130% at 25% 15%,#e2d8ff,#8b5cf6 40%,#4c1d95)',color:'#fff',scale:1.18,duration:.35,ease:'back.out(2)'}},{S.t(97.26)});")
sfx(97.26, "hit", 2, -12)
chip(S, "m", 1440, 860, "جلسة وحدة ف الشهر", "check", "green", fs=38, h=88); S.pop(f"#{S.id('m')}", S.t(97.83), 0.6, "expo.out", 0.5)
for i, (x, y, t0) in enumerate(((1120, 250, 102.04), (1790, 300, 102.4), (1830, 640, 104.32), (1110, 700, 104.7), (1450, 180, 105.04))):
    S.box(f"q{i}", x, y, 96, 96, "qbubble", "?"); S.pop(f"#{S.id(f'q{i}')}", S.t(t0), 0.2, "back.out(2)", 0.5)
    S.tw(f"tl.to('#{S.id(f'q{i}')}',{{y:-40,duration:{108.55 - 95.75 - S.t(t0) - 0.8:.2f},ease:'none'}},{S.t(t0) + 0.5:.3f});")
sfx(102.04, "pop", 3, -16); sfx(104.32, "pop", 0, -16)
S.tw(f"tl.to('#{S.id('m')}',{{opacity:0,y:20,filter:'blur(8px)',duration:.2,ease:'power3.in'}},{S.t(105.04) - 0.2:.3f});")
kword(S, "kw", 1440, 860, "أسئلة تقنية", S.t(105.04), 84, grad=[1], w=900)

# end: face only, a slow push to the last word
lay(108.5, "full", 0.6); zoom(109.3, 1.06, TOTAL - 109.3 - 0.1)
sfx(108.76, "swell", 1, -18)

for S in scenes:
    S.write(COMP)

# ---------- fx: purple wipes into the full-screen beats ----------
wipe_html = "\n    ".join(f'<div id="fx-w{i}" class="wipe"><div class="wipe-in"></div></div>' for i in range(len(WIPES)))
wipe_js = "\n    ".join(f"tl.fromTo('#fx-w{i}',{{xPercent:-130}},{{xPercent:130,duration:.62,ease:'power2.inOut'}},{t - 0.31:.3f});" for i, t in enumerate(WIPES))
open(os.path.join(COMP, "fx.html"), "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
  </style>
  <div id="root" data-composition-id="fx" data-width="1920" data-height="1080" data-layout-ignore>
    {wipe_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    gsap.set('.wipe', {{xPercent: -130}});
    {wipe_js}
    window.__timelines["fx"] = tl;
  </script>
</template>
""")
open(os.path.join(COMP, "bg.html"), "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
  </style>
  <div id="root" data-composition-id="bg" data-width="1920" data-height="1080" data-layout-ignore>
    <div class="bg-base"></div>
    <div id="bg-g1" class="bg-glow g1"></div>
    <div id="bg-g2" class="bg-glow g2"></div>
    <div class="halo"></div>
    <div class="bg-grid"></div>
    <div class="floor"></div>
    <div id="bg-o1" class="sphere bgo" style="left:-60px;top:760px;width:260px;height:260px"></div>
    <div id="bg-o2" class="sphere bgo soft" style="left:1720px;top:-70px;width:220px;height:220px"></div>
    <div id="bg-o3" class="sphere bgo soft" style="left:1790px;top:870px;width:120px;height:120px"></div>
    <div id="bg-o4" class="sphere bgo soft" style="left:90px;top:80px;width:90px;height:90px"></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.to('#bg-g1', {{x: 260, y: 80, duration: {TOTAL}, ease: 'none'}}, 0);
    tl.to('#bg-g2', {{x: -220, y: -60, duration: {TOTAL}, ease: 'none'}}, 0);
    tl.to('#bg-o1', {{x: 120, y: -60, rotation: 30, duration: {TOTAL}, ease: 'none'}}, 0);
    tl.to('#bg-o2', {{x: -90, y: 70, duration: {TOTAL}, ease: 'none'}}, 0);
    tl.to('#bg-o3', {{x: -60, y: -40, duration: {TOTAL}, ease: 'none'}}, 0);
    tl.to('#bg-o4', {{x: 50, y: 60, duration: {TOTAL}, ease: 'none'}}, 0);
    window.__timelines["bg"] = tl;
  </script>
</template>
""")

# ---------- index: bg, presenter cut-out on a camera rig, raw opening, scenes, wipes, audio ----------
cam_js, prev = [], "full"
for t, state, d in sorted(CAM):
    clip, x, y, sc = LAYOUTS[state]
    cam_js.append(f"tl.to('#cam',{{clipPath:'{clip}',x:{x},y:{y},scale:{sc},duration:{max(d, 0.01)},ease:'power3.inOut'}},{t});")
    on = 1 if state == "split" else 0
    cam_js.append(f"tl.to('#cardframe',{{opacity:{on},duration:{max(d, 0.01)},ease:'power2.inOut'}},{t});")
    cam_js.append(f"tl.to('#ring',{{opacity:{1 if state == 'circle' else 0},duration:{max(d * 0.6, 0.01)},ease:'power2.inOut'}},{t + (d * 0.4 if state == 'circle' else 0):.3f});")
    cam_js.append(f"tl.set('#cam',{{zIndex:{7 if state == 'circle' else 3}}},{t if state == 'circle' else t + d:.3f});")
for t, sc, d in sorted(ZOOM):
    cam_js.append(f"tl.to('#camz',{{scale:{sc},duration:{max(d, 0.01)},ease:'power2.inOut'}},{t});")
hosts = "\n      ".join(
    f'<div id="{S.sid}" data-composition-id="{S.sid}" data-composition-src="compositions/{S.sid}.html" data-start="{S.start}" data-duration="{round(S.end - S.start, 3)}" '
    f'data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:6"></div>' for S in scenes)
CSS = open(os.path.join(HERE, "ai_editing_v2.css")).read() + open(os.path.join(HERE, "intro_ai.css")).read()
open(os.path.join(PROJ, "index.html"), "w").write(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
{CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      <div id="bg" data-composition-id="bg" data-composition-src="compositions/bg.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:1"></div>
      <div id="cardframe" class="cardframe" style="z-index:2"></div>
      <div id="cam" class="cam" style="z-index:3"><div id="camz" class="camz">
        <video id="aroll" class="clip" src="assets/aroll.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="1"></video>
      </div></div>
      <div id="ring" class="ring-frame" style="z-index:8"></div>
      <video id="rawclip" class="clip" src="assets/raw.mp4" muted playsinline data-start="0" data-duration="3.12" data-track-index="1" style="z-index:4"></video>
      {hosts}
      <div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:8"></div>
      <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      gsap.set('#cam', {{transformOrigin: '{FACE[0]}px {FACE[1]}px', clipPath: 'inset(0px 0px 0px 0px round 0px)'}});
      gsap.set('#camz', {{transformOrigin: '{FACE[0]}px {FACE[1]}px'}});
      gsap.set(['#cardframe', '#ring'], {{opacity: 0}});
      {chr(10).join("      " + j for j in cam_js)}
      tl.to({{}}, {{duration: 0.001}}, {TOTAL - 0.01});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")
json.dump(sorted(CUES), open(os.path.join(WK, "sfx_cues.json"), "w"), indent=0)
print("ok", len(scenes), "scenes,", len(CUES), "sfx,", "logo: claude-mark.png", "total", TOTAL)
