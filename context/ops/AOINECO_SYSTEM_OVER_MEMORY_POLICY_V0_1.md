# AOINECO_SYSTEM_OVER_MEMORY_POLICY_V0_1.md

Status: SSOT (local)
Last updated: 2026-03-13

## Intent
Aoineco & Co. should not run repeated internal work by relying on chat memory, urgency, or human recollection.
The operating default is:

**memory-dependent operation → system-dependent operation**

This policy promotes repeated, proof-based, internal work into SSOT, checklists, handoff artifacts, and automation-ready structures.

## Core policy
1. If a task is repeatable, evidence-based, and internal, do not leave it only in conversational memory.
   - Promote it into SSOT, playbooks, checklists, runbooks, README, handoff docs, or automation docs.
2. If a task must keep running even when the user is absent, move it into a persistent execution lane.
   - Default execution lane: **Ralph Loop** for decomposition / throughput / repeated operational handling.
3. Human intervention should be reserved for **manual / external gates** only.
   - Examples: login, identity confirmation, KYC, captcha, payment, signing, final submit approval, external publishing/sending.
4. Submission / application / operations work should be run in **preparation-first mode**.
   - Do not wait for last-minute urgency.
   - Prepare build, repo, README, demo, proof bundle, submit copy, and required artifacts in advance.
5. The goal is not shallow automation.
   - Reduce last-minute confusion
   - Increase success / acceptance / award probability
   - Accumulate reusable operating assets
   - Strengthen long-term team capability

## Operating consequences
### Promote to SSOT when
- a rule repeats more than once
- a task has clear acceptance criteria or proof
- the same explanation would otherwise need to be repeated in chat
- a failure mode should not be relearned from scratch
- a topic/project has stable role boundaries, recurring tasks, or key memory points that should survive context loss

### Topic hardening obligation
For each active topic/project, sweep existing memory/handoff/playbook/state docs and promote at least the following into durable SSOT/state form when missing:
- topic role / owner expectation
- current purpose and scope boundary
- recurring tasks
- key facts that must survive context loss
- current state / next / escalation rule

The goal is that agents can resume naturally and answer consistently even after interruption, compacting, or handoff.

### Allowlist friction rule
If a user explicitly instructs that SSOT/memory promotion should proceed and a first write/commit is blocked only by allowlist friction, treat that as user auto-approval to add the minimum necessary allowlist entry and continue.

Constraints:
- Keep the allowlist change minimal and scoped to the intended SSOT/memory files only.
- Do not treat this as blanket approval for unrelated paths.
- Record the change in durable docs or commit history when possible.

### Move to Ralph Loop when
- the work is repeated
- it can be decomposed into packets / checkpoints / queue items
- it benefits from throughput, backlog control, dedupe, or periodic sweep

Reference:
- `context/ops/RALPH_LOOP_BUSINESS_WIDE_APPLICATION_POLICY_V0_1.md`

### Keep in main session when
- the user is deciding direction
- the work is ambiguous / strategic / identity-sensitive
- escalation or final human judgment is required

### Human gate required when
- external account actions are needed
- legal / financial / trust-bearing actions are involved
- the final irreversible submission or publication must happen

## Minimum artifact standard
For repeated operational work, the minimum package should contain:
- one SSOT/playbook/rule doc
- one checklist or acceptance list
- one handoff or tracked state anchor
- one proof location or evidence rule
- one escalation rule for human/manual gates

## Standard wording (short form)
Use this wording when promoting a repeated rule into a topic or project:

> This work must not depend on conversational memory alone. Repeated internal execution should be fixed into SSOT/checklists/handoff/proof structures, and moved into Ralph Loop or automation lanes when it must continue without the user.

## Shared search rule
All agents should be able to inspect shared topic state before continuing work.

Shared search environment:
- `context/ops/AOINECO_TOPIC_SHARED_SEARCH_ENV_V0_1.md`
- `context/telegram_topics/TOPIC_STATUS_INDEX_V0_1.md`

Default expectation:
- search durable topic state first
- continue from indexed files
- promote newly stabilized recurring knowledge back into SSOT/state

## Scope
This is a company-wide operating rule.
It is not limited to Topic 71 or builder-only workflows.
