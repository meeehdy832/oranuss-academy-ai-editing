import React, { createContext, useContext, useId } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { EASE_PRO, Ease, clamp01, noise1 } from "./curves";
import { K, num, sample } from "./keyed";
import { useAccum } from "./MotionBlur";

/**
 * CAMERA v2: continuous, overlapping, jitter-free.
 *
 * A "look-at" camera. Position = keys (absolute)  +  moves (ADDITIVE, may overlap)  +  drift  +  extra.
 *   cx, cy  world point (px from frame center) that sits at the screen center
 *   zoom    1 = normal (moves multiply it; drift multiplies it)
 *   rot     roll in degrees;  rx, ry = 3D tilt in degrees
 *
 * WHY ADDITIVE MOVES: in an editor you stack animations so the next one starts BEFORE the previous one
 * lands. With absolute keys a camera must arrive (velocity 0) before the next key leaves. With `moves`
 * every move is a delta with its own curve; overlapping moves sum their velocities, so the camera never
 * stops. Rule of thumb: start each move at 55-75% of the previous one, and keep a drift running under all.
 *
 * WHY THE 3D LAYER + RASTER: Chrome snaps 2D-transformed text to whole pixels. A slow drift (<1 px/f)
 * then jitters +-0.5 px (measured: direction flips on 31/38 frames). The layer below is composited in 3D
 * (perspective + rotateX 0.01deg), which moves sub-pixel exactly (measured jitter 0.5 -> 0.065 px), and the
 * content is laid out at `raster`x resolution (CSS zoom) so it stays crisp when the camera pushes in.
 * Use raster 3 if the camera zooms beyond ~2.2.
 */
export type Shake = { at: number; dur?: number; amp?: number; freq?: number };
export type CamMove = {
  at: number;
  dur: number;
  /** world px added to cx / cy */
  x?: number;
  y?: number;
  /** zoom multiplier reached at the end (1.3 = push in 30%, 0.8 = pull back) */
  zoom?: number;
  rot?: number;
  rx?: number;
  ry?: number;
  ease?: Ease;
};
export type CamExtra = { cx?: number; cy?: number; zoom?: number; rot?: number };
export type CamOpts = {
  keys?: K[];
  moves?: CamMove[];
  drift?: { zoomPerSec?: number; xPerSec?: number; yPerSec?: number; rotPerSec?: number };
  extra?: (f: number) => CamExtra;
  shake?: Shake[];
  fps?: number;
};

/** Sum of overlapping moves at frame f. */
export const movesAt = (moves: CamMove[], f: number) => {
  let x = 0, y = 0, lz = 0, rot = 0, rx = 0, ry = 0;
  for (const m of moves) {
    if (f <= m.at) continue;
    const e = (m.ease ?? EASE_PRO.move)(clamp01((f - m.at) / Math.max(1, m.dur)));
    x += (m.x ?? 0) * e;
    y += (m.y ?? 0) * e;
    lz += Math.log(m.zoom ?? 1) * e;
    rot += (m.rot ?? 0) * e;
    rx += (m.rx ?? 0) * e;
    ry += (m.ry ?? 0) * e;
  }
  return { x, y, zoom: Math.exp(lz), rot, rx, ry };
};

/** Full camera state (world look-at) at frame f, before shake. Pure: safe to call for any frame. */
export const camState = (f: number, o: CamOpts) => {
  const fps = o.fps ?? 30;
  const v = sample(o.keys ?? [], f, EASE_PRO.move);
  const m = movesAt(o.moves ?? [], f);
  const d = o.drift ?? {};
  const t = f / fps;
  const ex = o.extra ? o.extra(f) : {};
  return {
    cx: num(v.cx, 0) + m.x + (d.xPerSec ?? 0) * t + (ex.cx ?? 0),
    cy: num(v.cy, 0) + m.y + (d.yPerSec ?? 0) * t + (ex.cy ?? 0),
    zoom: num(v.zoom, 1) * m.zoom * (1 + (d.zoomPerSec ?? 0) * t) * (ex.zoom ?? 1),
    rot: num(v.rot, 0) + m.rot + (d.rotPerSec ?? 0) * t + (ex.rot ?? 0),
    rx: num(v.rx, 0) + m.rx,
    ry: num(v.ry, 0) + m.ry,
  };
};

