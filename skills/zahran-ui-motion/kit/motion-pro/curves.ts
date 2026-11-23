// Motion curves MEASURED from the 24 reference reels (optical-flow velocity profiles @30fps).
// See ~/.claude/skills/zahran-ui-motion/references/02-motion.md for the data.
//
// AE <-> CSS naming (the classic confusion):
//   AE "ease IN" on the arrival key  = element DECELERATES into place  = CSS/Remotion ease-OUT  (ENTER)
//   AE "ease OUT" on the leaving key = element ACCELERATES away         = CSS/Remotion ease-IN   (EXIT)
import { Easing, interpolate, interpolateColors } from "remotion";

export type Ease = (t: number) => number;

export const EASE_PRO = {
  /** Signature curve: camera moves, transfers, morph positions. 70% of travel in ~5f around the middle. 24-40f. */
  move: Easing.bezier(0.85, 0, 0.15, 1),
  /** Softer variant of move for long camera drifts between holds. */
  moveSoft: Easing.bezier(0.65, 0, 0.25, 1),
  /** Big elements / scenes arriving: short ramp, very long landing. 18-30f. */
  enter: Easing.bezier(0.5, 0, 0, 1),
  /** Small UI, words, chips, pins arriving (expo-out). 8-16f. */
  enterSnap: Easing.bezier(0.16, 1, 0.3, 1),
  /** Leaving / handing off: accelerate, end at peak speed. 8-16f. */
  exit: Easing.bezier(0.7, 0, 0.84, 0),
  /** Hard exit (expo-in): long creep then a violent finish. Cut or morph on its last frame. */
  exitHard: Easing.bezier(0.95, 0.05, 0.8, 0.04),
  /** Holds: alive but calm. */
  drift: Easing.bezier(0.33, 0, 0.67, 1),
  linear: (t: number) => t,
};

/**
 * Build a curve the way an After Effects editor thinks:
 * outInfluence = influence (%) on the LEAVING keyframe (higher = slower start),
 * inInfluence  = influence (%) on the ARRIVING keyframe (higher = longer, softer landing).
 * aeEase(33,33) = Easy Ease. aeEase(0,90) = fast entrance. aeEase(85,0) = accelerating exit.
 */
export const aeEase = (outInfluence: number, inInfluence: number): Ease =>
  Easing.bezier(Math.min(1, outInfluence / 100), 0, 1 - Math.min(1, inInfluence / 100), 1);

export const SPRING_PRO = {
  /** container w/h/radius morphs: ~3% overshoot */
  morph: { damping: 17, stiffness: 140, mass: 1 },
  /** icons, avatars, emoji, buttons: ~8% overshoot */
  pop: { damping: 12, stiffness: 180, mass: 0.8 },
  /** settles with no visible overshoot */
  settle: { damping: 26, stiffness: 120, mass: 1 },
};

export const clamp01 = (t: number) => (t < 0 ? 0 : t > 1 ? 1 : t);
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

/** 0..1 progress of a tween that starts at `start` and lasts `dur` frames. */
export const prog = (frame: number, start: number, dur: number, ease: Ease = EASE_PRO.enter) =>
  ease(clamp01((frame - start) / Math.max(1, dur)));

/** Tween a number. */
export const tw = (frame: number, start: number, dur: number, from: number, to: number, ease: Ease = EASE_PRO.enter) =>
  lerp(from, to, prog(frame, start, dur, ease));

/** Tween a color. */
export const twc = (frame: number, start: number, dur: number, from: string, to: string, ease: Ease = EASE_PRO.enter) =>
  interpolateColors(prog(frame, start, dur, ease), [0, 1], [from, to]);

/** Piecewise tween through several [frame, value] stops with one easing per segment. */
export const path = (frame: number, stops: Array<[number, number]>, ease: Ease = EASE_PRO.move) => {
  if (frame <= stops[0][0]) return stops[0][1];
  for (let i = 1; i < stops.length; i++) {
    if (frame <= stops[i][0]) {
      const [f0, v0] = stops[i - 1];
      const [f1, v1] = stops[i];
      return lerp(v0, v1, ease(clamp01((frame - f0) / Math.max(1, f1 - f0))));
    }
  }
  return stops[stops.length - 1][1];
};

/** Interpolate with clamping (shorthand). */
export const ip = (frame: number, input: number[], output: number[], ease?: Ease) =>
  interpolate(frame, input, output, { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });

/** Deterministic pseudo-random in [0,1) from integers (stable across renders). */
export const rand = (a: number, b = 0, c = 0) => {
  let h = (a * 374761393 + b * 668265263 + c * 2147483647) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  h ^= h >>> 16;
  return ((h >>> 0) % 100000) / 100000;
};

/** Smooth value noise in [-1,1] (for shake, float, flicker). */
export const noise1 = (t: number, seed = 0) => {
  const i = Math.floor(t);
  const f = t - i;
  const u = f * f * (3 - 2 * f);
  const a = rand(i, seed) * 2 - 1;
  const b = rand(i + 1, seed) * 2 - 1;
  return a + (b - a) * u;
};
