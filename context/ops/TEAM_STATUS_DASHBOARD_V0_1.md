# TEAM_STATUS_DASHBOARD_V0_1 (SSOT)

목적: 에드몽이 언제 물어봐도, 현재 진행상황/맥락을 **문서 기반으로 즉시** 답할 수 있게 하는 “단일 대시보드”.

## Canonical indexes
- SSOT index: `context/SSOT_INDEX.md`
- Handoff index: `context/handoff/INDEX.md`
- Telegram topics map: `context/telegram_topics/thread_topic_map.json`

## Current operating rule
- 각 토픽의 큰 작업/긴급건은 반드시 HF(핸드오프) 문서 1장으로 상태를 누적한다.
- 사용자가 “상태/진행상황/그거 뭐야”라고 물으면: 
  1) `context/handoff/INDEX.md`의 ACTIVE를 우선 요약
  2) 필요 시 해당 HF의 Proof/Commands로 증빙 제공

## Update cadence (to be automated)
- maintenance digest에 다음을 포함:
  - launchd jobs health
  - OpenClaw cron/heartbeat 최근 실행
  - ACTIVE HF 목록 + 1줄 상태
