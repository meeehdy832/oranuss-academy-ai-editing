#!/bin/bash
# Oranuss Academy AI Editing: installer (macOS, Apple Silicon). Developed by Mehdi ORANUSS | Powered by Claude
# usage:  gh api repos/meeehdy832/oranuss-academy-ai-editing/contents/install.sh -H "Accept: application/vnd.github.raw" > /tmp/oranuss-install.sh
#         bash /tmp/oranuss-install.sh [target] [--tools] [--model] [--earshot]
# The repo is PRIVATE: the GitHub account signed in with `gh auth login` must be invited to it.
#   target     editing folder (default ~/Documents/oranuss-academy-ai-editing)
#   --tools    install ffmpeg-full, whisper-cpp, node with Homebrew (Homebrew must already exist)
#   --model    download the whisper large-v3 model (2.9 GB, Hugging Face)
#   --earshot  install earshot (listen/judge sound) from GitHub into a Python venv
# Only Oranuss files come from this repo; every other piece is installed from its own official link (SOURCES.md).
# Never overwrites an existing file.
set -e
REPO="meeehdy832/oranuss-academy-ai-editing"
TARGET="$HOME/Documents/oranuss-academy-ai-editing"; TOOLS=0; MODEL=0; EARSHOT=0
for a in "$@"; do case "$a" in --tools) TOOLS=1;; --model) MODEL=1;; --earshot) EARSHOT=1;; *) TARGET="$a";; esac; done
[ "$(uname -sm)" = "Darwin arm64" ] || { echo "STOP: needs a Mac with Apple Silicon."; exit 1; }
ok(){ echo "   ✅ $*"; }; no(){ echo "   ❌ $*"; }

echo "== 1/7 Oranuss files"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
if [ -n "$HERE" ] && [ -d "$HERE/workspace" ] && [ -d "$HERE/skills" ]; then SRC="$HERE"; else
  TMP="$(mktemp -d)"
  # private repo: needs the GitHub CLI signed in with an account that was invited to the repo
  command -v gh >/dev/null && gh auth status >/dev/null 2>&1 || { echo "STOP: run  brew install gh  then  gh auth login --web  (account invited to $REPO)"; exit 3; }
  gh api "repos/$REPO/tarball/main" > "$TMP/repo.tgz" || { echo "STOP: no access to $REPO. Ask Oranuss Academy for an invite, accept it on github.com, then run again."; exit 4; }
  tar -xzf "$TMP/repo.tgz" -C "$TMP" && rm "$TMP/repo.tgz"
  SRC="$(ls -d "$TMP"/*/ | head -1)"; SRC="${SRC%/}"; fi
mkdir -p "$TARGET" "$HOME/.claude/skills"
rsync -a --ignore-existing "$SRC/workspace/" "$TARGET/"
rsync -a --ignore-existing "$SRC/skills/" "$HOME/.claude/skills/"
fix(){ grep -rIl "/Users/Apple" "$1" 2>/dev/null | while read -r f; do d="$2/${f#$1/}"; [ -f "$d" ] &&
  T="$TARGET" H="$HOME" perl -pi -e 's#/Users/Apple/Downloads/editing-ai#$ENV{T}#g; s#/Users/Apple#$ENV{H}#g' "$d"; done; }
fix "$SRC/workspace" "$TARGET"; fix "$SRC/skills" "$HOME/.claude/skills"
ok "workspace -> $TARGET ($(ls "$TARGET/.claude/skills" | wc -l | tr -d ' ') project skills)"

echo "== 2/7 Homebrew tools"
if [ "$TOOLS" = 1 ]; then
  command -v brew >/dev/null || { no "Homebrew missing: install it from https://brew.sh, then run again"; exit 2; }
  brew install ffmpeg-full whisper-cpp node
fi
[ -x /opt/homebrew/opt/ffmpeg-full/bin/ffmpeg ] && ok ffmpeg-full || no "ffmpeg-full (brew install ffmpeg-full)"
command -v whisper-cli >/dev/null && ok whisper-cpp || no "whisper-cpp (brew install whisper-cpp)"
command -v node >/dev/null && ok "node $(node -v)" || no "node (brew install node)"

