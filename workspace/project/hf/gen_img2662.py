# Developed by Mehdi ORANUSS | Powered by Claude
"""IMG_2662 reel (9:16, 81.95 s): josephswork-blue-ui layouts in YELLOW (reference/styles/short/josephswork-blue-ui/STYLE.md).
Topic: the 3 kinds of content (educational, solves problems, people's experiences) + clothes-shop example + like CTA.
Footage: work/img2662/tight.mov (graded, 30 fps, no cuts). Face box (Vision): y 640-1270, x 160-800.
Safe zone (universal): every word/logo inside x 120-960, y 380-1440.
Layouts: FULL face (graphics in the top band y 380-620, keyword caption under the chin y 1300) / SPLIT (yellow
stage 0-960, footage moved down 200 px, graphics in y 380-930) / STAGE (full-screen yellow, y 380-1440).
On-screen words: only words clearly said (Arabic script; social media / like in Latin). No subtitle bar.
Writes hf/img2662/index.html and work/img2662/sfx_cues.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "img2662")
WK = os.path.join(HERE, "..", "work", "img2662")
TOTAL = 81.95

LAY = [(0, "full"), (3.1, "split"), (8.6, "stage"), (15.9, "full"), (21.4, "stage"), (24.5, "split"), (30.9, "stage"),
       (37.7, "split"), (47.9, "full"), (49.3, "stage"), (59.9, "split"), (62.9, "full"), (67.2, "split"), (75.0, "full")]
CAPS = [(0.48, 2.9, "كل نهار", [1])]           # keyword captions only (full layouts)

H, J, CUES = [], [], []
def h(s): H.append(s)
def tw(s): J.append(s)
def sfx(t, sid, align="peak", extra=0, trim=None): CUES.append((round(t, 3), sid, align, extra, trim))

# ---------------- camera + stage rig ----------------
STAGE_CLIP = {"full": "inset(0px 0px 1920px 0px)", "split": "inset(0px 0px 960px 0px)", "stage": "inset(0px 0px 0px 0px)"}
for t, st in LAY:
    if t == 0:
        continue
    d = 0.45
    tw(f"tl.to('#stage',{{clipPath:'{STAGE_CLIP[st]}',duration:{d},ease:'expo.inOut'}},{t - 0.12:.3f});")
    tw(f"tl.to('#cam',{{y:{200 if st == 'split' else 0},scale:{1.0 if st != 'full' else 1.0},duration:{d},ease:'expo.inOut'}},{t - 0.12:.3f});")
    tw(f"tl.fromTo('#camv',{{filter:'blur(14px)'}},{{filter:'blur(0px)',duration:.35,ease:'power2.out',immediateRender:false}},{t + 0.05:.3f});")
    sfx(t, "WH-163" if st == "stage" else "WH-012", "peak", -2 if st == "stage" else -3)
# punch-ins inside long full-face takes (hide the static frame)
for t0, t1 in [(0, 3.1), (15.9, 21.4), (62.9, 67.2), (75.0, TOTAL)]:
    tw(f"tl.fromTo('#camv',{{scale:1.0}},{{scale:1.08,duration:{t1 - t0:.2f},ease:'none',immediateRender:false}},{t0:.3f});")

def grp(gid, t0, t1, inner):
    h(f'<div id="{gid}" class="grp">{inner}</div>')
    tw(f"tl.set('#{gid}',{{autoAlpha:1}},{t0:.3f});tl.to('#{gid}',{{autoAlpha:0,duration:.25,ease:'power2.in'}},{t1 - 0.25:.3f});")
def rise(sel, t, dy=80, d=0.5, blur=10):
    tw(f"tl.fromTo('{sel}',{{y:{dy},opacity:0,filter:'blur({blur}px)'}},{{y:0,opacity:1,filter:'blur(0px)',duration:{d},ease:'expo.out'}},{t:.3f});")
def pop(sel, t, s0=0.4, d=0.55, ease="back.out(1.8)"):
    tw(f"tl.fromTo('{sel}',{{scale:{s0},opacity:0}},{{scale:1,opacity:1,duration:{d},ease:'{ease}'}},{t:.3f});")
def slam(sel, t):
    tw(f"tl.fromTo('{sel}',{{scale:1.6,opacity:0,filter:'blur(18px)'}},{{scale:1,opacity:1,filter:'blur(0px)',duration:.4,ease:'expo.out'}},{t:.3f});")
def bob(sel, t, d=2.2, dy=-14, rot=10):
    tw(f"tl.to('{sel}',{{y:{dy},rotation:{rot},duration:{d},ease:'sine.inOut',yoyo:true,repeat:1}},{t:.3f});")
def ic(iid, name, x, y, w, rot=0):
    return f'<div id="{iid}" class="ic" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)"><img src="assets/icon_{name}.png"/></div>'
CHECK = '<svg width="34" height="34" viewBox="0 0 24 24"><path d="M4 12.5 9.5 18 20 6.5" stroke="#fff" stroke-width="3.4" fill="none" stroke-linecap="round"/></svg>'

# S1 full 0-3.1: hook, "social media" pill in the top band
grp("s1", 0, 3.1,
    '<div class="ctr" style="top:440px"><div id="sm" class="pill y">social media</div></div>'
    + ic("p1", "phone", 120, 400, 170, -12) + ic("p2", "think", 790, 395, 170, 10))
pop("#p1", 0.2); pop("#p2", 0.45); slam("#sm", 1.14 - 0.067); bob("#p1", 0.9); bob("#p2", 0.9, dy=12, rot=-10)
sfx(0.2, "PO-006", "peak", -3); sfx(0.45, "PO-008", "peak", -3); sfx(1.14, "IM-003", "peak", -6, 1.4)

# S2 split 3.1-8.6: the problem, the same question every time
grp("s2", 3.1, 8.65,
    '<div id="pc" class="card" style="left:100px;top:400px;width:880px;height:500px">'
    '<div class="thead"><img src="assets/icon_question.png"/><div class="tt">المشكلة</div></div>'
    '<div id="b1" class="bub" style="left:110px;top:170px">?</div><div id="b2" class="bub" style="left:365px;top:170px">?</div>'
    '<div id="b3" class="bub" style="left:620px;top:170px">?</div>'
    '<div id="lp" class="loop" style="left:380px;top:340px"></div></div>')
rise("#pc", 3.25, -90, 0.6)
for i, t in enumerate([4.32, 5.36, 6.44]):
    pop(f"#b{i + 1}", t - 0.067, 0.3, 0.5, "back.out(2.4)"); sfx(t, ["PO-006", "PO-008", "PO-009"][i], "peak", -4)
tw("tl.fromTo('#lp',{opacity:0,rotation:0},{opacity:1,rotation:720,duration:2.0,ease:'power1.inOut'},6.5);")
sfx(3.25, "WH-166", "peak", -3); sfx(6.5, "WH-004", "peak", -6)

# S3 stage 8.6-15.9: a new idea every time costs time and effort
grp("s3", 8.6, 15.95,
    '<div id="t3" class="ttl" style="top:410px"><span class="hl">فكرة جديدة</span></div>'
    + ic("bulb", "bulb", 390, 560, 300)
    + '<div id="m1" class="meter" style="left:100px;top:1000px"><img src="assets/icon_clock.png"/><div class="ml">الوقت</div><div class="bar"><i id="mb1"></i></div></div>'
    '<div id="m2" class="meter" style="left:580px;top:1000px"><img src="assets/icon_battery.png"/><div class="ml">المجهود</div><div class="bar"><i id="mb2"></i></div></div>')
slam("#t3", 8.97 - 0.067); pop("#bulb", 9.3, 0.3, 0.6)
tw("tl.to('#bulb',{filter:'drop-shadow(0 0 60px rgba(255,255,255,.95)) brightness(1.15)',duration:.12,yoyo:true,repeat:5,ease:'steps(1)'},10.2);")
rise("#m1", 13.31 - 0.067, 120, 0.55); rise("#m2", 13.75 - 0.067, 120, 0.55)
tw("tl.fromTo('#mb1',{scaleX:0},{scaleX:1,duration:2.0,ease:'power1.in'},13.5);tl.fromTo('#mb2',{scaleX:0},{scaleX:1,duration:1.8,ease:'power1.in'},13.9);")
tw("tl.to('#bulb',{filter:'grayscale(1) brightness(.55) drop-shadow(0 24px 34px rgba(60,40,0,.4))',duration:1.0,ease:'power2.in'},14.6);")
sfx(8.97, "IM-029", "peak", -6, 1.4); sfx(9.3, "PO-016", "peak", -2); sfx(13.31, "WH-091", "peak", -4); sfx(13.75, "PO-019", "peak", -4)

# S4 full 15.9-21.4: the simple solution
grp("s4", 15.9, 21.45,
    '<div class="ctr" style="top:430px"><div id="sol" class="pill w ar"><img src="assets/icon_key.png"/>الحل بسيط</div></div>'
    + ic("sp1", "sparkles", 130, 395, 120, -10) + ic("sp2", "sparkles", 830, 520, 110, 14))
slam("#sol", 16.15 - 0.067); pop("#sp1", 16.5); pop("#sp2", 16.7); bob("#sp1", 17.2); bob("#sp2", 17.2, dy=12, rot=-12)
sfx(16.15, "RW-007", "peak", -3); sfx(16.5, "PO-006", "peak", -5)

# S5 stage 21.4-24.5: split the ideas into 3 kinds
grp("s5", 21.4, 24.55,
    '<div id="t5" class="ttl" style="top:420px">الأفكار</div>'
    '<div id="big3" class="mega" style="top:560px">3</div>'
    '<div class="row3" style="top:1090px">' + "".join(f'<div id="k{i}" class="tile"><img src="assets/icon_{n}.png"/><div class="n">{i + 1}</div></div>'
                                                for i, n in enumerate(["books", "speech", "star"])) + '</div>')
rise("#t5", 21.64 - 0.067, 40, 0.45); slam("#big3", 22.95 - 0.067)
for i in range(3):
    rise(f"#k{i}", 23.2 + i * 0.1, 160, 0.55, 12)
sfx(21.64, "WH-174", "peak", -3); sfx(22.95, "IM-025", "peak", -5, 1.4); sfx(23.2, "PO-022", "peak", -3)

# S6 split 24.5-30.9: kind 1, educational
grp("s6", 24.5, 30.95,
    '<div id="c1" class="card" style="left:100px;top:395px;width:880px;height:520px">'
    '<div class="thead"><div class="dia"><b>1</b></div><img src="assets/icon_books.png"/><div id="c1t" class="tt">محتوى تعليمي</div></div>'
    '<div class="chips" style="top:200px"><span id="ch1">استفادة</span><span id="ch2">المعلومات</span></div>'
    '<div class="bar" style="top:330px"><i id="c1b"></i></div>'
    + ic("c1p", "people", 50, 380, 110) + ic("c1s", "sparkles", 720, 370, 110) + '</div>')
rise("#c1", 24.6, -90, 0.6); rise("#c1t", 26.15 - 0.067, 0, 0.4, 8)
pop("#ch1", 27.98 - 0.067, 0.5, 0.45); pop("#ch2", 28.67 - 0.067, 0.5, 0.45)
tw("tl.fromTo('#c1b',{scaleX:0},{scaleX:1,duration:2.4,ease:'power2.out'},28.1);")
pop("#c1p", 29.0); pop("#c1s", 29.2)
sfx(24.6, "WH-166", "peak", -3); sfx(26.15, "PO-019", "peak", -4); sfx(27.98, "PO-006", "peak", -4); sfx(28.67, "PO-008", "peak", -4)

# S7 stage 30.9-37.7: kind 2, content that solves problems (questions in, answer out)
msgs = "".join(f'<div id="q{i}" class="msg in" style="top:{130 + i * 120}px"><b>?</b><i style="width:{[300, 240, 280][i]}px"></i></div>' for i in range(3))
grp("s7", 30.9, 37.75,
    '<div class="row3" style="top:400px"><div id="d2" class="dia"><b>2</b></div><div id="t7" class="ttl" style="position:static">يحل المشاكل</div></div>'
    '<div id="ph" class="phone" style="left:190px;top:560px;width:700px;height:780px">'
    '<div class="ph-h"><img src="assets/icon_speech.png"/></div>' + msgs +
    '<div id="ans" class="msg out" style="top:520px"><div id="typ" class="dots3"><u></u><u></u><u></u></div><img id="ansok" src="assets/icon_check.png" style="display:block"/></div></div>')
pop("#d2", 31.16 - 0.067, 0.4, 0.45); rise("#ph", 31.4, 200, 0.65); slam("#t7", 33.57 - 0.067)
for i in range(3):
    tw(f"tl.fromTo('#q{i}',{{x:-120,opacity:0}},{{x:0,opacity:1,duration:.4,ease:'expo.out'}},{35.06 - 0.067 + i * 0.35:.3f});")
    sfx(35.06 + i * 0.35, ["PO-006", "PO-008", "PO-009"][i], "peak", -5)
tw("tl.fromTo('#ans',{x:120,opacity:0},{x:0,opacity:1,duration:.4,ease:'expo.out'},36.25);")
tw("tl.fromTo('#typ u',{y:0},{y:-10,duration:.18,yoyo:true,repeat:3,stagger:.08,ease:'sine.inOut'},36.35);")
tw("tl.set('#typ',{display:'none'},37.05);tl.fromTo('#ansok',{scale:0},{scale:1,duration:.35,ease:'back.out(2.4)',immediateRender:false},37.05);")
tw("tl.set('#ansok',{scale:0},30.9);")
sfx(31.4, "WH-176", "peak", -2); sfx(33.57, "IM-003", "peak", -8, 1.2); sfx(36.25, "UI-029", "peak", -3); sfx(37.05, "PO-019", "peak", -3)

# S8 split 37.7-47.9: kind 3, people's experiences and results
def review(rid, x):
    return (f'<div id="{rid}" class="rv" style="left:{x}px;top:500px"><img src="assets/icon_people.png"/>'
            f'<div class="st" id="{rid}s">★★★★★</div><i style="top:120px;width:360px"></i><i style="top:150px;width:260px"></i></div>')
grp("s8", 37.7, 47.95,
    '<div class="row3" style="top:395px"><div id="d3" class="dia"><b>3</b></div><div id="t8" class="ttl" style="position:static;font-size:72px">تجارب الناس</div></div>'
    + review("r1", 100) + review("r2", 550) +
    '<div id="rs" class="res" style="left:100px;top:730px;width:880px;height:190px"><img src="assets/icon_chart.png"/><div class="rl">النتائج</div>'
    '<svg width="880" height="190"><path id="ln" d="M130 160 C 230 150, 290 128, 360 122 S 500 92, 560 80 S 640 62, 680 56" stroke="#FFC800" stroke-width="10" fill="none" stroke-linecap="round"/></svg></div>')
pop("#d3", 37.92 - 0.067, 0.4, 0.45); rise("#t8", 39.49 - 0.067, 30, 0.45)
rise("#r1", 40.6, 100, 0.55); rise("#r2", 41.8, 100, 0.55)
tw("tl.fromTo('#r1s',{color:'#E3DCC6'},{color:'#FFC800',duration:.6,ease:'none'},41.0);tl.fromTo('#r2s',{color:'#E3DCC6'},{color:'#FFC800',duration:.6,ease:'none'},42.2);")
rise("#rs", 43.6 - 0.067, 80, 0.55)
tw("tl.fromTo('#ln',{strokeDasharray:900,strokeDashoffset:900},{strokeDashoffset:0,duration:1.6,ease:'power2.out'},43.8);")
sfx(37.92, "WH-166", "peak", -3); sfx(39.49, "PO-019", "peak", -4); sfx(40.6, "PO-022", "peak", -4); sfx(41.8, "PO-022", "peak", -5)
sfx(43.6, "RW-006", "peak", -6, 1.6)

# S9 full 47.9-49.3: example
grp("s9", 47.9, 49.35, '<div class="ctr" style="top:430px"><div id="ex" class="pill y ar"><img src="assets/icon_shirt.png"/>مثال</div></div>')
slam("#ex", 48.23 - 0.067); sfx(48.23, "IM-029", "peak", -8, 1.2)

# S10 stage 49.3-59.9: clothes shop example, photos swap with each idea, then the colours
grp("s10", 49.3, 59.95,
    '<div id="gl" class="glass" style="left:140px;top:410px;width:800px;height:640px"><div class="inner">'
    '<img id="ph1" src="assets/img_store.jpg"/><img id="ph2" src="assets/img_choose.jpg" style="opacity:0"/><img id="ph3" src="assets/img_colors.jpg" style="opacity:0"/>'
    + "".join(f'<div id="sw{i}" class="sw" style="left:{60 + i * 140}px;top:480px;background:{c}"></div>' for i, c in enumerate(["#15120A", "#F2EBDD", "#C8A27A", "#3F5A7A", "#FFC800"]))
    + '</div></div>' + ic("shirt", "shirt", 790, 360, 190, 12)
    + '<div class="row3" style="top:1130px;gap:60px">'
    + '<div id="e1" class="tile"><img src="assets/icon_dress.png"/><div class="n">1</div><div id="o1" class="ok">' + CHECK + '</div></div>'
    + '<div id="e2" class="tile"><img src="assets/icon_search.png"/><div class="n">2</div><div id="o2" class="ok">' + CHECK + '</div></div>'
    + '<div id="e3" class="tile lab"><img src="assets/icon_palette.png"/><span>الألوان</span><div class="n">3</div><div id="o3" class="ok">' + CHECK + '</div></div></div>')
tw("tl.fromTo('#gl',{y:300,rotation:5,opacity:0,filter:'blur(12px)'}," "{y:0,rotation:-2,opacity:1,filter:'blur(0px)',duration:.7,ease:'expo.out'},49.4);")
tw("tl.fromTo('#ph1',{scale:1.0},{scale:1.12,duration:10.5,ease:'none'},49.4);")
pop("#shirt", 49.61 - 0.067); bob("#shirt", 50.3, 2.4)
for i, t in enumerate([52.63, 54.74, 57.67]):
    rise(f"#e{i + 1}", t - 0.067, 140, 0.5, 12)
    tw(f"tl.fromTo('#o{i + 1}',{{scale:0}},{{scale:1,duration:.35,ease:'back.out(2.4)'}},{t + 0.5:.3f});")
    sfx(t, "PO-022", "peak", -4); sfx(t + 0.5, ["PO-019", "PO-019", "RW-007"][i], "peak", -5)
tw("tl.to('#ph2',{opacity:1,duration:.3},54.67);tl.fromTo('#ph2',{scale:1.12},{scale:1.0,duration:3.2,ease:'none'},54.67);")
tw("tl.to('#ph3',{opacity:1,duration:.3},57.6);tl.fromTo('#ph3',{scale:1.0},{scale:1.1,duration:2.4,ease:'none'},57.6);")
for i in range(5):
    pop(f"#sw{i}", 57.9 + i * 0.08, 0.2, 0.45, "back.out(2.2)")
sfx(49.4, "WH-156", "peak", -4); sfx(49.61, "PO-016", "peak", -3); sfx(54.67, "WH-004", "peak", -4); sfx(57.6, "WH-004", "peak", -4)
sfx(57.9, "PO-006", "peak", -6)

# S11 split 59.9-62.9: share people's experience with them
grp("s11", 59.9, 62.95,
    '<div id="c11" class="card" style="left:100px;top:420px;width:880px;height:430px">'
    '<div class="thead"><img src="assets/icon_people.png"/><div id="c11t" class="tt">تجربة الناس</div></div>'
    '<div id="c11s" class="st" style="left:0;right:0;top:170px;text-align:center;font:900 96px Poppins;color:#FFC800;-webkit-text-stroke:3px #15120A">★★★★★</div>'
    + ic("c11m", "megaphone", 680, 250, 160, -10) + ic("c11h", "heart", 70, 260, 130, 10) + '</div>')
rise("#c11", 60.0, -90, 0.55); rise("#c11t", 60.81 - 0.067, 0, 0.4, 8)
tw("tl.fromTo('#c11s',{scale:.6,opacity:0},{scale:1,opacity:1,duration:.5,ease:'back.out(2)'},61.2);")
pop("#c11m", 61.5); pop("#c11h", 61.7)
sfx(60.0, "WH-166", "peak", -3); sfx(60.81, "PO-019", "peak", -4); sfx(61.2, "RW-008", "peak", -6, 1.4)

# S12 full 62.9-67.2: try these 3 kinds, ticks in the top band
grp("s12", 62.9, 67.25,
    '<div class="row3" style="top:410px;gap:40px">' + "".join(
        f'<div id="z{i}" class="tile" style="width:170px;height:170px"><img src="assets/icon_{n}.png" style="width:110px"/><div id="zo{i}" class="ok">{CHECK}</div></div>'
        for i, n in enumerate(["books", "speech", "star"])) + '</div>')
for i in range(3):
    rise(f"#z{i}", 63.0 + i * 0.1, -80, 0.5)
    tw(f"tl.fromTo('#zo{i}',{{scale:0}},{{scale:1,duration:.35,ease:'back.out(2.4)'}},{63.17 + i * 0.33:.3f});")
    sfx(63.17 + i * 0.33, "PO-019", "peak", -5)
sfx(63.0, "WH-012", "peak", -5)

# S13 split 67.2-75.0: social media, ideas burst out of the phone
fly = ["bulb", "sparkles", "bulb", "speech", "bulb", "star", "sparkles", "bulb"]
pos = [(130, 420), (820, 410), (150, 640), (830, 650), (250, 820), (720, 820), (480, 390), (600, 700)]
grp("s13", 67.2, 75.05,
    '<div id="t13" class="ttl lt" style="top:395px;font-size:96px">social media</div>'
    + ic("ph13", "phone", 430, 520, 220)
    + "".join(f'<div id="f{i}" class="ic fly" style="left:470px;top:560px;width:{110 if i % 2 else 130}px"><img src="assets/icon_{n}.png"/></div>' for i, n in enumerate(fly))
    + '<div id="t13b" class="ttl" style="top:790px"><span class="hl">الأفكار</span></div>')
slam("#t13", 67.45 - 0.067); pop("#ph13", 67.8, 0.4, 0.55)
for i, (x, y) in enumerate(pos):
    t = 70.07 if i < 4 else 71.85
    tw(f"tl.fromTo('#f{i}',{{x:0,y:0,scale:.2,opacity:0,rotation:0}},{{x:{x - 470},y:{y - 560},scale:1,opacity:1,rotation:{(i * 37) % 40 - 20},duration:.7,ease:'expo.out'}},{t + (i % 4) * 0.06:.3f});")
slam("#t13b", 70.07 - 0.067)
tw("tl.to('#s13 .fly',{y:'-=18',duration:1.2,ease:'sine.inOut',yoyo:true,repeat:1,stagger:.05},72.6);")
sfx(67.45, "IM-003", "peak", -8, 1.2); sfx(67.8, "PO-016", "peak", -3); sfx(70.07, "WH-176", "peak", -2); sfx(71.85, "WH-158", "peak", -4)

# S14 full 75.0-end: like CTA + Oranuss wordmark (top band, inside the safe zone)
hearts = "".join(f'<div id="hh{i}" class="ic ht" style="left:{470 + (i - 2.5) * 60:.0f}px;top:420px"><img src="assets/icon_heart.png"/></div>' for i in range(6))
grp("s14", 75.0, TOTAL + 0.1,
    '<div id="lk" class="likec" style="top:390px;height:180px"><img src="assets/icon_thumbs.png"/><b>like</b></div>' + hearts +
    '<div id="wm" class="wm" style="top:585px">ORANUSS <span>ACADEMY</span></div>')
pop("#lk", 76.58 - 0.2, 0.3, 0.55)
for k, t in enumerate([77.0, 80.15]):
    tw(f"tl.fromTo('#lk',{{scale:1}},{{scale:.88,duration:.09,yoyo:true,repeat:1,ease:'power2.inOut',immediateRender:false}},{t:.3f});")
    for i in range(6):
        tw(f"tl.fromTo('#hh{i}',{{x:0,y:0,scale:.3,opacity:0}},{{x:{(i - 2.5) * 70:.0f},y:{-160 - (i * 53) % 120},scale:1,opacity:1,duration:.6,ease:'expo.out',immediateRender:false}},{t + 0.05 + i * 0.03:.3f});"
           f"tl.to('#hh{i}',{{opacity:0,y:'-=60',duration:.5,ease:'power1.in'}},{t + 0.8:.3f});")
    sfx(t, "UI-029", "peak", -3); sfx(t + 0.05, "RW-001", "peak", -6)
rise("#wm", 78.4, 20, 0.5)
sfx(76.38, "PO-016", "peak", -2); sfx(78.4, "LO-003", "peak", -10, 1.6)

# ---------------- keyword captions ----------------
for k, (a, b, text, acc) in enumerate(CAPS):
    words = text.split(" ")
    spans = "".join(f'<span id="w{k}_{i}" class="cw{" acc" if i in acc else ""}">{w}</span> ' for i, w in enumerate(words))
    h(f'<div id="cap{k}" class="cap" style="top:1345px">{spans}</div>')
    tw(f"tl.set('#cap{k}',{{autoAlpha:1}},{a - 0.067:.3f});tl.to('#cap{k}',{{autoAlpha:0,duration:.2}},{b:.3f});")
    tw(f"tl.fromTo('#cap{k}',{{y:18}},{{y:0,duration:.3,ease:'expo.out'}},{a - 0.067:.3f});")
    step = 0.3
    for i in range(len(words)):
        tw(f"tl.fromTo('#w{k}_{i}',{{opacity:.38}},{{opacity:1,duration:.12}},{a - 0.067 + i * step:.3f});")
        if i in acc:
            tw(f"tl.fromTo('#w{k}_{i}',{{scale:.8}},{{scale:1,duration:.35,ease:'back.out(2.5)'}},{a - 0.067 + i * step:.3f});")

CSS = open(os.path.join(HERE, "img2662.css")).read()
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
print("ok", len(CUES), "sfx")
