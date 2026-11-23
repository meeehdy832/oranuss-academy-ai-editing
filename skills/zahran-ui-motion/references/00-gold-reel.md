# The gold reel: "Orbit" (ProDemo v3), the smoothness standard

The author (Yahia Zahran, Zahran Motion) chose this render (code: `kit/examples/ProDemo.tsx`; render it yourself to see it)
as THE reference for how smooth and fluid this style must feel. When in doubt, do what this reel does, with these values.
1080×1080 · 30 fps · 540 f (18 s) · Inter · one accent `#0A84FF`. Rendered with `<MotionBlur samples={10}>` + 14-sample
boost on the four fastest windows.

Measured (`scripts/energy.py`): median energy **0.77** (pro reel v12: 0.84), max **13.7** (the light → dark dusk), match
cut peak ~7.5 (pro transitions 4.5–6), **no freeze**, **no flat-colour frame**, text jitter on holds < 0.1 px.

## Palette and type

| Token | Value | Use |
|---|---|---|
| BLUE | `#0A84FF` | the one accent: key word, field caret, click ring, logo dot |
| SKY | `#5AC8FA` | accent on dark (arrival colour, "autopilot.") |
| INK | `#111111` | text on light |
| LIGHT | `#F7F8FA` | light stage |
| TINT | `#D6E5FF` | first frames (blue → light, frames 0–26) |
| NAVY | `#060B16` | dark stage |
| SHADOW | `0 40px 80px -30px rgba(0,0,0,.20), 0 14px 28px -14px rgba(0,0,0,.10)` | cards, bar, notification |
| HOOK_F | Inter 66 / 600 / −0.035 em, line 86 px | hook lines |
| DARK_F | Inter 76 / 600 / −0.035 em | statement |
| field text | Inter 36 / 500 / −0.01 em | typing |
| stat number | Inter 92 / 700 / −0.05 em | "4h 40m" |
| wordmark | Inter 92 / 700 / −0.05 em | "orbit" |

## Layers (bottom → top)

1. **Backdrop** (OUTSIDE the motion-blur stack, so soft gradients never band): world colour + drifting blobs.
   - Colour: `TINT → LIGHT` over frames 0–26 (enter), then the **dusk** from frame 286 over 58 f (drift ease) through
     `LIGHT → #A9C8FF → #1E3F9E → NAVY` at stops 0 / .35 / .70 / 1. Never straight light→navy (it passes through gray).
   - Light blobs (opacity × (1 − darkness)): `#C9DFFF` 1000 px at (−330, −360) α .75 period 260 f; `#D3F2DE` 900 px at
     (380, 380) α .6 period 300 f phase 90.
   - Dark blobs (opacity × darkness): `#0A84FF` 1400 px at (0, 470) α .5 period 220 ay 70; `#3A2BFF` 800 px at (−420, −380)
     α .22 period 280 phase 60.
2. **`<MotionBlur samples={mb} shutter={180} boost={{ samples: 14, windows: [[52,66],[116,140],[216,242],[308,332]] }}>`**
3. Scenes, each inside its own `CameraRig` (3D layer + 2× raster: no jitter): LightWorld (0–237) → StatsWorld (236–327)
   → DarkWorld (318–427) → Logo (418–513) → EndCard (505–540).

## Timeline, beat by beat

