#!/usr/bin/env python3
"""voice-ai-lesson: Arabic glass keyword chips (Graphik Arabic) + end card over the puppet video, voice + ducked music at -14 LUFS.
Usage: python3 project/build_voice_ai_lesson.py <puppet.mp4> <out.mp4>"""
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_whatsapp_lesson import ts, rrect, ass as _unused  # noqa: F401  (shared helpers)
import build_whatsapp_lesson as B

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WK = os.path.join(ROOT, "project/work/voice-ai-lesson")
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
WIDTH, HEIGHT = 1080, 1920
END = 56.5
CY = 300  # chip centre (top safe area, above the character)
# (in, out, text pieces right->left, small line, highlight) -- only words heard clearly in the voice
CHIPS = [
    (4.0, 6.9, ["يا سي محمد"], "", 0),
    (7.3, 8.55, ["الصوت ديالي"], "", 1),
    (9.6, 12.35, ["بالذكاء الاصطناعي"], "", 0),
    (12.6, 13.58, ["الصوت ديالك"], "", 0),
    (13.6, 14.7, ["براند"], "", 1),
    (14.7, 16.7, ["الناس يعقلو عليك"], "", 0),
    (17.1, 20.6, ["AI"], "الفيديو", 1),
    (24.6, 25.8, ["جهود كبيرة"], "", 0),
    (25.8, 26.7, ["ياخدو وقت"], "", 0),
    (30.0, 32.75, ["شخصية", "2D"], "", 0),
    (33.3, 35.75, ["شخصية", "3D"], "", 1),
    (36.4, 38.35, ["كتسجلو أوديوات"], "", 0),
    (38.7, 40.5, ["تشارك شي معلومة"], "", 0),
    (41.0, 42.4, ["المونتاج"], "", 0),
    (42.45, 43.65, ["كتعجب الناس"], "", 1),
    (44.4, 46.3, ["توصل لهم الفكرة"], "", 0),
    (47.9, 50.5, ["الصور والفيديوهات"], "", 0),
    (52.4, 54.6, ["للجمهور ديالك"], "", 1),
]


