// Documentary explainer style (reference: Aziz Nawfal / Vox-like): charcoal + grain + vignette, flat white pictograms,
// one blue accent for labels, white boxes on footage, Cairo font. Same beats.json as Explainer.tsx.
import React from "react";
import { AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { loadFont } from "@remotion/google-fonts/Cairo";
import type { Beat as BaseBeat, Item } from "./types";
import { BRAND } from "./brand";
import { IdeaFx, type Fx } from "./IdeaFx";
type Beat = BaseBeat & { fx?: Fx[] };

const { fontFamily: CAIRO } = loadFont("normal", { weights: ["600", "700", "800", "900"], subsets: ["arabic", "latin"] });
const FPS = 30;
const C = { bg: "#151A24", bg2: "#1D2533", gray: "#4B586C", mid: "#8C98AA", light: "#D3DAE4", white: "#FFFFFF", red: BRAND.accent /* accent */, blue2: "#5B9BFF", ink: "#0E1320" };
const ar = (s?: string) => /[\u0621-\u064A\u0671-\u06D3]/.test(s ?? ""); // Arabic letters only (not ؟ ، punctuation)
const ease = Easing.bezier(0.2, 0.9, 0.25, 1);
const io = (f: number, a: number, b: number, from = 0, to = 1) =>
  interpolate(f, [a, b], [from, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });

/* ---------- base layers ---------- */
const Backdrop: React.FC = () => {
  const f = useCurrentFrame();
  const sky = [[0, 140], [90, 230], [170, 120], [250, 300], [330, 180], [420, 260], [500, 150], [590, 340], [680, 210], [760, 160], [850, 280],
    [940, 190], [1030, 250], [1120, 140], [1200, 320], [1290, 200], [1380, 240], [1470, 150], [1560, 290], [1650, 180], [1740, 230], [1830, 160]];
  return (
    <AbsoluteFill
      style={{ background: `radial-gradient(90% 80% at 50% 42%, ${C.bg2} 0%, ${C.bg} 55%, #0B0F17 100%)` }}
    >
      {/* faint city skyline, like the reference's grey silhouettes */}
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: 0.18, transform: `translateX(${Math.sin(f / 300) * 12}px)` }}>
        {sky.map(([x, h], i) => <rect key={i} x={x} y={1080 - h} width={86} height={h} fill={C.gray} />)}
        {sky.filter((_, i) => i % 3 === 0).map(([x, h], i) => <polygon key={`t${i}`} points={`${x},${1080 - h} ${x + 43},${1080 - h - 50} ${x + 86},${1080 - h}`} fill={C.gray} />)}
      </svg>
      {/* designed shapes: blue glow, dot grid, rotating rings, drifting outlines, light beams */}
      <AbsoluteFill style={{ background: `radial-gradient(40% 35% at 78% 18%, ${C.red}33, transparent 70%), radial-gradient(35% 30% at 12% 85%, ${C.blue2}22, transparent 70%)` }} />
      <AbsoluteFill style={{ backgroundImage: `radial-gradient(${C.blue2}2E 1.6px, transparent 1.6px)`, backgroundSize: "44px 44px", backgroundPosition: `${(f * 0.15) % 44}px 0px`,
        maskImage: "radial-gradient(60% 55% at 50% 45%, transparent 35%, black 100%)", WebkitMaskImage: "radial-gradient(60% 55% at 50% 45%, transparent 35%, black 100%)" }} />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <g transform={`translate(1640 230) rotate(${f * 0.08})`} fill="none" stroke={C.red} strokeOpacity={0.28}>
          <circle r={260} strokeWidth={2} strokeDasharray="6 14" /><circle r={190} strokeWidth={1.5} /><circle r={120} strokeWidth={1} strokeDasharray="2 10" />
        </g>
        <g transform={`translate(230 900) rotate(${-f * 0.06})`} fill="none" stroke={C.blue2} strokeOpacity={0.22}>
          <circle r={210} strokeWidth={1.5} strokeDasharray="10 18" /><circle r={140} strokeWidth={1.2} />
        </g>
        {[[300, 210, 70, 0], [1500, 760, 90, 40], [880, 120, 46, 80], [1180, 930, 60, 120], [120, 480, 40, 160]].map(([x, y, s2, ph], i) =>
          <rect key={`sq${i}`} x={-s2 / 2} y={-s2 / 2} width={s2} height={s2} rx={6} fill="none" stroke={i % 2 ? C.blue2 : C.red} strokeOpacity={0.3} strokeWidth={2}
            transform={`translate(${x + Math.sin((f + ph) / 90) * 18} ${y + Math.cos((f + ph) / 110) * 14}) rotate(${(f + ph) * 0.2})`} />)}
        {[[1040, 300], [400, 640], [1720, 560]].map(([x, y], i) =>
          <polygon key={`tr${i}`} points="0,-30 26,15 -26,15" fill="none" stroke={C.blue2} strokeOpacity={0.3} strokeWidth={2}
            transform={`translate(${x + Math.cos((f + i * 50) / 100) * 16} ${y + Math.sin((f + i * 50) / 80) * 16}) rotate(${-(f + i * 40) * 0.25})`} />)}
        <g opacity={0.12}>
          {[0, 1, 2].map(i => <line key={`ln${i}`} x1={-400 + i * 120 + ((f * 0.6) % 600)} y1={0} x2={500 + i * 120 + ((f * 0.6) % 600)} y2={1080} stroke={C.red} strokeWidth={i === 1 ? 3 : 1.2} />)}
        </g>
      </svg>
      {/* film grain */}
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: 0.09, mixBlendMode: "overlay" }}>
        <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 7} /></filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
      <AbsoluteFill
        style={{
          boxShadow: "inset 0 0 260px 60px rgba(0,0,0,.55)",
          color: "#000000",
          backgroundColor: "rgba(255, 255, 255, 0)"
        }}
      />
    </AbsoluteFill>
  );
};

