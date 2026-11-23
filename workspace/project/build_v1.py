#!/usr/bin/env python3
# Developed by Mehdi ORANUSS | Powered by Claude
"""Build edit for IMG_2399: cut list, Latin-Darija captions, ASS graphics, ffmpeg command.
Source of truth for words: work/words_ar.txt (whisper large-v3 word timings, source timeline).
"""
import json, os, re, shlex

ROOT = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(ROOT, "work")

# ---------- 1. keep segments (source seconds) + zoom per segment ----------
# Cuts sit inside silences measured by silencedetect (-35dB, 0.5s).
# zoom: (start_scale, end_scale) -> slow push or static punch-in
SEGMENTS = [
    (0.00, 17.92, (1.00, 1.06)),
    (18.22, 24.69, (1.14, 1.14)),   # jump cut -> punch in
    (24.95, 49.00, (1.00, 1.07)),
    (49.00, 55.00, (1.16, 1.16)),   # emphasis "ghatl9aw bzzaf dyal lm3lomat"
    (55.00, 70.28, (1.02, 1.08)),
    (70.72, 80.88, (1.14, 1.14)),   # jump cut -> punch in
    # 80.88 -> 98.58 removed: retakes + off-camera talk ("zid zid", "ayeh dak s7i7, dkhel")
    (98.58, 110.90, (1.00, 1.06)),
    (110.90, 118.00, (1.14, 1.14)),
    (118.00, 123.00, (1.02, 1.06)),
    (123.00, 125.60, (1.18, 1.18)),  # outro punch
]
BIG_CUT_INDEX = 6  # segment that starts after the retake cut -> wipe transition

def src_to_out(t):
    off = 0.0
    for s, e, _ in SEGMENTS:
        if s <= t < e:
            return off + (t - s)
        off += e - s
    return None

TOTAL = sum(e - s for s, e, _ in SEGMENTS)
SEG_OUT_START = []
_o = 0.0
for s, e, _ in SEGMENTS:
    SEG_OUT_START.append(_o)
    _o += e - s

