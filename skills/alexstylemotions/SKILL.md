---
name: "alexstylemotions"
description: "Recreate the Alex-style talking-head motion system (word-synced kinetic captions, flat infographic builds, counters, card UI inserts) in a color palette the user chooses, when planning, animating or prompting videos."
---

# alexstylemotions — Talking-Head + Infographic Motion System

Reverse-engineered from two long-form business-education YouTube videos (10 min and 16 min, 1280x720, 29.97 fps). The style is **"Premium Explainer Talking-Head"**: a mostly-static seated presenter in a dark studio, interrupted every 10–30 s by fast, flat 2D motion graphics on a dark solid canvas, with word-synced kinetic captions as the connective tissue.

Use this skill to: plan an edit, write motion specs for an editor, build graphics in After Effects / Premiere / Resolve / Remotion / HTML-canvas, or write prompts for AI video tools. Always use **original content and branding** — reproduce the motion language, never the creator's name, logo, face, book covers or channel UI.

---

> **Pro upgrades:** also read `pro-motion-upgrades.md` (motion language lock, A/B/C treatments per line, morph-not-fade, per-element timing, 8 motion-effects recipes adapted). Apply on every edit.
> **Real objects:** when a line names a real thing (money, gold, car, phone, product), read `png-objects.md` — Pinterest/own image → Apple Vision cutout (`tools/png_kit/`) → shadow, masked shine, landing shake.

## 1. Style DNA (one paragraph)

Dark, cool, cinematic A-roll (blue curtains, warm practical light behind) + **flat, high-contrast vector graphics** on a near-black `canvas` field. Everything animates **on the word** — text, numbers, icons and diagram parts appear exactly when they are spoken. Motion is fast-in / soft-settle (strong ease-out), almost never bouncy. `punch` color = the punchline, `body` color = the setup, `accent` color = structure/brand (all chosen by the user — see section 2). Graphics build **additively** (piece by piece, never all at once) and are held on screen just long enough to read, then the edit returns to the face.

---

## 2. Design tokens — colors are the user's choice

The style is defined by **color roles**, not by specific colors. The user picks the palette; the motion system stays the same.

**Before building anything, settle the palette:**
1. If the user has given colors (in this request, earlier in the conversation, or a brand kit / design system), map them onto the roles below.
2. If not, ask once: "Which colors do you want for background, punch/highlight, body text and accent?" Offer the presets below as options. If the user isn't there to answer, use the Reference preset and say so.
3. Fill any role the user left out by deriving it (see "Deriving missing roles").
4. Write the final palette at the top of every output (beat sheet, prompt, code) so it is reused consistently.

| Role | What it does | Reference value (from the analyzed videos) |
|---|---|---|
| `canvas` | Background of every full-screen graphic; also the color A-roll fades into | `#13162A` dark navy |
| `punch` | The one emphasized word/number per line, headlines, key data; gets a soft glow | `#FDFE48` neon yellow |
| `body` | Setup words, labels, line art, icons, strokes | `#FFFFFF` white |
| `accent` | Pills, map fills, icon circles, numbered badges, section-title scenes | `#6A2BF0` purple |
| `accent-gradient` | Background of section-title scenes (T12) | `#240E4A → #391276` |
| `ghost` | Giant background counters, secondary UI | `body` at 35–55% opacity |
| `negative` / `positive` | Down/up arrows, X marks, ticks only | red / green |

**Rules that keep the look regardless of colors chosen:**
- `canvas` must be very dark (or very light for an inverted version); `punch` must be the most saturated, eye-catching color in the frame. Aim for ≥ 7:1 contrast between `punch` and `canvas` on dark palettes (≥ 4.5:1 is enough on light palettes, since punch text is large and bold), and ≥ 4.5:1 for `body`.
- Only `punch` gets the glow. Glow = same color, 15–25 px radius at 720p, 40–60% opacity.
- `punch` is used sparingly: one key word or number per line, never whole paragraphs.
- `accent` must be clearly different in hue from `punch` so structure and emphasis don't blur together.
- Grade the A-roll so its shadows lean toward `canvas` (e.g. teal shadows for a teal canvas) — this makes fades between A-roll and graphics seamless.

**Deriving missing roles:**
- Only `punch` given → `canvas` = near-black tinted toward the complementary hue (L ≈ 8–12%), `body` = white, `accent` = a hue 90–150° away from `punch` at medium lightness.
- Only a brand color given → use it as `accent`; pick `punch` from neon yellow, lime, cyan or orange (whichever has the most hue distance from `accent`).
- `accent-gradient` = `accent` darkened to L ≈ 15% → L ≈ 25%.

**Presets to offer:**

