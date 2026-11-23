# Style: dark-green

The premium-serif layout in a deep emerald and mint palette: calm, expensive, "money / business" feel. Made for footage with green in the set (green sofa, plants).

- **Best for:** business, e-commerce and money topics; checklists ("you need these 9 skills"); win or lose questions.
- **Videos made in this style:** 650 (`project/build_650.py`)
- **Code:** `project/styles/dark_green.py`. It reuses `premium_serif.py` for captions, glass, diamonds and pills, and switches them to green with `apply_palette()`.
- **Examples:** `examples/` (empty so far; drop green references here). **Notes:** `breakdowns/`

## Colours
| Token | Hex | Use |
|---|---|---|
| Emerald | `#0E9F6E` | diamond fill, done ticks, icon discs |
| Glow | `#2EE59D` | bloom, panel rim, flashes |
| Mint | `#A7F3D0` | serif accent words, rims, labels |
| Forest | `#0A2A1F` | glass fill, frosted panel tint |
| Ink | `#05140F` | end card |
| Red | `#F87171` | only for "loss" or "no" (TKHSER, ✗) |

## Captions
Same as premium-serif: one heavy word and one mint italic-serif word per phrase; each word fades in ~2 frames before it is spoken (`LEAD 0.067`); the phrase rises 18px. Captions may not overlap (checked at build time).

## Placement for social media
Instagram Reels, TikTok and YouTube Shorts cover the edges of the frame:
- **Top:** keep text below y = 250 (status bar and "Reels" header).
- **Bottom:** keep text above y = 1480 (caption, username, music line).
- **Right:** keep text left of x = 940 (like, comment, share column).
- **Captions:** centred at y = 1290, below the chin and above the platform caption.

The zoom is anchored on the tracked face (`anchor_y` = face centre y / 1920) so punch-ins don't push the face out of frame. Faces are tracked with macOS Vision: `project/work/<video>/faces.swift`.

## Signature pieces
| Element | Function |
|---|---|
| Frosted lower panel: blurred, darkened band of the plate with a forest tint and glow rim. Also hides text burned into the source. | `frost_panel` + `frost_win` in `filter_graph` |
| Checklist tracker at the top: title, `0N / 09` counter, diamond ticks that fill emerald as each item is spoken, all flashing together on the recap word | `tracker` |
| Result cards (TRBE7 ↑ emerald / TKHSER ↓ red) | `flag` |
| Topic word **behind the head** (hero beat, Vision cut-out) | `filter_graph(behind_ass=…, roto_win=…)` |
| Zoom-blur whip on hard cuts (pair with a zoom spike in ZK) | `filter_graph(whips=[…])` |
| Diamond badges with serif labels; side glass cards next to the face | `premium_serif.diamond`; `card` in the build script |

## Grade and sound
- **Grade:** `eq=contrast=1.10:gamma=0.94:saturation=0.98`, green-teal shadows (`colorbalance rs=-.03 gs=.04 gm=.015`), vignette PI/3.8.
- **Audio:** no denoiser, because the source may already contain a music bed. Highpass, light compression, then loudness at −14 LUFS.
- **SFX:**
  - one rising bell per checklist tick
  - snap on punch-ins
  - short whoosh when the background blurs
  - hit on the recap
  - drop on "lose"
  - long whoosh and a bell on the end card

## Don't
- Don't use purple (that's the other styles).
- Don't use red except for losses.
- Don't put text outside the safe zone.
- Don't let a fade-out baked into the source show: freeze the last clean frame (`hold_from`).
