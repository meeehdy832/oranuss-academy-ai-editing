# 11 · Setup (once per machine)

Needs: **Node.js 18+**, **Python 3.9+** (only for the QA scripts). Works on Windows, macOS and Linux.

## 1. A Remotion project
If the user has no Remotion project yet:
```bash
npx create-video@latest          # choose the "Blank" template, TypeScript
cd <project-folder>
npm i @remotion/google-fonts@<the exact version of "remotion" in package.json>
```
All `remotion` / `@remotion/*` packages must have the **same version** (the kit was built on Remotion 4.0.535 with
React 19; any recent 4.x works). Check with `npx remotion versions`.

## 2. Copy the kit into the project
From this skill folder:
```
kit/motion-pro/   →  <project>/src/motion-pro/
kit/examples/     →  <project>/src/examples/        (ProDemo = the gold reel, TextLab = every text technique)
setup/Root.tsx    →  <project>/src/Root.tsx          (or merge its <Composition>s into the existing Root)
```
The kit only depends on `react`, `remotion` and `@remotion/google-fonts` (fonts live in `src/motion-pro/theme.ts`).

## 3. Check it works
```bash
npx remotion studio                                   # open ProDemo and TextLab in the browser
npx remotion render src/index.ts ProDemo out/ProDemo_draft.mp4 --props='{"mb":1}'
```
On Windows PowerShell write the props as `--props='{\"mb\":1}'` or put them in a file: `--props=props.json`.

## 4. QA scripts (optional but recommended)
```bash
pip install -r <skill>/scripts/requirements.txt
python <skill>/scripts/energy.py out/ProDemo_draft.mp4
```
No ffmpeg needed for the scripts (OpenCV reads the MP4). Remotion ships its own ffmpeg for rendering.

## Common problems
- **"Cannot find module @remotion/google-fonts/Inter"** → step 1 install was skipped, or its version differs from `remotion`.
- **Text jumps / wrong widths in the first frames** → `useFontsReady()` is missing at the top of the composition.
- **Final render hangs or runs out of memory** → lower `--concurrency` (e.g. 2) and close heavy apps; motion blur with
  10–14 samples renders every frame 10–14 times.
- **The render "finished" but the file did not change** → the MP4 was open in a player; render to a new file name.
