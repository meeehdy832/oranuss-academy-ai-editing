---
name: oranuss-visual-system
description: The Oranuss Academy look - colour tokens, fonts, glass cards, neon glow, highlight boxes, end card - with exact ASS/ffmpeg recipes. Use for any Oranuss video graphic so every reel looks like one brand.
---

# Oranuss visual system

Developed by Mehdi ORANUSS | Powered by Claude

The brand name is spelled **Oranuss** ("ORANUSS ACADEMY", "Hamza Oranuss"). Never write Ouranos or Uranus.

## Tokens (ASS colour = &H00BBGGRR&)
| Token | Hex | ASS | Use |
|---|---|---|---|
| purple | `#5B2BE0` | `&H00E02B5B&` | caption highlight box, solid accents, number circles |
| neon | `#8B5CF6` | `&H00F65C8B&` | glow/bloom, progress bar, flashes |
| lavender | `#E0C4FF` | `&H00FFC4E0&` | glass rims, small labels, secondary text |
| navy | `#140F2E` | `&H002E0F14&` | glass fill (alpha `&H30&`–`&H38&`) |
| ink | `#100820` | `&H00200810&` | full-screen backgrounds, end card |
| yellow | `#F5C400` | `&H0000C4F5&` | rare accent only (office wall yellow) |

All values are provisional until the user supplies official brand codes; update `brand/BRAND_CONFIG.md` when they do.

## Type
- Heavy titles: **Avenir Next Heavy** (uppercase, letter-spacing 1).
- Captions and step text: **Avenir Next Demi Bold** (upright; a "Bold=-1" Avenir style gives italic, so avoid it).
- Small labels: Avenir Next Regular, lavender, letter-spacing 4–8 (e.g. `MO9ADDIMA`, `STEPS 1/4`).
- Accent word (the equivalent of the reference's italic serif): lavender italic, or white text in a purple highlight box.

## Components (reference implementation: `project/styles/base.py` + `project/styles/purple_glass.py`; per-style recipes in `reference/styles/<long|short>/<style>/STYLE.md`)
- **Glass card:** neon bloom (`\blur22`, alpha `&H70&`), then navy fill (alpha `&H38&`), then a white top sheen (alpha `&HEC&`), then a 2px lavender rim. Rounded corners (r = 22–34). Entrance: `\fscx92→100` in 260ms with fade.
- **Callout:** a glass card with a small light line above a big heavy line, sliding 24px in from its side.
- **Chip:** a glass pill with a purple icon circle and a heavy label, sliding in from the side with overshoot.
- **Icon bubble:** a glass circle with a white vector icon (100×100 box, pinned with an anchor so `\an5` centres it); bounces 0→115→100%, floats up 14px, shrinks out.
- **Sparkle burst:** 6 four-point stars, scale 0→size→0 with 90° rotation over 750ms.
- **Caption highlight:** BorderStyle 3 box in purple behind the active word only (`\3a&H00&` on that word, `&HFF&` elsewhere), plus a soft dark halo layer underneath.
- **Transitions:** neon flash (purple full-frame alpha ramp plus a blurred lavender circle) on big cuts; a 0.15s lavender flash on small trims.
- **Intro:** the first ~3s blurred (`gblur=28`) and darkened under a glass title card, then sharp again.
- **End card:** ink background, purple radial bloom, glowing glass folder with cards, "ORANUSS ACADEMY" heavy with glow, "PERSONAL BRANDING" (or the topic) in small spaced lavender.
- **Progress bar:** 8px neon line along the bottom edge that fills over the video's duration.

## Grade
HDR iPhone → SDR (zscale + tonemap mobius); `eq contrast 1.09, sat 1.06, gamma 0.96`; shadows tinted purple (`colorbalance bs=0.06 rs=0.03`); vignette PI/4.2.

## Safe areas
- 16:9: the face is usually in the centre third; put cards in the corners (y 70–230) or at mid-height on the sides (x < 400 or x > 1500); captions at the bottom (MarginV 80).
- 9:16 (1080×1920): captions 250–420px above the bottom (clear of platform UI); nothing in the top 180px or the right 140px (platform buttons).

## Motion language (motion-dynamics skill, implemented in `project/motion.py`)
Every animation picks a curve per property; never use one curve for everything.
- **Enter (cards, titles):** 420 ms. Position travels 24–60 px on an out-cubic curve, built from piecewise `\move` keys with `eased_moves()` because `\move` is linear. Opacity finishes in the first ~30% of the move, then the position settles. No overshoot on premium cards.
- **Pop (chips, badges, buttons):** `pop()`, scale 0 → 104% (ease-out, 220 ms) → 100% (140 ms). One 4% overshoot only.
- **Spring (icons, sparkles only):** `spring()`, 0 → 112 → 96 → 100%. Decorative elements only, never text blocks.
- **Press (button click):** `press()`, 100 → 93 → 100% in 180 ms, plus a ripple ring that expands on an ease-out and fades.
- **Exit:** 220 ms ease-in fade plus a shrink to 92% (`exit_()`).
- **Cursor travel:** ease in-out over 500 ms (`in_out_cubic`), then the press.
- **Bounded values** (charts, progress bar): linear or ease-out clip wipes (`wipe_lr()`). Never overshoot, never invent numbers. A dot riding a chart line uses the same linear progress as the line's wipe.
- **Stagger:** lock each item to its spoken word; otherwise use 70–90 ms in reading order.
- **ASS mapping:** `\t(t1,t2,accel,…)` gives progress^accel, so accel 0.4 is an ease-out and 2.2 an ease-in.
- **Camera zoom keys:** hold segments ease with smoothstep; hard punches use two keys 1 ms apart, on layout or idea switches only.
- **Flashes:** at most one 140 ms lavender flash per layout switch; no flicker faster than 3 per second.