# ---------- 2. Arabic ASR token -> Latin Darija (as spoken) ----------
# "" = drop token (ASR artefact). Uncertain ones listed in caption_uncertainties.md
LATIN = [
 ("السلام","Salam"),("عليكم","3likom"),("اخواني","khwani,"),("مرحبا","mar7ba"),("بكم","bikom"),("في","f"),("هذا","had"),("الفيديو","lvideo."),
 ("تقصير","T9dim"),("ليه","lih"),("كمقدمة","k mo9addima"),("بالنسبة","bnnisba"),("لpersonal","l personal"),("branding","branding"),
 ("اللي","li"),("كاينة","kayna"),("في","f"),("البلاتفوم","la plateforme"),("اللي","li"),("انتو","ntoma"),("مبسطاتها","mabonniyin fiha"),("دخلتو","dkhltu"),("لهنا","lhna."),
 ("هاد","Had"),("المقدمة","lmo9addima"),("هادي","hadi"),("بغيت","bghit"),("نوريكم","nwrikom"),("البلاصة","lblassa"),("اللي","li"),("كنخدم","kankhdm"),("فيها","fiha"),("انايا","ana"),("مع","m3a"),("السي","si"),("حمزة","Hamza."),
 ("لهاد","Lhad"),("المكتبة","lmaktab,"),("دا",""),("كما","kima"),("كتشوفو","katchofo,"),("المكاتب","lmakatib"),("فاش","fach"),("كيكون","kaykon"),("لي","l'équipe"),("كيب",""),("دي","dyal"),("الاورانوس","Ouranos"),("اكاديمي","Academy"),
 ("اللي","li"),("كنخدمو","kankhdmo"),("اعلى","3la"),("الاماج","l'image"),("دي","dyal"),("الحمزة","Hamza"),("اورانوس","Ouranos"),("وللشركة","w la société"),("دي","dyal"),("الاورانوس","Ouranos"),("بشكل","bchkl"),("كبير","kbir."),
 ("فكيما","Fkima"),("كتعرفو","kat3rfo,"),("personal","personal"),("branding","branding"),("وحدة","wa7da"),("بين","mn"),("اهم","ahamm"),("الحواج","l7wayj"),("ليه","li"),("ولدها","wlat"),("بحاليين","daba lyoum"),("مهمة","mohimma"),
 ("لبزاف","lbzzaf"),("دي","dyal"),("الناس","nnas."),("ولو","Wlaw"),("كيقدرو","kay9dro"),("انهم","annahom"),("يبانو","ybanu"),("السوشال","f social"),("ميديا","media"),("بالوجه","b lwjh"),("ديالهم","dyalhom,"),
 ("وكيقدرو","w kay9dro"),("انهم","annahom"),("ينشؤو","ynchrou"),("محتوى","mo7tawa"),("ويبارطجو","w ypartagiw"),("افكار","afkar,"),("بارطجو","ypartagiw"),("المعلومات","lm3lomat"),("ليه","li"),("ما",""),("عندهم","3ndhom."),
 ("تكا","7tta"),("داريك","dik"),("الناس","nnas"),("ليه","li"),("ما","ma"),("عندهم","3ndhom"),("سنوات","snawat"),("ديال","dyal"),("الخبرة","lkhibra"),("في","f"),("شي","chi"),("مجال","majal"),("معين","mo3ayyan,"),
 ("برا","bra"),("كيقدرو","kay9dro"),("انهم","annahom"),("ينشؤو","ynchrou"),("المحتوى","lmo7tawa"),("وهكا","w hakka"),("كيقدرو","kay9dro"),("انهم","annahom"),("يشؤو","ynchou"),("بشكل","bchkl"),("كبير","kbir"),("بزين","bzzaf."),
 ("فهد","F had"),("الفيديوهات","lvidyouhat"),("هادو","hado"),("غتلقاو","ghatl9aw"),("بزاف","bzzaf"),("دي","dyal"),("المعلومات","lm3lomat"),
 ("لهادي","lhad"),("السنوات","snawat"),("في","f"),("أورانوس","Ouranos"),("اكاديمي","Academy,"),("وحتى","w 7tta"),("كدالك","kdalik"),("مع","m3a"),("اخويا","khoya"),("حمزة","Hamza."),
 ("ديكو","Dik"),("المعلومات","lm3lomat"),("ليه","li"),("جمعت","jm3t"),("منا","mn"),("عندو","3ndo,"),("لي","li"),("كيما","kima"),("كتشوفو","katchofo"),("هنية","hna"),("فهاد","f had"),("البلاصة","lblassa"),("هادي","hadi,"),
 ("هي","hiya"),("فاش","fach"),("كنكون","kankon"),("كنقريكم","kan9rikom"),("يا","ana"),("جماعة","w"),("اخويا","khoya"),("حمزة","Hamza."),
 ("هنية","Hna"),("فاش","fach"),("كنكون","kankono"),("كنديرو","kandiro"),("الدروس","ddrous"),("ديالنا","dyalna,"),("وهنية","w hna"),("فاش","fach"),("كنكونو","kankono"),("كنديرو","kandiro"),("الحصص","l7isas"),("ديالنا","dyalna."),
 ("فهد","F had"),("الامر","l'amr"),("هادو","hada"),("ليه","li"),("خصني","khassni"),("ضروري","darori"),("اننا","annana"),("نعطيكم","n3tikom"),("الطريقة","ttari9a"),("ليه","li"),("تنخد","kankhdm"),("بيانا","biha ana"),
 ("مع","m3a"),("حمزة","Hamza"),("أورانوس","Ouranos,"),("وهكا","w hakka"),("كنقدر","kan9dr"),("انا","ana"),("لنسندكم","nsandkom"),("بنفس","b nafs"),("المعلومات","lm3lomat"),("ليه","li"),
 ("تعلمتم","t3llmt"),("لهدي","lhad"),("السنوات","snawat."),
 # --- removed region (81-98.6s): first takes ---
 ("اوكي",""),("فلي",""),("بغيتكم",""),("انكم",""),("تبعو",""),("هاد",""),("الفيديوهات",""),("هادو",""),("زيد",""),("زيد",""),("سبعين",""),("سبعين",""),
 ("لي",""),("بغيتكم",""),("انكم",""),("تبعو",""),("هاد",""),("الفيديوهات",""),("فيديو",""),("فيديو",""),("باش",""),("تقدرو",""),("انكم",""),("تاخدو",""),("المعلومات",""),("ليه",""),("غي",""),("يعاونوكم",""),("سوى",""),("تقدرو",""),("انكم",""),
 ("ايه",""),("ذاك",""),("صح",""),("دخل",""),
 # --- final take ---
 ("لي","Li"),("بغيتكم","bghitkom"),("انكم","annakom"),("هو","huwa"),("تبعو","tb3o"),("هاد","had"),("الفيديوهات","lvidyouhat"),("شوية","chwiya"),("بشوية","b chwiya,"),
 ("باش","bach"),("تقدرو","t9dro"),("انكم","annakom"),("تجمعو","tjm3o"),("المعلومات","lm3lomat"),("ليه","li"),("غي","ghadi"),("تحتاجوهم","t7tajohom,"),
 ("باش","bach"),("تقدرو","t9dro"),("اول","awwal"),("حاجة","7aja"),("سوى","swa"),("انتو","ntoma"),("ما",""),("تبدو","tbdaw"),("وتبانو","w tbanu"),("بوجهكم","b wjhkom"),("في","f"),("السوشال","social"),("ميديا","media,"),
 ("سوى","swa"),("كذلك","kdalik"),("الناس","nnas"),("اخرين","lokhrin"),("ليه","li"),("ما","homa"),("محتاجينكم","m7tajinkom"),("انكم","annakom"),("تعاونوهم","t3awnohom,"),
 ("سوى","swa"),("باستشارة","b istichara,"),("سوى","swa"),("باعلومات","b m3lomat,"),("سوى","swa"),("بشي","b chi"),("حاجة","7aja"),("انتو","ntoma"),("ما",""),("محتاجينها","m7tajinha..."),
 ("ليه","li"),("ما","homa"),("محتاجينها","m7tajinha,"),("عفوا","3afwan."),
 ("باش","Bach"),("تقدرو","t9dro"),("انكم","annakom"),("تعاونوهم","t3awnohom"),("مشكل","bchkl"),("كبير","kbir."),
 ("فتبعو","Ftb3o"),("هاد","had"),("الفيديوهات","lvidyouhat"),("شوية","chwiya"),("بشوية","b chwiya"),("باش","bach"),("تقدرو","t9dro"),("انكم","annakom"),("تمشيو","tmchiw"),("مزيان","mzyan."),
 ("وحظ","W l7dd"),("موافق","mowaffaq"),("للجميع","lljami3!"),
]

