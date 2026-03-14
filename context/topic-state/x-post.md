# Topic State — x-post

- Topic: `x-post`
- Status: ACTIVE
- Last saved: 2026-03-08 23:13 KST

## Current objective
- X에서 터질 각 콘텐츠를 발굴해 후보3 + 선정1 초안 패키지를 꾸준히 생산하되 자동 게시 없이 수동 게시 지원만 한다.

## Latest checkpoint
- 운영 고정값은 08:10/12:10/18:10, 좋아요 500+ 중심(300→150 폴백), 자동 게시 금지, 바닷가재 RPG 이미지 컨셉이다.
- launchd 미부트스트랩으로 인한 미발행 이슈를 교정했고, 스케줄/로그/아티팩트 증빙 경로가 남아 있다.
- 후보3 + 초안1 + 인용박스 생산이 매 회차 산출 계약이다.

## Decisions locked
- discovery는 브라우저 로그인 세션 우선.
- 국내 재바이럴 제외.
- 게시는 메르세데스 수동 복붙.
- 읽기 전용/1탭/최대 4분/계정 안전 가드 적용.

## Next actions
1. 회차별 후보3+초안1 결과 또는 실패 원인을 checkpoint에 남긴다.
2. 룰 변경 시 playbook 즉시 갱신.
3. 문제 생기면 launchd 로그와 artifacts를 함께 확인.
4. delegated execution track:
   - parent: `ops/items/TASK-20260314-XPOST-RLP-01.md`
   - discovery/filter/extract: `ops/items/TASK-20260314-XPOST-RLP-02.md`
   - packet/blocker/return: `ops/items/TASK-20260314-XPOST-RLP-03.md`

## Key files
- Playbook: `context/topics/x-post_PLAYBOOK_V0_1.md`
- Handoff: `context/handoff/HF_x-post.md`, `context/handoff/HF_xpost_ralph_transfer_20260314.md`
- Audit note: `context/research/x-post/XPOST_RALPH_TRANSFER_AUDIT_2026-03-14.md`
- Automation: `context/automation/launchd/com.aoineco.xpost.tick.plist`
- Logs/Evidence: `logs/launchd/xpost_tick.log`, `artifacts/x-post/`

## Restore instructions
- 먼저 이 파일 읽기
- 이어서 `context/topics/x-post_PLAYBOOK_V0_1.md`
- 진행 이슈 있으면 `context/handoff/HF_x-post.md`
- 자동화/실패 증빙이 필요하면 launchd log와 artifacts 확인

## Notes
- x-post의 핵심은 “발굴/초안 생산 자동화”이지 자동 게시가 아니다.
