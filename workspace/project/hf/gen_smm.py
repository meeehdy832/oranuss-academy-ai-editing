# Developed by Mehdi ORANUSS | Powered by Claude
"""SMM 10-scripts series (9:16, ElevenLabs Khalil voiceover). v2 look (user notes 2026-11-21): WHITE background, Oranuss purple
accents, real photos in rounded cards (ElevenLabs Seedream) + 1 AI clip, Arabic-script captions (Graphik Arabic, RTL), no Latin Darija.
Inputs: output/smm-10-scripts/<NN>/ (voice.mp3, words_aligned.json, ai.mp4, p1..p6.jpg) -> project/hf/smm<NN>/index.html
+ project/work/smm<NN>/sfx_cues.json (mix by project/audio_smm.py).  usage: python3 -I gen_smm.py 01"""
import json, os, shutil, sys
NN = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(TOP, "output", "smm-10-scripts", NN)
PROJ = os.path.join(HERE, f"smm{NN}"); AS = os.path.join(PROJ, "assets")
WK = os.path.join(TOP, "project", "work", f"smm{NN}")
os.makedirs(os.path.join(AS, "fonts"), exist_ok=True); os.makedirs(WK, exist_ok=True)
for f in os.listdir(os.path.join(HERE, "leverage", "assets", "fonts")):
    shutil.copy(os.path.join(HERE, "leverage", "assets", "fonts", f), os.path.join(AS, "fonts", f))
for f in os.listdir(SRC):
    if f.startswith("p") and f.endswith(".jpg"):
        shutil.copy(os.path.join(SRC, f), os.path.join(AS, f))
W = json.load(open(os.path.join(SRC, "words_aligned.json")))
LEAD = 0.067
def T(i): return round(max(W[i][0] - LEAD, 0), 3)          # graphic time for word i
VOICE_END = W[-1][1] + 0.3
END_HOLD = 2.6
TOTAL = round(VOICE_END + END_HOLD, 2)

# ---------------- kit ----------------
H, J, CUES = [], [], []
def h(s): H.append(s)
def tw(s): J.append(s)
def sfx(t, sid, extra=0, trim=None): CUES.append((round(max(t, 0), 3), sid, "peak", extra, trim))
def grp(gid, t0, t1, inner):
    h(f'<div id="{gid}" class="grp">{inner}</div>')
    tw(f"tl.set('#{gid}',{{autoAlpha:1}},{t0:.3f});")
    tw(f"tl.to('#{gid}',{{autoAlpha:0,y:-40,filter:'blur(10px)',duration:.25,ease:'power2.in'}},{t1 - 0.25:.3f});")
def rise(sel, t, dy=60, d=0.55):
    tw(f"tl.fromTo('{sel}',{{y:{dy},opacity:0,filter:'blur(10px)'}},{{y:0,opacity:1,filter:'blur(0px)',duration:{d},ease:'expo.out'}},{t:.3f});")
def slide(sel, t, dx=-140, d=0.5):
    tw(f"tl.fromTo('{sel}',{{x:{dx},opacity:0,filter:'blur(8px)'}},{{x:0,opacity:1,filter:'blur(0px)',duration:{d},ease:'expo.out'}},{t:.3f});")
def pop(sel, t, s0=0.4, d=0.55):
    tw(f"tl.fromTo('{sel}',{{scale:{s0},opacity:0}},{{scale:1,opacity:1,duration:{d},ease:'back.out(1.8)'}},{t:.3f});")
def slam(sel, t, s0=1.6):
    tw(f"tl.fromTo('{sel}',{{scale:{s0},opacity:0,filter:'blur(14px)'}},{{scale:1,opacity:1,filter:'blur(0px)',duration:.38,ease:'expo.out'}},{t:.3f});")
def strike(sel, t):
    tw(f"tl.fromTo('{sel}',{{scaleX:0}},{{scaleX:1,duration:.35,ease:'expo.out'}},{t:.3f});")
def dim(sel, t, o=.35):
    tw(f"tl.to('{sel}',{{opacity:{o},filter:'grayscale(1)',duration:.4}},{t:.3f});")
def glow(sel, t):
    tw(f"tl.fromTo('{sel}',{{boxShadow:'0 20px 50px rgba(91,43,224,.15)'}},{{boxShadow:'0 0 80px rgba(91,43,224,.6)',duration:.5,yoyo:true,repeat:1}},{t:.3f});")
def count(sel, t, v0, v1, d=1.2):
    tw(f"(function(){{const o={{v:{v0}}};tl.to(o,{{v:{v1},duration:{d},ease:'power3.out',onUpdate:()=>{{"
       f"document.querySelector('{sel}').textContent=Math.round(o.v).toLocaleString('en-US')}}}},{t:.3f});}})();")
def photo(pid, src, t0, t1, x=60, y=230, w=960, h=560, z0=1.0, z1=1.12):
    """rounded photo card with slow Ken Burns push"""
    rise(f"#{pid}", t0 + 0.02, 70, 0.7)
    tw(f"tl.fromTo('#{pid} img',{{scale:{z0}}},{{scale:{z1},duration:{t1 - t0:.3f},ease:'none',immediateRender:false}},{t0:.3f});")
    return f'<div id="{pid}" class="ph" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><img src="assets/{src}"/></div>'

IC = {
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>', "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M21.5 20a6.5 6.5 0 0 0-4-6"/>',
    "cart": '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.6 12.2a2 2 0 0 0 2 1.6h8.2a2 2 0 0 0 2-1.5L21.5 7H6"/>',
    "heart": '<path d="M12 20.5s-8-4.6-8-10.4A4.6 4.6 0 0 1 12 7a4.6 4.6 0 0 1 8 3.1c0 5.8-8 10.4-8 10.4z" fill="currentColor"/>',
    "gift": '<rect x="3" y="8" width="18" height="13" rx="2"/><path d="M12 8v13M3 12h18M12 8S10 3 7.5 4 9 8 12 8zm0 0s2-5 4.5-4S15 8 12 8z"/>',
    "trophy": '<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4"/>',
    "fire": '<path d="M12 2c1 4 5 6 5 11a5 5 0 0 1-10 0c0-3 2-4 2-7 2 1 3 3 3 5 1-2 1-5 0-9z"/>',
    "clover": '<circle cx="8.5" cy="8.5" r="3.5"/><circle cx="15.5" cy="8.5" r="3.5"/><circle cx="8.5" cy="15.5" r="3.5"/><circle cx="15.5" cy="15.5" r="3.5"/><path d="M12 12l5 10"/>',
    "q": '<circle cx="12" cy="12" r="10"/><path d="M9.2 9a3 3 0 0 1 5.8 1c0 2-3 2.5-3 4.5M12 18h.01"/>',
    "image": '<rect x="3" y="4" width="18" height="16" rx="2.5"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-9 9"/>',
    "briefcase": '<rect x="2.5" y="7" width="19" height="13" rx="2.5"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M2.5 13h19"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/>',
    "spark": '<path d="M12 2c.6 4.6 2.4 6.4 7 7-4.6.6-6.4 2.4-7 7-.6-4.6-2.4-6.4-7-7 4.6-.6 6.4-2.4 7-7z" fill="currentColor" stroke="none"/>',
    "folder": '<path d="M3 6.5A2.5 2.5 0 0 1 5.5 4H10l2 2.5h6.5A2.5 2.5 0 0 1 21 9v8.5a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 17.5z"/>',
}
P, INK = "#5B2BE0", "#140F2E"
def svg(name, size=80, sw=2.0, color=P):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" style="color:{color}">{IC[name]}</svg>')
def chip(cid, x, y, ic, label, cls="chip"):
    return f'<div id="{cid}" class="{cls}" style="left:{x}px;top:{y}px">{svg(ic, 54, 2.2)}<span>{label}</span></div>'

