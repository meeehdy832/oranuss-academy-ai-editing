import React from "react";
import { AbsoluteFill, interpolateColors, useCurrentFrame } from "remotion";
import {
  FONT,
  CamMove, CameraRig, ClickRing, Decode, DriftBlob, EASE_PRO, FieldCfg, FontSpec, LiquidIn, MacCursor, MotionBlur, Move, PixelGather, RingDraw, Stage,
  StackLines, SwapLine, TypeLine, WaveNumber, WheelPicker, WordIn, aeEase, camState, clamp01, collapseOut, emergeIn, fieldGeom, layoutLine, lerp,
  pressScale, prog, snapIn, springFollow, useFontsReady,
} from "../motion-pro";

/*
 * ProDemo v3 ("Orbit"): rebuilt on the pro-vs-AI comparison (dnyxstudios Wallet reel, v12).
 * - real shutter motion blur (MotionBlur), no gaussian layer smears
 * - every hold keeps a visible push (0.2-0.6 % zoom per frame), background blobs always move
 * - transitions overlap: collapse -> emerge, a MATCH CUT (notification icon -> stats ring),
 *   zoom-through with a gradual light -> dark background (no flash, no solid frames)
 * - key moments on a 30f beat grid; numbers wave per character; decode uses letters only;
 *   a 3D wheel picker with a focus plane; the logo stays alive and becomes the end card.
 * 1080x1080 @30fps, 540f. inputProps.mb = motion-blur samples (1 for drafts).
 */

const BLUE = "#0A84FF";
const INK = "#111111";
const LIGHT = "#F7F8FA";
const TINT = "#D6E5FF";
const NAVY = "#060B16";
const SHADOW = "0 40px 80px -30px rgba(0,0,0,.20), 0 14px 28px -14px rgba(0,0,0,.10)";
export const PRO_DEMO_DURATION = 540;

// ---- beat grid (30f) ----
const COLLAPSE = 52; // hook collapses into a point...
const FIELD: FieldCfg = {
  at: 57, // ...and the bar emerges from it 4f before the hook is gone
  start: 63,
  text: "plan my week around the gym",
  cpf: 0.9,
  font: { family: FONT.ui, size: 36, weight: 500, letterSpacing: -0.01 },
  from: { w: 26, h: 26 },
  minW: 560,
  h: 104,
  padL: 92,
  padR: 100,
  omega: 0.3,
  zeta: 0.78,
};
const CLICK = 120; // beat 4
const MORPH = 122;
const NOTIF = 180; // beat 6
const MC = 200; // match-cut push starts
const CUT = 236; // notification icon -> stats ring
const ODO = 270; // beat 9
const DARK0 = 300; // beat 10: zoom-through + background darkens
const DCUT = 324;
const WHEEL1 = 360; // beat 12
const WHEEL2 = 386;
const LCOLL = 412; // statement collapses into the logo point
const LOGO = 418;
const SWAP = 468;
const ECOLL = 498; // logo collapses into the end card
const END = 505;

// ---- world colour: tint -> light, then light -> navy during the zoom-through (gradual, no flash) ----
// dusk starts during the stats hold and finishes after the cut: ~58f, so no frame jumps more than the pro's transitions
const darkness = (f: number) => EASE_PRO.drift(clamp01((f - (DARK0 - 14)) / 58));
// light -> navy THROUGH blue (a straight light -> navy blend passes through a muddy gray)
const bgAt = (f: number) =>
  darkness(f) <= 0
    ? interpolateColors(EASE_PRO.enter(clamp01(f / 26)), [0, 1], [TINT, LIGHT])
    : interpolateColors(darkness(f), [0, 0.35, 0.7, 1], [LIGHT, "#A9C8FF", "#1E3F9E", NAVY]);

// ---- type ----
const HOOK_F: FontSpec = { family: FONT.ui, size: 66, weight: 600, letterSpacing: -0.035 };
const HLH = 86;
const DARK_F: FontSpec = { family: FONT.ui, size: 76, weight: 600, letterSpacing: -0.035 };

