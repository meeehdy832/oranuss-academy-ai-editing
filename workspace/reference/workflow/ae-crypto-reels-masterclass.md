# Breakdown: "How to Edit VIRAL Crypto Instagram Reels in After Effects" (Joseph | Video Editing)

> Developed by Mehdi ORANUSS | Powered by Claude

- Source: https://www.youtube.com/watch?v=ila1noDhK_8 (31 min tutorial, published 2025-04-03)
- How it was studied: I read the YouTube transcript panel in the browser and looked at a few frames. Neither the video nor the raw footage on Drive was downloaded.
- What it is: a full workflow for a talking-head crypto reel. The steps are clean cuts and captions in Premiere, three motion-graphics inserts in After Effects, then sound design and music.
- Use this file for **techniques only**. Never copy the creator's graphics, text, branding, figures (the "$100,000" on screen is demo content) or his course pitch.

---

## 1. The reel's structure (why it works)

| Beat | Time in the reel | What happens |
|---|---|---|
| Hook | 0–3 s | The talking head opens with a whoosh on a zoom-out. The topic is stated in one line ("X has blown up"). |
| Insert 1: "proof" UI | ~3–9 s | A dark UI dashboard: tiles pop in, a cursor hovers and clicks, the tiles slide off, and a growth graph draws in ("blown up off the charts"). |
| Insert 2: "question" 3D | ~9–16 s | A 3D scene: two glowing bubbles (play and pause), then a glass box with a rotating extruded coin and a title. A camera move happens on each element, and there is a reflection on the floor. |
| Insert 3: "payoff" coin | ~16–22 s | Circles expand behind the subject. A frosted-glass card holds a title, a price box and a spinning 3D coin. The camera pulls back from the coin to the whole card. |
| Close | end | The talking head comes back with an open question ("all we have so far are questions"), which drives comments. |

- Pacing: each insert is tied to one spoken sentence, and each element lands on the word that names it.
- About 70 % of the screen time is graphics: the face sets up the point and the graphics prove it.
- The look is a dark navy and black world, glassy grey-blue UI, soft blue and purple glow, and orange or gold reserved for money.

---

## 2. His workflow, step by step (and how we do it)

### Stage 1: cuts and captions (Premiere in the tutorial; ffmpeg and whisper for us)

1. **Remove the silences.** Cut out every pause between phrases with the razor tool.
   - We already automate this: `project/intro_ai_cut.py` removes pauses at −32 dB that last 0.28 s or more, keeping 0.10 s of padding.
2. **Use J-cuts.** Let the next clip's audio start a few frames before its picture. This makes jump cuts feel smooth.
   - *Not in our cutter yet.* Possible upgrade: lead the audio by 2–4 frames (0.07–0.13 s) at each cut in the EDL.
3. **Build the captions.**
   - His settings: "create captions from transcript", 20 characters a line, one line, a thin font, centred just under the chin, saved as a text style.
   - Ours: `kinetic-captions` / `darija-voice-captions` (Latin Darija, or Arabic in Graphik Arabic), 2–4 words at a time.
   - Worth adopting: put the captions **just under the chin**, not at the bottom of the frame, on talking-head reels.
4. **Send it to After Effects.** In Premiere, "Replace with After Effects composition", then tidy the layers in AE.
   - He uses the free *UnPrecompose* script so the captions become loose text layers.
   - In our AE projects, the captions and keywords are built as editable text by script (see `project/ae/intro_ai_build.jsx`).

### Stage 2: shared text animation (used on every caption and keyword)

- Glow: Deep Glow at exposure 0.2. The regular Glow effect works as a fallback.
- Entrance:
  - Scale from 0 to 100 %, then smoothed in the graph editor so it starts fast and slows into place.
  - Opacity from 0 to 100 % at the same time.
- Copy and paste the same keyframes onto every text layer, so the motion stays consistent.
- Our equivalent is the `kword` blur-slam in `hfkit` (scale 1.35 → 1, blur 16 → 0, expo.out over 0.32 s), and `S.pop` for chips.

### Stage 3: Insert 1, dark UI dashboard with a cursor and a growth graph

1. **Background:**
   - A solid with *4-Color Gradient*: black, dark blue, grey-blue and grey.
   - Set *Blend* to 200 so the colours mix into soft blobs instead of corners.
2. **Tiles:**
   - Shape-layer rounded rectangles in grey-blue.
   - Duplicate a layer and delete its path to get the same style with a new shape.
   - Make a bento grid: one large tile, two squares, one long bar and one more square.
3. **Content per tile:**
   - A bold title, a thin subtitle and an icon. Recolour the icons with the *Tint* effect so they match the text.
   - A small arrow in each tile makes it read as UI.
4. **Parent each tile's content to the tile's shape layer.** Then one keyframe set on the tile animates the whole card.
5. **Tile entrance:**
   - Scale up from slightly smaller (fast start, slow end).
   - Opacity 0 → 100 % on the tile and on its children.
   - **Stagger the tiles** by a few frames each, so they don't all appear at once.
