# Effects and transitions: what, when, how

Each entry: what it looks like (refs), when to use it, and the build recipe. Kit component names
refer to `kit/motion-pro` (see SKILL.md).

## Transitions (scene → scene)

**Pro standard (07-pro-standard.md):** default to match cut on motion, collapse → emerge, zoom-through, or a morph whose
new content appears while it grows, with 3–8 f of overlap. Flashes (white / brand / strobe / glitch), irises to a flat
colour, fade to black and hard cuts on still frames spike the energy metric (> 15) and read as amateur in the author's review:
use them only when a brief explicitly asks for a beat-driven, glitchy edit, and never more than 1–2 frames.

| Transition | Looks like | Use when | Frames | Kit |
|---|---|---|---|---|
| **Morph** | one container changes shape/color/content | default between UI states; the most-used "transition" | 6–14 | `MorphBox` |
| **Hard cut on motion** | cut exactly on the velocity peak of an accelerating exit | music beat, keeping energy | 0 | timeline: place the cut on the exit's last frame |
| **Zoom-through / portal** | camera pushes into a window/screen/orb and its content becomes the next scene (v07, v13, v14, v23) | entering a product, "look inside" | 12–18 | `CameraRig` push + scale the window up (build it per reel; no ready component) |
| **Reverse portal** | the whole scene shrinks into a card, widget, icon or screen (v10, v18, v07) | scene → product component; outro to logo | 8–14 | `ShrinkToCard` |
| **Whip pan** | camera slides fast with heavy horizontal blur (v07, v09, v10, v21) | next item in a sequence; reveal off-screen UI | ~6 visible inside an 18–26 f MOVE | `whipKeys` in `CameraRig` + auto blur |
| **Pixel dissolve (full screen)** | square cells (≈1.4% of width, 2 px gaps, accent-tinted) flood the frame randomly in 4 f, form a mosaic, then disappear randomly revealing the next scene; a few stray cells linger as dots (v09) | **RARE: 1 of 24 videos.** One act break in a long video at most. The refs' usual pixels are LOCAL and few, around a word: see `06-text-and-pixels.md` | ~16 | `PixelDissolve` |
| **Fill becomes the world** | a progress fill / button / selection grows (exit curve, accelerating) until it covers the frame; the next scene starts on that same color and darkens/lightens while its first words are already arriving (ProDemo 234–258) | stats → statement, "it's done" moments, color-world change | 16–20 | geometry lerp + `CameraRig` exit move |
| **Orb iris** | a small glowing object (orb, dot, avatar) travels to the center and grows into the next background (ProDemo 320–336) | dark → light, pre-logo | 14–18 | circle radius with EASE_PRO.exit |
| **Ribbon swoosh** | a thick black (or ink-color) zig-zag stroke with heavy motion blur sweeps diagonally across the whole frame, covering then uncovering (v06) | energy peak; switching from intro to product; once per video | 10–14 | `RibbonSwoosh` |
| **Glitch flash** | 3–7 frames alternating RGB static, white, black, brand color, flare (v13 opening, v14 before logo, v19 opening) | hook (first 4 f) or right before the logo | 3–7 | `GlitchFlash` |
| **Brand-color flash** | 1 frame full brand color then 1 dark frame (v19) | the first frame of a brand video | 2 | `Flash` |
| **White/black flash** | 1 frame white (scene ghosted) (v17) | punctuation at act changes, on a beat | 1–2 | `Flash` |
| **Strobe invert** | 1–2 f black↔white inversions with a blue glow (v10) | beat hits in music-driven edits | 2–4 | `Strobe` |
| **Soft wipe** | wide soft-edged gradient wipe (v04), with a persistent object staying on top through it | world change while keeping a hero object | 8–12 | `SoftWipe` |
| **Stripe wipe** | horizontal bands slide with a center-out stagger | bold color flips | 7–9 | build per reel: N `Move`d bands, 1–2 f stagger (no ready component) |
| **Letterbox** | black cinema bars slide in from top/bottom (v13) | cinematic emphasis on one key UI moment | 6 in / 6 out | build per reel: two black bars with `EASE_PRO` enter/exit (no ready component) |
| **Vignette to black** | edges darken first, then the whole frame, while the camera pushes (v01) | outro into a dark end card | 8–10 | `VignetteOut` |
| **Liquid ripple** | the background liquefies (displacement) and resolves into the next scene (v12, v18) | water/flow/brand ripple, sky → map | 8–12 | `LiquidRipple` |
| **Light sweep / comet** | a light streak travels and eats the sentence into an icon (v23) | text → symbol, a hook into the product | 12–16 | `Comet` |
| **Blur cross-dissolve** | old scene blurs out (12–20 px) while the new one focus-pulls in | soft transitions in calm sections | 6–10 | `BlurSwap` |
| **Implode / explode** | particles sucked into a hero (v08) or tiles exploding out of an inline image (v09) | gather → reveal, or one → many | 6–12 | `Particles` + keys |

