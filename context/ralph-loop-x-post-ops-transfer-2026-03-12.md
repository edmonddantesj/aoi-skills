# Ralph Loop ↔ x-post ops transfer note

Status: ACTIVE
Recorded: 2026-03-12
Source topic: `x-post` (956)
Target topic: `ralph-loop` (68)

## Transfer intent
The `x-post` topic should remain the **editorial room**.
Ralph Loop should act as the **operations room** for repeated discovery / triage / batching / decomposition around x-post production.

## Source-topic truth retained in x-post
These stay primarily in `x-post`:
- editorial tone and final draft shape,
- candidate selection policy,
- anti-dup / KR re-viral filter,
- posting policy (manual copy/paste only; auto-post forbidden),
- final human-facing draft package.

## What moves into Ralph Loop
The following recurring operations belong in Ralph Loop:
1. run-level scheduling and queueing
2. discovery backlog triage across candidate sources
3. repeated failure handling / blockers / proof logging
4. decomposition into smaller tasks (find candidates, filter, extract quotes, assemble packet)
5. throughput tracking and WIP discipline

## Recurring task shapes for Ralph Loop
### RL-XP-01 Discovery run
- collect candidate tweets/posts from approved sources
- keep proof of why each candidate was considered

### RL-XP-02 Anti-dup filter pass
- remove KR re-viral duplicates / already-translated items
- note rejection reason briefly

### RL-XP-03 Quote extraction
- capture source quote lines / context / fallback extraction proof

### RL-XP-04 Draft packet assembly
- package 후보3 + 선정1 + 인용박스
- hand back to `x-post` editorial room

### RL-XP-05 Failure / blocker logging
- captcha, login breakage, source instability, time-window miss
- keep ops proof so future runs become faster and safer

## Operating split
- `x-post` topic = editorial room
- `ralph-loop` topic = operating room

This separation prevents the editorial topic from filling with low-level operational noise while preserving fast repeated throughput in Ralph Loop.

## Gates
- discovery / filtering / draft packet prep: L1/L2
- external posting remains manual and fail-closed

## Expected artifacts
- operational cadence stays referenced by `context/topics/x-post_PLAYBOOK_V0_1.md`
- queue/task decomposition should live in Ralph Loop ledger/queue
- maintenance keeps scheduler-level automation, but Ralph Loop owns decomposition logic

## Proof / references
- Source memory: `memory/2026-03-11.md`
- Existing x-post playbook: `context/topics/x-post_PLAYBOOK_V0_1.md`
- Existing HF: `context/handoff/HF_x-post.md`
- `context/handoff/HF_xpost_ralph_transfer_20260314.md`
- `context/research/x-post/XPOST_RALPH_TRANSFER_AUDIT_2026-03-14.md`
- `ops/items/TASK-20260314-XPOST-RLP-01.md`
