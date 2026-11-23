# Developed by Mehdi ORANUSS | Powered by Claude
"""Short #1 v4 «واش أي واحد يقدر يكون مقاول؟» (9:16, ≈59 s) from the entrepreneur podcast.
Story: question → «لا» → why most fail (stress, results vs action) → input/output → dream at night, work by day
→ 3-step recipe (start now, patience in one field, sell what clients rebuy) → problems + team → «مع السنوات غادي تمشي مزيان».
Layouts: FACE (full footage, face centred by macOS Vision) · SPLIT (green animation stage on top, face below)
· MEDIA (Pinterest photo, full-frame or framed) · TEXT (full-screen kinetic words).
Target mix (user, v2): animation ≈40 %, photos ≈30 %, text ≈10 %, faces the rest (+ face visible under every SPLIT).
usage: python3 -I gen_entrepreneur1_v2.py [--media]"""
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "entrepreneur1-v4")
AS = os.path.join(PROJ, "assets")
TOP = os.path.abspath(os.path.join(HERE, "..", ".."))
WK = os.path.join(TOP, "project", "work", "ytsave-entrepreneur")
PIN = os.path.join(TOP, "output", "ytsave-entrepreneur", "assets", "pinterest")
SRC = os.path.join(WK, "src.mp4")
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
END_HOLD = 2.6

# (src_start, src_end, layout, beat, caption chunks [(text, accent word index)])
SEGS = [   # v3: whole sentences only, repeats removed (user: concise but complete, ideas must connect)
    (191.40, 195.95, "face", "q", [("ولكن واش بالصح", 2), ("أي واحد يقدر", 1)]),
    (195.95, 197.10, "text", "no", [("يكون مقاول؟", 1)]),
    (198.62, 202.65, "face", "a1", [("ممكن ينجحو الناس", 1), ("ولكن ماشي أي واحد", 2), ("ممكن يكون مقاول", 2)]),
    (202.85, 205.30, "media", "training", [("بزاف ديال الناس اللي دربتهم", 4), ("خلال هاد السنوات", 2)]),
    (205.30, 208.60, "face", "a1b", [("اكتشفت أنه…", 0), ("كيديروها ولكن ماكينجحوش فيها", 2)]),
    (211.20, 213.50, "media", "stress", [("ماكيتحملوش داك الستريس", 2)]),
    (213.50, 215.95, "split", "gauge", [("وداك الضغط", 1), ("اللي كيكون فالمقاولة", 2), ("فبعض الأحيان", 1)]),
    (219.35, 222.30, "text", "result", [("واجدين للنتيجة", 1), ("ولكن ماواجدينش للفعل", 2)]),
    (222.60, 227.05, "split", "io0", [("يعني كاين الإنبوت", 2), ("وكاين الأوتبوت", 1), ("الإنبوت شنو كندير", 0), ("والنتيجة شنو كناخد", 0)]),
    (227.05, 230.50, "media", "buy", [("ناخدو الفلوس", 1), ("ونشريو الطوموبيل", 1), ("ونشريو الدار", 1)]),
    (237.60, 243.60, "split", "io", [("والمقاول هو داك الشخص", 0), ("اللي كيركز على الفعل", 3), ("والنتيجة كتجي من بعد", 0)]),
    (247.95, 250.95, "face", "a2", [("كتحلم بالأوتبوت", 1), ("ولكن ماكديرش الإنبوت", 2)]),
    (251.60, 254.70, "media", "night", [("يعني أنا كنقول للناس", 3), ("ديما حلموها بالليل", 2)]),
    (258.90, 262.45, "split", "nightday", [("حلم بالليل وخدم بالنهار", 3), ("باش توصل للشي", 2), ("اللي حلمتي بيه البارح", 3)]),
    (271.55, 277.05, "split", "steps12", [("بدا فأقرب وقت ممكن", 1), ("والصبر لمدة ديال سنوات", 3), ("فحاجة وحدة فمجال واحد", 1)]),
    (278.65, 283.20, "split", "step3", [("وبيع شي حاجة", 1), ("اللي الكليان", 1), ("غيعاود يشريها", 0), ("من عندك", 1)]),
    (285.15, 288.05, "media", "climb", [("وراه غادي يطلعو المشاكل", 3), ("وغادي يخصك تجاوز المشاكل", 2)]),
    (289.55, 292.95, "media", "team", [("وغادي دير فريق", 2), ("غادي ترتاح تخدم معاهم", 1), ("ويرتاحو يخدمو معاك", 1)]),
    (292.95, 294.30, "face", "a3", [("مع السنوات غادي تمشي مزيان", 4)]),
]
OUTS, t = [], 0.0
for a, b, *_ in SEGS:
    OUTS.append((round(t, 3), round(t + b - a, 3))); t += b - a
VOICE_END = round(t, 3)
TOTAL = round(t + END_HOLD, 3)

IMGS = {"training": "04-training", "stress": "05-stress", "money": "07a-money", "car": "07b-car", "house": "07c-house",
        "night": "10-night", "climb": "15-obstacles", "team": "16-team"}
FRAMED = {"training", "stress"}          # low-res landscape sources: shown in a glass frame, not full-frame

