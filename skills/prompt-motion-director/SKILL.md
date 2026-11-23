---
name: prompt-motion-director
description: Direct and build impressive, 3D-first motion graphics with Claude, using the brief structure and techniques distilled from the Prompt Motion library (prompt-motion.com). Use whenever the user wants a motion graphic, product explainer, launch film, showreel, kinetic-type piece, or b-roll cover scenes for a talking-head short that must look "incredible" rather than flat; also when they paste a one-line prompt like "make a dynamic 30-second motion graphic about X" and expect a premium result.
---

# Prompt Motion director

The Prompt Motion library (240+ videos made with Claude) shows one clear pattern: **one-line prompts make generic showreels; structured briefs make films.** This skill turns any request, however short, into a structured brief and then builds it as deterministic code that renders frame-exact to MP4.

Source of the patterns: https://prompt-motion.com (prompts belong to their creators; this skill keeps only the techniques, in its own words). Read `references/50-prompts-analysis.md` first: it covers 50 prompts one by one, what they share, and which technique fits which moment of an Oranuss talking-head short. `references/library-index.md` lists entries by technique.

## 0. Defaults for this user (Oranuss)

- Brand kit: `/Users/Apple/Downloads/editing-ai/brand/BRAND_CONFIG.md`. Ink `#100820`, navy `#140F2E`, purple `#5B2BE0`, neon `#8B5CF6`, lavender `#E0C4FF`, yellow `#F5C400` (rare).
- Arabic type: **Graphik Arabic** from `/Users/Apple/Downloads/editing-ai/brand/fonts/graphik-arabic/` (load with `@font-face` from the `.woff2` files; Bold 700, Black 900, Super for hero words). Latin/numbers: Graphik Arabic's Latin glyphs or one clean grotesk; never Cairo.
- Language on screen: the speaker's real Darija words.
- Keep the source video's size and aspect ratio. Never crop to 9:16 unless asked.
- The user wants **3D depth** and a "wow" reaction. Flat cards, bars and fades alone are rejected.

## 1. Expand the request into a brief (always, even for one-liners)

Write the brief in six blocks before any code (the full fill-in form is `references/brief-template.md`):

1. **Inputs**: what you need from the user (logo, product link, screenshots, track). Use a sensible default for each one so you never stall.
2. **Direction**: the look in 4–6 lines (palette with HEX, two fonts max, light or dark stage), the **signature shot** everything builds toward, and a **Banned** list.
3. **Structure**: timed beats in seconds, every beat named by what changes on screen. Something visible lands on every major beat; no dead time over ~1.5 s.
4. **Build**: how it is made: one HTML file, `seek(t)` is a pure function of time, seeded randomness, no CSS transitions or timers.
5. **Gotchas**: the known failure modes for this kind of piece (see §4).
6. **Start**: describe the signature shot and shot list in a few lines, then build without more questions.

## 2. The techniques that make it look expensive

**Camera and space**
- **One continuous world, one camera.** Lay every UI piece, card or object in a single world and move a camera through it (position + log-space zoom in 2D, or a real perspective camera in three.js). Close-ups are camera moves, not cuts.
- **Named camera moves**: dolly, crane, orbit, push-in, rack focus, rise-to-overhead, dive. One move per shot, eased in and out, and the camera never passes through geometry.
- **Depth**: perspective tilt that settles to frontal, layers floating at different heights with soft shadows, thin depth of field (sharp subject, foreground melts), parallax between layers.

**Continuity**
- **A hero object that travels**: one dot, ball, card or logo tile carries the viewer from scene to scene. It never teleports. Every transition is that object becoming the next thing.
- **Object-driven transitions**: a card becomes the next card, a chart line becomes a connector, a number becomes a UI element, a shape morphs circle → rounded square → pill. No crossfades.
- **Loopable ending** when it is a social piece: the last frame matches the first.

