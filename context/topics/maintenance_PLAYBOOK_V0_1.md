# maintenance PLAYBOOK V0.1 (Topic 77)

- **Purpose:** 운영/주기작업/헬스체크/리커버리
- **Last updated:** 2026-03-08

## Recurring tasks (must not forget)
1) 주기작업 헬스체크(launchd + OpenClaw cron/heartbeat)
   - PASS/FAIL + 최근 실행 흔적 + 실패 시 조치
2) x-post(956) tick 스케줄 유지(08:10/12:10/18:10 KST)
   - launchd spec: `context/automation/launchd/com.aoineco.xpost.tick.plist`
   - runner: `scripts/xpost_tick.sh`
   - proof: `artifacts/x-post/<timestamp>/OUTPUT_TEMPLATE.md`
3) 3h Digest / Daily scan / Weekly triage 등 주기 리포트(확정되면 여기 고정)
4) 리커버리 작업은 항상 HF 문서로(증빙/커맨드 포함)

## Where to record
- 진행중 작업: `context/handoff/INDEX.md` 및 개별 `HF_*.md`
- 정책/인덱스: `context/SSOT_INDEX.md`, `context/telegram_topics/TOPIC_PLAYBOOK_INDEX_V0_1.md`

## Proof locations (examples)
- Gateway logs: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- launchd: `~/Library/LaunchAgents/*.plist`
