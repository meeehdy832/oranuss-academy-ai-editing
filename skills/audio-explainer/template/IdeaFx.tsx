// Idea animations: one small animated diagram per spoken idea, laid over photos/clips (in a 3D glass panel)
// or played full-size on dark cards. Every module times itself from `at` (seconds from the beat start),
// which scripts/cue_fx.py fills in from the word timings so each move lands on the spoken word.
import React from "react";
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { loadFont } from "@remotion/google-fonts/Cairo";

const { fontFamily: CAIRO } = loadFont("normal", { weights: ["700", "800", "900"], subsets: ["arabic", "latin"] });
const FPS = 30;
import { BRAND } from "./brand";
const C = { blue: BRAND.accent, blue2: "#5B9BFF", white: "#FFFFFF", light: "#D3DAE4", mid: "#8C98AA", gray: "#4B586C", ink: "#0E1320",
  gold: "#F5C542", gold2: "#C8961E", red: "#FF4D5E", green: "#2FD27A" };
const ar = (s?: string) => /[\u0621-\u064A\u0671-\u06D3]/.test(s ?? "");
const ease = Easing.bezier(0.2, 0.9, 0.25, 1);
const io = (f: number, a: number, b: number, from = 0, to = 1) =>
  interpolate(f, [a, b], [from, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
const useSp = (at: number, damping = 14, stiffness = 150) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  return spring({ frame: f - at, fps, config: { damping, stiffness } });
};

export type FxItem = { label: string; icon?: string; value?: number; from?: number; to?: number; at?: number; cue?: string; x?: number; y?: number };
export type Fx = {
  k: "chips" | "stamp" | "count" | "calendar" | "clock" | "tags" | "receipt" | "line" | "scale" | "domino" | "flow" | "globe" | "meter" | "ring";
  pos?: "left" | "right" | "full";
  at?: number; cue?: string; dur?: number;
  title?: string; label?: string; sub?: string; text?: string; icon?: string; good?: boolean;
  items?: FxItem[]; a?: FxItem; b?: FxItem;
  value?: number; from?: number; to?: number; suffix?: string; n?: number; kind?: "up" | "down" | "gap"; tip?: "a" | "b";
  x?: number; y?: number; r?: number;
};

/* ---------- small parts ---------- */
const Tx: React.FC<{ s: string; size: number; color?: string; weight?: number; style?: React.CSSProperties }> = ({ s, size, color = C.white, weight = 800, style }) => (
  <div dir={ar(s) ? "rtl" : "ltr"} style={{ fontFamily: CAIRO, fontSize: size, fontWeight: weight, color, lineHeight: 1.3, textAlign: "center", unicodeBidi: "isolate", whiteSpace: "nowrap", ...style }}>{s}</div>
);
const Ico: React.FC<{ name?: string; size: number; dim?: boolean; style?: React.CSSProperties }> = ({ name, size, dim, style }) =>
  name ? <Img src={staticFile(`icons-flat/${name}.svg`)} style={{ width: size, height: size, filter: dim ? "invert(1) brightness(.5)" : "invert(1)", ...style }} /> : null;
const Chip: React.FC<{ s: string; size?: number; bg?: string; color?: string }> = ({ s, size = 34, bg = C.blue, color = C.white }) => (
  <div style={{ background: bg, padding: `${size * 0.1}px ${size * 0.45}px`, borderRadius: size * 0.22, boxShadow: "0 10px 26px rgba(0,0,0,.35)" }}><Tx s={s} size={size} color={color} /></div>
);
/** A gold coin seen at an angle (3D look: rim + face), spinning when `spin` is set. */
export const Coin: React.FC<{ size?: number; spin?: number }> = ({ size = 70, spin = 0 }) => {
  const sx = Math.max(0.12, Math.abs(Math.cos(spin)));
  return <svg width={size} height={size * 0.75} viewBox="-50 -40 100 80" style={{ overflow: "visible" }}>
    <g transform={`scale(${sx} 1)`}>
      <ellipse cx={0} cy={8} rx={46} ry={26} fill={C.gold2} />
      <rect x={-46} y={-2} width={92} height={10} fill={C.gold2} />
      <ellipse cx={0} cy={-2} rx={46} ry={26} fill={C.gold} />
      <ellipse cx={0} cy={-2} rx={34} ry={18} fill="none" stroke={C.gold2} strokeWidth={3} />
      <text x={0} y={6} textAnchor="middle" fontFamily={CAIRO} fontWeight={900} fontSize={22} fill={C.gold2}>DH</text>
    </g>
  </svg>;
};
const fmt = (v: number) => Math.round(v).toLocaleString("fr-FR").replace(/ /g, " ");

/* ---------- modules ---------- */
/** Key words pop in one by one, each on its own spoken word. */
const Chips: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const items = fx.items ?? [];
  return <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
    {fx.title && <Tx s={fx.title} size={40} color={C.light} style={{ opacity: io(f, at, at + 8) }} />}
    {items.map((it, i) => {
      const st = it.at !== undefined ? it.at * FPS : at + 8 + i * 18;
      const sp = spring({ frame: f - st, fps: FPS, config: { damping: 13, stiffness: 170 } });
      const last = items.filter(x => (x.at !== undefined ? x.at * FPS : 0) <= f).length - 1;
      return <div key={i} dir="rtl" style={{ display: "flex", alignItems: "center", gap: 18, opacity: Math.min(1, sp * 1.4),
        transform: `perspective(900px) rotateX(${(1 - sp) * 70}deg) translateY(${(1 - sp) * 30}px)` }}>
        {it.icon && <div style={{ width: 84, height: 84, borderRadius: 22, background: i === last || it.at === undefined ? C.blue : "rgba(255,255,255,.08)", display: "grid", placeItems: "center" }}>
          <Ico name={it.icon} size={54} /></div>}
        <Tx s={it.label} size={44} />
      </div>;
    })}
  </div>;
};

