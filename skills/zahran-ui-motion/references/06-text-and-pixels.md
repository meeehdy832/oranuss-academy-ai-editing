# Text motion and pixel effects: the full menu (2nd study pass, frame by frame)

Why this file exists: the first demo used one text style everywhere (rise + blur) and a full-screen
pixel dissolve. Yahia's note: the references vary text and element motion a lot, and their pixels are
FEW, LOCAL, and mostly tied to a word appearing. This file is the result of re-reading every text
appearance in the 24 videos frame by frame.

## The variety rule

- **Never use the same text technique twice in a row.** A 15 s video uses 4–6 different ones.
- Pick the technique from the **meaning** of the line (table "use when") and from the energy of the
  moment (calm statement vs hook vs result).
- Vary the **unit** too: whole line, word by word, letter by letter, one key word only.
- Vary **how the old text leaves**: blur-up exit, swallowed by an object, selected and replaced,
  swapped word by word, wiped, smeared off, hard cut.
- One accent color moment per line at most (the key word), and it settles to ink unless it is the point.

## Text entrances (what the refs do)

| # | Technique | Refs (frames) | Look, measured | Use when | Kit |
|---|---|---|---|---|---|
| 1 | **Blur-in, no rise** | v18 0–16, v21 119–140, v23 8–28, v11 10–30, v07 0–48 | word by word every 4–6 f; translucent/gray → ink over ~10 f; blur 12–16 → 0; the LINE drifts with the camera, words don't move | calm statements, questions, premium; the camera carries the motion | `BlurIn` (`from`, `exitAt`, `unit="letter"`) |
| 2 | **Rise + tilt** | v06 0–24 "Ready to level up" | from below-left, rotated ~-10°, heavy blur 18 → 0, accent → ink, each word 6 f apart | energetic hooks, onboarding, "level up" | `RiseTilt` |
| 3 | **Liquid blob → word** | v04 4–18 "Have you ever" | a blue blob (+ a droplet) flies in, stretches horizontally into the word's shape, dissolves into the blurred word which sharpens; serif | soft, curious, organic brands | `BlobToWord` |
| 4 | **Random-letter reveal** | v09 16–30 "collecting", 404–452 "making" | letters pop in random order over ~12 f, accent color, then darken | "decoding", data, AI | `RandomReveal` |
| 5 | **Scramble / decode** | v12 6–15 "Bank" (Bbqr → Banl → Bank), v08 262–296 "for free" (+ a 2nd scramble pass to stay alive) | glyph noise resolving left → right, accent while scrambling | tech, CTAs, money, AI | `Scramble` (keep it short: dur 7–8, stagger ≤ 0.4) |
| 6 | **Typewriter + caret** | v17 0–14 "wait…", v24 2–30 serif, v21 10–68, v05 60–108 | 1–2 chars/f in UI fields, word-by-word for statements; caret bar or block | prompts, search, chat, "someone is talking" | `TypeLine`, `TypeField` |
| 7 | **Converge (scattered → line)** | v22 0–24 "Go from an idea" (+ code glyphs), v09 575–600 "All your health data" | words start at different heights/offsets (±1 em), land in random order, accent → ink; glyphs "/ 0 1 +" drift in and vanish | building, assembling, "ideas → product", data coming together | `Converge` (`glyphs`) |
| 8 | **Emerge from behind the hero** | v08 30–48 "Ready to create" | words slide outward from behind the mascot with horizontal motion blur; "to" appears last in accent | the product "produces" the message | `Emerge` + draw the hero on top |
| 9 | **Object wipe** | v20 440–510 (mascot wipes "Meet Maverick" in/out) | a soft-edged mask follows a moving object; words slide 20 px as they're uncovered | mascots, cursors, comets revealing copy | `WipeReveal` + `wipeEdge()` for the object x |
| 10 | **Select → replace** | v03 50–84 "Stop Scrolling." → "Start Showing up.", v05 100–124 query → "Use Concerta.", v10 112–117 | a solid accent block sweeps over the old text (text turns white on it), collapses into a block caret, the new line types behind it; the block can end as the period | contrast / "instead of" / a better answer | `SelectReplace`; or let the block become the next object (ProDemo: block → input bar) |
| 11 | **Word wave** | v15 90–108 song title | words pop with alternating vertical offsets and a springy bounce | results, music, playful UI | `WordWave` |
| 12 | **Drop-in + underline** | v11 204–240 "it'll work, trust" | words drop from above, big → normal with overshoot, slight rotation; the key word bold accent, underline draws | promises, emphasis, "trust" | `DropIn` + `UnderlineDraw` |
| 13 | **Swap line word by word** | v18 178–194 "find everyone" → "with find my" | old words leave up (blur) one by one, new words rise in with varied offsets, overlapping | a sentence that changes meaning | `SwapLine` |
| 14 | **Word swap with dust** | v02 280–316 softer → deeper → personal | only the last word changes; the old one dissolves into tiny square dust; weight/color change with meaning | adjectives, options, "more X" | `WordSwap` + `PixelDust` |
| 15 | **Smear in / out** | v09 639 "together", v11 55–59 wordmark exit | 2–4 f of extreme horizontal stretch (scaleX 1.3–1.8) + directional blur | fast hand-offs, punctuation | `Smear` |
| 16 | **Tracking collapse** | v06 131–155 "Choose Your Gender" | letter-spacing and size settle while blur clears | titles, onboarding headers | `TrackIn` |
| 17 | **Hard typographic cuts** | v13 186–226 "Calendar / Plan / Plan Smarter.", v19 0–4 "inspo?" flicker | 1 card per beat, black ↔ white, 1 f inverted flicker frames, slow push on each card | brand lockups, beat-driven outros | `CutSequence` |
| 18 | **Camera-zoomed typing → pull-back** | v01 148–196, v22 160–215 | the camera is pushed in on the caret, then pulls back to reveal the full sentence (often with an inline chip) | long questions, prompts | `TypeLine` + `CameraRig` moves |
| 19 | **Inline object in the sentence** | v12 6–30 (icon chips), v18 26–42 (avatars replace "friends"), v22 19–28 (media slot opens) | the sentence splits to make room; the object pops in | concrete examples, "this, not that" | `InlineSlot`, `Pixelate` for media |
| 20 | **Sweep-eat** | v23 31–46 | a comet becomes an orb and swallows the words right → left (they compress + blur into it) | ending a question, "AI takes it from here", pre-logo | `Comet` + per-word suck (build it with `Comet` + per-word scale/blur toward the orb) |
| 21 | **Guide marks** | v09 404–452 "sense" | crosshairs "+" and thin guide lines draw around the key word | precision, design, "makes sense" | `GuideMarks` |
| 22 | **Lyric per beat** | v17 64–145 | one word per beat on a screen | music | `WordSwap` |
| 23 | **Odometer / slot roll** | v16 40–60, v12 222–262, v20 900–950 | digits roll per column; options roll vertically with faded neighbors | numbers, "works with everything" | `Odometer`, `SlotRoll` |