def ts(s):
    m, sec = s.split(":")
    return int(m) * 60 + float(sec.replace(",", "."))

words = []
for line in open(os.path.join(W, "words_ar.txt"), encoding="utf8"):
    p = line.rstrip("\n").split(" ", 2)
    if len(p) < 3 or not p[2].strip():
        continue
    words.append((ts(p[0]), ts(p[1]), p[2].strip()))
assert len(words) == len(LATIN), (len(words), len(LATIN))
for (a, b, ar), (chk, lat) in zip(words, LATIN):
    assert ar == chk, (a, ar, chk)

# Whisper snaps many boundaries to whole seconds and gives zero-length words;
# spread zero/short words evenly between neighbours so captions stay readable.
lat_words = []
for (a, b, _), (_, lat) in zip(words, LATIN):
    if lat:
        lat_words.append([a, b, lat])
i = 0
while i < len(lat_words):
    j = i
    while j + 1 < len(lat_words) and abs(lat_words[j + 1][0] - lat_words[i][0]) < 1e-6:
        j += 1
    if j > i:  # group with identical start
        start = lat_words[i][0]
        end = max(lat_words[j][1], lat_words[j + 1][0] if j + 1 < len(lat_words) else start + 0.3 * (j - i + 1))
        end = max(end, start + 0.18 * (j - i + 1))
        step = (end - start) / (j - i + 1)
        for k in range(i, j + 1):
            lat_words[k][0] = start + step * (k - i)
            lat_words[k][1] = start + step * (k - i + 1)
    i = j + 1

# map to output timeline, drop words in removed regions
RETAKE = (80.88, 98.58)
def snap(t):
    """Whisper boundaries are coarse; a word inside a small trimmed pause really
    starts after it, so move it to the next kept segment instead of dropping it."""
    for s, e, _ in SEGMENTS:
        if t < s:
            return s
    return None