def build_media():
    os.makedirs(os.path.join(AS, "img"), exist_ok=True)
    faces = json.load(open(os.path.join(WK, "faces.json")))
    tmp = os.path.join(WK, "seg4"); os.makedirs(tmp, exist_ok=True)
    lst = []
    for k, (a, b, *_r) in enumerate(SEGS):
        near = sorted(f["x"] + f["w"] / 2 for f in faces if a <= f["t"] <= b)
        x = int(min(max(near[len(near) // 2] - 304, 0), 1920 - 608))
        p = os.path.join(tmp, f"v{k:02d}.mp4")
        subprocess.run([FF, "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", SRC,
                        "-vf", f"crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,eq=contrast=1.06:saturation=1.04,fps=30,setsar=1",
                        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", p], check=True)
        lst.append(p)
    open(os.path.join(tmp, "list.txt"), "w").write("".join(f"file '{p}'\n" for p in lst))
    subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"),
                    "-vf", f"tpad=stop_mode=clone:stop_duration={END_HOLD}", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "16", "-pix_fmt", "yuv420p", os.path.join(AS, "aroll.mp4")], check=True)
    fl, parts = [], ""
    for k, (a, b, *_r) in enumerate(SEGS):
        fl.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={b - a - 0.03:.3f}:d=0.03[a{k}]")
        parts += f"[a{k}]"
    fl.append(parts + f"concat=n={len(SEGS)}:v=0:a=1[out]")
    subprocess.run([FF, "-v", "error", "-y", "-i", SRC, "-filter_complex", ";".join(fl), "-map", "[out]",
                    "-ar", "48000", "-ac", "1", os.path.join(WK, "voice_v4_raw.wav")], check=True)
    for key, beat in IMGS.items():
        shutil.copy(os.path.join(PIN, "bg", f"{beat}.jpg"), os.path.join(AS, "img", f"{key}.jpg"))
        raw = os.path.join(WK, "pins", f"raw_{beat}.jpg")
        if key in FRAMED:
            subprocess.run([FF, "-v", "error", "-y", "-i", raw, "-vf", "scale=1200:-2:flags=lanczos", "-q:v", "2",
                            os.path.join(AS, "img", f"{key}_wide.jpg")], check=True)
    os.makedirs(os.path.join(AS, "fonts"), exist_ok=True)
    for w in ("Bold", "Black", "Medium"):
        shutil.copy(os.path.join(HERE, "1112/assets/fonts", f"GraphikArabic-{w}.woff2"), os.path.join(AS, "fonts"))
    print("media ok")

if "--media" in sys.argv:
    build_media()

# ---------------- timeline helpers ----------------
H, J, CUES = [], [], []
def h(s): H.append(s)
def tw(s): J.append(s)
def sfx(t, sid, extra=0, trim=None): CUES.append((round(max(t, 0), 3), sid, "peak", extra, trim))
def grp(gid, t0, t1, inner, cls="grp"):
    h(f'<div id="{gid}" class="{cls}">{inner}</div>')
    tw(f"tl.set('#{gid}',{{autoAlpha:1}},{t0:.3f});tl.to('#{gid}',{{autoAlpha:0,duration:.18}},{t1 - 0.18:.3f});")
def rise(sel, t, dy=60, d=0.5):
    tw(f"tl.fromTo('{sel}',{{y:{dy},opacity:0,filter:'blur(10px)'}},{{y:0,opacity:1,filter:'blur(0px)',duration:{d},ease:'expo.out'}},{t:.3f});")
def pop(sel, t, s0=0.4, d=0.5):
    tw(f"tl.fromTo('{sel}',{{scale:{s0},opacity:0}},{{scale:1,opacity:1,duration:{d},ease:'back.out(1.8)'}},{t:.3f});")
def slam(sel, t, s0=1.8):
    tw(f"tl.fromTo('{sel}',{{scale:{s0},opacity:0,filter:'blur(16px)'}},{{scale:1,opacity:1,filter:'blur(0px)',duration:.38,ease:'expo.out'}},{t:.3f});")

IC = {
    "hammer": '<path d="M14 6l4 4M5 19l8.5-8.5M12 4l6 6 2-2-6-6z"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>',
    "car": '<path d="M3 13l2-5h14l2 5v5H3z"/><circle cx="7.5" cy="17" r="1.6"/><circle cx="16.5" cy="17" r="1.6"/>',
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "cash": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
    "moon": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    "sun": '<circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "play": '<path d="M8 5l11 7-11 7z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "repeat": '<path d="M17 2l4 4-4 4"/><path d="M3 11V9a3 3 0 0 1 3-3h15"/><path d="M7 22l-4-4 4-4"/><path d="M21 13v2a3 3 0 0 1-3 3H3"/>',
}
def svg(name, size=80, sw=2.0, color="#fff"):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{IC[name]}</svg>')

PILL = ''   # v4: the chapter tracker replaces the title pill

# ---------------- layout state per beat ----------------
CLIP = {"face": "inset(0px 0px 1920px 0px)", "split": "inset(0px 0px 930px 0px)", "text": "inset(0px 0px 0px 0px)",
        "media": "inset(0px 0px 0px 0px)"}
CAMY = {"face": 0, "split": 520, "text": 0, "media": 0}
CAPY = {"face": 1300, "split": 850, "text": 1300, "media": 1330}
prev = None
for k, (a, b, lay, beat, caps) in enumerate(SEGS):
    t0, t1 = OUTS[k]
    if lay != prev:
        d = 0.0 if k == 0 else 0.4
        tw(f"tl.to('#stage',{{clipPath:'{CLIP[lay]}',duration:{d},ease:'expo.inOut'}},{max(t0 - 0.12, 0):.3f});")
        tw(f"tl.to('#cam',{{y:{CAMY[lay]},duration:{d},ease:'expo.inOut'}},{max(t0 - 0.12, 0):.3f});")
        if k:
            sfx(t0, "WH-163" if lay in ("media", "text") else "WH-012", -3)
    if lay in ("face", "split"):
        tw(f"tl.fromTo('#camv',{{filter:'blur(12px)'}},{{filter:'blur(0px)',duration:.3,ease:'power2.out',immediateRender:false}},{t0:.3f});")
        z0, z1 = (1.0, 1.08) if k % 2 == 0 else (1.08, 1.0)
        tw(f"tl.fromTo('#camz',{{scale:{z0}}},{{scale:{z1},duration:{t1 - t0:.3f},ease:'sine.inOut',immediateRender:false}},{t0:.3f});")
    prev = lay
tw(f"tl.to('#stage',{{clipPath:'{CLIP['text']}',duration:.4,ease:'expo.inOut'}},{VOICE_END - 0.1:.3f});")
tw(f"tl.to('#cam',{{y:0,duration:.4}},{VOICE_END - 0.1:.3f});")

def media_full(gid, key, t0, t1, dz=0.08):
    h(f'<div id="{gid}" class="media"><img id="{gid}i" src="assets/img/{key}.jpg"/><div class="mshade"></div></div>')
    tw(f"tl.set('#{gid}',{{autoAlpha:1}},{t0:.3f});tl.set('#{gid}',{{autoAlpha:0}},{t1:.3f});")
    tw(f"tl.fromTo('#{gid}i',{{scale:1.18,filter:'blur(18px)'}},{{scale:1.1,filter:'blur(0px)',duration:.35,ease:'expo.out'}},{t0:.3f});")
    tw(f"tl.to('#{gid}i',{{scale:{1.1 - dz:.2f},duration:{max(t1 - t0 - 0.35, 0.1):.3f},ease:'none'}},{t0 + 0.35:.3f});")
def media_framed(gid, key, t0, t1):
    h(f'<div id="{gid}" class="media"><img class="mblur" src="assets/img/{key}.jpg"/>'
      f'<div id="{gid}f" class="frame"><img id="{gid}i" src="assets/img/{key}_wide.jpg"/></div>{PILL}</div>')
    tw(f"tl.set('#{gid}',{{autoAlpha:1}},{t0:.3f});tl.set('#{gid}',{{autoAlpha:0}},{t1:.3f});")
    pop(f"#{gid}f", t0, 0.85, 0.45)
    tw(f"tl.fromTo('#{gid}i',{{scale:1}},{{scale:1.08,duration:{t1 - t0:.3f},ease:'none'}},{t0:.3f});")

BX, BY, BW, BH = 60, 365, 960, 420

CHAPTERS = [("السؤال", 0, 4), ("علاش كيفشلو", 5, 7), ("الفعل والنتيجة", 8, 13), ("الوصفة", 14, 17), ("الخلاصة", 18, 18)]
def chapter_span(c):
    _, i0, i1 = CHAPTERS[c]
    return OUTS[i0][0], (OUTS[i1][1] if c < len(CHAPTERS) - 1 else TOTAL)

segs = "".join(f'<div class="tseg" id="ts{c}"><div class="tbar"><i id="tf{c}"></i></div><div class="tlab" id="tl{c}">'
               f'<b>{c + 1:02d}</b> {name}</div></div>' for c, (name, _, _) in enumerate(CHAPTERS))
h(f'<div id="trk" class="trk">{segs}</div>')
tw("tl.fromTo('#trk',{y:-30,opacity:0},{y:0,opacity:1,duration:.5,ease:'expo.out'},0.15);")
for c in range(len(CHAPTERS)):
    a_, b_ = chapter_span(c)
    tw(f"tl.fromTo('#tf{c}',{{scaleX:0}},{{scaleX:1,duration:{b_ - a_:.3f},ease:'none'}},{a_:.3f});")
    tw(f"tl.to('#tl{c}',{{opacity:1,color:'#ffffff',duration:.25}},{a_:.3f});")
    tw(f"tl.fromTo('#ts{c}',{{scale:1}},{{scale:1.08,duration:.18,yoyo:true,repeat:1,ease:'power2.out'}},{a_:.3f});")
    if c < len(CHAPTERS) - 1:
        tw(f"tl.to('#tl{c}',{{color:'#A7F3D0',opacity:.75,duration:.25}},{b_:.3f});")
    if c:
        sfx(a_, "PO-016", -10)

def board(gid, t0, t1, inner, extra=""):
    """One card on the shared grid; same entrance and exit for every scene."""
    grp(gid, t0, t1, f'<div id="{gid}c" class="board" style="{extra}">{inner}</div>')
    tw(f"tl.fromTo('#{gid}c',{{y:40,opacity:0,scale:.97,filter:'blur(8px)'}},{{y:0,opacity:1,scale:1,filter:'blur(0px)',duration:.5,ease:'expo.out'}},{t0:.3f});")
    tw(f"tl.to('#{gid}c',{{scale:.96,opacity:0,duration:.22,ease:'power2.in'}},{t1 - 0.24:.3f});")

def node(nid, kicker, title, icons, cls=""):
    ic = "".join(f'<span class="nic">{svg(i, 44, 2.2)}</span>' for i in icons)
    return (f'<div class="node {cls}" id="{nid}"><div class="nk">{kicker}</div><div class="nt">{title}</div>'
            f'<div class="nics">{ic}</div></div>')

def flow(prefix):
    # RTL flow: INPUT (right) → OUTPUT (left), dashed path with travelling dots
    dots = "".join(f'<circle class="fdot" r="7" cx="0" cy="0" fill="#2EE59D"/>' for _ in range(3))
    return (node(f"{prefix}in", "INPUT", "شنو كندير", ("hammer", "list"), "in") +
            node(f"{prefix}out", "OUTPUT", "شنو كناخد", ("car", "home", "cash"), "out") +
            f'<svg class="fpath" width="240" height="60" viewBox="0 0 240 60"><path id="{prefix}p" d="M230 30H10" stroke="#2EE59D" '
            f'stroke-width="4" stroke-dasharray="10 12" fill="none" opacity=".7"/>'
            f'<path d="M30 12L8 30l22 18" stroke="#2EE59D" stroke-width="5" fill="none" stroke-linecap="round"/></svg>'
            f'<div class="fdots" id="{prefix}d">{"".join("<i></i>" for _ in range(3))}</div>')

for k, (a, b, lay, beat, caps) in enumerate(SEGS):
    t0, t1 = OUTS[k]
    g = f"b{k}"
    if beat == "no":
        grp(g, t0, t1 + 0.05, '<div id="no" class="giant red">لا.</div>')
        slam("#no", t0 + 0.6, 2.4); sfx(t0 + 0.6, "IM-003", -4)
    elif beat in ("training", "stress"):
        media_framed(g, beat, t0, t1); sfx(t0, "PO-006", -6)
    elif beat == "gauge":
        rows = [("الستريس", "m1", 0.92), ("الضغط", "m2", 0.86)]
        inner = '<div class="bk">STRESS · PRESSURE</div>'
        for i, (lab, mid, v) in enumerate(rows):
            inner += (f'<div class="mrow"><div class="mlab">{lab}</div><div class="mtrack"><i id="{mid}" style="width:{v * 100:.0f}%"></i>'
                      + "".join(f'<u style="right:{p}%"></u>' for p in (25, 50, 75)) + '</div></div>')
        board(g, t0, t1, inner)
        for i, (_, mid, _) in enumerate(rows):
            st = t0 + 0.25 + i * (t1 - t0) * 0.33
            tw(f"tl.fromTo('#{mid}',{{scaleX:0}},{{scaleX:1,duration:1.1,ease:'power3.out'}},{st:.3f});")
            sfx(st, "RS-001" if False else "WH-012", -10)
        tw(f"tl.to('#{g}c',{{x:6,duration:.05,yoyo:true,repeat:9,ease:'none'}},{t1 - 0.9:.3f});")
    elif beat == "result":
        grp(g, t0, t1,
            '<div id="rs1" class="tline" style="top:640px"><span class="tk ok">' + svg("check", 92, 3) + '</span> واجدين <b>للنتيجة</b></div>'
            '<div id="rs2" class="tline" style="top:900px"><span class="tk no">' + svg("x", 92, 3) + '</span> ماواجدينش <b class="r">للفعل</b></div>')
        slam("#rs1", t0 + 0.05, 1.4); sfx(t0 + 0.05, "PO-013", -6)
        slam("#rs2", t0 + 1.25, 1.4); sfx(t0 + 1.25, "IM-003", -8)
    elif beat in ("io0", "io"):
        p = "f0" if beat == "io0" else "f1"
        board(g, t0, t1, '<div class="bk">INPUT → OUTPUT</div>' + flow(p))
        d = t1 - t0
        if beat == "io0":   # "كاين الإنبوت / وكاين الأوتبوت / الإنبوت شنو كندير / والنتيجة شنو كناخد"
            pop(f"#{p}in", t0 + 0.15, 0.7); sfx(t0 + 0.15, "PO-006", -8)
            pop(f"#{p}out", t0 + d * 0.33, 0.7); sfx(t0 + d * 0.33, "PO-006", -8)
            tw(f"tl.from('#{p}p',{{attr:{{'stroke-dashoffset':200}},opacity:0,duration:.6}},{t0 + d * 0.4:.3f});")
            tw(f"tl.to('#{p}in',{{borderColor:'#2EE59D',boxShadow:'0 0 60px rgba(46,229,157,.55)',backgroundColor:'rgba(14,159,110,.22)',duration:.3}},{t0 + d * 0.55:.3f});")
            tw(f"tl.to('#{p}in',{{borderColor:'rgba(167,243,208,.35)',boxShadow:'0 0 0px rgba(0,0,0,0)',backgroundColor:'rgba(10,42,31,.6)',duration:.3}},{t0 + d * 0.8:.3f});")
            tw(f"tl.to('#{p}out',{{borderColor:'#2EE59D',boxShadow:'0 0 60px rgba(46,229,157,.55)',backgroundColor:'rgba(14,159,110,.22)',duration:.3}},{t0 + d * 0.8:.3f});")
        else:               # "المقاول هو داك الشخص / اللي كيركز على الفعل / والنتيجة كتجي من بعد"
            tw(f"tl.set('#{p}out',{{opacity:.45}},{t0:.3f});")
            h(f'<div id="{g}chip" class="chip" style="right:110px;top:338px">المقاول</div>')
            tw(f"tl.set('#{g}chip',{{autoAlpha:0}},0);tl.set('#{g}chip',{{autoAlpha:1}},{t0 + d * 0.15:.3f});tl.set('#{g}chip',{{autoAlpha:0}},{t1 - 0.2:.3f});")
            pop(f"#{g}chip", t0 + d * 0.15, 0.5); sfx(t0 + d * 0.15, "PO-008", -8)
            tw(f"tl.to('#{p}in',{{borderColor:'#2EE59D',boxShadow:'0 0 60px rgba(46,229,157,.55)',backgroundColor:'rgba(14,159,110,.22)',duration:.3}},{t0 + d * 0.42:.3f});")
            sfx(t0 + d * 0.42, "PO-013", -8)
            tw(f"tl.to('#{p}out',{{opacity:1,borderColor:'#2EE59D',boxShadow:'0 0 60px rgba(46,229,157,.55)',backgroundColor:'rgba(14,159,110,.22)',duration:.35}},{t0 + d * 0.72:.3f});")
            sfx(t0 + d * 0.72, "PO-006", -8)
        reps = max(int((t1 - t0 - 0.8) / 1.05), 0)
        for j in range(3):
            tw(f"tl.fromTo('#{p}d i:nth-child({j + 1})',{{x:0,opacity:1}},{{x:-210,opacity:0,duration:1.05,ease:'none',repeat:{reps}}},{t0 + 0.6 + j * 0.35:.3f});")
    elif beat in ("night", "climb", "team"):
        media_full(g, beat, t0, t1)
    elif beat == "nightday":
        inner = ('<div class="bk">NIGHT · DAY</div>'
                 '<div class="dial"><div class="dn"></div><div class="dd"></div>'
                 f'<div class="dm">{svg("moon", 62, 1.6, "#A7F3D0")}</div><div class="ds">{svg("sun", 62, 1.6, "#FDE68A")}</div>'
                 '<div class="hand" id="hand"><i></i></div><div class="hub"></div></div>'
                 '<div class="dlab l" id="dl1">حلم<span>بالليل</span></div><div class="dlab r" id="dl2">خدم<span>بالنهار</span></div>')
        board(g, t0, t1, inner)
        rise("#dl1", t0 + 0.15, 20, 0.4)
        tw(f"tl.fromTo('#hand',{{rotation:90}},{{rotation:-90,duration:1.1,ease:'power3.inOut'}},{t0 + 1.0:.3f});")
        rise("#dl2", t0 + 1.2, 20, 0.4); sfx(t0 + 1.0, "WH-012", -8)
    elif beat == "steps12":
        s0, s1 = OUTS[k][0], OUTS[k + 1][1]
        rows = [("play", "بدا فأقرب وقت"), ("clock", "الصبر · مجال واحد"), ("repeat", "بيع اللي كيتعاود يتشرى")]
        inner = '<div class="bk">3 STEPS</div><div class="sline"><i id="sfill"></i></div>'
        for i, (ic, txt) in enumerate(rows):
            inner += (f'<div class="srow" id="sr{i}" style="top:{96 + i * 104}px"><div class="snode" id="sn{i}">{i + 1}</div>'
                      f'<div class="sic">{svg(ic, 40, 2.2)}</div><div class="stx">{txt}</div>'
                      f'<div class="sck" id="sc{i}">{svg("check", 34, 3)}</div></div>')
        board("ckg", s0, s1, inner)
        d1 = OUTS[k][1] - OUTS[k][0]
        n3 = OUTS[k + 1][0]
        marks = [(s0 + 0.1, s0 + 1.3), (s0 + d1 * 0.36, s0 + d1 * 0.92), (n3 + 0.05, OUTS[k + 1][1] - 0.6)]
        tw(f"tl.set('.srow',{{opacity:.25}},{s0:.3f});")
        for i, (ta, tb) in enumerate(marks):
            tw(f"tl.to('#sr{i}',{{opacity:1,x:0,duration:.35,ease:'expo.out'}},{ta:.3f});")
            tw(f"tl.fromTo('#sn{i}',{{scale:.6}},{{scale:1,backgroundColor:'#0E9F6E',duration:.4,ease:'back.out(2)'}},{ta:.3f});")
            tw(f"tl.to('#sfill',{{scaleY:{(i + 1) / 3:.3f},duration:.5,ease:'power2.out'}},{ta:.3f});")
            pop(f"#sc{i}", tb, 0.3, 0.4); sfx(tb, "PO-013", -8)
            sfx(ta, "PO-006", -10)

# end card (text layout, after the last spoken word)
grp("endg", VOICE_END - 0.05, TOTAL + 0.2,
    '<div id="e1" class="tline" style="top:600px">مع <b>السنوات</b></div>'
    '<div id="e2" class="tline big" style="top:800px">غادي تمشي <b>مزيان</b></div>'
    '<div id="endc" class="glass" style="left:190px;top:1180px;width:700px;height:200px;text-align:center">'
    '<div class="wm">ORANUSS ACADEMY</div><div class="sub" style="margin-top:14px">BUSINESS · DARIJA</div></div>', "grp tgrp")
slam("#e1", VOICE_END + 0.05, 1.4); slam("#e2", VOICE_END + 0.35, 1.4); rise("#endc", VOICE_END + 0.8, 40, 0.6)
sfx(VOICE_END + 0.05, "IM-003", -6); sfx(VOICE_END + 0.8, "LO-003", -8, 1.8)

# ---------------- captions ----------------
CAPS = []
for k, (a, b, lay, beat, caps) in enumerate(SEGS):
    t0, t1 = OUTS[k]
    n = sum(len(c.split()) for c, _ in caps); done = 0
    for text, acc in caps:
        nw = len(text.split())
        CAPS.append((t0 + (t1 - t0) * done / n, t0 + (t1 - t0) * (done + nw) / n, text, acc, CAPY[lay], beat))
        done += nw
for k, (a, b, text, acc, y, beat) in enumerate(CAPS):
    if beat == "result":
        continue                      # the full-screen kinetic lines already show these words
    if beat == "no":
        y = 1500
    words = text.split(" ")
    if k + 1 < len(CAPS):
        b = min(b, CAPS[k + 1][0] - 0.07)
    sp = "".join(f'<span id="w{k}_{i}" class="cw{" acc" if i == acc else ""}{" lat" if w.isascii() else ""}">{w}</span> '
                 for i, w in enumerate(words))
    h(f'<div id="cap{k}" class="cap{" sm" if y == CAPY["split"] else ""}" style="top:{y}px">{sp}</div>')
    tw(f"tl.set('#cap{k}',{{autoAlpha:1}},{a - 0.067:.3f});tl.set('#cap{k}',{{autoAlpha:0}},{b:.3f});")
    tw(f"tl.fromTo('#cap{k}',{{y:18}},{{y:0,duration:.3,ease:'expo.out'}},{a - 0.067:.3f});")
    step = (b - a) / max(len(words), 1)
    for i in range(len(words)):
        tw(f"tl.fromTo('#w{k}_{i}',{{opacity:.45}},{{opacity:1,duration:.1}},{a - 0.067 + i * step:.3f});")
        if i == acc:
            tw(f"tl.fromTo('#w{k}_{i}',{{scale:.8}},{{scale:1,duration:.35,ease:'back.out(2.5)'}},{a - 0.067 + i * step:.3f});")

CSS = """
@font-face{font-family:GA;src:url(assets/fonts/GraphikArabic-Medium.woff2);font-weight:500}
@font-face{font-family:GA;src:url(assets/fonts/GraphikArabic-Bold.woff2);font-weight:700}
@font-face{font-family:GA;src:url(assets/fonts/GraphikArabic-Black.woff2);font-weight:900}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#05140F;font-family:GA,'Avenir Next',sans-serif;color:#fff}
#root{position:absolute;inset:0;overflow:hidden}
#cam{position:absolute;inset:0}
#camz{position:absolute;inset:0;transform-origin:50% 35%}
#camv{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.vig{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,20,15,.35) 0%,rgba(5,20,15,0) 22%,rgba(5,20,15,0) 55%,rgba(5,20,15,.75) 100%)}
#stage{position:absolute;inset:0;background:radial-gradient(circle at 50% 30%,#11402F 0%,#0A2A1F 40%,#05140F 85%);clip-path:inset(0px 0px 1920px 0px)}
#stage::before{content:"";position:absolute;inset:0;opacity:.07;background-image:linear-gradient(#A7F3D0 1px,transparent 1px),linear-gradient(90deg,#A7F3D0 1px,transparent 1px);background-size:90px 90px}
#stage::after{content:"";position:absolute;left:0;right:0;top:986px;height:4px;background:#2EE59D;box-shadow:0 0 24px #2EE59D}
.grp,.media{position:absolute;inset:0;visibility:hidden}
.grp div,.grp svg,.media div{position:absolute}
.grp .glass div,.grp .row div,.grp .ckr div{position:relative}
.media img{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover}
.mshade{inset:0;background:linear-gradient(180deg,rgba(5,20,15,.25) 0%,rgba(5,20,15,0) 30%,rgba(5,20,15,.15) 55%,rgba(5,20,15,.85) 100%)}
.media .mblur{filter:blur(36px) brightness(.35);transform:scale(1.15)}
.frame{left:70px;top:460px;width:940px;height:640px;border-radius:40px;overflow:hidden;border:3px solid rgba(167,243,208,.6);box-shadow:0 30px 90px rgba(0,0,0,.6),0 0 50px rgba(46,229,157,.25)}
.frame img{position:absolute;left:0;top:0;width:940px;height:640px;object-fit:cover}
.glass{border-radius:44px;background:linear-gradient(160deg,rgba(17,64,47,.95),rgba(10,42,31,.92));border:2px solid rgba(167,243,208,.45);
  box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 40px rgba(46,229,157,.18),inset 0 1px 0 rgba(255,255,255,.18)}
.lbl{direction:rtl;text-align:center;font-weight:900;font-size:58px}
.sub{position:relative;direction:ltr;text-align:center;font-family:'Avenir Next';font-weight:600;letter-spacing:8px;font-size:28px;color:#A7F3D0}
.row{display:flex;gap:20px;justify-content:center;margin-top:40px}
.disc,.disc2{width:112px;height:112px;border-radius:50%;background:#0E9F6E;display:flex;align-items:center;justify-content:center;box-shadow:0 0 40px rgba(46,229,157,.55)}
.disc2{background:#163F31;box-shadow:none}
.pill{position:absolute;top:250px;left:50%;transform:translateX(-50%);direction:rtl;padding:12px 32px;border-radius:60px;background:rgba(10,42,31,.85);
  border:2px solid rgba(167,243,208,.55);box-shadow:0 0 30px rgba(46,229,157,.35);font-weight:700;font-size:34px;white-space:nowrap}
.pill i{font-style:normal;color:#2EE59D}
.giant{left:0;right:0;top:620px;text-align:center;font-weight:900;font-size:340px;line-height:1;direction:rtl}
.giant.red{color:#F87171;text-shadow:0 0 60px rgba(248,113,113,.7)}
.tline{left:60px;right:60px;text-align:center;direction:rtl;font-weight:900;font-size:110px;line-height:1.2;display:flex;align-items:center;justify-content:center;gap:30px}
.tline.big{font-size:120px}
.tline b{color:#A7F3D0;text-shadow:0 0 34px rgba(46,229,157,.75)}
.tline b.r{color:#F87171;text-shadow:0 0 34px rgba(248,113,113,.7)}
.grp .tline .tk{position:relative;width:140px;height:140px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.tk.ok{background:#0E9F6E;box-shadow:0 0 50px rgba(46,229,157,.7)} .tk.no{background:#9b2c2c;box-shadow:0 0 50px rgba(248,113,113,.6)}
.half{top:0;width:540px;height:990px}
.ckr{display:flex;flex-direction:row;direction:rtl;align-items:center;gap:22px;height:130px;border-bottom:1px solid rgba(167,243,208,.18)}
.ckn{font-family:'Avenir Next';font-weight:800;font-size:34px;color:#2EE59D;width:56px}
.cki{width:84px;height:84px;border-radius:50%;background:#163F31;display:flex;align-items:center;justify-content:center}
.ckt{flex:1;font-weight:900;font-size:50px;text-align:right}
.ckd{width:76px;height:76px;border-radius:50%;background:#0E9F6E;display:flex;align-items:center;justify-content:center;box-shadow:0 0 30px rgba(46,229,157,.7)}
.wm{position:relative;margin-top:44px;font-family:'Avenir Next';font-weight:800;letter-spacing:10px;font-size:50px;color:#fff;text-shadow:0 0 30px rgba(46,229,157,.7)}

.trk{position:absolute;left:60px;top:248px;width:960px;display:flex;flex-direction:row-reverse;gap:14px;z-index:5}
.trk .tseg{position:relative;flex:1}
.trk .tbar{position:relative;height:8px;border-radius:4px;background:rgba(167,243,208,.18);overflow:hidden}
.trk .tbar i{position:absolute;inset:0;background:linear-gradient(270deg,#2EE59D,#0E9F6E);transform-origin:right center;transform:scaleX(0);box-shadow:0 0 12px #2EE59D}
.trk .tlab{position:relative;margin-top:10px;text-align:center;direction:rtl;font:700 24px GA;color:#A7F3D0;opacity:.45;white-space:nowrap;text-shadow:0 2px 8px rgba(0,0,0,.8)}
.trk .tlab b{font-family:'Avenir Next';font-weight:800;color:#2EE59D;margin-left:4px}
.board{left:60px;top:365px;width:960px;height:420px;border-radius:36px;background:linear-gradient(160deg,rgba(17,64,47,.96),rgba(8,32,24,.94));
  border:2px solid rgba(167,243,208,.35);box-shadow:0 30px 80px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.15);overflow:hidden}
.board .bk{left:0;right:0;top:26px;text-align:center;font:600 24px 'Avenir Next';letter-spacing:8px;color:#A7F3D0;opacity:.85}
.board .mrow{left:50px;right:50px;height:90px;display:flex;flex-direction:row-reverse;align-items:center;gap:30px}
.board .mrow:nth-of-type(2){top:110px} .board .mrow:nth-of-type(3){top:250px}
.grp .board .mrow div{position:relative}
.board .mlab{width:220px;text-align:right;direction:rtl;font:900 50px GA}
.board .mtrack{flex:1;height:36px;border-radius:18px;background:#163F31;overflow:hidden}
.board .mtrack i{position:absolute;right:0;top:0;bottom:0;border-radius:18px;background:linear-gradient(270deg,#2EE59D,#F5C400 60%,#F87171);transform-origin:right center}
.board .mtrack u{position:absolute;top:0;bottom:0;width:2px;background:rgba(5,20,15,.6)}
.board .node{top:90px;width:330px;height:280px;border-radius:28px;border:2px solid rgba(167,243,208,.35);background:rgba(10,42,31,.6);text-align:center}
.board .node.in{right:50px} .board .node.out{left:50px}
.grp .board .node div{position:relative}
.board .nk{margin-top:30px;font:600 22px 'Avenir Next';letter-spacing:6px;color:#A7F3D0}
.board .nt{margin-top:10px;direction:rtl;font:900 50px GA}
.board .nics{display:flex;justify-content:center;gap:14px;margin-top:34px}
.board .nic{width:80px;height:80px;border-radius:50%;background:#0E9F6E;display:flex;align-items:center;justify-content:center;box-shadow:0 0 26px rgba(46,229,157,.5)}
.board .out .nic{background:#163F31;box-shadow:none}
.board .fpath{left:360px;top:200px}
.board .fdots{left:360px;top:222px;width:240px;height:16px}
.grp .board .fdots i{position:absolute;right:0;top:0;width:16px;height:16px;border-radius:50%;background:#2EE59D;box-shadow:0 0 14px #2EE59D;opacity:0}
.chip{position:absolute;padding:10px 34px;border-radius:40px;background:#0E9F6E;font:900 44px GA;direction:rtl;box-shadow:0 0 40px rgba(46,229,157,.6);z-index:6}
.board .dial{left:340px;top:80px;width:280px;height:280px;border-radius:50%;overflow:hidden;border:3px solid rgba(167,243,208,.5)}
.board .dn{right:0;top:0;width:140px;height:280px;background:linear-gradient(180deg,#020806,#0b2a1f)}
.board .dd{left:0;top:0;width:140px;height:280px;background:linear-gradient(180deg,#2a8a63,#14533c)}
.board .dm{right:30px;top:108px} .board .ds{left:30px;top:108px}
.board .hand{left:139px;top:20px;width:2px;height:120px;transform-origin:50% 100%}
.grp .board .hand i{position:absolute;left:-4px;top:0;width:10px;height:120px;border-radius:5px;background:#fff;box-shadow:0 0 16px rgba(255,255,255,.7)}
.board .hub{left:122px;top:122px;width:36px;height:36px;border-radius:50%;background:#fff}
.board .dlab{top:150px;width:260px;text-align:center;direction:rtl;font:900 64px/1.1 GA}
.board .dlab span{display:block;font-size:40px;color:#A7F3D0}
.board .dlab.l{right:40px} .board .dlab.r{left:40px;color:#FDE68A}
.board .dlab.r span{color:#FDE68A}
.board .sline{right:88px;top:118px;width:6px;height:212px;border-radius:3px;background:#163F31}
.grp .board .sline i{position:absolute;inset:0;border-radius:3px;background:#2EE59D;box-shadow:0 0 14px #2EE59D;transform-origin:50% 0;transform:scaleY(0)}
.board .srow{right:50px;width:860px;height:84px;display:flex;flex-direction:row-reverse;align-items:center;gap:22px;transform:translateX(-20px)}
.grp .board .srow div{position:relative}
.board .snode{width:82px;height:82px;border-radius:50%;background:#163F31;border:3px solid #2EE59D;display:flex;align-items:center;justify-content:center;font:800 38px 'Avenir Next'}
.board .sic{width:60px;height:60px;border-radius:50%;background:rgba(167,243,208,.12);display:flex;align-items:center;justify-content:center}
.board .stx{flex:1;text-align:right;direction:rtl;font:900 48px GA}
.board .sck{width:62px;height:62px;border-radius:50%;background:#0E9F6E;display:flex;align-items:center;justify-content:center;box-shadow:0 0 24px rgba(46,229,157,.7);opacity:0}
.cap{position:absolute;left:60px;right:150px;text-align:center;direction:rtl;font:700 68px/1.3 GA;text-shadow:0 4px 18px rgba(0,0,0,.8);visibility:hidden}
.cap .cw{display:inline-block}
.cap.sm{font-size:58px;white-space:nowrap;left:40px;right:40px} .cap.sm .acc{font-size:72px}
.cap .acc{font-weight:900;font-size:88px;color:#A7F3D0;text-shadow:0 0 28px rgba(46,229,157,.7),0 4px 18px rgba(0,0,0,.6)}
.cap .lat{font-family:'Avenir Next';font-weight:800;font-style:italic}
"""
html = f"""<!doctype html>
<html lang="ar"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <div id="cam"><div id="camz"><video id="camv" class="clip" src="assets/aroll.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0"></video></div><div class="vig"></div></div>
  <div id="stage"></div>
  {chr(10).join("  " + x for x in H)}
  <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-volume="1"></audio>
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join("  " + x for x in J)}
  tl.to({{}},{{duration:0.001}},{TOTAL - 0.01});
  window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>"""
os.makedirs(PROJ, exist_ok=True)
open(os.path.join(PROJ, "index.html"), "w", encoding="utf-8").write(html)
json.dump({"total": TOTAL, "cues": sorted(CUES)}, open(os.path.join(WK, "sfx_cues_v4.json"), "w"))
mix = {}
for k, s in enumerate(SEGS):
    mix[s[2]] = mix.get(s[2], 0) + OUTS[k][1] - OUTS[k][0]
mix["text"] = mix.get("text", 0) + END_HOLD
print(f"total {TOTAL}s · " + " · ".join(f"{k} {v:.1f}s ({v / TOTAL:.0%})" for k, v in mix.items()) + f" · caps {len(CAPS)} · sfx {len(CUES)}")
