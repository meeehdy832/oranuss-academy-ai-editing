# Reel breakdown: "that is my process"

- Source: https://www.instagram.com/reel/DexY5nvJzhm/ (viewed through the public embed page; no file was downloaded)
- 115s, 9:16 (720×1280), Tunisian derja, Arabic-script captions
- Watched with the sound off, by sampling a frame about every 4s. The topic and timings come from what's on screen, not the audio.

## What the reel says (his 4-step process)
1. **Find a reel you like** and copy its link ("Copier le lien").
2. **Give it to Claude to analyse in detail:** "tfarrej fel vidéo hedhi w analysiha b détails: chnowa ma3moula, b chnowa…". Claude returns a style spec: étapes, layout, couleur (terracotta `#CF6F56`), outils.
3. **Brainstorm the same style and the same motion** ("act as expert"). Idea chips: *hook en 1s*, *spark 3D*, *SFX sur chaque mot*, *kinetic type*, *split + clamps*. Then he gives Claude the topic and script.
4. **Claude builds it while he watches** ("Claude ykhdem w ana netfarrej"): voice (ElevenLabs), music, and design / rythme / vibe controls. It renders 1080×1920 at 30fps, plus a 16:9 version, with GPU-accelerated rendering. Last, "a3melli skill": the whole process is saved as `SKILL.md` (`/aura-trailer`) so he can run it again.

## Visual system
| Element | What he does |
|---|---|
| **Layout A: face full screen** | Selfie camera in a warm, dim room; small floating widgets around the face (a "motion graphics" pill, a "60 secondes" ring timer, a Claude asterisk logo, an "easy peasy" sticker) |
| **Layout B: split screen** | Face in the top ~45%, a dark panel below (~55%) showing an app UI mockup. The panel header has a small mono label "STEPS 1/4" and an Arabic headline whose Latin keyword is set in an italic serif accent ("reel", "Claude", "style", "motion") |
| **Layout C: full-screen cutaway** | Pure motion graphics: a carousel of reel cards on a dark stage with his face in the centre card, and an orbit diagram of "2 agents" around a glowing core |
| **UI mockups** | Rebuilt, not screen-recorded: share menu, chat box with typewriter text, response cards with key/value rows, terminal, idea chips, voice waveform card, timeline tracks, music list, design/rythme/vibe knobs, render settings card (1080×1920, 30fps), 9:16↔16:9 frame swap, GPU chip + speedometer ×5, folder "01", SKILL.md code card, slash-command chip |
| **Captions** | Bottom of the panel, 2–4 words, white bold Arabic; Latin/tech words in **bold accent colour**; pop in word by word |
| **Palette** | Warm near-black brown background, terracotta/orange accent `#CF6F56`, cream text, soft orange glow and vignette |
| **Type** | Bold sans for captions, italic serif for accent words, tiny monospace labels (handles, step counters, metadata) |
| **Motion** | Cards slide and scale in, typing animations, counters, progress bars and waveforms; hard cuts between layouts on each beat |
| **Pacing** | The layout or the UI changes every 3–5s; one idea per beat; a hook in the first second |

## How it maps onto Oranuss
| His | Yours |
|---|---|
| Terracotta `#CF6F56` on warm brown | Neon purple `#8B5CF6` / `#5B2BE0` on deep navy `#140F2E` / `#100820` |
| Arabic-script derja captions | Latin Darija captions (your choice); Arabic script is possible as an option |
| Italic serif accent word | Keep the idea, but in your style: lavender `#E0C4FF` italic, or a purple highlight box |
| Glow orange | Neon purple bloom plus glass cards (already in your v2/v3) |

The new skills in `.claude/skills/` turn this into a repeatable workflow. Copy the techniques, not his exact graphics.

---
See also the batch-2 breakdowns: `BREAKDOWN_Dd69jHUR4mX.md`, `BREAKDOWN_DfHasR3Is5L.md`, `BREAKDOWN_Deu8ZBhoTdr.md`. Their techniques were added to the ui-demo-mockups, talking-head-layouts, kinetic-captions and reel-from-reference skills.
