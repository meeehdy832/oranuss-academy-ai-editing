---
name: ui-demo-mockups
description: Rebuild app interfaces (chat with typing, terminal, share menu, response cards, idea chips, waveform, timeline, music list, knobs, render settings, code file, folder, bento tiles, cursor hover and click, glowing bubbles, frosted cards, lit 3D objects with floor reflections) as clean animated Oranuss-style mockups instead of raw screen recordings. Use for "how I do it" demos inside split-screen panels.
---

# UI demo mockups

Developed by Mehdi ORANUSS | Powered by Claude

Rebuilt UI reads better than screen recordings: it's sharp at any size, on brand, has no private data, and every element can animate on cue.

## Base frame
Every mockup sits in a glass card (see `oranuss-visual-system`). It has a 36px title bar with three small dots or the app name in mono lavender, rounded corners (r=24), and padding of 32px.

## Component library (one call each, timed to the spoken word)
| Component | Animation |
|---|---|
| **Share menu** | Card with 3 rows (icon + label: `Copier le lien`, `Partager…`, `Enregistrer`); a cursor arrow moves to row 1, the row highlights purple, then a "copied ✓" toast |
| **Chat input** | Typewriter: the text grows by one character every 35–45ms (a series of ASS events or `\clip` growing left→right per word), blinking caret `|`, a send button pulses at the end |
| **Response card** | Rows of `KEY  value` (mono key in lavender, value white) appear one by one, 120ms apart; colour swatches as circles with their hex |
| **Terminal** | Ink background, mono green/lavender prompt `❯`, lines print one by one, a spinner `⠋⠙⠹` while "working" |
| **Idea chips** | Pills pop in a loose grid with bounce, stagger 90ms; the chosen chip turns purple |
| **Voice waveform** | 40–60 vertical bars; heights driven by the real audio level (sample the RMS per 1/15s with ffmpeg `astats`) or a seeded random; a playhead sweeps |
| **Timeline** | 3–4 tracks (VIDEO, VOICE, MUSIC, SFX), purple clips slide into place, the playhead moves, a timecode counts |
| **Music list** | Rows of track names, the selected one highlights with an equaliser icon animating |
| **Knobs/sliders** | Labelled `design` / `rythme` / `vibe`; the knob rotates (`\frz`) to its value and the value label counts up |
| **Render settings** | `Composition MAIN · 1080×1920 · 30 fps`; a big fps number counts up; a progress bar fills; a "✓ rendu" toast |
| **Aspect swap** | 9:16 frame morphs to 16:9 (animate the width and height of a rounded rect) with a label |
| **Speed gauge** | Chip icon + an arc gauge whose needle rotates to "×5" |
| **Code file** | `SKILL.md` card: mono lines with YAML front matter highlighted lavender, typing in line by line |
| **Folder / carousel** | Glass folder with cards rising out; or 3–5 cards on a stage, the centre one bigger and glowing |

### Added from reference batch 2 (Dd69jHUR4mX, DfHasR3Is5L, Deu8ZBhoTdr)
| Component | Animation (Oranuss version) |
|---|---|
| **Notification toast** | macOS-style glass pill sliding down from the top: app icon + bold title + one line ("Render complete · Oranuss-final.mp4"); holds 1.5s, slides up |
| **Phone mockup** | Rounded black device frame (r=56) playing a video or clip inside; tilts in 6° → 0°; used for a meta hook or to show a phone POV |
| **Viewer question card** | White or lavender rounded card with an avatar circle and the comment text (a real comment, approved by the user); pops over the face as the hook |
| **Selector card** | Options with radio dots, a highlight bar following a cursor, a slider filling; the chosen option turns purple |
| **Command transform** | Terminal: typing `/command`, then the text lines collapse (scale Y→0, merge) into one summary box, then a connector line to the app icon |
| **Node graph** | Input card → glowing core icon → N output cards (connector lines draw with `\clip`, cards pop with a stagger); for "one input, many results" |
| **Video player + comment pins** | Player frame, a scrubber moving, a comment bubble pinned to a timecode marker; for showing review and edits |
| **Step list card** | Light paper or glass card: "Step by Step" + an italic accent word, rows 01–05 sliding in with a stagger, the active row highlighted |
| **Question form** | Dark card with a question and multiple-choice options; the cursor hovers, one gets selected |
| **Tag groups** | Labelled groups (Transitions / Text Animation / Graphics) with small chips popping |
| **Price / offer pill** | Glass pill with an icon + a big number in purple/yellow ("14 jour fabor") |
| **Comment-box CTA** | Comment input with an emoji row and a typing placeholder ("Kteb 'ORANUSS' f comments") |
| **Design-editor overlay** | Dashed selection rectangle with corner handles around the head (tracking per segment) + an "EP 0N" badge + 2–4 lavender words placed and rotated around the box |
| **Content card (top half)** | Prompt, result image or screenshot in a rounded card in the top 45%; the speaker below |
| **Arched title** | Heavy text on an arc (one ASS event per letter, rotated `\frz` along the arc) above an image row |

## Rules
- Use the user's real words or plausible ones; never show real personal data, emails, private chats, or another creator's handles unless the user approves it.
- Text inside mockups must be readable: at least 28px in 1080-wide, and on screen for at least 1.2s after it finishes appearing.
- One mockup per beat; switch the mockup's state on the spoken keyword (take word timings from the caption JSON).
- Implementation: ASS drawings and events (see `project/build.py` helpers `rr`, `co`, `glass`, `chip`). If the user approves installing Remotion, build these as React components for richer motion. Ask before installing it.

