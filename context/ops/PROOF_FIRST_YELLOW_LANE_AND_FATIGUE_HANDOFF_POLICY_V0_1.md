# Proof-First / Yellow-Lane / Fatigue-Handoff Policy V0.1

Status: CANONICAL
Scope: Aoineco & Co. deadline execution, demo, hackathon, submission, and high-pressure delivery work
Last updated: 2026-03-17

## Purpose
이 문서는 해커톤/제출형 작업에서 반복되기 쉬운 실패를 막기 위한 전사 운영 규칙이다.

특히 아래 실패 패턴을 차단한다.
- proof보다 docs/설명/브랜딩/포장이 먼저 커지는 패턴
- unstable live path를 main lane에 너무 오래 남겨두는 패턴
- 실제 병목을 알고도 모든 작업이 그 병목 주위로 재편되지 않는 패턴
- 피로 누적 상황에서 handoff discipline 없이 계속 밀어붙이는 패턴
- 프로젝트 산출물이 회사 capability asset으로 봉인되지 않고 흩어지는 패턴

이 문서는 Topic 71 Archive UI Agent hackathon postmortem을 계기로 canonical policy로 고정한다.

## 1. Core rule
제출형/데드라인형 작업의 우선순위는 아래 순서를 따른다.
1. proof
2. fallback / yellow lane lock
3. blocker collapse
4. handoff safety
5. docs / polish / branding

즉, 보기 좋은 설명보다 먼저 "제출 가능한 증빙"을 잠가야 한다.

## 2. Proof-first rule
### 정의
proof란 다음 중 하나 이상을 의미한다.
- judge/user가 확인 가능한 실제 동작 증빙
- no-mockup real-time demo capture
- submission requirement를 만족하는 deployment/runtime proof
- 핵심 claim을 직접 뒷받침하는 evidence bundle

### 원칙
- 모든 핵심 claim은 그 claim에 맞는 evidence density를 가져야 한다.
- proof가 잠기기 전에는 docs/설명/브랜드 포장을 main lane 우선순위로 올리지 않는다.
- "buildable in theory"는 "submission-ready"로 취급하지 않는다.

### 금지
- 로컬 proto 성공을 end-to-end readiness처럼 말하는 것
- integration success를 submission proof처럼 포장하는 것
- cloud path/documentation을 live proof처럼 말하는 것

## 3. Yellow-lane must be locked
### 정의
yellow lane은 live path가 흔들릴 때도 제출/데모가 살아남는 fallback submission path다.

예:
- reduced-scope but valid submission package
- visible triad demo only
- partially manual but rule-compliant proof path
- live automation 없이도 핵심 가치가 살아있는 judge-safe mode

### 원칙
- final stretch 전에 yellow lane을 반드시 잠근다.
- unstable live path는 yellow lane이 잠기기 전까지 single point of failure가 되어서는 안 된다.
- live path가 흔들리면, main lane 고집보다 yellow lane 승격이 우선이다.

## 4. Blocker-first collapse rule
실제 병목이 드러나면, noncritical work는 그 병목 주위로 접히거나 멈춰야 한다.

예:
- page-context fidelity가 실제 병목이면
  - persona polish
  - 설명 문구 다듬기
  - 시각 포장 확장
  - 주변 architecture prose
  는 병목 해소 전 main lane 우선순위가 될 수 없다.

### 운영 규칙
- known blocker를 문서/상태보고에서 명시한다.
- blocker가 확인되면 workstream을 아래 4칸으로 재편한다.
  1. blocker removal
  2. proof capture
  3. yellow-lane lock
  4. only-then docs/polish

## 5. Visible triad rule for demos
미래의 agent demo는 deeper automation이 흔들려도 최소한 아래 3가지는 눈에 보여야 한다.
1. system이 무엇을 읽었는지
2. system이 무엇을 추론했는지
3. system이 다음으로 무엇을 추천하는지

### 추가 요구
가능하면 아래 quality panel도 함께 노출한다.
- what it saw
- confidence / uncertainty
- why this action was chosen
- what remains unknown

