# Topic State — ralph-loop

- Topic: `ralph-loop`
- Telegram topic id: `68`
- Status: ACTIVE
- Last saved: 2026-03-08 23:13 KST

## Current objective
- 반복 운영업무를 자동 순찰/정리하는 실행 모드로서 WIP/SLA/cron/drift 무결성을 유지한다.

## Latest checkpoint
- Ralph Loop은 사업 전체 태스크 수행에 적용하는 실행 모드이며, ADP 쪽 라벨링 정책과도 연결된다. Source: MEMORY.md#L32-L35
- 핵심 운영축은 WIP<=5, stale 24h, cron health, drift/integrity 감시·복구다.
- 2026-03-12 기준 메인 운영 SSOT(`context/ralph-loop-ssot.md`)와 transfer notes(`context/ralph-loop-hackathons-transfer-2026-03-11.md`, `context/ralph-loop-x-post-ops-transfer-2026-03-12.md`)를 복구해, scan-centric 상태에서 small-task throughput 모드로 되돌리는 중이다.
- 2026-03-14 기준 longform delegated execution 복구를 위해 parent/child/synthesis 트랙을 실제 파일로 복원했다: `ops/items/TASK-20260314-LONGFORM-RLP-01.md` ~ `04.md`, `context/handoff/HF_longform_ralph_transfer_20260314.md`.
- 같은 날 hackathons / x-post delegated execution도 parent/child/handoff 기준으로 복구했다: `ops/items/TASK-20260314-HACKATHONS-RLP-01.md` ~ `03.md`, `ops/items/TASK-20260314-XPOST-RLP-01.md` ~ `03.md`.
- 현재 무결성 복구 관련 active HF는 `context/handoff/HF_ralph_loop_drift_integrity_restore_20260308.md`다.

## Decisions locked
- 증빙 없는 “정리했다/고쳤다”는 금지.
- 공지 라우팅은 topic 68로 고정.
- L1/L2는 자율, L3는 승인 게이트.

## Next actions
1. 최근 drift/cron/scan 결과를 checkpoint에 주기적으로 반영.
2. stale 태스크는 분해/blocked/backlog 중 하나로 명시적 전환.
3. 자동복구 범위 변경 시 관련 SSOT도 함께 갱신.

## Key files
- Playbook: `context/topics/ralph-loop_PLAYBOOK_V0_1.md`
- Handoff: `context/handoff/HF_ralph_loop_drift_integrity_restore_20260308.md`
- Topic map: `context/telegram_topics/thread_topic_map.json`

## Restore instructions
- 먼저 이 파일을 읽고, 실제 내용이 얇으면 Playbook과 관련 HF를 최소만 추가로 읽는다.
- 복구 응답은 `현재 목표 / 마지막 체크포인트 / 다음 액션` 순서로 짧게 재구성한다.

## Notes
- ralph-loop는 운영 무결성용이라 상태가 낡으면 의미가 급격히 떨어진다. 자주 저장하는 토픽으로 취급.
