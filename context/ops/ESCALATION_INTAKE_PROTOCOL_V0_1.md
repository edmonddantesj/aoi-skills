# Escalation Intake Protocol V0.1

Status: DRAFT-OPERABLE
Scope: Aoineco & Co. internal topic-to-main escalation lane
Last updated: 2026-03-16

## Purpose
각 팀원/토픽이 상위 검토, 개입, 정책 판단, blocker 해소가 필요할 때
채팅 휘발성에 의존하지 않고 **md 파일 단위로 에스컬레이션을 남기는 intake system**을 만든다.

목표:
- 검색 가능
- triage 가능
- 후속 조치 추적 가능
- 토픽 피드백/반려/보완 요청 가능
- 나중에 `에스컬레이션 확인해줘` 한마디로 스캔 가능

## 1. Directory layout
- `context/escalations/INDEX.md`
- `context/escalations/ACTIVE/`
- `context/escalations/RESOLVED/`
- `context/escalations/HOLD/`
- `context/escalations/REJECTED/`
- `context/escalations/_TEMPLATE.md`

원칙:
- 1건 = 1 markdown file
- ACTIVE에서 처리 시작
- 결론 나면 상태 디렉터리로 이동하거나 status 갱신

## 2. File naming
권장 형식:
- `ESC_YYYY-MM-DD_<source>_<short-slug>.md`

예시:
- `ESC_2026-03-16_cheongnoe_execution_continuity_gap.md`
- `ESC_2026-03-16_ops_backup_risk.md`
- `ESC_2026-03-16_bazaar_publish_gate_conflict.md`

## 3. Minimum schema
```md
# Escalation
- id:
- created_at:
- source_topic:
- source_owner:
- escalated_by:
- priority: critical | high | medium | low
- type: decision | conflict | blocker | risk | policy | resource | review-request
- status: active | reviewing | actioned | resolved | hold | rejected
- owner:
- due_by:

## Summary
한 줄 요약

## Context
배경

## Escalation Reason
왜 상위 검토/개입이 필요한지

## Requested Decision / Action
무엇을 결정하거나 해줘야 하는지

## Options
- A:
- B:
- C:

## Recommended
추천안

## Evidence / Links
- path:
- path:

## Assistant Triage
청묘 검토 메모

## Resolution
결론 / 피드백 / 후속조치
```

## 4. Intake rule
토픽/팀원은 아래 경우 에스컬레이션을 생성한다.
- 상위 정책 판단 필요
- owner 권한 밖 결정 필요
- blocker가 1회성 답변으로 안 풀림
- topic 간 충돌 발생
- 외부 리스크/공개 리스크/배포 리스크 존재
- 사람이 다시 묻기 전에 durable 검토 요청을 남기고 싶음

## 5. Triage rule
청묘는 `ACTIVE/`를 기준으로 triage 한다.

기본 응답 패턴:
1. 즉시 처리 가능 → 처리 + Resolution 기록
2. 추가 정보 필요 → 보완 요청 문안 작성
3. 상위 승인 필요 → decision memo / human gate로 승격
4. topic 재반송 필요 → 피드백/수정 요청 후 ACTIVE 유지

## 6. Expected outputs
에스컬레이션 검토 결과는 최소 하나 이상 남긴다.
- SSOT 문서
- topic-state update
- playbook update
- handoff
- 공지 초안
- 토픽 피드백 문안
- commit / artifact path

## 7. Query contract
사용자는 아래처럼 짧게 지시할 수 있다.
- 에스컬레이션 확인해줘
- ACTIVE 에스컬레이션 triage 해줘
- 청뇌 건 처리해줘
- 해당 토픽에 피드백 써줘

## 8. Relation to existing operating direction
이 프로토콜은 아래 장기 방향과 정합적이다.
- 구조화/문서화/검색/인수인계 규격을 먼저 세운 뒤 자동화/확장을 붙인다.
- 기억 의존이 아니라 searchable durable state에 의존한다.

## 9. Initial operating note
초기에는 자동 스캔보다 **문서 기반 intake + 수동 triage**로 시작한다.
실사용이 쌓이면 이후:
- index 자동갱신
- priority sort
- stale escalation reminder
- topic feedback 템플릿 자동생성
같은 보강을 붙인다.
