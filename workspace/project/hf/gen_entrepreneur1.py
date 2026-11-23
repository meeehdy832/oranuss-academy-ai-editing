# Developed by Mehdi ORANUSS | Powered by Claude
"""Short #1 «واش أي واحد يقدر يكون مقاول؟» (9:16) from the entrepreneur podcast (output/ytsave-entrepreneur/PLAN.md).
Style dark-green, Arabic captions (Graphik Arabic). Mix target: animation 60 %, images 20 %, face A 10 %, face B 10 %.
Footage: one face, centred on the macOS Vision face track (work/ytsave-entrepreneur/faces.json), static crop per piece.
usage: python3 -I gen_entrepreneur1.py [--media]   (--media rebuilds aroll.mp4 + voice.wav)"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "entrepreneur1")
AS = os.path.join(PROJ, "assets")
WK = os.path.abspath(os.path.join(HERE, "..", "work", "ytsave-entrepreneur"))
SRC = os.path.join(WK, "src.mp4")
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
if not os.path.exists(FF):
    FF = "ffmpeg"
END_HOLD = 1.8

# (src_start, src_end, beat, caption chunks [(text, accent word index)])
# beats: faceB, faceA, no, stress_img, gauge, result, img_buy, io, img_night, nightday, img_dream, field
SEGS = [
    (191.40, 195.95, "faceB", [("ولكن واش بالصح", 2), ("أي واحد يقدر", 1)]),
    (195.95, 197.05, "no", [("يكون مقاول؟", 1)]),
    (198.62, 200.55, "faceA", [("ممكن ينجحو الناس", 1)]),
    (200.55, 202.60, "few", [("ولكن ماشي أي واحد", 1), ("يكون مقاول", 1)]),
    (211.15, 213.50, "stress_img", [("ماكيتحملوش داك الستريس", 2)]),
    (213.50, 215.95, "gauge", [("وداك الضغط", 1), ("اللي كيكون فالمقاولة", 2)]),
    (219.30, 222.20, "result", [("واجدين للنتيجة", 1), ("ولكن ماواجدينش للفعل", 2)]),
    (227.05, 230.55, "img_buy", [("ناخدو الفلوس", 1), ("ونشريو الطوموبيل", 1), ("ونشريو الدار", 1)]),
    (237.60, 243.45, "io", [("والمقاول هو داك الشخص", 0), ("اللي كيركز على الفعل", 3), ("والنتيجة كتجي من بعد", 0)]),
    (247.95, 250.95, "faceA3", [("كتحلم بالـ output", 1), ("ولكن ماكديرش الـ input", 2)]),
    (251.95, 254.25, "img_night", [("أنا كنقول للناس", 2), ("ديما حلموها بالليل", 2)]),
    (258.85, 262.45, "nightday", [("حلم بالليل وخدم بالنهار", 3), ("باش توصل للشي اللي حلمتي بيه", 5)]),
    (262.65, 264.95, "img_dream", [("ممكن نتا كتحلم", 2), ("بالنهار وبالليل", 1)]),
    (271.55, 277.00, "field", [("بدا فأقرب وقت ممكن", 1), ("والصبر لمدة ديال سنوات", 3), ("فحاجة وحدة فمجال واحد", 1)]),
]
FACE_BEATS = {"faceB", "faceA", "faceA3"}
OUTS = []
t = 0.0
for a, b, beat, caps in SEGS:
    OUTS.append((round(t, 3), round(t + b - a, 3)))
    t += b - a
VOICE_END = round(t, 3)
TOTAL = round(t + END_HOLD, 3)

# ---------------- media ----------------
def build_media():
    os.makedirs(AS, exist_ok=True)
    faces = json.load(open(os.path.join(WK, "faces.json")))
    tmp = os.path.join(WK, "seg"); os.makedirs(tmp, exist_ok=True)
    lst = []
    for k, (a, b, beat, _) in enumerate(SEGS):
        near = sorted(f["x"] + f["w"] / 2 for f in faces if a <= f["t"] <= b)
        cx = near[len(near) // 2]
        x = int(min(max(cx - 304, 0), 1920 - 608))
        p = os.path.join(tmp, f"v{k:02d}.mp4")
        subprocess.run([FF, "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", SRC,
                        "-vf", f"crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,eq=contrast=1.06:saturation=1.04,fps=30,setsar=1",
                        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", p], check=True)
        lst.append(p)
    open(os.path.join(tmp, "list.txt"), "w").write("".join(f"file '{p}'\n" for p in lst))
    subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"),
                    "-vf", f"tpad=stop_mode=clone:stop_duration={END_HOLD}", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "16", "-pix_fmt", "yuv420p", os.path.join(AS, "aroll.mp4")], check=True)
    # voice: same pieces, 15 ms fades, cleaned, then -14 LUFS
    parts, fl = [], []
    for k, (a, b, _, _) in enumerate(SEGS):
        d = b - a
        fl.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={d - 0.03:.3f}:d=0.03[a{k}]")
        parts.append(f"[a{k}]")
    fl.append("".join(parts) + f"concat=n={len(SEGS)}:v=0:a=1,highpass=f=80,afftdn=nf=-25,"
              "acompressor=threshold=-20dB:ratio=3:attack=5:release=80,"
              f"apad=pad_dur={END_HOLD},loudnorm=I=-14:TP=-1.5:LRA=9[out]")
    subprocess.run([FF, "-v", "error", "-y", "-i", SRC, "-filter_complex", ";".join(fl), "-map", "[out]",
                    "-ar", "48000", "-ac", "2", os.path.join(AS, "voice.wav")], check=True)
    os.makedirs(os.path.join(AS, "fonts"), exist_ok=True)
    for w in ("Bold", "Black", "Medium"):
        subprocess.run(["cp", os.path.join(HERE, "1112/assets/fonts", f"GraphikArabic-{w}.woff2"), os.path.join(AS, "fonts")])
    print("media ok")

if "--media" in sys.argv:
    build_media()

# ---------------- html / timeline ----------------
H, J = [], []
def h(s): H.append(s)
def tw(s): J.append(s)
def grp(gid, t0, t1, inner):
    h(f'<div id="{gid}" class="grp">{inner}</div>')
    tw(f"tl.set('#{gid}',{{autoAlpha:1}},{t0:.3f});tl.to('#{gid}',{{autoAlpha:0,duration:.2}},{t1 - 0.2:.3f});")
def rise(sel, t, dy=70, d=0.5):
    tw(f"tl.fromTo('{sel}',{{y:{dy},opacity:0,filter:'blur(10px)'}},{{y:0,opacity:1,filter:'blur(0px)',duration:{d},ease:'expo.out'}},{t:.3f});")
def pop(sel, t, s0=0.4, d=0.5):
    tw(f"tl.fromTo('{sel}',{{scale:{s0},opacity:0}},{{scale:1,opacity:1,duration:{d},ease:'back.out(1.8)'}},{t:.3f});")
def slam(sel, t):
    tw(f"tl.fromTo('{sel}',{{scale:1.7,opacity:0,filter:'blur(16px)'}},{{scale:1,opacity:1,filter:'blur(0px)',duration:.4,ease:'expo.out'}},{t:.3f});")

IC = {
    "hammer": '<path d="M14 6l4 4M5 19l8.5-8.5M12 4l6 6 2-2-6-6z"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>',
    "car": '<path d="M3 13l2-5h14l2 5v5H3z"/><circle cx="7.5" cy="17" r="1.6"/><circle cx="16.5" cy="17" r="1.6"/>',
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "cash": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
    "moon": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    "sun": '<circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "img": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-9 9"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
}
def svg(name, size=80, sw=2.0, color="#fff"):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{IC[name]}</svg>')

def photo(pid, x, y, w, hgt, icon, label):
    """Placeholder photo (to be replaced by a real photo once picked): frosted frame + Ken Burns layer."""
    return (f'<div id="{pid}" class="glass photo" style="left:{x}px;top:{y}px;width:{w}px;height:{hgt}px">'
            f'<div class="ph" id="{pid}k">{svg(icon, min(w, hgt) * 0.32, 1.4, "#A7F3D0")}<div class="phl">PHOTO · {label}</div></div></div>')
def kb(pid, t0, t1):
    tw(f"tl.fromTo('#{pid}k',{{scale:1}},{{scale:1.07,duration:{t1 - t0:.3f},ease:'none'}},{t0:.3f});")

STAGE_BEATS = []   # (t0, t1) when the green stage covers the footage
def beat_span(k):
    return OUTS[k]

PILL = '<div class="pill">فكرة <i>01</i> · واش أي واحد يقدر يكون مقاول؟</div>'
for k, (a, b, beat, caps) in enumerate(SEGS):
    t0, t1 = OUTS[k]
    if beat in FACE_BEATS:
        tw(f"tl.fromTo('#cam',{{scale:1}},{{scale:1.07,duration:{t1 - t0:.3f},ease:'sine.inOut'}},{t0:.3f});")
        tw(f"tl.fromTo('#camv',{{filter:'blur(12px)'}},{{filter:'blur(0px)',duration:.3,ease:'power2.out',immediateRender:false}},{t0:.3f});")
        continue
    STAGE_BEATS.append((t0, t1))
    g = f"b{k}"
    if beat == "no":
        grp(g, t0, t1 + 0.05, '<div id="no" class="nochip">لا.</div>')
        slam("#no", t0 + 0.55)
    elif beat == "few":
        cells = "".join(f'<div class="pp{" lit" if i in (5, 14) else ""}" id="pp{i}">{svg("user", 70, 1.8)}</div>' for i in range(20))
        grp(g, t0, t1, PILL + f'<div id="ppg" class="ppg">{cells}</div>')
        tw(f"tl.from('#ppg .pp',{{scale:0,opacity:0,stagger:.025,duration:.35,ease:'back.out(2)'}},{t0 + 0.05:.3f});")
        tw(f"tl.to('#ppg .pp:not(.lit)',{{opacity:.22,duration:.3}},{t0 + 1.0:.3f});")
        tw(f"tl.to('#ppg .lit',{{background:'#0E9F6E',boxShadow:'0 0 50px rgba(46,229,157,.8)',scale:1.15,duration:.35,ease:'back.out(2)'}},{t0 + 1.0:.3f});")
    elif beat == "stress_img":
        grp(g, t0, t1, PILL + photo("p1", 110, 430, 860, 680, "img", "STRESSED ENTREPRENEUR"))
        pop("#p1", t0, 0.85, 0.45); kb("p1", t0, t1)
    elif beat == "gauge":
        grp(g, t0, t1, PILL +
            '<div id="gc" class="glass" style="left:140px;top:470px;width:800px;height:600px">'
            '<div class="sub" style="margin-top:44px">STRESS · PRESSURE</div>'
            '<svg style="position:absolute;left:150px;top:150px" width="500" height="300" viewBox="0 0 500 300">'
            '<defs><linearGradient id="gg" x1="0" x2="1"><stop offset="0" stop-color="#2EE59D"/><stop offset=".6" stop-color="#F5C400"/><stop offset="1" stop-color="#F87171"/></linearGradient></defs>'
            '<path d="M40 260A210 210 0 0 1 460 260" stroke="#163F31" stroke-width="44" fill="none" stroke-linecap="round"/>'
            '<path id="garc" d="M40 260A210 210 0 0 1 460 260" stroke="url(#gg)" stroke-width="44" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
            '<g id="needle" style="transform-origin:250px 260px"><path d="M250 260L250 90" stroke="#fff" stroke-width="12" stroke-linecap="round"/><circle cx="250" cy="260" r="22" fill="#fff"/></g></svg>'
            '<div id="glbl" class="lbl" style="position:absolute;left:0;right:0;top:470px;color:#F87171">الضغط</div></div>')
        rise("#gc", t0, 60, 0.45)
        tw(f"tl.fromTo('#garc',{{attr:{{'stroke-dashoffset':1}}}},{{attr:{{'stroke-dashoffset':0.04}},duration:1.6,ease:'power2.inOut'}},{t0 + 0.3:.3f});")
        tw(f"tl.fromTo('#needle',{{rotation:-90}},{{rotation:78,duration:1.6,ease:'power2.inOut'}},{t0 + 0.3:.3f});")
        tw(f"tl.to('#needle',{{rotation:72,duration:.08,yoyo:true,repeat:7,ease:'none'}},{t0 + 1.9:.3f});")
        slam("#glbl", t0 + 0.9)
    elif beat == "result":
        grp(g, t0, t1, PILL +
            '<div id="r1" class="glass on" style="left:560px;top:520px;width:420px;height:470px">'
            '<div class="sub" style="margin-top:50px">OUTPUT</div><div class="lbl" style="margin-top:14px">النتيجة</div>'
            f'<div class="disc" style="margin:50px auto 0">{svg("check", 80, 2.6)}</div></div>'
            '<div id="r2" class="glass" style="left:100px;top:520px;width:420px;height:470px">'
            '<div class="sub" style="margin-top:50px">INPUT</div><div class="lbl" style="margin-top:14px">الفعل</div>'
            f'<div class="disc red" style="margin:50px auto 0">{svg("x", 80, 2.6)}</div></div>')
        pop("#r1", t0 + 0.05, 0.6); pop("#r2", t0 + 1.25, 0.6)
        tw(f"tl.to('#r2',{{opacity:.55,duration:.3}},{t0 + 2.0:.3f});")
    elif beat == "img_buy":
        o = OUTS[k][0]
        grp(g, t0, t1, PILL + photo("p2", 90, 420, 430, 560, "cash", "MONEY") + photo("p3", 560, 420, 430, 560, "car", "CAR"))
        # three beats on the spoken words: money, car, house (house replaces the pair, full width)
        pop("#p2", t0 + 0.0, 0.8, 0.4); kb("p2", t0, t1)
        pop("#p3", t0 + 1.05, 0.8, 0.4); kb("p3", t0 + 1.05, t1)
        h(f'<div id="p5w" class="grp">{photo("p5", 110, 420, 860, 600, "home", "HOUSE")}</div>')
        tw(f"tl.set('#p5w',{{autoAlpha:1}},{t0 + 2.35:.3f});tl.to('#p5w',{{autoAlpha:0,duration:.2}},{t1 - 0.2:.3f});")
        tw(f"tl.to('#p2,#p3',{{opacity:0,scale:.9,duration:.25}},{t0 + 2.3:.3f});")
        pop("#p5", t0 + 2.35, 0.85, 0.4); kb("p5", t0 + 2.35, t1)
    elif beat == "io":
        grp(g, t0, t1, PILL +
            '<div id="io1" class="glass" style="left:80px;top:520px;width:440px;height:470px">'
            '<div class="sub" style="margin-top:46px">OUTPUT</div><div class="lbl" style="margin-top:14px">النتيجة</div>'
            f'<div class="row">{"".join(f"<div class=disc2>{svg(i, 64)}</div>" for i in ("car", "home", "cash"))}</div></div>'
            '<div id="io2" class="glass" style="left:560px;top:520px;width:440px;height:470px">'
            '<div class="sub" style="margin-top:46px">INPUT</div><div class="lbl" style="margin-top:14px">الفعل</div>'
            f'<div class="row">{"".join(f"<div class=disc>{svg(i, 64)}</div>" for i in ("hammer", "list"))}</div></div>'
            '<svg id="arr" style="position:absolute;left:470px;top:715px" width="140" height="80" viewBox="0 0 140 80"><path d="M130 40H20M44 14L16 40l28 26" stroke="#2EE59D" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>'
            '<div id="later" class="chip2" style="left:330px;top:1040px">… من بعد</div>')
        rise("#io2", t0 + 0.1); rise("#io1", t0 + 0.3)
        tw(f"tl.to('#io2',{{borderColor:'#2EE59D',boxShadow:'0 0 80px rgba(46,229,157,.55)',scale:1.04,duration:.35}},{t0 + 2.4:.3f});")
        tw(f"tl.to('#arr path',{{attr:{{'stroke-dashoffset':0}},duration:.6,ease:'power2.out'}},{t0 + 3.2:.3f});")
        tw(f"tl.from('#io1 .disc2',{{scale:0,opacity:0,stagger:.08,duration:.4,ease:'back.out(2)'}},{t0 + 3.7:.3f});")
        pop("#later", t0 + 4.1, 0.6)
    elif beat == "img_night":
        grp(g, t0, t1, PILL + photo("p6", 110, 430, 860, 680, "moon", "NIGHT · DREAMING"))
        pop("#p6", t0, 0.85, 0.45); kb("p6", t0, t1)
    elif beat == "nightday":
        grp(g, t0, t1,
            '<div id="nl" class="half" style="left:0;background:linear-gradient(180deg,#020806,#071a13)"></div>'
            '<div id="nr" class="half" style="left:540px;background:linear-gradient(180deg,#1a6a4c,#0A2A1F)"></div>'
            '<div id="nd" style="position:absolute;left:538px;top:0;width:4px;height:1920px;background:#2EE59D;box-shadow:0 0 30px #2EE59D"></div>'
            f'<div id="mo" style="left:150px;top:560px">{svg("moon", 240, 1.2, "#A7F3D0")}</div>'
            f'<div id="su" style="left:690px;top:560px">{svg("sun", 240, 1.2, "#FDE68A")}</div>'
            '<div id="ml" class="lbl" style="left:0;width:540px;top:860px">حلم بالليل</div>'
            '<div id="sl" class="lbl" style="left:540px;width:540px;top:860px;color:#A7F3D0">خدم بالنهار</div>' + PILL)
        tw(f"tl.from('#nr',{{xPercent:100,duration:.5,ease:'expo.out'}},{t0 + 0.9:.3f});")
        tw(f"tl.from('#nd',{{scaleY:0,duration:.5,ease:'expo.out'}},{t0 + 0.9:.3f});")
        pop("#mo", t0 + 0.1); rise("#ml", t0 + 0.25, 40)
        pop("#su", t0 + 1.0); rise("#sl", t0 + 1.15, 40)
        tw(f"tl.to('#su svg',{{rotation:90,duration:{t1 - t0:.2f},ease:'none'}},{t0 + 1.0:.3f});")
    elif beat == "img_dream":
        grp(g, t0, t1, PILL + photo("p7", 110, 430, 860, 680, "img", "DAYDREAMING"))
        pop("#p7", t0, 0.85, 0.45); kb("p7", t0, t1)
    elif beat == "field":
        grp(g, t0, t1 + END_HOLD + 0.2, PILL +
            '<div id="fc" class="glass" style="left:110px;top:470px;width:860px;height:560px;padding:56px 60px">'
            '<div class="sub">ONE FIELD · YEARS</div><div class="lbl" style="position:static;margin-top:20px">حاجة وحدة فمجال واحد</div>'
            '<div style="position:relative;margin-top:70px;height:26px;border-radius:13px;background:#163F31">'
            '<div id="bar" style="position:absolute;right:0;top:0;height:26px;width:100%;border-radius:13px;background:linear-gradient(270deg,#0E9F6E,#2EE59D);box-shadow:0 0 30px #2EE59D;transform-origin:right center"></div></div>'
            '<div class="yrs">' + "".join(f'<span id="y{i}">{i}</span>' for i in range(1, 6)) + '</div></div>'
            '<div id="endc" class="glass" style="left:140px;top:1150px;width:800px;height:230px;text-align:center">'
            '<div class="wm">ORANUSS ACADEMY</div><div class="sub" style="margin-top:18px">BUSINESS · DARIJA</div></div>')
        rise("#fc", t0 + 0.05)
        tw(f"tl.fromTo('#bar',{{scaleX:0}},{{scaleX:1,duration:{t1 - t0 - 1.0:.2f},ease:'power1.inOut'}},{t0 + 1.6:.3f});")
        tw(f"tl.from('.yrs span',{{opacity:.2,stagger:{(t1 - t0 - 1.0) / 5:.2f},duration:.2}},{t0 + 1.6:.3f});")
        rise("#endc", VOICE_END + 0.05, 50, 0.6)

# stage on/off: covers the footage on every non-face beat (merged spans)
spans = []
for a, b in STAGE_BEATS:
    if spans and abs(spans[-1][1] - a) < 0.01:
        spans[-1][1] = b
    else:
        spans.append([a, b])
spans[-1][1] = TOTAL
for a, b in spans:
    tw(f"tl.fromTo('#stage',{{clipPath:'circle(0% at 50% 50%)'}},{{clipPath:'circle(150% at 50% 50%)',duration:.4,ease:'expo.inOut',immediateRender:false}},{max(a - 0.1, 0):.3f});")
    if b < TOTAL:
        tw(f"tl.to('#stage',{{clipPath:'circle(0% at 50% 50%)',duration:.35,ease:'expo.inOut'}},{b - 0.15:.3f});")

# ---------------- captions ----------------
CAPS = []
for k, (a, b, beat, caps) in enumerate(SEGS):
    t0, t1 = OUTS[k]
    n = sum(len(c.split()) for c, _ in caps)
    done = 0
    for text, acc in caps:
        nw = len(text.split())
        s = t0 + (t1 - t0) * done / n
        e = t0 + (t1 - t0) * (done + nw) / n
        CAPS.append((s, e, text, acc))
        done += nw
for k, (a, b, text, acc) in enumerate(CAPS):
    words = text.split(" ")
    if k + 1 < len(CAPS):
        b = min(b, CAPS[k + 1][0] - 0.07)
    spans_ = "".join(f'<span id="w{k}_{i}" class="cw{" acc" if i == acc else ""}{" lat" if w.isascii() else ""}">{w}</span> ' for i, w in enumerate(words))
    h(f'<div id="cap{k}" class="cap">{spans_}</div>')
    tw(f"tl.set('#cap{k}',{{autoAlpha:1}},{a - 0.067:.3f});tl.set('#cap{k}',{{autoAlpha:0}},{b:.3f});")
    tw(f"tl.fromTo('#cap{k}',{{y:18}},{{y:0,duration:.3,ease:'expo.out'}},{a - 0.067:.3f});")
    step = (b - a) / max(len(words), 1)
    for i in range(len(words)):
        tw(f"tl.fromTo('#w{k}_{i}',{{opacity:.4}},{{opacity:1,duration:.1}},{a - 0.067 + i * step:.3f});")
        if i == acc:
            tw(f"tl.fromTo('#w{k}_{i}',{{scale:.8}},{{scale:1,duration:.35,ease:'back.out(2.5)'}},{a - 0.067 + i * step:.3f});")

CSS = """
@font-face{font-family:GA;src:url(assets/fonts/GraphikArabic-Medium.woff2);font-weight:500}
@font-face{font-family:GA;src:url(assets/fonts/GraphikArabic-Bold.woff2);font-weight:700}
@font-face{font-family:GA;src:url(assets/fonts/GraphikArabic-Black.woff2);font-weight:900}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#05140F;font-family:GA,'Avenir Next',sans-serif;color:#fff}
#root{position:absolute;inset:0;overflow:hidden}
#cam{position:absolute;inset:0;transform-origin:50% 30%}
#camv{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.vig{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,20,15,.35) 0%,rgba(5,20,15,0) 22%,rgba(5,20,15,0) 58%,rgba(5,20,15,.7) 100%)}
#stage{position:absolute;inset:0;background:radial-gradient(circle at 50% 38%,#11402F 0%,#0A2A1F 38%,#05140F 78%);clip-path:circle(0% at 50% 50%)}
#stage::before{content:"";position:absolute;inset:0;opacity:.07;background-image:linear-gradient(#A7F3D0 1px,transparent 1px),linear-gradient(90deg,#A7F3D0 1px,transparent 1px);background-size:90px 90px}
.grp{position:absolute;inset:0}
.grp div,.grp svg{position:absolute}
.grp .glass div,.grp .row div,.grp .yrs span{position:relative}
.glass{border-radius:44px;background:linear-gradient(160deg,rgba(17,64,47,.95),rgba(10,42,31,.92));border:2px solid rgba(167,243,208,.45);
  box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 40px rgba(46,229,157,.18),inset 0 1px 0 rgba(255,255,255,.18)}
