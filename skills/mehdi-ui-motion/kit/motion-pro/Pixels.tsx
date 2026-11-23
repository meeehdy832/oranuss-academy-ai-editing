import React from "react";
import { useCurrentFrame } from "remotion";
import { EASE_PRO, clamp01, lerp, rand } from "./curves";
import { useFxId } from "./Elements";

/*
 * PIXEL EFFECTS as the refs actually use them: FEW cells, LOCAL to a word or an object, short-lived.
 * (A full-screen pixel dissolve exists in only 1 of 24 videos; see PixelDissolve in Transitions.tsx.)
 *
 *  PixelSparkle  v11 "meet": 4-9 big square cells flicker AROUND a word as it lands (~12f)
 *  PixelReveal   text/element revealed cell by cell, accent cells leading the front
 *  Pixelate      v22 inline media: coarse mosaic -> fine -> sharp, with stray noise pixels
 *  PixelOrbit    v08: squares burst out of a hero and settle into a slow orbit
 *  PixelDust     v02: a word leaves as a puff of tiny square particles
 *
 * Coordinates are px relative to the frame center (same space as Move / CameraRig content).
 */

type Box = { x: number; y: number; w: number; h: number };

/* ------------------------------------------------------------------ */
/* PIXEL SPARKLE (v11, frames 1-12, measured)                          */
/* f0 4 cells appear translucent+soft, f1 they saturate, f2-5 the set   */
/* grows to 7-9 cells by spawning NEIGHBOURS on a grid (pairs, L shapes),*/
/* each cell lives 2-4f, f6-9 fewer + lighter + drifting outward,       */
/* f10-12 one or two ghosts. Cells never cover the word.               */
/* ------------------------------------------------------------------ */
export const PixelSparkle: React.FC<{
  at: number;
  /** the word's box (center x/y, w/h) */
  box: Box;
  /** areas the cells must never cover (each text line); defaults to box */
  avoid?: Box | Box[];
  /** cell size in px (v11: ~4.3% of frame width) */
  cell?: number;
  colors?: string[];
  /** total frames (v11: 12) */
  life?: number;
  /** cells at the peak (v11: 7-9) */
  peak?: number;
  /** how far from the word the seeds land, in cells */
  spread?: number;
  /** outward drift in px over the life */
  drift?: number;
  seed?: number;
}> = ({ at, box, avoid, cell = 40, colors = ["#B44CFF", "#7A1CF5", "#E040FB", "#F48FE6"], life = 12, peak = 8, spread = 1.6, drift = 26, seed = 3 }) => {
  const frame = useCurrentFrame();
  const d = frame - at;
  if (d < 0 || d > life) return null;
  // build the event list deterministically
  type Ev = { gx: number; gy: number; b: number; l: number; c: number; o: number };
  const evs: Ev[] = [];
  const hw = box.w / 2 / cell;
  const hh = box.h / 2 / cell;
  const avs: Box[] = avoid ? (Array.isArray(avoid) ? avoid : [avoid]) : [box];
  const blocked = (gx: number, gy: number) =>
    avs.some((av) => Math.abs(box.x + gx * cell - av.x) < av.w / 2 + cell * 0.7 && Math.abs(box.y + gy * cell - av.y) < av.h / 2 + cell * 0.7);
  // seeds around the word
  const nSeeds = 4;
  for (let i = 0; i < nSeeds; i++) {
    const a = (i / nSeeds) * Math.PI * 2 + rand(i, seed) * 1.2 + 0.4;
    let r = 0.6 + rand(i, seed, 1) * spread;
    let gx = 0;
    let gy = 0;
    // push the seed outward until it clears every avoided line
    for (let k = 0; k < 14; k++) {
      gx = Math.round(Math.cos(a) * (hw + r));
      gy = Math.round(Math.sin(a) * (hh + r * 0.8));
      if (!blocked(gx, gy)) break;
      r += 0.6;
    }
    if (!blocked(gx, gy)) evs.push({ gx, gy, b: 0, l: 3 + Math.floor(rand(i, seed, 2) * 3), c: i % colors.length, o: 1 });
  }
  // neighbours spawn from frames 2..8
  const want = Math.max(peak * 2, 10);
  for (let k = 0; k < want && evs.length > 0; k++) {
    const parent = evs[Math.floor(rand(k, seed, 7) * evs.length)];
    const dir = Math.floor(rand(k, seed, 8) * 4);
    const gx = parent.gx + (dir === 0 ? 1 : dir === 1 ? -1 : 0);
    const gy = parent.gy + (dir === 2 ? 1 : dir === 3 ? -1 : 0);
    if (blocked(gx, gy)) continue;
    const b = Math.min(life - 3, parent.b + 1 + Math.floor(rand(k, seed, 9) * 2));
    const o = rand(k, seed, 10) < 0.45 ? 1 : rand(k, seed, 11) < 0.5 ? 0.6 : 0.35;
    evs.push({ gx, gy, b, l: 2 + Math.floor(rand(k, seed, 12) * 3), c: Math.floor(rand(k, seed, 13) * colors.length), o });
  }
  const fade = d < 6 ? 1 : 1 - (d - 6) / (life - 5);
  return (
    <>
      {evs.map((e, i) => {
        if (d < e.b || d >= e.b + e.l) return null;
        const age = (d - e.b) / e.l;
        const first = d === 0;
        const out = (d / life) * drift;
        const len = Math.hypot(e.gx, e.gy) || 1;
        const x = box.x + e.gx * cell + (e.gx / len) * out;
        const y = box.y + e.gy * cell + (e.gy / len) * out;
        const op = (first ? 0.32 : e.o) * fade * (age > 0.8 && d > 6 ? 0.6 : 1);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: "50%",
              top: "50%",
              width: cell,
              height: cell,
              marginLeft: -cell / 2,
              marginTop: -cell / 2,
              transform: `translate(${x}px, ${y}px)`,
              background: colors[e.c],
              opacity: Math.max(0, op),
              filter: first ? "blur(2px)" : undefined,
            }}
          />
        );
      })}
    </>
  );
};

