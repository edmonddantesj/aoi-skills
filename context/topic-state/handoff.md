# Topic State - handoff

- Topic: `handoff`
- Telegram topic id: `586`
- Status: ACTIVE
- Last saved: 2026-03-17 13:33 KST

## Current objective
- HF 중심 handoff/dispatch/compact로 컨텍스트 끊김을 막고 병렬 작업을 제어한다.

## Latest checkpoint
- ACTIVE/HOLD/DONE 정본은 `context/handoff/INDEX.md`이고, 큰 작업은 모두 `HF_*.md`로 관리하는 구조가 정착돼 있다.
- 장문/이전대화 인입은 끝까지 읽기 → 요약 → 분석/제안 → SSOT 저장 순서가 고정 규칙이다.
- 컨텍스트 60% 이상이면 compact/reset 권고를 함께 주는 운영 규칙도 여기와 연결된다.
- 복구 실행일 2026-03-17: `HF_handoff_compact_reminder_202603.md` 파일 없음 확인 후 재생성 완료.

## Decisions locked
- 큰 작업은 반드시 HF 1장으로 분리.
- 결정 3종 세트는 즉시 영구 저장.
- thread/topic 매핑은 병렬 라우팅의 전제다.

## ACTIVE HF 목록 (2026-03-17 기준)
- `HF_inbox_dev_urgent_202603.md` — DB/State loss 복구 + Base Batches 데모
- `HF_handoff_compact_reminder_202603.md` — 09:30 KST 자동 compact (재생성됨)
- `HF_v6_invest_live_restart_202603.md` — 실투 재개발/운영 복구
- `HF_x-post.md` — 브라우저 파이프라인 안정화
- `HF_moltbook_ops_202603.md` — 운영 복구 + 루프 자동화
- `HF_topic81_basebatches_submission_package_202603.md` — Base Batches 제출 패키지
- `HF_aoi_pro_install_quickstart_preflight_202603.md` — 설치/퀵스타트 Preflight
- `HF_render_502_warmup_retry_policy_202603.md` — 502 워밍업/재시도 정책
- `HF_aoi_pro_lite_lifetime_spec_202603.md` — Lite 평생권 스펙
- `HF_acp_ops_202603.md` — ACP Playbook 영구화 + 자동화
- `HF_acp_dispatch_002_202603.md` — Dispatch #002 투고 패키지
- `HF_ralph_loop_drift_integrity_restore_20260308.md` — drift 무결성 체크/자동복구
- `HF_random_playbook_hardening_20260312.md` — compact/context-loss 복구 규칙 반영
- `HF_topic81_internal_qa_reservation_discovery_202603.md` — 예약 링크/필터/중복 QA
- `HF_antigravity_team_onboarding_20260316.md` — Antigravity 팀 온보딩
- `HF_hackathon_research_support_request_2026-03-16.md` — 해커톤 winner 리서치
- `HF_hackathons_ralph_transfer_20260314.md` — hackathons→ralph 전환 복구

## Next actions
1. 이어갈 HF 지정 후 해당 HF 집중 작업.
2. compact 자동화 구현 (`HF_handoff_compact_reminder_202603.md` 참조).
3. 새 에픽 시작 시 HF 생성 후 INDEX 등록.

## Key files
- Handoff index: `context/handoff/INDEX.md`
- Playbook: `context/topics/handoff_PLAYBOOK_V0_1.md`
- Topic map: `context/telegram_topics/thread_topic_map.json`

## Restore instructions
- 먼저 이 파일을 읽고, 실제 내용이 얇으면 Playbook과 관련 HF를 최소만 추가로 읽는다.
- 복구 응답은 `현재 목표 / 마지막 체크포인트 / 다음 액션` 순서로 짧게 재구성한다.

## Notes
- handoff는 세부 내용보다 "어떤 HF를 먼저 읽어야 하는가"를 명확히 해주는 게 핵심이다.
