# Developed by Mehdi ORANUSS | Powered by Claude
"""Generates the HyperFrames project hf/ai-editing-v2 (AI Editing launch v2, 16:9, rendered at 4K):
glass + glossy-3D purple look from the user's style board (reference/styles/long/purple-3d-glass/), same voiceover,
same word timings and audio premix as v1 (project/build_ai_editing.py, assets/mix.wav).
Writes index.html and compositions/*.html as static HTML (every element authored, GSAP timelines per scene)."""
import ast, os, sys, html
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from styles.purple_glass import chunk_words

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "ai-editing-v2")
COMP = os.path.join(PROJ, "compositions")
os.makedirs(COMP, exist_ok=True)

# ---------- words + scene cuts, read from the v1 build so both versions stay in sync ----------
src = ast.parse(open(os.path.join(HERE, "..", "build_ai_editing.py")).read())
V = {}
for node in src.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ("RAW", "SENT_END", "KEYWORDS"):
        V[node.targets[0].id] = ast.literal_eval(node.value)
SPEECH_END, TOTAL, LEAD = 58.30, 60.5, 0.067
SC = [0.0, 5.55, 11.45, 13.95, 18.75, 23.0, 27.1, 29.45, 32.3, 38.3, 43.25, 49.35, 53.85, SPEECH_END + 0.05, TOTAL]
toks = V["RAW"].split()
WORDS = []
for t, wd in zip(toks[::2], toks[1::2]):
    WORDS.append([float(t), None, wd.replace("|", " ")])
for i, wd in enumerate(WORDS):
    nxt = WORDS[i + 1][0] if i + 1 < len(WORDS) else SPEECH_END
    ends = [e for e in V["SENT_END"] if wd[0] < e <= nxt]
    wd[1] = min(ends[0] if ends else nxt, wd[0] + 1.2)
WORDS = [tuple(x) for x in WORDS]