def build_ass():
    head = B.ass().split("[Events]")[0]  # same styles as video 1
    ev = ["[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    ev.append(f"Dialogue: 5,{ts(0.4)},{ts(END-2.0)},Brand,,0,0,0,,{{\\fad(400,300)\\blur2}}ORANUSS ACADEMY")
    # hook stamp: "أنا هنا" slams in with the landing
    stamp = "\\fscx170\\fscy170\\t(0,140,\\fscx92\\fscy92)\\t(140,240,\\fscx100\\fscy100)"
    y = 420
    ev.append(f"Dialogue: 3,{ts(0.78)},{ts(2.6)},Shape,,0,0,0,,{{\\pos({WIDTH//2-260},{y-78})\\org({WIDTH//2},{y})\\fad(0,250){stamp}\\1c&HE02B5B&\\bord0}}{{\\p1}}{rrect(520,156,34)}{{\\p0}}")
    ev.append(f"Dialogue: 4,{ts(0.78)},{ts(2.6)},Big,,0,0,0,,{{\\pos({WIDTH//2},{y})\\fad(0,250){stamp}\\fs140\\3c&H200810&\\bord5\\shad0}}أنا هنا")
    for a, b, pieces, small, hl in CHIPS:
        txt = " ".join(pieces)
        w = min(980, max(300, int(len(txt) * 46 + 150)))
        h = 190 if small else 130
        x0, y0 = (WIDTH - w) // 2, CY - h // 2
        shape = rrect(w, h, 36)
        pop = "\\fscx70\\fscy70\\t(0,180,\\fscx104\\fscy104)\\t(180,320,\\fscx100\\fscy100)"
        org = f"\\org({WIDTH//2},{CY})"; fad = "\\fad(140,200)"
        fill = "\\1c&HE02B5B&\\1a&H10&" if hl else "\\1c&H2E0F14&\\1a&H38&"
        ev.append(f"Dialogue: 1,{ts(a)},{ts(b)},Shape,,0,0,0,,{{\\pos({x0},{y0}){org}{fad}{pop}\\1c&HF65C8B&\\1a&H90&\\blur24\\bord0}}{{\\p1}}{shape}{{\\p0}}")
        ev.append(f"Dialogue: 2,{ts(a)},{ts(b)},Shape,,0,0,0,,{{\\pos({x0},{y0}){org}{fad}{pop}{fill}\\bord0}}{{\\p1}}{shape}{{\\p0}}")
        ev.append(f"Dialogue: 3,{ts(a)},{ts(b)},Shape,,0,0,0,,{{\\pos({x0},{y0}){org}{fad}{pop}\\1a&HFF&\\3c&HFFC4E0&\\3a&H30&\\bord2.5}}{{\\p1}}{shape}{{\\p0}}")
        ty = CY + (24 if small else 0)
        if len(pieces) == 1:
            ev.append(f"Dialogue: 4,{ts(a+0.05)},{ts(b)},Big,,0,0,0,,{{\\pos({WIDTH//2},{ty}){org}{fad}{pop}\\bord0\\blur0.6}}{pieces[0]}")
        else:  # Arabic word on the right, Latin token on the left (bidi-safe manual placement)
            ar, la = pieces
            wa = len(ar) * 44; wl = len(la) * 50; gap = 26
            tot = wa + wl + gap; xr = WIDTH // 2 + tot / 2 - wa / 2; xl = WIDTH // 2 - tot / 2 + wl / 2
            ev.append(f"Dialogue: 4,{ts(a+0.05)},{ts(b)},Big,,0,0,0,,{{\\pos({xr:.0f},{ty}){org}{fad}{pop}\\bord0\\blur0.6}}{ar}")
            ev.append(f"Dialogue: 4,{ts(a+0.17)},{ts(b)},Big,,0,0,0,,{{\\pos({xl:.0f},{ty}){org}{fad}{pop}\\1c&HFFC4E0&\\bord0\\blur0.6}}{la}")
        if small:
            ev.append(f"Dialogue: 4,{ts(a+0.2)},{ts(b)},Small,,0,0,0,,{{\\pos({WIDTH//2},{CY-50}){fad}\\bord0\\fsp0}}{small}")
    # end card
    E0 = 54.6
    ev.append(f"Dialogue: 6,{ts(E0)},{ts(END)},Shape,,0,0,0,,{{\\pos(0,0)\\fad(450,0)\\1c&H200810&\\1a&H20&\\bord0}}{{\\p1}}m 0 0 l {WIDTH} 0 l {WIDTH} {HEIGHT} l 0 {HEIGHT}{{\\p0}}")
    ev.append(f"Dialogue: 7,{ts(E0)},{ts(END)},Shape,,0,0,0,,{{\\pos({WIDTH//2-260},{HEIGHT//2-260})\\fad(450,0)\\1c&HF65C8B&\\1a&HA0&\\blur60\\bord0}}{{\\p1}}{rrect(520,520,260)}{{\\p0}}")
    pop = "\\fscx60\\fscy60\\t(0,260,\\fscx106\\fscy106)\\t(260,420,\\fscx100\\fscy100)"
    ev.append(f"Dialogue: 8,{ts(E0+0.2)},{ts(END)},Big,,0,0,0,,{{\\pos({WIDTH//2},{HEIGHT//2-20})\\org({WIDTH//2},{HEIGHT//2})\\fad(250,0){pop}\\fs86\\fsp8\\3c&HF65C8B&\\bord3\\blur8}}ORANUSS")
    ev.append(f"Dialogue: 9,{ts(E0+0.2)},{ts(END)},Big,,0,0,0,,{{\\pos({WIDTH//2},{HEIGHT//2-20})\\org({WIDTH//2},{HEIGHT//2})\\fad(250,0){pop}\\fs86\\fsp8\\bord0}}ORANUSS")
    ev.append(f"Dialogue: 9,{ts(E0+0.45)},{ts(END)},Small,,0,0,0,,{{\\pos({WIDTH//2},{HEIGHT//2+60})\\fad(300,0)\\fsp10}}ACADEMY")
    return head + "\n".join(ev) + "\n"


def mix(out_wav):
    voice = os.path.join(WK, "voice48.wav")
    music = os.path.join(ROOT, "music/sub_clair-background-music-591220 (2).mp3")
    fc = (f"[0:a]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-15:TP=-2:LRA=9,apad=whole_dur={END}[v];"
          f"[v]asplit=2[vm][vk];"
          f"[1:a]atrim=0:{END},asetpts=PTS-STARTPTS,volume=0.16,afade=t=in:d=0.4,afade=t=out:st={END-2.2}:d=2.2[m];"
          f"[m][vk]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];"
          f"[vm][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[a]")
    raw = out_wav.replace(".wav", "_raw.wav")
    subprocess.run([FF, "-v", "error", "-y", "-i", voice, "-stream_loop", "-1", "-i", music, "-filter_complex", fc, "-map", "[a]", "-t", str(END), raw], check=True)
    r = subprocess.run([FF, "-hide_banner", "-i", raw, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = float([l for l in r.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    subprocess.run([FF, "-v", "error", "-y", "-i", raw, "-af", f"volume={-14 - I:.2f}dB,alimiter=limit=0.89:level=false", out_wav], check=True)
    print("loudness", I, "-> -14")


def main():
    src, out = sys.argv[1], sys.argv[2]
    assf = os.path.join(WK, "overlay.ass"); open(assf, "w").write(build_ass())
    wav = os.path.join(WK, "mix.wav"); mix(wav)
    tmp = os.path.join(os.path.dirname(out), "_part_" + os.path.basename(out))
    subprocess.run([FF, "-v", "error", "-y", "-i", src, "-i", wav, "-filter_complex",
                    f"[0:v]tpad=stop_mode=clone:stop_duration=3,trim=0:{END},ass='{assf}',format=yuv420p[v]",
                    "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-t", str(END), "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out); print("ok", out)


if __name__ == "__main__":
    main()
