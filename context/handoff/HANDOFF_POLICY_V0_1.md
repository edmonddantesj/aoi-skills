# Handoff Policy V0.1 (끊김 방지 운영 규칙)

목적: 시간이 지나 다시 물어봐도(또는 다른 에이전트가 받더라도) **맥락/할일/결정/증빙**을 즉시 복구하고 이어서 실행한다.

## 핵심 원칙
1) **증빙 기반**: “추측으로 단정” 금지. 항상 파일/링크/로그/커맨드 결과로 근거를 남긴다.
2) **SSOT 우선**: 대화 로그는 휘발될 수 있으니, 지속되어야 하는 정보는 `context/` 아래 SSOT로 승격한다.
3) **작업은 문서 1장에 묶기**: 큰 작업/긴급건은 HF 문서 1개로 상태를 누적한다.

## 반드시 지켜야 하는 4가지 행동 규칙
### R1. 작업 시작/재시작 시 "Context Card"를 먼저 만든다
- 6줄 요약(Goal/Now/Next/Proof/Blocker/Owner)을 먼저 생성하고 시작.
- 저장 위치: `context/handoff/HF_<slug>.md`

### R2. 외부로 보고/요청/결정이 나가면 HF에 기록한다
- Telegram/Notion/GitHub로 나간 핵심 메시지/결정은 HF 문서에 bullet로 기록.

### R3. 멈추기 전에 "Next 3"을 남긴다
- 작업 종료/중단 직전에 다음 3개 액션을 HF에 적는다.

### R4. "긴급/중요"는 키워드가 아니라 식별자다
- 사용자가 "긴급"이라고 말하면, 에이전트는 즉시 다음 중 하나를 요구한다:
  - (A) HF 문서 링크/파일명
  - (B) 토픽+키워드 2~3개(예: "inbox-dev/585, XX repo, YY 기능")
- 없으면 **추측으로 진행하지 않고**, HF 문서를 먼저 만드는 데 집중.

## 디렉토리/파일 규약
- Index: `context/handoff/INDEX.md`
- Template: `context/handoff/_TEMPLATE.md`
- Handoff file: `context/handoff/HF_<slug>.md`

## 운영 체크(자동/수동)
- (수동) 사용자가 "상태"라고 치면: 해당 토픽의 ACTIVE HF 1~3개를 즉시 요약.
- (자동, 추후) maintenance digest에:
  - launchd jobs health
  - OpenClaw cron/heartbeat 최근 실행
  - ACTIVE HF 목록