const T: React.FC<{ s: string; size: number; weight?: number; color?: string; style?: React.CSSProperties }> = ({ s, size, weight = 800, color = C.white, style }) => (
  <div dir={ar(s) ? "rtl" : "ltr"} style={{ fontFamily: CAIRO, fontSize: size, fontWeight: weight, color, lineHeight: 1.35, unicodeBidi: "isolate", textAlign: "center", ...style }}>{s}</div>
);
const RedLabel: React.FC<{ s: string; size?: number; at?: number }> = ({ s, size = 54, at = 0 }) => {
  const f = useCurrentFrame(), p = io(f, at, at + 10);
  return <div style={{ display: "inline-block", background: C.red, padding: `${size * 0.08}px ${size * 0.42}px`, clipPath: `inset(0 ${(1 - p) * 100}% 0 0)` }}>
    <T s={s} size={size} weight={800} /></div>;
};
const WhiteLabel: React.FC<{ s: string; size?: number; at?: number }> = ({ s, size = 54, at = 0 }) => {
  const f = useCurrentFrame(), p = io(f, at, at + 10);
  return <div style={{ display: "inline-block", background: C.white, padding: `${size * 0.06}px ${size * 0.4}px`, clipPath: `inset(0 0 0 ${(1 - p) * 100}%)` }}>
    <T s={s} size={size} weight={800} color={C.ink} /></div>;
};
/** Flat white pictogram (Fluent high-contrast SVG, recoloured). dim = grey "inactive" look. */
const Pict: React.FC<{ name?: string; size: number; at?: number; dim?: boolean }> = ({ name, size, at = 0, dim }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  if (!name) return null;
  const sp = spring({ frame: f - at, fps, config: { damping: 18, stiffness: 140 } });
  return <Img src={staticFile(`icons-flat/${name}.svg`)} style={{ width: size, height: size, opacity: sp,
    transform: `translateY(${(1 - sp) * 30}px) scale(${0.85 + 0.15 * sp})`,
    filter: dim ? "invert(1) brightness(.45)" : "invert(1) drop-shadow(0 18px 24px rgba(0,0,0,.45))" }} />;
};
const Words: React.FC<{ s: string; size: number; at?: number; color?: string }> = ({ s, size, at = 4, color = C.white }) => {
  const f = useCurrentFrame();
  const words: string[] = [];
  for (const w of s.split(" ")) { const p = words[words.length - 1]; if (p !== undefined && ar(s) && !ar(w) && !ar(p)) words[words.length - 1] = p + " " + w; else words.push(w); }
  return <div dir={ar(s) ? "rtl" : "ltr"} style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: `0 ${size * 0.25}px`, maxWidth: 1500 }}>
    {words.flatMap(w => { const m = ar(s) && !ar(w) ? w.match(/^(.*?)([؟،:!?.…]+)$/) : null; return m && m[1] ? [m[1], m[2]] : [w]; }).map((w, i) => { const p = io(f, at + i * 3, at + i * 3 + 9);
      const punct = /^[؟،:!?.…]+$/.test(w);
      return <span key={i} dir={ar(w) || punct ? "rtl" : "ltr"} style={{ unicodeBidi: "isolate", whiteSpace: "nowrap", fontFamily: CAIRO, fontWeight: 800, fontSize: size, color, lineHeight: 1.35,
        marginRight: punct ? -size * 0.22 : 0, opacity: p, transform: `translateY(${(1 - p) * 16}px)` }}>{w}</span>; })}
  </div>;
};
const PUNCH = 75; // a "cut" every 2.5 s: quick zoom step so long shots never feel static
const punch = (f: number, step: number, max: number) => {
  const k = Math.floor(f / PUNCH), p = io(f - k * PUNCH, 0, 7);
  return Math.min(max, 1 + step * (k + p));
};
const Scene: React.FC<{ dur: number; media?: boolean; children: React.ReactNode }> = ({ dur, media, children }) => {
  const f = useCurrentFrame();
  const inP = io(f, 0, 6), outP = io(f, dur - 6, dur);
  const z = media ? 1 : punch(f, 0.018, 1.08);
  return <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: inP * (1 - outP),
    transform: `scale(${z * (0.96 + 0.04 * inP)}) translateY(${(1 - inP) * 20}px)` }}>{children}</AbsoluteFill>;
};
/** Media motion: strong push + a punch-in "cut" every 2.5 s that also re-frames left/right. */
const mediaMotion = (f: number, dur: number) => {
  const k = Math.floor(f / PUNCH), p = io(f - k * PUNCH, 0, 7);
  const z = interpolate(f, [0, dur], [1.04, 1.16]) + Math.min(0.18, 0.06 * (k + p));
  const dir = k % 2 ? -1 : 1, x = dir * interpolate(f - k * PUNCH, [0, PUNCH], [-28, 28], { extrapolateRight: "clamp" });
  return `scale(${z}) translateX(${x}px)`;
};
const MEDIA_ICON: Record<string, string> = {
  inbox: "e_mail", support: "speech_balloon", singapore: "globe_with_meridians", chess: "balance_scale", learning: "books", jet: "airplane",
  office: "office_building", doctor: "briefcase", investor: "handshake", garage: "house", family: "beach_with_umbrella", bills: "receipt",
  wealth: "money_bag", prices: "shopping_cart", notebook: "memo", business: "factory", savings: "coin", worklate: "laptop", invest: "chart_increasing",
  realestate: "house", container: "factory", skills: "brain", path: "rocket", shoes: "check_mark_button", services: "laptop", assets: "key",
  team: "link", compound: "gem_stone", dominoes: "gem_stone", mountain: "trophy", beach: "beach_with_umbrella", agadir: "seedling", notifications: "mobile_phone",
  v_brain: "brain", v_rules: "balance_scale", v_partner: "handshake", v_relax: "smiling_face_with_sunglasses", v_city: "office_building", v_bills: "receipt",
  v_worklate: "laptop", v_capital: "money_bag", v_climb: "trophy", v_free: "crown", v_focus: "fire", v_older: "hourglass_not_done", v_talk: "speech_balloon",
  v_busy: "mobile_phone", v_success: "party_popper", v_how: "money_with_wings", v_plan: "memo", v_passive: "key", v_asset: "house", v_confused: "thinking_face", v_teach: "graduation_cap",
};
const mediaIcon = (src?: string) => { const k = (src ?? "").split("/").pop()?.replace(/\.(jpg|png|mp4)$/, "") ?? ""; return MEDIA_ICON[k]; };
/** Quick icon pop on photos/clips: a blue disc with a white pictogram, bouncing in from the side. */
const MediaPop: React.FC<{ icon?: string }> = ({ icon }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  if (!icon) return null;
  const sp = spring({ frame: f - 10, fps, config: { damping: 11, stiffness: 170 } });
  const k = Math.floor(f / PUNCH), side = k % 2 ? 1 : 0;
  return <div style={{ position: "absolute", top: 330, [side ? "left" : "right"]: 120, width: 170, height: 170, borderRadius: 85, background: C.red,
    display: "grid", placeItems: "center", transform: `scale(${sp}) rotate(${(1 - sp) * -25}deg)`, boxShadow: "0 20px 50px rgba(0,0,0,.5), 0 0 0 10px rgba(31,107,255,.25)" } as React.CSSProperties}>
    <Img src={staticFile(`icons-flat/${icon}.svg`)} style={{ width: 100, height: 100, filter: "invert(1)" }} />
  </div>;
};

