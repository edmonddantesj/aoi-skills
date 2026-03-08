# maintenance PLAYBOOK V0.1 (Topic 77)

- **Purpose:** 운영/주기작업/헬스체크/리커버리
- **Last updated:** 2026-03-08

## Recurring tasks (must not forget)

## Imported from DM export (Shadow Ingest)
- 운영 감시 규칙(선보고 후조치): 성능 저하를 감지하면 먼저 보고하고, 승인 후 재시작/모델전환/설정 변경.
  - Proof: DM export `messages.html` msgId=123747

### A. Core scheduled reports (Topic 77)
(백업 기준으로 “실제로 올라오던 패턴”을 SSOT로 고정)

1) **Maintenance Digest (3h)** — 통합 헬스 대시보드
- schedule: 매일 `00:01/03:01/06:01/09:01/12:01/15:01/18:01/21:01 KST`
- includes (typical): `acp_watch`, `adp_smoke`, `notion_sync`, `oracle_dispatch`, `stability`, `sim_receipts`, `tmp` (+ 필요시 `error-triage`, `longform_ingest` 등)
- output:
  - 성공: 요약(OK/FAIL)
  - proof: `artifacts/digest/digest_YYYYMMDD_HHMMSS.txt`

2) **Ralph Loop Daily Scan** (23:00 KST)
- schedule: 매일 `23:00 KST`
- output:
  - report: `ops/reports/ralph_loop_daily/REPORT_YYYY-MM-DD.md`
  - (옵션) drift/integrity 체크 + `.state_backups/` 생성 + `ops/items/TASK-*.md` 큐잉

3) **Notion Sync Digest (AM/PM)**
- schedule: 매일 `08:50`, `20:50 KST`
- policy: `NO_STATE`/권한/키 이슈는 즉시 알림, 정상은 짧게(노이즈 최소)

4) **Knowledge Index Digest (daily)**
- schedule: 매일 `09:01 KST`
- output:
  - `context/knowledge/index.json` 스냅샷
  - `context/knowledge/digests/YYYY-MM-DD.md` 생성/갱신 (없으면 디렉토리부터 생성)

5) **maintenance_daily_smoke**
- schedule: 매일 `09:10 KST`
- policy: 성공 시 침묵(또는 1줄 PASS), 실패 시 상세 로그 + 즉시 알림
- log: `artifacts/.../maintenance_daily_smoke.YYYYMMDD_HHMMSS.log`

### B. Weekly cadence (ideas → adoption/build)
6) **Weekly Idea Triage** (ADOPT/BUILD/HOLD/DROP)
- cadence: **주 1회(LOCKED)**
- schedule suggestion: 월 `10:00 KST`
- SSOT:
  - `context/IDEA_TRIAGE_WEEKLY_SOP_V0_1.md`
  - `context/recommendations/RECOMMENDATIONS_LOG.md` (cadence locked 기록)

7) **Skills scouting batch** (벤치마크 후보 5개)
- cadence: 매일 오전 `11:05 KST` (복구본)
- source: ClawHub + GitHub
- output:
  - 후보 5개
  - `ADOPT / REBUILD / HOLD` 1차 판정
  - proof: `ops/reports/skill_scouting/daily/REPORT_YYYY-MM-DD.md`
  - decision docs: `context/skill_scouting/decisions/YYYY-MM-DD_<slug>_DECISION.md`
  - ADOPT/REBUILD는 Adoption Pack 자동 착수
- playbook: `context/SKILL_SCOUTING_DAILY_PLAYBOOK_V0_1.md`
- runner: `scripts/skill_scouting_daily.py`

### C. Existing scheduled ops owned here
8) x-post(956) tick 스케줄 유지(08:10/12:10/18:10 KST)
- launchd spec: `context/automation/launchd/com.aoineco.xpost.tick.plist`
- runner: `scripts/xpost_tick.sh`
- proof: `artifacts/x-post/<timestamp>/OUTPUT_TEMPLATE.md`

### D. Rule of thumb
9) 리커버리/긴급/큰 작업은 항상 **HF 문서 1장**으로 분리(증빙/커맨드/결정/Next 누적)

## Where to record
- 진행중 작업: `context/handoff/INDEX.md` 및 개별 `HF_*.md`
- 정책/인덱스: `context/SSOT_INDEX.md`, `context/telegram_topics/TOPIC_PLAYBOOK_INDEX_V0_1.md`

## Proof locations (examples)
- Gateway logs: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- launchd: `~/Library/LaunchAgents/*.plist`
