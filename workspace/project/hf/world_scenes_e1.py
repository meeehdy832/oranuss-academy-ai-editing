# Developed by Mehdi ORANUSS | Powered by Claude
# Storyboard scenes (STORYBOARD-premium-short1.md) for short #1, spliced into gen_entrepreneur1_v5.py.
# Uses the generator's helpers (h, tw, grp, rise, pop, slam, sfx, svg, OUTS, SEGS) and world_kit.

def world(gid, t0, t1, inner, floor=True, beam=True):
    extra = ('<div class="floor"></div>' if floor else '') + ('<div class="beam"></div>' if beam else '')
    grp(gid, t0, t1, f'<div class="world"><div class="rig" id="{gid}r">{extra}{inner}</div></div>')

def cam(gid, t0, t1, frm, to, ease="sine.inOut"):
    tw(f"tl.fromTo('#{gid}r',{frm},{{...{to},duration:{t1 - t0:.3f},ease:'{ease}',immediateRender:false}},{t0:.3f});")

def drift(cls, t0, t1, dy=-120):
    tw(f"tl.fromTo('.{cls}',{{y:0}},{{y:{dy},duration:{t1 - t0:.3f},ease:'none',stagger:{{each:.02,from:'random'}}}},{t0:.3f});")

def scene_no(k, t0, t1):
    g = f"b{k}"
    cr = ('<svg class="crack" width="600" height="140" viewBox="0 0 600 140" fill="none" stroke="#F87171" stroke-width="5" '
          'stroke-linecap="round" filter="drop-shadow(0 0 8px #F87171)">'
          + "".join(f'<path class="crk" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="{d}"/>' for d in (
              "M300 20L250 60L270 90L200 130", "M300 20L350 55L330 85L420 120", "M300 20L300 70L280 140", "M300 20L180 40L120 30", "M300 20L430 35L500 20"))
          + '</svg>')
    world(g, t0, t1 + 0.05, cr + f'<div id="nox" class="ex" style="left:0;right:0;top:640px;text-align:center">لا.</div>'
          + particles("pd", 26, 11, "#F87171", (320, 1000, 760, 1080)), beam=False)
    hit = t0 + 0.62
    tw(f"tl.fromTo('#nox',{{y:-1100,scale:1.15}},{{y:0,scale:1,duration:.32,ease:'power4.in'}},{hit - 0.32:.3f});")
    tw(f"tl.fromTo('#nox',{{scaleY:1}},{{scaleY:.86,duration:.06,yoyo:true,repeat:1,ease:'power2.out',transformOrigin:'50% 100%'}},{hit:.3f});")
    tw(f"tl.to('.crk',{{attr:{{'stroke-dashoffset':0}},duration:.28,stagger:.03,ease:'power2.out'}},{hit:.3f});")
    tw(f"tl.fromTo('.pd',{{scale:0,opacity:1}},{{scale:1.6,opacity:0,y:-160,x:'random(-220,220)',duration:.7,ease:'expo.out'}},{hit:.3f});")
    tw(f"tl.to('#{g}r',{{x:14,duration:.04,yoyo:true,repeat:5,ease:'none'}},{hit:.3f});")
    sfx(hit, "IM-003", -3)

def scene_training(k, t0, t1):
    g = f"b{k}"
    cols = [("#8FB59A", "short"), ("#D8C3A0", "bob"), ("#2F3E66", "short"), ("#EDEDED", "curly"), ("#7FA38B", "bob"), ("#3B4A73", "short")]
    av = ""
    pos = [(200, 900, 170), (455, 900, 170), (710, 900, 170), (110, 1050, 215), (432, 1050, 215), (755, 1050, 215)]
    for i, ((c, hk), (x, y, w)) in enumerate(zip(cols, pos)):
        av += f'<div class="tr{" keep" if i in (1, 4) else " drop"}" id="tr{i}" style="left:{x}px;top:{y}px">{avatar(c, w=w, hair_kind=hk)}</div>'
    stage = ('<div style="left:300px;top:840px;width:480px;height:90px;border-radius:50%;background:radial-gradient(ellipse,rgba(46,229,157,.45),rgba(46,229,157,0) 70%)"></div>')
    world(g, t0, t1, stage + f'<div id="ytr" style="left:440px;top:420px">{youssef("talk", w=200)}</div>' + av
          + particles("pk", 16, 5, "#2EE59D", (150, 700, 950, 1100)))
    cam(g, t0, t1, "{rotationY:-7,z:-60}", "{rotationY:6,z:40}")
    rise("#ytr", t0, 40, 0.5)
    tw(f"tl.from('.tr',{{y:60,opacity:0,duration:.45,stagger:.05,ease:'expo.out'}},{t0 + 0.1:.3f});")
    tw(f"tl.to('.tr.drop',{{filter:'grayscale(1) brightness(.55)',y:46,opacity:.5,duration:.5,stagger:.12,ease:'power2.inOut'}},{t0 + 1.0:.3f});")
    tw(f"tl.to('.tr.keep',{{filter:'drop-shadow(0 0 26px #2EE59D)',duration:.4}},{t0 + 1.0:.3f});")
    drift("pk", t0, t1, -90)
    sfx(t0 + 1.0, "PO-016", -10)