/* ------------------------------------------------------------------ */
/* PIXEL REVEAL: content appears cell by cell (local, not full screen)  */
/* Each cell flashes the accent for `flash` frames, then shows content. */
/* dir biases the order (left->right like a scan) + random jitter.      */
/* ------------------------------------------------------------------ */
export const PixelReveal: React.FC<{
  at: number;
  w: number;
  h: number;
  cell?: number;
  dur?: number;
  flash?: number;
  color?: string;
  dir?: "left" | "right" | "center" | "random";
  /** share of cells that flash the accent before showing content (sparse = 0.25-0.4) */
  flashRatio?: number;
  /** reverse = hide cell by cell */
  reverse?: boolean;
  seed?: number;
  children: React.ReactNode;
}> = ({ at, w, h, cell = 18, dur = 12, flash = 2, color = "#0A84FF", dir = "left", flashRatio = 0.35, reverse = false, seed = 7, children }) => {
  const frame = useCurrentFrame();
  const id = useFxId("pxr");
  const cols = Math.ceil(w / cell);
  const rows = Math.ceil(h / cell);
  const d = frame - at;
  if (!reverse && d >= dur + flash + 1) return <div style={{ width: w, height: h, position: "relative" }}>{children}</div>;
  if (reverse && d >= dur + flash + 1) return <div style={{ width: w, height: h }} />;
  const on: string[] = [];
  const fl: React.ReactNode[] = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const u = (c + 0.5) / cols;
      const bias = dir === "left" ? u : dir === "right" ? 1 - u : dir === "center" ? Math.abs(u - 0.5) * 2 : rand(c, r, seed);
      const t = clamp01(bias * 0.6 + rand(c, r, seed + 1) * 0.4) * dur;
      const age = d - t;
      const flashes = rand(c, r, seed + 2) < flashRatio;
      const visible = reverse ? age < 0 : age >= (flashes ? flash : 0);
      if (visible) on.push(`<rect x='${c * cell}' y='${r * cell}' width='${cell + 0.6}' height='${cell + 0.6}'/>`);
      if (flashes && age >= 0 && age < flash)
        fl.push(<div key={r * 999 + c} style={{ position: "absolute", left: c * cell, top: r * cell, width: cell, height: cell, background: color, opacity: reverse ? 0.9 : 1 - age / (flash + 1) * 0.3 }} />);
    }
  }
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='${cols * cell}' height='${rows * cell}'>${on.join("")}</svg>`;
  const mask = `url("data:image/svg+xml;utf8,${encodeURIComponent(svg)}")`;
  return (
    <div id={id} style={{ position: "relative", width: w, height: h }}>
      <div style={{ position: "absolute", inset: 0, maskImage: mask, WebkitMaskImage: mask, maskSize: `${cols * cell}px ${rows * cell}px`, WebkitMaskSize: `${cols * cell}px ${rows * cell}px`, maskRepeat: "no-repeat", WebkitMaskRepeat: "no-repeat" }}>
        {children}
      </div>
      {fl}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* PIXELATE (v22 inline video): mosaic -> finer -> noise pixels -> sharp */
/* ------------------------------------------------------------------ */
export const Pixelate: React.FC<{
  at: number;
  w: number;
  h: number;
  /** cell sizes per step (px), each held `hold` frames, then sharp */
  steps?: number[];
  hold?: number;
  noise?: number;
  noiseColor?: string;
  seed?: number;
  children: React.ReactNode;
}> = ({ at, w, h, steps = [w / 5, w / 10, w / 22], hold = 2, noise = 14, noiseColor = "#ffffff", seed = 4, children }) => {
  const frame = useCurrentFrame();
  const id = useFxId("pxl");
  const d = frame - at;
  const k = Math.floor(d / hold);
  const s = d < 0 ? steps[0] : k < steps.length ? steps[k] : 0;
  const noiseOn = d >= hold && d < steps.length * hold + 3;
  return (
    <div style={{ position: "relative", width: w, height: h, overflow: "hidden" }}>
      {s > 1 ? (
        <svg width={0} height={0} style={{ position: "absolute" }}>
          <filter id={id} x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse" primitiveUnits="userSpaceOnUse">
            <feFlood x={s / 2} y={s / 2} width="1" height="1" floodColor="#000" />
            <feComposite width={s} height={s} />
            <feTile result="grid" />
            <feComposite in="SourceGraphic" in2="grid" operator="in" />
            <feMorphology operator="dilate" radius={s / 2} />
          </filter>
        </svg>
      ) : null}
      <div style={{ position: "absolute", inset: 0, filter: s > 1 ? `url(#${id})` : undefined }}>{children}</div>
      {noiseOn
        ? Array.from({ length: noise }).map((_, i) => {
            const sz = 3 + Math.floor(rand(i, d, seed) * 4);
            return (
              <div key={i} style={{ position: "absolute", left: rand(i, d, seed + 1) * (w - sz), top: rand(i, d, seed + 2) * (h - sz), width: sz, height: sz,
                background: noiseColor, opacity: 0.35 + rand(i, d, seed + 3) * 0.6 }} />
            );
          })
        : null}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* PIXEL ORBIT (v08): squares burst out of the hero, then orbit slowly  */
/* ------------------------------------------------------------------ */
export const PixelOrbit: React.FC<{
  at: number;
  count?: number;
  rx?: number;
  ry?: number;
  sizes?: [number, number];
  color?: string;
  period?: number;
  burst?: number;
  seed?: number;
  x?: number;
  y?: number;
}> = ({ at, count = 9, rx = 230, ry = 170, sizes = [8, 22], color = "#111", period = 260, burst = 14, seed = 2, x = 0, y = 0 }) => {
  const frame = useCurrentFrame();
  const d = frame - at;
  if (d < 0) return null;
  return (
    <>
      {Array.from({ length: count }).map((_, i) => {
        const st = i * 0.8;
        const t = EASE_PRO.enterSnap(clamp01((d - st) / burst));
        if (t <= 0) return null;
        const a0 = (i / count) * Math.PI * 2 + rand(i, seed) * 0.5;
        const a = a0 + (d / period) * Math.PI * 2;
        const rr = lerp(0.85, 1.15, rand(i, seed, 1));
        const px = x + Math.cos(a) * rx * rr * t;
        const py = y + Math.sin(a) * ry * rr * t;
        const depth = (Math.sin(a) + 1) / 2; // front = lower half
        const sz = lerp(sizes[0], sizes[1], rand(i, seed, 2)) * lerp(0.75, 1.15, depth) * lerp(0.3, 1, t);
        return (
          <div key={i} style={{ position: "absolute", left: "50%", top: "50%", width: sz, height: sz, marginLeft: -sz / 2, marginTop: -sz / 2,
            transform: `translate(${px}px, ${py}px)`, background: color, opacity: clamp01(t * 3) }} />
        );
      })}
    </>
  );
};

/* ------------------------------------------------------------------ */
/* PIXEL DUST (v02 word swap): tiny squares puff off a box and fade     */
/* ------------------------------------------------------------------ */
export const PixelDust: React.FC<{ at: number; box: Box; count?: number; color?: string; dur?: number; dx?: number; dy?: number; size?: [number, number]; seed?: number }> = ({
  at, box, count = 26, color = "#8E8E93", dur = 14, dx = 40, dy = -50, size = [2, 5], seed = 9,
}) => {
  const frame = useCurrentFrame();
  const d = frame - at;
  if (d < 0 || d > dur) return null;
  return (
    <>
      {Array.from({ length: count }).map((_, i) => {
        const st = rand(i, seed) * dur * 0.35;
        const t = clamp01((d - st) / (dur - st));
        if (d < st) return null;
        const e = EASE_PRO.enter(t);
        const sx = box.x + (rand(i, seed, 1) - 0.5) * box.w;
        const sy = box.y + (rand(i, seed, 2) - 0.5) * box.h;
        const px = sx + e * dx * (0.4 + rand(i, seed, 3));
        const py = sy + e * dy * (0.4 + rand(i, seed, 4));
        const sz = lerp(size[0], size[1], rand(i, seed, 5));
        return <div key={i} style={{ position: "absolute", left: "50%", top: "50%", width: sz, height: sz, transform: `translate(${px}px, ${py}px)`, background: color, opacity: (1 - t) * 0.9 }} />;
      })}
    </>
  );
};

/* ------------------------------------------------------------------ */
/* PIXEL GATHER: square cells fly in from around a word on eased paths, */
/* converge INTO the word's box and shrink away while the word sharpens */
/* (pixels that BUILD the word, instead of popping at random places).   */
/* Start the word's own entrance ~60% into `dur`.                       */
/* ------------------------------------------------------------------ */
export const PixelGather: React.FC<{ at: number; box: Box; count?: number; cell?: number; colors?: string[]; dur?: number; spread?: number; seed?: number; reverse?: boolean }> = ({
  at, box, count = 14, cell = 18, colors = ["#0A84FF", "#5AC8FA", "#0040DD"], dur = 16, spread = 170, seed = 5, reverse = false,
}) => {
  const frame = useCurrentFrame();
  const d = frame - at;
  if (d < 0 || d > dur + 8) return null;
  return (
    <>
      {Array.from({ length: count }).map((_, i) => {
        const delay = rand(i, seed) * 6;
        const raw = clamp01((d - delay) / dur);
        if (d < delay) return null;
        const t = reverse ? 1 - EASE_PRO.exit(raw) : EASE_PRO.enter(raw);
        const a = rand(i, seed, 1) * Math.PI * 2;
        const r = spread * (0.45 + rand(i, seed, 2) * 0.55);
        const sx = box.x + Math.cos(a) * (box.w / 2 + r);
        const sy = box.y + Math.sin(a) * (box.h / 2 + r * 0.55);
        const tx = box.x + (rand(i, seed, 3) - 0.5) * box.w * 0.9;
        const ty = box.y + (rand(i, seed, 4) - 0.5) * box.h * 0.6;
        const x = lerp(sx, tx, t);
        const y = lerp(sy, ty, t);
        const sz = cell * lerp(1, 0.3, t);
        const op = clamp01((d - delay) / 3) * (1 - clamp01((t - 0.72) / 0.28));
        if (op <= 0.01) return null;
        return (
          <div key={i} style={{ position: "absolute", left: "50%", top: "50%", width: sz, height: sz, marginLeft: -sz / 2, marginTop: -sz / 2,
            transform: `translate(${x}px, ${y}px)`, background: colors[i % colors.length], opacity: op, borderRadius: sz * 0.12 }} />
        );
      })}
    </>
  );
};
