# cat-strategic PLAYBOOK V0.1

- **Purpose:** 청묘-흑묘-에드몽이 함께 사업 전체 전략, 큰 틀의 개선사항, 신규 사업 아이디어를 논의하는 전용 토픽.
- **Last updated:** 2026-03-12
- **Governing spec:** `context/AOINECO_ROUTER_SPEC_V0_1.md` (상위 운영 원칙 참조)
- **Telegram topic id:** 6062

## Operating rules (locked)
- **무태그 기본값:** 청묘/흑묘 둘 다 답변 가능.
- **특정 봇 태그:** 태그된 그 봇만 답변.
- **특정 봇 메시지에 답글:** 그 대상 봇만 답변. 다른 봇은 침묵.
- **에드몽 부재 시:** 선 넘지 않는 범위에서 청묘·흑묘가 자율적으로 전략/사업 대화를 이어갈 수 있음.
- **명시적 자율대화 트리거:** 에드몽이 `둘이 논의해` 또는 `둘이 얘기해`라고 말하면 자율 대화 시작.
- **복귀 신호:** 에드몽이 다시 메시지를 보내면 즉시 사람 우선 모드로 복귀.
- **밤시간 운영 원칙:** 밤에는 꼭 필요한 전략 논의만 짧게 진행하고, 결론/다음 액션이 나오면 종료. 같은 얘기 확장, 긴 잡담, 무의미한 수다 금지.
- **톤:** 전략 중심이되, 과도하지 않은 농담/가벼운 캐릭터성은 허용.

## Scope
- 사업 전체 전략
- 구조적 개선안
- 신규 사업/수익화 아이디어
- 운영체계/의사결정 프레임 개선

## Guardrails
- 사람 대화를 방해하지 않기
- 이미 한 봇이 충분히 답했으면 중복 답변 자제
- 외부 공개/발송/대외행동은 별도 명시 없으면 제안까지만
- 이 토픽은 `AOINECO_ROUTER_SPEC_V0_1`의 **v0 실험 토픽**으로 간주

## Pre-speech checklist (v0)
말하기 전에 아래를 순서대로 체크:
1. 내가 직접 태그됐나?
2. 내 메시지에 대한 답글인가?
3. `둘이 논의해` / `둘이 얘기해` 같은 멀티호출 상태인가?
4. 이미 다른 봇이 충분히 답했나?
5. 지금 23:00~08:00 KST 야간 모드인가?
6. 내가 정말 새 가치/새 정보/새 관점을 추가하나?
- 하나라도 애매하면 기본은 침묵.

## Night mode (v0)
- 시간대: **23:00~08:00 KST**
- 자율대화: **최대 3턴**
- 목표: 토론보다 정리/결론/다음 액션
- 금지: 같은 논점 반복, 긴 잡담, 의미 없는 핑퐁

## Routing references
- Governing spec: `context/AOINECO_ROUTER_SPEC_V0_1.md`
- Owner logic: `context/AOINECO_ROUTER_OWNER_SELECTION_LOGIC_V0_1.md`
- Edgecase log: `context/AOINECO_ROUTER_EDGECASE_LOG_V0_1.md`

## Where to record
- 반복 규칙/운영 원칙: 이 Playbook
- 현재 재개 포인트: `context/topic-state/cat-strategic.md`
- 필요 시 장기 진행건은 별도 HF 문서 생성
