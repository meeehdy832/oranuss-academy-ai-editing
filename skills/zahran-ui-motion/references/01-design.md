# Design system of the references

## 1. Formats and safe areas

| Format | Seen in | How the refs use it |
|---|---|---|
| 1:1 (720/1080 square) | 17 of 24 | content centered; hero element 30–55% of width; copy above or below on the vertical axis |
| 9:16 with a content band | v03, v04, v20 | a 1:1 or 16:9 **content band** in the middle; the top/bottom areas are a **blurred, enlarged copy of the live band** (ambient fill, blur 40–80 px, brightness −5%), so the whole frame changes color with the scene; handle/credit small under the band |
| 16:9 | v02, v09, v22 | split layouts (visual left 50%, copy right), or wide UI (chat input, website) |

Safe area: keep text 8% inside every edge (12% top/bottom for 9:16 reels because of the UI overlay).

## 2. Composition and alignment rules

1. **One hero at a time.** Each beat has one focal object (a pill, a card, a phone, a word) at
   **optical center** (≈ 2–4% above geometric center). Secondary items are smaller, lower contrast, or blurred.
2. **Center axis.** 80% of the layouts are symmetric around the vertical center line: headline above, object
   below, or the object with flanking words left/right (v04 "take [phone] screenshot").
3. **Vertical stacks** use a consistent rhythm: headline → 16–24 px → subline → 40–64 px → object (at 720p).
   Spacing between groups is ≥ 2× the spacing inside a group (Gestalt proximity).
4. **Split screen** (16:9): media fills one half, copy is left-aligned in the other half, vertically
   centered, with a margin equal to the gutter.
5. **Inline objects in sentences**: icons, avatars, chips and media sit **inside** the line of text at
   cap-height size (or 1.2× x-height), with word spacing on both sides: "Bank [icon] slowing",
   "Lost your [avatars] again?", "how to find this [Figma] files?", "One [pill] text away". The
   sentence reflows (spring) to make room.
6. **Fans and arcs** for collections: cards fanned at −8°/0°/+8° (v19), devices on an arc with the
   center one biggest (v17), coins on a wheel arc (v12), apps on a diagonal track (v16).
7. **Deck / stack** for sequences: the new card lands on top, the previous one slides back, scales to
   0.92 and shifts 30–60 px (v09 widgets, v06 carousel ghosts).
8. **Diagonals** add energy: staircase of cards (v21), diagonal app track (v16), ribbon swoosh (v06).
9. **Crop to imply scale**: phones rising from the bottom edge, cropped (v21, v16, v08 MacBook);
   giant wordmarks cropped by the frame (v04 "Pool").
10. **Grid fidelity** when showing real UI: real 8-pt spacing, real iOS/macOS component sizes. Credibility
    comes from accuracy.

## 3. Typography

| Use | Typeface (available in @remotion/google-fonts) | Weight | Size @1080 | Tracking |
|---|---|---|---|---|
| Apple-like UI + headlines | **Inter** / **Inter Tight** (SF Pro stand-in) | 500–700 headlines, 400–500 UI | headline 64–110, UI 28–40 | −2% to −4% on headlines |
| Wide modern grotesk (tech/AI brands, v08) | **Hanken Grotesk** / **Manrope** / **Geist** | 500–600 | 60–90 | −2% |
| Editorial serif (books, premium, v04, v24) | **Instrument Serif** / **Newsreader** | 400–600 | 70–120 | −1% to −2% |
| Small sign-off / captions | Inter | 400–500 | 24–34 | 0 |

Rules:
- Short copy: **2–6 words per line, max 2 lines on screen.** Questions as hooks ("Need inspo?",
  "Lost your friends again?", "wait… what is this song?").
- Lowercase is common for the casual voice; Title case for brand names only.
- **Emphasis by one property only**: color (accent word), weight (bold word), or a pill highlight
  (white box + black text inside white copy, v07). Never all three.
- **Typography carries meaning**: "softer" in light gray, "deeper" in bold black (v02); serif for books;
  a scramble for "AI".
- Small copy is fine. The references often use small, calm type (20–34 px @1080) for statements, which
  looks premium and confident. Reserve big type for the hook and the brand.
- The accent-to-ink settle: new words appear in the accent color and fade to the ink color within 6–10 f (v06, v08, v09).

## 4. Color

Measured from pixels (k-means per video): **the background covers 50–85% of the frame and is neutral in
19 of 24 videos.** One accent hue covers 5–15%. Blue is the accent in 14 of 24.

