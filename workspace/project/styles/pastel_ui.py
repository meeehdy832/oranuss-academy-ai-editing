# Developed by Mehdi ORANUSS | Powered by Claude
"""pastel-app-ui style (reference/styles/long/pastel-app-ui/STYLE.md): faceless 16:9 explainer built from mobile-app UI pieces -
soft lavender canvas, white rounded cards with soft purple shadows, phone mockups, pastel tiles with white glyphs,
big stat type, progress rings, bar charts, avatar stacks, pill tabs. Text in Avenir Next, ink on white.
Every element enters with an eased move (or a pop for small atoms) and leaves with its scene (`el`)."""
import math
from motion import eased_moves, pop, OUT, IN
from styles.base import E, ms, rrect, co, rr, ICONS, ANCHOR, STAR

W, H = 1920, 1080
# ---------- palette (ASS &HBBGGRR&) ----------
BG = "&H00FFEEF2&"       # #F2EEFF lavender canvas
CARD = "&H00FFFFFF&"
INKT = "&H002E1216&"     # #16122E text ink
MUTED = "&H00A3868A&"    # #8A86A3 secondary text
LINE = "&H00F5E9EC&"     # #ECE9F5 hairlines, empty tracks
PURP = "&H00E02B5B&"     # #5B2BE0 brand purple (primary)
NEON = "&H00F65C8B&"     # #8B5CF6 brand glow purple
LILAC = "&H00FFDEE6&"    # #E6DEFF purple tint
ORANGE = "&H003D8AFF&"   # #FF8A3D
YELLOW = "&H003DC8FF&"   # #FFC83D
GREEN = "&H008AC52D&"    # #2DC58A
CORAL = "&H007A6BFF&"    # #FF6B7A
BLUE = "&H00FF8D4C&"     # #4C8DFF
SKY = "&H00FFEBDC&"      # #DCEBFF blue tint
PEACH = "&H00D6E8FF&"    # #FFE8D6 orange tint
MINT = "&H00E5F7DC&"     # #DCF7E5 green tint
SHADOW = "&H00A0306A&"   # #6A30A0 shadow tint (used at high transparency)

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Shape,Arial,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: T,Avenir Next Heavy,72,&H002E1216,&H002E1216,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: H,Avenir Next Demi Bold,40,&H002E1216,&H002E1216,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: B,Avenir Next Medium,28,&H00A3868A,&H00A3868A,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Cap,Avenir Next Demi Bold,50,&H002E1216,&H002E1216,&H00FFEEF2,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def in_cubic(p):
    return p ** 3

# ---------- the one motion primitive: enter, hold, leave with the scene ----------
EXITS = {"left": (-90, 0), "right": (90, 0), "up": (0, -70), "down": (0, 70), "fade": (0, 0)}
def el(layer, st, en, x, y, body, tags="", style="Shape", enter="up", d=40, dur=0.45, out="left", out_dur=0.3):
    """Element at centre (x, y). enter: up/down/left/right (eased travel d px, fade leads), pop (scale 0->104->100),
    fade, none. out: left/right/up/down/fade (eased-in travel + fade over out_dur at the end), none (hard cut)."""
    p1, p0 = ("\\p1", "{\\p0}") if style == "Shape" else ("", "")
    def line(a, b, pos, extra=""):
        if b - a > 0.005:
            E(layer, a, b, style, f"{{\\an5{pos}{extra}{tags}{p1}}}{body}{p0}")
    hold_end = en - (out_dur if out != "none" else 0)
    t = st
    if enter in ("up", "down", "left", "right"):
        dx, dy = {"up": (0, d), "down": (0, -d), "left": (-d, 0), "right": (d, 0)}[enter]
        for k, (a, b, mv) in enumerate(eased_moves(st, x + dx, y + dy, x, y, dur)):
            if b > hold_end:
                break
            line(a, b, mv, f"\\fad({ms(b - a) + 40},0)" if k == 0 else "")
            t = b
    elif enter == "pop":
        line(st, min(st + 0.4, hold_end), f"\\pos({x},{y})", f"\\fad(80,0){pop()}")
        t = min(st + 0.4, hold_end)
    elif enter == "fade":
        line(st, min(st + 0.3, hold_end), f"\\pos({x},{y})", "\\fad(300,0)")
        t = min(st + 0.3, hold_end)
    line(t, hold_end, f"\\pos({x},{y})")
    if out != "none" and hold_end < en:
        ox, oy = EXITS[out]
        line(hold_end, en, f"\\move({x},{y},{x + ox},{y + oy})", f"\\t(0,{ms(en - hold_end)},{IN},\\alpha&HFF&)")

