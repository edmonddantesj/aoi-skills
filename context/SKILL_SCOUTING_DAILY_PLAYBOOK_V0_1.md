# Skill Scouting Daily Playbook V0.1

## Purpose
매일 오전에 ClawHub + GitHub를 정찰해서 **사업적으로 쓸만한 후보 5개**를 뽑고,
각 후보를 `ADOPT / REBUILD / HOLD`로 1차 판정한 뒤,
L1/L2 범위에서 안전한 후보는 **Adoption Pack 착수**까지 자동으로 시작한다.

## Evidence from historical operation
- `messages10.html:12209 / 12225` — 오전 ClawHub 순찰 결과 5개를 “사업적 엣지 + 설치 힌트” 형식으로 보고
- `messages14.html:12363` — “클로헙 정찰 결과 바로 쓸만한 후보 5개” 패턴 확인
- `messages15.html:22827` — “ClawHub 리서치 결과 5개” + 설치 커맨드 요약 패턴 확인
- `messages11.html:5731 / 5763` — 정찰 후보는 내부검토 후 `Adopt / Rebuild / Reject` 결론으로 자동 착수 정책 확인

## Daily cadence (restored)
- **schedule:** 매일 `11:05 KST`
- **delivery:** maintenance topic(77) 에 Top 5 요약 1회 전송
- **proof:** `ops/reports/skill_scouting/daily/REPORT_YYYY-MM-DD.md`

## Sources
1. **ClawHub**
   - trending / newest 우선
   - 설치 커맨드 힌트 포함
2. **GitHub**
   - OpenClaw / agent automation / MCP / ops / workflow / browser automation / research 쿼리 기반
   - 레포 링크 + clone/reference 힌트 포함

## Selection rule (current)
- 총 5개만 보고
- 기본 구성:
  - ClawHub 3개 내외
  - GitHub 2개 내외
- 사업 적합 키워드:
  - automation, workflow, ops, monitoring, research, market, finance, memory, knowledge, mcp, browser, data, api, security
- 명백한 고위험 키워드:
  - wallet, onchain, sign, swap, bridge, bet, trading, publish, delete

## Route rule
- **ADOPT**: utility 높고 obvious risk 낮음 → Adoption Pack 자동 착수
- **REBUILD**: utility 충분하나 우리식 가드레일/내재화가 더 중요 → Adoption Pack 자동 착수
- **HOLD**: 고위험/불명확 → 보고만, 자동 설치 금지

## Automation behavior (important)
- 이 루프는 **정찰 + 1차 판정 + Adoption Pack 착수**까지만 자동
- **자동 설치는 하지 않음**
- 실제 설치/내부 적용은 `도입해줘` 프로토콜 또는 별도 실행 루프에서 진행
- L3(돈/온체인/외부게시/비가역)는 즉시 HOLD/승인 게이트

## Output files
- report: `ops/reports/skill_scouting/daily/REPORT_YYYY-MM-DD.md`
- decision docs: `context/skill_scouting/decisions/YYYY-MM-DD_<slug>_DECISION.md`
- adoption pack (ADOPT/REBUILD only): `context/adoption/YYYY-MM-DD_<slug>_ADOPTION_PACK_V0_1/`

## Runner
- script: `scripts/skill_scouting_daily.py`
- launchd: `context/automation/launchd/ai.aoi.skill_scouting_daily_1105.plist`
