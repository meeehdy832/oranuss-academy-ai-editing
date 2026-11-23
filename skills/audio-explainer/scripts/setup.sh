#!/bin/bash
# Usage: setup.sh REMOTION_DIR WORKDIR "BRAND NAME" "#1F6BFF" [AUDIO_FILE]
# Installs the engine into a Remotion project once, sets brand + accent, links this video's beats + audio,
# and registers the composition "Explainer". Safe to re-run (only overwrites the engine files).
set -e
R="$1"; W="$2"; NAME="$3"; ACCENT="${4:-#1F6BFF}"; AUDIO="$5"
[ "$NAME" = "none" ] && NAME=""   # "none" in the brief = no name on top
S="$(cd "$(dirname "$0")/.." && pwd)"
E="$R/src/compositions/audio-explainer"
mkdir -p "$E" "$R/public/audio" "$R/public/img" "$R/public/vid"
cp "$S/template/ExplainerDoc.tsx" "$S/template/IdeaFx.tsx" "$S/template/types.ts" "$E/"
printf '// Set by setup.sh from the brief.\nexport const BRAND = { name: "%s", accent: "%s" };\n' "$NAME" "$ACCENT" > "$E/brand.ts"
cp "$W/beats.json" "$E/beats.json"
[ -n "$AUDIO" ] && ffmpeg -v error -y -i "$AUDIO" -vn -ac 2 -ar 48000 -c:a aac -b:a 192k "$R/public/audio/voice.m4a"
cd "$R"
V=$(node -p "require('./package.json').dependencies.remotion")
for p in @remotion/google-fonts @remotion/fonts; do node -e "require.resolve('$p/package.json')" 2>/dev/null || npm i --save-exact "$p@$V" >/dev/null 2>&1; done
# register once
if ! grep -q 'id="Explainer"' src/Root.tsx; then
python3 - <<'EOF'
p = "src/Root.tsx"; s = open(p).read()
s = s.replace('import { Composition', 'import { ExplainerDoc as SkillExplainer } from "./compositions/audio-explainer/ExplainerDoc";\nimport explainerBeats from "./compositions/audio-explainer/beats.json";\nimport { Composition', 1)
i = s.rfind("</>")
s = s[:i] + '''  <Composition id="Explainer" component={SkillExplainer as never} fps={30} width={1920} height={1080}
        durationInFrames={Math.ceil(explainerBeats.duration * 30)}
        defaultProps={{ beats: explainerBeats.beats as never, audio: explainerBeats.audio, duration: explainerBeats.duration }} />
    ''' + s[i:]
open(p, "w").write(s)
EOF
fi
# macOS blocks Chrome's GPU helper inside ~/Downloads: use a copy outside it (see remotion.config.ts)
SHELL_DIR="$R/node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64"
CACHE="$HOME/.cache/remotion-chrome/$V"
if [[ "$R" == *"/Downloads/"* ]]; then
  [ -d "$SHELL_DIR" ] || npx remotion browser ensure >/dev/null 2>&1
  [ -d "$CACHE/chrome-headless-shell-mac-arm64" ] || { mkdir -p "$CACHE"; cp -R "$SHELL_DIR" "$CACHE/"; }
  grep -q setBrowserExecutable remotion.config.ts || printf '\nimport fs from "node:fs"; import os from "node:os"; import path from "node:path";\nconst c = path.join(os.homedir(), ".cache/remotion-chrome/%s/chrome-headless-shell-mac-arm64/chrome-headless-shell");\nif (fs.existsSync(c)) Config.setBrowserExecutable(c);\n' "$V" >> remotion.config.ts
fi
npx tsc --noEmit >/dev/null 2>&1 && echo "setup ok · composition: Explainer" || echo "⚠ typecheck failed: run npx tsc --noEmit"
