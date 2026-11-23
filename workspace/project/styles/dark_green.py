# Developed by Mehdi ORANUSS | Powered by Claude
"""dark-green style (reference/styles/short/dark-green/STYLE.md): the premium-serif layout (phrase captions with one heavy
word and one italic-serif accent, depth-blur plate, diamond badges, glass cards, pills) in a deep emerald / mint
palette, plus social-safe caption placement, a frosted lower panel (also hides text burned into the source) and a
top checklist tracker. Call apply_palette() once before drawing: it switches the shared helpers to green."""
import os
from motion import eased_moves, pop, exit_, OUT
import styles.base as base
import styles.premium_serif as ps
from styles.base import E, ms, rrect, zexpr

# ---------- palette (ASS &HBBGGRR&) ----------
EMERALD = "&H006E9F0E&"   # #0E9F6E solid accents, diamond fill
GLOW = "&H009DE52E&"      # #2EE59D bloom, progress, flashes
MINT = "&H00D0F3A7&"      # #A7F3D0 rims, serif accent words, labels
FOREST = "&H001F2A0A&"    # #0A2A1F glass fill
INK = "&H000F1405&"       # #05140F full-frame backgrounds, end card
WHITE = "&H00FFFFFF&"
RED = "&H007171F8&"       # #F87171 losses / "no" only

def apply_palette():
    """premium_serif and base draw with module globals; point them at the green tokens."""
    for m in (base, ps):
        m.PURPLE, m.NEON, m.LAV, m.NAVY, m.INK = EMERALD, GLOW, MINT, FOREST, INK
    ps.FONTS["s"] = "\\fnDidot\\fs84\\c" + MINT + "\\i1"
    ps.FONTS["L"] = "\\fnAvenir Next Heavy\\fs120\\c" + MINT + "\\i0"
    ps.LEAD = 0.067   # words land ~2 frames before they are said

# ---------- social safe zones (1080x1920): Reels / TikTok / Shorts UI covers the edges ----------
SAFE_TOP = 250       # status + "Reels" header
SAFE_BOTTOM = 1480   # caption, username, music line
SAFE_RIGHT = 940     # like / comment / share column (from y ~1000 down)
CAP_Y = 1290         # caption centre: below the chin, above the platform caption

def captions(chunks, cap_y=lambda t: CAP_Y):
    """premium-serif phrase captions with a per-chunk centre; returns srt rows.
    A caption's exit (its 120 ms fade) must finish before the next caption starts."""
    for (_, en, _), (nst, _, _) in zip(chunks, chunks[1:]):
        if en > nst:
            raise ValueError(f"caption ending {en} overlaps the next one starting {nst}")
    srt = []
    for st, en, toks in chunks:
        y = cap_y(st)
        for a, b, mv in eased_moves(st, 540, y + 18, 540, y, 0.28):
            E(60, a, b, "Cap", f"{{\\an5{mv}}}" + ps.line_text(toks, a, True))
            E(61, a, b, "Cap", f"{{\\an5{mv}}}" + ps.line_text(toks, a, False))
        hs = st + 0.28
        E(60, hs, en, "Cap", f"{{\\an5\\pos(540,{y})\\fad(0,120)}}" + ps.line_text(toks, hs, True))
        E(61, hs, en, "Cap", f"{{\\an5\\pos(540,{y})\\fad(0,120)}}" + ps.line_text(toks, hs, False))
        srt.append((st, en, " ".join(t[2] for t in toks if t != ps.N)))
    return srt

# ---------- frosted lower panel: tint + rim drawn over a plate band that filter_graph blurs ----------
def frost_panel(st, en, y, h, fade_in=0, fade_out=200):
    E(20, st, en, "Shape", f"{{\\an7\\pos(0,{y})\\fad({fade_in},{fade_out})\\c{FOREST}\\1a&H48&\\p1}}m 0 0 l 1080 0 l 1080 {h} l 0 {h}{{\\p0}}")
    E(21, st, en, "Shape", f"{{\\an7\\pos(0,{y - 1})\\fad({fade_in},{fade_out})\\c{GLOW}\\1a&H30&\\blur3\\p1}}m 0 0 l 1080 0 l 1080 3 l 0 3{{\\p0}}")
    E(21, st, en, "Shape", f"{{\\an7\\pos(0,{y + h - 2})\\fad({fade_in},{fade_out})\\c{MINT}\\1a&HA0&\\p1}}m 0 0 l 1080 0 l 1080 2 l 0 2{{\\p0}}")

