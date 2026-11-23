# Developed by Mehdi ORANUSS | Powered by Claude
"""premium-serif style (reference/styles/short/premium-serif/STYLE.md): phrase captions with one heavy word and one
italic-serif lavender word, depth-blur plate under graphics, floating tilted glass cards, diamond badges, pills,
darker moody grade. Used by build_1025_v2.py."""
import os
from motion import eased_moves, pop, spring, exit_, OUT
from styles.base import (PURPLE, NEON, LAV, NAVY, INK, WHITE, E, ms, rrect, icon, zexpr)

# ---------- captions: phrase chunks, sans + one heavy word + one italic-serif accent ----------
# kinds: n regular sans, b heavy sans, s italic serif (lavender), L big lavender number
FONTS = {"n": "\\fnAvenir Next Demi Bold\\fs62\\c&HFFFFFF&\\i0",
         "b": "\\fnAvenir Next Heavy\\fs80\\c&HFFFFFF&\\i0",
         "s": "\\fnDidot\\fs84\\c" + LAV + "\\i1",
         "L": "\\fnAvenir Next Heavy\\fs120\\c" + LAV + "\\i0"}
N = "\\N"
CAP_Y = 1630   # below the chin, safe during punch-ins
LEAD = 0.0     # seconds each word appears before its timestamp (editing-craft: ~2 frames = 0.067)

def line_text(tokens, ev_start, halo):
    out = []
    for tk in tokens:
        if tk == N:
            out.append(N); continue
        t, kind, txt = tk
        f = FONTS[kind]
        if halo:
            base, on, full, b0, b1 = f"{f}\\1a&HFF&\\bord7\\3c{INK}\\blur10", "\\3a&HFF&", "\\3a&H70&", "", ""
        else:
            base, on, full, b0, b1 = f, "\\alpha&HFF&", "\\alpha&H00&", "\\blur6", "\\blur0"
        d = ms(t - LEAD - ev_start)
        if d <= 0:
            out.append(f"{{{base}{full}{b1}}}{txt} ")
        else:  # word arrives as it is spoken: fade + blur-in, 160 ms ease-out
            out.append(f"{{{base}{on}{b0}\\t({d},{d + 160},{OUT},{full}{b1})}}{txt} ")
    return "".join(out).replace(" " + N, N)

def captions(chunks):
    """chunks [(start, end, [(word_time, kind, text) | N])] -> caption events; returns srt rows."""
    srt = []
    for st, en, toks in chunks:
        for a, b, mv in eased_moves(st, 540, CAP_Y + 18, 540, CAP_Y, 0.28):
            E(60, a, b, "Cap", f"{{\\an5{mv}}}" + line_text(toks, a, True))
            E(61, a, b, "Cap", f"{{\\an5{mv}}}" + line_text(toks, a, False))
        hs = st + 0.28
        E(60, hs, en, "Cap", f"{{\\an5\\pos(540,{CAP_Y})\\fad(0,120)}}" + line_text(toks, hs, True))
        E(61, hs, en, "Cap", f"{{\\an5\\pos(540,{CAP_Y})\\fad(0,120)}}" + line_text(toks, hs, False))
        srt.append((st, en, " ".join(t[2] for t in toks if t != N)))
    return srt

def srt_t(t):
    return f"00:{int(t // 60):02d}:{int(t % 60):02d},{int(round((t % 1) * 1000)) % 1000:03d}"
def write_srt(path, srt):
    with open(path, "w", encoding="utf8") as f:
        for n, (a, b, t) in enumerate(srt, 1):
            f.write(f"{n}\n{srt_t(a)} --> {srt_t(b)}\n{t}\n\n")

