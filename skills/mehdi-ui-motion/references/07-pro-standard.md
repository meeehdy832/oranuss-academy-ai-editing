# The pro standard: the measured gap to a pro motion designer, and how the gold reel closed it

Source: the author's frame-by-frame comparison report (pro = dnyxstudios Wallet
reel = v12; AI = the v2 demo), every number re-measured with `scripts/energy.py` (mean abs luma difference between
frames, gray, 180 px wide). The gap was NOT design or ideas: it was motion physics, blur, transitions and liveness.

## 1. Measurements

| Metric | Pro (v12) | v2 (rejected) | Gold reel (v3) |
|---|---|---|---|
| median energy (how alive a typical frame is) | **0.84** | 0.52 | **0.77** |
| max energy inside the video (spike = flash / naked cut) | **6** (58 at the loop seam, 189 at the studio card) | 111 (white iris), 250 (cut to black) | **13.7** (the dusk); match cut ~7.5 |
| longest run below 0.2 (a freeze) | 11 f | 34 f | **none ≥ 8 f** |
| flat single-colour frames | 0 | 2 runs | **0** |

## 2. What the pro does → the rule

1. **Holds are not still.** While the buttons wait (v12 116–135) the camera pushes in at 0.45–0.8 % scale per frame,
   then the same push accelerates into the transition (2 → 5 → 13.7 %/f at 135–140). v2 drifted at 0.04–0.1 %/f.
   → Every hold pushes **0.2–0.8 %/frame** (a camera move ×1.15–1.35 over 50–100 f, drift ease), background blobs wander,
   and the hold's last move becomes the transition's acceleration.
2. **Pulse shape and rhythm.** A UI change accelerates ~8 f, peaks, decays 12–20 f; peaks every ~28–30 f in v12.
   → Key moments roughly every 30 f (15 f in fast parts); long soft tails; never linear for elements.
3. **Real motion blur.** Moving things smear along their own path; still parts stay sharp.
   → `<MotionBlur samples={10} shutter={180}>` (sub-frame accumulation). Gaussian `blur()` only for one element's
   focus pull (8–12 px → 0) or constant depth of field (2–6 px). A gaussian blur on a whole moving layer = gray block.
4. **Transitions hide the cut.** v12: the pressed Send button (blurred) becomes the blue "$" coin (match cut,
   140 → 141); the sentence collapses into a point and "Add Funds" grows out of it (52–64, 3–4 f overlap); coins rush
   at the camera and blur, cut, "Pay" focus-pulls in (zoom-through, 211–219).
   → Allowed: match cut on motion · collapse → emerge from one point · zoom-through · a morph whose new content appears
   while it grows. Always 3–8 f of overlap. Forbidden: white flash / iris to white, fade to black, flat colour > 2 f,
   hard cut on a still frame. Gate: no energy value above 15.
5. **Smallest meaningful unit.** Words one by one (2–4 f), y + blur + opacity + skew tied to speed; existing lines move
   to make room; UI pieces stagger 2–6 f; numbers change per character on a wave with blur and an accent tint.
6. **Decode = real letters**, ≤ 8 f, under a clearing blur. ASCII symbols read as "hacker", not Apple.
7. **Depth / focus plane.** Inactive items smaller (0.85–0.92), lighter (0.35–0.6), blurred (2–6 px); lists as 3D wheels.
8. **Cursor and click.** Curved path, arrow → hand 6 f before, press, accent ring, the result grows from the button.
9. **The ending stays alive.** Push + moving dot + tagline change; the end card emerges from the collapsing logo.
10. **Pixels with intent.** Cells move on eased paths and BUILD a word (gather), not pop at random places.

## 3. Lessons from building the gold reel (all apply by default)

- **Match cut physics:** a push into a cut with `EASE_PRO.exit` / `exitHard` spiked to 19–44. Use AE ease-in
  `aeEase(70, 0)` (ends at half the speed) and start the incoming camera with `aeEase(0, 75)` so the speeds match.
- **Fade body text out before a match cut** so only flat surfaces + the matched shape rush at the camera
  (with real blur: 21.8 → 7.5).
- **Light → dark world change:** never through gray, never a flash. Through blue midtones
  (`LIGHT → #A9C8FF → #1E3F9E → NAVY`), starting ~14 f before the zoom-through and spread over ~58 f (peak 13.7).
  Budget: Δluma ÷ frames × 1.5 must stay under ~12.
- **Backdrop outside `<MotionBlur>`**: averaging copies of a soft gradient bands it into rings.
- **Drafts under-report energy** (with `mb: 1` the camera falls back to a gaussian blur that smooths frame
  differences). Re-measure risky windows with real blur: `--frames=A-B` (1–2 min) before the full final.
- **Continuity between frames:** `<MotionBlur>` samples fractional frames. Anything computed per whole frame (a
  `Math.floor(frame)` loop, a stepped state) shows as a DOUBLED image. `springFollow` interpolates sub-frames; do the
  same in any stateful animation. Check fast frames at 100 % crop.
- **Render settings:** `--concurrency=3 --timeout=120000`, boost ≤ 14 samples, new output file name every time (a failed
  render silently leaves the old MP4). Close other heavy apps (video editors, browsers with many tabs) before a final: a render with 10–14 blur samples needs a lot of RAM.
- Wheel picker mask window ≈ 1.5 rows (else the rolled-away item ghosts over the line above).

**Lessons from v-02 (AgencyReel, 26 s voice-over reel, 9 scenes, one camera):**
- A placement helper (`At` = translate(x,y) translate(-50%,-50%)) must APPEND a transform passed in `style`, never let
  `...style` replace it. Overriding it silently dropped half the layout to the frame centre (draft 1).
- A morph target drawn BEFORE the morphing hero hides it: draw the growing container (chat card) first, then the hero
  (editor → thumbnail), then the content, all inside one `Stage` so they collapse together.
- `Converge` lands words in random order spread over `every × words` frames: keep `every` ≤ 3 when the line is spoken
  word by word, or the last word lands first.
- `WaveNumber` across values of different length ("$97" → "$0") passes through junk like "$07": use a vertical swap
  (old drops out with EXIT + blur, new drops in 3 f later with ENTER-SNAP) instead.
- collapse → emerge: start the emerge 6–7 f after the collapse (EXIT is still slow in its first half; at +3 f the two
  scenes read as a double exposure).
- Morph containers: start the content fade when the container is ~12 % grown (not 30 %), or the camera pull-back shows an
  empty white card for 4–6 f.
- Voice-over reels: transcribe with whisper (`scripts/transcribe.mjs`), write word start frames into the beat sheet and
  start each word's animation 2–4 f BEFORE it is spoken; numbers start rolling as they appear (never a static "$0").
- Draft gates reached on v-02: max 14.3, median 0.87, no low runs (mb 1); render ≈ 2.6 s/frame on boosted frames.

## 4. Optional knobs (tested AFTER the gold reel; not part of its look, use only when a measurement asks for it)

- A dark section measuring a median below ~0.5: push ~0.4 %/f instead of ~0.27 and add slow rising square bokeh
  (`Particles shape="square"`, vy −1.1, opacity .1–.45).
- Render time: `boost` accepts tiers (`[{samples: 10, windows}, {samples: 14, windows}]` with a base of 4) — same
  look on calm frames, ~30 % faster.