/** Rubber stamp slams onto the frame (ممنوع / ✓ / ✗). */
const Stamp: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const sp = useSp(at, 11, 230);
  const shake = f > at && f < at + 8 ? Math.sin(f * 3) * (8 - (f - at)) : 0;
  const col = fx.good ? C.green : C.red;
  return <div style={{ transform: `translate(${shake}px, ${-shake}px) rotate(-12deg) scale(${f < at ? 0 : 2.4 - 1.4 * sp})`, opacity: f < at ? 0 : Math.min(1, sp * 2),
    border: `8px solid ${col}`, outline: `3px solid ${col}`, outlineOffset: 8, borderRadius: 18, padding: "6px 40px", background: "rgba(10,12,20,.35)" }}>
    <Tx s={fx.text ?? "ممنوع"} size={86} color={col} weight={900} />
  </div>;
};

/** Number counts up while coins drop onto a growing 3D stack. */
const Count: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const d = (fx.dur ?? 2) * FPS;
  const p = io(f, at, at + d), v = (fx.from ?? 0) + ((fx.value ?? 0) - (fx.from ?? 0)) * p;
  const coins = Math.round(p * 9);
  return <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
    {fx.title && <Tx s={fx.title} size={38} color={C.light} />}
    <div style={{ position: "relative", width: 260, height: 260 }}>
      {Array.from({ length: coins }).map((_, i) => {
        const land = at + (i / 9) * d, drop = io(f, land - 6, land, -220, 0);
        return <div key={i} style={{ position: "absolute", left: 60 + (i % 2) * 6, bottom: 10 + i * 18 - drop }}><Coin size={140} /></div>;
      })}
      {f > at - 4 && f < at + d && <div style={{ position: "absolute", left: 60, top: -20 - ((f - at) % 6) * 6 }}><Coin size={140} spin={f / 3} /></div>}
    </div>
    <div dir="ltr" style={{ fontFamily: CAIRO, fontWeight: 900, fontSize: 104, color: C.white, lineHeight: 1 }}>
      {fmt(v)}<span style={{ fontSize: 56, marginLeft: 10, color: C.gold }}>{fx.suffix ?? "DH"}</span></div>
    {fx.sub && <Chip s={fx.sub} size={32} />}
  </div>;
};

