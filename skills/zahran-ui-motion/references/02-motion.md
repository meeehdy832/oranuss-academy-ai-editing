# Motion language (measured from 24 reference reels, 30 fps)

Everything here is from frame-by-frame study plus optical-flow measurement of the references
(velocity curves, sharpness and frozen-frame counts). Numbers are frames at 30 fps.

## 0. Terminology bridge: After Effects vs CSS/Remotion (read this first)

Editors speak After Effects. Remotion speaks CSS. The two name the same curve oppositely:

| What the element does | After Effects words | CSS / Remotion words |
|---|---|---|
| **Enters** and **decelerates** into its rest position | "Easy Ease **In**" on the arrival keyframe (high incoming influence 80–95%) | ease-**out** (`Easing.out(...)`, `cubic-bezier(0.16,1,0.3,1)`) |
| **Exits**: starts slowly then **accelerates** away | "Ease **Out**" on the departure keyframe (high outgoing influence 70–90%) | ease-**in** (`Easing.in(...)`, `cubic-bezier(0.7,0,0.84,0)`) |
| Moves A→B and rests at both ends | ease out on key A + ease in on key B (both 75–90%) | ease-**in-out** (`cubic-bezier(0.85,0,0.15,1)`) |

So the editor rule "high ease-out on exits, ease-in on entrances" means: **exits accelerate away,
entrances decelerate into place.** The measurements confirm it (section 2).

## 1. The signature curve: a very sharp in-out

Median normalized velocity around the peak of 65 isolated moves:

```
frame from peak: -6   -5   -4   -3   -2   -1    0   +1   +2   +3   +4   +5   +6   +8  +10
velocity:       .14  .18  .23  .29  .42  .68  1.0  .64  .36  .27  .19  .15  .13  .09  .07
```

- About **70% of the travel happens in ~5 frames** around the peak. The rest is long, soft tails of 10–15 frames on each side.
- Best fit: **`cubic-bezier(0.85, 0, 0.15, 1)` over 30–37 frames**, close to easeInOutExpo.
- Read it like this: a move *looks* fast (5–6 frames of real travel), but it's *animated* over about 1.1 s, so it starts and lands silky. That's the "fast but smooth" premium feel. A linear or short cubic move over 8 frames looks cheap because it has no tails.

## 2. Curves by role (use these, don't improvise)

| Role | Curve | Duration | Measured evidence |
|---|---|---|---|
| **MOVE**: camera pans/zooms, an element transferring position, morph position | `cubic-bezier(0.85,0,0.15,1)` | 24–40f | symmetric group (n=30): bezier(0.8–0.9, 0, 0.1–0.2, 1), 36–40f |
| **ENTER**: big elements and scenes arriving | `cubic-bezier(0.5,0,0,1)` (short ramp, very long landing) | 18–30f | decelerating group (n=12): peak then a long decay; bezier(0.6,0,0,1) |
| **ENTER_SNAP**: small UI, words, chips, pins | `cubic-bezier(0.16,1,0.3,1)` (expo-out) | 8–16f | words/pills settle within 6–10f |
| **EXIT**: leaving the frame or handing off | `cubic-bezier(0.7,0,0.84,0)`, or `cubic-bezier(0.95,0.05,0.8,0.04)` for a hard exit | 8–16f | accelerating group (n=20): ramps for 6f, then **ends at peak speed** (inExpo fit) |
| **DRIFT**: holds and "alive" motion | linear or `cubic-bezier(0.33,0,0.67,1)` | the whole hold | 1–4% scale or 5–20 px over 1–2 s |
| **MORPH SIZE**: w/h/radius of containers | spring, damping 17, stiffness 140 (2–5% overshoot) **or** MOVE curve | 8–14f | pill→card→pill chains |
| **POP**: icons, avatars, emoji, buttons | spring, damping 12–14 (6–10% overshoot) | 8–12f | avatar pins, emoji chips |

**Exits end at peak speed.** The measured accelerating moves never decelerate. At the moment of
maximum speed, one of three things happens: the element leaves the frame, a cut or transition fires, or the
element **morphs into the next thing**. That's the hand-off (section 4).

## 2b. Amplitude: how far and how fast (measured)

Peak speed = distance × curve slope ÷ duration. Peak slopes: MOVE 6.7, ENTER 4.8, ENTER_SNAP / EXIT 6.25, moveSoft 3.4.

