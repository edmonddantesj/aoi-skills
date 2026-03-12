# Topic State — random

- Topic: `random`
- Topic id: `81`
- Status: ACTIVE
- Owner: 청묘
- Last saved: 2026-03-13 08:33 KST

## Role / purpose
- 혼재된 이슈를 임시로 받되, 오래 머물지 않게 빠르게 분류·배출하는 토픽.
- 반복 운영형 / 멀티스텝 실행형 / 교차 토픽형 작업은 random에 장기 체류시키지 않고 HF 또는 Ralph Loop로 전환한다.

## Scope boundary
### stays in random
- 임시 잡담 / 보류 / 분류 전 메모
- 아직 목적지가 확정되지 않은 단발성 이슈
- 짧은 checkpoint / pointer / 복구 포인트

### leaves random
- 오늘 안에 끝나지 않을 가능성이 큰 작업
- 산출물이 2개 이상 생기는 작업
- 증빙 / 결정 / blocker 추적이 필요한 작업
- 다른 topic / repo / 운영 lane과 연결되는 작업

## Recurring tasks
1. random에 들어온 이슈는 가능한 빨리 분류한다.
2. 반복 운영형 / 멀티스텝 실행형이면 HF 또는 Ralph Loop task로 전환한다.
3. random 본문에는 긴 실행 로그를 남기지 말고 pointer만 남긴다.
4. compact / context-loss 위험이 보이면 복구 포인트를 명시적으로 남긴다.
5. 즉시 실행이 어려운 건 “나중에 기억”으로 두지 말고 tracked artifact(HF / SSOT / task)로 전환한다.

## Key facts to remember
- random은 편하지만 기억 의존 운영에 가장 취약한 버퍼 토픽이다.
- 운영 기본값은 chat-memory가 아니라 durable state / playbook / HF다.
- random 직접 규칙은 `context/topics/random_PLAYBOOK_V0_1.md`가 canonical이다.
- 남은 검증 이슈는 `context/handoff/HF_random_playbook_hardening_20260312.md`에서 추적한다.

## Ralph Loop split
- State: **L1 fixed / L2 not yet fixed**
- Meaning:
  - random에서 반복형 내부 실행이 보이면 Ralph Loop shape로 보낸다.
  - 다만 random 자체에 대해 cadence / trigger / packet / proof / return / escalation까지 완전히 고정된 L2 운영 패킷은 아직 없다.
- Linked records:
  - `context/ralph-loop-random-triage-note-2026-03-12.md`
  - `context/ralph_loop/ledger.json` → `RL-20260312-035`

## Current state
- random 직접 운영 규칙은 playbook에 반영 완료:
  - compact / context-loss 복구 포인트 규칙
  - 장기화 / 다산출물 / 교차연결 작업의 HF 분리 규칙
  - “나중에 기억” 금지 + tracked artifact 전환 규칙
- 남은 일은 random 자체를 더 키우는 게 아니라, 새 장기 작업이 들어올 때 즉시 HF 또는 Ralph Loop로 분기하는 운영 일관성을 유지하는 것.
- A/B export divergence 및 전사정책 일반론은 random 직접 규칙과 분리해 HF에서 추적 중이다.

## Next
1. 새 장기 작업이 random에 들어오면 random 본문에는 요약 + pointer만 남기고 즉시 HF 생성/연결.
2. 반복 내부 실행으로 굳어지는 패턴이 확인되면 Ralph Loop L2 패킷(cadence / trigger / proof / return / escalation)을 별도 문서로 고정.
3. random topic-state는 “현재 메인 이슈 1~2개 + 포인터” 수준으로 얇게 유지하고, 세부 진행은 HF에 누적.

## Escalation rule
- 아래 중 하나면 main-session / owner 판단으로 올린다:
  - 새 메인 topic 분리가 필요한 수준으로 범위가 커짐
  - 외부 발신 / 제출 / 승인 / 계정 / 결제 / 서명 같은 human gate가 생김
  - random 직접 규칙과 전사 운영정책이 충돌하거나, canonical SSOT 승격 판단이 필요함

## Canonical files
- Topic state: `context/topic-state/random.md`
- Playbook: `context/topics/random_PLAYBOOK_V0_1.md`
- Handoff: `context/handoff/HF_random_playbook_hardening_20260312.md`
- Handoff index: `context/handoff/INDEX.md`
- Shared topic index: `context/telegram_topics/TOPIC_STATUS_INDEX_V0_1.md`

## Re-entry path
1. `context/topic-state/random.md`
2. `context/topics/random_PLAYBOOK_V0_1.md`
3. `context/handoff/HF_random_playbook_hardening_20260312.md`
4. related HF / proof docs as needed
5. `context/telegram_topics/TOPIC_STATUS_INDEX_V0_1.md`