/** Calendar pages flip month after month, a +amount chip pops each time and the total adds up. */
const Calendar: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const n = fx.n ?? 6; const per = Math.max(10, ((fx.dur ?? 4) * FPS) / n);
  const k = Math.max(0, Math.min(n, Math.floor((f - at) / per) + 1)); const ph = ((f - at) % per) / per;
  const MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "ماي", "يونيو", "يوليوز", "غشت", "شتنبر", "أكتوبر", "نونبر", "دجنبر"];
  const page = (m: number, rot: number, z: number) => <div style={{ position: "absolute", inset: 0, transformOrigin: "50% 0%", transform: `rotateX(${rot}deg) translateZ(${z}px)`,
    backfaceVisibility: "hidden", background: "#F4F6FA", borderRadius: 22, boxShadow: "0 20px 40px rgba(0,0,0,.4)", overflow: "hidden" }}>
    <div style={{ height: 70, background: C.blue, display: "grid", placeItems: "center" }}><Tx s={MONTHS[m % 12]} size={36} /></div>
    <div style={{ display: "grid", placeItems: "center", height: 190 }}><Tx s={`${(m % 12) + 1}`} size={120} color={C.ink} weight={900} /></div>
  </div>;
  return <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 22 }}>
    {fx.title && <Tx s={fx.title} size={38} color={C.light} />}
    <div style={{ position: "relative", width: 280, height: 260, perspective: 900, opacity: io(f, at - 6, at) }}>
      {page(k, 0, 0)}
      {k > 0 && k < n && ph < 0.5 && page(k - 1, -io(ph, 0, 0.5, 0, 1) * 180 * 0.999, 1)}
      {fx.label && k > 0 && k <= n && (() => { const sp = spring({ frame: f - at - (k - 1) * per, fps: FPS, config: { damping: 12, stiffness: 180 } });
        return <div style={{ position: "absolute", right: -70, top: -30, transform: `scale(${sp}) translateY(${(1 - sp) * 30}px)` }}><Chip s={fx.label ?? ""} size={30} bg={C.green} /></div>; })()}
    </div>
    {fx.value !== undefined ? <div dir="ltr" style={{ fontFamily: CAIRO, fontWeight: 900, fontSize: 70, color: C.white }}>{fmt((fx.value ?? 0) * k)}<span style={{ fontSize: 40, color: C.gold, marginLeft: 8 }}>{fx.suffix ?? "DH"}</span></div>
      : <Tx s={`${Math.max(1, k)} / ${n}`} size={56} />}
    {fx.sub && <Chip s={fx.sub} size={32} />}
  </div>;
};

/** Clock hands race while coins pop out on each turn: time traded for money. */
const Clock: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const t = Math.max(0, f - at); const sp = useSp(at, 15, 140);
  const R = 150;
  return <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 20 }}>
    <div style={{ position: "relative", width: 420, height: 360, transform: `scale(${sp})` }}>
      <svg width={420} height={360} viewBox="-210 -180 420 360" style={{ position: "absolute" }}>
        <circle r={R + 14} fill="none" stroke={C.blue} strokeWidth={6} strokeDasharray={`${(2 * Math.PI * (R + 14)) * io(f, at, at + 40)} 2000`} transform="rotate(-90)" />
        <circle r={R} fill="rgba(255,255,255,.06)" stroke={C.white} strokeWidth={8} />
        {Array.from({ length: 12 }).map((_, i) => <line key={i} x1={0} y1={-R + 14} x2={0} y2={-R + (i % 3 ? 26 : 40)} stroke={C.light} strokeWidth={i % 3 ? 4 : 8} transform={`rotate(${i * 30})`} />)}
        <line x1={0} y1={0} x2={0} y2={-R * 0.55} stroke={C.white} strokeWidth={12} strokeLinecap="round" transform={`rotate(${t * 3})`} />
        <line x1={0} y1={0} x2={0} y2={-R * 0.82} stroke={C.blue2} strokeWidth={7} strokeLinecap="round" transform={`rotate(${t * 36})`} />
        <circle r={14} fill={C.white} />
      </svg>
      {Array.from({ length: 6 }).map((_, i) => {
        const st = at + 10 + i * 10, q = io(f, st, st + 22);
        if (f < st) return null;
        const ang = (i * 61 + 20) * Math.PI / 180;
        return <div key={i} style={{ position: "absolute", left: 175 + Math.cos(ang) * 230 * q, top: 140 - 120 * q + Math.sin(ang) * 60 * q + q * q * 120, opacity: 1 - io(f, st + 18, st + 26) }}>
          <Coin size={70} spin={f / 4 + i} /></div>;
      })}
    </div>
    <div dir="rtl" style={{ display: "flex", gap: 18, alignItems: "center", opacity: io(f, at + 14, at + 24) }}>
      <Chip s={fx.a?.label ?? "وقتك"} size={34} bg="rgba(255,255,255,.12)" /><Tx s="←" size={40} /><Chip s={fx.b?.label ?? "فلوس"} size={34} bg={C.gold2} />
    </div>
  </div>;
};