# ---------------- per-video spec ----------------
SPEC = {}
def video01():
    # 1 hook: AI clip (from photo p1) + follower counter + 0 sales
    t0, t1 = 0.0, T(10)
    grp("g1", t0, t1,
        '<div id="vcard" class="ph" style="left:60px;top:230px;width:960px;height:540px"><video id="aiv" class="clip" src="assets/ai.mp4" muted playsinline '
        f'data-start="0" data-duration="{t1:.2f}" data-track-index="2"></video></div>'
        '<div id="fol" class="card stat" style="left:140px;top:830px;width:800px;height:220px">'
        f'<div class="sic">{svg("users", 88, 2)}</div><div><div id="foln" class="big">0</div><div class="lbl">متابع</div></div></div>'
        f'<div id="ven" class="redpill" style="left:330px;top:1100px">{svg("cart", 56, 2.4, "#fff")}<span>0 مبيعات</span></div>')
    rise("#vcard", 0.0, 80, 0.7); rise("#fol", T(1), 50); count("#foln", T(1), 0, 10000, 1.3)
    slam("#ven", T(8)); tw(f"tl.to('#ven',{{x:-14,duration:.06,yoyo:true,repeat:5}},{T(8) + 0.3:.3f});")
    sfx(T(1), "WH-012", -4); sfx(T(8), "IM-003", -5)
    # 2 not luck -> who follows you
    t0, t1 = T(10), T(19)
    grp("g2", t0, t1,
        f'<div id="clv" class="card ico" style="left:390px;top:300px">{svg("clover", 170, 1.6)}<div id="clx" class="xline"></div></div>'
        '<div id="l7" class="tline" style="top:640px">ماشي <b>الحظ</b></div>'
        f'<div id="qbig" style="left:430px;top:830px">{svg("q", 220, 1.6)}</div>'
        '<div id="ava" class="arow" style="top:1090px">' + "".join(f'<div class="av" id="av{i}">{svg("user", 66, 2, "#fff")}</div>' for i in range(5)) + '</div>')
    pop("#clv", t0 + 0.02); rise("#l7", T(11), 40); strike("#clx", T(13)); dim("#clv", T(13) + 0.2)
    pop("#qbig", T(14), 0.3, 0.6)
    for i in range(5): pop(f"#av{i}", T(16) + i * 0.08, 0.3, 0.45)
    sfx(T(13), "WH-163", -6); sfx(T(16), "PO-013", -6)
    # 3 chasing numbers (photo p2: staged trend video)
    t0, t1 = T(19), T(34)
    grp("g3", t0, t1, photo("p2", "p2.jpg", t0, t1) +
        '<div id="ar" class="tline sm" style="top:830px">كيجريو مور <b>الأرقام</b></div>' +
        chip("c1", 560, 990, "gift", "giveaways") + chip("c2", 150, 990, "trophy", "تحديات") + chip("c3", 380, 1130, "fire", "ترند") +
        '<div id="z3" class="redpill" style="left:200px;top:1100px"><span>حتى علاقة مع الخدمة</span></div>')
    rise("#ar", T(21), 40)
    for c, i in (("c1", 24), ("c2", 25), ("c3", 27)):
        slide(f"#{c}", T(i), 160 if c == "c1" else -160); sfx(T(i), "PO-013", -9)
    tw(f"tl.to('#c1,#c2,#c3',{{opacity:0,y:-30,duration:.25}},{T(28) + 0.4:.3f});")
    slam("#z3", T(30)); sfx(T(30), "IM-003", -7)
    # 4 big crowd, few clients (photo p3)
    t0, t1 = T(34), T(42)
    dots = "".join(f'<i class="dot{" on" if i in (7, 24, 33) else ""}"></i>' for i in range(40))
    grp("g4", t0, t1, photo("p3", "p3.jpg", t0, t1) +
        '<div id="nt" class="tline sm" style="top:830px">جمهور <b>كبير</b>…</div>'
        f'<div id="crowd" class="crowd" style="left:140px;top:980px">{dots}</div>')
    slam("#nt", T(35), 1.3)
    tw(f"tl.fromTo('#crowd i',{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.35,ease:'back.out(2)',stagger:{{each:.015,from:'center'}}}},{T(35) + 0.15:.3f});")
    tw(f"tl.to('#crowd i:not(.on)',{{opacity:.15,duration:.4}},{T(40):.3f});")
    tw(f"tl.to('#crowd i.on',{{scale:1.8,background:'{P}',boxShadow:'0 0 30px rgba(91,43,224,.8)',duration:.45,ease:'back.out(2)'}},{T(40):.3f});")
    sfx(T(35), "WH-012", -5); sfx(T(40), "PO-013", -5)
    # 5 wrong question -> right question
    t0, t1 = T(42), T(61)
    grp("g5", t0, t1,
        '<div id="qa" class="qcard" style="left:90px;top:330px;width:900px"><span class="qn">✕</span>شحال عندي من فولوور؟<div id="qax" class="xline"></div></div>'
        '<div id="qb" class="qcard ok" style="left:90px;top:640px;width:900px"><span class="qn y">✓</span>واش الناس اللي تابعيني عندهم المشكل اللي <b>كنحلو</b>؟</div>'
        f'<div id="tg" style="left:440px;top:1020px">{svg("target", 200, 1.6)}</div>')
    rise("#qa", T(44), 50); strike("#qax", T(49)); dim("#qa", T(49) + 0.2, .45)
    rise("#qb", T(52), 50); glow("#qb", T(57)); pop("#tg", T(57), 0.3)
    sfx(T(49), "WH-163", -6); sfx(T(57), "IM-003", -8)
    # 6 1000 interested vs 100K watchers (photo p6: engaged customers) — numbers are the spoken example
    t0, t1 = T(61), T(74)
    grp("g6", t0, t1, photo("p6", "p6.jpg", t0, t1, y=230, h=500) +
        '<div id="o1" class="orb solid" style="left:610px;top:800px"><div class="on1">1,000</div><div class="ol">مهتم</div></div>'
        '<div id="gt" class="tline" style="left:470px;right:auto;width:140px;top:870px"><b>&gt;</b></div>'
        '<div id="o2" class="orb hollow" style="left:90px;top:780px"><div class="on1">100K</div><div class="ol">كيتفرجو</div></div>')
    pop("#o1", T(61), 0.3); pop("#o2", T(69), 0.3); slam("#gt", T(66), 2)
    tw(f"tl.to('#o2',{{opacity:.4,y:50,duration:.6,ease:'power2.out'}},{T(71):.3f});")
    tw(f"tl.to('#o1',{{y:-30,boxShadow:'0 0 90px rgba(91,43,224,.75)',duration:.6,ease:'power2.out'}},{T(71):.3f});")
    sfx(T(66), "IM-003", -6); sfx(T(71), "WH-012", -6)
    # 7 before posting: client or likes? (photo p5: owner thinking)
    t0, t1 = T(74), T(95)
    grp("g7", t0, t1, photo("p5", "p5.jpg", t0, t1) +
        '<div id="sl" class="tline sm" style="top:830px">سول راسك <b>قبل</b> ما تنشر</div>'
        f'<div id="tz" class="tog" style="left:570px;top:1000px">{svg("briefcase", 58, 2.2)}<span>الزبون</span></div>'
        f'<div id="tl_" class="tog" style="left:110px;top:1000px">{svg("heart", 58, 2.2, "#FF4D6D")}<span>likes</span></div>')
    rise("#sl", T(81), 40); pop("#tz", T(88), 0.4); pop("#tl_", T(90), 0.4)
    tw(f"tl.to('#tz',{{background:'{P}',color:'#fff',borderColor:'{P}',boxShadow:'0 0 60px rgba(91,43,224,.6)',scale:1.08,duration:.4}},{T(94) + 0.2:.3f});")
    tw(f"tl.to('#tz svg',{{stroke:'#fff',duration:.4}},{T(94) + 0.2:.3f});")
    dim("#tl_", T(94) + 0.2, .45)
    sfx(T(88), "PO-013", -7); sfx(T(94) + 0.2, "IM-003", -8)
    # 8 followers -> image, clients -> business (photo p4: real sale)
    t0, t1 = T(95), T(102)
    grp("g8", t0, t1, photo("p4", "p4.jpg", t0, t1, y=230, h=500) +
        f'<div id="k1" class="card kc" style="left:560px;top:790px;width:430px;height:420px"><div class="kic">{svg("users", 90, 1.8)}</div><div class="kt">الفولوورز</div><div class="ka">↓</div><div class="kt">الصورة</div></div>'
        f'<div id="k2" class="card kc hi" style="left:90px;top:790px;width:430px;height:420px"><div class="kic">{svg("target", 90, 1.8, "#fff")}</div><div class="kt">الكليان</div><div class="ka">↓</div><div class="kt"><b>البيزنس</b></div></div>')
    slide("#k1", T(95), 160); slide("#k2", T(98), -160); glow("#k2", T(101))
    sfx(T(95), "WH-012", -6); sfx(T(101), "IM-003", -6)
    # 9 CTA end card
    t0 = T(102)
    grp("g9", t0, TOTAL + 0.3,
        f'<div id="fd" style="left:340px;top:330px">{svg("folder", 400, 1.1)}</div>'
        '<div id="wm" class="wm" style="top:820px">ORANUSS ACADEMY</div>'
        '<div id="e1" class="tline sm" style="top:930px">جمهور <b>كيشري</b>،<br>ماشي غير كيتفرج</div>'
        f'<div id="fb" class="redpill vio" style="left:360px;top:1200px">{svg("spark", 48, 2, "#fff")}<span>تابعنا</span></div>')
    pop("#fd", t0, 0.4, 0.7); slam("#wm", T(103), 1.4); rise("#e1", T(108), 40); pop("#fb", VOICE_END, 0.4)
    tw(f"tl.fromTo('#fd svg',{{filter:'drop-shadow(0 0 0px {P})'}},{{filter:'drop-shadow(0 0 40px rgba(91,43,224,.7))',duration:1.2,yoyo:true,repeat:3}},{t0:.3f});")
    sfx(T(103), "IM-003", -6); sfx(VOICE_END, "LO-003", -8, 1.8)
    # caption chunks: (first word, end word excl, accent position in chunk) — text = the spoken script words (Arabic script)
    return [(0, 4, 3), (4, 10, 4), (10, 14, 3), (14, 19, 2), (19, 24, 4), (24, 28, 0), (28, 34, 3), (34, 37, 1),
            (37, 42, 3), (42, 49, 3), (49, 52, 1), (52, 57, 4), (57, 61, 0), (61, 66, 2), (66, 74, 6), (74, 81, 4),
            (81, 85, 3), (85, 90, 3), (90, 95, 4), (95, 98, 2), (98, 102, 3), (102, 105, 1), (105, 114, 5)]