## Pixel effects (measured)

| Effect | Refs | Measured | Use | Kit |
|---|---|---|---|---|
| **Pixel sparkle around a word** | v11 1–12 "meet" | f0: 4 cells, translucent (~30%) + 2 px blur. f1: the same cells saturated. f2–5: 7–9 cells, new ones spawn as **grid neighbours** (pairs, L shapes), each lives 2–4 f, colours = accent family at 100/60/35% opacity. f6–9: fewer, lighter, drifting outward ~25 px. f10–12: 1–2 ghosts. Cell ≈ 4.3% of frame width (≈ 0.5× the font size). Cells NEVER cover the text. | the hook word, a key word landing, a brand word | `PixelSparkle` (`avoid` = every text line) |
| **Pixelated media reveal** | v22 19–28 | the inline slot shows a coarse mosaic (≈ 5×2 cells) for 2 f, then a finer one, then the image with ~15 stray light pixels for 3–4 f | inline video/photo appearing, "loading" content | `Pixelate` |
| **Pixels burst + orbit** | v08 0–22 | 8–10 black squares (2–3 sizes) burst out of the mascot in ~6 f, then orbit slowly in a ring | a hero/mascot/logo coming alive | `PixelOrbit` |
| **Pixel dust** | v02 280–290 | tiny 2–5 px squares puff off a word that dissolves | word swaps, deleting | `PixelDust` |
| **Cell-by-cell reveal** | (kit variant of v09/v11, used sparingly) | cells switch on with a left → right bias + randomness; ~30% flash the accent for 2 f first | revealing a wordmark or a small UI piece | `PixelReveal` (`flashRatio` 0.25–0.4) |
| **Floating square particles** | v07 210–280 (white squares on blue), v17 (album squares rising) | 5–15 small squares drifting, low opacity | ambience on flat colour backgrounds | `Particles shape="square"` |
| **Full-screen pixel dissolve** | v09 456–472 only (1 of 24 videos) | cells flood the frame in 4 f, mosaic, clear in ~11 f | rare: one act break in a long video, never as a default transition | `PixelDissolve` |

## Options per step (pick a different one each time)

- **Hook (0–2 s):** blur-in + pixel sparkle on the key word · rise + tilt · impact frame + one word · glyph converge · blob → word · scramble.
- **Old text leaves:** blur-up exit (accelerating, stagger 1–2 f) · selected and replaced · swallowed by an orb · swapped word by word · wiped by an object · smear off · hard cut on a beat · shrinks into a UI element (text → bubble, v07).
- **Text → UI:** the selection block becomes the input bar · the sentence shrinks into a bubble (v07) · a word is erased and objects pop into the gap (v18) · a sliver becomes a word (v01).
- **Typing beats:** bar grows while it types (`TypeField`) · camera zoomed on the caret then pull-back · word-by-word typing for statements.
- **Numbers:** odometer roll · count with accent while moving · slot roll for options.
- **Scene change:** morph (default) · fill becomes the world (a progress fill/button grows to the full frame, ProDemo 234–254) · orb iris (an object grows into the next background, ProDemo 302–336) · whip · portal into a screen/window · soft wipe with a persistent object · hard cut on motion.
- **Pre-logo:** sweep-eat · glitch flash 3–7 f · strobe on beats · vignette to black.
- **Logo:** ring/shape draws + accent dot · wordmark cell reveal · letters assemble from blobs (v03) · brush-stroke draw (v19) · tagline swap ("plan less." → "live more.").
