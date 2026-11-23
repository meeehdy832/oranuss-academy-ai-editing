# Developed by Mehdi ORANUSS | Powered by Claude
"""Leverage reel «الرافعة المالية» (9:16, ≈47 s) from 6 Google Flow (Veo 3.1 Fast) clips of the AI advisor.
Hook → problem → solution (definition, rule, risk) → CTA. Style: josephswork-blue-ui layouts in royal blue (user request).
Layouts: FACE (full clip) · SPLIT (blue stage on top, face below) · TEXT (full blue stage).
usage: python3 -I gen_leverage.py [--media]"""
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "leverage")
AS = os.path.join(PROJ, "assets")
TOP = os.path.abspath(os.path.join(HERE, "..", ".."))
WK = os.path.join(TOP, "project", "work", "leverage-flow")
CL = os.path.join(TOP, "output", "leverage-flow", "clips")
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
END_HOLD = 2.6

# script per clip (what the advisor says; captions use these words, timed on whisper word starts)
SCRIPT = {
    1: "شي مقاولين كيكبرو البيزنس ديالهم بفلوس ماشي ديالهم وانت باقي كتسنى حتى تجمع الفلوس؟",
    2: "المشكل؟ يا إما كتخاف من الكريدي يا إما كتشدو وكتصرفو فالمصاريف وهنا كتطيح",
    3: "هادي هي الرافعة المالية تستعمل فلوس الآخرين باش تشري حاجة كتجيب ليك الربح",
    4: "القاعدة بسيطة إلا كان الربح اللي كتدخل ليك كثر من تكلفة الكريدي راك رابح",
    5: "ولكن عقل الرافعة كتكبّر الربح وكتكبّر حتى الخسارة ما تسلفش باش تخلص المصاريف",
    6: "بغيتي تعرف كيفاش تطبقها فالبيزنس ديالك؟ تابعنا وكتب ليا رافعة فالكومنتير",
}
# caption chunks per clip: (number of words, accent word index)
CHUNKS = {
    1: [(5, 2), (3, 0), (3, 2), (3, 2)],
    2: [(1, 0), (5, 4), (4, 2), (1, 0), (2, 1)],
    3: [(4, 2), (3, 1), (3, 2), (3, 2)],
    4: [(2, 1), (5, 2), (4, 3), (2, 1)],
    5: [(2, 1), (3, 2), (3, 2), (2, 1), (3, 2)],
    6: [(4, 3), (2, 0), (1, 0), (3, 2), (1, 0)],
}
# (clip, src_start, src_end, layout, beat)
SEGS = [
    (1, 0.15, 7.35, "face", "hook"),
    (2, 0.00, 7.55, "split", "problem"),
    (3, 0.00, 1.70, "text", "title"),
    (3, 1.70, 7.15, "split", "opm"),
    (4, 0.00, 7.20, "split", "rule"),
    (5, 0.00, 7.45, "split", "risk"),
    (6, 0.00, 2.85, "face", "cta1"),
    (6, 3.75, 6.80, "face", "cta2"),
]
OUTS, t = [], 0.0
for c, a, b, *_ in SEGS:
    OUTS.append((round(t, 3), round(t + b - a, 3))); t += b - a
VOICE_END = round(t, 3)
TOTAL = round(t + END_HOLD, 3)

def words_json(n):
    d = json.load(open(os.path.join(WK, f"scene-{n:02d}.json")))
    return [w for s in d["segments"] for w in s.get("words", [])]

def src_to_out(clip, ts):
    for k, (c, a, b, *_r) in enumerate(SEGS):
        if c == clip and a - 0.05 <= ts <= b + 0.05:
            return OUTS[k][0] + min(max(ts - a, 0), b - a)
    nxt = [(a, k) for k, (c, a, b, *_r) in enumerate(SEGS) if c == clip and a > ts]   # inside a cut gap → next kept part
    if nxt:
        return OUTS[min(nxt)[1]][0]
    prv = [k for k, (c, a, b, *_r) in enumerate(SEGS) if c == clip and b < ts]
    return OUTS[prv[-1]][1] if prv else None

