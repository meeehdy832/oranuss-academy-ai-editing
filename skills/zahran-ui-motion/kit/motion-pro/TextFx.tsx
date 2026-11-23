import React from "react";
import { interpolateColors, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EASE_PRO, SPRING_PRO, clamp01, lerp, rand } from "./curves";
import { FontSpec, caretX, measure } from "./flow";
import { useFxId } from "./Elements";

/*
 * TEXT MOTION LIBRARY: one component per technique seen in the 24 refs. RULE: never use the same text
 * technique twice in a row; a 15 s video uses 4-6 different ones (see references/06-text-and-pixels.md).
 *
 * All components lay words out ABSOLUTELY from measured widths (exact positions -> words can fly in from
 * anywhere and land on their true slot). The block is W x LH and centered by the parent.
 */

export type LineLayout = { words: Array<{ t: string; x: number; w: number }>; W: number; LH: number };

export const layoutLine = (text: string, font: FontSpec, gapEm = 0.26): LineLayout => {
  const parts = text.split(" ").filter((s) => s.length);
  const gap = gapEm * font.size;
  let x = 0;
  const words = parts.map((t) => {
    const w = measure(t, font);
    const o = { t, x, w };
    x += w + gap;
    return o;
  });
  return { words, W: Math.max(0, x - gap), LH: font.size * 1.25 };
};

const fontCss = (font: FontSpec): React.CSSProperties => ({
  fontFamily: font.family,
  fontSize: font.size,
  fontWeight: font.weight ?? 400,
  letterSpacing: font.letterSpacing ? `${font.letterSpacing}em` : undefined,
  whiteSpace: "pre",
});

const col = (t: number, from: string | undefined, to: string) => (from ? interpolateColors(clamp01(t), [0, 1], [from, to]) : to);

type Common = {
  text: string;
  start: number;
  font: FontSpec;
  ink?: string;
  /** color a word arrives in before settling to ink (accent) */
  accent?: string;
  /** word indexes that keep the accent */
  keep?: number[];
  every?: number;
  dur?: number;
  gapEm?: number;
  /** per-word style overrides by index (weight, italic, color) */
  wordStyle?: Record<number, React.CSSProperties>;
  style?: React.CSSProperties;
};

const Line: React.FC<{ L: LineLayout; font: FontSpec; style?: React.CSSProperties; children: React.ReactNode }> = ({ L, font, style, children }) => (
  <div style={{ position: "relative", width: L.W, height: L.LH, lineHeight: `${L.LH}px`, ...fontCss(font), ...style }}>{children}</div>
);

const settleColor = (frame: number, s: number, dur: number, i: number, ink: string, accent?: string, keep: number[] = []) =>
  accent ? (keep.indexOf(i) >= 0 ? accent : col((frame - s - dur * 0.45) / 10, accent, ink)) : ink;

