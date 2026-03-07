# TASK-20260304-ADP-MC-OVERVIEW-01

labels: adp, ops, overview, dashboard, ralph-loop, rebuild
priority: P0
status: in-progress
assignee: 청정
updated: 2026-03-08T08:13:19+09:00

## Goal
Create an ADP Ops Overview page/panel that shows (at minimum):
- Sessions
- Agents
- Tasks
- Errors
- Health
- Recent logs/activity

## Reference
- `context/adp/MISSION_CONTROL_REFERENCE_ADOPTION_NOTES_V0_1.md`

## Data sources (initial stub)
- `ops/agent_states/agents_summary.json` (or rebuild equivalent)
- sessions list from OpenClaw (if available) or a stub json

## Acceptance
- One screen that gives operator situational awareness in <10s.
- Works even with stub data.