const Ring: React.FC<{ d: number; thick: number; p?: number }> = ({ d, thick, p = 1 }) => {
  const mask = `radial-gradient(circle, transparent ${d / 2 - thick - 0.5}px, black ${d / 2 - thick}px)`;
  return (
    <div style={{ width: d, height: d, borderRadius: d, background: `conic-gradient(from -90deg, #0A84FF, #34C759 ${p * 0.35 * 100}%, #FFD60A ${p * 0.7 * 100}%, #FF9F0A ${p * 100}%, #E5E5EA ${p * 100}%)`,
      maskImage: mask, WebkitMaskImage: mask }} />
  );
};
const SendBtn: React.FC<{ s: number }> = ({ s }) => (
  <div style={{ width: 72, height: 72, borderRadius: 72, background: INK, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${s})` }}>
    <svg width="30" height="30" viewBox="0 0 24 24"><path d="M12 19V5M5.5 11.5 12 5l6.5 6.5" stroke="#fff" strokeWidth="2.6" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
  </div>
);

/* ---------------- HOOK ---------------- */
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame > COLLAPSE + 16) return null;
  const A = layoutLine("your week by", HOOK_F);
  const handW = layoutLine("hand?", HOOK_F).W;
  const gap = HOOK_F.size * 0.26;
  const rowW = A.W + gap + handW;
  const handBox = { x: rowW / 2 - handW / 2, y: HLH / 2, w: handW, h: HOOK_F.size * 0.8 };
  return (
    <Stage keys={collapseOut(COLLAPSE, 12)}>
      <StackLines lineH={HLH} dur={16} lines={[
        { at: 0, node: (
          <div style={{ display: "flex", gap, alignItems: "center" }}>
            <LiquidIn text="Still" start={-3} font={HOOK_F} ink={INK} accent={BLUE} dur={16} />
            <span style={{ fontFamily: HOOK_F.family, fontSize: HOOK_F.size, fontWeight: 600, letterSpacing: "-0.035em", lineHeight: `${HLH}px` }}>
              <Decode text="planning" start={7} dur={8} ink={INK} />
            </span>
          </div>
        ) },
        { at: 18, node: (
          <div style={{ display: "flex", gap, alignItems: "center" }}>
            <WordIn text="your week by" start={18} every={3} font={HOOK_F} ink={INK} />
            <WordIn text="hand?" start={31} font={HOOK_F} ink={INK} accent={BLUE} keep={[0]} dur={18} />
          </div>
        ) },
      ]} />
      <PixelGather at={19} box={handBox} count={16} cell={20} colors={[BLUE, "#5AC8FA", "#0040DD", "#9BD1FF"]} dur={16} spread={150} />
    </Stage>
  );
};

/* ---------------- BAR -> CARD (one object) ---------------- */
const CARD = { w: 820, h: 620, r: 48 };
const cardGeo = (f: number) => {
  const fg = fieldGeom(MORPH - 1, FIELD);
  const w = springFollow(f, (g) => (g < MORPH ? fg.w : CARD.w), MORPH - 1, 0.24, 0.74);
  const h = springFollow(f, (g) => (g < MORPH ? fg.h : CARD.h), MORPH - 1, 0.26, 0.74);
  const k = clamp01((h - FIELD.h) / (CARD.h - FIELD.h));
  return { w, h, r: lerp(h / 2, CARD.r, clamp01(k * 3)), k };
};

type Ev = { d: number; s: number; l: number; c: string; t: string };
const EVENTS: Ev[] = [
  { d: 0, s: 0.05, l: 0.18, c: "#34C759", t: "Gym" }, { d: 0, s: 0.36, l: 0.26, c: "#0A84FF", t: "Design review" },
  { d: 1, s: 0.18, l: 0.2, c: "#FF9F0A", t: "Lunch w/ Sara" }, { d: 1, s: 0.55, l: 0.3, c: "#AF52DE", t: "Deep work" },
  { d: 2, s: 0.05, l: 0.18, c: "#34C759", t: "Gym" }, { d: 2, s: 0.4, l: 0.22, c: "#0A84FF", t: "Standup" },
  { d: 3, s: 0.25, l: 0.34, c: "#AF52DE", t: "Deep work" }, { d: 3, s: 0.7, l: 0.16, c: "#FF9F0A", t: "Call mom" },
  { d: 4, s: 0.05, l: 0.18, c: "#34C759", t: "Gym" }, { d: 4, s: 0.45, l: 0.24, c: "#0A84FF", t: "Ship v2" },
];
const RANK = EVENTS.map((e, i) => ({ i, k: e.d + e.s * 3 })).sort((a, b) => a.k - b.k).reduce<Record<number, number>>((m, o, r) => ((m[o.i] = r), m), {});

const Calendar: React.FC = () => {
  const frame = useCurrentFrame();
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri"];
  const colW = 148;
  const gridH = 430;
  return (
    <div style={{ position: "absolute", left: "50%", top: "50%", width: CARD.w, height: CARD.h, marginLeft: -CARD.w / 2, marginTop: -CARD.h / 2, padding: "44px 40px", boxSizing: "border-box", fontFamily: FONT.ui }}>
      <div style={{ display: "flex", alignItems: "flex-end", gap: 16, height: 56 }}>
        <WordIn text="This week" start={MORPH + 4} every={3} font={{ family: FONT.ui, size: 44, weight: 700, letterSpacing: -0.03 }} ink={INK} />
        <WordIn text="planned by Orbit" start={MORPH + 12} every={2} dur={16} font={{ family: FONT.ui, size: 26, weight: 500 }} ink={BLUE} style={{ marginBottom: 6 }} />
      </div>
      <div style={{ position: "relative", marginTop: 26, height: gridH + 40 }}>
        {days.map((d, i) => {
          const t = EASE_PRO.enterSnap(clamp01((frame - MORPH - 6 - i * 2) / 16));
          return <div key={d} style={{ position: "absolute", left: i * colW, top: 0, fontSize: 22, fontWeight: 600, color: "#8E8E93", opacity: t, transform: `translateY(${(1 - t) * 12}px)` }}>{d}</div>;
        })}
        {EVENTS.map((e, i) => {
          const at = MORPH + 12 + RANK[i] * 2.5; // diagonal order
          const t = EASE_PRO.enterSnap(clamp01((frame - at) / 18));
          const o = clamp01((frame - at) / 5);
          return (
            <div key={i} style={{ position: "absolute", left: e.d * colW, top: 40 + e.s * gridH, width: colW - 12, height: e.l * gridH, borderRadius: 14, background: e.c + "26",
              borderLeft: `5px solid ${e.c}`, opacity: o, transform: `scale(${0.9 + 0.1 * t})`, transformOrigin: "0% 0%", filter: t < 0.8 ? `blur(${(1 - t / 0.8) * 6}px)` : undefined,
              padding: "8px 10px", boxSizing: "border-box", fontSize: 21, fontWeight: 600, color: e.c, overflow: "hidden" }}>
              {e.t}
            </div>
          );
        })}
      </div>
    </div>
  );
};

const HeroObject: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < FIELD.at) return null;
  const fg = fieldGeom(frame, FIELD);
  const cg = frame >= MORPH ? cardGeo(frame) : null;
  const w = cg ? cg.w : fg.w;
  const h = cg ? cg.h : fg.h;
  const r = cg ? cg.r : fg.r;
  const grow = fg.grow;
  const bg = interpolateColors(clamp01(grow * 1.6), [0, 1], [BLUE, "#FFFFFF"]);
  const fieldOp = clamp01((grow - 0.4) / 0.35) * (1 - clamp01((frame - MORPH) / 4));
  const n = frame < FIELD.start ? 0 : Math.min(FIELD.text.length, Math.floor((frame - FIELD.start) * FIELD.cpf));
  const caretOn = frame < CLICK && (n < FIELD.text.length || Math.floor((frame - FIELD.start) / 8) % 2 === 0);
  return (
    <>
      <Stage keys={emergeIn(FIELD.at - 2, 16, 0.8)}>
        <div style={{ position: "absolute", left: "50%", top: "50%", width: w, height: h, marginLeft: -w / 2, marginTop: -h / 2, borderRadius: r, background: bg,
          boxShadow: grow > 0.3 ? SHADOW : undefined, overflow: "hidden" }}>
          {fieldOp > 0.01 ? (
            <div style={{ position: "absolute", inset: 0, opacity: fieldOp, filter: frame > MORPH ? `blur(${clamp01((frame - MORPH) / 4) * 8}px)` : undefined }}>
              <div style={{ position: "absolute", left: 0, top: 0, width: FIELD.padL, height: h, display: "flex", alignItems: "center", justifyContent: "center" }}><Ring d={46} thick={7} /></div>
              <div style={{ position: "absolute", left: FIELD.padL, top: 0, height: h, width: Math.max(0, w - FIELD.padL - 60), overflow: "hidden", display: "flex", alignItems: "center",
                whiteSpace: "pre", fontFamily: FIELD.font.family, fontSize: FIELD.font.size, fontWeight: 500, letterSpacing: "-0.01em", color: INK }}>
                <span>{FIELD.text.slice(0, n)}</span>
                {caretOn ? <span style={{ display: "inline-block", width: 3, height: 38, background: BLUE, marginLeft: 2, borderRadius: 2 }} /> : null}
              </div>
              <div style={{ position: "absolute", right: 0, top: 0, width: FIELD.padR, height: h, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <SendBtn s={pressScale(frame, CLICK, 0.05)} />
              </div>
            </div>
          ) : null}
          {cg && cg.k > 0.05 ? (
            <div style={{ position: "absolute", inset: 0, opacity: clamp01((cg.k - 0.05) / 0.25) * (1 - EASE_PRO.exit(clamp01((frame - MC - 6) / 16))) }}><Calendar /></div>
          ) : null}
        </div>
      </Stage>
      {frame < MORPH ? <RingDraw at={68} w={w} h={h} color={BLUE} dur={12} fadeAt={90} /> : null}
    </>
  );
};

const NOTE = { y: -CARD.h / 2 - 76, w: 640, h: 108 };
const ICON = { x: -NOTE.w / 2 + 24 + 28, y: NOTE.y, d: 56 };
const Notification: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < NOTIF) return null;
  return (
    <Move keys={snapIn(NOTIF, { dir: "down", dist: 80, dur: 18, y: NOTE.y })}>
      <div style={{ width: NOTE.w, height: NOTE.h, borderRadius: 30, background: "rgba(255,255,255,.96)", boxShadow: SHADOW, display: "flex", alignItems: "center", gap: 18,
        padding: "0 24px", boxSizing: "border-box", fontFamily: FONT.ui }}>
        <Ring d={ICON.d} thick={8} p={0.9} />
        <div style={{ flex: 1, opacity: 1 - EASE_PRO.exit(clamp01((frame - MC - 12) / 14)) }}>
          <div style={{ fontSize: 24, fontWeight: 700, color: INK }}>Orbit</div>
          <TypeLine text="You saved 4h 40m this week" start={NOTIF + 8} cpf={1.4} caret="none" style={{ fontSize: 22, color: "#3A3A3C" }} />
        </div>
        <div style={{ fontSize: 20, color: "#8E8E93", alignSelf: "flex-start", marginTop: 22, opacity: 1 - clamp01((frame - MC - 12) / 10) }}>now</div>
      </div>
    </Move>
  );
};

/* ---------------- LIGHT WORLD CAMERA ---------------- */
const LIGHT_KEYS = [{ f: 0, zoom: 1.22, cy: 14 }, { f: 64, zoom: 1.0, cy: 0, ease: EASE_PRO.drift }];
const LIGHT_DRIFT = { zoomPerSec: 0.012 };
const BASE_MOVES: CamMove[] = [
  { at: 50, dur: 44, zoom: 1.3 }, // push into the bar as it emerges (direction flips ON the collapse event)
  { at: 92, dur: 32, zoom: 1.06, ease: EASE_PRO.drift }, // keeps creeping while the cursor travels
  { at: 116, dur: 40, zoom: 0.68, ease: aeEase(50, 85) }, // pull back as the bar becomes the card
  { at: 150, dur: 56, zoom: 1.18, y: -70, ease: EASE_PRO.drift }, // alive hold, drifting toward the notification
];
// the match-cut push lands EXACTLY on the notification icon at a known screen size
const MC_ZOOM_AT_CUT = 4.4;
const mcMove = (): CamMove => {
  const base = camState(CUT, { keys: LIGHT_KEYS, moves: BASE_MOVES, drift: LIGHT_DRIFT });
  // AE ease-in (70% influence, no landing): accelerates into the cut but ends at HALF the speed of EASE_PRO.exit
  return { at: MC, dur: CUT - MC, zoom: MC_ZOOM_AT_CUT / base.zoom, x: ICON.x - base.cx, y: ICON.y - base.cy, ease: aeEase(70, 0) };
};

const LightWorld: React.FC = () => {
  const frame = useCurrentFrame();
  const moves = [...BASE_MOVES, mcMove()];
  const fw = (f: number) => prog(f, 62, 18, EASE_PRO.moveSoft) * (1 - prog(f, 100, 30, EASE_PRO.move));
  const followX = (f: number) => springFollow(f, (g) => fieldGeom(g, FIELD).caret * 0.4, 57, 0.16);
  const extra = (f: number) => ({ cx: fw(f) * followX(f) });
  const btnX = fieldGeom(CLICK, FIELD).w / 2 - FIELD.padR / 2;
  return (
    <CameraRig keys={LIGHT_KEYS} moves={moves} drift={LIGHT_DRIFT} extra={extra}>
      <Hook />
      <Notification />
      <HeroObject />
      {frame >= CLICK - 2 && frame < CLICK + 14 ? <ClickRing at={CLICK} w={72} h={72} x={btnX} color={BLUE} /> : null}
      <MacCursor appearAt={94} hideAt={MORPH + 8} size={44}
        keys={[{ f: 94, x: 470, y: 330, kind: "arrow" }, { f: CLICK - 8, x: btnX + 6, y: 8, kind: "arrow", bend: 0.22 }, { f: CLICK - 6, x: btnX + 6, y: 8, kind: "hand" },
          { f: CLICK, x: btnX + 6, y: 8, kind: "hand", click: true }]} />
    </CameraRig>
  );
};

/* ---------------- STATS (the icon became this ring) ---------------- */
const RING_D = 440;
const StatsWorld: React.FC = () => {
  const frame = useCurrentFrame();
  const p = lerp(0.3, 0.9, EASE_PRO.move(clamp01((frame - ODO) / 16)));
  const numF: FontSpec = { family: FONT.ui, size: 92, weight: 700, letterSpacing: -0.05 };
  return (
    <CameraRig keys={[{ f: CUT, zoom: (ICON.d * MC_ZOOM_AT_CUT) / RING_D }, { f: CUT + 28, zoom: 1.0, ease: aeEase(0, 75) }]}
      moves={[{ at: CUT + 16, dur: 66, zoom: 1.22, y: 20, ease: EASE_PRO.drift }, { at: DARK0 - 6, dur: DCUT - DARK0 + 10, zoom: 3.0, ease: aeEase(70, 0) }]} drift={{ zoomPerSec: 0.012 }}>
      <div style={{ position: "absolute", left: "50%", top: "50%", marginLeft: -RING_D / 2, marginTop: -RING_D / 2 - 30, transform: `rotate(${(frame - CUT) * 0.35}deg)` }}><Ring d={RING_D} thick={62} p={p} /></div>
      <div style={{ position: "absolute", left: 0, right: 0, top: "50%", marginTop: -30 - 60, height: 120, display: "flex", alignItems: "center", justifyContent: "center",
        fontFamily: numF.family, fontSize: numF.size, fontWeight: 700, letterSpacing: "-0.05em", color: INK, opacity: clamp01((frame - CUT - 4) / 6) * (1 - EASE_PRO.exit(clamp01((frame - DARK0 - 2) / 14))) }}>
        <WaveNumber values={[{ v: "1h 20m", at: 0 }, { v: "4h 40m", at: ODO }]} ink={INK} accent={BLUE} dur={14} stagger={1.5} />
      </div>
      <div style={{ position: "absolute", left: "50%", top: "50%", marginTop: RING_D / 2 + 10, transform: `translateX(-50%)`, opacity: 1 - EASE_PRO.exit(clamp01((frame - DARK0) / 12)) }}>
        <WordIn text="time saved this week" start={CUT + 12} every={3} font={{ family: FONT.ui, size: 34, weight: 500 }} ink="#8E8E93" />
      </div>
    </CameraRig>
  );
};

/* ---------------- DARK STATEMENT + WHEEL ---------------- */
const WHEEL_ITEMS = ["track.", "time.", "autopilot."];
const DarkWorld: React.FC = () => {
  const frame = useCurrentFrame();
  const onW = layoutLine("on", DARK_F).W;
  const itemW = Math.max(...WHEEL_ITEMS.map((t) => layoutLine(t, DARK_F).W));
  const gap = DARK_F.size * 0.26;
  const rowW = onW + gap + itemW;
  const wheelIn = EASE_PRO.enterSnap(clamp01((frame - DCUT - 12) / 18));
  return (
    <Stage keys={[{ f: DCUT - 6, scale: 0.86, blur: 12, opacity: 0 }, { f: DCUT + 4, opacity: 1, ease: EASE_PRO.linear }, { f: DCUT + 16, scale: 1, blur: 0, ease: EASE_PRO.enterSnap },
      ...collapseOut(LCOLL, 12)]}>
      <CameraRig keys={[{ f: DCUT, zoom: 1.0 }]} moves={[{ at: DCUT, dur: 96, zoom: 1.3, rot: -1.6, ease: EASE_PRO.drift }]} drift={{ zoomPerSec: 0.01 }}>
        <div style={{ position: "absolute", left: "50%", top: "50%", marginLeft: -layoutLine("Your week,", DARK_F).W / 2, marginTop: -DARK_F.size * 1.25 - 6 }}>
          <WordIn text="Your week," start={DCUT} every={4} font={DARK_F} ink="#FFFFFF" accent="#5AC8FA" dist={26} />
        </div>
        <div style={{ position: "absolute", left: "50%", top: "50%", marginLeft: -rowW / 2, marginTop: 6, display: "flex", gap, alignItems: "center" }}>
          <WordIn text="on" start={DCUT + 10} font={DARK_F} ink="#FFFFFF" dist={26} />
          <div style={{ opacity: wheelIn, filter: wheelIn < 1 ? `blur(${(1 - wheelIn) * 8}px)` : undefined, transform: `translateY(${(1 - wheelIn) * 24}px)` }}>
            <WheelPicker itemH={DARK_F.size * 1.25} width={itemW} at={[WHEEL1, WHEEL2]} dur={16} step={32} window={1.5}
              items={WHEEL_ITEMS.map((t, i) => (
                <span key={t} style={{ fontFamily: DARK_F.family, fontSize: DARK_F.size, fontWeight: 600, letterSpacing: "-0.035em", whiteSpace: "pre",
                  color: i === 2 ? "#5AC8FA" : "#FFFFFF" }}>{t}</span>
              ))} />
          </div>
        </div>
      </CameraRig>
    </Stage>
  );
};

/* ---------------- LOGO (alive) -> END CARD ---------------- */
const Logo: React.FC = () => {
  const frame = useCurrentFrame();
  const draw = EASE_PRO.enter(clamp01((frame - LOGO) / 24));
  const circ = 2 * Math.PI * 68;
  const tagF: FontSpec = { family: FONT.ui, size: 36, weight: 500, letterSpacing: -0.01 };
  const tagW = Math.max(layoutLine("plan less.", tagF).W, layoutLine("live more.", tagF).W);
  const a = ((frame - LOGO) / 84) * Math.PI * 2 - Math.PI / 2;
  const dotIn = EASE_PRO.enterSnap(clamp01((frame - LOGO) / 12));
  const front = Math.sin(a) > 0;
  return (
    <Stage keys={[...emergeIn(LOGO, 22), ...collapseOut(ECOLL, 9, 0.55)]}>
      <CameraRig keys={[{ f: LOGO, zoom: 1.0 }]} moves={[{ at: LOGO, dur: 86, zoom: 1.28, y: -6, ease: EASE_PRO.drift }]} drift={{ zoomPerSec: 0.012 }}>
        <div style={{ position: "absolute", left: "50%", top: "50%", marginLeft: -84, marginTop: -84 - 70 }}>
          <svg width={168} height={168} viewBox="0 0 168 168" style={{ transform: `rotate(${-90 + (1 - draw) * -140}deg)` }}>
            <circle cx={84} cy={84} r={68} fill="none" stroke="#FFFFFF" strokeWidth={15} strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * (1 - draw)} />
          </svg>
        </div>
        <div style={{ position: "absolute", left: "50%", top: "50%", width: 34, height: 34, marginLeft: -17, marginTop: -17 - 70, borderRadius: 34, background: BLUE,
          transform: `translate(${Math.cos(a) * 110}px, ${Math.sin(a) * 36}px) scale(${dotIn * (front ? 1.08 : 0.86)})`, zIndex: front ? 2 : 0,
          boxShadow: `0 0 24px 6px ${BLUE}66` }} />
        <div style={{ position: "absolute", left: "50%", top: "50%", marginLeft: -layoutLine("orbit", { family: FONT.ui, size: 92, weight: 700, letterSpacing: -0.05 }).W / 2, marginTop: 52 }}>
          <WordIn text="orbit" start={LOGO + 10} font={{ family: FONT.ui, size: 92, weight: 700, letterSpacing: -0.05 }} ink="#FFFFFF" dist={24} />
        </div>
        <div style={{ position: "absolute", left: "50%", top: "50%", marginLeft: -tagW / 2, marginTop: 176, width: tagW, display: "flex", justifyContent: "center" }}>
          {frame < SWAP ? <WordIn text="plan less." start={LOGO + 24} every={4} font={tagF} ink="#8E9AB0" /> : <SwapLine from="plan less." to="live more." at={SWAP} font={tagF} ink="#8E9AB0" accent="#5AC8FA" />}
        </div>
      </CameraRig>
    </Stage>
  );
};

const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const t = clamp01((frame - END) / (PRO_DEMO_DURATION - END));
  return (
    <Stage keys={emergeIn(END, 22, 0.5)}>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <div style={{ fontFamily: FONT.ui, fontSize: 64, fontWeight: 600, color: "#FFFFFF", letterSpacing: "-0.02em", transform: `scale(${lerp(1, 1.16, EASE_PRO.drift(t))})`,
          textShadow: "0 0 18px rgba(255,255,255,.65), 0 0 46px rgba(90,200,250,.35)" }}>
          ui-motion-pro
        </div>
      </AbsoluteFill>
    </Stage>
  );
};

/* ---------------- ROOT ---------------- */
// The backdrop (world colour + wandering blobs) lives OUTSIDE the motion-blur stack: it moves slowly, and averaging
// 10-16 copies of a soft gradient bands it into visible rings.
const Backdrop: React.FC = () => {
  const frame = useCurrentFrame();
  const dk = darkness(frame);
  return (
    <AbsoluteFill style={{ background: bgAt(frame) }}>
      <div style={{ position: "absolute", inset: 0, opacity: 1 - dk }}>
        <DriftBlob x={-330} y={-360} size={1000} color="#C9DFFF" opacity={0.75} period={260} />
        <DriftBlob x={380} y={380} size={900} color="#D3F2DE" opacity={0.6} period={300} phase={90} />
      </div>
      <div style={{ position: "absolute", inset: 0, opacity: dk }}>
        <DriftBlob x={0} y={470} size={1400} color="#0A84FF" opacity={0.5} period={220} ay={70} />
        <DriftBlob x={-420} y={-380} size={800} color="#3A2BFF" opacity={0.22} period={280} phase={60} />
      </div>
    </AbsoluteFill>
  );
};

const Scenes: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      {frame < CUT + 2 ? <LightWorld /> : null}
      {frame >= CUT && frame < DCUT + 4 ? (
        <Stage keys={[{ f: CUT, opacity: 0.35 }, { f: CUT + 2, opacity: 1, ease: EASE_PRO.linear }, { f: DCUT - 6, opacity: 1 }, { f: DCUT + 4, opacity: 0, ease: EASE_PRO.linear }]}><StatsWorld /></Stage>
      ) : null}
      {frame >= DCUT - 6 && frame < LCOLL + 16 ? <DarkWorld /> : null}
      {frame >= LOGO && frame < ECOLL + 16 ? <Logo /> : null}
      {frame >= END ? <EndCard /> : null}
    </AbsoluteFill>
  );
};

export const ProDemo: React.FC<{ mb?: number }> = ({ mb = 10 }) => {
  useFontsReady();
  return (
    <AbsoluteFill>
      <Backdrop />
      <MotionBlur samples={mb} shutter={180} boost={{ samples: mb > 1 ? 14 : 1, windows: [[MC + 16, CUT + 6], [DARK0 + 8, DCUT + 8], [COLLAPSE, COLLAPSE + 14], [116, 140]] }}>
        <Scenes />
      </MotionBlur>
    </AbsoluteFill>
  );
};
