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
 ("لهاد","Lhad"),("المكتبة","lmaktab,"),("دا",""),("كما","kima"),("كتشوفو","katchofo,"),("المكاتب","lmakatib"),("فاش","fach"),("كيكون","kaykon"),("لي","l'équipe"),("كيب",""),("دي","dyal"),("الاورانوس","Oranuss"),("اكاديمي","Academy"),
 ("اللي","li"),("كنخدمو","kankhdmo"),("اعلى","3la"),("الاماج","l'image"),("دي","dyal"),("الحمزة","Hamza"),("اورانوس","Oranuss"),("وللشركة","w la société"),("دي","dyal"),("الاورانوس","Oranuss"),("بشكل","bchkl"),("كبير","kbir."),
 ("فكيما","Fkima"),("كتعرفو","kat3rfo,"),("personal","personal"),("branding","branding"),("وحدة","wa7da"),("بين","mn"),("اهم","ahamm"),("الحواج","l7wayj"),("ليه","li"),("ولدها","wlat"),("بحاليين","daba lyoum"),("مهمة","mohimma"),
 ("لبزاف","lbzzaf"),("دي","dyal"),("الناس","nnas."),("ولو","Wlaw"),("كيقدرو","kay9dro"),("انهم","annahom"),("يبانو","ybanu"),("السوشال","f social"),("ميديا","media"),("بالوجه","b lwjh"),("ديالهم","dyalhom,"),
 ("وكيقدرو","w kay9dro"),("انهم","annahom"),("ينشؤو","ynchrou"),("محتوى","mo7tawa"),("ويبارطجو","w ypartagiw"),("افكار","afkar,"),("بارطجو","ypartagiw"),("المعلومات","lm3lomat"),("ليه","li"),("ما",""),("عندهم","3ndhom."),
 ("تكا","7tta"),("داريك","dik"),("الناس","nnas"),("ليه","li"),("ما","ma"),("عندهم","3ndhom"),("سنوات","snawat"),("ديال","dyal"),("الخبرة","lkhibra"),("في","f"),("شي","chi"),("مجال","majal"),("معين","mo3ayyan,"),
 ("برا","bra"),("كيقدرو","kay9dro"),("انهم","annahom"),("ينشؤو","ynchrou"),("المحتوى","lmo7tawa"),("وهكا","w hakka"),("كيقدرو","kay9dro"),("انهم","annahom"),("يشؤو","ynchou"),("بشكل","bchkl"),("كبير","kbir"),("بزين","bzzaf."),
 ("فهد","F had"),("الفيديوهات","lvidyouhat"),("هادو","hado"),("غتلقاو","ghatl9aw"),("بزاف","bzzaf"),("دي","dyal"),("المعلومات","lm3lomat"),
 ("لهادي","lhad"),("السنوات","snawat"),("في","f"),("أورانوس","Oranuss"),("اكاديمي","Academy,"),("وحتى","w 7tta"),("كدالك","kdalik"),("مع","m3a"),("اخويا","khoya"),("حمزة","Hamza."),
 ("ديكو","Dik"),("المعلومات","lm3lomat"),("ليه","li"),("جمعت","jm3t"),("منا","mn"),("عندو","3ndo,"),("لي","li"),("كيما","kima"),("كتشوفو","katchofo"),("هنية","hna"),("فهاد","f had"),("البلاصة","lblassa"),("هادي","hadi,"),
 ("هي","hiya"),("فاش","fach"),("كنكون","kankon"),("كنقريكم","kan9rikom"),("يا","ana"),("جماعة","w"),("اخويا","khoya"),("حمزة","Hamza."),
 ("هنية","Hna"),("فاش","fach"),("كنكون","kankono"),("كنديرو","kandiro"),("الدروس","ddrous"),("ديالنا","dyalna,"),("وهنية","w hna"),("فاش","fach"),("كنكونو","kankono"),("كنديرو","kandiro"),("الحصص","l7isas"),("ديالنا","dyalna."),
 ("فهد","F had"),("الامر","l'amr"),("هادو","hada"),("ليه","li"),("خصني","khassni"),("ضروري","darori"),("اننا","annana"),("نعطيكم","n3tikom"),("الطريقة","ttari9a"),("ليه","li"),("تنخد","kankhdm"),("بيانا","biha ana"),
 ("مع","m3a"),("حمزة","Hamza"),("أورانوس","Oranuss,"),("وهكا","w hakka"),("كنقدر","kan9dr"),("انا","ana"),("لنسندكم","nsandkom"),("بنفس","b nafs"),("المعلومات","lm3lomat"),("ليه","li"),
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

