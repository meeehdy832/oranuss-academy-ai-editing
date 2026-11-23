# Motion bible: every motion, every variant, every knob

Values come from the 24-reel study (`02`–`06`, `videos/`), the pro comparison (`07`) and the gold reel (`00`).
"Gold" = the value the gold reel uses. Frames at 30 fps. Kit names in `code` (API: `09-kit-api.md`).

## A. Curves and physics

| Name | Curve | Use | Typical duration |
|---|---|---|---|
| `EASE_PRO.move` | bezier(.85, 0, .15, 1) | camera moves, transfers, morph positions (the measured signature: 70 % of the travel in ~5 f around the middle, long soft tails) | 24–40 f |
| `EASE_PRO.moveSoft` | (.65, 0, .25, 1) | gentler transfers, follow weights | 18–40 f |
| `EASE_PRO.enter` | (.5, 0, 0, 1) | big arrivals (scenes, cards, pull-back landings) | 18–30 f |
| `EASE_PRO.enterSnap` | (.16, 1, .3, 1) | small UI, words, chips, focus pulls (expo-out) | 8–18 f |
| `EASE_PRO.exit` | (.7, 0, .84, 0) | leaving / handing off: accelerates and ENDS AT PEAK SPEED | 8–16 f |
| `EASE_PRO.exitHard` | (.95, .05, .8, .04) | violent expo-in finish (use sparingly: spikes energy) | 8–14 f |
| `EASE_PRO.drift` | (.33, 0, .67, 1) | holds, long camera drifts, dusk | 40–120 f |
| `aeEase(out, in)` | bezier(out/100, 0, 1 − in/100, 1) | AE-style influence: `aeEase(70, 0)` = accelerate into a cut at half EXIT's end speed (gold match cut / zoom-through); `aeEase(0, 75)` = leave fast, long landing (gold incoming camera); `aeEase(50, 85)` = gold pull-back; `aeEase(33, 33)` = AE Easy Ease | — |
| `SPRING_PRO.morph` | damping 17, stiffness 140, mass 1 | container size morphs, ~3 % overshoot | auto |
| `SPRING_PRO.pop` | 12 / 180 / .8 | icons, avatars, buttons, ~8 % overshoot | auto |
| `SPRING_PRO.settle` | 26 / 120 / 1 | no visible overshoot | auto |
| `springFollow(f, target, from, ω, ζ)` | critically-damped follower, sub-frame interpolated | anything chasing a stepped value: follow-cams (ω .12–.20, ζ 1), growing fields (ω .30, ζ .78), card morphs (ω .24–.26, ζ .74), tight UI (ω .45) | lag ≈ 2ζ/ω f |

AE ↔ CSS: an editor's "ease-out on exits / ease-in on entrances" = exits accelerate away (CSS ease-in = `EASE_PRO.exit`)
and entrances decelerate in (CSS ease-out = `enter` / `enterSnap`). Never linear on elements; never a short
symmetric ease on a big move; never an ease-in that simply stops on screen.

## B. Timing, overlap, offsets

| Thing | Frames |
|---|---|
| word-by-word | a word every 2–6 f, each 12–20 f long |
| letters (typing) | 0.9–2 chars/f fast UI (gold 0.9), 2–3 f per char "human" |
| stagger: letters 1 f · list items / avatars 2–4 f · cards / scene pieces 4–8 f · grid blocks 2–2.5 f diagonal (gold) |
| cursor travel | 14–20 f on a curved path (MOVE) |
| click | press 3 f (1 → .9–.95), release 5–9 f (spring to 1.04 → 1); target reacts on release |
| morph | 12–20 f spring; old content out in 3–4 f; new content from ~5 % of the size change |
| hold on a readable state | 20–45 f (with a push), logo 1.5–2.5 s |
| a beat (one idea) | 1–2 s; a big camera move every ~1.5 s; a small event every 4–12 f |

**Overlap (the editor's stacking):** start the next move when the previous is 55–80 % done (gold: 50 vs 64, 92 vs 94,
116 vs 124, 150 vs 156, 200 vs 206). **Hand-off:** an exit accelerates; the next element starts fast in the same
direction and decelerates; a cut placed on that peak frame is invisible.
**Offset properties:** opacity done by 30–35 %, blur cleared by 65–70 %, position over 100 %, scale/rotation settle
2–5 f later, children lag their container 2–4 f, neighbours 1–4 f.

## C. Camera (`CameraRig`: keys + additive `moves` + `drift` + `extra`)

