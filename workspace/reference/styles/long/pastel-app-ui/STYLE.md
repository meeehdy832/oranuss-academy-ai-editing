# Style: pastel-app-ui

Faceless 16:9 explainer built from mobile-app UI pieces, the look of Dribbble app shots: soft lavender canvas, white rounded cards with soft purple shadows, phone mockups, pastel tiles with big white glyphs, progress rings, bar charts, avatar stacks, pill tabs and badges. Calm, clean, "product launch" feel, with Oranuss purple as the one strong colour.

- **Best for:** voiceover-only videos (course launches, offers, "how it works"), 16:9 YouTube or 1:1 ads.
- **Videos made in this style:** AI Editing launch (`project/build_ai_editing.py`)
- **Code:** `project/styles/pastel_ui.py` (palette, `el` motion primitive, card, phone, pill, tile, avatar, ring, bar, check, skeleton, wipe, background).
- **Examples:** reference shots in `examples/` (`imgi_*.jpg`); numbered thumbnails in `project/work/ai-editing/ref/`. **Notes:** `breakdowns/reference-shots.md`

## Colours
| Token | Hex | Use |
|---|---|---|
| Canvas | `#F2EEFF` | background, plus drifting blurred lilac / sky / peach / mint blobs |
| Card | `#FFFFFF` | every card and caption pill; shadow `#6A30A0` at ~90 % transparency, blur 26, 18 px down |
| Ink | `#16122E` | titles and caption text |
| Muted | `#8A86A3` | secondary text, captions not yet spoken, "taken" states |
| Purple | `#5B2BE0` | primary: active word, active tab/step, hero bar, buttons, wipe |
| Accents | coral `#FF6B7A`, blue `#4C8DFF`, yellow `#FFC83D`, green `#2DC58A`, orange `#FF8A3D` | tiles, badges, icons (green = done/earn, yellow = important/star, coral = new/alert) |
| Tints | lilac `#E6DEFF`, sky `#DCEBFF`, peach `#FFE8D6`, mint `#DCF7E5` | thumbnails, image areas, inactive items |

## Type
Avenir Next: Heavy for titles (60–124 px), Demi Bold for labels and pills, Medium for small secondary text. Ink on white; never white text on the canvas.

## Layout (1920×1080)
- Content lives in y 70–860; the bottom band (y ~950–1050) is reserved for the caption pill.
- One focal card or phone per beat, usually left text + right phone/card, or one centred card.
- Corner radius 26–44 on cards, fully round pills; spacing on a ~30 px grid.

## Captions
Latin Darija, 2–4 words, in a white pill at y = 1000: spoken words ink, upcoming words muted, the active word purple, keywords in Heavy. Entrances lead the word by 2 frames.

## Motion
- Every element uses `el`: enter with an eased 40 px rise (or a pop for small atoms), hold, leave with its scene (eased-in slide + fade). Rotate scene exits: left / up / fade.
- Graphics land on their spoken word (`w(t)` = word time − 2 frames). Hide what is not said yet with skeleton loaders (shimmer).
- Bounded things (rings, bars, progress lines) fill with an ease-out, never overshoot.
- Section changes: purple + lilac rounded wipe panel (`wipe`). Camera: slow 2.8 % push per scene, reset on the cut; captions are a separate static layer.

## Sound
Music bed under the voice (≈ 15 dB below, sidechain ducked, rises after the last word, fades out). SFX ≤ 1 per second: soft whoosh on scene changes, pop on badges, tick on checks, bell on wins, click on buttons. −14 LUFS.

## Don't
- No dark backgrounds or neon glow (that's purple-glass).
- No invented numbers: charts have no axis values, rings show completion only.
- No more than one saturated colour per card besides purple.