SPEC["01"] = video01

# ---------------- kit v2 (videos 02-10, same look as approved 01 v2; photos p1 (clip start) + p2..p4) ----------------
IC.update({
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "msg": '<path d="M4 5h16v11H9l-5 4z"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2.5"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    "video": '<rect x="2.5" y="6" width="13" height="12" rx="2.5"/><path d="M15.5 10.5l6-3.5v10l-6-3.5z"/>',
    "repeat": '<path d="M17 2l4 4-4 4"/><path d="M3 11V9a3 3 0 0 1 3-3h15M7 22l-4-4 4-4"/><path d="M21 13v2a3 3 0 0 1-3 3H3"/>',
    "text": '<path d="M5 6h14M12 6v13M9 19h6"/>',
    "book": '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5z"/><path d="M4 21.5V4.5"/>',
    "star": '<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
})
def hook(t1, extra=""):
    grp("g1", 0.0, t1,
        '<div id="vcard" class="ph" style="left:60px;top:230px;width:960px;height:540px"><video id="aiv" class="clip" src="assets/ai.mp4" muted playsinline '
        f'data-start="0" data-duration="{min(t1, 6.0):.2f}" data-track-index="2"></video></div>' + extra)
    rise("#vcard", 0.0, 80, 0.7); sfx(0.05, "WH-012", -4)
def pill(pid, y, ic, label, vio=False):
    return f'<div id="{pid}" class="redpill{" vio" if vio else ""} ctr" style="top:{y}px">{svg(ic, 52, 2.4, "#fff")}<span>{label}</span></div>'
def title(tid, y, html, sm=True):
    return f'<div id="{tid}" class="tline{" sm" if sm else ""}" style="top:{y}px">{html}</div>'
def bigic(bid, y, ic, size=220):
    return f'<div id="{bid}" class="ctr" style="top:{y}px">{svg(ic, size, 1.6)}</div>'
def chips(rid, y, items):
    return (f'<div id="{rid}" class="crow" style="top:{y}px">' +
            "".join(f'<div id="{rid}k{i}" class="chip">{svg(ic, 50, 2.2)}<span>{lb}</span></div>' for i, (ic, lb, _) in enumerate(items)) + '</div>')
def chips_go(rid, items):
    for i, (_, _, t) in enumerate(items): pop(f"#{rid}k{i}", t, 0.4, 0.5); sfx(t, "PO-013", -9)
def steps(sid, y, items, gap=150):
    return "".join(f'<div id="{sid}_{i}" class="step" style="top:{y + i * gap}px"><span class="sn">{i + 1}</span><span>{tx}</span></div>' for i, (tx, _) in enumerate(items))
def steps_go(sid, items):
    for i, (_, t) in enumerate(items): slide(f"#{sid}_{i}", t, 160); sfx(t, "WH-012", -8)
def qc(qid, y, text, ok=False):
    return (f'<div id="{qid}" class="qcard{" ok" if ok else ""}" style="left:90px;top:{y}px;width:900px"><span class="qn{" y" if ok else ""}">{"✓" if ok else "✕"}</span>'
            f'{text}<div id="{qid}x" class="xline"></div></div>')
def kcard(kid, x, top, ic, l1, l2, hi=False, arrow=True):
    return (f'<div id="{kid}" class="card kc{" hi" if hi else ""}" style="left:{x}px;top:{top}px;width:430px;height:420px">'
            f'<div class="kic">{svg(ic, 90, 1.8, "#fff" if hi else P)}</div><div class="kt">{l1}</div>{"<div class=ka>↓</div>" if arrow else ""}'
            f'<div class="kt">{l2}</div><div id="{kid}x" class="xline"></div></div>')
