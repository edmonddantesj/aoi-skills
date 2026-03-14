# ADP_AC_JUDGE_SURFACE_SPEC_V0_1

Status: DRAFT SPEC
Last updated: 2026-03-14
Scope: Topic 45 (ADP) AC/Judge operating surface

## Purpose
Topic 45 (ADP)를 단순 activity 뷰가 아니라,
판정 가능한 작업 단위 + handoff 가능한 운영 surface로 올린다.

## Core design
ADP에는 아래 3종 세트를 붙인다.
1. office work card schema
2. judge/status UI
3. detail panel

## Data schema
Each task / office-state unit should include:
- owner
- state
- status
- handoff
- nextAction
- definitionOfDone
- acceptanceCriteria
- judgeRule
- judgeResult
- holdReason
- humanGate
- updatedAt
- updatedBy
- proofLinks

## Field meaning
- state: `active | blocked | ready-for-judge | hold | done`
- status: 사람이 바로 읽는 한 줄 상태
- handoff: 다음 소유/단계
- nextAction: 한 줄 다음 행동
- definitionOfDone: 완료 조건
- acceptanceCriteria: 수용 기준
- judgeRule: 판정 규칙
- judgeResult: `pass | fail | hold | needs-human-review`
- holdReason: hold 사유
- humanGate: `none | asset-approval | org-change | external-approval | publish-approval`
- proofLinks: `{ label, urlOrPath, kind }[]`

## UI layers
### A. Status badge
- ACTIVE
- BLOCKED
- READY_FOR_JUDGE
- HOLD
- DONE

### B. Judge badge
- PASS
- FAIL
- HOLD
- NEEDS HUMAN

### C. One-line next
Every card must expose:
- `Next: ...`

### D. Detail panel
Expose:
- Owner
- Status
- Handoff
- DoD
- AC
- Judge rule
- Hold reason
- Human gate
- Proof links

## Workflow mapping
- meeting room → approval / judge / handoff
- engineering floor → active implementation
- QA lab → ready-for-judge / fail / retest
- server room → build / validation / deploy check
- lounge → hold / idle

## Design rules
- no decorative judge UI
- judge UI must map to actual workflow
- nextAction is always one line
- DoD / AC should be list-based
- humanGate must be explicit
- state and judgeResult stay separate
  - example: `state=ready-for-judge`, `judgeResult=hold`

## Phase plan
### Phase 1
- schema extension
- status / handoff / next / judge visible

### Phase 2
- DoD / AC / Judge rule / holdReason / humanGate in detail panel

### Phase 3
- judge result drives color / room / queue / event feed transitions

## Expected effect
ADP becomes:
- a task surface
- a judgment surface
- a handoff surface
- a proof-aware operating surface
