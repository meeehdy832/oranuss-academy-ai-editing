# Zahran UI Motion: a Claude skill for premium UI motion reels

A free [Claude skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that turns Claude into a
motion designer for **Apple-style UI / app reels**: product promos, app concepts and AI / SaaS launch videos, built in
[Remotion](https://www.remotion.dev) (React → MP4).

You give Claude a brief or a voice-over. It writes a beat sheet, builds the video with a ready-made motion kit, renders
it with real motion blur, and checks the result with measurement scripts.

Made by **Yahia Zahran (Zahran Motion)**.

## What's inside

| Folder | What it is |
|---|---|
| `SKILL.md` | The workflow and the rules Claude follows |
| `references/` | The style guide: the gold reel beat by beat, design, motion curves, transitions, pacing, 23 text techniques, a motion "bible" with safe value ranges, the kit API, and 24 frame-by-frame breakdowns of reference reels |
| `kit/motion-pro/` | The Remotion component kit: camera rig, real shutter motion blur, text effects, morphs, transitions, pixels |
| `kit/examples/` | `ProDemo` (the gold reel, 18 s) and `TextLab` (every text technique, one after another) |
| `scripts/` | Python QA: motion energy, contact sheets, hold jitter, velocity profile |
| `setup/Root.tsx` | Drop-in Remotion root that registers the examples |

## Install

**Claude app (claude.ai / desktop):** download `zahran-ui-motion.zip`, then upload it in Settings under Skills (skills must be enabled for your account).

**Claude Code:** put the `zahran-ui-motion` folder in `~/.claude/skills/` (all projects) or `<project>/.claude/skills/`.

## Requirements

- Node.js 18+ (for Remotion)
- Python 3.9+ (optional, for the QA scripts): `pip install -r scripts/requirements.txt`
- Works on Windows, macOS and Linux

You don't need a Remotion project first: ask Claude to *"set up the zahran-ui-motion skill"* and it follows
`references/11-setup.md` (create the project, copy the kit, render the gold reel as a test).
Claude needs to be able to run commands for this (Claude Code, or the desktop app with a connected folder).

## Use

> Make a 15 s UI promo for a habit-tracker app called Loop. Copy: "Your habits. / On autopilot. / Meet Loop."

> Here's my voice-over (attached). Make a 1:1 app reel in the Zahran UI Motion style.

> Review this render's motion and transitions and fix what's off.

## Credits

The style was learned from frame-by-frame study of reels by **dnyxstudios**, **creatoroly**, **stepanvfx** and others.
Go follow them. Their videos are not included, only measurements and notes.

## License

MIT. See `LICENSE`.
