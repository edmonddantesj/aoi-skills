# TASK-20260304-ADP-BUBBLE-UX-01

labels: adp, ui, pixel-office, bubble, ralph-loop, rebuild
priority: P0
status: in-progress
assignee: 청정
updated: 2026-03-08T08:13:19+09:00

## Goal
Add 1-line status bubble UI to each agent (mobile-safe).

## Depends on
- `context/adp/ADP_AGENT_STATE_SCHEMA_V0_1.md`

## Spec
- Show `message` near sprite/card.
- One-line only.
- Truncate overflow with ellipsis.

## Acceptance
- Bubble never expands layout vertically beyond 1 line.
- Works on mobile widths.
