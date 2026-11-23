# Kit API (`src/motion-pro/`, `import { … } from "../motion-pro"`)

The kit lives in your Remotion project at `src/motion-pro/` (copied from this skill's
`kit/motion-pro/`, see `references/11-setup.md`). Coordinates are px from the frame centre unless noted. Every component reads `useCurrentFrame()`, so
it works inside `Sequence` / `Freeze` / `MotionBlur` (fractional frames are fine).

**Fonts:** `FONT.ui` (Inter, weights 300–700) and `FONT.mono` come from `theme.ts`, loaded with `@remotion/google-fonts`.
Add families there. Call `useFontsReady()` once at the top of every composition.

## Curves & helpers (`curves.ts`, `keyed.ts`, `timeline.ts`, `flow.ts`)

| Export | Signature / defaults | Notes |
|---|---|---|
| `EASE_PRO` | `{move, moveSoft, enter, enterSnap, exit, exitHard, drift, linear}` | see `08` §A |
| `aeEase(out, in)` | AE influences in % | `aeEase(70,0)`, `aeEase(0,75)`, `aeEase(50,85)` |
| `SPRING_PRO` | `{morph, pop, settle}` | for `spring()` / `springEase()` |
| `clamp01, lerp` | — | — |
| `prog(f, start, dur, ease=enter)` | 0..1 progress | `tw(f,start,dur,from,to,ease)`, `twc(...)` colours |
| `path(f, stops[[f,v]], ease=move)`, `ip(f, in, out, ease?)` | piecewise / clamped interpolate | — |
| `rand(a,b,c)`, `noise1(t, seed)` | deterministic random / smooth noise | never `Math.random()` |
| `K` keys + `sample(keys, f, defaultEase)` | `{f, ease?, ...props}` | a key's `ease` shapes the segment ARRIVING at it; each prop animates only between keys that mention it |
| `shift(keys, n)`, `num`, `str` | — | — |
| `chain(beats, start, overlapRatio=.25)`, `chainEnd` | overlap-chained beat slots | — |
| `stagger(n, each, start)`, `staggerCenter` | start frames | — |
| `handoff(exitStart, exitDur, lead=2)` | where the next element starts | — |
| `beatFrame(n, bpm=120, fps=30)`, `onBeat(beat, dur)`, `readFrames(text)` | music / readability | — |
| `useFontsReady()` | call once at the top of any composition that measures text | holds the frame until web fonts load |
| `measure(text, font)` | px width (canvas, cached once fonts are loaded) | `FontSpec = {family, size, weight?, letterSpacing? (em)}` |
| `caretX(f, start, text, cpf, font)` | continuous caret x | follow-cams |
| `springFollow(f, target(f), from, ω=.22, ζ=1)` | follower of a stepped target, sub-frame interpolated | see `08` §A table |
| `smoothSteps(f, [[at, v]], dur=10, ease=move)` | blended steps | — |

## Camera (`CameraRig.tsx`)

`<CameraRig keys moves drift extra shake blur=.45 blurDeadZone=8 dof=0 perspective=2400 raster=2>`
- `keys`: `{f, cx, cy, zoom, rot, rx, ry, ease?}` absolute look-at (default ease MOVE).
- `moves`: `CamMove[] = {at, dur, x?, y?, zoom? (multiplier), rot?, rx?, ry?, ease?}`: ADDITIVE, may overlap.
- `drift`: `{zoomPerSec?, xPerSec?, yPerSec?, rotPerSec?}` (default `{zoomPerSec: .015}`).
- `extra(f) => {cx?, cy?, zoom?, rot?}`: procedural offsets (follow-cam, punch). Pure function of f.
- `shake`: `[{at, dur=8, amp=4, freq=10}]`, impacts only.
- 3D-composited layer (perspective + rotateX .01°) + content laid out at `raster`× (CSS zoom): sub-pixel smooth, crisp.
- Inside `<MotionBlur>` its gaussian velocity blur switches off automatically.
- Helpers: `camState(f, opts)` (look-at state, use it to aim pushes exactly), `movesAt`, `camSpeed`, `punch(f, at, .05, 3, 18)`,
  `follow(f, target, lag)` (prefer `springFollow`), `portalKeys(at, dur, target, frameW, overfill=1.25)`,
  `whipKeys(at, from, to, dur=22)`, `<DepthBlur amount inner=38 outer=75 mode="radial"|"tilt">`, `useRaster()`.

