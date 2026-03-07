# TASK-20260304-ADP-STATE-SCHEMA-01

labels: adp, ralph-loop, schema, ssot, rebuild
priority: P0
status: in-progress
assignee: 청정
updated: 2026-03-08T08:13:19+09:00

## Goal
Lock the minimal ADP agent state schema v0.1 so UI + downstream tasks use the same contract.

## SSOT
- `context/adp/ADP_AGENT_STATE_SCHEMA_V0_1.md`

## Acceptance
- Schema doc exists and is referenced by all related ADP UI tasks.
- 4 canonical statuses: idle|writing|syncing|error.

## Notes
Reconstructed from Telegram topic 45 after DB loss.
## Next Actions (decompose)
- [ ] Confirm schema file is canonical: `context/adp/ADP_AGENT_STATE_SCHEMA_V0_1.md`
- [ ] Add/verify a minimal JSON example payload in SSOT (1 agent, 4 statuses)
- [ ] Define OFFLINE_THRESHOLD default + where it lives (SSOT constant)
- [ ] Add boundary mapping rule section (non-canonical statuses → 4-state)

## Exit Criteria
- SSOT updated + referenced by Bubble/Offline/Pixel Move/MC Overview tasks
