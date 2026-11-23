# Oranuss video editing (folder map)

> Developed by Mehdi ORANUSS | Powered by Claude

Oranuss Academy videos (Moroccan Darija), edited with Claude Code: reels, YouTube intros and motion-graphics explainers.
**New here? Start with [GETTING_STARTED.md](GETTING_STARTED.md).**
**Another Mac?** `oranuss-editing-kit.zip` holds all skills, brand, fonts, styles and code; unzip it and follow its `INSTALL.md`.

```
editing-ai/
├── README.md                this map
├── GETTING_STARTED.md       setup for a new person + how to make a video
├── CLAUDE.md                house rules Claude follows in this folder
├── .claude/skills/          editing skills Claude uses (captions, motion, sound, layouts, review…)
│                            editing-craft = pro rules + approval gates (based on video-editor-skill by OTHMANZR)
├── brand/
│   ├── BRAND_CONFIG.md      Oranuss spelling, colours, type, logo rules
│   ├── logos/               official logos to use as-is (claude-logo-2023.png)
│   └── fonts/graphik-arabic/  Arabic font family (ttf, woff, woff2, stylesheet)
├── input/                   ORIGINALS, never edited or overwritten
│   ├── recordings/          camera footage (talking-head videos)
│   ├── voiceover/           voice-only audio for faceless videos
│   └── hook-videos/         hook clips to cut into reels
├── music/                   music beds
├── reference/
│   ├── styles/              one folder per look, split by format (see styles/README.md)
│   │   ├── long/            16:9 YouTube styles (purple-3d-glass, pastel-app-ui)
│   │   └── short/           9:16 Reels/TikTok/Shorts styles (purple-glass, premium-serif, dark-green, josephswork-blue-ui study)
│   ├── workflow/            breakdowns about process, not a look
│   └── skill-packages/      original skill downloads (.skill files and folders)
├── tools/earshot-0.4.0/     sound-effect bank (Python venv inside)
├── project/                 code that builds the edits
│   ├── motion.py            shared animation tokens (ease, pop, spring, press…)
│   ├── styles/              ffmpeg/ASS styles: base.py + one file per style
│   ├── build_*.py, intro_ai_*.py   one build script per video (see the table)
│   ├── hf/                  HyperFrames (HTML + GSAP) videos: generators, shared kit (hfkit.py), CSS, one project per video
│   ├── tools/ves/           our compiled macOS Vision helpers (cut-out masks)
│   ├── models/              whisper large-v3 model (2.9 GB, not in git, see GETTING_STARTED)
│   └── work/                generated files and caches per video (safe to regenerate); _archive/ = old frame grabs
└── output/                  one folder per video: previews, FINAL, captions, plans, words to confirm
```

## Videos

