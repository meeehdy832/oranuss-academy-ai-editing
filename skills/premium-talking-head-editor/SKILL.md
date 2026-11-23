---
name: premium-talking-head-editor
description: Edit raw talking-head or podcast clips into premium vertical 9:16 short-form videos (minimal podcast style: gold/warm palette, thin+bold captions, tracked-selector B-roll, cream full-screen animations, sound design). Use when the user wants a talking-head video edited, montaged or "tmonta" in this style.
---

# Premium Talking-Head Editor

Turns a raw talking-head / podcast clip into a premium vertical short (Instagram Reels / TikTok / Shorts) in the "minimal podcast" style reverse-engineered from Joseph's video (see `references/full-analysis.md`, and `examples/` for real frames).

The user speaks Moroccan Darija; talk to them in Darija. On-screen text stays in the language of the clip unless they ask otherwise.

## Golden rule
**The human plans, the AI executes.** Never jump from raw clip to final edit. Always stop at the planning document and the caption sheet for the user's approval. With no reply, take the most reasonable plan, say so, and continue.

## Pipeline (follow in order, with a checkpoint at each ★)

### 1. Prep the raw clip
1. Word-by-word transcript with start/end in ms (`scripts/transcribe.py`, faster-whisper; keep Darija/Arabic/French as spoken).
2. Frame-by-frame breakdown: shot changes, who is speaking, framing.
3. Cut silences, filler and false starts (`scripts/cut_silences.py`). Target ~60 s unless the user says otherwise. Keep 80–120 ms of breath on each side of a cut.
4. Reframe to 9:16 1080×1920: track the speaker's **nose** (`scripts/reframe_9x16.py`, MediaPipe) and keep it on the vertical center line, smoothed so the crop never jitters; reset on hard cuts.
5. Re-transcribe the cut so timings match the new clip.

### 2. ★ Planning document
Build it as an HTML page (or doc) with:
- **The look:** 4 palette options extracted from the footage (see Color system) + 3 font-family options (sans only / sans+serif / serif only). Recommend one.
- **The cut, line by line:** numbered lines `L01 0.00–2.62s` with the text and a speaker thumbnail on the right; on the left an empty "What goes on screen?" box.
- Pre-fill each box with your **suggested** scene type (see Scene selection), clearly marked as a suggestion, so the user only edits what they disagree with.
Then a **timeline view**: one card per line, tagged `A-roll` / `B-roll + selector` / `B-roll + graphics` / `Full-screen: <type>` / `Illustration`.
Wait for the user's plan.

### 3. Assets
From the approved plan, list every asset needed: Images · Illustrations · B-roll · Icons, each with a search phrase. Collect from free-licence sources (Pexels, Pixabay, Unsplash) or generate (image/video generation tools if connected). Save to `assets/` with a manifest (source URL + licence).

### 4. ★ Captions first
Build every caption page and render a **caption design sheet** (grid of stills, each labelled with line id, time and text). Send it and wait for fixes.

### 5. Scenes, one by one
Build each designed scene in the order of the timeline. Send a still or a short preview for each. Recommended engine: **Remotion** (React, 30 fps, 1080×1920); ffmpeg for compositing and the final mux. Keep every scene as its own component so it can be redone alone.

### 6. Final render
Assemble at 1080×1920, 30 fps, H.264 high quality, AAC 48 kHz, voice at about -14 LUFS integrated. Send the export for review.

### 7. ★ Sound design + music
1. Write a **sound audit** table: `Time | What happens on screen | Sound effect | dB` (the reference edit had 85 cues for 60 s). Rules in `references/full-analysis.md` part 4. Use the user's SFX library if one exists (e.g. the `orcaxv-sfx` skill / OrcaXV Essentials).
2. Propose 10 music tracks with 10-second previews; the user picks one.
3. Mix: music ducked under voice (about -22 to -26 dB under speech), music drop on the first cut to the second speaker or the first big hook word. Render the master.

## Style rulebook (short version; details in references/full-analysis.md)

### Color system
1. Collect accent colors visible in the raw footage (shirt, lamp, window, wall).
2. Pick one accent. Derive: **vibrant** version (e.g. gold `#F2E186`), **dark rich** version (e.g. orange-brown `#8E4A2B`), **white tinted** toward the accent (e.g. `#F6EBE2`), **black tinted** toward the accent.
3. Usage: A-roll = dark footage, thin text white, special word vibrant. Full-screen scenes = tinted-white (cream) background, shapes/pills/circles in the dark rich color. B-roll = darkened footage, special word vibrant or white.
Preset palettes: Gold + dark orange (default), Green + cool grey, Oxblood + peach, Gold + light.