# ---------- 3. ASS (v2: dark glass / neon purple style from reference/) ----------
PURPLE = "&H00E02B5B&"   # #5B2BE0 wall purple
NEON = "&H00F65C8B&"     # #8B5CF6 glow purple
LAV = "&H00FFC4E0&"      # #E0C4FF lavender border/text
NAVY = "&H002E0F14&"     # #140F2E glass fill
INK = "&H00200810&"      # #100820 end-card bg
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

def rrect(w, h, r):
    return (f"m {r} 0 l {w - r} 0 b {w} 0 {w} 0 {w} {r} l {w} {h - r} b {w} {h} {w} {h} {w - r} {h} "
            f"l {r} {h} b 0 {h} 0 {h} 0 {h - r} l 0 {r} b 0 0 0 0 {r} 0")

def circle(d):
    r = d / 2; k = r * 0.5523
    return (f"m {r} 0 b {r + k} 0 {d} {r - k} {d} {r} b {d} {r + k} {r + k} {d} {r} {d} "
            f"b {r - k} {d} 0 {r + k} 0 {r} b 0 {r - k} {r - k} 0 {r} 0")

POP = "\\fscx92\\fscy92\\t(0,260,0.6,\\fscx100\\fscy100)"

def glass(layer, st, en, cx, cy, w, h, r=26, fade=(220, 220), anim=POP):
    """Glass card: neon bloom + translucent navy fill + top sheen + thin lavender rim."""
    f = f"\\fad({fade[0]},{fade[1]})"
    E(layer, st, en, "Shape", f"{{\\an5\\pos({cx},{cy}){f}{anim}\\c{NEON}\\1a&H70&\\blur22\\p1}}{rrect(w + 16, h + 16, r + 8)}{{\\p0}}")
    E(layer + 1, st, en, "Shape", f"{{\\an5\\pos({cx},{cy}){f}{anim}\\c{NAVY}\\1a&H38&\\p1}}{rrect(w, h, r)}{{\\p0}}")
    E(layer + 2, st, en, "Shape", f"{{\\an5\\pos({cx},{cy - h // 4}){f}{anim}\\c{WHITE}\\1a&HEC&\\p1}}{rrect(w - 8, h // 2 - 4, r - 4)}{{\\p0}}")
    E(layer + 3, st, en, "Shape", f"{{\\an5\\pos({cx},{cy}){f}{anim}\\1a&HFF&\\bord2\\3c{LAV}\\3a&H30&\\p1}}{rrect(w, h, r)}{{\\p0}}")

def glow_text(layer, st, en, style, tags, text, glow=NEON):
    E(layer, st, en, style, f"{{{tags}\\c{glow}\\3c{glow}\\bord4\\blur14\\1a&H40&}}{text}")
    E(layer + 1, st, en, style, f"{{{tags}}}{text}")

def callout(st, en, small, big, side="R", y=150):
    w = max(len(big) * 34, len(small or "") * 17) + 110
    h = 150 if small else 112
    cx = 1840 - w // 2 if side == "R" else 80 + w // 2
    glass(10, st, en, cx, y, w, h)
    lx = cx - w // 2 + 48
    mv = lambda yy: f"\\an4\\move({lx - 24},{yy},{lx},{yy},0,350)\\fad(250,220)"
    if small:
        E(15, st + 0.10, en, "Light", f"{{{mv(y - 34)}}}{small}")
        glow_text(15, st + 0.18, en, "Heavy", mv(y + 22), big)
    else:
        glow_text(15, st + 0.12, en, "Heavy", mv(y), big)

