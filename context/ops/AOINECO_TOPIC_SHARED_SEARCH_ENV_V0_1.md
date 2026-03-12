# AOINECO_TOPIC_SHARED_SEARCH_ENV_V0_1.md

Status: SSOT (local)
Last updated: 2026-03-13

## Purpose
Create a shared search environment so any Aoineco agent can inspect the current state of any topic/project, resume naturally, and perform follow-on work based on durable evidence instead of conversational memory.

## Core rule
Before answering from memory or starting new work in a topic/project, agents should search the durable topic layer first.

Search order:
1. topic-state
2. playbook
3. handoff / HF
4. decision/proof artifacts
5. topic index

## What this environment must provide
For each active topic/project, the shared layer should expose at least:
- topic slug
- topic id
- owner / role expectation
- current purpose
- recurring tasks
- key facts to remember
- current state / next
- escalation rule
- canonical file paths
- last updated timestamp when available

## Canonical components
### A. topic-state docs
Primary quick-resume anchors under:
- `context/topic-state/`

### B. playbooks
Operational rule docs under:
- `context/topics/`
- other topic-specific SSOT paths when needed

### C. handoff / HF
Tracked transition anchors under:
- `context/handoff/`

### D. shared topic index
Cross-topic lookup file:
- `context/telegram_topics/TOPIC_STATUS_INDEX_V0_1.md`

## Agent rule
When a task touches an existing topic/project:
1. search the shared layer first
2. do not rely on vague memory if topic-state/playbook exists
3. quote or align with durable state before extending the work
4. if new recurring knowledge appears, promote it back into SSOT/state

## Update obligation
When a topic/project becomes active or changes materially, agents should update:
- topic-state
- playbook or handoff if needed
- shared topic index summary if the quick-resume view changed

## Goal
Any agent should be able to:
- ask “what is this topic doing now?”
- locate the current operating base quickly
- continue work without guessing
- perform follow-on work on top of durable context

## Scope
This applies to all internal operational topics and projects, including Ralph Loop-linked topics and handoff/takeover contexts.
