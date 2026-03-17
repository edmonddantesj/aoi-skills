# Templates & Examples

## Template 1: SUPPORT_REQUEST

```md
---
request_id: TASK-{YYYYMMDD}-{LANE}-{SLUG}-{NN}
state: OPEN
date: YYYY-MM-DD
requester: <topic-slug | agent-name>
executor: <topic-slug | agent-name | "TBD">
priority: P0 / P1 / P2
---

## Request

- **From**: <requester>
- **To**: <executor>
- **Relation**: topic↔topic / agent↔agent / agent↔subagent / cross-server
- **Priority**: P0 / P1 / P2
- **Deadline**: <YYYY-MM-DD or "this cycle">

### Current state
<what's done / not done / bottleneck — 3 lines max>

### Goal
<outcome-based: "produce X so that Y">

### Needed support
<what to produce — not "help me", but "create X / review Y / structure Z">

### Expected output type
research memo | checklist | draft | implementation plan | review | SSOT draft | structured notes | handoff artifact

### Constraints / human gate
<external submit, publish, deploy, policy change → these stay human-gated>

### Reference paths
- <path or URL>
```

---

## Template 2: SUPPORT_RESULT

```md
---
request_id: <same as request>
state: RESULT_SENT
date: YYYY-MM-DD
executor: <who completed>
---

## Result

- **State**: done | partial | blocked | needs-human-review
- **What was done**: <1–3 line summary of actual work>
- **Output**:
  - <artifact type + path or description>
- **Next** (for requester): <one clear action>
- **Blocker / human gate**: <what can't proceed without human — or "none">
- **Updated paths**:
  - <new or modified files>
- **Promote candidate**: no | local-protocol | SSOT-candidate
```

---

## Template 3: SUPPORT_FEEDBACK

```md
---
request_id: <same as request>
state: REVISION
date: YYYY-MM-DD
from: <requester>
---

## Feedback

- **Overall**: accept | accept-with-notes | revision-needed | blocked
- **Notes**:
  <specific change requests — numbered if multiple>
- **Revision scope**: <what needs to change — stay bounded>
- **Deadline for revision**: <YYYY-MM-DD or "same cycle">
```

---

## Template 4: SUPPORT_CLOSE

```md
---
request_id: <same as request>
state: CLOSED
date: YYYY-MM-DD
closed_by: <requester or executor>
close_type: full | partial
---

## Close Summary

- **Completed**: <what was fully done>
- **Remaining** (if partial): <what was not done + why>
- **Artifacts**:
  - <final artifact paths>
- **Promoted**: no | local-protocol | SSOT-candidate
- **Follow-up request**: <next request ID if partial, or "none">
- **Reflection**:
  <1–3 lines: what worked / what to improve next time>
```

---

## Example Flow A: GitHub Intake → Benchmark → Result → Close

**Scenario**: Topic 60 (GitHub adoption intake) evaluates a new library reference and needs an implementation benchmark from inbox-dev.

### Step 1 — REQUEST (topic-60 → inbox-dev)
```md
request_id: TASK-20260317-INBOXDEV-BENCHMARK-01
state: OPEN
requester: topic-60
executor: inbox-dev
priority: P1

## Request
- From: topic-60 (GitHub adoption intake)
- To: inbox-dev
- Relation: topic↔topic
- Priority: P1
- Deadline: this cycle

### Current state
Evaluated `viem` v2.x as replacement for `ethers.js` in Base Batches flow. Opinion: adopt. Need proof.

### Goal
Produce a minimal benchmark showing viem v2 works for Base tx signing + send in the current codebase.

### Needed support
Create a benchmark script (or draft) for viem v2 → Base tx signing flow; document result.

### Expected output type
implementation plan + draft benchmark script

### Constraints / human gate
No production deployment. Script runs in dry-run / testnet only.

### Reference paths
- context/github/GITHUB_ADOPTION_PACK_VIEM_V2_20260317.md
- repos/aoi-basebatches-demo/src/
```

