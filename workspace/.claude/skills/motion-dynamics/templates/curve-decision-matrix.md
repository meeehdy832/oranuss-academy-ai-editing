# Curve decision matrix

| Desired result | Curve family | Overshoot? | Typical use |
|---|---|---:|---|
| Constant speed | Linear | No | Progress, path draw |
| Smooth arrival | Ease Out | No | UI entrance |
| Smooth departure | Ease In | No | UI exit |
| Start/end at rest | Ease In Out | No | State transition |
| Premium reveal | Custom Bézier | Usually no | Cards, titles |
| Snappy response | Strong Ease Out | No | Button feedback |
| Playful pop | Back | Small | Decorative icon |
| Spring settle | Damped spring | Optional | Drag release |
| Impact | Bounce | Yes | Ball-like object |
| Discrete switch | Hold/Steps | Not applicable | Frame-step effect |
| Numeric chart | Monotonic/clamped | No | Data visualization |

Use the matrix as a starting point. Confirm the target library's exact curve semantics.