def build_media():
    tmp = os.path.join(WK, "seg"); os.makedirs(tmp, exist_ok=True)
    lst = []
    for k, (c, a, b, *_r) in enumerate(SEGS):
        p = os.path.join(tmp, f"v{k:02d}.mp4")
        subprocess.run([FF, "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", os.path.join(CL, f"scene-{c:02d}.mp4"),
                        "-vf", "scale=1080:1920:flags=lanczos,eq=contrast=1.05:saturation=1.03,fps=30,setsar=1",
                        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", p], check=True)
        lst.append(p)
    open(os.path.join(tmp, "list.txt"), "w").write("".join(f"file '{p}'\n" for p in lst))
    os.makedirs(AS, exist_ok=True)
    subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"),
                    "-vf", f"tpad=stop_mode=clone:stop_duration={END_HOLD}", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "16", "-pix_fmt", "yuv420p", os.path.join(AS, "aroll.mp4")], check=True)
    ins, fl, parts = [], [], ""
    for k, (c, a, b, *_r) in enumerate(SEGS):
        ins += ["-i", os.path.join(CL, f"scene-{c:02d}.mp4")]
        fl.append(f"[{k}:a]aresample=48000,atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,"
                  f"afade=t=out:st={b - a - 0.03:.3f}:d=0.03[a{k}]")
        parts += f"[a{k}]"
    fl.append(parts + f"concat=n={len(SEGS)}:v=0:a=1[out]")
    subprocess.run([FF, "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fl), "-map", "[out]",
                    "-ar", "48000", "-ac", "1", os.path.join(WK, "voice_raw.wav")], check=True)
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
def slide(sel, t, dx=-120, d=0.45):
    tw(f"tl.fromTo('{sel}',{{x:{dx},opacity:0,filter:'blur(8px)'}},{{x:0,opacity:1,filter:'blur(0px)',duration:{d},ease:'expo.out'}},{t:.3f});")
def pop(sel, t, s0=0.4, d=0.5):
    tw(f"tl.fromTo('{sel}',{{scale:{s0},opacity:0}},{{scale:1,opacity:1,duration:{d},ease:'back.out(1.8)'}},{t:.3f});")
def slam(sel, t, s0=1.8):
    tw(f"tl.fromTo('{sel}',{{scale:{s0},opacity:0,filter:'blur(16px)'}},{{scale:1,opacity:1,filter:'blur(0px)',duration:.38,ease:'expo.out'}},{t:.3f});")

IC = {
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "cash": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
    "bank": '<path d="M3 10l9-6 9 6"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>',
    "factory": '<path d="M3 21V10l6 4V10l6 4V6h6v15z"/><path d="M7 17h2M12 17h2M17 17h2"/>',
    "up": '<path d="M12 20V5M5.5 11.5L12 5l6.5 6.5"/>',
    "down": '<path d="M12 4v15M5.5 12.5L12 19l6.5-6.5"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "receipt": '<path d="M5 3h14v18l-3-2-2 2-2-2-2 2-2-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
    "send": '<path d="M21 3L10 14"/><path d="M21 3l-7 18-4-7-7-4z"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "lever": '<path d="M2 18h20"/><path d="M12 18l-3-5h6z"/><path d="M3 9l18 4"/><circle cx="4" cy="6.5" r="2"/>',
}
def svg(name, size=80, sw=2.0, color="#fff"):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{IC[name]}</svg>')

PILL = '<div class="pill">الرافعة المالية <i>·</i> <span class="lt">LEVERAGE</span></div>'

# ---------------- layout state per beat ----------------
CLIP = {"face": "inset(0px 0px 1920px 0px)", "split": "inset(0px 0px 930px 0px)", "text": "inset(0px 0px 0px 0px)"}
CAMY = {"face": 0, "split": 770, "text": 0}
CAPY = {"face": 1330, "split": 1640, "text": 1330}
prev = None
for k, (c, a, b, lay, beat) in enumerate(SEGS):
    t0, t1 = OUTS[k]
    if lay != prev:
        d = 0.0 if k == 0 else 0.42
        tw(f"tl.to('#stage',{{clipPath:'{CLIP[lay]}',duration:{d},ease:'expo.inOut'}},{max(t0 - 0.12, 0):.3f});")
        tw(f"tl.to('#cam',{{y:{CAMY[lay]},duration:{d},ease:'expo.inOut'}},{max(t0 - 0.12, 0):.3f});")
        if k:
            sfx(t0, "WH-163" if lay == "text" else "WH-012", -3)
    if lay in ("face", "split") and (k == 0 or SEGS[k - 1][0] != c or lay != prev):
        tw(f"tl.fromTo('#camv',{{filter:'blur(12px)'}},{{filter:'blur(0px)',duration:.3,ease:'power2.out',immediateRender:false}},{t0:.3f});")
    if lay in ("face", "split"):
        z0, z1 = (1.0, 1.07) if k % 2 == 0 else (1.07, 1.0)
        tw(f"tl.fromTo('#camz',{{scale:{z0}}},{{scale:{z1},duration:{t1 - t0:.3f},ease:'sine.inOut',immediateRender:false}},{t0:.3f});")
    prev = lay
