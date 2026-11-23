import React, { useId } from "react";
import { AbsoluteFill, interpolateColors, useCurrentFrame, useVideoConfig } from "remotion";
import { EASE_PRO, clamp01, lerp, noise1, rand } from "./curves";

/* ------------------------------------------------------------------ */
/* AMBIENT FRAME (v03 v04 v20): 9:16 frame, sharp content band in the   */
/* middle, blurred enlarged copy of the SAME content fills top/bottom.  */
/* ------------------------------------------------------------------ */
export const AmbientFrame: React.FC<{
  bandW: number;
  bandH: number;
  radius?: number;
  blur?: number;
  dim?: number;
  /** caption under the band (handle, credit) */
  caption?: React.ReactNode;
  children: React.ReactNode;
}> = ({ bandW, bandH, radius = 28, blur = 60, dim = 0.06, caption, children }) => {
  const { width: W, height: H } = useVideoConfig();
  const s = Math.max(W / bandW, H / bandH) * 1.15;
  return (
    <AbsoluteFill style={{ background: "#000", overflow: "hidden" }}>
      <div style={{ position: "absolute", left: "50%", top: "50%", width: bandW, height: bandH, transform: `translate(-50%,-50%) scale(${s})`, filter: `blur(${blur / s}px)` }}>
        {children}
      </div>
      <AbsoluteFill style={{ background: `rgba(0,0,0,${dim})` }} />
      <div style={{ position: "absolute", left: "50%", top: "50%", width: bandW, height: bandH, transform: "translate(-50%,-50%)", borderRadius: radius, overflow: "hidden",
        boxShadow: "0 30px 80px -20px rgba(0,0,0,.35)" }}>
        {children}
      </div>
      {caption ? (
        <div style={{ position: "absolute", left: 0, right: 0, top: `calc(50% + ${bandH / 2 + 28}px)`, textAlign: "center" }}>{caption}</div>
      ) : null}
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* CURSOR (macOS arrow / hand / grab) on CURVED paths with press         */
/* ------------------------------------------------------------------ */
export type CurKey = { f: number; x: number; y: number; kind?: "arrow" | "hand" | "grab"; click?: boolean; bend?: number };

export const MacCursor: React.FC<{ keys: CurKey[]; size?: number; appearAt?: number; hideAt?: number; color?: string }> = ({
  keys, size = 54, appearAt, hideAt, color = "#000",
}) => {
  const frame = useCurrentFrame();
  const posAt = (f: number) => {
    if (f <= keys[0].f) return { x: keys[0].x, y: keys[0].y, k: keys[0].kind ?? "arrow" };
    for (let i = 1; i < keys.length; i++) {
      const a = keys[i - 1];
      const b = keys[i];
      if (f <= b.f) {
        const t = EASE_PRO.move(clamp01((f - a.f) / Math.max(1, b.f - a.f)));
        // quadratic bezier with a control point offset perpendicular to the segment (natural hand arc)
        const mx = (a.x + b.x) / 2;
        const my = (a.y + b.y) / 2;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const bend = b.bend ?? 0.18;
        const cx = mx - dy * bend;
        const cy = my + dx * bend;
        const x = (1 - t) * (1 - t) * a.x + 2 * (1 - t) * t * cx + t * t * b.x;
        const y = (1 - t) * (1 - t) * a.y + 2 * (1 - t) * t * cy + t * t * b.y;
        return { x, y, k: t > 0.85 ? b.kind ?? a.kind ?? "arrow" : a.kind ?? "arrow" };
      }
    }
    const l = keys[keys.length - 1];
    return { x: l.x, y: l.y, k: l.kind ?? "arrow" };
  };
  const p = posAt(frame);
  const q = posAt(frame - 1);
  let s = 1;
  keys.forEach((k) => {
    if (!k.click) return;
    const d = frame - k.f;
    if (d >= 0 && d < 3) s = Math.min(s, 1 - 0.15 * (d + 1) / 3);
    else if (d >= 3 && d <= 8) s = Math.min(s, 0.85 + 0.15 * EASE_PRO.enterSnap((d - 3) / 5));
  });
  const fade =
    (appearAt !== undefined ? clamp01((frame - appearAt) / 4) : 1) * (hideAt !== undefined ? 1 - clamp01((frame - hideAt) / 4) : 1);
  const v = Math.hypot(p.x - q.x, p.y - q.y);
  const blur = Math.min(8, v * 0.12);
  const kind = p.k;
  const hot = kind === "arrow" ? { x: 0.18, y: 0.1 } : { x: 0.42, y: 0.12 };
  return (
    <div style={{ position: "absolute", left: "50%", top: "50%", zIndex: 100, opacity: fade,
      transform: `translate(${p.x - size * hot.x}px, ${p.y - size * hot.y}px) scale(${s})`, transformOrigin: `${hot.x * 100}% ${hot.y * 100}%`,
      filter: `drop-shadow(0 3px 5px rgba(0,0,0,.28))${blur > 0.4 ? ` blur(${blur}px)` : ""}` }}>
      {kind === "arrow" ? (
        <svg width={size} height={size} viewBox="0 0 28 28">
          <path d="M5 2.5 L5 22 L10 17.3 L13.4 25 L17 23.5 L13.7 15.9 L20.5 15.9 Z" fill={color} stroke="#fff" strokeWidth="1.6" strokeLinejoin="round" />
        </svg>
      ) : (
        <svg width={size} height={size} viewBox="0 0 32 32">
          <path fill="#fff" stroke={color} strokeWidth="1.4" strokeLinejoin="round"
            d={kind === "grab"
              ? "M9 13c0-1.2 1-2 2-2s2 .8 2 2v-1c0-1.2 1-2 2-2s2 .8 2 2v1c0-1.2 1-2 2-2s2 .8 2 2v1c0-1.1 .9-2 2-2s2 .9 2 2v6c0 4.4-3.4 8-7.8 8h-1.8c-2.6 0-4.6-1.3-6-3.4L6.6 18c-.6-1-.3-2.2.7-2.8 1-.6 2.2-.3 2.7.6z"
              : "M11 3.5c1.2 0 2 .9 2 2V14l.8-.2V11c0-1.1.9-1.9 2-1.9s2 .9 2 1.9v2.6l.6-.1v-1.4c0-1.1.9-1.9 2-1.9s2 .9 2 1.9v1.8l.4-.1c1.1-.1 2.1.8 2.1 2v5.4c0 4.4-3.2 7.7-7.6 7.7h-1.5c-2.4 0-4.4-1.1-5.8-3l-4.3-6c-.7-.9-.5-2.2.4-2.8.9-.7 2.1-.5 2.8.3L9 17.6V5.5c0-1.1.9-2 2-2z"} />
        </svg>
      )}
    </div>
  );
};

/** Press scale for the clicked target: 1 -> 0.92 -> 1.04 -> 1 around `at`. */
export const pressScale = (frame: number, at: number, depth = 0.08) => {
  const d = frame - at;
  if (d < 0 || d > 12) return 1;
  if (d < 3) return 1 - depth * (d / 3);
  const t = (d - 3) / 9;
  return 1 - depth + (depth + 0.04) * EASE_PRO.enterSnap(clamp01(t / 0.5)) - 0.04 * EASE_PRO.drift(clamp01((t - 0.5) / 0.5));
};

/* ------------------------------------------------------------------ */
/* MORPH BOX (v15): one container, many states                          */
/* ------------------------------------------------------------------ */
export type MorphState = { f: number; w: number; h: number; radius: number; bg: string; shadow?: string; x?: number; y?: number };

export const MorphBox: React.FC<{
  states: MorphState[];
  dur?: number;
  /** render content of state i; receives 0..1 visibility */
  render: (i: number, vis: number) => React.ReactNode;
  overshoot?: number;
}> = ({ states, dur = 10, render, overshoot = 0.035 }) => {
  const frame = useCurrentFrame();
  let i = 0;
  for (let k = 0; k < states.length; k++) if (frame >= states[k].f) i = k;
  const a = states[Math.max(0, i - 1)];
  const b = states[i];
  const raw = i === 0 ? 1 : clamp01((frame - b.f) / dur);
  const t = EASE_PRO.move(raw);
  // tiny overshoot on size at the end (spring-like), measured 2-5%
  const os = raw > 0.6 ? Math.sin(((raw - 0.6) / 0.4) * Math.PI) * overshoot : 0;
  const w = lerp(a.w, b.w, t) * (1 + os);
  const h = lerp(a.h, b.h, t) * (1 + os * 0.6);
  const r = lerp(a.radius, b.radius, t);
  const bg = interpolateColors(t, [0, 1], [a.bg, b.bg]);
  const x = lerp(a.x ?? 0, b.x ?? 0, t);
  const y = lerp(a.y ?? 0, b.y ?? 0, t);
  const outVis = i === 0 ? 0 : 1 - clamp01((frame - b.f) / 3);
  const inVis = i === 0 ? clamp01((frame - b.f) / 4) : clamp01((frame - b.f - dur * 0.45) / 5);
  return (
    <div style={{ position: "absolute", left: "50%", top: "50%", width: w, height: h, borderRadius: r, background: bg, overflow: "hidden",
      transform: `translate(-50%,-50%) translate(${x}px, ${y}px)`, boxShadow: b.shadow ?? a.shadow }}>
      {i > 0 && outVis > 0 ? (
        <div style={{ position: "absolute", inset: 0, opacity: outVis, filter: `blur(${(1 - outVis) * 8}px)`, transform: `scale(${1 - (1 - outVis) * 0.06})` }}>
          {render(i - 1, outVis)}
        </div>
      ) : null}
      <div style={{ position: "absolute", inset: 0, opacity: inVis, filter: inVis < 1 ? `blur(${(1 - inVis) * 8}px)` : undefined }}>{render(i, inVis)}</div>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* PARTICLES: bokeh squares rising (v17), snow dots (v07), glyphs (v09) */
/* ------------------------------------------------------------------ */
export const Particles: React.FC<{
  count?: number;
  seed?: number;
  shape?: "square" | "dot" | "glyph";
  colors?: string[];
  size?: [number, number];
  /** px per frame */
  vx?: number;
  vy?: number;
  blur?: [number, number];
  opacity?: [number, number];
  wobble?: number;
  start?: number;
  fadeIn?: number;
}> = ({ count = 30, seed = 1, shape = "dot", colors = ["#ffffff"], size = [4, 12], vx = 0, vy = -0.6, blur = [0, 6], opacity = [0.3, 0.9], wobble = 10, start = 0, fadeIn = 12 }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H } = useVideoConfig();
  const t = frame - start;
  if (t < 0) return null;
  const glyphs = "01/<>+=*{}";
  const items: React.ReactNode[] = [];
  for (let i = 0; i < count; i++) {
    const depth = rand(i, seed, 1);
    const sz = lerp(size[0], size[1], depth);
    const sp = 0.5 + depth;
    let x = rand(i, seed, 2) * W + vx * sp * t + noise1(t / 40 + i, seed) * wobble;
    let y = rand(i, seed, 3) * H + vy * sp * t + noise1(t / 50 + i, seed + 9) * wobble;
    x = ((x % (W + 40)) + W + 40) % (W + 40) - 20;
    y = ((y % (H + 40)) + H + 40) % (H + 40) - 20;
    const op = lerp(opacity[0], opacity[1], rand(i, seed, 4)) * clamp01(t / fadeIn);
    const bl = lerp(blur[0], blur[1], Math.abs(depth - 0.5) * 2);
    const col = colors[Math.floor(rand(i, seed, 5) * colors.length)];
    items.push(
      <div key={i} style={{ position: "absolute", left: x, top: y, width: shape === "glyph" ? undefined : sz, height: shape === "glyph" ? undefined : sz,
        borderRadius: shape === "dot" ? sz : sz * 0.15, background: shape === "glyph" ? undefined : col, color: col, opacity: op,
        filter: bl > 0.4 ? `blur(${bl}px)` : undefined, fontSize: sz * 2.2, fontFamily: "monospace", transform: `rotate(${rand(i, seed, 6) * 40 - 20}deg)` }}>
        {shape === "glyph" ? glyphs[Math.floor(rand(i, seed, 7) * glyphs.length)] : null}
      </div>,
    );
  }
  return <AbsoluteFill style={{ pointerEvents: "none" }}>{items}</AbsoluteFill>;
};

/* ------------------------------------------------------------------ */
/* ORBIT (v08 satellites, v18 avatars): items on an ellipse with depth  */
/* ------------------------------------------------------------------ */
export const Orbit: React.FC<{ items: React.ReactNode[]; rx: number; ry: number; period?: number; phase?: number; depthScale?: number; depthBlur?: number; cx?: number; cy?: number }> = ({
  items, rx, ry, period = 180, phase = 0, depthScale = 0.25, depthBlur = 3, cx = 0, cy = 0,
}) => {
  const frame = useCurrentFrame();
  return (
    <>
      {items.map((it, i) => {
        const a = ((frame + phase) / period) * Math.PI * 2 + (i / items.length) * Math.PI * 2;
        const z = Math.sin(a); // -1 back, 1 front
        const s = 1 + z * depthScale;
        return (
          <div key={i} style={{ position: "absolute", left: "50%", top: "50%", zIndex: Math.round(z * 10) + 20,
            transform: `translate(-50%,-50%) translate(${cx + Math.cos(a) * rx}px, ${cy + z * ry}px) scale(${s})`,
            filter: z < 0 ? `blur(${-z * depthBlur}px)` : undefined, opacity: 0.75 + 0.25 * (z + 1) / 2 }}>
            {it}
          </div>
        );
      })}
    </>
  );
};

/* ------------------------------------------------------------------ */
/* GLOW / LIGHT LEAK / MESH BACKGROUND / DOT GRID                       */
/* ------------------------------------------------------------------ */
export const Glow: React.FC<{ x?: number; y?: number; size: number; color: string; opacity?: number; breathe?: number; period?: number }> = ({
  x = 0, y = 0, size, color, opacity = 0.6, breathe = 0.12, period = 90,
}) => {
  const frame = useCurrentFrame();
  const b = 1 + Math.sin((frame / period) * Math.PI * 2) * breathe;
  return (
    <div style={{ position: "absolute", left: "50%", top: "50%", width: size, height: size, borderRadius: "50%",
      transform: `translate(-50%,-50%) translate(${x}px, ${y}px) scale(${b})`,
      background: `radial-gradient(circle, ${color} 0%, transparent 65%)`, opacity, pointerEvents: "none" }} />
  );
};

export const MeshBg: React.FC<{ colors: string[]; base?: string; speed?: number; blur?: number; seed?: number }> = ({ colors, base = "#fff", speed = 1, blur = 90, seed = 2 }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: base, overflow: "hidden" }}>
      {colors.map((c, i) => {
        const x = (rand(i, seed) - 0.5) * W * 0.8 + noise1((frame * speed) / 70 + i * 3, seed) * W * 0.18;
        const y = (rand(i, seed + 1) - 0.5) * H * 0.8 + noise1((frame * speed) / 80 + i * 5, seed + 4) * H * 0.18;
        const s = (0.55 + rand(i, seed + 2) * 0.5) * Math.max(W, H);
        return (
          <div key={i} style={{ position: "absolute", left: "50%", top: "50%", width: s, height: s, borderRadius: "50%", background: c,
            transform: `translate(-50%,-50%) translate(${x}px, ${y}px)`, filter: `blur(${blur}px)`, opacity: 0.85 }} />
        );
      })}
    </AbsoluteFill>
  );
};