# ---------- icons (24x24 line glyphs) ----------
IC = {
    "play": '<path d="M7 4.5v15l12.5-7.5z" fill="currentColor" stroke="none"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "star": '<path d="m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z" fill="currentColor" stroke="none"/>',
    "cart": '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.6 12.2a2 2 0 0 0 2 1.6h8.2a2 2 0 0 0 2-1.5L21.5 7H6"/>',
    "megaphone": '<path d="m3 11 16-6v14L3 13z"/><path d="M11.5 16.5a3 3 0 1 1-5.6-2"/>',
    "briefcase": '<rect x="2.5" y="7" width="19" height="13" rx="2.5"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M2.5 13h19"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "building": '<rect x="4" y="2.5" width="16" height="19" rx="2"/><path d="M9 21.5v-4h6v4M8.5 7h1M14.5 7h1M8.5 11h1M14.5 11h1"/>',
    "coins": '<circle cx="9" cy="9" r="6"/><path d="M18.1 10.4A6 6 0 1 1 10.3 18M8 7h1.5v4"/>',
    "chip": '<rect x="5" y="5" width="14" height="14" rx="2.5"/><rect x="9" y="9" width="6" height="6" rx="1"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M19 9h3M19 15h3M2 9h3M2 15h3"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/>',
    "up": '<path d="M7 17 17 7M8 7h9v9"/>',
    "film": '<rect x="2.5" y="3" width="19" height="18" rx="2.5"/><path d="M7 3v18M17 3v18M2.5 12h19M2.5 7.5H7M2.5 16.5H7M17 7.5h4.5M17 16.5h4.5"/>',
    "seat": '<path d="M7 13V6.5A3.5 3.5 0 0 1 10.5 3h3A3.5 3.5 0 0 1 17 6.5V13"/><rect x="4.5" y="12" width="15" height="5" rx="2"/><path d="M7 17v4M17 17v4"/>',
    "layers": '<path d="m12 2.5 9.5 5-9.5 5-9.5-5z"/><path d="m2.5 12 9.5 5 9.5-5M2.5 16.5l9.5 5 9.5-5"/>',
    "id": '<rect x="3" y="4.5" width="18" height="15" rx="2.5"/><circle cx="9" cy="11" r="2.2"/><path d="M5.5 16.5a3.6 3.6 0 0 1 7 0M15 9.5h3M15 13h3"/>',
    "cap": '<path d="m22 9.5-10-5-10 5 10 5z"/><path d="M6 11.5V16c3.5 3 8.5 3 12 0v-4.5M22 9.5v5"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="m12 15-3-3a22 22 0 0 1 2-4A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M21.5 20a6.5 6.5 0 0 0-4-6"/>',
    "spark": '<path d="M12 2c.6 4.6 2.4 6.4 7 7-4.6.6-6.4 2.4-7 7-.6-4.6-2.4-6.4-7-7 4.6-.6 6.4-2.4 7-7z" fill="currentColor" stroke="none"/>',
}
def icon(name, size, color="#fff", sw=2.2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" style="color:{color}">{IC[name]}</svg>')

# ---------- scene builder ----------
class Scene:
    def __init__(self, sid, start, end, exit="blur"):
        self.sid, self.start, self.end, self.exit = sid, start, end, exit
        self.html, self.js, self.n, self.last = [], [], 0, {}
    def t(self, word_t):           # scene-local time of a graphic for a word spoken at word_t
        return round(max(0.05, word_t - LEAD - self.start), 3)
    def lt(self, local):
        return round(local, 3)
    def id(self, name):
        return f"{self.sid}-{name}"
    def box(self, name, x, y, w, h, cls, inner="", style=""):
        """Absolutely placed element centred at (x, y)."""
        self.html.append(f'<div id="{self.id(name)}" class="{cls}" style="left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;'
                         f'width:{w}px;height:{h}px;{style}">{inner}</div>')
        return "#" + self.id(name)
    def raw(self, s):
        self.html.append(s)
    def tw(self, s):
        self.js.append(s)
    # entrances
    def up(self, sel, t, d=40, dur=0.8):
        self.tw(f"tl.fromTo('{sel}',{{opacity:0,y:{d},filter:'blur(8px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{dur},ease:'expo.out'}},{t});")
    def side(self, sel, t, dx=-90, dur=0.8):
        self.tw(f"tl.fromTo('{sel}',{{opacity:0,x:{dx},filter:'blur(10px)'}},{{opacity:1,x:0,filter:'blur(0px)',duration:{dur},ease:'expo.out'}},{t});")
    def pop(self, sel, t, s0=0.4, ease="back.out(1.6)", dur=0.6):
        self.tw(f"tl.fromTo('{sel}',{{opacity:0,scale:{s0}}},{{opacity:1,scale:1,duration:{dur},ease:'{ease}'}},{t});")
    def blurin(self, sel, t, dur=0.45):
        self.tw(f"tl.fromTo('{sel}',{{opacity:0,scale:1.06,filter:'blur(14px)'}},{{opacity:1,scale:1,filter:'blur(0px)',duration:{dur},ease:'power4.out'}},{t});")
    def tilt(self, sel, t, ry0=-38, rx0=18, ry=-14, rx=6, dur=1.1):
        self.last[sel] = (round(t + dur, 3), {"rotationY": ry, "rotationX": rx})
        self.tw(f"tl.fromTo('{sel}',{{opacity:0,rotationY:{ry0},rotationX:{rx0},scale:.8}},{{opacity:1,rotationY:{ry},rotationX:{rx},scale:1,duration:{dur},ease:'expo.out'}},{t});")
    def words(self, sel_prefix, n, t, gap=0.067):
        for i in range(n):
            self.tw(f"tl.fromTo('{sel_prefix}{i}',{{opacity:0,filter:'blur(8px)'}},{{opacity:1,filter:'blur(0px)',duration:.16,ease:'power2.out'}},{t + i * gap:.3f});")
    def drift(self, sel, t, prop="rotationY", to=10, dur=None):
        """Slow constant turn after the object has landed (absolute end value, starts after its entrance)."""
        t_end, vals = self.last.get(sel, (t, {}))
        t = max(t, t_end)
        base = vals.get(prop, 0)
        dur = dur or max(0.5, (self.end - self.start) - t - 0.35)
        self.tw(f"tl.to('{sel}',{{{prop}:{base + to},duration:{dur:.2f},ease:'none'}},{t:.3f});")
    def write(self):
        dur = round(self.end - self.start, 3)
        ex = {"blur": "{opacity:0,scale:.965,filter:'blur(12px)',duration:.32,ease:'power3.in'}",
              "left": "{opacity:0,x:-180,filter:'blur(14px)',duration:.32,ease:'power3.in'}",
              "up": "{opacity:0,y:-120,filter:'blur(12px)',duration:.32,ease:'power3.in'}",
              "zoom": "{opacity:0,scale:1.25,filter:'blur(16px)',duration:.34,ease:'power3.in'}",
              "none": None}[self.exit]
        exit_js = f"tl.to('#{self.sid}-w',{ex},{dur - 0.34:.3f});" if ex else ""
        body = "\n      ".join(self.html)
        js = "\n    ".join(self.js)
        out = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
  </style>
  <div id="root" data-composition-id="{self.sid}" data-width="1920" data-height="1080" data-layout-allow-overlap>
    <div id="{self.sid}-w" class="stage">
      {body}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {js}
    {exit_js}
    tl.to({{}}, {{duration: 0.001}}, {dur - 0.01:.3f});
    window.__timelines["{self.sid}"] = tl;
  </script>
</template>
"""
        open(os.path.join(COMP, f"{self.sid}.html"), "w").write(out)

# ---------- reusable pieces ----------
def glass(S, name, x, y, w, h, inner="", r=36, extra=""):
    return S.box(name, x, y, w, h, "glass", inner, f"border-radius:{r}px;{extra}")
def gloss(S, name, x, y, w, h, ic=None, r=30, kind="", isz=None, inner=""):
    isz = isz or int(min(w, h) * 0.46)
    ico = f'<div class="gl-ic">{icon(ic, isz)}</div>' if ic else ""
    return S.box(name, x, y, w, h, f"gloss {kind}", ico + inner, f"border-radius:{r}px")
def sphere(S, name, x, y, d, kind=""):
    return S.box(name, x, y, d, d, f"sphere {kind}")
def chip(S, name, x, y, text, lead=None, kind="", fs=30, h=72):
    """Label pill like the style board ('01 UI Motion'): glass pill, purple badge with a number or icon, ink text."""
    w = int(len(text) * fs * 0.6 + h + 70)
    badge = (f'<span class="badge {kind}" style="width:{h - 16}px;height:{h - 16}px;font-size:{fs * 0.85:.0f}px">'
             f'{icon(lead, int(h * 0.42)) if lead and lead in IC else html.escape(lead or "")}</span>') if lead else ""
    return S.box(name, x, y, w, h, "chip", f'{badge}<span class="chip-t" style="font-size:{fs}px">{html.escape(text)}</span>',
                 f"border-radius:{h // 2}px")
def title(S, name, x, y, text, fs=96, w=1400, color=None, align="center", weight=800):
    parts = text.split(" ")
    spans = " ".join(f'<span id="{S.id(name)}-{i}" class="tw">{html.escape(p)}</span>' for i, p in enumerate(parts))
    col = f"color:{color};" if color else ""
    S.box(name, x, y, w, int(fs * 1.3), "title", spans, f"font-size:{fs}px;text-align:{align};font-weight:{weight};{col}")
    return f"#{S.id(name)}-", len(parts)
def skel(S, name, x, y, w, h=18, light=False):
    return S.box(name, x, y, w, h, "skel" + (" light" if light else ""), "", f"border-radius:{h // 2}px")
def phone(S, name, x, y, h, screen_html, dark=False):
    w = round(h * 0.49)
    inner = (f'<div class="ph-screen{" dark" if dark else ""}">{screen_html}</div><div class="ph-island"></div>')
    return S.box(name, x, y, w, h, "phone", inner)
def avatar(S, name, x, y, d, kind=""):
    face = ('<svg viewBox="0 0 100 100" width="100%" height="100%" style="position:absolute;left:0;top:0">'
            '<circle cx="50" cy="40" r="19" fill="#fff" fill-opacity=".95"/><path d="M14 104 C14 68 86 68 86 104Z" fill="#fff" fill-opacity=".95"/></svg>')
    return S.box(name, x, y, d, d, f"avatar {kind}", face)

scenes = []

# S01 0-5.55: launch. "W akhiran 9derna ntel9ou t-tadrib dyal AI Editing f Oranuss Academy"
S = Scene("s01", SC[0], SC[1], "zoom"); scenes.append(S)
chip(S, "new", 470, 300, "Jdid", "rocket"); S.pop(f"#{S.id('new')}", S.t(0.97), 0.6, "back.out(1.4)")
S.raw(f'<div id="{S.id("ttl")}" class="title hero" style="left:120px;top:360px;width:900px;height:200px">'
      f'<span id="{S.id("ttl")}-0" class="tw"><span class="grad">AI</span></span> <span id="{S.id("ttl")}-1" class="tw">Editing</span></div>')
S.tw(f"tl.fromTo('#{S.id('ttl')}-0',{{opacity:0,filter:'blur(10px)',y:20}},{{opacity:1,filter:'blur(0px)',y:0,duration:.5,ease:'expo.out'}},{S.t(2.47)});")
S.tw(f"tl.fromTo('#{S.id('ttl')}-1',{{opacity:0,filter:'blur(10px)',y:20}},{{opacity:1,filter:'blur(0px)',y:0,duration:.5,ease:'expo.out'}},{S.t(3.04)});")
S.box("sub", 470, 600, 700, 70, "subtitle", 'f <b>Oranuss Academy</b>', "text-align:left;left:120px")
S.up(f"#{S.id('sub')}", S.t(4.27), 24)
S.box("bar", 220, 660, 200, 10, "accent-bar"); S.side(f"#{S.id('bar')}", S.t(4.27) + 0.12, -40)
# hero: glass card with a glossy 3D play tile, selection frame and a cursor (style board 02), rocket launch line art (17)
S.raw(f'<div class="persp" style="left:1060px;top:150px;width:720px;height:720px">')
glass(S, "card", 360, 360, 600, 600, "", 48)
S.raw("</div>")
S.tilt(f"#{S.id('card')}", S.t(0.56), -30, 14, -12, 5, 1.2); S.drift(f"#{S.id('card')}", 1.4, "rotationY", 6)
S.raw(f'<div class="persp" style="left:1060px;top:150px;width:720px;height:720px">')
gloss(S, "play", 360, 370, 300, 300, "play", 64, "", 140)
S.raw("</div>")
S.tilt(f"#{S.id('play')}", S.t(2.47), -40, 20, -14, 8, 1.0); S.drift(f"#{S.id('play')}", S.t(2.47) + 1.0, "rotationY", 8)
S.box("frame", 1420, 520, 400, 400, "sel-frame",
      "".join(f'<i class="h" style="left:{a}%;top:{b}%"></i>' for a, b in ((0, 0), (100, 0), (0, 100), (100, 100))))
S.pop(f"#{S.id('frame')}", S.t(3.04), 0.85, "expo.out", 0.5)
S.box("cur", 1640, 720, 80, 80, "cursor", '<svg viewBox="0 0 24 24" width="80" height="80"><path d="M4 2.5 20 11l-7 1.8-3.3 7z" fill="#fff" stroke="#3B1C8C" stroke-width="1.6" stroke-linejoin="round"/></svg>')
S.tw(f"tl.fromTo('#{S.id('cur')}',{{opacity:0,x:220,y:160}},{{opacity:1,x:0,y:0,duration:.7,ease:'power3.out'}},{S.t(2.9)});")
S.tw(f"tl.to('#{S.id('cur')}',{{scale:.86,duration:.08,yoyo:true,repeat:1,ease:'power2.out'}},{S.t(3.04) + 0.62:.3f});")
S.raw(f'<svg id="{S.id("rk")}" class="rocket-line" viewBox="0 0 1920 1080" width="1920" height="1080">'
      f'<path id="{S.id("trail")}" d="M1120 860 C 1180 760, 1250 700, 1330 610" />'
      f'</svg>')
gloss(S, "rkg", 1340, 590, 130, 130, "rocket", 34, "", 66)   # glossy rocket tile rides the trail, then launches
S.tw(f"(()=>{{const p=document.querySelector('#{S.id('trail')}');const L=p.getTotalLength();gsap.set(p,{{strokeDasharray:L,strokeDashoffset:L}});"
     f"tl.to(p,{{strokeDashoffset:0,duration:.6,ease:'power2.out'}},{S.t(0.97)});"
     f"tl.fromTo('#{S.id('rkg')}',{{opacity:0,x:-220,y:270,scale:.6,rotation:-12}},{{opacity:1,x:0,y:0,scale:1,rotation:0,duration:.6,ease:'power2.out'}},{S.t(0.97)});"
     f"tl.to('#{S.id('rkg')}',{{x:520,y:-700,scale:.55,rotation:10,duration:.75,ease:'power3.in'}},{S.t(0.97) + 0.6:.3f});"
     f"tl.to(p,{{opacity:0,duration:.4}},{S.t(0.97) + 1.0:.3f});}})();")
S.box("ac", 1420, 865, 290, 64, "chip mini", f'<span class="chip-t" style="font-size:30px">Oranuss Academy</span>', "border-radius:32px")
S.up(f"#{S.id('ac')}", S.t(4.27) + 0.15, 20)
for i, (x, y, d) in enumerate(((1000, 260, 70), (1800, 820, 110))):
    sphere(S, f"o{i}", x, y, d); S.pop(f"#{S.id(f'o{i}')}", S.t(2.47) + 0.2 + i * 0.1, 0.2, "expo.out", 0.9)

# S02 5.55-11.45: "... tntej 3adad kbir mn l-videos b-nafs l-uslub w-l-hawiya dyalk"
S = Scene("s02", SC[1], SC[2], "up"); scenes.append(S)
p, n = title(S, "ttl", 960, 140, "3adad kbir mn l-videos", 78); S.words(p, n, S.t(7.62), 0.09)
tints = ["#FFD9C2", "#CDE3FF", "#FFE9A8", "#C9F2DD", "#FFC9D2", "#D9D0FF", "#CDE3FF", "#FFD9C2", "#C9F2DD", "#FFE9A8", "#FFC9D2", "#D9D0FF"]
S.raw(f'<div class="persp iso-wrap" style="left:160px;top:230px;width:1600px;height:560px"><div id="{S.id("grid")}" class="iso-grid">')
for i in range(12):
    c, r = i % 6, i // 6
    S.raw(f'<div id="{S.id(f"v{i}")}" class="vcard glass" style="left:{c * 262}px;top:{r * 250}px">'
          f'<div class="thumb" style="background:{tints[i]}"><div id="{S.id(f"u{i}")}" class="thumb-u"></div>'
          f'<div class="tplay">{icon("play", 26)}</div><div id="{S.id(f"b{i}")}" class="brand-dot">O</div></div>'
          f'<div class="skel" style="position:absolute;left:18px;bottom:22px;width:140px;height:14px;border-radius:7px"></div></div>')
S.raw("</div></div>")
S.tw(f"tl.fromTo('#{S.id('grid')}',{{rotationX:38,rotationZ:-10,y:60,opacity:0}},{{rotationX:30,rotationZ:-8,y:0,opacity:1,duration:1.4,ease:'expo.out'}},{S.t(8.38)});")
S.tw(f"tl.to('#{S.id('grid')}',{{rotationZ:-4,duration:{SC[2] - SC[1] - S.t(8.38) - 1.6:.2f},ease:'none'}},{S.t(8.38) + 1.4:.3f});")
for i in range(12):
    S.up(f"#{S.id(f'v{i}')}", S.t(8.38) + i * 0.06, 50, 0.7)
    S.tw(f"tl.fromTo('#{S.id(f'u{i}')}',{{opacity:0}},{{opacity:1,duration:.35,ease:'power2.inOut'}},{S.t(9.63) + i * 0.035:.3f});")
    S.pop(f"#{S.id(f'b{i}')}", S.t(10.52) + i * 0.04, 0.2, "back.out(2)", 0.45)
chip(S, "c1", 740, 860, "Nafs l-uslub", "layers"); S.pop(f"#{S.id('c1')}", S.t(9.63), 0.7, "expo.out", 0.5)
chip(S, "c2", 1180, 860, "Nafs l-hawiya", "id"); S.pop(f"#{S.id('c2')}", S.t(10.52), 0.7, "expo.out", 0.5)

# S03 11.45-13.95: "sawa2 mo7tawa twil awla mo7tawa 9sir"
S = Scene("s03", SC[2], SC[3], "left"); scenes.append(S)
S.raw('<div class="persp" style="left:180px;top:150px;width:960px;height:660px">')
S.box("mon", 480, 300, 860, 500, "glass monitor",
      f'<div class="mon-in"><div id="{S.id("mplay")}" class="gloss round" style="left:345px;top:150px;width:130px;height:130px">'
      f'<div class="gl-ic">{icon("play", 56)}</div></div><div class="track"><div id="{S.id("prog")}" class="track-fill"></div></div></div>',
      "border-radius:34px")
S.raw("</div>")
S.tilt(f"#{S.id('mon')}", S.t(11.88), 30, 10, 10, 4, 1.0); S.drift(f"#{S.id('mon')}", S.t(11.88) + 1.0, "rotationY", -4)
S.pop(f"#{S.id('mplay')}", S.t(12.43), 0.4, "back.out(1.6)")
S.tw(f"tl.fromTo('#{S.id('prog')}',{{scaleX:0}},{{scaleX:1,duration:{SC[3] - SC[2] - S.t(12.43) - 0.3:.2f},ease:'none'}},{S.t(12.43)});")
chip(S, "l1", 660, 860, "Mo7tawa twil", "16:9", fs=30); S.up(f"#{S.id('l1')}", S.t(12.43), 24)
sphere(S, "or", 1230, 450, 150, "label-sphere"); S.raw(f'<div id="{S.id("ort")}" class="sphere-t" style="left:1155px;top:425px;width:150px">awla</div>')
S.pop(f"#{S.id('or')}", S.t(12.78), 0.3); S.pop(f"#{S.id('ort')}", S.t(12.78), 0.3)
S.raw('<div class="persp" style="left:1350px;top:120px;width:460px;height:720px">')
phone(S, "ph", 230, 350, 620, f'<div id="{S.id("pplay")}" class="gloss round" style="left:95px;top:230px;width:110px;height:110px"><div class="gl-ic">{icon("play", 46)}</div></div>')
S.raw("</div>")
S.tilt(f"#{S.id('ph')}", S.t(13.48), -40, 10, -12, 4, 0.9)
chip(S, "l2", 1580, 860, "Mo7tawa 9sir", "9:16", fs=30); S.up(f"#{S.id('l2')}", S.t(13.48), 24)

# S04 13.95-18.75: "W-l-ahamm ... tdereb d-dakaa l-istina3i 3la l-mo7tawa dyalk"
S = Scene("s04", SC[3], SC[4], "blur"); scenes.append(S)
chip(S, "imp", 960, 110, "L-ahamm", "star", "gold"); S.pop(f"#{S.id('imp')}", S.t(13.96), 0.6, "expo.out", 0.5)
glass(S, "panel", 1260, 500, 620, 640, "", 48); S.up(f"#{S.id('panel')}", S.t(15.81), 60, 0.9)
S.raw(f'<svg id="{S.id("ring")}" class="ring" viewBox="0 0 400 400" style="left:1060px;top:230px;width:400px;height:400px">'
      f'<defs><linearGradient id="{S.id("rg")}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C4B5FD"/><stop offset=".5" stop-color="#8B5CF6"/><stop offset="1" stop-color="#5B21B6"/></linearGradient></defs>'
      f'<circle cx="200" cy="200" r="160" class="ring-track"/><circle id="{S.id("arc")}" cx="200" cy="200" r="160" class="ring-arc" stroke="url(#{S.id("rg")})" transform="rotate(-90 200 200)"/></svg>')
S.blurin(f"#{S.id('ring')}", S.t(16.14))
S.tw(f"(()=>{{const c=document.querySelector('#{S.id('arc')}');const L=2*Math.PI*160;gsap.set(c,{{strokeDasharray:L,strokeDashoffset:L}});"
     f"tl.to(c,{{strokeDashoffset:0,duration:2.0,ease:'power2.inOut'}},{S.t(16.14) + 0.3:.3f});}})();")
S.raw('<div class="persp" style="left:1060px;top:230px;width:400px;height:400px">')
gloss(S, "chip", 200, 200, 190, 190, "chip", 46, "", 92)
S.raw("</div>")
S.tilt(f"#{S.id('chip')}", S.t(16.14) + 0.1, -50, 25, -10, 10, 1.0); S.drift(f"#{S.id('chip')}", S.t(16.14) + 1.1, "rotationY", 20)
S.box("ptxt", 1260, 730, 560, 50, "label-t", "Tdereb d-dakaa l-istina3i", "font-size:32px"); S.up(f"#{S.id('ptxt')}", S.t(16.65), 20)
S.box("ok", 1440, 290, 86, 86, "okdot", icon("check", 46, "#fff", 3)); S.pop(f"#{S.id('ok')}", 18.35 - S.start, 0.3, "back.out(2)", 0.5)
for i, tint in enumerate(("#FFD9C2", "#CDE3FF", "#C9F2DD")):
    y = 330 + i * 160
    S.box(f"c{i}", 470, y, 420, 130, "glass vrow",
          f'<div class="thumb sm" style="background:{tint}"><div class="tplay sm">{icon("play", 20)}</div></div>'
          f'<div class="skel" style="position:absolute;left:170px;top:40px;width:180px;height:16px;border-radius:8px"></div>'
          f'<div class="skel" style="position:absolute;left:170px;top:74px;width:120px;height:12px;border-radius:6px"></div>', "border-radius:28px")
    S.side(f"#{S.id(f'c{i}')}", S.t(17.92) + i * 0.08, -100)
S.raw(f'<svg class="flow" viewBox="0 0 1920 1080" width="1920" height="1080">' + "".join(
    f'<path id="{S.id(f"f{i}")}" d="M690 {330 + i * 160} C 820 {330 + i * 160}, 880 {430 + (i - 1) * 40}, 1040 {430 + (i - 1) * 40}"/>' for i in range(3)) + "</svg>")
for i in range(3):
    S.tw(f"(()=>{{const p=document.querySelector('#{S.id(f'f{i}')}');const L=p.getTotalLength();gsap.set(p,{{strokeDasharray:L,strokeDashoffset:L}});"
         f"tl.to(p,{{strokeDashoffset:0,duration:.55,ease:'power2.inOut'}},{S.t(17.92) + 0.3 + i * 0.1:.3f});}})();")
S.box("mine", 470, 830, 520, 50, "label-t", "3la l-mo7tawa dyalk", "font-size:34px;color:#6D28D9"); S.up(f"#{S.id('mine')}", S.t(17.92), 20)

# S05 18.75-23.0: "bach twelli tntej videos b-jawda 3alya w-b-tari9a i7tirafiya" - isometric laptop (12)
S = Scene("s05", SC[4], SC[5], "left"); scenes.append(S)
S.raw('<div class="persp far" style="left:460px;top:250px;width:1000px;height:760px">'
      f'<div id="{S.id("lap")}" class="laptop"><div class="lap-base"><div class="keys"></div><div class="pad"></div></div>'
      f'<div class="lap-screen"><div class="lap-display"><div id="{S.id("lp")}" class="gloss round" style="left:270px;top:150px;width:140px;height:140px"><div class="gl-ic">{icon("play", 60)}</div></div>'
      f'<div class="track lap-track"><div id="{S.id("lprog")}" class="track-fill"></div></div></div></div></div></div>')
S.tw(f"tl.fromTo('#{S.id('lap')}',{{opacity:0,rotationX:62,rotationZ:-50,y:120}},{{opacity:1,rotationX:55,rotationZ:-38,y:0,duration:1.2,ease:'expo.out'}},{S.t(19.47)});")
S.drift(f"#{S.id('lap')}", S.t(19.47) + 1.2, "rotationZ", 6)
S.pop(f"#{S.id('lp')}", S.t(19.93), 0.4)
S.tw(f"tl.fromTo('#{S.id('lprog')}',{{scaleX:0}},{{scaleX:1,duration:{SC[5] - SC[4] - S.t(19.93) - 0.4:.2f},ease:'none'}},{S.t(19.93)});")
chip(S, "q", 1450, 300, "Jawda 3alya", "check", "green", fs=34, h=84); S.pop(f"#{S.id('q')}", S.t(20.65), 0.6, "expo.out", 0.55)
chip(S, "pro", 470, 720, "I7tirafiya", "star", "gold", fs=34, h=84); S.pop(f"#{S.id('pro')}", S.t(21.52), 0.6, "expo.out", 0.55)
for i, (x, y) in enumerate(((1600, 230), (1680, 360), (380, 640))):
    S.box(f"sp{i}", x, y, 44, 44, "sparkle", icon("spark", 44, "#A78BFA")); S.pop(f"#{S.id(f'sp{i}')}", S.t(20.65 if i < 2 else 21.52) + 0.1 + i * 0.06, 0, "back.out(3)", 0.5)
S.box("plant", 1480, 700, 160, 220, "plant", '<div class="pot"></div><div class="leaf l1"></div><div class="leaf l2"></div><div class="leaf l3"></div>')
S.up(f"#{S.id('plant')}", S.t(19.93) + 0.2, 40)

# S06 23.0-27.1: "Had l-mahara wellat mn bin ktar l-maharat l-matlouba 7aliyan" - chart (04 / 11)
S = Scene("s06", SC[5], SC[6], "zoom"); scenes.append(S)
glass(S, "panel", 960, 470, 1180, 680, "", 48); S.up(f"#{S.id('panel')}", S.t(23.33), 60, 0.9)
S.box("pt", 640, 182, 600, 60, "label-t", "L-maharat l-matlouba", "font-size:42px;text-align:left;font-weight:800")
S.up(f"#{S.id('pt')}", S.t(25.04), 20)
S.raw(f'<div class="gridlines" style="left:430px;top:270px;width:1060px;height:440px"></div>')
hs = [0.34, 0.48, 0.96, 0.58, 0.80, 0.66]
for i, hh in enumerate(hs):
    x = 520 + i * 176; h = int(420 * hh)
    S.box(f"b{i}", x, 710 - h / 2, 112, h, "bar" + (" hero" if i == 2 else ""), "", "transform-origin:50% 100%")
    S.tw(f"tl.fromTo('#{S.id(f'b{i}')}',{{scaleY:0}},{{scaleY:1,duration:.9,ease:'power3.out'}},{S.t(24.41) + i * 0.07:.3f});")
    S.box(f"bl{i}", x, 745, 80, 14, "skel")
S.raw(f'<svg class="trend" viewBox="0 0 1920 1080" width="1920" height="1080"><defs><linearGradient id="{S.id("lg")}" x1="0" x2="1"><stop offset="0" stop-color="#C4B5FD"/><stop offset="1" stop-color="#6D28D9"/></linearGradient></defs>'
      f'<path id="{S.id("tr")}" d="M470 640 C 640 600, 720 520, 870 470 S 1180 360, 1420 250" stroke="url(#{S.id("lg")})"/>'
      f'<path id="{S.id("ah")}" d="M1380 240 L1424 248 L1408 290" class="ahead"/></svg>')
S.tw(f"(()=>{{const p=document.querySelector('#{S.id('tr')}');const L=p.getTotalLength();gsap.set(p,{{strokeDasharray:L,strokeDashoffset:L}});"
     f"tl.to(p,{{strokeDashoffset:0,duration:1.1,ease:'power2.inOut'}},{S.t(25.04)});}})();")
S.pop(f"#{S.id('ah')}", S.t(25.04) + 1.0, 0.3, "back.out(2)", 0.4)
chip(S, "ai", 872, 262, "AI Editing", "up", fs=28, h=68); S.pop(f"#{S.id('ai')}", S.t(25.76), 0.6, "expo.out", 0.5)
chip(S, "now", 1360, 182, "7aliyan", "up", "green", fs=28, h=64); S.pop(f"#{S.id('now')}", S.t(26.48), 0.6, "expo.out", 0.5)

# S07 27.1-29.45: "W-t9der tstaghelha b-toro9 mokhtalifa" - process animation (10)
S = Scene("s07", SC[6], SC[7], "blur"); scenes.append(S)
S.raw('<div class="persp" style="left:760px;top:120px;width:400px;height:300px">')
gloss(S, "core", 200, 150, 200, 200, "chip", 48, "", 96)
S.raw("</div>")
S.tilt(f"#{S.id('core')}", S.t(27.16), -40, 20, -12, 8); S.drift(f"#{S.id('core')}", S.t(27.16) + 1.0, "rotationY", 12)
S.box("coret", 960, 400, 400, 50, "label-t", "AI Editing", "font-size:36px;font-weight:800"); S.up(f"#{S.id('coret')}", S.t(27.16) + 0.1, 16)
S.raw(f'<svg class="flow dash" viewBox="0 0 1920 1080" width="1920" height="1080">' + "".join(
    f'<path id="{S.id(f"k{i}")}" d="M960 440 C 960 520, {x} 500, {x} 580"/>' for i, x in enumerate((520, 960, 1400))) + "</svg>")
for i, (x, kind) in enumerate(((520, ""), (960, "violet"), (1400, "deep"))):
    S.tw(f"(()=>{{const p=document.querySelector('#{S.id(f'k{i}')}');const L=p.getTotalLength();gsap.set(p,{{strokeDasharray:'10 12',strokeDashoffset:L}});"
         f"tl.fromTo(p,{{opacity:0}},{{opacity:1,duration:.2}},{S.t(28.40)});tl.to(p,{{strokeDashoffset:0,duration:1.6,ease:'none'}},{S.t(28.40)});}})();")
    glass(S, f"t{i}", x, 720, 360, 230, "", 34); S.up(f"#{S.id(f't{i}')}", S.t(28.40) + i * 0.08, 50)
    gloss(S, f"n{i}", x - 110, 690, 96, 96, None, 26, kind, inner=f'<div class="gl-num">{i + 1}</div>')
    S.pop(f"#{S.id(f'n{i}')}", S.t(28.40) + 0.15 + i * 0.08, 0.4)
    skel(S, f"s{i}a", x + 40, 668, 140, 18); skel(S, f"s{i}b", x + 20, 708, 180, 14); skel(S, f"s{i}c", x, 770, 280, 14)
    for k in "abc":
        S.up(f"#{S.id(f's{i}{k}')}", S.t(28.40) + 0.2 + i * 0.08, 10, 0.5)
p, n = title(S, "ttl", 960, 900 - 20, "B-toro9 mokhtalifa", 60); S.words(p, n, S.t(28.40), 0.44)

# S08-S10 share a stepper (style board labels "01 UI Motion" ...)
def stepper(S, active):
    S.box("stl", 960, 100, 420, 6, "step-line", "")
    for i in range(3):
        on = i + 1 == active
        S.box(f"st{i}", 800 + i * 160, 100, 120 if on else 84, 120 if on else 84, "step" + (" on" if on else (" done" if i + 1 < active else "")),
              f'<span>{i + 1:02d}</span>', "border-radius:50%")
        if on:
            S.pop(f"#{S.id(f'st{i}')}", 0.05, 0.5, "back.out(1.8)", 0.55)
        else:
            S.blurin(f"#{S.id(f'st{i}')}", 0.05)

S = Scene("s08", SC[7], SC[8], "left"); scenes.append(S)
stepper(S, 1)
p, n = title(S, "ttl", 960, 250, "Ttawwer l-mo7tawa dyalk", 72); S.words(p, n, S.t(29.54), 0.08)
for k, (x, ic, lab, t0, kind) in enumerate(((690, "user", "Ch-chakhsi", 30.93, ""), (1230, "briefcase", "T-tijari", 31.66, "deep"))):
    glass(S, f"g{k}", x, 580, 400, 400, "", 44); S.up(f"#{S.id(f'g{k}')}", S.t(t0), 60)
    S.raw(f'<div class="persp" style="left:{x - 150}px;top:380px;width:300px;height:300px">')
    gloss(S, f"i{k}", 150, 150, 220, 220, ic, 54, kind, 104)
    S.raw("</div>")
    S.tilt(f"#{S.id(f'i{k}')}", S.t(t0) + 0.08, -40 if k == 0 else 40, 20, -10 if k == 0 else 10, 6)
    S.drift(f"#{S.id(f'i{k}')}", S.t(t0) + 1.1, "rotationY", 6 if k == 0 else -6)
    S.box(f"l{k}", x, 720, 360, 56, "label-t", lab, "font-size:40px;font-weight:800"); S.up(f"#{S.id(f'l{k}')}", S.t(t0) + 0.12, 16)
sphere(S, "or", 960, 580, 120, "label-sphere"); S.raw(f'<div id="{S.id("ort")}" class="sphere-t" style="left:900px;top:560px;width:120px;font-size:26px">awla</div>')
S.pop(f"#{S.id('or')}", S.t(31.48), 0.3); S.pop(f"#{S.id('ort')}", S.t(31.48), 0.3)

# S09 32.3-38.3: products: "t9addem 9ima idafiya l-l-khadamat w-l-mountajat dyalk, tsta3melha bach tsewwe9 l-mountajat lli katbi3"
S = Scene("s09", SC[8], SC[9], "left"); scenes.append(S)
stepper(S, 2)
glass(S, "prod", 640, 560, 520, 680, "", 44); S.up(f"#{S.id('prod')}", 0.1, 60)
S.box("pimg", 640, 450, 440, 330, "pimg", "", "border-radius:30px"); S.up(f"#{S.id('pimg')}", 0.18, 40)
S.raw('<div class="persp" style="left:490px;top:300px;width:300px;height:300px">')
gloss(S, "cart", 150, 150, 200, 200, "cart", 50, "warm", 104)
S.raw("</div>")
S.tilt(f"#{S.id('cart')}", 0.3, -40, 20, -12, 8); S.drift(f"#{S.id('cart')}", 1.4, "rotationY", 12)
skel(S, "pk1", 600, 660, 360, 22); skel(S, "pk2", 570, 705, 300, 16)
S.up(f"#{S.id('pk1')}", 0.3, 10); S.up(f"#{S.id('pk2')}", 0.36, 10)
chip(S, "val", 800, 230, "+ 9ima idafiya", "spark", "green", fs=30); S.pop(f"#{S.id('val')}", S.t(32.75), 0.6, "expo.out", 0.5)
S.box("tabs", 640, 800, 440, 76, "seg", f'<div id="{S.id("knob")}" class="seg-knob"></div><span class="seg-a">Khadamat</span><span class="seg-b">Mountajat</span>', "border-radius:38px")
S.up(f"#{S.id('tabs')}", S.t(33.64), 20)
S.tw(f"tl.fromTo('#{S.id('knob')}',{{x:0}},{{x:212,duration:.45,ease:'power3.inOut'}},{S.t(34.22)});")
S.tw(f"tl.to('#{S.id('tabs')} .seg-a',{{color:'#1B1240',duration:.2}},{S.t(34.22) + 0.1:.3f});tl.to('#{S.id('tabs')} .seg-b',{{color:'#ffffff',duration:.2}},{S.t(34.22) + 0.1:.3f});")
S.raw('<div class="persp" style="left:1130px;top:150px;width:460px;height:760px">')
phone(S, "ph", 230, 380, 700,
      f'<div class="reel"><div class="reel-img"></div><div id="{S.id("rp")}" class="gloss round" style="left:110px;top:250px;width:100px;height:100px"><div class="gl-ic">{icon("play", 44)}</div></div>'
      f'<div class="skel light" style="position:absolute;left:30px;bottom:110px;width:200px;height:16px;border-radius:8px"></div>'
      f'<div class="skel light" style="position:absolute;left:30px;bottom:80px;width:140px;height:12px;border-radius:6px"></div></div>', dark=True)
S.raw("</div>")
S.tilt(f"#{S.id('ph')}", S.t(35.56), -40, 10, -14, 4, 1.0); S.drift(f"#{S.id('ph')}", S.t(35.56) + 1.0, "rotationY", 6)
S.raw('<div class="persp" style="left:1500px;top:180px;width:260px;height:260px">')
gloss(S, "mega", 130, 130, 170, 170, "megaphone", 44, "warm", 84)
S.raw("</div>")
S.tilt(f"#{S.id('mega')}", S.t(36.48), 40, 20, 12, 6, 0.9)
S.raw(f'<svg class="waves" viewBox="0 0 1920 1080" width="1920" height="1080">' + "".join(
    f'<path id="{S.id(f"w{i}")}" d="M{1735 + i * 26} {225 - i * 18} q {40 + i * 16} {80 + i * 18} 0 {160 + i * 36}"/>' for i in range(3)) + "</svg>")
for i in range(3):
    S.tw(f"tl.fromTo('#{S.id(f'w{i}')}',{{opacity:0}},{{opacity:1,duration:.2,ease:'power2.out'}},{S.t(36.48) + 0.25 + i * 0.1:.3f});")
chip(S, "sold", 1360, 860, "Katbi3", "cart", "green", fs=32, h=76); S.pop(f"#{S.id('sold')}", S.t(37.83), 0.6, "expo.out", 0.5)

# S10 38.3-43.25: "awla t7awwelha l-khidma mousta9illa t9addemha l-ch-charikat w-l-achkhas w-terba7 menha"
S = Scene("s10", SC[9], SC[10], "zoom"); scenes.append(S)
stepper(S, 3)
glass(S, "svc", 600, 540, 520, 600, "", 44); S.up(f"#{S.id('svc')}", S.t(39.15), 60)
S.raw('<div class="persp" style="left:450px;top:290px;width:300px;height:300px">')
gloss(S, "bc", 150, 150, 220, 220, "briefcase", 54, "", 108)
S.raw("</div>")
S.tilt(f"#{S.id('bc')}", S.t(39.15) + 0.1, -40, 20, -10, 8); S.drift(f"#{S.id('bc')}", S.t(39.15) + 1.2, "rotationY", 10)
S.box("svt", 600, 650, 460, 60, "label-t", "L-khidma", "font-size:46px;font-weight:800"); S.up(f"#{S.id('svt')}", S.t(39.15) + 0.12, 16)
S.box("svs", 600, 715, 460, 50, "label-t", "mousta9illa", "font-size:40px;color:#6D28D9;font-weight:700"); S.up(f"#{S.id('svs')}", S.t(39.66), 16)
glass(S, "cl", 1270, 460, 640, 440, "", 40); S.up(f"#{S.id('cl')}", S.t(40.34), 60)
for i, (lab, t0, ic) in enumerate((("Ch-charikat", 40.91, "building"), ("L-achkhas", 41.58, "users"))):
    y = 350 + i * 150
    S.box(f"r{i}", 1270, y, 570, 118, "row", "", "border-radius:28px"); S.side(f"#{S.id(f'r{i}')}", S.t(t0), 80)
    gloss(S, f"ri{i}", 1050, y, 80, 80, ic, 22, "deep" if i else "", 40); S.pop(f"#{S.id(f'ri{i}')}", S.t(t0) + 0.08, 0.4)
    S.box(f"rt{i}", 1250, y, 260, 50, "label-t", lab, "font-size:36px;text-align:left;font-weight:700"); S.side(f"#{S.id(f'rt{i}')}", S.t(t0) + 0.1, 40)
    S.box(f"rs{i}", 1490, y, 64, 64, "send", icon("send", 30, "#6D28D9")); S.pop(f"#{S.id(f'rs{i}')}", S.t(t0) + 0.2, 0.3)
S.raw('<div class="persp" style="left:1060px;top:640px;width:260px;height:260px">')
S.box("coins", 130, 130, 200, 200, "coins", "".join(f'<div class="coin" style="top:{110 - k * 26}px"></div>' for k in range(4)))
S.raw("</div>")
S.tilt(f"#{S.id('coins')}", S.t(42.44), -30, 30, -10, 20, 0.9)
chip(S, "earn", 1450, 770, "Terba7", "up", "green", fs=36, h=84); S.pop(f"#{S.id('earn')}", S.t(42.44) + 0.08, 0.6, "expo.out", 0.5)

# S11 43.25-49.35: "W-7na ghadi n3allmouk kifach dir had chi khatwa b-khatwa mn khilal tadrib tatbi9i w-b-jawda 3alya"
S = Scene("s11", SC[10], SC[11], "left"); scenes.append(S)
rows = "".join(f'<div class="lesson" style="top:{330 + i * 108}px"><div class="ln">{i + 1:02d}</div>'
               f'<div class="skel" style="position:absolute;left:96px;top:26px;width:150px;height:14px;border-radius:7px"></div>'
               f'<div class="skel" style="position:absolute;left:96px;top:52px;width:100px;height:10px;border-radius:5px"></div>'
               f'<div id="{S.id(f"ck{i}")}" class="okdot sm">{icon("check", 22, "#fff", 3)}</div></div>' for i in range(4))
course = (f'<div class="course-hd"><div class="gl-ic small">{icon("cap", 40)}</div><div class="course-t">AI Editing</div>'
          f'<div class="course-s">Oranuss Academy</div></div>{rows}')
S.raw('<div class="persp" style="left:330px;top:100px;width:480px;height:860px">')
phone(S, "ph", 240, 420, 800, course)
S.raw("</div>")
S.tilt(f"#{S.id('ph')}", 0.1, -40, 12, -14, 4, 1.1); S.drift(f"#{S.id('ph')}", 1.2, "rotationY", 6)
for i, t0 in enumerate((45.82, 46.06, 46.40, 46.75)):
    S.pop(f"#{S.id(f'ck{i}')}", S.t(t0), 0.2, "back.out(2.2)", 0.45)
S.box("pre", 1300, 260, 700, 50, "label-t", "N3allmouk kifach", "font-size:38px;color:#7A72A0;font-weight:600"); S.up(f"#{S.id('pre')}", S.t(43.98), 16)
p, n = title(S, "ttl", 1300, 360, "Khatwa b-khatwa", 92, 900); S.words(p, n, S.t(45.82), 0.24)
# isometric steps building with each "khatwa"
for i in range(3):
    S.box(f"step{i}", 1130 + i * 120, 600 - i * 40, 150, 90 + i * 60, "stepblock", "", "transform-origin:50% 100%")
    S.tw(f"tl.fromTo('#{S.id(f'step{i}')}',{{opacity:0,scaleY:0}},{{opacity:1,scaleY:1,duration:.5,ease:'expo.out'}},{S.t((45.82, 46.06, 46.40)[i])});")
chip(S, "tt", 1560, 520, "Tadrib tatbi9i", "play", fs=32, h=80); S.pop(f"#{S.id('tt')}", S.t(47.18), 0.6, "expo.out", 0.5)
chip(S, "jq", 1560, 640, "Jawda 3alya", "star", "gold", fs=32, h=80); S.pop(f"#{S.id('jq')}", S.t(48.28), 0.6, "expo.out", 0.5)

# S12 49.35-53.85: "Ila bghiti ttawwer l-maharat dyalk w-tkoun mn n-nas lli ghadi ystafdou mn had l-forsa"
S = Scene("s12", SC[11], SC[12], "up"); scenes.append(S)
chip(S, "grow", 960, 190, "Ttawwer l-maharat dyalk", "up", "green", fs=36, h=88); S.pop(f"#{S.id('grow')}", S.t(49.93), 0.6, "expo.out", 0.5)
glass(S, "row", 960, 490, 1160, 320, "", 160); S.up(f"#{S.id('row')}", S.t(51.12), 60)
kinds = ["a1", "a2", "a3", "a4", "a5", "a6"]
for i, dx in enumerate((-430, -290, -150, 150, 290, 430)):
    avatar(S, f"a{i}", 960 + dx, 490, 130, kinds[i]); S.pop(f"#{S.id(f'a{i}')}", S.t(51.61) + abs(dx) / 1400, 0.4, "back.out(1.6)", 0.5)
avatar(S, "me", 960, 490, 190, "me"); S.pop(f"#{S.id('me')}", S.t(51.12), 0.4, "back.out(1.6)", 0.6)
S.box("met", 960, 620, 130, 56, "me-tag", "Nta", "border-radius:26px"); S.pop(f"#{S.id('met')}", S.t(51.12) + 0.15, 0.5)
chip(S, "ch", 960, 790, "L-forsa", "star", "gold", fs=40, h=96); S.pop(f"#{S.id('ch')}", S.t(53.52), 0.6, "expo.out", 0.5)
for i, (x, y) in enumerate(((800, 740), (1130, 760), (1180, 700))):
    S.box(f"sp{i}", x, y, 40, 40, "sparkle", icon("spark", 40, "#F5B83D")); S.pop(f"#{S.id(f'sp{i}')}", S.t(53.52) + 0.1 + i * 0.07, 0, "back.out(3)", 0.5)

# S13 53.85-58.35: "tewasel m3ana daba w-7jez l-blasa dyalk 9bel ma tkmel l-ma9a3id"
S = Scene("s13", SC[12], SC[13], "blur"); scenes.append(S)
glass(S, "card", 960, 470, 1180, 760, "", 52); S.up(f"#{S.id('card')}", 0.05, 60, 0.9)
S.box("ct", 760, 170, 700, 70, "label-t", "7jez l-blasa dyalk", "font-size:56px;text-align:left;font-weight:800"); S.up(f"#{S.id('ct')}", S.t(55.40), 20)
S.box("warn", 1290, 170, 520, 50, "label-t", "9bel ma tkmel l-ma9a3id", "font-size:32px;color:#E0527A;font-weight:700"); S.up(f"#{S.id('warn')}", S.t(56.69), 16)
mine = (1, 3); k = 0
for r in range(3):
    for c in range(8):
        x = 540 + c * 120; y = 300 + r * 125
        if (r, c) == mine:
            S.box("mine", x, y, 96, 96, "seat", icon("seat", 60, "#6D28D9", 2.4), "border-radius:24px")
            S.up(f"#{S.id('mine')}", 0.15 + k * 0.012, 14, 0.5)
            S.tw(f"tl.to('#{S.id('mine')}',{{background:'linear-gradient(145deg,#6EE7B7,#10B981)',scale:1.12,duration:.35,ease:'back.out(2)'}},{S.t(55.72)});")
            S.tw(f"tl.to('#{S.id('mine')} svg',{{stroke:'#fff',duration:.2}},{S.t(55.72)});")
        else:
            S.box(f"s{k}", x, y, 96, 96, "seat", icon("seat", 60, "#8B5CF6", 2.4), "border-radius:24px")
            S.up(f"#{S.id(f's{k}')}", 0.15 + k * 0.012, 14, 0.5)
            order = (k * 7) % 24
            S.tw(f"tl.to('#{S.id(f's{k}')}',{{background:'linear-gradient(145deg,#A78BFA,#6D28D9)',duration:.25,ease:'power2.out'}},{S.t(56.69) + order * 0.045:.3f});")
            S.tw(f"tl.to('#{S.id(f's{k}')} svg',{{stroke:'#fff',duration:.2}},{S.t(56.69) + order * 0.045:.3f});")
        k += 1
S.box("btn", 960, 720, 640, 110, "gloss btn", f'<div class="btn-in">{icon("send", 40)}<span>Tewasel m3ana daba</span></div>', "border-radius:55px")
S.up(f"#{S.id('btn')}", 0.2, 30)
S.tw(f"tl.to('#{S.id('btn')}',{{scale:.94,duration:.09,yoyo:true,repeat:1,ease:'power2.out'}},{S.t(54.83) + 0.067:.3f});")
S.box("cur", 1180, 790, 84, 84, "cursor", '<svg viewBox="0 0 24 24" width="84" height="84"><path d="M4 2.5 20 11l-7 1.8-3.3 7z" fill="#fff" stroke="#3B1C8C" stroke-width="1.6" stroke-linejoin="round"/></svg>')
S.tw(f"tl.fromTo('#{S.id('cur')}',{{opacity:0,x:260,y:200}},{{opacity:1,x:0,y:0,duration:.55,ease:'power3.out'}},{S.t(54.50)});")
S.tw(f"tl.to('#{S.id('cur')}',{{opacity:0,duration:.3}},{S.t(55.40)});")

# END 58.35-60.5: parallax mountains (16) + mark + wordmark
S = Scene("s14", SC[13], SC[14], "none"); scenes.append(S)
S.box("sun", 1500, 800, 240, 240, "sun", "", "border-radius:50%"); S.up(f"#{S.id('sun')}", 0.3, 80, 1.2)
for i in range(3):
    S.box(f"m{i}", 960, 1000 - i * 40, 2400, 520, f"mount m{i}", "")
    S.tw(f"tl.fromTo('#{S.id(f'm{i}')}',{{y:{260 + i * 120},opacity:0}},{{y:0,opacity:1,duration:{1.1 + i * 0.15:.2f},ease:'expo.out'}},{0.05 + i * 0.08:.2f});")
    S.tw(f"tl.to('#{S.id(f'm{i}')}',{{x:{-20 - i * 25},duration:2.0,ease:'none'}},0.2);")
S.raw('<div class="persp" style="left:860px;top:150px;width:200px;height:200px">')
gloss(S, "mark", 100, 100, 170, 170, "cap", 46, "", 90)
S.raw("</div>")
S.tilt(f"#{S.id('mark')}", 0.15, -60, 30, -8, 6, 1.0); S.drift(f"#{S.id('mark')}", 1.2, "rotationY", 10)
S.box("wm", 960, 420, 1400, 120, "wordmark", "ORANUSS ACADEMY")
S.tw(f"tl.fromTo('#{S.id('wm')}',{{opacity:0,scale:1.12,filter:'blur(14px)'}},{{opacity:1,scale:1,filter:'blur(0px)',duration:.9,ease:'expo.out'}},0.35);")
chip(S, "ae", 960, 540, "AI Editing", "film", fs=36, h=88); S.pop(f"#{S.id('ae')}", 0.6, 0.6, "expo.out", 0.5)
S.box("cta", 960, 640, 900, 60, "label-t", "7jez l-blasa dyalk daba", "font-size:40px;color:#5B4A99;font-weight:600"); S.up(f"#{S.id('cta')}", 0.8, 20)

for S in scenes:
    S.write()

# ---------- background (bg), section wipes (fx), captions ----------
open(os.path.join(COMP, "bg.html"), "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
  </style>
  <div id="root" data-composition-id="bg" data-width="1920" data-height="1080" data-layout-ignore>
    <div class="bg-base"></div>
    <div id="bg-g1" class="bg-glow g1"></div>
    <div id="bg-g2" class="bg-glow g2"></div>
    <div id="bg-g3" class="bg-glow g3"></div>
    <div class="bg-grid"></div>
    <div id="bg-o1" class="sphere bgo" style="left:-60px;top:760px;width:260px;height:260px"></div>
    <div id="bg-o2" class="sphere bgo soft" style="left:1720px;top:-70px;width:220px;height:220px"></div>
    <div id="bg-o3" class="sphere bgo soft" style="left:1780px;top:860px;width:120px;height:120px"></div>
    <div id="bg-o4" class="sphere bgo soft" style="left:90px;top:80px;width:90px;height:90px"></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.to('#bg-g1', {{x: 260, y: 80, duration: {TOTAL}, ease: 'none'}}, 0);
    tl.to('#bg-g2', {{x: -220, y: -60, duration: {TOTAL}, ease: 'none'}}, 0);
    tl.to('#bg-g3', {{x: 120, y: -140, duration: {TOTAL}, ease: 'none'}}, 0);
    tl.to('#bg-o1', {{x: 90, y: -50, rotation: 30, duration: {TOTAL}, ease: 'none'}}, 0);
    tl.to('#bg-o2', {{x: -70, y: 60, duration: {TOTAL}, ease: 'none'}}, 0);
    tl.to('#bg-o3', {{x: -50, y: -40, duration: {TOTAL}, ease: 'none'}}, 0);
    tl.to('#bg-o4', {{x: 40, y: 50, duration: {TOTAL}, ease: 'none'}}, 0);
    window.__timelines["bg"] = tl;
  </script>
</template>
""")

