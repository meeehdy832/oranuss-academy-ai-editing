import React, { useId } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { EASE_PRO, Ease, clamp01, lerp, prog, rand } from "./curves";

// Every overlay transition exposes the frame where the underlying scene should switch (`switchAt`).
// Pattern:  {frame < T.switchAt ? <SceneA/> : <SceneB/>}  <Overlay at={...}/>

/* ------------------------------------------------------------------ */
/* PIXEL DISSOLVE (v09): cells flood in randomly, mosaic, then vanish  */
/* ------------------------------------------------------------------ */
export const pixelTiming = (at: number, inDur = 5, hold = 2, outDur = 11) => ({
  switchAt: at + inDur + Math.floor(hold / 2),
  end: at + inDur + hold + outDur + 6,
});

export const PixelDissolve: React.FC<{
  at: number;
  color: string;
  /** secondary color mixed randomly (lighter/darker tint) */
  color2?: string;
  cols?: number;
  gap?: number;
  inDur?: number;
  hold?: number;
  outDur?: number;
  /** fraction of cells that linger as small dots after the reveal */
  linger?: number;
  seed?: number;
}> = ({ at, color, color2, cols = 56, gap = 0.18, inDur = 5, hold = 2, outDur = 11, linger = 0.06, seed = 7 }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const t = frame - at;
  if (t < 0 || t > inDur + hold + outDur + 8) return null;
  const cell = width / cols;
  const rows = Math.ceil(height / cell);
  const rects: React.ReactNode[] = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const a = rand(c, r, seed);
      const b = rand(c, r, seed + 1);
      const on = a * inDur;
      const lingerer = b < linger;
      const off = inDur + hold + b * outDur + (lingerer ? 4 + rand(c, r, seed + 2) * 6 : 0);
      if (t < on || t > off + 1) continue;
      const appear = clamp01((t - on) / 1.5);
      const vanish = clamp01((t - (off - 2)) / 3);
      let s = (1 - gap) * (0.6 + 0.4 * appear) * (1 - 0.5 * vanish);
      let op = appear * (1 - vanish);
      if (lingerer && t > inDur + hold + outDur * 0.5) {
        s *= 0.45; // stray dots
        op *= 0.9;
      }
      const sz = cell * s;
      rects.push(
        <rect
          key={r * cols + c}
          x={c * cell + (cell - sz) / 2}
          y={r * cell + (cell - sz) / 2}
          width={sz}
          height={sz}
          rx={sz * 0.12}
          fill={color2 && rand(c, r, seed + 3) > 0.6 ? color2 : color}
          opacity={op}
        />,
      );
    }
  }
  return (
    <AbsoluteFill style={{ pointerEvents: "none", zIndex: 80 }}>
      <svg width={width} height={height}>{rects}</svg>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* RIBBON SWOOSH (v06): thick blurred zig-zag stroke sweeps diagonally */
/* ------------------------------------------------------------------ */
export const swooshTiming = (at: number, dur = 12) => ({ switchAt: at + Math.round(dur * 0.5), end: at + dur });

export const RibbonSwoosh: React.FC<{ at: number; dur?: number; color?: string; thickness?: number; blur?: number }> = ({
  at, dur = 12, color = "#0A0A0A", thickness = 0.5, blur = 10,
}) => {
  const frame = useCurrentFrame();
  const { width: W, height: H } = useVideoConfig();
  const id = "sw" + useId().replace(/[^a-zA-Z0-9]/g, "");
  const t = (frame - at) / dur;
  if (t < 0 || t > 1.05) return null;
  const head = EASE_PRO.enter(clamp01(t / 0.6));
  const tail = EASE_PRO.exit(clamp01((t - 0.45) / 0.55));
  const d = `M ${-0.35 * W} ${-0.05 * H} C ${0.4 * W} ${-0.25 * H}, ${0.75 * W} ${0.1 * H}, ${0.35 * W} ${0.45 * H}
             S ${0.2 * W} ${0.85 * H}, ${0.75 * W} ${0.75 * H} S ${1.4 * W} ${1.05 * H}, ${1.35 * W} ${1.35 * H}`;
  const L = 1000;
  const vis = Math.max(0, head - tail);
  return (
    <AbsoluteFill style={{ pointerEvents: "none", zIndex: 85 }}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <defs>
          <filter id={id} x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation={blur * (0.4 + 1.2 * Math.sin(Math.PI * clamp01(t)))} />
          </filter>
        </defs>
        <path
          d={d}
          pathLength={L}
          fill="none"
          stroke={color}
          strokeWidth={H * thickness}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeDasharray={`${vis * L} ${L * 2}`}
          strokeDashoffset={-tail * L}
          filter={`url(#${id})`}
        />
      </svg>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* GLITCH FLASH (v13, v14, v19): 1-frame cards of static/white/black    */
/* ------------------------------------------------------------------ */
export type GlitchCard = "noise" | "noiseLight" | "white" | "black" | "color" | "flare" | "clear";

export const GlitchFlash: React.FC<{ at: number; pattern?: GlitchCard[]; color?: string }> = ({
  at, pattern = ["noise", "noiseLight", "black"], color = "#E60023",
}) => {
  const frame = useCurrentFrame();
  const { width: W, height: H } = useVideoConfig();
  const id = "gl" + useId().replace(/[^a-zA-Z0-9]/g, "");
  const i = frame - at;
  if (i < 0 || i >= pattern.length) return null;
  const card = pattern[i];
  if (card === "clear") return null;
  if (card === "white" || card === "black" || card === "color")
    return <AbsoluteFill style={{ background: card === "white" ? "#fff" : card === "black" ? "#000" : color, zIndex: 90 }} />;
  if (card === "flare")
    return (
      <AbsoluteFill style={{ background: "#000", zIndex: 90 }}>
        <div style={{ position: "absolute", left: "55%", top: "45%", width: W * 0.5, height: H * 0.5, transform: "translate(-50%,-50%)",
          background: "radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(255,255,255,.35) 25%, transparent 60%)" }} />
      </AbsoluteFill>
    );
  const light = card === "noiseLight";
  return (
    <AbsoluteFill style={{ zIndex: 90, background: light ? "#ddd" : "#111" }}>
      <svg width={W} height={H}>
        <filter id={id}>
          <feTurbulence type="fractalNoise" baseFrequency="0.9 0.02" numOctaves={2} seed={frame} />
          <feColorMatrix type="saturate" values="0" />
          <feComponentTransfer>
            <feFuncA type="table" tableValues={light ? "0 0.5" : "0 0.9"} />
          </feComponentTransfer>
        </filter>
        <rect width={W} height={H} filter={`url(#${id})`} />
      </svg>
      <AbsoluteFill style={{ background: `repeating-linear-gradient(0deg, rgba(0,0,0,${light ? 0.12 : 0.35}) 0 2px, transparent 2px 5px)` }} />
    </AbsoluteFill>
  );
};

/** Single flash frame(s): white/black/brand. */
export const Flash: React.FC<{ at: number; len?: number; color?: string; opacity?: number }> = ({ at, len = 1, color = "#fff", opacity = 1 }) => {
  const frame = useCurrentFrame();
  if (frame < at || frame >= at + len) return null;
  return <AbsoluteFill style={{ background: color, opacity, zIndex: 90 }} />;
};

/** Strobe: invert the wrapped scene on the given frames (v10 beat hits). */
export const Strobe: React.FC<{ frames: number[]; children: React.ReactNode }> = ({ frames, children }) => {
  const frame = useCurrentFrame();
  const on = frames.indexOf(frame) >= 0;
  return <AbsoluteFill style={{ filter: on ? "invert(1) hue-rotate(180deg)" : undefined }}>{children}</AbsoluteFill>;
};

/* ------------------------------------------------------------------ */
/* SOFT WIPE (v04) and VIGNETTE OUT (v01)                               */
/* ------------------------------------------------------------------ */
export const SoftWipe: React.FC<{ at: number; dur?: number; color?: string; dir?: "left" | "right" | "up" | "down"; soft?: number }> = ({
  at, dur = 12, color = "#fff", dir = "left", soft = 0.35,
}) => {
  const frame = useCurrentFrame();
  const t = (frame - at) / dur;
  if (t < 0 || t > 1) return null;
  // first half covers, second half uncovers (same direction)
  const cover = EASE_PRO.move(clamp01(t / 0.55));
  const uncover = EASE_PRO.move(clamp01((t - 0.45) / 0.55));
  const angle = dir === "left" ? 270 : dir === "right" ? 90 : dir === "up" ? 0 : 180;
  const a = lerp(-soft * 100, 100, cover);
  const b = lerp(-soft * 100, 100, uncover);
  const bg = `linear-gradient(${angle}deg, transparent ${b}%, ${color} ${b + soft * 100}%, ${color} ${a}%, transparent ${a + soft * 100}%)`;
  return <AbsoluteFill style={{ background: bg, zIndex: 85, pointerEvents: "none" }} />;
};

export const VignetteOut: React.FC<{ at: number; dur?: number; color?: string }> = ({ at, dur = 10, color = "#000" }) => {
  const frame = useCurrentFrame();
  const t = prog(frame, at, dur, EASE_PRO.exit);
  if (t <= 0) return null;
  const inner = lerp(75, -10, t);
  return (
    <AbsoluteFill
      style={{ background: `radial-gradient(ellipse at center, transparent ${inner}%, ${color} ${inner + 45}%)`, zIndex: 85, pointerEvents: "none" }}
    />
  );
};

/* ------------------------------------------------------------------ */
/* BLUR SWAP: A blurs out while B focus-pulls in                        */
/* ------------------------------------------------------------------ */
export const BlurSwap: React.FC<{ at: number; dur?: number; a: React.ReactNode; b: React.ReactNode; maxBlur?: number; scale?: number }> = ({
  at, dur = 8, a, b, maxBlur = 18, scale = 0.04,
}) => {
  const frame = useCurrentFrame();
  const t = clamp01((frame - at) / dur);
  if (frame < at) return <AbsoluteFill>{a}</AbsoluteFill>;
  if (t >= 1) return <AbsoluteFill>{b}</AbsoluteFill>;
  const ea = EASE_PRO.exit(clamp01(t / 0.6));
  const eb = EASE_PRO.enter(clamp01((t - 0.3) / 0.7));
  return (
    <>
      <AbsoluteFill style={{ opacity: 1 - ea, filter: `blur(${maxBlur * ea}px)`, transform: `scale(${1 + scale * ea})` }}>{a}</AbsoluteFill>
      <AbsoluteFill style={{ opacity: eb, filter: `blur(${maxBlur * (1 - eb)}px)`, transform: `scale(${1 - scale * (1 - eb)})` }}>{b}</AbsoluteFill>
    </>
  );
};

/* ------------------------------------------------------------------ */
/* SHRINK TO CARD (reverse portal: map->widget v18, frame->icon v10)    */
/* ------------------------------------------------------------------ */
export const ShrinkToCard: React.FC<{
  at: number;
  dur?: number;
  /** target card in px relative to the frame center */
  to: { x: number; y: number; w: number; h: number; radius: number };
  ease?: Ease;
  shadow?: string;
  reverse?: boolean;
  children: React.ReactNode;
}> = ({ at, dur = 12, to, ease = EASE_PRO.move, shadow = "0 40px 80px -30px rgba(0,0,0,.35)", reverse = false, children }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H } = useVideoConfig();
  let t = clamp01((frame - at) / dur);
  t = ease(reverse ? 1 - t : t);
  const w = lerp(W, to.w, t);
  const h = lerp(H, to.h, t);
  const x = lerp(0, to.x, t);
  const y = lerp(0, to.y, t);
  const r = lerp(0, to.radius, t);
  const s = Math.max(w / W, h / H); // content scale (cover)
  return (
    <div
      style={{
        position: "absolute", left: "50%", top: "50%", width: w, height: h,
        transform: `translate(-50%,-50%) translate(${x}px, ${y}px)`,
        borderRadius: r, overflow: "hidden", boxShadow: t > 0.02 ? shadow : undefined,
      }}
    >
      <div style={{ position: "absolute", left: "50%", top: "50%", width: W, height: H, transform: `translate(-50%,-50%) scale(${s})` }}>
        {children}
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* LIQUID RIPPLE (v12, v18): displacement that peaks mid-transition     */
/* ------------------------------------------------------------------ */
export const LiquidRipple: React.FC<{ at: number; dur?: number; strength?: number; children: React.ReactNode }> = ({
  at, dur = 12, strength = 90, children,
}) => {
  const frame = useCurrentFrame();
  const id = "lq" + useId().replace(/[^a-zA-Z0-9]/g, "");
  const t = clamp01((frame - at) / dur);
  const amt = Math.sin(Math.PI * t) * strength;
  if (amt < 0.5) return <AbsoluteFill>{children}</AbsoluteFill>;
  return (
    <AbsoluteFill>
      <svg width={0} height={0} style={{ position: "absolute" }}>
        <filter id={id} x="-10%" y="-10%" width="120%" height="120%">
          <feTurbulence type="fractalNoise" baseFrequency={`${0.006 + 0.002 * t} ${0.012 + 0.004 * t}`} numOctaves={2} seed={3} result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale={amt} xChannelSelector="R" yChannelSelector="G" />
        </filter>
      </svg>
      <AbsoluteFill style={{ filter: `url(#${id})` }}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* IMPACT FRAME (v11 frame 0): radial echo of a word for 1-2 frames     */
/* ------------------------------------------------------------------ */
export const ImpactFrame: React.FC<{ at: number; len?: number; children: React.ReactNode; color?: string; copies?: number }> = ({
  at, len = 1, children, color = "#E1007A", copies = 7,
}) => {
  const frame = useCurrentFrame();
  if (frame < at || frame >= at + len) return null;
  const items: React.ReactNode[] = [];
  for (let i = copies; i >= 0; i--) {
    items.push(
      <div key={i} style={{ position: "absolute", left: "50%", top: "50%", transform: `translate(-50%,-50%) scale(${1 + i * 0.35})`,
        opacity: i === 0 ? 1 : 0.5 / (1 + i * 0.4), color, filter: i ? `blur(${i * 1.5}px)` : undefined }}>
        {children}
      </div>,
    );
  }
  return <AbsoluteFill style={{ background: "#fff", zIndex: 95, overflow: "hidden" }}>{items}</AbsoluteFill>;
};

/* ------------------------------------------------------------------ */
/* LIGHT SWEEP / COMET (v23): a glowing streak travels across           */
/* ------------------------------------------------------------------ */
export const Comet: React.FC<{ at: number; dur?: number; from: { x: number; y: number }; to: { x: number; y: number }; color?: string; size?: number; ease?: Ease }> = ({
  at, dur = 12, from, to, color = "#fff", size = 18, ease = EASE_PRO.move,
}) => {
  const frame = useCurrentFrame();
  const t = clamp01((frame - at) / dur);
  if (frame < at || frame > at + dur + 2) return null;
  const e = ease(t);
  const ep = ease(clamp01((frame - 1 - at) / dur));
  const x = lerp(from.x, to.x, e);
  const y = lerp(from.y, to.y, e);
  const vx = x - lerp(from.x, to.x, ep);
  const vy = y - lerp(from.y, to.y, ep);
  const len = Math.max(size, Math.hypot(vx, vy) * 2.2);
  const ang = (Math.atan2(vy, vx) * 180) / Math.PI;
  return (
    <div style={{ position: "absolute", left: "50%", top: "50%", width: len, height: size * 0.5, borderRadius: size,
      transform: `translate(${x - len}px, ${y - size * 0.25}px) rotate(${ang}deg)`, transformOrigin: "100% 50%",
      background: `linear-gradient(90deg, transparent, ${color})`, boxShadow: `0 0 ${size}px ${size * 0.4}px ${color}55`, zIndex: 60 }} />
  );
};
