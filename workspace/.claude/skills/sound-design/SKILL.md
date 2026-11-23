---
name: sound-design
description: Voice polish, music bed and SFX for reels - whoosh on layout cuts, pop on chips, typing clicks on mockups, hit on keywords - mixed under the voice to -14 LUFS. Use once the visual beats are timed.
---

# Sound design

Developed by Mehdi ORANUSS | Powered by Claude

## Voice (always)
`highpass=80, afftdn=nf=-25, equalizer 3kHz +2dB, acompressor -20dB 3:1, loudnorm I=-14:TP=-1.5:LRA=9`, with 15–20ms fades at every cut.

## Rules from editing-craft
- At most 1 SFX per second; vary the takes, and pitch repeats 0.94–1.06 (done automatically in `dark_green`).
- Align each SFX's loudest moment to its cue (`place_sfx`).
- Voice target −14 LUFS integrated, true peak ≤ −1.5 dBTP.
- If the user wants music and SFX added in their own editor, deliver a voice-only master plus the cue sheet.

## Music
- With a licensed track: `python3 -I .claude/skills/video-editor-skill/scripts/mix.py --voice <render or source> --music music/<track> --bed-db -27 --sfx cues.json --out mix.wav --duration <s>`. It ducks with a voice sidechain (ratio 3, attack 40 ms, release 450 ms), fades in 0.6 s and out 1.8 s, and normalises to −14 LUFS. Then mux with `-map 0:v -map 1:a -c:v copy`.
- Use only tracks the user owns or has licensed (put them in `music/`, with the licence noted in the plan). If there's no music, render without it; never pull music from the web.
- Mix at about −24 to −28 LUFS under the voice; duck it with `sidechaincompress` keyed by the voice; fade in 0.5s and fade out 1.5s.

## SFX map (from the beat table)
| Event | Sound | Level |
|---|---|---|
| Layout cut / flash | short whoosh (150–300ms) | −18 dB |
| Chip / bubble pop | soft pop or click | −22 dB |
| Typing mockup | key clicks, one per 2–3 characters | −26 dB |
| Keyword hit / sparkle | shimmer or sub hit | −20 dB |
| Counter / progress | ticks, then a "done" ding | −22 dB |
"SFX on every word" (from the reference) means accent hits on keywords only, not every syllable.

## Sources
- Preferred: SFX files the user supplies in `music/sfx/` (licensed packs).
- Fallback, synthesised in ffmpeg (no licence issue):
  - whoosh: `anoisesrc=c=pink:d=0.3,bandpass=f=1200:w=800,afade=in:d=0.12,afade=out:st=0.12:d=0.18`
  - pop: `sine=f=900:d=0.06,afade=out:d=0.06`
  - tick: `sine=f=2000:d=0.015`
- Place each sound with `adelay=<ms>|<ms>` and mix everything with `amix=normalize=0`, then run loudnorm on the final mix.

## Voice from text (optional)
If the user wants AI voice (like ElevenLabs in the reference), it needs their own account and API key, which they enter themselves. Never clone someone else's voice. Their own recorded voice stays the default.

## QA
Listen at the start, the middle and the end. The voice must stay clear above the music and SFX, with no clipping (peak ≤ −1.5 dBTP) and no SFX landing on a spoken key word.

## earshot sound bank (installed: tools/earshot-0.4.0/.venv, Python 3.12, no torch or models)
The `sfx` and `kit` commands need no AI models. Render the launch kit once:
```
cd tools/earshot-0.4.0 && PYTHONPATH=. .venv/bin/python -m earshot kit init --preset launch -o ../../project/work/sfx/kit.json
PYTHONPATH=. .venv/bin/python -m earshot kit render ../../project/work/sfx/kit.json --out ../../project/work/sfx/kit
```
- Roles include tick, tock, pop, land, land.light, hit, snap (shutter), whoosh.short / long, swell, riser, bell (glock notes), text (pluck notes) and key. `kit.lock.json` holds each take's onset_s / peak_s and each role's offset_ms and min_gap_ms.
- **Placement (as in project/build_7s.py):** for whoosh and swell, the peak lands offset_ms after the cue; for every other role, the onset does. File start = cue + offset_ms/1000 − anchor.
- **Spacing:** keep the role's min_gap_ms (pops ≥ 114 ms apart, ticks ≥ 66 ms).
- **Where sounds go:** a whoosh when the plate blurs or a card group flies in; a pop on each card or badge; a tick on a chip or title; a snap on a punch-in zoom; a hit on a big number or diamond badge; land.light when the plate returns to sharp.
- **Levels:** effects at −6 to −11 dB under the voice chain, mixed before loudnorm (I=−14), so the voice stays dominant.
- Listening checks (`describe`, `critique`, `timeline`) need torch plus the ~1.1 GB models. Not installed: ask before installing them.
