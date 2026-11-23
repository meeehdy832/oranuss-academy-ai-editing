# Developed by Mehdi ORANUSS | Powered by Claude
"""2.5D "world" kit for HyperFrames shorts: SVG character Youssef (one identity, several poses), trainee/team
avatars, hologram objects, city skyline, glowing stairs, particles and a perspective floor. Pure HTML/SVG/CSS,
animated by GSAP from the generator (no AI images or video).
Identity (keep fixed): Moroccan man ~28, short black wavy hair side part, short trimmed beard, warm light-brown skin,
white open-collar shirt sleeves rolled, navy chinos, white sneakers, brown leather watch on his left wrist."""
import random

SKIN, SKIN_D, HAIR, SHIRT, SHIRT_D, PANTS, PANTS_D = "#C68B63", "#9A6644", "#17110D", "#FFFFFF", "#D3E2DB", "#26355A", "#121A30"

DEFS = f"""<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="gSkin" x1="0" x2="1"><stop offset="0" stop-color="{SKIN}"/><stop offset="1" stop-color="{SKIN_D}"/></linearGradient>
<linearGradient id="gShirt" x1="0" x2="1"><stop offset="0" stop-color="{SHIRT}"/><stop offset="1" stop-color="{SHIRT_D}"/></linearGradient>
<linearGradient id="gPants" x1="0" x2="1"><stop offset="0" stop-color="{PANTS}"/><stop offset="1" stop-color="{PANTS_D}"/></linearGradient>
<radialGradient id="gHolo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFC15E" stop-opacity=".35"/><stop offset="1" stop-color="#FFC15E" stop-opacity="0"/></radialGradient>
</defs></svg>"""

# arm polylines (shoulder → elbow → hand) per pose, in the 200×400 body box
ARMS = {
    "stand": [((64, 140), (52, 198), (58, 250)), ((136, 140), (148, 198), (142, 250))],
    "talk": [((64, 140), (50, 196), (78, 214)), ((136, 140), (160, 180), (176, 132))],
    "headhands": [((64, 140), (34, 150), (74, 74)), ((136, 140), (166, 150), (126, 74))],
    "reach": [((64, 140), (52, 198), (58, 250)), ((136, 140), (168, 104), (192, 62))],
    "write": [((64, 140), (60, 196), (96, 222)), ((136, 140), (146, 196), (118, 224))],
}

def _arm(pts, watch=False):
    (sx, sy), (ex, ey), (hx, hy) = pts
    w = (f'<rect x="{hx - 9 + (ex - hx) * .18:.0f}" y="{hy - 6 + (ey - hy) * .18:.0f}" width="18" height="10" rx="3" fill="#6B3E1F"/>'
         if watch else "")
    return (f'<path d="M{sx} {sy}L{ex} {ey}" stroke="url(#gShirt)" stroke-width="30" stroke-linecap="round"/>'
            f'<path d="M{ex} {ey}L{hx} {hy}" stroke="url(#gSkin)" stroke-width="21" stroke-linecap="round"/>{w}'
            f'<circle cx="{hx}" cy="{hy}" r="12" fill="url(#gSkin)"/>')