def out(src):
    o = src_to_out(src)
    assert o is not None, src
    return o

# --- captions: white words, active word in a purple highlight box (kinetic style) ---
srt = []
for ci, ch in enumerate(chunks):
    c_start, c_end = ch[0][0], ch[-1][1]
    if ci + 1 < len(chunks):
        c_end = min(c_end + 0.15, chunks[ci + 1][0][0])
    srt.append((c_start, c_end, " ".join(w[2] for w in ch)))
    words_ = [clean(x[2]) for x in ch]
    pop = "{\\fscx88\\fscy88\\t(0,110,\\fscx100\\fscy100)}"
    for wi, w in enumerate(ch):
        st = w[0] if wi else c_start
        en = ch[wi + 1][0] if wi + 1 < len(ch) else c_end
        p = pop if wi == 0 else ""
        # soft dark halo under the whole line for readability on bright walls
        E(4, st, en, "CapHalo", p + " ".join(words_))
        parts = [f"{{\\3a&H00&}}{t}{{\\3a&HFF&}}" if k == wi else t for k, t in enumerate(words_)]
        E(5, st, en, "Cap", p + "{\\3a&HFF&}" + " ".join(parts))

# --- intro: glass title card over blurred first seconds (blur done in ffmpeg) ---
IN0, IN1 = 0.25, 3.0
exit_ = f"\\t({int((IN1 - IN0 - 0.35) * 1000)},{int((IN1 - IN0) * 1000)},\\fscx112\\fscy112)"
glass(10, IN0, IN1, 960, 540, 980, 330, r=34, fade=(250, 300), anim=POP + exit_)
E(15, IN0 + 0.15, IN1, "Light", f"{{\\an5\\pos(960,420)\\fad(250,300)\\fsp6}}MO9ADDIMA")
glow_text(15, IN0 + 0.30, IN1, "Heavy", f"\\an5\\pos(960,505)\\fs92\\fad(200,300)\\fscx80\\t(0,300,\\fscx100)", "PERSONAL")
E(16, IN0 + 0.55, IN1, "Shape", f"{{\\an5\\pos(960,612)\\c{PURPLE}\\fad(150,300)\\clip(600,560,600,670)\\t(0,280,\\clip(600,560,1320,670))\\p1}}{rrect(660, 104, 10)}{{\\p0}}")
E(17, IN0 + 0.65, IN1, "Heavy", f"{{\\an5\\pos(960,612)\\fs88\\fad(150,300)}}BRANDING")
E(15, IN0 + 0.9, IN1, "Light", f"{{\\an5\\pos(960,690)\\fs30\\fad(250,300)\\c{LAV}}}Oranuss Academy")

# --- callouts, anchored to spoken words (source seconds) ---
callout(out(11.0), out(15.3), "office tour", "ORANUSS ACADEMY", side="L")
callout(out(26.4), out(30.6), "wa7da mn ahamm l7wayj", "PERSONAL BRANDING")
callout(out(33.1), out(36.0), "bano b lwjh dyalkom", "SOCIAL MEDIA")
callout(out(36.5), out(40.0), "ynchrou & ypartagiw", "CONTENT · IDEAS")
callout(out(41.7), out(46.0), "7tta bla", "SNAWAT DYAL LKHIBRA", side="L")
callout(out(56.0), out(59.0), "m3a khoya", "HAMZA ORANUSS", side="L")
callout(out(65.0), out(70.2), "hna fach kan9rikom", "DROUS & 7ISAS")

# --- 3 steps as stacked glass cards ---
steps = [(99.6, "1", "Tb3o lvidyouhat chwiya b chwiya"),
         (106.2, "2", "Bano b wjhkom f social media"),
         (111.0, "3", "3awno nnas lokhrin")]