| Video | Style | How it is built | Latest file | Captions |
|---|---|---|---|---|
| YouTube intro "AI editing" (16:9, 1:54, talking head) | purple-3d-glass | `project/intro_ai_cut.py` → `project/intro_ai_audio.py` → `project/hf/gen_intro_ai.py` → `sh project/hf/intro-ai/render_final.sh` | `output/intro-ai/Intro-AI-Editing-FINAL-v2.mp4` (approved; same picture as FINAL with 56 OrcaXV SFX, built by `python3 -I project/intro_ai_sfx_orcaxv.py <version>`, cue sheet `sfx-cue-sheet-orcaxv.md`). FINAL.mp4 = first version with the earshot SFX. Real footage in split/circle layouts, Arabic keywords in Graphik Arabic | keywords only |
| AI training offer (16:9, 62 s, voiceover, 100% animation) | pastel-app-ui | `python3 -I project/build_ai_training_offer.py preview v<N>` (Arabic keywords, OrcaXV SFX, no music) | `output/ai-training-offer/AI-Training-Offer-16x9-PREVIEW-v1.mp4` | keywords only (Arabic) |
| AI Editing launch v2 (16:9, 60.5 s, voiceover) | purple-3d-glass | `project/hf/gen_ai_editing_v2.py` → render `project/hf/ai-editing-v2/` | `output/ai-editing/AI-Editing-16x9-PREVIEW-v2.mp4` | built in |
| SMM 10 scripts series, video 01 followers (9:16, 55 s, ElevenLabs Khalil voice + 1 Veo Lite clip) | purple-3d-glass | scripts `output/smm-10-scripts/SCRIPTS.md`; whisper → `project/smm_align.py` → `project/hf/gen_smm.py 01` → `project/audio_smm.py 01` → `hyperframes render` in `project/hf/smm01/` | `output/smm-10-scripts/01/SMM01-followers-PREVIEW-v1.mp4` | Latin Darija keywords built in |
| SMM 10 scripts series, videos 02–10 (9:16, 47–55 s each, white v2 look as approved 01 v2: Arabic captions, real photos p2–p4 + 1 Veo Lite clip from p1, quiet music) | smm white v2 | same pipeline, `gen_smm.py NN` (video02…video10, auto captions) → `audio_smm.py NN` → `hyperframes render` in `project/hf/smmNN/` | `output/smm-10-scripts/NN/SMMNN-<topic>-PREVIEW-v1.mp4` | PREVIEW only, waiting for user approval; assets used ~17.4k ElevenLabs credits (2026-11-21) |
| AI Editing launch v1 (16:9, 60.5 s, voiceover + music) | pastel-app-ui | `project/build_ai_editing.py` → `sh project/work/ai-editing/render_final.sh` | `output/ai-editing/AI-Editing-16x9-FINAL.mp4` (approved) | `output/ai-editing/captions-ai-editing-latin-darija.srt` |
| Oranuss intro (9:16, 5 s, macOS Majed voice) | purple-glass | `project/build_intro.py` → `sh project/work/intro/render_final.sh` | `output/intro/Oranuss-Intro-5s-FINAL.mp4` (approved) | title on screen |
| 650 reel (9:16, 42.6 s) | dark-green | `project/build_650.py` → `sh project/work/650/render.sh` | `output/650/Reel-650-PREVIEW-v2.mp4` | `output/650/captions-650-latin-darija.srt` |
| 1025 reel v2 (9:16, 35.6 s) | premium-serif | `project/build_1025_v2.py` (render command below) | `output/1025/Reel-1025-PREVIEW-v2.mp4` | `output/1025/captions-1025-latin-darija.srt` |
| 1025 reel v1 | purple-glass | `project/build_1025.py` | `output/1025/Reel-1025-PREVIEW-v1.mp4` | `output/1025/captions-1025-latin-darija-v1.srt` |
| 1025 7 s test | premium-serif | `project/build_7s.py` | `output/1025/Reel-1025-7s-premium-serif-v1.mp4` | none |
| IMG_2399 (16:9, 106.9 s) | purple-glass | `project/build.py` (self-contained, older) | `output/IMG_2399/Video-PREVIEW-v3.mp4` | `output/IMG_2399/captions-latin-darija-v2.srt` |

Words to confirm: `output/<video>/caption_uncertainties*.md`.
Missing sources: `IMG_2399.MOV`, `650.mp4` and `1025.mp4` are not in `input/recordings/`; put them back there before re-rendering those videos.

## Reference breakdowns (process)

- `reference/workflow/BREAKDOWN_process_DexY5nvJzhm.md`: a creator's "reel with Claude" process (find, analyse, brainstorm, build, save as a skill).
- `reference/workflow/ae-crypto-reels-masterclass.md`: a talking-head reel with three After Effects inserts (UI dashboard with cursor + growth graph, 3D glass box with extruded coin and reflection, frosted card with 3D coin) plus the sound design, mapped to HyperFrames, AE and OrcaXV IDs.

## Rules

- Every edit follows `.claude/skills/editing-craft/SKILL.md`: plan → script breakdown → stills → draft → final, the pre-show checklist and the social safe areas.
- Originals stay in `input/`; nothing there is changed.
- Every video uses one style from `reference/styles/long/` (YouTube) or `reference/styles/short/` (Reels); a new look gets a new style folder there.
- New video → new folder `output/<video-name>/`, versioned names (`-PREVIEW-v1`, `-v2`…). `FINAL` only after approval. Never overwrite a delivered file.
- Renders write to a temporary `rendering-*` file first and move into `output/` only when they succeed.

## Re-render the 1025 reel

```bash
cd project && python3 -I build_1025_v2.py
args=(); while IFS= read -r p; do args+=(-i "$p"); done < work/1025v2_inputs.txt
/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg -i ../input/recordings/1025.mp4 "${args[@]}" -/filter_complex work/filter_1025v2.txt \
  -map "[vout]" -map "[aout]" -t 35.6 -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 -c:a aac -b:a 192k -movflags +faststart \
  work/rendering-1025v2.mp4 && mv work/rendering-1025v2.mp4 ../output/1025/Reel-1025-PREVIEW-v2.mp4
```

## Sound effects (earshot)

```bash
cd tools/earshot-0.4.0 && PYTHONPATH=. .venv/bin/python -m earshot kit render ../../project/work/sfx/kit.json --out ../../project/work/sfx/kit
```

---

Developed by Mehdi ORANUSS | Powered by Claude
