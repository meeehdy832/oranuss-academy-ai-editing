---
name: editorial-ui-explainer
description: Plan, script, design and animate short vertical (9:16) "educational tips" videos in the editorial UI-explainer style, where a talking head alternates with a calm off-white "design board" and a fake cursor builds rounded UI elements, call-out lines and word-by-word mixed-font captions (sans + italic serif). Use when the user wants a reel/TikTok/Shorts in this style, a shot list, an animation spec, caption styling, a motion brief for an editor, or prompts for an AI video tool for this look.
---

# Editorial UI Explainer (short-form)

This skill reproduces a proven short-form format: **talking head (A-roll) + animated design board (B-roll)**. The video teaches a few numbered tips and *demonstrates* each one live on a minimal UI canvas.

Read `references/style-spec.md` for the exact design tokens and motion values. Read `references/production-guide.md` when the user wants to build the video themselves in a specific editor.

## What to produce

Ask only for what you cannot infer: **topic**, **number of steps (default 3)**, **brand colors (optional)**, **language**, and **the editing tool they use** (After Effects, Premiere, CapCut, Canva, DaVinci, or an AI video tool). Then deliver, in order:

1. **Script** (≤ 65 s spoken, ~150 words). Structure:
   - **Hook (0–8 s):** a pain-point + promise line. Pattern: "If your ___ still look like *this* in [year]… I'm about to make you a *Master* at ___ in under 60 seconds." Show a bad "before" example on screen.
   - **Step 1–3 (~15–18 s each):** "Step N: ___" title, one rule, one live demo.
   - **CTA (last ~6 s):** "If you want more ___, comment *[keyword]*." Show a mock comment box typing the keyword.
   - Mark the **one emphasis word per line** (it becomes italic serif) and the **bold keywords**.
2. **Shot list / timeline table:** time, A-roll or Board, the spoken line, on-screen visual, the animation event on each keyword, and the transition.
3. **Board animation spec** for each step: elements, the order they appear, positions (% of frame), easing and durations, all taken from `style-spec.md`.
4. **Caption spec:** the exact words, grouping and font role per word.
5. Optionally, **AI video prompts** or **After Effects build notes**, if the user asked.

## Non-negotiable style rules

- **Two scene types only:** dark talking head (captions white) and a light cream board (text navy). Alternate them every ~8–17 s.
- **60-30-10 color:** neutral/dark primary 60 %, light secondary 30 %, one saturated accent 10 %. A single warm "pop" element is allowed once.
- **Two typefaces:** a clean neo-grotesk sans (primary) and a high-contrast **italic serif** for one emphasis word per line. Tiny UPPERCASE tracked labels for metadata ("STEP 1").
- **One thing moves at a time.** Each new element arrives on its spoken keyword.
- **Every spawn has a spring overshoot. Every exit uses blur.** Lists, bars and lines are **staggered**.
- **A cursor drives the demo:** it moves to the object *before* the object reacts.
- **Annotations** are thin hairline call-out lines with a dot anchor and a small two-line label (value bold, descriptor small).
- **Big negative space:** centered single column, ~8 % side margins, captions on the A-roll at 58–64 % of frame height, nothing important in the bottom 12 %.
- **Callback:** reuse one element (for example, the accent swatch) in a later step so the tips feel like one system.

## Demo patterns you can reuse

Pick the one that fits each tip, or invent one in the same grammar:
- **Swatch → system:** spawn color squares, label them, morph them into a proportional bar chart.
- **Grid overlay:** draw dashed thirds/grid lines on a card, then snap objects onto intersections and step through layouts with a "‹ ›" control.
- **Before/after card:** a mock thumbnail or post card with call-outs explaining each part.
- **Font cycling:** a line of text rapidly swaps typefaces and lands on the chosen one, with a "PRIMARY · FONT NAME" label.
- **Drag-to-apply:** drag a swatch or style chip onto text and it recolors on drop.
- **Mock app UI:** a comment sheet, search bar or toggle that types or taps itself (great for CTAs).

## Output format

Use clear headings and tables. Give timestamps in seconds. Give colors as HEX. Give positions as % of a 1080×1920 frame. Keep all content original: never copy another creator's exact script, logo, or assets. Only the *style grammar* is reused.