echo "== 3/7 Skills from their official repos"
if command -v npx >/dev/null; then
  npx -y skills add greensock/gsap-skills -g -a claude-code -s gsap-core -s gsap-timeline -y --copy >/dev/null 2>&1 && ok "GSAP skills (greensock/gsap-skills)" || no "GSAP skills"
  npx -y skills add heygen-com/hyperframes -g -a claude-code -s '*' -y --copy >/dev/null 2>&1 && ok "HyperFrames skills (heygen-com/hyperframes)" || no "HyperFrames skills"
  npx -y skills add Leonxlnx/earshot -g -a claude-code -s '*' -y --copy >/dev/null 2>&1 && ok "earshot skill (Leonxlnx/earshot)" || no "earshot skill"
  ok "global skills now: $(ls "$HOME/.claude/skills" | wc -l | tr -d ' ')"
else no "node missing: run again with --tools to get the GSAP/HyperFrames/earshot skills"; fi

echo "== 4/7 Fonts"
FD="$TARGET/brand/fonts/free"; mkdir -p "$FD"
[ -f "$FD/NotoKufiArabic.ttf" ] || curl -fsSL -o "$FD/NotoKufiArabic.ttf" "https://github.com/google/fonts/raw/main/ofl/notokufiarabic/NotoKufiArabic%5Bwght%5D.ttf" || true
cp -n "$FD"/*.ttf "$HOME/Library/Fonts/" 2>/dev/null || true
ls "$TARGET/brand/fonts/graphik-arabic/"*.ttf >/dev/null 2>&1 && cp -n "$TARGET"/brand/fonts/graphik-arabic/*.ttf "$HOME/Library/Fonts/" && ok "Graphik Arabic (your licence)" \
  || ok "Noto Kufi Arabic (free). Graphik Arabic is a paid font: put your licensed files in brand/fonts/graphik-arabic/"

echo "== 5/7 macOS helpers + HyperFrames"
if command -v swiftc >/dev/null; then mkdir -p "$TARGET/project/tools/ves/bin"
  for s in "$TARGET"/project/tools/ves/src/*.swift; do swiftc -O "$s" -o "$TARGET/project/tools/ves/bin/$(basename "$s" .swift)" 2>/dev/null || true; done
  ls "$TARGET/project/tools/ves/bin/face-track" >/dev/null 2>&1 && ok "face tracking helper" || no "face tracking helper"
else no "Xcode tools missing: run  xcode-select --install"; fi
command -v npx >/dev/null && (cd "$TARGET" && npx -y hyperframes@0.9.9 doctor >/dev/null 2>&1) && ok "HyperFrames (npm: hyperframes)" || no "HyperFrames: run  npx hyperframes@0.9.9 doctor"

echo "== 6/7 Transcription model"
M="$TARGET/project/models/ggml-large-v3.bin"; mkdir -p "$(dirname "$M")"
[ "$MODEL" = 1 ] && [ ! -f "$M" ] && curl -L --fail -o "$M.part" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin && mv "$M.part" "$M"
[ -f "$M" ] && ok "whisper large-v3" || no "model not installed (run again with --model, 2.9 GB)"

echo "== 7/7 earshot (optional)"
E="$TARGET/tools/earshot"
if [ "$EARSHOT" = 1 ] && [ ! -x "$E/.venv/bin/earshot" ]; then
  PY=$(command -v python3.12 || command -v python3.11 || command -v python3)
  "$PY" -m venv "$E/.venv" && "$E/.venv/bin/pip" install -q "git+https://github.com/Leonxlnx/earshot" && ok earshot || no "earshot (optional)"
else [ -x "$E/.venv/bin/earshot" ] && ok earshot || echo "   (skipped)"; fi

echo "DONE. Open this folder in Claude Code: $TARGET"
