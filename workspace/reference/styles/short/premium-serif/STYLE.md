# Style: premium-serif

Darker and calmer, a "creator studio" look: one bold word and one italic serif word in each caption, the background blurs behind graphics, diamond badges.

- **Best for:** offers, frameworks ("6 skills", "3 steps"), authority and personal-brand reels, CTAs.
- **Videos made in this style:** 1025 v2 (`project/build_1025_v2.py`), the 1025 7s test (`project/build_7s.py`)
- **Code:** `project/styles/premium_serif.py` (on top of `project/styles/base.py`)
- **Examples:** `examples/` (study of 15 reference reels: contact sheet and per-reel frames). **Notes:** `breakdowns/premium-serif-study.md`
- Adapted from the reference style, never copied: no names, scripts or on-screen lines from the reference creator.

## Colours
Same Oranuss tokens as purple-glass (`brand/BRAND_CONFIG.md`), used more sparingly:
- Lavender: only for the serif accent word and big numbers.
- Purple: diamond fill only.
- Mostly white text on a darkened picture.

## Type and captions
Phrase captions, 1–2 lines, with these word kinds:

| Kind | Font | Size | Colour |
|---|---|---|---|
| `n` regular | Avenir Next Demi Bold | 62 | white |
| `b` heavy (one per phrase) | Avenir Next Heavy | 80 | white |
| `s` serif accent (one per phrase) | Didot italic | 84 | lavender |
| `L` big number | Avenir Next Heavy | 120 | lavender |

- Each word fades and un-blurs as it is spoken (160ms ease-out), and the whole phrase rises 18px.
- No karaoke box.
- Position: centred at y=1630, below the chin, so the captions never cover the mouth during punch-ins.

## Layout and camera
- Full-face plate the whole time; no split screen.
- Punch-ins on key words: hard cuts from 1.0 to about 1.11–1.14, then a slow ease. The crop is anchored at 0.62 so the face stays high.
- **Depth trick:** while a graphic is up, the plate blurs (sigma 26), darkens (−0.13) and slightly enlarges, with 0.24s alpha fades in and out.

## Graphics kit
| Element | Function |
|---|---|
| Floating glass card: rises 60px, drifts up slowly, can tilt ±9° | `glass` |
| Diamond badge: rounded square at 45°, with a number or icon | `diamond` |
| Pill label: glass pill with icon and spaced caps | `pill` |
| Slide-in serif or label text | `slide_text` |
| Cursor click and sparkle | `cursor`, `sparkle` (base) |

- Numbered frameworks are a row of diamonds, the active one glowing, with a "0N / 07" counter.
- Progress timeline: thin line, labelled stops, a check marker riding along it.
- End card: ink background, glass folder, ORANUSS ACADEMY, and an italic serif CTA line.

## Grade and sound
- **Grade:** moody, `eq=contrast=1.12:gamma=0.92:saturation=1.03`, purple shadows (`colorbalance rs=.03 bs=.10`), vignette PI/3.8.
- **Sound (earshot launch kit, mixed −6 to −14 dB under the voice, then −14 LUFS):**
  - snap on punch-ins
  - short whoosh when the background blurs
  - pops on cards
  - rising glockenspiel notes, one per list item
  - riser into the CTA click
  - long whoosh and a bell on the end card

## Don't
- Don't use more than one heavy and one serif word per phrase.
- Don't use bright or saturated backgrounds.
- Don't use a karaoke box.
- Don't stack more than three graphics at once.