tw(f"tl.to('#stage',{{clipPath:'{CLIP['text']}',duration:.4,ease:'expo.inOut'}},{VOICE_END - 0.1:.3f});")
tw(f"tl.to('#cam',{{y:0,duration:.4}},{VOICE_END - 0.1:.3f});")

# word times (output timeline) per clip, script words spread over whisper word starts
WT = {}
for n, text in SCRIPT.items():
    sw = text.split(); ws = words_json(n); N, M = len(sw), len(ws)
    starts = [ws[min(int(i * M / N), M - 1)]["start"] for i in range(N)]
    if n == 1:
        starts[0] = max(starts[0], 0.27)
    WT[n] = (sw, starts, ws[-1]["end"])
def wt(n, i):
    """output time of the i-th script word of clip n"""
    return src_to_out(n, WT[n][1][i])

# ---------------- graphics per beat ----------------
for k, (c, a, b, lay, beat) in enumerate(SEGS):
    t0, t1 = OUTS[k]
    g = f"b{k}"
    if beat == "hook":
        h(PILL.replace('class="pill"', 'class="pill" id="hpill"'))
        tw(f"tl.set('#hpill',{{autoAlpha:1}},0);")
        pop("#hpill", 0.35, 0.7, 0.45); sfx(0.35, "PO-006", -8)
        tw(f"tl.to('#hpill',{{autoAlpha:0,duration:.2}},{t1 - 0.25:.3f});")
    elif beat == "problem":
        grp(g, t0, t1, PILL +
            '<div id="pc1" class="card" style="left:110px;top:380px;width:860px">'
            f'<div class="ico no">{svg("lock", 64, 2.4)}</div><div class="ct">كتخاف من <b>الكريدي</b></div></div>'
            '<div id="pc2" class="card" style="left:110px;top:600px;width:860px">'
            f'<div class="ico no">{svg("receipt", 64, 2.4)}</div><div class="ct">كتصرفو <b>فالمصاريف</b></div></div>'
            f'<div id="pdn" style="left:470px;top:790px">{svg("down", 140, 2.6, "#FF4D5E")}</div>')
        slide("#pc1", wt(2, 1), 140); sfx(wt(2, 1), "PO-006", -8)
        slide("#pc2", wt(2, 6), 140); sfx(wt(2, 6), "PO-006", -8)
        kt = wt(2, 11)
        pop("#pdn", kt, 0.3, 0.45); sfx(kt, "IM-003", -8)
        tw(f"tl.to('#pc1,#pc2',{{borderColor:'#FF4D5E',boxShadow:'0 0 60px rgba(255,77,94,.45)',duration:.25}},{kt:.3f});")
        tw(f"tl.to('#pc2',{{x:14,duration:.05,yoyo:true,repeat:5,ease:'none'}},{kt:.3f});")
    elif beat == "title":
        grp(g, t0, t1 + 0.05,
            f'<div id="tic" style="left:390px;top:520px">{svg("lever", 300, 1.3, "#93C5FD")}</div>'
            '<div id="tt1" class="tline big" style="top:880px">الرافعة <b>المالية</b></div>'
            '<div id="tt2" class="sub" style="position:absolute;left:0;right:0;top:1080px">LEVERAGE</div>', "grp tgrp")
        pop("#tic", t0 + 0.02, 0.5, 0.5)
        tw(f"tl.fromTo('#tic svg',{{rotation:-12}},{{rotation:6,duration:1.4,ease:'sine.inOut'}},{t0:.3f});")
        slam("#tt1", wt(3, 2), 1.5); sfx(wt(3, 2), "IM-003", -6)
        rise("#tt2", wt(3, 3), 30, 0.4)
    elif beat == "opm":
        grp(g, t0, t1, PILL +
            f'<div id="o1" class="node" style="left:720px;top:400px">{svg("bank", 90, 2)}<div class="nl">فلوس الآخرين</div></div>'
            f'<div id="o2" class="node" style="left:395px;top:400px">{svg("factory", 90, 2)}<div class="nl">حاجة كتنتج</div></div>'
            f'<div id="o3" class="node gr" style="left:70px;top:400px">{svg("cash", 90, 2)}<div class="nl">الربح</div></div>'
            '<svg id="oa1" style="position:absolute;left:675px;top:500px" width="80" height="60" viewBox="0 0 80 60"><path d="M74 30H10M30 12L10 30l20 18" stroke="#93C5FD" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>'
            '<svg id="oa2" style="position:absolute;left:350px;top:500px" width="80" height="60" viewBox="0 0 80 60"><path d="M74 30H10M30 12L10 30l20 18" stroke="#2DC58A" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>')
        t_a, t_b, t_c = wt(3, 5), wt(3, 8), wt(3, 12)
        rise("#o1", t_a - 0.1, 50, 0.45); sfx(t_a - 0.1, "PO-006", -8)
        tw(f"tl.to('#oa1 path',{{attr:{{'stroke-dashoffset':0}},duration:.4,ease:'power2.out'}},{t_b - 0.3:.3f});")
        rise("#o2", t_b, 50, 0.45); sfx(t_b, "PO-006", -8)
        tw(f"tl.to('#oa2 path',{{attr:{{'stroke-dashoffset':0}},duration:.4,ease:'power2.out'}},{t_c - 0.4:.3f});")
        pop("#o3", t_c, 0.4, 0.5); sfx(t_c, "PO-013", -6)
    elif beat == "rule":
        grp(g, t0, t1, PILL +
            '<div id="rb" class="glass" style="left:110px;top:350px;width:860px;height:560px">'
            '<div class="bars">'
            '<div class="bcol"><div id="bg1" class="bar gr"></div><div class="bl">الربح</div></div>'
            '<div class="bcol"><div id="bg2" class="bar rd"></div><div class="bl">تكلفة الكريدي</div></div>'
            '</div></div>'
            f'<div id="rok" class="okpill">{svg("check", 54, 3)}<span>راك رابح</span></div>')
        rise("#rb", t0, 50, 0.45); sfx(t0, "PO-006", -8)
        tw(f"tl.fromTo('#bg1',{{height:0}},{{height:330,duration:.8,ease:'expo.out'}},{wt(4, 4):.3f});")
        sfx(wt(4, 4), "PO-008", -8)
        tw(f"tl.fromTo('#bg2',{{height:0}},{{height:170,duration:.8,ease:'expo.out'}},{wt(4, 9):.3f});")
        sfx(wt(4, 9), "PO-008", -8)
        tr = wt(4, 12)
        pop("#rok", tr, 0.5, 0.45); sfx(tr, "PO-013", -5)
    elif beat == "risk":
        grp(g, t0, t1, PILL +
            '<div id="kup" class="glass" style="left:560px;top:380px;width:430px;height:380px">'
            f'<div class="kic gr">{svg("up", 110, 2.6, "#2DC58A")}</div><div class="kl">كتكبّر <b class="g">الربح</b></div></div>'
            '<div id="kdn" class="glass" style="left:90px;top:380px;width:430px;height:380px">'
            f'<div class="kic rd">{svg("up", 110, 2.6, "#FF4D5E")}</div><div class="kl">كتكبّر <b class="r">الخسارة</b></div></div>'
            f'<div id="kno" class="nopill">{svg("x", 50, 3)}<span>ما تسلفش للمصاريف</span></div>')
        t_p, t_l, t_n = wt(5, 2), wt(5, 6), wt(5, 9)
        rise("#kup", t_p, 50, 0.45); sfx(t_p, "PO-006", -8)
        tw(f"tl.fromTo('#kup .kic',{{y:30}},{{y:-10,duration:.9,ease:'expo.out'}},{t_p + 0.1:.3f});")
        rise("#kdn", t_l, 50, 0.45); sfx(t_l, "PO-006", -8)
        tw(f"tl.fromTo('#kdn .kic',{{y:30}},{{y:-10,duration:.9,ease:'expo.out'}},{t_l + 0.1:.3f});")
        tw(f"tl.to('#kdn',{{borderColor:'#FF4D5E',boxShadow:'0 0 70px rgba(255,77,94,.5)',duration:.3}},{t_l + 0.5:.3f});")
        slam("#kno", t_n, 1.5); sfx(t_n, "IM-003", -7)
    elif beat == "cta1":
        pass
    elif beat == "cta2":
        txt = "رافعة"
        grp(g, t0, t1 + 0.05,
            '<div id="cbox" class="cbox"><div class="cav">O</div><div class="cin"><span id="ctyp"></span><i id="ccur">|</i></div>'
            f'<div id="csend" class="csend">{svg("send", 44, 2.4)}</div></div>'
            f'<div id="cfol" class="folpill">{svg("plus", 40, 3)}<span>تابعنا</span></div>')
        pop("#cfol", t0 + 0.02, 0.5, 0.45); sfx(t0 + 0.02, "PO-006", -8)
        rise("#cbox", wt(6, 7) - 0.25, 60, 0.45); sfx(wt(6, 7) - 0.25, "WH-012", -8)
        ty = wt(6, 9) - 0.05
        for i in range(1, len(txt) + 1):
            tw(f"tl.set('#ctyp',{{textContent:'{txt[:i]}'}},{ty + (i - 1) * 0.09:.3f});")
        sfx(ty, "UI-001", -10)
        tw(f"tl.to('#ccur',{{opacity:0,duration:.01,repeat:9,yoyo:true,repeatDelay:.25}},{t0:.3f});")
        tw(f"tl.to('#csend',{{scale:1.18,background:'#2563EB',duration:.12,yoyo:true,repeat:1}},{ty + 0.75:.3f});")
        sfx(ty + 0.75, "PO-013", -8)

