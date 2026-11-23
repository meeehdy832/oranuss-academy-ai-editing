# Style: josephswork-blue-ui (Oranuss purple adaptation)

> Developed by Mehdi ORANUSS | Powered by Claude

Talking-head reel (9:16) that rotates four layouts every 2–6 s, with recreated app UIs on a bright stage. Adapted from the study of @josephswork (`README.md` here, Google Doc breakdown). Techniques only: his blue becomes Oranuss purple, and none of his graphics, words, figures or offer are reused.

- **Best for:** talking-head reels (offers, behind the scenes, "how we work", announcements), 45–90 s.
- **Engine:** HyperFrames (real footage inside a camera rig, like `project/hf/gen_intro_ai.py`) + OrcaXV SFX.
- **Videos made in this style:** IMG_2497 reel (`project/hf/gen_img2497.py`).

## Colours
| Token | Hex | Use |
|---|---|---|
| Stage | `#3B1FA8` → `#6D3BF5` radial, light rays from the top at 25 %, 1 px grid at 6 %, vignette | the graphic stage (his royal blue → our purple) |
| Card | `#FFFFFF`, radius 28, shadow 0 20 60 rgba(16,8,32,.28) | notifications, comment field, course card, price-free info cards |
| Dark label | `#100820` → `#5B2BE0` bottom gradient | course / topic labels on the stage |
| Glow | Neon `#8B5CF6`; green `#2DC58A` only for "done / money"; red `#FF4D5E` only for urgency circles | |
| Text | white on stage/footage, Ink `#100820` on white cards | |

## Layouts (1080×1920)
1. **Face full-frame**: camera punch-in 100 → 110 % on cuts inside a take.
2. **Split**: purple stage on the top 48 %, face below (re-framed so the head sits under the seam). The stage slides down from the top in 0.45 s ease-out while the face moves down blurred, then refocuses.
3. **Full stage**: the whole frame is the purple stage with a centred title and moving cards.
4. **Face + floating card**: one white card over the chest, 80 % width.
5. **Blurred face beat**: face defocused 20 px with one short caption on it.
Rotate them so the screen changes every 2–6 s; each graphic shows exactly the sentence being said.

## Captions (mixed)
- Arabic script in Graphik Arabic Semibold, with French/English terms (AI, editing, Oranuss Academy) in Latin as spoken.
- On the chest, y ≈ 62 % (under the chin), 2–5 words, max 2 lines, size 54–60 px.
- Word by word: upcoming words white at 40 %, spoken words white, the key word bigger in Graphik Arabic Bold (or Poppins ExtraBold for Latin).
- One accent word per line in neon purple with a soft glow (our version of his italic-serif accent; Latin accents may use an italic serif).

## Motion
- Cut-ins: the new shot starts blurred (14 px) and sharpens over 0.25 s.
- Cards: rise from below or slide from the side, 0.35–0.5 s expo.out, stagger 2–4 frames, motion blur while moving (blur 6 px on the move axis), tiny settle.
- Group exits: one eased move left/up, or a hard cut.
- UI recreations: typing letter by letter, cursor on an eased curve with hover scale 1.04 + glow, click squash.
- Thumbnail walls drift diagonally (linear), edges defocused.
- Counters only for numbers spoken in the video.

## Grade and sound
- Footage: lift contrast slightly, cool shadows, keep skin neutral-warm, light vignette.
- Voice cleaned (highpass, denoise, presence, compression); music from `music/` ≈ 20 dB under the voice, ducked; OrcaXV: whoosh on stage pushes, pops on cards, clicks/typing on UIs, ding on checks. −14 LUFS.

## Don't
- No blue, no copied UI text, no invented numbers or claims, no fake testimonials.
