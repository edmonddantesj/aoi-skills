# CAT_STRATEGIC Inbound Execution Layer Prototype — 2026-03-16 KST

## What was built
A thin topic-aware inbound execution layer prototype was added:
- `openclaw-telegram-topics-router/scripts/inbound_execution_layer.py`

Purpose:
- turn inbound topic messages into a single deterministic routing/execution decision
- emit the minimum execution shape needed by the alpha lab
- persist topic-local decision artifacts for auditability

## Output shape
The script emits:
- `mode`: `single | dual | silent`
- `owner`
- `secondary`
- `reason`
- `confidence`
- `delegate.should_delegate`
- `delegate.trigger_reason`
- `delegate.skip_reason`
- `context.primary`
- `context.collaborators`
- `context.reply_target_agent`
- `context.night`

## Decision order implemented
1. empty / low-value reaction -> `silent`
2. direct tag -> tagged bot gets `single`
3. reply target -> replied bot gets `single`
4. explicit multi-call -> `dual` (night still conservative but explicit call allowed)
5. mixed strategic+execution -> day=`dual`, night=`single`
6. execution-weighted text -> primary owner (`청묘` on `cat-strategic`)
7. strategic-weighted text -> `흑묘`
8. low-signal night text -> `silent`
9. fallback -> topic primary

## Topic-local runtime artifact path
When `--persist` is used:
- `context/telegram_topics/runtime/inbound_execution_layer/thread_<id>/latest/decision.json`
- `context/telegram_topics/runtime/inbound_execution_layer/thread_<id>/runs/<run_key>/decision.json`

## Validation snapshots
### Case A — current user request
Input:
- thread: `6062`
- text: `그럼 원래 여기서 하던 작업 이어서 진행해줘.`

Observed:
- `mode=single`
- `owner=청묘`
- `reason=execution_weighted_single_owner`
- `confidence=0.88`

### Case B — explicit dual at night
Input:
- `둘이 논의해. 이 구조 장기적으로 맞고 실제 도입은 어떻게 가야 해?`
- local hour = `2`

Observed:
- `mode=dual`
- `owner=청묘`
- `secondary=흑묘`
- `reason=explicit_multi_call`

### Case C — low-value night reaction
Input:
- `ㅋㅋ 알겠어`
- local hour = `2`

Observed:
- `mode=silent`
- `reason=night_low_signal_silent`

### Case D — strategic daytime question
Input:
- `이 구조 장기적으로 맞아?`
- local hour = `14`

Observed:
- `mode=single`
- `owner=흑묘`
- `reason=strategic_weighted_single_owner`

## Current limits
- direct-tag detection is string-based, not provider-native mention parsing yet
- reply target agent must currently be injected as payload field (`reply_target_agent`)
- cooldown / queue / orchestrator dispatch are not fused into one runner yet
- owner logic is heuristic, not full SSOT edgecase coverage yet

## Recommended next step
P1.5:
- add a single runner that chains:
  1. inbound execution decision
  2. cooldown check
  3. dispatch eligibility decision
  4. orchestrator/mock dispatch
  5. unified ledger pointer

## Status
- prototype built
- local validation done
- ready to wire into a combined runner
