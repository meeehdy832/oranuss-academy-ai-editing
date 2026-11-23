# Style spec: design and motion tokens

All values are estimated from a 720×1280 reference and expressed for a **1080×1920, 30 fps** project.

## Canvas
| Token | Value |
|---|---|
| Board background | #EEEAE4 radial (center #F2F1EC → edges #E8E3DC), faint 1 px grid at ~4 % opacity, ~40 px cells |
| A-roll | Dark set, colored backlight (cyan-blue), shallow depth of field, heavy bottom vignette to ~#000810 behind captions |
| Safe column | x 8 %–92 % |
| Board bands | Headline y 10–13 % · main object y 28–50 % · data/bars y 84–89 % |
| A-roll captions | Centered, baseline y 58–64 % |

## Color (default palette; swap for brand colors but keep the ratios)
| Role | HEX |
|---|---|
| Primary (60 %) | #183050 |
| Secondary (30 %) | #A0C0D8 |
| Accent (10 %) | #1868D8 |
| Annotation line | #3A9AD0 |
| Serif emphasis on board | #1E5AA8 |
| Warm pop (one use) | #E0704A |
| Positive / price | #1FA463 |
| Caption on A-roll | #FFFFFF (small words at ~85 % opacity) |

## Type
| Role | Font (reference → free alternatives) | Size @1080 w | Weight |
|---|---|---|---|
| Primary sans | Creato Display → Inter, Manrope, SF Pro Display | Running 40–46 px · Key word 60–72 px | 500 / 700 |
| Emphasis serif | Apple Garamond Italic → EB Garamond Italic, Cormorant Garamond Italic, Playfair Display Italic | 64–80 px | 400 italic |
| Micro label | Primary sans, UPPERCASE, tracking +18 % | 14–16 px | 600 |
| Headline numerals | Primary sans bold | ~2.2× the lead-in word | 700 |

Caption line recipe: `small sans` → `LARGE italic serif word` → `small sans` → `bold sans keyword`.

## Shapes
- Rounded squares: 110 px, corner radius 22 px (≈ 20 %).
- Cards: corner radius 24–32 px.
- Pills: full radius.
- Shadow: 0 / 8 px / 24 px blur, #000 at 22 %. While dragging: 0 / 16 / 36 at 28 %.
- Call-out line: 2 px stroke, anchor dot 10 px with a 2 px ring. The label is a bold value over a small grey descriptor.
- Dashed grid: 2 px, dash 8 / gap 6, annotation color.
- Step badge: a 64 px diamond (square rotated 45°), accent gradient, white numeral, soft outer glow.

## Motion (30 fps)
| Event | Duration | Easing / detail |
|---|---|---|
| Caption word in | 6–8 f | Opacity 0→100, Y +16→0 px, blur 8→0 px; cubic-bezier(0.16, 1, 0.3, 1) |
| Element spawn | 10–12 f | Scale 0 → 112 % (f7) → 100 %; spring, damping ~0.6 |
| Drag/move | 12–18 f | Ease-in-out (0.65, 0, 0.35, 1); the object lags the cursor by 2–3 f |
| Snap to grid cell | 6–8 f | Ease-out with a 4 % overshoot |
| Width morph (swatch → bar) | 15 f | Ease-in-out; label fades in at the end |
| Line draw-on | 10–12 f | Trim path 0→100 %, ease-out; dot pops at the end; label types 2 f/char |
| Stagger | 4–6 f between siblings | In reading order |
| Exit | 8–10 f | Blur 0→40 px + opacity → 0 + scale 100→92 % or a fly-off |
| Board slide-in (split screen) | 15–20 f | Y −100 % → 0, blur during motion |
| Font cycling | 4–8 f per face | Slow down over the last 2 swaps |
| Cursor | Bezier path | Arrives 4–6 f before the reaction; a 3 f "press" (scale 90 %) on click |

## Rhythm
- A new visual event every 0.5–1.5 s. No static hold longer than 2 s.
- Section lengths: Hook ~8 s · Steps ~15–18 s each · CTA ~6 s · total ≤ 66 s.
- Every board scene starts empty and ends "complete" (an accumulating build).

## Sound (optional; not verified in the reference)
Soft UI click on cursor taps, a light whoosh on blur transitions and a subtle pop on spawns, ~−20 dB under the voice. Animations fire on spoken keywords: the voice leads and the visuals follow.
