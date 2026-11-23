# Developed by Mehdi ORANUSS | Powered by Claude
"""9:16 reel from input/recordings/650.mp4 (1080x1920, 30 fps, 40.19 s, already edited once: burned-in Arabic captions
0-4.57 s, money B-roll 4.57-6.75 s), in the dark-green style (styles/dark_green.py, reference/styles/short/dark-green/STYLE.md).
Old captions are hidden under frosted bands; captions and graphics stay inside the Reels/TikTok safe zone;
the zoom is anchored on the tracked face (work/650/faces.txt). Earshot `launch` kit sound effects.
v2 (editing-craft upgrades from the video-editor-skill): words lead by 2 frames, "E-COMMERCE" title behind the head
(macOS Vision matte, work/650/roto/masks), zoom-blur whips on 3 cuts, pitch-varied repeat SFX.
Writes work/650/650.ass, 650_behind.ass, filter_650.txt, render.sh, output/650/captions-650-latin-darija.srt.
Render: sh work/650/render.sh"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import pop, spring, exit_
from styles.base import E, ms, co, icon, sparkle, write_ass, place_sfx, ev
import styles.dark_green as dg
from styles.dark_green import EMERALD, GLOW, MINT, FOREST, INK, RED, CAP_Y
dg.apply_palette()
from styles.premium_serif import N, glass, diamond, slide_text, pill, write_srt

ROOT = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(ROOT, "work")
OUT = os.path.join(ROOT, "..", "output", "650")
os.makedirs(OUT, exist_ok=True)
SPEECH_END = 40.19
END_CARD = 40.90   # last frame holds (blurred) so the TRBE7 / TKHSER cards can be read
TOTAL = 42.6
CUT1, CUT2 = 3.20, 4.567   # source cuts: close-up, then money B-roll (crossfades back to the wide shot ~6.75)

# ---------- captions: phrase chunks (start, end, tokens); kinds n sans, b heavy, s italic serif ----------
CHUNKS = [
    (0.02, 1.38, [(0.02, "n", "Ma"), (0.20, "b", "T9DERCH"), N, (0.66, "n", "annak"), (1.00, "s", "ddir")]),
    (1.40, 3.18, [(1.40, "b", "E-COMMERCE"), N, (2.42, "s", "7aliyan"), (3.06, "n", "illa")]),
    (3.20, 4.58, [(3.25, "n", "ma"), (3.38, "n", "kontich"), (3.56, "n", "kat3ref"), N, (3.86, "s", "tdkhel"), (4.11, "b", "LFLOUS")]),
    (4.60, 5.54, [(4.60, "n", "Mlli"), (4.68, "n", "kan9ol"), N, (4.88, "n", "t3ref"), (5.04, "s", "tdkhel"), (5.20, "b", "LFLOUS")]),
    (5.56, 6.98, [(5.56, "n", "kan9ol"), (5.92, "n", "lik"), (6.08, "n", "t3ref"), N, (6.42, "b", "L'BUSINESS")]),
    (7.00, 7.94, [(7.00, "n", "Mlli"), (7.11, "n", "kan9ol"), N, (7.43, "n", "kat3ref"), (7.64, "s", "l'business")]),
    (7.96, 8.98, [(7.96, "n", "ya3ni"), (8.22, "n", "t3ref"), N, (8.40, "b", "TTESWI9")]),
    (9.00, 10.18, [(9.00, "n", "t3ref"), (9.18, "b", "L'I3LANAT"), N, (9.60, "n", "kifach"), (9.83, "s", "kaykhedmo")]),
    (10.20, 11.65, [(10.20, "n", "machi"), (10.34, "n", "fa9at"), N, (10.55, "n", "l'i3lanat"), (11.18, "s", "l'mumawwala")]),
    (11.67, 13.58, [(11.67, "n", "walakin"), (11.95, "b", "L'ADVERTISING"), N, (12.94, "s", "b sifa 3amma")]),
    (13.60, 14.84, [(13.60, "n", "T3ref"), (13.88, "b", "L'BI3"), N, (14.23, "s", "w l'i9na3")]),
    (14.86, 15.98, [(14.86, "n", "w t3ref"), (15.18, "n", "kifach"), N, (15.50, "n", "annak"), (15.71, "s", "tsiyyer")]),
    (16.00, 17.23, [(16.00, "n", "team"), (16.20, "n", "dyal"), N, (16.50, "b", "L'CLOSING")]),
    (17.25, 18.08, [(17.25, "n", "team"), (17.41, "n", "dyal"), N, (17.62, "s", "follow up")]),
    (18.10, 19.15, [(18.10, "n", "T3ref"), N, (18.40, "s", "for example")]),
    (19.17, 20.57, [(19.17, "n", "annak"), (19.39, "n", "tsiyyer"), N, (19.68, "b", "FARI9"), (19.97, "s", "l3oummal")]),
    (20.59, 22.60, [(20.59, "n", "t3ref"), (20.91, "n", "annak"), (21.22, "n", "tsiyyer"), N, (21.57, "b", "LFLOUS"), (22.12, "s", "dyalk")]),
    (22.62, 24.22, [(22.62, "n", "t3ref"), (22.90, "n", "annak"), (23.11, "n", "tsiyyer"), N, (23.54, "b", "L'WE9T"), (23.82, "s", "dyalk")]),
    (24.24, 26.23, [(24.24, "n", "t3ref"), (24.53, "n", "annak"), (24.75, "n", "tsiyyer"), N, (25.25, "b", "L'STRESS"), (25.69, "s", "dyalk")]),
    (26.25, 28.08, [(26.25, "n", "l'oumour"), (26.51, "b", "L9ANOUNIYA"), N, (26.89, "n", "dyalk"), (27.21, "s", "mosta9balan")]),
    (28.10, 29.62, [(28.10, "n", "Ya3ni"), (28.38, "n", "kifach"), N, (28.73, "s", "tsiyyer"), (29.06, "n", "had"), (29.22, "n", "l'oumour")]),
    (29.64, 30.38, [(29.64, "n", "hadou"), N, (29.92, "b", "KAMLIN")]),
    (30.40, 31.58, [(30.40, "n", "khoususan"), (30.71, "n", "katkoun"), N, (30.99, "s", "katfhem"), (31.31, "n", "fihom")]),
    (31.60, 33.25, [(31.60, "n", "t3ref"), (31.84, "n", "lih"), (32.03, "b", "L'7SAB"), N, (32.43, "n", "dyalk"), (32.76, "s", "b yeddik"), (33.00, "n", "hna")]),
    (33.27, 34.78, [(33.27, "n", "La"), (33.40, "s", "plupart"), N, (33.72, "n", "dyal lli f"), (34.21, "b", "E-COMMERCE")]),
    (34.80, 36.08, [(34.80, "n", "7tta"), (34.96, "b", "L'7SAB"), N, (35.30, "n", "ma"), (35.41, "s", "y3erfouhch"), (35.74, "n", "lih")]),
    (36.10, 37.13, [(36.10, "n", "Walakin"), (36.38, "n", "ila"), (36.59, "n", "ma"), N, (36.73, "s", "kat3refch")]),
    (37.15, 37.83, [(37.15, "n", "annak"), (37.36, "n", "7tta"), N, (37.57, "b", "T7SEB")]),
    (37.85, 38.81, [(37.85, "n", "fkifach"), (38.27, "n", "3aref"), N, (38.55, "s", "rassek")]),
    (38.83, 40.18, [(38.83, "n", "ghadi"), (39.11, "b", "TRBE7"), N, (39.39, "n", "wla"), (39.60, "n", "ghadi"), (39.88, "s", "tkhser?")]),
]
def cap_y(t):
    if t < CUT1:
        return 1210          # inside the frosted panel that hides the old green caption
    if t < CUT2:
        return 975           # close-up: on the band that hides the old white caption
    return CAP_Y
srt = dg.captions(CHUNKS, cap_y)

# ---------- helpers ----------
def card(st, en, cx, cy, ic, label, w=310, h=130):
    """Side card: glass, emerald icon disc, label; for lists next to the face."""
    glass(30, st, en, cx, cy, w, h, r=28, dy=36, drift=8)
    E(36, st + 0.08, en, "Shape", f"{{\\an5\\pos({cx - w // 2 + 60},{cy})\\fad(120,200){pop()}{exit_(ms(en - st - 0.08))}\\c{EMERALD}\\bord2\\3c{MINT}\\3a&H40&\\p1}}{co(0, 0, 80)}{{\\p0}}")
    icon(37, st + 0.08, en, cx - w // 2 + 60, cy, ic, 42, f"\\fad(120,200){spring(42, 60)}", fill=EMERALD)
    E(37, st + 0.12, en, "Label", f"{{\\an4\\pos({cx - w // 2 + 112},{cy + 2})\\fs40\\fsp2\\fad(120,200){pop(100, 40)}}}{label}")

def badge(st, en, cx, cy, ic, label, size=150):
    diamond(30, st, en, cx, cy, size, ic, kind="icon")
    slide_text(34, st + 0.10, en, "Serif", cx, cy + int(size * 0.78), "\\an5\\fs50", label, dx=0, dy=16)

# ---------- beats ----------
# HOOK 0 - 4.57: frosted lower panel hides the burned-in captions; topic pill on top
dg.frost_panel(0.0, CUT1, 1000, 420)
dg.frost_panel(CUT1, CUT2, 880, 190, fade_out=180)
pill(0.0, 1.38, 540, 330, "E-COMMERCE", ic="cart")
# 1.36 - 3.18 hero beat: the topic word sits behind his head (cut-out), lands 2 frames before "e-commerce"
ROTO_WIN = [(1.30, CUT1)]
n0 = len(ev)
E(10, 1.333, CUT1, "Heavy", f"{{\\an5\\pos(540,430)\\fs146\\fsp-2\\c{GLOW}\\1a&H40&\\bord0\\blur18\\fad(150,0){pop(100)}}}E-COMMERCE")
E(11, 1.333, CUT1, "Heavy", f"{{\\an5\\pos(540,430)\\fs146\\fsp-2\\c&HFFFFFF&\\fad(150,0){pop(100)}}}E-COMMERCE")
BEHIND = ev[n0:]; del ev[n0:]
sparkle(1.40, 540, 330, 0.9)

# MONEY B-ROLL 4.57 - 6.95 (no face on screen)
diamond(30, 5.20, 6.40, 540, 560, 170, "coins", kind="icon")
diamond(30, 6.42, 7.00, 540, 560, 170, "briefcase", kind="icon")
slide_text(34, 6.50, 7.00, "Serif", 540, 700, "\\an5\\fs58", "l'business", dx=0, dy=16)

# CHECKLIST TRACKER 7.64 - 33.05: L'BUSINESS = 9 skills, one tick per skill as it is named
SKILL_T = [8.40, 9.18, 13.88, 16.70, 19.68, 21.57, 23.54, 25.25, 26.51]
dg.tracker(7.64, 33.05, "L'BUSINESS", SKILL_T, done_at=29.92)

# 8.30 - 13.55 marketing (plate blurred)
badge(8.40, 13.50, 320, 760, "megaphone", "Tteswi9")
badge(9.18, 13.50, 760, 760, "play", "L'i3lanat")
pill(11.95, 13.50, 540, 1080, "ADVERTISING", ic="eye")

# 13.60 - 18.08 sales (face sharp, punch-in): cards beside the face
card(13.88, 18.05, 220, 640, "briefcase", "L'BI3")
card(14.23, 18.05, 220, 800, "chat", "L'I9NA3")
card(16.70, 18.05, 830, 560, "people", "CLOSING")
card(17.62, 18.05, 815, 720, "chat", "FOLLOW UP", w=340)

# 18.10 - 28.05 management (plate blurred): "tsiyyer" + 5 badges
slide_text(34, 19.39, 28.00, "Serif", 540, 560, "\\an5\\fs72", "tsiyyer", dx=0, dy=20)
badge(19.68, 28.00, 250, 730, "people", "Fari9")
badge(21.57, 28.00, 540, 730, "coins", "Lflous")
badge(23.54, 28.00, 830, 730, "clock", "L'we9t")
badge(25.25, 28.00, 395, 990, "pulse", "Stress")
badge(26.51, 28.00, 685, 990, "scale", "L9anouniya")

# 28.10 - 33.25 recap: all ticks flash on "kamlin", then the calculator
sparkle(29.92, 540, 360, 1.0)
badge(32.03, 33.22, 215, 700, "calc", "L'7sab", size=130)

# 33.27 - 36.08 "la plupart ... 7tta l'7sab ma y3erfouhch"
pill(33.40, 34.92, 540, 330, "LA PLUPART", ic="cart")
pill(34.96, 36.06, 540, 330, "L'7SAB", ic="calc")
E(53, 35.41, 36.06, "Shape", f"{{\\an5\\pos(680,300)\\fad(80,200){pop()}\\c{RED}\\bord2\\3c&HFFFFFF&\\p1}}{co(0, 0, 54)}{{\\p0}}")
icon(54, 35.41, 36.06, 680, 300, "cross", 28, f"\\fad(80,200){pop(28)}", fill=RED)

# 38.83 - 40.19 win or lose (plate blurred)
dg.flag(39.11, END_CARD, 540, 700, "TRBE7", "up", EMERALD)
dg.flag(39.88, END_CARD, 540, 880, "TKHSER?", "down", RED, w=340)

# END CARD: ink, brand
E(95, END_CARD, TOTAL, "Shape", f"{{\\an7\\pos(0,0)\\c{INK}\\fad(240,0)\\p1}}m 0 0 l 1080 0 l 1080 1920 l 0 1920{{\\p0}}")
E(96, END_CARD, TOTAL, "Shape", f"{{\\an5\\pos(540,800)\\c{GLOW}\\1a&H60&\\blur60\\fad(300,0)\\p1}}{co(0, 0, 460)}{{\\p0}}")
diamond(97, END_CARD + 0.10, TOTAL + 0.5, 540, 780, 190, "cart", kind="icon")
E(99, END_CARD + 0.30, TOTAL, "Heavy", f"{{\\an5\\pos(540,1010)\\fs76\\fad(200,0){pop(100, 0)}}}ORANUSS ACADEMY")
slide_text(99, END_CARD + 0.45, TOTAL, "Serif", 540, 1100, "\\an5\\fs58", "E-commerce = business", dx=0, dy=20)
sparkle(END_CARD + 0.30, 540, 780, 1.2)

# ---------- sound effects (earshot launch kit) ----------
CUES = [
    (0.0, "pop", 0, -11), (0.20, "snap", 0, -10), (1.40, "tick", 0, -9),
    (CUT1, "whoosh.short", 0, -9), (1.333, "hit", 1, -10), (4.11, "tick", 1, -9),
    (5.20, "pop", 1, -10), (6.42, "pop", 2, -10), (7.00, "whoosh.short", 1, -9), (7.64, "land.light", 0, -9),
    (8.30, "whoosh.short", 1, -8),
    # skills: rising glock notes, one per tick
    (8.40, "bell", 0, -14), (9.18, "bell", 1, -14), (11.95, "pop", 3, -11),
    (13.60, "snap", 0, -9), (13.88, "bell", 2, -14), (14.23, "pop", 0, -11), (16.70, "bell", 3, -14), (17.62, "pop", 1, -11),
    (18.10, "whoosh.short", 2, -8), (19.68, "bell", 4, -14), (21.57, "bell", 5, -14), (23.54, "bell", 6, -14),
    (25.25, "bell", 7, -14), (26.51, "bell", 8, -14),
    (28.10, "land.light", 1, -9), (29.92, "hit", 0, -9), (32.03, "pop", 2, -10),
    (33.25, "whoosh.short", 2, -9), (34.96, "tick", 2, -9), (35.41, "tock", 0, -9),
    (36.10, "land.light", 2, -10), (38.83, "whoosh.short", 0, -8), (39.11, "pop", 3, -10), (39.88, "drop", 0, -12),
    (END_CARD + 0.05, "whoosh.long", 0, -9), (END_CARD + 0.30, "bell", 9, -13),
]
sfx = place_sfx(CUES, os.path.join(W, "sfx", "kit"))

D = os.path.join(W, "650")
write_ass(os.path.join(D, "650.ass"), dg.HEADER)
open(os.path.join(D, "650_behind.ass"), "w", encoding="utf8").write(dg.HEADER + "\n".join(BEHIND) + "\n")
write_srt(os.path.join(OUT, "captions-650-latin-darija.srt"), srt)

# ---------- filter graph ----------
# zoom keys (t, zoom): hard punches are two keys 1 ms apart, placed on sentence starts and source cuts
ZK = [(0.0, 1.06), (CUT1 - 0.15, 1.10), (CUT1, 1.16), (CUT1 + 0.001, 1.08), (CUT1 + 0.25, 1.0), (CUT2, 1.0), (CUT2 + 0.001, 1.02),
      (6.75, 1.05), (6.86, 1.07), (7.00, 1.20), (7.001, 1.20), (7.25, 1.14), (8.30, 1.15), (13.55, 1.08), (13.60, 1.08), (13.601, 1.18), (18.099, 1.21), (18.10, 1.21),
      (18.101, 1.08), (28.05, 1.06), (28.10, 1.06), (28.101, 1.12), (33.10, 1.15), (33.25, 1.30), (33.251, 1.30), (33.50, 1.24), (36.08, 1.26),
      (36.081, 1.12), (38.82, 1.14), (38.821, 1.24), (SPEECH_END, 1.27), (TOTAL, 1.27)]
BLUR_WIN = [(8.30, 13.55), (18.10, 28.05), (38.83, END_CARD + 0.40)]   # last one stays until the end card is opaque
FROST_WIN = [(0.0, CUT1, 1000, 420), (CUT1, CUT2, 880, 190)]
WHIPS = [CUT1, 7.00, 33.25]   # zoom-blur whips (each has a zoom spike in ZK); punches and blurs fill the other beats
fc = dg.filter_graph(os.path.join(D, "650.ass"), TOTAL, SPEECH_END, ZK, BLUR_WIN, FROST_WIN, sfx,
                     hold_from=39.70,   # the source fades to black from 39.73; hold the last clean frame (under the blur)
                     whips=WHIPS, behind_ass=os.path.join(D, "650_behind.ass"), roto_win=ROTO_WIN)
open(os.path.join(D, "filter_650.txt"), "w").write(";\n".join(fc))
dg.render_cmd(os.path.join(D, "render.sh"), os.path.abspath(os.path.join(ROOT, "..", "input", "recordings", "650.mp4")),
              os.path.join(D, "filter_650.txt"), sfx, os.path.abspath(os.path.join(OUT, "Reel-650-PREVIEW-v2.mp4")), TOTAL,
              matte_dir=os.path.join(D, "roto", "masks"))
print(f"events={len(ev)} sfx={len(sfx)} chunks={len(CHUNKS)}")
