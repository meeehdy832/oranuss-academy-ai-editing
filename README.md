# Oranuss Academy AI Editing

> Developed by Mehdi ORANUSS | Powered by Claude

Video editing with **Claude Code** for Moroccan Darija content: reels and YouTube videos, Arabic or Latin-Darija captions, motion graphics in HTML (HyperFrames + GSAP), face tracking, sound design.

## Install (one text)
Open Claude Code on a Mac (Apple Silicon), then copy and paste the content of **[INSTALL-PROMPT.md](INSTALL-PROMPT.md)**.
Claude downloads and installs everything from the original links (see [SOURCES.md](SOURCES.md)), then asks whether you want to start a video.

This repo is **public**: anyone can install it, with no GitHub account, password or key.

Manual install (Mac):
```bash
curl -fsSL https://raw.githubusercontent.com/meeehdy832/oranuss-academy-ai-editing/main/install.sh -o /tmp/oranuss-install.sh
bash /tmp/oranuss-install.sh --tools --model
```

## What is inside
- `skills/`: global skills (copied to `~/.claude/skills`).
- `workspace/`: the editing folder (house rules `CLAUDE.md`, project skills, brand, styles, build code).
- `install.sh`: the installer.
- `INSTALL-PROMPT.md`: the one text to paste into Claude Code.