/** Price tags swing in, their numbers climb with a red up-arrow. */
const Tags: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const items = fx.items ?? [];
  return <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 16 }}>
    {fx.title && <Tx s={fx.title} size={38} color={C.light} />}
    <div dir="rtl" style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      {items.map((it, i) => {
        const st = it.at !== undefined ? it.at * FPS : at + i * 12;
        const sp = spring({ frame: f - st, fps: FPS, config: { damping: 8, stiffness: 120 } });
        const v = interpolate(f, [st + 10, st + 50], [it.from ?? 0, it.to ?? 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const up = io(f, st + 10, st + 50);
        return <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, transformOrigin: "90% 0%", transform: `rotate(${(1 - sp) * 28}deg)`, opacity: Math.min(1, sp * 2) }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14, background: "#F4F6FA", padding: "8px 26px 8px 20px", borderRadius: "16px 50px 50px 16px", minWidth: 420, position: "relative" }}>
            <div style={{ width: 18, height: 18, borderRadius: 9, background: C.ink, opacity: 0.6 }} />
            <Ico name={it.icon} size={50} style={{ filter: "none" }} />
            <Tx s={it.label} size={34} color={C.ink} />
            <div dir="ltr" style={{ marginRight: "auto", fontFamily: CAIRO, fontWeight: 900, fontSize: 40, color: up > 0.02 ? "#D7263D" : C.ink }}>{fmt(v)} DH</div>
          </div>
          <svg width={40} height={56} style={{ opacity: up, transform: `translateY(${(1 - up) * 20}px)` }}><polygon points="20,0 40,24 28,24 28,56 12,56 12,24 0,24" fill={C.red} /></svg>
        </div>;
      })}
    </div>
  </div>;
};

/** Receipt prints line by line (each line on its spoken word), then the total stamps at the bottom. */
const Receipt: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const items = fx.items ?? [];
  const starts = items.map((it, i) => it.at !== undefined ? it.at * FPS : at + 10 + i * 16);
  const end = (starts[starts.length - 1] ?? at) + 18;
  const shown = starts.filter(s => f >= s).length;
  const total = items.reduce((a, it, i) => a + (f >= starts[i] ? (it.value ?? 0) * io(f, starts[i], starts[i] + 12) : 0), 0);
  const h = 120 + shown * 74 + (f > end ? 110 : 0);
  return <div style={{ width: 470, height: io(f, at - 6, at + 6, 0, 1) * Math.min(h, 700), overflow: "hidden", position: "relative", transition: "none" }}>
    <div style={{ background: "#F6F4EE", padding: "26px 34px 40px", clipPath: "polygon(0 0,100% 0,100% calc(100% - 16px),94% 100%,88% calc(100% - 16px),82% 100%,76% calc(100% - 16px),70% 100%,64% calc(100% - 16px),58% 100%,52% calc(100% - 16px),46% 100%,40% calc(100% - 16px),34% 100%,28% calc(100% - 16px),22% 100%,16% calc(100% - 16px),10% 100%,4% calc(100% - 16px),0 100%)", boxShadow: "0 30px 60px rgba(0,0,0,.45)" }}>
      <Tx s={fx.title ?? "مصاريف الشهر"} size={36} color={C.ink} weight={900} />
      <div style={{ borderTop: `3px dashed ${C.mid}`, margin: "12px 0 6px" }} />
      {items.map((it, i) => f >= starts[i] && <div key={i} dir="rtl" style={{ display: "flex", alignItems: "center", gap: 14, height: 74, opacity: io(f, starts[i], starts[i] + 6) }}>
        <Ico name={it.icon} size={44} style={{ filter: "none" }} /><Tx s={it.label} size={34} color={C.ink} />
        {it.value !== undefined && <div dir="ltr" style={{ marginRight: "auto", fontFamily: CAIRO, fontWeight: 800, fontSize: 32, color: C.ink }}>{fmt(it.value)}</div>}
      </div>)}
      {f > end && <div dir="rtl" style={{ borderTop: `4px solid ${C.ink}`, marginTop: 8, paddingTop: 10, display: "flex", alignItems: "center", opacity: io(f, end, end + 8) }}>
        <Tx s={fx.label ?? "المجموع"} size={38} color={C.ink} weight={900} />
        {items.some(it => it.value !== undefined) && <div dir="ltr" style={{ marginRight: "auto", fontFamily: CAIRO, fontWeight: 900, fontSize: 42, color: "#D7263D" }}>{fmt(total)} DH</div>}
      </div>}
    </div>
  </div>;
};

