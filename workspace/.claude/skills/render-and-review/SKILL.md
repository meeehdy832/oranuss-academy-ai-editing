---
name: render-and-review
description: Review, debug and export a faceless motion-graphics Reel as an MP4 while protecting originals and checking caption, audio, branding and privacy quality.
---

# Rendering and QA

Developed by Mehdi ORANUSS | Powered by Claude

0. Follow the approval gates, pre-show checklist and pitfalls in `editing-craft` (plan → script breakdown → stills → draft → final). Final resolution = source resolution; never upscale.
1. Confirm video duration follows input voiceover; vertical 1080x1920; 30fps; H.264 MP4; suitable AAC audio if available.
2. Render first draft to `output/Reel-PREVIEW-v1.mp4`. On failure, report actual error and fix; do not claim success without verifying file and ffprobe metadata.
3. Check frames near every scene boundary, and opening/middle/end. Watch for text collisions, tiny font, incorrect aspect-ratio crops, flickers, broken gradients, missing logos and unmapped recordings.
4. Audit on-screen words against the **recorded** audio and provided script. Read and flag uncertain Latin Darija terms, dates or app interface terms. Validate SRT/JSON segments are ordered and have positive durations.
5. Privacy: inspect recordings for account names, emails, profile photos, addresses, personal chats, notifications. Crop or mask if necessary; do not rely on rough crop guesses.
6. Listen for clipped voice, too-loud music/SFX, unintended silence and abrupt tails. Fade SFX/music without clipping the voiceover.
7. Record a short issue list and the preview path. Only render `output/Reel-FINAL-v1.mp4` when the user explicitly approves the preview.
8. Never overwrite earlier renders: version increment on revision; preserve original source assets and editable project files.

Paths: every `output/...` file above lives in that video's own folder, `output/<video-name>/` (for example `output/1025/Reel-1025-PREVIEW-v2.mp4`). Partial or test renders go to `project/work/`, never `output/`.
