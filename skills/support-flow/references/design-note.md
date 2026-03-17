# Design Note — support-flow v0.1

## Skill Name Decision

**Chosen**: `support-flow`

Rationale:
- `inter-agent-support-flow` is more precise but verbose
- `support-intake-execution` front-loads intake, missing the full lifecycle
- `support-flow` is short, self-describing, and directly indicates the lifecycle pattern
- Canonical reference: `TASK-20260317-INBOXDEV-SUPPORT-FLOW-01`

## State Machine Decisions

```
OPEN → WORKING → RESULT_SENT → CLOSED
                      ↓
                  REVISION → RESULT_SENT → CLOSED
```

**Why minimal (5 states)**:
- Protocol clarity over automation coverage
- WORKING signals active pickup without granular sub-steps
- REVISION is the only loop-back; max 2 revision rounds before escalation
- CLOSED covers both full and partial close (differentiated by `close_type`)

**Omitted on purpose (v0.1)**:
- TRIAGE state — handled inline by executor on pickup
- BLOCKED as a terminal state — represented by `close_type: partial` + follow-up request
- ESCALATED — handled by stop conditions in SKILL.md

## Relation Coverage

| Relation | Transport recommendation |
|---|---|
| topic↔topic | doc-only (canonical path) |
| agent↔agent (same server) | `sessions_send` OR doc-only |
| agent→subagent | `sessions_spawn` (new task) |
| cross-server | doc-only + GitHub canonical |

Rule: doc-only is always the fallback. Tool transport only when live coordination adds value.

## Artifact Naming Convention

| Artifact | Naming pattern |
|---|---|
| Request file | `CHEONGMYO_SUPPORT_REQUEST_{SLUG}_{DATE}.md` |
| Batch request | `CHEONGMYO_SUPPORT_REQUEST_BATCH_{DATE}.md` |
| Result file | `SUPPORT_RESULT_{SLUG}_{DATE}.md` |
| Feedback file | `SUPPORT_FEEDBACK_{SLUG}_{DATE}.md` |
| Close file | `SUPPORT_CLOSE_{SLUG}_{DATE}.md` |

Request ID: `TASK-{YYYYMMDD}-{LANE}-{SLUG}-{NN}`

## Intended Upgrade Path

### v0.1 (current)
- Internal operating protocol
- Markdown templates + state machine
- Manual transport (doc-only or sessions_send/spawn)
- Used first by: topic-60 ↔ inbox-dev, cheongmyo ↔ heukmyo

### v0.2 (next)
- Add triage automation (field validation + human gate detection)
- Add periodic scan / watcher for new requests at canonical paths
- Integrate with READY queue / handoff index

### v0.3+
- Template-driven bounded support execution
- Request ↔ result artifact linking
- Priority-based routing

### Future (aoi-pro-beta-dist)
- Full productization only after internal repeatability is proven
- Do not prematurely productize

## v0.2 Changes

### What changed from v0.1

**1. Canonical path split**
- v0.1: all files flat in `requests/`
- v0.2: `support/requests/` / `support/results/` / `support/closed/`
- Reason: REQUEST + RESULT + CLOSE mixed in one dir caused confusion when scanning

**2. Partial close rule explicit**
- v0.1: partial close existed but handling was implicit
- v0.2: `Remaining` + `Follow-up request` required; state never silently upgraded
- Reason: real run (STITCH_MCP PoC) revealed partial close is common, needs clear rules

**3. Watcher script added**
- v0.2: `scripts/watcher.py` — scans canonical paths, detects OPEN/WORKING requests
- Reason: no signal when executor picks up a request → WORKING state transition now explicit
- v0.1 gap: REQUEST → WORKING had no marker; now executor updates state field

**4. Triage rules formalized**
- v0.2: field check + human gate scan + scope check + reference check documented in `references/watcher.md`
- Reason: v0.1 triage was implicit; v0.2 makes it checkable

### Real run findings (TASK-20260317-INBOXDEV-STITCH-MCP-POC-01)
- Partial close + human gate blocker was the most natural outcome — not an edge case
- `requests/` flat structure mixed REQUEST/RESULT/CLOSE immediately — split confirmed needed
- watcher correctly detected OPEN state on the REQUEST file — confirms value of state field

## v0.1 Close Criteria (from request spec)

- [x] Skill created with SKILL.md
- [x] Templates: REQUEST / RESULT / FEEDBACK / CLOSE
- [x] State machine defined
- [x] End-to-end examples: GitHub intake + agent→subagent + feedback revision
- [x] Rollout guidance documented
- [ ] Deployed to aoi-skills repo (pending)
- [ ] One real run logged (pending)
