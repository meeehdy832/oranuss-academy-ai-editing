// FLOW: helpers that keep motion continuous (no stops between stacked animations).
import { useEffect, useState } from "react";
import { continueRender, delayRender } from "remotion";
import { EASE_PRO, Ease, clamp01 } from "./curves";

/**
 * Call once at the top of a composition that uses measured layouts (TextFx, TypeField, caretX).
 * Holds the frame until web fonts are ready and re-renders, so no frame is laid out with fallback widths.
 */
export const useFontsReady = () => {
  const [ready, setReady] = useState(() => typeof document === "undefined" || document.fonts.status === "loaded");
  const [handle] = useState(() => (ready ? null : delayRender("mehdi-ui-motion: waiting for fonts")));
  useEffect(() => {
    if (ready) return;
    document.fonts.ready.then(() => {
      setReady(true);
      if (handle !== null) continueRender(handle);
    });
  }, [ready, handle]);
  return ready;
};

/**
 * Critically-damped spring follow of a target signal, integrated deterministically from frame `from`.
 * Use for follow-cams and anything that chases a value that changes in steps (typed text width,
 * caret x, list length): the follower accelerates smoothly, never stops between steps and lands softly.
 * omega: responsiveness (0.12 lazy camera, 0.25 UI container, 0.45 tight).
 * zeta: damping (1 = no overshoot; 0.7 = a soft ~4% overshoot for containers that grow, like the refs' morphs).
 */
export const springFollow = (f: number, target: (f: number) => number, from: number, omega = 0.22, zeta = 1): number => {
  let x = target(from);
  let v = 0;
  const end = Math.floor(f);
  const frac = f - end;
  // integrate one step PAST the current frame so sub-frame times (motion-blur samples) interpolate smoothly;
  // without this every sample inside a frame lands on one of two positions = a doubled image, not a smear
  let prev = x;
  for (let i = from + 1; i <= end + 1; i++) {
    if (i === end + 1) prev = x;
    const tg = target(i);
    for (let s = 0; s < 4; s++) {
      const dt = 0.25;
      const a = omega * omega * (tg - x) - 2 * zeta * omega * v;
      v += a * dt;
      x += v * dt;
    }
  }
  if (end < from + 1) return frac > 0 && end >= from ? prev + (x - prev) * frac : target(from);
  return prev + (x - prev) * frac;
};

/** Smooth step function of a stepped signal: blend between steps with a curve instead of jumping. */
export const smoothSteps = (f: number, steps: Array<[number, number]>, dur = 10, ease: Ease = EASE_PRO.move) => {
  let v = steps[0][1];
  for (let i = 1; i < steps.length; i++) {
    const [at, val] = steps[i];
    v += (val - steps[i - 1][1]) * ease(clamp01((f - at) / dur));
  }
  return v;
};

/* ---------------- text measuring (exact widths for growing fields and follow-cams) ---------------- */
const wCache = new Map<string, number>();
let ctx: CanvasRenderingContext2D | null = null;
export type FontSpec = { family: string; size: number; weight?: number | string; letterSpacing?: number /* em */ };

/** Width of `text` in px for a font. Cached only once the font is really loaded (no fallback-width bugs). */
export const measure = (text: string, font: FontSpec): number => {
  const key = `${font.family}|${font.size}|${font.weight ?? 400}|${font.letterSpacing ?? 0}|${text}`;
  const hit = wCache.get(key);
  if (hit !== undefined) return hit;
  if (typeof document === "undefined") return text.length * font.size * 0.52;
  if (!ctx) ctx = document.createElement("canvas").getContext("2d");
  if (!ctx) return text.length * font.size * 0.52;
  const fam = font.family.indexOf(",") >= 0 || font.family.indexOf('"') >= 0 ? font.family : `"${font.family}"`;
  const css = `${font.weight ?? 400} ${font.size}px ${fam}`;
  ctx.font = css;
  const w = ctx.measureText(text).width + (font.letterSpacing ?? 0) * font.size * text.length;
  let loaded = false;
  try {
    loaded = document.fonts.check(css);
  } catch {
    loaded = false;
  }
  if (loaded) wCache.set(key, w);
  return w;
};

/**
 * Continuous caret x for typing: width of the typed prefix, interpolated INSIDE the current character
 * (so a follow-cam driven by it moves every frame instead of stepping per character).
 */
export const caretX = (f: number, start: number, text: string, cpf: number, font: FontSpec) => {
  const n = Math.max(0, Math.min(text.length, (f - start) * cpf));
  const i = Math.floor(n);
  const a = measure(text.slice(0, i), font);
  if (i >= text.length) return a;
  const b = measure(text.slice(0, i + 1), font);
  return a + (b - a) * (n - i);
};
