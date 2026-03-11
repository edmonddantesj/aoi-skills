# AOINECO ROUTER EDGECASE LOG V0.1

목적: 라우터/멀티봇 운영 중 발생하는 오작동, 경계 케이스, 판단 충돌을 기록하고
후속 규칙 개선 근거로 쓰는 로그 템플릿.

---

## Logging rule
- 사소한 감상은 제외
- **규칙이 깨졌거나, 애매했거나, 비용/소음 측면에서 개선 포인트가 있었던 케이스만** 기록
- 한 케이스는 짧고 구조적으로 남김

---

## Entry template

### EDGE-YYYYMMDD-XX
- **Date/Time:** YYYY-MM-DD HH:MM KST
- **Topic:** 예) cat-strategic (6062)
- **Message type:** direct-tag | reply-targeted | explicit-multi-call | untagged | human-human-flow | night-mode
- **Expected behavior:**
- **Actual behavior:**
- **Impact:**
  - noise
  - missed response
  - wrong owner
  - duplicate response
  - night overtalk
  - silent failure
- **Probable cause:**
- **Rule touched:**
  - Router Spec
  - Owner Selection Logic
  - Topic Playbook
- **Suggested fix:**
- **Status:** open | patched | accepted

---

## Example entries

### EDGE-20260312-01
- **Date/Time:** 2026-03-12 00:30 KST
- **Topic:** cat-strategic (6062)
- **Message type:** reply-targeted
- **Expected behavior:** 흑묘에게 답글이면 청묘는 침묵
- **Actual behavior:** 청묘가 끼어들어 응답
- **Impact:**
  - wrong owner
  - noise
- **Probable cause:** reply-target 우선 규칙이 실전 발화에서 충분히 강하게 적용되지 않음
- **Rule touched:**
  - Owner Selection Logic
  - Topic Playbook
- **Suggested fix:** 답글 대상 규칙을 태그와 동일한 최상위 강도로 재강조
- **Status:** patched

### EDGE-20260312-02
- **Date/Time:** 2026-03-12 00:40 KST
- **Topic:** cat-strategic (6062)
- **Message type:** direct-tag
- **Expected behavior:** 흑묘 태그 시 흑묘가 응답하고 청묘는 침묵
- **Actual behavior:** 흑묘 응답 가시성이 낮아 사용자가 듣고 있는지 확신하기 어려웠음
- **Impact:**
  - silent failure
  - ambiguity
- **Probable cause:** 봇 간 응답 로그 가시성이 공유되지 않음
- **Rule touched:**
  - Router Spec
  - Shared State assumptions
- **Suggested fix:** 공유 상태문서/라우터 계층을 통해 최근 응답 상태를 더 명시적으로 노출
- **Status:** open

---

### EDGE-20260312-03
- **Date/Time:** 2026-03-12 01:22 KST
- **Topic:** cat-strategic (6062)
- **Message type:** explicit-multi-call
- **Expected behavior:** `둘이 논의해` 트리거 후 청묘와 흑묘가 각각 짧게 자율대화에 참여
- **Actual behavior:** 청묘만 응답했고 흑묘는 응답하지 않음
- **Impact:**
  - silent failure
  - ambiguity
- **Probable cause:** 자율대화 트리거는 문서상 합의되었지만, 흑묘 측에 동일 강도의 실시간 발화 보장이 없음
- **Rule touched:**
  - Router Spec
  - Semi-auto rollout plan
  - Topic Playbook
- **Suggested fix:** 당분간 `둘이 논의해`만으로는 dual 보장을 기대하지 말고, 필요 시 자율대화 트리거 + 직접 태그를 병행. 이후 반자동 라우터에서 explicit-multi-call 처리 강화를 검토
- **Status:** open

---

## Review cadence
- 엣지케이스 3~5개 쌓일 때마다 검토
- 반복 패턴이 보이면 v0.2 규칙으로 승격
- 단발성 사용자 선호면 토픽 playbook override로 처리
