import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame } from "remotion";
import {
  FONT,
  BlobToWord, BlurIn, CameraRig, Converge, DropIn, EASE_PRO, Emerge, FontSpec, GuideMarks, PixelDust, PixelOrbit, PixelReveal, PixelSparkle, Pixelate,
  RiseTilt, SelectReplace, Smear, SwapLine, TrackIn, TypeField, WipeReveal, WordWave, clamp01, layoutLine, useFontsReady, wipeEdge, wordBox,
} from "../motion-pro";

// Visual test bench: every text / pixel technique plays alone for SEG frames, inside a drifting camera.
export const SEG = 36;
const F: FontSpec = { family: FONT.ui, size: 72, weight: 600, letterSpacing: -0.03 };
const INK = "#111";
const BLUE = "#0A84FF";

const Center: React.FC<{ children: React.ReactNode; y?: number }> = ({ children, y = 0 }) => (
  <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", transform: `translateY(${y}px)` }}>{children}</div>
);
const Label: React.FC<{ t: string }> = ({ t }) => (
  <div style={{ position: "absolute", left: 40, top: 36, fontFamily: FONT.ui, fontSize: 30, fontWeight: 600, color: "#8E8E93" }}>{t}</div>
);

const S = 4; // local start

const tests: Array<[string, React.FC]> = [
  ["BlurIn + PixelSparkle", () => {
    const b = wordBox("meet the new", 2, F);
    return (<><Center><BlurIn text="meet the new" start={S} font={F} from="#C7C7CC" every={5} /></Center>
      <PixelSparkle at={S + 12} box={{ x: b.x, y: 0, w: b.w, h: b.h }} avoid={{ x: 0, y: 0, w: b.lineW, h: F.size }} cell={34} colors={[BLUE, "#5AC8FA", "#0040DD", "#9BD1FF"]} /></>);
  }],
  ["RiseTilt", () => <Center><RiseTilt text="Ready to level up" start={S} font={F} accent={BLUE} /></Center>],
  ["Converge + glyphs", () => <Center><Converge text="Go from an idea" start={S} font={F} accent={BLUE} glyphs={10} /></Center>],
  ["Emerge (behind hero)", () => {
    const L = layoutLine("Ready to create", F);
    return (<><Center y={40}><Emerge text="Ready to create" start={S} font={F} accent={BLUE} originX={L.W / 2} /></Center>
      <Center y={-20}><div style={{ width: 170, height: 170, borderRadius: 170, background: "#111" }} /></Center></>);
  }],
  ["WipeReveal + wiper", () => {
    const f = useCurrentFrame();
    const L = layoutLine("Your AI, right in your texts", F);
    const e = wipeEdge(f, S, 24, L.W);
    return (<Center><div style={{ position: "relative" }}><WipeReveal text="Your AI, right in your texts" start={S} dur={24} font={F} accent={BLUE} />
      <div style={{ position: "absolute", left: e - 40, top: 10, width: 80, height: 80, borderRadius: 80, background: BLUE, opacity: f < S + 26 ? 1 : 0 }} /></div></Center>);
  }],
  ["WordWave", () => <Center><WordWave text="Wish (feat. Trippie Redd)" start={S} font={F} /></Center>],
  ["DropIn", () => <Center><DropIn text="it'll work, trust" start={S} font={F} accent="#9B1B5A" keep={[2]} /></Center>],
  ["SwapLine", () => <Center><SwapLine from="find everyone" to="with find my" at={S + 6} font={F} accent={BLUE} /></Center>],
  ["Smear in", () => <Center><Smear text="together" at={S} font={F} dist={420} /></Center>],
  ["TrackIn", () => <Center><TrackIn text="Choose Your Gender" at={S} font={F} /></Center>],
  ["BlobToWord", () => <Center><BlobToWord text="Have you ever" at={S} font={{ ...F, family: "Georgia, serif", weight: 400 }} accent="#4B5BFF" ink="#3A44D8" /></Center>],
  ["SelectReplace", () => <Center><SelectReplace from="Stop Scrolling." to="Start Showing up." at={S} font={F} cpf={1.2} /></Center>],
  ["GuideMarks", () => {
    const b = wordBox("making sense", 1, F);
    return (<><Center><BlurIn text="making sense" start={S} font={F} accent="#20B486" keep={[1]} /></Center>
      <div style={{ position: "absolute", inset: 0, transform: `translateX(${b.x}px)` }}><GuideMarks at={S + 10} w={b.w + 20} h={F.size * 1.0} color="#20B486" /></div></>);
  }],
  ["PixelReveal", () => (
    <Center><PixelReveal at={S} w={560} h={100} cell={20} dur={14}>
      <div style={{ fontFamily: FONT.ui, fontSize: 72, fontWeight: 700, color: INK, letterSpacing: "-0.03em", lineHeight: "100px" }}>autopilot.</div>
    </PixelReveal></Center>)],
  ["Pixelate", () => (
    <Center><Pixelate at={S} w={420} h={260}>
      <div style={{ width: 420, height: 260, borderRadius: 24, background: "linear-gradient(135deg,#FF9F0A,#FF375F 45%,#5E5CE6)" }}>
        <div style={{ position: "absolute", left: 30, top: 30, width: 120, height: 120, borderRadius: 120, background: "#fff" }} />
      </div>
    </Pixelate></Center>)],
  ["PixelOrbit", () => (<><Center><div style={{ width: 170, height: 170, borderRadius: 170, background: "#111" }} /></Center><PixelOrbit at={S} /></>)],
  ["PixelDust", () => {
    const f = useCurrentFrame();
    const o = 1 - EASE_PRO.exit(clamp01((f - S - 6) / 8));
    return (<><Center><span style={{ fontFamily: FONT.ui, fontSize: 72, fontWeight: 300, color: "#8E8E93", opacity: o, filter: `blur(${(1 - o) * 8}px)` }}>softer</span></Center>
      <PixelDust at={S + 6} box={{ x: 0, y: 0, w: 220, h: 60 }} count={30} /></>);
  }],
  ["TypeField", () => (
    <TypeField at={S} start={S + 7} text="plan my week around the gym" cpf={1.1} font={{ family: FONT.ui, size: 34, weight: 500 }} minW={420} h={96} padL={86} padR={92}
      shadow="0 30px 60px -30px rgba(0,0,0,.3)" bgFrom={BLUE} left={<div style={{ width: 40, height: 40, borderRadius: 40, background: BLUE }} />}
      right={<div style={{ width: 62, height: 62, borderRadius: 62, background: INK }} />} />)],
];

export const TEXT_LAB_DURATION = tests.length * SEG;

export const TextLab: React.FC = () => {
  useFontsReady();
  return (
  <AbsoluteFill style={{ background: "#F5F5F7" }}>
    <CameraRig drift={{ zoomPerSec: 0.01 }}>
      {tests.map(([name, C], i) => (
        <Sequence key={name} from={i * SEG} durationInFrames={SEG} layout="none">
          <AbsoluteFill>
            <Label t={`${i + 1}. ${name}`} />
            <C />
          </AbsoluteFill>
        </Sequence>
      ))}
    </CameraRig>
  </AbsoluteFill>
  );
};