def scene_stress(k, t0, t1):
    g = f"b{k}"
    papers = "".join(f'<div class="paper pp" id="pp{i}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)"></div>'
                     for i, (x, y, r) in enumerate(((180, 1000, -14), (300, 960, 8), (720, 990, 12), (820, 950, -6), (250, 900, 20), (760, 900, -18), (520, 860, 4))))
    inner = ('<div class="lampglow" id="lg" style="left:-60px;top:220px"></div>'
             f'<div id="ys" style="left:410px;top:560px">{youssef("headhands", w=260)}</div>'
             '<div class="desk" style="left:120px;top:1110px;width:840px"></div>'
             '<div style="left:120px;top:1150px;width:840px;height:300px;background:linear-gradient(180deg,#2a1b10,#0a0705)"></div>'
             + papers + '<div id="ph" style="left:640px;top:1060px;width:90px;height:48px;border-radius:10px;background:#0b1512;border:3px solid #2EE59D"></div>')
    world(g, t0, t1, inner, floor=False, beam=False)
    cam(g, t0, t1, "{scale:1,rotation:0}", "{scale:1.12,rotation:2}")
    tw(f"tl.from('.pp',{{y:-1200,rotation:'random(-40,40)',duration:.5,stagger:.18,ease:'power3.in'}},{t0 + 0.05:.3f});")
    tw(f"tl.to('#ph',{{x:5,duration:.04,yoyo:true,repeat:21,ease:'none'}},{t0 + 0.6:.3f});")
    tw(f"tl.to('#lg',{{opacity:.25,duration:.05,yoyo:true,repeat:3}},{t0 + 1.2:.3f});")
    tw(f"tl.to('#lg',{{background:'radial-gradient(circle,rgba(248,113,113,.5),rgba(248,113,113,0) 65%)',duration:1.2}},{t0 + 0.8:.3f});")
    tw(f"tl.to('#ys',{{y:6,duration:.12,yoyo:true,repeat:7,ease:'sine.inOut'}},{t0 + 0.5:.3f});")
    sfx(t0 + 0.3, "PO-006", -12); sfx(t0 + 0.9, "PO-006", -12)

def scene_buy(k, t0, t1):
    g = f"b{k}"
    c1, c2 = t0 + 1.05, t0 + 2.35
    inner = (f'<div id="yb1" style="left:410px;top:560px">{youssef("stand", w=260)}</div>'
             f'<div id="yb2" style="left:410px;top:560px;opacity:0">{youssef("reach", w=260)}</div>'
             + f'<div style="left:40px;top:640px">{holo("cash", "hc")}</div>'
             + f'<div style="left:800px;top:600px">{holo("car", "hv", 210)}</div>'
             + f'<div style="left:425px;top:250px">{holo("house", "hh")}</div>'
             + particles("pb", 22, 9, "#FFC15E", (60, 300, 1020, 1100)))
    world(g, t0, t1, inner)
    cam(g, t0, t1, "{rotationY:10,z:-80}", "{rotationY:-8,z:30}")
    for sel, t in (("#hc", t0 + 0.05), ("#hv", c1), ("#hh", c2)):
        tw(f"tl.fromTo('{sel}',{{scale:0,opacity:0,rotationY:-90}},{{scale:1,opacity:1,rotationY:0,duration:.55,ease:'back.out(1.6)'}},{t:.3f});")
        tw(f"tl.to('{sel} svg',{{y:-14,duration:1.2,yoyo:true,repeat:1,ease:'sine.inOut'}},{t + 0.5:.3f});")
        sfx(t, "PO-022", -8)
    tw(f"tl.set('#yb1',{{opacity:0}},{c1 + 0.2:.3f});tl.set('#yb2',{{opacity:1}},{c1 + 0.2:.3f});")
    tw(f"tl.to('.holo',{{skewX:18,opacity:.2,duration:.05,yoyo:true,repeat:5}},{t1 - 0.45:.3f});")
    drift("pb", t0, t1, -140)

def scene_night(k, t0, t1):
    g = f"b{k}"
    inner = ('<div class="win" id="wn"><div class="sky"></div>'
             '<div class="moon" style="left:620px;top:90px"></div>'
             f'<div id="sk" style="left:-120px;top:40px;width:1300px;height:900px">{skyline()}</div><div class="mull"></div></div>'
             '<div class="lampglow" id="lg2" style="left:640px;top:880px"></div>'
             f'<div id="yn" style="left:390px;top:860px">{youssef("write", w=300, back=True, legs=False)}</div>'
             '<div class="desk" style="left:60px;top:1210px;width:960px"></div>'
             '<div style="left:60px;top:1250px;width:960px;height:300px;background:linear-gradient(180deg,#24170d,#070504)"></div>')
    world(g, t0, t1, inner, floor=False, beam=False)
    cam(g, t0, t1, "{scale:1.4,y:120}", "{scale:1,y:0}", "power2.out")
    tw(f"tl.fromTo('#sk',{{x:0}},{{x:-60,duration:{t1 - t0:.3f},ease:'none'}},{t0:.3f});")
    tw(f"tl.to('#sk .bld i',{{opacity:'random(.2,1)',duration:.3,stagger:{{each:.01,from:'random'}},repeat:1,yoyo:true}},{t0 + 0.3:.3f});")

