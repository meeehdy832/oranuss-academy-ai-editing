import React, { useId } from "react";
import { spring, useCurrentFrame } from "remotion";
import { EASE_PRO, Ease, SPRING_PRO } from "./curves";
import { K, num, sample, str } from "./keyed";
import { useAccum } from "./MotionBlur";

/** Turn a spring into an easing function over `dur` frames (for size morphs with overshoot). */
export const springEase = (config = SPRING_PRO.morph, dur = 14, fps = 30): Ease => (t: number) =>
  spring({ frame: t * dur, fps, config, durationInFrames: dur });

/**
 * The element animator. Keys (all optional): x, y, scale, sx, sy, rot, rx, ry, opacity, blur,
 * w, h, radius, bg, color. Default easing = EASE_PRO.enter.
 * - Directional motion blur from velocity (blurK px per px/frame).
 * - `smear`: stretch along fast horizontal/vertical motion (1-3f smear frames in the refs).
 * - `float`: idle bob so holds never freeze.
 * - anchor "center": positioned at frame center + (x,y); "flow": stays in layout.
 */
export const Move: React.FC<{
  keys?: K[];
  anchor?: "center" | "flow";
  blurK?: number;
  smear?: number;
  float?: { amp?: number; period?: number; phase?: number; rot?: number };
  origin?: string;
  perspective?: number;
  style?: React.CSSProperties;
  frame?: number;
  children?: React.ReactNode;
}> = ({ keys = [], anchor = "center", blurK = 0.45, smear = 0, float, origin = "50% 50%", perspective = 1400, style, frame: fo, children }) => {
  const cur = useCurrentFrame();
  const frame = fo ?? cur;
  const id = "mv" + useId().replace(/[^a-zA-Z0-9]/g, "");
  const v = sample(keys, frame, EASE_PRO.enter);
  const p = sample(keys, frame - 1, EASE_PRO.enter);

  let x = num(v.x, 0);
  let y = num(v.y, 0);
  let rot = num(v.rot, 0);
  if (float) {
    const per = float.period ?? 90;
    const ph = float.phase ?? 0;
    y += Math.sin(((frame + ph) / per) * Math.PI * 2) * (float.amp ?? 8);
    rot += Math.sin(((frame + ph) / per) * Math.PI * 2 + 1.3) * (float.rot ?? 0);
  }
  const vx = x - num(p.x, 0);
  const vy = y - num(p.y, 0);
  const sc = num(v.scale, 1);
  const vs = Math.abs(sc - num(p.scale, 1)) * 120;
  const base = Math.max(0, num(v.blur, 0));
  // dead zone: slow moves (< 6 px/f) stay sharp; fast moves smear along their direction
  const dz = (q: number) => Math.max(0, q - 6);
  // inside <MotionBlur> the shutter already smears fast moves: keep only the keyed focus blur
  const accum = useAccum();
  const k = accum ? 0 : blurK;
  const bx = Math.min(60, base + (dz(Math.abs(vx)) + dz(vs)) * k);
  const by = Math.min(60, base + (dz(Math.abs(vy)) + dz(vs)) * k);
  const useBlur = bx > 0.3 || by > 0.3;
  const stretchX = smear ? 1 + Math.min(0.8, (Math.abs(vx) / 160) * smear) : 1;
  const stretchY = smear ? 1 + Math.min(0.8, (Math.abs(vy) / 160) * smear) : 1;

  const sized: React.CSSProperties = {};
  if (typeof v.w === "number") sized.width = v.w;
  if (typeof v.h === "number") sized.height = v.h;
  if (typeof v.radius === "number") sized.borderRadius = v.radius;
  if (typeof v.bg === "string") sized.background = str(v.bg, "transparent");
  if (typeof v.color === "string") sized.color = v.color;

  const rx = num(v.rx, 0);
  const ry = num(v.ry, 0);
  const transform = [
    anchor === "center" ? "translate(-50%, -50%)" : "",
    `translate(${x}px, ${y}px)`,
    rx || ry ? `perspective(${perspective}px) rotateX(${rx}deg) rotateY(${ry}deg)` : "",
    `rotate(${rot}deg)`,
    `scale(${num(v.sx, 1) * sc * stretchX}, ${num(v.sy, 1) * sc * stretchY})`,
  ].join(" ");

  return (
    <>
      {useBlur ? (
        <svg width={0} height={0} style={{ position: "absolute" }}>
          <filter id={id} x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation={`${bx.toFixed(2)} ${by.toFixed(2)}`} />
          </filter>
        </svg>
      ) : null}
      <div
        style={{
          position: anchor === "center" ? "absolute" : "relative",
          left: anchor === "center" ? "50%" : undefined,
          top: anchor === "center" ? "50%" : undefined,
          transform,
          transformOrigin: origin,
          opacity: num(v.opacity, 1),
          filter: useBlur ? `url(#${id})` : undefined,
          ...sized,
          ...style,
        }}
      >
        {children}
      </div>
    </>
  );
};

