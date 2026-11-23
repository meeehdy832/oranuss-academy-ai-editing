# Developed by Mehdi ORANUSS | Powered by Claude
"""AI Editing launch (16:9, 60.5 s): faceless motion graphics on the voiceover
input/voiceover/ElevenLabs_..._Khalil...mp3, style pastel-app-ui (reference/styles/long/pastel-app-ui/STYLE.md),
background music music/sub_clair-background-music-591220 (2).mp3 ducked under the voice.
One scene per sentence; every graphic lands on its spoken word (LEAD). Latin-Darija captions in a second, static ASS.
Writes work/ai-editing/{scenes.ass, captions.ass, filter.txt, render.sh}, output/ai-editing/captions-ai-editing-latin-darija.srt"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import OUT, IN
import styles.base as base
from styles.base import E, ms, rrect, co, rr, write_ass, place_sfx, zexpr
from styles.pastel_ui import (HEADER, CARD, INKT, MUTED, LINE, PURP, NEON, LILAC, ORANGE, YELLOW, GREEN, CORAL, BLUE, SKY,
                              PEACH, MINT, el, card, phone, txt, pill, icon_at, tile, avatar, ring, bar, check, skeleton,
                              sparkle_ui, wipe, background)
from styles.purple_glass import chunk_words, write_srt

ROOT = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.dirname(ROOT)
WK = os.path.join(ROOT, "work", "ai-editing")
KIT = os.path.join(ROOT, "work", "sfx", "kit")
VOICE = glob.glob(os.path.join(TOP, "input", "voiceover", "*.mp3"))[0]
MUSIC = os.path.join(TOP, "music", "sub_clair-background-music-591220 (2).mp3")
OUT_MP4 = os.path.join(TOP, "output", "ai-editing", "AI-Editing-16x9-PREVIEW-v1.mp4")
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
SPEECH_END, TOTAL = 58.30, 60.5
LEAD = 0.067
def w(t):   # graphic entrance for a word spoken at t
    return t - LEAD

# ---------- words (whisper large-v3 -l ar, one Latin-Darija token per Arabic token) ----------
RAW = """0.06 W 0.56 akhiran 0.97 9derna|ntel9ou 1.44 t-tadrib 2.00 dyal 2.47 AI 3.04 Editing 3.55 f 4.27 Oranuss 4.95 Academy.
5.68 Daba 5.87 tkhayyel 6.27 m3aya 6.79 annak 6.94 t9der 7.28 tntej 7.62 3adad 7.87 kbir 8.21 mn 8.38 l-videos 9.63 b-nafs 9.82 l-uslub 10.52 w-l-hawiya 11.04 dyalk,
11.48 sawa2 11.88 mo7tawa 12.43 twil 12.78 awla 13.00 mo7tawa 13.48 9sir.
13.96 W-l-ahamm 14.47 mn 14.63 had 14.96 chi 15.23 annak 15.48 t9der 15.81 tdereb 16.14 d-dakaa 16.65 l-istina3i 17.40 3la 17.92 l-mo7tawa 18.25 dyalk
18.82 bach 19.10 twelli 19.47 tntej 19.93 videos 20.65 b-jawda 21.06 3alya 21.52 w-b-tari9a 22.18 i7tirafiya.
23.06 Had 23.33 l-mahara 24.03 wellat 24.23 mn 24.41 bin 24.74 ktar 25.04 l-maharat 25.76 l-matlouba 26.48 7aliyan.
27.16 W-t9der 27.68 tstaghelha 28.40 b-toro9 28.84 mokhtalifa:
29.54 Ttawwer 29.85 l-mo7tawa 30.48 dyalk 30.93 ch-chakhsi 31.48 awla 31.66 t-tijari,
32.38 t9addem 32.75 9ima 33.09 idafiya 33.64 l-l-khadamat 34.22 w-l-mountajat 35.00 dyalk,
35.56 tsta3melha 36.22 bach 36.48 tsewwe9 36.81 l-mountajat 37.49 lli 37.83 katbi3,
38.36 awla 38.56 t7awwelha 39.15 l-khidma 39.66 mousta9illa 40.34 t9addemha 40.91 l-ch-charikat 41.58 w-l-achkhas 42.44 w-terba7 42.82 menha.
43.34 W-7na 43.66 ghadi 43.98 n3allmouk 44.46 kifach 44.86 dir 45.18 had 45.42 chi 45.82 khatwa 46.06 b-khatwa
46.58 mn 46.78 khilal 47.18 tadrib 47.69 tatbi9i 48.28 w-b-jawda 48.88 3alya.
49.44 Ila 49.65 bghiti 49.93 ttawwer 50.20 l-maharat 50.77 dyalk 51.12 w-tkoun 51.47 mn 51.61 n-nas 51.97 lli 52.24 ghadi 52.52 ystafdou 53.05 mn 53.21 had 53.52 l-forsa,
53.94 tewasel 54.50 m3ana 54.83 daba 55.40 w-7jez 55.72 l-blasa 56.37 dyalk 56.69 9bel 56.93 ma 57.09 tkmel 57.40 l-ma9a3id!"""
SENT_END = [5.50, 11.50, 14.00, 18.80, 23.10, 27.00, 29.30, 32.40, 35.40, 38.20, 43.40, 46.40, 49.40, 53.90, 58.08]
toks = RAW.split()
WORDS = []
for t, word in zip(toks[::2], toks[1::2]):
    WORDS.append([float(t), None, word.replace("|", " ").replace("-", "-")])
for i, wd in enumerate(WORDS):
    nxt = WORDS[i + 1][0] if i + 1 < len(WORDS) else SPEECH_END
    ends = [e for e in SENT_END if wd[0] < e <= nxt]
    wd[1] = min(ends[0] if ends else nxt, wd[0] + 1.2)
WORDS = [tuple(x) for x in WORDS]
KEYWORDS = {"ai", "editing", "oranuss", "academy.", "l-videos", "l-uslub", "w-l-hawiya", "twil", "9sir.", "d-dakaa", "l-istina3i",
            "b-jawda", "3alya", "i7tirafiya.", "l-matlouba", "7aliyan.", "mokhtalifa:", "ch-chakhsi", "t-tijari,", "9ima", "idafiya",
            "tsewwe9", "mousta9illa", "w-terba7", "khatwa", "b-khatwa", "tatbi9i", "l-forsa,", "l-blasa", "l-ma9a3id!", "daba"}

# ---------- scenes ----------
SC = [0.0, 5.55, 11.45, 13.95, 18.75, 23.0, 27.1, 29.45, 32.3, 38.3, 43.25, 49.35, 53.85, SPEECH_END + 0.05, TOTAL]
background(TOTAL)

def stepper(st, en, active, out="left"):
    """3-step tracker for the 'different ways' section (reference: date chips with one active pill)."""
    xs = (820, 960, 1100)
    el(10, st, en, 960, 110, rr(0, 0, 280, 8, 4), f"\\c{LINE}", enter="fade", out=out)
    for i, x in enumerate(xs, 1):
        on = i == active
        el(11, st, en, x, 113, co(0, 0, 84 if on else 62), f"\\c{PURP if on else (LILAC if i < active else CARD)}",
           enter="pop" if on else "fade", out=out)
        el(12, st, en, x, 115, str(i), f"\\fs{38 if on else 30}\\c{CARD if on else PURP}", style="H", enter="pop" if on else "fade", out=out)

def connector(st, en, x0, y0, x1, y1, color=LILAC, out="fade"):
    """Curved line (zero-area path outlined) from (x0,y0) down to (x1,y1)."""
    my = (y0 + y1) / 2
    path = f"m {x0} {y0} b {x0} {my} {x1} {my} {x1} {y1} b {x1} {my} {x0} {my} {x0} {y0}"
    E(9, st, en - 0.3, "Shape", f"{{\\an7\\pos(0,0)\\1a&HFF&\\bord3\\3c{color}\\clip(0,{y0},1920,{y0})"
                               f"\\t(0,450,{OUT},\\clip(0,{y0 - 4},1920,{y1 + 4}))\\p1}}{path}{{\\p0}}")
    E(9, en - 0.3, en, "Shape", f"{{\\an7\\pos(0,0)\\1a&HFF&\\bord3\\3c{color}\\t(0,300,\\3a&HFF&)\\p1}}{path}{{\\p0}}")

# S1 0-5.55 launch: "W akhiran 9derna ntel9ou t-tadrib dyal AI Editing f Oranuss Academy"
a, b = SC[0], SC[1]; K = dict(out="left")
sx, sy, swd, sh = phone(20, 0.10, b, 1350, 470, 760, **K)
scx = sx + swd // 2
el(25, 0.35, b, sx + 70, sy + 74, rrect(56, 56, 28), f"\\c{LILAC}", enter="fade", **K)
el(25, 0.35, b, sx + 170, sy + 66, rrect(120, 16, 8), f"\\c{LINE}", enter="fade", **K)
el(25, 0.35, b, sx + 150, sy + 92, rrect(80, 12, 6), f"\\c{LINE}", enter="fade", **K)
for i in range(3):   # lesson rows (UI chrome)
    yy = sy + 470 + i * 96
    el(25, 0.55 + i * 0.08, b, scx, yy, rrect(swd - 50, 78, 22), f"\\c&H00FBF7F8&", **K)
    el(26, 0.55 + i * 0.08, b, sx + 70, yy, rrect(50, 50, 16), f"\\c{[PEACH, SKY, MINT][i]}", **K)
    el(26, 0.55 + i * 0.08, b, sx + 190, yy - 10, rrect(150, 14, 7), f"\\c{LINE}", **K)
    el(26, 0.55 + i * 0.08, b, sx + 170, yy + 14, rrect(110, 10, 5), f"\\c{LINE}", **K)
card(26, w(2.47), b, scx, sy + 260, swd - 50, 250, 30, PURP, **K)
icon_at(29, w(2.47) + 0.08, b, sx + 90, sy + 200, "film", 64, CARD, PURP, enter="pop", **K)
txt(29, w(2.47) + 0.1, b, scx - 10, sy + 280, "AI Editing", "T", f"\\fs50\\c{CARD}", **K)
el(29, w(4.27), b, scx - 40, sy + 335, "Oranuss Academy", f"\\fs24\\c{LILAC}", style="H", **K)
pill(30, w(0.97), b, 560, 300, "Jdid", CORAL, fs=30, ic="star", enter="pop", **K)
sparkle_ui(0.97, 560, 300, 0.8)
txt(30, w(2.47), b, 600, 440, "AI Editing", "T", "\\fs124", d=60, **K)
el(30, w(4.27), b, 600, 560, "f Oranuss Academy", f"\\fs50\\c{PURP}", style="H", **K)
el(30, w(4.27) + 0.1, b, 600, 620, rr(0, 0, 160, 8, 4), f"\\c{YELLOW}", enter="left", **K)
sparkle_ui(2.47, 600, 440, 1.3)
wipe(SC[1])

# S2 5.55-11.45: "Tkhayyel ... tntej 3adad kbir mn l-videos b-nafs l-uslub w-l-hawiya dyalk"
a, b = SC[1], SC[2]; K = dict(out="up")
txt(30, w(7.62), b, 960, 150, "3adad kbir mn l-videos", "T", "\\fs68", **K)
cols = [CORAL, BLUE, YELLOW, GREEN, ORANGE, BLUE, PURP, CORAL, GREEN, YELLOW]
tints = [PEACH, SKY, PEACH, MINT, PEACH, SKY, LILAC, PEACH, MINT, PEACH]
for i in range(10):
    x = 400 + (i % 5) * 280; y = 390 + (i // 5) * 210; st = w(8.38) + i * 0.07
    card(20, st, b, x, y, 250, 180, 26, **K)
    # thumbnail: varied colours until "b-nafs l-uslub", then one shared look
    el(22, st, w(9.63) + i * 0.03, x, y - 22, rrect(220, 110, 18), f"\\c{tints[i]}", out="none")
    el(22, w(9.63) + i * 0.03, b, x, y - 22, rrect(220, 110, 18), f"\\c{LILAC}", enter="fade", **K)
    el(23, st, w(9.63) + i * 0.03, x, y - 22, co(0, 0, 44), f"\\c{cols[i]}", enter="pop", out="none")
    el(23, w(9.63) + i * 0.03, b, x, y - 22, co(0, 0, 44), f"\\c{PURP}", enter="none", **K)
    el(24, st, b, x + 2, y - 22, "m 0 0 l 16 10 l 0 20", f"\\c{CARD}", **K)
    el(23, st, b, x - 40, y + 58, rrect(140, 12, 6), f"\\c{LINE}", **K)
    el(24, w(10.52) + i * 0.05, b, x + 92, y - 64, co(0, 0, 34), f"\\c{PURP}\\bord4\\3c{CARD}", enter="pop", **K)
    el(25, w(10.52) + i * 0.05, b, x + 92, y - 63, "O", f"\\fs20\\c{CARD}", style="H", enter="pop", **K)
pill(30, w(9.63), b, 730, 760, "Nafs l-uslub", PURP, fs=30, ic="check", enter="pop", **K)
pill(30, w(10.52), b, 1190, 760, "Nafs l-hawiya", NEON, fs=30, ic="heart", enter="pop", **K)

# S3 11.45-13.95: "sawa2 mo7tawa twil awla mo7tawa 9sir"
a, b = SC[2], SC[3]; K = dict(out="left")
card(20, w(11.88), b, 720, 430, 640, 380, 34, **K)
el(22, w(11.88) + 0.05, b, 720, 400, rrect(590, 280, 22), f"\\c{SKY}", **K)
el(23, w(12.43), b, 720, 400, co(0, 0, 90), f"\\c{BLUE}", enter="pop", **K)
el(24, w(12.43), b, 724, 400, "m 0 0 l 28 18 l 0 36", f"\\c{CARD}", enter="pop", **K)
el(23, w(11.88) + 0.05, b, 720, 575, rrect(560, 10, 5), f"\\c{LINE}", **K)
E(24, w(12.43), b - 0.3, "Shape", f"{{\\an7\\pos(440,570)\\c{BLUE}\\clip(440,560,440,590)\\t(0,{ms(b - 0.3 - w(12.43))},\\clip(440,560,960,590))\\p1}}{rrect(560, 10, 5)}{{\\p0}}")
txt(25, w(12.43), b, 720, 690, "Mo7tawa twil", "H", "\\fs44", **K)
el(25, w(12.43) + 0.05, b, 720, 735, "16:9", f"\\fs26\\c{MUTED}", style="H", **K)
el(26, w(12.78), b, 1100, 430, co(0, 0, 96), f"\\c{YELLOW}", enter="pop", **K)
el(27, w(12.78), b, 1100, 432, "awla", f"\\fs28\\c{INKT}", style="H", enter="pop", **K)
card(20, w(13.48), b, 1400, 430, 230, 400, 34, **K)
el(22, w(13.48) + 0.05, b, 1400, 410, rrect(200, 330, 22), f"\\c{PEACH}", **K)
el(23, w(13.48) + 0.05, b, 1400, 410, co(0, 0, 70), f"\\c{CORAL}", enter="pop", **K)
el(24, w(13.48) + 0.05, b, 1403, 410, "m 0 0 l 22 14 l 0 28", f"\\c{CARD}", enter="pop", **K)
txt(25, w(13.48), b, 1400, 690, "Mo7tawa 9sir", "H", "\\fs44", **K)
el(25, w(13.48) + 0.05, b, 1400, 735, "9:16", f"\\fs26\\c{MUTED}", style="H", **K)

# S4 13.95-18.75: "W-l-ahamm ... t9der tdereb d-dakaa l-istina3i 3la l-mo7tawa dyalk"
a, b = SC[3], SC[4]; K = dict(out="left")
pill(30, w(13.96), b, 960, 120, "L-ahamm", YELLOW, INKT, fs=30, ic="star", enter="pop", **K)
card(20, w(15.81), b, 1240, 470, 520, 560, 40, **K)
ring(23, w(16.14), b, 1240, 430, 300, 26, 1.0, PURP, w(16.14) + 0.3, fill_dur=2.1)
el(22, w(16.14), b, 1240, 430, co(0, 0, 200), f"\\c{LILAC}", enter="pop", **K)
icon_at(24, w(16.14) + 0.1, b, 1240, 430, "chip", 110, PURP, LILAC, enter="pop", **K)
el(25, w(16.14) + 0.06, b, 1240, 432, "AI", f"\\fs34\\c{CARD}", style="T", enter="pop", **K)
txt(25, w(15.81), b, 1240, 650, "Tdereb d-dakaa l-istina3i", "H", "\\fs34", **K)
check(26, 18.35, b, 1390, 300, 60, **K)
for i, (c, t2) in enumerate([(CORAL, PEACH), (BLUE, SKY), (GREEN, MINT)]):
    y = 330 + i * 150; st = w(17.92) + i * 0.08
    card(20, st, b, 520, y, 360, 120, 26, enter="left", **K)
    el(22, st, b, 410, y, rrect(110, 84, 16), f"\\c{t2}", enter="left", **K)
    el(23, st, b, 412, y, "m 0 0 l 18 12 l 0 24", f"\\c{c}", enter="left", **K)
    el(22, st, b, 560, y - 14, rrect(150, 14, 7), f"\\c{LINE}", enter="left", **K)
    el(22, st, b, 540, y + 14, rrect(110, 10, 5), f"\\c{LINE}", enter="left", **K)
    for k in range(3):   # content flowing into the AI
        t0 = st + 0.25 + k * 0.22
        E(21, t0, t0 + 0.55, "Shape", f"{{\\an5\\move(700,{y},1010,{430 + (i - 1) * 30})\\c{c}\\fad(80,120)\\p1}}{co(0, 0, 16)}{{\\p0}}")
txt(25, w(17.40), b, 520, 800, "3la l-mo7tawa dyalk", "H", f"\\fs34\\c{PURP}", **K)

# S5 18.75-23.0: "bach twelli tntej videos b-jawda 3alya w-b-tari9a i7tirafiya"
a, b = SC[4], SC[5]; K = dict(out="up")
card(20, w(19.47), b, 960, 440, 1000, 600, 40, **K)
el(22, w(19.47) + 0.05, b, 960, 400, rrect(940, 440, 26), f"\\c{LILAC}", **K)
for (dx, dy, d, c) in [(-260, -60, 300, SKY), (240, 80, 360, PEACH), (60, -120, 220, MINT)]:
    el(22, w(19.47) + 0.1, b, 960 + dx, 400 + dy, co(0, 0, d), f"\\c{c}\\1a&H40&\\blur40", **K)
el(23, w(19.93), b, 960, 400, co(0, 0, 130), f"\\c{PURP}", enter="pop", **K)
el(24, w(19.93), b, 966, 400, "m 0 0 l 40 26 l 0 52", f"\\c{CARD}", enter="pop", **K)
el(23, w(19.47) + 0.1, b, 960, 668, rrect(860, 12, 6), f"\\c{LINE}", **K)
E(24, w(19.93), b - 0.3, "Shape", f"{{\\an7\\pos(530,662)\\c{PURP}\\clip(530,650,530,690)\\t(0,{ms(b - 0.3 - w(19.93))},\\clip(530,650,1390,690))\\p1}}{rrect(860, 12, 6)}{{\\p0}}")
pill(30, w(20.65), b, 1290, 240, "Jawda 3alya", GREEN, fs=30, ic="check", enter="pop", **K)
sparkle_ui(20.65, 1290, 240, 0.7)
pill(30, w(21.52), b, 640, 240, "I7tirafiya", ORANGE, fs=30, ic="star", enter="pop", **K)

# S6 23.0-27.1: "Had l-mahara wellat mn bin ktar l-maharat l-matlouba 7aliyan"
a, b = SC[5], SC[6]; K = dict(out="left")
card(20, w(23.33), b, 960, 450, 1000, 640, 40, **K)
txt(25, w(25.04), b, 720, 190, "L-maharat l-matlouba", "H", "\\fs40", **K)
el(25, w(23.33), b, 1320, 190, rrect(150, 46, 23), f"\\c{LILAC}", enter="fade", **K)
hs = [0.42, 0.58, 0.95, 0.52, 0.84, 0.66]
for i, hh in enumerate(hs):
    x = 600 + i * 145; ai = i == 2
    el(21, w(23.33), b, x, 470, rrect(90, 380, 18), f"\\c&H00FCF8F9&", enter="fade", **K)
    bar(22, 0, b, x, 660, 90, int(380 * hh), PURP if ai else LILAC, w(24.41) + i * 0.08)
    el(22, w(24.41), b, x, 700, rrect(60, 12, 6), f"\\c{LINE}", enter="fade", **K)
pill(30, w(25.76), b, 890, 255, "AI Editing", PURP, fs=28, ic="up", enter="pop", **K)
pill(30, w(26.48), b, 1320, 190, "7aliyan", GREEN, fs=26, h=46, enter="pop", **K)
sparkle_ui(25.76, 890, 255, 0.6)
wipe(SC[6])

# S7 27.1-29.45: "W-t9der tstaghelha b-toro9 mokhtalifa"
a, b = SC[6], SC[7]; K = dict(out="fade")
pill(30, w(27.16), b, 960, 240, "AI Editing", PURP, fs=36, h=84, ic="chip", enter="pop", **K)
for i, x in enumerate((560, 960, 1360)):
    connector(w(28.40), b, 960, 285, x, 520)
    card(20, w(28.40) + i * 0.08, b, x, 620, 340, 220, 30, **K)
    el(22, w(28.40) + i * 0.08, b, x - 110, 570, co(0, 0, 60), f"\\c{[CORAL, BLUE, GREEN][i]}", enter="pop", **K)
    el(23, w(28.40) + i * 0.08, b, x - 110, 572, str(i + 1), f"\\fs30\\c{CARD}", style="H", enter="pop", **K)
    skeleton(22, w(28.40) + i * 0.08, b, x + 20, 575, 150, 20, w(28.84) + i * 0.1, **K)
    skeleton(22, w(28.40) + i * 0.08, b, x - 10, 640, 260, 18, w(28.84) + i * 0.1 + 0.05, **K)
    skeleton(22, w(28.40) + i * 0.08, b, x - 50, 680, 180, 18, w(28.84) + i * 0.1 + 0.1, **K)
txt(30, w(28.84), b, 960, 860 - 40, "B-toro9 mokhtalifa", "T", "\\fs52", **K)

# S8 29.45-32.3 step 1: "Ttawwer l-mo7tawa dyalk ch-chakhsi awla t-tijari"
a, b = SC[7], SC[8]; K = dict(out="left")
stepper(a, b, 1)
txt(30, w(29.54), b, 960, 250, "Ttawwer l-mo7tawa dyalk", "T", "\\fs60", **K)
tile(20, w(30.93), b, 720, 540, 320, 320, CORAL, "person", "Ch-chakhsi", **K)
el(30, w(31.48), b, 960, 540, co(0, 0, 90), f"\\c{YELLOW}", enter="pop", **K)
el(31, w(31.48), b, 960, 542, "awla", f"\\fs26\\c{INKT}", style="H", enter="pop", **K)
tile(20, w(31.66), b, 1200, 540, 320, 320, BLUE, "briefcase", "T-tijari", **K)

# S9 32.3-38.3 step 2: "t9addem 9ima idafiya l-l-khadamat w-l-mountajat dyalk, tsta3melha bach tsewwe9 l-mountajat lli katbi3"
a, b = SC[8], SC[9]; K = dict(out="left")
stepper(a, b, 2)
card(20, a + 0.05, b, 660, 520, 460, 620, 40, **K)
el(22, a + 0.1, b, 660, 400, rrect(400, 280, 26), f"\\c{PEACH}", **K)
icon_at(23, a + 0.15, b, 660, 400, "cart", 130, ORANGE, PEACH, enter="pop", **K)
skeleton(22, a + 0.15, b, 610, 590, 300, 22, a + 0.4, **K)
skeleton(22, a + 0.15, b, 580, 635, 240, 18, a + 0.5, **K)
pill(30, w(32.75), b, 790, 245, "+ 9ima idafiya", GREEN, fs=28, enter="pop", **K)
sparkle_ui(32.75, 790, 245, 0.6)
# tabs: khadamat / mountajat
el(25, w(33.64), b, 660, 740, rrect(400, 64, 32), f"\\c&H00FBF7F8&", enter="fade", **K)
el(26, w(33.64), w(34.22), 560, 740, rrect(190, 52, 26), f"\\c{PURP}", enter="pop", out="none")
el(26, w(34.22), b, 760, 740, rrect(190, 52, 26), f"\\c{PURP}", enter="left", d=200, dur=0.3, **K)
el(27, w(33.64), w(34.22), 560, 741, "Khadamat", f"\\fs26\\c{CARD}", style="H", enter="fade", out="none")
el(27, w(34.22), b, 560, 741, "Khadamat", f"\\fs26\\c{MUTED}", style="H", enter="none", **K)
el(27, w(34.22), b, 760, 741, "Mountajat", f"\\fs26\\c{CARD}", style="H", enter="fade", **K)
sx, sy, swd, sh = phone(20, w(35.56), b, 1300, 500, 700, screen=INKT, **K)
scx = sx + swd // 2
el(25, w(35.56) + 0.1, b, scx, sy + 300, rrect(swd - 30, 420, 24), f"\\c{PEACH}", enter="fade", **K)
icon_at(26, w(35.56) + 0.15, b, scx, sy + 280, "cart", 110, ORANGE, PEACH, enter="pop", **K)
el(26, w(35.56) + 0.2, b, scx, sy + 440, co(0, 0, 64), f"\\c{CARD}\\1a&H30&", enter="pop", **K)
el(27, w(35.56) + 0.2, b, scx + 3, sy + 440, "m 0 0 l 20 13 l 0 26", f"\\c{ORANGE}", enter="pop", **K)
tile(30, w(36.48), b, 1560, 300, 150, 150, CORAL, "megaphone", r=30, **K)
sparkle_ui(36.48, 1560, 300, 0.5)
pill(30, w(37.83), b, scx, sy + 580, "Katbi3", GREEN, fs=28, ic="cart", enter="pop", **K)

# S10 38.3-43.25 step 3: "awla t7awwelha l-khidma mousta9illa t9addemha l-ch-charikat w-l-achkhas w-terba7 menha"
a, b = SC[9], SC[10]; K = dict(out="left")
stepper(a, b, 3)
card(20, w(39.15), b, 640, 500, 520, 520, 40, **K)
tile(22, w(39.15) + 0.05, b, 640, 420, 220, 220, PURP, "briefcase", r=40, **K)
txt(25, w(39.15) + 0.1, b, 640, 610, "L-khidma", "H", "\\fs44", **K)
txt(25, w(39.66), b, 640, 665, "mousta9illa", "H", f"\\fs40\\c{PURP}", **K)
card(20, w(40.34), b, 1260, 470, 560, 470, 40, **K)
for i, (lab, t0, kind) in enumerate([("Ch-charikat", 40.91, "briefcase"), ("L-achkhas", 41.58, "person")]):
    y = 340 + i * 130; st = w(t0)
    el(22, st, b, 1260, y, rrect(500, 104, 26), f"\\c&H00FCF8F9&", **K)
    if kind == "person":
        avatar(23, st, b, 1070, y, 70, CORAL, **K)
    else:
        tile(23, st, b, 1070, y, 76, 76, BLUE, kind, r=22, shadow=False, **K)
    el(25, st, b, 1200, y, lab, f"\\fs32\\c{INKT}\\an4", style="H", **K)
    icon_at(25, st + 0.1, b, 1450, y, "send", 40, PURP, CARD, enter="pop", **K)
tile(22, w(42.44), b, 1160, 620, 130, 110, YELLOW, "coins", r=28, **K)
pill(30, w(42.44) + 0.05, b, 1370, 620, "Terba7", GREEN, fs=30, ic="up", enter="pop", **K)
sparkle_ui(42.44, 1200, 610, 0.6)
wipe(SC[10])

# S11 43.25-49.35: "W-7na ghadi n3allmouk kifach dir had chi khatwa b-khatwa mn khilal tadrib tatbi9i w-b-jawda 3alya"
a, b = SC[10], SC[11]; K = dict(out="left")
sx, sy, swd, sh = phone(20, a + 0.1, b, 640, 470, 780, **K)
scx = sx + swd // 2
card(26, a + 0.3, b, scx, sy + 170, swd - 40, 200, 28, PURP, shadow=False, **K)
icon_at(28, a + 0.4, b, sx + 80, sy + 130, "film", 56, CARD, PURP, enter="pop", **K)
el(28, a + 0.4, b, scx - 10, sy + 200, "AI Editing", f"\\fs40\\c{CARD}", style="T", **K)
for i, t0 in enumerate((45.82, 46.06, 46.40, 46.75)):
    y = sy + 340 + i * 100
    el(25, a + 0.5 + i * 0.07, b, scx, y, rrect(swd - 40, 82, 22), f"\\c&H00FBF7F8&", **K)
    el(26, a + 0.5 + i * 0.07, b, sx + 64, y, co(0, 0, 50), f"\\c{LILAC}", **K)
    el(27, a + 0.5 + i * 0.07, b, sx + 64, y, str(i + 1), f"\\fs22\\c{PURP}", style="H", **K)
    el(26, a + 0.5 + i * 0.07, b, sx + 180, y - 10, rrect(140, 14, 7), f"\\c{LINE}", **K)
    el(26, a + 0.5 + i * 0.07, b, sx + 160, y + 14, rrect(100, 10, 5), f"\\c{LINE}", **K)
    check(28, w(t0), b, sx + swd - 54, y, 40, **K)
el(30, w(43.98), b, 1300, 260, "N3allmouk kifach", f"\\fs36\\c{MUTED}", style="H", **K)
txt(30, w(45.82), b, 1300, 350, "Khatwa b-khatwa", "T", "\\fs76", **K)
pill(30, w(47.18), b, 1300, 500, "Tadrib tatbi9i", PURP, fs=32, h=72, ic="play", enter="pop", **K)
pill(30, w(48.28), b, 1300, 610, "Jawda 3alya", YELLOW, INKT, fs=32, h=72, ic="star", enter="pop", **K)
sparkle_ui(48.28, 1300, 610, 0.6)

# S12 49.35-53.85: "Ila bghiti ttawwer l-maharat dyalk w-tkoun mn n-nas lli ghadi ystafdou mn had l-forsa"
a, b = SC[11], SC[12]; K = dict(out="up")
pill(30, w(49.93), b, 960, 200, "Ttawwer l-maharat dyalk", GREEN, fs=34, h=78, ic="up", enter="pop", **K)
card(20, w(51.12), b, 960, 480, 1000, 300, 150, **K)
cols = [BLUE, CORAL, YELLOW, GREEN, ORANGE, SKY]
for i, dx in enumerate((-380, -250, -120, 120, 250, 380)):
    avatar(22, w(51.61) + abs(dx) / 1200, b, 960 + dx, 480, 104, cols[i], **K)
avatar(24, w(51.12), b, 960, 480, 150, PURP, ring=LILAC, **K)
el(26, w(51.12) + 0.1, b, 960, 588, rrect(96, 40, 20), f"\\c{INKT}", enter="pop", **K)
el(27, w(51.12) + 0.1, b, 960, 589, "Nta", f"\\fs24\\c{CARD}", style="H", enter="pop", **K)
pill(30, w(53.52), b, 960, 760, "L-forsa", YELLOW, INKT, fs=36, h=80, ic="star", enter="pop", **K)
sparkle_ui(53.52, 960, 760, 0.8)

# S13 53.85-58.35: "tewasel m3ana daba w-7jez l-blasa dyalk 9bel ma tkmel l-ma9a3id"
a, b = SC[12], SC[13]; K = dict(out="fade")
card(20, a + 0.05, b, 960, 460, 1100, 700, 44, **K)
txt(25, w(55.40), b, 760, 190, "7jez l-blasa dyalk", "T", "\\fs54", **K)
seats = [(r, c) for r in range(3) for c in range(8)]
mine = (1, 3)
for k, (r, c) in enumerate(seats):
    x = 560 + c * 110; y = 340 + r * 120; st = a + 0.1 + k * 0.012
    if (r, c) == mine:
        icon_at(23, st, w(55.72), x, y, "seat", 84, LINE, CARD, out="none", enter="fade")
        icon_at(23, w(55.72), b, x, y, "seat", 84, GREEN, CARD, enter="pop", **K)
        continue
    order = (k * 7) % len(seats)
    flip = w(56.69) + order * 0.045
    icon_at(23, st, flip, x, y, "seat", 84, LILAC, CARD, out="none", enter="fade")
    icon_at(23, flip, b, x, y, "seat", 84, MUTED, CARD, enter="pop", **K)
for k in range(2):   # pulse on your seat
    E(22, w(55.72) + k * 0.6, w(55.72) + k * 0.6 + 0.8, "Shape", f"{{\\an5\\pos({560 + 3 * 110},460)\\1a&HFF&\\bord5\\3c{GREEN}"
                                                         f"\\fscx60\\fscy60\\t(0,800,{OUT},\\fscx160\\fscy160\\3a&HFF&)\\p1}}{co(0, 0, 110)}{{\\p0}}")
pill(30, a + 0.1, b, 960, 720, "Tewasel m3ana daba", PURP, fs=36, h=88, ic="send", enter="up", **K)
E(40, w(54.50), w(54.83) + 0.4, "Shape", f"{{\\an7\\move(1250,900,1080,735,0,{ms(w(54.83) - w(54.50))})\\fad(100,150)\\c{CARD}\\bord3\\3c{INKT}\\p1}}"
                                          f"m 0 0 l 0 62 l 15 48 l 26 74 l 38 69 l 27 44 l 46 44{{\\p0}}")
E(39, w(54.83), w(54.83) + 0.45, "Shape", f"{{\\an5\\pos(1084,738)\\c{CARD}\\1a&HFF&\\bord4\\3c{LILAC}\\fscx20\\fscy20"
                                          f"\\t(0,450,{OUT},\\fscx100\\fscy100\\3a&HFF&)\\p1}}{co(0, 0, 140)}{{\\p0}}")
el(31, w(56.69), b, 1300, 190, "9bel ma tkmel l-ma9a3id", f"\\fs34\\c{CORAL}", style="H", enter="fade", **K)

# end card 58.35-60.5
a, b = SC[13], SC[14]; K = dict(out="none")
wipe(a)
el(20, a + 0.15, b, 960, 380, co(0, 0, 150), f"\\c{PURP}", enter="pop", **K)
icon_at(21, a + 0.25, b, 960, 380, "chip", 80, CARD, PURP, enter="pop", **K)
txt(22, a + 0.25, b, 960, 540, "ORANUSS ACADEMY", "T", "\\fs90\\fsp6", **K)
pill(22, a + 0.45, b, 960, 650, "AI Editing", PURP, fs=34, h=76, ic="film", enter="pop", **K)
el(22, a + 0.6, b, 960, 760, "7jez l-blasa dyalk daba", f"\\fs42\\c{MUTED}", style="H", enter="up", **K)
sparkle_ui(a + 0.3, 960, 540, 1.2)

write_ass(os.path.join(WK, "scenes.ass"), HEADER)

# ---------- captions: white pill, ink words, active word purple, keywords heavy ----------
base.ev.clear()
chunks = chunk_words(WORDS, SC[1:-2])
srt = []
CY = 1000
for ch in chunks:
    c0, c1 = ch[0][0] - LEAD, ch[-1][1]
    plain = " ".join(x[2] for x in ch)
    wpx = int(len(plain) * 29 + 100)
    E(80, c0, c1, "Shape", f"{{\\an5\\pos(960,{CY + 14})\\c&H00A0306A&\\1a&HE6&\\blur16\\fad(90,90)\\p1}}{rrect(wpx, 92, 46)}{{\\p0}}")
    E(81, c0, c1, "Shape", f"{{\\an5\\pos(960,{CY})\\c{CARD}\\fad(90,90)\\fscx94\\fscy94\\t(0,140,{OUT},\\fscx100\\fscy100)\\p1}}{rrect(wpx, 92, 46)}{{\\p0}}")
    for i, (s, e, _) in enumerate(ch):
        a = c0 if i == 0 else s - LEAD
        z = ch[i + 1][0] - LEAD if i + 1 < len(ch) else c1
        parts = []
        for j, (_, _, wd) in enumerate(ch):
            font = "\\fnAvenir Next Heavy" if wd.lower() in KEYWORDS else "\\fnAvenir Next Demi Bold"
            col = PURP if j == i else (INKT if j < i else MUTED)
            parts.append(f"{{{font}\\c{col}}}{wd}")
        fad = "\\fad(90,0)" if i == 0 else ""
        tail = "\\fad(0,90)" if i == len(ch) - 1 else ""
        E(82, a, z, "Cap", f"{{\\an5\\pos(960,{CY + 2}){fad}{tail}\\fs50}}" + " ".join(parts))
    srt.append((c0, c1, plain))
write_ass(os.path.join(WK, "captions.ass"), HEADER)
write_srt(os.path.join(TOP, "output", "ai-editing", "captions-ai-editing-latin-darija.srt"), srt)

# ---------- picture: slow drift per scene, small reset punch on each cut; captions stay static ----------
ZK = [(0.0, 1.0)]
for s0, s1 in zip(SC[:-1], SC[1:]):
    ZK += [(s0 + 0.001, 1.0), (s1 - 0.001, 1.028)]
ZK.append((TOTAL, 1.028))
z = zexpr(sorted(set(ZK)))
# ---------- sound: SFX on transitions and reveals (<= 1/s), voice polish, music ducked under the voice ----------
CUES = [(0.97, "pop", 0, -14), (2.47, "swell", 0, -16), (SC[1], "whoosh.short", 0, -12), (8.38, "tick", 0, -18), (9.63, "pop", 1, -16),
        (10.52, "pop", 2, -16), (SC[2], "whoosh.short", 1, -14), (12.43, "pop", 0, -16), (13.48, "pop", 3, -16), (SC[3], "whoosh.short", 2, -14),
        (16.14, "riser", 0, -20), (18.35, "click.confirm", 0, -14), (SC[4], "whoosh.short", 0, -14), (20.65, "bell", 2, -18), (21.52, "pop", 1, -16),
        (SC[5], "whoosh.short", 1, -14), (24.41, "tick", 1, -18), (25.76, "pop", 2, -15), (SC[6], "whoosh.long", 0, -13), (28.40, "pop", 0, -17),
        (SC[7], "whoosh.short", 2, -14), (30.93, "pop", 1, -16), (31.66, "pop", 2, -16), (SC[8], "whoosh.short", 0, -14), (32.75, "bell", 4, -18),
        (34.22, "click", 0, -15), (35.56, "whoosh.short", 1, -16), (36.48, "pop", 3, -16), (37.83, "click.confirm", 0, -15),
        (SC[9], "whoosh.short", 2, -14), (40.91, "pop", 0, -17), (41.58, "pop", 1, -17), (42.44, "bell", 6, -17), (SC[10], "whoosh.long", 1, -13),
        (45.82, "tick", 0, -16), (46.06, "tick", 1, -16), (46.40, "tick", 2, -16), (47.18, "pop", 2, -16), (48.28, "bell", 7, -18),
        (SC[11], "whoosh.short", 0, -14), (51.12, "pop", 0, -15), (51.61, "land.light", 0, -17), (53.52, "bell", 8, -17), (SC[12], "whoosh.short", 1, -14),
        (54.83, "click", 1, -12), (55.72, "pop", 1, -15), (56.69, "tick", 2, -20), (SC[13], "whoosh.long", 0, -12), (SC[13] + 0.3, "bell", 0, -15)]
sfx = place_sfx(CUES, KIT)
sc_ass = os.path.join(WK, "scenes.ass").replace(":", "\\:")
cap_ass = os.path.join(WK, "captions.ass").replace(":", "\\:")
duck_end = SPEECH_END + 0.1
g = [f"color=c=0xF2EEFF:s=1920x1080:r=30:d={TOTAL},ass='{sc_ass}',"
     f"scale=w='trunc(1920*({z})/2)*2':h='trunc(1080*({z})/2)*2':eval=frame:flags=bicubic,crop=1920:1080:(iw-1920)/2:(ih-1080)/2,"
     f"ass='{cap_ass}',format=yuv420p[v]",
     f"[0:a]aresample=48000,highpass=f=70,equalizer=f=3500:t=q:w=1.2:g=1.5,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120,"
     f"volume=8dB,apad=whole_dur={TOTAL},asplit=2[vo][vk]",
     f"[1:a]aresample=48000,atrim=0:{TOTAL},asetpts=PTS-STARTPTS,volume='if(lt(t,{duck_end}),0.13,0.13+0.22*min((t-{duck_end})/0.8,1))':eval=frame,"
     f"afade=t=in:d=0.6,afade=t=out:st={TOTAL - 1.4}:d=1.4[mu]",
     f"[mu][vk]sidechaincompress=threshold=0.04:ratio=4:attack=25:release=350:makeup=1[md]"]
labels = ["[vo]", "[md]"]
for i, (st, path, gain) in enumerate(sfx):
    g.append(f"[{i + 2}:a]aresample=48000,volume={gain}dB,adelay={ms(st)}:all=1[s{i}]"); labels.append(f"[s{i}]")
g.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,atrim=0:{TOTAL},"
         f"loudnorm=I=-14:TP=-1.5:LRA=11,volume=0dB,alimiter=limit=0.84:level=0,aresample=48000[a]")
open(os.path.join(WK, "filter.txt"), "w").write(";\n".join(g))
tmp = os.path.join(WK, "rendering-ai-editing.mp4")
inputs = " ".join(f"-i '{p}'" for _, p, _ in sfx)
open(os.path.join(WK, "render.sh"), "w").write(
    f"set -e\n'{FF}' -hide_banner -y -i '{VOICE}' -i '{MUSIC}' {inputs} -/filter_complex '{os.path.join(WK, 'filter.txt')}' "
    f"-map '[v]' -map '[a]' -t {TOTAL} -r 30 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k "
    f"-movflags +faststart '{tmp}'\nmv '{tmp}' '{OUT_MP4}'\n")
print("ok", len(base.ev), "caption events,", len(sfx), "sfx,", len(chunks), "chunks")
