---
name: talking-head-layouts
description: Build 9:16 (and 16:9) talking-head reels that switch between full-face, split-screen (face top + UI panel bottom) and full-screen motion cutaways on each beat, Oranuss style. Use when a selfie/talking video needs the "creator explains a process" look.
---

# Talking-head layouts

Developed by Mehdi ORANUSS | Powered by Claude

## The three layouts (9:16, 1080×1920)
| Layout | Composition | When |
|---|---|---|
| **A: Face** | Camera fills the frame (crop 9:16 from the source; face's eyes about 38% from the top). 1–3 small floating widgets: an icon bubble, a timer ring, a label pill, a sticker | Hook, opinions, emotion, the CTA |
| **B: Split** | Face in the top 0–860px (crop centred on the face, slight push-in). Panel 860–1920: ink background with a neon top border line 2px. Header at 900–1010: mono label `STEPS 2/4` + heavy headline with a lavender accent word. UI mockup at 1030–1560. Captions at 1600–1720 | Every "how to" step and demo |
| **C: Cutaway** | Full ink stage, no face (or the face inside a card): carousel of cards, orbit diagram, big kinetic words, numbers | Concept explanations, transitions between steps, "wow" moments; 2–6s at most |

16:9: Split = face on the left 55%, panel on the right 45% (header at the top of the panel); A and C as above.

### Variants (from reference batch 2)
| Variant | Composition | When |
|---|---|---|
| **B2: UI top + PiP** | UI card in the top 55% on a light or ink background; the speaker in a **rounded rectangle (r=36) at the bottom**, 900×620 centred, with a neon rim | Software demos where the UI matters more than the face |
| **B3: Circle avatar** | Full-screen UI; the speaker in a **circular PiP** (d=260) in a corner, with a lavender rim and a soft glow | Long UI moments; keeps a human presence |
| **A2: Cinematic** | Face full screen, darker grade, **single-word captions**, minimal graphics | Story, emotion, the intro of an episode |
| **A3: B&W beat** | The A layout turned monochrome for 1–2s (`hue=s=0`) with a big word | Warning, punchline, a "mistake everyone makes" |

### Chapter system
Each section gets a persistent header in the top right: a thin, big numeral **"0N"** + a divider + a label ("01 / Application"), lavender, in for the whole chapter. It replaces or complements `STEPS n/N`.

### Text behind the subject
A big word or number placed behind the speaker needs a per-frame person mask. It is **installed**: `project/tools/ves/bin/cutout-video <source> <dir>/masks` (macOS Vision, from the video-editor-skill, ~0.05 s per frame).
- Pipeline in `dark_green.filter_graph(behind_ass=…, roto=(mask_dir, windows))`: plate + "behind" ASS → person over it through `alphamerge` (matte: `tmix`, choke LUT, `gblur 0.6`) → front ASS.
- The matte gets the same trim, zoom and crop as the plate.
- Use it on 1–2 hero beats where the speaker is fairly still. Details: `editing-craft` §5.

## Rules
- Change layout or UI state every 3–5s; hard cuts between layouts, with a 0.15s neon flash or a 6-frame scale-in on the new layout.
- The step header persists while the step lasts; update `STEPS n/N` when the step changes.
- In layout B the face crop must keep the eyes and mouth inside the top area for the whole beat. Check frames at the beat's start, middle and end; if the speaker moves, track by changing the crop offset per segment.
- Never put captions over the face in B; in A, captions go below the chin.
- Hook (0–1s): layout C or A with a big kinetic word plus a sparkle; never start on a static frame.

## ffmpeg recipe (B)
```
[face]crop=ih*9/16*0.9:ih*0.9*860/1080:X:Y,scale=1080:860[top];
color=c=0x100820:s=1080x1060[panel];
[top][panel]vstack[split];  # then ass= draws header, UI, captions
```
Compute X and Y from the face position measured on the stills (per segment if the speaker moves). Draw the UI mockups and header with the `ui-demo-mockups` and `oranuss-visual-system` components.

## Output
- Add a `layout` column (A/B/C) to `output/EDITING_PLAN.md` for every beat.
- Before the full render, check frames at every layout switch for collisions and face crop.

### Depth trick (premium-serif)
While a graphic is up, the plate blurs (gblur σ≈26), darkens (−0.13), desaturates (0.8) and scales up 4%. Overlay that blurred copy with 240 ms alpha fades on each side (`BLUR_WIN` in `project/build_7s.py`). Diamond badges (rounded square at 45°, purple fill, lavender inner stroke, glow) replace plain chips for numbers and lists of 3. Make a cut or graphic change every 1.5–3 s.
