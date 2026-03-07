# DISPATCH_PROTOCOL_V0_1 (SSOT)

목적: 청묘가 토픽(에이전트)에게 작업을 분산 지시하고, 결과를 SSOT로 회수해 전체 맥락을 유지한다.

## Dispatch message format (copy/paste)
- Title: [DISPATCH] <task>
- Inputs:
  - Source data path(s)
- Deliverables (must):
  1) Update topic Playbook: `context/topics/<slug>_PLAYBOOK_V0_1.md`
  2) If ongoing work exists: create/update HF: `context/handoff/HF_<slug>_<name>.md` and register in `context/handoff/INDEX.md`
  3) Drop a 6-line Context Card in-topic (Goal/Now/Next3/Decisions/Proof/Recurring)

## Completion criteria
- Git commit exists with the updated SSOT/HF/Index.

## Escalation
- If ambiguous: do not guess. Create HF skeleton + ask for identifiers (topic+keywords+expected artifact).
