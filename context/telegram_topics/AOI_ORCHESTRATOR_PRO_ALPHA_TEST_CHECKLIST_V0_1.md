# AOI Orchestrator PRO Alpha Test Checklist v0.1

Purpose: internal alpha-only test plan before any beta distribution.

## Current live target
- Chat: `telegram:-1003732040608`
- Topic: `6062`
- Topic slug: `cat-strategic`
- Operating mode: `orchestrator-alpha-lab`
- Primary owner: `청묘`
- Collaborators: `흑묘`, `에드몽`
- Note: treat topic 6062 as a private internal alpha lab for orchestrator tests before any external beta distribution.

## Goal
Verify that this topic can act as a realistic internal proving ground for:
- topic-aware routing
- delegation decision
- topic isolation
- orchestrator runtime state/event handling
- failure/recovery behavior

## Phase A — Router SSOT sanity
- [x] `thread_topic_map.json` contains topic `6062 -> cat-strategic`
- [x] `thread_agent_map.json` contains `cat-strategic`
- [x] `resolve_primary_agent.py --thread-id 6062` returns `청묘`
- [x] `delegation_decider.py` returns `should_delegate=true` for a meaningful request in this topic
- [x] `delegation_state.py record/check` works under workspace context

## Phase B — Topic-local orchestration runtime
- [x] test run creates dedicated runtime path keyed by topic/workstream
- [x] mock dispatch artifact created under `context/telegram_topics/runtime/orchestrator_alpha_lab/thread_6062/`
- [x] local orchestrator `state.json` created
- [x] local orchestrator `events.jsonl` created
- [x] `turn_handoff` sequence visible in local run output
- [x] final state closes cleanly (`mode=idle`, `currentTurn=null`)

## Phase C — Isolation / repeated use
- [x] same topic repeated runs do not corrupt state
- [x] different topics can be isolated by runtime path
- [x] repeated run preserves auditability via runId/event trail

## Phase D — Failure injection
- [x] stale lock recovery observed
- [x] broken `state.json` fallback observed
- [x] malformed last event line tolerated
- [x] watchdog timeout preemption observed

## Go / No-Go
### GO minimum
- all Phase A items pass
- Phase B core items pass
- no cross-topic contamination observed
- state/event files remain readable after repeated runs

### NO-GO
- wrong primary owner resolution for topic 6062
- workspace-vs-home path mismatch remains
- runtime files overwrite each other across topics
- recovery cannot restore from broken state

## Notes
- This checklist is for internal alpha only.
- 2026-03-16 KST revalidation completed after prewipe restore check.
- Revalidated with: `npm test` in `repos/aoi-skills/skills/aoi-squad-orchestrator-lite`, live `mock_orchestrator_dispatch.py` runs for topic `6062` and topic `60`, and existing runtime proof under `~/.openclaw/aoi/squad_runtime/planner-builder-reviewer/`.
- Do not package for beta until GO minimum is satisfied.