/* ---------- scene types ---------- */
const Title: React.FC<{ b: Beat }> = ({ b }) => (
  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
    <Pict name={b.icon} size={300} at={0} />
    <RedLabel s={b.title ?? ""} size={b.title && b.title.length > 26 ? 62 : 78} at={6} />
    {b.sub && <Words s={b.sub} size={40} at={16} color={C.light} />}
  </div>
);

const Icons: React.FC<{ b: Beat }> = ({ b }) => {
  const f = useCurrentFrame(); const items = b.items ?? [];
  const dur = (b.to - b.from) * FPS, per = Math.max(18, Math.min(60, (dur - 30) / Math.max(1, items.length)));
  const active = Math.min(items.length - 1, Math.max(0, Math.floor((f - 10) / per)));
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 60 }}>
      {b.title && <Words s={b.title} size={64} at={0} />}
      <div dir="rtl" style={{ display: "flex", gap: 110, alignItems: "flex-end" }}>
        {items.map((it, i) => {
          const st = 8 + i * 6, on = i === active;
          return <div key={i} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 22, opacity: io(f, st, st + 10) }}>
            <Pict name={it.icon} size={on ? 220 : 180} at={st} dim={!on} />
            {on ? <RedLabel s={it.label} size={42} at={st + 4} /> : <T s={it.label} size={40} weight={700} color={C.mid} />}
            {it.sub && <T s={it.sub} size={28} weight={600} color={C.light} />}
          </div>;
        })}
      </div>
    </div>
  );
};

