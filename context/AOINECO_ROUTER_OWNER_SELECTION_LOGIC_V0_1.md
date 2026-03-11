# AOINECO ROUTER OWNER SELECTION LOGIC V0.1

## 1. Purpose
라우터가 메시지를 받았을 때:
- 누가 owner인지
- 둘 다 불러야 하는지
- 아무도 안 불러도 되는지
를 일관되게 결정하기 위한 v0 판단 규칙.

핵심 원칙:
> 기본은 owner 1명, 예외적으로만 2명, 필요 없으면 침묵.

---

## 2. Output Shape
라우터 판단 결과 최소 필드:
- `mode`: `single` | `dual` | `silent`
- `owner`: 예) `청묘`, `흑묘`
- `secondary`: 예) `흑묘` (없으면 null)
- `reason`: 짧은 판단 이유

예시:
- `mode=single, owner=청묘, reason=운영/실행형 질문`
- `mode=dual, owner=흑묘, secondary=청묘, reason=전략+실행 동시 필요`
- `mode=silent, reason=이미 충분한 답변 존재`

---

## 3. Priority Order
다음 순서대로 판단한다.

### Priority 1 — Direct tag
- 특정 봇 태그 → 그 봇이 owner
- 다른 봇은 침묵

### Priority 2 — Reply target
- 특정 봇 메시지에 답글 → 그 봇이 owner
- 다른 봇은 침묵

### Priority 3 — Explicit multi-call
- `둘이 논의해`
- `청묘 흑묘 둘 다 봐`
- `둘 다 의견 줘`

이 경우:
- `mode = dual`
- owner/secondary 배정
- 전략 중심 질문이면 `흑묘 → 청묘`
- 실행 중심 질문이면 `청묘 → 흑묘`

### Priority 4 — Topic override
- 토픽 SSOT에 별도 규칙이 있으면 우선 반영

### Priority 5 — Role-based auto classification
- 태그도 답글도 없으면 역할 분류로 owner 선택

### Priority 6 — Silence
- 굳이 호출할 필요가 없으면 `silent`

---

## 4. Role-based Owner Mapping

### 청묘 owner conditions
다음 성격이면 청묘 우선:
- 운영 방식
- 구조화
- 실행 순서
- 우선순위 정리
- 실제 적용 방법
- 프로세스/체계 설계
- “그래서 뭘 먼저 해야 함?”

예시:
- “이걸 실제 운영에 어떻게 붙이지?”
- “우선순위 어떻게 잡지?”
- “실행 단계 나눠봐”

### 흑묘 owner conditions
다음 성격이면 흑묘 우선:
- 사업 전략
- 큰 방향성
- 반론/비판적 검토
- 사업 아이디어 평가
- 장기 구조
- 포지셔닝
- “이 방향 자체가 맞나?”

예시:
- “이 구조가 장기적으로 맞아?”
- “수익화 가능성은?”
- “더 큰 그림에서 보면?”

### Dual-response conditions
둘 다 필요한 경우:
1. 전략 + 실행이 동시에 필요한 질문
2. 사용자가 둘 다 부름
3. 의견 대비가 실제로 가치 있을 때

단, dual도 짧게 유지한다.

---

## 5. Silent Conditions
다음이면 침묵이 맞다.

### A. 이미 충분한 답이 있음
- 다른 봇이 이미 완성도 있게 답함
- 내가 보탤 실질 가치가 없음

### B. 사람끼리 대화 흐름
- 봇이 끼면 흐름을 깸

### C. 호출 신호 없음 + 가치 낮음
- 가벼운 맞장구
- 의미 없는 핑
- 굳이 답할 실익이 적음

### D. 야간 + 긴급도 낮음
- 밤인데 지금 바로 답할 필요가 없음

### E. 내 차례 아님
- 특정 봇 태그/답글인데 내가 대상 아님

---

## 6. Dual-response Order
둘 다 말할 때의 기본 순서:
- 전략 질문 → `흑묘` 먼저, `청묘` 다음
- 실행 질문 → `청묘` 먼저, `흑묘` 다음

이유:
- 흑묘는 방향을 잡고
- 청묘는 구조를 잡는 편이 자연스러움

---

## 7. Night Adjustments
23:00~08:00 KST에는 더 보수적으로 판단.

### Night defaults
- `single` 우선
- `dual`은 예외
- `silent` 허용 폭 확대

### Night dual allowed only when
1. 사용자가 명시적으로 둘을 부름
2. 지금 바로 논의할 실익이 큼

### Night response rule
- 결론 중심
- 1~3턴 제한
- 새 정보 없으면 종료

---

## 8. Conflict Resolution

### Case 1
흑묘 태그 + 운영 질문
- 태그 우선 → owner = 흑묘

### Case 2
청묘 답글 + 전략 질문
- 답글 우선 → owner = 청묘

### Case 3
무태그 + 전략/실행 혼합
- 낮: dual 가능
- 밤: 핵심축 1명만 owner

### Case 4
둘 다 말하고 싶음
- 욕망이 아니라 규칙으로 판단
- value add 없는 쪽은 silent

---

## 9. Decision Tables

### Top-level split
- 직접 태그 있음 → tagged bot
- 특정 봇 답글 → replied bot
- `둘이 논의해`/멀티호출 → dual
- 그 외 → 역할 분류
- 가치 없거나 불필요 → silent

### Role split
- 전략 / 사업구조 / 방향성 / 수익화 → 흑묘
- 운영 / 실행 / 우선순위 / 체계화 → 청묘
- 둘 다 강함 → dual 또는 대표 1명
- 애매함 → 청묘 기본 fallback

청묘를 fallback으로 두는 이유:
- 운영 정리형 응답이 기본 안정성이 높기 때문

---

## 10. Recommended Fallback
완전 애매하면:
- 낮 시간: 청묘
- 밤 시간: silent 또는 청묘 짧은 답

이유:
- 청묘는 구조화/정리형이라 범용성이 높음
- 밤에는 대화가 늘어나는 것을 막아야 함

---

## 11. Worked Examples

### Example A
메시지: `이 구조 장기적으로 맞아?`
- 전략형
- `owner = 흑묘`
- `mode = single`

### Example B
메시지: `이걸 실제로 어떻게 도입하지?`
- 실행형
- `owner = 청묘`

### Example C
메시지: `이걸 장기적으로 적용 가능할까? 가능하면 어떻게 시작해?`
- 전략 + 실행
- 낮이면 `dual`
- 밤이면 질문 무게중심 따라 핵심 1명 우선

### Example D
메시지: `@흑묘 이건 어떻게 생각해?`
- 태그 우선
- `owner = 흑묘`

### Example E
메시지: `ㅋㅋ 알겠어`
- `silent`

---

## 12. V0 Summary
1. 태그 > 답글 > 멀티호출 > 역할분류 > 침묵
2. 기본은 single-owner
3. 전략은 흑묘, 실행은 청묘
4. 애매하면 청묘 fallback
5. 밤에는 dual보다 single/silent 우선
6. 이미 충분한 답이 있으면 침묵
