# Topic State — hackathons

- Topic: `hackathons`
- Telegram topic id: `71`
- Status: ACTIVE
- Last saved: 2026-03-08 23:13 KST

## Current objective
- 해커톤 후보 발굴부터 제출 패키징/데모/레포 정리까지 “제출 가능한 형태”를 유지한다.

## Latest checkpoint
- Topic 71 Archive UI Agent 해커톤 시도 postmortem 기준으로, 제출 실패의 핵심 원인을 `Gemini 자체`가 아니라 `page-context fidelity + proof discipline failure`로 고정했다.
- 새 canonical policy를 추가했다: `context/ops/PROOF_FIRST_YELLOW_LANE_AND_FATIGUE_HANDOFF_POLICY_V0_1.md`
- 앞으로 hackathons lane은 `proof-first / yellow-lane locked / blocker-first / fatigue-handoff / capability packaging`을 기본 규칙으로 사용한다.
- 특히 unstable live path를 main lane에 오래 남기지 않고, visible triad demo와 fallback submission path를 final stretch 전에 잠그는 것을 운영 기본값으로 삼는다.

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
