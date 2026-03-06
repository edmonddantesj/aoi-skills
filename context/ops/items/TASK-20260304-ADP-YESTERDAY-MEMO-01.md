# TASK-20260304-ADP-YESTERDAY-MEMO-01

labels: adp, ui, narrative, memo, ralph-loop, rebuild
priority: P1
status: TODO

## Goal
Show a small "Yesterday memo" panel (2–5 lines) to add context/narrative.

## Spec
- Read from a daily note source (e.g., `memory/YYYY-MM-DD.md`) or a precomputed summary.
- Render 2–5 lines, truncated.

## Acceptance
- Panel does not dominate layout.
- Missing data fails gracefully.