type Dir = "up" | "down" | "left" | "right" | "none";
const vec = (d: Dir, dist: number) =>
  d === "up" ? { x: 0, y: dist } : d === "down" ? { x: 0, y: -dist } : d === "left" ? { x: dist, y: 0 } : d === "right" ? { x: -dist, y: 0 } : { x: 0, y: 0 };

/**
 * ENTRANCE keys with offset properties (follow-through), as measured:
 * opacity done at 30%, blur cleared at 65%, position over the full duration (ENTER curve),
 * scale settles last with a tiny overshoot.
 * dir = direction of travel ("up" = comes from below moving up).
 */
export const enter = (
  at: number,
  o: { dir?: Dir; dist?: number; dur?: number; blur?: number; scale?: number; rot?: number; ease?: Ease; x?: number; y?: number } = {},
): K[] => {
  const dur = o.dur ?? 20;
  const d = vec(o.dir ?? "up", o.dist ?? 80);
  const bx = o.x ?? 0;
  const by = o.y ?? 0;
  return [
    { f: at, x: bx + d.x, y: by + d.y, opacity: 0, blur: o.blur ?? 16, scale: o.scale ?? 0.92, rot: o.rot ?? 0 },
    { f: at + Math.max(2, Math.round(dur * 0.3)), opacity: 1, ease: EASE_PRO.linear },
    { f: at + Math.round(dur * 0.65), blur: 0, ease: EASE_PRO.enterSnap },
    { f: at + dur, x: bx, y: by, rot: 0, ease: o.ease ?? EASE_PRO.enter },
    { f: at + dur + 3, scale: 1, ease: springEase(SPRING_PRO.morph, dur + 3) },
  ];
};

/** Small things (words, chips, pins): quick snap-in from blur. */
export const snapIn = (at: number, o: { dir?: Dir; dist?: number; dur?: number; blur?: number; x?: number; y?: number; scale?: number } = {}): K[] =>
  enter(at, { dur: o.dur ?? 10, dist: o.dist ?? 24, blur: o.blur ?? 10, ease: EASE_PRO.enterSnap, dir: o.dir, x: o.x, y: o.y, scale: o.scale ?? 0.96 });

/** Pop: scale from small with spring overshoot (icons, avatars, emoji, buttons). */
export const pop = (at: number, o: { from?: number; dur?: number; x?: number; y?: number; blur?: number } = {}): K[] => {
  const dur = o.dur ?? 12;
  return [
    { f: at, scale: o.from ?? 0.4, opacity: 0, blur: o.blur ?? 8, x: o.x ?? 0, y: o.y ?? 0 },
    { f: at + 3, opacity: 1, ease: EASE_PRO.linear },
    { f: at + 6, blur: 0, ease: EASE_PRO.enterSnap },
    { f: at + dur, scale: 1, ease: springEase(SPRING_PRO.pop, dur) },
  ];
};

/**
 * EXIT keys: accelerate away and END AT PEAK SPEED (cut / morph / hand-off on the last frame).
 * Blur grows with speed automatically; extra blur ramps in the last 40%.
 */
export const exit = (at: number, o: { dir?: Dir; dist?: number; dur?: number; scale?: number; x?: number; y?: number; hard?: boolean } = {}): K[] => {
  const dur = o.dur ?? 12;
  const d = vec(o.dir ?? "up", o.dist ?? 120);
  const bx = o.x ?? 0;
  const by = o.y ?? 0;
  const e = o.hard ? EASE_PRO.exitHard : EASE_PRO.exit;
  return [
    { f: at, x: bx, y: by, opacity: 1, blur: 0, scale: 1 },
    { f: at + Math.round(dur * 0.6), blur: 0 },
    { f: at + dur, x: bx - d.x, y: by - d.y, opacity: 0, blur: 14, scale: o.scale ?? 0.9, ease: e },
  ];
};

/** Hold keys with a slow drift so a resting element is still alive. */
export const holdDrift = (from: number, to: number, o: { scale?: number; y?: number; x?: number } = {}): K[] => [
  { f: from, scale: 1, y: 0, x: 0 },
  { f: to, scale: o.scale ?? 1.03, y: o.y ?? 0, x: o.x ?? 0, ease: EASE_PRO.drift },
];
