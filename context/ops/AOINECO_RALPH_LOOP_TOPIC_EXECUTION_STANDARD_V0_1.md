# AOINECO_RALPH_LOOP_TOPIC_EXECUTION_STANDARD_V0_1.md

Status: SSOT (local)
Last updated: 2026-03-13

## Purpose
Standardize how work moves from a domain topic into Ralph Loop, and define what must happen after L1/L2 approval so the operating split becomes a real execution loop rather than a paper-only division.

## Core split
### Domain topic
The source topic keeps:
- domain meaning and scope
- topic-specific decisions
- final deliverable definition
- final acceptance / submission criteria
- external-facing package truth

### Ralph Loop
Ralph Loop owns:
- repeated intake / triage / decomposition
- backlog slicing
- checkpoint packets
- repeated proof-first execution packets
- repeated scout / benchmark / signal / synthesis loops
- queue / throughput / WIP discipline
- deciding whether work becomes HF / task card / topic-local note

### Human gate
Human gate remains only for:
- manual / external / identity-bearing acts
- irreversible submission / payment / signing / outward publication

## Approval meaning
### L1 approval
L1 means:
- the work is confirmed as repeatable/internal enough to be routed into Ralph Loop
- source topic truth and Ralph Loop truth are separated
- proof location and escalation path are known

L1 is **candidate approval**.
It means “this belongs in Ralph Loop shape.”

### L2 approval
L2 means:
- the repeated execution loop is now active
- Ralph Loop is expected to actually run the recurring work
- cadence / trigger / packet shape / output path / return rule are fixed

L2 is **active execution approval**.
It means “do not just define the split — run it.”

## Required execution fields after L2
If work is marked L2, the following must be explicit somewhere in playbook/state/handoff:
1. **source topic**
2. **target execution lane** (`ralph-loop`)
3. **recurring task shapes**
4. **cadence or trigger**
   - examples: daily, on-event, backlog-nonempty, checkpoint-based
5. **artifact rule**
   - where proof / task packets / checkpoint outputs land
6. **return rule**
   - what gets handed back to the source topic
7. **escalation rule**
   - when it must return to main-session or human gate

If these are missing, the split is not fully operational yet.

## Non-operational anti-pattern
The following state is considered incomplete:
- topic ↔ Ralph Loop boundary is documented
- but no one knows when Ralph Loop should run
- no cadence/trigger is defined
- no packet shape is defined
- no proof path is defined
- no return rule is defined

This is **division without execution** and should be treated as unfinished.

## Standard operating sequence
1. Identify repeated internal work in a domain topic.
2. Separate source-topic truth from repeated operational work.
3. Approve L1 if the work is Ralph-loop-shaped.
4. Approve L2 only when execution fields are fixed.
5. Start repeated execution from Ralph Loop.
6. Return domain-relevant outputs/checkpoints back to the source topic.
7. Escalate to human gate only at manual/external boundaries.

## Recommended trigger patterns
### backlog-nonempty
Use when there is a queue/backlog waiting for decomposition.

### checkpoint-based
Use when the source topic repeatedly needs `today / blocker / next` packaging.

### deadline sweep
Use when repeated urgency scanning is required (hackathons, submissions, time windows).

### discovery cadence
Use when repeated scouting/benchmarking is core work (x-post, hackathons, signals).

## Artifact standard
Ralph Loop repeated execution should leave at least one of:
- task card / ledger item
- checkpoint packet
- HF / handoff entry
- proof log / evidence bundle
- topic-state update

## Example split patterns
### Hackathons
- source topic keeps event/package/submission truth
- Ralph Loop runs scout / deadline sweep / benchmark / signal / synthesis

### X-post
- source topic keeps editorial truth and final draft package
- Ralph Loop runs discovery / anti-dup / quote extraction / draft packet assembly / blocker logging

### Bazaar
- source topic keeps product/build/demo truth
- Ralph Loop runs backlog slicing / checkpoint packet / proof route / scope guard

## Short reusable wording
> Topic rooms keep domain truth. Ralph Loop owns repeated internal execution. L1 means candidate routing approval. L2 means the recurring execution loop must actually run with cadence, packet shape, proof path, and return rule fixed.
