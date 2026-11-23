---
name: orcaxv-sfx
description: Pick and place sound effects from the OrcaXV Essentials 100 (100 curated SFX bundled in this skill) for video edits: cue sheets with exact files and timings, or a rendered video with SFX mixed in.
---

# OrcaXV Essentials 100: sound effects for video editing

You are the sound designer. The user has a curated, level-matched set of **100 essential sound effects**, the **OrcaXV Essentials 100**. Your job is to pick the right sound for each moment of a video, say exactly where it goes and how loud, and, when you can reach the files, mix it into the video. Never suggest paid SFX apps or websites. Use only these sounds.

## Where the files are

**The 100 sounds are bundled inside this skill**, so it works anywhere, even without the user's Mac.

- Skill folder layout:
  - `sounds/<folder>/<ID> <Name>.mp3`: the 100 sounds (MP3 320 kbps, level-matched to about -2 dB peak), e.g. `sounds/01 Whoosh & Transitions/WH-174 Whoosh Fast 1.mp3`
  - `scripts/catalog.tsv`: the same list as below (columns `id folder name best_for dur_s peak_s shape level path`, with paths relative to `sounds/`)
  - `scripts/render_sfx.py`: mixes cues into a video. By default it reads sounds from the skill's own `sounds/` folder
- Find the skill folder at runtime: `SK=$(dirname "$(find / -path '*orcaxv-sfx/SKILL.md' 2>/dev/null | head -1)")`
- **Never invent file names: use only the IDs in the table below.**
- The user also has WAV masters (48 kHz/24-bit) of the same 100 sounds on their Mac at `/Users/Apple/Downloads/Thumbnails/OrcaXV Essentials 100` (same folder and file names, `.wav`), with `OrcaXV Essentials 100.html` to preview them. In cue sheets meant for their editor, name the file by folder/ID/name, which works for both.
- The full original pack (857 sounds) is only on their Mac at `/Users/Apple/Downloads/Thumbnails/OrcaXV SFX Pack`, with its own `_library/catalog.tsv`. Use it **only** if the user asks for something the 100 don't cover (horror ambience, weather, sword slices, meme voices) and the Mac is linked. In it, skip names marked `[UNCLEAR NAME - preview first]` and files tagged `compilation-multiple-sounds-in-one-file`.

**Columns:** `Peak s` = second where the sound is loudest, so line it up with the cut or word. `Shape`: `hit-first` (loudest at the start), `swells-middle` (rises, then hits), `builds-up` (loudest at the end, like a riser). `Level` = how loud it feels: loud, normal or quiet. It sets the default volume.

## The 100 sounds

### 01 Whoosh & Transitions

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| WH-174 | Whoosh Fast 1 | fast jump cut, quick swipe | 0.64 | 0.3 | swells-middle | loud |
| WH-175 | Whoosh Fast 2 | fast jump cut (soft, subtle) | 0.66 | 0.3 | swells-middle | quiet |
| WH-176 | Whoosh Fast 3 | fast cut, text whipping in | 1.32 | 0.5 | swells-middle | quiet |
| WH-012 | Whoosh Short Deep | short deep cut, punchy B-roll change | 0.92 | 0.34 | swells-middle | normal |
| WH-004 | Whip Micro | tiny whip, very fast cuts in reels, caption swaps | 0.31 | 0.06 | hit-first | normal |
| WH-156 | Whoosh Big 1 | big scene change, zoom transition | 1.54 | 0.7 | swells-middle | normal |
| WH-158 | Whoosh Big 2 | big scene change (softer) | 2.14 | 0.74 | swells-middle | normal |
| WH-013 | Whoosh Cinematic Flyby | cinematic fly-by, camera move, drone shot | 4.12 | 0.66 | hit-first | normal |
| WH-011 | Whoosh Sci-Fi Large | large sci-fi transition, intro/outro | 5.52 | 1.56 | swells-middle | loud |
| WH-163 | Whoosh Digital 1 | digital/tech slide-in, UI panel appears | 0.75 | 0.22 | swells-middle | loud |
| WH-166 | Whoosh Digital 2 | digital slide-in, graphic/text in | 0.72 | 0.26 | swells-middle | normal |
| WH-091 | Swoosh Small | small swoosh, light element moves | 0.55 | 0.24 | swells-middle | normal |
| WH-067 | Swoosh Reverse | reverse swoosh INTO a cut/reveal (sucks in) | 3.98 | 2.78 | swells-middle | normal |
| WH-132 | Whip | whip pan, fast camera whip | 2.93 | 1.1 | swells-middle | quiet |
| WH-062 | Whoosh Metal | metallic swoosh, sharp/aggressive cut | 3.81 | 0.44 | hit-first | loud |
| FI-009 | Whoosh Fire | fire swoosh, hot/fiery transition | 1.78 | 0.44 | hit-first | normal |

