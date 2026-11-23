---
name: video-project-setup
description: Prepare a safe Claude Code workspace for faceless educational reels, inspect assets, check tools, and make a production plan before editing.
---

# Setup and asset inventory

Developed by Mehdi ORANUSS | Powered by Claude

Use when starting a video project or troubleshooting missing assets and dependencies.

1. Confirm the current working directory, then list input/, reference/, brand/, music/, output/, input/recordings/ if present. **Never switch projects silently.**
2. Do not delete or overwrite originals. Store generated code in `project/` and reviews and exports in `output/` with versioned names. Each video gets its own folder, `output/<video-name>/` (for example `output/1025/`), holding its previews, captions, uncertainties and plan. Folder map: `README.md` at the project root. Each video uses one style from `reference/styles/` (its `STYLE.md` is the recipe, `project/styles/<style>.py` the code).
3. Probe actual tools first: Node.js/npm, FFmpeg/ffprobe, Python, installed speech-recognition libraries, existing Remotion code. Report what is missing; request approval before installs.
4. Read script as UTF-8 and determine audio duration from the real file. Detect language mixing without translating.
5. List relevant recordings by filenames, dimensions, fps, and duration. Extract a few stills for inspection when available; do not pretend to watch a video if uninspectable.
6. Inspect supplied logo and color specs. Do not invent exact official hex codes; if none are supplied, propose an explicitly provisional palette.
7. Produce `output/EDITING_PLAN.md` with time-aligned scenes, visual descriptions, assets, caption sources, and uncertain words for review. Use `TEMPLATES/SCENE_PLAN.md` if present.
8. Do not promise a final MP4 until rendering is tested. Ask permission only for operations that require it.