def avrow(aid, y, n, ic="user"):
    return f'<div id="{aid}" class="arow" style="top:{y}px">' + "".join(f'<div class="av" id="{aid}{i}">{svg(ic, 66, 2, "#fff")}</div>' for i in range(n)) + '</div>'
def endcard(t0, ic, line):
    grp("g9", t0, TOTAL + 0.3,
        bigic("fd", 330, ic, 360) +
        '<div id="wm" class="wm" style="top:800px">ORANUSS ACADEMY</div>' + title("e1", 910, line) +
        f'<div id="fb" class="redpill vio ctr" style="top:1200px">{svg("spark", 48, 2, "#fff")}<span>تابعنا</span></div>')
    pop("#fd", t0, 0.4, 0.7); slam("#wm", t0 + 0.4, 1.4); rise("#e1", t0 + 0.9, 40); pop("#fb", VOICE_END, 0.4)
    tw(f"tl.fromTo('#fd svg',{{filter:'drop-shadow(0 0 0px {P})'}},{{filter:'drop-shadow(0 0 40px rgba(91,43,224,.7))',duration:1.2,yoyo:true,repeat:3}},{t0:.3f});")
    sfx(t0 + 0.4, "IM-003", -6); sfx(VOICE_END, "LO-003", -8, 1.8)
STOPW = set("ديال ديالك ديالو ما من على و ولا اللي هو هي هوما راه كل باش غير حتى مع هاد هادا هادي فيه ليك ليهم منو كان".split())
def autocaps(maxw=5):
    """caption chunks from the spoken words: break on punctuation or every maxw words; accent = strongest word"""
    out, cur = [], []
    for i, w in enumerate(W):
        cur.append(i)
        if w[2].rstrip('"“”«»').endswith((".", "،", "؟", "?", ":", "…", ",")) or len(cur) >= maxw:
            out.append(cur); cur = []
    if cur: out.append(cur)
    m = []
    for c in out:
        if m and len(c) == 1 and len(m[-1]) < 6: m[-1] += c
        else: m.append(c)
    caps = []
    for c in m:
        ws = [W[i][2].strip('"“”«»:.،؟?…') for i in c]
        acc = max(range(len(c)), key=lambda k: (ws[k] not in STOPW, (3 if ws[k].isascii() else 0) + len(ws[k])))
        caps.append((c[0], c[-1] + 1, acc))
    return caps
def ph(pid, t0, t1, h=500): return photo(pid, f"{pid}.jpg", t0, t1, y=230, h=h)

def video02():
    hook(T(8), pill("pl", 840, "clock", "أول ثواني")); slam("#pl", T(6)); sfx(T(6), "IM-003", -5)
    t0, t1 = T(8), T(19)
    grp("g2", t0, t1, ph("p2", t0, t1) + qc("q2", 790, '"السلام عليكم، اليوم غادي نهضرو على…"') + pill("ms", 1080, "x", "صافي، مشاو"))
    rise("#q2", T(9), 50); strike("#q2x", T(17)); dim("#q2", T(17) + 0.2, .45); slam("#ms", T(18)); sfx(T(17), "WH-163", -6)
    t0, t1 = T(19), T(36)
    grp("g3", t0, t1, bigic("ey", 330, "eye") + title("bt", 640, "البداية هي <b>الإعلان</b>", False) + pill("nv", 1030, "x", "كلشي ما كيتشافش"))
    pop("#ey", t0, 0.3); rise("#bt", T(22), 40); slam("#nv", T(30)); sfx(T(22), "IM-003", -7); sfx(T(30), "WH-163", -7)
    t0, t1 = T(36), T(62); S = [("بدا بالمشكل", T(42)), ("بدا بنتيجة", T(50)), ("بدا بحاجة ضد اللي كيتسناو", T(57))]
    grp("g4", t0, t1, ph("p3", t0, t1, 420) + steps("s4", 700, S)); steps_go("s4", S)
    t0, t1 = T(62), T(77); C = [("text", "كتابة كبيرة", T(70)), ("spark", "حركة", T(73)), ("eye", "لقطة غريبة", T(75))]
    grp("g5", t0, t1, ph("p4", t0, t1) + title("hb", 790, '"حبس تنشر كل <b>نهار</b>."') + chips("c5", 960, C)); rise("#hb", T(62), 40); chips_go("c5", C)
    t0, t1 = T(77), T(93)
    grp("g6", t0, t1, title("ru", 380, "القاعدة: <b>أول جملة</b>", False) + qc("qk", 700, "«أشنو؟ <b>كمّل</b>»", True) + chips("c6", 1000, [("repeat", "جرب وقارن", T(87))]))
    rise("#ru", T(79), 40); rise("#qk", T(85), 50); glow("#qk", T(86)); chips_go("c6", [("", "", T(87))]); sfx(T(85), "IM-003", -8)
    endcard(T(93), "eye", "كل أسبوع <b>تقنية جديدة</b>")
    return autocaps()
SPEC["02"] = video02

def video03():
    hook(T(9), pill("pl", 840, "cart", '"اشري دابا"'))
    slam("#pl", T(5)); tw(f"tl.to('#pl',{{x:-14,duration:.06,yoyo:true,repeat:5}},{T(7):.3f});"); sfx(T(5), "IM-003", -5)
    t0, t1 = T(9), T(23)
    grp("g2", t0, t1, avrow("av", 330, 4) + qc("q1", 560, "ما كيشريوش من واحد ما كيعرفوهش") + qc("q2", 820, "ولا من واحد كيبيع ليهم كل نهار"))
    for i in range(4): pop(f"#av{i}", t0 + i * 0.08, 0.3, 0.45)
    rise("#q1", T(10), 50); rise("#q2", T(16), 50); sfx(T(10), "PO-013", -6); sfx(T(16), "WH-163", -7)
    for g, (t0, t1, pid, tt, ti, C) in enumerate([
            (T(23), T(37), "p2", "<b>1</b> · يعلّم", T(28), [("book", "نصيحة", T(30)), ("spark", "معلومة", T(31)), ("check", "حل لمشكل صغير", T(32))]),
            (T(37), T(49), "p3", "<b>2</b> · يبني الثقة", T(37), [("eye", "كواليس الخدمة", T(40)), ("users", "قصص الكليان", T(42)), ("briefcase", "كيفاش كتخدم", T(44))]),
            (T(49), T(58), "p4", "<b>3</b> · يبيع", T(49), [("cart", "العرض ديالك", T(51)), ("check", "بوضوح", T(53)), ("fire", "بلا حشمة", T(54))])]):
        gid = f"g{3 + g}"
        grp(gid, t0, t1, ph(pid, t0, t1) + title(f"{gid}t", 790, tt) + chips(f"{gid}c", 950, C)); slam(f"#{gid}t", ti, 1.3); chips_go(f"{gid}c", C)
    t0, t1 = T(58), T(72)
    grp("g6", t0, t1, kcard("k1", 560, 420, "cart", "غير البيع", "كيهربو") + kcard("k2", 90, 420, "book", "غير التعليم", "ما كيشريوش"))
    slide("#k1", T(58), 160); slide("#k2", T(64), -160); sfx(T(58), "WH-012", -6); sfx(T(64), "WH-012", -6)
    t0, t1 = T(72), T(93); S = [("كيعلّم", T(88)), ("كيبني الثقة", T(89)), ("ولا كيبيع؟", T(91))]
    grp("g7", t0, t1, title("sr", 330, "السر: <b>الخليط</b>", False) + pill("hd", 540, "target", "هدف واضح", True) + steps("s7", 700, S))
    slam("#sr", T(72), 1.3); pop("#hd", T(80), 0.4); steps_go("s7", S); sfx(T(72), "IM-003", -6)
    endcard(T(93), "target", "خطة محتوى <b>كتجيب النتيجة</b>")
    return autocaps()
