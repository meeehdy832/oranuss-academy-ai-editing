---
name: reel-from-reference
description: Master workflow to make a new Oranuss reel "like this one" from a reference reel link or file - analyse, brainstorm, script, build, render, then package the process. Use when the user shares a reel/TikTok/Short and wants a video in that style with their own topic and brand.
---

# Reel from reference (master workflow)

Developed by Mehdi ORANUSS | Powered by Claude

The 4-step process: reference → analysis → brainstorm → build. Each step calls a specialist skill.

## 0. Intake
- Ask only what is missing: the topic, the format (9:16 reel by default, 16:9 also possible), whether the user will film themselves (talking head) or wants it faceless, and the deadline or target length.
- Load the brand from `brand/BRAND_CONFIG.md` (Oranuss). Never borrow the reference's colours or logo.
- Pick the style: an existing one from `reference/styles/` (read its `STYLE.md` and build with `project/styles/<style>.py`), or a new style folder when the reference is a new look. Record the style in the README video table.

## 1. Analyse the reference → `reel-style-breakdown`
- Output: `reference/styles/<long|short>/<style>/breakdowns/BREAKDOWN_<handle>_<id>.md` (the style the reference belongs to; a new look gets a new style folder, see `reference/styles/README.md`), covering the layouts, beat timing, caption style, palette, type, motion vocabulary, UI mockups, sound and pacing.
- Show the user a 5-line summary and confirm it's the right reference before going on.

## 2. Brainstorm the same energy in Oranuss style
- Propose 6–10 "idea chips": the hook in the first second, layout per beat, signature motion, caption treatment, sound moments.
- Map every reference element to its Oranuss equivalent, using the table format in the breakdown.
- For a new style, write `reference/styles/<long|short>/<style>/STYLE.md`: palette tokens, fonts, captions, layouts, graphics, motion rules, grade, sound and what not to copy; then `project/styles/<style>.py`, and a ~7s test before the full video.

### Hook bank (tested in the references)
- **Viewer question card:** answer a real comment from the audience.
- **Meta result:** a phone mockup of the finished video + a "Render complete" notification.
- **Cold-open B-roll:** 3–6s of a different scene or a phone POV before the talking head.
- **"N tips" title:** numbered icons, then go straight to tip 1.
- **Big number:** "30", "3", "14" huge behind or beside the speaker on the first word.

### Episode / series identity
For recurring content, use an "EP 0N" badge and the chapter header "0N / Label", always in the same position, so the series is recognisable.

## 3. Script + beats
- Gates (from `editing-craft`): plan preview → script breakdown per paragraph, where the user picks **their idea / Auto / no graphics** → stills → draft → final.
- Script in the user's own Darija voice: hook → steps (numbered, "STEPS 1/N") → payoff → CTA. Keep it short; one idea per 3–5s beat.
- `output/EDITING_PLAN.md`: a table with one row per beat (time, spoken words, layout A/B/C, UI mockup, caption keyword, SFX).
- If the user records a voiceover or video, transcribe it with `darija-voice-captions` and re-time the beats to the real audio.

## 4. Build → render
- Layout per beat: `talking-head-layouts`.
- UI demos: `ui-demo-mockups`.
- Captions: `kinetic-captions` (which builds on `darija-voice-captions`).
- Sound: `sound-design`.
- Look: `oranuss-visual-system`.
- Render the preview with `render-and-review`, as `output/<Name>-PREVIEW-vN.mp4`. Write to a temporary file and rename it only when the render succeeds, so a half-written MP4 is never visible.
- Export the final only after the user approves.

## 5. Package (optional)
- If the user wants to repeat this format, write a new skill in `.claude/skills/<format-name>/SKILL.md` that captures the beat template, the layout sequence and the parameters, so the next video is one command.

## Rules
- A reference guides direction; never recreate its exact graphics, text or branding. Don't download a reference without the user's OK; view it through its public page, or have the user drop the file into `reference/`.
- Originals stay untouched; renders get versioned names.
