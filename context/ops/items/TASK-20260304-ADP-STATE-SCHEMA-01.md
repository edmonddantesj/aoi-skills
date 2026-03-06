# TASK-20260304-ADP-STATE-SCHEMA-01

labels: adp, ralph-loop, schema, ssot, rebuild
priority: P0
status: TODO

## Goal
Lock the minimal ADP agent state schema v0.1 so UI + downstream tasks use the same contract.

## SSOT
- `context/adp/ADP_AGENT_STATE_SCHEMA_V0_1.md`

## Acceptance
- Schema doc exists and is referenced by all related ADP UI tasks.
- 4 canonical statuses: idle|writing|syncing|error.

## Notes
Reconstructed from Telegram topic 45 after DB loss.
