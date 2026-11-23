# Style: purple-3d-glass

The look of the user's style board (`examples/style-board-20-motion-types.webp`, 20 tiles: UI motion, icon animation, 3D product, infographic, data viz, transitions, character, text, map, process, chart, isometric, liquid, glassmorphism, shapes, parallax, line animation, illustration, device mockup, mixed). Light lavender world, frosted glass cards, glossy "clay" 3D purple objects, soft glow, depth.

- **Engine:** HyperFrames (HTML + CSS + GSAP, rendered by headless Chrome). Our ASS/ffmpeg pipeline can't do real gradients, backdrop blur or 3D transforms, so this style is built in HyperFrames.
- **Videos made in this style:** AI Editing launch v2 (`project/hf/gen_ai_editing_v2.py` → `project/hf/ai-editing-v2/`).
- **Code:** design system in `project/hf/ai_editing_v2.css`; scene generator `project/hf/gen_ai_editing_v2.py` (glass, gloss, sphere, chip, phone, laptop, ring, bars, stepper, avatars, wipes, captions).
- **Render:** author at 1920×1080, render with `--resolution 4k` for a sharp 3840×2160 master (pure graphics, so 4K is real detail).

## Colours
| Token | Hex | Use |
|---|---|---|
| Canvas | `#F6F2FF` → `#DDD0FF` vertical gradient, white glow top-left, lilac glow bottom-right, faint 96 px grid | background |
| Glass | white 84 % → 46 %, blur 24, 2 px white rim, soft purple shadow | every card, chip, caption pill |
| Gloss purple | radial `#E2D8FF` → `#A78BFA` → `#7C3AED` → `#4C1D95`, top sheen, inner shadow | hero objects, buttons, active states |
| Ink | `#1B1240` | titles, labels |
| Muted | `#7E76AA` | upcoming caption words, secondary text |
| Accents | gold `#FBBF24`, green `#34D399`, warm gloss orange | star/importance, done/earn, product |

## Type
Poppins: 800 for titles and the wordmark, 600 for labels and captions. Hero title up to 176 px, gradient fill on the key word ("AI").

## Pieces (style board → our component)
| Board tile | Component |
|---|---|
| 01 UI Motion, 19 Device Mockup | `phone()` with a live screen, tilted in 3D, slow turn |
| 02 Icon Animation | glossy play tile + selection frame with handles + cursor |
| 04 / 11 Infographic, Chart | glass panel, gradient bars (hero bar glossy), trend line drawing with arrow head |
| 05 Data Visualization | gradient progress ring around a glossy chip |
| 06 Creative Transition | purple colour-flood wipe between sections, blur/zoom exits |
| 08 Text Animation | per-word blur-in titles |
| 10 Process Animation | glossy node → dashed animated connectors → numbered steps |
| 12 Isometric | CSS 3D laptop, tilted video grid |
| 14 Glassmorphism | `.glass` everywhere |
| 15 Shape Animation | floating glossy spheres (background, slow drift) |
| 16 Parallax | layered mountains + sun on the end card |
| 17 Line Animation | glowing trail line under the launching rocket tile |
| 07 / 20 Character | presenter image (needs an image generator: HeyGen sign-in) |

## Motion
Arrivals `expo.out` 0.6–1.2 s; 3D objects enter tilted (rotationY ±40°) and settle to ±12°, then turn slowly; small atoms pop with `back.out`; exits 0.32 s blur + fade (vary: blur, slide-left, rise, zoom-through). Graphics land 2 frames before their spoken word.

## Captions
Glass pill at the bottom, Poppins 600 48 px; upcoming words muted, spoken words ink, the active word purple, keywords 800.
