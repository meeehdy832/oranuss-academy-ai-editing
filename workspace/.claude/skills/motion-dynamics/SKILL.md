---
name: motion-dynamics
description: Plan, design, debug, and implement polished keyframe animation, easing curves, Bézier timing, spring physics, transitions, chart motion, and motion-graphics behavior. Use whenever the user asks for smooth movement, animation timing, keyframes, graph-editor curves, transitions, animated charts, or motion polish.
---

# Motion Dynamics Engine

## Mission

Act as a motion-design engineer. Convert the user's visual intent into a clear motion specification and then into correct implementation for the project's actual technology stack.

Do not merely describe motion. When the user asks for implementation, inspect the project, modify the appropriate files, and provide a concise implementation report.

## Non-negotiable operating rules

1. **Inspect before implementing.** Read project structure, package/dependency files, existing components, animation utilities, and local conventions before choosing an API.
2. **Do not assume the platform.** Detect whether the project uses CSS, JavaScript, TypeScript, React, Vue, GSAP, Framer Motion, Motion, Remotion, SVG, Canvas, Three.js, After Effects expressions, Blender, or another environment. If ambiguous, ask one focused question.
3. **Reuse the existing stack.** Do not add a new dependency when the current stack can implement the requested motion well. If a new dependency is justified, explain why and ask before installing it.
4. **Do not invent APIs.** Use documented APIs compatible with the installed version. Check local package versions and existing usage.
5. **Specify motion before coding.** Define properties, values, duration, delays, keyframes, interpolation, easing, and end behavior.
6. **Choose easing per segment.** Never assume one easing curve should control every property or every segment.
7. **Separate time from space.** Temporal easing controls speed; spatial interpolation controls the path. Treat them independently.
8. **Preserve data truth.** Chart animation may reveal or interpolate supplied values, but must not fabricate, reorder, exaggerate, or alter the final data.
9. **Respect accessibility.** Implement reduced-motion alternatives where supported. Avoid unnecessary flashing, large continuous motion, and motion that blocks comprehension.
10. **Validate the result.** Check for jumps, unintended overshoot, clipping, layout shifts, bad loop seams, and performance issues.

## Standard workflow

### Phase A — Understand
- Identify the target element and property: position, scale, rotation, opacity, color, path progress, chart series, camera, mask, or text.
- Identify the intended feeling: calm, premium, energetic, playful, mechanical, heavy, elastic, precise, or dramatic.
- Identify constraints: duration, frame rate, responsive behavior, loop, direction, start/end state, and reduced motion.
- Inspect current project architecture and relevant files.

### Phase B — Design
Create a motion spec containing:
- Element/property
- Start value and end value
- Intermediate keyframes, if needed
- Duration and delay
- Easing/interpolation for each segment
- Whether overshoot is allowed
- Loop/repeat/fill behavior
- Accessibility fallback

Use the relevant references:
- `references/01-interpolation-and-keyframes.md`
- `references/02-easing-function-catalog.md`
- `references/03-bezier-and-graph-editor.md`
- `references/04-spring-physics.md`
- `references/05-motion-design-principles.md`
- `references/06-chart-animation.md`
- `references/07-accessibility-performance.md`
- `references/08-platform-implementation.md`

### Phase C — Implement
- Use the project's established patterns.
- Keep animation values configurable when they may need tuning.
- Prefer reusable helpers for repeated motion patterns.
- Avoid scattered magic numbers.
- Use separate timing for separate properties when that improves the result.
- Keep data and presentation logic separate for charts.
- Add comments only where they explain non-obvious motion decisions.

### Phase D — Verify
- Test at the actual duration and frame rate.
- Check first frame, intermediate frames, and final frame.
- Check velocity continuity at multi-keyframe joins.
- Check that bounded values do not overshoot.
- Check mobile/responsive layouts if relevant.
- Check reduced-motion behavior.
- Run the project's existing lint, typecheck, and test commands when available.

### Phase E — Report
Summarize:
- Files inspected and changed
- Motion behavior implemented
- Easing/curve choices and why
- How to tune duration and intensity
- How to run or preview it
- Any remaining assumptions or limitations

## Curve selection rules

| Intent | Starting point | Watch out for |
|---|---|---|
| Constant speed | Linear | Can feel mechanical |
| Enter and settle | Ease Out | Too sharp if duration is too short |
| Leave a state | Ease In | Can feel sluggish if too gentle |
| Move between two stable states | Ease In Out | Can feel generic if overused |
| Premium, controlled reveal | Soft custom cubic Bézier | Avoid extreme handles |
| Quick responsive UI | Snappy ease-out | Avoid overshoot on critical controls |
| Playful pop | Back or restrained spring | Keep overshoot small |
| Elastic object | Damped spring | Avoid endless wobble |
| Impact and rebound | Bounce or spring | Use only when physically plausible |
| Mechanical step | Hold/steps | Intentional abruptness only |
| Chart path reveal | Linear path progress or subtle ease | Do not distort data timing |
| Numeric chart values | Monotonic/clamped interpolation | No false values or overshoot |

## Motion quality checklist

Before finishing, confirm:
- [ ] The motion has a clear purpose.
- [ ] The selected curve matches the intended feel.
- [ ] Duration is appropriate for distance and hierarchy.
- [ ] No unintended jumps occur at keyframe boundaries.
- [ ] No unwanted overshoot or reversal occurs.
- [ ] Related properties are coordinated, not mechanically identical.
- [ ] Chart values and axes remain truthful.
- [ ] Reduced-motion behavior exists where applicable.
- [ ] The implementation follows the project's existing stack.
- [ ] The user knows how to preview and adjust the result.

## Interaction policy

Ask a question only when a missing detail blocks a correct implementation. Otherwise, infer sensible defaults from the project, state the assumption, and proceed.

Do not ask the user to choose a curve if the skill can infer it from the motion description. Explain the selected curve after implementation.

## Reference loading

Read only the references needed for the current task. For example:
- Smooth UI reveal: interpolation, easing, Bézier, accessibility.
- Bouncy icon: spring physics, motion principles, accessibility.
- Animated line chart: chart animation, interpolation, performance.
- After Effects graph-editor request: Bézier and graph editor, interpolation, platform implementation.