# ---------- graphics ----------
def glass(layer, st, en, cx, cy, w, h, r=30, tilt=0, t_in=0.42, dy=60, drift=12):
    """Floating glass card: rises dy px with an out-cubic, then drifts up slowly and shrinks out."""
    parts = [(layer, f"\\c{NEON}\\1a&H78&\\blur26", rrect(w + 18, h + 18, r + 9), 0),
             (layer + 1, f"\\c{NAVY}\\1a&H40&", rrect(w, h, r), 0),
             (layer + 2, f"\\c{WHITE}\\1a&HEE&", rrect(w - 10, h // 2 - 6, r - 6), -h // 4),
             (layer + 3, f"\\1a&HFF&\\bord2\\3c{LAV}\\3a&H30&", rrect(w, h, r), 0)]
    for ly, tg, shp, oy in parts:
        for k, (a, b, mv) in enumerate(eased_moves(st, cx, cy + oy + dy, cx, cy + oy, t_in)):
            fd = f"\\fad({ms(b - a)},0)" if k == 0 else ""
            E(ly, a, b, "Shape", f"{{\\an5{mv}{fd}\\frz{tilt}{tg}\\p1}}{shp}{{\\p0}}")
        d = ms(en - st - t_in)
        E(ly, st + t_in, en, "Shape", f"{{\\an5\\move({cx},{cy + oy},{cx},{cy + oy - drift})\\fad(0,200)\\frz{tilt}{tg}{exit_(d)}\\p1}}{shp}{{\\p0}}")

def diamond(layer, st, en, cx, cy, size, inner, kind="num"):
    """Diamond badge: rounded square at 45 deg, purple fill, light inner stroke, soft glow; pops in."""
    d = ms(en - st)
    E(layer, st, en, "Shape", f"{{\\an5\\pos({cx},{cy})\\frz45\\fad(100,200){pop()}{exit_(d)}\\c{NEON}\\1a&H60&\\blur22\\p1}}{rrect(size + 26, size + 26, size // 4)}{{\\p0}}")
    E(layer + 1, st, en, "Shape", f"{{\\an5\\pos({cx},{cy})\\frz45\\fad(100,200){pop()}{exit_(d)}\\c{PURPLE}\\bord3\\3c{LAV}\\3a&H40&\\p1}}{rrect(size, size, size // 5)}{{\\p0}}")
    E(layer + 2, st, en, "Shape", f"{{\\an5\\pos({cx},{cy - size // 6})\\frz45\\fad(100,200){pop()}{exit_(d)}\\c{WHITE}\\1a&HE4&\\p1}}{rrect(size - 14, size // 2, size // 6)}{{\\p0}}")
    if kind == "num":
        E(layer + 3, st, en, "Heavy", f"{{\\an5\\pos({cx},{cy})\\fs{int(size * 0.62)}\\fad(100,200){pop(100, 60)}{exit_(d)}}}{inner}")
    else:
        s = int(size * 0.5)
        icon(layer + 3, st, en, cx, cy, inner, s, f"\\fad(100,200){spring(s, 60)}{exit_(d, s)}", fill=PURPLE)

def slide_text(layer, st, en, style, x, y, tags, text, dx=30, dy=0, dur=0.38):
    segs = eased_moves(st, x + dx, y + dy, x, y, dur)
    for k, (a, b, mv) in enumerate(segs):
        fd = f"\\fad({ms(b - a)},0)" if k == 0 else ""
        E(layer, a, b, style, f"{{{mv}{fd}{tags}}}{text}")
    E(layer, st + dur, en, style, f"{{\\pos({x},{y})\\fad(0,180){tags}}}{text}")

def pill(st, en, cx, cy, text, w=None, h=96, ic=None):
    w = w or len(text) * 25 + (150 if ic else 90)
    E(50, st, en, "Shape", f"{{\\an5\\pos({cx},{cy})\\fad(120,200){pop()}{exit_(ms(en - st))}\\c{NEON}\\1a&H68&\\blur20\\p1}}{rrect(w + 20, h + 12, (h + 12) // 2)}{{\\p0}}")
    E(51, st, en, "Shape", f"{{\\an5\\pos({cx},{cy})\\fad(120,200){pop()}{exit_(ms(en - st))}\\c{NAVY}\\1a&H30&\\bord2\\3c{LAV}\\3a&H30&\\p1}}{rrect(w, h, h // 2)}{{\\p0}}")
    tx = cx + (28 if ic else 0)
    E(52, st + 0.03, en, "Label", f"{{\\an5\\pos({tx},{cy + 2})\\fs36\\fsp4\\fad(120,200){pop(100, 30)}{exit_(ms(en - st - 0.03))}}}{text}")
    if ic:
        icon(52, st, en, cx - w // 2 + 56, cy, ic, 44, f"\\fad(120,200){spring(44, 60)}", fill=PURPLE)

# ---------- ASS header ----------
HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Avenir Next Demi Bold,62,&H00FFFFFF,&H00FFFFFF,&H00200810,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,40,40,0,1
Style: Shape,Arial,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Heavy,Avenir Next Heavy,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Light,Avenir Next Demi Bold,30,&H00FFC4E0,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Label,Avenir Next Demi Bold,38,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,0,0,5,0,0,0,1
Style: Serif,Didot,64,&H00FFC4E0,&H00FFFFFF,&H00000000,&H00000000,0,-1,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# ---------- filter graph: moody grade, camera zoom, depth blur under graphics, voice chain + SFX, -14 LUFS ----------
def filter_graph(ass_file, total, speech_end, zk, blur_win, sfx):
    ass_path = ass_file.replace(":", "\\:")
    fc = [f"[0:v]eq=contrast=1.12:gamma=0.92:saturation=1.03,colorbalance=rs=0.03:bs=0.10:rm=0.01:bm=0.05,"
          f"tpad=stop_mode=clone:stop_duration={total - speech_end + 0.2:.2f},trim=0:{total},setpts=PTS-STARTPTS,"
          f"scale=w='2*trunc(540*{zexpr(zk)})':h='2*trunc(960*{zexpr(zk)})':eval=frame:flags=bicubic,"
          f"crop=1080:1920:(iw-1080)/2:(ih-1920)*0.62,split={1 + len(blur_win)}[vs]" + "".join(f"[b{i}]" for i in range(len(blur_win)))]
    last = "vs"
    for i, (s, e) in enumerate(blur_win):
        fc.append(f"[b{i}]trim={s}:{e},setpts=PTS-STARTPTS,scale=1124:-2,crop=1080:1920,gblur=sigma=26,"
                  f"eq=brightness=-0.13:saturation=0.8,format=yuva420p,fade=t=in:d=0.24:alpha=1,"
                  f"fade=t=out:st={e - s - 0.24:.2f}:d=0.24:alpha=1,setpts=PTS+{s}/TB[bl{i}]")
        fc.append(f"[{last}][bl{i}]overlay=eof_action=pass:format=auto[o{i}]"); last = f"o{i}"
    fc.append(f"[{last}]vignette=angle=PI/3.8:mode=forward,ass='{ass_path}',format=yuv420p[vout]")
    fc.append(f"[0:a]highpass=f=80,afftdn=nf=-25:tn=1,equalizer=f=3000:t=q:w=1.2:g=2,"
              f"acompressor=threshold=-20dB:ratio=3:attack=10:release=150:makeup=2,aresample=48000,apad=whole_dur={total}[voice]")
    for i, (st, _, g) in enumerate(sfx):
        fc.append(f"[{i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,adelay={ms(st)}|{ms(st)}[s{i}]")
    fc.append("[voice]" + "".join(f"[s{i}]" for i in range(len(sfx))) +
              f"amix=inputs={len(sfx) + 1}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,atrim=0:{total}[aout]")
    return fc