SPEC["03"] = video03

def video04():
    hook(T(10), pill("pl", 840, "q", '"أشنو غادي ننشر اليوم؟"')); slam("#pl", T(3)); sfx(T(3), "IM-003", -6)
    t0, t1 = T(10), T(26); C = [("check", "مرة كاين", T(16)), ("x", "مرة غابر", T(18))]
    grp("g2", t0, t1, title("nk", 360, "النشر بلا <b>خطة</b>", False) + chips("c2", 640, C) + bigic("qq", 880, "q", 200))
    slam("#nk", T(10), 1.3); chips_go("c2", C); pop("#qq", T(20), 0.3); sfx(T(20), "WH-163", -7)
    t0, t1 = T(26), T(50); C = [("calendar", "نهار فالأسبوع", T(33)), ("clock", "ساعة", T(35)), ("target", "الموضوع", T(43)), ("spark", "الهدف", T(45)), ("eye", "فين غادي يتنشر", T(47))]
    grp("g3", t0, t1, ph("p2", t0, t1) + title("cc", 790, "content <b>calendar</b>") + chips("c3", 950, C)); slam("#cc", T(28), 1.3); chips_go("c3", C); sfx(T(28), "IM-003", -7)
    t0, t1 = T(50), T(65); C = [("video", "دفعة وحدة", T(56)), ("clock", "كيوفر الوقت", T(61))]
    grp("g4", t0, t1, ph("p3", t0, t1) + title("bc", 790, "<b>batching</b>") + chips("c4", 950, C)); slam("#bc", T(58), 1.3); chips_go("c4", C); sfx(T(58), "IM-003", -7)
    t0, t1 = T(65), T(81); C = [("calendar", "برمج البوستات", T(66)), ("msg", "الكليان والميساجات", T(71))]
    grp("g5", t0, t1, ph("p4", t0, t1) + chips("c5", 790, C) + title("ct", 960, "الاستمرارية كتبني <b>الثقة</b>")); chips_go("c5", C); rise("#ct", T(73), 40)
    t0, t1 = T(81), T(89)
    grp("g6", t0, t1, kcard("k1", 560, 420, "calendar", "كل نهار", "ماشي ضروري") + kcard("k2", 90, 420, "check", "بانتظام", "<b>المهم</b>", True))
    slide("#k1", T(81), 160); strike("#k1x", T(83)); dim("#k1", T(83) + 0.2, .45); slide("#k2", T(86), -160); glow("#k2", T(87))
    sfx(T(83), "WH-163", -6); sfx(T(86), "IM-003", -6)
    endcard(T(89), "calendar", "كيفاش <b>تنظم الشهر</b> كامل")
    return autocaps()
SPEC["04"] = video04

def video05():
    hook(T(9), pill("pl", 840, "spark", "أقوى من أي إشهار", True) + pill("pf", 1000, "x", "وما كيخلصكش"))
    pop("#pl", T(3), 0.4); slam("#pf", T(7)); sfx(T(3), "PO-013", -6); sfx(T(7), "IM-003", -6)
    t0, t1 = T(9), T(31)
    grp("g2", t0, t1, ph("p2", t0, t1, 460) + qc("q1", 750, '"الخدمة ديالي مزيانة"') + qc("q2", 980, "ملي كليان كيقولها، الناس <b>كيتيقو</b>", True))
    rise("#q1", T(14), 50); dim("#q1", T(22), .45); rise("#q2", T(26), 50); glow("#q2", T(29)); sfx(T(22), "WH-163", -7); sfx(T(26), "IM-003", -7)
    t0, t1 = T(31), T(50); C = [("msg", "رأي قصير", T(40)), ("mic", "صوت", T(42)), ("video", "فيديو بالتليفون", T(44)), ("repeat", "قبل وبعد", T(47))]
    grp("g3", t0, t1, ph("p3", t0, t1) + title("kt", 790, "كل كليان فرحان = <b>محتوى</b>") + chips("c3", 950, C)); rise("#kt", T(33), 40); chips_go("c3", C)
    t0, t1 = T(50), T(73); C = [("heart", "ردة الفعل", T(51)), ("image", "screenshot", T(63))]
    grp("g4", t0, t1, ph("p4", t0, t1) + chips("c4", 790, C) + title("sp", 960, "social <b>proof</b>")); chips_go("c4", C); slam("#sp", T(69), 1.3); sfx(T(69), "IM-003", -6)
    t0, t1 = T(73), T(84)
    grp("g5", t0, t1, qc("q5", 330, "ما تخترعش شهادة") +
        '<div id="o1" class="orb solid" style="left:610px;top:640px"><div class="on1">1</div><div class="ol">حقيقية</div></div>'
        '<div id="gt" class="tline" style="left:470px;right:auto;width:140px;top:710px"><b>&gt;</b></div>'
        '<div id="o2" class="orb hollow" style="left:90px;top:620px"><div class="on1">10</div><div class="ol">مصنوعين</div></div>')
    rise("#q5", T(74), 50); pop("#o1", T(78), 0.3); slam("#gt", T(80), 2); pop("#o2", T(82), 0.3)
    tw(f"tl.to('#o1',{{y:-30,boxShadow:'0 0 90px rgba(91,43,224,.75)',duration:.6}},{T(83):.3f});"); sfx(T(78), "PO-013", -6); sfx(T(80), "IM-003", -6)
    t0, t1 = T(84), T(94); C = [("msg", "صيفط لآخر كليان فرحان", T(86)), ("spark", "جوج كلمات", T(92))]
    grp("g6", t0, t1, title("by", 380, "ابدا <b>اليوم</b>", False) + chips("c6", 660, C)); slam("#by", T(84), 1.3); chips_go("c6", C)
    endcard(T(94), "star", "أفكار ماركوتينغ <b>اللي كتخدم</b>")
    return autocaps()
SPEC["05"] = video05

def video06():
    hook(T(9), pill("pl", 840, "spark", "كيتفكرو القصة", True)); pop("#pl", T(7), 0.4); sfx(T(7), "IM-003", -6)
    t0, t1 = T(9), T(33)
    grp("g2", t0, t1, ph("p2", t0, t1, 460) + qc("q1", 750, '"عندنا جودة عالية وثمن مناسب"') + qc("q2", 960, '"بديت هاد المشروع فالكوزينة ديال الدار…"', True))
    rise("#q1", T(9), 50); strike("#q1x", T(14)); dim("#q1", T(14) + 0.2, .45); rise("#q2", T(17), 50); glow("#q2", T(30))
    sfx(T(14), "WH-163", -6); sfx(T(30), "IM-003", -7)
    t0, t1 = T(33), T(56); S = [("المشكل", T(38)), ("اللحظة", T(45)), ("النتيجة", T(51))]
    grp("g3", t0, t1, title("m3", 330, "القصة الزوينة: <b>3</b> مراحل") + steps("s3", 560, S, 170)); rise("#m3", T(33), 40); steps_go("s3", S)
    t0, t1 = T(56), T(73); C = [("user", "قصة البداية ديالك", T(63)), ("users", "قصة كليان", T(66)), ("gift", "قصة منتوج", T(70))]
    grp("g4", t0, t1, ph("p3", t0, t1) + title("st", 790, "<b>storytelling</b>") + chips("c4", 950, C)); slam("#st", T(57), 1.3); chips_go("c4", C); sfx(T(57), "IM-003", -6)
    t0, t1 = T(73), T(80)
    grp("g5", t0, t1, bigic("ck", 330, "check") + title("hq", 620, "خاصها تكون <b>حقيقية</b>", False) + pill("kd", 1000, "x", "الناس كيحسو بالكذب"))
    pop("#ck", T(73), 0.3); rise("#hq", T(74), 40); slam("#kd", T(77)); sfx(T(77), "IM-003", -6)
    t0, t1 = T(80), T(87)
    grp("g6", t0, t1, ph("p4", t0, t1, 460) + kcard("k1", 560, 760, "gift", "ما تبداش", "بالمنتوج") + kcard("k2", 90, 760, "user", "بدا", "<b>بالإنسان</b>", True))
    slide("#k1", T(82), 160); dim("#k1", T(85), .45); slide("#k2", T(85), -160); glow("#k2", T(86)); sfx(T(85), "IM-003", -6)
    endcard(T(87), "user", "كيفاش <b>تحكي القصة</b> ديال المشروع ديالك")
    return autocaps()