def youssef(pose="stand", cid="", w=260, back=False, legs=True):
    """Full-body Youssef (viewBox 200×400). back=True draws him from behind (hair, no face)."""
    arms = ARMS.get(pose, ARMS["stand"])
    head_dy = 10 if pose == "headhands" else 0
    leg = (f'<g class="legL"><path d="M84 232L80 362" stroke="url(#gPants)" stroke-width="30" stroke-linecap="round"/>'
           f'<ellipse cx="78" cy="374" rx="20" ry="9" fill="#F4F7F5"/></g>'
           f'<g class="legR"><path d="M116 232L120 362" stroke="url(#gPants)" stroke-width="30" stroke-linecap="round"/>'
           f'<ellipse cx="122" cy="374" rx="20" ry="9" fill="#F4F7F5"/></g>') if legs else ""
    torso = ('<path d="M60 132Q100 116 140 132L146 238Q100 248 54 238Z" fill="url(#gShirt)"/>'
             '<path d="M58 228Q100 240 142 228L146 246Q100 256 54 246Z" fill="url(#gPants)"/>')
    collar = "" if back else '<path d="M88 124L100 146L112 124Z" fill="url(#gSkin)"/><path d="M86 122L100 140L94 124ZM114 122L100 140L106 124Z" fill="#E9F1ED"/>'
    if back:
        head = (f'<g transform="translate(0 {head_dy})"><rect x="90" y="104" width="20" height="22" fill="url(#gSkin)"/>'
                f'<ellipse cx="100" cy="76" rx="34" ry="40" fill="{HAIR}"/><ellipse cx="66" cy="82" rx="6" ry="9" fill="url(#gSkin)"/>'
                f'<ellipse cx="134" cy="82" rx="6" ry="9" fill="url(#gSkin)"/></g>')
    else:
        head = (f'<g transform="translate(0 {head_dy})"><rect x="90" y="104" width="20" height="22" fill="url(#gSkin)"/>'
                f'<ellipse cx="66" cy="82" rx="6" ry="9" fill="{SKIN_D}"/><ellipse cx="134" cy="82" rx="6" ry="9" fill="{SKIN_D}"/>'
                f'<ellipse cx="100" cy="78" rx="34" ry="40" fill="url(#gSkin)"/>'
                f'<path d="M68 92Q72 120 100 122Q128 120 132 92Q128 108 100 110Q72 108 68 92Z" fill="{HAIR}" opacity=".88"/>'
                f'<path d="M86 100Q100 106 114 100" stroke="{HAIR}" stroke-width="5" fill="none" stroke-linecap="round"/>'
                f'<path d="M64 70Q62 30 100 34Q140 32 136 68Q130 50 112 50Q118 44 108 40Q96 52 74 52Q66 58 64 70Z" fill="{HAIR}"/>'
                f'<ellipse cx="86" cy="80" rx="4" ry="5" fill="#1B1210"/><ellipse cx="114" cy="80" rx="4" ry="5" fill="#1B1210"/>'
                f'<path d="M78 68L94 66M106 66L122 68" stroke="{HAIR}" stroke-width="4" stroke-linecap="round"/></g>')
    a_l, a_r = _arm(arms[0]), _arm(arms[1], watch=True)
    # hands in front of the face only for headhands
    body = (leg + torso + collar + a_l + a_r + head) if pose != "headhands" else (leg + torso + collar + head + a_l + a_r)
    return (f'<svg {f"id=\"{cid}\" " if cid else ""}class="yz" width="{w}" height="{w * 2}" viewBox="0 0 200 400" '
            f'style="overflow:visible">{body}</svg>')

def avatar(color, skin="#B98260", hair="#1C1410", back=True, w=150, cid="", hair_kind="short"):
    """Bust avatar (viewBox 120×150): trainees and team. back=True shows the back of the head."""
    hb = {"short": f'<ellipse cx="60" cy="44" rx="30" ry="32" fill="{hair}"/>',
          "bob": f'<path d="M26 56Q24 14 60 12Q96 14 94 56L94 70Q60 60 26 70Z" fill="{hair}"/>',
          "curly": "".join(f'<circle cx="{x}" cy="{y}" r="11" fill="{hair}"/>' for x, y in ((38, 30), (52, 20), (68, 20), (82, 30), (86, 46), (34, 46)))}[hair_kind]
    face = "" if back else (f'<ellipse cx="60" cy="52" rx="26" ry="30" fill="{skin}"/>'
                             f'<ellipse cx="51" cy="54" rx="3" ry="4" fill="#1B1210"/><ellipse cx="69" cy="54" rx="3" ry="4" fill="#1B1210"/>'
                             f'<path d="M52 68Q60 73 68 68" stroke="#5a3523" stroke-width="3" fill="none" stroke-linecap="round"/>')
    top = hb if back else (face + hb.replace('cy="44"', 'cy="34"').replace('ry="32"', 'ry="18"') if hair_kind == "short" else face + hb)
    return (f'<svg {f"id=\"{cid}\" " if cid else ""}class="av" width="{w}" height="{w * 1.25:.0f}" viewBox="0 0 120 150">'
            f'<path d="M14 150Q14 96 60 92Q106 96 106 150Z" fill="{color}"/><rect x="52" y="76" width="16" height="20" fill="{skin}"/>{top}</svg>')