| Move | Peak speed in the refs | Example at 1080 px |
|---|---|---|
| ordinary camera pan / drift-pan | 3–6% of frame width per frame | 30–65 px/f, e.g. a 300 px pan with MOVE over 36–60f |
| **whip pan** | 15–35% of width per frame at its peak | 1100 px with MOVE over 20–24f (≈300 px/f for ~5f) |
| camera zoom | 3.5% (typical) to 15% (punch / portal) scale change per frame | 1.0→1.55 with MOVE over 24–30f; a snap punch is +5–8% in 2f |
| big element entrances | travel 15–40% of the frame, not 30 px | a card rising 300–450 px with ENTER over 20–26f |

**Big whole-frame motion (camera move, zoom, scene-sized morph) happens about every 1.5 s.** Small
element pops alone are not enough: the frame itself must move regularly. Element-only animation on a
static camera reads as amateur.

**Motion-blur dead zone.** Slow follows and drifts (< ~6–10 px/frame) stay tack sharp in the refs;
blur appears only on fast moves. The kit's `CameraRig` (`blurDeadZone`, default 10) and `Move` (dead
zone 6) do this. Without a dead zone, a typing follow-cam smears the text and it can't be read.

**Follow-cam on typing is CONTINUOUS and spring-smoothed** (Yahia's note, 2026-11-07: a word-stepped
follow reads as "the animation stops on some frames"). Drive it with the continuous caret position
(`caretX`, which moves inside each character) through `springFollow(omega 0.14–0.2)`, weight it to
0.4–0.6 of the caret travel, and keep the zoom moderate (1.25–1.4) so the follow speed stays near
or under the blur dead zone and the typed text stays readable. Never step the camera per word.

## 3. Timing table (frames @30fps)

| Thing | Frames |
|---|---|
| typing | 1–2 chars per frame (fast UI typing); 2–3 f per char for "human" typing in a search bar |
| word-by-word reveal | a new word every 4–8 f; each word fades/blurs in over 4–6 f |
| kinetic word slam | in 4–6 f, held 8–12 f |
| stagger: dominoes / letters | 1 f |
| stagger: list items, cards, avatars | 2–4 f |
| stagger: big cards / scene pieces | 4–8 f |
| cursor travel | 14–20 f on a curved path, MOVE curve |
| click | press 3 f (scale 1→0.9), release 5 f (0.9→1.04→1); the target reacts on the release frame |
| hover feedback (focus ring, tooltip) | 6–10 f |
| morph between UI states | 6–14 f; old content fades out in 3 f, new content fades in 4 f starting at the morph midpoint |
| transitions | 4–10 f (glitch 3–7 f, whip 5–8 f, pixel dissolve ~16 f, swoosh ~10 f) |
| hold on a readable state | 20–45 f (with drift), up to 60–90 f for the final logo |
| a full "beat" (one idea) | 1.0–2.0 s in fast videos, 2–3 s in slow ones |

## 4. Continuity: motion never stops (keyframe overlapping)

Measured: in the body of the videos (end cards excluded) **the median longest fully-frozen run is 2.5
frames, and 14 of 24 videos have zero frozen frames.** Something is always moving.

### 4a. The camera NEVER stops: stack additive moves (the editor's way)

Yahia's rule, as an editor does it: the second animation starts BEFORE the first one ends, never after.
With absolute camera keys that is impossible (the camera must arrive, velocity 0, before the next key
leaves). So the kit camera uses **additive `moves`**: each move is a delta (x, y, zoom ×, rot) with its
own curve and they can overlap; their velocities add, so the camera never reaches zero.

```tsx
<CameraRig drift={{ zoomPerSec: 0.01 }} moves={[
  { at: -8, dur: 60, zoom: 1.07, y: 18, ease: EASE_PRO.enter },   // already moving on frame 0
  { at: 38, dur: 34, zoom: 1.3,  y: 27 },                          // starts at 77% of the previous one
  { at: 88, dur: 46, zoom: 0.71, y: -50, ease: aeEase(50, 85) },   // reversal happens ON an event (a click)
  { at: 124, dur: 46, zoom: 1.05, y: -36, ease: EASE_PRO.moveSoft },
  { at: 166, dur: 24, x: 1100, y: 36 },                            // whip
]} />
```

Rules:
- Start every move at **55–80 % of the previous one**; keep a `drift` running under everything.
- Prefer **same-direction stacking** (push-in → stronger push-in): velocities add and the energy rises.
  Change direction only on an event (a click, an impact, a whip, a cut) so the reversal is motivated.
