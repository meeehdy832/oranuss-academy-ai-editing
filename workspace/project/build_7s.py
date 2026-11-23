# Developed by Mehdi ORANUSS | Powered by Claude
"""7 s test: first 7 s of input/recordings/1025.mp4, premium-serif style (first draft of styles/premium_serif.py),
sound effects from the earshot `launch` kit (work/sfx/kit, placed with its measured sync points).
Writes work/7s.ass, work/filter_7s.txt."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import eased_moves, out_cubic, pop, spring, exit_, OUT, IN
from styles.base import PURPLE, NEON, LAV, NAVY, INK, WHITE, rrect, co, rr, ICONS, ANCHOR

ROOT = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(ROOT, "work")
TOTAL = 7.0

ev = []
def at(t):
    t = max(0, t); return f"0:00:{t:05.2f}"
def E(layer, st, en, style, text):
    if en - st > 0.005:
        ev.append(f"Dialogue: {layer},{at(st)},{at(en)},{style},,0,0,0,,{text}")
def ms(x):
    return int(round(x * 1000))

# ---------- captions: phrase chunks, sans + italic-serif accent, words fade/blur in as spoken ----------
# token kinds: n = regular sans, b = heavy sans (bigger), s = italic serif accent (lavender), L = big lavender number
FONTS = {"n": "\\fnAvenir Next Demi Bold\\fs62\\c&HFFFFFF&\\i0",
         "b": "\\fnAvenir Next Heavy\\fs80\\c&HFFFFFF&\\i0",
         "s": "\\fnDidot\\fs84\\c" + LAV + "\\i1",
         "L": "\\fnAvenir Next Heavy\\fs120\\c" + LAV + "\\i0"}
CHUNKS = [  # (start, end, [(word_time, kind, text) | "\\N"])
    (0.0, 2.03, [(0.07, "n", "Bghiti"), (0.43, "s", "t3llem"), "\\N", (0.83, "b", "MHARAT"), (1.45, "b", "JDAD?")]),
    (2.06, 3.00, [(2.06, "n", "lli t7ell lik"), "\\N", (2.41, "s", "forass"), (2.56, "b", "KBIRA")]),
    (3.03, 3.92, [(3.03, "n", "f"), (3.06, "b", "SOUK"), (3.27, "s", "l'internet?")]),
    (3.94, 5.52, [(3.94, "n", "Wfferna lik"), "\\N", (4.50, "L", "6"), (4.74, "s", "dyal"), (5.05, "b", "MHARAT")]),
    (5.56, 6.98, [(5.56, "n", "lli tqder"), (6.00, "n", "annaha"), "\\N", (6.34, "s", "tqeddem"), (6.68, "b", "LIK")]),
]
CAP_Y = 1630

def line_text(tokens, ev_start, halo):
    out = []
    for tk in tokens:
        if tk == "\\N":
            out.append("\\N"); continue
        t, kind, txt = tk
        f = FONTS[kind]
        if halo:
            base = f"{f}\\1a&HFF&\\bord7\\3c{INK}\\blur10"
            on, full = "\\3a&HFF&", "\\3a&H70&"
        else:
            base, on, full = f, "\\alpha&HFF&", "\\alpha&H00&"
        d = ms(t - ev_start)
        if d <= 0:
            out.append(f"{{{base}{full}{'' if halo else chr(92) + 'blur0'}}}{txt} ")
        else:  # word arrives: fade + blur-in, 160 ms ease-out
            out.append(f"{{{base}{on}{'' if halo else chr(92) + 'blur6'}\\t({d},{d + 160},{OUT},{full}{'' if halo else chr(92) + 'blur0'})}}{txt} ")
    return "".join(out).replace(" \\N", "\\N")

for st, en, toks in CHUNKS:
    # whole phrase rises 18 px on an out-cubic, then fades out quickly before the next phrase
    for a, b, mv in eased_moves(st, 540, CAP_Y + 18, 540, CAP_Y, 0.28):
        E(60, a, b, "Cap", f"{{\\an5{mv}}}" + line_text(toks, a, True))
        E(61, a, b, "Cap", f"{{\\an5{mv}}}" + line_text(toks, a, False))
    hs = st + 0.28
    E(60, hs, en, "Cap", f"{{\\an5\\pos(540,{CAP_Y})\\fad(0,120)}}" + line_text(toks, hs, True))
    E(61, hs, en, "Cap", f"{{\\an5\\pos(540,{CAP_Y})\\fad(0,120)}}" + line_text(toks, hs, False))

# ---------- graphics ----------
def glass(layer, st, en, cx, cy, w, h, r=30, tilt=0, t_in=0.42, dy=60):
    parts = [(layer, f"\\c{NEON}\\1a&H78&\\blur26", rrect(w + 18, h + 18, r + 9), 0),
             (layer + 1, f"\\c{NAVY}\\1a&H40&", rrect(w, h, r), 0),
             (layer + 2, f"\\c{WHITE}\\1a&HEE&", rrect(w - 10, h // 2 - 6, r - 6), -h // 4),
             (layer + 3, f"\\1a&HFF&\\bord2\\3c{LAV}\\3a&H30&", rrect(w, h, r), 0)]
    for ly, tg, shp, oy in parts:
        for k, (a, b, mv) in enumerate(eased_moves(st, cx, cy + oy + dy, cx, cy + oy, t_in)):
            E(ly, a, b, "Shape", f"{{\\an5{mv}{'\\fad(' + str(ms(b - a)) + ',0)' if k == 0 else ''}\\frz{tilt}{tg}\\p1}}{shp}{{\\p0}}")
        d = ms(en - st - t_in)
        # slow float after landing (constant drift, linear) + ease-in exit
        E(ly, st + t_in, en, "Shape", f"{{\\an5\\move({cx},{cy + oy},{cx},{cy + oy - 12})\\fad(0,200)\\frz{tilt}{tg}{exit_(d)}\\p1}}{shp}{{\\p0}}")

def icon(layer, st, en, cx, cy, name, scale, tags="", fill=NAVY):
    for path, role in ICONS[name]:
        col = WHITE if role == "w" else fill
        E(layer, st, en, "Shape", f"{{\\an5\\pos({cx},{cy}){tags}\\fscx{scale}\\fscy{scale}\\c{col}\\p1}}{path}{ANCHOR}{{\\p0}}")

def diamond(layer, st, en, cx, cy, size, inner=None, inner_kind="num"):
    """premium-serif diamond badge: rounded square at 45 deg, purple fill, light inner stroke, soft glow."""
    d = ms(en - st)
    sq = rrect(size, size, size // 5)
    E(layer, st, en, "Shape", f"{{\\an5\\pos({cx},{cy})\\frz45\\fad(100,200){pop()}{exit_(d)}\\c{NEON}\\1a&H60&\\blur22\\p1}}{rrect(size + 26, size + 26, size // 4)}{{\\p0}}")
    E(layer + 1, st, en, "Shape", f"{{\\an5\\pos({cx},{cy})\\frz45\\fad(100,200){pop()}{exit_(d)}\\c{PURPLE}\\bord3\\3c{LAV}\\3a&H40&\\p1}}{sq}{{\\p0}}")
    E(layer + 2, st, en, "Shape", f"{{\\an5\\pos({cx},{cy - size // 6})\\frz45\\fad(100,200){pop()}{exit_(d)}\\c{WHITE}\\1a&HE4&\\p1}}{rrect(size - 14, size // 2, size // 6)}{{\\p0}}")
    if inner_kind == "num":
        E(layer + 3, st, en, "Heavy", f"{{\\an5\\pos({cx},{cy})\\fs{int(size * 0.62)}\\fad(100,200){pop(100, 60)}{exit_(d)}}}{inner}")
    else:
        s = int(size * 0.5)
        icon(layer + 3, st, en, cx, cy, inner, s, f"\\fad(100,200){spring(s, 60)}{exit_(d, s)}", fill=PURPLE)

# 2.06 - 3.94: plate blurs; floating-cards carousel + "souk l'internet" chip
CARDS = [(290, -9, "play", "VIDEO"), (540, 0, "chat", "CLIENTS"), (790, 9, "briefcase", "BUSINESS")]
for k, (x, tilt, ic, lab) in enumerate(CARDS):
    t0 = 2.10 + k * 0.13
    y = 640 + (0 if k == 1 else 30)
    glass(30 + k * 6, t0, 3.92, x, y, 220, 290, r=26, tilt=tilt)
    E(35 + k * 6, t0 + 0.12, 3.92, "Shape", f"{{\\an5\\pos({x},{y - 40})\\frz{tilt}\\fad(150,200){spring(100)}\\c{NEON}\\1a&H50&\\blur14\\p1}}{co(0, 0, 120)}{{\\p0}}")
    icon(35 + k * 6, t0 + 0.12, 3.92, x, y - 40, ic, 54, f"\\frz{tilt}\\fad(150,200){spring(54)}", fill=PURPLE)
    E(35 + k * 6, t0 + 0.18, 3.92, "Label", f"{{\\an5\\pos({x},{y + 80})\\frz{tilt}\\fs26\\fsp6\\fad(150,200)\\c{LAV}}}{lab}")
E(50, 3.03, 3.92, "Shape", f"{{\\an5\\pos(540,380)\\fad(120,200){pop()}\\c{NEON}\\1a&H68&\\blur20\\p1}}{rrect(560, 100, 50)}{{\\p0}}")
E(51, 3.03, 3.92, "Shape", f"{{\\an5\\pos(540,380)\\fad(120,200){pop()}\\c{NAVY}\\1a&H30&\\bord2\\3c{LAV}\\3a&H30&\\p1}}{rrect(540, 88, 44)}{{\\p0}}")
E(52, 3.06, 3.92, "Label", f"{{\\an5\\pos(540,382)\\fs38\\fsp4\\fad(120,200){pop(100, 30)}}}SOUK L'INTERNET")

# 4.50 - 5.52: diamond "6" + spaced label / bold title (lower-third style, placed on the wall above the head)
diamond(40, 4.50, 5.52, 330, 420, 130, "6")
for a, b, mv in eased_moves(4.62, 460, 385, 430, 385, 0.38):
    E(45, a, b, "Light", f"{{\\an4{mv}\\fs28\\fsp10}}SKILLS")
E(45, 5.00, 5.52, "Light", "{\\an4\\pos(430,385)\\fs28\\fsp10\\fad(0,180)}SKILLS")
for a, b, mv in eased_moves(5.05, 470, 448, 430, 448, 0.38):
    E(45, a, b, "Heavy", f"{{\\an4{mv}\\fs72{'\\fad(90,0)' if a == 5.05 else ''}}}Mharat")
E(45, 5.43, 5.52, "Heavy", "{\\an4\\pos(430,448)\\fs72\\fad(0,90)}Mharat")

# 5.56 - 7.0: plate blurs again; icon trio row of diamonds
E(50, 5.58, TOTAL, "Light", "{\\an5\\pos(540,400)\\fs30\\fsp14\\fad(160,0)}L'MHARAT")
TRIO = [(270, "eye", "Tsswi9", 5.66), (540, "briefcase", "Lbi3", 5.86), (810, "bulb", "AI", 6.06)]
for x, ic, lab, t0 in TRIO:
    diamond(40, t0, TOTAL + 0.3, x, 620, 150, ic, inner_kind="icon")
    E(48, t0 + 0.12, TOTAL, "Serif", f"{{\\an5\\pos({x},{800})\\fs72\\fad(140,0)}}{lab}")

# ---------- sound effects: earshot launch kit, placed by its measured sync points ----------
LOCK = json.load(open(os.path.join(W, "sfx", "kit", "kit.lock.json")))
def take(role, i=0):
    r = LOCK["roles"][role]; t = r["takes"][i % len(r["takes"])]
    return r, t
# (cue time, role, take index, gain dB). Whoosh/swell: peak lands offset_ms after the cue; others: onset does.
CUES = [
    (0.43, "tick", 0, -8), (1.45, "snap", 0, -9),                       # hook accent, snap punch-in
    (2.06, "whoosh.short", 0, -6),                                       # plate blurs, cards fly in
    (2.10, "pop", 0, -10), (2.23, "pop", 1, -11), (2.36, "pop", 2, -11),
    (3.03, "tick", 1, -9),                                               # chip
    (3.94, "land.light", 0, -8),                                         # plate back to sharp
    (4.50, "hit", 0, -7), (5.05, "tick", 2, -10),                        # diamond 6, title
    (5.56, "whoosh.short", 1, -7),
    (5.66, "pop", 0, -11), (5.86, "pop", 1, -11), (6.06, "pop", 2, -11),
]
sfx = []
for cue, role, i, g in CUES:
    r, t = take(role, i)
    anchor = t["peak_s"] if role.startswith(("whoosh", "swell")) else t["onset_s"]
    start = cue + (r.get("offset_ms") or 0) / 1000 - anchor
    sfx.append((max(0, start), os.path.join(W, "sfx", "kit", t["file"]), g))

open(os.path.join(W, "7s.ass"), "w", encoding="utf8").write("""[Script Info]
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
""" + "\n".join(ev) + "\n")

# ---------- filter graph ----------
# camera: slow push, snap punch-ins on "jdad" and "6" (premium-serif: 110-120 % on emphasis)
ZK = [(0.0, 1.0), (1.45, 1.04), (1.451, 1.13), (2.06, 1.14), (3.94, 1.06), (3.941, 1.0), (4.50, 1.02),
      (4.501, 1.11), (5.55, 1.13), (5.551, 1.05), (TOTAL, 1.08)]
def zexpr():
    e = f"{ZK[-1][1]}"
    for (t0, z0), (t1, z1) in reversed(list(zip(ZK, ZK[1:]))):
        p = f"((t-{t0})/{t1 - t0:.3f})"
        e = f"if(lt(t,{t1}),{z0}+({z1 - z0:.3f})*(3*{p}*{p}-2*{p}*{p}*{p}),{e})"
    return e
BLUR_WIN = [(2.02, 3.94), (5.52, TOTAL + 0.1)]   # depth trick: plate blurs + darkens while a graphic is up
ass_path = os.path.join(W, "7s.ass").replace(":", "\\:")
fc = [f"[0:v]trim=0:{TOTAL},setpts=PTS-STARTPTS,"
      f"eq=contrast=1.12:gamma=0.92:saturation=1.03,colorbalance=rs=0.03:bs=0.10:rm=0.01:bm=0.05,"
      f"scale=w='2*trunc(540*{zexpr()})':h='2*trunc(960*{zexpr()})':eval=frame:flags=bicubic,"
      f"crop=1080:1920:(iw-1080)/2:(ih-1920)*0.62,split={1 + len(BLUR_WIN)}[vs]" + "".join(f"[b{i}]" for i in range(len(BLUR_WIN)))]
last = "vs"
for i, (s, e) in enumerate(BLUR_WIN):
    e2 = min(e, TOTAL)
    fc.append(f"[b{i}]trim={s}:{e2},setpts=PTS-STARTPTS,scale=1124:-2,crop=1080:1920,gblur=sigma=26,"
              f"eq=brightness=-0.13:saturation=0.8,format=yuva420p,fade=t=in:d=0.24:alpha=1"
              + (f",fade=t=out:st={e2 - s - 0.24:.2f}:d=0.24:alpha=1" if e < TOTAL else "")
              + f",setpts=PTS+{s}/TB[bl{i}]")
    fc.append(f"[{last}][bl{i}]overlay=eof_action=pass:format=auto[o{i}]"); last = f"o{i}"
fc.append(f"[{last}]vignette=angle=PI/3.8:mode=forward,ass='{ass_path}',format=yuv420p[vout]")
# audio: voice chain, then the sfx bus under it, then loudness on the full mix
fc.append(f"[0:a]atrim=0:{TOTAL},asetpts=PTS-STARTPTS,highpass=f=80,afftdn=nf=-25:tn=1,equalizer=f=3000:t=q:w=1.2:g=2,"
          f"acompressor=threshold=-20dB:ratio=3:attack=10:release=150:makeup=2,afade=t=out:st={TOTAL - 0.12}:d=0.12,aresample=48000[voice]")
for i, (st, _, g) in enumerate(sfx):
    fc.append(f"[{i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,adelay={ms(st)}|{ms(st)}[s{i}]")
fc.append("[voice]" + "".join(f"[s{i}]" for i in range(len(sfx))) +
          f"amix=inputs={len(sfx) + 1}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,atrim=0:{TOTAL}[aout]")
open(os.path.join(W, "filter_7s.txt"), "w").write(";\n".join(fc))
open(os.path.join(W, "7s_inputs.txt"), "w").write("\n".join(p for _, p, _ in sfx) + "\n")
print(f"events={len(ev)} sfx={len(sfx)}")