/* ------------------------------------------------------------------ */
/* BLUR IN (v18 v21 v23 v11 v07): word by word, translucent/gray ->ink, */
/* blur -> sharp, NO rise. Calm and premium; let the camera carry motion */
/* ------------------------------------------------------------------ */
export const BlurIn: React.FC<Common & { from?: string; blur?: number; dx?: number; scaleFrom?: number; unit?: "word" | "letter"; exitAt?: number }> = ({
  text, start, font, ink = "#111", accent, keep, every = 5, dur = 12, gapEm, wordStyle = {}, style, from, blur = 14, dx = 0, scaleFrom = 1, unit = "word", exitAt,
}) => {
  const frame = useCurrentFrame();
  const L = layoutLine(text, font, gapEm);
  let k = 0;
  return (
    <Line L={L} font={font} style={style}>
      {L.words.map((w, i) => {
        const pieces = unit === "letter" ? w.t.split("").map((ch, j) => ({ ch, x: w.x + measure(w.t.slice(0, j), font) })) : [{ ch: w.t, x: w.x }];
        return pieces.map((p, j) => {
          const s = start + (k++) * every;
          const t = clamp01((frame - s) / dur);
          const op = clamp01((frame - s) / (dur * 0.35));
          const b = blur * (1 - EASE_PRO.enterSnap(clamp01((frame - s) / (dur * 0.7))));
          const e = EASE_PRO.enter(t);
          let c = settleColor(frame, s, dur, i, ink, accent, keep);
          if (from) c = col((frame - s) / (dur * 0.9), from, c);
          let o = op;
          let eb = b;
          let ey = 0;
          if (exitAt !== undefined) {
            const xt = EASE_PRO.exit(clamp01((frame - exitAt - i * 1.5) / 10));
            o *= 1 - xt;
            eb += xt * 16;
            ey = -xt * font.size * 0.4;
          }
          if (o <= 0.001) return null;
          return (
            <span key={i + "_" + j} style={{ position: "absolute", left: p.x, top: 0, color: c, opacity: o, filter: eb > 0.3 ? `blur(${eb}px)` : undefined,
              transform: `translate(${(1 - e) * dx}px, ${ey}px) scale(${lerp(scaleFrom, 1, e)})`, transformOrigin: "0% 60%", ...wordStyle[i] }}>
              {p.ch}
            </span>
          );
        });
      })}
    </Line>
  );
};

/* ------------------------------------------------------------------ */
/* RISE + TILT (v06 "Ready to level up"): from below-left, rotated,     */
/* heavily blurred, accent -> ink. Energetic hooks.                    */
/* ------------------------------------------------------------------ */
export const RiseTilt: React.FC<Common & { dist?: number; tilt?: number; blur?: number }> = ({
  text, start, font, ink = "#111", accent, keep, every = 6, dur = 16, gapEm, wordStyle = {}, style, dist, tilt = -12, blur = 18,
}) => {
  const frame = useCurrentFrame();
  const L = layoutLine(text, font, gapEm);
  const D = dist ?? font.size * 0.9;
  return (
    <Line L={L} font={font} style={style}>
      {L.words.map((w, i) => {
        const s = start + i * every;
        const e = EASE_PRO.enter(clamp01((frame - s) / dur));
        const op = clamp01((frame - s) / (dur * 0.3));
        if (op <= 0) return null;
        const b = blur * (1 - EASE_PRO.enterSnap(clamp01((frame - s) / (dur * 0.65))));
        return (
          <span key={i} style={{ position: "absolute", left: w.x, top: 0, opacity: op, color: settleColor(frame, s, dur, i, ink, accent, keep),
            filter: b > 0.3 ? `blur(${b}px)` : undefined, transformOrigin: "0% 100%",
            transform: `translate(${-(1 - e) * D * 0.35}px, ${(1 - e) * D}px) rotate(${(1 - e) * tilt}deg)`, ...wordStyle[i] }}>
            {w.t}
          </span>
        );
      })}
    </Line>
  );
};

