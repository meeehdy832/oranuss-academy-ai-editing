# Developed by Mehdi ORANUSS | Powered by Claude
"""Oranuss motion language for ASS graphics (from the motion-dynamics skill).

ASS `\\t(t1,t2,accel,...)` maps progress p -> p**accel, so accel < 1 is an ease-out and accel > 1 an ease-in.
`\\move` is always linear, so eased travel is built from piecewise-linear \\move keys sampled on a curve.

Tokens
  ENTER   420 ms, out-cubic travel 24-60 px, opacity done by ~30% of the move (opacity leads, position settles)
  POP     scale 0 -> 104 (ease-out) -> 100 (ease-in-out): one 4% overshoot, no wobble
  SPRING  scale 0 -> 112 -> 96 -> 100: light underdamped spring, decorative icons only
  PRESS   100 -> 93 -> 100 in 180 ms: button click
  EXIT    220 ms ease-in fade + shrink to 92%
  STAGGER 70-90 ms in reading order, or locked to the spoken word when one exists
  Bounded values (bars, progress, chart lines) never overshoot: linear or ease-out only.
"""

OUT = 0.4      # ~out-cubic
IN = 2.2       # ~in-cubic
INOUT = 1.0    # used for the settle half of a two-part move

def out_cubic(p):
    return 1 - (1 - p) ** 3

def in_out_cubic(p):
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2

# key times for piecewise travel: dense at the start where an ease-out moves fastest
KEYS = (0.0, 0.18, 0.36, 0.56, 0.78, 1.0)

def eased_moves(st, x0, y0, x1, y1, dur=0.42, curve=out_cubic, keys=KEYS):
    """[(t_start, t_end, '\\move(...)')] approximating an eased travel from (x0,y0) to (x1,y1)."""
    segs = []
    for a, b in zip(keys, keys[1:]):
        pa, pb = curve(a), curve(b)
        xa, ya = x0 + (x1 - x0) * pa, y0 + (y1 - y0) * pa
        xb, yb = x0 + (x1 - x0) * pb, y0 + (y1 - y0) * pb
        segs.append((st + a * dur, st + b * dur, f"\\move({xa:.1f},{ya:.1f},{xb:.1f},{yb:.1f})"))
    return segs

def pop(s=100, t0=0, over=1.04):
    """Overshoot-and-settle scale-in starting t0 ms after the event start."""
    o = s * over
    return (f"\\fscx0\\fscy0\\t({t0},{t0 + 220},{OUT},\\fscx{o:.0f}\\fscy{o:.0f})"
            f"\\t({t0 + 220},{t0 + 360},{INOUT},\\fscx{s}\\fscy{s})")

def spring(s=100, t0=0):
    return (f"\\fscx0\\fscy0\\t({t0},{t0 + 200},{OUT},\\fscx{s * 1.12:.0f}\\fscy{s * 1.12:.0f})"
            f"\\t({t0 + 200},{t0 + 330},\\fscx{s * 0.96:.0f}\\fscy{s * 0.96:.0f})"
            f"\\t({t0 + 330},{t0 + 440},\\fscx{s}\\fscy{s})")

def press(t_ms, s=100):
    return (f"\\t({t_ms},{t_ms + 80},{OUT},\\fscx{s * 0.93:.0f}\\fscy{s * 0.93:.0f})"
            f"\\t({t_ms + 80},{t_ms + 180},{OUT},\\fscx{s}\\fscy{s})")

def exit_(dur_ms, s=100, t=220):
    """Ease-in shrink at the end of an event of length dur_ms (pair with \\fad(..,t))."""
    return f"\\t({dur_ms - t},{dur_ms},{IN},\\fscx{s * 0.92:.0f}\\fscy{s * 0.92:.0f})"

def wipe_lr(x0, y0, x1, y1, t0, t1, accel=1.0):
    """Linear (or eased) left-to-right clip reveal: for chart lines and progress, never overshoots."""
    return f"\\clip({x0},{y0},{x0},{y1})\\t({t0},{t1},{accel},\\clip({x0},{y0},{x1},{y1}))"
