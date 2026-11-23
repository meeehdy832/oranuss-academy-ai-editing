# Developed by Mehdi ORANUSS | Powered by Claude
"""1112 reel (9:16, 61.7 s): josephswork-blue-ui in Oranuss purple (reference/styles/short/josephswork-blue-ui/STYLE.md).
Real footage (work/1112/tight.mov: silence 23.28-30.0 cut, graded, 30 fps) + animations + GPT Image 2 icons/images.
Face rule: macOS Vision face box is y 748-1380 in every sample (work/1112/faces.json); nothing is drawn over it.
Layouts: FULL face (graphics only in the top band y<640, captions under the chin y~1440) / SPLIT (purple stage
top 0-900, footage moved down 190 px so the face sits under it) / STAGE (full-screen animation, no face).
Captions: only clearly heard words, in Arabic script (Graphik Arabic) with one purple accent word.
Writes hf/1112/index.html and work/1112/sfx_cues.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "1112")
WK = os.path.join(HERE, "..", "work", "1112")
TOTAL = 63.46                  # 61.66 of footage + 1.8 s hold on the last frame for the end card
CUT = 6.72                     # removed silence (orig 23.28-30.0)
def T(orig):                   # original recording time -> tight timeline
    return round(orig - CUT if orig >= 30.0 else orig, 3)

# ---------------- layout states (time, state) ----------------
LAY = [(0, "full"), (3.0, "split"), (T(10.1), "stage"), (T(17.64), "split"), (T(23.28), "full"),
       (T(39.88), "stage"), (T(46.72), "split"), (T(51.2), "stage"), (T(57.4), "split"), (T(67.14), "full")]

# ---------------- captions (start, end, words, accent index) ----------------
CAPS = [(0.0, 2.1, "حنا دابا فاللايف", [2]), (2.12, 4.3, "هاد الفيديو", [1]), (4.35, 5.6, "معاكم فالحصة", [1]),
        (6.66, 8.2, "الذكاء الاصطناعي", [0, 1]), (8.24, 9.9, "ويقدر يمونتيه", [1]),
        (12.86, 14.4, "كيزيد الإيقونات", [1]), (15.38, 17.5, "اللي ما كيتماشاوش مع السكريبت", [4]),
        (18.9, 19.9, "معايا فاللايف", [1]), (22.04, 23.2, "على شكل الإيقونات", [2]),
        (T(30.0), T(30.9), "كل ما خصك تدير", [3]), (T(32.3), T(33.1), "المراحل", [0]),
        (T(36.38), T(37.2), "تدرب الذكاء الاصطناعي", [1, 2]), (T(38.1), T(39.6), "الفيديوهات بالطريقة اللي بغيتي", [0]),
        (T(45.58), T(46.4), "ف أسرع وقت", [1, 2]), (T(48.25), T(49.2), "تتعلمو الذكاء الاصطناعي", [1, 2]),
        (T(53.27), T(54.6), "يحتاجو المحتوى بشكل كبير", [1]), (T(59.02), T(59.9), "الحصة ديال اليوم", [2]),
        (T(61.06), T(61.85), "المحتوى", [0]), (T(62.86), T(63.9), "تبني الجمهور ديالك", [1]),
        (T(64.72), T(65.9), "داخل مواقع التواصل الاجتماعي", [2, 3])]
def cap_y(t):
    st = [s for s, _ in [(a, b) for a, b in LAY]]
    cur = [s for a, s in LAY if a <= t + 0.05][-1]
    return {"full": 1440, "split": 1600, "stage": 1560}[cur]

H, J, CUES = [], [], []        # html, timeline js, sfx cues (t, id, align, extra_db, trim)
def h(s): H.append(s)
def tw(s): J.append(s)
def sfx(t, sid, align="peak", extra=0, trim=None): CUES.append((round(t, 3), sid, align, extra, trim))

# ---------------- camera + stage rig ----------------
STAGE_CLIP = {"full": "inset(0px 0px 1920px 0px)", "split": "inset(0px 0px 1020px 0px)", "stage": "inset(0px 0px 0px 0px)"}
prev = "full"
for t, st in LAY:
    if t == 0:
        continue
    d = 0.45
    tw(f"tl.to('#stage',{{clipPath:'{STAGE_CLIP[st]}',duration:{d},ease:'expo.inOut'}},{t - 0.12:.3f});")
    cam_y = 190 if st == "split" else 0
    tw(f"tl.to('#cam',{{y:{cam_y},duration:{d},ease:'expo.inOut'}},{t - 0.12:.3f});")
    # face blur-in on every layout change (the josephswork focus pull)
    tw(f"tl.fromTo('#camv',{{filter:'blur(14px)'}},{{filter:'blur(0px)',duration:.35,ease:'power2.out',immediateRender:false}},{t + 0.05:.3f});")
    sfx(t, "WH-163" if st == "stage" else "WH-012", "peak", -2 if st == "stage" else -3)
    prev = st

# ---------------- scenes ----------------
def grp(gid, t0, t1, inner, style=""):
    h(f'<div id="{gid}" class="grp" style="{style}">{inner}</div>')
    tw(f"tl.set('#{gid}',{{autoAlpha:1}},{t0:.3f});tl.to('#{gid}',{{autoAlpha:0,duration:.25,ease:'power2.in'}},{t1 - 0.25:.3f});")
def rise(sel, t, dy=80, d=0.5, blur=10):
    tw(f"tl.fromTo('{sel}',{{y:{dy},opacity:0,filter:'blur({blur}px)'}},{{y:0,opacity:1,filter:'blur(0px)',duration:{d},ease:'expo.out'}},{t:.3f});")
def pop(sel, t, s0=0.4, d=0.55, ease="back.out(1.8)"):
    tw(f"tl.fromTo('{sel}',{{scale:{s0},opacity:0}},{{scale:1,opacity:1,duration:{d},ease:'{ease}'}},{t:.3f});")
def slam(sel, t):
    tw(f"tl.fromTo('{sel}',{{scale:1.6,opacity:0,filter:'blur(18px)'}},{{scale:1,opacity:1,filter:'blur(0px)',duration:.4,ease:'expo.out'}},{t:.3f});")
def icon(src, x, y, w, rot=0, extra=""):
    return f'<img class="icon" src="assets/icon_{src}.png" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg){extra}"/>'

# S1 hook 0-3: full face, LIVE + AI slam in the top band
grp("s1", 0, 3.05,
    '<div id="live" class="pill dark" style="left:70px;top:250px"><i class="rec"></i>LIVE</div>'
    '<div id="ai" class="mega" style="top:300px">AI</div>'
    '<div id="aisub" class="sub" style="top:540px">EDITING</div>'
    '<div id="i1" class="ic" style="left:800px;top:240px;width:210px">' + '<img src="assets/icon_ai.png"/></div>'
    '<div id="i2" class="ic" style="left:70px;top:400px;width:150px">' + '<img src="assets/icon_scissors.png"/></div>')
pop("#live", 0.1, 0.6, 0.4, "expo.out"); slam("#ai", 0.35); rise("#aisub", 0.6, 30, 0.45)
pop("#i1", 0.7); pop("#i2", 0.85)
tw("tl.to('#i1',{y:-14,rotation:16,duration:2.2,ease:'sine.inOut'},1.2);tl.to('#i2',{y:12,rotation:-16,duration:2.2,ease:'sine.inOut'},1.2);")
sfx(0.35, "IM-003", "peak", -6, 1.6); sfx(0.1, "PO-016", "peak", -2); sfx(0.7, "PO-006", "peak", -2); sfx(0.85, "PO-008", "peak", -3)

# S2 split 3-10.1: AI chat card, the clip drops in, prompt types, send, progress
chat = ('<div id="chat" class="card" style="left:100px;top:150px;width:880px;height:650px">'
        '<div class="chat-h"><img src="assets/icon_ai.png"/><b>AI Editor</b><span class="online">online</span></div>'
        '<div id="clip" class="clipcard"><img src="assets/th_4.jpg"/><div class="cliplab">▶ 1112.mp4 · 1:08</div></div>'
        '<div class="prompt"><div id="ptext" class="ptext"></div><i id="caret" class="caret"></i>'
        '<div id="send" class="send"><svg width="40" height="40" viewBox="0 0 24 24"><path d="M3 11.5 21 3l-8.5 18-2-7.5z" fill="#fff"/></svg></div></div>'
        '<div id="prog" class="prog"><i id="progb"></i><span>Editing your video…</span></div></div>')
grp("s2", 3.0, T(10.1) + 0.05, chat)
rise("#chat", 3.25, 120, 0.6); rise("#clip", 3.75, -160, 0.55, 14)
tw("(()=>{const el=document.querySelector('#ptext');const s='Edit this video ✨';const o={n:0};"
   "tl.to(o,{n:s.length,duration:1.4,ease:'none',onUpdate:()=>{el.textContent=s.slice(0,Math.round(o.n));}},5.7);})();")
tw("tl.fromTo('#caret',{opacity:1},{opacity:0,duration:.4,repeat:9,yoyo:true,ease:'steps(1)'},3.3);")
tw("tl.fromTo('#send',{scale:1},{scale:.82,duration:.08,yoyo:true,repeat:1,ease:'power2.inOut'},8.65);")
tw("tl.fromTo('#prog',{opacity:0,y:20},{opacity:1,y:0,duration:.3,ease:'expo.out'},8.85);tl.fromTo('#progb',{scaleX:0},{scaleX:1,duration:1.15,ease:'power1.inOut'},8.9);")
sfx(3.25, "WH-166", "peak", -3); sfx(3.75, "PO-022", "peak", -2); sfx(5.7, "UI-004", "start", -8, 1.4); sfx(8.65, "UI-029", "peak", -3); sfx(8.9, "DA-002", "start", -5)

# S3 stage 10.1-17.64: the timeline edits itself
tl_html = ('<div class="ttl" id="t3" style="top:240px">كيزيد <span class="acc">الإيقونات</span></div>'
           '<div id="tlc" class="card dark" style="left:70px;top:420px;width:940px;height:620px">'
           '<div class="dots"><i></i><i></i><i></i></div>'
           '<div class="trk" style="top:92px">V1</div><div class="clips" style="top:80px">'
           '<div id="c1" class="clp" style="flex:1.2;background-image:url(assets/th_11.jpg)"></div>'
           '<div id="c2" class="clp" style="flex:1;background-image:url(assets/th_20.jpg)"></div>'
           '<div id="c3" class="clp" style="flex:.8;background-image:url(assets/th_26.jpg)"><b id="x3" class="xx">✕</b></div>'
           '<div id="c4" class="clp" style="flex:1;background-image:url(assets/th_34.jpg)"></div></div>'
           '<div class="trk" style="top:245px">FX</div><div class="fxrow" style="top:228px">'
           + "".join(f'<img id="fx{i}" src="assets/icon_{n}.png"/>' for i, n in enumerate(["sparkle", "play", "megaphone", "clapper", "people"])) +
           '</div><div class="trk" style="top:355px">A1</div><div id="wave" class="wave" style="top:335px"></div>'
           '<div id="ph" class="playhead"></div>'
           '<div class="legend"><span>✂ cut</span><span class="acc2">+ icons</span><span class="red">− off-script</span></div></div>'
           '<div id="sc" class="ic" style="left:640px;top:330px;width:200px"><img src="assets/icon_scissors.png"/></div>')
grp("s3", T(10.1), T(17.64) + 0.05, tl_html)
rise("#t3", 10.2, 40, 0.5); rise("#tlc", 10.25, 140, 0.6)
tw("tl.fromTo('#ph',{x:0},{x:820,duration:7.0,ease:'none'},10.4);")
tw("tl.fromTo('#sc',{x:300,y:-200,rotation:60,opacity:0},{x:0,y:0,rotation:14,opacity:1,duration:.55,ease:'expo.out'},11.6);"
   "tl.to('#c1',{x:-10,duration:.2,ease:'power2.out'},12.1);tl.to('#c2',{x:10,duration:.2,ease:'power2.out'},12.1);")
for i in range(5):
    tw(f"tl.fromTo('#fx{i}',{{y:-220,opacity:0,filter:'blur(8px)'}},{{y:0,opacity:1,filter:'blur(0px)',duration:.45,ease:'back.out(1.6)'}},{12.86 + i * 0.12:.3f});")
tw("tl.to('#c3',{filter:'grayscale(1) brightness(.45)',duration:.3},15.62);tl.fromTo('#x3',{scale:2.2,opacity:0},{scale:1,opacity:1,duration:.35,ease:'back.out(2)'},15.62);")
sfx(10.25, "WH-174", "peak", -3); sfx(11.6, "WH-004", "peak", 0); sfx(12.1, "CA-001", "peak", 0)
for i in range(5):
    sfx(12.86 + i * 0.12, ["PO-006", "PO-008", "PO-009", "PO-006", "PO-008"][i], "peak", -4)
sfx(15.62, "NG-007", "peak", -12)

# S4 split 17.64-23.28: icons fly into a grid on top
names = ["ai", "scissors", "clapper", "sparkle", "megaphone", "calendar", "people", "play"]
grid = "".join(f'<div id="g{i}" class="ic" style="left:{90 + (i % 4) * 230}px;top:{150 + (i // 4) * 280}px;width:210px"><img src="assets/icon_{n}.png"/></div>' for i, n in enumerate(names))
grp("s4", T(17.64), T(23.28) + 0.02, grid + '<div id="gl" class="glowbar"></div>')
for i in range(8):
    ang = (i * 47) % 360
    tw(f"tl.fromTo('#g{i}',{{x:{int(400 * (1 if i % 2 else -1))},y:{-300 + (i * 61) % 200},rotation:{ang - 180},scale:.3,opacity:0,filter:'blur(10px)'}},"
       f"{{x:0,y:0,rotation:{(-8 if i % 2 else 8)},scale:1,opacity:1,filter:'blur(0px)',duration:.7,ease:'expo.out'}},{17.85 + i * 0.12:.3f});")
tw("tl.to('#s4 .ic',{rotation:0,duration:.5,ease:'back.out(2)',stagger:.03},22.0);tl.fromTo('#gl',{opacity:0,scaleX:.2},{opacity:1,scaleX:1,duration:.5,ease:'expo.out'},22.04);")
sfx(17.85, "WH-176", "peak", -2); sfx(22.04, "RW-001", "peak", -3)

# S5 full face 23.28-33.16: 3-step card in the top band
steps = [("المراحل", T(32.3)), ("تدرب الذكاء الاصطناعي", T(36.38)), ("بالطريقة اللي بغيتي", T(38.96))]
st_html = ('<div id="stc" class="card" style="left:80px;top:170px;width:920px;height:450px">'
           '<div class="st-h"><img src="assets/icon_sparkle.png"/><b class="ar">3 خطوات</b></div>'
           + "".join(f'<div id="st{i}" class="step" style="top:{120 + i * 106}px"><div class="dia"><b>{i + 1}</b></div>'
                     f'<div class="ar stt">{lab}</div><div id="ck{i}" class="ck"><svg width="30" height="30" viewBox="0 0 24 24"><path d="M4 12.5 9.5 18 20 6.5" stroke="#fff" stroke-width="3.2" fill="none" stroke-linecap="round"/></svg></div></div>'
                     for i, (lab, _) in enumerate(steps)) + '</div>')
grp("s5", T(30.0), T(39.88) + 0.05, st_html)
rise("#stc", T(30.0) + 0.15, -60, 0.6)
for i, (_, t) in enumerate(steps):
    tw(f"tl.fromTo('#st{i}',{{x:60,opacity:.35}},{{x:0,opacity:1,duration:.45,ease:'expo.out'}},{t - 0.067:.3f});"
       f"tl.to('#st{i}',{{background:'linear-gradient(90deg,#6D3BF5,#8B5CF6)',color:'#fff',duration:.3}},{t - 0.067:.3f});"
       f"tl.fromTo('#ck{i}',{{scale:0}},{{scale:1,duration:.4,ease:'back.out(2.2)'}},{t + 0.25:.3f});")
    if i < 2:
        tw(f"tl.to('#st{i}',{{background:'#F6F3FF',duration:.3}},{steps[i + 1][1] - 0.1:.3f});tl.to('#st{i} .stt',{{color:'#100820',duration:.3}},{steps[i + 1][1] - 0.1:.3f});")
    sfx(t + 0.25, ["PO-019", "PO-019", "RW-007"][i], "peak", -3)
sfx(T(30.0) + 0.15, "WH-091", "peak", -2)

# S6 stage 33.16-40.0: the future + a GPT Image 2 photo in a glass frame
grp("s6", T(39.88), T(46.72) + 0.05,
    '<div class="ttl" id="t6" style="top:230px"><span class="acc">مستقبلا</span></div>'
    '<div id="frame" class="glass" style="left:190px;top:380px;width:700px;height:1050px"><div class="inner"><img id="desk" src="assets/img_desk.png"/></div></div>'
    '<div id="fast" class="pill light" style="left:640px;top:1330px"><svg width="40" height="40" viewBox="0 0 24 24"><path d="M3 5v14l9-7zM12 5v14l9-7z" fill="#6D3BF5"/></svg>FAST</div>'
    '<div id="cal" class="ic" style="left:60px;top:1240px;width:200px"><img src="assets/icon_calendar.png"/></div>')
tw(f"tl.fromTo('#frame',{{y:300,rotation:6,opacity:0,filter:'blur(12px)'}},{{y:0,rotation:-3,opacity:1,filter:'blur(0px)',duration:.7,ease:'expo.out'}},{T(39.88) + 0.15:.3f});")
tw(f"tl.fromTo('#desk',{{scale:1.0}},{{scale:1.1,duration:6.6,ease:'none'}},{T(39.88) + 0.15:.3f});")
slam("#t6", T(43.08) - 0.067); pop("#cal", T(41.1)); pop("#fast", T(45.58) - 0.067, 0.5, 0.45)
tw(f"tl.to('#fast',{{x:30,duration:.25,yoyo:true,repeat:3,ease:'power1.inOut'}},{T(45.9):.3f});")
sfx(T(39.88) + 0.15, "WH-156", "peak", -4); sfx(T(43.08), "IM-029", "peak", -6, 1.4); sfx(T(41.1), "PO-009", "peak", -3); sfx(T(45.58), "WH-004", "peak", 0)

# S7 split 40.0-44.48: learn AI now, progress card on top
grp("s7", T(46.72), T(51.2) + 0.05,
    '<div id="lc" class="card" style="left:110px;top:200px;width:860px;height:520px">'
    '<img src="assets/icon_ai.png" style="position:absolute;left:50%;top:40px;width:200px;margin-left:-100px"/>'
    '<div class="ar lt">تعلّم الذكاء الاصطناعي</div><div class="bar"><i id="lb"></i></div>'
    '<div class="chips"><span id="ch1">AI</span><span id="ch2">Editing</span><span id="ch3">Content</span></div></div>')
rise("#lc", T(46.72) + 0.15, -80, 0.6)
tw(f"tl.fromTo('#lb',{{scaleX:0}},{{scaleX:.85,duration:2.6,ease:'power2.out'}},{T(48.25):.3f});")
for i in range(3):
    pop(f"#ch{i + 1}", T(48.25) + 0.4 + i * 0.25, 0.5, 0.45)
sfx(T(46.72) + 0.15, "WH-166", "peak", -3); sfx(T(48.25), "RW-006", "peak", -6, 1.6)

# S8 stage 44.48-50.68: people need lots of content, wall of video cards
thumbs = ["th_4", "th_11", "th_20", "th_26", "th_34", "th_47", "th_55"]
wall = "".join(f'<div class="vc" style="left:{-60 + (i % 4) * 300}px;top:{-120 + (i // 4) * 420}px;background-image:url(assets/{thumbs[i % 7]}.jpg)"><i class="vplay"></i></div>' for i in range(20))
grp("s8", T(51.2), T(57.4) + 0.05,
    f'<div id="wall" class="wall">{wall}</div><div class="wallfade"></div>'
    '<div class="ttl big" id="t8" style="top:700px"><span class="acc">المحتوى</span></div>'
    '<div id="t8b" class="sub ar" style="top:930px">بشكل كبير</div>')
tw(f"tl.fromTo('#wall',{{x:0,y:0,rotation:-8}},{{x:-260,y:-340,rotation:-8,duration:6.4,ease:'none'}},{T(51.2):.3f});")
tw(f"tl.fromTo('#s8 .vc',{{scale:.4,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:'expo.out',stagger:.035}},{T(51.2) + 0.1:.3f});")
slam("#t8", T(53.65) - 0.067); rise("#t8b", T(54.1) - 0.067, 30, 0.45)
sfx(T(51.2) + 0.1, "WH-158", "peak", -4); sfx(T(53.65), "IM-025", "peak", -6, 1.4)

# S9 split 50.68-60.42: bonus, community image, audience card
grp("s9", T(57.4), T(67.14) + 0.05,
    '<div id="bonus" class="pill gold" style="left:385px;top:60px">★ BONUS</div>'
    '<div id="comm" class="photo" style="left:60px;top:160px;width:960px;height:500px"><img id="commi" src="assets/img_community.png"/></div>'
    '<div id="aud" class="card row" style="left:110px;top:700px;width:860px;height:170px"><img src="assets/icon_people.png"/>'
    '<div class="ar"><div class="r1">تبني الجمهور ديالك</div><div class="r2">داخل مواقع التواصل الاجتماعي</div></div></div>')
pop("#bonus", T(57.4) + 0.2, 0.3, 0.5); rise("#comm", T(57.4) + 0.35, -100, 0.6)
tw(f"tl.fromTo('#commi',{{scale:1.0}},{{scale:1.08,duration:9.5,ease:'none'}},{T(57.4) + 0.35:.3f});")
rise("#aud", T(62.86) - 0.067, 60, 0.5)
sfx(T(57.4) + 0.2, "RW-008", "peak", -5, 1.6); sfx(T(57.4) + 0.35, "WH-176", "peak", -2); sfx(T(62.86), "PO-013", "peak", -5, 1.6)

# S10 full face 60.42-end: Oranuss end card in the top band
grp("s10", T(67.14), TOTAL + 0.1,
    '<div id="endc" class="card" style="left:140px;top:230px;width:800px;height:330px;text-align:center">'
    '<img src="assets/icon_play.png" style="width:130px;margin-top:30px"/>'
    '<div class="wm">ORANUSS ACADEMY</div><div class="pill2">AI Editing</div></div>')
rise("#endc", T(67.14) + 0.1, -60, 0.6)
sfx(T(67.14) + 0.1, "LO-003", "peak", -8, 1.8)

# ---------------- captions ----------------
for k, (a, b, text, acc) in enumerate(CAPS):
    words = text.split(" ")
    nxt = CAPS[k + 1][0] - 0.067 - 0.08 if k + 1 < len(CAPS) else TOTAL
    b = min(max(b, a + 0.5 + 0.3 * len(words)), nxt - 0.15)
    y = cap_y(a)
    spans = "".join(f'<span id="w{k}_{i}" class="cw{" acc" if i in acc else ""}">{w}</span> ' for i, w in enumerate(words))
    h(f'<div id="cap{k}" class="cap" style="top:{y}px">{spans}</div>')
    tw(f"tl.set('#cap{k}',{{autoAlpha:1}},{a - 0.067:.3f});tl.set('#cap{k}',{{autoAlpha:0}},{b + 0.15:.3f});")
    tw(f"tl.fromTo('#cap{k}',{{y:18}},{{y:0,duration:.3,ease:'expo.out'}},{a - 0.067:.3f});")
    step = (b - a) / max(len(words), 1)
    for i in range(len(words)):
        tw(f"tl.fromTo('#w{k}_{i}',{{opacity:.38}},{{opacity:1,duration:.12}},{a - 0.067 + i * step:.3f});")
        if i in acc:
            tw(f"tl.fromTo('#w{k}_{i}',{{scale:.8}},{{scale:1,duration:.35,ease:'back.out(2.5)'}},{a - 0.067 + i * step:.3f});")

CSS = open(os.path.join(HERE, "1112.css")).read()
html = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <div id="cam"><video id="camv" class="clip" src="assets/aroll.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0"></video><div class="vig"></div></div>
  <div id="stage"><div class="rays"></div></div>
  {chr(10).join("  " + x for x in H)}
  <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-volume="1"></audio>
</div>
<script>
  document.getElementById('wave').innerHTML = Array.from({{length:70}},(_,i)=>`<i style="height:${{18+((i*37)%60)}}px"></i>`).join('');
  const tl = gsap.timeline({{ paused: true }});
  gsap.set('.grp,.cap',{{autoAlpha:0}});
  gsap.set('#stage',{{clipPath:'{STAGE_CLIP["full"]}'}});
  gsap.set('#camv',{{filter:'blur(0px)'}});
  {chr(10).join("  " + x for x in J)}
  tl.to({{}},{{duration:0.001}},{TOTAL - 0.01});
  window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>"""
open(os.path.join(PROJ, "index.html"), "w", encoding="utf-8").write(html)
json.dump(sorted(CUES), open(os.path.join(WK, "sfx_cues.json"), "w"))
print("ok", len(CAPS), "captions,", len(CUES), "sfx")