const Check: React.FC<{ ok: boolean; at: number }> = ({ ok, at }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const sp = spring({ frame: f - at, fps, config: { damping: 14, stiffness: 160 } });
  return <div style={{ width: 62, height: 62, borderRadius: 31, background: ok ? C.white : C.gray, display: "grid", placeItems: "center", flex: "none",
    transform: `scale(${sp})`, fontFamily: CAIRO, fontWeight: 900, fontSize: 38, color: ok ? C.ink : C.white }}>{ok ? "✓" : "✗"}</div>;
};

const Steps: React.FC<{ b: Beat }> = ({ b }) => {
  const f = useCurrentFrame(); const items = b.items ?? [];
  const per = Math.max(10, Math.min(40, Math.floor(((b.to - b.from) * FPS - 40) / Math.max(1, items.length))));
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 120 }}>
      {b.icon && <Pict name={b.icon} size={300} at={2} />}
      <div style={{ display: "flex", flexDirection: "column", gap: 34, minWidth: 820 }}>
        {b.title && <div style={{ marginBottom: 14 }}><Words s={b.title + ":"} size={60} at={0} /></div>}
        {items.map((it, i) => {
          const st = 10 + i * per;
          return <div key={i} dir="rtl" style={{ display: "flex", alignItems: "center", gap: 26, opacity: io(f, st, st + 8), transform: `translateX(${io(f, st, st + 12, -40, 0)}px)` }}>
            <Check ok at={st + 2} />
            <T s={it.label} size={50} weight={800} style={{ textAlign: "right" }} />
          </div>;
        })}
      </div>
    </div>
  );
};

