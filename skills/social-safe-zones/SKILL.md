---
name: social-safe-zones
description: Keep every word, face, logo and key graphic of a vertical 9:16 video (Instagram Reels, TikTok, YouTube Shorts) out of the areas the apps cover with their own buttons, username and caption. Gives exact pixel margins per platform on 1080x1920, overlay PNGs to check a frame, and a frame check with ffmpeg. Use for any reel/short/TikTok edit, caption placement, cover/thumbnail of a reel, or when the user says "safe zone", "text hidden by buttons", "المساحة الآمنة", "السيف زون".
---

# Safe zones for vertical video (1080 × 1920)

The apps draw their UI on top of the video. Anything important under that UI is lost.
Source of the margins: orsonlord.com, "Free safe zone overlays for Reels, TikTok and Shorts".

| Platform | Avoid top | Avoid bottom | Avoid left / right | Safe box (x, y, w, h) |
|---|---|---|---|---|
| Instagram Reels | 250 | 320 | 120 / 120 | 120, 250, 840 × 1350 |
| TikTok | 160 | 480 | 120 / 120 | 120, 160, 840 × 1280 |
| YouTube Shorts | 380 | 380 | 60 / 120 | 60, 380, 900 × 1160 |
| **Universal (default)** | **380** | **480** | **120 / 120** | **120, 380, 840 × 1060** |

**Default = Universal**, because one reel is usually posted on all three apps. Use a single platform's box only if the brief says the video is for that app only.

## Rules

1. **Hook text, keywords, numbers, logos, CTA:** inside the safe box. Centre them on x = 540 even on Shorts (the Shorts box is shifted left; centred text still looks right).
2. **Faces:** eyes around y 600–800 (upper third of the safe box), so captions and graphics can sit under the chin without covering the mouth.
3. **Background, footage, colour fills:** may cover the full 1080 × 1920. Only the *information* stays inside.
4. **Bottom area is busiest.** Caption, music line and buttons grow upward when the caption is long. Never put the key line in the bottom 480 px.
5. **Right edge:** like/comment/share column. Nothing readable in the right 120 px from y 900 down.
6. **Reel cover (Instagram grid):** the profile grid shows a 3:4 crop of the cover (centre 1080 × 1440, y 240–1680). Keep the cover title inside it *and* inside the safe box.
7. **Arabic (RTL) lines** take the same box; long Darija lines wrap to 2 lines max, 3–6 words each.

## How to check (every reel, before export)

Overlays in the kit: `safe-zones/safe-zone-{universal,instagram-reels,tiktok,youtube-shorts}.png` (transparent 1080 × 1920).

- In an editor (CapCut, Premiere, DaVinci, After Effects): put the PNG on the top track, check, then hide it before export.
- With code, test 3–5 frames (hook, every new text card, CTA):

```bash
ffmpeg -v error -ss 1.5 -i reel.mp4 -i safe-zones/safe-zone-universal.png \
  -filter_complex "[0:v]scale=1080:1920[v];[v][1:v]overlay" -frames:v 1 check_1.5s.jpg
```

Look at the picture: no word or face inside the red areas. Put the checks in one board for the user (one image, not many).

- In code that places text (HTML/Remotion/canvas), use constants instead of guessing:

```js
const SAFE = { x: 120, y: 380, w: 840, h: 1060 }; // universal
```

## Export (with the reel-export skill)
1080 × 1920, 30 fps, H.264 high, yuv420p, bt709, limited range, AAC, `-movflags +faststart`, audio about −14 LUFS.
Never stretch a 16:9 video to 9:16. Crop with the face kept inside the safe box, or place it on a background (see `reel-export`).
