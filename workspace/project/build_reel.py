#!/usr/bin/env python3
# Developed by Mehdi ORANUSS | Powered by Claude
"""9:16 reel version of IMG_2399 using the reference-driven layouts
(A face / B face-top + panel / B2 UI-top + rounded PiP / C cutaway / A3 B&W beat).
Reuses cut list, captions and graphic helpers from build.py.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(ROOT, "work")
ns = {"__file__": os.path.join(ROOT, "build.py"), "__name__": "build"}
exec(open(os.path.join(ROOT, "build.py"), encoding="utf8").read(), ns)

ev = ns["ev"]; ev.clear()
E, glass, glow_text, chip, bubble, sparkle = ns["E"], ns["glass"], ns["glow_text"], ns["chip"], ns["bubble"], ns["sparkle"]
social_float, growth_chart, folder_pop, playlist = ns["social_float"], ns["growth_chart"], ns["folder_pop"], ns["playlist"]
rr, co, ICONS, ANCHOR = ns["rr"], ns["co"], ns["ICONS"], ns["ANCHOR"]
PURPLE, NEON, LAV, NAVY, INK, WHITE = (ns[k] for k in ("PURPLE", "NEON", "LAV", "NAVY", "INK", "WHITE"))
out, chunks, clean, TOTAL = ns["out"], ns["chunks"], ns["clean"], ns["TOTAL"]
T_CUT = ns["SEG_OUT_START"][ns["BIG_CUT_INDEX"]]
RW, RH = 1080, 1920

# ---------- layout timeline (output seconds) ----------
LAYOUT = [
    (0.0, 2.6, "C"),
    (2.6, out(17.9), "A"),
    (out(18.22), out(24.6), "B"),
    (out(24.95), out(30.5), "A"),
    (out(30.5), out(36.4), "B"),
    (out(36.4), out(40.6), "B"),
    (out(40.6), out(45.9), "A3"),
    (out(45.9), out(48.99), "B"),
    (out(49.0), out(55.0), "B"),
    (out(55.0), out(63.5), "A"),
    (out(63.5), out(70.27), "B"),
    (out(70.72), T_CUT, "A"),
    (T_CUT, out(118.0), "B2"),
    (out(118.0), out(123.0), "B"),
    (out(123.0), TOTAL, "A"),
]
# fill tiny gaps left by trims so every frame has a layout
LAYOUT = [(s, (LAYOUT[i + 1][0] if i + 1 < len(LAYOUT) else e), k) for i, (s, e, k) in enumerate(LAYOUT)]

def layout_at(t):
    for s, e, k in LAYOUT:
        if s <= t < e:
            return k
    return "A"

def windows(kind):
    return [(s, e) for s, e, k in LAYOUT if k == kind]

# ---------- chapters ----------
CHAPTERS = [(2.6, out(24.6), "01", "L'BLASSA"),
            (out(24.95), out(55.0), "02", "PERSONAL BRANDING"),
            (out(55.0), T_CUT, "03", "DROUS"),
            (T_CUT, TOTAL - 2.4, "04", "KIFACH?")]

def chapter_header(st, en, num, label, kind):
    if kind in ("B", "B2"):
        x, y = 70, (910 if kind == "B" else 120)
        E(80, st, en, "Thin", f"{{\\an4\\pos({x},{y})\\fad(150,150)\\c{LAV}}}{num}")
        E(80, st, en, "Shape", f"{{\\an4\\pos({x + 118},{y})\\fad(150,150)\\c{LAV}\\1a&H60&\\p1}}m 0 -28 l 2 -28 l 2 28 l 0 28{{\\p0}}")
        E(80, st, en, "Label", f"{{\\an4\\pos({x + 142},{y})\\fad(150,150)}}{label}")
    else:  # A / A3: top-right, under the platform top bar
        x, y = 1010, 250
        E(80, st, en, "Label", f"{{\\an6\\pos({x},{y})\\fad(150,150)\\bord3\\3c&H00200810&\\3a&H60&}}{label}")
        E(80, st, en, "Shape", f"{{\\an6\\pos({x - len(label) * 21 - 24},{y})\\fad(150,150)\\c{LAV}\\1a&H40&\\p1}}m 0 -24 l 2 -24 l 2 24 l 0 24{{\\p0}}")
        E(80, st, en, "Thin", f"{{\\an6\\pos({x - len(label) * 21 - 44},{y})\\fad(150,150)\\c{LAV}\\fs72\\bord3\\3c&H00200810&\\3a&H60&}}{num}")

for cs, ce, num, label in CHAPTERS:
    for ls, le, kind in LAYOUT:
        s, e = max(cs, ls), min(ce, le)
        if e - s > 0.05:
            chapter_header(s, e, num, label, kind)

# panel frame for B: neon divider line under the face
for s, e in windows("B"):
    E(70, s, e, "Shape", f"{{\\an7\\pos(0,858)\\c{NEON}\\blur3\\p1}}m 0 0 l {RW} 0 l {RW} 4 l 0 4{{\\p0}}")
# rim + glow around the rounded PiP in B2
PIP = (90, 1200, 900, 620)
for s, e in windows("B2"):
    px, py, pw, ph = PIP
    E(70, s, e, "Shape", f"{{\\an7\\pos({px - 10},{py - 10})\\c{NEON}\\1a&H70&\\blur20\\p1}}{rr(0, 0, pw + 20, ph + 20, 48)}{{\\p0}}")
    E(72, s, e, "Shape", f"{{\\an7\\pos({px},{py})\\1a&HFF&\\bord3\\3c{LAV}\\3a&H20&\\p1}}{rr(0, 0, pw, ph, 40)}{{\\p0}}")

# ---------- captions (position depends on layout) ----------
CAP_Y = {"A": 1560, "A3": 1560, "C": 1560, "B": 1830, "B2": 1130}
for ci, ch in enumerate(chunks):
    c_start, c_end = ch[0][0], ch[-1][1]
    if ci + 1 < len(chunks):
        c_end = min(c_end + 0.15, chunks[ci + 1][0][0])
    if c_start >= TOTAL - 2.4:
        continue
    words_ = [clean(x[2]) for x in ch]
    for wi, w in enumerate(ch):
        st = w[0] if wi else c_start
        en = ch[wi + 1][0] if wi + 1 < len(ch) else c_end
        y = CAP_Y[layout_at(st + 0.01)]
        p = f"{{\\pos(540,{y})" + ("\\fscx88\\fscy88\\t(0,110,\\fscx100\\fscy100)}" if wi == 0 else "}")
        E(90, st, en, "CapHalo", p + " ".join(words_))
        parts = [f"{{\\3a&H00&}}{t}{{\\3a&HFF&}}" if k == wi else t for k, t in enumerate(words_)]
        E(91, st, en, "Cap", p + "{\\3a&HFF&}" + " ".join(parts))

# ---------- C: intro cutaway ----------
E(10, 0, 2.6, "Shape", f"{{\\an7\\pos(0,0)\\c{INK}\\p1}}m 0 0 l {RW} 0 l {RW} {RH} l 0 {RH}{{\\p0}}")
E(11, 0, 2.6, "Shape", f"{{\\an5\\pos(540,820)\\c{PURPLE}\\1a&H50&\\blur90\\p1}}{co(0, 0, 900)}{{\\p0}}")
E(12, 0.1, 2.6, "Shape", f"{{\\an5\\pos(540,520)\\fad(200,150)\\c{NAVY}\\1a&H30&\\bord2\\3c{LAV}\\p1}}{rr(0, 0, 220, 72, 36)}{{\\p0}}")
E(13, 0.15, 2.6, "Label", f"{{\\an5\\pos(540,520)\\fad(200,150)}}EP 01")
glow_text(14, 0.25, 2.6, "Heavy", "\\an5\\pos(540,760)\\fs128\\fad(150,200)\\fscx70\\t(0,260,\\fscx100)", "PERSONAL")
E(14, 0.55, 2.6, "Shape", f"{{\\an5\\pos(540,900)\\c{PURPLE}\\fad(100,200)\\clip(150,840,150,960)\\t(0,260,\\clip(150,840,930,960))\\p1}}{rr(0, 0, 780, 124, 14)}{{\\p0}}")
E(15, 0.65, 2.6, "Heavy", f"{{\\an5\\pos(540,900)\\fs120\\fad(100,200)}}BRANDING")
E(15, 0.9, 2.6, "Light", f"{{\\an5\\pos(540,1010)\\fs40\\fsp8\\fad(200,200)}}ORANUSS ACADEMY")
sparkle(0.7, 540, 830, 2.2)

# ---------- A widgets ----------
chip(out(6.4), out(9.8), 540, 1200, "play", "LA PLATEFORME")
chip(out(11.0), out(15.3), 540, 1200, "pin", "ORANUSS ACADEMY")
bubble(out(16.2), out(17.85), 880, 1040, "eye")
glass(20, out(26.4), out(30.4), 540, 1200, 900, 190, r=34)
E(25, out(26.5), out(30.4), "Light", f"{{\\an5\\pos(540,1150)\\fad(200,200)\\fs34}}wa7da mn ahamm l7wayj")
glow_text(25, out(26.6), out(30.4), "Heavy", "\\an5\\pos(540,1225)\\fs78\\fad(200,200)\\fscx80\\t(0,250,\\fscx100)", "PERSONAL BRANDING")
sparkle(out(26.6), 540, 1180, 2.0)
chip(out(56.0), out(59.0), 540, 1200, "people", "HAMZA ORANUSS")
chip(out(59.3), out(62.9), 540, 1200, "info", "LM3LOMAT")
chip(out(72.4), out(76.2), 540, 1200, "key", "TTARI9A")
chip(out(76.6), T_CUT - 0.05, 540, 1200, "heart", "NSANDKOM")
sparkle(out(123.1), 540, 1150, 2.0)

# ---------- A3: black & white emphasis beat ----------
a3s, a3e = windows("A3")[0]
glow_text(30, a3s + 0.1, a3e, "Heavy", "\\an5\\pos(540,1150)\\fs150\\fad(120,200)\\fscx60\\fscy60\\t(0,220,\\fscx105\\fscy105)\\t(220,320,\\fscx100\\fscy100)", "BLA KHIBRA?")
E(31, a3s + 0.4, a3e, "Light", f"{{\\an5\\pos(540,1270)\\fs40\\fsp4\\fad(200,200)}}7TTA BLA SNAWAT DYAL LKHIBRA")

# ---------- B panels ----------
def node_graph(st, en):
    cx, cy = 540, 1230
    E(20, st, en, "Shape", f"{{\\an5\\pos({cx},{cy})\\fad(200,200)\\c{NEON}\\1a&H50&\\blur26\\p1}}{co(0, 0, 210)}{{\\p0}}")
    E(21, st, en, "Shape", f"{{\\an5\\pos({cx},{cy})\\fad(200,200)\\c{PURPLE}\\bord3\\3c{LAV}\\fscx0\\fscy0\\t(0,250,\\fscx100\\fscy100)\\p1}}{co(0, 0, 170)}{{\\p0}}")
    E(22, st + 0.1, en, "Heavy", f"{{\\an5\\pos({cx},{cy})\\fs34\\fad(200,200)}}ORANUSS")
    outs = [(out(18.4), 200, "people", "L'ÉQUIPE"), (out(21.0), 540, "camera", "L'IMAGE"), (out(23.2), 880, "briefcase", "LA SOCIÉTÉ")]
    for t0, x, icon, label in outs:
        t0 = max(t0, st + 0.3)
        y0, y1 = cy + 90, 1520
        E(20, t0, en, "Shape", f"{{\\an7\\pos(0,0)\\fad(0,200)\\c{LAV}\\1a&H40&\\clip(0,{y0},{RW},{y0})\\t(0,300,\\clip(0,{y0},{RW},{y1}))\\p1}}m {cx - 2} {y0} l {cx + 2} {y0} l {x + 2} {y1 - 70} l {x - 2} {y1 - 70}{{\\p0}}")
        glass(22, t0 + 0.2, en, x, y1, 280, 190, r=26)
        for path, role in ICONS[icon]:
            col = WHITE if role == "w" else NAVY
            E(27, t0 + 0.3, en, "Shape", f"{{\\an5\\pos({x},{y1 - 28})\\fad(150,200)\\fscx0\\fscy0\\t(0,200,\\fscx70\\fscy70)\\c{col}\\p1}}{path}{ANCHOR}{{\\p0}}")
        E(27, t0 + 0.35, en, "Heavy", f"{{\\an5\\pos({x},{y1 + 55})\\fs32\\fad(150,200)}}{label}")

def phone(st, en, cx, cy):
    w, h = 330, 600
    E(20, st, en, "Shape", f"{{\\an5\\move({cx},{cy + 80},{cx},{cy},0,350)\\fad(200,200)\\frz6\\t(0,350,\\frz0)\\c{NEON}\\1a&H60&\\blur24\\p1}}{rr(0, 0, w + 30, h + 30, 64)}{{\\p0}}")
    E(21, st, en, "Shape", f"{{\\an5\\move({cx},{cy + 80},{cx},{cy},0,350)\\fad(200,200)\\frz6\\t(0,350,\\frz0)\\c&H00100810&\\bord6\\3c&H00303030&\\p1}}{rr(0, 0, w, h, 56)}{{\\p0}}")
    for k in range(3):
        y = cy - 200 + k * 175
        E(22, st + 0.3 + k * 0.15, en, "Shape", f"{{\\an5\\pos({cx},{y})\\fad(200,200)\\c{NAVY}\\bord1\\3c{LAV}\\3a&H80&\\p1}}{rr(0, 0, w - 50, 150, 18)}{{\\p0}}")
        E(23, st + 0.3 + k * 0.15, en, "Shape", f"{{\\an5\\pos({cx - 90},{y})\\fad(200,200)\\c{PURPLE}\\p1}}{co(0, 0, 70)}{{\\p0}}")
        E(23, st + 0.35 + k * 0.15, en, "Shape", f"{{\\an7\\pos({cx - 40},{y - 30})\\fad(200,200)\\c{LAV}\\1a&H60&\\p1}}{rr(0, 0, 150, 16, 8)}{{\\p0}}")
        E(23, st + 0.35 + k * 0.15, en, "Shape", f"{{\\an7\\pos({cx - 40},{y + 4})\\fad(200,200)\\c{LAV}\\1a&HA0&\\p1}}{rr(0, 0, 110, 14, 7)}{{\\p0}}")
    social_float(st + 0.6, x=860, y0=1700, y1=1050)

def idea_chips(st, en):
    items = [("MO7TAWA", 300, 1130), ("AFKAR", 780, 1130), ("LM3LOMAT", 330, 1330), ("PARTAGE", 760, 1330), ("SOCIAL MEDIA", 540, 1530)]
    for k, (txt, x, y) in enumerate(items):
        t0 = st + 0.15 + k * 0.18
        w = len(txt) * 30 + 90
        col = PURPLE if txt in ("AFKAR",) else NAVY
        E(20, t0, en, "Shape", f"{{\\an5\\pos({x},{y})\\fad(150,200)\\c{NEON}\\1a&H70&\\blur16\\fscx0\\fscy0\\t(0,200,\\fscx110\\fscy110)\\t(200,300,\\fscx100\\fscy100)\\p1}}{rr(0, 0, w + 14, 104, 52)}{{\\p0}}")
        E(21, t0, en, "Shape", f"{{\\an5\\pos({x},{y})\\fad(150,200)\\c{col}\\1a&H20&\\bord2\\3c{LAV}\\fscx0\\fscy0\\t(0,200,\\fscx110\\fscy110)\\t(200,300,\\fscx100\\fscy100)\\p1}}{rr(0, 0, w, 90, 45)}{{\\p0}}")
        E(22, t0 + 0.08, en, "Heavy", f"{{\\an5\\pos({x},{y})\\fs40\\fad(150,200)}}{txt}")
    sparkle(out(37.5), 780, 1130, 1.0)

def drous_cards(st, en):
    for k, (icon, title, sub, x) in enumerate([("book", "DROUS", "ddrous dyalna", 290), ("cap", "L7ISAS", "hna fach kan9rikom", 790)]):
        t0 = st + 0.2 + k * 0.6
        glass(20, t0, en, x, 1330, 420, 520, r=34)
        E(25, t0 + 0.1, en, "Shape", f"{{\\an5\\pos({x},1220)\\fad(150,200)\\c{PURPLE}\\bord2\\3c{LAV}\\fscx0\\fscy0\\t(0,220,\\fscx100\\fscy100)\\p1}}{co(0, 0, 170)}{{\\p0}}")
        for path, role in ICONS[icon]:
            col = WHITE if role == "w" else PURPLE
            E(26, t0 + 0.2, en, "Shape", f"{{\\an5\\pos({x},1220)\\fad(150,200)\\fscx0\\fscy0\\t(0,220,\\fscx90\\fscy90)\\c{col}\\p1}}{path}{ANCHOR}{{\\p0}}")
        glow_text(26, t0 + 0.3, en, "Heavy", f"\\an5\\pos({x},1410)\\fs52\\fad(150,200)", title)
        E(26, t0 + 0.4, en, "Light", f"{{\\an5\\pos({x},1480)\\fs30\\fad(150,200)}}{sub}")

b_windows = windows("B")
node_graph(*b_windows[0])
phone(b_windows[1][0], b_windows[1][1], 540, 1330)
idea_chips(*b_windows[2])
growth_chart(b_windows[3][0], b_windows[3][1], 540, 1330)
sparkle(b_windows[3][0] + 1.2, 560, 1220)
folder_pop(b_windows[4][0], b_windows[4][1], 540, 1330)
sparkle(b_windows[4][0] + 0.4, 540, 1280, 1.4)
drous_cards(*b_windows[5])
playlist(b_windows[6][0], b_windows[6][1], 540, 1300)

# ---------- B2: step-by-step guide card + PiP ----------
g0, g1 = windows("B2")[0]
glass(20, g0, g1, 540, 620, 960, 820, r=40)
E(25, g0 + 0.1, g1, "Heavy", f"{{\\an4\\pos(110,300)\\fs64\\fad(200,200)}}Step by Step")
E(25, g0 + 0.25, g1, "Serif", f"{{\\an4\\pos(110,385)\\fad(200,200)\\c{LAV}}}Guide")
rows = [(99.6, "01", "Tb3o lvidyouhat chwiya b chwiya", "play"),
        (106.2, "02", "Bano b wjhkom f social media", "camera"),
        (111.0, "03", "3awno nnas lokhrin", "heart")]
for k, (s_, n, txt, icon) in enumerate(rows):
    y = 520 + k * 150
    t_in = g0 + 0.4 + k * 0.15
    t_act = out(s_)
    E(26, t_in, g1, "Shape", f"{{\\an7\\pos(100,{y - 55})\\fad(200,200)\\c{WHITE}\\1a&HE8&\\p1}}{rr(0, 0, 880, 110, 22)}{{\\p0}}")
    E(27, t_act, g1, "Shape", f"{{\\an7\\pos(100,{y - 55})\\fad(150,200)\\c{PURPLE}\\1a&H30&\\bord2\\3c{LAV}\\clip(100,{y - 60},100,{y + 60})\\t(0,300,\\clip(100,{y - 60},980,{y + 60}))\\p1}}{rr(0, 0, 880, 110, 22)}{{\\p0}}")
    E(28, t_in, g1, "Thin", f"{{\\an4\\move(110,{y},130,{y},0,300)\\fs54\\fad(200,200)\\c{LAV}}}{n}")
    E(28, t_in + 0.05, g1, "Step", f"{{\\an4\\move(220,{y},240,{y},0,300)\\fad(200,200)}}{txt}")
    for path, role in ICONS[icon]:
        col = WHITE if role == "w" else PURPLE
        E(29, t_act, g1, "Shape", f"{{\\an5\\pos(930,{y})\\fad(150,200)\\fscx0\\fscy0\\t(0,220,\\fscx46\\fscy46)\\c{col}\\p1}}{path}{ANCHOR}{{\\p0}}")
    sparkle(t_act + 0.05, 930, y, 0.6)

# ---------- big cut flash ----------
E(95, T_CUT - 0.22, T_CUT + 0.32, "Shape", f"{{\\an7\\pos(0,0)\\c{PURPLE}\\1a&HFF&\\t(0,200,\\1a&H20&)\\t(260,540,\\1a&HFF&)\\p1}}m 0 0 l {RW} 0 l {RW} {RH} l 0 {RH}{{\\p0}}")
E(96, T_CUT - 0.18, T_CUT + 0.30, "Shape", f"{{\\an5\\pos(540,960)\\c{LAV}\\1a&HFF&\\blur70\\fscx40\\fscy40\\t(0,200,\\1a&H30&\\fscx180\\fscy180)\\t(240,480,\\1a&HFF&\\fscx280\\fscy280)\\p1}}{co(0, 0, 800)}{{\\p0}}")

# ---------- end card + comment CTA ----------
TE = TOTAL; E0 = TE - 2.4
E(100, E0, TE, "Shape", f"{{\\an7\\pos(0,0)\\c{INK}\\fad(350,0)\\p1}}m 0 0 l {RW} 0 l {RW} {RH} l 0 {RH}{{\\p0}}")
E(101, E0 + 0.1, TE, "Shape", f"{{\\an5\\pos(540,760)\\c{PURPLE}\\1a&H60&\\blur90\\fad(500,0)\\p1}}{co(0, 0, 820)}{{\\p0}}")
fx, fy = 330, 520
fold = f"\\fad(300,0)\\move({fx},{fy + 40},{fx},{fy},0,450)"
E(102, E0 + 0.2, TE, "Shape", f"{{\\an7{fold}\\c{PURPLE}\\1a&H30&\\p1}}m 0 24 b 0 8 8 0 24 0 l 140 0 b 156 0 162 6 170 16 l 190 40 l 396 40 b 412 40 420 48 420 64 l 420 300 l 0 300{{\\p0}}")
for k, (dx, rot) in enumerate([(60, 8), (150, -5), (230, 6)]):
    E(103, E0 + 0.35 + k * 0.08, TE, "Shape", f"{{\\an7\\fad(250,0)\\move({fx + dx},{fy + 80},{fx + dx},{fy + 20 + k * 6},0,550)\\frz{rot}\\c{LAV}\\1a&H18&\\bord1\\3c{WHITE}\\p1}}{rr(0, 0, 150, 190, 14)}{{\\p0}}")
E(104, E0 + 0.2, TE, "Shape", f"{{\\an7{fold}\\c{NEON}\\1a&H58&\\bord2\\3c{LAV}\\3a&H20&\\p1}}m 0 110 l 440 110 l 420 300 l 0 300{{\\p0}}")
E(105, E0 + 0.35, TE, "Heavy", f"{{\\an4\\pos({fx + 30},{fy + 255})\\fs34\\fad(250,0)}}ORANUSS")
glow_text(106, E0 + 0.5, TE, "Heavy", "\\an5\\pos(540,960)\\fs92\\fad(300,0)\\fscx90\\t(0,450,\\fscx100)", "ORANUSS ACADEMY")
E(107, E0 + 0.6, TE, "Light", f"{{\\an5\\pos(540,1040)\\fs34\\fsp8\\fad(300,0)}}PERSONAL BRANDING")
# comment-box CTA
E(108, E0 + 0.8, TE, "Shape", f"{{\\an5\\pos(540,1260)\\fad(250,0)\\c{NAVY}\\1a&H20&\\bord2\\3c{LAV}\\p1}}{rr(0, 0, 860, 120, 60)}{{\\p0}}")
E(109, E0 + 0.85, TE, "Shape", f"{{\\an5\\pos(170,1260)\\fad(250,0)\\c{PURPLE}\\p1}}{co(0, 0, 76)}{{\\p0}}")
E(109, E0 + 0.9, TE, "Step", f"{{\\an4\\pos(230,1260)\\fad(250,0)\\clip(230,1200,230,1320)\\t(0,700,\\clip(230,1200,960,1320))}}Kteb \"ORANUSS\" f comments")

# progress bar along the top edge
E(110, 0, E0, "Shape", f"{{\\an7\\pos(0,0)\\c{NEON}\\blur3\\clip(0,0,0,10)\\t(0,{int(E0 * 1000)},\\clip(0,0,{RW},10))\\p1}}m 0 0 l {RW} 0 l {RW} 8 l 0 8{{\\p0}}")

HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {RW}
PlayResY: {RH}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Avenir Next Demi Bold,72,&H00FFFFFF,&H00FFFFFF,&H00E02B5B,&H00000000,0,0,0,0,100,100,0,0,3,10,0,2,70,70,80,1
Style: CapHalo,Avenir Next Demi Bold,72,&HFF000000,&HFF000000,&H00200810,&HFF000000,0,0,0,0,100,100,0,0,1,8,0,2,70,70,80,1
Style: Shape,Arial,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Heavy,Avenir Next Heavy,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,4,0,0,0,1
Style: Light,Avenir Next,30,&H00FFC4E0,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,4,0,0,0,1
Style: Label,Avenir Next Demi Bold,38,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,3,0,1,0,0,4,0,0,0,1
Style: Thin,Avenir Next Ultra Light,84,&H00FFC4E0,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,4,0,0,0,1
Style: Serif,Didot,80,&H00FFC4E0,&H00FFFFFF,&H00000000,&H00000000,0,-1,0,0,100,100,0,0,1,0,0,4,0,0,0,1
Style: Num,Avenir Next Heavy,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Step,Avenir Next Demi Bold,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,4,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ass_file = os.path.join(W, "reel.ass")
open(ass_file, "w", encoding="utf8").write(HEADER + "\n".join(ev) + "\n")

# ---------- ffmpeg graph: reuse the 16:9 edit up to concat, then compose 9:16 ----------
base = []
for line in ns["fc"]:
    base.append(line)
    if "concat=n=" in line:
        break
audio = [l for l in ns["fc"] if l.startswith("[ac]")][0]

# speaker x-position keyframes (source seconds -> x in the 1920 frame), measured on gridded stills
FACE_X = [(0.0, 960), (21, 988), (33, 920), (38, 957), (47, 863), (52, 1003), (58, 832), (64, 988),
          (67, 1102), (69.5, 1118), (72, 1190), (75, 1019), (79, 978), (99, 920), (120, 842), (125.5, 842)]
KF = [(out(s_), x) for s_, x in FACE_X]

def track(width):
    """Piecewise-linear crop x that keeps the speaker centred in a crop of `width`."""
    hi = 1920 - width
    expr = f"{KF[-1][1] - width / 2:.1f}"
    for (t0, x0), (t1, x1) in reversed(list(zip(KF, KF[1:]))):
        seg = f"({x0 - width / 2:.1f}+({x1 - x0})*(t-{t0:.3f})/{max(t1 - t0, 0.01):.3f})"
        expr = f"if(lt(t,{t1:.3f}),{seg},{expr})"
    return f"'max(0,min({hi},{expr}))'"

def en_expr(kinds):
    parts = [f"between(t,{s:.3f},{e:.3f})" for s, e, k in LAYOUT if k in kinds]
    return "+".join(parts) if parts else "0"

fc = base + [
    "[vc]split=3[f0][f1][f2]",
    # A: centre 9:16 crop; A3 windows go monochrome
    f"[f0]crop=608:1080:{track(608)}:0,scale=1080:1920:flags=lanczos,hue=s='if({en_expr(['A3'])},0,1)'[full]",
    # B: face strip for the top 860px
    f"[f1]crop=904:720:{track(904)}:40,scale=1080:860:flags=lanczos[top]",
    # B2: rounded PiP
    f"[f2]crop=1103:760:{track(1103)}:20,scale=900:620:flags=lanczos,format=yuva420p[pipc]",
    "[pipc][1:v]alphamerge[pip]",
    f"color=c=0x100820:s=1080x1920:r=60000/1001:d={TOTAL + 1:.2f}[ink]",
    "[ink]split=2[ink1][ink2]",
    f"[full][ink1]overlay=enable='{en_expr(['B', 'B2', 'C'])}'[s1]",
    f"[s1][top]overlay=0:0:enable='{en_expr(['B'])}'[s2]",
    f"[s2][pip]overlay={PIP[0]}:{PIP[1]}:enable='{en_expr(['B2'])}'[s3]",
    f"[s3]vignette=angle=PI/4.4:mode=forward,ass='{ass_file.replace(':', chr(92) + ':')}',format=yuv420p[vout]",
    audio,
]
# ink2 unused safeguard: discard
fc[fc.index("[ink]split=2[ink1][ink2]")] = "[ink]null[ink1]"
open(os.path.join(W, "filter_reel.txt"), "w").write(";\n".join(fc))
print(f"reel events={len(ev)} duration={TOTAL:.2f}s layouts={len(LAYOUT)} cut={T_CUT:.2f}")