### 02 Impacts & Hits

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| IM-007 | Impact Deep | deep impact: title reveal, big statement | 7.99 | 0.16 | hit-first | loud |
| IM-003 | Impact Bass Drop | heavy bass drop: hook, beat drop, reveal | 4.24 | 0.18 | hit-first | normal |
| IM-016 | Impact Hard Cinematic | hard cinematic hit: dramatic reveal | 6.08 | 0.36 | hit-first | normal |
| IM-020 | Boom Cinematic | cinematic boom: trailer moment, big word | 3.11 | 0.24 | hit-first | loud |
| IM-012 | Impact Trailer Ring | ringing trailer hit: epic title card | 4.16 | 0.1 | hit-first | normal |
| IM-025 | Impact Bass | bass impact: punchy text slam | 4.9 | 0.28 | hit-first | loud |
| IM-029 | Impact Bass Drum | bass drum hit: number/stat slam | 5.64 | 0.08 | hit-first | normal |
| IM-033 | Punch | punch: hit, fight, strong point | 1.07 | 0.38 | swells-middle | loud |
| IM-023 | Slap | slap: comedic hit, wake-up moment | 0.94 | 0.48 | swells-middle | normal |

### 03 Risers & Cinematic

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| RS-006 | Riser Smooth | short smooth build (3s) into reveal | 3.18 | 2.92 | builds-up | normal |
| RS-012 | Riser Corporate + Hit | corporate rise + hit: product/logo reveal | 6.0 | 1.92 | swells-middle | normal |
| RS-021 | Riser Suspense | long suspense build (10s) | 10.06 | 3.6 | swells-middle | normal |
| RS-024 | Riser Classic | classic riser into a drop | 5.3 | 5.18 | builds-up | normal |
| RS-018 | Riser Reverse | reverse riser: dramatic build | 9.55 | 4.08 | swells-middle | quiet |
| RS-001 | Riser Cinematic Tension | cinematic tension build (18s), trailers | 18.25 | 7.96 | swells-middle | loud |
| CI-002 | Cinematic Hit A | cinematic hit/atmosphere, storytelling | 5.6 | 0.1 | hit-first | normal |
| CI-014 | Cinematic Hit B | short cinematic sting | 3.8 | 0.34 | hit-first | normal |

### 04 Pops & Dings

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| PO-006 | Pop 1 | pop: caption, emoji, sticker appears | 0.68 | 0.2 | swells-middle | normal |
| PO-008 | Pop 2 | pop variant 2 (alternate in lists) | 0.57 | 0.12 | hit-first | normal |
| PO-009 | Pop 3 | pop variant 3 (alternate in lists) | 0.57 | 0.1 | hit-first | normal |
| PO-022 | Pop Bubble | bubble pop-up: soft playful element | 2.5 | 0.8 | swells-middle | quiet |
| PO-003 | Pop Spring | spring pop-up: bouncy icon/sticker | 3.53 | 1.78 | swells-middle | quiet |
| PO-016 | Ting | ting: idea, tip, highlight | 1.2 | 0.28 | hit-first | quiet |
| PO-013 | Ding | ding: correct, good point | 3.45 | 0.42 | hit-first | normal |
| PO-019 | Ding Quick Win | quick win ding: small success | 1.95 | 0.16 | hit-first | normal |
| UI-041 | Highlight | highlight: text marker, emphasis | 1.0 | 0.48 | swells-middle | normal |

