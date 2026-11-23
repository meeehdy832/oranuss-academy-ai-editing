# Developed by Mehdi ORANUSS | Powered by Claude
"""Oranuss brand base shared by every style: colours, ASS shapes, icon set, the event list and helpers
that look the same in every style (icon, sparkle, cursor, camera zoom). Style modules build on this."""
import json, os
from motion import eased_moves, in_out_cubic, press, OUT, IN

# ---------- brand colours (ASS &HBBGGRR&) ----------
PURPLE = "&H00E02B5B&"   # #5B2BE0 wall purple
NEON = "&H00F65C8B&"     # #8B5CF6 glow purple
LAV = "&H00FFC4E0&"      # #E0C4FF lavender border/text
NAVY = "&H002E0F14&"     # #140F2E glass fill
INK = "&H00200810&"      # #100820 end-card bg
WHITE = "&H00FFFFFF&"

# ---------- events: every style appends here; the build script writes them out ----------
ev = []
def at(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
def E(layer, st, en, style, text):
    if en - st > 0.005:
        ev.append(f"Dialogue: {layer},{at(st)},{at(en)},{style},,0,0,0,,{text}")
def ms(x):
    return int(round(x * 1000))

# ---------- shapes ----------
def rrect(w, h, r):
    return (f"m {r} 0 l {w - r} 0 b {w} 0 {w} 0 {w} {r} l {w} {h - r} b {w} {h} {w} {h} {w - r} {h} "
            f"l {r} {h} b 0 {h} 0 {h} 0 {h - r} l 0 {r} b 0 0 0 0 {r} 0")

def circle(d):
    r = d / 2; k = r * 0.5523
    return (f"m {r} 0 b {r + k} 0 {d} {r - k} {d} {r} b {d} {r + k} {r + k} {d} {r} {d} "
            f"b {r - k} {d} 0 {r + k} 0 {r} b 0 {r - k} {r - k} 0 {r} 0")

def rr(x, y, w, h, r):
    return (f"m {x + r} {y} l {x + w - r} {y} b {x + w} {y} {x + w} {y} {x + w} {y + r} l {x + w} {y + h - r} "
            f"b {x + w} {y + h} {x + w} {y + h} {x + w - r} {y + h} l {x + r} {y + h} b {x} {y + h} {x} {y + h} {x} {y + h - r} "
            f"l {x} {y + r} b {x} {y} {x} {y} {x + r} {y}")

def co(x, y, d):
    r = d / 2; k = r * 0.5523; cx = x + r; cy = y + r
    return (f"m {cx} {y} b {cx + k} {y} {x + d} {cy - k} {x + d} {cy} b {x + d} {cy + k} {cx + k} {y + d} {cx} {y + d} "
            f"b {cx - k} {y + d} {x} {cy + k} {x} {cy} b {x} {cy - k} {cx - k} {y} {cx} {y}")

# every icon lives in a 100x100 box; ANCHOR pins the bbox so \an5 centres all parts identically
ANCHOR = " m 0 0 l 0.2 0 l 0 0.2 m 100 100 l 99.8 100 l 100 99.8"
ICONS = {
    "play": [(rr(8, 20, 84, 60, 12), "w"), ("m 42 36 l 66 50 l 42 64", "n")],
    "heart": [("m 50 84 b 18 62 8 46 16 30 b 24 14 44 14 50 30 b 56 14 76 14 84 30 b 92 46 82 62 50 84", "w")],
    "chat": [(rr(8, 16, 84, 56, 16), "w"), ("m 24 68 l 20 90 l 46 70", "w"),
             (co(26, 38, 12), "n"), (co(44, 38, 12), "n"), (co(62, 38, 12), "n")],
    "bulb": [(co(24, 6, 52), "w"), ("m 36 50 l 64 50 l 62 76 l 38 76", "w"), (rr(38, 80, 24, 9, 4), "w"),
             ("m 46 30 l 54 30 l 52 60 l 48 60", "n")],
    "people": [(co(37, 12, 26), "w"), ("m 22 86 b 22 50 78 50 78 86", "w"),
               (co(10, 26, 19), "w"), ("m 0 80 b 0 56 30 54 34 64 l 18 80", "w"),
               (co(71, 26, 19), "w"), ("m 100 80 b 100 56 70 54 66 64 l 82 80", "w")],
    "camera": [(rr(6, 28, 88, 58, 12), "w"), (rr(30, 16, 28, 16, 5), "w"), (co(30, 36, 40), "n"), (co(40, 46, 20), "w")],
    "pin": [("m 50 94 b 28 64 20 52 20 38 b 20 20 34 8 50 8 b 66 8 80 20 80 38 b 80 52 72 64 50 94", "w"), (co(37, 25, 26), "n")],
    "eye": [("m 4 50 b 28 16 72 16 96 50 b 72 84 28 84 4 50", "w"), (co(32, 32, 36), "n"), (co(41, 41, 18), "w")],
    "calendar": [(rr(10, 18, 80, 72, 12), "w"), ("m 10 38 l 90 38 l 90 43 l 10 43", "n"),
                 (rr(27, 8, 9, 20, 4), "w"), (rr(64, 8, 9, 20, 4), "w")] +
                [(rr(22 + 20 * c, 52 + 16 * r_, 12, 10, 2), "n") for r_ in range(2) for c in range(3)],
    "book": [("m 50 28 b 36 18 18 18 6 24 l 6 84 b 18 78 36 78 50 88", "w"),
             ("m 50 28 b 64 18 82 18 94 24 l 94 84 b 82 78 64 78 50 88", "w"), ("m 48 30 l 52 30 l 52 86 l 48 86", "n")],
    "cap": [("m 50 16 l 98 38 l 50 60 l 2 38", "w"), ("m 22 48 l 50 62 l 78 48 l 78 70 b 64 84 36 84 22 70", "w"),
            ("m 86 42 l 90 42 l 90 70 l 86 70", "w")],
    "key": [(co(4, 28, 44), "w"), (co(16, 40, 20), "n"), ("m 44 44 l 96 44 l 96 56 l 44 56", "w"),
            ("m 72 56 l 80 56 l 80 70 l 72 70", "w"), ("m 86 56 l 94 56 l 94 66 l 86 66", "w")],
    "info": [(co(8, 8, 84), "w"), ("m 44 42 l 56 42 l 56 76 l 44 76", "n"), (co(43, 22, 14), "n")],
    "folder": [("m 6 24 b 6 16 10 12 18 12 l 38 12 l 46 22 l 84 22 b 90 22 94 26 94 32 l 94 84 l 6 84", "w"),
               ("m 6 38 l 94 38 l 94 42 l 6 42", "n")],
    "briefcase": [(rr(6, 30, 88, 56, 10), "w"), ("m 34 30 l 34 20 b 34 16 36 14 40 14 l 60 14 b 64 14 66 16 66 20 l 66 30 l 60 30 l 60 20 l 40 20 l 40 30", "w"),
                  ("m 6 54 l 94 54 l 94 59 l 6 59", "n")],
    "check": [("m 14 52 l 26 40 l 42 56 l 76 22 l 88 34 l 42 80", "w")],
    "cart": [("m 4 10 l 22 10 l 36 64 l 29 64 l 17 17 l 4 17", "w"), ("m 22 24 l 96 24 l 85 62 l 33 62", "w"),
             ("m 45 32 l 50 32 l 50 54 l 45 54", "n"), ("m 66 32 l 71 32 l 69 54 l 64 54", "n"),
             (co(26, 70, 18), "w"), (co(70, 70, 18), "w")],
    "coins": [(co(8, 8, 84), "w"), (co(20, 20, 60), "n"), (rr(45, 28, 10, 44, 4), "w"), (rr(36, 36, 28, 8, 3), "w"), (rr(36, 56, 28, 8, 3), "w")],
    "megaphone": [("m 8 38 l 30 38 l 80 12 l 80 88 l 30 62 l 8 62", "w"), (rr(28, 60, 14, 28, 5), "w"),
                  (rr(86, 30, 8, 12, 3), "w"), (rr(86, 58, 8, 12, 3), "w"), (rr(88, 45, 10, 10, 3), "w")],
    "clock": [(co(6, 6, 88), "w"), (co(16, 16, 68), "n"), (rr(46, 24, 8, 30, 3), "w"), (rr(46, 46, 26, 8, 3), "w")],
    "pulse": [("m 2 52 l 26 52 l 36 28 l 52 78 l 62 44 l 70 52 l 98 52 l 98 60 l 66 60 l 63 56 l 51 92 l 36 46 l 31 60 l 2 60", "w")],
    "scale": [(rr(30, 86, 40, 8, 3), "w"), (rr(46, 14, 8, 74, 3), "w"), (rr(10, 22, 80, 7, 3), "w"),
              ("m 2 58 l 34 58 b 32 74 4 74 2 58", "w"), ("m 66 58 l 98 58 b 96 74 68 74 66 58", "w"),
              ("m 16 28 l 20 28 l 20 58 l 16 58", "w"), ("m 80 28 l 84 28 l 84 58 l 80 58", "w")],
    "calc": [(rr(16, 4, 68, 92, 12), "w"), (rr(26, 14, 48, 20, 4), "n")] +
            [(rr(26 + 18 * c, 44 + 16 * r_, 12, 10, 2), "n") for r_ in range(3) for c in range(3)],
    "up": [("m 50 6 l 92 50 l 66 50 l 66 94 l 34 94 l 34 50 l 8 50", "w")],
    "down": [("m 50 94 l 92 50 l 66 50 l 66 6 l 34 6 l 34 50 l 8 50", "w")],
    "cross": [("m 18 8 l 50 40 l 82 8 l 92 18 l 60 50 l 92 82 l 82 92 l 50 60 l 18 92 l 8 82 l 40 50 l 8 18", "w")],
}
STAR = "m 50 0 b 54 40 60 46 100 50 b 60 54 54 60 50 100 b 46 60 40 54 0 50 b 40 46 46 40 50 0"

# ---------- helpers shared by all styles ----------
def icon(layer, st, en, cx, cy, name, scale, tags="", fill=NAVY):
    for path, role in ICONS[name]:
        col = WHITE if role == "w" else fill
        E(layer, st, en, "Shape", f"{{\\an5\\pos({cx},{cy}){tags}\\fscx{scale}\\fscy{scale}\\c{col}\\p1}}{path}{ANCHOR}{{\\p0}}")

def sparkle(t, cx, cy, k=1.0):
    pts = [(-200, -70, 40, LAV), (190, -110, 30, WHITE), (230, 50, 22, NEON), (-170, 90, 26, WHITE), (30, -150, 20, NEON)]
    for i, (dx, dy, s, c) in enumerate(pts):
        st = t + i * 0.07; sc = int(s * k)
        E(70, st, st + 0.9, "Shape", f"{{\\an5\\pos({cx + dx * k:.0f},{cy + dy * k:.0f})\\c{c}\\blur1"
                                     f"\\fscx0\\fscy0\\t(0,260,{OUT},\\fscx{sc}\\fscy{sc}\\frz45)\\t(560,900,{IN},\\fscx0\\fscy0\\frz90)\\p1}}{STAR}{{\\p0}}")

def cursor(st, en, x0, y0, x1, y1, click_t):
    """Arrow cursor: in-out eased travel, a press dip on click, then a ripple."""
    arrow = "m 0 0 l 0 62 l 15 48 l 26 74 l 38 69 l 27 44 l 46 44"
    for k, (a, b, mv) in enumerate(eased_moves(st, x0, y0, x1, y1, 0.5, in_out_cubic)):
        fd = "\\fad(120,0)" if k == 0 else ""
        E(80, a, b, "Shape", f"{{\\an7{mv}{fd}\\c{WHITE}\\bord3\\3c{INK}\\p1}}{arrow}{{\\p0}}")
    E(80, st + 0.5, en, "Shape", f"{{\\an7\\pos({x1},{y1})\\fad(0,200)\\c{WHITE}\\bord3\\3c{INK}{press(ms(click_t - st - 0.5))}\\p1}}{arrow}{{\\p0}}")
    E(79, click_t, click_t + 0.5, "Shape", f"{{\\an5\\pos({x1 + 4},{y1 + 4})\\c{LAV}\\1a&HFF&\\bord4\\3c{LAV}"
                                         f"\\fscx20\\fscy20\\t(0,500,{OUT},\\fscx100\\fscy100\\3a&HFF&)\\p1}}{co(0, 0, 140)}{{\\p0}}")

def zexpr(zk):
    """Camera zoom keys [(t, zoom)] -> ffmpeg expression; holds ease in-out (smoothstep), punches are keys 1 ms apart."""
    e = f"{zk[-1][1]}"
    for (t0, z0), (t1, z1) in reversed(list(zip(zk, zk[1:]))):
        p = f"((t-{t0})/{t1 - t0:.3f})"
        e = f"if(lt(t,{t1}),{z0}+({z1 - z0:.3f})*(3*{p}*{p}-2*{p}*{p}*{p}),{e})"
    return e

def write_ass(path, header):
    open(path, "w", encoding="utf8").write(header + "\n".join(ev) + "\n")

# ---------- sound effects: earshot kit, placed by each take's measured sync point ----------
PEAK_ROLES = ("whoosh", "swell", "riser")
def place_sfx(cues, kit_dir):
    """cues [(time, role, take, gain_db)] -> [(start_s, wav_path, gain_db)]: whooshes/risers line up their peak, the rest their onset."""
    lock = json.load(open(os.path.join(kit_dir, "kit.lock.json")))
    out = []
    for cue, role, i, g in cues:
        r = lock["roles"][role]; t = r["takes"][i % len(r["takes"])]
        anchor = t["peak_s"] if role.startswith(PEAK_ROLES) else t["onset_s"]
        out.append((max(0, cue + (r.get("offset_ms") or 0) / 1000 - anchor), os.path.join(kit_dir, t["file"]), g))
    return out
