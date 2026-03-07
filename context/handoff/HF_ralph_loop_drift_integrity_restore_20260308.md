# HF_ralph_loop_drift_integrity_restore_20260308

## Context Card (R1)
- **Goal:** ralph-loop의 스캔/크론 **상태 저장(state save)** 및 **drift 무결성 체크 + 자동 복구(aggressive)** 를 SSOT 기반으로 복원/고정한다.
- **Now:** Telegram topic(68) 대화 백업(2026-03-03~03-08) 확보. 과거에는 Daily Scan/Task hygiene/공지 라우팅까지 구성됐으나, `.openclaw` DB 유실/환경 드리프트로 “축약 모드”로만 도는 병목이 재발.
- **Next:** (1) Playbook에 반복업무/규칙 SSOT화 (2) drift 체크 정의(정본 파일 + 체크섬) (3) OpenClaw cron 또는 launchd로 자동 실행 고정 (4) 실패 시 롤백/쿨다운 가드.
- **Proof:** 입력 SSOT = `inbox/ralph-loop-export/.../messages.html`(ChatExport_2026-03-08). 관련 스크립트: `scripts/ralph_loop_daily_scan.py`, `scripts/ralph_loop_wip_sweep.py`, 상태파일: `context/state/ralph_loop_sync.state.json`.
- **Blocker:** drift 무결성 체크의 “정본(canonical) 상태 파일 목록”과 “자동 복구가 허용되는 범위”가 아직 명시 SSOT로 고정되지 않음.
- **Owner:** maintainer(청정) / 승인: 메르세데스(L2, auto-repair까지)

## Decisions / Approvals
- 2026-03-08: **L2 승인** — “ralph-loop 스캔/크론 상태 저장 및 drift 무결성 체크 복구” 진행 승인 (drift 발견 시 **자동 복구까지**).

## Worklog (요약)
- 2026-03-08: ChatExport(zip) 수신 → messages.html 파싱 가능 확인.
- Playbook/자동화/드리프트 정의를 **SSOT 문서로 재구성**하는 작업 착수.

## Next 3 (R3)
1) `context/topics/ralph-loop_PLAYBOOK_V0_1.md` 를 백업 기반으로 채워서 “반복업무/규칙” SSOT 확정
2) drift 무결성 체크 설계 SSOT: 정본 파일 리스트 + 체크섬 저장 위치 + 자동복구 정책(atomic/rollback/cooldown)
3) 스케줄러 확정 후 자동화 적용: OpenClaw cron(우선) 또는 launchd(plist)로 daily-scan + drift-check + state-save 고정
