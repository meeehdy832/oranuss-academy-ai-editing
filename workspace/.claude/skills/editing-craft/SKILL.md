---
name: editing-craft
description: Pro editing rules for every Oranuss video, adapted from the video-editor-skill (OthmanZr) to our ffmpeg + ASS pipeline - approval gates (plan, script breakdown, stills, draft, final), word-timed entrances, caption exit rules, one focal element per beat, transition rotation, social safe areas, text behind the subject (macOS Vision cut-out), the pre-show checklist and known pitfalls. Use whenever editing, reviewing or rendering a video.
---

# Editing craft (Oranuss pipeline)

Developed by Mehdi ORANUSS | Powered by Claude

Source: `.claude/skills/video-editor-skill/` (OthmanZr), especially `references/craft.md`, `workflow.md`, `audio.md` and `roto.md`. That skill builds edits in HyperFrames (HTML + GSAP). **This project builds them in Python → ASS + ffmpeg** (`project/styles/`, `project/build_*.py`). Same rules, our engine. Installing HyperFrames, Node or mlx-whisper (~5 GB) needs the user's OK first.

## 1. Approval gates (every video)
1. **Plan preview** (a few lines): length, structure (hook → points → CTA), style from `reference/styles/`, the hero beats, the overall feel.
2. **Script breakdown:** transcribe (whisper large-v3 + Darija prompt; re-check unclear clips with `-l fr` / `-l ar`) and proofread. Split into paragraphs with times. For each paragraph propose the graphic, layout, transition and focal element, and ask: **your idea, Auto (I decide), or no graphics?** Unanswered means Auto; say so. List the uncertain words in the same message.
3. **Stills:** fast draft render (`-preset veryfast -crf 20`, into `project/work/<video>/`), then a contact sheet with one frame per beat plus the middle of every transition. Run the checklist (§6) yourself and fix before showing.
4. **Draft:** full-quality 1080×1920 preview → `output/<video>/<Name>-PREVIEW-vN.mp4`. Check loudness and frames, then send.
5. **Final:** only after approval. Final resolution = **source resolution**. Never upscale a 1080p source to "4K"; render 2160×3840 only when the source is 4K.

If the user says "just do it" or "start editing", run gates 1–2 without waiting: show the plan and breakdown in the same message as the preview, and mark everything as Auto.

## 2. Timing
- **Entrances lead the word by ~2 frames** (0.067 s at 30 fps). Captions do it through `premium_serif.LEAD`; for graphics, start at `word_time - 0.067`.
- Nothing appears before it is said. For suspense, show it concealed (blurred, "?") and reveal it on the word.
- **Caption exits finish before the next caption's first word.** `dark_green.captions()` checks this and raises on overlap.
- Hard cuts and punch-ins sit on sentence starts or on the source's own cuts (find them with `select='gt(scene,0.12)'`).

## 3. Composition
- **The person is the anchor.** Never cover the face, and never compete with the eyes on a key sentence. Track the face (`project/work/<video>/faces.swift`, macOS Vision) and anchor the zoom on it.
- **Safe areas, 1080×1920:**
  - Text stays in y 250–1480 and x 64–940; this is stricter than the skill's top 190 / bottom 330 / right 150.
  - Margins ≥ 64 px.
  - Captions go at chest height under the chin, chosen per layout, not globally.
- **One focal element per beat**, about 3× its neighbours. Group related items with even spacing; no orphans.
- **Restraint:**
  - one saturated accent on screen
  - one glow per frame
  - particles only on reveals, never over the face
- **Real things:** a named tool or brand gets its real logo or UI. Never invent numbers or claims; every figure comes from the speech.
- Icon and logo tiles ≥ 140 px at 1080 width; the icon fills 55–60 % of its tile.

