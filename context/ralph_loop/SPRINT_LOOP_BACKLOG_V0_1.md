# SPRINT_LOOP_BACKLOG_V0_1

Owner: ralph-loop (Topic 68)
Status: SSOT

## Purpose
Sprint Loop(4-topic batch)으로 DM export/운영 백로그를 **토픽별 SSOT(Playbook/HF)로 병합**하고, 충돌 없이 Safe Promotion까지 수행한다.

## Sprint definition
- 1 Sprint = 4 topics
- Standard deliverables per topic:
  1) Shadow Ingest: Playbook에 `Imported from DM export (Shadow Ingest)` 섹션 + 반복업무 Top N + Proof 1+
  2) Automation candidates: launchd vs Ralph Loop 분류
  3) Safe Promotion patch: 토픽에 ‘작은 패치’ 배포 + ADOPT/HOLD/CONFLICT 회신 수집

## Governance (L1/L2/L3)
- L1/L2: 자동 진행(완료 후 proof-only 리포트)
- L3: 승인 필요(돈/키/서명/온체인/외부게시/권한변경/비가역)

## Current cycle

### Sprint 1 (DONE → ADOPT confirmed)
- Topics: ops / maintenance / inbox-dev / github
- Decision:
  - ADOPT (confirmed by 메르세데스, 2026-03-08)
- Proof:
  - Commit: `2602b51` (Sprint1 shadow-ingest playbooks)
  - Commit: `daf5645` (automation candidates Sprint1)
  - Commit: `67fdf76` (launchd audit report)
  - Safe Promotion msgs: ops=3190, github=3191, maintenance=3192, inbox-dev=3193
  - Audit post: maintenance(77) msgId=3189

### Sprint 2 (DONE → ADOPT confirmed)
- Topics: acp / adp / handoff / ralph-loop
- Decision:
  - ADOPT (confirmed by 메르세데스, 2026-03-08)
- Proof:
  - Commit: `23a08cb` (Sprint2 shadow-ingest playbooks + automation candidates)
  - Safe Promotion msgs: acp=3194, adp=3195, handoff=3196, ralph-loop=3198

### Sprint 3 (NEXT)
- Topics: v6-invest / x-post / longform / hackathons
- Deliverables: same as above

### Sprint 4 (NEXT)
- Topics: bazaar / moltbook / random / (none/untagged triage)
- Deliverables: same as above

## Notes
- DM export merge policy: `context/ops/DM_EXPORT_SHADOW_INGEST_AND_SAFE_PROMOTION_POLICY_V0_1.md`
- Launchd audit report: `context/ops/MAINTENANCE_LAUNCHD_AUDIT_REPORT_2026-03-08_V0_1.md`