### Typography
- One family only. Default sans: PP Neue Montreal → fallback Urbanist / Inter. For Arabic text: a matching geometric sans (e.g. IBM Plex Sans Arabic, Tajawal).
- Thin text 300–400 weight, small. Special word 600–700, 2–3× the size of the thin text.
- Page pattern: small thin lead-in line above, big bold colored keyword below, optional small tail line under it at the right ("for two reasons").

### A-roll and captions
- Speaker in the upper half, captions in the lower half (about 60–75% of the height), left-aligned block.
- **Hook** (every time a new speaker first appears): the most attractive phrase (negative word or big question) in the special style; white **name card** bottom-left (name in black on a white box + a small role line under it). Letters glitch in and glitch out.
- Body: 6–8 words per page, exactly one special word per page.
- Transitional lines ("what does that mean?"): small thin text, no special word, punch-in (about 115–125%) on the face.
- Occasionally one small word beside the speaker as a bridge.

### Scene selection (what the speaker says → scene)
| Speaker is… | Scene |
|---|---|
| introducing themself / a big question | Hook A-roll + name card |
| naming a group, behaviour, example | B-roll still/clip + **tracked selector box** (thin white box with corners) + curved arrow + small label; several stills with a pan and a camera-shutter cut |
| one concept / object | **One object centered**: object in a circle or card, cast shadow, depth arcs in the corner, serif or bold caption |
| comparing two things / one thing + explanation | **Two object alignment**: object one side with a cast shadow, text the other side; or text on top + design element filling the lower third up to the center |
| numbers going up/down | **Graphs & numbers**: line graph centered with text around, or bar graph in the lower half with clean text above |
| an experience / something to see | **Real elements**: real photos snapped onto cream background with a clean stroke, or split layout with text in the middle |
| an abstract idea ("you can learn to focus") | **Illustration** on cream: thin lead-in + bold word in a filled dark-rich box + illustration in a circle |
| a metaphor (sleep, clouds, sky) | composite B-roll (subject cut out on a fitting background) + thin text |
| a problem stated early and solved at the end | **Callback**: build the problem scene (e.g. molecules under a "Threshold" line), then reuse it at the end with the solution (molecules breaking through with light trails) |

### Recurring design DNA
Cream backgrounds · thin brown arcs/rings in a corner · long soft cast shadows · vertical light/blur columns under objects · circles in the dark rich color holding small 3D objects · dark pill + dotted line labels · thin gold ring around a B-roll subject · filled color box behind a key word · vignette (darken + blur) on all edges · rough film texture on B-roll · serif caps for cinematic text on images.

### Rhythm
- New scene every 2–3 s (about 25 scene changes in 60 s).
- Alternate A-roll ↔ designed scene; designed scenes in a row only when they belong to one idea.
- Assets serve the exact word: "sleep" → clouds, "exercise" → gym, "hard training" → boxing.

### Motion
- Text: glitch-in for hook words; mask-rise (word rises 20–30 px out of a baseline clip over about 8–10 frames) for body words; boxes wipe left→right behind words over about 7 frames.
- Objects: pop-in with a small overshoot (scale 0.8 → 1.04 → 1.0 over about 10–12 frames), staggered 4–6 frames apart.
- Camera: slow push-ins on full-screen scenes; pans between stills with a whoosh peaking on the cut.
- Ease: ease-out (cubic or expo) for entrances, ease-in for exits; no linear moves except light trails.

### Sound rules
Special word → pop / UI notification. Normal page → soft click or nothing. Glitch text → micro-glitch / tiny mechanical clicks. Whoosh peaks exactly on the cut. Camera shutter on still-image pans. Name card → soft round pluck. Music drops on the first speaker change. SFX levels between -9 and -19 dB (pop about -11, click about -14, whoosh about -11 to -17, music cue about -19).

## Files
- `references/full-analysis.md`: complete breakdown (full video map, the 14 animation categories with counts, the final edit second by second, the sound audit, ready prompts).
- `examples/`: real frames of every scene type, the planning doc, the caption sheet and the sound audit.
- `scripts/`: prep helpers (transcribe, cut silences, reframe 9:16 with nose tracking). Run with `python3 scripts/<name>.py --help`.

## Honest limits
Animation timings above are estimates from stills and the visible breakdown notes, not measured from the original project files. Check fonts' licences before using commercial fonts like PP Neue Montreal.