# ---------- building blocks ----------
def card(layer, st, en, x, y, w, h, r=36, fill=CARD, shadow=True, **kw):
    if shadow:
        el(layer, st, en, x, y + 18, rrect(w, h, r), f"\\c{SHADOW}\\1a&HE4&\\blur26", **kw)
    el(layer + 1, st, en, x, y, rrect(w, h, r), f"\\c{fill}", **kw)

def phone(layer, st, en, x, y, h=760, screen=CARD, **kw):
    """Phone mockup centred at (x, y): returns the screen rect (left, top, w, h) for placing UI on it."""
    w = round(h * 0.49)
    el(layer, st, en, x, y + 26, rrect(w, h, 64), f"\\c{SHADOW}\\1a&HD8&\\blur34", **kw)
    el(layer + 1, st, en, x, y, rrect(w, h, 64), f"\\c&H1A1418&", **kw)
    el(layer + 2, st, en, x, y, rrect(w - 24, h - 24, 52), f"\\c{screen}", **kw)
    el(layer + 3, st, en, x, y - h // 2 + 34, rrect(118, 32, 16), f"\\c&H1A1418&", **kw)
    return (x - (w - 24) // 2, y - (h - 24) // 2, w - 24, h - 24)

def txt(layer, st, en, x, y, text, style="H", tags="", **kw):
    el(layer, st, en, x, y, text, tags, style=style, **kw)

def pill(layer, st, en, x, y, text, fill=PURP, color=CARD, fs=30, w=None, h=64, ic=None, k=1.25, **kw):
    fs, h = round(fs * k), round(h * k)
    w = w or int(len(text) * fs * 0.62 + (110 if ic else 64))
    el(layer, st, en, x, y, rrect(w, h, h // 2), f"\\c{fill}", **kw)
    tx = x + (24 if ic else 0)
    if ic:
        icon_at(layer + 1, st, en, x - w // 2 + h // 2 + 6, y, ic, int(h * 0.55), CARD if fill != CARD else PURP, fill, **kw)
    el(layer + 1, st, en, tx, y + 1, text, f"\\fs{fs}\\c{color}", style="H", **kw)
    return w

def icon_at(layer, st, en, x, y, name, size, color=CARD, under=PURP, **kw):
    """ICONS glyph (100x100 box) at (x, y), size px; 'w' parts in color, 'n' (cut-out) parts in the colour underneath."""
    for path, role in ICONS[name]:
        el(layer, st, en, x, y, path + ANCHOR, f"\\fscx{size}\\fscy{size}\\c{color if role == 'w' else under}", **kw)

def tile(layer, st, en, x, y, w, h, fill, name, label=None, r=34, glyph=None, shadow=True, **kw):
    """Pastel tile with a big white glyph (reference: colourful category tiles)."""
    card(layer, st, en, x, y, w, h, r, fill, shadow, **kw)
    gy = y - (22 if label else 0)
    icon_at(layer + 2, st, en, x, gy, name, glyph or int(min(w, h) * 0.42), CARD, fill, **kw)
    if label:
        el(layer + 3, st, en, x, y + h // 2 - 44, label, f"\\fs38\\c{CARD}", style="H", **kw)

PERSON = [(co(31, 10, 38), "w"), ("m 12 96 b 12 58 88 58 88 96", "w")]
ICONS.setdefault("person", PERSON)
def avatar(layer, st, en, x, y, d, fill, ring=CARD, **kw):
    el(layer, st, en, x, y, co(0, 0, d + 10), f"\\c{ring}", **kw)
    el(layer + 1, st, en, x, y, co(0, 0, d), f"\\c{fill}", **kw)
    for path, _ in PERSON:   # glyph clipped to the disc
        el(layer + 2, st, en, x, y + d * 0.06, path + ANCHOR, f"\\fscx{d * 0.78:.0f}\\fscy{d * 0.78:.0f}\\c{CARD}\\1a&H18&", **kw)

def arc(cx, cy, r_out, r_in, a0, a1, step=4):
    """Thick arc polygon from angle a0 to a1 (degrees, 0 = 12 o'clock, clockwise), absolute coords."""
    n = max(2, int(abs(a1 - a0) / step) + 1)
    angs = [a0 + (a1 - a0) * i / (n - 1) for i in range(n)]
    pt = lambda r, a: (cx + r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a)))
    outer = [pt(r_out, a) for a in angs]; inner = [pt(r_in, a) for a in reversed(angs)]
    p = outer + inner
    return f"m {p[0][0]:.1f} {p[0][1]:.1f} " + " ".join(f"l {x:.1f} {y:.1f}" for x, y in p[1:])

def ring(layer, st, en, x, y, d, thick, frac, color, fill_from, fill_dur=0.9, track=LINE, out="left", out_dur=0.3):
    """Progress ring: track + an arc that sweeps to frac (ease-out, no overshoot) from fill_from, exits with the scene."""
    r = d / 2
    el(layer, st, en, x, y, co(0, 0, d), f"\\1a&HFF&\\bord{thick}\\3c{track}", out=out, out_dur=out_dur, enter="fade")
    steps = 24
    hold_end = en - out_dur
    for i in range(1, steps + 1):
        p = 1 - (1 - i / steps) ** 3
        a = fill_from + fill_dur * (i - 1) / steps
        b = fill_from + fill_dur * i / steps if i < steps else hold_end
        if a >= hold_end:
            break
        E(layer + 1, a, min(b, hold_end), "Shape", f"{{\\an7\\pos(0,0)\\c{color}\\p1}}{arc(x, y, r + thick / 2, r - thick / 2, 0, 360 * frac * p)}{{\\p0}}")
    ox, oy = EXITS[out]
    E(layer + 1, hold_end, en, "Shape", f"{{\\an7\\move(0,0,{ox},{oy})\\t(0,{ms(out_dur)},{IN},\\alpha&HFF&)\\c{color}\\p1}}"
                                        f"{arc(x, y, r + thick / 2, r - thick / 2, 0, 360 * frac)}{{\\p0}}")

def bar(layer, st, en, x, base_y, w, h, color, grow_at, grow=0.55, r=14, out="left", out_dur=0.3):
    """Bar anchored at its bottom centre (x, base_y), grows up with an ease-out (bounded: no overshoot)."""
    hold_end = en - out_dur
    E(layer, grow_at, hold_end, "Shape", f"{{\\an2\\pos({x},{base_y})\\fscy0\\t(0,{ms(grow)},{OUT},\\fscy100)\\c{color}\\p1}}{rrect(w, h, r)}{{\\p0}}")
    ox, oy = EXITS[out]
    E(layer, hold_end, en, "Shape", f"{{\\an2\\move({x},{base_y},{x + ox},{base_y + oy})\\t(0,{ms(out_dur)},{IN},\\alpha&HFF&)\\c{color}\\p1}}{rrect(w, h, r)}{{\\p0}}")

def check(layer, st, en, x, y, d=44, fill=GREEN, **kw):
    el(layer, st, en, x, y, co(0, 0, d), f"\\c{fill}", enter="pop", **kw)
    el(layer + 1, st + 0.08, en, x, y, f"m 0 22 l 8 14 l 18 24 l 38 4 l 46 12 l 18 40" + " m 0 0 l 0.1 0 m 46 46 l 45.9 46",
       f"\\fscx{d * 1.6:.0f}\\fscy{d * 1.6:.0f}\\c{CARD}", enter="pop", **kw)

def skeleton(layer, st, en, x, y, w, h, shimmer_at, **kw):
    """Loading placeholder (conceals what is not said yet): grey block with a light sweep."""
    el(layer, st, en, x, y, rrect(w, h, h // 2), f"\\c{LINE}", **kw)
    E(layer + 1, shimmer_at, shimmer_at + 0.7, "Shape",
      f"{{\\an7\\move({x - w // 2 - 120},{y - h // 2},{x + w // 2},{y - h // 2})\\clip({x - w // 2},{y - h // 2},{x + w // 2},{y + h // 2})"
      f"\\c{CARD}\\1a&H50&\\blur12\\p1}}{rrect(110, h, h // 2)}{{\\p0}}")

def sparkle_ui(t, x, y, k=1.0):
    pts = [(-150, -60, 34, YELLOW), (140, -90, 26, PURP), (170, 40, 20, CORAL), (-120, 80, 22, BLUE), (20, -130, 18, GREEN)]
    for i, (dx, dy, s, c) in enumerate(pts):
        a = t + i * 0.06; sc = int(s * k)
        E(70, a, a + 0.85, "Shape", f"{{\\an5\\pos({x + dx * k:.0f},{y + dy * k:.0f})\\c{c}"
                                    f"\\fscx0\\fscy0\\t(0,250,{OUT},\\fscx{sc}\\fscy{sc}\\frz45)\\t(520,850,{IN},\\fscx0\\fscy0\\frz90)\\p1}}{STAR}{{\\p0}}")

def wipe(t, color=PURP, dur=0.62):
    """Brand transition: a rounded purple panel sweeps across the frame (covers the scene change at t)."""
    pw = 2400
    E(95, t - dur / 2, t + dur / 2, "Shape", f"{{\\an4\\move({-pw // 2 - 200},540,{W + pw // 2 + 200},540)\\c{color}\\p1}}{rrect(pw, 1400, 300)}{{\\p0}}")
    E(94, t - dur / 2 + 0.05, t + dur / 2 + 0.05, "Shape", f"{{\\an4\\move({-pw // 2 - 520},540,{W + pw // 2 - 120},540)\\c{LILAC}\\p1}}{rrect(pw, 1400, 300)}{{\\p0}}")

def background(total):
    E(0, 0, total, "Shape", f"{{\\an7\\pos(0,0)\\c{BG}\\p1}}m 0 0 l {W} 0 l {W} {H} l 0 {H}{{\\p0}}")
    for (x0, y0, x1, y1, d, c, a) in [(260, 220, 420, 300, 900, LILAC, "30"), (1700, 860, 1540, 760, 1000, SKY, "40"),
                                      (1650, 120, 1500, 200, 620, PEACH, "60"), (300, 980, 420, 900, 700, MINT, "70")]:
        E(1, 0, total, "Shape", f"{{\\an5\\move({x0},{y0},{x1},{y1})\\c{c}\\1a&H{a}&\\blur120\\p1}}{co(0, 0, d)}{{\\p0}}")

# extra glyphs for this style (100x100 box, same convention as base.ICONS)
ICONS.setdefault("chip", [(rr(20, 20, 60, 60, 12), "w"), (rr(34, 34, 32, 32, 6), "n")]
                 + [(rr(x, 6, 6, 12, 3), "w") for x in (32, 47, 62)] + [(rr(x, 82, 6, 12, 3), "w") for x in (32, 47, 62)]
                 + [(rr(6, y, 12, 6, 3), "w") for y in (32, 47, 62)] + [(rr(82, y, 12, 6, 3), "w") for y in (32, 47, 62)])
ICONS.setdefault("film", [(rr(6, 16, 88, 68, 12), "w"), ("m 42 36 l 64 50 l 42 64", "n")]
                 + [(rr(x, 20, 8, 7, 2), "n") for x in (14, 30, 46, 62, 78)] + [(rr(x, 73, 8, 7, 2), "n") for x in (14, 30, 46, 62, 78)])
ICONS.setdefault("star", [(STAR.replace("m 50 0", "m 50 0"), "w")])
ICONS.setdefault("send", [("m 4 46 l 96 6 l 66 94 l 48 60", "w"), ("m 48 60 l 96 6 l 40 52", "n")])
ICONS.setdefault("seat", [(rr(22, 8, 56, 50, 14), "w"), (rr(12, 52, 76, 22, 10), "w"), (rr(18, 72, 10, 22, 4), "w"), (rr(72, 72, 10, 22, 4), "w")])