out_words = []
for a, b, lat in lat_words:
    if RETAKE[0] <= a < RETAKE[1]:
        continue
    oa = src_to_out(a + 0.01)
    if oa is None:
        a = snap(a); b = a + 0.3
        oa = src_to_out(a + 0.01)
    if oa is None:
        continue
    ob = src_to_out(min(b, a + 1.2) - 0.001)
    if ob is None or ob <= oa:
        ob = oa + 0.25
    out_words.append([oa, ob, lat])
for k in range(len(out_words) - 1):  # no overlap, fill tiny gaps
    nxt = out_words[k + 1][0]
    if out_words[k][1] > nxt or nxt - out_words[k][1] < 0.25:
        out_words[k][1] = nxt

# chunk into 2-4 word phrases, break after punctuation
chunks, cur = [], []
for w in out_words:
    cur.append(w)
    txt = w[2]
    long_ = sum(len(x[2]) for x in cur) > 22
    if txt[-1] in ".,!" or len(cur) >= 4 or long_:
        chunks.append(cur); cur = []
if cur:
    chunks.append(cur)
# merge one-word orphans into the previous phrase when it stays short
merged = []
for ch in chunks:
    if merged and len(ch) == 1 and merged[-1][-1][2][-1] not in ".!" \
            and len(" ".join(w[2] for w in merged[-1] + ch)) <= 34:
        merged[-1] += ch
    else:
        merged.append(ch)
chunks = merged

# ---------- 3. ASS ----------
PURPLE = "&H00E02B5B&"   # #5B2BE0 (wall purple, provisional)
YELLOW = "&H0000C4F5&"   # #F5C400 (wall yellow, provisional)
WHITE = "&H00FFFFFF&"

