# Workflow: natural language to motion specification

Translate a motion request into structured intent before implementation.

## Step 1 — Extract intent
Identify:
- Subject
- Property
- Direction
- Start and end state
- Desired feel
- Duration, if supplied
- Repetition or loop
- Constraints

## Step 2 — Break into phases
Example request: “Start slowly, accelerate quickly, overshoot, then settle with a small bounce.”

Phases:
1. Anticipation or slow start
2. Acceleration
3. Overshoot
4. Return
5. Settle

## Step 3 — Assign curves per phase
Choose a suitable curve for each phase. Do not use a spring for the whole movement if only the final settle should feel springy.

## Step 4 — Produce a spec
```yaml
name: controlled-overshoot
property: translateX
duration_ms: 560
segments:
  - from: -80
    to: 0
    start_ms: 0
    end_ms: 390
    easing: custom-ease-out
  - from: 0
    to: 6
    start_ms: 390
    end_ms: 455
    easing: ease-out
  - from: 6
    to: 0
    start_ms: 455
    end_ms: 560
    easing: ease-out
overshoot_allowed: true
reduced_motion: opacity-only
```

The numbers above are illustrative. Scale overshoot to the element's travel distance and use target-specific units.
