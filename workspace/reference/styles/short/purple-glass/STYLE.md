# Style: purple-glass

Energetic, bright Oranuss look: neon purple glass on navy, many icons and chips, captions with a purple box on the spoken word.

- **Best for:** tutorials, "how I do it" demos, lists of tools, high-energy hooks.
- **Videos made in this style:** IMG_2399 (16:9, `project/build.py`), 1025 v1 (9:16, `project/build_1025.py`)
- **Code:** `project/styles/purple_glass.py` (on top of `project/styles/base.py`)
- **Examples:** `examples/` (Pinterest clips and images). **Notes:** `breakdowns/`

## Colours
Brand tokens from `brand/BRAND_CONFIG.md`:

| Token | Hex | Use |
|---|---|---|
| Purple | `#5B2BE0` | caption box, solid accents |
| Neon | `#8B5CF6` | glow and bloom, progress bar |
| Lavender | `#E0C4FF` | glass rims, keywords, labels |
| Navy | `#140F2E` | glass fill |
| Ink | `#100820` | split-panel background, end card |

## Type
- Captions: Avenir Next Demi Bold, 68px.
- Titles: Avenir Next Heavy.
- Labels: Demi Bold with wide spacing.
- Serif accent (Didot italic): only in titles, never in captions.

## Captions
- 2–4 words per chunk, at most 18 characters, split at punctuation, never across a layout switch.
- The active word sits in a **solid purple box**. Keywords (skills, tech terms, French/English terms) are lavender when not active.
- Each chunk pops in from 88% to 100% in 110ms with an ease-out, over a dark halo.
- Position: 330px from the bottom in full-face shots, 90px from the bottom in the split layout.

## Layouts
- **A, full face:** slow push-ins with punch-ins on key words.
- **B, split:** the face is cropped into the top 860px and the bottom is an ink panel holding a glass card, chart, grid or folder.
- **Layout switch:** 140ms lavender flash.
- **Progress bar:** neon, along the top edge, filling over the length of the speech.

## Graphics kit
| Element | Function |
|---|---|
| Glass card: neon bloom, navy fill, top sheen, lavender rim | `glass` |
| Icon bubble: neon circle, icon, light spring | `bubble` |
| Chip: glass pill with icon and label | `chip` |
| Highlight bar that wipes in from the left | `hl_box` |
| Cursor that eases to a target and clicks, with a ripple | `cursor` |
| Sparkle stars | `sparkle` |
| Eased entrance | `enter` |

- Growth line charts reveal left to right and never overshoot.
- End card: glass folder with cards rising out, ORANUSS ACADEMY and a topic line.

## Motion
From `project/motion.py`:
- Entrances: 420ms ease-out, rising 24–60px; opacity finishes before the position settles.
- Pop: one 4% overshoot. Spring: only for decorative icons.
- Exit: 220ms ease-in shrink to 92%.
- Stagger: 70–90ms, or locked to the spoken word.

## Grade and sound
- **Grade:** light lift, `eq=contrast=1.07:saturation=1.05:gamma=0.97`, a slight purple colorbalance, and vignette PI/4.4.
- **Sound:**
  - whoosh on layout switches
  - pop on chips and icons
  - typing clicks on mockups
  - hit on keywords
  - voice chain mixed to −14 LUFS

## Don't
- Don't put serif italic in captions; that belongs to premium-serif.
- Don't blur the background plate; use the split layout instead.
- Don't copy reference logos, brand names or exact layouts.
