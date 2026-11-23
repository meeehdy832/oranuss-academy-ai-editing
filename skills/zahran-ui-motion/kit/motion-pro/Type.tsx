import React from "react";
import { interpolateColors, useCurrentFrame } from "remotion";
import { EASE_PRO, clamp01, lerp, rand } from "./curves";

/* ------------------------------------------------------------------ */
/* TYPE LINE: typing with caret (bar or block), refs v01 v05 v14 v21 v23 */
/* ------------------------------------------------------------------ */
export const typedCount = (frame: number, start: number, text: string, cpf = 0.6) =>
  Math.max(0, Math.min(text.length, Math.floor((frame - start) * cpf)));

/** Rough width estimate for follow-cam (avg glyph ≈ 0.52em for Inter). */
export const textWidth = (text: string, fontSize: number, em = 0.52) => text.length * fontSize * em;

export const TypeLine: React.FC<{
  text: string;
  start: number;
  /** characters per frame (0.5-2 fast UI typing; 0.35 human) */
  cpf?: number;
  caret?: "bar" | "block" | "none";
  caretColor?: string;
  /** hide the caret after this frame */
  caretUntil?: number;
  placeholder?: string;
  placeholderColor?: string;
  style?: React.CSSProperties;
}> = ({ text, start, cpf = 0.6, caret = "bar", caretColor = "#0A84FF", caretUntil, placeholder, placeholderColor = "#A1A1A6", style }) => {
  const frame = useCurrentFrame();
  const n = typedCount(frame, start, text, cpf);
  const typing = frame >= start && n < text.length;
  const blinkOn = typing || Math.floor((frame - start) / 8) % 2 === 0;
  const showCaret = caret !== "none" && frame >= start - 6 && (caretUntil === undefined || frame < caretUntil) && blinkOn;
  const fs = typeof style?.fontSize === "number" ? style.fontSize : 40;
  return (
    <span style={{ whiteSpace: "pre", display: "inline-flex", alignItems: "center", ...style }}>
      {n === 0 && placeholder ? <span style={{ color: placeholderColor }}>{placeholder}</span> : null}
      <span>{text.slice(0, n)}</span>
      {showCaret ? (
        caret === "bar" ? (
          <span style={{ display: "inline-block", width: Math.max(2, fs * 0.07), height: fs * 1.05, background: caretColor, marginLeft: fs * 0.04, borderRadius: 2 }} />
        ) : (
          <span style={{ display: "inline-block", width: fs * 0.55, height: fs * 1.0, background: caretColor, marginLeft: fs * 0.05, borderRadius: fs * 0.08 }} />
        )
      ) : null}
    </span>
  );
};

/* ------------------------------------------------------------------ */
/* WORD RISE: words appear one by one, accent color settles to ink      */
/* refs v06 v08 v09 v11                                                 */
/* ------------------------------------------------------------------ */
export const WordRise: React.FC<{
  text: string;
  start: number;
  every?: number;
  dur?: number;
  dist?: number;
  blur?: number;
  ink?: string;
  accent?: string;
  /** frames for accent -> ink settle */
  settle?: number;
  /** words (by index) that keep the accent color */
  keepAccent?: number[];
  /** exit: all words leave starting at this frame (stagger 1f, accelerate up) */
  exitAt?: number;
  gap?: number;
  style?: React.CSSProperties;
}> = ({ text, start, every = 6, dur = 10, dist = 26, blur = 10, ink = "#111", accent, settle = 10, keepAccent = [], exitAt, gap = 0.28, style }) => {
  const frame = useCurrentFrame();
  const words = text.split(" ");
  return (
    <span style={{ display: "inline-flex", flexWrap: "wrap", justifyContent: "center", columnGap: `${gap}em`, ...style }}>
      {words.map((w, i) => {
        const s = start + i * every;
        const t = clamp01((frame - s) / dur);
        const e = EASE_PRO.enterSnap(t);
        const op = clamp01((frame - s) / (dur * 0.35));
        const b = blur * (1 - EASE_PRO.enterSnap(clamp01((frame - s) / (dur * 0.65))));
        let col = ink;
        if (accent) {
          col = keepAccent.indexOf(i) >= 0 ? accent : interpolateColors(clamp01((frame - s - dur * 0.4) / settle), [0, 1], [accent, ink]);
        }
        let y = (1 - e) * dist;
        let o = op;
        let eb = b;
        if (exitAt !== undefined) {
          const xt = EASE_PRO.exit(clamp01((frame - exitAt - i) / 9));
          y -= xt * dist * 2;
          o *= 1 - xt;
          eb += xt * 12;
        }
        return (
          <span key={i} style={{ display: "inline-block", transform: `translateY(${y}px)`, opacity: o, filter: eb > 0.3 ? `blur(${eb}px)` : undefined, color: col }}>
            {w}
          </span>
        );
      })}
    </span>
  );
};

