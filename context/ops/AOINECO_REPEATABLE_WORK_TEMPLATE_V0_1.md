# AOINECO_REPEATABLE_WORK_TEMPLATE_V0_1.md

Status: TEMPLATE
Last updated: 2026-03-13

## Purpose
Reusable minimum template for converting a repeated operational rule from memory-dependent handling into system-dependent handling.

Use this when hardening a topic, project, or recurring workflow.

---

## A. SSOT snippet template
Copy/adapt this into a playbook, topic-state doc, or ops SSOT.

> This workflow must not depend on chat memory alone.
> Repeated internal execution should be fixed into SSOT/checklists/handoff/proof structures.
> If it must continue without the user, move repeated operational handling into Ralph Loop or another persistent automation lane.
> Human intervention is reserved for manual/external gates only.

---

## B. Minimal checklist template
- [ ] 목적/완료조건이 문서에 적혀 있다
- [ ] 반복 규칙이 playbook/SSOT에 적혀 있다
- [ ] 현재 상태를 남길 handoff/state anchor가 있다
- [ ] proof/evidence 위치가 정해져 있다
- [ ] 인간 개입이 필요한 manual/external gate가 명시돼 있다
- [ ] 반복 실행 부분이 Ralph Loop 또는 automation 후보로 분리돼 있다
- [ ] 마지막 순간 대응이 아니라 preparation-first 구조로 준비돼 있다

---

## C. Escalation rule template
### Escalate to main-session when
- 우선순위 충돌
- 방향/전략 변경 필요
- acceptance criteria 불명확
- canonical SSOT 간 충돌

### Escalate to human gate when
- 로그인 필요
- KYC/captcha 필요
- 결제/서명 필요
- 최종 제출/대외 발신 승인 필요

### Keep inside Ralph Loop / internal execution when
- 반복 가능
- 내부 작업
- 증빙 가능
- packet/checkpoint로 쪼갤 수 있음

---

## D. Preparation-first packet template
Before submit/apply/operate, prepare:
- build:
- repo/path:
- README/usage note:
- demo/screenshot:
- proof bundle:
- submit/apply copy:
- blocker list:
- final human gate:

---

## E. Ralph Loop execution split template
If a topic/project sends work into Ralph Loop, define at minimum:
- source topic:
- target lane: `ralph-loop`
- L1 approved?:
- L2 approved?:
- recurring task shapes:
- cadence/trigger:
- proof/artifact path:
- return rule to source topic:
- escalation rule to main-session/human gate:

Rule:
- L1 = candidate routing approval
- L2 = actual recurring execution activated
- If cadence/trigger/packet/proof/return are missing, the split is incomplete

---

## F. Migration prompts
Use these questions when migrating an existing topic/project:
1. 무엇이 반복되는가?
2. 무엇이 아직 기억/대화에만 남아 있는가?
3. 무엇을 Ralph Loop로 보내야 하는가?
4. 인간은 정확히 어느 수동/외부 게이트에서만 들어오면 되는가?
5. 제출 전에 미리 준비해둘 패키지는 무엇인가?
6. Ralph Loop로 보냈다면 L1/L2 중 어디까지 승인됐는가?
7. L2라면 실제 cadence/trigger/packet/proof/return rule이 정의됐는가?