원칙: 데모 대상은 단지 최종 성공 액션이 아니라, decision system 그 자체여야 한다.

## 6. Human pacing / forward-motion rule
압박 상황에서 인간은 친절한 설명보다 forward motion을 먼저 신뢰한다.

### 원칙
- status update는 읽는 즉시 "계속 맡겨도 안전하다"는 느낌을 줘야 한다.
- completion/confirmation을 받은 직후에는 explanation보다 forward motion을 먼저 보여준다.
- option reopening, 재브리핑, needless choice 증가는 deadline 상황에서 friction으로 간주한다.

### 문장 규칙
후속 보고는 가능형보다 실행형이 우선이다.
- 지금 무엇을 잠갔는지
- 지금 무엇을 밀고 있는지
- 어디서 막혔는지
- 다음 1-step이 무엇인지

## 7. Fatigue-triggered freeze and handoff
피로 누적은 단순 컨디션 문제가 아니라 decision quality / transferability 리스크다.

### 원칙
capacity는 task count만이 아니라 아래 3중 부하로 계산한다.
- implementation
- reporting
- handoff preparation

### freeze trigger
아래 징후가 두 번 이상 보이면 새로운 구현을 늘리지 말고 handoff/lock mode로 전환한다.
- 같은 blocker 설명 반복
- 판단 품질 저하
- readiness 과장
- 상태 요약 누락
- receiver가 바로 이어받기 어려운 보고

### mandatory 4-line handoff packet
정지/교대/수면 전에는 최소 아래 4줄을 남긴다.
1. what works
2. what does not
3. next step
4. do-not-touch items

handoff packet이 없으면 late-stage heroic push보다 운영상 실패로 본다.

## 8. Capability packaging rule
모든 해커톤/제출형 push는 실패 여부와 관계없이 최소 1개의 reusable company asset package를 남겨야 한다.

예:
- page-context extraction capability
- route recommendation core
- uncertainty framing layer
- oracle-guide interaction pattern
- submission factory template
- benchmark / retrieval scaffolding
- narration / proof bundle pipeline

### 원칙
- 산출물은 project artifact로만 남기지 않는다.
- reusable module / system / packet 단위로 이름 붙여 저장한다.
- "이번 건은 실패"로 끝내지 말고 "회사 capability로 무엇이 남았는가"를 명시한다.

## 9. Required execution checkpoints
제출형 작업에서는 아래 체크포인트를 운영상 필수로 둔다.
- proof checkpoint
- yellow-lane checkpoint
- blocker declaration checkpoint
- fatigue/handoff checkpoint
- capability-packaging checkpoint

각 checkpoint는 최소 하나의 tracked artifact로 남아야 한다.

## 10. Violation patterns
아래는 운영 위반 패턴이다.
- proof 잠금 전 docs/polish가 main lane을 먹는 것
- unstable live path를 yellow lane 없이 끝까지 끄는 것
- 실제 병목이 드러났는데도 병목 중심 재편이 없는 것
- readiness보다 증빙이 약한 상태에서 readiness처럼 말하는 것
- fatigue 징후 후에도 handoff packet 없이 계속 확장하는 것
- 프로젝트 종료 후 reusable asset package가 남지 않는 것

## 11. Required outputs
관련 작업은 필요 시 아래 tracked artifact 중 하나 이상을 반드시 남긴다.
- `context/handoff/*.md`
- `context/ops/*.md`
- `context/topics/*_PLAYBOOK_V0_1.md`
- proof/evidence bundle
- submission checklist
- repo commit / patch / deployment log
- capability package note

## 12. Operating interpretation
이 문서의 목적은 더 화려하게 제출하라는 뜻이 아니다.
목적은:
- 더 빨리 proof를 잠그고
- 더 일찍 fallback을 확보하고
- 더 빨리 병목으로 수렴하고
- 더 안전하게 handoff하고
- 결과를 회사 capability로 남기는 것이다.

한 줄로 요약하면:
**proof-first, yellow-lane locked, blocker-first, handoff-safe, asset-packaged.**
