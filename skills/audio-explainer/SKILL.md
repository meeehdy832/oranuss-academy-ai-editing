---
name: audio-explainer
description: Turn a voice-over / audio (Darija, Arabic, French, English) into a full YouTube explainer video in the documentary style the user approved (charcoal + one accent colour, Cairo font, flat white pictograms, white labels on footage, ~50% animation / 50% high-res photos + HD clips, idea animations, punch-in rhythm, sound effects, -14 LUFS), built in Remotion with ready scripts so it costs few tokens. Use when the user gives an audio or a BRIEF and wants a video from it, "audio to video", "explainer from my voice", "اصاوب فيديو من هاد الأوديو".
---

# Audio → explainer video (token-lean)

Everything heavy is already written: the engine (`template/`), and scripts that print **one line**. Your job is
mostly **data**: `plan.json` (scenes) and `fx_plan.json` (idea animations). Never rewrite the engine for a video.

`S` = this skill folder · `R` = the Remotion project (default `/Users/Apple/Downloads/motion-graphics-skills-main/remotion-studio`)
· `W` = this video's work folder (`<project>/output/<video-name>/`).

## Token rules (follow all of them)

1. **One video = one fresh session.** If this session already holds other work, tell the user to start a new one and paste the BRIEF there.
2. **Brief first.** Read the user's BRIEF (template: `S/BRIEF.md`). Missing fields → use the defaults written there; ask at most ONE question, only if the audio path or the brand is missing.
3. **Read compact files only:** `W/transcript_20s.txt` (never `words.json`), `W/text_audit.txt`. Scripts already print one line — add `| tail -3` to any other command that can be long. Never dump logs.
4. **Few, small images.** One stills board for approval (`stills.sh`, ≤ 8 frames, one image), one media sheet (`fetch_media.py`), one final sheet. No browser screenshots except when picking Pinterest cutouts.
5. **Media search:** fill `window.__Q` and run `S/scripts/pexels.js` in ONE JavaScript call on pexels.com, read `__res` in a second call. For > 30 queries, or if the browser is busy, delegate the search to a subagent (cheaper model) that returns only `media_candidates.json`.
6. **Write data, not code.** Only `plan.json`, `fx_plan.json`, small edits. If a scene type is missing, add it to the engine ONCE in `S/template/` (then it exists for every next video).
7. **Two approval gates only:** (a) one stills board after the plan is built, (b) the final video. Everything else runs without asking.
8. **Long jobs in the background** (`finish.sh` ≈ 25–45 min for 16 min of video). Don't poll; wait for the notification.

## Workflow

```bash
S=~/.claude/skills/audio-explainer/scripts; R=…/remotion-studio; W=…/output/<video-name>
bash $S/transcribe.sh "<audio>" $W            # ~2 min for 16 min audio → transcript_20s.txt
```
1. **Read `transcript_20s.txt`** once. Note the 5–8 key ideas, every number actually said, and the words he uses.
2. **Write `$W/plan.json`** (schema below). One scene every **4–7 s**; key ideas get a diagram (`flow`, `equation`, `bars`, `chain`)
   or an idea animation; long explanations alternate graphic ↔ media. Target the brief's mix (default 50/50 by time).
   `python3 $S/build_beats.py $W` → fix what it reports (long > 14 s → split or `fill` media; short < 3 s → merge).
3. **Text check:** `python3 $S/text_audit.py $W`, read `text_audit.txt`, fix. **Only words he clearly says.** Unclear → remove (icon only).
   Never write a number he doesn't clearly say. French/English loanwords in Latin, Darija in Arabic. No subtitle bar.
4. **Idea animations (optional, recommended for 6–12 key moments):** write `$W/fx_plan.json` `{ "<beat index>": [ {fx} ] }`,
   kinds in `template/IdeaFx.tsx` (`chips stamp count calendar clock tags receipt line scale domino flow globe meter ring`, `pos: left|right|full`,
   `cue: "spoken word"`), then `python3 $S/cue_fx.py $W $W/beats.json`.
5. **Media:** queries in English, concrete (`"judge gavel"`, `"man working late laptop"`). Photos for places/objects, clips for people/actions.
   Save `__res` as `$W/media_candidates.json` → `python3 $S/fetch_media.py $W $R` → look at `media/sheet.jpg` once → swap off-topic ones with
   `--pick name=2`. Photos are 2400 px (never use < 1920 px). No brand logos, no real famous people.
6. `python3 $S/icons.py $W $R` → `bash $S/setup.sh $R $W "<BRAND>" "<#accent>" "<audio>"`.
7. **Stills board:** `bash $S/stills.sh $R $W/board.jpg <6–8 times in seconds covering each scene type>` → send to the user → wait for OK.
8. **Final (background):** `bash $S/finish.sh $R $W <name>` → render + 300+ SFX on animation frames + mix (voice to −16 LUFS, master −14 LUFS,
   TP ≤ −1) + sheet. Check `final-sheet.jpg`, send the file. > 30 MB can't reach the phone; say so.

## plan.json (scenes)

```json
{"duration": 972.9, "audio": "audio/voice.m4a", "beats": [
 {"anchor": "حرية", "near": 31, "type": "title", "icon": "money_with_wings", "title": "كيفاش نوصلو للحرية المالية؟", "sub": "…"},
 {"anchor": "غاراج", "near": 204, "type": "image", "img": "img/garage.jpg", "title": "غاراج كتكريه لشركة"},
 {"anchor": "الدماغ", "near": 42, "type": "video", "video": "vid/v_brain.mp4", "title": "الدماغ كيتحبس"},
 {"t": 78, "fill": true, "type": "image", "img": "img/chess.jpg", "title": "القوانين"}
]}
```
Types and fields: `title` (icon, title, sub) · `quote` (icon, title) · `icons` (title, items[{icon,label,sub}] 2–4) · `steps` (title, icon, items[{label}])
· `stat` (value, prefix, suffix, sub, icon, title — **only numbers said**) · `vs` (title, left{icon,label,sub}, right{…}; right = the good one)
· `image` (img, title) · `video` (video, title) · `cutout` (img PNG, title, sub) · `flow` (title, rows[{a,mid,b,note}] — what feeds what)
· `equation` (title, left, right, result — left bar grows past right) · `bars` (title, a{label,sub}, b{label,sub} — flat vs rising line)
· `chain` (title, label, n — compounding). Icons = Fluent emoji names in snake_case (`money_bag`, `house`, `key`, `chart_increasing`…).
Media keys: `img/<name>.jpg` ↔ `media_candidates.photos.<name>`, `vid/<v_name>.mp4` ↔ `media_candidates.videos.<v_name>`.

## Look (already built into the engine)
Charcoal-navy background with moving rings/squares/dot grid, brand name centred on top, accent colour labels, punch-in "cut" every 2.5 s,
icon pop on every photo/clip, words reveal one by one, scenes cut in 6 frames. Change the look only if the brief asks.

## Rights
Pexels photos/clips: free licence, fine for monetized YouTube (credits kept in `media/credits.json`). Pinterest only for cutout objects,
and say they belong to their owners. Fluent icons: MIT.