/** Line chart drawing itself (up, down, or flat income vs rising costs = the gap). */
const Line: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const W = 520, H = 340; const t = io(f, at, at + (fx.dur ?? 2.2) * FPS);
  const fnA = fx.kind === "down" ? (x: number) => 0.85 - x * 0.65 + Math.sin(x * 14) * 0.04 : (x: number) => 0.12 + x * 0.72 + Math.sin(x * 12) * 0.05;
  const fnB = (x: number) => 0.42;
  const path = (fn: (x: number) => number) => Array.from({ length: 50 }, (_, i) => i / 49).filter(x => x <= t)
    .map(x => `${30 + x * (W - 60)},${H - 30 - fn(x) * (H - 60)}`).join(" ");
  const endA = [30 + t * (W - 60), H - 30 - fnA(t) * (H - 60)];
  const colA = fx.kind === "down" ? C.green : C.red;
  return <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
    {fx.title && <Tx s={fx.title} size={38} color={C.light} />}
    <svg width={W} height={H} style={{ overflow: "visible" }}>
      {[0, 1, 2, 3].map(k => <line key={k} x1={30} x2={W - 30} y1={30 + k * (H - 60) / 3} y2={30 + k * (H - 60) / 3} stroke={C.gray} strokeOpacity={0.5} strokeWidth={1.5} />)}
      {fx.kind === "gap" && <>
        <polygon points={`${path(fnA)} ${path(fnB).split(" ").reverse().join(" ")}`} fill={C.red} opacity={0.18} />
        <polyline points={path(fnB)} fill="none" stroke={C.light} strokeWidth={7} strokeLinecap="round" />
        <circle cx={30 + t * (W - 60)} cy={H - 30 - fnB(t) * (H - 60)} r={11} fill={C.light} /></>}
      <polyline points={path(fnA)} fill="none" stroke={colA} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" style={{ filter: `drop-shadow(0 0 10px ${colA})` }} />
      <circle cx={endA[0]} cy={endA[1]} r={13} fill={colA} />
      {fx.label && <foreignObject x={Math.min(endA[0] - 90, W - 200)} y={endA[1] - 80} width={260} height={70}><div style={{ display: "flex" }}><Chip s={fx.label} size={30} bg={colA} /></div></foreignObject>}
    </svg>
    {fx.kind === "gap" && <div dir="rtl" style={{ display: "flex", gap: 30 }}>
      <Tx s={`● ${fx.a?.label ?? "المداخل"}`} size={30} color={C.light} /><Tx s={`● ${fx.b?.label ?? "المصاريف"}`} size={30} color={C.red} /></div>}
  </div>;
};

/** Balance beam: two pans, tips toward the heavier side. */
const Scale: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const sp = useSp(at + 14, 7, 60);
  const ang = (fx.tip === "a" ? -1 : 1) * 14 * sp; const L = 210;
  const pan = (side: -1 | 1, it?: FxItem) => {
    const x = side * L * Math.cos(ang * Math.PI / 180), y = side * L * Math.sin(ang * Math.PI / 180);
    return <div style={{ position: "absolute", left: 260 + x - 110, top: 120 + y, width: 220, display: "flex", flexDirection: "column", alignItems: "center" }}>
      <svg width={220} height={70}><line x1={110} y1={0} x2={30} y2={60} stroke={C.light} strokeWidth={3} /><line x1={110} y1={0} x2={190} y2={60} stroke={C.light} strokeWidth={3} />
        <path d="M10 60 Q110 100 210 60 Z" fill={C.light} /></svg>
      <div style={{ marginTop: -110, display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}><Ico name={it?.icon} size={70} />
        <div style={{ marginTop: 60 }}><Chip s={it?.label ?? ""} size={30} bg={(side === -1) === (fx.tip === "a") ? C.blue : "rgba(255,255,255,.14)"} /></div></div>
    </div>;
  };
  return <div style={{ position: "relative", width: 520, height: 420, opacity: io(f, at, at + 8) }}>
    <svg width={520} height={420} style={{ position: "absolute" }}>
      <polygon points="260,110 230,380 290,380" fill={C.gray} /><rect x={180} y={380} width={160} height={14} rx={7} fill={C.gray} />
      <line x1={260 - L * Math.cos(ang * Math.PI / 180)} y1={120 - L * Math.sin(ang * Math.PI / 180)} x2={260 + L * Math.cos(ang * Math.PI / 180)} y2={120 + L * Math.sin(ang * Math.PI / 180)} stroke={C.white} strokeWidth={10} strokeLinecap="round" />
      <circle cx={260} cy={120} r={14} fill={C.blue} />
    </svg>
    {pan(-1, fx.a)}{pan(1, fx.b)}
  </div>;
};

