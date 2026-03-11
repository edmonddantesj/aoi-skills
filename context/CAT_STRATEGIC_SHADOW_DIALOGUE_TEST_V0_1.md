# CAT_STRATEGIC SHADOW DIALOGUE TEST V0.1

`cat-strategic` 토픽에서 청묘↔흑묘 turn-taking 대화를 시험하기 위한 최소 테스트 절차.

## Trigger
- `둘이 논의해`
- 또는 청묘/흑묘 동시 태그

## Test flow
1. 질문 성격을 전략형 / 실행형 / 혼합형으로 분류
2. 선발화자 결정
   - 전략형 → 흑묘
   - 실행형 → 청묘
   - 혼합형 → owner logic 기준
3. 1턴 발화
4. 직전 발언을 1~3줄로 요약해 shared state에 반영
5. 2턴 발화자는 반드시 `받음:` 형식으로 직전 요지 수용
6. 필요하면 3턴 정리 후 종료

## Night limits
- 23:00~08:00 KST
- 최대 2턴 권장, 예외적으로 3턴
- 장문 금지
- 결론형 종료

## Success check
- 둘 다 따로 에드몽에게 말하지 않았는가?
- 2턴째가 1턴째 요지를 실제로 받았는가?
- 2~3턴 안에 종료했는가?
- 결과가 에드몽 입장에서 읽기 쉬웠는가?

## Failure logging
실패 시 `AOINECO_ROUTER_EDGECASE_LOG_V0_1.md`에 기록:
- turn-taking 실패
- 직전 요지 미수용
- 과잉 턴
- 밤시간 과잉 대화
