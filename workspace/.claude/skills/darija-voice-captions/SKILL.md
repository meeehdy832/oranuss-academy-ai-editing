---
name: darija-voice-captions
description: Create and audit timed Latin-Darija captions for mixed Moroccan Darija, French and English voiceovers, preserving the speaker's exact wording.
---

# Darija voiceover and captions

Developed by Mehdi ORANUSS | Powered by Claude

Use when the reel has recorded Moroccan Darija, often Latin Darija and French/English words.

1. Treat the **real voiceover** as the authoritative source of what was spoken; the UTF-8 script is the spelling reference, not proof that the speaker said every word.
2. Preserve Latin Darija, names and English/French product terms **exactly as supplied** (e.g., Claude Code, input, reference, output, motion graphics). Do not translate into MSA, French or English.
3. Measure the audio length first. Use locally available ASR/forced alignment where possible. If automatic timings are inaccurate, correct manually from playback/waveform; never state an unverified word timestamp is exact.
4. Produce a structured `captions.json` or `captions.srt` with accurate start/end seconds and text. Keep a separate `caption_uncertainties.md` listing mismatches to approve.
5. Chunk captions into short readable phrases (about 2–5 words where natural); avoid line breaks inside product names; no more than two lines at once. Timing should track speech; don't flash text faster than it can be read.
6. Visually emphasize relevant terms in brand accent color, sparingly. Use caption-safe areas above common platform bottom overlays, and verify that the always-on logo never clashes.
7. Test at three positions: early, middle and end of the audio; listen and confirm captions follow the *spoken* syllables, especially rapid Darija.
8. Do not time captions off silent gaps alone. Build scene changes around semantic words and precise audio timestamps.

If uncertain, flag the region instead of hallucinating a word.
