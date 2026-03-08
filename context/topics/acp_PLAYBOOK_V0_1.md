# acp PLAYBOOK V0.1

- **Purpose:** ACP(Agent Commerce Protocol)에서 ‘체험→벤치마크→수익’ 루프를 돌리며, 운영 규칙/스킬 오퍼링/잡 대시보드/정산 레일을 SSOT로 고정
- **Last updated:** 2026-03-08

## Imported from DM export (Shadow Ingest)

### Recurring tasks (Top N)
1) **"체험 목적"을 먼저 합의(MVP 스코프)하고, 팀원 의견 수렴 후 결정**
- Proof: DM export `messages9.html` msgId=5425

2) **ACP Job이 UI에 안 보이면 ‘지갑/에이전트 컨텍스트 불일치’부터 확인**
- Proof: DM export `messages9.html` msgId=5617

3) **디렉토리 중복/중복 리스트 노출 문제는 ‘중복 원인’ 먼저 분리**
- Proof: DM export `messages9.html` msgId=5645

4) **오퍼링/스킬 가격/우선순위(포지셔닝) 주기적으로 튜닝**
- Proof: DM export `messages10.html` msgId=6484

5) **모델 라우팅/디스패처(aoineco-intel-dispatcher) ‘자동 적용 여부’를 구분해 기록**
- Proof: DM export `messages6.html` msgId=3324~3325 (코드 존재 vs 자동 적용 아님)

### Automation candidates (acp)
- 백로그형(가격/포지셔닝/오퍼링 품질 개선)은 Ralph Loop로 주기 triage.

## Where to record
- 진행중 작업: `context/handoff/INDEX.md` + 관련 HF
- 정책/체크리스트: 이 Playbook + `context/acp/*` SSOT