SPEC["06"] = video06

def video07():
    hook(T(12), pill("pl", 840, "clock", "من بعد يومين؟")); slam("#pl", T(8)); sfx(T(8), "IM-003", -5)
    t0, t1 = T(12), T(30)
    grp("g2", t0, t1, ph("p2", t0, t1) + avrow("av", 790, 3, "briefcase") + title("fs", 960, "اللي جاوب <b>اللول</b> هو اللي كيبيع"))
    for i, k in enumerate((18, 19, 21)): pop(f"#av{i}", T(k), 0.3, 0.45); sfx(T(k), "PO-013", -9)
    rise("#fs", T(23), 40); sfx(T(23), "IM-003", -7)
    t0, t1 = T(30), T(40)
    grp("g3", t0, t1, bigic("mi", 330, "msg") + title("js", 620, "ماشي خدمة <b>جانبية</b>", False) + pill("lr", 960, "target", "المرحلة اللخرة قبل البيع", True))
    pop("#mi", T(30), 0.3); rise("#js", T(32), 40); pop("#lr", T(35), 0.4); sfx(T(35), "IM-003", -7)
    t0, t1 = T(40), T(62); S = [("جاوب بسرعة", T(43)), ("وجّد أجوبة", T(53))]; C = [("cart", "الثمن", T(58)), ("gift", "التوصيل", T(59)), ("check", "كيفاش نخلص", T(60))]
    grp("g4", t0, t1, ph("p3", t0, t1, 420) + steps("s4", 700, S) + chips("c4", 1020, C)); steps_go("s4", S); chips_go("c4", C)
    t0, t1 = T(62), T(71)
    grp("g5", t0, t1, title("sq", 380, "<b>3</b> · سالي بسؤال", False) + qc("qf", 650, '"بغيتي نوصلوها ليك فين؟"', True) + pill("kb", 950, "cart", "كتقرّب البيع", True))
    slam("#sq", T(62), 1.3); rise("#qf", T(65), 50); pop("#kb", T(69), 0.4); sfx(T(65), "PO-013", -6)
    t0, t1 = T(71), T(92); C = [("msg", "جاوب بأدب", T(72)), ("eye", "الناس كيشوفو", T(79))]
    grp("g6", t0, t1, ph("p4", t0, t1) + chips("c6", 790, C) + title("cm", 960, "community <b>management</b>")); chips_go("c6", C); slam("#cm", T(85), 1.3); sfx(T(85), "IM-003", -6)
    endcard(T(92), "msg", "تسيّر الصفحة ديالك <b>بحال المحترفين</b>")
    return autocaps()
SPEC["07"] = video07

def video08():
    hook(T(10), pill("pl", 840, "clock", "ما عندكش الوقت؟")); slam("#pl", T(1)); sfx(T(1), "IM-003", -5)
    t0, t1 = T(10), T(22); C = [("video", "فيديو واحد طويل", T(14)), ("mic", "شرح ولا لايف", T(18))]
    grp("g2", t0, t1, ph("p2", t0, t1) + title("uo", 790, "تستعمل <b>اللي عندك</b>") + chips("c2", 950, C)); rise("#uo", T(10), 40); chips_go("c2", C)
    t0, t1 = T(22), T(52)
    C = [("video", "ريلز قصار", T(27)), ("image", "كاروسيل", T(36)), ("text", "بوست كتابة", T(38)), ("mic", "بودكاست", T(43)), ("q", "كل سؤال فيديو جديد", T(48))]
    grp("g3", t0, t1, ph("p3", t0, t1, 420) + chips("c3", 720, C)); chips_go("c3", C)
    t0, t1 = T(52), T(68)
    grp("g4", t0, t1, title("rp", 330, "<b>repurposing</b>", False) + chips("c4", 520, [("spark", "story + sondage", T(55))]) +
        kcard("k1", 560, 700, "video", "كتصاوب", "مرة") + kcard("k2", 90, 700, "repeat", "كتنشر", "<b>فبلايص مختلفين</b>", True))
    chips_go("c4", [("", "", T(55))]); slam("#rp", T(58), 1.3); slide("#k1", T(61), 160); slide("#k2", T(63), -160); glow("#k2", T(65)); sfx(T(58), "IM-003", -6)
    t0, t1 = T(68), T(78)
    grp("g5", t0, t1, title("nk", 360, "الناس ما كيشوفوش <b>كلشي</b>") + kcard("k3", 560, 560, "eye", "شاف", "الريل", True, False) + kcard("k4", 90, 560, "image", "ما شافش", "الكاروسيل", False, False))
    rise("#nk", T(68), 40); slide("#k3", T(73), 160); slide("#k4", T(76), -160); dim("#k4", T(77), .45); sfx(T(73), "WH-012", -6)
    t0, t1 = T(78), T(91); C = [("video", "آخر فيديو صاوبتي", T(82)), ("spark", "جوج حوايج جداد", T(88))]
    grp("g6", t0, t1, ph("p4", t0, t1) + title("jr", 790, "جرب هاد <b>الأسبوع</b>") + chips("c6", 950, C)); rise("#jr", T(78), 40); chips_go("c6", C)
    endcard(T(91), "repeat", "أفكار عملية <b>كل أسبوع</b>")
    return autocaps()
SPEC["08"] = video08

