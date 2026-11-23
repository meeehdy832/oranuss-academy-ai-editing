# Workflow: create an animated chart

1. Inspect the chart library and current data model.
2. Record the final data values, labels, units, axes, and scale.
3. Decide whether the chart needs a path reveal, bar growth, point entrance, or number count-up.
4. Keep the data unchanged. Animate a reveal/progress value or visual geometry.
5. Use monotonic interpolation for numeric values.
6. Choose a short, controlled easing curve; avoid decorative overshoot on data.
7. Stagger dense series or categories only when it improves comprehension.
8. Add a static final state or reduced-motion alternative.
9. Verify the final rendered values match the source exactly.
10. Run the project's normal checks and report the implementation.