/* ------------------------------------------------------------------ */
/* RANDOM REVEAL (v09): letters appear in random order                  */
/* ------------------------------------------------------------------ */
export const RandomReveal: React.FC<{ text: string; start: number; dur?: number; seed?: number; accent?: string; ink?: string; style?: React.CSSProperties }> = ({
  text, start, dur = 12, seed = 5, accent, ink = "#111", style,
}) => {
  const frame = useCurrentFrame();
  return (
    <span style={{ whiteSpace: "pre", ...style }}>
      {text.split("").map((ch, i) => {
        const at = start + rand(i, seed) * dur;
        const op = clamp01((frame - at) / 2);
        const col = accent ? interpolateColors(clamp01((frame - start - dur) / 10), [0, 1], [accent, ink]) : ink;
        return <span key={i} style={{ opacity: op, color: col }}>{ch}</span>;
      })}
    </span>
  );
};

/* ------------------------------------------------------------------ */
/* SCRAMBLE / DECODER (v08 "for free")                                  */
/* ------------------------------------------------------------------ */
const GLYPHS = "!<>-_\\/[]{}=+*^?#%&$@01ABCDEFabcdef";
export const Scramble: React.FC<{ text: string; start: number; dur?: number; stagger?: number; ink?: string; accent?: string; style?: React.CSSProperties }> = ({
  text, start, dur = 12, stagger = 1, ink = "#111", accent = "#2D5BD7", style,
}) => {
  const frame = useCurrentFrame();
  return (
    <span style={{ whiteSpace: "pre", fontVariantNumeric: "tabular-nums", ...style }}>
      {text.split("").map((ch, i) => {
        const lockAt = start + dur + i * stagger;
        if (frame < start + i * stagger * 0.5) return <span key={i} style={{ opacity: 0 }}>{ch}</span>;
        if (frame >= lockAt || ch === " ") return <span key={i} style={{ color: ink }}>{ch}</span>;
        const g = GLYPHS[Math.floor(rand(i, frame, 9) * GLYPHS.length)];
        return <span key={i} style={{ color: accent }}>{g}</span>;
      })}
    </span>
  );
};

/* ------------------------------------------------------------------ */
/* ODOMETER (v12 amounts, v16 time): per-character vertical roll        */
/* ------------------------------------------------------------------ */
export const Odometer: React.FC<{
  values: Array<{ v: string; at: number }>;
  dur?: number;
  stagger?: number;
  ink?: string;
  accent?: string;
  style?: React.CSSProperties;
}> = ({ values, dur = 8, stagger = 1.5, ink = "#111", accent, style }) => {
  const frame = useCurrentFrame();
  let idx = 0;
  for (let i = 0; i < values.length; i++) if (frame >= values[i].at) idx = i;
  const cur = values[idx];
  const prev = idx > 0 ? values[idx - 1] : null;
  const len = Math.max(cur.v.length, prev ? prev.v.length : 0);
  const chars: React.ReactNode[] = [];
  for (let i = 0; i < len; i++) {
    const a = prev ? prev.v[i] ?? " " : " ";
    const b = cur.v[i] ?? " ";
    const t = prev ? EASE_PRO.move(clamp01((frame - cur.at - i * stagger) / dur)) : 1;
    const moving = t > 0 && t < 1 && a !== b;
    const col = moving && accent ? accent : ink;
    const LH = 1.2; // cell height in em
    const glyph = (c: string) => (c === " " ? " " : c);
    if (a === b || !prev) {
      chars.push(<span key={i} style={{ display: "block", height: `${LH}em`, lineHeight: `${LH}em`, color: ink }}>{glyph(b)}</span>);
      continue;
    }
    // fixed-height clipped cell; inner column (old over new) slides up exactly one cell
    chars.push(
      <span key={i} style={{ display: "block", position: "relative", overflow: "hidden", height: `${LH}em`, lineHeight: `${LH}em` }}>
        <span style={{ visibility: "hidden" }}>{glyph(b.length ? b : a)}</span>
        <span style={{ position: "absolute", left: 0, top: 0, transform: `translateY(${-t * LH}em)`, color: col,
          filter: moving ? `blur(0px ${Math.sin(Math.PI * t) * 3}px)` : undefined }}>
          <span style={{ display: "block", height: `${LH}em`, opacity: 1 - t * 0.7 }}>{glyph(a)}</span>
          <span style={{ display: "block", height: `${LH}em` }}>{glyph(b)}</span>
        </span>
      </span>,
    );
  }
  return <span style={{ display: "inline-flex", alignItems: "flex-start", fontVariantNumeric: "tabular-nums", ...style }}>{chars}</span>;
};