| Preset | canvas | punch | body | accent |
|---|---|---|---|---|
| Reference (Navy / Yellow / Purple) | `#13162A` | `#FDFE48` | `#FFFFFF` | `#6A2BF0` |
| Midnight Cyan | `#0B1220` | `#22E4F5` | `#FFFFFF` | `#FF4D8D` |
| Charcoal Orange | `#141414` | `#FF8A1F` | `#F5F5F5` | `#2F7BFF` |
| Forest Lime | `#0E1A14` | `#B6FF3B` | `#FFFFFF` | `#1FB57A` |
| Royal Gold | `#120F24` | `#FFC83D` | `#FFFFFF` | `#8B5CF6` |
| Light / inverted | `#F4F3EF` | `#C41E1A` | `#111111` | `#1F4FFF` (punch glow off; use underline or bold instead) |

**Typography** (inferred, not confirmed): geometric sans in two weights.
- Punch line: ALL CAPS, Extra-Bold/Black (Montserrat Black / Poppins ExtraBold class), tight tracking, `punch` color with soft glow (glow radius ~15–25 px at 720p, 40–60% opacity).
- Setup line: sentence case or caps, Medium/SemiBold, `body` color, ~45–55% the size of the punch line, sitting directly above it.
- Labels in diagrams: small caps Bold, `punch` headers, `body` text at ~2% frame height.
- Mixed-color lines: `body` words + `punch` keyword(s) in the same line ("MAKES THE **MOST MONEY**").

**Geometry**: thin `body`-color 2 px strokes, rounded-rect frames (radius ~8–16 px), circles, flat glyph icons (person, play button, gear, target, magnifier), silhouettes, dot-matrix maps, dashed lines. No 3D extrusions, no textures. Light glow on strokes and `punch` text is the only "effect".

---

## 3. Layout system

1. **A-roll framings** (multi-cam, ~3 angles): (a) frontal medium, subject centered, table edge at bottom 10%; (b) 3/4 side angle from camera-left, subject left-of-center; (c) tighter frontal for emphasis. Digital punch-ins (110–130%) on emphatic lines.
2. **Caption zone**: lower-center, baseline at ~80–88% of frame height, max width ~75%. Two stacked tiers (setup above, punch below).
3. **Split layout (A-roll + panel)**: speaker pushed to one side (side angle or reframed), the empty side darkened with a gradient to near-black, and a vertical panel of screenshots / bullet list / tweet card occupies the other 35–40%. Text in the panel builds line-by-line with speech.
4. **Full-screen infographic**: `canvas` background, centered composition, headline top-center (8–15% from top), graphic center, generous negative space (≥40% empty).
5. **Corner callouts**: small card or label in the upper-right third beside the head (tweet card, list of items, keyword stack).
6. **Framed media**: B-roll / screen recordings placed inside a rounded card with soft drop shadow on `canvas`, never just full-bleed (occasional full-bleed stock B-roll for metaphors).

---

## 4. Motion principles (the rules)

1. **Speech is the timeline.** Every reveal is keyed to the syllable that names it (±2 frames). Word captions arrive ~1 word per 0.15–0.3 s.
2. **Ease-out dominant.** Entrances use a strong ease-out (cubic-bezier ≈ `0.16, 1, 0.3, 1` / "expo out"). Elements reach ~90% of their move in the first third of the duration and glide to rest. Overshoot is rare and small (≤3%).
3. **Short entrances, long holds.** Entrances 6–12 frames (0.2–0.4 s); holds 1.5–6 s; exits are usually a hard cut or a 0.3–0.6 s fade to `canvas` — not animated individually.
4. **Additive build.** Diagrams appear in reading order: frame → headers → icon → connector → label → next item. Never reveal the whole graphic at once.
5. **Blur as softness.** Text and numbers enter with Gaussian blur 8–15 px → 0 combined with opacity 0 → 100% and a small scale (105–110% → 100%) or 10–20 px upward drift. This is the signature "soft focus-in" look.
6. **Stagger, don't sync.** Groups (cards, icons, grid items, bullets) use 2–5 frame offsets left→right or top→bottom.
7. **One focal point at a time.** When a new element arrives, previous ones stay but stop moving; `punch` marks the current focus.
8. **Camera moves are slow, edits are fast.** Virtual camera pushes in 2D (scale 100→115% over 2–4 s) on held graphics; cuts between A-roll angles happen on sentence boundaries.
9. **Flat depth only.** Depth comes from scale, opacity, darkened edges/vignette and drop shadows — not 3D perspective (exception: a short 3D tilt of a framed card settling flat).

---

## 5. Technique library (recipes with timings)

Timings measured from the reference at 30 fps; treat as defaults.

### T1 — Two-tier kinetic caption (the backbone)
- Setup line: words appear one at a time, each fading in from 0% with blur ~10 px over 4–6 frames; `body` color, smaller.
- Punch line: below it, each word pops in `punch` color, caps, glow; same blur-fade + scale 110→100% over 4–6 frames.
- Lines replace each other with a hard swap (no slide-out) when the phrase ends.
- Only key phrases get the two-tier treatment; filler speech gets a single small `body` line or nothing.

