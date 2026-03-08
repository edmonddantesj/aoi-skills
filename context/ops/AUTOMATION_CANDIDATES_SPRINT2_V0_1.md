# AUTOMATION_CANDIDATES_SPRINT2_V0_1

Scope (Sprint 2): acp / handoff / adp / ralph-loop

Policy: DM Export Shadow Ingest → Safe Promotion (`context/ops/DM_EXPORT_SHADOW_INGEST_AND_SAFE_PROMOTION_POLICY_V0_1.md`)

## A) launchd (fixed schedule) candidates

### A1. ADP healthcheck + autorestart (if hung)
- Type: launchd
- Why: ADP(로컬 포털)가 ‘살아있는데 응답 먹통’인 케이스가 반복될 수 있음
- Proof: DM export `messages16.html` msgId=11190
- Note: 실제 포트/프로세스/리스타트 커맨드는 현행 ADP runner 기준으로 확정 필요 (L1/L2)

## B) Ralph Loop (backlog/throughput) candidates

### B1. ACP offering price/positioning tuning loop
- Type: Ralph Loop
- Why: 고정 시간보다 ‘주기적으로 N개 점검’이 적합
- Proof: DM export `messages10.html` msgId=6484

### B2. ADP board classification rule maintenance (labels 포함)
- Type: Ralph Loop
- Why: 라벨/분류 규칙이 좁으면 “보이는 개수”가 틀어짐 → backlog형 점검 적합
- Proof: DM export `messages17.html` msgId=11547, 11549

### B3. Handoff discipline enforcer
- Type: Ralph Loop
- Why: ‘장문 인입 처리 순서’/‘즉시 SSOT 저장’ 같은 운영 헌법을 위반하는 항목을 큐로 잡아내고 패치
- Proof: DM export `messages9.html` msgId=5866

## C) Safe Promotion patches (to Forum topics)
- acp: UI에서 job 안 보일 때 “지갑/에이전트 컨텍스트 불일치” 체크리스트 패치
- adp: ADP 명칭 고정 + 헬스/URL 구분 패치
- handoff: 장문 인입 처리 순서/compact 권고 룰 패치
- ralph-loop: (기존 playbook이 이미 성숙) — ADP 분류/라벨 누락 정리 루프 패치 후보

## Next actions
1) acp/adp/handoff playbook을 기반으로 Safe Promotion 패치 발행 후 ADOPT/HOLD/CONFLICT 수집
2) ADP healthcheck launchd 후보를 실제 커맨드로 확정(가역적 L1/L2)