| Move | When | Gold / measured values |
|---|---|---|
| **Drift** (always on) | everywhere, under everything | `drift.zoomPerSec` 0.010–0.015 |
| **Hold push** | every hold | ×1.15–1.30 over 50–100 f, drift ease → 0.2–0.4 %/f (pro reaches 0.8 %/f) |
| **Pull-back reveal** | context after detail (hook, card opening) | keys zoom 1.22 → 1.0 over 64 f drift (hook); move ×0.68 over 40 f `aeEase(50, 85)` (card) |
| **Push-in on the hero** | a UI element is born / gets focus | ×1.3 over 44 f MOVE |
| **Follow-cam** | typing, a route | `extra: cx = weight × springFollow(caret × 0.4–0.6, ω .14–.20)`; weight ramps in 12–18 f, out 30 f; zoom ≤ 1.4 so text stays readable; NEVER stepped per word |
| **Push to a target (match cut)** | into an icon / button that becomes the next scene | 30–36 f `aeEase(70, 0)`; solve x / y / zoom with `camState()` so the target lands centred at the size of the next shape; incoming camera starts at the matched scale, `aeEase(0, 75)` over 26–28 f |
| **Zoom-through** | into a hole / ring / screen to a new world | ×3 over 30–34 f `aeEase(70, 0)`; next scene enters from scale .86, blur 12 over 10–22 f; fade outgoing text first |
| **Whip pan** | to off-screen UI / next item | x ±1100 over 18–26 f MOVE (visible whip 5–6 f, 15–35 % of width per frame at peak) |
| **Roll** | holds on statements | rot ±1.2–2° over 60–100 f drift |
| **3D tilt** | devices, cards entering | rx / ry 25–60° → 0 with ENTER, perspective 1200–2400 |
| **Punch** | a beat hit only | `punch()` +5 % in 3 f, back in 18 f; ≤ 1–2 per video |
| **Shake** | impacts only (launch, slam) | 2–6 px, 8–12 Hz, 4–8 f; zero shakes is fine |
| **Portal** | through a window / screen | `portalKeys(at, dur, target, frameW)` |
| **Depth of field** | pushed-in shots | `dof` 4–10 px, constant per shot (toggling pops) |

Rules: stack `moves` (velocities add, the camera never reaches zero); change direction only on an event (collapse,
click, cut); `raster` 2 (3 beyond ~2.2× zoom) keeps slow drifts jitter-free and text crisp; one rig per world.

## D. Entrances

| Technique | Values | Kit |
|---|---|---|
| Focus pull | blur 8–20 → 0 by 65 %, opacity by 30 %, scale .92–.96 → 1 | `enter()`, `Move` keys |
| Word rise with skew | y 20–26 → 0, blur 8 → 0, skewX −10° × speed, every 3–4 f, 20 f | `WordIn` |
| Snap-in from an edge / from behind | dist 70–80, 14–18 f ENTER-SNAP | `snapIn()` |
| Pop | scale .3 → 1, spring pop | `pop()` |
| Emerge from a point | scale .5–.8 → 1, blur 12 → 0, opacity in 5 f, 16–22 f | `Stage` + `emergeIn()` |
| Grow from a seed | 26 px dot → pill (spring ω .3 ζ .78), colour accent → white with growth | `fieldGeom` / `TypeField` |
| Liquid | wavy displacement 70 → 0, scaleX 1.35 → 1, accent → ink, 16 f | `LiquidIn` |
| Decode | real letters, ≤ 8 f, blur 5 → 0 | `Decode` |
| Pixel build | 14–16 cells converge into the word, word appears ~60 % in | `PixelGather` |
| Line makes room | existing lines slide (MOVE 16 f) as a new line arrives | `StackLines` |
| + 23 more text entrances (blur-in, rise+tilt, converge, emerge from hero, wipe, wave, drop-in, swap, smear, tracking, blob → word, select → replace, guide marks, cuts…) | see `06-text-and-pixels.md` | `TextFx` |

## E. Exits

| Technique | Values | Kit |
|---|---|---|
| Accelerate away | EXIT 8–16 f, ends at peak speed, hand off on that frame | `exit()` |
| Blur-up words | y −1.6 × dist, blur +12, fade, stagger 1.5 f | `WordIn exitAt` / `BlurIn exitAt` |
| Collapse to a point | scale → .55–.7, blur → 10, EXIT 9–12 f, opacity held then 0 in 3 f | `Stage` + `collapseOut()` |
| Fade-before-cut | body text EXIT 12–16 f, ending before the match cut | opacity × (1 − EXIT) |
| Smear | 2–4 f scaleX 1.3–1.8 + directional blur | `Smear mode="out"` |

## F. Morphs (one object, many states)

Gold chain: dot (26 px) → bar (560 × 104, radius h/2) → card (820 × 620, radius 48); icon (56) → stats ring (440).
Geometry by `springFollow` (or `MorphBox` / `SPRING_PRO.morph`); radius moves within the first third of the size change;
colour changes with growth; old content leaves in 4 f with blur 8; new content fades in from 5 % to 30 % of the size
change, then its children stagger. The click's result grows OUT of the clicked object.

## G. Transitions (scene → scene)

