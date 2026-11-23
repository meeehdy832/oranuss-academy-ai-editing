# Oranuss video editing: rules for Claude

Read `README.md` (folder map) and `brand/BRAND_CONFIG.md` before editing.

- Brand spelling is **Oranuss** (Oranuss Academy). Speech is Moroccan Darija; on-screen captions are Latin-letter Darija by default, Arabic script (Graphik Arabic, right-to-left) when asked. Keep French and English terms as spoken. Never invent words: unclear ones go to `output/<video>/caption_uncertainties*.md`.
- Follow `.claude/skills/editing-craft/SKILL.md`: ask questions, write a plan to `output/<video>/PLAN.md`, show stills, then a preview. Render `FINAL` only after the user approves a preview.
- Never change files in `input/`. Never overwrite a delivered file in `output/`; version up (`-PREVIEW-v2`…). Render to a temporary file, then move it into place.
- One style per video, from `reference/styles/<long|short>/<style>/STYLE.md`. Adapt reference techniques; never copy other creators' content or branding. Logos come from `brand/logos/`, never redrawn.
- Never invent numbers or claims; figures come from the speech or the user.
- Final resolution = source resolution (no upscaling footage). Audio −14 LUFS.
- Ask before big installs (models, toolchains) and before downloading other people's videos.
