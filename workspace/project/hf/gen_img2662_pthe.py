# Developed by Mehdi ORANUSS | Powered by Claude
"""IMG_2662 reel (9:16, 81.95 s) in the premium-talking-head-editor style (~/.claude/skills/premium-talking-head-editor).
Palette Gold + dark orange: vibrant #F2E186 · dark rich #8E4A2B · tinted white #F6EBE2 · tinted black #1C1410.
Type: Milan Display (special words, boxes, numbers; user's choice) + IBM Plex Sans Arabic Regular (thin lead-ins).
Scenes change every 2-4 s: A-roll pages (thin lead-in + one gold special word) ↔ cream full-screen scenes
(threshold + callback, two-object, one-object/illustration, real elements, graph) ↔ B-roll stills with selector / ring.
No emoji: line icons in dark-rich orbs, real photos. Safe zone x 120-960, y 380-1440. Only clearly spoken words.
Writes hf/img2662-pthe/index.html and work/img2662/sfx_cues_pthe.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "img2662-pthe")
WK = os.path.join(HERE, "..", "work", "img2662")
TOTAL = 81.95
H, J, CUES = [], [], []
def h(s): H.append(s)
def tw(s): J.append(s)
def sfx(t, sid, db, align="peak", trim=None): CUES.append((round(t, 3), sid, align, db, trim))
L = lambda x: round(x - 0.067, 3)

P = {
 "bulb": ['<path d="M9 18h6M10 21h4"/>', '<path d="M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>'],
 "clock": ['<circle cx="12" cy="12" r="9"/>', '<path d="M12 7v5l3.5 2"/>'],
 "battery": ['<rect x="2" y="7" width="17" height="10" rx="2.5"/>', '<path d="M22 11v2M5.5 10.5v3"/>'],
 "book": ['<path d="M3 5h6a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H3z"/>', '<path d="M21 5h-6a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h7z"/>'],
 "chat": ['<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.4A8 8 0 1 1 21 12z"/>'],
 "star": ['<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9z"/>'],
 "check": ['<path d="M5 12.5l4.5 4.5L19 7"/>'],
 "user": ['<circle cx="12" cy="8" r="4"/>', '<path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>'],
}
def svg(name, size=96, color="#F6EBE2", sw=1.8):
    inner = "".join(p.replace("/>", ' pathLength="1" class="dr"/>', 1) for p in P[name])
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray:1">{inner}</svg>')
def orb(oid, icon, x, y, w=200, col=True):
    c = f'<div id="{oid}c" class="col" style="left:{x + w / 2 - 75:.0f}px;top:{y + w * .6:.0f}px"></div>' if col else ""
    return c + f'<div id="{oid}" class="orb" style="left:{x}px;top:{y}px;width:{w}px;height:{w}px">{svg(icon, int(w * .48))}</div>'
ARCS = ('<svg class="arcs" viewBox="0 0 640 640" fill="none"><path d="M60 600 C 80 300, 300 90, 600 70" stroke="#C9A58C" stroke-width="40" stroke-linecap="round" opacity=".55"/>'
        '<path d="M150 610 C 170 380, 360 190, 610 170" stroke="#DCC2AE" stroke-width="26" stroke-linecap="round" opacity=".6"/></svg>')

# ---------------- base camera: speaker in the upper half (scale 1.12, up 110 px) ----------------
BASE = "scale:1.12,y:-110"
CUTS = []   # (t, kind) every scene change, for the whoosh-on-cut rule
def grp(gid, t0, t1, inner, kind="cream", push=True):
    bg = '<div class="cream"></div>' + ARCS if kind == "cream" else ""
    h(f'<div id="{gid}" class="grp">{bg}<div id="{gid}in" class="grp">{inner}</div></div>')
    tw(f"tl.set('#{gid}',{{autoAlpha:1}},{t0:.3f});tl.set('#{gid}',{{autoAlpha:0}},{t1:.3f});")
    if push:
        tw(f"tl.fromTo('#{gid}in',{{scale:1}},{{scale:1.04,duration:{t1 - t0:.2f},ease:'none'}},{t0:.3f});")
    CUTS.append((t0, kind)); CUTS.append((t1, "a"))
def rise(sel, t, dy=26, d=0.32):      # mask-rise
    tw(f"tl.fromTo('{sel}',{{y:{dy},opacity:0}},{{y:0,opacity:1,duration:{d},ease:'expo.out'}},{t:.3f});")
def popo(sel, t):                    # pop with small overshoot 0.8 → 1.04 → 1
    tw(f"tl.fromTo('{sel}',{{scale:.8,opacity:0}},{{keyframes:[{{scale:1.04,opacity:1,duration:.24,ease:'power2.out'}},{{scale:1,duration:.14,ease:'power1.inOut'}}]}},{t:.3f});")
def draw(sel, t, d=0.6):
    tw(f"tl.fromTo('{sel} .dr',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{d},ease:'power2.out',stagger:.08}},{t:.3f});")
def wipe(sel, t):                    # box wipes in from the right (RTL), ~7 frames
    tw(f"tl.fromTo('{sel}',{{clipPath:'inset(0% 0% 0% 100%)'}},{{clipPath:'inset(0% 0% 0% 0%)',duration:.24,ease:'power3.out'}},{t:.3f});")
def glitch(sel, t):                  # hook glitch-in (whole word: Arabic letters must stay joined)
    tw(f"tl.fromTo('{sel}',{{opacity:0}},{{keyframes:[{{opacity:1,x:-14,skewX:-12,textShadow:'4px 0 #ff3b3b,-4px 0 #3bd5ff',duration:.04}},"
       f"{{opacity:.2,x:10,skewX:8,duration:.04}},{{opacity:1,x:-6,skewX:0,duration:.04}},{{opacity:.5,x:4,duration:.04}},"
       f"{{opacity:1,x:0,textShadow:'0 0 26px rgba(242,225,134,.25), 0 4px 20px rgba(0,0,0,.45)',duration:.06}}]}},{t:.3f});")

# ---------------- caption pages (A-roll) ----------------
pages = []
def page(t_th, th, t_sp, sp, t_end, latin=False, gl=False, top=1235):
    k = len(pages); pages.append(k)
    a = f'<span class="mk"><span id="g{k}t" class="th">{th}</span></span>' if th else ""
    b = f'<span class="mk"><span id="g{k}s" class="sp{" lt" if latin else ""}">{sp}</span></span>' if sp else ""
    h(f'<div id="pg{k}" class="page" style="top:{top}px">{a}{b}</div>')
    t0 = min(x for x in [t_th, t_sp] if x is not None)
    tw(f"tl.set('#pg{k}',{{autoAlpha:1}},{L(t0):.3f});tl.set('#pg{k}',{{autoAlpha:0}},{t_end:.3f});")
    if th: rise(f"#g{k}t", L(t_th)); sfx(t_th, "PO-008", -14)
    if sp:
        (glitch if gl else rise)(f"#g{k}s", L(t_sp)); sfx(t_sp, "NG-007" if gl else "PO-006", -12 if gl else -11)

# A-roll beats (+ punch-ins on transitional lines)
page(0.48, "كل نهار", 1.14, "social media", 3.05, latin=True, gl=True)
page(None, "", 3.22, "المشكلة", 6.25)
page(16.15, "الحل", 16.55, "بسيط", 19.05)
page(27.98, "استفادة", 28.67, "المعلومات", 30.85)
page(None, "", 39.49, "تجارب الناس", 40.55)
page(None, "", 48.23, "مثال", 49.25, gl=True)
page(60.3, "تجربة", 60.81, "الناس", 62.85)
page(None, "", 67.45, "social media", 69.95, latin=True, gl=True)
page(None, "", 76.58, "like", 81.9, latin=True, gl=True)
PUNCH = [(10.6, 13.1), (19.1, 21.4), (37.7, 39.4)]
for a, b in PUNCH:      # transitional lines: punch-in on the face, no text
    tw(f"tl.set('#camv',{{scale:1.22,y:-40}},{a:.3f});tl.set('#camv',{{{BASE}}},{b:.3f});")
tw("tl.to('#camv',{scale:1.16,duration:.5,ease:'expo.out'},76.5);tl.to('#camv',{scale:1.2,duration:.12,yoyo:true,repeat:1},80.15);")
sfx(80.15, "UI-029", -11)

# L03 cream 6.3-10.6: THRESHOLD (problem) — ideas stay under the dotted line
OX = [(170, 1010), (440, 960), (710, 1010)]
grp("s3", 6.3, 10.6,
    '<div id="t3" class="tl c" style="top:430px">كل مرة</div>'
    '<div id="dl3" class="dline" style="left:120px;right:120px;top:820px"></div>'
    '<div style="left:0;right:0;top:783px;display:flex;justify-content:center"><div id="pk3" class="pillk" style="position:relative">فكرة جديدة</div></div>'
    + "".join(orb(f"o3{i}", "bulb", x, y) for i, (x, y) in enumerate(OX)))
rise("#t3", L(6.44)); tw("tl.fromTo('#dl3',{scaleX:0},{scaleX:1,duration:.5,ease:'power3.out'},6.5);")
for i in range(3):
    tw(f"tl.fromTo('#o3{i},#o3{i}c',{{y:420,opacity:0}},{{y:0,opacity:1,duration:.7,ease:'expo.out'}},{6.9 + i * 0.5:.3f});"); draw(f"#o3{i}", 7.2 + i * 0.5)
    tw(f"tl.to('#o3{i}',{{y:-60,duration:.35,yoyo:true,repeat:1,ease:'power2.out'}},{9.3 + i * 0.12:.3f});")   # bump into the line, fall back
    sfx(6.9 + i * 0.5, "PO-006", -14)
popo("#pk3", L(8.97)); sfx(8.97, "PO-016", -11)

# L05 cream 13.1-15.9: two objects (upper text / lower objects)
grp("s5", 13.1, 15.9,
    '<div id="t5" class="tl" style="top:440px">الوقت</div><div class="bxw" style="top:530px"><div id="b5" class="bx">والمجهود</div></div>'
    + orb("o51", "clock", 600, 900, 230) + orb("o52", "battery", 250, 940, 230))
rise("#t5", L(13.31)); wipe("#b5", L(13.75)); popo("#o51", 13.4); draw("#o51", 13.6); popo("#o52", 13.85); draw("#o52", 14.05)
tw("tl.fromTo('#o51c,#o52c',{opacity:0},{opacity:1,duration:.6},13.5);")
sfx(13.75, "PO-006", -11); sfx(13.4, "PO-008", -15)

# L08 cream 21.4-24.5: the ideas → 3 kinds
grp("s8", 21.4, 24.5,
    '<div id="t8" class="tl c" style="top:420px">الأفكار</div><div id="n8" class="num" style="top:520px">3</div>'
    + "".join(orb(f"o8{i}", n, x, 1000, 190) + f'<div id="l8{i}" class="olab" style="left:{x - 35}px;top:1210px">0{i + 1}</div>'
              for i, (n, x) in enumerate([("book", 720), ("chat", 445), ("star", 170)])))
rise("#t8", L(21.64)); popo("#n8", L(22.95)); sfx(22.95, "PO-016", -11)
for i in range(3):
    popo(f"#o8{i}", 23.2 + i * 0.15); draw(f"#o8{i}", 23.35 + i * 0.15); rise(f"#l8{i}", 23.4 + i * 0.15); sfx(23.2 + i * 0.15, "PO-008", -16)

# L09 cream 24.5-27.6: illustration — kind 1, educational
grp("s9", 24.5, 27.6,
    '<div id="t9" class="tl" style="top:430px">محتوى</div><div class="bxw" style="top:520px"><div id="b9" class="bx">تعليمي</div></div>'
    '<div id="c9" style="left:240px;top:820px;width:600px;height:600px;border-radius:50%;background:#EAD6C4"></div>'
    + orb("o9", "book", 390, 970, 300, col=False))
rise("#t9", 24.6); popo("#c9", 24.6); popo("#o9", 24.8); draw("#o9", 25.0, 0.9); wipe("#b9", L(26.15)); sfx(26.15, "PO-006", -11)

# L11 cream 30.9-34.0: kind 2, solves problems
grp("s11", 30.9, 34.0,
    '<div id="t11" class="tl" style="top:430px">محتوى</div><div class="bxw" style="top:520px"><div id="b11" class="bx">يحل المشاكل</div></div>'
    '<div id="c11" style="left:240px;top:820px;width:600px;height:600px;border-radius:50%;background:#EAD6C4"></div>'
    + orb("o11", "chat", 390, 970, 300, col=False))
rise("#t11", L(31.16)); popo("#c11", 31.0); popo("#o11", 31.2); draw("#o11", 31.4, 0.9); wipe("#b11", L(33.57)); sfx(33.57, "PO-006", -11)

# L12 cream 34.0-37.7: real elements — questions in, answer out
bubs = "".join(f'<div id="q{i}" class="bub in" style="left:30px;top:{50 + i * 110}px;width:{[460, 410, 440][i]}px"><div class="qm">?</div><i style="width:{[290, 230, 270][i]}px"></i></div>' for i in range(3))
grp("s12", 34.0, 37.7,
    '<div id="t12" class="tl c" style="top:420px">للأسئلة</div>'
    f'<div id="cw" class="wcard" style="left:150px;top:560px;width:780px;height:520px">{bubs}'
    '<div id="an" class="bub out" style="right:30px;top:390px;width:390px"><div id="ty" class="dots3"><u></u><u></u><u></u></div>'
    f'<div id="ao" style="position:static;opacity:0">{svg("check", 50, "#F2E186", 2.6)}</div></div></div>')
tw("tl.fromTo('#cw',{y:80,opacity:0,rotation:-3},{y:0,opacity:1,rotation:0,duration:.5,ease:'expo.out'},34.05);"); rise("#t12", L(35.06))
for i in range(3):
    rise(f"#q{i}", L(35.06) + i * 0.3, 20, 0.3); sfx(35.06 + i * 0.3, "PO-008", -15)
rise("#an", 36.25, 20, 0.3)
tw("tl.fromTo('#ty u',{y:0},{y:-10,duration:.18,yoyo:true,repeat:3,stagger:.08,ease:'sine.inOut'},36.35);tl.set('#ty',{display:'none'},37.0);tl.to('#ao',{opacity:1,duration:.1},37.0);")
draw("#ao", 37.0, 0.3); sfx(37.0, "PO-006", -11)

# L14 cream 40.6-43.6: real elements — people's reviews
def rvc(rid, x, y, rot):
    return (f'<div id="{rid}" class="wcard rvc" style="left:{x}px;top:{y}px;width:560px;height:220px;transform:rotate({rot}deg)">'
            f'<div style="left:28px;top:28px;width:96px;height:96px;border-radius:50%;background:var(--rich);display:flex;align-items:center;justify-content:center">{svg("user", 52)}</div>'
            f'<div id="{rid}s" class="stars" style="left:150px;top:40px">★★★★★</div><i style="left:30px;top:150px;width:480px"></i><i style="left:30px;top:178px;width:330px"></i></div>')
grp("s14", 40.6, 43.6, '<div id="t14" class="tl c" style="top:420px">تجارب الناس</div>' + rvc("r1", 400, 600, 3) + rvc("r2", 120, 880, -3))
rise("#t14", 40.65)
for i, t in enumerate([40.7, 41.8]):
    tw(f"tl.fromTo('#r{i + 1}',{{y:120,opacity:0}},{{y:0,opacity:1,duration:.5,ease:'expo.out'}},{t:.3f});tl.to('#r{i + 1}s',{{color:'#C9963B',duration:.6}},{t + 0.4:.3f});")
    sfx(t, "PO-008", -15)

# L15 cream 43.6-47.9: graph — results
grp("s15", 43.6, 47.9,
    '<div class="bxw c" style="top:430px"><div id="b15" class="bx">النتائج</div></div>'
    '<svg id="g15" style="left:120px;top:700px" width="840" height="620" viewBox="0 0 840 620">'
    '<defs><linearGradient id="gf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E4A2B" stop-opacity=".35"/><stop offset="1" stop-color="#8E4A2B" stop-opacity="0"/></linearGradient></defs>'
    '<path id="fl" d="M40 560 C 200 540, 320 470, 420 420 S 640 220, 800 90 V600 H40 Z" fill="url(#gf)" opacity="0"/>'
    '<path id="ln" d="M40 560 C 200 540, 320 470, 420 420 S 640 220, 800 90" stroke="#8E4A2B" stroke-width="10" fill="none" stroke-linecap="round" pathLength="1" style="stroke-dasharray:1"/>'
    '<path d="M40 600 H800" stroke="rgba(74,42,30,.35)" stroke-width="3" stroke-dasharray="6 10"/>'
    '<circle id="d15" cx="800" cy="90" r="20" fill="#F2E186" stroke="#8E4A2B" stroke-width="6" opacity="0"/></svg>')
wipe("#b15", L(43.6)); sfx(43.6, "PO-006", -11)
tw("tl.fromTo('#ln',{strokeDashoffset:1},{strokeDashoffset:0,duration:1.6,ease:'power2.inOut'},43.9);tl.to('#fl',{opacity:1,duration:.8},44.6);"
   "tl.fromTo('#d15',{opacity:0,scale:0,transformOrigin:'50% 50%'},{opacity:1,scale:1,duration:.35,ease:'back.out(1.6)'},45.45);")
sfx(45.45, "PO-016", -13)

# L17-18 b-roll 49.3-57.6: stills with tracked selector, pan + camera-shutter cut
def broll(gid, t0, t1, img, sel, lab, ring=None):
    x, y, w, hh = sel
    inner = (f'<div class="broll"><img id="{gid}i" class="bg" src="assets/{img}"/></div>'
             + (f'<div id="{gid}r" class="ring" style="left:{ring[0]}px;top:{ring[1]}px;width:{ring[2]}px;height:{ring[2]}px"></div>' if ring else "")
             + f'<div id="{gid}s" class="sel" style="left:{x}px;top:{y}px;width:{w}px;height:{hh}px"><i></i><i></i><i></i><i></i></div>'
             + f'<svg id="{gid}a" style="left:{x + w - 40}px;top:{y - 170}px" width="160" height="170" fill="none"><path d="M140 20 C 60 20, 30 70, 40 150" stroke="#fff" stroke-width="5" stroke-linecap="round" pathLength="1" style="stroke-dasharray:1" class="dr"/><path d="M22 128 L40 152 L58 128" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
             + f'<div id="{gid}l" class="slab" style="right:{1080 - (x + w) - 120}px;top:{y - 250}px">{lab}</div>')
    grp(gid, t0, t1, inner, kind="broll", push=False)
    tw(f"tl.fromTo('#{gid}i',{{x:0}},{{x:-80,duration:{t1 - t0:.2f},ease:'none'}},{t0:.3f});")
    sfx(t0, "CA-001", -9)
broll("s17", 49.3, 54.7, "img_store.jpg", (330, 820, 300, 480), '<span style="font-family:var(--bold)">1</span>')
broll("s18", 54.7, 57.6, "img_choose.jpg", (260, 760, 520, 420), '<span>2</span>', ring=(170, 640, 700))
for gid, t in [("s17", 52.63), ("s18", 54.74)]:
    tw(f"tl.fromTo('#{gid}s',{{scale:1.25,opacity:0}},{{scale:1,opacity:1,duration:.3,ease:'expo.out'}},{L(t):.3f});")
    draw(f"#{gid}a", L(t) + 0.15, 0.4); rise(f"#{gid}l", L(t) + 0.3)
    sfx(t, "PO-008", -14)
tw("tl.fromTo('#s18r',{scale:.85,opacity:0,transformOrigin:'50% 50%'},{scale:1,opacity:1,duration:.5,ease:'expo.out'},54.9);")

# L19 cream 57.6-59.9: real elements — colours
grp("s19", 57.6, 59.9,
    '<div class="bxw c" style="top:420px"><div id="b19" class="bx">الألوان</div></div>'
    '<div id="ph19" class="photo" style="left:170px;top:640px;width:740px;height:520px;transform:rotate(-2deg)"><img src="assets/img_colors.jpg"/></div>'
    + "".join(f'<div id="sw{i}" class="sw" style="left:{215 + i * 135}px;top:1205px;background:{c}"></div>' for i, c in enumerate(["#1C1410", "#F2EBDD", "#C8A27A", "#3F5A7A", "#8E4A2B"])))
wipe("#b19", L(57.67)); tw("tl.fromTo('#ph19',{y:140,opacity:0,rotation:4},{y:0,opacity:1,rotation:-2,duration:.55,ease:'expo.out'},57.65);")
for i in range(5):
    popo(f"#sw{i}", 58.2 + i * 0.08)
sfx(57.67, "PO-006", -11); sfx(58.2, "PO-008", -16)

# L21 cream 62.9-67.2: the 3 kinds, checked
grp("s21", 62.9, 67.2, '<div id="n21" class="num" style="top:400px;font-size:260px">3</div>'
    + "".join(orb(f"o21{i}", n, x, 820, 190) + f'<div id="k21{i}" style="left:{x + 120}px;top:800px;width:76px;height:76px;border-radius:50%;background:#F2E186;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 18px rgba(74,42,30,.3)">{svg("check", 44, "#4A2A1E", 3)}</div>'
              for i, (n, x) in enumerate([("book", 720), ("chat", 445), ("star", 170)])))
popo("#n21", 62.95)
for i in range(3):
    popo(f"#o21{i}", 63.0 + i * 0.1); draw(f"#o21{i}", 63.1 + i * 0.1); popo(f"#k21{i}", L(63.17) + i * 0.33); draw(f"#k21{i}", L(63.17) + i * 0.33 + 0.05, 0.3)
    sfx(63.17 + i * 0.33, "PO-006", -13)

# L23 cream 70.0-75.0: CALLBACK — the same threshold, now the ideas break through with light trails
OX2 = OX + [(305, 1080), (575, 1080)]
grp("s23", 70.0, 75.0,
    '<div id="dl23" class="dline" style="left:120px;right:120px;top:820px"></div>'
    '<div style="left:0;right:0;top:783px;display:flex;justify-content:center"><div id="pk23" class="pillk g" style="position:relative">الأفكار</div></div>'
    + "".join(f'<div id="tr{i}" class="trail" style="left:{x + 92}px;top:{y + 100}px;height:420px;opacity:0"></div>' + orb(f"o23{i}", "bulb", x, y, 180, col=False)
              for i, (x, y) in enumerate(OX2)))
popo("#pk23", L(70.07)); sfx(70.07, "PO-016", -11)
for i, (x, y) in enumerate(OX2):
    t = (70.2 if i < 3 else 71.85) + (i % 3) * 0.18
    dy = -(y - 420) - (i % 2) * 60
    tw(f"tl.fromTo('#o23{i}',{{y:300,opacity:0}},{{y:0,opacity:1,duration:.4,ease:'expo.out'}},{t - 0.4:.3f});draw;"
       .replace("draw;", ""))
    tw(f"tl.to('#o23{i}',{{y:{dy},duration:.8,ease:'power3.inOut'}},{t:.3f});"
       f"tl.fromTo('#tr{i}',{{opacity:0,scaleY:0}},{{opacity:1,scaleY:1,y:{dy},duration:.8,ease:'power3.inOut'}},{t:.3f});")
    draw(f"#o23{i}", t - 0.3); sfx(t + 0.3, "WH-004", -17)
tw("tl.fromTo('#dl23',{opacity:1},{opacity:.35,duration:.4},70.6);")

# whoosh peaking on every cut into / out of a designed scene
seen = set()
for t, kind in CUTS:
    if round(t, 1) in seen or t <= 0.1 or t >= TOTAL - 0.1:
        continue
    seen.add(round(t, 1)); sfx(t, "WH-012", -15)

CSS = open(os.path.join(HERE, "img2662_pthe.css")).read()
html = f"""<!doctype html>
<html lang="ar"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <div id="cam"><video id="camv" class="clip" src="assets/aroll.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0"></video></div>
  <div id="low"></div>
  {chr(10).join("  " + x for x in H)}
  <div id="vig"></div>
  <svg id="grain" width="1180" height="2020"><filter id="nz"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#nz)"/></svg>
  <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-volume="1"></audio>
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  gsap.set('.grp,.page',{{autoAlpha:0}});
  gsap.set('.grp .grp',{{autoAlpha:1}});
  gsap.set('#camv',{{{BASE},filter:'brightness(.84) contrast(1.06)'}});
  {chr(10).join("  " + x for x in J)}
  tl.to({{}},{{duration:0.001}},{TOTAL - 0.01});
  window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>"""
open(os.path.join(PROJ, "index.html"), "w", encoding="utf-8").write(html)
json.dump(sorted(CUES), open(os.path.join(WK, "sfx_cues_pthe.json"), "w"))
print("ok", len(CUES), "sfx,", len(set(round(t, 1) for t, _ in CUTS)), "cuts")
