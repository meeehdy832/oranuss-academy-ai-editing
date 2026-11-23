#!/usr/bin/env python3
"""WhatsApp voice lesson: 6 Flow 3D shots + Oranuss glass keyword chips + quiet music.
Usage: python3 project/build_whatsapp_lesson.py <clips_dir> <out.mp4>
Clips: shot1.mp4..shot6.mp4 (any res, 9:16). Audio: output/whatsapp-lesson/audio/mix.wav"""
import subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, "output/whatsapp-lesson")
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
WIDTH, HEIGHT, FPS = 1080, 1920, 30
END = 47.5
CHIP_Y = 0  # v2 puppet: chips at top (set in main)

# (start, end) of each shot on the voice timeline (from whisper segments)
SHOTS = [(0.0, 7.7), (7.7, 17.0), (17.0, 26.5), (26.5, 34.5), (34.5, 38.5), (38.5, END)]
# keyword chips: (in, out, big line, small line)  -- only words he says
CHIPS = [
    (0.6, 7.3, "شخصية بصوتك", ""),
    (8.2, 12.2, "صوتك", ""),
    (12.4, 16.6, "ولا صوت AI", ""),
    (17.6, 26.1, "شارك المعلومة", ""),
    (29.0, 34.1, "الناس كيعقلو على الصوت", ""),
    (34.8, 38.2, "3D|ولا|2D", "2D animation  ·  3D character"),
    (39.0, 44.9, "تشرح الدروس", "فمختلف المجالات"),
]


def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def rrect(w, h, r):
    """ASS vector rounded rectangle, origin top-left."""
    k = r * 0.45
    return (f"m {r} 0 l {w-r} 0 b {w-k} 0 {w} {k} {w} {r} l {w} {h-r} b {w} {h-k} {w-k} {h} {w-r} {h} "
            f"l {r} {h} b {k} {h} 0 {h-k} 0 {h-r} l 0 {r} b 0 {k} {k} 0 {r} 0")