# end card
grp("endg", VOICE_END - 0.05, TOTAL + 0.2,
    f'<div id="eic" style="left:440px;top:470px">{svg("lever", 200, 1.3, "#93C5FD")}</div>'
    '<div id="e1" class="tline" style="top:740px">كتب <b>رافعة</b></div>'
    '<div id="e2" class="tline sm" style="top:920px">فالكومنتير</div>'
    '<div id="endc" class="glass" style="left:190px;top:1180px;width:700px;height:200px;text-align:center">'
    '<div class="wm">ORANUSS ACADEMY</div><div class="sub" style="margin-top:14px">BUSINESS · DARIJA</div></div>', "grp tgrp")
pop("#eic", VOICE_END + 0.02, 0.5); slam("#e1", VOICE_END + 0.15, 1.4); rise("#e2", VOICE_END + 0.45, 30, 0.4)
rise("#endc", VOICE_END + 0.8, 40, 0.6)
sfx(VOICE_END + 0.15, "IM-003", -6); sfx(VOICE_END + 0.8, "LO-003", -8, 1.8)

# ---------------- captions ----------------
CAPS = []
for k, (c, a, b, lay, beat) in enumerate(SEGS):
    if lay == "text":
        continue
    sw, starts, s_end = WT[c]
    i = 0
    for nw, acc in CHUNKS[c]:
        j = i + nw
        s0 = starts[i]; s1 = starts[j] if j < len(sw) else s_end + 0.25
        if a - 0.01 <= s0 < b:
            st, en = src_to_out(c, s0), src_to_out(c, min(s1, b))
            CAPS.append((st, en, sw[i:j], acc, CAPY[lay], [src_to_out(c, x) for x in starts[i:j]]))
        i = j