/** Screen transform (translation of the frame center) for a camera state, with shake. */
const screen = (f: number, o: CamOpts) => {
  const fps = o.fps ?? 30;
  const c = camState(f, o);
  let sx = 0, sy = 0, sr = 0;
  (o.shake ?? []).forEach((s, i) => {
    const d = f - s.at;
    const dur = s.dur ?? 8;
    if (d < 0 || d > dur) return;
    const decay = Math.pow(1 - d / dur, 2);
    const fr = (s.freq ?? 10) / fps;
    const amp = s.amp ?? 4;
    sx += noise1(d * fr * 4, 11 + i) * amp * decay;
    sy += noise1(d * fr * 4, 23 + i) * amp * decay;
    sr += noise1(d * fr * 4, 37 + i) * amp * 0.08 * decay;
  });
  const r = ((c.rot + sr) * Math.PI) / 180;
  const wx = c.cx * c.zoom;
  const wy = c.cy * c.zoom;
  return {
    tx: -(wx * Math.cos(r) - wy * Math.sin(r)) + sx,
    ty: -(wx * Math.sin(r) + wy * Math.cos(r)) + sy,
    zoom: c.zoom,
    rot: c.rot + sr,
    rx: c.rx,
    ry: c.ry,
  };
};

/** Screen speed of the camera at frame f in px/frame (translation + zoom smear at the frame edge). Useful for QA. */
export const camSpeed = (f: number, o: CamOpts, halfDiag = 764) => {
  const a = screen(f, o);
  const b = screen(f - 1, o);
  return Math.hypot(a.tx - b.tx, a.ty - b.ty) + Math.abs(Math.log(a.zoom / b.zoom)) * halfDiag;
};

/** Raster factor of the enclosing camera (components that build their own SVG filters can scale by it). */
export const RasterContext = createContext(1);
export const useRaster = () => useContext(RasterContext);

export const CameraRig: React.FC<
  CamOpts & {
    /** blur px per px/frame of motion (0.45 ~ 160 deg shutter). 0 disables. */
    blur?: number;
    /** screen speed (px/frame) below which the camera adds NO blur, so slow moves stay tack sharp */
    blurDeadZone?: number;
    /** depth-of-field edge blur in px (constant: never toggle it on/off mid-shot) */
    dof?: number;
    perspective?: number;
    /** internal resolution of the content (2 = crisp up to ~2.2x zoom, 3 for deeper pushes) */
    raster?: number;
    children?: React.ReactNode;
  }
> = ({ keys = [], moves = [], drift = { zoomPerSec: 0.015 }, shake = [], extra, blur = 0.45, blurDeadZone = 8, dof = 0, perspective = 2400, raster = 2, children }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const id = "cam" + useId().replace(/[^a-zA-Z0-9]/g, "");
  const o: CamOpts = { keys, moves, drift, extra, shake, fps };

  const c = screen(frame, o);
  const p = screen(frame - 1, o);
  const halfDiag = Math.hypot(width, height) / 2;
  const zoomSmear = Math.abs(Math.log(c.zoom / p.zoom)) * halfDiag * 0.5;
  const dz = (v: number) => Math.max(0, v - blurDeadZone);
  const bx = blur ? Math.min(60, (dz(Math.abs(c.tx - p.tx)) + dz(zoomSmear)) * blur) : 0;
  const by = blur ? Math.min(60, (dz(Math.abs(c.ty - p.ty)) + dz(zoomSmear)) * blur) : 0;
  // inside <MotionBlur> the real shutter blur does the job: no fake gaussian
  const accum = useAccum();
  const useBlur = !accum && (bx > 0.3 || by > 0.3);
  const R = raster;

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {useBlur ? (
        <svg width={0} height={0} style={{ position: "absolute" }}>
          <filter id={id} x="-10%" y="-10%" width="120%" height="120%">
            <feGaussianBlur stdDeviation={`${bx.toFixed(2)} ${by.toFixed(2)}`} />
          </filter>
        </svg>
      ) : null}
      <AbsoluteFill style={{ filter: useBlur ? `url(#${id})` : undefined }}>
        <AbsoluteFill
          style={{
            transform: `translate(${c.tx}px, ${c.ty}px) perspective(${perspective}px) rotateX(${c.rx + 0.01}deg) rotateY(${c.ry}deg) rotate(${c.rot}deg) scale(${c.zoom / R})`,
            transformOrigin: "50% 50%",
          }}
        >
          <div
            style={
              {
                position: "absolute",
                left: "50%",
                top: "50%",
                width,
                height,
                marginLeft: -width / 2,
                marginTop: -height / 2,
                zoom: R,
              } as React.CSSProperties
            }
          >
            <RasterContext.Provider value={R}>{children}</RasterContext.Provider>
          </div>
        </AbsoluteFill>
      </AbsoluteFill>
      {dof > 0.3 ? <DepthBlur amount={dof} /> : null}
    </AbsoluteFill>
  );
};