- A beat with no big move still gets a slow move (`moveSoft`, 40–80 f, 4–8 % zoom or 20–60 px).
- Measured on the rebuilt demo: camera speed never drops to zero between frame 0 and the end card.

### 4b. No jitter on slow moves (sub-pixel smoothness)

Chrome snaps 2D-transformed text to whole pixels. A slow drift (< 1 px/f) then visibly vibrates
(measured on the first demo: the text centroid reversed direction on 31 of 38 frames, ±0.5 px). Yahia
saw it as "shake in the scenes that don't move". `CameraRig` v2 fixes it: the world layer is
composited in 3D (`perspective + rotateX(0.01deg)`, which moves sub-pixel exactly) and laid out at
2× resolution with CSS `zoom` (`raster`, default 2; use 3 beyond ~2.2× zoom) so text stays crisp.
Measured: jitter 0.5 → 0.065 px, zero reversals. Never put a slow drift on a plain 2D transform.
Check with `scripts/hold_jitter.py`.

### 4c. Shake only where it means something

Shake is an impact: a launch, a slam, a heavy landing, a beat drop. Never on ordinary UI changes,
never on holds, never as "energy". A video can have zero shakes. `punch()` (snap zoom) is also an
impact tool: at most 1–2 per video.

### 4d. Elements never wait for each other

- A container that grows while content types: ONE animation (`TypeField`/`fieldGeom`): the bar grows
  from its seed with a spring, typing starts at ~60% of the growth, and the width keeps following the
  typed text (`springFollow` aimed ahead by 2ζ/ω frames). Never "grow → stop → type".
- A morph's new content starts appearing at 6–25% of the size change, not after it lands.
- The next scene's first word may start 2–3 f BEFORE the cut (start time < cut), so it arrives mid-fade.

### 4e. The classic tools

1. **Overlap the next move into the previous tail.** Start move B when move A is 60–80% done
   (still in its slow landing tail). Because of the long tails in section 1, two overlapped moves read as one
   continuous gesture. Gaps between motion peaks measured ~20–40 f; the tails cover them.
2. **Hand-off at peak velocity (velocity matching).** The exit accelerates (EXIT curve). On its fastest
   frame, the next element starts at high speed in the **same direction** and decelerates (ENTER curve).
   Fast ↔ fast at the joint means the eye never sees a stop. A hard cut placed on that peak frame is invisible.
   That's "cut on motion".
3. **Follow-through and offset properties.** Never animate all properties of an element on the same frames:
   - opacity reaches 1 within the first 25–35% of the entrance;
   - blur clears by 50–70% (measured: sharpness recovers 80% about 10 f after the velocity peak);
   - position leads; scale settles 2–3 f later; rotation settles 3–5 f later;
   - a container's children lag the container by 2–4 f;
   - neighbors in a group offset 1–4 f (stagger).
4. **Idle motion inside holds.** During a "hold", something must still move: camera drift (1–4% zoom
   over the hold), breathing glows, a waveform, a blinking caret, ticking numbers, orbiting particles, a
   slow parallax of background layers.
5. **The camera keeps moving across cuts.** A new scene starts with the camera already in motion (v24
   starts with the flow peak on frame 2). Don't start scenes from a dead stop.
6. **Morph instead of cut.** Most "scene changes" in the references are a single object changing what it
   is: line→dot→caret→text→chip→word (v01), video tile→widget→pill→button (v15),
   map→widget (v18), screen→phone (v07), window content→full scene (v07), card→bubble→logo (v02).

## 5. Camera language