def video09():
    hook(T(7), pill("pl", 840, "heart", "likes", True) + pill("pk", 1000, "q", "واش كيخلصو الكرا؟"))
    pop("#pl", T(1), 0.4); slam("#pk", T(4)); sfx(T(1), "PO-013", -6); sfx(T(4), "IM-003", -5)
    t0, t1 = T(7), T(28); C = [("heart", "likes", T(15)), ("eye", "vues", T(16)), ("users", "فولوورز", T(17))]
    grp("g2", t0, t1, ph("p2", t0, t1) + chips("c2", 790, C) + title("vm", 960, "vanity <b>metrics</b>")); chips_go("c2", C); slam("#vm", T(20), 1.3)
    dim("#c2", T(25), .5); sfx(T(20), "IM-003", -6)
    t0, t1 = T(28), T(61); S = [("صيفط ليك ميساج", T(36)), ("دخل للموقع ولا الواتساب", T(42)), ("شرا فعلا", T(49)), ("رجع شرا مرة أخرى", T(54))]
    grp("g3", t0, t1, ph("p3", t0, t1, 400) + steps("s3", 680, S, 140)); steps_go("s3", S)
    t0, t1 = T(61), T(77)
    grp("g4", t0, t1, title("lq", 330, "likes <b>قلال</b>…") +
        '<div id="o1" class="orb solid" style="left:610px;top:620px"><div class="on1">2</div><div class="ol">كليان</div></div>'
        '<div id="gt" class="tline" style="left:470px;right:auto;width:140px;top:690px"><b>&gt;</b></div>'
        '<div id="o2" class="orb hollow" style="left:90px;top:600px"><div class="ol">فيروسي</div><div class="on1" style="font-family:GA">والو</div></div>')
    rise("#lq", T(61), 40); pop("#o1", T(66), 0.3); slam("#gt", T(70), 2); pop("#o2", T(72), 0.3)
    tw(f"tl.to('#o2',{{opacity:.4,y:50,duration:.6}},{T(75):.3f});"); sfx(T(66), "PO-013", -6); sfx(T(70), "IM-003", -6)
    t0, t1 = T(77), T(95); C = [("msg", "ميساجات", T(85)), ("cart", "مبيعات", T(86))]
    grp("g5", t0, t1, ph("p4", t0, t1) + chips("c5", 790, C) + title("km", 960, "صاوب منهم <b>كثر</b>")); chips_go("c5", C); slam("#km", T(87), 1.3); sfx(T(87), "IM-003", -6)
    endcard(T(95), "chart", "تعرف <b>تقرا الأرقام</b> ديالك")
    return autocaps()
SPEC["09"] = video09

def video10():
    hook(T(13), pill("pl", 840, "user", "ما فيها حتى وجه") + pill("pq", 1000, "q", "علاش ما كيتيقوش؟", True))
    slam("#pl", T(4)); pop("#pq", T(9), 0.4); sfx(T(4), "IM-003", -5); sfx(T(9), "PO-013", -7)
    t0, t1 = T(13), T(21)
    grp("g2", t0, t1, kcard("k1", 560, 420, "image", "لوغو", "ما كيرتابطوش") + kcard("k2", 90, 420, "user", "إنسان", "<b>كيرتابطو</b>", True))
    slide("#k1", T(13), 160); strike("#k1x", T(17)); dim("#k1", T(17) + 0.2, .45); slide("#k2", T(18), -160); glow("#k2", T(19)); sfx(T(18), "IM-003", -6)
    t0, t1 = T(21), T(38); C = [("mic", "كيهضر", T(25)), ("book", "كيشرح", T(26)), ("heart", "كيضحك", T(27)), ("check", "كيعترف بغلطة", T(28))]
    grp("g3", t0, t1, ph("p2", t0, t1) + chips("c3", 790, C) + title("hq", 1060, "شي حد <b>حقيقي</b>")); chips_go("c3", C); rise("#hq", T(30), 40)
    t0, t1 = T(38), T(46)
    grp("g4", t0, t1, title("pb", 400, "personal <b>branding</b>", False) + pill("mt", 760, "x", "ماشي ضروري تولي مؤثر"))
    slam("#pb", T(38), 1.3); slam("#mt", T(42)); sfx(T(38), "IM-003", -6)
    t0, t1 = T(46), T(65); S = [("فيديو قصير: علاش بديتي", T(49)), ("كواليس الخدمة", T(55)), ("رأيك فالمجال ديالك", T(59))]
    grp("g5", t0, t1, ph("p3", t0, t1, 420) + steps("s5", 700, S)); steps_go("s5", S)
    t0, t1 = T(65), T(84); C = [("x", "كاميرا غالية", T(67)), ("x", "كلام مثالي", T(70))]
    grp("g6", t0, t1, ph("p4", t0, t1) + chips("c6", 790, C) + title("ws", 960, "<b>واضح</b> و<b>صادق</b>")); chips_go("c6", C); dim("#c6", T(72), .45)
    slam("#ws", T(74), 1.3); sfx(T(74), "IM-003", -6)
    t0, t1 = T(84), T(93)
    grp("g7", t0, t1, bigic("vd", 330, "video", 240) + title("fv", 680, "فيديو وحد، <b>أنت فيه</b>", False) + pill("sf", 1000, "eye", "وشوف الفرق", True))
    pop("#vd", T(84), 0.3); rise("#fv", T(87), 40); pop("#sf", T(91), 0.4); sfx(T(91), "PO-013", -7)
    endcard(T(93), "user", "نبنيو مع بعض <b>البراند ديالك</b>")
    return autocaps()
SPEC["10"] = video10
CAPS = SPEC[NN]()

def clean(w):
    w = w.strip('"“”«»:').replace("…", "")
    return w.rstrip("؟،.") if w.isascii() or w.rstrip("؟،.").isascii() else w     # no RTL punctuation stuck to Latin words
for k, (a, b, acc) in enumerate(CAPS):
    st = T(a); en = T(CAPS[k + 1][0]) - 0.05 if k + 1 < len(CAPS) else VOICE_END
    ws = [clean(x[2]) for x in W[a:b]]
    sp = "".join(f'<span id="c{k}_{i}" class="cw{" acc" if i == acc else ""}">{w}</span> ' for i, w in enumerate(ws))
    h(f'<div id="cap{k}" class="cap">{sp}</div>')
    tw(f"tl.set('#cap{k}',{{autoAlpha:1}},{st:.3f});tl.set('#cap{k}',{{autoAlpha:0}},{en:.3f});")
    tw(f"tl.fromTo('#cap{k}',{{y:22}},{{y:0,duration:.3,ease:'expo.out'}},{st:.3f});")
    for i in range(len(ws)):                       # each word lights on its spoken time
        tw(f"tl.fromTo('#c{k}_{i}',{{opacity:.35}},{{opacity:1,duration:.1}},{T(a + i):.3f});")
    tw(f"tl.fromTo('#c{k}_{acc}',{{scale:.8,backgroundColor:'rgba(91,43,224,0)',color:'{INK}'}},"
       f"{{scale:1,backgroundColor:'rgba(91,43,224,1)',color:'#fff',duration:.3,ease:'back.out(2.5)'}},{T(a + acc):.3f});")

