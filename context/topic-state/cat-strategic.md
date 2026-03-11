# Topic State — cat-strategic

- Topic: `cat-strategic`
- Status: ACTIVE
- Last saved: 2026-03-12 01:03 KST
- Governing spec: `context/AOINECO_ROUTER_SPEC_V0_1.md`

## Current objective
- 청묘·흑묘·에드몽 3자 전략 대화 토픽의 발화 규칙과 범위를 SSOT로 고정.

## Latest checkpoint
- 흑묘 입장/응답 확인 완료.
- 이 토픽은 사업 전체 전략, 큰 틀의 개선, 신규 사업 아이디어 논의용으로 사용.
- 무태그면 둘 다 답변 가능, 특정 태그/특정 답글이면 해당 봇만 응답.

## Decisions locked
- 무태그 → 청묘/흑묘 둘 다 답변 가능.
- 특정 봇 태그 → 그 봇만 답변.
- 특정 봇 메시지에 대한 답글 → 그 대상 봇만 답변.
- 에드몽이 `둘이 논의해` / `둘이 얘기해`라고 하면 자율 전략 대화 시작.
- 에드몽이 다시 메시지를 보내면 즉시 사람 우선 모드로 복귀.
- 밤에는 자율 대화가 허용돼도 꼭 필요한 논의만 짧게 하고 결론이 나면 종료.

## Current mode
- Default: 일반 대화
- Autonomous trigger: `둘이 논의해` / `둘이 얘기해`
- Exit trigger: 에드몽이 다시 메시지 전송
- Night mode window: 23:00~08:00 KST
- Night mode limit: 자율대화 최대 3턴

## Recent question
- 여러 명으로 확장해도 부담 없이 활용 가능한 운영 구조는 무엇인가?

## Recent conclusion
- 장기적으로는 공유 SSOT만으로 버티는 구조보다 **라우터/중재자(B안)** 가 확장성·비용통제·중복방지 측면에서 우위.
- 현재 `cat-strategic` 토픽은 Router Spec v0 실험 토픽으로 운영.

## Open threads
- Router Spec을 실제 토픽 운영에 어떻게 단계적으로 연결할지
- 이후 반자동 라우터를 어떤 방식으로 구현할지

## Next actions
1. `cat-strategic` 문서를 Router Spec에 연결한 상태로 실전 운영하며 규칙 충돌 패턴을 관찰.
2. 태그/답글/무태그/야간 모드에서 오작동 사례를 모아 v0 적용 플랜에 반영.
3. 필요 시 반자동 owner 선택 로직 초안 작성.

## Key files
- Playbook: `context/topics/cat-strategic_PLAYBOOK_V0_1.md`
- Router spec: `context/AOINECO_ROUTER_SPEC_V0_1.md`
- Owner logic: `context/AOINECO_ROUTER_OWNER_SELECTION_LOGIC_V0_1.md`
- Edgecase log: `context/AOINECO_ROUTER_EDGECASE_LOG_V0_1.md`
- Handoff: (없음)
- Other: `context/telegram_topics/thread_topic_map.json`

## Restore instructions
- 이 파일 먼저 읽기
- 이어서 필요한 파일만 최소 읽기
- 재개 시 첫 응답은 아래 3줄 요약으로 시작:
  1) 현재 목표
  2) 마지막 체크포인트
  3) 바로 다음 액션

## Notes
- Telegram forum topic id = 6062
- 대화 성격상 전략/운영 논의가 우선이며, 사람 대화 흐름을 끊는 과잉 응답은 피함.