/** Tiles stand in a row seen in 3D; each falls onto the next, faster every time (compound effect). */
const Domino: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const n = fx.n ?? 6;
  const starts: number[] = []; let t = at + 6, gap = 26; for (let i = 0; i < n; i++) { starts.push(t); t += gap; gap = Math.max(5, gap * 0.72); }
  return <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 30 }}>
    {fx.title && <Tx s={fx.title} size={38} color={C.light} />}
    <div style={{ perspective: 1200 }}>
      <div dir="ltr" style={{ position: "relative", width: 640, height: 300, transformStyle: "preserve-3d", transform: "rotateX(18deg) rotateY(-28deg)" }}>
        <div style={{ position: "absolute", left: -30, bottom: -16, width: 700, height: 16, background: C.gray, borderRadius: 8, boxShadow: `0 0 40px ${C.blue}44` }} />
        {starts.map((st, i) => {
          const fall = io(f, st, st + 9); const h = 120 + i * 30, w = 30 + i * 4;
          const lit = fall > 0.5;
          return <div key={i} style={{ position: "absolute", left: 20 + i * 104, bottom: 0, width: w, height: h, transformOrigin: "100% 100%",
            transform: `rotate(${fall * (i === n - 1 ? 80 : 58)}deg)`, borderRadius: 6,
            background: lit ? `linear-gradient(90deg, ${C.blue}, ${C.blue2})` : "linear-gradient(90deg, #C9D2E0, #F4F6FA)",
            boxShadow: `${lit ? `0 0 26px ${C.blue}` : "0 10px 20px rgba(0,0,0,.4)"}, inset -8px 0 0 rgba(0,0,0,.18)` }}>
            <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
              <div style={{ writingMode: "vertical-rl", fontFamily: CAIRO, fontWeight: 900, fontSize: 22, color: lit ? C.white : C.ink }}>{i + 1}</div></div>
          </div>;
        })}
      </div>
    </div>
    <div dir="ltr" style={{ display: "flex", gap: 10, opacity: io(f, at + 6, at + 14) }}>
      {starts.map((st, i) => <div key={i} style={{ transform: `scale(${spring({ frame: f - st - 6, fps: FPS, config: { damping: 12, stiffness: 180 } })})` }}>
        <Chip s={`${fx.label ?? "Asset"} ${i + 1}`} size={22} bg={i === 0 ? C.blue : "rgba(255,255,255,.14)"} /></div>)}
    </div>
  </div>;
};