/* ------------------------------------------------------------------ */
/* SLOT ROLL / PICKER (v01 app chip, v12 Pay→Earn→Wallet, v20 platforms)*/
/* ------------------------------------------------------------------ */
export const SlotRoll: React.FC<{
  items: React.ReactNode[];
  /** frame at which each item (after the first) becomes current */
  at: number[];
  itemH: number;
  dur?: number;
  /** show neighbors faded above/below */
  neighbors?: boolean;
  width?: number | string;
  align?: "left" | "center";
}> = ({ items, at, itemH, dur = 10, neighbors = true, width = "auto", align = "left" }) => {
  const frame = useCurrentFrame();
  let pos = 0;
  at.forEach((f) => {
    pos += EASE_PRO.move(clamp01((frame - f) / dur));
  });
  let vel = 0;
  at.forEach((f) => {
    vel += EASE_PRO.move(clamp01((frame - f) / dur)) - EASE_PRO.move(clamp01((frame - 1 - f) / dur));
  });
  const mask = neighbors
    ? "linear-gradient(to bottom, transparent 0%, rgba(0,0,0,.35) 22%, black 40%, black 60%, rgba(0,0,0,.35) 78%, transparent 100%)"
    : "linear-gradient(to bottom, transparent 0%, black 30%, black 70%, transparent 100%)";
  const viewH = neighbors ? itemH * 3 : itemH;
  return (
    <span style={{ display: "inline-block", position: "relative", width, height: itemH, verticalAlign: "middle" }}>
      <span style={{ position: "absolute", left: 0, right: 0, top: (itemH - viewH) / 2, height: viewH, overflow: "hidden", maskImage: mask, WebkitMaskImage: mask }}>
        <span style={{ position: "absolute", left: 0, right: 0, top: (viewH - itemH) / 2, transform: `translateY(${-pos * itemH}px)`,
          filter: Math.abs(vel) > 0.02 ? `blur(0px ${Math.min(8, Math.abs(vel) * 30)}px)` : undefined }}>
          {items.map((it, i) => (
            <span key={i} style={{ display: "flex", height: itemH, alignItems: "center", justifyContent: align === "center" ? "center" : "flex-start" }}>{it}</span>
          ))}
        </span>
      </span>
    </span>
  );
};

/* ------------------------------------------------------------------ */
/* WORD SWAP (v02 softer → deeper → personal; v17 lyric per beat)       */
/* ------------------------------------------------------------------ */
export const WordSwap: React.FC<{
  words: Array<{ text: string; at: number; style?: React.CSSProperties }>;
  outDur?: number;
  inDur?: number;
  style?: React.CSSProperties;
}> = ({ words, outDur = 5, inDur = 8, style }) => {
  const frame = useCurrentFrame();
  let idx = -1;
  for (let i = 0; i < words.length; i++) if (frame >= words[i].at) idx = i;
  const nodes: React.ReactNode[] = [];
  if (idx >= 0) {
    const w = words[idx];
    const t = EASE_PRO.enterSnap(clamp01((frame - w.at) / inDur));
    nodes.push(
      <span key={"in" + idx} style={{ display: "inline-block", opacity: clamp01((frame - w.at) / (inDur * 0.4)), filter: `blur(${(1 - t) * 10}px)`,
        transform: `translateY(${(1 - t) * 10}px)`, ...w.style }}>
        {w.text}
      </span>,
    );
    if (idx > 0) {
      const p = words[idx - 1];
      const o = EASE_PRO.exit(clamp01((frame - w.at) / outDur));
      if (o < 1)
        nodes.push(
          <span key={"out" + idx} style={{ position: "absolute", left: 0, top: 0, opacity: 1 - o, filter: `blur(${o * 12}px)`,
            letterSpacing: `${o * 0.25}em`, transform: `translateY(${-o * 8}px)`, ...p.style }}>
            {p.text}
          </span>,
        );
    }
  }
  return <span style={{ position: "relative", display: "inline-block", ...style }}>{nodes}</span>;
};

/* ------------------------------------------------------------------ */
/* HIGHLIGHT WORD (v07 "more") and UNDERLINE DRAW (v05, v11)            */
/* ------------------------------------------------------------------ */
export const HighlightWord: React.FC<{
  at: number; dur?: number; bg?: string; color?: string; fromColor?: string; children: React.ReactNode; padX?: number; radius?: number;
}> = ({ at, dur = 8, bg = "#fff", color = "#111", fromColor = "#ffffff", children, padX = 0.22, radius = 0.22 }) => {
  const frame = useCurrentFrame();
  const t = EASE_PRO.enter(clamp01((frame - at) / dur));
  const textCol = interpolateColors(clamp01((frame - at - dur * 0.3) / (dur * 0.5)), [0, 1], [fromColor, color]);
  return (
    <span style={{ position: "relative", display: "inline-block", padding: `0 ${padX}em` }}>
      <span style={{ position: "absolute", inset: "0.02em 0", background: bg, borderRadius: `${radius}em`, transform: `scaleX(${t})`, transformOrigin: "0% 50%" }} />
      <span style={{ position: "relative", color: t > 0.05 ? textCol : undefined }}>{children}</span>
    </span>
  );
};

export const UnderlineDraw: React.FC<{ at: number; dur?: number; color?: string; thickness?: number; offset?: number; children: React.ReactNode }> = ({
  at, dur = 10, color = "#2D5BD7", thickness = 0.07, offset = 0.08, children,
}) => {
  const frame = useCurrentFrame();
  const t = EASE_PRO.enter(clamp01((frame - at) / dur));
  return (
    <span style={{ position: "relative", display: "inline-block" }}>
      {children}
      <span style={{ position: "absolute", left: 0, bottom: `-${offset}em`, height: `${thickness}em`, width: `${lerp(0, 100, t)}%`, background: color, borderRadius: 99 }} />
    </span>
  );
};