export const DotGrid: React.FC<{ gap?: number; size?: number; color?: string; opacity?: number }> = ({ gap = 28, size = 2, color = "#8aa0c8", opacity = 0.25 }) => (
  <AbsoluteFill style={{ backgroundImage: `radial-gradient(${color} ${size / 2}px, transparent ${size / 2 + 0.5}px)`, backgroundSize: `${gap}px ${gap}px`, opacity }} />
);

/* ------------------------------------------------------------------ */
/* PHONE (iPhone-like device frame)                                     */
/* ------------------------------------------------------------------ */
export const Phone: React.FC<{ w?: number; tone?: "black" | "titanium" | "white"; children?: React.ReactNode; island?: boolean; screenBg?: string }> = ({
  w = 420, tone = "black", children, island = true, screenBg = "#fff",
}) => {
  const h = w * 2.06;
  const frameCol = tone === "black" ? "#0b0b0c" : tone === "titanium" ? "linear-gradient(135deg,#8d8780,#3b3835 40%,#a59f97 60%,#4a4643)" : "#f2f2f4";
  const bezel = w * 0.035;
  return (
    <div style={{ position: "relative", width: w, height: h, borderRadius: w * 0.17, background: frameCol, padding: bezel, boxSizing: "border-box",
      boxShadow: "0 40px 90px -30px rgba(0,0,0,.45), inset 0 0 0 2px rgba(255,255,255,.08)" }}>
      <div style={{ position: "relative", width: "100%", height: "100%", borderRadius: w * 0.14, overflow: "hidden", background: screenBg }}>
        {children}
        {island ? (
          <div style={{ position: "absolute", left: "50%", top: w * 0.03, width: w * 0.3, height: w * 0.085, borderRadius: w, background: "#000", transform: "translateX(-50%)" }} />
        ) : null}
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* END CARD (studio sign-off with bloom, as in dnyxstudios outros)      */
/* ------------------------------------------------------------------ */
export const EndCard: React.FC<{ text: string; start?: number; dur?: number; bg?: string; color?: string; font?: string; size?: number }> = ({
  text, start = 0, dur = 45, bg = "#000", color = "#fff", font, size = 64,
}) => {
  const frame = useCurrentFrame();
  const t = clamp01((frame - start) / dur);
  const inT = EASE_PRO.enterSnap(clamp01((frame - start) / 6));
  const outT = EASE_PRO.exit(clamp01((frame - start - dur + 8) / 8));
  const scale = lerp(1.08, 0.94, EASE_PRO.drift(t));
  return (
    <AbsoluteFill style={{ background: bg, alignItems: "center", justifyContent: "center" }}>
      <div style={{ position: "absolute", width: "70%", height: "40%", background: `radial-gradient(ellipse, ${color}22 0%, transparent 70%)` }} />
      <div style={{ fontFamily: font, fontSize: size, fontWeight: 600, color, letterSpacing: "-0.02em", transform: `scale(${scale})`,
        opacity: inT * (1 - outT), filter: `blur(${(1 - inT) * 14 + outT * 10}px)`,
        textShadow: `0 0 18px ${color}aa, 0 0 42px ${color}55` }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};

/** Inline slot that opens a gap inside a sentence for an icon/avatar/media (v09 v12 v18 v22). */
export const InlineSlot: React.FC<{ at: number; w: number; dur?: number; children: React.ReactNode }> = ({ at, w, dur = 10, children }) => {
  const frame = useCurrentFrame();
  const t = EASE_PRO.enter(clamp01((frame - at) / dur));
  const pop = EASE_PRO.enterSnap(clamp01((frame - at - 2) / 8));
  return (
    <span style={{ display: "inline-flex", width: w * t, justifyContent: "center", alignItems: "center", verticalAlign: "middle", overflow: "visible" }}>
      <span style={{ display: "inline-flex", transform: `scale(${0.3 + 0.7 * pop})`, opacity: pop, filter: pop < 1 ? `blur(${(1 - pop) * 6}px)` : undefined }}>{children}</span>
    </span>
  );
};

/** A unique id hook re-export for custom SVG filters in compositions. */
export const useFxId = (prefix = "fx") => prefix + useId().replace(/[^a-zA-Z0-9]/g, "");

/* ------------------------------------------------------------------ */
/* DRIFT BLOB: soft colour blob that wanders slowly (background is never */
/* frozen; v12's background shifts blue -> white, refs' blobs move).     */
/* ------------------------------------------------------------------ */
export const DriftBlob: React.FC<{ x?: number; y?: number; size: number; color: string; opacity?: number; period?: number; ax?: number; ay?: number; phase?: number }> = ({
  x = 0, y = 0, size, color, opacity = 0.5, period = 240, ax = 70, ay = 50, phase = 0,
}) => {
  const frame = useCurrentFrame();
  const t = ((frame + phase) / period) * Math.PI * 2;
  const px = x + Math.sin(t) * ax;
  const py = y + Math.sin(t * 0.77 + 1.1) * ay;
  const s = 1 + Math.sin(t * 1.3 + 0.4) * 0.08;
  return (
    <div style={{ position: "absolute", left: "50%", top: "50%", width: size, height: size, marginLeft: -size / 2, marginTop: -size / 2,
      transform: `translate(${px}px, ${py}px) scale(${s})`, background: `radial-gradient(circle, ${color} 0%, transparent 68%)`, opacity }} />
  );
};

/* Click ring (pro click feedback): an accent ring leaves the button, 1 -> 1.3, opacity .6 -> 0, 10-12f. */
export const ClickRing: React.FC<{ at: number; w: number; h: number; radius?: number; color?: string; dur?: number; x?: number; y?: number; width?: number }> = ({
  at, w, h, radius, color = "#0A84FF", dur = 12, x = 0, y = 0, width = 3,
}) => {
  const frame = useCurrentFrame();
  const d = frame - at;
  if (d < 0 || d > dur) return null;
  const t = EASE_PRO.enterSnap(d / dur);
  return (
    <div style={{ position: "absolute", left: "50%", top: "50%", width: w, height: h, marginLeft: -w / 2, marginTop: -h / 2, borderRadius: radius ?? h / 2,
      border: `${width}px solid ${color}`, transform: `translate(${x}px, ${y}px) scale(${1 + 0.3 * t})`, opacity: 0.6 * (1 - t), boxSizing: "border-box" }} />
  );
};

/* Ring draw-on (v12 66-72): an accent outline draws around a pill/button, then stays or fades. */
export const RingDraw: React.FC<{ at: number; w: number; h: number; radius?: number; color?: string; dur?: number; stroke?: number; fadeAt?: number; x?: number; y?: number; gap?: number }> = ({
  at, w, h, radius, color = "#0A84FF", dur = 10, stroke = 3, fadeAt, x = 0, y = 0, gap = 6,
}) => {
  const frame = useCurrentFrame();
  const d = frame - at;
  if (d < 0) return null;
  const W = w + gap * 2;
  const H = h + gap * 2;
  const r = Math.min(radius ?? H / 2, H / 2);
  const per = 2 * (W - 2 * r) + 2 * (H - 2 * r) + 2 * Math.PI * r;
  const t = EASE_PRO.enter(clamp01(d / dur));
  const o = fadeAt !== undefined ? 1 - EASE_PRO.exit(clamp01((frame - fadeAt) / 8)) : 1;
  if (o <= 0) return null;
  return (
    <svg width={W + stroke * 2} height={H + stroke * 2} style={{ position: "absolute", left: "50%", top: "50%", marginLeft: -(W + stroke * 2) / 2, marginTop: -(H + stroke * 2) / 2,
      transform: `translate(${x}px, ${y}px)`, opacity: o, overflow: "visible" }}>
      <rect x={stroke} y={stroke} width={W} height={H} rx={r} fill="none" stroke={color} strokeWidth={stroke} strokeDasharray={per} strokeDashoffset={per * (1 - t)} strokeLinecap="round" />
    </svg>
  );
};