WIPES = [SC[1], SC[6], SC[10], SC[13]]
wipe_html = "\n    ".join(f'<div id="fx-w{i}" class="wipe"><div class="wipe-in"></div></div>' for i in range(len(WIPES)))
wipe_js = "\n    ".join(
    f"tl.fromTo('#fx-w{i}',{{xPercent:-130}},{{xPercent:130,duration:.7,ease:'power2.inOut'}},{t - 0.35:.3f});" for i, t in enumerate(WIPES))
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

chunks = chunk_words(WORDS, SC[1:-2])
g_html, g_js = [], []
for gi, ch in enumerate(chunks):
    a = round(ch[0][0] - LEAD, 3); z = round(ch[-1][1], 3)
    if gi + 1 < len(chunks):
        z = min(z, round(chunks[gi + 1][0][0] - LEAD - 0.02, 3))
    spans = " ".join(f'<span id="cw{gi}-{j}" class="cw{" kw" if w.lower() in V["KEYWORDS"] else ""}">{html.escape(w)}</span>' for j, (_, _, w) in enumerate(ch))
    g_html.append(f'<div id="cg{gi}" class="cg"><span class="cg-pill">{spans}</span></div>')
    g_js.append(f"tl.fromTo('#cg{gi}',{{opacity:0,y:18,filter:'blur(6px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.2,ease:'power3.out'}},{a});")
    for j, (s, e, _) in enumerate(ch):
        on = max(a, round(s - LEAD, 3))
        g_js.append(f"tl.set('#cw{gi}-{j}',{{color:'#6D28D9'}},{on});")
        nxt = round(ch[j + 1][0] - LEAD, 3) if j + 1 < len(ch) else None
        if nxt:
            g_js.append(f"tl.set('#cw{gi}-{j}',{{color:'#1B1240'}},{nxt});")
    g_js.append(f"tl.to('#cg{gi}',{{opacity:0,duration:.12,ease:'power2.in'}},{z - 0.12:.3f});")
    g_js.append(f"tl.set('#cg{gi}',{{opacity:0,visibility:'hidden'}},{z});")
open(os.path.join(COMP, "captions.html"), "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080" data-layout-allow-caption-zone>
    {chr(10).join("    " + g for g in g_html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    gsap.set('.cg', {{opacity: 0}});
    {chr(10).join("    " + j for j in g_js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
""")

# ---------- index ----------
hosts = []
for S in scenes:
    hosts.append(f'<div id="{S.sid}" data-composition-id="{S.sid}" data-composition-src="compositions/{S.sid}.html" data-start="{S.start}" '
                 f'data-duration="{round(S.end - S.start, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:2"></div>')
CSS = open(os.path.join(HERE, "ai_editing_v2.css")).read()
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
      {chr(10).join("      " + h for h in hosts)}
      <div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:5"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="captions" data-width="1920" data-height="1080" style="z-index:6"></div>
      <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")
print("ok", len(scenes), "scenes,", len(chunks), "caption groups")
