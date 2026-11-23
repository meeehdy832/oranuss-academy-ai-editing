# Developed by Mehdi ORANUSS | Powered by Claude
"""AI training offer (16:9, ~62 s): 100 % animation on the Khalil voiceover
input/voiceover/ElevenLabs_2026-11-05T17_50_05_Khalil...mp3, style pastel-app-ui (reference/styles/long/pastel-app-ui/STYLE.md).
Keywords only, in Arabic script (Graphik Arabic), each landing on its spoken word (whisper large-v3 word times).
Sound: voice + OrcaXV SFX (.claude/skills/orcaxv-sfx), no music, -14 LUFS. Plan: output/ai-training-offer/PLAN.md.
usage: python3 -I project/build_ai_training_offer.py [preview|stills] [version]"""
import csv, glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import OUT, IN
import styles.base as base
from styles.base import E, ms, rrect, co, rr, write_ass, zexpr
from styles.pastel_ui import (HEADER, CARD, INKT, MUTED, LINE, PURP, NEON, LILAC, ORANGE, YELLOW, GREEN, CORAL, BLUE, SKY,
                              PEACH, MINT, SHADOW, el, card, phone, txt, pill, icon_at, tile, avatar, ring, bar, check, skeleton,
                              sparkle_ui, wipe, background)

ROOT = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.dirname(ROOT)
WK = os.path.join(ROOT, "work", "ai-training-offer")
OUTDIR = os.path.join(TOP, "output", "ai-training-offer")
SK = os.path.join(TOP, ".claude", "skills", "orcaxv-sfx")
VOICE = glob.glob(os.path.join(TOP, "input", "voiceover", "ElevenLabs_2026-11-05T17_50_05_Khalil*.mp3"))[0]
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
MODE = sys.argv[1] if len(sys.argv) > 1 else "preview"
VERSION = sys.argv[2] if len(sys.argv) > 2 else "v1"
os.makedirs(WK, exist_ok=True)
SPEECH_END, TOTAL = 60.30, 62.0
LEAD = 0.067
def w(t):
    return t - LEAD

# Arabic styles (Graphik Arabic, installed in ~/Library/Fonts)
HEAD = HEADER.replace("\n[Events]", "Style: AR,Graphik Arabic Bold,96,&H002E1216,&H002E1216,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1\n"
                      "Style: ARS,Graphik Arabic Semibold,40,&H002E1216,&H002E1216,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1\n\n[Events]")

def akw(st, en, x, y, text, fs=96, color=INKT, layer=50, **kw):
    """Arabic keyword (the only on-screen words): Graphik Arabic Bold, eased rise on its word."""
    el(layer, st, en, x, y, ar(text), f"\\fs{fs}\\c{color}", style="AR", **kw)

def ar(text):
    """Graphik Arabic draws ت+ى as a ligature that reads like 'حق': a zero-width joiner keeps the letters apart but joined."""
    return text.replace("تى", "ت\u200dى")

def alabel(layer, st, en, x, y, text, fs=34, color=INKT, **kw):
    fs = round(fs * 1.15)
    el(layer, st, en, x, y, ar(text), f"\\fs{fs}\\c{color}", style="ARS", **kw)

