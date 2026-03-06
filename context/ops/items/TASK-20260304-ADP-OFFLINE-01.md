# TASK-20260304-ADP-OFFLINE-01

labels: adp, ui, ops, offline, ralph-loop, rebuild
priority: P1
status: TODO

## Goal
Derive online/offline indicator based on `updated_at`.

## Depends on
- `context/adp/ADP_AGENT_STATE_SCHEMA_V0_1.md`

## Spec
- offline if `now - updated_at > threshold`.
- Show subtle offline badge/grey-out.

## Acceptance
- Agents clearly show stale state.
- Threshold configurable.