def at(t):
    t = max(0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def clean(txt):
    return txt.rstrip(".,!").replace("...", "")

ev = []
def E(layer, st, en, style, text):
    ev.append(f"Dialogue: {layer},{at(st)},{at(en)},{style},,0,0,0,,{text}")

srt = []
for ci, ch in enumerate(chunks):
    c_start, c_end = ch[0][0], ch[-1][1]
    if ci + 1 < len(chunks):
        c_end = min(c_end + 0.15, chunks[ci + 1][0][0])
    srt.append((c_start, c_end, " ".join(w[2] for w in ch)))
    for wi, w in enumerate(ch):
        st = w[0] if wi else c_start
        en = ch[wi + 1][0] if wi + 1 < len(ch) else c_end
        parts = []
        for k, x in enumerate(ch):
            t = clean(x[2])
            parts.append(f"{{\\c{YELLOW}}}{t}{{\\c{WHITE}}}" if k == wi else t)
        pop = "{\\fscx85\\fscy85\\t(0,90,\\fscx100\\fscy100)}" if wi == 0 else ""
        E(5, st, en, "Cap", pop + " ".join(parts))

def out(src):  # src time -> out time (must be inside kept region)
    o = src_to_out(src)
    assert o is not None, src
    return o

def pill(st, en, x, y, label, sub=None, align_right=False):
    """Animated purple card: bar wipes in, text fades up, all slides out."""
    wbar = max(len(label) * 30, len(sub or "") * 20) + 80
    hbar = 96 if sub is None else 140
    x0 = x - wbar if align_right else x
    clip_in = f"\\clip({x0},{y},{x0},{y + hbar})\\t(0,260,\\clip({x0},{y},{x0 + wbar},{y + hbar}))"
    E(10, st, en, "Shape", f"{{\\pos({x0},{y}){clip_in}\\fad(0,220)\\c{PURPLE}\\p1}}m 0 0 l {wbar} 0 l {wbar} {hbar} l 0 {hbar}{{\\p0}}")
    E(11, st, en, "Shape", f"{{\\pos({x0},{y}){clip_in}\\fad(0,220)\\c{YELLOW}\\p1}}m 0 0 l 10 0 l 10 {hbar} l 0 {hbar}{{\\p0}}")
    ty = y + (hbar // 2 if sub is None else 52)
    E(12, st + 0.15, en, "Card", f"{{\\an4\\pos({x0 + 40},{ty})\\fad(180,220)\\move({x0 + 20},{ty},{x0 + 40},{ty},150,400)}}{label}")
    if sub:
        E(12, st + 0.25, en, "CardSub", f"{{\\an4\\pos({x0 + 42},{y + 106})\\fad(200,220)}}{sub}")

# intro title
E(10, 0.4, 4.2, "Shape", f"{{\\pos(110,410)\\clip(110,410,110,600)\\t(0,350,\\clip(110,410,900,600))\\fad(0,300)\\c{PURPLE}\\p1}}m 0 0 l 760 0 l 760 170 l 0 170{{\\p0}}")
E(11, 0.6, 4.2, "Title", f"{{\\an4\\pos(150,470)\\fad(200,300)\\c{YELLOW}}}PERSONAL BRANDING")
E(11, 0.8, 4.2, "CardSub", f"{{\\an4\\pos(152,540)\\fad(200,300)}}Mo9addima · Ouranos Academy")

# timed callouts (anchored to the spoken source words)
pill(out(11.0), out(15.3), 80, 70, "OFFICE TOUR", "Ouranos Academy")
pill(out(26.4), out(30.6), 1840, 70, "PERSONAL BRANDING", align_right=True)
pill(out(33.1), out(36.0), 1840, 70, "SOCIAL MEDIA", "b lwjh dyalkom", align_right=True)
pill(out(36.5), out(40.0), 1840, 70, "CONTENT · IDEAS · INFO", align_right=True)
pill(out(41.7), out(46.0), 80, 70, "7tta bla snawat dyal lkhibra", align_right=False)
pill(out(56.0), out(59.0), 80, 70, "HAMZA OURANOS", "Ouranos Academy")
pill(out(65.0), out(70.2), 1840, 70, "DROUS & 7ISAS", "hna fach kan9rikom", align_right=True)

# 3 steps list after the retake cut
steps = [(99.6, "1", "Tb3o lvidyouhat chwiya b chwiya"),
         (106.2, "2", "Bano b wjhkom f social media"),
         (111.0, "3", "3awno nnas lokhrin")]
list_end = out(119.5)
for k, (s, n, txt) in enumerate(steps):
    st = out(s); y = 90 + k * 110
    bw = len(txt) * 20 + 140
    E(10, st, list_end, "Shape", f"{{\\pos(80,{y})\\clip(80,{y},80,{y + 90})\\t(0,300,\\clip(80,{y},{80 + bw},{y + 90}))\\fad(0,250)\\c{PURPLE}\\p1}}m 0 0 l {bw} 0 l {bw} 90 l 0 90{{\\p0}}")
    E(10, st, list_end, "Shape", f"{{\\pos(80,{y})\\fad(0,250)\\c{YELLOW}\\p1}}m 0 0 l 90 0 l 90 90 l 0 90{{\\p0}}")
    E(11, st + 0.05, list_end, "Num", f"{{\\an5\\pos(125,{y + 45})\\fad(150,250)}}{n}")
    E(11, st + 0.15, list_end, "Step", f"{{\\an4\\pos(195,{y + 45})\\fad(200,250)\\move(175,{y + 45},195,{y + 45},150,400)}}{txt}")

# wipe transition over the big retake cut
T = SEG_OUT_START[BIG_CUT_INDEX]
bar = "m 0 0 l 2400 0 l 2100 1080 l -300 1080"
E(20, T - 0.28, T, "Shape", f"{{\\pos(0,0)\\c{PURPLE}\\move(-2500,0,0,0)\\p1}}{bar}{{\\p0}}")
E(21, T - 0.20, T, "Shape", f"{{\\pos(0,0)\\c{YELLOW}\\move(-2700,0,-200,0)\\p1}}m 0 0 l 120 0 l -180 1080 l -300 1080{{\\p0}}")
E(20, T, T + 0.30, "Shape", f"{{\\pos(0,0)\\c{PURPLE}\\move(0,0,2500,0)\\p1}}{bar}{{\\p0}}")

# outro end card
TE = TOTAL
E(30, TE - 1.6, TE, "Shape", f"{{\\pos(0,0)\\c{PURPLE}\\fad(450,0)\\p1}}m 0 0 l 1920 0 l 1920 1080 l 0 1080{{\\p0}}")
E(31, TE - 1.4, TE, "Title", f"{{\\an5\\pos(960,500)\\fad(350,0)\\c{WHITE}\\fs120\\fscx90\\fscy90\\t(0,500,\\fscx100\\fscy100)}}OURANOS ACADEMY")
E(31, TE - 1.2, TE, "Title", f"{{\\an5\\pos(960,620)\\fs54\\fad(350,0)\\c{YELLOW}}}PERSONAL BRANDING")

HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Arial Black,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,5,3,2,120,120,80,1
Style: Shape,Arial,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Card,Arial Black,46,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,4,0,0,0,1
Style: CardSub,Avenir Next,34,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,1,0,1,0,0,4,0,0,0,1
Style: Title,Arial Black,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,4,0,0,0,1
Style: Num,Arial Black,54,&H00502B2B,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Step,Arial Black,42,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,4,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(os.path.join(W, "graphics.ass"), "w", encoding="utf8").write(HEADER + "\n".join(ev) + "\n")

def srt_t(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
os.makedirs(os.path.join(ROOT, "..", "output", "IMG_2399"), exist_ok=True)
with open(os.path.join(ROOT, "..", "output", "IMG_2399", "captions-latin-darija-v1.srt"), "w", encoding="utf8") as f:
    for n, (a, b, t) in enumerate(srt, 1):
        assert b > a
        f.write(f"{n}\n{srt_t(a)} --> {srt_t(b)}\n{t}\n\n")
json.dump([{"start": round(a, 3), "end": round(b, 3), "text": t} for a, b, t in out_words],
          open(os.path.join(W, "captions_words.json"), "w", encoding="utf8"), ensure_ascii=False, indent=0)

# ---------- 4. ffmpeg filter graph ----------
TONEMAP = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
fc = []
fc.append(f"[0:v]{TONEMAP},eq=contrast=1.06:saturation=1.12:gamma=0.98,"
          f"colorbalance=rs=0.02:bs=-0.02,split={len(SEGMENTS)}" + "".join(f"[v{i}]" for i in range(len(SEGMENTS))))
fc.append(f"[0:a]asplit={len(SEGMENTS)}" + "".join(f"[a{i}]" for i in range(len(SEGMENTS))))
cat = []
for i, (s, e, (z0, z1)) in enumerate(SEGMENTS):
    d = e - s
    if abs(z1 - z0) < 1e-6 and z0 == 1.0:
        zf = ""
    elif abs(z1 - z0) < 1e-6:
        zf = f",scale={int(1920 * z0) // 2 * 2}:-2,crop=1920:1080:(iw-1920)/2:(ih-1080)/2*0.85"
    else:
        zexpr = f"({z0}+({z1}-{z0})*t/{d:.3f})"
        zf = (f",scale=w='2*trunc(960*{zexpr})':h='2*trunc(540*{zexpr})':eval=frame:flags=bicubic"
              f",crop=1920:1080:(iw-1920)/2:(ih-1080)/2*0.85")
    fc.append(f"[v{i}]trim={s}:{e},setpts=PTS-STARTPTS{zf},setsar=1[vs{i}]")
    fc.append(f"[a{i}]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={d - 0.02:.3f}:d=0.02[as{i}]")
    cat.append(f"[vs{i}][as{i}]")
fc.append("".join(cat) + f"concat=n={len(SEGMENTS)}:v=1:a=1[vc][ac]")
ass_path = os.path.join(W, "graphics.ass").replace(":", "\\:")
fc.append(f"[vc]ass='{ass_path}',vignette=angle=PI/5:mode=forward,format=yuv420p[vout]")
fc.append("[ac]highpass=f=80,afftdn=nf=-25:tn=1,equalizer=f=3000:t=q:w=1.2:g=2,"
          "acompressor=threshold=-20dB:ratio=3:attack=10:release=150:makeup=2,"
          "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[aout]")
open(os.path.join(W, "filter.txt"), "w").write(";\n".join(fc))

print(f"segments={len(SEGMENTS)} out_duration={TOTAL:.2f}s words={len(out_words)} chunks={len(chunks)} big_cut_at={SEG_OUT_START[BIG_CUT_INDEX]:.2f}s")