## Motion blur & stages (`MotionBlur.tsx`)

- `<MotionBlur samples=10 shutter=180 boost? active?>`: sub-frame accumulation (centred shutter). `boost`:
  `{samples, windows: [[a,b]...]}` or an array of tiers (highest containing tier wins). `active(f)` can skip frames.
  Keep backgrounds OUTSIDE it. Drafts: `samples={1}`.
- `<Stage keys origin={{x,y}} style>`: a full-frame layer animated by keys `x, y, scale, rot, blur, opacity` around an origin.
- Recipes (keys): `collapseOut(at, dur=12, to=.7)`, `emergeIn(at, dur=20, from=.6)`, `zoomOutThrough(at, dur=14, to=2.2)`,
  `zoomInThrough(at, dur=18, from=.88)`. Combine: `[...emergeIn(a), ...collapseOut(b)]`.

## Elements in motion (`Move.tsx`)

`<Move keys anchor="center"|"flow" blurK=.45 smear=0 float origin="50% 50%" perspective=1400 style frame>`
- keys: `x, y, scale, sx, sy, rot, rx, ry, opacity, blur, w, h, radius, bg, color` (default ease ENTER).
- velocity blur with a 6 px/f dead zone (off inside `<MotionBlur>`); `smear` stretches fast moves; `float: {amp, period, phase, rot}`.
- Recipes: `enter(at, {dir, dist, dur=20, blur=16, scale=.92, rot, ease, x, y})`, `snapIn(at, {dir, dist, dur, blur, x, y, scale})`,
  `pop(at, {from, dur, x, y, blur})`, `exit(at, {dir, dist, dur, scale, x, y, hard})`, `holdDrift(from, to, {scale, x, y})`,
  `springEase(config, dur)`.

## Field (`Field.tsx`)

`FieldCfg = {at, start, text, cpf, font, from?: {w,h}, minW, h, padL, padR, maxW?, omega=.3, zeta=.78}`;
`fieldGeom(f, cfg) → {w, h, r, grow, caret}`; `<TypeField {...cfg} bg bgFrom shadow ink caretColor caretUntil placeholder left right>`.
The bar grows from its seed with a spring, typing starts inside the growth, the width follows the typed text aimed
2ζ/ω frames ahead.

## Text: pro primitives (`TextPro.tsx`)

| Component | Props (defaults) |
|---|---|
| `WordIn` | `text, start, font, ink="#111", accent, keep=[], every=3, dur=20, dist=20, blur=8, skew=10, gapEm, wordStyle, exitAt, exitDur=10, style` |
| `LiquidIn` | `text, start, font, ink="#111", accent="#2F6BFF", dur=16, strength=70, style` |
| `Decode` | `text, start, dur=8, ink="#111", blur=5, seed=2, style` (wrap in a span carrying the font) |
| `WaveNumber` | `values=[{v, at}], dur=14, stagger=1.5, amp=.16 (em), ink, accent="#0A84FF", style` |
| `StackLines` | `lines=[{at, node}], lineH, dur=16, align="center", width=1000` |
| `WheelPicker` | `items, at[], itemH, dur=16, step=30, width=600, align="left", window=2.3` (gold: step 32, window 1.5) |

## Text: menu (`TextFx.tsx`), all take `font: FontSpec` and lay words out from measured widths

