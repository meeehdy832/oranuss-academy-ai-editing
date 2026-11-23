# Platform implementation guide

This guide is a decision aid, not a replacement for the target platform's documentation. Always inspect installed versions and local project patterns.

## CSS
- Use `@keyframes` for simple, declarative sequences.
- Use `transition` for state changes.
- Use `animation-timing-function` or per-keyframe timing functions when supported.
- Use `transform` and `opacity` for performant UI motion.
- Use `prefers-reduced-motion` for accessibility.
- Remember CSS cubic Bézier x control values must be within `[0,1]`.

## JavaScript / Web Animations API
- Use the Web Animations API when imperative control, playback, cancellation, or dynamic keyframes are needed.
- Use `Element.animate()` only in browser environments.
- Do not assume browser APIs exist in server-side rendering or Node execution.
- Cancel or finish animations intentionally when component state changes.

## GSAP
- Inspect whether GSAP is already installed and which version is used.
- Reuse existing timelines and project conventions.
- Use labels and stagger for coordinated sequences.
- Kill or clean up timelines when components are removed.
- Do not assume a particular plugin is available unless installed.

## React / Vue / other UI frameworks
- Prefer the project's existing animation library and component lifecycle patterns.
- Avoid starting duplicate animations on every render.
- Keep animation state separate from business/data state.
- Clean up listeners and animation instances.

## SVG / Canvas
- For SVG path reveals, consider path-length-based stroke drawing.
- For Canvas, use a stable frame loop and derive values from elapsed time rather than accumulating frame-dependent increments.
- Keep rendering separate from data calculation.

## Remotion / video rendering
- Use frame-based deterministic calculations.
- Convert duration to frames using the project's configured frame rate.
- Avoid non-deterministic timing APIs.
- Check that the final frame contains the intended settled state.

## After Effects
- Distinguish temporal interpolation from spatial interpolation.
- Use the Graph Editor to inspect speed/value behavior.
- Use Easy Ease only as a starting point; refine handles for the desired motion.
- Expressions must use valid After Effects expression syntax and property dimensions.
- Do not assume expressions can modify every keyframe interpolation feature.
- Explain whether the implementation is an expression, script, or manual keyframe workflow.

## Blender
- Inspect the current Blender version and whether the user expects F-curves, drivers, or Python scripting.
- Use interpolation and easing settings supported by that version.
- Check handles and extrapolation modes.
- Keep frame ranges and scene frame rate explicit.

## Unknown platform
Ask one direct question: “Which application or runtime should I implement this in?” Do not provide fake cross-platform code.