const Stat: React.FC<{ b: Beat }> = ({ b }) => {
  const f = useCurrentFrame();
  const p = io(f, 6, 36), v = Math.round((b.value ?? 0) * p);
  const latin = b.suffix && !ar(b.suffix);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
      {b.title && <Words s={b.title} size={58} at={0} color={C.light} />}
      <div style={{ display: "flex", alignItems: "center", gap: 70, marginTop: 10 }}>
        <div dir="ltr" style={{ fontFamily: CAIRO, fontWeight: 900, fontSize: 210, color: C.white, lineHeight: 1, letterSpacing: -2 }}>
          {b.prefix ?? ""}{v.toLocaleString("fr-FR")}{latin && <span style={{ fontSize: 110, marginLeft: 16 }}>{b.suffix}</span>}
        </div>
        {b.icon && <Pict name={b.icon} size={210} at={8} />}
      </div>
      <div style={{ width: io(f, 20, 40, 0, 900), height: 5, background: C.red, marginTop: 8 }} />
      {b.suffix && !latin && <T s={b.suffix} size={56} weight={800} />}
      {b.sub && <T s={b.sub} size={46} weight={700} color={C.light} style={{ opacity: io(f, 30, 40) }} />}
    </div>
  );
};

const Vs: React.FC<{ b: Beat }> = ({ b }) => {
  const f = useCurrentFrame();
  const side = (it: Item | undefined, i: number, good: boolean) => {
    const st = 8 + i * 14;
    return <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 24, width: 620, opacity: io(f, st, st + 10) }}>
      <div style={{ position: "relative" }}>
        <Pict name={it?.icon} size={240} at={st} dim={!good} />
        <div style={{ position: "absolute", top: -10, right: -40 }}><Check ok={good} at={st + 16} /></div>
      </div>
      {good ? <RedLabel s={it?.label ?? ""} size={52} at={st + 6} /> : <T s={it?.label ?? ""} size={50} weight={800} color={C.mid} />}
      {it?.sub && <T s={it.sub} size={34} weight={700} color={good ? C.white : C.mid} />}
    </div>;
  };
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 60 }}>
      {b.title && <Words s={b.title} size={64} at={0} />}
      <div dir="rtl" style={{ display: "flex", alignItems: "flex-start", gap: 60 }}>
        {side(b.left, 0, false)}
        <div style={{ width: 3, height: 380, background: C.gray, opacity: io(f, 10, 20) }} />
        {side(b.right, 1, true)}
      </div>
    </div>
  );
};

const Quote: React.FC<{ b: Beat }> = ({ b }) => (
  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 34, maxWidth: 1500 }}>
    <Pict name={b.icon} size={150} at={0} dim />
    <Words s={`«${b.title ?? ""}»`} size={b.title && b.title.length > 40 ? 72 : 88} at={4} />
  </div>
);

const ImageScene: React.FC<{ b: Beat; dur: number }> = ({ b, dur }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      {b.img && <Img src={staticFile(b.img)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: mediaMotion(f, dur), filter: "saturate(.8) brightness(.72) contrast(1.05)" }} />}
      <AbsoluteFill style={{ boxShadow: "inset 0 0 240px 40px rgba(0,0,0,.6)" }} />
      {!b.fx?.length && <MediaPop icon={mediaIcon(b.img)} />}
      {b.title && <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 150 }}><WhiteLabel s={b.title} size={60} at={6} /></AbsoluteFill>}
    </AbsoluteFill>
  );
};

const VideoScene: React.FC<{ b: Beat & { video?: string }; dur: number }> = ({ b, dur }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      {b.video && <OffthreadVideo src={staticFile(b.video)} muted style={{ width: "100%", height: "100%", objectFit: "cover", transform: mediaMotion(f, dur), filter: "saturate(.85) brightness(.7) contrast(1.05)" }} />}
      <AbsoluteFill style={{ boxShadow: "inset 0 0 240px 40px rgba(0,0,0,.6)" }} />
      {!(b as Beat).fx?.length && <MediaPop icon={mediaIcon(b.video)} />}
      {b.title && <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 150 }}><WhiteLabel s={b.title} size={b.title.length > 34 ? 52 : 62} at={6} /></AbsoluteFill>}
    </AbsoluteFill>
  );
};