# ---------- checklist tracker: title + N diamond ticks that fill as each item is spoken ----------
def tracker(st, en, title, ticks, y=360, x0=220, step=80, done_at=None):
    """ticks: [time each item is said]. Ticks show empty from st, fill emerald with a glow at their time."""
    E(40, st, en, "Heavy", f"{{\\an6\\pos(650,{y - 72})\\fs50\\fsp3\\fad(200,250){pop(100)}}}{title}")
    for k, t in enumerate(ticks):
        x = x0 + k * step; s0 = st + 0.30 + k * 0.05
        E(41, s0, en, "Shape", f"{{\\an5\\pos({x},{y})\\frz45\\fad(120,250){pop()}\\1a&HFF&\\bord2\\3c{MINT}\\3a&H40&\\p1}}{rrect(30, 30, 7)}{{\\p0}}")
        E(42, t, en, "Shape", f"{{\\an5\\pos({x},{y})\\frz45\\fad(60,250){pop()}\\c{GLOW}\\1a&H50&\\blur10\\p1}}{rrect(44, 44, 10)}{{\\p0}}")
        E(43, t, en, "Shape", f"{{\\an5\\pos({x},{y})\\frz45\\fad(60,250){pop()}\\c{EMERALD}\\bord2\\3c{MINT}\\p1}}{rrect(30, 30, 7)}{{\\p0}}")
        nxt = ticks[k + 1] if k + 1 < len(ticks) else en
        E(44, t, nxt, "Light", f"{{\\an4\\pos(680,{y - 72})\\fs40\\c{MINT}\\fad(80,0)}}{k + 1:02d} / {len(ticks):02d}")
    if done_at:
        for k in range(len(ticks)):
            E(45, done_at + k * 0.04, done_at + k * 0.04 + 0.5, "Shape", f"{{\\an5\\pos({x0 + k * step},{y})\\frz45\\c{MINT}\\1a&H40&\\blur6"
                                                                    f"\\t(0,500,{OUT},\\fscx220\\fscy220\\1a&HFF&)\\p1}}{rrect(30, 30, 7)}{{\\p0}}")