### T2 — Ghost rolling counter behind caption
- Giant number (~20–25% frame height), `ghost` (body at ~40–55% opacity), positioned right behind the caption zone.
- Counts up fast (≈ 1–1.5 s) with ease-out on value, digits slightly blurred while rolling, then holds the final figure.
- Variant: big `punch` currency line at top of frame ("$250,000,000") whose characters reveal left→right with blur-fade over ~1 s while digits still roll.

### T3 — Fade-to-canvas into a full-screen graphic
- A-roll dims/fades to the `canvas` color over ~0.5–0.6 s (cross-dissolve via `canvas`, not black).
- The graphic starts building immediately as the frame turns to `canvas`.

### T4 — "Grow from point" object reveal (road/fork example)
- A flat road shape scales up from a point on the horizon (0.6–0.9 s, ease-out), dashed center line rides with it.
- Signpost pole extends upward (stroke/scale-Y from base), then direction signs slide out sideways from the pole (6–8 frames each, staggered).
- Headline words cascade in above (T1 style). Later beats add new signs/labels to the same scene and the virtual camera pans to the new area.

### T5 — Stroke draw-on diagram
- Rounded frame and divider lines draw on from their endpoints (trim-path 0→100%, ~0.6–0.8 s).
- Column headers type on character by character (~0.3–0.4 s per header), `punch` color.
- Icon fades/scales in → connector arrow grows down (trim path, ~0.4 s) → label types on → next node.
- Annotation: a `negative` "X" draws across a section to negate it (two strokes, ~0.3 s each).

### T6 — Radial pie fill + value counter
- `body`-color circle fills by a clockwise radial wipe from 12 o'clock (~1.2–1.5 s, ease-out) while an `accent` currency number in the center counts to the target. Headline above in `punch` types on word by word.

### T7 — Dot-matrix map / data split
- Map built from a dot grid in dim `body`; region highlights by recoloring dots (`punch` or `accent`) with a left→right sweep; percentage labels fade in; big values ($2 vs $98) scale-pop in `body` on `accent`.

### T8 — A-roll shrinks into a UI card
- Full-frame talking head scales down to ~50–60% over ~0.6–0.9 s (ease-in-out), gaining rounded corners, a drop shadow, and a fake video-player control bar.
- `canvas` background revealed around it; then a dense icon grid (people glyphs) fades in behind with edge vignette, so the card sits "on top of the audience".

### T9 — Grid multiplication (zoom-out reveal)
- Single rounded card with a silhouette illustration, then the camera zooms out (card 100% → ~15% scale over ~1.2 s) revealing it is one of a large grid of identical cards; grid items fill in with a stagger. Communicates "everyone / many people".

### T10 — Social post / tweet build
- Card (white-on-light or dark variant) pops in (scale 95→100 + fade, ~0.25 s) in the upper-right of A-roll or full-screen on `canvas`.
- Body text typed word by word synced to VO; key words become bold `punch`. Each new word blur-fades in like T1.

### T11 — Bullet side-panel
- Reframe speaker to one side; darken the other side with a horizontal gradient.
- Bullet points appear word by word, a new bullet starting the moment it is spoken; lines wrap naturally; no boxes around text.

### T12 — Glassy stage cards (section titles)
- `accent-gradient` background. 3 tall rounded "glass" cards (semi-transparent, subtle top highlight, bottom glow) rise from below with a 4–6 frame stagger.
- Numbered badges (01/02/03) pop at the corners; glowing orbs fade in inside each card, then morph into icons (target, magnifier, cycle).
- Title types on top ("3 STAGES OF …"). Then camera pushes into card 01 while the others fade out → that card becomes the chapter header.

### T13 — Circle / iris transitions
- Avatar circle with gradient ring: silhouette placeholder → photo revealed with a glow sweep; a `punch` label pops underneath.
- Exit: a circle mask expands from the center of the graphic revealing the A-roll underneath (≈0.5 s), or a profile page scrolls up with ease-out and the next shot is revealed through a growing circle.

### T14 — Whip / directional-blur swap
- Swapping one card for the next: 4–6 frame vertical or horizontal move with heavy directional motion blur, new content lands with ease-out. Used to change values inside the same chart.

### T15 — Chart draw
- Axes draw on (L-shape trim path), a dashed trend line draws from origin, a `punch` gradient fill grows under it; axis label types on ("DECADE OF EXPERIENCE"). Bar charts: bars grow from baseline with stagger; product icons pop at bar tops.

### T16 — Opening focus-pull
- Video starts on a defocused frame (blur ~20 px) that snaps sharp in ~0.2 s as the first caption word lands.