`layoutLine(text, font, gapEm=.26)`, `wordBox(text, i, font)`.
`BlurIn` (every 5, dur 12, from, blur 14, dx, scaleFrom, unit "word"|"letter", exitAt) · `RiseTilt` (every 6, dur 16,
dist .9em, tilt −12°, blur 18) · `Converge` (every 3, dur 18, spreadX/Y, glyphs, glyphColor) · `Emerge` (every 3, dur 16,
originX) · `WipeReveal` (dur 24, feather 60, slide 24) + `wipeEdge()` · `WordWave` (every 3, amp .7em) · `DropIn`
(every 5, dist, scaleFrom 1.35) · `SwapLine` (from, to, at, every 2, dur 12, overlap 5) · `Smear` (dur 10, dist 260,
mode in|out, dir) · `TrackIn` (dur 18, fromEm .22) · `BlobToWord` (dur 18, from) · `SelectReplace` (selDur 7, hold 4,
cpf .9, color) · `GuideMarks` (w, h, dur 8, hold 30, ext 40) · `CutSequence` (cuts, flicker, family, push).
Common props: `ink, accent, keep, every, dur, gapEm, wordStyle, style`.

## Text: classic (`Type.tsx`)

`TypeLine` (cpf .6, caret bar|block|none, caretColor, caretUntil, placeholder) · `typedCount`, `textWidth` ·
`WordRise` · `RandomReveal` · `Scramble` · `Odometer` (values, dur 8, stagger 1.5) · `SlotRoll` (items, at, itemH, dur 10,
neighbors) · `WordSwap` · `HighlightWord` · `UnderlineDraw`.

## Pixels (`Pixels.tsx`)

`PixelGather` (at, box, count 14, cell 18, colors, dur 16, spread 170, reverse) · `PixelSparkle` (at, box, avoid, cell 40,
colors, life 12, peak 8, spread 1.6, drift 26) · `PixelReveal` (w, h, cell 18, dur 12, flash 2, flashRatio .35, dir) ·
`Pixelate` (w, h, steps, hold 2, noise 14) · `PixelOrbit` (count 9, rx 230, ry 170, sizes, period 260, burst 14) ·
`PixelDust` (box, count 26, dur 14, dx, dy).

## Elements (`Elements.tsx`)

`MacCursor` (keys `{f, x, y, kind arrow|hand|grab, click, bend}`, size 54, appearAt, hideAt) · `pressScale(f, at, depth=.08)` ·
`ClickRing` (at, w, h, radius, color, dur 12, x, y, width 3) · `RingDraw` (at, w, h, radius, color, dur 10, stroke 3,
fadeAt, gap 6) · `MorphBox` (states, dur 10, render, overshoot) · `DriftBlob` (x, y, size, color, opacity .5, period 240,
ax 70, ay 50, phase) · `Glow` · `MeshBg` · `DotGrid` · `Particles` (count, shape dot|square|glyph, colors, size, vx, vy,
blur, opacity, wobble, start, fadeIn) · `Orbit` · `Phone` · `AmbientFrame` (9:16 band) · `EndCard` · `InlineSlot` · `useFxId`.

## Transitions (`Transitions.tsx`), mostly for briefs that ask for a punchy edit

`PixelDissolve` (+`pixelTiming`) · `RibbonSwoosh` (+`swooshTiming`) · `GlitchFlash` · `Flash` · `Strobe` · `SoftWipe` ·
`VignetteOut` · `BlurSwap` · `ShrinkToCard` · `LiquidRipple` · `ImpactFrame` · `Comet`. Flash-type transitions spike the
energy gate: 1–2 f max, only on request.

## Gotchas

- Measured layouts need `useFontsReady()` once per composition.
- Anything stateful must interpolate sub-frames (MotionBlur); never `Math.floor(frame)` in motion.
- Fonts available: Inter (400–800), Anton, plus any `@remotion/google-fonts` family. SF Pro is not available.
- TypeScript is strict (`noUnusedLocals`): remove unused imports before rendering.