const Cutout: React.FC<{ b: Beat }> = ({ b }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const sp = spring({ frame: f - 2, fps, config: { damping: 18, stiffness: 110 } });
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 90 }} dir="rtl">
      <div style={{ display: "flex", flexDirection: "column", gap: 24, alignItems: "center", maxWidth: 760 }}>
        {b.title && <RedLabel s={b.title} size={74} at={8} />}
        {b.sub && <Words s={b.sub} size={44} at={16} color={C.light} />}
      </div>
      {b.img && <Img src={staticFile(b.img)} style={{ maxWidth: 680, maxHeight: 640, objectFit: "contain", opacity: sp,
        transform: `translateY(${(1 - sp) * 40}px)`, filter: "grayscale(.35) drop-shadow(0 40px 50px rgba(0,0,0,.6))" }} />}
    </div>
  );
};


type DBeat = Beat & { rows?: { a: Item; mid: string; b: Item; note?: string }[]; left?: Item; right?: Item; result?: string;
  a?: { label: string; sub?: string }; label?: string; n?: number };

/** Two flows: what feeds what (time → money vs asset → money), dots travelling along the arrows. */
const Flow: React.FC<{ b: DBeat }> = ({ b }) => {
  const f = useCurrentFrame(); const rows = b.rows ?? [];
  const half = Math.max(60, ((b.to - b.from) * FPS) / 2 - 10);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 44 }}>
      {b.title && <Words s={b.title} size={60} at={0} />}
      {rows.map((r, i) => {
        const st = 6 + i * half, on = io(f, st, st + 10), w = 520;
        return <div key={i} dir="rtl" style={{ display: "flex", alignItems: "center", gap: 30, opacity: Math.max(0.35, on), filter: f < st ? "grayscale(1)" : "none" }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8, width: 220 }}>
            <Pict name={r.a.icon} size={130} at={st} /><T s={r.a.label} size={36} weight={800} /></div>
          <div style={{ position: "relative", width: w, height: 110, display: "grid", placeItems: "center" }}>
            <svg width={w} height={40} style={{ position: "absolute", top: 60 }}>
              <line x1={w - 10} y1={20} x2={10 + (1 - io(f, st + 6, st + 22)) * (w - 20)} y2={20} stroke={C.white} strokeWidth={4} strokeDasharray="14 10" />
              <polygon points="0,20 22,8 22,32" fill={C.white} opacity={io(f, st + 18, st + 24)} />
              {[0, 1, 2].map(k => { const t = ((f - st + k * 20) % 60) / 60; return f > st + 22 ?
                <circle key={k} cx={w - 20 - t * (w - 40)} cy={20} r={9} fill={C.red} /> : null; })}
            </svg>
            <div style={{ position: "absolute", top: 0 }}><RedLabel s={r.mid} size={38} at={st + 10} /></div>
          </div>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8, width: 220 }}>
            <Pict name={r.b.icon} size={130} at={st + 20} /><T s={r.note ?? r.b.label} size={34} weight={800} color={C.light} /></div>
        </div>;
      })}
    </div>
  );
};