/* ------------------------------------------------------------------ */
/* CONVERGE (v22 "Go from an idea", v09 "All your health data"):        */
/* words start scattered at different heights/offsets and LAND in line; */
/* optional code glyphs drift in and dissolve into the sentence.        */
/* ------------------------------------------------------------------ */
export const Converge: React.FC<Common & { spreadX?: number; spreadY?: number; glyphs?: number; glyphColor?: string; seed?: number }> = ({
  text, start, font, ink = "#111", accent, keep, every = 3, dur = 18, gapEm, wordStyle = {}, style, spreadX, spreadY, glyphs = 0, glyphColor = "#0A84FF", seed = 3,
}) => {
  const frame = useCurrentFrame();
  const L = layoutLine(text, font, gapEm);
  const SX = spreadX ?? font.size * 1.2;
  const SY = spreadY ?? font.size * 1.1;
  const G = "/01+<>{}#";
  return (
    <Line L={L} font={font} style={style}>
      {Array.from({ length: glyphs }).map((_, g) => {
        const s = start - 6 + rand(g, seed, 9) * 8;
        const t = clamp01((frame - s) / (dur + 6));
        if (t <= 0 || t >= 1) return null;
        const gx = (rand(g, seed, 1) - 0.5) * (L.W + SX * 3);
        const gy = (rand(g, seed, 2) - 0.5) * SY * 3;
        const e = EASE_PRO.enter(t);
        const tx = lerp(gx, L.W / 2 + (rand(g, seed, 3) - 0.5) * L.W * 0.6, e);
        const ty = lerp(gy, 0, e);
        return (
          <span key={"g" + g} style={{ position: "absolute", left: 0, top: 0, transform: `translate(${tx}px, ${ty}px) scale(${lerp(0.8, 0.4, e)})`,
            color: g % 2 ? glyphColor : ink, opacity: Math.sin(Math.PI * t) * 0.9, fontWeight: 500 }}>
            {G[Math.floor(rand(g, seed, 4) * G.length)]}
          </span>
        );
      })}
      {L.words.map((w, i) => {
        const order = Math.floor(rand(i, seed, 5) * 100) / 100;
        const s = start + Math.round(order * every * L.words.length);
        const e = EASE_PRO.enter(clamp01((frame - s) / dur));
        const op = clamp01((frame - s) / 5);
        if (op <= 0) return null;
        const ox = (rand(i, seed, 6) - 0.5) * 2 * SX;
        const oy = (rand(i, seed, 7) < 0.5 ? -1 : 1) * (0.35 + rand(i, seed, 8) * 0.65) * SY;
        const b = 8 * (1 - EASE_PRO.enterSnap(clamp01((frame - s) / (dur * 0.5))));
        return (
          <span key={i} style={{ position: "absolute", left: w.x, top: 0, opacity: op, color: settleColor(frame, s, dur, i, ink, accent, keep),
            filter: b > 0.3 ? `blur(${b}px)` : undefined, transform: `translate(${(1 - e) * ox}px, ${(1 - e) * oy}px) scale(${lerp(0.82, 1, e)})`, ...wordStyle[i] }}>
            {w.t}
          </span>
        );
      })}
    </Line>
  );
};

/* ------------------------------------------------------------------ */
/* EMERGE (v08 "Ready to create" slides out from behind the mascot):    */
/* every word starts at `originX` (hidden behind a hero drawn on top)   */
/* and slides to its slot with horizontal motion blur.                  */
/* ------------------------------------------------------------------ */
export const Emerge: React.FC<Common & { originX?: number }> = ({
  text, start, font, ink = "#111", accent, keep, every = 3, dur = 16, gapEm, wordStyle = {}, style, originX,
}) => {
  const frame = useCurrentFrame();
  const id = useFxId("em");
  const L = layoutLine(text, font, gapEm);
  const O = originX ?? L.W / 2;
  return (
    <Line L={L} font={font} style={style}>
      {L.words.map((w, i) => {
        const s = start + i * every;
        const pos = (f: number) => lerp(O - w.w / 2, w.x, EASE_PRO.enter(clamp01((f - s) / dur)));
        const x = pos(frame);
        const v = Math.abs(x - pos(frame - 1));
        const b = Math.max(0, v - 4) * 0.5;
        const op = clamp01((frame - s) / 4);
        if (op <= 0) return null;
        return (
          <React.Fragment key={i}>
            {b > 0.3 ? (
              <svg width={0} height={0} style={{ position: "absolute" }}>
                <filter id={id + i} x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation={`${b.toFixed(2)} 0`} /></filter>
              </svg>
            ) : null}
            <span style={{ position: "absolute", left: 0, top: 0, transform: `translateX(${x}px)`, opacity: op, color: settleColor(frame, s, dur, i, ink, accent, keep),
              filter: b > 0.3 ? `url(#${id + i})` : undefined, ...wordStyle[i] }}>
              {w.t}
            </span>
          </React.Fragment>
        );
      })}
    </Line>
  );
};