## 4. Motion
- **Momentum:** exits carry into the next entrance; nothing pops in from nowhere.
- **Anticipation and settle:** springs overshoot ≤ 4 % (`motion.pop`). Bounded values (bars, progress) never overshoot.
- **Never frozen:** a slow zoom drift on held shots. Punch-ins of +4–12 % on beats (`ZK` keys 1 ms apart).
- **Variety:** rotate transitions, caption entrances, icon containers and backgrounds; never the same move twice in a row.
- **Transitions in our pipeline:**
  - *Zoom-blur whip* (`dark_green.filter_graph(whips=[t…])`): zoom spike plus a blurred overlay, ±0.16 s around a cut.
  - *Depth blur* (`BLUR_WIN`): the plate blurs and dims under a graphic beat.
  - *Hard punch-in* (ZK keys).
  - *Frosted band* (`frost_win`).
  - *Flash* (`purple_glass.flash`).
  - Start a transition from empty space, never from inside a word.

## 5. Text behind the subject (cut-out)
- **Matte:** `project/tools/ves/bin/cutout-video <source.mp4> <dir>/masks` (macOS Vision person mask, compiled from the skill's `cutout-video.swift`, no install needed). It takes about 0.05 s per frame.
- **Build:** `dark_green.filter_graph(..., behind_ass=…, roto=(mask_dir, [(a, b)…]))`:
  - the plate gets the "behind" ASS layer;
  - the person comes back on top through `alphamerge`, with the matte cleaned by `tmix=3`, a choke LUT and `gblur 0.6`;
  - it is shown only inside its time windows.
- The matte gets **exactly the same** trim, zoom and crop as the plate, or the person floats.
- Use it for 1–2 hero beats (a title or big number behind the head) where the person is fairly still. Fast hands smear the matte.

## 6. Pre-show checklist (every contact sheet)
- [ ] No caption overlaps another caption, a graphic, the face or the mouth (check punch-ins).
- [ ] Captions are legible on every background, including light clothing. Prefer a tight edge (`\bord2\blur1`) over big soft halos on light shirts.
- [ ] Every transition reads as intentional in its middle frame: no blobs, no half-revealed words, no double person.
- [ ] Nothing load-bearing sits in the platform safe areas.
- [ ] One clear focal element per beat; colours follow the style's STYLE.md.
- [ ] Arabic script: joined correctly, nothing clipped, Latin words in the right order. Animate per word, never letter-space.
- [ ] First and last frames are clean. No baked-in fade-to-black under end graphics (freeze the clean frame: `hold_from`).
- [ ] Audio: −14 LUFS integrated, true peak ≤ −1.5 dBTP, music under the voice, ≤ 1 SFX per second.

## 7. Pitfalls (learned on real edits)
| Problem | Fix |
|---|---|
| Source already has burned-in captions, inserts or a fade | find them (scene detect + frames); cover with a frosted band, keep or replace inserts, freeze the last clean frame before a fade |
| Dark smudge behind captions on a white shirt | tight edge only, no big blur halo |
| Person appears twice | keep the footage still under the cut-out; reveal by clipping, not moving |
| Coloured rim around the cut-out | erode the matte 1–3 px in that window |
| A whoosh feels late | align its peak to the cut (`place_sfx` does this) |
| The same pop over and over | vary the take and pitch repeats 0.94–1.06 (`dark_green` does this) |
| Music drowns the voice | measure the voice LUFS; music bed at −27 dB, sidechain ratio 3, then normalise the sum (`.claude/skills/video-editor-skill/scripts/mix.py`) |
| Stale or partial renders | render to `project/work/.../rendering-*.mp4`, then `mv` into place |

## 8. Lasting preferences
When the user states a lasting preference ("no SFX", "smaller captions"), write it into that style's `reference/styles/<long|short>/<style>/STYLE.md` right away (or `brand/BRAND_CONFIG.md` if it applies to every style), so it holds for future videos.

## Tools from the skill we use directly (no install)
- `.claude/skills/video-editor-skill/scripts/analyze-reference.sh <file> <outdir>`: shots, cuts/min, average shot length, palette, loudness, contact sheets.
- `.../scripts/contact-sheet.sh <video> <out.jpg> t1 t2 … | --every 2`
- `.../scripts/mix.py`: voice + ducked music bed + SFX cue sheet → −14 LUFS mix.