def flag(st, en, cx, cy, label, ic, color, w=300, h=150):
    """Result card: glass, coloured icon disc, heavy label (e.g. TRBE7 / TKHSER)."""
    ps.glass(30, st, en, cx, cy, w, h, r=32, dy=40, drift=8)
    E(36, st + 0.10, en, "Shape", f"{{\\an5\\pos({cx - w // 2 + 62},{cy})\\fad(120,200){pop()}{exit_(ms(en - st - 0.1))}\\c{color}\\p1}}{base.co(0, 0, 76)}{{\\p0}}")
    base.icon(37, st + 0.10, en, cx - w // 2 + 62, cy, ic, 40, f"\\fad(120,200){pop(40, 60)}", fill=FOREST)
    E(37, st + 0.14, en, "Heavy", f"{{\\an4\\pos({cx - w // 2 + 116},{cy + 2})\\fs52\\fad(120,200){pop(100, 40)}}}{label}")

PITCH = (1.0, 1.04, 0.96, 1.06, 0.94)

HEADER = ps.HEADER.replace("&H00FFC4E0", "&H00D0F3A7").replace("&H00200810", "&H000F1405")

# ---------- filter graph: green grade, face-anchored zoom, frosted bands, depth blur, gentle voice chain, SFX, -14 LUFS ----------
def filter_graph(ass_file, total, speech_end, zk, blur_win, frost_win, sfx, anchor_y=0.354, hold_from=None,
                 whips=(), behind_ass=None, roto_win=()):
    """frost_win: [(start, end, y, h)] plate bands blurred + darkened (under frost_panel).
    anchor_y: crop anchor so the face centre stays put while zooming (face_y / 1920).
    hold_from: freeze the picture from this time (skips a fade-out baked into the source); default speech_end.
    whips: cut times that get a zoom-blur whip (pair them with a zoom spike in zk).
    behind_ass + roto_win: text behind the subject. Input 1 must be the person matte (render_cmd adds it);
    the plate gets behind_ass, then the person is laid back on top inside roto_win."""
    hold = speech_end if hold_from is None else hold_from
    ass_path = ass_file.replace(":", "\\:")
    roto = bool(behind_ass and roto_win)
    n = 1 + len(blur_win) + len(frost_win) + len(whips) + (1 if roto else 0)
    timeline = (f"trim=0:{hold},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={total - hold + 0.3:.2f},trim=0:{total},setpts=PTS-STARTPTS,"
                f"scale=w='2*trunc(540*{zexpr(zk)})':h='2*trunc(960*{zexpr(zk)})':eval=frame:flags=bicubic,"
                f"crop=1080:1920:(iw-1080)/2:(ih-1920)*{anchor_y}")
    fc = [f"[0:v]eq=contrast=1.10:gamma=0.94:saturation=0.98,colorbalance=rs=-0.03:gs=0.04:bs=-0.01:gm=0.015,"
          f"{timeline},vignette=angle=PI/3.8:mode=forward,split={n}[vs]" + "".join(f"[p{i}]" for i in range(n - 1))]   # vignette the plate only, never text
    last, i = "vs", 0
    if roto:   # matte gets the same trim / hold / zoom / crop as the plate, so the person never floats
        behind = behind_ass.replace(":", "\\:")
        fc.append(f"[1:v]format=gray,tmix=frames=3,lut=y='clip((val-56)*1.4,0,255)',gblur=sigma=0.6,{timeline},format=gray[matte]")
        fc.append(f"[{last}]ass='{behind}'[bh]")
        fc.append(f"[p{i}]format=yuva420p[pa]")
        fc.append(f"[pa][matte]alphamerge[subj]")
        en = "+".join(f"between(t,{a},{b})" for a, b in roto_win)
        fc.append(f"[bh][subj]overlay=0:0:enable='{en}':format=auto[ro]"); last = "ro"; i += 1
    for s, e, y, h in frost_win:
        fc.append(f"[p{i}]trim={s}:{e},setpts=PTS-STARTPTS,crop=1080:{h}:0:{y},gblur=sigma=30,"
                  f"eq=brightness=-0.14:saturation=0.55,setpts=PTS+{s}/TB[fr{i}]")
        fc.append(f"[{last}][fr{i}]overlay=0:{y}:eof_action=pass[o{i}]"); last = f"o{i}"; i += 1
    for s, e in blur_win:
        fc.append(f"[p{i}]trim={s}:{e},setpts=PTS-STARTPTS,scale=1124:-2,crop=1080:1920,gblur=sigma=26,"
                  f"eq=brightness=-0.15:saturation=0.75,format=yuva420p,fade=t=in:d=0.24:alpha=1,"
                  f"fade=t=out:st={e - s - 0.24:.2f}:d=0.24:alpha=1,setpts=PTS+{s}/TB[bl{i}]")
        fc.append(f"[{last}][bl{i}]overlay=eof_action=pass:format=auto[o{i}]"); last = f"o{i}"; i += 1
    for t in whips:   # zoom-blur whip: a pushed-in, blurred copy flashes over the cut
        s, e = max(0, t - 0.16), t + 0.16
        fc.append(f"[p{i}]trim={s}:{e},setpts=PTS-STARTPTS,scale=1296:-2,crop=1080:1920,gblur=sigma=34,format=yuva420p,"
                  f"fade=t=in:d=0.12:alpha=1,fade=t=out:st={e - s - 0.18:.2f}:d=0.18:alpha=1,setpts=PTS+{s}/TB[wh{i}]")
        fc.append(f"[{last}][wh{i}]overlay=eof_action=pass:format=auto[o{i}]"); last = f"o{i}"; i += 1
    fc.append(f"[{last}]ass='{ass_path}',format=yuv420p[vout]")
    # source already has a mix (possible music bed): no denoiser, just clean-up EQ and light compression
    fc.append(f"[0:a]aresample=48000,highpass=f=70,equalizer=f=3000:t=q:w=1.2:g=1.5,"
              f"acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=2,apad=whole_dur={total}[voice]")
    first = 2 if roto else 1   # input index of the first SFX file
    seen = {}
    for k, (st, path, g) in enumerate(sfx):
        rep = seen[path] = seen.get(path, -1) + 1   # repeats of the same take get a slight pitch shift
        p = PITCH[rep % len(PITCH)]
        pitch = f"asetrate={48000 * p:.0f},aresample=48000," if p != 1.0 else ""
        fc.append(f"[{k + first}:a]aresample=48000,{pitch}aformat=channel_layouts=stereo,volume={g}dB,adelay={ms(st)}|{ms(st)}[s{k}]")
    fc.append("[voice]" + "".join(f"[s{k}]" for k in range(len(sfx))) +
              f"amix=inputs={len(sfx) + 1}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,atrim=0:{total}[aout]")
    return fc

def render_cmd(path, source, filt, sfx, out, total, matte_dir=None):
    """Write the exact ffmpeg render command for this edit (temp name, then mv on success)."""
    ff = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
    tmp = os.path.join(os.path.dirname(filt), "rendering-" + os.path.basename(out))
    ins = [f'-i "{source}"'] + ([f'-framerate 30 -i "{matte_dir}/%05d.png"'] if matte_dir else []) + [f'-i "{p}"' for _, p, _ in sfx]
    cmd = (f'{ff} -v error -y {" ".join(ins)} -/filter_complex "{filt}" -map "[vout]" -map "[aout]" -t {total} '
           f'-c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 '
           f'-r 30 -c:a aac -b:a 192k -movflags +faststart "{tmp}" && mv "{tmp}" "{out}"')
    open(path, "w").write("#!/bin/sh\n# generated by the build script; run: sh " + os.path.basename(path) + "\n" + cmd + "\n")