/** Edge blur overlay (depth of field / tilt-shift). inner = clear radius in % of the frame. */
export const DepthBlur: React.FC<{ amount: number; inner?: number; outer?: number; mode?: "radial" | "tilt" }> = ({
  amount, inner = 38, outer = 75, mode = "radial",
}) => {
  const mask =
    mode === "radial"
      ? `radial-gradient(ellipse at center, transparent ${inner}%, black ${outer}%)`
      : `linear-gradient(to bottom, black 0%, transparent ${inner}%, transparent ${100 - inner}%, black 100%)`;
  return (
    <AbsoluteFill
      style={{
        backdropFilter: `blur(${amount}px)`,
        WebkitBackdropFilter: `blur(${amount}px)`,
        maskImage: mask,
        WebkitMaskImage: mask,
        pointerEvents: "none",
      }}
    />
  );
};

/**
 * Camera keys that push THROUGH a target rect (portal): the target grows until it overfills the frame.
 * target = center (x,y) in world px from frame center and its width. Next scene should start at at+dur.
 */
export const portalKeys = (
  at: number,
  dur: number,
  target: { x: number; y: number; w: number },
  frameW: number,
  overfill = 1.25,
): K[] => [
  { f: at, cx: 0, cy: 0, zoom: 1 },
  { f: at + dur, cx: target.x, cy: target.y, zoom: (frameW / target.w) * overfill, ease: EASE_PRO.exit },
];

/**
 * Whip pan keys. The VISIBLE whip is ~5-6f, but it lives inside a MOVE curve of 18-26f
 * (slow creep -> violent middle -> soft landing), exactly like the measured refs.
 */
export const whipKeys = (at: number, from: { cx: number; cy: number }, to: { cx: number; cy: number }, dur = 22): K[] => [
  { f: at, cx: from.cx, cy: from.cy },
  { f: at + dur, cx: to.cx, cy: to.cy, ease: EASE_PRO.move },
];

/**
 * Snap-zoom punch: zoom multiplier that jumps up in `up` frames then eases back.
 * IMPACTS ONLY (a slam, a logo landing, a beat drop). Never on ordinary UI changes: it reads as shake.
 */
export const punch = (f: number, at: number, amount = 0.05, up = 3, back = 18) => {
  const d = f - at;
  if (d < 0 || d > up + back) return 1;
  if (d <= up) return 1 + amount * EASE_PRO.enterSnap(d / up);
  return 1 + amount * (1 - EASE_PRO.enter((d - up) / back));
};

/** Lagged follow (moving average of a target over `lag` frames). Prefer springFollow (flow.ts) for smooth cams. */
export const follow = (f: number, target: (f: number) => number, lag = 6) => {
  let s = 0;
  for (let i = 0; i < lag; i++) s += target(f - i);
  return s / lag;
};
