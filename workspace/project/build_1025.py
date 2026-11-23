# Developed by Mehdi ORANUSS | Powered by Claude
"""9:16 reel from input/recordings/1025.mp4 (already vertical, 30 fps, SDR), v1, in the purple-glass style
(styles/purple_glass.py, reference/styles/short/purple-glass/STYLE.md) + motion language from motion.py.
Writes work/1025.ass, work/filter_1025.txt, output/1025/captions-1025-latin-darija-v1.srt."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import eased_moves, out_cubic, in_out_cubic, pop, spring, press, exit_, wipe_lr, OUT, IN
from styles.base import (PURPLE, NEON, LAV, NAVY, INK, WHITE, rrect, co, rr, ICONS, ANCHOR, STAR,
                         E, ms, icon, sparkle, cursor, write_ass)
from styles.purple_glass import (enter, glass, bubble, hl_box, chip, flash, chunk_words, captions, write_srt,
                                 HEADER, filter_graph)

ROOT = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(ROOT, "work")

SPEECH_END = 33.97
TOTAL = 35.6
END0 = SPEECH_END

# ---------- 1. words (whisper large-v3 word timings, transliterated to Latin Darija) ----------
WORDS = [
    (0.07, "Bghiti"), (0.43, "t3llem"), (0.83, "mharat"), (1.45, "jdad"), (2.06, "lli"), (2.11, "t7ell"),
    (2.31, "lik"), (2.41, "forass"), (2.56, "kbira"), (3.03, "f"), (3.06, "souk"), (3.27, "l'internet?"),
    (3.94, "Wfferna"), (4.37, "lik"), (4.50, "6"), (4.74, "dyal"), (5.05, "l'mharat"), (5.56, "lli"),
    (5.70, "tqder"), (6.00, "annaha"), (6.34, "tqeddem"), (6.68, "lik"), (6.97, "wa7d"), (7.24, "l7all"),
    (7.61, "kbir"), (8.00, "w b jhd"), (8.37, "9lil."),
    (8.70, "Tsswi9,"), (9.32, "lbi3,"), (9.68, "l'i9na3,"), (10.27, "l'i3lanat,"), (11.10, "w kadalik"),
    (11.44, "7tta"), (11.73, "SMMA,"), (12.47, "l'automation"), (13.00, "w"), (13.15, "dka2"),
    (13.59, "l'istina3i."),
    (14.30, "Rah hadou"), (14.75, "l'mharat"), (15.56, "lli"), (15.74, "mohimmin"), (16.28, "men"), (16.46, "daba."),
    (16.86, "Mharat"), (17.40, "momkin"), (17.76, "ennak"), (18.03, "tstamer"), (18.48, "fihom"), (18.84, "men"),
    (19.02, "l'we9t"), (19.29, "dyal"), (19.65, "daba,"), (20.06, "w tqder"), (20.40, "ennak"), (20.62, "twsel"),
    (20.90, "l wa7d"), (21.25, "l'mostawa"), (21.67, "lli"), (21.81, "howa"), (21.95, "kbir."),
    (22.36, "Chno"), (22.57, "katsna?"), (23.00, "Tsjjel"), (23.28, "f"), (23.48, "l7issa"), (23.79, "l'majjaniya."),
    (24.57, "Kon"), (24.72, "akid"), (25.16, "ennak"), (25.49, "ghatwsel"), (26.09, "kadalik"), (26.41, "7tta"),
    (26.66, "b majmou3a"), (27.23, "men"), (27.38, "l'hadaya"), (28.00, "lli"), (28.14, "ghatkhallik"),
    (28.56, "ennak"), (28.77, "t3ref"), (29.05, "majmou3a"), (29.47, "men"), (29.61, "l'ma3lomat"),
    (30.30, "lli"), (30.55, "nta"), (30.74, "m7tajhom."),
    (31.20, "Chno"), (31.47, "katsna?"), (32.04, "Sjjel"), (32.32, "daba"), (32.66, "w khod"), (32.90, "l'khatwa"),
    (33.26, "dyalk"), (33.60, "lowla."),
]
KEYWORDS = {"mharat", "l'mharat", "l'internet?", "tsswi9,", "lbi3,", "l'i9na3,", "l'i3lanat,", "smma,",
            "l'automation", "dka2", "l'istina3i.", "mohimmin", "l'mostawa", "kbir.", "l7issa", "l'majjaniya.",
            "l'hadaya", "l'ma3lomat", "sjjel", "daba", "l'khatwa", "6"}
words = [(t, (WORDS[i + 1][0] if i + 1 < len(WORDS) else SPEECH_END), w) for i, (t, w) in enumerate(WORDS)]
words = [(a, min(b, a + 0.9), w) for a, b, w in words]  # no word hangs through a pause

# ---------- 2. layouts ----------
B_WIN = [(8.62, 14.30), (16.80, 22.36), (24.45, 31.20)]
def is_B(t):
    return any(s <= t < e for s, e in B_WIN)

# ---------- 4. beats ----------
# HOOK 0 - 3.94: stacked kinetic title in a glass card above the face, cursor clicks the key words
glass(20, 0.0, 2.05, 540, 440, 900, 420)
enter(25, 0.07, 2.05, "Light", 540, 300, "\\an5\\fs44\\fsp10", "BGHITI", dy=24)
enter(25, 0.43, 2.05, "Heavy", 540, 410, "\\an5\\fs128", "T3LLEM", dy=46)
hl_box(24, 0.83, 2.05, 540, 548, 700, 112)
enter(25, 0.83, 2.05, "Heavy", 470, 548, "\\an5\\fs84", "MHARAT", dy=30)
E(25, 1.45, 2.05, "Heavy", f"{{\\an5\\pos(800,548)\\fs84\\c{LAV}\\fad(0,200){pop()}{exit_(600)}}}JDAD?")
cursor(1.0, 2.05, 980, 860, 760, 580, 1.55)
sparkle(0.43, 540, 420)
chip(2.11, 3.92, 540, 360, "key", "FORASS KBIRA")
chip(3.06, 3.92, 540, 500, "eye", "SOUK L'INTERNET")

# 3.94 - 8.62: big number 6, then the promise (7all kbir / jhd 9lil)
glass(20, 3.94, 6.92, 540, 450, 860, 360)
E(26, 4.50, 6.92, "Heavy", f"{{\\an5\\pos(290,450)\\fs330\\c{NEON}\\3c{NEON}\\bord8\\blur22\\1a&H50&\\fad(120,220){pop()}{exit_(2420)}}}6")
E(27, 4.50, 6.92, "Heavy", f"{{\\an5\\pos(290,450)\\fs330\\fad(120,220){pop()}{exit_(2420)}}}6")
enter(25, 3.94, 6.92, "Light", 470, 365, "\\an4\\fs38\\fsp8", "WFFERNA LIK", dx=-30, dy=0)
enter(25, 5.05, 6.92, "Heavy", 470, 455, "\\an4\\fs96", "MHARAT", dx=-40, dy=0)
enter(25, 5.40, 6.92, "Light", 470, 540, f"\\an4\\fs32\\fsp4\\c{LAV}", "F SOUK L'INTERNET", dx=-30, dy=0)
sparkle(4.50, 290, 450, 0.8)
chip(7.24, 8.60, 540, 360, "check", "7ALL KBIR")
chip(8.00, 8.60, 540, 500, "check", "JHD 9LIL")

# B 8.62 - 14.30: skills grid, each card lands on its word, active card glows
SKILLS = [(8.70, "TSSWI9", "MARKETING", "eye"), (9.32, "LBI3", "SALES", "briefcase"),
          (9.68, "L'I9NA3", "PERSUASION", "chat"), (10.27, "L'I3LANAT", "ADS", "play"),
          (11.73, "SMMA", "AGENCY", "people"), (12.47, "AUTOMATION", "NO-CODE", "key"),
          (13.15, "DKA2 STINA3I", "AI", "bulb")]
SK_END = 14.30
def panel_header(st, en, label, title, accent=None):
    E(30, st, en, "Shape", f"{{\\an7\\pos(0,860)\\c{NEON}\\fad(150,150)\\p1}}m 0 0 l 1080 0 l 1080 3 l 0 3{{\\p0}}")
    enter(31, st + 0.05, en, "Light", 70, 920, "\\an4\\fs28\\fsp6", label, dx=-20, dy=0)
    enter(31, st + 0.12, en, "Heavy", 70, 985, "\\an4\\fs62", title, dx=-30, dy=0)
    if accent:
        enter(31, st + 0.25, en, "Serif", 70 + len(title) * 40 + 24, 990, "\\an4\\fs62", accent, dx=-20, dy=0)

panel_header(8.62, SK_END, "SKILLS", "L'MHARAT", "jdad")
for k, (t, name, sub, ic) in enumerate(SKILLS):
    if k < 6:
        cx, cy = (300 if k % 2 == 0 else 780), 1130 + (k // 2) * 150
    else:
        cx, cy = 540, 1580
    w, h = 450, 124
    glass(40, t - 0.05, SK_END, cx, cy, w, h, r=28)
    bubble(45, t, SK_END, cx - w // 2 + 62, cy, ic, d=78, t0=80)
    enter(48, t + 0.05, SK_END, "Label", cx - w // 2 + 116, cy - 18, "\\an4\\fs38", name, dx=-20, dy=0)
    enter(48, t + 0.10, SK_END, "Light", cx - w // 2 + 117, cy + 26, "\\an4\\fs24\\fsp5", sub, dx=-20, dy=0)
    E(47, t + 0.05, t + 0.05 + 0.24, "Shape", f"{{\\an5\\pos({cx},{cy})\\1a&HFF&\\bord3\\3c{NEON}\\blur6\\3a&HFF&\\t(0,120,\\3a&H00&)\\t(120,240,\\3a&H90&)\\p1}}{rrect(w, h, 28)}{{\\p0}}")
    nxt = SKILLS[k + 1][0] if k + 1 < len(SKILLS) else SK_END - 0.3
    E(39, t, nxt, "Shape", f"{{\\an5\\pos({cx},{cy})\\c{NEON}\\1a&HFF&\\t(0,200,{OUT},\\1a&H8C&)\\t({ms(nxt - t) - 200},{ms(nxt - t)},\\1a&HFF&)\\blur26\\p1}}{rrect(w + 30, h + 30, 40)}{{\\p0}}")
    E(32, t, (nxt if k + 1 < len(SKILLS) else SK_END), "Light", f"{{\\an6\\pos(1010,920)\\fs28\\fsp6\\c{LAV}}}0{k + 1} / 07")

# A 14.30 - 16.80: kinetic emphasis
glass(20, 14.30, 16.78, 540, 430, 880, 400)
enter(25, 14.30, 16.78, "Light", 540, 300, "\\an5\\fs44\\fsp10", "RAH HADOU", dy=24)
enter(25, 14.75, 16.78, "Heavy", 540, 405, "\\an5\\fs110", "L'MHARAT", dy=40)
hl_box(24, 15.56, 16.78, 540, 532, 640, 104)
enter(25, 15.60, 16.78, "Heavy", 540, 532, "\\an5\\fs74", "LLI MOHIMMIN", dy=26)
E(25, 16.28, 16.78, "Light", f"{{\\an5\\pos(540,615)\\fs38\\fsp12\\c{LAV}\\fad(0,180){pop()}}}MEN DABA")
sparkle(15.74, 540, 520, 1.1)

# B 16.80 - 22.36: growth line chart (illustrative, no numbers; line reveal is linear, no overshoot)
CH_END = 22.36
panel_header(16.80, CH_END, "NOMOU", "TSTAMER", "w twsel")
gx0, gx1, gy0, gy1 = 130, 950, 1660, 1110   # plot box: left, right, bottom, top
for i in range(4):
    y = gy0 - i * (gy0 - gy1) // 3
    E(33, 16.90 + i * 0.06, CH_END, "Shape", f"{{\\an7\\pos(0,0)\\c{LAV}\\1a&HD0&\\fad(200,200){wipe_lr(gx0, y - 2, gx1, y + 2, 0, 400, OUT)}\\p1}}m {gx0} {y - 1} l {gx1} {y - 1} l {gx1} {y + 1} l {gx0} {y + 1}{{\\p0}}")
E(33, 16.86, CH_END, "Light", f"{{\\an7\\pos({gx0},{gy0 + 18})\\fs26\\fsp6\\fad(200,200)}}DABA")
def curve_y(p):  # monotonic ease-in growth, values only rise
    return gy0 - 30 - (gy0 - gy1 - 60) * (p ** 1.8)
N = 40
pts = [(gx0 + (gx1 - gx0) * i / N, curve_y(i / N)) for i in range(N + 1)]
up = " l ".join(f"{x:.0f} {y - 6:.0f}" for x, y in pts)
dn = " l ".join(f"{x:.0f} {y + 6:.0f}" for x, y in reversed(pts))
area = " l ".join(f"{x:.0f} {y:.0f}" for x, y in pts) + f" l {gx1} {gy0} l {gx0} {gy0}"
L0, L1 = 17.40, 21.25
reveal = wipe_lr(gx0 - 10, gy1 - 60, gx1 + 30, gy0 + 10, ms(L0 - 16.86), ms(L1 - 16.86))
E(34, 16.86, CH_END, "Shape", f"{{\\an7\\pos(0,0)\\c{NEON}\\1a&HB8&\\fad(0,200){reveal}\\p1}}m {area}{{\\p0}}")
E(35, 16.86, CH_END, "Shape", f"{{\\an7\\pos(0,0)\\c{NEON}\\1a&H60&\\blur10\\fad(0,200){reveal}\\p1}}m {up} l {dn}{{\\p0}}")
E(36, 16.86, CH_END, "Shape", f"{{\\an7\\pos(0,0)\\c{WHITE}\\fad(0,200){reveal}\\p1}}m {up} l {dn}{{\\p0}}")
# leading dot rides the line at the same linear progress as the wipe
for i in range(N):
    a = L0 + (L1 - L0) * i / N; b = L0 + (L1 - L0) * (i + 1) / N
    (xa, ya), (xb, yb) = pts[i], pts[i + 1]
    E(37, a, b, "Shape", f"{{\\an5\\move({xa:.0f},{ya:.0f},{xb:.0f},{yb:.0f})\\c{LAV}\\bord4\\3c{NEON}\\blur2\\p1}}{co(0, 0, 26)}{{\\p0}}")
ex, ey = pts[-1]
E(37, L1, CH_END, "Shape", f"{{\\an5\\pos({ex:.0f},{ey:.0f})\\fad(0,200)\\c{LAV}\\bord4\\3c{NEON}{spring(100)}\\p1}}{co(0, 0, 34)}{{\\p0}}")
E(36, L1, CH_END, "Shape", f"{{\\an5\\pos({ex:.0f},{ey:.0f})\\1a&HFF&\\bord3\\3c{LAV}\\fscx30\\fscy30\\t(0,600,{OUT},\\fscx260\\fscy260\\3a&HFF&)\\p1}}{co(0, 0, 40)}{{\\p0}}")
glass(40, 21.25, CH_END, 690, 1200, 380, 96, r=48, anim="pop")
E(44, 21.30, CH_END, "Label", f"{{\\an5\\pos(690,1200)\\fs36\\fad(150,200){pop(100, 60)}}}MOSTAWA KBIR")
sparkle(21.95, ex, ey, 0.7)

# A 22.36 - 24.45: free class badge
enter(25, 22.36, 24.43, "Heavy", 540, 330, "\\an5\\fs100\\bord6\\3c&H00200810&\\3a&H70&", "CHNO KATSNA?", dy=36)
chip(23.00, 24.43, 540, 470, "calendar", "L7ISSA MAJJANIYA")
glass(40, 23.79, 24.43, 940, 470, 150, 70, r=35, anim="pop")
E(46, 23.84, 24.43, "Heavy", f"{{\\an5\\pos(940,470)\\fs36\\c{LAV}\\fad(100,200){pop(100, 40)}}}FREE")

# B 24.45 - 31.20: gift folder (glass folder, cards rise out on "l'hadaya")
G_END = 31.20
panel_header(24.45, G_END, "BONUS", "L'HADAYA", "dyalk")
fx, fy = 540, 1390
fw, fh = 560, 380
def at_folder(layer, st, en, tags, shape, dy=40):
    enter(layer, st, en, "Shape", fx, fy, f"\\an5{tags}\\p1", f"{shape}{{\\p0}}", dy=dy, dur=0.5)
back = (f"m 0 30 b 0 12 12 0 30 0 l 190 0 b 210 0 216 8 226 22 l 240 44 l {fw - 30} 44 b {fw - 12} 44 {fw} 56 {fw} 74 "
        f"l {fw} {fh - 30} b {fw} {fh - 12} {fw - 12} {fh} {fw - 30} {fh} l 30 {fh} b 12 {fh} 0 {fh - 12} 0 {fh - 30}")
at_folder(40, 24.60, G_END, f"\\c{NEON}\\1a&H70&\\blur30", back)
at_folder(41, 24.60, G_END, f"\\c{PURPLE}\\1a&H30&\\bord2\\3c{LAV}\\3a&H50&", back)
CARDS = [(-170, -10, "HADIYA 01"), (0, 6, "HADIYA 02"), (170, -10, "HADIYA 03")]
for k, (dx, rot, lab) in enumerate(CARDS):
    t0 = 27.38 + k * 0.08
    cx, cy0, cy1 = fx + dx, fy + 60, fy - 150 - (20 if k == 1 else 0)
    for a, b, mv in eased_moves(t0, cx, cy0, cx, cy1, 0.5):
        E(42, a, b, "Shape", f"{{\\an5{mv}\\frz{rot}\\c{WHITE}\\1a&H18&\\bord2\\3c{LAV}\\p1}}{rrect(170, 220, 16)}{{\\p0}}")
        E(43, a, b, "Label", f"{{\\an5{mv}\\frz{rot}\\fs22\\c{PURPLE}}}{lab}")
    E(42, t0 + 0.5, G_END, "Shape", f"{{\\an5\\pos({cx},{cy1})\\frz{rot}\\fad(0,220)\\c{WHITE}\\1a&H18&\\bord2\\3c{LAV}\\p1}}{rrect(170, 220, 16)}{{\\p0}}")
    E(43, t0 + 0.5, G_END, "Label", f"{{\\an5\\pos({cx},{cy1})\\frz{rot}\\fad(0,220)\\fs22\\c{PURPLE}}}{lab}")
    icon(43, t0 + 0.5, G_END, cx, cy1 - 50, "book", 50, f"\\frz{rot}\\fad(150,220)", fill=WHITE)
front = (f"m 0 {fh * 0.32:.0f} l {fw} {fh * 0.32:.0f} l {fw - 14} {fh - 26} b {fw - 16} {fh - 8} {fw - 26} {fh} {fw - 44} {fh} "
         f"l 44 {fh} b 26 {fh} 16 {fh - 8} 14 {fh - 26}")
at_folder(44, 24.60, G_END, f"\\c{NEON}\\1a&H58&\\bord2\\3c{LAV}\\3a&H20&", front, dy=40)
at_folder(45, 24.60, G_END, f"\\c{WHITE}\\1a&HE8&", f"m 20 {fh * 0.34:.0f} l {fw - 20} {fh * 0.34:.0f} l {fw - 24} {fh * 0.5:.0f} l 24 {fh * 0.5:.0f}", dy=40)
enter(46, 24.75, G_END, "Heavy", fx, fy + 110, "\\an5\\fs56", "ORANUSS", dy=40, dur=0.5)
sparkle(27.38, fx, fy - 160, 1.0)
chip(29.61, G_END, 540, 1700 - 30, "check", "L'MA3LOMAT LLI M7TAJ")

# A 31.20 - 33.97: CTA button with cursor click
enter(25, 31.20, SPEECH_END, "Heavy", 540, 300, "\\an5\\fs100\\bord6\\3c&H00200810&\\3a&H70&", "CHNO KATSNA?", dy=36)
bw, bh = 640, 150
for ly, tg, shp in [(40, f"\\c{NEON}\\1a&H60&\\blur26", rrect(bw + 24, bh + 24, 87)),
                    (41, f"\\c{PURPLE}\\bord2\\3c{LAV}\\3a&H30&", rrect(bw, bh, 75)),
                    (42, f"\\c{WHITE}\\1a&HE6&", rrect(bw - 16, bh // 2 - 8, 60))]:
    oy = -bh // 4 if ly == 42 else 0
    d = ms(SPEECH_END - 31.47)
    E(ly, 31.47, SPEECH_END, "Shape", f"{{\\an5\\pos(540,{460 + oy})\\fad(120,200){pop()}{press(ms(32.04 - 31.47))}{tg}\\p1}}{shp}{{\\p0}}")
E(43, 31.52, SPEECH_END, "Heavy", f"{{\\an5\\pos(540,460)\\fs68\\fad(120,200){pop(100, 40)}{press(ms(32.04 - 31.52))}}}SJJEL DABA")
cursor(31.55, SPEECH_END, 960, 820, 760, 500, 32.04)
chip(32.90, SPEECH_END, 540, 640, "check", "L'KHATWA 01")
flash(32.04)

# END 33.97 - 35.6: ink end card
E(95, END0, TOTAL, "Shape", f"{{\\an7\\pos(0,0)\\c{INK}\\fad(200,0)\\p1}}m 0 0 l 1080 0 l 1080 1920 l 0 1920{{\\p0}}")
E(96, END0, TOTAL, "Shape", f"{{\\an5\\pos(540,820)\\c{NEON}\\1a&H50&\\blur60\\fad(300,0)\\p1}}{co(0, 0, 520)}{{\\p0}}")
for ly, tg, shp in [(97, f"\\c{PURPLE}\\1a&H20&\\bord2\\3c{LAV}\\3a&H40&", back), (98, f"\\c{NEON}\\1a&H58&\\bord2\\3c{LAV}\\3a&H20&", front)]:
    E(ly, END0 + 0.1, TOTAL, "Shape", f"{{\\an5\\pos(540,800)\\fscx50\\fscy50\\fad(150,0){pop(50, 0)}{tg}\\p1}}{shp}{{\\p0}}")
E(99, END0 + 0.3, TOTAL, "Heavy", f"{{\\an5\\pos(540,1010)\\fs76\\c{NEON}\\3c{NEON}\\bord5\\blur16\\1a&H40&\\fad(200,0)}}ORANUSS ACADEMY")
E(99, END0 + 0.3, TOTAL, "Heavy", f"{{\\an5\\pos(540,1010)\\fs76\\fad(200,0){pop(100, 0)}}}ORANUSS ACADEMY")
enter(99, END0 + 0.45, TOTAL, "Light", 540, 1090, "\\an5\\fs32\\fsp10", "SJJEL DABA  ·  L7ISSA MAJJANIYA", dy=24, shrink=False)
sparkle(END0 + 0.3, 540, 800, 1.2)

# flashes on layout switches + progress bar (linear, bounded)
for t in (8.62, 14.30, 16.80, 22.36, 24.45, 31.20):
    flash(t)
E(91, 0, SPEECH_END, "Shape", f"{{\\an7\\pos(0,0)\\c{NEON}{wipe_lr(0, 0, 1080, 8, 0, ms(SPEECH_END))}\\p1}}m 0 0 l 1080 0 l 1080 8 l 0 8{{\\p0}}")

# ---------- 5. captions: 2-4 word chunks, active word in a purple box, keywords lavender ----------
SWITCH = [8.62, 14.30, 16.80, 22.36, 24.45, 31.20]   # a chunk never straddles a layout switch
chunks = chunk_words(words, SWITCH)
def cap_y(t):
    return 90 if is_B(t) else 330
srt = captions(chunks, KEYWORDS, cap_y)

write_ass(os.path.join(W, "1025.ass"), HEADER)
write_srt(os.path.join(ROOT, "..", "output", "1025", "captions-1025-latin-darija-v1.srt"), srt)

# ---------- 6. filter graph ----------
# camera zoom keys (t, zoom); hard punches are two keys 1 ms apart, holds ease in-out (smoothstep)
ZK = [(0.0, 1.14), (0.55, 1.0), (3.94, 1.0), (3.941, 1.06), (8.62, 1.10), (14.30, 1.10), (14.301, 1.18),
      (16.80, 1.10), (22.36, 1.0), (22.361, 1.08), (24.45, 1.12), (31.20, 1.12), (31.201, 1.04), (TOTAL, 1.12)]
fc = filter_graph(os.path.join(W, "1025.ass"), TOTAL, SPEECH_END, ZK, B_WIN)
open(os.path.join(W, "filter_1025.txt"), "w").write(";\n".join(fc))
from styles.base import ev
print(f"events={len(ev)} chunks={len(chunks)} total={TOTAL}")