### Step 2 — RESULT (inbox-dev → topic-60)
```md
request_id: TASK-20260317-INBOXDEV-BENCHMARK-01
state: RESULT_SENT
executor: inbox-dev

## Result
- State: done
- What was done: Implemented viem v2 signing stub, ran against Base Sepolia testnet, tx confirmed.
- Output: benchmark script + testnet tx hash as proof
- Next: topic-60 updates adoption pack with "verified" status
- Blocker / human gate: mainnet deploy requires human gate
- Updated paths:
  - repos/aoi-basebatches-demo/scripts/benchmark_viem_v2.ts
  - context/github/GITHUB_ADOPTION_PACK_VIEM_V2_20260317.md (proof section)
- Promote candidate: local-protocol
```

### Step 3 — CLOSE (topic-60 closes)
```md
request_id: TASK-20260317-INBOXDEV-BENCHMARK-01
state: CLOSED
close_type: full

## Close Summary
- Completed: viem v2 benchmark verified, adoption pack updated
- Remaining: none
- Artifacts: benchmark_viem_v2.ts + updated adoption pack
- Promoted: local-protocol (benchmark pattern reusable)
- Follow-up request: none
- Reflection: topic↔topic handoff worked cleanly; canonical path discipline made pickup immediate.
```

---

## Example Flow B: Agent → Subagent Support Request

**Scenario**: 청묘팀 main session needs a structured research memo from a spawned subagent.

### Step 1 — REQUEST (청묘 → subagent)
```md
request_id: TASK-20260317-SUBAGENT-RESEARCH-01
state: OPEN
requester: cheongmyo-main
executor: subagent (to be spawned)
priority: P1

## Request
- From: cheongmyo-main
- To: subagent (sessions_spawn)
- Relation: agent→subagent
- Priority: P1
- Deadline: same session

### Current state
Need competitive analysis on Polymarket vs Limitless UX/product positioning. No prior doc exists.

### Goal
Produce a 1-page comparison memo ready for strategy review.

### Needed support
Research memo: Polymarket vs Limitless on (1) market types, (2) UX, (3) fee structure, (4) differentiation

### Expected output type
research memo

### Constraints / human gate
No external posting. Internal use only.

### Reference paths
- context/topics/v6-invest_PLAYBOOK_V0_1.md
```

### Step 2 — RESULT (subagent → parent)
```md
request_id: TASK-20260317-SUBAGENT-RESEARCH-01
state: RESULT_SENT
executor: subagent-oracle-research

## Result
- State: done
- What was done: Searched and synthesized Polymarket vs Limitless on 4 axes
- Output: research memo (1 page)
- Next: parent session reviews and decides whether to promote to SSOT
- Blocker / human gate: none
- Updated paths:
  - context/research/POLYMARKET_VS_LIMITLESS_MEMO_20260317.md
- Promote candidate: SSOT-candidate
```

---

## Example Flow C: Feedback + Revision Round

**Scenario**: Result returned, but requester needs one revision before closing.

### Step 1 — RESULT received (state: RESULT_SENT)
*(same structure as Template 2)*

### Step 2 — FEEDBACK
```md
request_id: TASK-20260317-INBOXDEV-BENCHMARK-01
state: REVISION
from: topic-60

## Feedback
- Overall: revision-needed
- Notes:
  1. Add gas estimate comparison (viem v2 vs ethers.js)
  2. Confirm testnet tx hash is retrievable from output log
- Revision scope: benchmark script only, not the adoption pack
- Deadline for revision: today
```

### Step 3 — REVISED RESULT (state: RESULT_SENT again)
```md
request_id: TASK-20260317-INBOXDEV-BENCHMARK-01
state: RESULT_SENT

## Result
- State: done
- What was done: Added gas estimate comparison table; tx hash now logged to stdout
- Output: updated benchmark_viem_v2.ts
- Next: topic-60 final review + close
- Blocker / human gate: none
- Updated paths:
  - repos/aoi-basebatches-demo/scripts/benchmark_viem_v2.ts (rev2)
- Promote candidate: local-protocol
```

### Step 4 — CLOSE
*(same structure as Template 4)*
