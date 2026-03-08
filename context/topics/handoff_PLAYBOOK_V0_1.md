# handoff PLAYBOOK V0.1

- **Purpose:** SSOT 기반 handoff/dispatch/compact로 ‘컨텍스트 끊김’ 방지 + 토픽 간 병렬 운영을 제어
- **Last updated:** 2026-03-08

## Imported from DM export (Shadow Ingest)

### Recurring tasks (Top N)
1) **장문/이전대화 인입 처리 순서 고정: 끝까지 읽기 → 요약 → 분석/제안 → SSOT 저장**
- Proof: DM export `messages9.html` msgId=5866

2) **B-min 결정/정산 레일(USDC/Base/Notion) 같은 ‘결정 3종 세트’는 즉시 영구 저장**
- Proof: DM export `messages9.html` msgId=5876~5880

3) **컨텍스트 60% 이상이면 /compact 또는 /reset 권고를 함께 고정**
- Proof: DM export `messages18.html` msgId=12076

4) **토픽 thread_id 매핑/담당자 매핑은 운영 전제(병렬 라우팅 기반)**
- Proof: DM export `messages18.html` msgId=12454

## Where to record
- ACTIVE/HOLD/DONE: `context/handoff/INDEX.md`
- 개별 큰 작업: `context/handoff/HF_*.md`
- 통합 컴팩트: `context/telegram_topics/compact/`
