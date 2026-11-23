# Developed by Mehdi ORANUSS | Powered by Claude
"""Shared purple-3d-glass HyperFrames kit (reference/styles/long/purple-3d-glass/STYLE.md): icons, the Scene builder
(entrances, tilt/drift, per-scene exit) and the glass / gloss / chip / phone / avatar pieces.
Used by gen_intro_ai.py; gen_ai_editing_v2.py keeps its own copy (it was written first)."""
import os, re, html
LEAD = 0.067
AR_RE = re.compile("[\u0600-\u06FF]")
def is_ar(text):
    return bool(AR_RE.search(text or ""))
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
    def write(self, comp_dir):
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
        open(os.path.join(comp_dir, f"{self.sid}.html"), "w").write(out)

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
    return S.box(name, x, y, w, h, "chip ar" if is_ar(text) else "chip", f'{badge}<span class="chip-t" style="font-size:{fs}px">{html.escape(text)}</span>',
                 f"border-radius:{h // 2}px")
def title(S, name, x, y, text, fs=96, w=1400, color=None, align="center", weight=800):
    parts = text.split(" ")
    spans = " ".join(f'<span id="{S.id(name)}-{i}" class="tw">{html.escape(p)}</span>' for i, p in enumerate(parts))
    col = f"color:{color};" if color else ""
    S.box(name, x, y, w, int(fs * 1.45), "title ar" if is_ar(text) else "title", spans, f"font-size:{fs}px;text-align:{align};font-weight:{weight};{col}")
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