### T17 — Framed B-roll / proof clips
- Real-world or stock footage dropped in a rounded card on `canvas`, often entering with a slight 3D tilt that flattens (≈0.5 s), with a `punch`/`body` caption build underneath ("GUINNESS WORLD RECORD FOR …").

---

## 6. Edit rhythm

- Hook (first 10–20 s): densest section — a graphic, counter or proof clip every 1–4 s, captions on almost every phrase.
- Body: alternates **long A-roll holds (10–60 s, often uncut)** with **graphic beats (3–15 s)**. Median shot ≈ 6–7 s, mean ≈ 10–13 s (scene-detect on the references).
- Angle changes (front ↔ side ↔ tight) on sentence boundaries to reset attention; punch-ins on emphatic words.
- Key-phrase captions appear on maybe 1 phrase in 3–5 during the body; full graphics when introducing a framework, number, list or comparison.
- Graphic scenes exit by cut back to the face — the face is "home base".
- Ends with a small legal-disclaimer text block over the A-roll.

**Sound**: not verified in detail from the references. Speech-first mix; if adding SFX, keep it subtle (soft whooshes on scale/whip moves, light ticks on counters/typing, short hits on punch words) and never louder than the voice.

---

## 7. Production workflow (plausible, not confirmed)

1. **Shoot**: 2–3 cameras in a dark set (blue curtain backdrop, warm practical lights, desk), 4K for clean 120–130% punch-ins. Grade so shadows lean toward the `canvas` hue (reference: lifted blacks toward navy, blue curtains, warm skin).
2. **Cut A-roll** in Premiere/Resolve: remove pauses, switch angles at sentence ends, mark beats for graphics.
3. **Transcript → beat sheet**: word-level timestamps (Whisper or Premiere transcript). Tag every number, list, framework, comparison and proof claim as a graphic beat.
4. **Graphics** in After Effects (most likely): shape layers + trim paths (T5, T15), text animators with per-word range selectors (opacity + blur + scale) for T1/T10/T11, Number-counter expressions / slider controls (T2, T6), radial wipe (T6), track mattes / circle masks (T13), 2D camera or null-parent scale for pushes (T4, T9, T12), directional blur / motion blur (T14). Vector assets from Illustrator. Reusable as Essential Graphics / MOGRT templates so editors can retype.
5. **Captions**: either AE text presets or a caption tool with per-word animation; keyword color set by hand.
6. **Composite** back over A-roll; graphics for full-screen beats are rendered as `canvas` plates.
7. **Mix & export** 16:9, 30 fps.

Code alternative: Remotion / Motion Canvas / GSAP with the same tokens — `spring` with high damping (no bounce) or `easeOutExpo`, per-word timestamps driving reveals.

---

## 8. Build checklist (use when producing a beat)

0. Palette settled (section 2) and written at the top?
1. Which spoken word triggers each element? Write the timestamp next to it.
2. Background: A-roll, darkened split, or `canvas`?
3. Headline: setup (`body`) + punch (`punch`) — which single word gets the `punch` color?
4. Build order: frame → header → focal object → connector → labels.
5. Entrance: 6–12 frames, ease-out, blur-fade for text, stagger 2–5 frames for groups.
6. Hold until the line ends + ~0.5 s; exit by cut or fade to `canvas`.
7. Check: ≥40% negative space, one focal point, contrast readable on phone, no more than ~8 words in the punch line.

---

## 9. Prompt template for AI video / for briefing an editor

Replace `{canvas}`, `{punch}`, `{body}`, `{accent}` with the user's chosen palette (hex + plain color name, e.g. "#22E4F5 cyan").

> Solid {canvas} background, flat 2D infographic in modern YouTube business-education style. [OBJECT] builds piece by piece in sync with narration: thin {body} 2px line art draws on, a {body} header types on, then the key phrase "[PHRASE]" appears in bold all-caps {punch} with a soft glow, each word blur-fading in. Strong ease-out motion, no bounce, quick 0.3 s entrances, staggered groups, slow 2D camera push-in, lots of negative space, {accent} accents. Clean, premium, high contrast, 16:9.

For A-roll caption beats:
> Seated presenter in a dark studio graded toward {canvas}; lower-third two-tier kinetic captions: small {body} setup line above, large bold {punch} all-caps punch words below, each word appearing exactly as spoken with a blur-to-sharp fade and slight scale-down; a giant semi-transparent {body} number counts up behind the captions.

---

## 10. Output format when asked to "apply alexstylemotions"

Start with the palette line (`canvas / punch / body / accent` with hex values). Then deliver a **beat sheet** table: `timestamp | spoken line | layout (A-roll / split / canvas) | technique ID (T1–T17) | elements & build order | timing (frames) | color roles`. Then list required assets and any AE/Remotion implementation notes. Keep all branding original to the user.