CSS = f"""
@font-face{{font-family:GA;src:url(assets/fonts/GraphikArabic-Medium.woff2);font-weight:500}}
@font-face{{font-family:GA;src:url(assets/fonts/GraphikArabic-Bold.woff2);font-weight:700}}
@font-face{{font-family:GA;src:url(assets/fonts/GraphikArabic-Black.woff2);font-weight:900}}
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#fff;font-family:GA,'Avenir Next',sans-serif;color:{INK}}}
#root{{position:absolute;inset:0;overflow:hidden;background:linear-gradient(180deg,#FFFFFF 0%,#F7F4FF 100%)}}
#dots{{position:absolute;inset:0;opacity:.5;background-image:radial-gradient(rgba(91,43,224,.18) 2px,transparent 2px);background-size:54px 54px}}
#blob1{{position:absolute;left:-220px;top:-200px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(139,92,246,.20),rgba(139,92,246,0) 70%)}}
#blob2{{position:absolute;right:-260px;bottom:180px;width:760px;height:760px;border-radius:50%;background:radial-gradient(circle,rgba(91,43,224,.14),rgba(91,43,224,0) 70%)}}
#brand{{position:absolute;top:120px;left:0;right:0;text-align:center;font-family:'Avenir Next';font-weight:700;letter-spacing:8px;font-size:26px;color:{P};opacity:.75}}
.grp{{position:absolute;inset:0;visibility:hidden}}
.grp>div,.grp>svg{{position:absolute}}
.ph{{border-radius:44px;overflow:hidden;background:#EEE9FB;box-shadow:0 30px 70px rgba(20,15,46,.18),0 0 0 6px #fff}}
.ph img,.ph video{{width:100%;height:100%;object-fit:cover;display:block;transform-origin:50% 50%}}
.card{{border-radius:40px;background:#fff;border:2px solid #E6DEFF;box-shadow:0 20px 50px rgba(91,43,224,.15)}}
.stat{{display:flex;align-items:center;gap:40px;padding:0 50px;box-sizing:border-box;direction:rtl}}
.sic{{width:140px;height:140px;border-radius:50%;background:#F1ECFF;display:flex;align-items:center;justify-content:center}}
.big{{font-family:'Avenir Next';font-weight:800;font-size:116px;line-height:1;color:{INK};direction:ltr}}
.lbl{{font-weight:700;font-size:44px;color:{P};margin-top:6px}}
.redpill{{display:flex;align-items:center;gap:18px;padding:20px 46px;border-radius:80px;background:#FF4D6D;color:#fff;box-shadow:0 18px 50px rgba(255,77,109,.4);
  font-weight:900;font-size:52px;white-space:nowrap;direction:rtl}}
.redpill.vio{{background:{P};box-shadow:0 18px 50px rgba(91,43,224,.45)}}
.ico{{width:300px;height:280px;display:flex;align-items:center;justify-content:center}}
.xline{{position:absolute;left:-4%;top:48%;width:108%;height:12px;border-radius:8px;background:#FF4D6D;transform-origin:100% 50%;transform:scaleX(0) rotate(-8deg)}}
.tline{{left:60px;right:60px;text-align:center;direction:rtl;font-weight:900;font-size:110px;line-height:1.2;color:{INK}}}
.tline.sm{{font-size:76px}}
.tline b{{color:{P}}}
.arow{{left:0;right:0;display:flex;justify-content:center;gap:26px}}
.av{{width:120px;height:120px;border-radius:50%;background:linear-gradient(160deg,#8B5CF6,{P});display:flex;align-items:center;justify-content:center;box-shadow:0 12px 30px rgba(91,43,224,.3)}}
.chip{{display:flex;align-items:center;gap:16px;padding:20px 36px;border-radius:70px;background:#fff;border:2px solid #E6DEFF;
  box-shadow:0 14px 36px rgba(91,43,224,.18);font-weight:700;font-size:50px;white-space:nowrap;direction:rtl}}
.crowd{{width:800px;display:grid;grid-template-columns:repeat(10,1fr);gap:30px 0;justify-items:center}}
.dot{{display:block;width:50px;height:50px;border-radius:50%;background:#C9BCEF}}
.qcard{{position:absolute;padding:44px 140px 44px 50px;box-sizing:border-box;border-radius:40px;background:#fff;border:2px solid #E6DEFF;direction:rtl;
  font-weight:700;font-size:60px;line-height:1.35;box-shadow:0 20px 50px rgba(91,43,224,.12)}}
.qcard.ok{{background:{P};color:#fff;border-color:{P}}}
.qcard b{{color:#FFD43B}}
.qn{{position:absolute;right:40px;top:48px;width:72px;height:72px;border-radius:50%;background:#FF4D6D;color:#fff;display:flex;align-items:center;justify-content:center;font-size:42px;font-family:'Avenir Next'}}
.qn.y{{background:#22C58B}}
.orb{{border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.orb.solid{{width:380px;height:380px;background:radial-gradient(circle at 35% 30%,#A98BFF,{P} 65%);color:#fff;box-shadow:0 20px 60px rgba(91,43,224,.45)}}
.orb.hollow{{width:400px;height:400px;border:5px dashed #C9BCEF;background:#fff;color:#8E84AD}}
.on1{{font-family:'Avenir Next';font-weight:800;font-size:96px}}
.ol{{font-weight:700;font-size:48px}}
.tog{{width:400px;height:150px;border-radius:80px;display:flex;align-items:center;justify-content:center;gap:20px;background:#fff;direction:rtl;
  border:3px solid #E6DEFF;font-weight:900;font-size:56px;box-sizing:border-box;box-shadow:0 14px 36px rgba(91,43,224,.15)}}
.kc{{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}}
.kc.hi{{background:{P};border-color:{P};color:#fff}}
.kic{{width:150px;height:150px;border-radius:50%;background:#F1ECFF;display:flex;align-items:center;justify-content:center}}
.kc.hi .kic{{background:rgba(255,255,255,.18)}}
.kt{{font-weight:900;font-size:58px}} .kt b{{color:#FFD43B}}
.ka{{font-size:46px;opacity:.6}}
.wm{{left:0;right:0;text-align:center;font-family:'Avenir Next';font-weight:800;letter-spacing:12px;font-size:62px;color:{P}}}
.grp>div.ctr{{left:0;right:0;margin:0 auto;width:fit-content}}
.crow{{left:50px;right:50px;display:flex;flex-wrap:wrap;justify-content:center;gap:22px 24px;direction:rtl}}
.step{{left:90px;width:900px;box-sizing:border-box;display:flex;align-items:center;gap:28px;padding:22px 34px;border-radius:34px;background:#fff;
  border:2px solid #E6DEFF;box-shadow:0 14px 36px rgba(91,43,224,.14);direction:rtl;font-weight:900;font-size:54px}}
.sn{{flex:none;width:84px;height:84px;border-radius:50%;background:{P};color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Avenir Next';font-weight:800;font-size:46px}}
.cap{{position:absolute;left:70px;right:70px;top:1360px;text-align:center;direction:rtl;font-weight:900;font-size:76px;line-height:1.45;color:{INK};visibility:hidden}}
.cap .cw{{display:inline-block}}
.cap .acc{{padding:0 18px;border-radius:18px}}
"""
html = f"""<!doctype html>
<html lang="ar"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <div id="dots"></div><div id="blob1"></div><div id="blob2"></div><div id="brand">ORANUSS ACADEMY</div>
  {chr(10).join("  " + x for x in H)}
  <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-volume="1"></audio>
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  tl.fromTo('#blob1',{{x:0,y:0}},{{x:120,y:80,duration:{TOTAL / 2:.2f},yoyo:true,repeat:1,ease:'sine.inOut'}},0);
  tl.fromTo('#blob2',{{x:0,y:0}},{{x:-100,y:-120,duration:{TOTAL / 2:.2f},yoyo:true,repeat:1,ease:'sine.inOut'}},0);
  {chr(10).join("  " + x for x in J)}
  tl.to({{}},{{duration:0.001}},{TOTAL - 0.01});
  window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>"""
open(os.path.join(PROJ, "index.html"), "w", encoding="utf-8").write(html)
for f in ("hyperframes.json", "package.json"):
    shutil.copy(os.path.join(HERE, "leverage", f), os.path.join(PROJ, f))
json.dump({"total": TOTAL, "voice": os.path.join(SRC, "voice.mp3"), "music": os.path.join(SRC, "music.mp3"), "cues": sorted(CUES)},
          open(os.path.join(WK, "sfx_cues.json"), "w"))
print(f"smm{NN}: total {TOTAL}s · caps {len(CAPS)} · sfx {len(CUES)}")