**Motion quality**
- **Closed-form springs** for every landing (small overshoot, then settle), stacked one per target change so any frame renders on its own. Never linear tweens.
- **Overlap**: elements never all start and stop on the same frame; stagger siblings 60–125 ms.
- **Reactions**: what gets hit moves, what is near lights up (a wave of light running along a wall of cards, each tilting as it passes).
- **Kinetic type**: per-glyph spring on y, opacity and blur; words rising 12–16 px out of a 10–12 px blur; masked vertical reveals; the outgoing word can be the mask for the incoming one.
- **Motion blur**: render 4 sub-frames per frame and average them on fast moves.
- **Beat grid**: pick a BPM (120 is a safe default), put the downbeat at t = 0, land hits on beats. With real music, measure the grid (numpy/librosa), calibrate it to the actual kick hits, put the biggest change on the drop, and start the song a few bars before the drop.
- **Shots enter already moving** (exponential ease-out) and leave on an acceleration or a blur ramp; blur follows speed and direction. Never cut on a still frame.
- **Scale journey**: micro → macro → micro (a dot → windows → zoom out until the desktop is a point in space → back into a phone). A strong spine for "big picture" lines.
- **Two-edge springs**: a pill or tab indicator whose leading and trailing edges ride different springs stretches as it moves; it reads as physical.
- **Values computed from motion**: a slider's fill and number come from the moving object's position; a graph is drawn from the same spring that moves the dot. Never animate them separately.
- **Liquid glass** (only when the brief wants it): frost and refract the scene behind the control, a top sheen, a bright rim and a soft lift shadow; give it something colourful behind, or it vanishes on plain backgrounds.
- **Words as structure**: give key spoken words a physical role (support, load, opening, platform) and let the typography build the set.
- **Screenshots broken into parts**: never show a screenshot raw; cut it into its components and icons and animate those.

**3D (three.js) look**
- Key, fill and rim lights with soft shadows; PMREM environment from `RoomEnvironment` for reflections; `MeshPhysicalMaterial` with varied roughness; ACES tone mapping; fog for depth. Never default materials or lighting.
- Real content on the 3D surfaces: video posters, screenshots or the speaker's own frames as textures.
- Signature-shot thinking: design the most memorable frame first (for example, corridors of cards resolving into a word seen from above) and make every earlier shot build toward it.

**Restraint (what the best briefs ban)**
- One shot = one idea; let scenes breathe.
- No particle spam, glows on everything, glassmorphism everywhere, pointless spinning cards, constant zooming, bouncy cartoon UI, 20 different animation styles, or paragraphs of copy.
- No AI clichés (brains, robots, neural nets) unless the subject is literally that.

## 3. Build and render

- **Standalone pieces** (explainers, launch films, showreels): one HTML file at the target size and 60 fps (30 fps is fine for talking-head b-roll), `window.seek(t)` draws the frame, a `?render` mode disables clocks. Capture with Playwright (headless Chrome) frame by frame and encode with ffmpeg (`libx264`, `yuv420p`, `-crf 16–18`). Patterns already used in this workspace: `output/oranuss-live-gif/render.mjs`, `homepage-broll/`.
- **b-roll over a talking head**: use the `talking-head-b-roll` skill's page and `render.mjs`. For a 3D cover, render three.js into an offscreen WebGL canvas (`preserveDrawingBuffer: true`), drive its camera from `s.now`/`s.audioNow`, then `ctx.drawImage(glCanvas, 0, 0, W, H)` inside the scene's `draw(t, s)`. Covers stay opaque once in; overlays stay out of `FACE`.
- **three.js locally**: `/Users/Apple/Downloads/motion-graphics-skills-main/output/khalil-stack-v1/node_modules/three` (r187; `build/three.module.js`, `examples/jsm/environments/RoomEnvironment.js`, `examples/jsm/postprocessing/*`). Use an import map pointing at those files when the page is rendered from disk, so nothing depends on a CDN.
- **Sound**: one soft SFX per element that appears and silence otherwise; master around −14 LUFS, −2 dBTP, measured again after the AAC encode.
- **Self-critique loop**: after the first render, ask "would a pro designer ship this?" If not, change the plan, not just the timing.
- **Pre-pass**: before the full render, export one still per beat or shot, look at each, and fix cramped type, orphan words, low contrast, aliasing, clipping and anything flat. Then render. Then look at a contact sheet of the finished film.

## 4. Gotchas

- Seed every random number, or the render won't match the preview.
- Set shadow bias, or surfaces get striped acne. Keep the near and far planes tight, or distant surfaces flicker.
- Use mipmaps and anisotropic filtering on textured planes, or small text shimmers as the camera moves.
- Never animate text during a fast camera move without motion blur: it smears unreadably.
- When a shape fills the screen, scale it past all four corners.
- Give outgoing and incoming text separate timing so letters do not overlap.
- Arabic text: set `direction = 'rtl'` and measure the whole line before splitting it for coloured key words; never animate Arabic letter by letter (it breaks the joining). Animate by word instead.

## 5. Deliver

Give the MP4, the HTML source, and a short shot list (time, what is on screen, the camera move). Say what you chose that the user did not ask for.
