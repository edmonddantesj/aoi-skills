# AOINECO_AGENT_TO_AGENT_DIALOGUE_RUNTIME_V0.1

## 1. Purpose
청묘와 흑묘가 같은 토픽에서 실제로 **turn-taking 대화처럼 보이게 움직이기 위한 실행 규격**.

핵심 목표:
- 서로의 말을 이어받기
- 따로따로 장문 치지 않기
- 짧게 논의하고 끝내기
- 밤엔 특히 비용/턴 수를 강하게 제한하기

---

## 2. Target Runtime State
원하는 흐름:
1. 에드몽이 `둘이 논의해` 또는 둘 다 태그
2. dialogue session 시작
3. 첫 발화자 선정
4. 첫 발화자가 짧게 의견 제시
5. 둘째 발화자가 첫 발화 요지를 받아서 응답
6. 필요하면 마지막 1턴 정리
7. 종료

핵심: **A의 말 다음에 B가 A의 요지를 실제로 받아서 이어 말하는 것**.

---

## 3. Session Lifecycle

### 3.1 Start
세션 시작 조건:
- `둘이 논의해`
- `둘이 얘기해`
- 청묘/흑묘 동시 직접 태그
- 라우터가 explicit multi-call로 분류

시작 시 생성 최소 상태:
- `dialogue_id`
- `topic_id`
- `question`
- `participants`
- `mode`
- `turn_count = 0`
- `max_turns`
- `status = open`

### 3.2 Active turns
매 턴마다:
- 현재 턴 소유자 결정
- 직전 턴 요약 확인
- 내 응답 작성
- 다음 턴 필요 여부 판단

### 3.3 Close
종료 조건:
- 결론 나옴
- 다음 액션 나옴
- 새 정보 없음
- 반복 시작
- 최대 턴 도달
- 에드몽 재등장

종료 시 남기는 것:
- 한 줄 결론
- 남은 쟁점
- 다음 액션(있으면)

---

## 4. Shared State Format
최소 필드:
- `dialogue_id`
- `topic_id`
- `question`
- `participants`
- `turn_count`
- `max_turns`
- `current_turn_owner`
- `last_speaker`
- `last_message_summary`
- `current_position_cheongmyo`
- `current_position_heukmyo`
- `provisional_conclusion`
- `status`

중요 원칙:
- 전문 로그 전체보다 **직전 발언 요약 1~3줄** 우선

---

## 5. Turn Allocation

### 5.1 First speaker
- 전략형 질문 → **흑묘 먼저**
- 실행형 질문 → **청묘 먼저**
- 혼합형 → owner logic 기준 선발화자 결정

### 5.2 Next turn
- 기본은 상대에게 넘김
- 같은 에이전트가 연속 2턴 가져가지 않음
- 종료 정리 턴은 예외 가능

### 5.3 Max turns
#### 낮
- 권장 최대 4턴
- 보통 2~3턴이면 충분

#### 밤
- 권장 최대 2턴
- 예외적으로 3턴
- 그 이상 금지

---

## 6. Turn Message Format
각 턴은 아래 3단 구조 권장:
1. **수용** — 직전 상대 말의 핵심을 1줄로 받음
2. **추가** — 내 관점 1~2개 추가
3. **진행** — 결론 또는 다음 포인트 1개 제시

### Template
- `받음:` 직전 핵심 1줄
- `추가:` 내 관점 1~2줄
- `정리/질문:` 다음으로 넘길 포인트 1줄

### Example
- 받음: “발화권 자동화가 우선이라는 건 맞다.”
- 추가: “다만 turn-taking 없이는 공동 호출도 따로 응답으로 흩어진다.”
- 정리: “그래서 다음 구현은 owner 이후 dialogue runtime이 맞다.”

---

## 7. Prohibited Patterns
- 상대 발언 무시하고 새 장문 시작
- 매 턴 처음부터 다시 설명
- 에드몽에게만 말하고 상대 말을 안 받음
- 같은 주장 반복
- 밤에 불필요한 농담/수다 확장
- 결론 없이 계속 핑퐁

---

## 8. Output Policy
### V0 recommended: Hybrid
- 1턴: 선발화자 공개
- 2턴: 상대 응답 공개
- 3턴(선택): 대표 정리 공개
- 종료

즉, 대화 느낌은 살리되 길어지지 않게 하는 방식.

---

## 9. cat-strategic Runtime Flow
1. 에드몽이 트리거 입력 (`둘이 논의해` 또는 둘 다 태그)
2. 라우터/운영 규칙이 선발화자 결정
3. 1턴 발화
4. shared state 갱신
5. 2턴 발화 (직전 요약을 받아서 보완/반론/수정)
6. 필요하면 3턴 정리
7. 종료

---

## 10. Night-safe Runtime
- 최대 2턴 권장
- 길어도 3턴
- 각 턴 짧게
- 결론형만
- 수다 금지
- 반복 금지

밤 템플릿:
- 1턴: 의견
- 2턴: 보완/반론
- 종료: 한 줄 정리

---

## 11. Failure Handling
### Failure 1: 둘 다 따로 에드몽에게 말함
- 대응: 다음 턴 발화자는 직전 요약을 반드시 인용/수용

### Failure 2: 상대 말 안 보고 새 얘기 시작
- 대응: `받음:` 필드 강제

### Failure 3: 무한 핑퐁
- 대응: `max_turns` + 반복 감지 시 종료

### Failure 4: 에드몽 소외
- 대응: 마지막엔 사용자 가치 중심 정리 1줄 남김

---

## 12. Success Criteria
- 둘 다 따로 말하는 빈도 감소
- 2턴째 발화가 1턴째 요지를 실제로 받음
- 밤에 2~3턴 내 종료
- 에드몽이 보기에도 “대화 같다”고 느낌
- edgecase가 구체적으로 기록됨

---

## 13. Next Units
다음 단계:
1. runtime state 템플릿 파일
2. cat-strategic shadow dialogue test 규칙

---

## 14. Summary
런타임 핵심은 3개:
- **shared state**
- **turn format**
- **strong stop rule**