6. **Cursor:**
   - Moves along a curved motion path (pen tool) with eased speed.
   - Tinted light grey.
   - Click = scale 100 → 10 → 15 (shrink and pop back, easy ease), then fade out.
7. **Hover feedback on a tile:**
   - When the cursor arrives, the tile scales up a little and its fill colour animates (blue → light green).
   - When the cursor leaves, both return to normal.
   - The tile's glow also turns on (0 → 0.1) while hovered and off when the cursor leaves.
8. **Exit:** after the click, every tile slides off to the left together, with an eased position move.
9. **Graph scene** (slides in from the right as the tiles leave):
   - Two rounded rectangles with gradients: one slightly lighter than the background, one slightly darker, to give depth.
   - A stat chip in one corner.
   - Axis lines drawn on with *Trim Paths* (end 0 → 100 %).
   - A thick wiggly line with a multicolour gradient stroke, drawn on with Trim Paths.
   - **Area glow under the line:**
     - A shape traced along the line and down to the axis.
     - Filled with *Gradient Ramp* from light orange to black.
     - Blending mode *Add*, so only the light shows.
     - It fades in as the line draws.
   - Deep Glow on the line (0.2) and on the area.
   - A heavy title and a description to finish.

**For Oranuss:** this matches our `ui-demo-mockups` and `animated-chart` skills.
- The new pieces worth reusing are:
  - the cursor hover-and-click choreography (scale bump, colour change and glow while hovered);
  - the additive area glow under a line chart;
  - staggered bento tiles parented to their card.
- In HyperFrames:
  - Trim Paths = `strokeDashoffset`.
  - The Add blending mode = `mix-blend-mode: screen` (or `plus-lighter`).
  - The tint = a CSS `color` on SVG icons.
- In our purple worlds:
  - The tiles become frosted glass (`.glass`), and the line gradient runs lavender → violet `#8B5CF6` → `#5B21B6`.
  - Use green for hover/confirm, as he does; it also matches our check chips.

### Stage 4: Insert 2, a 3D scene with glowing bubbles, a glass box, an extruded coin and a reflection

1. **Gradient-lit bubble:**
   - A circle with a *radial gradient* fill from black to light blue.
   - Duplicate it and move the gradient so the light comes from a second side.
   - Set both copies to the *Add* blending mode: the black drops out and only the rim light stays.
   - Put the icon (play/pause) inside, with a light 4-colour gradient on it.
2. **Bubble pop:** rises from below with eased position and fades in. Deep Glow on the gradients.
3. **3D set-up:**
   - Make every layer except the background 3D. Effects render with the *Classic 3D* renderer.
   - Arrange the layers in depth.
   - To make the second bubble, duplicate the first and move its anchor point.
4. **Glass box:** several stacked rounded rectangles, each with a slightly different gradient colour and angle. Deep Glow on each coloured layer.
5. **Extruded coin:**
   - A circle precomposed, with the precomp set to the *Advanced 3D* renderer and *Extrusion depth* raised.
   - Rotation keyframes on X and Y, kept **linear**, so it floats like a machine part.
   - **Two lights:** a spot light from above and a second from below facing up, as rim/contrast light. Then glow.
6. **Text:** 3D text layers.
   - The title is white and bold, with a thin-font description and one script-font accent word.
   - The text sits in front of the box on Z for depth, with a subtle glow.
7. **One-node camera with a cut per element:**
   - Element 1: starts zoomed out and pushes in (fast start, slow end).
   - Element 2: the same move.
   - Element 3: starts close on the box and pulls back to the full frame, with a speed spike in the graph.
8. **Floor reflection:**
   - Duplicate all the layers, precompose them and flip the copy onto the floor plane (rotate X).
   - Add Gaussian Blur 150 and *Wave Warp* (speed 0.5) so it ripples.
   - Recut and reposition the reflection for each camera cut.

**For Oranuss:** this is our purple-3d-glass world, but in dark mode.
- The two-light rim trick and the Add-blended radial gradients are the reusable lessons. In HyperFrames:
  - two `radial-gradient` layers with `mix-blend-mode: screen`;
  - the rim light = an inset box-shadow plus a highlight gradient.
- An extruded coin needs real 3D: three.js in HyperFrames (`title-sequence-3d`), or AE's Advanced 3D.
- The floor reflection is easy in HyperFrames: a flipped copy with `transform: scaleY(-1)`, a blur and a fading mask.

### Stage 5: Insert 3, expanding circles, a frosted UI card and a 3D model spin

1. **Background:**
   - Concentric circles scale from 0 to beyond full screen.
   - Each one starts a few frames after the last, in progressively lighter greys.
   - Together they make a "ripple" wipe.
2. **Frosted glass card:**
   - An *adjustment layer* with a rectangle mask, *Gaussian Blur* 300 and the mask expansion raised to round the corners: this blurs everything behind the card.
   - A shape layer on top traces the same rounded rect with a 1 px white stroke and no fill.