.glass.on{border-color:#2EE59D;box-shadow:0 0 70px rgba(46,229,157,.45),0 30px 80px rgba(0,0,0,.5)}
.photo{overflow:hidden;padding:0}
.grp .photo .ph{position:absolute;inset:16px;border-radius:30px;background:linear-gradient(135deg,#1d4a3a,#0b2219);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px}
.grp .ph svg{position:relative}
.phl{font-family:'Avenir Next';font-weight:700;letter-spacing:5px;font-size:24px;color:#A7F3D0;opacity:.85}
.lbl{direction:rtl;text-align:center;font-weight:900;font-size:60px}
.sub{position:relative;direction:ltr;text-align:center;font-family:'Avenir Next';font-weight:600;letter-spacing:8px;font-size:30px;color:#A7F3D0}
.row{display:flex;gap:22px;justify-content:center;margin-top:46px}
.disc,.disc2{width:120px;height:120px;border-radius:50%;background:#0E9F6E;display:flex;align-items:center;justify-content:center;box-shadow:0 0 40px rgba(46,229,157,.55)}
.disc2{background:#163F31;box-shadow:none}
.disc.red{background:#7f2a2a;box-shadow:0 0 40px rgba(248,113,113,.5)}
.pill{top:270px;left:50%;transform:translateX(-50%);direction:rtl;padding:14px 34px;border-radius:60px;background:rgba(10,42,31,.82);
  border:2px solid rgba(167,243,208,.55);box-shadow:0 0 30px rgba(46,229,157,.35);font-weight:700;font-size:38px;white-space:nowrap}
.pill i{font-style:normal;color:#2EE59D}
.nochip{left:340px;top:640px;width:400px;height:300px;border-radius:50px;background:rgba(10,42,31,.9);border:4px solid #F87171;color:#F87171;
  font-weight:900;font-size:200px;line-height:300px;text-align:center;direction:rtl;text-shadow:0 0 40px rgba(248,113,113,.6);box-shadow:0 0 80px rgba(248,113,113,.35)}
.chip2{direction:rtl;padding:12px 40px;border-radius:50px;background:#0E9F6E;font-weight:900;font-size:46px;box-shadow:0 0 40px rgba(46,229,157,.5)}
.ppg{left:130px;top:470px;width:820px;display:flex;flex-wrap:wrap;gap:30px;justify-content:center}
.grp .ppg .pp{position:relative;width:134px;height:134px;border-radius:50%;background:#163F31;border:2px solid rgba(167,243,208,.4);display:flex;align-items:center;justify-content:center}
.grp .pp svg{position:relative}
.half{top:0;width:540px;height:1920px}
.yrs{display:flex;flex-direction:row-reverse;justify-content:space-between;margin-top:22px;font-family:'Avenir Next';font-weight:700;font-size:34px;color:#A7F3D0}
.wm{position:relative;margin-top:50px;font-family:'Avenir Next';font-weight:800;letter-spacing:10px;font-size:54px;color:#fff;text-shadow:0 0 30px rgba(46,229,157,.7)}
.cap{position:absolute;left:70px;right:150px;top:1220px;text-align:center;direction:rtl;font:700 70px/1.3 GA;text-shadow:0 4px 18px rgba(0,0,0,.75);visibility:hidden}
.cap .cw{display:inline-block}
.cap .acc{font-weight:900;font-size:90px;color:#A7F3D0;text-shadow:0 0 28px rgba(46,229,157,.7),0 4px 18px rgba(0,0,0,.6)}
.cap .lat{font-family:'Avenir Next';font-weight:800;font-style:italic;direction:ltr}
"""
html = f"""<!doctype html>
<html lang="ar"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <div id="cam"><video id="camv" class="clip" src="assets/aroll.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0"></video><div class="vig"></div></div>
  <div id="stage"></div>
  {chr(10).join("  " + x for x in H)}
  <audio id="mix" class="clip" src="assets/voice.wav" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-volume="1"></audio>
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  gsap.set('.grp,.cap',{{autoAlpha:0}});
  {chr(10).join("  " + x for x in J)}
  tl.to({{}},{{duration:0.001}},{TOTAL - 0.01});
  window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>"""
os.makedirs(PROJ, exist_ok=True)
open(os.path.join(PROJ, "index.html"), "w", encoding="utf-8").write(html)
# screen-mix report
face = sum(OUTS[k][1] - OUTS[k][0] for k, s in enumerate(SEGS) if s[2] in FACE_BEATS)
img = sum(OUTS[k][1] - OUTS[k][0] for k, s in enumerate(SEGS) if s[2].startswith("img") or s[2] == "stress_img")
fb = OUTS[0][1] - OUTS[0][0]
print(f"total {TOTAL}s  faceB {fb:.1f}s ({fb / TOTAL:.0%})  faceA {face - fb:.1f}s ({(face - fb) / TOTAL:.0%})  "
      f"images {img:.1f}s ({img / TOTAL:.0%})  anim {TOTAL - face - img:.1f}s ({(TOTAL - face - img) / TOTAL:.0%})  caps {len(CAPS)}")