/** Passive Income bar grows until it reaches the expenses bar → "حر ماليا". */
const Equation: React.FC<{ b: DBeat }> = ({ b }) => {
  const f = useCurrentFrame(); const dur = (b.to - b.from) * FPS;
  const exp = 0.72, grow = io(f, 14, Math.min(dur - 30, 150), 0.12, 0.86);
  const done = grow >= exp;
  const bar = (v: number, label: string, icon: string | undefined, hi: boolean) =>
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
      <div style={{ width: 210, height: 440, display: "flex", alignItems: "flex-end", borderBottom: `4px solid ${C.mid}` }}>
        <div style={{ width: "100%", height: `${v * 100}%`, background: hi ? C.red : C.gray, borderRadius: "14px 14px 0 0",
          boxShadow: hi && done ? `0 0 40px ${C.red}` : "none" }} /></div>
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}><Pict name={icon} size={56} at={4} /><T s={label} size={40} weight={800} /></div>
    </div>;
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 30 }}>
      {b.title && <Words s={b.title} size={60} at={0} />}
      <div dir="rtl" style={{ display: "flex", alignItems: "flex-end", gap: 110 }}>
        {bar(grow, b.left?.label ?? "", b.left?.icon, true)}
        <div style={{ fontFamily: CAIRO, fontWeight: 900, fontSize: 120, color: done ? C.white : C.gray, marginBottom: 200 }}>{done ? "≥" : "<"}</div>
        {bar(exp, b.right?.label ?? "", b.right?.icon, false)}
      </div>
      <div style={{ height: 80, opacity: done ? 1 : 0 }}>{done && <RedLabel s={b.result ?? ""} size={56} at={0} />}</div>
    </div>
  );
};

/** Income stays flat while expenses climb, year after year. */
const Bars: React.FC<{ b: DBeat }> = ({ b }) => {
  const f = useCurrentFrame(); const W = 1200, H = 460;
  const t = io(f, 10, 120);
  const pts = (fn: (x: number) => number) => Array.from({ length: 41 }, (_, i) => i / 40).filter(x => x <= t)
    .map(x => `${60 + x * (W - 120)},${H - 40 - fn(x) * (H - 100)}`).join(" ");
  const inc = () => 0.45, exp = (x: number) => 0.18 + x * 0.75;
  const end = (fn: (x: number) => number) => [60 + t * (W - 120), H - 40 - fn(t) * (H - 100)];
  const [ex, ey] = end(exp), [ix, iy] = end(inc);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 20 }}>
      {b.title && <Words s={b.title} size={60} at={0} />}
      <svg width={W} height={H}>
        <line x1={60} y1={H - 40} x2={W - 60} y2={H - 40} stroke={C.mid} strokeWidth={3} />
        {[0, 1, 2, 3, 4].map(k => <text key={k} x={60 + k * (W - 120) / 4} y={H - 8} fill={C.mid} fontFamily={CAIRO} fontSize={24} textAnchor="middle">{k === 0 ? "0" : `+${k}`}</text>)}
        <polyline points={pts(inc)} fill="none" stroke={C.light} strokeWidth={8} strokeLinecap="round" />
        <polyline points={pts(exp)} fill="none" stroke={C.red} strokeWidth={8} strokeLinecap="round" />
        <circle cx={ix} cy={iy} r={12} fill={C.light} /><circle cx={ex} cy={ey} r={12} fill={C.red} />
      </svg>
      <div dir="rtl" style={{ display: "flex", gap: 80, opacity: io(f, 40, 55) }}>
        <div style={{ display: "flex", gap: 14, alignItems: "center" }}><div style={{ width: 34, height: 8, background: C.light }} /><T s={`${b.a?.label} · ${b.a?.sub}`} size={40} weight={800} /></div>
        <div style={{ display: "flex", gap: 14, alignItems: "center" }}><div style={{ width: 34, height: 8, background: C.red }} /><T s={`${(b as DBeat & { b?: { label: string; sub?: string } }).b?.label ?? ""} · ${(b as unknown as { b?: { sub?: string } }).b?.sub ?? ""}`} size={40} weight={800} /></div>
      </div>
    </div>
  );
};