/* ------------------------------------------------------------------ */
/* WIPE REVEAL (v20 mascot wipes the text in): a soft edge travels and  */
/* reveals the line; draw your wiper object at edgeX(frame).            */
/* ------------------------------------------------------------------ */
export const wipeEdge = (frame: number, at: number, dur: number, W: number, feather = 60) =>
  lerp(-feather, W + feather, EASE_PRO.move(clamp01((frame - at) / dur)));

export const WipeReveal: React.FC<Common & { feather?: number; slide?: number }> = ({ text, start, font, ink = "#111", dur = 24, gapEm, wordStyle = {}, style, feather = 60, slide = 24, accent, keep }) => {
  const frame = useCurrentFrame();
  const L = layoutLine(text, font, gapEm);
  const edge = wipeEdge(frame, start, dur, L.W, feather);
  const mask = `linear-gradient(to right, black ${edge - feather}px, transparent ${edge}px)`;
  return (
    <Line L={L} font={font} style={{ ...style, maskImage: mask, WebkitMaskImage: mask }}>
      {L.words.map((w, i) => {
        const local = clamp01((edge - w.x) / (w.w + feather));
        return (
          <span key={i} style={{ position: "absolute", left: w.x, top: 0, transform: `translateX(${-(1 - EASE_PRO.enter(local)) * slide}px)`,
            color: accent ? (keep && keep.indexOf(i) >= 0 ? accent : col(local * 1.6 - 0.6, accent, ink)) : ink, ...wordStyle[i] }}>
            {w.t}
          </span>
        );
      })}
    </Line>
  );
};

/* ------------------------------------------------------------------ */
/* WORD WAVE (v15 song title): words pop in with vertical offsets and a */
/* springy bounce (playful, music, results).                            */
/* ------------------------------------------------------------------ */
export const WordWave: React.FC<Common & { amp?: number }> = ({ text, start, font, ink = "#111", accent, keep, every = 3, gapEm, wordStyle = {}, style, amp }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = layoutLine(text, font, gapEm);
  const A = amp ?? font.size * 0.7;
  return (
    <Line L={L} font={font} style={style}>
      {L.words.map((w, i) => {
        const s = start + i * every;
        if (frame < s) return null;
        const sp = spring({ frame: frame - s, fps, config: SPRING_PRO.pop });
        const dir = i % 2 === 0 ? 1 : -0.7;
        const op = clamp01((frame - s) / 3);
        return (
          <span key={i} style={{ position: "absolute", left: w.x, top: 0, opacity: op, color: settleColor(frame, s, 10, i, ink, accent, keep),
            transform: `translateY(${(1 - sp) * A * dir}px) scale(${lerp(0.6, 1, sp)})`, transformOrigin: "50% 70%", ...wordStyle[i] }}>
            {w.t}
          </span>
        );
      })}
    </Line>
  );
};

