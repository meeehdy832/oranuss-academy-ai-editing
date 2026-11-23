# Workflow: diagnose jerky or unnatural motion

## Symptoms and likely causes

| Symptom | Possible cause | What to inspect |
|---|---|---|
| Sudden jerk at a keyframe | Velocity discontinuity | Incoming/outgoing tangents |
| Stutter on web | Layout thrashing or heavy paint | Animated properties and frame loop |
| Feels robotic | Linear timing on expressive movement | Easing and staging |
| Overshoots unexpectedly | Auto Bézier or spring settings | Value graph and damping |
| Path loops or bends oddly | Spatial handles | Path interpolation |
| Animation snaps at end | Fill/cleanup or final state mismatch | Final keyframe and component state |
| Loop visibly jumps | Value or velocity mismatch | First/last frame and tangents |
| Chart looks misleading | Animated values or axes altered | Data model and scale |

## Debug process
1. Reproduce at the actual frame rate and duration.
2. Identify the exact property that jumps.
3. Inspect values at keyframes and between them.
4. Inspect velocity/tangents where available.
5. Temporarily replace complex easing with linear to isolate the issue.
6. Restore the intended curve and tune one parameter at a time.
7. Check cleanup, cancellation, and state synchronization.
8. Retest reduced motion and responsive layouts.
