# Handoff Index (SSOT)

목적: 시간이 지나 다시 물어봐도, 현재 진행중인 작업을 **끊김없이 즉시 재구성**하기 위한 작업 현황 SSOT.

규칙:
- 새 작업/에픽 시작 시: `context/handoff/HF_<slug>.md` 생성
- 작업 진행/결정/막힌점/다음 액션은 해당 HF 문서에 누적
- 완료 시: 상태를 DONE으로 바꾸고, 산출물/링크/후속 액션을 기록

템플릿: `context/handoff/_TEMPLATE.md`

## ACTIVE
- `HF_inbox_dev_urgent_202603.md` — Inbox-dev(585) 긴급개발: DB/State loss 복구 + Base Batches(3/9) 데모
- `HF_handoff_compact_reminder_202603.md` — handoff(586): DAILY COMPACT 스냅샷 리마인더 자동화(09:30 KST)
- `HF_v6_invest_live_restart_202603.md` — v6-invest(1029): 실투 재개발/운영 복구 SSOT 및 반복업무 자동화
- `HF_x-post.md` — x-post(956): 브라우저 기반 후보발굴/본문추출 파이프라인 안정화 + 3회/일 산출 루틴 고정
- `HF_moltbook_ops_202603.md` — moltbook(1114): 운영 복구(키/스크립트/SSOT) + Daily/Weekly 루프 자동화
- `HF_topic81_basebatches_submission_package_202603.md` — topic81: Base Batches 제출 패키지(500 words + 인터뷰 + 데모) SSOT 합본
- `HF_aoi_pro_install_quickstart_preflight_202603.md` — aoi-pro: 설치/퀵스타트 Preflight(노드/경로/라이선스)로 성공률 개선
- `HF_render_502_warmup_retry_policy_202603.md` — render: 502 워밍업/재시도 정책 SSOT 확정
- `HF_aoi_pro_lite_lifetime_spec_202603.md` — aoi-pro: Lite 평생권($0.01) 스펙/가드레일 숫자 확정
- `HF_acp_ops_202603.md` — ACP(topic 50): Playbook 규칙 영구화 + 진행작업 HF 분리 + launchd/Ralph 자동화
- `HF_acp_dispatch_002_202603.md` — ACP(topic 50): Dispatch #002 (Bought & Analyzed) 오늘 투고 가능한 패키지 준비
- `HF_ralph_loop_drift_integrity_restore_20260308.md` — ralph-loop: 스캔/크론 상태저장 + drift 무결성 체크/자동복구(L2)
- `HF_random_playbook_hardening_20260312.md` — topic81(random): compact/context-loss 복구 규칙 즉시 반영 + 남은 검증 항목 추적
- `HF_topic81_internal_qa_reservation_discovery_202603.md` — topic81(random): 예약 링크/필터/추천/중복 정리 내부 QA tracked execution