/* ------------------------------------------------------------------ */
/* DROP IN (v11 "it'll work, trust"): words fall from above, big ->    */
/* normal with an overshoot; pair with UnderlineDraw on the key word.   */
/* ------------------------------------------------------------------ */
export const DropIn: React.FC<Common & { dist?: number; scaleFrom?: number }> = ({ text, start, font, ink = "#111", accent, keep, every = 5, gapEm, wordStyle = {}, style, dist, scaleFrom = 1.35 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = layoutLine(text, font, gapEm);
  const D = dist ?? font.size * 1.1;
  return (
    <Line L={L} font={font} style={style}>
      {L.words.map((w, i) => {
        const s = start + i * every;
        if (frame < s) return null;
        const sp = spring({ frame: frame - s, fps, config: SPRING_PRO.morph });
        const b = 10 * (1 - clamp01((frame - s) / 7));
        return (
          <span key={i} style={{ position: "absolute", left: w.x, top: 0, opacity: clamp01((frame - s) / 3), color: settleColor(frame, s, 10, i, ink, accent, keep),
            filter: b > 0.3 ? `blur(${b}px)` : undefined, transformOrigin: "50% 100%",
            transform: `translateY(${-(1 - sp) * D}px) scale(${lerp(scaleFrom, 1, sp)}) rotate(${(1 - sp) * (i % 2 ? 4 : -4)}deg)`, ...wordStyle[i] }}>
            {w.t}
          </span>
        );
      })}
    </Line>
  );
};

/* ------------------------------------------------------------------ */
/* SWAP LINE (v18 "find everyone" -> "with find my"): old words leave  */
/* up one by one while new words rise in with varied offsets (overlap). */
/* ------------------------------------------------------------------ */
export const SwapLine: React.FC<{ from: string; to: string; at: number; font: FontSpec; ink?: string; accent?: string; every?: number; dur?: number; overlap?: number; gapEm?: number; style?: React.CSSProperties }> = ({
  from, to, at, font, ink = "#111", accent, every = 2, dur = 12, overlap = 5, gapEm, style,
}) => {
  const frame = useCurrentFrame();
  const A = layoutLine(from, font, gapEm);
  const B = layoutLine(to, font, gapEm);
  const W = Math.max(A.W, B.W);
  const D = font.size * 0.8;
  const tB = at + overlap;
  // container width morphs between the two lines (smooth)
  const cw = lerp(A.W, B.W, EASE_PRO.move(clamp01((frame - tB) / (dur + B.words.length * every))));
  return (
    <div style={{ position: "relative", width: W, height: A.LH, lineHeight: `${A.LH}px`, ...fontCss(font), ...style }}>
      {A.words.map((w, i) => {
        const x = EASE_PRO.exit(clamp01((frame - at - i * every) / (dur * 0.8)));
        if (x >= 1) return null;
        return (
          <span key={"a" + i} style={{ position: "absolute", left: (W - cw) / 2 + w.x * (cw / A.W), top: 0, color: ink, opacity: 1 - x,
            filter: x > 0.02 ? `blur(${x * 12}px)` : undefined, transform: `translateY(${-x * D}px)` }}>
            {w.t}
          </span>
        );
      })}
      {B.words.map((w, i) => {
        const s = tB + i * every;
        const e = EASE_PRO.enter(clamp01((frame - s) / dur));
        const op = clamp01((frame - s) / (dur * 0.35));
        if (op <= 0) return null;
        const off = D * (0.7 + (i % 3) * 0.35);
        return (
          <span key={"b" + i} style={{ position: "absolute", left: (W - cw) / 2 + w.x * (cw / B.W), top: 0, opacity: op, color: settleColor(frame, s, dur, i, ink, accent),
            filter: e < 0.7 ? `blur(${(1 - e / 0.7) * 10}px)` : undefined, transform: `translateY(${(1 - e) * off}px)` }}>
            {w.t}
          </span>
        );
      })}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* SMEAR IN / OUT (v09 "together", v11 wordmark exit): a fast slide with */
/* horizontal stretch + directional blur on the fastest frames.         */
/* ------------------------------------------------------------------ */
export const Smear: React.FC<{ text: string; at: number; font: FontSpec; ink?: string; dur?: number; dist?: number; mode?: "in" | "out"; dir?: 1 | -1; style?: React.CSSProperties }> = ({
  text, at, font, ink = "#111", dur = 10, dist = 260, mode = "in", dir = 1, style,
}) => {
  const frame = useCurrentFrame();
  const id = useFxId("sm");
  const ease = mode === "in" ? EASE_PRO.enterSnap : EASE_PRO.exitHard;
  const xAt = (f: number) => {
    const t = ease(clamp01((f - at) / dur));
    return mode === "in" ? (1 - t) * dist * dir : t * dist * dir;
  };
  const x = xAt(frame);
  const v = Math.abs(x - xAt(frame - 1));
  const b = Math.min(40, Math.max(0, v - 3) * 0.6);
  const sx = 1 + Math.min(0.9, v / 120);
  const op = mode === "in" ? clamp01((frame - at) / 3) : 1 - clamp01((frame - at - dur + 2) / 2);
  const L = layoutLine(text, font);
  if (op <= 0) return <div style={{ width: L.W, height: L.LH }} />;
  return (
    <div style={{ position: "relative", width: L.W, height: L.LH, lineHeight: `${L.LH}px`, ...fontCss(font), ...style }}>
      {b > 0.3 ? (
        <svg width={0} height={0} style={{ position: "absolute" }}>
          <filter id={id} x="-60%" y="-20%" width="220%" height="140%"><feGaussianBlur stdDeviation={`${b.toFixed(2)} 0`} /></filter>
        </svg>
      ) : null}
      <span style={{ position: "absolute", left: 0, top: 0, color: ink, opacity: op, transform: `translateX(${x}px) scaleX(${sx})`, transformOrigin: dir > 0 ? "100% 50%" : "0% 50%",
        filter: b > 0.3 ? `url(#${id})` : undefined }}>
        {text}
      </span>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* TRACK IN (v06 "Choose Your Gender"): tracking collapses + size settle */
/* ------------------------------------------------------------------ */
export const TrackIn: React.FC<{ text: string; at: number; font: FontSpec; ink?: string; dur?: number; fromEm?: number; style?: React.CSSProperties }> = ({
  text, at, font, ink = "#111", dur = 18, fromEm = 0.22, style,
}) => {
  const frame = useCurrentFrame();
  const e = EASE_PRO.enter(clamp01((frame - at) / dur));
  const op = clamp01((frame - at) / (dur * 0.35));
  const b = 12 * (1 - EASE_PRO.enterSnap(clamp01((frame - at) / (dur * 0.6))));
  const ls = lerp(fromEm, font.letterSpacing ?? 0, e);
  return (
    <span style={{ ...fontCss(font), letterSpacing: `${ls}em`, color: ink, opacity: op, display: "inline-block", filter: b > 0.3 ? `blur(${b}px)` : undefined,
      transform: `scale(${lerp(1.12, 1, e)})`, ...style }}>
      {text}
    </span>
  );
};

/* ------------------------------------------------------------------ */
/* BLOB -> WORD (v04 "Have"): a liquid accent blob flies in, stretches  */
/* into the word's shape and dissolves into the (blurred -> sharp) word. */
/* ------------------------------------------------------------------ */
export const BlobToWord: React.FC<{ text: string; at: number; font: FontSpec; ink?: string; accent?: string; dur?: number; from?: { x: number; y: number }; style?: React.CSSProperties }> = ({
  text, at, font, ink = "#111", accent = "#4B5BFF", dur = 18, from = { x: -40, y: 40 }, style,
}) => {
  const frame = useCurrentFrame();
  const L = layoutLine(text, font);
  const d = frame - at;
  const p1 = EASE_PRO.enter(clamp01(d / (dur * 0.45)));
  const p2 = EASE_PRO.move(clamp01((d - dur * 0.25) / (dur * 0.45)));
  const p3 = clamp01((d - dur * 0.45) / (dur * 0.55));
  const bw = lerp(font.size * 0.62, L.W * 0.92, p2);
  const bh = lerp(font.size * 0.62, font.size * 0.6, p2);
  const bx = lerp(L.W / 2 + from.x, L.W / 2, p1) - bw / 2;
  const by = lerp(L.LH / 2 + from.y, L.LH / 2, p1) - bh / 2;
  const blobOp = d < 0 ? 0 : clamp01(d / 3) * (1 - EASE_PRO.enter(p3));
  const wb = 14 * (1 - EASE_PRO.enterSnap(p3));
  return (
    <div style={{ position: "relative", width: L.W, height: L.LH, lineHeight: `${L.LH}px`, ...fontCss(font), ...style }}>
      {blobOp > 0.01 ? (
        <div style={{ position: "absolute", left: bx, top: by, width: bw, height: bh, borderRadius: bh, background: accent, opacity: blobOp,
          filter: `blur(${lerp(1, 9, p2)}px)`, transform: `skewX(${-12 * p2 * (1 - p3)}deg)` }} />
      ) : null}
      {blobOp > 0.01 && p2 < 0.9 ? (
        <div style={{ position: "absolute", left: lerp(L.W / 2 + from.x * 1.8, bx + bw * 0.85, EASE_PRO.enter(clamp01((d - 2) / (dur * 0.5)))) - font.size * 0.14,
          top: lerp(L.LH / 2 + from.y * 1.6, L.LH / 2, EASE_PRO.enter(clamp01((d - 2) / (dur * 0.5)))) - font.size * 0.14, width: font.size * 0.28, height: font.size * 0.28,
          borderRadius: font.size, background: accent, opacity: blobOp * clamp01((d - 2) / 3), filter: "blur(2px)" }} />
      ) : null}
      {p3 > 0 ? (
        <span style={{ position: "absolute", left: 0, top: 0, opacity: clamp01(p3 * 2.5), color: col((d - dur) / 12, accent, ink), filter: wb > 0.3 ? `blur(${wb}px)` : undefined }}>{text}</span>
      ) : null}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* SELECT -> REPLACE (v03 "Stop Scrolling." -> "Start Showing up.",     */
/* v05 query -> "Use Concerta."): a solid block selects the old line,   */
/* collapses into a block caret, the new line types behind it.          */
/* ------------------------------------------------------------------ */
export const SelectReplace: React.FC<{ from: string; to: string; at: number; font: FontSpec; ink?: string; color?: string; selDur?: number; hold?: number; cpf?: number; caretUntil?: number; style?: React.CSSProperties }> = ({
  from, to, at, font, ink = "#111", color = "#0A84FF", selDur = 7, hold = 4, cpf = 0.9, caretUntil, style,
}) => {
  const frame = useCurrentFrame();
  const A = layoutLine(from, font);
  const B = layoutLine(to, font);
  const W = Math.max(A.W, B.W);
  const LH = A.LH;
  const caretW = font.size * 0.5;
  const tColl = at + selDur + hold;
  const tType = tColl + 5;
  // block geometry: sweep over old text -> collapse to caret -> ride the typed text (spring-smoothed)
  const sel = EASE_PRO.enterSnap(clamp01((frame - at) / selDur));
  const coll = EASE_PRO.move(clamp01((frame - tColl) / 8));
  const typedN = (f: number) => Math.max(0, Math.min(to.length, Math.floor((f - tType) * cpf)));
  // the block caret sits exactly at the end of the typed text (continuous inside each character)
  const cx = frame < tType ? 0 : caretX(frame, tType, to, cpf, font);
  const offA = (W - A.W) / 2;
  const offB = (W - B.W) / 2;
  const blockX = frame < tColl ? offA : lerp(offA, offB, coll) + cx;
  const blockW = frame < tColl ? A.W * sel : lerp(A.W, caretW, coll);
  const showOld = frame < tColl + 2;
  const n = typedN(frame);
  const done = caretUntil !== undefined && frame >= caretUntil;
  const blink = n >= to.length && Math.floor((frame - tType) / 9) % 2 === 1;
  return (
    <div style={{ position: "relative", width: W, height: LH, lineHeight: `${LH}px`, ...fontCss(font), ...style }}>
      {showOld ? <span style={{ position: "absolute", left: offA, top: 0, color: ink, opacity: frame < tColl ? 1 : 0 }}>{from}</span> : null}
      {n > 0 ? <span style={{ position: "absolute", left: offB, top: 0, color: ink }}>{to.slice(0, n)}</span> : null}
      {frame >= at && !done && !blink ? (
        <div style={{ position: "absolute", left: blockX, top: LH * 0.12, width: Math.max(2, blockW), height: LH * 0.76, background: color, borderRadius: font.size * 0.06,
          mixBlendMode: frame < tColl ? "multiply" : undefined, opacity: frame < tColl ? 0.9 : 1 }} />
      ) : null}
      {frame >= at && frame < tColl ? (
        <span style={{ position: "absolute", left: offA, top: 0, color: "#fff", clipPath: `inset(0 ${(1 - sel) * 100}% 0 0)` }}>{from}</span>
      ) : null}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* GUIDE MARKS (v09 "sense"): design crosshairs + guide lines draw     */
/* around a key word (technical, precise, "making sense").             */
/* ------------------------------------------------------------------ */
export const GuideMarks: React.FC<{ at: number; w: number; h: number; color?: string; dur?: number; hold?: number; ext?: number }> = ({ at, w, h, color = "#5CE1B5", dur = 8, hold = 30, ext = 40 }) => {
  const frame = useCurrentFrame();
  const d = frame - at;
  if (d < 0) return null;
  const t = EASE_PRO.enter(clamp01(d / dur));
  const o = 1 - clamp01((d - dur - hold) / 10);
  if (o <= 0) return null;
  const plus = (x: number, y: number, k: number) => (
    <div key={k} style={{ position: "absolute", left: x - 9, top: y - 9, width: 18, height: 18, transform: `scale(${t}) rotate(${(1 - t) * 90}deg)` }}>
      <div style={{ position: "absolute", left: 8, top: 0, width: 2, height: 18, background: color }} />
      <div style={{ position: "absolute", left: 0, top: 8, width: 18, height: 2, background: color }} />
    </div>
  );
  return (
    <div style={{ position: "absolute", left: "50%", top: "50%", width: w, height: h, marginLeft: -w / 2, marginTop: -h / 2, opacity: o, pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: -ext * t, right: -ext * t, top: 0, height: 1, background: color, opacity: 0.6 }} />
      <div style={{ position: "absolute", left: -ext * t, right: -ext * t, bottom: 0, height: 1, background: color, opacity: 0.6 }} />
      <div style={{ position: "absolute", top: -ext * t, bottom: -ext * t, left: 0, width: 1, background: color, opacity: 0.6 }} />
      <div style={{ position: "absolute", top: -ext * t, bottom: -ext * t, right: 0, width: 1, background: color, opacity: 0.6 }} />
      {plus(0, 0, 0)}
      {plus(w, 0, 1)}
      {plus(0, h, 2)}
      {plus(w, h, 3)}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* CUT SEQUENCE (v13 "Calendar / Plan / Plan Smarter.", v19 "inspo?"):  */
/* hard typographic cuts on beats, with 1f inverted flicker frames.     */
/* ------------------------------------------------------------------ */
export const CutSequence: React.FC<{
  cuts: Array<{ at: number; text: string; bg: string; color: string; size?: number; weight?: number }>;
  flicker?: number[];
  family: string;
  /** slow push on every card (refs never hold a dead frame) */
  push?: number;
}> = ({ cuts, flicker = [], family, push = 0.0025 }) => {
  const frame = useCurrentFrame();
  let idx = -1;
  for (let i = 0; i < cuts.length; i++) if (frame >= cuts[i].at) idx = i;
  if (idx < 0) return null;
  const c = cuts[idx];
  const inv = flicker.indexOf(frame) >= 0;
  const z = 1 + (frame - c.at) * push;
  return (
    <div style={{ position: "absolute", inset: 0, background: inv ? c.color : c.bg, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <span style={{ fontFamily: family, fontSize: c.size ?? 64, fontWeight: c.weight ?? 600, color: inv ? c.bg : c.color, letterSpacing: "-0.03em", transform: `scale(${z})` }}>{c.text}</span>
    </div>
  );
};

/** Lerp helper for scenes that want a word's measured box (for PixelSparkle, GuideMarks, Underline...). */
export const wordBox = (text: string, wordIndex: number, font: FontSpec, gapEm?: number) => {
  const L = layoutLine(text, font, gapEm);
  const w = L.words[wordIndex];
  return { x: w.x + w.w / 2 - L.W / 2, y: 0, w: w.w, h: font.size * 0.8, lineW: L.W };
};