### 05 UI, Clicks & Typing

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| UI-019 | Click Soft | soft click: cursor click in screen recording | 0.47 | 0.04 | hit-first | quiet |
| UI-005 | Click Mouse | mouse click | 0.88 | 0.58 | swells-middle | quiet |
| UI-029 | UI Tap | UI tap: mobile app tap | 0.16 | 0.04 | hit-first | loud |
| UI-001 | UI Button | button/menu press | 1.7 | 0.02 | hit-first | quiet |
| UI-028 | Typing Typewriter | typewriter: title typed out | 4.06 | 1.64 | swells-middle | quiet |
| UI-004 | Typing Digital | digital typing: text appearing letter by letter | 4.28 | 2.66 | swells-middle | normal |
| UI-006 | Notification Phone | phone notification: message, DM | 4.32 | 0.58 | hit-first | normal |
| UI-025 | Notification Pop Up | notification pop-up: alert box, comment appears | 4.2 | 2.02 | swells-middle | normal |

### 06 Data & Glitch

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| DA-007 | Data Reveal | data reveal: chart/stat appears | 2.23 | 1.56 | swells-middle | normal |
| DA-001 | Data Digital Clicks | digital clicks: hacker/AI processing | 1.44 | 0.28 | hit-first | normal |
| DA-002 | Data System Online | system online: tech feature activated | 2.96 | 1.18 | swells-middle | normal |
| GL-002 | Glitch TV | TV glitch: glitch cut, AI/tech | 1.06 | 0.24 | hit-first | normal |
| GL-004 | Glitch Short | short glitch accent | 0.89 | 0.26 | swells-middle | loud |
| GL-010 | Glitch Hit | glitch hit: distortion transition | 1.07 | 0.24 | hit-first | loud |
| NG-004 | Censor Bleep | censor bleep: hide a word | 1.5 | 0.08 | hit-first | loud |

### 07 Camera & Time

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| CA-001 | Camera Shutter | camera shutter: photo, freeze frame | 0.6 | 0.16 | swells-middle | quiet |
| CA-010 | Camera Flash | camera flash: flash transition | 2.17 | 0.26 | hit-first | normal |
| CA-013 | Screenshot | screenshot | 1.95 | 1.14 | swells-middle | quiet |
| CA-015 | Flashback | flashback: going back in time | 4.41 | 2.34 | swells-middle | loud |
| EL-017 | Rewind Tape | tape rewind: rewind/undo moment | 5.11 | 1.3 | swells-middle | normal |
| TI-008 | Clock Ticking Fast | fast clock ticking: deadline, time pressure | 4.15 | 1.56 | swells-middle | quiet |
| TI-006 | Bell Boxing | boxing bell: round start, "let's go" | 1.62 | 1.16 | builds-up | loud |

### 08 Money & Wins

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| RW-020 | Cash Register | cash register: money, sale, price | 3.06 | 0.94 | swells-middle | quiet |
| RW-021 | Money | money sound: profit, earnings | 1.39 | 0.6 | swells-middle | quiet |
| RW-010 | Coin | coin: small gain, points | 3.19 | 0.08 | hit-first | quiet |
| RW-001 | Level Up | level up: achievement unlocked | 0.87 | 0.2 | hit-first | normal |
| RW-007 | Win Retro Ding | retro positive ding: unlocked, success | 0.84 | 0.14 | hit-first | loud |
| RW-006 | Win Skill Up | skill level up: progress, growth | 2.74 | 0.04 | hit-first | normal |
| RW-008 | Win Unlock | unlock: new feature/skill | 3.34 | 0.1 | hit-first | normal |

