---
name: kinetic-captions
description: Turn timed Darija transcripts into animated reel captions - 2-4 word pops, active-word purple box, tech/French/English keywords in accent, Latin-Darija by default or Arabic script on request. Builds on darija-voice-captions for the words and timing.
---

# Kinetic captions

Developed by Mehdi ORANUSS | Powered by Claude

1. Get the words and timings from `darija-voice-captions`: whisper.cpp large-v3 with `-l ar -ml 1 -sow`, then transliterate to Latin Darija, keeping French and English terms as spoken. Whisper snaps boundaries to whole seconds, so spread zero-length words and snap words that fall inside trimmed pauses to the next kept segment.
2. **Script choice:** Latin Darija (default for Oranuss) or Arabic script (like the reference). In Arabic script, keep Latin words (reel, Claude, motion, style, détails) in Latin letters, set them **bold in the accent colour**, and check right-to-left order on every chunk.
3. **Chunking:** 2–4 words, break after punctuation, merge one-word orphans, never split a product name; at most 34 characters per line.
4. **Style per word:**
   - default: white Demi Bold, soft dark halo;
   - active word: purple highlight box (BorderStyle 3);
   - **keyword list** (product, tool or tech words: Claude, reel, motion graphics, personal branding, social media, ElevenLabs, rendering, skill…): lavender or neon text even when inactive, plus a 1.1× scale while active.
4b. **Modes** (pick per beat):
   - *Chunk mode* (default): 2–4 words, with the purple box on the active word.
   - *Single-word mode* (cinematic beats, like reference Dd69jHUR4mX): one word at a time, smaller (56px), lavender or white, at chest height; no box.
   - *Two-tone mode* (like Deu8ZBhoTdr): white words; the keyword in neon `#8B5CF6` on its own; a Latin product name on a second line, bold.
5. **Entrance:** the chunk pops 88→100% in 110ms; optionally each new word slides up 12px.
6. **Placement:** 16:9 at the bottom (MarginV 80). 9:16 full-face: 300–420px from the bottom. 9:16 split: inside the panel, under the mockup.
7. Export both the burned-in ASS and a sidecar `output/captions-<lang>-vN.srt` for platform upload.
7b. **Timing rules (editing-craft):**
   - each word leads its timestamp by ~2 frames (`premium_serif.LEAD = 0.067`);
   - a caption's exit finishes before the next caption's first word (`dark_green.captions` checks this);
   - choose the caption zone per layout (chest under the chin, under a graphic, inside a panel).
7c. **Legibility:** on light clothing or paper, use a tight edge (`\bord2\blur1`) instead of a big soft halo, which shows as a dark blob. Arabic script: animate per word, never per letter, never letter-space, line height ≥ 1.2, and Latin words in their own left-to-right runs.
8. Every uncertain word goes to `output/caption_uncertainties.md`; never invent words.
4c. *Premium phrase mode* (premium-serif style, `project/build_7s.py`): 2–6 word phrases on 1–2 lines; regular sans plus **one heavy word** plus *one italic-serif lavender word* (Didot italic). Each word fades and blurs in (6 → 0) over 160 ms as it is spoken, and the phrase rises 18 px on an out-cubic. No karaoke box and no bouncy scale. A soft dark halo keeps it readable. Place it below the chin; check frames at every punch-in so it never covers the mouth.
