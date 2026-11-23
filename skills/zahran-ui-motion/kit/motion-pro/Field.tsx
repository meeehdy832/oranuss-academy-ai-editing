import React from "react";
import { interpolateColors, useCurrentFrame } from "remotion";
import { clamp01, lerp } from "./curves";
import { FontSpec, caretX, springFollow } from "./flow";

/*
 * TYPE FIELD: the "bar grows while the text types" beat (v01 v14 v20 v21 v23), done as ONE continuous
 * animation instead of separate steps:
 *   - the container morphs from a seed (dot / selection block / chip) to a pill with a spring,
 *   - typing starts INSIDE the morph (typingStart ~ at + 60% of the growth), never after it,
 *   - the width keeps FOLLOWING the typed text (springFollow) so the bar keeps growing word by word,
 *   - the caret position is exposed (fieldGeom) so a follow-cam can chase it smoothly.
 */
export type FieldCfg = {
  /** morph start */
  at: number;
  /** typing start: put it inside the morph (at + 6..10f) */
  start: number;
  text: string;
  /** characters per frame */
  cpf: number;
  font: FontSpec;
  /** seed geometry the bar grows from */
  from?: { w: number; h: number };
  minW: number;
  h: number;
  /** px from the left edge to the first character (leading icon space) */
  padL: number;
  /** px after the caret to the right edge (trailing button space) */
  padR: number;
  /** stop growing past this width */
  maxW?: number;
  omega?: number;
  zeta?: number;
};

export const fieldGeom = (f: number, c: FieldCfg) => {
  const seed = c.from ?? { w: 30, h: 30 };
  const typed = (g: number) => (g < c.start ? 0 : caretX(g, c.start, c.text, c.cpf, c.font));
  // the spring lags a ramp by 2*zeta/omega frames: aim AHEAD so the bar edge stays just past the caret
  const lead = (2 * (c.zeta ?? 0.78)) / (c.omega ?? 0.3);
  const tgtW = (g: number) => (g < c.at ? seed.w : Math.min(c.maxW ?? 99999, Math.max(c.minW, c.padL + typed(g + lead) + c.font.size * 0.3 + c.padR)));
  const tgtH = (g: number) => (g < c.at ? seed.h : c.h);
  const w = springFollow(f, tgtW, c.at - 1, c.omega ?? 0.3, c.zeta ?? 0.78);
  const h = springFollow(f, tgtH, c.at - 1, (c.omega ?? 0.3) * 1.15, c.zeta ?? 0.78);
  const grow = clamp01((w - seed.w) / Math.max(1, c.minW - seed.w));
  return { w, h, r: h / 2, grow, caret: -w / 2 + c.padL + typed(f) };
};

export const TypeField: React.FC<
  FieldCfg & {
    bg?: string;
    bgFrom?: string;
    shadow?: string;
    ink?: string;
    caretColor?: string;
    caretUntil?: number;
    placeholder?: string;
    left?: React.ReactNode;
    right?: React.ReactNode;
  }
> = (p) => {
  const frame = useCurrentFrame();
  const g = fieldGeom(frame, p);
  const n = frame < p.start ? 0 : Math.max(0, Math.min(p.text.length, Math.floor((frame - p.start) * p.cpf)));
  const typing = n > 0 && n < p.text.length;
  const blink = typing || Math.floor((frame - p.start) / 8) % 2 === 0;
  const showCaret = frame >= p.start - 4 && (p.caretUntil === undefined || frame < p.caretUntil) && blink && g.grow > 0.5;
  const contentOp = clamp01((g.grow - 0.45) / 0.35);
  const bg = p.bgFrom ? interpolateColors(clamp01(g.grow * 1.4), [0, 1], [p.bgFrom, p.bg ?? "#fff"]) : p.bg ?? "#fff";
  const fs = p.font.size;
  return (
    <div style={{ position: "absolute", left: "50%", top: "50%", width: g.w, height: g.h, marginLeft: -g.w / 2, marginTop: -g.h / 2, borderRadius: g.r, background: bg,
      boxShadow: g.grow > 0.2 ? p.shadow : undefined, overflow: "hidden" }}>
      <div style={{ position: "absolute", left: 0, top: 0, height: g.h, width: p.padL, display: "flex", alignItems: "center", justifyContent: "center", opacity: contentOp,
        transform: `scale(${lerp(0.6, 1, contentOp)})` }}>
        {p.left}
      </div>
      <div style={{ position: "absolute", left: p.padL, top: 0, height: g.h, width: Math.max(0, g.w - p.padL - p.padR * 0.6), overflow: "hidden", display: "flex", alignItems: "center", whiteSpace: "pre", fontFamily: p.font.family,
        fontSize: fs, fontWeight: p.font.weight ?? 400, letterSpacing: p.font.letterSpacing ? `${p.font.letterSpacing}em` : undefined, color: p.ink ?? "#111", opacity: contentOp }}>
        {n === 0 && p.placeholder ? <span style={{ color: "#A1A1A6", position: "absolute", left: fs * 0.12 }}>{p.placeholder}</span> : null}
        <span>{p.text.slice(0, n)}</span>
        {showCaret ? <span style={{ display: "inline-block", width: Math.max(2, fs * 0.07), height: fs * 1.05, background: p.caretColor ?? "#0A84FF", marginLeft: fs * 0.04, borderRadius: 2 }} /> : null}
      </div>
      <div style={{ position: "absolute", right: 0, top: 0, height: g.h, width: p.padR, display: "flex", alignItems: "center", justifyContent: "center", opacity: contentOp,
        transform: `scale(${lerp(0.5, 1, contentOp)})` }}>
        {p.right}
      </div>
    </div>
  );
};
