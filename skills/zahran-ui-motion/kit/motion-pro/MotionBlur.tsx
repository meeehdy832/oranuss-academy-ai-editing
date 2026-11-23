import React, { createContext, useContext } from "react";
import { AbsoluteFill, Freeze, useCurrentFrame } from "remotion";
import { K, num, sample } from "./keyed";
import { EASE_PRO } from "./curves";

/*
 * REAL MOTION BLUR (film shutter): the scene is rendered `samples` times at sub-frame moments inside the
 * shutter window and averaged. Everything that moves (camera, elements, morphs, zooms) smears along its
 * own path, proportional to its own speed; still things stay sharp. This is what the pro reels look like.
 * A gaussian `filter: blur()` on a whole layer is NOT motion blur (it turns a moving scene into a gray block).
 *
 * - Wrap the whole composition (or one scene) once.
 * - samples 8-12 for finals, 1 for fast drafts (pass it from inputProps).
 * - `active(f)` lets you skip the extra renders on frames where nothing moves fast.
 * - Inside, CameraRig and Move switch their fake gaussian velocity blur off automatically.
 */
export const AccumContext = createContext(false);
export const useAccum = () => useContext(AccumContext);

export const MotionBlur: React.FC<{
  samples?: number;
  /**
   * Sample tiers: more samples only where things move fast (whips, zoom-throughs, morphs) so the smear is continuous,
   * and the cheap base count everywhere else. The highest tier containing the frame wins. Halves render time.
   */
  boost?: { samples: number; windows: Array<[number, number]> } | Array<{ samples: number; windows: Array<[number, number]> }>;
  shutter?: number;
  active?: (f: number) => boolean;
  children: React.ReactNode;
}> = ({ samples = 10, boost, shutter = 180, active, children }) => {
  const frame = useCurrentFrame();
  const tiers = boost ? (Array.isArray(boost) ? boost : [boost]) : [];
  let boosted = samples;
  if (samples > 1) for (const t of tiers) if (t.windows.some(([a, b]) => frame >= a && frame <= b)) boosted = Math.max(boosted, t.samples);
  const n = samples > 1 && (!active || active(frame)) ? boosted : 1;
  if (n === 1) return <AccumContext.Provider value={samples > 1}>{children}</AccumContext.Provider>;
  const sf = shutter / 360;
  return (
    <AbsoluteFill style={{ isolation: "isolate" }}>
      {Array.from({ length: n }).map((_, i) => {
        // centred shutter (AE default phase = -angle/2): samples spread evenly around the frame time
        const off = sf * ((i + 0.5) / n - 0.5);
        return (
          <AbsoluteFill key={i} style={{ mixBlendMode: "plus-lighter", filter: `opacity(${1 / n})` }}>
            <Freeze frame={frame + off}>
              <AccumContext.Provider value={true}>{children}</AccumContext.Provider>
            </Freeze>
          </AbsoluteFill>
        );
      })}
    </AbsoluteFill>
  );
};

/*
 * STAGE: a full-frame layer animated by keys (x, y, scale, rot, blur, opacity) around an origin point.
 * Scene transitions are key recipes on two overlapping Stages (the next one starts BEFORE the old one is gone).
 */
export const Stage: React.FC<{ keys?: K[]; origin?: { x: number; y: number }; style?: React.CSSProperties; children: React.ReactNode }> = ({
  keys = [], origin = { x: 0, y: 0 }, style, children,
}) => {
  const frame = useCurrentFrame();
  const v = sample(keys, frame, EASE_PRO.move);
  const op = num(v.opacity, 1);
  if (op <= 0.001) return null;
  const b = num(v.blur, 0);
  return (
    <AbsoluteFill
      style={{
        transform: `translate(${num(v.x, 0)}px, ${num(v.y, 0)}px) rotate(${num(v.rot, 0)}deg) scale(${num(v.scale, 1)})`,
        transformOrigin: `calc(50% + ${origin.x}px) calc(50% + ${origin.y}px)`,
        opacity: op,
        filter: b > 0.3 ? `blur(${b}px)` : undefined,
        ...style,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

/** Outgoing scene collapses into a point: scale -> 0.7, blur -> 10, fade (exit curve, ends fast). */
export const collapseOut = (at: number, dur = 12, to = 0.7): K[] => [
  { f: at, scale: 1, blur: 0, opacity: 1 },
  { f: at + dur, scale: to, blur: 10, ease: EASE_PRO.exit },
  { f: at + dur - 1, opacity: 1, ease: EASE_PRO.linear },
  { f: at + dur + 2, opacity: 0, ease: EASE_PRO.linear },
];

/** Incoming scene emerges from the same point: scale 0.6 -> 1, blur 12 -> 0, opacity in 5f (enter curve). */
export const emergeIn = (at: number, dur = 20, from = 0.6): K[] => [
  { f: at, scale: from, blur: 12, opacity: 0 },
  { f: at + 5, opacity: 1, ease: EASE_PRO.linear },
  { f: at + dur * 0.6, blur: 0, ease: EASE_PRO.enterSnap },
  { f: at + dur, scale: 1, ease: EASE_PRO.enterSnap },
];

/** Zoom-through, outgoing half: the scene rushes at the camera (accelerating) and blurs; cut on its last frame. */
export const zoomOutThrough = (at: number, dur = 14, to = 2.2): K[] => [
  { f: at, scale: 1, blur: 0 },
  { f: at + dur, scale: to, blur: 14, ease: EASE_PRO.exitHard },
];

/** Zoom-through, incoming half: starts slightly small and soft, settles (expo-out). */
export const zoomInThrough = (at: number, dur = 18, from = 0.88): K[] => [
  { f: at, scale: from, blur: 12, opacity: 0.2 },
  { f: at + 3, opacity: 1, ease: EASE_PRO.linear },
  { f: at + dur, scale: 1, blur: 0, ease: EASE_PRO.enterSnap },
];
