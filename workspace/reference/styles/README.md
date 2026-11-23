# Styles

Each folder is one look. Every video uses exactly one style.

Styles are split by format. Pick from `long/` for YouTube videos and from `short/` for Reels, TikTok and Shorts.

### long/ (16:9 YouTube: intros, explainers, launches)
| Style | Look | Used in |
|---|---|---|
| [purple-3d-glass](long/purple-3d-glass/STYLE.md) | the user's 20-tile style board: frosted glass, glossy 3D purple objects, glow, isometric devices, parallax; built in HyperFrames | YouTube intro "AI editing", AI Editing launch v2 |
| [pastel-app-ui](long/pastel-app-ui/STYLE.md) | light 16:9 explainer from mobile-app UI pieces: white cards, phone mockups, pastel tiles, rings, bars, purple accents | AI Editing launch v1, AI training offer |

### short/ (9:16 Reels, TikTok, Shorts)
| Style | Look | Used in |
|---|---|---|
| [purple-glass](short/purple-glass/STYLE.md) | bright neon glass, purple caption box, many icons, split layout (also used once in 16:9: IMG_2399) | 1025 v1, IMG_2399 |
| [premium-serif](short/premium-serif/STYLE.md) | dark and moody, bold and italic-serif captions, background blur, diamond badges | 1025 v2, 1025 7s test |
| [dark-green](short/dark-green/STYLE.md) | premium-serif layout in emerald and mint, frosted lower panel, checklist tracker, social safe zones | 650 |
| [josephswork-blue-ui](short/josephswork-blue-ui/README.md) | study only (no STYLE.md yet): dark studio talking head + royal-blue UI stage, split screens, word-by-word captions with italic-serif accent | not used yet |

## Folder layout
```
long/ or short/
└── <style-name>/
    ├── STYLE.md      the recipe Claude follows: colours, type, captions, layouts, graphics, motion, grade, sound, don'ts
    ├── examples/     reference reels and images for this look
    └── breakdowns/   BREAKDOWN_*.md notes written from those examples
```
Code for each style is in `project/styles/<style_name>.py`. Everything shared by all styles is in `project/styles/base.py`.

## Picking a style for a video
Say it with the request, for example "edit 1025 in premium-serif". The style is recorded in the main `README.md` video table.

## Adding a new style
1. Make `reference/styles/<long|short>/<new-name>/examples/` and drop the reels or images there.
2. Claude writes the breakdowns into `breakdowns/`, then `STYLE.md`, then `project/styles/<new_name>.py`.
3. Claude makes a ~7s test so you can approve the look before a full video.
