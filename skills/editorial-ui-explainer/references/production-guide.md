# Production guide: step-by-step instructions

## 1. Pre-production (15 min)
1. Pick **one topic and 3 tips**. Each tip must be *showable* on a simple canvas (colors, layout, fonts, settings, a before/after).
2. Write the script with the SKILL.md structure (Hook → Step 1–3 → CTA), about 150 words.
3. In the script, **underline the emphasis word** of each line (italic serif) and **bold the keywords** (these trigger animations).
4. Make a "bad example" visual for the hook.

## 2. Shoot the A-roll
- Vertical 4K or 1080×1920, at eye level, framed as a medium close-up (head in the top 45 % of the frame).
- Dark background with texture (slats, shelves, plants) plus **one colored backlight** (an RGB tube or lamp aimed at the wall from above).
- Soft key light from the front, slightly to one side. Wide aperture so the background blurs.
- Record clean audio (lav or shotgun mic). Do several takes per line so you can jump-cut.

## 3. Build the board template (once, reuse forever)
Create a 1080×1920 composition or project with:
- A cream radial background, a faint grid and a vignette (see style-spec).
- Pre-made components: rounded square, card, pill bar, call-out line with dot and label, dashed grid, diamond step badge, cursor, comment sheet.
- Text styles: Sans Regular, Sans Bold, Serif Italic, Micro Caps.

### After Effects
- Shapes: shape layers (Rectangle + Roundness). Shadows: Drop Shadow effect.
- Spawns: Scale keyframes 0 → 112 → 100 with Easy Ease, or a spring expression on Scale.
- Lines: shape path + **Trim Paths** End 0 → 100. Dashes: the Stroke "Dashes" option.
- Captions: a text layer + Animator (Opacity 0, Position Y +16, Blur 8) with Range Selector **Based On: Words** and Ease High 100. Or hand-time each word on its own layer.
- Exits: Gaussian Blur 0 → 40 + Opacity, over 8–10 frames.
- Cursor: a PNG cursor with a position path; add a slight scale "press" on clicks.
- Font cycling: keyframe Source Text through several fonts (hold keyframes).

### Premiere Pro / DaVinci Resolve
- Build the board scenes in Essential Graphics / Fusion, or render them from AE as ProRes.
- Captions: auto-transcribe, then manually style the key word in the italic serif (separate text layers for mixed fonts).
- Transitions: Gaussian Blur keyframes across the cut. Split screen: crop/position the board layer to slide in from the top.

### CapCut (mobile/desktop)
- Captions: Auto Captions → split the key word into its own text layer → set the italic serif font. Use "Fade in" / "Typewriter" by word.
- Board: a cream background image + shape stickers (rounded squares) + keyframes (scale/position). Add a cursor PNG as an overlay with keyframes.
- Transitions: "Blur" and "Pull in" transitions. Split screen with a keyframed position on the overlay layer.

### Canva
- Build each board step as a page in a 1080×1920 design. Use element "Rise"/"Pop" animations and set the timing per element.
- Export as MP4 and drop into your editor over the A-roll.

## 4. Edit
1. Lay down the A-roll and cut out pauses (tight jump cuts; add one punch-in of ~110 % for variety).
2. Place each board clip where the step's demo starts. Let the voice continue over it.
3. Time **every board event to its spoken keyword** (zoom into the waveform).
4. Add the step badges ("STEP 1" plus the title) on the A-roll before each board.
5. Use blur transitions between A-roll and board. Use the split-screen slide once for variety.
6. CTA: a mock comment sheet slides up, types your keyword and taps send.

## 5. Finish
- Color grade the A-roll cool with a deep black bottom (it keeps white captions readable).
- Optional sound effects: soft clicks, whooshes and pops at a low level.
- Export 1080×1920, 30 fps, H.264, ~15–20 Mbps. Check that nothing important sits in the bottom 12 % or the right 10 % (platform UI).

## Quality checklist
- [ ] ≤ 66 s, hook in the first 2 s, CTA at the end
- [ ] Only 2 typefaces, 1 italic-serif emphasis word per caption line
- [ ] Colors follow 60-30-10, with one accent
- [ ] Only one thing moves at a time; every spawn overshoots; every exit blurs
- [ ] Every board animation lands on a spoken keyword
- [ ] One element is called back in a later step
- [ ] All assets and wording are original
