# Developed by Mehdi ORANUSS | Powered by Claude
"""IMG_2662 reel (9:16, 81.95 s) in the ALEX style (skill alexstylemotions + pro-motion-upgrades, Creating B-rolls look).
Palette (Reference preset): canvas #13162A · punch #FDFE48 · body #FFFFFF · accent #6A2BF0 · accent-gradient #240E4A→#391276.
Font: Milan Display (captions, titles, Latin words). Flat white line icons in accent circles, no emoji.
Treatments: A speaker (two-tier captions on key phrases) / DIM (A-roll darkened, overlay) / CANVAS cover (T3 fade).
Safe zone: everything inside x 120-960, y 380-1440. Only clearly spoken words on screen.
Writes hf/img2662-alex/index.html and work/img2662/sfx_cues_alex.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "img2662-alex")
WK = os.path.join(HERE, "..", "work", "img2662")
TOTAL = 81.95

LAY = [(0, "a"), (3.1, "dim"), (8.6, "canvas"), (15.9, "a"), (21.4, "grad"), (27.6, "dim"), (30.9, "grad"), (34.0, "dim"),
       (37.7, "grad"), (40.6, "dim"), (47.9, "a"), (49.3, "canvas"), (59.9, "dim"), (62.9, "a"), (67.2, "canvas"), (75.0, "a")]
H, J, CUES = [], [], []
def h(s): H.append(s)
def tw(s): J.append(s)
def sfx(t, sid, extra=0, align="peak", trim=None): CUES.append((round(t, 3), sid, align, extra, trim))

# ---------------- line icons (24 grid, white 2.2 stroke, drawn on) ----------------
P = {
 "user": ['<circle cx="12" cy="8" r="4"/>', '<path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>'],
 "users": ['<circle cx="9" cy="8" r="3.5"/>', '<path d="M2.5 20c0-3.5 3-5.5 6.5-5.5s6.5 2 6.5 5.5"/>', '<path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.8c2.2.6 3.5 2.4 3.5 5.2"/>'],
 "bulb": ['<path d="M9 18h6M10 21h4"/>', '<path d="M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>'],
 "clock": ['<circle cx="12" cy="12" r="9"/>', '<path d="M12 7v5l3.5 2"/>'],
 "battery": ['<rect x="2" y="7" width="17" height="10" rx="2.5"/>', '<path d="M22 11v2M5.5 10.5v3"/>'],
 "book": ['<path d="M3 5h6a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H3z"/>', '<path d="M21 5h-6a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h7z"/>'],
 "chat": ['<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.4A8 8 0 1 1 21 12z"/>'],
 "star": ['<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9z"/>'],
 "shirt": ['<path d="M8 3l4 2 4-2 5 4-3 3-2-1v12H8V9l-2 1-3-3z"/>'],
 "search": ['<circle cx="11" cy="11" r="7"/>', '<path d="M20 20l-4-4"/>'],
 "palette": ['<path d="M12 3a9 9 0 1 0 0 18c1.5 0 2-1 2-2s-1-1.5-1-2.5 1-1.5 2-1.5h2a4 4 0 0 0 4-4c0-4.5-4-8-9-8z"/>',
             '<circle cx="7.5" cy="11.5" r="1"/>', '<circle cx="10" cy="7.5" r="1"/>', '<circle cx="15" cy="7.5" r="1"/>'],
 "check": ['<path d="M5 12.5l4.5 4.5L19 7"/>'],
 "x": ['<path d="M6 6l12 12M18 6L6 18"/>'],
 "phone": ['<rect x="6" y="2" width="12" height="20" rx="3"/>', '<path d="M11 18h2"/>'],
 "thumbs": ['<path d="M7 10v11H4V10z"/>', '<path d="M7 10l4-7c1.5 0 2.5 1 2.2 2.6L12.6 9H19a2 2 0 0 1 2 2.3l-1.2 7A2 2 0 0 1 17.8 20H7"/>'],
 "key": ['<circle cx="7.5" cy="15.5" r="4.5"/>', '<path d="M10.7 12.3L20 3M16 7l3 3"/>'],
 "question": ['<path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 2.5-3 4.5"/>', '<path d="M12 18h.01"/>'],
}
def svg(name, size=80, color="#fff", sw=2.2):
    inner = "".join(p.replace("/>", ' pathLength="1" class="dr"/>', 1) for p in P[name])
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray:1">{inner}</svg>')
def badge(bid, name, x, y, w=150, kind="", size=None):
    return f'<div id="{bid}" class="ib {kind}" style="left:{x}px;top:{y}px;width:{w}px;height:{w}px">{svg(name, size or int(w * .52))}</div>'

# ---------------- rig: A-roll / dim / canvas (T3 fade to canvas) ----------------
for t, st in LAY:
    if t == 0:
        continue
    cv, c2, sh = (1 if st == "canvas" else 0), (1 if st == "grad" else 0), (1 if st == "dim" else 0)
    d = 0.5 if (cv or c2) else 0.35
    tw(f"tl.to('#canvas',{{opacity:{cv},duration:{d},ease:'power2.inOut'}},{t - 0.25:.3f});tl.to('#canvas2',{{opacity:{c2},duration:{d},ease:'power2.inOut'}},{t - 0.25:.3f});")
    tw(f"tl.to('#shade',{{opacity:{sh},duration:.4,ease:'power2.inOut'}},{t - 0.2:.3f});")
    tw(f"tl.to('#camv',{{filter:'blur({4 if sh else 0}px)',scale:1,duration:.4,ease:'power2.inOut'}},{t - 0.2:.3f});")
    if cv or c2:
        sfx(t, "WH-012", -9)
# punch-ins on key words in A sections: ease in 0.5 s and hold (no pulse)
for t in [1.14, 16.15, 48.23, 76.58]:
    tw(f"tl.to('#camv',{{scale:1.07,duration:.5,ease:'expo.out'}},{t - 0.067:.3f});")

def grp(gid, t0, t1, inner):
    h(f'<div id="{gid}" class="grp">{inner}</div>')
    tw(f"tl.set('#{gid}',{{autoAlpha:1}},{t0:.3f});tl.to('#{gid}',{{autoAlpha:0,duration:.25,ease:'power2.in'}},{t1 - 0.25:.3f});")
def fin(sel, t, dy=20, d=0.4, blur=10, s0=1.06):   # the Alex soft focus-in: blur + opacity + small scale / drift
    tw(f"tl.fromTo('{sel}',{{y:{dy},scale:{s0},opacity:0,filter:'blur({blur}px)'}},{{y:0,scale:1,opacity:1,filter:'blur(0px)',duration:{d},ease:'expo.out'}},{t:.3f});")
def pop(sel, t, d=0.4):
    tw(f"tl.fromTo('{sel}',{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:{d},ease:'back.out(1.4)'}},{t:.3f});")
def draw(sel, t, d=0.6):
    tw(f"tl.fromTo('{sel} .dr',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{d},ease:'power2.out',stagger:.08}},{t:.3f});")
def badge_in(sel, t):
    pop(sel, t); draw(sel, t + 0.12)
L = lambda x: x - 0.067                              # 2 frames before the word

# ---------------- two-tier captions (T1) ----------------
caps = []
def cap(t_su, su, t_pu, pu, t_end, latin=False, top=1270):
    k = len(caps); caps.append(k)
    s = f'<span id="c{k}s" class="su">{su}</span>' if su else ""
    p = f'<span id="c{k}p" class="pu{" lt" if latin else ""}">{pu}</span>' if pu else ""
    h(f'<div id="cap{k}" class="cap" style="top:{top}px">{s}{p}</div>')
    t0 = min(x for x in [t_su, t_pu] if x is not None)
    tw(f"tl.set('#cap{k}',{{autoAlpha:1}},{L(t0):.3f});tl.to('#cap{k}',{{autoAlpha:0,duration:.15}},{t_end:.3f});")
    if su: fin(f"#c{k}s", L(t_su), 12, 0.3, 10, 1.0)
    if pu: fin(f"#c{k}p", L(t_pu), 0, 0.3, 12, 1.1)
    sfx(t_pu if pu else t_su, "PO-008", -12)

# S1 A 0-3.1: hook
cap(0.48, "كل نهار", 1.14, "social media", 3.0, latin=True)
grp("s1", 0, 3.1, badge("b1", "phone", 820, 410, 130))
badge_in("#b1", 1.3); sfx(1.3, "PO-006", -9)

# S2 DIM 3.1-8.6: the problem
grp("s2", 3.1, 8.65, badge("b2", "question", 465, 450, 150, "grad")
    + '<div id="t2" class="t p" style="top:650px">المشكلة</div><div id="t2b" class="t s" style="top:800px">كل مرة</div>'
    + '<div id="t2c" class="t" style="top:880px">فكرة جديدة</div>')
badge_in("#b2", L(3.22)); fin("#t2", L(3.22) + 0.1); fin("#t2b", L(6.44), 12, 0.35); fin("#t2c", L(8.0), 12, 0.35)
sfx(3.22, "IM-003", -12, trim=1.0)

# S3 CANVAS 8.6-15.9: a new idea every time costs time and effort (VS columns)
grp("s3", 8.6, 15.95,
    '<div id="t3" class="t p" style="top:410px">فكرة جديدة</div>' + badge("b3", "bulb", 450, 560, 180)
    + '<div id="vl" class="vline" style="left:538px;top:860px;height:440px"></div>'
    + badge("b3r", "clock", 735, 880, 130) + '<div id="l3r" class="lab" style="left:540px;top:1040px">الوقت</div>'
    + badge("b3l", "battery", 215, 880, 130) + '<div id="l3l" class="lab" style="right:540px;top:1040px">المجهود</div>'
    + badge("x3r", "x", 760, 1130, 80, "neg") + badge("x3l", "x", 240, 1130, 80, "neg"))
fin("#t3", L(8.97)); badge_in("#b3", 9.3)
tw("tl.fromTo('#vl',{scaleY:0},{scaleY:1,duration:.6,ease:'expo.out'},13.1);")
badge_in("#b3r", L(13.31)); fin("#l3r", L(13.31) + 0.15, 12, 0.35); badge_in("#b3l", L(13.75)); fin("#l3l", L(13.75) + 0.15, 12, 0.35)
badge_in("#x3r", 14.4); badge_in("#x3l", 14.7)
tw("tl.to('#b3',{opacity:.35,duration:.8,ease:'power2.in'},14.9);")
sfx(9.3, "PO-006", -9); sfx(13.31, "PO-008", -10); sfx(13.75, "PO-008", -10); sfx(14.4, "NG-007", -16); sfx(14.7, "NG-007", -16)

# S4 A 15.9-21.4: the simple solution
cap(16.15, "الحل", 16.55, "بسيط", 19.0)
grp("s4", 15.9, 21.45, badge("b4", "key", 820, 410, 130))
badge_in("#b4", 16.7); sfx(16.7, "PO-006", -9)

# three glass stage cards (T12), RTL: 01 on the right
CX = [775, 405, 35]
def cards(prefix, active, icon, t0, rise):
    out = ""
    for i in range(3):
        on = " on" if i == active else ""
        ic = svg(icon, 120, "#FDFE48", 1.8) if i == active else ""
        out += (f'<div id="{prefix}{i}" class="gc{on}" style="left:{CX[i]}px;top:560px;{"" if i == active or active < 0 else "opacity:.45"}">'
                f'<div class="no">0{i + 1}</div><div class="orb" id="{prefix}o{i}"></div><div class="ico" id="{prefix}i{i}">{ic}</div></div>')
    return out
def cards_anim(prefix, active, t0, t_on, rise):
    if rise:
        for i in range(3):
            tw(f"tl.fromTo('#{prefix}{i}',{{y:200,opacity:0}},{{y:0,opacity:{1 if i == active else .45},duration:.6,ease:'expo.out'}},{t0 + i * 0.12:.3f});")
    else:
        tw(f"tl.fromTo('#{prefix}0,#{prefix}1,#{prefix}2',{{opacity:0}},{{opacity:(i,el)=>el.classList.contains('on')?1:.45,duration:.25}},{t0:.3f});")
    # orb morphs into the icon on the spoken word
    tw(f"tl.to('#{prefix}o{active}',{{scale:.2,opacity:0,duration:.35,ease:'power2.in'}},{t_on:.3f});tl.to('#{prefix}i{active}',{{opacity:1,duration:.2}},{t_on + 0.2:.3f});")
    draw(f"#{prefix}i{active}", t_on + 0.2, 0.7)
    sfx(t_on, "PO-019", -8)

# S5 GRAD 21.4-27.6: the ideas → 3 kinds, 01 educational
grp("s5", 21.4, 27.65, '<div id="t5" class="t s" style="top:420px">الأفكار</div>' + cards("k", 0, "book", 22.95, True)
    + '<div id="t5b" class="t p" style="top:1030px">محتوى تعليمي</div>')
fin("#t5", L(21.64)); cards_anim("k", 0, L(22.95), L(24.04), True); fin("#t5b", L(26.15))
sfx(22.95, "WH-176", -6)

# S6 DIM 27.6-30.9: benefit + information
def pill(pid, txt, top):
    return (f'<div class="t" style="top:{top}px;display:flex;justify-content:center"><div id="{pid}" class="pill" style="position:relative">'
            f'<div class="ib pos" style="width:64px;height:64px">{svg("check", 40)}</div>{txt}</div></div>')
grp("s6", 27.6, 30.95, badge("b6", "book", 465, 420, 150) + pill("p61", "استفادة", 640) + pill("p62", "المعلومات", 780))
badge_in("#b6", 27.7)
fin("#p61", L(27.98), 16, 0.4, 8, 0.96); draw("#p61", 28.05, 0.4); fin("#p62", L(28.67), 16, 0.4, 8, 0.96); draw("#p62", 28.75, 0.4)
sfx(27.98, "PO-006", -9); sfx(28.67, "PO-008", -9)

# S7 GRAD 30.9-34.0: 02 solves problems
grp("s7", 30.9, 34.05, cards("m", 1, "chat", 30.9, False) + '<div id="t7" class="t p" style="top:1030px">يحل المشاكل</div>')
cards_anim("m", 1, 31.0, L(31.16), False); fin("#t7", L(33.57))

# S8 DIM 34.0-37.7: questions come in, the answer goes out
bubs = "".join(f'<div id="q{i}" class="bub in" style="left:30px;top:{50 + i * 115}px;width:{[470, 420, 450][i]}px"><div class="qm">?</div><i style="width:{[300, 240, 280][i]}px"></i></div>' for i in range(3))
grp("s8", 34.0, 37.75, '<div id="t8" class="t s" style="top:400px">للأسئلة</div>'
    + f'<div id="cw" class="wc" style="left:140px;top:500px;width:800px;height:520px">{bubs}'
    + f'<div id="an" class="bub out" style="right:30px;top:395px;width:400px"><div id="ty" class="dots3"><u></u><u></u><u></u></div>'
    + f'<div id="ao" class="ib pos" style="width:60px;height:60px;opacity:0">{svg("check", 38)}</div></div></div>')
fin("#cw", 34.1, 40, 0.5, 8, 0.98); fin("#t8", L(35.06), 12, 0.3)
for i in range(3):
    fin(f"#q{i}", L(35.06) + i * 0.3, 0, 0.35, 8, 0.96); sfx(35.06 + i * 0.3, "PO-008", -11)
fin("#an", 36.25, 0, 0.35, 8, 0.96)
tw("tl.fromTo('#ty u',{y:0},{y:-10,duration:.18,yoyo:true,repeat:3,stagger:.08,ease:'sine.inOut'},36.35);")
tw("tl.set('#ty',{display:'none'},37.0);tl.to('#ao',{opacity:1,duration:.15},37.0);"); pop("#ao", 37.0); draw("#ao", 37.05, 0.3)
sfx(37.0, "PO-019", -8)

# S9 GRAD 37.7-40.6: 03 people's experiences
grp("s9", 37.7, 40.65, cards("n", 2, "star", 37.7, False) + '<div id="t9" class="t p" style="top:1030px">تجارب الناس</div>')
cards_anim("n", 2, 37.8, L(37.92), False); fin("#t9", L(39.49))

# S10 DIM 40.6-47.9: reviews + results chart (T15)
def rv(rid, x):
    return (f'<div id="{rid}" class="rv" style="left:{x}px;top:420px"><div class="ib" style="left:24px;top:24px;width:84px;height:84px">{svg("user", 46)}</div>'
            f'<div id="{rid}s" class="stars">★★★★★</div><i style="top:130px;width:360px"></i><i style="top:156px;width:250px"></i></div>')
grp("s10", 40.6, 47.95, rv("r1", 560) + rv("r2", 100) + '<div id="t10" class="t p" style="top:650px">النتائج</div>'
    + '<svg id="ch" class="chart" style="left:120px;top:790px" viewBox="0 0 840 420">'
      '<defs><linearGradient id="gf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FDFE48" stop-opacity=".45"/><stop offset="1" stop-color="#FDFE48" stop-opacity="0"/></linearGradient></defs>'
      '<path id="ax" d="M40 20 V380 H820" stroke="rgba(255,255,255,.5)" stroke-width="4" fill="none" pathLength="1" style="stroke-dasharray:1"/>'
      '<path id="fl" d="M60 360 C 220 340, 330 300, 430 270 S 650 150, 800 70 V380 H60 Z" fill="url(#gf)" opacity="0"/>'
      '<path id="ln" d="M60 360 C 220 340, 330 300, 430 270 S 650 150, 800 70" stroke="#FDFE48" stroke-width="9" fill="none" stroke-linecap="round" pathLength="1" style="stroke-dasharray:1"/>'
      '<circle id="dt" cx="800" cy="70" r="16" fill="#FDFE48" opacity="0"/></svg>')
fin("#r1", 40.6, 30, 0.45, 8, 0.97); fin("#r2", 41.8, 30, 0.45, 8, 0.97)
tw("tl.to('#r1s',{color:'#FDFE48',duration:.6,ease:'none'},41.0);tl.to('#r2s',{color:'#FDFE48',duration:.6,ease:'none'},42.2);")
fin("#t10", L(43.6))
tw("tl.fromTo('#ax',{strokeDashoffset:1},{strokeDashoffset:0,duration:.6,ease:'power2.out'},43.7);"
   "tl.fromTo('#ln',{strokeDashoffset:1},{strokeDashoffset:0,duration:1.4,ease:'power2.inOut'},44.1);"
   "tl.to('#fl',{opacity:1,duration:.8,ease:'power1.out'},44.6);tl.fromTo('#dt',{opacity:0,scale:0,transformOrigin:'50% 50%'},{opacity:1,scale:1,duration:.35,ease:'back.out(1.4)'},45.45);")
sfx(40.6, "PO-008", -10); sfx(41.8, "PO-008", -10); sfx(44.1, "RW-006", -10, trim=1.6)

# S11 A 47.9-49.3: example
cap(None, "", 48.23, "مثال", 49.25)

# S12 CANVAS 49.3-59.9: framed b-roll (T17) + 3-step chain (T5)
sw = "".join(f'<div id="sw{i}" class="sw" style="left:{100 + i * 126}px;top:440px;background:{c}"></div>' for i, c in enumerate(["#13162A", "#F2EBDD", "#C8A27A", "#3F5A7A", "#FDFE48"]))
steps = [("shirt", ""), ("search", ""), ("palette", "الألوان")]
chain = "".join(f'<div id="e{i}"><div class="ib">{svg(n, 80)}<div class="n">{i + 1}</div><div id="o{i}" class="ok">{svg("check", 32)}</div></div>'
                + (f'<div class="cl">{lab}</div>' if lab else "") + '</div>' for i, (n, lab) in enumerate(steps))
grp("s12", 49.3, 59.95,
    '<div id="fr" class="frame" style="left:140px;top:410px;width:800px;height:560px">'
    '<img id="ph1" src="assets/img_store.jpg"/><img id="ph2" src="assets/img_choose.jpg" style="opacity:0"/><img id="ph3" src="assets/img_colors.jpg" style="opacity:0"/>'
    f'{sw}</div><div class="chain" style="top:1050px">{chain}</div>')
tw("tl.fromTo('#fr',{rotationX:18,y:60,opacity:0,transformPerspective:1200},{rotationX:0,y:0,opacity:1,duration:.6,ease:'expo.out'},49.4);")
tw("tl.fromTo('#ph1',{scale:1.0},{scale:1.1,duration:5.3,ease:'none'},49.4);")
for i, t in enumerate([52.63, 54.74, 57.67]):
    fin(f"#e{i}", L(t), 24, 0.4, 8, 0.96); draw(f"#e{i}", L(t) + 0.1, 0.6)
    tw(f"tl.fromTo('#o{i}',{{scale:0}},{{scale:1,duration:.35,ease:'back.out(1.4)'}},{t + 0.5:.3f});")
    sfx(t, "PO-006", -9); sfx(t + 0.5, "PO-019", -11)
# whip swaps (T14)
tw("tl.fromTo('#ph2',{opacity:0,y:120,filter:'blur(14px)'},{opacity:1,y:0,filter:'blur(0px)',duration:.3,ease:'expo.out'},54.67);")
tw("tl.fromTo('#ph3',{opacity:0,y:120,filter:'blur(14px)'},{opacity:1,y:0,filter:'blur(0px)',duration:.3,ease:'expo.out'},57.6);")
for i in range(5):
    pop(f"#sw{i}", 57.95 + i * 0.07, 0.35)
sfx(49.4, "WH-156", -8); sfx(54.67, "WH-004", -8); sfx(57.6, "WH-004", -8)

# S13 DIM 59.9-62.9: share people's experience
grp("s13", 59.9, 62.95, badge("b13", "users", 465, 430, 150) + '<div id="t13" class="t p" style="top:630px">تجربة الناس</div>'
    + '<div id="st13" class="stars" style="left:0;right:0;top:780px;text-align:center;font-size:76px">★★★★★</div>')
badge_in("#b13", 60.0); fin("#t13", L(60.81))
tw("tl.fromTo('#st13',{opacity:0,y:16},{opacity:1,y:0,duration:.4,ease:'expo.out'},61.2);tl.to('#st13',{color:'#FDFE48',duration:.7,ease:'none'},61.3);")
sfx(60.81, "PO-008", -10); sfx(61.3, "RW-008", -12, trim=1.2)

# S14 A 62.9-67.2: the 3 kinds, ticked (overlay in the top band)
grp("s14", 62.9, 67.25, "".join(badge(f"z{i}", n, [640, 465, 290][i], 405, 130, "ghost") + badge(f"zk{i}", "check", [640, 465, 290][i] + 86, 400, 52, "pos")
                                for i, n in enumerate(["book", "chat", "star"])))
for i in range(3):
    badge_in(f"#z{i}", 63.0 + i * 0.08); badge_in(f"#zk{i}", L(63.17) + i * 0.33); sfx(63.17 + i * 0.33, "PO-019", -11)

# S15 CANVAS 67.2-75.0: social media, one source feeding many ideas (flowing paths)
nodes = [(170, 900), (465, 940), (760, 900), (170, 1130), (465, 1170), (760, 1130)]
lines = "".join(f'<path id="fp{i}" d="M540 750 Q {540 + (x + 55 - 540) * .3} {(750 + y + 55) / 2 - 60} {x + 55} {y + 55}" stroke="rgba(253,254,72,.7)" stroke-width="4" fill="none" pathLength="1" style="stroke-dasharray:1"/>'
                for i, (x, y) in enumerate(nodes))
grp("s15", 67.2, 75.05,
    '<div id="t15" class="t p lt" style="top:400px">social media</div>' + badge("b15", "phone", 465, 600, 150)
    + f'<svg style="left:0;top:0" width="1080" height="1920">{lines}</svg>'
    + "".join(badge(f"nd{i}", "bulb", x, y, 110, "ghost") for i, (x, y) in enumerate(nodes))
    + '<div id="t15b" class="t" style="top:1310px">الأفكار</div>')
fin("#t15", L(67.45)); badge_in("#b15", 67.8)
for i in range(6):
    t = (70.07 if i < 3 else 71.85) + (i % 3) * 0.1
    tw(f"tl.fromTo('#fp{i}',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.5,ease:'power2.out'}},{t - 0.3:.3f});")
    badge_in(f"#nd{i}", t + 0.15)
    tw(f"tl.to('#nd{i}',{{background:'#6A2BF0',duration:.25}},{t + 0.25:.3f});")
    sfx(t + 0.15, "PO-006", -12)
fin("#t15b", L(70.07), 12, 0.35)
sfx(67.45, "IM-003", -12, trim=1.0)

# S16 A 75.0-end: like CTA
grp("s16", 75.0, TOTAL + 0.1,
    f'<div class="t" style="top:420px;display:flex;justify-content:center"><div id="lk" class="pill lt" style="position:relative;height:130px;border-radius:65px;font-size:76px;padding:0 50px">'
    f'{svg("thumbs", 74, "#6A2BF0", 2.4)}like</div></div>'
    '<svg style="left:390px;top:335px" width="300" height="300"><circle id="rg" cx="150" cy="150" r="120" stroke="#FDFE48" stroke-width="6" fill="none" opacity="0"/></svg>')
fin("#lk", L(76.58), 16, 0.4, 8, 0.96); draw("#lk", 76.65, 0.5)
for t in [80.15]:
    tw(f"tl.fromTo('#lk',{{scale:1}},{{scale:.9,duration:.09,yoyo:true,repeat:1,ease:'power2.inOut',immediateRender:false}},{t:.3f});")
    tw(f"tl.fromTo('#rg',{{opacity:.9,scale:.6,transformOrigin:'50% 50%'}},{{opacity:0,scale:1.6,duration:.6,ease:'expo.out'}},{t + 0.05:.3f});")
    sfx(t, "UI-029", -6)
sfx(76.58, "PO-016", -8)

CSS = open(os.path.join(HERE, "img2662_alex.css")).read()
html = f"""<!doctype html>
<html lang="ar"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <div id="cam"><video id="camv" class="clip" src="assets/aroll.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0"></video><div class="vig"></div></div>
  <div id="shade"></div><div id="canvas"></div><div id="canvas2"></div>
  {chr(10).join("  " + x for x in H)}
  <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-volume="1"></audio>
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  gsap.set('.grp,.cap',{{autoAlpha:0}});
  gsap.set('#camv',{{filter:'blur(0px)',scale:1,transformOrigin:'50% 45%'}});
  {chr(10).join("  " + x for x in J)}
  tl.to({{}},{{duration:0.001}},{TOTAL - 0.01});
  window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>"""
open(os.path.join(PROJ, "index.html"), "w", encoding="utf-8").write(html)
json.dump(sorted(CUES), open(os.path.join(WK, "sfx_cues_alex.json"), "w"))
print("ok", len(CUES), "sfx")
