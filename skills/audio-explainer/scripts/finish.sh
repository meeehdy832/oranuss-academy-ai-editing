#!/bin/bash
# Usage: finish.sh REMOTION_DIR WORKDIR OUT_NAME
# Full render (background-friendly, prints one line), then SFX bus + mix + two-pass loudness (-14 LUFS, TP -1.5),
# then a 1-frame-per-minute contact sheet. Final file: WORKDIR/OUT_NAME-FINAL.mp4
set -e
R="$1"; W="$2"; N="$3"; S="$(cd "$(dirname "$0")" && pwd)"
cd "$R"
npx remotion render src/index.ts Explainer "$W/$N-render.mp4" --concurrency=4 --crf=20 --log=error > "$W/render.log" 2>&1
python3 "$S/sfx_mix.py" bus "$W" "$R/src/compositions/audio-explainer/beats.json" > "$W/sfx.log"
python3 "$S/sfx_mix.py" master "$W" "$W/$N-render.mp4" "$W/$N-FINAL.mp4" | tail -1
ffmpeg -v error -y -i "$W/$N-FINAL.mp4" -vf "fps=1/60,scale=320:-1,tile=6x3" -frames:v 1 -q:v 5 "$W/final-sheet.jpg"
echo "done: $W/$N-FINAL.mp4 · sheet $W/final-sheet.jpg · $(tail -1 "$W/sfx.log")"
