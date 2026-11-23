import React from "react";
import { interpolateColors, useCurrentFrame } from "remotion";
import { EASE_PRO, clamp01, lerp, rand } from "./curves";
import { FontSpec } from "./flow";
import { layoutLine } from "./TextFx";
import { useFxId } from "./Elements";

/*
 * PRO TEXT PRIMITIVES (from the frame-by-frame study of the dnyxstudios Wallet reel, v12, and the
 * pro-vs-AI comparison). These are the DEFAULTS; the TextFx menu adds variety on top.
 */

const fcss = (font: FontSpec): React.CSSProperties => ({
  fontFamily: font.family,
  fontSize: font.size,
  fontWeight: font.weight ?? 400,
  letterSpacing: font.letterSpacing ? `${font.letterSpacing}em` : undefined,
  whiteSpace: "pre",
});

/* ------------------------------------------------------------------ */
/* WORD IN (v12 "you down?"): per word y 20->0, blur 8->0, opacity, and */
/* a skewX that follows the word's SPEED (max at the fastest frame, 0   */
/* at rest) -> sense of speed without extra blur. Expo-out, 18-22f.     */
/* ------------------------------------------------------------------ */
export const WordIn: React.FC<{
  text: string;
  start: number;
  font: FontSpec;
  ink?: string;
  accent?: string;
  keep?: number[];
  every?: number;
  dur?: number;
  dist?: number;
  blur?: number;
  skew?: number;
  gapEm?: number;
  wordStyle?: Record<number, React.CSSProperties>;
  /** exit: words accelerate up (stagger 1.5f), skew + blur grow with speed */
  exitAt?: number;
  exitDur?: number;
  style?: React.CSSProperties;
}> = ({ text, start, font, ink = "#111", accent, keep = [], every = 3, dur = 20, dist = 20, blur = 8, skew = 10, gapEm, wordStyle = {}, exitAt, exitDur = 10, style }) => {
  const frame = useCurrentFrame();
  const L = layoutLine(text, font, gapEm);
  const e = EASE_PRO.enterSnap;
  const slope = 6.25; // max slope of the enterSnap curve, used to normalise speed to 0..1
  return (
    <div style={{ position: "relative", width: L.W, height: L.LH, lineHeight: `${L.LH}px`, ...fcss(font), ...style }}>
      {L.words.map((w, i) => {
        const s = start + i * every;
        const t = clamp01((frame - s) / dur);
        if (frame < s) return null;
        const p = e(t);
        const v = clamp01(((p - e(clamp01((frame - 1 - s) / dur))) * dur) / slope);
        let y = (1 - p) * dist;
        let b = blur * (1 - p);
        let o = clamp01(t / 0.35);
        let sk = -skew * v;
        if (exitAt !== undefined && frame >= exitAt + i * 1.5) {
          const xt = clamp01((frame - exitAt - i * 1.5) / exitDur);
          const xp = EASE_PRO.exit(xt);
          const xv = clamp01((xp - EASE_PRO.exit(clamp01((frame - 1 - exitAt - i * 1.5) / exitDur))) * exitDur / 6.25);
          y -= xp * dist * 1.6;
          b += xp * 12;
          o *= 1 - xp;
          sk += skew * xv;
        }
        const c = accent ? (keep.indexOf(i) >= 0 ? accent : interpolateColors(clamp01((frame - s - dur * 0.35) / 10), [0, 1], [accent, ink])) : ink;
        return (
          <span key={i} style={{ position: "absolute", left: w.x, top: 0, color: c, opacity: o, filter: b > 0.3 ? `blur(${b}px)` : undefined,
            transform: `translateY(${y}px) skewX(${sk}deg)`, transformOrigin: "50% 100%", ...wordStyle[i] }}>
            {w.t}
          </span>
        );
      })}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* LIQUID IN (v12 frames 0-6 "slowing"): a wavy accent smear resolves  */
/* into the word through a liquid displacement that calms down.        */
/* ------------------------------------------------------------------ */
export const LiquidIn: React.FC<{ text: string; start: number; font: FontSpec; ink?: string; accent?: string; dur?: number; strength?: number; style?: React.CSSProperties }> = ({
  text, start, font, ink = "#111", accent = "#2F6BFF", dur = 16, strength = 70, style,
}) => {
  const frame = useCurrentFrame();
  const id = useFxId("liq");
  const L = layoutLine(text, font);
  const t = clamp01((frame - start) / dur);
  if (frame < start) return <div style={{ width: L.W, height: L.LH }} />;
  const p = EASE_PRO.enter(t);
  const S = strength * (1 - p);
  const b = 10 * (1 - EASE_PRO.enterSnap(t));
  const sx = lerp(1.35, 1, p);
  const c = interpolateColors(clamp01((t - 0.35) / 0.5), [0, 1], [accent, ink]);
  return (
    <div style={{ position: "relative", width: L.W, height: L.LH, lineHeight: `${L.LH}px`, ...fcss(font), ...style }}>
      {S > 0.5 ? (
        <svg width={0} height={0} style={{ position: "absolute" }}>
          <filter id={id} x="-30%" y="-80%" width="160%" height="260%">
            <feTurbulence type="fractalNoise" baseFrequency="0.008 0.05" numOctaves={2} seed={3} />
            <feDisplacementMap in="SourceGraphic" scale={S} xChannelSelector="R" yChannelSelector="G" />
            <feGaussianBlur stdDeviation={b.toFixed(2)} />
          </filter>
        </svg>
      ) : null}
      <span style={{ position: "absolute", left: 0, top: 0, color: c, opacity: clamp01(t / 0.2), transform: `scaleX(${sx})`, transformOrigin: "50% 50%",
        filter: S > 0.5 ? `url(#${id})` : b > 0.3 ? `blur(${b}px)` : undefined }}>
        {text}
      </span>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* DECODE (v12 "Bank": Eh -> Cdu -> Bbqr -> Baon -> Banm -> Bank):      */
/* real LETTERS of the same font (never # @ $ { }), <= 8f, hidden under */
/* a blur that clears, settling left -> right.                          */
/* ------------------------------------------------------------------ */
const LOWER = "abcdefghijklmnopqrstuvwxyz";
const UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const DIGIT = "0123456789";
export const Decode: React.FC<{ text: string; start: number; dur?: number; ink?: string; blur?: number; seed?: number; style?: React.CSSProperties }> = ({
  text, start, dur = 8, ink = "#111", blur = 5, seed = 2, style,
}) => {
  const frame = useCurrentFrame();
  const d = frame - start;
  if (d < 0) return <span style={{ opacity: 0, whiteSpace: "pre", ...style }}>{text}</span>;
  const b = blur * (1 - EASE_PRO.enter(clamp01(d / dur)));
  const shownLen = Math.min(text.length, Math.max(1, Math.ceil(text.length * clamp01((d + 2) / (dur * 0.6)))));
  const chars = text.split("").map((ch, i) => {
    if (i >= shownLen) return "";
    const lock = (dur * 0.85 * (i + 1)) / text.length;
    if (d >= lock || ch === " ") return ch;
    const set = UPPER.indexOf(ch) >= 0 ? UPPER : DIGIT.indexOf(ch) >= 0 ? DIGIT : LOWER.indexOf(ch) >= 0 ? LOWER : "";
    if (!set) return ch;
    return set[Math.floor(rand(i, Math.floor(frame), seed) * set.length)];
  });
  return (
    <span style={{ whiteSpace: "pre", color: ink, opacity: clamp01(d / 2), filter: b > 0.3 ? `blur(${b}px)` : undefined, display: "inline-block", ...style }}>
      {chars.join("")}
    </span>
  );
};

/* ------------------------------------------------------------------ */
/* WAVE NUMBER (v12 900 USD -> 770 EUR -> 659 GBP): every character    */
/* lifts on a sine wave with its own delay, blurs and tints to the      */
/* accent at the top of the wave, and swaps glyph at the crest. 12-16f. */
/* ------------------------------------------------------------------ */
export const WaveNumber: React.FC<{ values: Array<{ v: string; at: number }>; dur?: number; stagger?: number; amp?: number; ink?: string; accent?: string; style?: React.CSSProperties }> = ({
  values, dur = 14, stagger = 1.5, amp = 0.16, ink = "#111", accent = "#0A84FF", style,
}) => {
  const frame = useCurrentFrame();
  let idx = 0;
  for (let i = 0; i < values.length; i++) if (frame >= values[i].at) idx = i;
  const cur = values[idx].v;
  const prev = idx > 0 ? values[idx - 1].v : cur;
  const at = values[idx].at;
  const n = Math.max(cur.length, prev.length);
  return (
    <span style={{ display: "inline-flex", alignItems: "baseline", whiteSpace: "pre", fontVariantNumeric: "tabular-nums", ...style }}>
      {Array.from({ length: n }).map((_, i) => {
        const t = idx === 0 ? 1 : EASE_PRO.move(clamp01((frame - at - i * stagger) / dur));
        const lift = Math.sin(Math.PI * t);
        const ch = t < 0.5 ? prev[i] ?? "" : cur[i] ?? "";
        return (
          <span key={i} style={{ display: "inline-block", transform: `translateY(${-lift * amp}em)`, filter: lift > 0.05 ? `blur(${lift * 4}px)` : undefined,
            color: lift > 0.02 ? interpolateColors(lift, [0, 1], [ink, accent]) : ink }}>
            {ch}
          </span>
        );
      })}
    </span>
  );
};

/* ------------------------------------------------------------------ */
/* STACK LINES (v12 17-23: "Bank slowing" is pushed up as "you down?"   */
/* enters): the existing lines MOVE to make room, they never jump.      */
/* ------------------------------------------------------------------ */
export const StackLines: React.FC<{ lines: Array<{ at: number; node: React.ReactNode }>; lineH: number; dur?: number; align?: "center" | "left"; width?: number }> = ({
  lines, lineH, dur = 16, align = "center", width = 1000,
}) => {
  const frame = useCurrentFrame();
  const reveal = lines.map((l) => (frame < l.at ? 0 : EASE_PRO.move(clamp01((frame - l.at) / dur))));
  const H = reveal.reduce((a, r) => a + r * lineH, 0);
  let acc = 0;
  return (
    <div style={{ position: "absolute", left: "50%", top: "50%", width, marginLeft: -width / 2, height: 0 }}>
      {lines.map((l, i) => {
        const y = -H / 2 + acc + lineH / 2;
        acc += reveal[i] * lineH;
        if (frame < l.at) return null;
        return (
          <div key={i} style={{ position: "absolute", left: 0, right: 0, top: y - lineH / 2, height: lineH, display: "flex", alignItems: "center",
            justifyContent: align === "center" ? "center" : "flex-start" }}>
            {l.node}
          </div>
        );
      })}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* WHEEL PICKER (v12 Pay -> Earn -> Apple Wallet): a 3D wheel. The      */
/* active item is sharp and dark; neighbours are rotated away, smaller, */
/* lighter and blurred (focus plane).                                   */
/* ------------------------------------------------------------------ */
export const WheelPicker: React.FC<{ items: React.ReactNode[]; at: number[]; itemH: number; dur?: number; step?: number; width?: number; align?: "left" | "center"; window?: number }> = ({
  items, at, itemH, dur = 16, step = 30, width = 600, align = "left", window = 2.3,
}) => {
  const frame = useCurrentFrame();
  const pos = at.reduce((a, f) => a + EASE_PRO.move(clamp01((frame - f) / dur)), 0);
  const R = itemH / Math.sin((step * Math.PI) / 180); // adjacent items sit ~one row apart
  // neighbours are cut by a soft mask (v12): visible as hints, never colliding with the lines around
  const VH = itemH * window;
  const mask = "linear-gradient(to bottom, transparent 0%, rgba(0,0,0,.55) 22%, black 40%, black 60%, rgba(0,0,0,.55) 78%, transparent 100%)";
  return (
    <div style={{ position: "relative", width, height: itemH }}>
    <div style={{ position: "absolute", left: 0, right: 0, top: (itemH - VH) / 2, height: VH, maskImage: mask, WebkitMaskImage: mask, perspective: 800 }}>
     <div style={{ position: "absolute", left: 0, right: 0, top: (VH - itemH) / 2, height: itemH }}>
      {items.map((it, i) => {
        const d = i - pos;
        if (Math.abs(d) > 2.2) return null;
        const a = d * step;
        const y = Math.sin((a * Math.PI) / 180) * R;
        const z = (Math.cos((a * Math.PI) / 180) - 1) * R;
        const o = clamp01(1 - Math.abs(d) * 0.62);
        const b = Math.min(6, Math.abs(d) * 3.2);
        return (
          <div key={i} style={{ position: "absolute", left: 0, right: 0, top: 0, height: itemH, display: "flex", alignItems: "center",
            justifyContent: align === "center" ? "center" : "flex-start", transform: `translateY(${y}px) translateZ(${z}px) rotateX(${-a}deg)`,
            opacity: o, filter: b > 0.3 ? `blur(${b}px)` : undefined, backfaceVisibility: "hidden" }}>
            {it}
          </div>
        );
      })}
     </div>
    </div>
    </div>
  );
};