| Move | When | Recipe |
|---|---|---|
| **Slow push-in** | default during any hold, typing, focus | scale 1→1.03–1.08 over the hold, linear or DRIFT |
| **Follow-cam** | typing (camera follows the caret), a route on a map, word-by-word copy | `extra: cx = weight × springFollow(caretX…)`, continuous, weight 0.4–0.6, zoom ≤ 1.4 (see §2b) |
| **Pull-back reveal** | detail → context (digits → phone, word → sentence, screen → device) | scale 2–3→1 over 15–25 f, ENTER curve, blur during the fast part |
| **Push-through / portal** | entering an element's content (window, screen, orb, card) | scale ×3–8 into the target over 12–18 f with the EXIT curve; the target's content becomes the new full frame |
| **Reverse portal** | the full scene becomes a component (map→widget, frame→app icon) | animate the scene container's w/h/radius/scale down to a card over 8–14 f, MOVE curve |
| **Whip pan** | to reveal the off-screen end of a long UI, or between items | MOVE curve over 18–26 f: the visible whip is ~5–6 f in the middle at 15–35% of width per frame, with heavy directional blur; slow creep before, soft landing after (`whipKeys`) |
| **Snap zoom** | punch on a beat (typing the key word); max 1–2 per video | instant ×1.5–2 (1–2 f), then ease back over 15–20 f (v23) |
| **3D tilt / tumble** | devices, widgets, cards entering | rotateX/Y 25–60°→0 with ENTER, perspective 1200–2000 px |
| **Shake** | impacts only (launch, slam, explosion); zero shakes is fine | 2–6 px amplitude, 8–12 Hz, decays in 4–8 f; never on holds or UI changes (§4c) |
| **Depth of field** | when the camera is pushed in | blur the frame edges (radial mask) 4–10 px; tilt-shift on wide shots. Keep it constant within a shot: toggling it on/off pops |

## 6. Motion blur rules

**Use real shutter blur: `<MotionBlur samples={10} shutter={180}>` around the composition** (sub-frame accumulation,
like a film camera; see `07-pro-standard.md` §2.3). The SVG/gaussian directional blur below is the fallback for drafts
only; on a whole layer it turns a moving card into a gray block (Yahia's comparison, frames 176–190 of the v2 demo).

- Blur tracks velocity. Measured sharpness at the velocity peak is **~15% of the resting sharpness**
  (median), so the references blur hard during fast frames.
- Directional: horizontal moves blur horizontally (SVG `feGaussianBlur stdDeviation="bx 0"`); scale moves
  get a zoom smear (uniform blur plus echo copies).
- Strength: blur px ≈ 0.35–0.5 × displacement in px per frame (a 180° shutter ≈ 0.5). Cap around 40–60 px.
- Entrances **arrive blurred and focus-pull to sharp** (blur 8–20 px → 0 across 60–70% of the move). This is
  separate from velocity blur and is visible in nearly every reference.
- Holds are tack sharp. Never leave residual blur on a resting element (except deliberate DoF background).
- Echo/trail copies (3–5 ghosts, 1–2 f apart, opacity ×0.55 each) for super-fast zooms and smears.
- Smear frames: for 1–2 f at peak speed, stretch scaleX 1.3–1.8 along the motion (v11 wordmark exit).

## 7. Morph mechanics (the core UI trick)

A morph changes several properties of one container at once:
- **Shape**: w, h, radius (pill radius = h/2 → card radius 24–32 px → circle).
- **Color**: background interpolated in a perceptual space (white→gray→charcoal, gray→blue).
- **Content**: old content fades out (3 f) and slightly scales down/blurs; new content waits until the
  shape is ~50% morphed, then fades/staggers in (4–8 f).
- **Position**: optional, using the MOVE curve.
- Size uses a spring with a small overshoot (2–5%) or the MOVE curve; never linear.
Chains of morphs (one object → many states) are the main storytelling device of the UI style.

## 8. Micro-interactions (copy them exactly)

- **Cursor**: macOS arrow, turns into a hand over clickables, grab-hand for drags. It travels on a
  curved (quadratic) path with the MOVE curve and slight overshoot, has a soft shadow, and blurs when fast.
- **Click**: cursor scale 1→0.85→1; target 1→0.92→1.04→1; optional ripple/focus ring (accent at 25%
  alpha, +6–10 px) grows on hover 6–8 f before the click.
- **Hover → highlight → tooltip** (v14): 6 f hover, highlight fill, tooltip pops 4 f later.
- **Long-press radial menu** (v19): item dims, circles fan out with a 2 f stagger, label above changes per hover.
- **Typing**: caret blinks (on 8 f / off 8 f) when idle and stays solid while typing. Text width grows and the
  container grows with it (spring). Placeholder is gray and disappears on the first char.
- **Selection**: a solid accent rectangle wipes across the text in 4–6 f (select-and-replace, v05/v10).
- **Toggle / slider / stepper**: the knob uses the MOVE curve 8–12 f; numbers roll (odometer) at the same time.
- **Dock magnification + bounce** (v24) for app launches.
- **Notifications** slide from the top or from behind other UI, wider than the device (v10), with a
  spring and a soft shadow.