/** Coins travel along an arc from A to B (money moving between two things). */
const Flow: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const W = 540;
  const node = (it: FxItem | undefined, st: number) => { const sp = spring({ frame: f - st, fps: FPS, config: { damping: 13, stiffness: 160 } });
    return <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10, transform: `scale(${sp})`, width: 170 }}>
      <div style={{ width: 130, height: 130, borderRadius: 34, background: "rgba(255,255,255,.08)", border: `2px solid ${C.blue2}66`, display: "grid", placeItems: "center" }}><Ico name={it?.icon} size={80} /></div>
      <Tx s={it?.label ?? ""} size={32} /></div>; };
  return <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6 }}>
    {fx.title && <Tx s={fx.title} size={38} color={C.light} />}
    <div dir="ltr" style={{ position: "relative", width: W, height: 330, display: "flex", alignItems: "flex-end", justifyContent: "space-between" }}>
      {node(fx.a, at)}{node(fx.b, at + 8)}
      <svg width={W} height={330} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        <path d={`M85 160 Q${W / 2} -40 ${W - 85} 160`} fill="none" stroke={C.blue2} strokeWidth={4} strokeDasharray="12 10" opacity={io(f, at + 8, at + 16)} />
      </svg>
      {Array.from({ length: 5 }).map((_, i) => {
        const st = at + 16 + i * 9; if (f < st) return null;
        const q = ((f - st) % 45) / 45;
        const x = (1 - q) * (1 - q) * 85 + 2 * (1 - q) * q * (W / 2) + q * q * (W - 85), y = (1 - q) * (1 - q) * 160 + 2 * (1 - q) * q * -40 + q * q * 160;
        return <div key={i} style={{ position: "absolute", left: x - 35, top: y - 26 }}>{fx.icon
          ? <div style={{ width: 64, height: 64, borderRadius: 32, background: C.blue, display: "grid", placeItems: "center", boxShadow: `0 0 20px ${C.blue}` }}><Ico name={fx.icon} size={38} /></div>
          : <Coin size={70} spin={f / 4 + i} />}</div>;
      })}
    </div>
    {fx.label && <div style={{ opacity: io(f, at + 24, at + 32) }}><Chip s={fx.label} size={32} /></div>}
  </div>;
};

/** Wireframe globe turning; pins drop on places as they are named. */
const Globe: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const R = 190; const rot = (f - at) * 0.6;
  return <div style={{ position: "relative", width: 480, height: 460, opacity: io(f, at - 6, at + 4) }}>
    <svg width={480} height={460} viewBox="-240 -230 480 460" style={{ position: "absolute" }}>
      <defs><radialGradient id="gl" cx="35%" cy="30%"><stop offset="0" stopColor="#2C4C8F" /><stop offset="1" stopColor="#0E1830" /></radialGradient></defs>
      <circle r={R} fill="url(#gl)" stroke={C.blue2} strokeWidth={3} />
      {[-60, -30, 0, 30, 60].map(lat => { const y = -R * Math.sin(lat * Math.PI / 180), rx = R * Math.cos(lat * Math.PI / 180);
        return <ellipse key={lat} cx={0} cy={y} rx={rx} ry={rx * 0.12} fill="none" stroke={C.blue2} strokeOpacity={0.35} strokeWidth={1.5} />; })}
      {Array.from({ length: 8 }).map((_, i) => { const a = ((i * 22.5 + rot) % 180) * Math.PI / 180;
        return <ellipse key={i} cx={0} cy={0} rx={Math.abs(R * Math.cos(a))} ry={R} fill="none" stroke={C.blue2} strokeOpacity={0.35} strokeWidth={1.5} />; })}
    </svg>
    {(fx.items ?? []).map((it, i) => {
      const st = it.at !== undefined ? it.at * FPS : at + 10 + i * 20;
      const sp = spring({ frame: f - st, fps: FPS, config: { damping: 9, stiffness: 160 } });
      if (f < st) return null;
      return <div key={i} style={{ position: "absolute", left: 240 + (it.x ?? 0), top: 230 + (it.y ?? 0), transform: `translate(-50%, -100%) translateY(${(1 - sp) * -80}px)`, opacity: Math.min(1, sp * 2),
        display: "flex", flexDirection: "column", alignItems: "center" }}>
        <Chip s={it.label} size={28} bg={it.icon === "cross_mark" ? C.red : C.blue} />
        <svg width={30} height={40}><path d="M15 40 L4 14 A12 12 0 1 1 26 14 Z" fill={C.white} /><circle cx={15} cy={12} r={5} fill={C.blue} /></svg>
      </div>;
    })}
  </div>;
};

/** Progress meter filling (from → to), e.g. energy, savings, goal. */
const Meter: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const p = io(f, at + 4, at + (fx.dur ?? 1.6) * FPS, (fx.from ?? 0) / 100, (fx.to ?? 100) / 100);
  return <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 20, opacity: io(f, at, at + 6) }}>
    {fx.icon && <Ico name={fx.icon} size={120} />}
    {fx.title && <Tx s={fx.title} size={40} color={C.light} />}
    <div style={{ width: 480, height: 56, borderRadius: 28, background: "rgba(255,255,255,.08)", border: `2px solid ${C.blue2}66`, overflow: "hidden" }}>
      <div style={{ width: `${p * 100}%`, height: "100%", background: `linear-gradient(90deg, ${C.blue}, ${C.blue2})`, boxShadow: `0 0 30px ${C.blue}` }} /></div>
    <div dir="ltr" style={{ fontFamily: CAIRO, fontWeight: 900, fontSize: 80, color: C.white, lineHeight: 1 }}>{Math.round(p * 100)}<span style={{ fontSize: 44 }}>%</span></div>
    {fx.label && <Chip s={fx.label} size={32} />}
  </div>;
};