list_end = out(119.5)
for k, (s, n, txt) in enumerate(steps):
    st = out(s); cy = 120 + k * 112
    w = len(txt) * 21 + 160; cx = 80 + w // 2
    glass(10, st, list_end, cx, cy, w, 92, r=22)
    E(14, st + 0.05, list_end, "Shape", f"{{\\an5\\pos({80 + 50},{cy})\\fad(200,220)\\c{NEON}\\1a&H40&\\blur10\\p1}}{circle(62)}{{\\p0}}")
    E(15, st + 0.05, list_end, "Shape", f"{{\\an5\\pos({80 + 50},{cy})\\fad(200,220)\\c{PURPLE}\\bord2\\3c{LAV}\\p1}}{circle(58)}{{\\p0}}")
    E(16, st + 0.08, list_end, "Num", f"{{\\an5\\pos({80 + 50},{cy + 2})\\fad(200,220)}}{n}")
    E(16, st + 0.15, list_end, "Step", f"{{\\an4\\move({80 + 95},{cy},{80 + 110},{cy},0,350)\\fad(250,220)}}{txt}")

# --- big retake cut: neon light flash ---
T = SEG_OUT_START[BIG_CUT_INDEX]
E(20, T - 0.22, T + 0.32, "Shape", f"{{\\an7\\pos(0,0)\\c{PURPLE}\\1a&HFF&\\t(0,200,\\1a&H20&)\\t(260,540,\\1a&HFF&)\\p1}}m 0 0 l 1920 0 l 1920 1080 l 0 1080{{\\p0}}")
E(21, T - 0.18, T + 0.30, "Shape", f"{{\\an5\\pos(960,540)\\c{LAV}\\1a&HFF&\\blur60\\fscx40\\fscy40\\t(0,200,\\1a&H30&\\fscx160\\fscy160)\\t(240,480,\\1a&HFF&\\fscx260\\fscy260)\\p1}}{circle(700)}{{\\p0}}")

# --- end card: dark navy, neon bloom, glass folder ---
TE = TOTAL; E0 = TE - 2.4
E(30, E0, TE, "Shape", f"{{\\an7\\pos(0,0)\\c{INK}\\fad(400,0)\\p1}}m 0 0 l 1920 0 l 1920 1080 l 0 1080{{\\p0}}")
E(31, E0 + 0.1, TE, "Shape", f"{{\\an5\\pos(960,400)\\c{PURPLE}\\1a&H60&\\blur90\\fad(600,0)\\p1}}{circle(760)}{{\\p0}}")
fx, fy = 750, 230  # folder top-left
fold = f"\\fad(350,0)\\move({fx},{fy + 40},{fx},{fy},0,500)"
E(32, E0 + 0.25, TE, "Shape", f"{{\\an7{fold}\\c{PURPLE}\\1a&H30&\\p1}}m 0 24 b 0 8 8 0 24 0 l 140 0 b 156 0 162 6 170 16 l 190 40 l 396 40 b 412 40 420 48 420 64 l 420 300 l 0 300{{\\p0}}")
for k, (dx, rot) in enumerate([(60, 8), (150, -5), (230, 6)]):
    E(33, E0 + 0.45 + k * 0.08, TE, "Shape", f"{{\\an7\\fad(250,0)\\move({fx + dx},{fy + 80},{fx + dx},{fy + 20 + k * 6},0,600)\\frz{rot}\\c{LAV}\\1a&H18&\\bord1\\3c{WHITE}\\p1}}{rrect(150, 190, 14)}{{\\p0}}")
