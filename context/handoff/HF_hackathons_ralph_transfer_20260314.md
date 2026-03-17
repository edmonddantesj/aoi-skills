# HF: hackathons(71) → ralph-loop(68) transfer recovery (2026-03-14)

- Status: ACTIVE
- Source topic: `hackathons` (71)
- Target execution lane: `ralph-loop` (68)

## Decision
Keep the split.
- `hackathons` remains the event/package room.
- `ralph-loop` owns repeated scout / deadline / benchmark / signal / synthesis loops.

## Current State
- parent restored: `ops/items/TASK-20260314-HACKATHONS-RLP-01.md`
- scout/deadline child restored: `ops/items/TASK-20260314-HACKATHONS-RLP-02.md`
- benchmark/signal/synthesis child restored: `ops/items/TASK-20260314-HACKATHONS-RLP-03.md`
- synthesis created: YES
- ssot promotion candidate: REVIEW_PENDING

## Lane IO / proof
- transfer note: `context/ralph-loop-hackathons-transfer-2026-03-11.md`
- source state: `context/topic-state/hackathons.md`
- audit: `context/research/hackathons/HACKATHONS_RALPH_TRANSFER_AUDIT_2026-03-14.md`

## Open Issues
- no concrete active candidate/deadline packet attached yet
- benchmark/signal output is structurally ready but not yet populated with a current run
- deadline execution policy was hardened on 2026-03-17; future pushes must honor proof-first / yellow-lane lock / fatigue-handoff discipline

## Next Actions
1. run scout/deadline sweep on next active queue
2. log candidate / null-result / blocker explicitly
3. return event-specific package truth back to `hackathons`