3. **Top-edge highlight:**
   - A black-filled copy of the card with *Light Sweep* (wide, intensity 0).
   - Set to *Add*, so only the bright edge shows, then glow.
4. **Content:**
   - A thick title, a light-font description and a "details" line at lower opacity.
   - A rounded price box with dark grey text.
5. **Coin base:**
   - A rounded rect with an orange Light Sweep and the Add mode, plus glow.
   - Under it, a copy with a light-grey-to-orange 4-colour gradient as the backplate.
6. **3D model:**
   - A downloaded 3D coin model inside an Advanced 3D precomp.
   - A Y spin that starts fast and slows to a stop.
   - Lights: a key light from above at intensity 500, plus an opposite rim light.
   - Deep Glow 0.5 on the precomp.
7. **Text over the scene:**
   - A big number with a *Gradient Ramp* (light grey → dark grey).
   - A script-font word with an orange → yellow ramp.
8. **Camera:** starts tight on the coin box and pulls out to the whole card (fast start, slow end).

**For Oranuss:** the frosted card is our `.glass`, already in HyperFrames as `backdrop-filter`. In AE, use an adjustment layer + blur + mask.
- The Light Sweep edge highlight and the ripple-circle background are new for us.
- Gradient text through the glyphs matches what our AE builder does: Gradient Ramp + Set Matte on the text layer.

### Stage 6: sound design and music (his choices → our OrcaXV IDs)

| Moment | His sound | OrcaXV Essentials 100 |
|---|---|---|
| Opening zoom-out | whoosh | `WH-156` Whoosh Big 1 / `WH-012` Whoosh Short Deep |
| UI tiles reveal | UI reveal | `WH-163` Whoosh Digital 1 or `DA-002` Data System Online |
| Tile turns green | small click per box | `PO-019` Ding Quick Win / `UI-019` Click Soft |
| Cursor click | click | `UI-005` Click Mouse |
| Everything slides off | big whoosh | `WH-158` Whoosh Big 2 |
| Graph draws in | wind + UI | `DA-007` Data Reveal + `WH-166` Whoosh Digital 2 |
| Bubbles pop (mysterious) | computer glitch ×2 | `GL-002` Glitch TV, `GL-004` Glitch Short |
| Big box reveal | UI select + glitch | `UI-001` UI Button + `GL-010` Glitch Hit |
| Camera pull-back | whoosh under it | `WH-013` Whoosh Cinematic Flyby |
| Ambience under the 3D scenes | sci-fi drone, cut on the scene change | none in the 100; use `RS-021` Riser Suspense quietly, or the full pack |
| Into the next cut | riser | `RS-006` Riser Smooth (`align: end` on the cut) |
| Coin highlight | metallic whoosh | `WH-062` Whoosh Metal |
| Money mention | cash register, low | `RW-020` Cash Register |
| Music | "mysterious synthwave" bed, turned well down | a track from `music/`, about −20 dB under the voice |

His rule matches ours: one sound for each visible event, layered when a reveal is big (UI + glitch, whoosh + drone), with ambience to glue the 3D scenes together.

---

## 3. Lessons to reuse (checklist)

1. Put the captions **under the chin**, one short line, in a thin font. The keywords get the heavy treatment.
2. Each graphic insert shows one spoken sentence. Elements land on their words, and the whole insert leaves as one move.
3. Parent the content to its card, animate the card, and stagger the cards by 2–4 frames.
4. Cursor choreography sells a UI: an eased curved path, a hover bump with colour and glow, a click squash (100 → 10 → 15 %), then exit.
5. Light shapes: radial or 4-colour gradients with the Add (screen) mode. Black drops out and only the light stays.
6. Use two lights on any 3D object (key above, rim below), then glow. Keep idle rotations linear so the object "floats".
7. Camera moves: a cut per element; push in on small things and pull back on the big reveal; fast start, slow end.
8. A floor reflection (flipped copy + blur + wave warp) makes a 3D scene feel expensive.
9. A frosted card = blur behind + 1 px white stroke + a bright top-edge highlight.
10. Sound: whoosh on camera moves, UI/click on interactions, glitch for "mystery", a riser into a cut, and a quiet drone under the 3D.

## Where these lessons now live

- `.claude/skills/ui-demo-mockups/SKILL.md`, "Batch 4": bento tiles, cursor choreography, light shapes, frosted-card edge highlight, ripple background, two-light 3D, floor reflection, camera per element.
- `~/.claude/skills/animated-chart/SKILL.md`, "Optional variant: glowing line chart": axes and line draw-on, additive area glow, line glow.

## 4. What was left out

- The 3D coin model downloaded from Sketchfab, and the paid tools he uses: Deep Glow, UnPrecompose, Epidemic Sound. Our equivalents are AE Glow / CSS bloom, our own build script, and OrcaXV + `music/`.
- His exact graphics, text and figures, the course and sponsor sections (14:00–15:30) and the "Ultimate Editors" pitch.
- Exact colour values. They were not read off frames, so the palettes above describe what he says, not measurements.
