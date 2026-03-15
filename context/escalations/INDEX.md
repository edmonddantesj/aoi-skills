# Escalation Index

목적: 토픽/팀원으로부터 올라온 상위 검토 요청을 durable하게 추적하기 위한 인덱스.

규칙:
- 새 에스컬레이션: `context/escalations/ACTIVE/ESC_*.md`
- 검토 시작 후 상태 갱신: active → reviewing/actioned/resolved/hold/rejected
- 처리 결과는 Resolution 또는 관련 SSOT/공지/피드백 문서로 남긴다.

참고 프로토콜:
- `context/ops/ESCALATION_INTAKE_PROTOCOL_V0_1.md`
- `context/escalations/_TEMPLATE.md`

## ACTIVE
- `ESC_2026-03-16_cheongnoe_execution_continuity_policy.md` — 청뇌 에스컬레이션: 원하면식 책임 환원 / 보고 후 정지 / 증빙 없는 진행 주장 재발 방지 정책 고정

## RESOLVED
- (없음)

## HOLD
- (없음)

## REJECTED
- (없음)
