# Developed by Mehdi ORANUSS | Powered by Claude
"""purple-glass style (reference/styles/short/purple-glass/STYLE.md): navy + neon purple glass cards, 2-4 word captions with
the active word in a purple box and keywords in lavender, icon bubbles and chips, split layout (face top + ink panel),
lavender flash on layout switches. Used by build_1025.py."""
from motion import eased_moves, pop, spring, exit_, wipe_lr, OUT
from styles.base import (PURPLE, NEON, LAV, NAVY, INK, WHITE, E, ms, rrect, rr, co, icon, zexpr)

# ---------- motion helpers ----------
def enter(layer, st, en, style, x, y, tags, text, dx=0, dy=40, dur=0.42, fade_out=220, shrink=True):
    """Premium enter: eased travel (piecewise \\move), opacity leads, then hold and ease-in exit."""
    segs = eased_moves(st, x + dx, y + dy, x, y, dur)
    for k, (a, b, mv) in enumerate(segs):
        if b > en:
            break
        fad = f"\\fad({ms(b - a)},0)" if k == 0 else ""
        E(layer, a, b, style, f"{{{mv}{fad}{tags}}}{text}")
    hs = st + dur
    if hs < en:
        d = ms(en - hs)
        ex = exit_(d) if shrink else ""
        E(layer, hs, en, style, f"{{\\pos({x},{y})\\fad(0,{min(fade_out, d)}){tags}{ex}}}{text}")