def apill(layer, st, en, x, y, text, fill=PURP, color=CARD, fs=36, h=80, ic=None, **kw):
    """Pill with an Arabic label; the icon sits on the right (reading starts there)."""
    fs, h = round(fs * 1.15), round(h * 1.08)
    wd = int(len(text) * fs * 0.52 + (120 if ic else 70))
    el(layer, st, en, x, y, rrect(wd, h, h // 2), f"\\c{fill}", **kw)
    if ic:
        icon_at(layer + 1, st, en, x + wd // 2 - h // 2 - 6, y, ic, int(h * 0.55), CARD if fill != CARD else PURP, fill, **kw)
    el(layer + 1, st, en, x - (26 if ic else 0), y + 2, ar(text), f"\\fs{fs}\\c{color}", style="ARS", **kw)
    return wd

SC = [0.0, 3.92, 9.90, 13.76, 18.04, 21.46, 25.02, 29.88, 36.40, 40.12, 42.60, 46.96, 51.26, 56.45, SPEECH_END, TOTAL]
background(TOTAL)

# S1 0-3.92 "الذكاء الاصطناعي اليوم ولا قادر يدير لك المونتاج ديال الفيديوهات"
a, b = SC[0], SC[1]; K = dict(out="left")
akw(w(0.07), b, 600, 330, "الذكاء الاصطناعي", 104, **K)
akw(w(2.23), b, 600, 470, "يدير لك المونتاج", 88, PURP, **K)
el(49, w(2.23) + 0.1, b, 600, 545, rr(0, 0, 220, 10, 5), f"\\c{YELLOW}", enter="left", **K)
sx, sy, swd, sh = phone(20, 0.10, b, 1350, 500, 780, **K)
scx = sx + swd // 2
tile(25, w(0.38), b, scx, sy + 150, 150, 150, PURP, "chip", r=40, shadow=False, **K)
el(28, w(0.38) + 0.1, b, scx, sy + 152, "AI", f"\\fs40\\c{CARD}", style="T", enter="pop", **K)
cols = [CORAL, BLUE, YELLOW, GREEN]
for i in range(4):   # raw clips in a messy order, then the AI snaps them into a clean edit on "المونتاج"
    y = sy + 330 + i * 92
    el(24, 0.5 + i * 0.06, b, scx, y, rrect(swd - 50, 74, 20), "\\c&H00FBF7F8&", **K)
    el(25, 0.6 + i * 0.06, w(2.23), sx + 60 + (i * 53) % 120, y, rrect(150 + (i * 37) % 90, 46, 14), f"\\c{cols[i]}", out="none")
    el(25, w(2.23) + i * 0.05, b, sx + 40 + 90 + i * 10, y, rrect(180, 46, 14), f"\\c{cols[i]}", enter="left", d=60, **K)
    check(27, w(2.95) + i * 0.08, b, sx + swd - 60, y, 40, **K)
sparkle_ui(2.23, 600, 470, 0.9)

# S2 3.92-9.90 "هاد التطور كيعني أن عملية المونتاج ما بقاتش معقدة أو مقتصرة غير على المحترفين"
a, b = SC[1], SC[2]; K = dict(out="up")
alabel(40, w(4.27), b, 960, 120, "هاد التطور كيعني", 40, MUTED, **K)
card(20, w(5.48), b, 960, 520, 1180, 600, 40, **K)
for i in range(7):   # a crowded pro editor: many tracks, many knobs
    y = 300 + i * 62
    el(22, w(5.48) + 0.05, w(7.48), 450, y, rrect(80, 38, 10), f"\\c{LILAC}", out="fade")
    for k in range(4):
        x0 = 560 + ((i * 97 + k * 173) % 640)
        el(23, w(5.48) + 0.08 + k * 0.03, w(7.48), x0, y, rrect(90 + (i * k * 13) % 70, 38, 10),
           f"\\c{[CORAL, BLUE, YELLOW, GREEN, ORANGE, NEON, SKY][(i + k) % 7]}", enter="fade", out="fade")
for k in range(5):
    el(23, w(6.01) + k * 0.05, w(7.48), 1350 + (k % 3) * 70 - 70, 300 + (k // 3) * 90, co(0, 0, 52), f"\\c{LINE}\\bord6\\3c{MUTED}", enter="pop", out="fade")
akw(w(6.90), b, 960, 220, "ما بقاتش معقدة", 92, **K)
tile(30, w(7.48) + 0.25, b, 960, 540, 260, 260, PURP, "chip", r=60, **K)
el(33, w(7.48) + 0.35, b, 960, 610, "AI", f"\\fs56\\c{CARD}", style="T", enter="pop", **K)
apill(40, w(9.07), b, 960, 760, "غير على المحترفين", CARD, INKT, fs=36, ic="person", **K)
E(45, w(9.07) + 0.35, b - 0.3, "Shape", f"{{\\an4\\pos({960 - 210},762)\\c{CORAL}\\fscx0\\t(0,300,{OUT},\\fscx100)\\p1}}{rrect(420, 8, 4)}{{\\p0}}")

# S3 9.90-13.76 "بل حتى الأشخاص العاديين يقدروا يستفدوا من هاد الإمكانيات"
a, b = SC[2], SC[3]; K = dict(out="left")
akw(w(10.06), b, 960, 210, "حتى الأشخاص العاديين", 96, **K)
cols = [BLUE, CORAL, YELLOW, GREEN, ORANGE]
for i in range(5):
    x = 560 + i * 200
    avatar(22, w(10.30) + i * 0.08, b, x, 520, 130, cols[i], **K)
    check(26, w(11.58) + i * 0.12, b, x + 52, 470, 46, **K)
card(20, w(12.94), b, 960, 760, 700, 130, 40, **K)
for i, (ic, c) in enumerate((("film", PURP), ("chip", BLUE), ("star", YELLOW))):
    tile(24, w(12.94) + 0.05 + i * 0.07, b, 1170 - i * 110, 760, 84, 84, c, ic, r=24, shadow=False, enter="pop", **K)
alabel(26, w(12.94) + 0.1, b, 790, 762, "الإمكانيات", 40, PURP, **K)

# S4 13.76-18.04 "وهنا كتجي الفرصة ديالك باش تستثمر هاد المهارة في المشروع ديالك"
a, b = SC[3], SC[4]; K = dict(out="left")
tile(30, w(14.44), b, 560, 300, 150, 150, YELLOW, "star", r=40, enter="pop", **K)
sparkle_ui(14.44, 560, 300, 0.8)
akw(w(14.44) + 0.1, b, 560, 480, "الفرصة ديالك", 100, **K)
card(20, w(16.17), b, 1080, 520, 300, 320, 36, **K)
tile(23, w(16.17) + 0.05, b, 1080, 480, 150, 150, PURP, "chip", r=36, shadow=False, **K)
alabel(25, w(16.17) + 0.1, b, 1080, 625, "المهارة", 38, **K)
card(20, w(16.90), b, 1480, 520, 340, 420, 36, **K)
tile(23, w(16.90) + 0.05, b, 1480, 450, 170, 170, BLUE, "briefcase", r=40, shadow=False, **K)
alabel(25, w(16.90) + 0.1, b, 1480, 610, "المشروع ديالك", 38, **K)
for k in range(3):   # the skill flows into the project
    t0 = w(16.90) + 0.2 + k * 0.18
    E(22, t0, t0 + 0.5, "Shape", f"{{\\an5\\move(1240,520,1310,520)\\c{PURP}\\fad(80,120)\\p1}}{co(0, 0, 20)}{{\\p0}}")
check(28, 17.55, b, 1600, 330, 60, **K)

# S5 18.04-21.46 "سواء كنتي كتقدم محتوى إعلاني أو محتوى عادي"
a, b = SC[4], SC[5]; K = dict(out="up")
alabel(40, w(18.04), b, 960, 160, "سواء كنتي كتقدم", 40, MUTED, **K)
tile(20, w(19.70), b, 1260, 520, 380, 380, CORAL, "megaphone", **K)
akw(w(19.70) + 0.1, b, 1260, 800, "محتوى إعلاني", 72, **K)
el(30, w(20.26), b, 960, 520, co(0, 0, 110), f"\\c{YELLOW}", enter="pop", **K)
alabel(31, w(20.26), b, 960, 524, "أو", 46, INKT, enter="pop", **K)
tile(20, w(20.96), b, 660, 520, 380, 380, BLUE, "play", **K)
akw(w(20.96) + 0.1, b, 660, 800, "محتوى عادي", 72, **K)

# S6 21.46-25.02 "خصوصاً أن الفيديوهات ولات عندها قيمة كبيرة"
a, b = SC[5], SC[6]; K = dict(out="left")
card(20, w(22.19), b, 680, 500, 640, 460, 40, **K)
el(22, w(22.19) + 0.05, b, 680, 460, rrect(580, 330, 26), f"\\c{LILAC}", **K)
el(23, w(22.19) + 0.1, b, 680, 460, co(0, 0, 120), f"\\c{PURP}", enter="pop", **K)
el(24, w(22.19) + 0.1, b, 686, 460, "m 0 0 l 36 24 l 0 48", f"\\c{CARD}", enter="pop", **K)
skeleton(22, w(22.19) + 0.1, b, 600, 680, 400, 18, w(22.6), **K)
ring(30, w(24.00), b, 1360, 430, 280, 30, 0.86, GREEN, w(24.00) + 0.15, fill_dur=1.2)
tile(32, w(24.00) + 0.1, b, 1360, 430, 140, 140, YELLOW, "star", r=36, shadow=False, enter="pop", **K)
akw(w(24.00), b, 1360, 700, "قيمة كبيرة", 96, PURP, **K)
sparkle_ui(24.45, 1360, 430, 0.8)

# S7 25.02-29.88 "وكتساهم بشكل مهم في نجاح المحتوى على مواقع التواصل الاجتماعي"
a, b = SC[6], SC[7]; K = dict(out="fade")
card(20, w(25.29), b, 640, 520, 700, 470, 40, **K)
pts = [(360, 690), (460, 650), (560, 670), (660, 590), (760, 560), (860, 470), (920, 400)]
path = "m " + " l ".join(f"{x} {y}" for x, y in pts) + " " + " ".join(f"l {x} {y + 1}" for x, y in reversed(pts))
E(24, w(26.58), b - 0.3, "Shape", f"{{\\an7\\pos(0,0)\\1a&HFF&\\bord7\\3c{PURP}\\clip(340,360,340,720)\\t(0,1200,{OUT},\\clip(340,360,940,720))\\p1}}{path}{{\\p0}}")
E(24, b - 0.3, b, "Shape", f"{{\\an7\\pos(0,0)\\1a&HFF&\\bord7\\3c{PURP}\\t(0,300,\\3a&HFF&)\\p1}}{path}{{\\p0}}")
el(25, w(26.58) + 1.1, b, 920, 400, co(0, 0, 30), f"\\c{GREEN}\\bord6\\3c{CARD}", enter="pop", **K)
akw(w(26.58), b, 640, 230, "النجاح", 104, **K)
sx, sy, swd, sh = phone(20, w(26.93), b, 1380, 500, 760, **K)
scx = sx + swd // 2
for i in range(3):
    y = sy + 150 + i * 200
    el(24, w(26.93) + 0.1 + i * 0.07, b, scx, y, rrect(swd - 40, 180, 24), f"\\c{[PEACH, SKY, MINT][i]}", **K)
    el(25, w(26.93) + 0.15 + i * 0.07, b, scx, y, co(0, 0, 60), f"\\c{CARD}\\1a&H30&", enter="pop", **K)
    el(26, w(26.93) + 0.15 + i * 0.07, b, scx + 3, y, "m 0 0 l 18 12 l 0 24", f"\\c{[ORANGE, BLUE, GREEN][i]}", enter="pop", **K)
for i, (dx, dy) in enumerate(((150, -180), (180, 20), (140, 200), (200, -60))):
    icon_at(30, w(28.26) + i * 0.12, b, 1380 + dx, 500 + dy, "heart", 64, CORAL, CARD, enter="pop", **K)
apill(40, w(28.26), b, 1380, 930, "مواقع التواصل الاجتماعي", PURP, fs=34, ic="people", **K)
wipe(SC[7])

# S8 29.88-36.40 "ومن هاد المنطلق وفرنا لك تدريب متخصص في التعديل والمونتاج باستعمال الذكاء الاصطناعي"
a, b = SC[7], SC[8]; K = dict(out="left")
card(20, w(31.18), b, 640, 470, 760, 520, 44, PURP, **K)
icon_at(24, w(31.18) + 0.1, b, 640, 360, "film", 120, CARD, PURP, enter="pop", **K)
txt(25, w(31.18) + 0.15, b, 640, 520, "AI Editing", "T", f"\\fs86\\c{CARD}", **K)
el(25, w(31.18) + 0.25, b, 640, 600, "ORANUSS ACADEMY", f"\\fs30\\fsp4\\c{LILAC}", style="H", **K)
sparkle_ui(31.18, 640, 470, 1.2)
akw(w(31.88), b, 1380, 230, "تدريب متخصص", 92, **K)
for i, (t0, lab) in enumerate(((33.08, "التعديل"), (33.94, "المونتاج"), (35.18, "الذكاء الاصطناعي"))):
    y = 420 + i * 130
    card(20, w(t0), b, 1380, y, 560, 104, 30, enter="left", **K)
    el(23, w(t0), b, 1590, y, co(0, 0, 60), f"\\c{[LILAC, SKY, PEACH][i]}", enter="left", **K)
    alabel(24, w(t0) + 0.05, b, 1340, y + 2, lab, 38, enter="left", **K)
    check(26, w(t0) + 0.35, b, 1170, y, 44, **K)

# S9 36.40-40.12 "ولكن الفرصة ما كتوقفش غير عن تعلم المهارة"
a, b = SC[8], SC[9]; K = dict(out="fade")
akw(w(36.63), b, 960, 210, "الفرصة ما كتوقفش", 96, **K)
card(20, w(38.78), b, 1230, 560, 420, 340, 40, **K)
tile(23, w(38.78) + 0.05, b, 1230, 520, 150, 150, PURP, "book", r=36, shadow=False, **K)
alabel(25, w(38.78) + 0.1, b, 1230, 660, "تعلم المهارة", 40, **K)
check(28, w(39.26), b, 1400, 410, 60, **K)
el(21, w(39.26) + 0.2, b, 960, 560, rr(0, 0, 80, 8, 4), f"\\c{LINE}", enter="left", **K)
card(20, w(39.26) + 0.25, b, 690, 560, 420, 340, 40, **K)
el(23, w(39.26) + 0.3, b, 690, 540, co(0, 0, 150), f"\\c{LILAC}", enter="pop", **K)
el(24, w(39.26) + 0.35, b, 690, 544, "؟", f"\\fs96\\c{PURP}", style="AR", enter="pop", **K)
for k in range(2):
    E(22, w(39.6) + k * 0.45, w(39.6) + k * 0.45 + 0.8, "Shape", f"{{\\an5\\pos(690,540)\\1a&HFF&\\bord5\\3c{PURP}\\fscx70\\fscy70"
                                                            f"\\t(0,800,{OUT},\\fscx150\\fscy150\\3a&HFF&)\\p1}}{co(0, 0, 150)}{{\\p0}}")

# S10 40.12-42.60 "تقدر حتى تستثمر هاد التدريب تجارياً"
a, b = SC[9], SC[10]; K = dict(out="left")
tile(20, w(40.56), b, 960, 440, 300, 300, BLUE, "briefcase", r=60, enter="pop", **K)
apill(30, w(41.07), b, 1230, 260, "التدريب", PURP, fs=34, ic="film", enter="pop", **K)
akw(w(41.51), b, 960, 740, "تجارياً", 120, PURP, **K)
tile(30, w(41.51) + 0.15, b, 700, 300, 120, 120, YELLOW, "coins", r=32, enter="pop", **K)
sparkle_ui(41.51, 960, 740, 0.8)

# S11 42.60-46.96 "تجيب زبناء مهتمين وتبيع لهم التدريب بالثمن اللي كتحدد نتا"
a, b = SC[10], SC[11]; K = dict(out="up")
akw(w(42.82), b, 1460, 200, "زبناء مهتمين", 84, **K)
card(20, w(42.82), b, 1460, 500, 560, 400, 40, **K)
cols = [CORAL, BLUE, GREEN]
for i in range(3):
    avatar(22, w(42.94) + i * 0.1, b, 1300 + i * 160, 450, 120, cols[i], **K)
    icon_at(26, w(43.50) + 0.3 + i * 0.1, b, 1300 + i * 160 + 46, 395, "heart", 40, CORAL, CARD, enter="pop", **K)
apill(30, w(43.50), b, 1460, 620, "تبيع لهم التدريب", GREEN, fs=34, ic="send", enter="pop", **K)
card(20, w(44.91), b, 560, 500, 600, 440, 40, **K)
tile(23, w(44.91) + 0.05, b, 560, 400, 130, 130, YELLOW, "coins", r=34, shadow=False, **K)
alabel(25, w(44.91) + 0.1, b, 560, 520, "الثمن", 44, **K)
el(24, w(44.91) + 0.15, b, 560, 610, rrect(440, 14, 7), f"\\c{LINE}", enter="fade", **K)
E(25, w(45.58), b - 0.3, "Shape", f"{{\\an4\\pos(340,610)\\c{PURP}\\fscx20\\t(0,700,{OUT},\\fscx75)\\p1}}{rrect(440, 14, 7)}{{\\p0}}")
E(26, w(44.91) + 0.15, w(45.58), "Shape", f"{{\\an5\\pos(428,610)\\c{CARD}\\bord6\\3c{PURP}\\fad(150,0)\\p1}}{co(0, 0, 44)}{{\\p0}}")
E(26, w(45.58), b - 0.3, "Shape", f"{{\\an5\\move(428,610,670,610,0,700)\\c{CARD}\\bord6\\3c{PURP}\\p1}}{co(0, 0, 44)}{{\\p0}}")
E(26, b - 0.3, b, "Shape", f"{{\\an5\\move(670,610,670,540)\\c{CARD}\\bord6\\3c{PURP}\\t(0,300,{IN},\\alpha&HFF&)\\p1}}{co(0, 0, 44)}{{\\p0}}")
akw(w(45.96), b, 560, 820, "اللي كتحدد نتا", 72, PURP, **K)

# S12 46.96-51.26 "والربح اللي كيبقى من عملية البيع كيرجع لك بنسبة 100%"
a, b = SC[11], SC[12]; K = dict(out="fade")
akw(w(47.22), b, 620, 230, "الربح", 110, **K)
card(20, w(47.22), b, 620, 560, 480, 360, 40, **K)
tile(23, w(47.22) + 0.05, b, 620, 520, 180, 180, GREEN, "coins", r=44, shadow=False, **K)
alabel(25, w(48.80), b, 620, 680, "عملية البيع", 38, MUTED, **K)
for k in range(6):   # coins flowing to you
    t0 = w(48.80) + k * 0.14
    E(30, t0, t0 + 0.6, "Shape", f"{{\\an5\\move(760,520,1180,480)\\c{YELLOW}\\bord4\\3c{ORANGE}\\fad(60,120)\\p1}}{co(0, 0, 34)}{{\\p0}}")
ring(30, w(49.22), b, 1340, 480, 380, 36, 1.0, PURP, w(49.22) + 0.1, fill_dur=0.95, out="fade")
txt(34, w(50.21), b, 1340, 470, "100%", "T", "\\fs120", enter="pop", **K)
akw(w(49.22), b, 1340, 790, "كيرجع لك", 80, PURP, **K)
sparkle_ui(50.21, 1340, 470, 1.2)
wipe(SC[12])

# S13 51.26-56.45 "إذن إلا بغيتي تستغل هاد الفرصة وتتعلم كيفاش تستافد من الذكاء الاصطناعي"
a, b = SC[12], SC[13]; K = dict(out="left")
akw(w(52.16), b, 1300, 260, "تستغل هاد الفرصة", 92, **K)
tile(30, w(52.82), b, 1680, 470, 140, 140, YELLOW, "star", r=36, enter="pop", **K)
sparkle_ui(52.82, 1680, 470, 0.7)
sx, sy, swd, sh = phone(20, w(53.33), b, 600, 500, 780, **K)
scx = sx + swd // 2
el(24, w(53.33) + 0.1, b, scx, sy + 200, rrect(swd - 40, 260, 26), f"\\c{LILAC}", **K)
el(25, w(53.33) + 0.15, b, scx, sy + 200, co(0, 0, 100), f"\\c{PURP}", enter="pop", **K)
el(26, w(53.33) + 0.15, b, scx + 4, sy + 200, "m 0 0 l 30 20 l 0 40", f"\\c{CARD}", enter="pop", **K)
el(25, w(53.33) + 0.2, b, scx, sy + 360, rrect(swd - 60, 12, 6), f"\\c{LINE}", **K)
E(26, w(53.6), b - 0.3, "Shape", f"{{\\an4\\pos({sx + 30},{sy + 360})\\c{PURP}\\fscx0\\t(0,2400,\\fscx70)\\p1}}{rrect(swd - 60, 12, 6)}{{\\p0}}")
for i in range(3):
    y = sy + 460 + i * 90
    el(24, w(53.6) + i * 0.08, b, scx, y, rrect(swd - 40, 72, 20), "\\c&H00FBF7F8&", **K)
    check(26, w(53.9) + i * 0.3, b, sx + swd - 60, y, 36, **K)
akw(w(53.33), b, 1300, 430, "وتتعلم كيفاش", 72, MUTED, **K)
apill(40, w(54.91), b, 1300, 600, "الذكاء الاصطناعي", PURP, fs=40, h=92, ic="chip", enter="pop", **K)

# S14 56.45-60.30 "تواصل معايا أو مع الفريق ديالنا في الخاص في أقرب وقت"
a, b = SC[13], SC[14]; K = dict(out="fade")
akw(w(56.50), b, 600, 330, "تواصل معايا", 104, **K)
akw(w(58.43), b, 600, 480, "في الخاص", 104, PURP, **K)
apill(40, w(59.27), b, 600, 640, "في أقرب وقت", YELLOW, INKT, fs=36, ic="clock", enter="pop", **K)
sx, sy, swd, sh = phone(20, a + 0.05, b, 1340, 500, 800, **K)
scx = sx + swd // 2
el(24, a + 0.1, b, scx, sy + 60, rrect(swd, 120, 0), "\\c&H00FBF7F8&", enter="fade", **K)
avatar(25, a + 0.15, b, sx + swd - 70, sy + 62, 64, PURP, **K)
alabel(26, a + 0.2, b, scx - 30, sy + 64, "Oranuss Academy", 30, **K)
for k in range(3):   # typing dots
    E(27, w(56.8) + k * 0.12, w(57.39), "Shape", f"{{\\an5\\pos({sx + swd - 130 + k * 30},{sy + swd + 100})\\c{MUTED}\\fad(100,0)\\p1}}{co(0, 0, 16)}{{\\p0}}")
el(27, w(57.39), b, scx + 40, sy + swd + 100, rrect(260, 84, 30), f"\\c{PURP}", enter="up", **K)
alabel(28, w(57.39), b, scx + 40, sy + swd + 102, "بغيت نتسجل", 30, CARD, enter="up", **K)
icon_at(30, w(57.8), b, sx + swd - 50, sy + sh - 60, "send", 56, PURP, CARD, enter="pop", **K)
E(29, w(57.8), w(57.8) + 0.5, "Shape", f"{{\\an5\\pos({sx + swd - 50},{sy + sh - 60})\\1a&HFF&\\bord5\\3c{LILAC}\\fscx30\\fscy30\\t(0,500,{OUT},\\fscx130\\fscy130\\3a&HFF&)\\p1}}{co(0, 0, 90)}{{\\p0}}")
el(27, w(58.43) + 0.2, b, scx - 40, sy + swd + 220, rrect(260, 84, 30), "\\c&H00F5E9EC&", enter="up", **K)
alabel(28, w(58.43) + 0.2, b, scx - 40, sy + swd + 222, "مرحبا بيك!", 30, INKT, enter="up", **K)

# end card
a, b = SC[14], SC[15]; K = dict(out="none")
wipe(a)
tile(20, a + 0.15, b, 960, 360, 170, 170, PURP, "film", r=44, enter="pop", **K)
txt(22, a + 0.25, b, 960, 540, "ORANUSS ACADEMY", "T", "\\fs90\\fsp6", **K)
pill(22, a + 0.45, b, 960, 650, "AI Editing", PURP, fs=34, h=76, ic="chip", enter="pop", **K)
alabel(22, a + 0.6, b, 960, 770, "تواصل معايا في الخاص", 44, MUTED, enter="up", **K)
sparkle_ui(a + 0.3, 960, 540, 1.2)

write_ass(os.path.join(WK, "scenes.ass"), HEAD)

# ---------- sound: voice + OrcaXV SFX (each on a visual event), -14 LUFS ----------
CAT = {r["id"]: r for r in csv.DictReader(open(os.path.join(SK, "scripts", "catalog.tsv"), encoding="utf-8"), delimiter="\t")}
LEVEL = {"loud": -12.0, "normal": -9.0, "quiet": -6.0}
CUES = [  # (time, id, align, extra dB, trim)
    (w(0.38), "DA-002", "start", -4, None), (w(2.23), "WH-004", "peak", 0, None), (w(2.95), "PO-019", "peak", -2, None),
    (SC[1], "WH-174", "peak", -2, None), (w(5.48), "UI-028", "start", -6, 1.6), (w(6.90), "GL-004", "peak", -4, None),
    (w(7.48) + 0.25, "IM-029", "peak", -5, 1.4), (w(9.07) + 0.35, "NG-007", "peak", -10, None),
    (SC[2], "WH-175", "peak", 0, None), (w(10.30), "PO-006", "peak", 0, None), (w(11.58), "PO-019", "peak", -3, None), (w(12.94), "PO-008", "peak", 0, None),
    (SC[3], "WH-012", "peak", -2, None), (w(14.44), "PO-016", "peak", 0, None), (w(16.90), "WH-091", "peak", 0, None), (17.55, "UI-041", "peak", 0, None),
    (SC[4], "WH-176", "peak", 0, None), (w(19.70), "PO-009", "peak", 0, None), (w(20.26), "UI-029", "peak", -4, None), (w(20.96), "PO-006", "peak", 0, None),
    (SC[5], "WH-166", "peak", -2, None), (w(24.00), "DA-007", "peak", -2, None), (w(24.45), "PO-013", "peak", -4, 1.8),
    (SC[6], "WH-174", "peak", -2, None), (w(26.58), "RW-006", "peak", -3, 1.6), (w(28.26), "PO-022", "peak", 0, None),
    (SC[7], "WH-156", "peak", 0, None), (w(31.18), "RS-012", "peak", -6, 3.0), (w(33.08) + 0.35, "UI-019", "peak", 0, None),
    (w(33.94) + 0.35, "UI-019", "peak", 0, None), (w(35.18) + 0.35, "PO-019", "peak", -3, None),
    (SC[8], "WH-175", "peak", 0, None), (w(39.26), "PO-013", "peak", -4, 1.6), (w(39.6), "HO-018", "peak", -10, None),
    (SC[9], "WH-163", "peak", -2, None), (w(40.56), "PO-008", "peak", 0, None), (w(41.51), "IM-029", "peak", -6, 1.4),
    (SC[10], "WH-012", "peak", -2, None), (w(42.94), "PO-006", "peak", 0, None), (w(43.50), "WH-004", "peak", 0, None),
    (w(45.58), "UI-005", "peak", 0, None), (w(46.0), "RW-020", "peak", 0, 1.8),
    (SC[11], "WH-176", "peak", 0, None), (w(48.80), "RW-010", "peak", -2, 2.0), (w(50.21), "RW-008", "peak", -4, 2.0),
    (SC[12], "WH-158", "peak", -2, None), (w(52.82), "PO-016", "peak", 0, None), (w(53.9), "UI-019", "peak", 0, None), (w(54.91), "PO-009", "peak", 0, None),
    (SC[13], "WH-166", "peak", -2, None), (w(56.8), "UI-004", "start", -8, 0.6), (w(57.8), "UI-029", "peak", -3, None),
    (w(58.43) + 0.2, "UI-006", "peak", -8, 1.2), (SC[14], "WH-156", "peak", -2, None), (SC[14] + 0.25, "LO-003", "peak", -8, 1.8),
]
rows = []
for t, sid, align, extra, trim in CUES:
    s = CAT[sid]; dur, peak = float(s["dur_s"]), float(s["peak_s"] or 0)
    eff = min(dur, trim) if trim else dur
    start = t - peak if align == "peak" else t - eff if align == "end" else t
    rows.append((max(start, 0), max(-start, 0), trim, LEVEL[s["level"]] + extra, os.path.join(SK, "sounds", s["path"]), t, sid, s["name"]))

def lufs(args):
    m = subprocess.run([FF, "-hide_banner"] + args + ["-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", m)[-1])
VCH = "aresample=48000,highpass=f=70,equalizer=f=3500:t=q:w=1.2:g=1.5,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120"
vgain = -20.0 - lufs(["-i", VOICE, "-af", VCH + ",ebur128"])          # voice at -20 LUFS before the mix (SFX gains are set against that)
g = [f"[0:a]{VCH},volume={vgain:.2f}dB,apad=whole_dur={TOTAL}[vo]"]
labels = ["[vo]"]
for i, (st, skip, trim, gain, path, *_r) in enumerate(rows):
    c = f"[{i + 1}:a]aresample=48000,pan=mono|c0=0.5*c0+0.5*c1"
    if skip:
        c += f",atrim=start={skip:.3f},asetpts=PTS-STARTPTS"
    if trim:
        c += f",atrim=0:{trim},afade=t=out:st={max(trim - 0.25, 0):.3f}:d=0.25"
    c += f",volume={gain}dB,adelay={ms(st)}:all=1[s{i}]"
    g.append(c); labels.append(f"[s{i}]")
g.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,atrim=0:{TOTAL},alimiter=limit=0.7:level=0,pan=stereo|c0=c0|c1=c0[a]")
open(os.path.join(WK, "audio_filter.txt"), "w").write(";\n".join(g))
MIX = os.path.join(WK, "mix.wav")
cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", "-i", VOICE] + sum([["-i", r[4]] for r in rows], [])
subprocess.run(cmd + ["-/filter_complex", os.path.join(WK, "audio_filter.txt"), "-map", "[a]", "-c:a", "pcm_s24le", MIX + ".pre.wav"], check=True)
trim_db = -14.0 - lufs(["-i", MIX + ".pre.wav", "-af", "ebur128"])
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", MIX + ".pre.wav", "-af", f"volume={trim_db:.2f}dB,alimiter=limit=0.84:level=0",
                "-c:a", "pcm_s24le", MIX], check=True)
with open(os.path.join(OUTDIR, "sfx-cue-sheet.md"), "w") as f:
    f.write("# AI training offer: SFX cue sheet (OrcaXV Essentials 100)\n\n> Developed by Mehdi ORANUSS | Powered by Claude\n\n"
            "| Time | Place clip at | ID | Sound | Gain |\n|---|---|---|---|---|\n")
    for st, skip, trim, gain, path, t, sid, name in rows:
        f.write(f"| {t:6.2f} | {st:6.2f} | {sid} | {name} | {gain:+.0f} dB |\n")
    f.write("\n---\n\nDeveloped by Mehdi ORANUSS | Powered by Claude\n")

# ---------- picture: slow push per scene, reset on each cut ----------
ZK = [(0.0, 1.0)]
for s0, s1 in zip(SC[:-1], SC[1:]):
    ZK += [(s0 + 0.001, 1.0), (s1 - 0.001, 1.028)]
ZK.append((TOTAL, 1.028))
z = zexpr(sorted(set(ZK)))
sc_ass = os.path.join(WK, "scenes.ass").replace(":", "\\:")
vf = (f"ass='{sc_ass}',scale=w='trunc(1920*({z})/2)*2':h='trunc(1080*({z})/2)*2':eval=frame:flags=bicubic,"
      f"crop=1920:1080:(iw-1920)/2:(ih-1080)/2,format=yuv420p")
if MODE == "stills":
    import shutil; shutil.rmtree(os.path.join(WK, "stills"), ignore_errors=True)
    os.makedirs(os.path.join(WK, "stills"), exist_ok=True)
    for i, t in enumerate([2.8, 8.0, 12.6, 17.2, 20.9, 24.6, 28.8, 34.8, 39.8, 42.0, 46.2, 50.6, 55.4, 59.6, 61.4]):
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-copyts", "-ss", str(t), "-f", "lavfi", "-i", f"color=c=0xF2EEFF:s=1920x1080:r=30:d={TOTAL}",
                        "-vf", vf.replace("format=yuv420p", "format=rgb24"), "-frames:v", "1",
                        os.path.join(WK, "stills", f"s{i:02d}_{t}.png")], check=False)
    print("stills ok")
else:
    out = os.path.join(OUTDIR, f"AI-Training-Offer-16x9-PREVIEW-{VERSION}.mp4")
    if os.path.exists(out):
        sys.exit(f"{out} exists: pass a new version")
    part = os.path.join(WK, f"rendering-{VERSION}.mp4")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"color=c=0xF2EEFF:s=1920x1080:r=30:d={TOTAL}",
                    "-i", MIX, "-vf", vf, "-map", "0:v", "-map", "1:a", "-t", str(TOTAL), "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                    "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", part], check=True)
    os.replace(part, out)
    print("ok", out)
print(len(base.ev), "events,", len(rows), "sfx, voice gain", round(vgain, 2), "trim", round(trim_db, 2))
