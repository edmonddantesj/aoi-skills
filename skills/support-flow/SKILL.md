---
name: support-flow
description: Inter-agent support lifecycle protocol. Use when: (1) structuring a support request between any two topics, agents, or subagents, (2) submitting or receiving a support result, (3) handling feedback or revision rounds, (4) closing a support request with artifacts, (5) deciding whether to use sessions_send vs sessions_spawn vs doc-only flow. Applies to topic↔topic, agent↔agent, agent↔subagent, and cross-server agent support. NOT for: direct external publishing, production deploys, or actions requiring human gate approval.
---

# Support Flow

Standardizes the full support lifecycle between any requester and executor pair —
topic, agent, subagent, or cross-server agent.

**Design principle: protocol first → tool-assisted second → automation later.**

## State Machine

```
OPEN → WORKING → RESULT_SENT → CLOSED
                      ↓
                  REVISION → RESULT_SENT → CLOSED
```

| State | Meaning |
|---|---|
| `OPEN` | Request created, not yet picked up |
| `WORKING` | Executor has started |
| `RESULT_SENT` | Result delivered, awaiting feedback or close |
| `REVISION` | Feedback received, revision in progress |
| `CLOSED` | Accepted and closed (or closed-partial) |

## Request ID Convention

```
TASK-{YYYYMMDD}-{LANE}-{SLUG}-{NN}
```

Example: `TASK-20260317-INBOXDEV-SUPPORT-FLOW-01`

## Transport Selection

| Situation | Use |
|---|---|
| Same-server session reachable | `sessions_send` |
| New isolated task needed | `sessions_spawn` |
| No live session / async OK | doc-only (file at canonical path) |
| Cross-server, no direct channel | doc-only + GitHub canonical |

**Default**: prefer doc-only first. Add tool transport only when live coordination is needed.

## Stop / Escalation Conditions

**Stop and flag** when:
- Required fields missing → return to requester
- Human gate item found inside scope → `NEEDS_HUMAN_REVIEW`, do not proceed
- Canonical path unavailable → block until resolved
- Executor cannot produce L1/L2 artifact → `blocked` state, document reason

**Escalate** when:
- External submit / publish / deploy required
- Policy or org-structure change needed
- Result impacts production systems
- Revision rounds > 2 without resolution

## Human Gate (never auto-execute)

External publish · production deploy · policy change · org change · approval-gated external system

## Templates & Examples

See `references/templates.md` — all four templates (REQUEST / RESULT / FEEDBACK / CLOSE) + three end-to-end example flows.

## Rollout Path

1. **Now**: Use as internal operating protocol (청묘팀 ↔ 흑묘팀, topic↔topic)
2. **Next**: Add `sessions_send`/`sessions_spawn` tooling where live coordination helps
3. **Later**: Promote to productized workflow in `aoi-pro-beta-dist` once repeatability is proven

## Design Note

See `references/design-note.md` for: chosen name rationale, state machine decisions, and intended upgrade path.
