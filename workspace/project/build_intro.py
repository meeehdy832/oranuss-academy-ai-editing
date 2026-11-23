# Developed by Mehdi ORANUSS | Powered by Claude
"""5 s Oranuss Academy intro, made fully on this Mac (ElevenLabs blocked by billing): macOS "Majed" Arabic voice,
purple-glass motion graphics (planet + ring, glass card, Arabic title revealed right-to-left with the voice,
ORANUSS ACADEMY wordmark), earshot kit SFX, -14 LUFS.
Voice: work/intro/voice_raw.aiff (say -v Majed -r 165 "مرحباً بك في أورانوس أكاديمي"), placed at VOICE_AT.
Writes work/intro/intro.ass, filter_intro.txt, render.sh -> output/intro/Oranuss-Intro-5s-PREVIEW-v1.mp4"""
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motion import pop, exit_, wipe_lr, OUT, IN
from styles.base import PURPLE, NEON, LAV, NAVY, INK, WHITE, E, ms, co, rr, sparkle, zexpr, write_ass, place_sfx
from styles.purple_glass import HEADER, glass

ROOT = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(ROOT, "work", "intro")
KIT = os.path.join(ROOT, "work", "sfx", "kit")
OUT_MP4 = os.path.join(os.path.dirname(ROOT), "output", "intro", "Oranuss-Intro-5s-PREVIEW-v1.mp4")
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
TOTAL = 5.0
VOICE_AT = 0.6
LEAD = 0.067
# word times in video time (whisper -l ar on the voice + VOICE_AT)
T_MARHABA, T_FI, T_ORANUSS, T_ACADEMY, T_END = 0.61, 1.76, 1.78, 2.69, 3.70

ARAB = HEADER.split("\n[Events]")[0].rstrip() + "\n" + \
    "Style: Ar1,Tajawal ExtraBold,122,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1\n" + \
    "Style: Ar2,Cairo Black,156,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1\n\n" + \
    "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

def S(layer, st, en, tags, path):
    E(layer, st, en, "Shape", f"{{{tags}\\p1}}{path}{{\\p0}}")

# ---------- background: ink, drifting neon blobs, rising dust ----------
S(0, 0, TOTAL, f"\\an7\\pos(0,0)\\c{INK}", "m 0 0 l 1080 0 l 1080 1920 l 0 1920")
for (x0, y0, x1, y1, d, c, a) in [(180, 420, 300, 520, 760, NEON, "C8"), (900, 1500, 760, 1380, 820, PURPLE, "B8"),
                                  (820, 300, 700, 380, 520, PURPLE, "D0")]:
    S(1, 0, TOTAL, f"\\an5\\move({x0},{y0},{x1},{y1})\\c{c}\\1a&H{a}&\\blur90", co(0, 0, d))
random.seed(7)
for i in range(22):
    x = random.randint(70, 1010); y = random.randint(300, 1800); s = random.choice((6, 8, 10, 14))
    st = random.uniform(0, 1.2); c = random.choice((LAV, WHITE, NEON))
    S(2, st, TOTAL, f"\\an5\\move({x},{y},{x + random.randint(-30, 30)},{y - random.randint(120, 260)})"
                    f"\\fad(500,0)\\c{c}\\1a&H{random.choice(('40', '70', 'A0'))}&\\blur{s // 4}", co(0, 0, s))

# ---------- planet + ring (Oranuss / Uranus) ----------
PX, PY, PD = 540, 640, 300
P_IN = 0.15
ring = co(0, 0, 640)
def ring_part(layer, clip):
    S(layer, P_IN + 0.12, TOTAL, f"\\an5\\pos({PX},{PY}){clip}\\fad(250,0)\\frz-12\\1a&HFF&\\bord7\\3c{LAV}\\3a&H20&"
                                f"\\fscx0\\fscy0\\t(0,520,{OUT},\\fscx100\\fscy22)\\t(520,{ms(TOTAL - P_IN)},\\frz-8)", ring)
    S(layer, P_IN + 0.12, TOTAL, f"\\an5\\pos({PX},{PY}){clip}\\fad(250,0)\\frz-12\\1a&HFF&\\bord18\\3c{NEON}\\3a&H90&\\blur10"
                                f"\\fscx0\\fscy0\\t(0,520,{OUT},\\fscx100\\fscy22)\\t(520,{ms(TOTAL - P_IN)},\\frz-8)", ring)
ring_part(10, "")                                            # back half, behind the disc
S(11, P_IN, TOTAL, f"\\an5\\pos({PX},{PY})\\fad(200,0){pop()}\\c{NEON}\\1a&H70&\\blur40", co(0, 0, PD + 90))   # bloom
S(12, P_IN, TOTAL, f"\\an5\\pos({PX},{PY})\\fad(200,0){pop()}\\c{PURPLE}", co(0, 0, PD))                    # disc
disc = co(PX - PD / 2, PY - PD / 2, PD)
S(13, P_IN + 0.25, TOTAL, f"\\an5\\pos({PX - 60},{PY - 70})\\clip({disc})\\fad(300,0)\\c{LAV}\\1a&H90&\\blur36", co(0, 0, 170))
S(13, P_IN + 0.25, TOTAL, f"\\an5\\pos({PX + 90},{PY + 100})\\clip({disc})\\fad(300,0)\\c{INK}\\1a&H40&\\blur50", co(0, 0, 330))
S(14, P_IN + 0.25, TOTAL, f"\\an5\\pos({PX},{PY})\\fad(300,0)\\1a&HFF&\\bord2\\3c{LAV}\\3a&H60&", co(0, 0, PD))  # rim
ring_part(15, f"\\clip(0,{PY},1080,{PY + 200})")             # front half, over the disc