Palette recipes:
| Name | bg | ink | surface | accent | refs |
|---|---|---|---|---|---|
| Apple light | #FFFFFF / #F5F5F7 / #EFEFEF | #111111 | #FFFFFF + soft shadow, #EBEBEB pills | iOS blue #0A84FF / #4A90F0 | v01 v05 v06 v12 v14 v15 |
| System gray | #E5E5EA | #1C1C1E | white cards, #2C2C2E dark pill | #4A63E7 | v15 |
| Pale tint | #EEF3FB (blue-white) / #F7F8FE | #0B1B2B navy | white | #2D5BD7 | v03 v08 |
| Sky | photo sky or gradient #2F7BF5 → #8EC1FF | white | frosted glass | white highlight | v07 v16 v18 v24 |
| Dark premium | #050407 → #0A1A2E bottom glow | #FFFFFF | #1C1C1E glass | brand glow (violet/blue) | v17 v21 v23 v02 |
| Brand-flood | the brand color full-frame (PayPal #0B2A97, Pinterest #E60023) | white | — | white | v10 v19 |
| Warm editorial | #FFFBF3 cream | #01030A | — | none or tiny blue UI hints | v22 |
| Health green | #EDEEEB + #3F9479 | #131417 | #1E1F1F widgets | mint #3FD39A | v09 |

Rules:
- **One accent per video.** It marks interaction (selection, caret, buttons, links) and the key word.
  Everything else is neutral.
- Scene color shifts tell the story without cuts: ambient bands (9:16) and background tints change per
  scene (white → pale blue → mint → warm), as in v03 and v20.
- Light/dark act switches mark chapters (v02 black→white, v13 light→dark→white/black flashes, v17 dark →
  white logo). The final brand frame is often the brightest or the darkest frame of the video.
- Glows: dark scenes use **one** colored light source (a radial gradient 30–60% of the frame, low
  opacity, slowly moving). Light scenes use soft colored blobs at the edges (orange/blue/green light leaks, v20).
- Pastels for collections: same lightness, different hues (widget grid v05, initials avatars v06).
- Shadows on light: large and soft (`0 30px 60px -20px rgba(0,0,0,.18), 0 12px 24px -12px rgba(0,0,0,.10)`).
  Raised/active items get a deeper shadow (v06 "Your friends" row).

## 5. Component recipes (sizes @1080 square)

- **Pill / search bar**: height 84–110, radius = h/2, fill #EEEEEE (on white) or white with a soft shadow
  (on gray), 1px inner light border for glass; icon 32–40 + label 32–36 Inter 500.
- **Safari-style toolbar** (v01, v05): back chevron circle | field (tabs icon + "type…" + reload) | ···
  circle, all gray pills; a rainbow underline (blue→green→yellow) for "AI".
- **Widget card**: radius 22–28% of the shorter side (squircle), dark #1E1F1F or pastel fill with a 2px border
  of the same hue at −10% lightness; big number 90–140 px, small label 26–30, unit in gray.
- **Folder label above a card** (v01, v09): macOS folder icon + filename, 28 px, 16 px above the card.
- **Chat bubbles** (v20): sent #3C8CF5 white text, received #E9E9EB black text, radius 36, tail, name
  label 22 px gray above, avatar 56 px.
- **Notification**: glass #F2F2F7 at 85% (light) or #1C1C1E at 80% (dark), radius 36, app icon 64, title
  600 + body 400, "now" right-aligned gray.
- **Avatar pin**: circle photo/memoji 90–120, 6 px white or colored ring, small badge (flag, check) at
  the bottom-right.
- **Glass (liquid glass)**: white 12–20% fill, backdrop blur 30–40 px, 1.5 px top highlight border, inner
  soft white gradient top→transparent.
- **Device**: real iPhone frame (titanium/black), Dynamic Island, 9:41 status bar; on white, show a black
  phone; on black, a titanium phone with a rim light.

## 6. How each design expresses its message (idea ⇄ visual)

The strongest references make the **visual a literal metaphor of the copy**:
- "Pool" app → pool-water caustics + rubber ducks (v04).
- "Find anything" → a fan of many phones (abundance) (v17).
- "organize it" → scattered thumbnails snap into a tidy grid (v19).
- "send money anywhere" → camera travels along a dashed route across a world map (v10).
- "Lost your friends?" → the cursor erases the word "friends" and the friends' avatars take its place (v18).
- "Plan smarter" → calendar → notification → maps → navigation (the plan unfolds) (v13).
- "AI search" → rainbow line becomes the caret; the answer is real files (v01).
- "There's more to this city" → look out of the airplane window, then push through it into the city (v07).
- "Customize" → the slider moves while the word swaps softer/deeper/personal (v02).
- "When did you last read?" → a serif typeface, book-page text texture, a cover flying out of the phone (v24).
Before designing any beat, write the copy line and pick the one object that **shows** it.