## Text effects

(The full list with frame numbers, the variety rule and the pixel effects are in `06-text-and-pixels.md`.)

| Effect | Refs | Use | Kit |
|---|---|---|---|
| Typewriter + caret (bar or block), container grows | v01 v05 v14 v20 v21 v23 | search/prompt/AI conversations | `TypeLine` |
| Word rise with **accent→ink settle** | v06 v08 v09 v11 | hooks and statements | `WordRise` |
| Random-order letter reveal | v09 "c_ll_c_ing" | "decoding", data, AI | `RandomReveal` |
| Scramble / decoder | v08 "for free" | CTA, AI, tech | `Scramble` |
| Odometer roll per character | v12 currency, v16 time, v02 clock | numbers changing value | `Odometer` |
| Slot roll / picker (masked neighbors) | v01 app chip, v12 Pay→Earn→Wallet, v20 iMessage→WhatsApp | lists of options, "works with everything" | `SlotRoll` |
| Word swap with particle dissolve | v02 softer/deeper/personal | one changing word in a fixed sentence | `WordSwap` |
| Highlight pill behind a word | v07 "more" | emphasis in white copy on color | `HighlightWord` |
| Underline draw | v05 swoosh, v11 "trust" | brand/keyword | `UnderlineDraw` |
| Swipe-erase word → objects | v18 | the hero metaphor: words become things | cursor keys + `WordRise` + pop |
| Inline media/object in a sentence | v09 v12 v18 v22 | concrete examples inside copy | `InlineSlot` |
| Lyric-per-beat on a screen | v17 | music products | `WordSwap` |
| Ghost background type (huge, 5–8% opacity) | v08 | texture behind a mascot/hero | plain text |
| Zoom-out while typing | v22 | a typed statement with camera energy | `TypeLine` + `CameraRig` |

## Looks / overlays

| Look | Refs | When | How |
|---|---|---|---|
| **Motion blur** (directional, velocity-driven) | everywhere | every fast move | `MotionBlur` (real shutter blur); `CameraRig` blurs the whole layer from camera velocity |
| **Focus-pull entrance** (blur→sharp) | everywhere | every entrance | keys: blur 12–20 → 0 by 60–70% of the move |
| **Echo / trail** | v11, zoom-throughs | super-fast zoom or smear | `MotionBlur` with a 14-sample boost (no separate echo component) |
| **Smear frame** | v11 wordmark exit | 2–3 f exits at extreme speed | scaleX 1.3–1.8 + blur on the peak frames |
| **Impact frame** | v11 frame 0 (radial echo of the word in magenta) | the first frame of the hook | `ImpactFrame` |
| **Camera shake** | v08 launch, v10 map | impact moments only | `CameraRig shake` |
| **Depth of field** | v01 zoomed typing, v04 floating icons, v17 album squares | push-ins; floating props | `DepthBlur` edge mask; props: closer = bigger + blurrier |
| **Bokeh particles** | v17 album squares rising, v21 colored dots ring, v07 snow dots | keep slow scenes alive | `Particles` |
| **Glow / light source** | v02 magenta arc, v17 blue ribbon, v21 Siri ring | dark scenes, AI presence | `Glow` |
| **Light leaks / color blobs** | v20 orange/blue/green edges | light scenes with ambient color | `Glow` (large, low alpha) |
| **Mesh gradient bg** | v11 (pink/peach/lilac) | brand-color backgrounds | `MeshBg` |
| **Dot grid / crosshair guides** | v18 dot grid, v09 crosshair "+" | technical, "map" texture | `DotGrid` |
| **Ambient band fill (9:16)** | v03 v04 v20 | vertical delivery of square/wide content | `AmbientFrame` |
| **Bloom end card** | dnyxstudios on black: white text with a soft glow, scale 1.05→0.95 over 1.5 s | studio sign-off | `EndCard` |
| **CRT static / scanlines** | v13 frames 0–2 | glitch hooks | `GlitchFlash` |

## Particle-like supporting motion

- **Orbit**: avatars/satellites on an ellipse around the hero, 1 revolution per 4–8 s, with depth
  (behind = smaller and blurrier) (v08, v18).
- **Float**: props bob ±6–12 px with 2–4 s periods, phase-offset per item (v04 icons, v19 cards, v01 dot).
- **Rise**: small squares drifting upward like embers (v17).
- **Converge / scatter**: glyphs or tiles fly into formation (v22, v19 "organize it") or apart (v18).
