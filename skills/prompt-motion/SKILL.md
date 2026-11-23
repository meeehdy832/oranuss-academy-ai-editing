---
name: prompt-motion
description: Library of 14 flagship production-grade motion design prompt blueprints from Prompt Motion (UI shape morphing, Apple-keynote continuous takes, WebGL2 3D landing page fly-overs, kinetic poster typography, AI voiceover launches, and deterministic seek(t) canvas/HTML/Remotion pipelines). Use when choosing the ideal motion-design direction and engineering architecture for a promo, explainer, showreel, or UI edit.
---

# Prompt Motion — Flagship Motion Design Skill

Choose the blueprint that best matches the user's input and deliverable, then follow its **Art Direction**, **Engineering Rules**, and **Quality Gate**.

## Quick Selector (Which Blueprint to Use)

| Use Case | Best Blueprint | Core Technique |
|---|---|---|
| **UI / SaaS / Product Value Morph** | **#2 Shape Morphing Through UI States** | Single container morphing size/radius/color on closed-form springs, real macOS cursor clicks/drags, zero cuts, warm-gray `#F4F4F5` canvas |
| **Apple-Keynote App Launch (Photos/UI)** | **#5 Photo Print App Launch / #11 Launch Sting** | 100% continuous 2D take, shared-element floods & iris wipes, liquid glass, directional motion blur |
| **Website / Landing Page 3D Promo** | **#6 / #33 Landing Page 3D Scroll** | WebGL2 flat studio floor + 56° camera glide, lifted `data-layer` cards, mipmapped DOF |
| **Bold Kinetic Street-Poster Identity** | **#28 TechHalla Kinetic Type Bumper** | 3-font hierarchy, `#0A0A0A` + `#FF2BD6` + `#B8FF00`, 2–4px print misregistration, mask wipes |
| **Looping Dot / Ball Systems** | **#29 Orange Dot / #30 White Ball Loop** | Single hero dot/ball physically connecting every UI scene, continuous camera world, `frame[0] == frame[last]` |
| **AI Voiceover Launch Film** | **#44 Ora 2 Image Model Launch** | Whisper word-level timing, liquid glass over blurred color wash, 16th-note image swaps, 3-band sidechain ducking |
| **Premium Music / Media Product Film** | **#73 Spotify Product Film** | Dark rounded inner stage, persistent bottom player bar, match-position artwork handoffs |
| **Editorial Spoken-Word Typography** | **#108 Build The Floor** | Letterforms as physical architecture (lintel, load, support, aperture, platform) |
| **Senior B2B Fintech / SaaS Film** | **#112 Taxtello Showreel** | Object-driven transitions (chart line → receipt edge → invoice), restrained gold/dark metal, zero template fluff |
| **Playful Paper & Physics Launch** | **#134 Paper-Style Launch Film** | HyperFrames + GSAP, marker stroke-dashoffset, squash/stretch, hard light/dark switches |

## Non-Negotiable Engineering Rules (Shared Across All Blueprints)

1. **Deterministic `window.seek(t)`:** Every position, scale, blur, opacity, and UI state is a pure function of `t`. Never use CSS `transition`, `setInterval`, or unseeded `Math.random()`.
2. **Closed-Form Springs:** Use analytic damped-harmonic step responses (`1 - e^(-ζωt) * ...`) summed per target change so any frame can be rendered out of order.
3. **Real Cursor Interaction (UI Blueprints):** Drive state transitions with a physical SVG macOS pointer (hover grow, press shrink, drag manipulation).
4. **No Overlapping Swaps:** Outgoing text/UI must exit or mask cleanly before incoming content occupies the same bounds.
5. **Pre-Render QA:** Always export beat-keyed check stills first (`render.mjs --frames ...`) and visually inspect before running the full MP4 encode.

Read `references/flagship-prompts.md` for the complete verbatim specifications of each flagship blueprint.