for k, (a, b, words, acc, y, wts) in enumerate(CAPS):
    if k + 1 < len(CAPS):
        b = min(b, CAPS[k + 1][0] - 0.05)
    sp = "".join(f'<span id="w{k}_{i}" class="cw{" acc" if i == acc else ""}">{w}</span> ' for i, w in enumerate(words))
    h(f'<div id="cap{k}" class="cap" style="top:{y}px">{sp}</div>')
    tw(f"tl.set('#cap{k}',{{autoAlpha:1}},{a - 0.067:.3f});tl.set('#cap{k}',{{autoAlpha:0}},{b:.3f});")
    tw(f"tl.fromTo('#cap{k}',{{y:18}},{{y:0,duration:.3,ease:'expo.out'}},{a - 0.067:.3f});")
    for i, wt_ in enumerate(wts):
        tw(f"tl.fromTo('#w{k}_{i}',{{opacity:.4}},{{opacity:1,duration:.1}},{wt_ - 0.05:.3f});")
        if i == acc:
            tw(f"tl.fromTo('#w{k}_{i}',{{scale:.8}},{{scale:1,duration:.35,ease:'back.out(2.5)'}},{wt_ - 0.05:.3f});")

CSS = """
@font-face{font-family:GA;src:url(assets/fonts/GraphikArabic-Medium.woff2);font-weight:500}
@font-face{font-family:GA;src:url(assets/fonts/GraphikArabic-Bold.woff2);font-weight:700}
@font-face{font-family:GA;src:url(assets/fonts/GraphikArabic-Black.woff2);font-weight:900}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#050B2E;font-family:GA,'Avenir Next',sans-serif;color:#fff}
#root{position:absolute;inset:0;overflow:hidden}
#cam{position:absolute;inset:0}
#camz{position:absolute;inset:0;transform-origin:50% 30%}
#camv{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.vig{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,11,46,.25) 0%,rgba(5,11,46,0) 20%,rgba(5,11,46,0) 55%,rgba(5,11,46,.7) 100%)}
#stage{position:absolute;inset:0;background:radial-gradient(circle at 50% 22%,#2F5BFF 0%,#1A36C9 32%,#0B1A6B 70%,#050B2E 100%);clip-path:inset(0px 0px 1920px 0px)}
#stage::before{content:"";position:absolute;inset:0;opacity:.07;background-image:linear-gradient(#BFDBFE 1px,transparent 1px),linear-gradient(90deg,#BFDBFE 1px,transparent 1px);background-size:90px 90px}
#stage::after{content:"";position:absolute;left:0;right:0;top:986px;height:4px;background:#60A5FA;box-shadow:0 0 24px #3B82F6}
.grp{position:absolute;inset:0;visibility:hidden}
.grp>div,.grp>svg{position:absolute}
.glass{border-radius:44px;background:linear-gradient(160deg,rgba(30,58,190,.92),rgba(11,26,107,.92));border:2px solid rgba(147,197,253,.5);
  box-shadow:0 30px 80px rgba(0,0,0,.5),0 0 40px rgba(59,130,246,.25),inset 0 1px 0 rgba(255,255,255,.2)}
.card{height:170px;border-radius:36px;background:#fff;color:#0B1A6B;display:flex;flex-direction:row-reverse;align-items:center;gap:34px;padding:0 40px;box-sizing:border-box;
  box-shadow:0 20px 60px rgba(5,11,46,.45);border:3px solid transparent;direction:ltr}
.card .ct{direction:rtl;font-weight:900;font-size:58px;flex:1;text-align:right}
.card .ct b{color:#FF4D5E}
.ico{width:110px;height:110px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none}
.ico.no{background:#FF4D5E;box-shadow:0 0 30px rgba(255,77,94,.5)}
.node{width:290px;height:300px;border-radius:40px;background:linear-gradient(160deg,rgba(30,58,190,.95),rgba(11,26,107,.95));border:2px solid rgba(147,197,253,.55);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;box-shadow:0 24px 60px rgba(0,0,0,.45)}
.node.gr{border-color:#2DC58A;box-shadow:0 0 60px rgba(45,197,138,.5)}
.nl{direction:rtl;font-weight:900;font-size:44px;text-align:center}
.node.gr .nl{color:#7CF0C0}
.pill{position:absolute;top:240px;left:50%;transform:translateX(-50%);direction:rtl;padding:12px 34px;border-radius:60px;background:rgba(11,26,107,.85);
  border:2px solid rgba(147,197,253,.6);box-shadow:0 0 30px rgba(59,130,246,.45);font-weight:700;font-size:36px;white-space:nowrap}
.pill i{font-style:normal;color:#60A5FA} .pill .lt{font-family:'Avenir Next';font-weight:700;letter-spacing:4px;font-size:28px;color:#BFDBFE}
#hpill{visibility:hidden}
.tline{left:60px;right:60px;text-align:center;direction:rtl;font-weight:900;font-size:110px;line-height:1.2}
.tline.big{font-size:130px} .tline.sm{font-size:80px;color:#BFDBFE}
.tline b{color:#93C5FD;text-shadow:0 0 36px rgba(59,130,246,.9)}
.sub{direction:ltr;text-align:center;font-family:'Avenir Next';font-weight:600;letter-spacing:12px;font-size:34px;color:#BFDBFE}
.bars{position:absolute;left:0;right:0;bottom:40px;height:470px;display:flex;direction:rtl;justify-content:center;align-items:flex-end;gap:180px}
.bcol{display:flex;flex-direction:column;align-items:center;gap:20px}
.bar{width:190px;height:0;border-radius:24px 24px 8px 8px}
.bar.gr{background:linear-gradient(180deg,#5EEAB4,#2DC58A);box-shadow:0 0 50px rgba(45,197,138,.55)}
.bar.rd{background:linear-gradient(180deg,#FF8A95,#FF4D5E);box-shadow:0 0 40px rgba(255,77,94,.45)}
.bl{direction:rtl;font-weight:900;font-size:44px;white-space:nowrap}
.gt{position:absolute;left:0;right:0;top:120px;text-align:center;font-family:'Avenir Next';font-weight:800;font-size:120px;color:#fff;text-shadow:0 0 30px rgba(59,130,246,.9)}
.okpill,.nopill,.folpill{left:50%;top:930px;transform:translate(-50%,-50%);display:flex;flex-direction:row-reverse;align-items:center;gap:18px;padding:18px 42px;border-radius:80px;
  font-weight:900;font-size:54px;white-space:nowrap;direction:ltr}
.okpill{background:#2DC58A;box-shadow:0 0 60px rgba(45,197,138,.7)}
.nopill{top:880px;background:#FF4D5E;box-shadow:0 0 60px rgba(255,77,94,.7)}
.kic{position:relative;margin:50px auto 0;width:170px;height:170px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.kic.gr{background:rgba(45,197,138,.15);border:3px solid #2DC58A} .kic.rd{background:rgba(255,77,94,.15);border:3px solid #FF4D5E}
.kl{position:relative;direction:rtl;text-align:center;font-weight:900;font-size:58px;margin-top:30px}
.kl b{font-weight:900} .kl b.g{color:#2DC58A} .kl b.r{color:#FF4D5E}
.cbox{left:70px;top:1080px;width:940px;height:150px;border-radius:80px;background:#fff;display:flex;align-items:center;gap:24px;padding:0 22px;box-sizing:border-box;
  box-shadow:0 24px 70px rgba(5,11,46,.55);direction:ltr}
.cav{width:104px;height:104px;border-radius:50%;background:linear-gradient(160deg,#2F5BFF,#0B1A6B);color:#fff;font-family:'Avenir Next';font-weight:800;font-size:50px;
  display:flex;align-items:center;justify-content:center;flex:none}
.cin{flex:1;direction:rtl;text-align:right;color:#0B1A6B;font-weight:900;font-size:62px}
.cin i{font-style:normal;color:#2563EB;font-weight:500}
.csend{width:104px;height:104px;border-radius:50%;background:#1A36C9;display:flex;align-items:center;justify-content:center;flex:none}
.folpill{top:300px;background:#fff;color:#0B1A6B;box-shadow:0 0 50px rgba(59,130,246,.6)}
.folpill svg{stroke:#1A36C9}
.wm{position:relative;margin-top:44px;font-family:'Avenir Next';font-weight:800;letter-spacing:10px;font-size:50px;color:#fff;text-shadow:0 0 30px rgba(59,130,246,.9)}
.cap{position:absolute;left:60px;right:60px;text-align:center;direction:rtl;font:700 70px/1.3 GA;text-shadow:0 4px 18px rgba(0,0,0,.85);visibility:hidden}
.cap .cw{display:inline-block}
.cap .acc{font-weight:900;font-size:90px;color:#93C5FD;text-shadow:0 0 28px rgba(59,130,246,.95),0 4px 18px rgba(0,0,0,.6)}
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
json.dump({"total": TOTAL, "cues": sorted(CUES)}, open(os.path.join(WK, "sfx_cues.json"), "w"))
mix = {}
for k, s in enumerate(SEGS):
    mix[s[3]] = mix.get(s[3], 0) + OUTS[k][1] - OUTS[k][0]
mix["text"] = mix.get("text", 0) + END_HOLD
print(f"total {TOTAL}s · " + " · ".join(f"{k} {v:.1f}s ({v / TOTAL:.0%})" for k, v in mix.items()) + f" · caps {len(CAPS)} · sfx {len(CUES)}")