### 09 Wrong & Fail

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| NG-007 | Wrong Answer | wrong answer | 1.54 | 0.32 | hit-first | loud |
| NG-011 | Wrong Buzzer | wrong buzzer: big mistake | 3.06 | 0.66 | hit-first | loud |
| NG-008 | Denied | denied: rejected, blocked | 2.72 | 0.84 | swells-middle | loud |
| NG-006 | Fail | fail sound: epic fail | 3.81 | 0.64 | hit-first | loud |
| NG-010 | Error Windows | Windows error: tech fail, meme | 1.04 | 0.34 | swells-middle | loud |

### 10 Funny & Reactions

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| FN-037 | Badum Tss | ba-dum-tss: after a joke | 2.14 | 0.46 | hit-first | normal |
| HO-021 | Awkward Crickets | crickets: awkward silence, no reaction | 4.47 | 3.7 | builds-up | loud |
| NG-009 | Wah Wah Fail | wah wah wah: sad fail | 8.28 | 0.64 | hit-first | normal |
| FN-036 | Anime Wow | anime wow: amazement | 4.18 | 0.34 | hit-first | normal |
| FN-040 | Cartoon Accent | cartoon accent: funny movement | 3.07 | 0.94 | swells-middle | normal |
| FN-069 | Record Scratch | record scratch: "wait, what?" freeze moment | 5.13 | 0.82 | hit-first | normal |
| CR-013 | Crowd Ooh | crowd oooh: impressive/shocking | 2.22 | 1.02 | swells-middle | normal |
| CR-006 | Crowd Aww | crowd aww: cute or sad moment | 2.01 | 0.5 | hit-first | normal |
| CR-008 | Crowd Clap | clapping: applause, well done | 2.32 | 0.18 | hit-first | quiet |
| CR-004 | Crowd Cheer | kids cheering: celebration | 4.23 | 1.78 | swells-middle | loud |

### 11 Suspense

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| HO-013 | Dun Dun Dun | dun dun dun: dramatic twist | 3.08 | 1.28 | swells-middle | loud |
| HO-018 | Suspense Sting | suspense sting: mystery moment | 1.83 | 0.8 | swells-middle | loud |
| HO-008 | Heartbeat | heartbeat: tension, fear, nervous | 8.57 | 7.24 | builds-up | loud |
| HO-027 | Suspense Panic | panic suspense: something bad coming | 3.53 | 2.62 | builds-up | loud |

### 12 Explosions & Elements

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| EX-009 | Explosion Short | short explosion: mind blown | 1.36 | 0.18 | hit-first | quiet |
| EX-012 | Explosion Big | big explosion: huge reveal | 2.57 | 0.22 | hit-first | loud |
| EX-002 | Debris Impact | debris impact: crash, break | 1.1 | 0.16 | hit-first | normal |
| EL-006 | Electric Zap | electric zap: energy, power on | 1.37 | 0.22 | hit-first | quiet |
| EL-012 | Liquid Splash | liquid splash: drink, water, product | 1.54 | 0.34 | hit-first | normal |

### 13 Paper & Logo

| ID | Name | Best for | Len s | Peak s | Shape | Level |
|---|---|---|---|---|---|---|
| PA-002 | Paper Flip | paper flip: page turn, next point | 0.93 | 0.2 | hit-first | quiet |
| PA-008 | Paper Crumple | paper crumple: throw away a bad idea | 1.84 | 0.64 | swells-middle | quiet |
| PA-005 | Pencil Writing | pencil writing: notes, checklist | 1.88 | 1.16 | swells-middle | normal |
| LO-003 | Logo Stomp | logo stomp: brand reveal | 4.44 | 0.94 | hit-first | loud |
| LO-002 | Logo Reverse Assembly | logo reverse assembly: logo builds up | 3.28 | 1.46 | swells-middle | normal |

## Workflow

1. **Understand the video.** Find out what happens and when: the cuts, the text on screen, the key words, the jokes, the reveals.
   - If you have the video file: find cuts with
     `ffmpeg -i in.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep -o "pts_time:[0-9.]*"`
     and look at frames around key moments (`ffmpeg -ss T -i in.mp4 -frames:v 1 f.jpg`).
   - For speech, use a transcription tool if one is available. Otherwise ask for the script or the timestamps of the key lines.
   - With only a script or a description, work from the times the user gives.