E(34, E0 + 0.25, TE, "Shape", f"{{\\an7{fold}\\c{NEON}\\1a&H60&\\blur20\\p1}}m -10 100 l 450 100 l 430 315 l -10 315{{\\p0}}")
E(35, E0 + 0.25, TE, "Shape", f"{{\\an7{fold}\\c{NEON}\\1a&H58&\\bord2\\3c{LAV}\\3a&H20&\\p1}}m 0 110 l 440 110 b 440 110 440 110 436 120 l 420 300 l 0 300{{\\p0}}")
E(36, E0 + 0.4, TE, "Heavy", f"{{\\an4\\pos({fx + 30},{fy + 255})\\fs34\\fad(300,0)}}ORANUSS")
glow_text(40, E0 + 0.6, TE, "Heavy", "\\an5\\pos(960,640)\\fs96\\fad(350,0)\\fscx90\\t(0,500,\\fscx100)", "ORANUSS ACADEMY")
E(41, E0 + 0.8, TE, "Light", f"{{\\an5\\pos(960,725)\\fs36\\fsp8\\fad(350,0)\\c{LAV}}}PERSONAL BRANDING")

HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Avenir Next Demi Bold,70,&H00FFFFFF,&H00FFFFFF,&H00E02B5B,&H00000000,0,0,0,0,100,100,0,0,3,10,0,2,120,120,80,1
Style: CapHalo,Avenir Next Demi Bold,70,&HFF000000,&HFF000000,&H00200810,&HFF000000,0,0,0,0,100,100,0,0,1,7,0,2,120,120,80,1
Style: Shape,Arial,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Heavy,Avenir Next Heavy,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,4,0,0,0,1
Style: Light,Avenir Next,30,&H00FFC4E0,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,4,0,0,0,1
Style: Num,Avenir Next Heavy,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Step,Avenir Next Demi Bold,42,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,4,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(os.path.join(W, "graphics.ass"), "w", encoding="utf8").write(HEADER + "\n".join(ev) + "\n")

def srt_t(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
os.makedirs(os.path.join(ROOT, "..", "output", "IMG_2399"), exist_ok=True)
with open(os.path.join(ROOT, "..", "output", "IMG_2399", "captions-latin-darija-v2.srt"), "w", encoding="utf8") as f:
    for n, (a, b, t) in enumerate(srt, 1):
        assert b > a
        f.write(f"{n}\n{srt_t(a)} --> {srt_t(b)}\n{t}\n\n")
json.dump([{"start": round(a, 3), "end": round(b, 3), "text": t} for a, b, t in out_words],
          open(os.path.join(W, "captions_words.json"), "w", encoding="utf8"), ensure_ascii=False, indent=0)

# ---------- 4. ffmpeg filter graph ----------
TONEMAP = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
fc = []
fc.append(f"[0:v]{TONEMAP},eq=contrast=1.09:saturation=1.06:gamma=0.96,"
          f"colorbalance=rs=0.03:gs=-0.01:bs=0.06:rh=0.01:bh=0.02,split={len(SEGMENTS)}" + "".join(f"[v{i}]" for i in range(len(SEGMENTS))))
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
# intro: blurred + darkened under the glass title card, easing back to sharp
fc.append("[vc]split[vm][vi]")
fc.append(f"[vi]trim=0:{IN1 + 0.6},setpts=PTS-STARTPTS,gblur=sigma=28,eq=brightness=-0.18:saturation=0.8,"
          f"format=yuva420p,fade=t=out:st={IN1 - 0.3}:d=0.8:alpha=1[vb]")
fc.append("[vm][vb]overlay=eof_action=pass:format=auto[vo]")
fc.append(f"[vo]vignette=angle=PI/4.2:mode=forward,ass='{ass_path}',format=yuv420p[vout]")
fc.append("[ac]highpass=f=80,afftdn=nf=-25:tn=1,equalizer=f=3000:t=q:w=1.2:g=2,"
          "acompressor=threshold=-20dB:ratio=3:attack=10:release=150:makeup=2,"
          "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[aout]")
open(os.path.join(W, "filter.txt"), "w").write(";\n".join(fc))

print(f"segments={len(SEGMENTS)} out_duration={TOTAL:.2f}s words={len(out_words)} chunks={len(chunks)} big_cut_at={SEG_OUT_START[BIG_CUT_INDEX]:.2f}s")