## Batch 3 components (Pinterest refs, built in project/build_1025.py)
- **Glass gift/portfolio folder:** a back panel, 3 cards that rise out on the keyword (eased, 80 ms stagger, slight rotation), and a front glass flap carrying the brand word.
- **Skill grid:** 2-column glass cards with an icon bubble, a Darija name and a small English sub-label. The active card glows while it is spoken, and a counter reads "0N / 07".
- **Line chart with a riding dot:** monotonic curve, area fill, linear wipe, a dot that follows the line, an end spring and a label pill.
- **Cursor + CTA button:** the cursor eases in, presses, the button dips and a ripple expands.
- **Stacked kinetic title:** small spaced label, huge heavy word, keyword in a purple bar that wipes in.

## Batch 4: cursor, glow and 3D-light recipes (from `reference/workflow/ae-crypto-reels-masterclass.md`)
Techniques only, adapted to Oranuss. In HyperFrames use `hfkit` (`glass`, `S.pop`, `S.side`) + GSAP; in After Effects use the notes in brackets.

**Bento tiles, parented + staggered**
- One large tile, two squares, one long bar, one more square. Each tile = `glass()` card; its title, sub-label, icon and small arrow live *inside* the card div, so one tween moves the whole card [AE: parent the content to the tile's shape layer].
- Entrance: scale .92 → 1 + opacity 0 → 1, `power3.out`, 0.45 s; stagger 2–4 frames (0.07–0.13 s) per tile, in reading order.
- Exit: all tiles leave together as one move (x −120 %, `power3.in`, 0.5 s) while the next scene slides in from the right.

**Cursor choreography** (sells any UI)
1. Path: curved, eased (`power2.inOut`), 0.6–0.9 s; light-grey arrow (`#E9E3FF`), slight drop shadow [AE: pen-tool motion path + easy ease].
2. Hover: as the cursor arrives, the target tile scales 1 → 1.04, its fill goes glass → green `#22C55E` tint (confirm) or purple `#8B5CF6` (select), and its glow turns on (box-shadow 0 → `0 0 40px rgba(139,92,246,.55)`). On leave, all three return.
3. Click: a squash and pop back. The tutorial goes 100 → 10 → 15 % on his cursor asset; on our small arrow start from 1 → .82 → .9 → 1 over 0.18 s and tune by eye on stills. Add a ripple ring from the tip (scale 0 → 1.6, opacity .6 → 0, 0.35 s).
4. Exit: cursor fades 0.2 s after the click. SFX: `UI-005` on the click, `PO-019`/`UI-019` on the colour change.

**Light shapes (Add / screen blending)**
- Glowing bubble: two stacked circles, each `radial-gradient(circle at 30% 25%, #C4B5FD, #000 70%)` and the second lit from the opposite side; both `mix-blend-mode: screen` (or `plus-lighter`) on a dark scene, so black drops out and only the rim light stays. Icon (play/pause) inside with a light gradient. Pop: rise 60 px + fade, `expo.out` [AE: radial-gradient fill, Add mode, glow].
- Works only on dark backgrounds. On our light purple-3d-glass world use `sphere()` instead.

**Frosted card edge highlight + ripple background**
- Card = `.glass` (backdrop-filter blur) + 1 px `rgba(255,255,255,.55)` border. Top-edge highlight: a `linear-gradient(90deg, transparent, #fff 50%, transparent)` 2 px strip on the top edge, `mix-blend-mode: screen`, optionally swept left → right once (0.8 s) [AE: black copy of the card + Light Sweep, Add mode, glow].
- Ripple wipe: 4–6 concentric circles scale 0 → 2.5× screen, each 3–4 frames after the last, each a step lighter (`#1E1B3A` → `#4C3D8F` on dark, `#EDE9FE` → `#C4B5FD` on light). SFX `WH-013` under it.

**3D object lighting (coin, logo, device)**
- Two lights: key from above + rim from below facing up, then glow. Idle rotation **linear** (constant speed) so it floats; a hero spin is fast-in, slow-to-stop (`expo.out`).
- HyperFrames: three.js (see `title-sequence-3d`): `DirectionalLight` key at (0, 5, 3), second `DirectionalLight`/`SpotLight` at (0, −4, 2) in lavender `#C4B5FD`, `UnrealBloomPass` small. AE: Advanced 3D precomp + extrusion depth, spot light above, second light below.
- Use only models we own or make (an extruded Oranuss mark from `brand/logos/`, a plain coin). Never a downloaded third-party model without the user's OK.

**Floor reflection** (makes a 3D scene feel expensive)
- Flipped copy of the scene group: `transform: scaleY(-1)`, `filter: blur(14px)`, opacity .35, `mask-image: linear-gradient(#000, transparent 60%)`, placed under the floor line. Optional slow ripple: animate a small `skewX` ±1° [AE: duplicate + precompose, rotate X onto the floor, Gaussian Blur 150 + Wave Warp speed 0.5].
- Re-place the reflection for every camera cut.

**Camera per element**
- One cut per element: push in on small things (scale 1.15 → 1, fast start, slow end), pull back on the big reveal. SFX: whoosh on each move (`WH-013`, `WH-156`).