def glass(layer, st, en, cx, cy, w, h, r=30, anim=None, fade=(200, 220)):
    """Glass card: neon bloom + navy fill + top sheen + lavender rim. Default motion: rise 30 px, out-cubic."""
    parts = [
        (layer, f"\\c{NEON}\\1a&H74&\\blur24", rrect(w + 18, h + 18, r + 9), 0),
        (layer + 1, f"\\c{NAVY}\\1a&H30&", rrect(w, h, r), 0),
        (layer + 2, f"\\c{WHITE}\\1a&HEE&", rrect(w - 10, h // 2 - 6, r - 6), -h // 4),
        (layer + 3, f"\\1a&HFF&\\bord2\\3c{LAV}\\3a&H28&", rrect(w, h, r), 0),
    ]
    for ly, tg, shp, oy in parts:
        if anim == "pop":
            d = ms(en - st)
            E(ly, st, en, "Shape", f"{{\\an5\\pos({cx},{cy + oy})\\fad({fade[0]},{fade[1]}){pop()}{exit_(d)}{tg}\\p1}}{shp}{{\\p0}}")
        else:
            enter(ly, st, en, "Shape", cx, cy + oy, f"\\an5{tg}\\p1", f"{shp}{{\\p0}}", dy=30)

def bubble(layer, st, en, cx, cy, name, d=110, t0=0):
    """Neon circle + icon, light spring (decorative only)."""
    dur = ms(en - st)
    sp = spring(100, t0)
    E(layer, st, en, "Shape", f"{{\\an5\\pos({cx},{cy})\\fad(120,200){sp}{exit_(dur)}\\c{NEON}\\1a&H60&\\blur18\\p1}}{co(0, 0, d + 22)}{{\\p0}}")
    E(layer + 1, st, en, "Shape", f"{{\\an5\\pos({cx},{cy})\\fad(120,200){sp}{exit_(dur)}\\c{PURPLE}\\bord2\\3c{LAV}\\3a&H30&\\p1}}{co(0, 0, d)}{{\\p0}}")
    s = int(d * 0.52)
    icon(layer + 2, st, en, cx, cy, name, s, f"\\fad(120,200){spring(s, t0 + 60)}{exit_(dur, s)}", fill=PURPLE)

def hl_box(layer, st, en, cx, cy, w, h, color=PURPLE):
    """Highlight bar that wipes in left->right with an ease-out (no overshoot)."""
    x0, x1 = cx - w // 2, cx + w // 2
    E(layer, st, en, "Shape", f"{{\\an7\\pos(0,0)\\fad(0,200)\\c{color}{wipe_lr(x0 - 2, cy - h // 2 - 2, x1 + 2, cy + h // 2 + 2, 0, 300, OUT)}\\p1}}"
                              f"{rr(x0, cy - h // 2, w, h, 14)}{{\\p0}}")

def chip(st, en, cx, cy, name, label, w=None):
    w = w or len(label) * 27 + 170
    glass(40, st, en, cx, cy, w, 112, r=56)
    bubble(45, st, en, cx - w // 2 + 58, cy, name, d=80, t0=120)
    enter(48, st + 0.08, en, "Label", cx - w // 2 + 112, cy, "\\an4\\fs40", label, dx=-24, dy=0)

def flash(t):
    E(90, t - 0.02, t + 0.14, "Shape", f"{{\\an7\\pos(0,0)\\c{LAV}\\1a&HB0&\\t(0,160,\\1a&HFF&)\\p1}}m 0 0 l 1080 0 l 1080 1920 l 0 1920{{\\p0}}")

# ---------- captions: 2-4 word chunks, active word in a purple box, keywords lavender ----------
def chunk_words(words, switch):
    """[(start, end, word)] -> chunks of up to 4 words / 18 chars, split at punctuation and never across a layout switch."""
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        txt = " ".join(x[2] for x in cur)
        if len(cur) >= 4 or len(txt) > 18 or w[2][-1] in ".,?":
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    fixed = []
    for ch in chunks:
        part = [ch[0]]
        for w in ch[1:]:
            if any(part[-1][0] < s <= w[0] for s in switch):
                fixed.append(part); part = []
            part.append(w)
        fixed.append(part)
    return fixed

def captions(chunks, keywords, cap_y):
    """Box captions; cap_y(t) gives the distance from the bottom edge. Returns srt rows."""
    srt = []
    for ch in chunks:
        c0, c1 = ch[0][0], ch[-1][1]
        mv = cap_y(c0)
        plain = " ".join(w for _, _, w in ch)
        E(60, c0, c1, "CapHalo", f"{{\\an2\\pos(540,{1920 - mv})\\fscx88\\fscy88\\t(0,110,{OUT},\\fscx100\\fscy100)}}{plain}")
        for i, (a, b, _) in enumerate(ch):
            end = ch[i + 1][0] if i + 1 < len(ch) else c1
            parts = []
            for j, (_, _, w) in enumerate(ch):
                col = f"\\c{LAV}" if w.lower() in keywords and j != i else "\\c&HFFFFFF&"
                box = "\\3a&H00&" if j == i else "\\3a&HFF&"
                parts.append(f"{{{box}{col}}}{w}")
            anim = f"\\fscx88\\fscy88\\t(0,110,{OUT},\\fscx100\\fscy100)" if i == 0 else ""
            E(61, a, end, "Cap", f"{{\\an2\\pos(540,{1920 - mv}){anim}}}" + " ".join(parts))
        srt.append((c0, c1, plain))
    return srt

def srt_t(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
def write_srt(path, srt):
    with open(path, "w", encoding="utf8") as f:
        for n, (a, b, t) in enumerate(srt, 1):
            f.write(f"{n}\n{srt_t(a)} --> {srt_t(b)}\n{t}\n\n")

# ---------- ASS header ----------
HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Avenir Next Demi Bold,68,&H00FFFFFF,&H00FFFFFF,&H00E02B5B,&H00000000,0,0,0,0,100,100,0,0,3,10,0,2,60,60,80,1
Style: CapHalo,Avenir Next Demi Bold,68,&HFF000000,&HFF000000,&H00200810,&HFF000000,0,0,0,0,100,100,0,0,1,8,0,2,60,60,80,1
Style: Shape,Arial,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Heavy,Avenir Next Heavy,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Light,Avenir Next Demi Bold,30,&H00FFC4E0,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Label,Avenir Next Demi Bold,38,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,0,0,4,0,0,0,1
Style: Serif,Didot,80,&H00FFC4E0,&H00FFFFFF,&H00000000,&H00000000,0,-1,0,0,100,100,0,0,1,0,0,4,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# ---------- filter graph: light grade, camera zoom, split layout B (face top over ink), voice chain, -14 LUFS ----------
def filter_graph(ass_file, total, speech_end, zk, b_win):
    ass_path = ass_file.replace(":", "\\:")
    z = zexpr(zk)
    return [
        f"[0:v]eq=contrast=1.07:saturation=1.05:gamma=0.97,colorbalance=rs=0.01:bs=0.05:rh=0.01:bh=0.03,"
        f"tpad=stop_mode=clone:stop_duration={total - speech_end + 0.2:.2f},trim=0:{total},setpts=PTS-STARTPTS,split[va][vb]",
        f"[va]scale=w='2*trunc(540*{z})':h='2*trunc(960*{z})':eval=frame:flags=bicubic,"
        f"crop=1080:1920:(iw-1080)/2:(ih-1920)*0.45[vA]",
        f"[vb]crop=1080:860:0:600[top]",
        f"color=c=0x100820:s=1080x1920:r=30:d={total}[ink]",
        f"[ink][top]overlay=0:0[vB]",
        f"[vA][vB]overlay=enable='" + "+".join(f"between(t,{s},{e - 0.001})" for s, e in b_win) + "'[vl]",
        f"[vl]vignette=angle=PI/4.4:mode=forward,ass='{ass_path}',format=yuv420p[vout]",
        f"[0:a]highpass=f=80,afftdn=nf=-25:tn=1,equalizer=f=3000:t=q:w=1.2:g=2,"
        f"acompressor=threshold=-20dB:ratio=3:attack=10:release=150:makeup=2,apad=whole_dur={total},"
        f"loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,atrim=0:{total}[aout]",
    ]