def scene_climb_team(k, t0, t1, t2):
    """k = climb beat; team beat runs t1→t2 in the same world."""
    g = f"b{k}"
    steps = ""
    S = [(60 + i * 180, 1260 - i * 150) for i in range(5)]
    for i, (x, y) in enumerate(S):
        steps += f'<div class="step" id="st{i}" style="left:{x}px;top:{y}px"><div class="top"></div><div class="front"></div></div>'
    probs = (f'<div class="prob" id="pr1" style="left:{S[2][0] + 180}px;top:{S[2][1] - 96}px">{svg("x", 50, 3)}</div>'
             f'<div class="prob" id="pr2" style="left:{S[3][0] + 160}px;top:{S[3][1] - 96}px">{svg("x", 50, 3)}</div>')
    team = (f'<div class="tm" id="tm0" style="left:{S[4][0] - 150}px;top:{S[4][1] - 250}px">{avatar("#E0A93B", skin="#C99272", hair="#2A1A10", back=False, w=150, hair_kind="bob")}</div>'
            f'<div class="tm" id="tm1" style="left:{S[4][0] + 250}px;top:{S[4][1] - 250}px">{avatar("#8A9099", skin="#B57C58", back=False, w=150)}</div>'
            f'<div class="tm" id="tm2" style="left:{S[4][0] + 60}px;top:{S[4][1] - 420}px">{avatar("#6E7B4F", skin="#A8704F", back=False, w=150, hair_kind="curly")}</div>')
    links = "".join(f'<div class="link" id="lk{i}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({r}deg)"></div>'
                    for i, (x, y, w, r) in enumerate(((S[4][0] + 20, S[4][1] - 170, 150, 180), (S[4][0] + 180, S[4][1] - 170, 120, 0), (S[4][0] + 140, S[4][1] - 330, 110, 90))))
    yw = f'<div id="yw" style="left:{S[0][0] + 85}px;top:{S[0][1] - 270}px">{youssef("stand", w=135)}</div>'
    world(g, t0, t2, steps + probs + links + team + yw + particles("pc", 24, 13, "#A7F3D0", (0, 200, 1080, 1300)))
    cam(g, t0, t2, "{z:120,y:-60,rotationX:6}", "{z:-120,y:80,rotationX:0}")
    tw(f"tl.from('.step',{{y:200,opacity:0,duration:.5,stagger:.08,ease:'expo.out'}},{t0:.3f});")
    # Youssef walks up step by step (hop over the problems)
    d = (t1 - t0 - 0.4) / 4
    for i in range(1, 5):
        x, y = S[i][0] + 85, S[i][1] - 270
        tw(f"tl.to('#yw',{{left:{x},top:{y - 40},duration:{d * 0.5:.3f},ease:'power2.out'}},{t0 + 0.3 + (i - 1) * d:.3f});")
        tw(f"tl.to('#yw',{{top:{y},duration:{d * 0.5:.3f},ease:'bounce.out'}},{t0 + 0.3 + (i - 0.5) * d:.3f});")
    tw(f"tl.to('#yw .legL',{{rotation:14,transformOrigin:'84px 232px',duration:.18,yoyo:true,repeat:{int((t1 - t0) / 0.18)},ease:'sine.inOut'}},{t0 + 0.3:.3f});")
    tw(f"tl.to('#yw .legR',{{rotation:-14,transformOrigin:'116px 232px',duration:.18,yoyo:true,repeat:{int((t1 - t0) / 0.18)},ease:'sine.inOut'}},{t0 + 0.3:.3f});")
    for j, t in ((1, t0 + 0.45), (2, t0 + 1.25)):
        pop(f"#pr{j}", t, 0.3, 0.4); sfx(t, "IM-003", -12)
        tw(f"tl.to('#pr{j}',{{scale:0,opacity:0,rotation:40,duration:.3}},{t + 0.9:.3f});")
    # team arrives (t1 → t2)
    tw(f"tl.from('.tm',{{scale:0,opacity:0,duration:.5,stagger:.35,ease:'back.out(1.8)'}},{t1 + 0.1:.3f});")
    tw(f"tl.from('.link',{{scaleX:0,duration:.4,stagger:.35}},{t1 + 0.4:.3f});")
    tw(f"tl.to('.step .front',{{boxShadow:'0 0 60px rgba(46,229,157,.8)',duration:.5}},{t1 + 0.3:.3f});")
    for i in range(3):
        sfx(t1 + 0.1 + i * 0.35, "PO-006", -9)
    drift("pc", t0, t2, -160)