HOLO = {
    "car": '<path d="M10 62l12-26h56l12 26v18H10z"/><circle cx="30" cy="80" r="9"/><circle cx="70" cy="80" r="9"/><path d="M26 36l8-16h32l8 16"/>',
    "house": '<path d="M10 50L50 16l40 34"/><path d="M18 44v44h64V44"/><path d="M42 88V64h16v24"/><path d="M26 56h10v10H26zM64 56h10v10H64z"/>',
    "cash": '<rect x="8" y="26" width="84" height="48" rx="6"/><circle cx="50" cy="50" r="13"/><path d="M8 40h12M80 60h12"/><rect x="14" y="18" width="84" height="48" rx="6" opacity=".45"/>',
}
def holo(kind, cid, w=230):
    return (f'<div class="holo" id="{cid}"><svg width="{w}" height="{w}" viewBox="0 0 100 100" fill="none" stroke="#FFC15E" '
            f'stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">{HOLO[kind]}</svg><div class="scan"></div>'
            f'<div class="ped"></div></div>')

def skyline(seed=7, width=1300, base=820):
    rnd = random.Random(seed); x, out = 0, []
    while x < width:
        bw, bh = rnd.randint(60, 130), rnd.randint(180, 620)
        wins = "".join(f'<i style="left:{rnd.randint(8, bw - 16)}px;top:{rnd.randint(12, bh - 20)}px;opacity:{rnd.choice((.25, .5, .9))}"></i>'
                       for _ in range(bh // 26))
        out.append(f'<div class="bld" style="left:{x}px;top:{base - bh}px;width:{bw}px;height:{bh}px">{wins}</div>')
        x += bw + rnd.randint(4, 18)
    return "".join(out)

def particles(pid, n=34, seed=3, color="#A7F3D0", area=(0, 0, 1080, 1920)):
    rnd = random.Random(seed)
    return "".join(f'<i class="pt {pid}" style="left:{rnd.randint(area[0], area[2])}px;top:{rnd.randint(area[1], area[3])}px;'
                   f'width:{(s := rnd.choice((3, 4, 6, 8)))}px;height:{s}px;background:{color};opacity:{rnd.uniform(.25, .8):.2f}"></i>'
                   for _ in range(n))

CSS = """
.world{position:absolute;inset:0;overflow:hidden;perspective:1400px;background:radial-gradient(circle at 50% 38%,#12432F 0%,#0A2A1F 42%,#03100B 90%)}
.rig{position:absolute;inset:0;transform-style:preserve-3d;transform-origin:50% 60%}
.world div,.world svg{position:absolute}
.floor{left:-540px;top:1120px;width:2160px;height:1700px;transform:rotateX(76deg);transform-origin:50% 0;
  background:radial-gradient(ellipse at 50% 0%,rgba(46,229,157,.28),rgba(5,20,15,0) 60%),
  repeating-linear-gradient(0deg,rgba(167,243,208,.12) 0 2px,transparent 2px 110px),repeating-linear-gradient(90deg,rgba(167,243,208,.12) 0 2px,transparent 2px 110px)}
.beam{width:700px;height:1500px;left:190px;top:-200px;background:linear-gradient(180deg,rgba(167,243,208,.22),rgba(167,243,208,0));clip-path:polygon(42% 0,58% 0,100% 100%,0 100%);filter:blur(6px)}
.pt{position:absolute;border-radius:50%;box-shadow:0 0 10px currentColor}
.yz{filter:drop-shadow(0 30px 30px rgba(0,0,0,.55)) drop-shadow(0 0 22px rgba(167,243,208,.18))}
.av{filter:drop-shadow(0 16px 20px rgba(0,0,0,.5))}
.holo{width:230px;height:300px}
.holo svg{left:0;top:0;filter:drop-shadow(0 0 12px #FFC15E) drop-shadow(0 0 30px rgba(255,193,94,.6))}
.holo .scan{left:0;top:0;width:230px;height:230px;background:repeating-linear-gradient(0deg,rgba(255,193,94,.16) 0 3px,transparent 3px 9px);mix-blend-mode:screen;
  -webkit-mask:radial-gradient(circle,#000 55%,transparent 72%)}
.holo .ped{left:25px;top:240px;width:180px;height:44px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,193,94,.55),rgba(255,193,94,0) 70%);
  border:2px solid rgba(255,193,94,.5)}
.bld{background:linear-gradient(180deg,#0E2A2A,#071512);border-top:2px solid rgba(167,243,208,.25)}
.bld i{position:absolute;width:8px;height:12px;background:#FFD27A;box-shadow:0 0 6px #FFB347}
.win{left:90px;top:330px;width:900px;height:900px;border:26px solid #0B1F18;border-radius:18px;overflow:hidden;
  box-shadow:inset 0 0 120px rgba(0,0,0,.7),0 0 0 2px rgba(167,243,208,.2)}
.win .mull{left:424px;top:0;width:26px;height:100%;background:#0B1F18}
.sky{left:0;top:0;width:900px;height:900px;background:linear-gradient(180deg,#041019 0%,#0B2A3A 55%,#123C3A 100%)}
.moon{width:120px;height:120px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#F4FFF9,#A7F3D0);box-shadow:0 0 60px #A7F3D0}
.desk{height:40px;border-radius:10px;background:linear-gradient(180deg,#5A3B26,#3A2617);box-shadow:0 20px 40px rgba(0,0,0,.6)}
.lampglow{width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(255,200,120,.55),rgba(255,200,120,0) 65%)}
.paper{width:150px;height:190px;border-radius:12px;background:#F2F6F4;box-shadow:0 14px 30px rgba(0,0,0,.45)}
.paper::before{content:"";position:absolute;left:20px;right:20px;top:30px;height:70%;background:repeating-linear-gradient(180deg,#C9D6D0 0 6px,transparent 6px 20px)}
.step{width:300px;height:90px;transform-style:preserve-3d}
.step .top{left:0;top:0;width:300px;height:120px;background:linear-gradient(180deg,#1E6B4F,#0E3B2C);transform:rotateX(80deg);transform-origin:50% 0;border:2px solid rgba(46,229,157,.6)}
.step .front{left:0;top:0;width:300px;height:90px;background:linear-gradient(180deg,#0E9F6E,#0A5E43);border:2px solid rgba(167,243,208,.5);box-shadow:0 0 30px rgba(46,229,157,.35)}
.prob{width:86px;height:86px;border-radius:18px;background:#9b2c2c;border:3px solid #F87171;box-shadow:0 0 30px rgba(248,113,113,.7);display:flex;align-items:center;justify-content:center}
.link{height:4px;background:#2EE59D;box-shadow:0 0 14px #2EE59D;transform-origin:0 50%}
.ring{left:540px;top:1000px;width:0;height:0;transform-style:preserve-3d}
.ring .slot{transform-style:preserve-3d}
.crack{left:240px;top:1040px}
.ex{color:#F87171;font:900 330px/1 GA;text-shadow:0 2px 0 #c94b4b,0 4px 0 #b84141,0 6px 0 #a63838,0 8px 0 #942f2f,0 10px 0 #822626,0 12px 0 #701d1d,0 14px 0 #5e1515,0 30px 60px rgba(0,0,0,.7),0 0 80px rgba(248,113,113,.6)}
"""