def ass():
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Shape,Graphik Arabic,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Big,Graphik Arabic Bold,78,&H00FFFFFF,&H00FFFFFF,&H00F65C8B,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Small,Graphik Arabic Medium,50,&H00FFC4E0,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Brand,Graphik Arabic SemiBold,34,&H00FFC4E0,&H00FFFFFF,&H00200810,&H00000000,0,0,0,0,100,100,6,0,1,2,0,8,0,0,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    ev.append(f"Dialogue: 5,{ts(0.3)},{ts(END-2.6)},Brand,,0,0,0,,{{\\fad(400,300)\\blur2}}ORANUSS ACADEMY")
    cy = 1430  # chip centre (inside Reels safe area)
    if CHIP_Y:  # v3 hook: three stacked kinetic words, stamped on the spoken word
        for (wt, word, y, hl) in [(3.24, "تخلق", 330, 0), (3.81, "شخصية", 470, 0), (4.33, "بصوتك", 615, 1)]:
            stamp = "\\fscx160\\fscy160\\t(0,140,\\fscx94\\fscy94)\\t(140,240,\\fscx100\\fscy100)"
            if hl:  # purple highlight box behind the key word
                ev.append(f"Dialogue: 3,{ts(wt)},{ts(7.5)},Shape,,0,0,0,,{{\\pos({WIDTH//2-250},{y-72})\\org({WIDTH//2},{y})\\fad(0,250){stamp}\\1c&HE02B5B&\\bord0}}{{\\p1}}{rrect(500,144,30)}{{\\p0}}")
            ev.append(f"Dialogue: 4,{ts(wt)},{ts(7.5)},Big,,0,0,0,,{{\\pos({WIDTH//2},{y})\\fad(0,250){stamp}\\fs138\\3c&H200810&\\bord5\\shad0}}{word}")
        ev.append(f"Dialogue: 4,{ts(0.15)},{ts(1.25)},Big,,0,0,0,,{{\\pos({WIDTH//2},{560})\\fad(120,150)\\fscx80\\fscy80\\t(0,200,\\fscx100\\fscy100)\\fs70\\1c&HFFC4E0&\\bord0}}هاد القضية")
    for a, b, big, small in (CHIPS[1:] if CHIP_Y else CHIPS):
        cy = CHIP_Y if CHIP_Y else (975 if "|" in big else 1430)  # v1: 3D/2D chip on the split divider
        n = len(big)
        w = min(980, max(520 if small else 360, int(n * 44 + 140)))
        h = 190 if small else 128
        x0, y0 = (WIDTH - w) // 2, cy - h // 2
        shape = rrect(w, h, 34)
        pop = "\\fscx70\\fscy70\\t(0,180,\\fscx104\\fscy104)\\t(180,320,\\fscx100\\fscy100)"
        org = f"\\org({WIDTH//2},{cy})"
        fad = "\\fad(140,220)"
        # bloom, glass fill, sheen, rim
        ev.append(f"Dialogue: 1,{ts(a)},{ts(b)},Shape,,0,0,0,,{{\\pos({x0},{y0}){org}{fad}{pop}\\1c&HF65C8B&\\1a&H90&\\blur24\\bord0}}{{\\p1}}{shape}{{\\p0}}")
        ev.append(f"Dialogue: 2,{ts(a)},{ts(b)},Shape,,0,0,0,,{{\\pos({x0},{y0}){org}{fad}{pop}\\1c&H2E0F14&\\1a&H38&\\bord0}}{{\\p1}}{shape}{{\\p0}}")
        ev.append(f"Dialogue: 3,{ts(a)},{ts(b)},Shape,,0,0,0,,{{\\pos({x0},{y0}){org}{fad}{pop}\\1a&HFF&\\3c&HFFC4E0&\\3a&H30&\\bord2.5}}{{\\p1}}{shape}{{\\p0}}")
        ty = cy - (30 if small else 0)
        if "|" in big:  # mixed Latin/Arabic: place pieces right-to-left by hand (bidi-safe)
            pieces = big.split("|"); xs = [WIDTH//2 + 190, WIDTH//2, WIDTH//2 - 190]
            for k, piece in enumerate(pieces):
                ev.append(f"Dialogue: 4,{ts(a+0.05+0.12*k)},{ts(b)},Big,,0,0,0,,{{\\pos({xs[k]},{ty}){org}{fad}{pop}\\bord0\\blur0.6}}{piece}")
        else:
            ev.append(f"Dialogue: 4,{ts(a+0.05)},{ts(b)},Big,,0,0,0,,{{\\pos({WIDTH//2},{ty}){org}{fad}{pop}\\bord0\\blur0.6}}{big}")
        if small:
            ev.append(f"Dialogue: 4,{ts(a+0.25)},{ts(b)},Small,,0,0,0,,{{\\pos({WIDTH//2},{cy+50}){fad}\\bord0\\fsp0}}{small}")
    # end card
    ev.append(f"Dialogue: 6,{ts(END-2.4)},{ts(END)},Shape,,0,0,0,,{{\\pos(0,0)\\fad(350,0)\\1c&H200810&\\bord0}}{{\\p1}}m 0 0 l {WIDTH} 0 l {WIDTH} {HEIGHT} l 0 {HEIGHT}{{\\p0}}")
    ev.append(f"Dialogue: 7,{ts(END-2.4)},{ts(END)},Shape,,0,0,0,,{{\\pos({WIDTH//2-260},{HEIGHT//2-260})\\fad(350,0)\\1c&HF65C8B&\\1a&HA0&\\blur60\\bord0}}{{\\p1}}{rrect(520,520,260)}{{\\p0}}")
    ev.append(f"Dialogue: 8,{ts(END-2.2)},{ts(END)},Big,,0,0,0,,{{\\pos({WIDTH//2},{HEIGHT//2-20})\\fad(300,0)\\fs86\\fsp8\\3c&HF65C8B&\\bord3\\blur8}}ORANUSS")
    ev.append(f"Dialogue: 9,{ts(END-2.2)},{ts(END)},Big,,0,0,0,,{{\\pos({WIDTH//2},{HEIGHT//2-20})\\fad(300,0)\\fs86\\fsp8\\bord0}}ORANUSS")
    ev.append(f"Dialogue: 9,{ts(END-2.0)},{ts(END)},Small,,0,0,0,,{{\\pos({WIDTH//2},{HEIGHT//2+60})\\fad(300,0)\\fsp10}}ACADEMY")
    return head + "\n".join(ev) + "\n"


def main():
    global CHIP_Y
    clips, out = sys.argv[1], sys.argv[2]
    if clips.endswith(".mp4"):  # v2: one pre-rendered puppet video
        CHIP_Y = 330
        work = os.path.join(ROOT, "project/work/whatsapp-lesson"); assf = os.path.join(work, "overlay_v2.ass")
        open(assf, "w").write(ass())
        tmp = out + ".part.mp4"
        cmd = [FF, "-v", "error", "-y", "-i", clips, "-i", os.path.join(W, "audio/mix.wav"), "-filter_complex",
               f"[0:v]tpad=stop_mode=clone:stop_duration=3,trim=0:{END},ass='{assf}',format=yuv420p[v]",
               "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-t", str(END), "-movflags", "+faststart", tmp]
        subprocess.run(cmd, check=True); os.replace(tmp, out); print("ok", out); return
    work = os.path.join(ROOT, "project/work/whatsapp-lesson"); os.makedirs(work, exist_ok=True)
    assf = os.path.join(work, "overlay.ass")
    open(assf, "w").write(ass())
    inputs, parts = [], []
    for i, (a, b) in enumerate(SHOTS):
        d = b - a
        inputs += ["-i", os.path.join(clips, f"shot{i+1}.mp4")]
        z = f"min(1+0.04*t/{d:.2f},1.04)"  # slow push-in for extra life
        parts.append(
            f"[{i}:v]setpts=PTS-STARTPTS,fps={FPS},scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={WIDTH}:{HEIGHT},tpad=stop_mode=clone:stop_duration=6,trim=0:{d+0.3:.3f},setpts=PTS-STARTPTS,"
            f"scale=w='trunc({WIDTH}*{z}/2)*2':h='trunc({HEIGHT}*{z}/2)*2':eval=frame,crop={WIDTH}:{HEIGHT},"
            f"eq=contrast=1.03:saturation=1.05,format=yuv420p[v{i}]")
    # xfade chain (0.3 s dissolves / slides)
    trans = ["fade", "slideleft", "fadewhite", "smoothup", "circleopen"]
    cur, acc = "v0", SHOTS[0][1] - SHOTS[0][0]
    for i in range(1, len(SHOTS)):
        off = acc - 0.0
        nxt = f"x{i}"
        parts.append(f"[{cur}][v{i}]xfade=transition={trans[i-1]}:duration=0.3:offset={off:.3f}[{nxt}]")
        cur = nxt; acc += SHOTS[i][1] - SHOTS[i][0]
    parts.append(f"[{cur}]trim=0:{END},ass='{assf}',format=yuv420p[vout]")
    audio = os.path.join(W, "audio/mix.wav")
    tmp = out + ".part.mp4"
    cmd = [FF, "-v", "error", "-y", *inputs, "-i", audio, "-filter_complex", ";".join(parts),
           "-map", "[vout]", "-map", f"{len(SHOTS)}:a", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(END), "-movflags", "+faststart", tmp]
    open(os.path.join(work, "render.sh"), "w").write(" ".join(f"'{c}'" for c in cmd) + "\n")
    subprocess.run(cmd, check=True)
    os.replace(tmp, out)
    print("ok", out)


if __name__ == "__main__":
    main()
