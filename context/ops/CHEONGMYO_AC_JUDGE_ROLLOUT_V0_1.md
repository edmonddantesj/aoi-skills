# CHEONGMYO_AC_JUDGE_ROLLOUT_V0_1

Status: DRAFT SSOT
Last updated: 2026-03-14
Scope: Cheongmyo team rollout of Acceptance Criteria / Judge Pipeline / fail-only review discipline

## 1. Purpose
This document adapts the Heukmyo-side AC/Judge discipline into a practical rollout plan for Cheongmyo team.

Goal:
- do not replace the current STATUS / HANDOFF / one-line next structure
- add a criteria layer on top of it
- make completion / failure / hold / human-review boundaries explicit
- improve takeover-readiness and automation-readiness

## 2. Core interpretation
Cheongmyo should not treat this as a heavy QA framework.
This is a lightweight operating rule for active lanes:
1. STATUS
2. HANDOFF
3. one-line next action
4. Definition of Done / Acceptance Criteria
5. Judge or review rule

## 3. Preferred judgment language
Use:
- `pass`
- `fail`
- `hold`
- `needs-human-review`

Avoid:
- vague “done enough” style wording
- “이어가면 됨” as a final state
- “나중에 보면 됨” without a condition

## 4. Minimal criteria layer format
Attach this block to active topic docs when possible.

### Definition of Done
- What minimum state counts as done for this packet/topic step?

### Acceptance Criteria
- What concrete checks must pass?

### Judge rule
- Who or what decides pass/fail/hold?

### Human gate
- Under what condition must a human explicitly review/approve?

## 5. Phase 1 rollout set (immediate)
### A. hackathons
Why:
- narrative, submission package, and external-facing output quality matter
- completion can be judged clearly

Minimum AC/Judge shape:
- DoD: customer/problem/value/revenue/submission narrative packet exists
- AC: submission-form-ready paragraph set, external tone, no major contradiction with locked business logic
- Judge: pass if directly re-usable in application form; hold if narrative exists but still too internal; needs-human-review at final submission/public use

### B. v6-invest
Why:
- implementation scope easily drifts without criteria
- L2/L3 boundary is critical

Minimum AC/Judge shape:
- DoD: P1 scope and implementation order locked
- AC: probability calibration, directional edge definition, executable edge filter, decision object normalization each have a clear next module/task
- Judge: pass if implementation-ready; hold if only conceptual; needs-human-review at real money / external account / live execution gates

### C. ops / fallback
Why:
- recovery status and next check should never be vague
- fail-only review is especially useful here

Minimum AC/Judge shape:
- DoD: incident state, cause hypothesis, current health, next check, fallback path recorded
- AC: reboot/host symptoms, OpenClaw state, recovery action, and follow-up observation are explicit
- Judge: pass if incident is bounded and next monitoring rule exists; fail if core evidence missing; needs-human-review if host-level/manual actions required

### D. longform / ralph-loop recovered study lane
Why:
- study lanes easily become “interesting but undefined” without explicit completion rules

Minimum AC/Judge shape:
- DoD: source packet converted into reusable study/execution packet
- AC: source summary, reuse angle, execution lane, and next action are explicit
- Judge: pass if it is ready for Ralph-loop synthesis or adoption work; hold if still just raw intake

## 6. Phase 2 rollout set
### A. inbox-dev
- DoD: verdict + next action + adoption lane are explicit
- Judge: `PROPOSE / READY / HOLD / DROP` becomes operationally meaningful

### B. adp
- DoD: asset/roster/structure change has clear effect and next action
- Judge: useful for separating stable structure from unresolved strategy

### C. bazaar
- DoD: build/proof/scope/checkpoint/public-safe state are explicit
- Judge: especially important for pass/hold/needs-human-review around publish/admin/receipt/verify flows

### D. ralph-loop
- DoD: repeated packet has cadence/trigger/proof/return rule
- Judge: prevents “repeated work” from becoming shapeless repetition

## 7. Phase 3 rollout set
- ACP
- external-resource-attached lanes
- broader ADP/strategic lanes when L3 boundaries become relevant

## 8. Application rule
### Rule 1
Do not rewrite whole playbooks first.
Add criteria layer to active docs incrementally.

### Rule 2
Apply to packets/active lanes before trying to standardize every dormant topic.

### Rule 3
If a topic already has STATUS + HANDOFF + next action, add AC/Judge there first.

### Rule 4
If there is no one-line next action yet, create that before adding fancier criteria.

## 9. Fail-only review principle
The review burden should focus on missing or failed criteria.
Not everything needs deep manual rereading every time.

Preferred pattern:
- criteria visible
- failed/missing items visible
- human attention pulled only where necessary

## 10. Immediate rollout recommendation
Cheongmyo should first attach AC/Judge blocks to these 7 lanes:
- hackathons
- v6-invest
- ops
- inbox-dev
- adp
- ralph-loop
- bazaar

Interpretation:
- these are the lanes where completion ambiguity, handoff value, and automation leverage are all high enough to justify immediate rollout

## 11. One-line summary
Cheongmyo team should adopt Acceptance Criteria / Judge discipline by layering Definition of Done, acceptance checks, and pass/fail/hold/human-review rules onto active topic STATUS/HANDOFF structures first, starting with 7 high-value lanes.