2. **Choose the moments.** Not every cut needs a sound (see density rules).
3. **Choose each sound** from the table above. Match the "Best for" column, the length and the shape to the moment.
4. **Always give a cue sheet:**

   | Time | ID | Sound (folder / file) | Align | Volume | Why |
   |---|---|---|---|---|---|
   | 00:03.20 | WH-174 | 01 Whoosh & Transitions / WH-174 Whoosh Fast 1 | peak on cut | -8 dB | jump cut to B-roll |

   Align: **peak** = the loudest point lands on the time (whooshes, impacts, rise-and-hit). **start** = the sound begins at the time (pops, clicks, dings). **end** = the sound finishes at the time (pure risers into a reveal).
   For Premiere, CapCut or DaVinci, also give **"place clip at"** = time minus `Peak s` (for peak alignment). `render_sfx.py --sheet` calculates it.
5. **Render** whenever you have the video (the sounds are always available in the skill):
   - Write `cues.json`: `[{"t": 3.2, "id": "WH-174", "align": "peak", "gain_db": -8, "note": "jump cut"}]`
   - Run `python3 "$SK/scripts/render_sfx.py" --video in.mp4 --cues cues.json --out in_sfx.mp4` (add `--sheet` to only print the cue sheet with "place clip at" times)
   - Work on a copy of the user's video and deliver the result as `<name>_sfx.mp4`. Never overwrite the original.
   - To also hand the user the chosen sounds as files, copy them out of `$SK/sounds/`.
6. **Check it:** run `ffmpeg -i out.mp4 -af volumedetect -f null -`. Max volume should be at or below about -1 dB, and no sound should cover a key spoken word.

## Placement rules (how a pro editor does it)

- **Whoosh on transitions:** the peak goes exactly on the cut frame. Use micro/fast (WH-004, WH-174–176) for jump cuts and big/cinematic (WH-156, WH-013, WH-011) for scene changes. WH-067 (reverse) goes INTO a cut.
- **Impact on reveals:** the hit lands on the frame where the title, number or key word appears. For extra power, put a riser that ENDS there (`align: end`) together with an impact (`align: peak`) at the same time.
- **Pops/dings on on-screen elements:** one per element, `align: start`. In lists, rotate PO-006 → PO-008 → PO-009 so it doesn't sound robotic.
- **UI clicks:** sync to the visible cursor click.
- **Comedy:** the funny sound comes right AFTER the punchline or reaction, never over the words. Use them rarely.
- **Under voice:** the voice is king. Keep SFX about -6 to -12 dB under speech, and use loud impacts in gaps between words. Default gain is loud -8 dB, normal -5 dB, quiet -2 dB.
- **Variety:** don't reuse the same ID within ~20–30 s if a sibling exists (e.g. alternate WH-174/175/176).
- **Silence is a tool:** a beat of nothing before a big reveal makes the hit land harder.
- **Density by style:**
  - Reels/TikTok/Shorts: a sound every 1–3 s is normal (whoosh on cuts, pop on captions/emoji, impact on the hook)
  - Talking-head YouTube: only B-roll transitions, text pop-ups, key stats, jokes
  - Corporate/product: digital whooshes, soft pops, RS-012 corporate rise + hit, UI sounds. No meme sounds
  - Cinematic/storytelling: risers, deep impacts, CI-002/CI-014, fewer and bigger sounds
  - Gaming/funny: folders 08, 09 and 10 are welcome

## Talking to the user

- Name sounds by ID **and** name, for example "`WH-174` Whoosh Fast 1", so they can find them in the folder or the HTML page.
- If they don't like a sound, offer 2–3 alternatives from the same folder with a similar length and shape. If none fit, search the full pack's catalog.
- To add sounds, they need a new version of this skill: put the file in the right numbered folder as `<PREFIX>-<NNN> <Name>.mp3`, add its row to `scripts/catalog.tsv` (ffprobe for duration, an RMS scan for peak_s) and to the table above, then re-upload the skill.
