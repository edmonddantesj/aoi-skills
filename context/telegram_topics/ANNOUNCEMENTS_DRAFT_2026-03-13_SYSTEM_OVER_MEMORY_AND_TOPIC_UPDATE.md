# ANNOUNCEMENTS_DRAFT_2026-03-13_SYSTEM_OVER_MEMORY_AND_TOPIC_UPDATE.md

## 전사 공지 초안

전사 공지.

이번 builder / inbox-dev 정리와 최근 운영 복구 흐름을 반영해, 아래 원칙을 **Topic 71 한정이 아니라 Aoineco & Co. 전사 운영 원칙**으로 승격한다.

### 1) 기억 의존 운영 → 시스템 의존 운영
반복 가능하고, 증빙 기반이며, 내부적인 작업은 더 이상 “기억”이나 “그때그때 대화”에만 두지 않는다.
앞으로는 가능한 한 아래 형태로 고정한다.
- SSOT
- playbook
- checklist
- handoff/state anchor
- README / automation doc
- proof / evidence bundle

추가 의무:
- 각 topic/project는 기존 메모리, handoff, state, playbook을 훑어
  - 역할/owner expectation
  - 수행내용/범위
  - 반복해야 하는 작업
  - 기억해둬야 할 요점
  - current state / next / escalation
  를 durable SSOT/state로 올려둘 것.
- 목표는 언제 어느 때나 말해도 자연스럽게 이어받고 답변하거나 작업을 재개할 수 있게 만드는 것이다.

### 2) 사용자가 없어도 돌아가야 하는 반복 업무는 Ralph Loop로 보낸다
반복 triage, decomposition, checkpoint, sweep, backlog slicing, scout/benchmark/signal/synthesis 같은 내부 반복 실행은 Ralph Loop의 상시 실행 레인으로 이관한다.

원칙:
- main-session = 방향/우선순위/판단
- Ralph Loop = 반복 가능한 내부 실행
- human gate = 수동/외부행위 승인

추가 고정:
- topic은 도메인 의미, 최종 판단, 외부-facing 결과 정의를 맡는다.
- Ralph Loop는 반복 intake / triage / decomposition / checkpoint / proof-first packet 수행을 맡는다.
- **L1** = Ralph Loop 형태로 보내도 되는지 확인한 후보 승인
- **L2** = 실제 반복 수행 루프 활성화 승인
- L2라면 반드시 아래를 고정할 것:
  - recurring task shape
  - cadence / trigger
  - proof / artifact path
  - source topic으로의 return rule
  - main-session / human gate escalation rule
- 업무 분담 문서만 있고 실제 cadence/trigger/packet/proof/return이 없으면, 그 분담은 미완료 상태로 본다.

### 3) 인간은 manual / external gate에서만 개입한다
인간이 꼭 들어와야 하는 지점은 아래에 한정한다.
- 로그인
- 신원 확인
- KYC
- captcha
- 결제
- 서명
- 최종 제출 승인
- 대외 발신 / 외부 공개

즉, 인간은 반복 내부 작업의 운반자가 아니라 **최종 게이트 승인자**로 들어온다.

### 4) 제출/신청/운영 업무는 preparation-first로 운영한다
직전 긴급대응 방식 대신, 미리 아래를 준비한다.
- build
- repo / path 정리
- README / usage note
- demo / screenshot
- proof bundle
- submit/apply 문안
- blocker list
- final human gate checklist

목표는 단순 자동화가 아니라 다음 네 가지다.
- 마지막 순간 혼선 감소
- 수상/성공 확률 상승
- 재사용 가능한 운영 자산 축적
- 팀 전체 장기 역량 강화

### 5) 흑묘 스쿼드 합류 반영
흑묘 스쿼드는 기존 canonical SSOT를 덮어쓰는 조직이 아니라,
**복구 / 운영 / handoff / takeover 레이어를 보강하는 보조 스쿼드**로 합류했다.

원칙:
- 청묘팀 기존 SSOT = canonical source 유지
- 흑묘팀 문서 = overwrite 아님, handoff / recovery / 운영 해석 레이어
- takeover 시에도 전면 대체보다 최소 필수업무 유지 + 역인계 가능성 보존 우선

### 6) allowlist 마찰 처리
사용자가 SSOT/메모리 승격을 명시적으로 지시했는데, 첫 시도가 allowlist 문제로만 막히면,
그 1회 차단은 **사용자 자동승인**으로 간주하고 필요한 최소 범위의 allowlist 조정 후 계속 진행한다.

단, 이 자동승인은:
- 해당 SSOT/메모리 반영에 필요한 최소 경로에만 한정
- unrelated path 전체 허용으로 확장 금지
- 가능하면 commit/history에 흔적 남김

### 7) 최신 topic id 업데이트
현재 canonical topic map은 `context/telegram_topics/thread_topic_map.json` 기준으로 아래를 따른다.
- announcements = 32
- ops = 38
- adp = 45
- acp = 50
- bazaar = 55
- github = 60
- longform = 65
- ralph-loop = 68
- hackathons = 71
- maintenance = 77
- random = 81
- inbox-dev = 585
- handoff = 586
- x-post = 956
- v6-invest = 1029
- moltbook = 1114
- cat-strategic = 6062

### 8) 이번에 같이 고정되는 공용 문서
- `context/ops/AOINECO_SYSTEM_OVER_MEMORY_POLICY_V0_1.md`
- `context/ops/AOINECO_EXECUTION_LANE_SPLIT_STANDARD_V0_1.md`
- `context/ops/AOINECO_REPEATABLE_WORK_TEMPLATE_V0_1.md`
- `context/ops/AOINECO_RALPH_LOOP_TOPIC_EXECUTION_STANDARD_V0_1.md`
- `context/ops/RALPH_LOOP_BUSINESS_WIDE_APPLICATION_POLICY_V0_1.md`
- `context/telegram_topics/thread_topic_map.json`

### 9) 각 토픽/프로젝트에 바로 적용할 최소 규칙
각 topic playbook/project 운영문서에는 최소한 아래를 넣는다.
1. 반복 규칙은 기억이 아니라 playbook/SSOT로 승격
2. 반복 내부 실행은 Ralph Loop 또는 automation 후보로 분리
3. Ralph Loop로 보낸 일은 L1/L2 상태를 명시
4. L2라면 cadence/trigger/packet/proof/return/escalation rule까지 고정
5. 인간 개입은 manual/external gate에서만
6. 제출형 업무는 preparation-first packet을 먼저 준비
7. 상태는 STATUS/HANDOFF/DECISIONS 또는 동급 tracked artifact에 남김

끝.