/** Hand-drawn ring around a spot on the photo, with a label. Uses full-frame coordinates. */
const Ring: React.FC<{ fx: Fx; at: number }> = ({ fx, at }) => {
  const f = useCurrentFrame(); const r = fx.r ?? 140, x = fx.x ?? 960, y = fx.y ?? 480; const p = io(f, at, at + 14);
  return <AbsoluteFill>
    <svg width={1920} height={1080} style={{ position: "absolute" }}>
      <ellipse cx={x} cy={y} rx={r * 1.15} ry={r} fill="none" stroke={C.white} strokeWidth={9} strokeLinecap="round" pathLength={1}
        strokeDasharray={`${p} 1`} transform={`rotate(-8 ${x} ${y})`} style={{ filter: "drop-shadow(0 4px 10px rgba(0,0,0,.6))" }} />
    </svg>
    {fx.label && <div style={{ position: "absolute", left: x + r * 1.1, top: y - r - 40, transform: `scale(${spring({ frame: f - at - 10, fps: FPS, config: { damping: 12, stiffness: 170 } })})`, transformOrigin: "0 100%" }}>
      <Chip s={fx.label} size={40} /></div>}
  </AbsoluteFill>;
};

const MODULES: Record<Fx["k"], React.FC<{ fx: Fx; at: number }>> = {
  chips: Chips, stamp: Stamp, count: Count, calendar: Calendar, clock: Clock, tags: Tags, receipt: Receipt, line: Line,
  scale: Scale, domino: Domino, flow: Flow, globe: Globe, meter: Meter, ring: Ring,
};

/** One idea animation. On photos/clips it sits in a glass panel that swings in in 3D; `full` plays it big on the card. */
export const IdeaFx: React.FC<{ fx: Fx; dur: number }> = ({ fx, dur }) => {
  const f = useCurrentFrame(); const at = Math.round((fx.at ?? 0.3) * FPS);
  const M = MODULES[fx.k]; if (!M) return null;
  if (fx.k === "ring") return <M fx={fx} at={at} />;
  if (fx.k === "stamp") return <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingBottom: 120 }}><M fx={fx} at={at} /></AbsoluteFill>;
  if (fx.pos === "full") {
    return <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", perspective: 1800 }}>
      <div style={{ transform: `scale(1.35) rotateY(${interpolate(f, [0, dur], [-7, 7])}deg) rotateX(${4 - 2 * io(f, 0, dur)}deg)`, transformStyle: "preserve-3d" }}><M fx={fx} at={at} /></div>
    </AbsoluteFill>;
  }
  const left = fx.pos === "left";
  const sp = spring({ frame: f - at + 8, fps: FPS, config: { damping: 16, stiffness: 120 } });
  const out = io(f, dur - 10, dur);
  return <AbsoluteFill style={{ perspective: 1600 }}>
    <div style={{ position: "absolute", top: 140, [left ? "left" : "right"]: 110, width: 640, height: 660, borderRadius: 34,
      background: "linear-gradient(160deg, rgba(30,40,62,.78), rgba(12,16,28,.82))", border: "1.5px solid rgba(255,255,255,.16)",
      boxShadow: "0 50px 90px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.18)", backdropFilter: "blur(18px)",
      display: "flex", alignItems: "center", justifyContent: "center", opacity: sp * (1 - out),
      transformOrigin: left ? "0% 50%" : "100% 50%",
      transform: `rotateY(${(left ? 1 : -1) * ((1 - sp) * 70 + 9 + Math.sin(f / 40) * 2)}deg) rotateX(${2 + Math.cos(f / 50) * 1.5}deg) translateZ(${(1 - sp) * -200}px)` } as React.CSSProperties}>
      <M fx={fx} at={at} />
    </div>
  </AbsoluteFill>;
};