| Frames | Beat | What moves (technique · values) | Camera |
|---|---|---|---|
| 0–18 | Hook line 1 | "Still": `LiquidIn` start −3, 16 f, accent BLUE → ink (wavy displacement 70 → 0, scaleX 1.35 → 1, blur 10 → 0). "planning": `Decode` start 7, 8 f, letters only, blur 5 → 0 | keys: zoom 1.22 / cy 14 at f0 → 1.0 / 0 at f64 (drift): a continuous pull-back through the whole hook. Drift +1.2 %/s under everything |
| 18–36 | Hook line 2 | `StackLines` (lineH 86, 16 f, MOVE): line 1 slides up as line 2 arrives. "your week by": `WordIn` start 18, every 3. "hand?": `WordIn` start 31, 18 f, BLUE kept | (pull-back continues) |
| 19–37 | Pixels build "hand?" | `PixelGather` at 19: 16 cells of 20 px, colours BLUE / SKY / `#0040DD` / `#9BD1FF`, spread 150, 16 f, ENTER paths, cells shrink to 30 % and fade in the last 28 % | — |
| 52–66 | **Collapse → emerge** | Hook `Stage collapseOut(52, 12)`: scale → .7, blur → 10, EXIT curve, opacity held to f63 then 0 by f66. The bar is born at f57 from a 26 px BLUE dot at the same centre (`emergeIn(55, 16, .8)`), 4 f before the hook is gone | move @50, 44 f, zoom ×1.3, MOVE: the camera direction flips ON the collapse (pull-back → push-in) |
| 57–100 | **Bar grows while it types** | `fieldGeom`: seed 26 → pill 560 × 104 (spring ω .30, ζ .78), BLUE → white with growth; typing starts f63 ("plan my week around the gym", 0.9 chars/f ≈ 30 f) while it is still growing; width keeps following the text (aim 2ζ/ω ≈ 5 f ahead). `RingDraw` at 68: blue outline draws in 12 f, fades at 90 | follow-cam: `cx = w(f) × springFollow(caret × 0.4, ω .16)`, weight in at 62 (18 f moveSoft), out at 100 (30 f MOVE). Move @92, 32 f, ×1.06 drift |
| 94–122 | Cursor + click | `MacCursor`: appears f94 at (470, 330) arrow → arc (bend .22) to the send button by f112 → hand at f114 (6 f before) → click f120 (press 1 → .85 → 1). Button `pressScale(.05)`. `ClickRing` at 120 (72 px, BLUE, 1 → 1.3, .6 → 0, 12 f) | — |
| 116–160 | **Bar → calendar card (one object)** | morph at 122: `springFollow` w (ω .24, ζ .74) / h (ω .26, ζ .74) → 820 × 620, radius h/2 → 48. Field content blurs out in 4 f. Calendar fades in from 5 % of the size change. "This week" `WordIn` 126 every 3 (44/700); "planned by Orbit" 134 (26/500 BLUE); day headers ENTER-SNAP 16 f, 2 f stagger from 128; 10 events from 134, 2.5 f apart in diagonal order, scale .9 → 1 (origin top-left), blur 6 → 0 by 80 % | move @116, 40 f, ×0.68, `aeEase(50, 85)`: pull-back reveal as the card opens |
| 150–206 | Alive hold + notification | notification `snapIn(180, down 80, 18 f)` from behind the card top, its text types at 1.4 chars/f from 188 | move @150, 56 f, ×1.18, y −70, drift (≈ 0.3 %/f push) |
| 200–238 | **Match cut: notification icon → stats ring** | calendar fades out from 206 (EXIT 16 f); notification text from 212 (EXIT 14 f) so only the white card + the ring icon rush at the camera. Cut at 236: the stats ring (same conic ring, 440 px) appears at exactly the icon's screen size (56 × 4.4 = 246 px), Stage opacity .35 → 1 in 2 f, light world kept 2 f under it | push @200, 36 f, to the icon (x/y solved with `camState`), zoom to 4.4 × at the cut, `aeEase(70, 0)` (ends at half the speed of EXIT). Stats camera starts at 246/440 = .56 → 1.0 at 264 with `aeEase(0, 75)`: speeds match at the cut |
| 236–300 | Stats | ring 440 / thick 62 rotates .35°/f; "1h 20m" → "4h 40m" `WaveNumber` at 270 (14 f, 1.5 f per char, sine lift .16 em, blur 4, BLUE at the crest); ring progress .3 → .9 MOVE 16 f from 270; label `WordIn` 248 every 3 (34/500 gray) | move @252, 66 f, ×1.22, y 20, drift |
| 286–330 | **Zoom-through + dusk** | dusk 286–344 (above). Number fades from 302 (EXIT 14 f), label from 300 (12 f). Stats Stage fades 318 → 328; the dark scene's Stage enters 318: scale .86, blur 12, opacity 0 → opacity 1 at 328 (linear) → scale 1, blur 0 at 340 (ENTER-SNAP) | move @294, 34 f, ×3.0, `aeEase(70, 0)`: the ring rushes past the camera while the world darkens |
| 324–412 | Statement + wheel | "Your week," `WordIn` 324 every 4, SKY → white, dist 26. "on" 334. Wheel container fades in 336–354 (blur 8, y 24). `WheelPicker` track. → time. → autopilot. at 360 / 386 (16 f, step 32°, mask window 1.5 rows); "autopilot." in SKY | move @324, 96 f, ×1.3, roll −1.6°, drift (+1 %/s drift) |
| 412–440 | **Collapse → logo** | statement `collapseOut(412, 12)`; Logo Stage `emergeIn(418, 22)`; ring stroke draws 24 f ENTER while rotating −230° → −90°; BLUE dot orbits an ellipse 110 × 36 px, one lap / 84 f, front 1.08 / back .86 scale, glow | logo camera @418, 86 f, ×1.28, y −6, drift |
| 428–498 | Logo alive | "orbit" `WordIn` 428 (92/700); "plan less." `WordIn` 442 every 4 → `SwapLine` to "live more." at 468 (SKY arrival) | (push continues) |
| 498–540 | **Logo → end card** | logo `collapseOut(498, 9, .55)`; end card `emergeIn(505, 22, .5)`: "ui-motion-pro" 64/600 white, glow `0 0 18px rgba(255,255,255,.65), 0 0 46px rgba(90,200,250,.35)`, scale 1 → 1.16 drift to the last frame | — |

## Why it feels smooth (the rules this reel proves)

1. **Nothing waits.** Typing starts inside the bar's growth; the card's content appears during the morph; the bar is
   born 4 f before the hook is gone; the dark text emerges 6 f before the stats are gone.
2. **The camera never stops.** Every camera entry starts while the previous one is landing (50 vs 64, 92 vs 94,
   116 vs 124, 150 vs 156, 200 vs 206). Direction changes only on events (collapse, click).
3. **Holds push.** 0.2–0.4 % zoom per frame on every hold, plus the backdrop blobs and the drift.
4. **One hero object carries three beats**: dot → bar → card; icon → ring.
5. **Cuts hide inside motion**: the match cut lands on an identical shape at an identical size and matched speed;
   the zoom-through hides the world change inside the rush and the dusk.
6. **Real shutter blur, sharp holds**: 10 samples everywhere, 14 on whips/rushes, backdrop outside the blur, fake
   gaussian off.
7. **Text varies**: LiquidIn, Decode, WordIn, PixelGather, typing, WordIn + stagger, WaveNumber, WheelPicker, SwapLine:
   no technique twice in a row.
