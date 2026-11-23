# Developed by Mehdi ORANUSS | Powered by Claude
"""Full 9:16 reel from input/recordings/1025.mp4, v2, in the premium-serif style (styles/premium_serif.py,
reference/styles/short/premium-serif/STYLE.md): phrase captions with italic-serif accent, depth-blur plate under graphics,
diamond badges, floating cards, progress timeline, punch-ins + earshot `launch` kit sound effects.
Writes work/1025v2.ass, work/filter_1025v2.txt, work/1025v2_inputs.txt, output/1025/captions-1025-latin-darija.srt."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import eased_moves, in_out_cubic, pop, spring, press, exit_, wipe_lr, OUT, IN
from styles.base import (PURPLE, NEON, LAV, NAVY, INK, WHITE, rrect, co, rr, ICONS, ANCHOR, STAR,
                         E, ms, icon, sparkle, cursor, write_ass, place_sfx)
from styles.premium_serif import (N, CAP_Y, captions, write_srt, glass, diamond, slide_text, pill,
                                  HEADER, filter_graph)

ROOT = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(ROOT, "work")
SPEECH_END = 33.97
TOTAL = 35.6

# ---------- captions: phrase chunks (start, end, tokens); kinds n sans, b heavy, s italic serif, L big number ----------
CHUNKS = [
    (0.00, 2.03, [(0.07, "n", "Bghiti"), (0.43, "s", "t3llem"), N, (0.83, "b", "MHARAT"), (1.45, "b", "JDAD?")]),
    (2.06, 3.00, [(2.06, "n", "lli t7ell lik"), N, (2.41, "s", "forass"), (2.56, "b", "KBIRA")]),
    (3.03, 3.92, [(3.03, "n", "f"), (3.06, "b", "SOUK"), (3.27, "s", "l'internet?")]),
    (3.94, 5.52, [(3.94, "n", "Wfferna lik"), N, (4.50, "L", "6"), (4.74, "s", "dyal"), (5.05, "b", "MHARAT")]),
    (5.56, 6.95, [(5.56, "n", "lli tqder"), (6.00, "n", "annaha"), N, (6.34, "s", "tqeddem"), (6.68, "b", "LIK")]),
    (6.97, 8.62, [(6.97, "n", "wa7d"), (7.24, "s", "l7all"), (7.61, "b", "KBIR"), N, (8.00, "n", "w b jhd"), (8.37, "b", "9LIL")]),
    (8.70, 9.66, [(8.70, "b", "TSSWI9,"), (9.32, "s", "lbi3,")]),
    (9.68, 11.08, [(9.68, "s", "l'i9na3,"), N, (10.27, "b", "L'I3LANAT")]),
    (11.10, 12.45, [(11.10, "n", "w kadalik"), (11.44, "n", "7tta"), N, (11.73, "b", "SMMA")]),
    (12.47, 14.28, [(12.47, "s", "l'automation"), N, (13.00, "n", "w"), (13.15, "b", "DKA2"), (13.59, "b", "STINA3I")]),
    (14.30, 15.54, [(14.30, "n", "Rah hadou"), N, (14.75, "b", "L'MHARAT")]),
    (15.56, 16.80, [(15.56, "n", "lli"), (15.74, "s", "mohimmin"), N, (16.28, "n", "men"), (16.46, "b", "DABA")]),
    (16.86, 18.82, [(16.86, "n", "Mharat momkin"), N, (17.76, "n", "ennak"), (18.03, "s", "tstamer"), (18.48, "b", "FIHOM")]),
    (18.84, 20.04, [(18.84, "n", "men l'we9t dyal"), N, (19.65, "b", "DABA")]),
    (20.06, 21.23, [(20.06, "n", "w tqder ennak"), N, (20.62, "s", "twsel"), (20.90, "n", "l wa7d")]),
    (21.25, 22.34, [(21.25, "s", "l'mostawa"), N, (21.67, "n", "lli howa"), (21.95, "b", "KBIR")]),
    (22.36, 22.98, [(22.36, "n", "Chno"), (22.57, "s", "katsna?")]),
    (23.00, 24.45, [(23.00, "n", "Tsjjel f"), N, (23.48, "s", "l7issa"), (23.79, "b", "L'MAJJANIYA")]),
    (24.57, 26.07, [(24.57, "n", "Kon"), (24.72, "b", "AKID"), N, (25.16, "n", "ennak"), (25.49, "s", "ghatwsel")]),
    (26.09, 27.98, [(26.09, "n", "kadalik 7tta"), (26.66, "s", "b majmou3a"), N, (27.23, "n", "men"), (27.38, "b", "L'HADAYA")]),
    (28.00, 29.45, [(28.00, "n", "lli ghatkhallik ennak"), N, (28.77, "s", "t3ref"), (29.05, "n", "majmou3a")]),
    (29.47, 31.18, [(29.47, "n", "men"), (29.61, "b", "L'MA3LOMAT"), N, (30.30, "n", "lli nta"), (30.74, "s", "m7tajhom")]),
    (31.20, 32.02, [(31.20, "n", "Chno"), (31.47, "s", "katsna?")]),
    (32.04, 32.88, [(32.04, "b", "SJJEL"), (32.32, "b", "DABA"), N, (32.66, "n", "w khod")]),
    (32.90, SPEECH_END, [(32.90, "s", "l'khatwa"), N, (33.26, "n", "dyalk"), (33.60, "b", "LOWLA")]),
]
srt = captions(CHUNKS)

# ---------- beats ----------
# 2.06 - 3.94 floating cards + chip (plate blurred)
for k, (x, tilt, ic, lab) in enumerate([(290, -9, "play", "VIDEO"), (540, 0, "chat", "CLIENTS"), (790, 9, "briefcase", "BUSINESS")]):
    t0 = 2.10 + k * 0.13; y = 640 + (0 if k == 1 else 30)
    glass(30 + k * 6, t0, 3.92, x, y, 220, 290, r=26, tilt=tilt)
    E(35 + k * 6, t0 + 0.12, 3.92, "Shape", f"{{\\an5\\pos({x},{y - 40})\\frz{tilt}\\fad(150,200){spring(100)}\\c{NEON}\\1a&H50&\\blur14\\p1}}{co(0, 0, 120)}{{\\p0}}")
    icon(35 + k * 6, t0 + 0.12, 3.92, x, y - 40, ic, 54, f"\\frz{tilt}\\fad(150,200){spring(54)}", fill=PURPLE)
    E(35 + k * 6, t0 + 0.18, 3.92, "Label", f"{{\\an5\\pos({x},{y + 80})\\frz{tilt}\\fs26\\fsp6\\fad(150,200)\\c{LAV}}}{lab}")
pill(3.03, 3.92, 540, 380, "SOUK L'INTERNET")

# 4.50 - 5.52 diamond 6 + label/title on the wall
diamond(40, 4.50, 5.52, 330, 420, 130, "6")
slide_text(45, 4.62, 5.52, "Light", 430, 385, "\\an4\\fs28\\fsp10", "SKILLS")
slide_text(45, 5.05, 5.52, "Heavy", 430, 448, "\\an4\\fs72", "Mharat", dx=40)

# 6.97 - 8.62 promise card: two check rows (plate sharp, card on the wall)
glass(30, 6.97, 8.60, 540, 430, 640, 230, r=34, dy=40)
for t0, y, txt, ser in [(7.24, 380, "7ALL", "kbir"), (8.00, 480, "JHD", "9lil")]:
    diamond(40, t0, 8.60, 300, y, 56, "check", kind="icon")
    slide_text(45, t0 + 0.06, 8.60, "Heavy", 360, y, "\\an4\\fs60", txt, dx=24)
    slide_text(45, t0 + 0.16, 8.60, "Serif", 360 + len(txt) * 44 + 20, y + 4, "\\an4\\fs66", ser, dx=24)

# 8.62 - 14.30 framework: 7 diamond badges, each lands on its word, active one glows (plate blurred)
SKILLS = [(8.70, "eye", "Tsswi9"), (9.32, "briefcase", "Lbi3"), (9.68, "chat", "L'i9na3"), (10.27, "play", "L'i3lanat"),
          (11.73, "people", "SMMA"), (12.47, "key", "Automation"), (13.15, "bulb", "AI")]
SK_END = 14.28
slide_text(30, 8.66, SK_END, "Light", 540, 290, "\\an5\\fs30\\fsp14", "L'MHARAT", dx=0, dy=20)
POS = [(210, 500), (430, 500), (650, 500), (870, 500), (320, 790), (540, 790), (760, 790)]
for k, ((t, ic, lab), (x, y)) in enumerate(zip(SKILLS, POS)):
    diamond(40, t, SK_END, x, y, 112, ic, kind="icon")
    slide_text(48, t + 0.10, SK_END, "Serif", x, y + 120, "\\an5\\fs54", lab, dx=0, dy=16, dur=0.3)
    nxt = SKILLS[k + 1][0] if k + 1 < len(SKILLS) else SK_END
    E(39, t, nxt, "Shape", f"{{\\an5\\pos({x},{y})\\frz45\\c{NEON}\\1a&HFF&\\t(0,180,{OUT},\\1a&H70&)\\t({ms(nxt - t) - 180},{ms(nxt - t)},\\1a&HFF&)\\blur30\\p1}}{rrect(190, 190, 50)}{{\\p0}}")
    E(32, t, nxt, "Light", f"{{\\an5\\pos(540,340)\\fs26\\fsp6\\c&HFFFFFF&\\1a&H40&}}0{k + 1} / 07")

# 15.74 punch accent: sparkle around "mohimmin"
sparkle(15.74, 540, 520, 1.0)

# 16.80 - 22.36 progress timeline: Daba -> Tstamer -> Mostawa kbir, marker rides the line (plate blurred)
TL_END = 22.34
tx0, tx1, ty = 170, 910, 640
slide_text(30, 16.84, TL_END, "Light", 540, 430, "\\an5\\fs30\\fsp14", "NOMOU", dx=0, dy=20)
E(31, 16.86, TL_END, "Shape", f"{{\\an7\\pos(0,0)\\c{LAV}\\1a&HA0&\\fad(0,200){wipe_lr(tx0 - 4, ty - 4, tx1 + 4, ty + 4, 0, 500, OUT)}\\p1}}{rr(tx0, ty - 3, tx1 - tx0, 6, 3)}{{\\p0}}")
M0, M1 = 17.40, 21.25
E(32, 16.86, TL_END, "Shape", f"{{\\an7\\pos(0,0)\\c{NEON}\\fad(0,200)\\blur1{wipe_lr(tx0, ty - 8, tx1, ty + 8, ms(M0 - 16.86), ms(M1 - 16.86))}\\p1}}{rr(tx0, ty - 4, tx1 - tx0, 8, 4)}{{\\p0}}")
for t0, x, lab in [(16.86, tx0, "Daba"), (18.03, (tx0 + tx1) // 2, "Tstamer"), (21.25, tx1, "Mostawa\\Nkbir")]:
    diamond(40, t0, TL_END, x, ty, 46, "", kind="num")
    slide_text(45, t0 + 0.08, TL_END, "Serif", x, ty + 110, "\\an5\\fs54", lab, dx=0, dy=16, dur=0.3)
for a, b, mv in eased_moves(M0, tx0, ty - 90, tx1, ty - 90, M1 - M0, lambda p: p, keys=tuple(i / 8 for i in range(9))):
    E(50, a, b, "Shape", f"{{\\an5{mv}\\c{WHITE}\\bord3\\3c{NEON}\\blur1\\p1}}{co(0, 0, 54)}{{\\p0}}")
    for path, role in ICONS["check"]:
        E(51, a, b, "Shape", f"{{\\an5{mv}\\fscx28\\fscy28\\c{PURPLE}\\p1}}{path}{ANCHOR}{{\\p0}}")
E(50, M1, TL_END, "Shape", f"{{\\an5\\pos({tx1},{ty - 90})\\fad(0,200)\\c{WHITE}\\bord3\\3c{NEON}{spring(100)}\\p1}}{co(0, 0, 54)}{{\\p0}}")
icon(51, M1, TL_END, tx1, ty - 90, "check", 28, f"\\fad(0,200){spring(28)}", fill=PURPLE)
sparkle(21.95, tx1, ty - 90, 0.7)

# 22.36 - 24.45 free class pill (plate sharp, top)
pill(23.00, 24.43, 540, 420, "L7ISSA MAJJANIYA", ic="calendar")
pill(23.79, 24.43, 540, 300, "FREE", w=180, h=76)

# 27.30 - 31.20 gift cards carousel + chip (plate blurred)
for k, (x, tilt) in enumerate([(290, -9), (540, 0), (790, 9)]):
    t0 = 27.38 + k * 0.13; y = 680 + (0 if k == 1 else 30)
    glass(30 + k * 6, t0, 31.18, x, y, 220, 290, r=26, tilt=tilt)
    E(35 + k * 6, t0 + 0.12, 31.18, "Shape", f"{{\\an5\\pos({x},{y - 40})\\frz{tilt}\\fad(150,200){spring(100)}\\c{NEON}\\1a&H50&\\blur14\\p1}}{co(0, 0, 120)}{{\\p0}}")
    icon(35 + k * 6, t0 + 0.12, 31.18, x, y - 40, "book", 54, f"\\frz{tilt}\\fad(150,200){spring(54)}", fill=PURPLE)
    E(35 + k * 6, t0 + 0.18, 31.18, "Label", f"{{\\an5\\pos({x},{y + 80})\\frz{tilt}\\fs26\\fsp6\\fad(150,200)\\c{LAV}}}HADIYA 0{k + 1}")
sparkle(27.38, 540, 640, 1.1)
pill(29.61, 31.18, 540, 400, "L'MA3LOMAT LLI M7TAJ", ic="check")

# 31.20 - 33.97 CTA button + cursor click
bw, bh = 640, 150
for ly, tg, shp, oy in [(40, f"\\c{NEON}\\1a&H60&\\blur26", rrect(bw + 24, bh + 24, 87), 0),
                        (41, f"\\c{PURPLE}\\bord2\\3c{LAV}\\3a&H30&", rrect(bw, bh, 75), 0),
                        (42, f"\\c{WHITE}\\1a&HE6&", rrect(bw - 16, bh // 2 - 8, 60), -bh // 4)]:
    E(ly, 31.47, SPEECH_END, "Shape", f"{{\\an5\\pos(540,{440 + oy})\\fad(120,200){pop()}{press(ms(32.04 - 31.47))}{tg}\\p1}}{shp}{{\\p0}}")
E(43, 31.52, SPEECH_END, "Heavy", f"{{\\an5\\pos(540,440)\\fs68\\fad(120,200){pop(100, 40)}{press(ms(32.04 - 31.52))}}}SJJEL DABA")
cursor(31.55, SPEECH_END, 960, 800, 760, 480, 32.04)
pill(32.90, SPEECH_END, 540, 610, "L'KHATWA 01", ic="check")

# END 33.97 - 35.6: ink end card with glass folder + brand
fw, fh = 560, 380
back = (f"m 0 30 b 0 12 12 0 30 0 l 190 0 b 210 0 216 8 226 22 l 240 44 l {fw - 30} 44 b {fw - 12} 44 {fw} 56 {fw} 74 "
        f"l {fw} {fh - 30} b {fw} {fh - 12} {fw - 12} {fh} {fw - 30} {fh} l 30 {fh} b 12 {fh} 0 {fh - 12} 0 {fh - 30}")
front = (f"m 0 {fh * 0.32:.0f} l {fw} {fh * 0.32:.0f} l {fw - 14} {fh - 26} b {fw - 16} {fh - 8} {fw - 26} {fh} {fw - 44} {fh} "
         f"l 44 {fh} b 26 {fh} 16 {fh - 8} 14 {fh - 26}")
E(95, SPEECH_END, TOTAL, "Shape", f"{{\\an7\\pos(0,0)\\c{INK}\\fad(240,0)\\p1}}m 0 0 l 1080 0 l 1080 1920 l 0 1920{{\\p0}}")
E(96, SPEECH_END, TOTAL, "Shape", f"{{\\an5\\pos(540,820)\\c{NEON}\\1a&H50&\\blur60\\fad(300,0)\\p1}}{co(0, 0, 520)}{{\\p0}}")
for ly, tg, shp in [(97, f"\\c{PURPLE}\\1a&H20&\\bord2\\3c{LAV}\\3a&H40&", back), (98, f"\\c{NEON}\\1a&H58&\\bord2\\3c{LAV}\\3a&H20&", front)]:
    E(ly, SPEECH_END + 0.1, TOTAL, "Shape", f"{{\\an5\\pos(540,800)\\fad(150,0){pop(50, 0)}{tg}\\p1}}{shp}{{\\p0}}")
E(99, SPEECH_END + 0.3, TOTAL, "Heavy", f"{{\\an5\\pos(540,1010)\\fs76\\c{NEON}\\3c{NEON}\\bord5\\blur16\\1a&H40&\\fad(200,0)}}ORANUSS ACADEMY")
E(99, SPEECH_END + 0.3, TOTAL, "Heavy", f"{{\\an5\\pos(540,1010)\\fs76\\fad(200,0){pop(100, 0)}}}ORANUSS ACADEMY")
slide_text(99, SPEECH_END + 0.45, TOTAL, "Serif", 540, 1100, "\\an5\\fs58", "Sjjel daba", dx=0, dy=20)
sparkle(SPEECH_END + 0.3, 540, 800, 1.2)

# ---------- sound effects (earshot launch kit) ----------
CUES = [
    (0.43, "tick", 0, -8), (1.45, "snap", 0, -9),
    (2.06, "whoosh.short", 0, -6), (2.10, "pop", 0, -10), (2.23, "pop", 1, -11), (2.36, "pop", 2, -11), (3.03, "tick", 1, -9),
    (3.94, "land.light", 0, -8), (4.50, "hit", 0, -7), (5.05, "tick", 2, -10),
    (6.97, "tock", 0, -9), (7.24, "pop", 3, -10), (8.00, "pop", 0, -10),
    (8.62, "whoosh.short", 1, -7),
    # skills: rising glock notes, one per badge (G4 A4 C5 D5 E5 G5 A5)
    (8.70, "bell", 0, -13), (9.32, "bell", 1, -13), (9.68, "bell", 2, -13), (10.27, "bell", 3, -13),
    (11.73, "bell", 4, -13), (12.47, "bell", 5, -13), (13.15, "bell", 6, -13),
    (14.30, "land.light", 1, -8), (15.74, "snap", 1, -9),
    (16.80, "whoosh.short", 2, -7), (16.86, "tick", 0, -10), (18.03, "tick", 1, -10), (21.25, "land", 0, -8), (21.95, "bell", 9, -13),
    (22.36, "land.light", 2, -8), (23.00, "pop", 1, -10), (23.79, "tick", 2, -9),
    (24.72, "snap", 0, -9),
    (27.30, "whoosh.short", 0, -7), (27.38, "pop", 2, -10), (27.51, "pop", 3, -11), (27.64, "pop", 0, -11), (29.61, "tick", 0, -9),
    (31.20, "land.light", 0, -8), (32.04, "riser", 0, -14), (32.04, "click.confirm", 0, -8), (32.90, "pop", 1, -10),
    (SPEECH_END + 0.05, "whoosh.long", 0, -8), (SPEECH_END + 0.3, "bell", 7, -12),
]
sfx = place_sfx(CUES, os.path.join(W, "sfx", "kit"))

write_ass(os.path.join(W, "1025v2.ass"), HEADER)
write_srt(os.path.join(ROOT, "..", "output", "1025", "captions-1025-latin-darija.srt"), srt)

# ---------- filter graph ----------
ZK = [(0.0, 1.0), (1.45, 1.04), (1.451, 1.13), (2.06, 1.14), (3.94, 1.06), (3.941, 1.0), (4.50, 1.02),
      (4.501, 1.11), (5.55, 1.13), (5.551, 1.04), (8.62, 1.08), (14.30, 1.04), (15.74, 1.06), (15.741, 1.10),
      (16.80, 1.11), (22.36, 1.04), (22.361, 1.0), (24.72, 1.02), (24.721, 1.12), (27.30, 1.14), (31.20, 1.06),
      (31.201, 1.0), (32.04, 1.02), (32.041, 1.08), (TOTAL, 1.10)]
BLUR_WIN = [(2.02, 3.94), (8.62, 14.30), (16.80, 22.36), (27.30, 31.20)]   # depth trick under graphics
fc = filter_graph(os.path.join(W, "1025v2.ass"), TOTAL, SPEECH_END, ZK, BLUR_WIN, sfx)
open(os.path.join(W, "filter_1025v2.txt"), "w").write(";\n".join(fc))
open(os.path.join(W, "1025v2_inputs.txt"), "w").write("\n".join(p for _, p, _ in sfx) + "\n")
from styles.base import ev
print(f"events={len(ev)} sfx={len(sfx)} chunks={len(CHUNKS)}")