/** Compound effect: each new asset arrives faster than the one before. */
const Chain: React.FC<{ b: DBeat }> = ({ b }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const n = b.n ?? 5;
  const starts: number[] = []; let t = 8, gap = 70; for (let i = 0; i < n; i++) { starts.push(t); t += gap; gap = Math.max(14, gap * 0.6); }
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 60 }}>
      {b.title && <Words s={b.title} size={64} at={0} />}
      <div dir="ltr" style={{ display: "flex", alignItems: "center", gap: 18 }}>
        {starts.map((st, i) => { const sp = spring({ frame: f - st, fps, config: { damping: 12, stiffness: 160 } });
          return <React.Fragment key={i}>
            {i > 0 && <div style={{ width: 70, height: 6, background: C.red, transformOrigin: "left", transform: `scaleX(${io(f, st - 8, st)})` }} />}
            <div style={{ width: 200, height: 200, borderRadius: 26, border: `4px solid ${i === 0 ? C.red : C.light}`, background: i === 0 ? `${C.red}33` : "rgba(255,255,255,.04)",
              display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 8, transform: `scale(${sp})` }}>
              <Pict name="house" size={80} at={st} /><T s={`${b.label ?? "Asset"} ${i + 1}`} size={34} weight={800} />
            </div></React.Fragment>; })}
      </div>
      <div style={{ opacity: io(f, starts[1] ?? 60, (starts[1] ?? 60) + 10) }}><T s="الأول صعيب… الباقي ساهلين" size={46} weight={800} color={C.light} /></div>
    </div>
  );
};

/** Card whose idea plays as a big animation: title on top, the animation under it. */
const FullFx: React.FC<{ b: Beat }> = ({ b }) => {
  const dur = Math.round((b.to - b.from) * FPS);
  return <AbsoluteFill>
    {b.title && !b.fx?.some(x => x.pos === "full" && x.title) && <AbsoluteFill style={{ alignItems: "center", paddingTop: 110 }}><Words s={b.title} size={62} at={0} /></AbsoluteFill>}
    <AbsoluteFill style={{ top: 70 }}>{b.fx?.filter(x => x.pos === "full").map((x, j) => <IdeaFx key={j} fx={x} dur={dur} />)}</AbsoluteFill>
  </AbsoluteFill>;
};

const Brand: React.FC = () => (
  <AbsoluteFill
    style={{ alignItems: "center", paddingTop: 34, pointerEvents: "none" }}
    hidden={!BRAND.name}
  >
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
      <div style={{ fontFamily: CAIRO, fontWeight: 900, fontSize: 30, letterSpacing: 9, color: C.white, opacity: 0.92, textShadow: "0 2px 14px rgba(0,0,0,.6)" }}>{BRAND.name}</div>
      <div style={{ width: 120, height: 3, background: C.red, borderRadius: 2 }} />
    </div>
  </AbsoluteFill>
);

export const ExplainerDoc: React.FC<{ beats: Beat[]; audio: string; duration: number }> = ({ beats, audio }) => (
  <AbsoluteFill style={{ background: C.bg }}>
    <Backdrop />
    <Audio src={staticFile(audio)} />
    {beats.map((b, i) => {
      const from = Math.round(b.from * FPS), dur = Math.max(20, Math.round((b.to - b.from) * FPS) + 4);
      const body = b.type === "title" ? <Title b={b} /> : b.type === "icons" ? <Icons b={b} /> : b.type === "steps" ? <Steps b={b} />
        : b.type === "stat" ? <Stat b={b} /> : b.type === "vs" ? <Vs b={b} /> : b.type === "quote" ? <Quote b={b} />
        : b.type === "cutout" ? <Cutout b={b} /> : (b.type as string) === "flow" ? <Flow b={b as DBeat} />
        : (b.type as string) === "equation" ? <Equation b={b as DBeat} /> : (b.type as string) === "bars" ? <Bars b={b as DBeat} />
        : (b.type as string) === "chain" ? <Chain b={b as DBeat} /> : null;
      const media = b.type === "image" || (b.type as string) === "video";
      const full = !media && b.fx?.some(x => x.pos === "full");
      const card = full ? <FullFx b={b} /> : body;
      return <Sequence key={i} from={from} durationInFrames={dur} layout="none">
        <Scene dur={dur} media={media}>{b.type === "image" ? <ImageScene b={b} dur={dur} /> : (b.type as string) === "video" ? <VideoScene b={b} dur={dur} /> : card}</Scene>
        {b.fx?.filter(x => x.pos !== "full").map((x, j) => <IdeaFx key={j} fx={x} dur={dur} />)}
      </Sequence>;
    })}
    <Brand />
  </AbsoluteFill>
);
