---
name: reel-style-breakdown
description: Watch a reference reel (Instagram/TikTok/YouTube link or local file) frame by frame and write a precise style breakdown - layouts, beat timing, captions, palette, typography, motion vocabulary, UI mockups, sound, pacing - plus a mapping to the Oranuss brand.
---

# Reel style breakdown

Developed by Mehdi ORANUSS | Powered by Claude

## Get the frames
- **First pass on any local file:** `bash .claude/skills/video-editor-skill/scripts/analyze-reference.sh <file> reference/styles/<long|short>/<style>/breakdowns/analysis/<name>`. It gives a shot contact sheet, cuts/min, average shot length, palette with accent candidates, loudness and a timeline sheet. Read `shots.jpg` and `timeline.jpg` yourself and quote the numbers in the breakdown.
- **Local file in `reference/styles/<long|short>/<style>/examples/`** (preferred): `ffprobe` for duration, size and fps. Grab frames every 1–2s with `ffmpeg -ss T -i file -frames:v 1`, and make contact sheets with `hstack`/`vstack`. Use `silencedetect` and a loudness scan to find the beats.
- **Instagram link:** the logged-out page often shows a sign-up wall; open `https://www.instagram.com/reel/<ID>/embed/` in the built-in browser instead. Make the `<video>` fixed-size (height = viewport, width = height×9/16), pause it, then for each time T run `await new Promise(r=>{v.addEventListener('seeked',r,{once:true});v.currentTime=T})`, wait two animation frames, and capture with `zoom` on the video region. Sample every 3–4s, plus extra frames around layout changes.
- Never download someone else's video without the user's explicit OK. Sound is usually unavailable in the browser; say so and infer the speech from the on-screen captions.

## What to record (write all of it)
1. **Meta:** creator, length, aspect ratio, language/dialect, what the video *says* (its argument, in steps).
2. **Layouts:** each distinct screen composition (full face, split screen, full cutaway, B-roll), the fraction of the screen each part takes, and when the video switches between them.
3. **Beat timeline:** a table of time → layout → on-screen element → caption, with one row per change.
4. **Captions:** position, words per chunk, font weight, how keywords are highlighted, script (Arabic or Latin), entrance animation.
5. **Palette:** background, accent and text colours; estimate hex values from the frames and mark them as estimates.
6. **Typography:** caption font family style, accent fonts (serif italic, mono labels), headers.
7. **Motion vocabulary:** entrances, transitions, typing, counters, charts, 3D, glow, blur.
8. **UI mockups:** which apps or interfaces are drawn, whether they're real screen recordings or rebuilt mockups, and any privacy masking.
9. **Sound:** music mood, SFX density (e.g. a hit on every word), voice source.
10. **Pacing:** average seconds per beat, how the hook works, the CTA.

## Output
- `reference/styles/<long|short>/<style>/breakdowns/BREAKDOWN_<handle>_<id>.md` with the sections above, plus a **"Maps onto Oranuss"** table (their element → our equivalent).
- Keep the contact sheets in `project/ref/`.
- Name the 3–5 techniques that make the reel work; those are what the new video should borrow.
