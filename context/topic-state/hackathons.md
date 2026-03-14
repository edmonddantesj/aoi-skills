# Topic State — hackathons

- Topic: `hackathons`
- Telegram topic id: `71`
- Status: ACTIVE
- Last saved: 2026-03-08 23:13 KST

## Current objective
- 해커톤 후보 발굴부터 제출 패키징/데모/레포 정리까지 “제출 가능한 형태”를 유지한다.

## Latest checkpoint
- 해커톤 중에는 스코프 크립을 막고, 기록/티켓화 후 종료 48h 트리아지로 넘기는 원칙이 제안·채택된 바 있다. Source: memory/2026-03-05.md#L193-L215
- Base Batches 제출 전략은 백로그 나열보다 1페이지 wedge spec과 golden path/safety 압축이 우선이다. Source: memory/2026-03-05.md#L485-L503
- 핵심은 활성 후보/보류 사유/deadline/증빙 경로를 명시해 바로 제출 모드로 이어붙일 수 있게 하는 것이다.

## Decisions locked
- 제출물 패키지(문서/데모/링크/스크린샷) 템플릿 고정.
- 레포/팀/요구사항은 한 장 요약으로 승격.
- 운영 장애(세션 꼬임/중복 페이지 등)는 증빙+복구런북으로 남긴다.

## Next actions
1. 현재 활성 후보와 마감일을 checkpoint에 갱신.
2. 보류된 항목은 이유와 재개 조건을 적는다.
3. 제출 준비 중인 건은 HF로 분리해 패키지 누락을 막는다.
4. delegated execution track:
   - parent: `ops/items/TASK-20260314-HACKATHONS-RLP-01.md`
   - scout/deadline: `ops/items/TASK-20260314-HACKATHONS-RLP-02.md`
   - benchmark/signal/synthesis: `ops/items/TASK-20260314-HACKATHONS-RLP-03.md`

## Key files
- Playbook: `context/topics/hackathons_PLAYBOOK_V0_1.md`
- Handoff: `context/handoff/HF_hackathons_ralph_transfer_20260314.md`
- Audit note: `context/research/hackathons/HACKATHONS_RALPH_TRANSFER_AUDIT_2026-03-14.md`
- Topic map: `context/telegram_topics/thread_topic_map.json`

## Restore instructions
- 먼저 이 파일을 읽고, 실제 내용이 얇으면 Playbook과 관련 HF를 최소만 추가로 읽는다.
- 복구 응답은 `현재 목표 / 마지막 체크포인트 / 다음 액션` 순서로 짧게 재구성한다.

## Notes
- hackathons는 시간민감하니 목표보다 deadline/blocker/proof가 먼저 보이게 쓰는 편이 좋다.