# ---------- glass card + Arabic title ----------
CY = 1120
glass(20, 0.45, TOTAL, 540, CY, 920, 470, r=40)
L1, L2 = CY - 125, CY + 35
# line 1 "مرحبا بك في": revealed right-to-left at the pace of the voice
t0 = T_MARHABA - LEAD
E(30, t0, TOTAL, "Ar1", f"{{\\an5\\pos(540,{L1})\\fad(150,0)\\clip(1000,{L1 - 90},1000,{L1 + 90})"
                       f"\\t(0,{ms(T_FI + 0.12 - t0)},0.8,\\clip(60,{L1 - 90},1000,{L1 + 90}))}}مرحبا بك في")
# line 2 "أورانوس أكاديمي": each word focus-pulls in on its own beat (right half, then left half)
for word_t, clip in [(T_ORANUSS, f"\\clip(540,{L2 - 120},1080,{L2 + 120})"), (T_ACADEMY, f"\\clip(0,{L2 - 120},540,{L2 + 120})")]:
    st = word_t - LEAD
    E(31, st, TOTAL, "Ar2", f"{{\\an5\\pos(540,{L2}){clip}\\c{NEON}\\1a&H30&\\blur22\\fad(120,0)"
                           f"\\t(0,500,\\1a&H70&)}}أورانوس أكاديمي")
    E(32, st, TOTAL, "Ar2", f"{{\\an5\\pos(540,{L2}){clip}\\c{LAV}\\blur14\\fad(120,0)"
                           f"\\t(0,260,{OUT},\\blur0.6\\c{WHITE})\\t(260,700,\\c{LAV})}}أورانوس أكاديمي")
# Latin wordmark under the title
WM = CY + 182
E(33, T_END - 0.45, TOTAL, "Heavy", f"{{\\an5\\pos(540,{WM})\\fs48\\fsp16\\c{LAV}"
                                     f"{wipe_lr(110, WM - 40, 970, WM + 40, 0, 420, OUT)}}}ORANUSS ACADEMY")
S(33, T_END - 0.25, TOTAL, f"\\an7\\pos(0,0)\\c{NEON}{wipe_lr(380, WM + 34, 700, WM + 42, 0, 380, OUT)}",
  rr(380, WM + 34, 320, 6, 3))

# ---------- accents: light sweep + sparkles on "Oranuss", sparkle on the wordmark ----------
band = "m 120 0 l 260 0 l 140 600 l 0 600"   # glass shine, clipped to the card
S(60, T_ORANUSS - 0.05, T_ORANUSS + 0.6, f"\\an7\\move(-300,{CY - 300},1100,{CY - 300})\\clip({rr(80, CY - 235, 920, 470, 40)})"
                                         f"\\c{WHITE}\\1a&HC8&\\blur18", band)
sparkle(T_ORANUSS, 540, L2, 1.4)
sparkle(T_END - 0.3, 540, WM, 0.9)

write_ass(os.path.join(W, "intro.ass"), ARAB)

# ---------- picture: slow push-in, grain, vignette; audio: voice polish + SFX, -14 LUFS ----------
ZK = [(0.0, 1.0), (TOTAL, 1.06)]
z = zexpr(ZK)
sfx = place_sfx([(P_IN + 0.35, "whoosh.long", 0, -9), (T_ORANUSS, "hit", 0, -10), (T_END - 0.3, "bell", 3, -17)], KIT)
ass = os.path.join(W, "intro.ass").replace(":", "\\:")
v = (f"[0:v]ass='{ass}',scale=w='trunc(1080*({z})/2)*2':h='trunc(1920*({z})/2)*2':eval=frame,"
     f"crop=1080:1920:(iw-1080)/2:(ih-1920)/2,noise=alls=5:allf=t,vignette=PI/4.2,format=yuv420p[v]")
a = [f"[1:a]aresample=48000,highpass=f=80,equalizer=f=220:t=q:w=1:g=2,equalizer=f=3800:t=q:w=1.2:g=2.5,"
     f"acompressor=threshold=-20dB:ratio=3:attack=5:release=80,aecho=0.8:0.6:38:0.12,adelay={ms(VOICE_AT)}:all=1[vo]"]
labels = ["[vo]"]
for i, (st, path, g) in enumerate(sfx):
    a.append(f"[{i + 2}:a]aresample=48000,volume={g}dB,adelay={ms(st)}:all=1[s{i}]"); labels.append(f"[s{i}]")
a.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,apad,atrim=0:{TOTAL},"
         f"loudnorm=I=-14:TP=-1.5:LRA=11,volume=2.2dB,alimiter=limit=0.84:level=0,aresample=48000[a]")
open(os.path.join(W, "filter_intro.txt"), "w").write(";\n".join([v] + a))

tmp = os.path.join(W, "rendering-intro.mp4")
inputs = " ".join(f"-i '{p}'" for _, p, _ in sfx)
cmd = (f"set -e\n'{FF}' -hide_banner -y -f lavfi -i color=c=0x100820:s=1080x1920:r=30:d={TOTAL} "
       f"-i '{os.path.join(W, 'voice_raw.aiff')}' {inputs} -/filter_complex '{os.path.join(W, 'filter_intro.txt')}' "
       f"-map '[v]' -map '[a]' -t {TOTAL} -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k "
       f"-movflags +faststart '{tmp}'\nmv '{tmp}' '{OUT_MP4}'\n")
open(os.path.join(W, "render.sh"), "w").write(cmd)
print("ok", len(sfx), "sfx")
