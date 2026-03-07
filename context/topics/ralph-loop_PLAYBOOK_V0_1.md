# ralph-loop PLAYBOOK V0.1

- **Purpose:** ralph-loop(토픽 68)은 “반복 운영업무를 자동 순찰/정리하는 루프”의 SSOT. 핵심은 **WIP 제한(<=5), stale(SLA 24h), cron health, drift(상태 무결성) 감시/복구**를 매일 자동으로 굴리고, 결과/결정/증빙을 `context/`에 남기는 것.
- **Last updated:** 2026-03-08

## 0) SSOT / 저장 위치
- **진행중 큰 작업(HF):** `context/handoff/HF_ralph_loop_drift_integrity_restore_20260308.md`
- **태스크(개별 카드):** `context/ops/items/TASK-*.md`
- **일일 스캔 리포트:** `context/ops/reports/ralph_loop_daily/REPORT_YYYY-MM-DD.md`
- **위생/정합성 리포트(있으면):** `context/ops/reports/task_manager/*`
- **상태 파일(state save):** `context/state/*.state.json` (예: `context/state/ralph_loop_sync.state.json`)
- **정책/승인 게이트:** `context/telegram_topics/ANNOUNCEMENTS_CANONICAL_V0_1.md` (L1/L2/L3)

## 1) 고정 운영 규칙(반복)
### R1. WIP/SLA 규칙
- WIP 한도: **<= 5**
- stale 기준: **in-progress가 24h 초과**면 stale
- stale 발생 시 기본 조치(자동화/수동 공통):
  - (a) 태스크를 더 작은 단위로 분해
  - (b) 외부 의존이면 `blocked`로 전환 + blocker 명시
  - (c) 더 이상 진행 안 하면 `backlog`로 되돌림

### R2. 증빙 기반
- 모든 “정리했다/고쳤다/돌린다”는 반드시 아래 중 1개 이상을 남김
  - 파일 경로(SSOT/리포트/태스크)
  - 커맨드 및 결과(로그/리포트)
  - cron job id 및 최근 run 결과

### R3. 공지 라우팅(텔레그램)
- ralph-loop 관련 자동 공지(announce)는 **토픽 68**로만.
- delivery target은 가능한 한 명시적으로 고정(예: `telegram:group:-1003732040608:topic:68`).

### R4. 승인/리스크 게이트
- L1/L2(가역적 내부 작업) = 자율 진행, 완료 시 증빙 보고.
- L3(돈/키/서명/온체인/외부게시/비가역/권한변경) = 즉시 STOP 후 인간 승인.

## 2) Recurring tasks (must not forget)
### Daily (기본)
1) **Ralph Loop Daily Scan**
   - 입력: `context/ops/items/` (WIP/stale) + cron 상태 + drift 상태
   - 산출물: `context/ops/reports/ralph_loop_daily/REPORT_YYYY-MM-DD.md`
   - 구현: `python3 scripts/ralph_loop_daily_scan.py` (확장 필요: drift 체크/상태 저장)

2) **Task hygiene** (태스크 메타데이터 정리)
   - 누락 필드(status/priority/assignee/labels) 감지/보정
   - 산출물: `context/ops/reports/task_manager/...`

3) **State save + Drift integrity check (자동복구 포함)**
   - 정본(canonical) 상태 파일 목록에 대해 체크섬 저장
   - drift 발견 시: snapshot → atomic repair → 재검증 → 알림

### Weekly (선택)
- 크론/루프 노이즈 감사(중복/연속에러/consecutiveErrors>0 제거)

## 3) 표준 응답 포맷(채팅 보고)
- 6줄 요약(Goal/Now/Next/Proof/Blocker/Owner) → 필요 시 HF 링크 포함
- 완료 보고에는 **증빙(파일 경로/cron id/로그)** 최소 1개 포함

## 4) 운영 자동화(선택지)
- **우선:** OpenClaw cron (상태/실행 이력/알림 라우팅 관리가 쉬움)
- **대안:** launchd (macOS 로컬 고정 잡)

> Note: drift 무결성 체크의 “정본 파일 목록/자동복구 허용 범위”는 별도 SSOT로 확정 후 적용한다.