| Transition | Recipe | Energy note |
|---|---|---|
| **Collapse → emerge** (gold 52–66, 412–440, 498–527) | outgoing `collapseOut(at, 9–12)`; incoming born at the same point 3–6 f before the outgoing is gone (`emergeIn`) | ~3–5 |
| **Match cut on a shape** (gold 200–238) | push to the shape with `aeEase(70,0)`, fade other text before, cut to the identical shape at the identical size, incoming `aeEase(0,75)`, 2 f opacity overlap | ~7.5 |
| **Zoom-through + world change** (gold 286–340) | rush ×3 `aeEase(70,0)` + dusk through blue midtones over ~58 f, incoming from scale .86 blur 12 with 10 f overlap | peak 13.7 |
| **Morph** | see F | low |
| **Whip pan** | camera x ±1100, 18–26 f MOVE + real blur | ~8 |
| **Pull-back reveal** | detail → context, ENTER / `aeEase(50,85)` | low |
| **Portal / reverse portal** | `portalKeys`, `ShrinkToCard` | medium |
| **Soft wipe / blur swap** | `SoftWipe`, `BlurSwap` (calm sections) | low |
| Avoid | white iris / flood (111), fill-the-screen flat colour (32), hard cut to black (250), flashes/strobes/glitch unless a brief asks for a beat edit (1–2 f max) | spikes |

## H. Numbers

`WaveNumber` (gold): per character, 14 f MOVE, 1.5 f delay per char, sine lift .16 em, blur 0 → 4 → 0, accent at
the crest, glyph swaps at the crest; progress arcs complete with the same MOVE timing. `Odometer`: per-character vertical
roll, 8–12 f, 1.5 f stagger. `SlotRoll` for option lists.

## I. Lists and depth

`WheelPicker`: 3D wheel, step 30–32°, 16 f MOVE per step, neighbours rotated / lighter / blurred, mask window ~1.5 rows.
Focus plane: inactive items scale .85–.92, opacity .35–.6, blur 2–6 px. Fans / arcs / decks for collections.

## J. Cursor and micro-interactions

`MacCursor` keys: appear ~26 f before the click far from the target → curved arc (bend .2–.25) arriving 8 f before →
`kind: "hand"` 6 f before → `click: true` (press 1 → .85 → 1). Target `pressScale(at, .05–.08)`. `ClickRing` 1 → 1.3,
α .6 → 0, 12 f. `RingDraw` outline draw-on 10–12 f around a new field, fade 20 f later. Hide the cursor ~8 f after.

## K. Pixels

Preferred `PixelGather` (cells build the key word, gold hook). `PixelSparkle` (v11 measured: 4–9 cells, 12 f, grid
neighbours, never over text). `Pixelate` (media mosaic → sharp). `PixelOrbit` (burst + orbit around a hero). `PixelDust`
(word dissolve). `PixelDissolve` full screen = rare (1 of 24 refs).

## L. Atmosphere and the world

Backdrop always alive: 2 `DriftBlob`s per world (sizes 800–1400 px, α .2–.75, periods 220–300 f). Glows breathe
(`Glow`, period 80–170 f). Particles on dark worlds (`Particles shape="square"`). World colour changes: through a
saturated midtone, ≥ 40–60 f, hidden inside a rush. Keep the backdrop OUTSIDE `<MotionBlur>`.

## M. Motion blur

`<MotionBlur samples={10} shutter={180}>` around the scenes; `boost` 14 samples on the fastest windows (whips, rushes,
collapses, morph + pull-back). Inside it, `CameraRig` and `Move` switch their fake gaussian off automatically. Every
animation must be continuous between frames (fractional frames!). Drafts: `mb: 1`.

## N. The knobs, with safe ranges

| Knob | Safe range | Gold |
|---|---|---|
| hold push (zoom per frame) | 0.2–0.8 % | 0.27–0.4 % |
| drift zoomPerSec | 0.010–0.015 | 0.012 |
| overlap between moves | 55–80 % | ~75 % |
| transition overlap | 3–8 f | 2–10 f |
| word stagger | 2–6 f | 3–4 f |
| WordIn dist / blur / skew | 16–26 px / 6–10 px / 8–12° | 20–26 / 8 / 10 |
| collapse | 9–12 f, to .55–.7 | 12 f / .7 |
| emerge | 16–22 f, from .5–.8 | 16–22 f / .5–.8 |
| match-cut push | 30–36 f, `aeEase(70,0)` | 36 f |
| zoom-through | ×2.4–3.0, 30–34 f | ×3.0, 34 f |
| dusk | 50–75 f through midtones | 58 f |
| motion blur | 10 samples, boost 14, shutter 180 | same |
| energy gates | max ≤ 15, median ≥ ~0.6, no run ≥ 12 f < 0.2, no flat ≥ 2 f | 13.7 / 0.77 |
