---
name: openclaw-telegram-topics-router
description: Set up and maintain Telegram forum Topics routing for OpenClaw. Use when a user wants to split a Telegram group chat into forum topics (threads) and route agent output/cron announcements by topic. Includes SSOT templates (topics definition + thread_id map) and scripts to initialize and update mappings.
---

# OpenClaw Telegram Topics Router

## What this skill gives you
- A lightweight **SSOT layout** for Telegram forum topics:
  - Topic taxonomy + rules file
  - `thread_id → topic_slug` mapping file
- Deterministic scripts to initialize and maintain the mapping.

## Files (SSOT)
Created/used under your workspace:
- `context/telegram_topics/TOPICS_DEFINITION_V0_1.md`
- `context/telegram_topics/thread_topic_map.json`
- `context/telegram_topics/thread_workstream_map.json` (optional: per-thread friendly name)
- `context/telegram_topics/thread_agent_map.json` (optional: per-thread primary agent + collaborators)

## Quick start
1) Initialize SSOT files:
   - Run: `python3 skills/public/openclaw-telegram-topics-router/scripts/init_topics_ssot.py`

2) Create Telegram forum topics (manual in Telegram UI)
   - Recommended starter set: `announcements`, `ops`, `maintenance`, `adp`, `acp`, `bazaar`, `github`, `longform`, `ralph-loop`, `hackathons`, `inbox-dev`, `handoff`, `random`.

3) Calibrate mapping (one-time per topic)
   - In each topic/thread, send a message like: `@<your_bot_username> ping`
   - Then run mapping command (repeat per topic):
     - `python3 skills/public/openclaw-telegram-topics-router/scripts/add_mapping.py --slug ops --thread-id 38`

4) Audit
   - `python3 skills/public/openclaw-telegram-topics-router/scripts/audit_map.py`
   - (optional) `python3 skills/public/openclaw-telegram-topics-router/scripts/audit_workstreams.py`

## Operating rule (recommended)
- In chat, never claim a topic mapping exists without proof.
- For operational reporting, combine this with Proof-first:
  - `context/protocols/PROOF_FIRST_STATUS_PROTOCOL_V0_1.md`

## Workstream naming (recommended)
If you want to declare a topic as a dedicated workstream ("이 토픽을 'xx' 작업 스레드로 고정/명명"), store a friendly name per thread.

## Topic → Primary agent routing (recommended)
If you want one default sub-agent (role) per topic/thread, store primary agent per thread.

## Workstream lock registry (prevent duplicated/conflicting work)
When multiple topics run in parallel, tasks can overlap (same file/pipeline) and cause conflicts.
This skill can maintain a lightweight **exclusive lock registry** (SSOT) keyed by lock strings.

## Cross-topic task handoff + queue (NEW)
You can hand off tasks from one topic to another by registering them into a lightweight **task queue SSOT**.
This enables priority-based dispatch with a configurable concurrency limit (default 3) and lock-aware scheduling.

### SSOT
- `context/ops/task_queue.json`

### Initialize queue SSOT
```bash
python3 skills/public/openclaw-telegram-topics-router/scripts/init_task_queue_ssot.py --chat-id telegram:-100...
```

### Enqueue a task (handoff)
```bash
python3 skills/public/openclaw-telegram-topics-router/scripts/enqueue_task.py \
  --title "Notion mirror incremental upsert" \
  --target-slug inbox-dev \
  --priority P1 \
  --policy L2 \
  --ledger-id RL-20260306-023
```

### Dispatch (select next work)
```bash
# plan only (marks in_progress and/or blocked based on locks/policy)
python3 skills/public/openclaw-telegram-topics-router/scripts/dispatch_queue.py

# optional: execute tasks that have exec_cmd set
python3 skills/public/openclaw-telegram-topics-router/scripts/dispatch_queue.py --execute
```

### Chat command parsing (optional)
```bash
python3 skills/public/openclaw-telegram-topics-router/scripts/parse_handoff_command.py \
  --text "#handoff ops P1 Fix inbound watcher"
```

### SSOT
- `context/telegram_topics/workstream_lock_map.json`

### Initialize
```bash
python3 skills/public/openclaw-telegram-topics-router/scripts/init_workstream_locks_ssot.py --chat-id telegram:-100...
```

### Claim / release locks
```bash
# claim a lock for a task
python3 skills/public/openclaw-telegram-topics-router/scripts/claim_workstream_lock.py \
  --lock scripts/notion_mirror_sync.py \
  --ledger-id RL-20260306-026 \
  --thread-id 68 \
  --owner "Blue-Gear"

# audit current locks
python3 skills/public/openclaw-telegram-topics-router/scripts/audit_workstream_locks.py

# release a lock
python3 skills/public/openclaw-telegram-topics-router/scripts/release_workstream_lock.py \
  --lock scripts/notion_mirror_sync.py \
  --ledger-id RL-20260306-026
```

### Policy (recommended)
- Before starting a task in a topic, **claim required locks**.
- If a lock is already claimed, either:
  - merge/supersede the task, or
  - split scope, or
  - wait until released.

## Delegation mode (ops policy)
- A-mode (manual): delegate only when `#delegate` is present.
- **B-mode (default): auto-delegate** to the primary agent when a message arrives, with noise filters + cooldown + L3 fail-closed.
- SSOT: `context/telegram_topics/DELEGATION_POLICY_V0_1.md`

### Execution-layer building blocks (included)
These scripts are deterministic helpers you can embed into an inbound router:
- `scripts/delegation_decider.py` — decide should_delegate from message text
- `scripts/delegation_state.py` — cooldown state file helper (180s default)
- `scripts/resolve_primary_agent.py` — thread_id -> primary agent lookup

1) Initialize (one-time):
- `python3 skills/public/openclaw-telegram-topics-router/scripts/init_agent_map_ssot.py --chat-id telegram:-100...`

2) Set primary agent:
- `python3 skills/public/openclaw-telegram-topics-router/scripts/set_agent_for_thread.py --thread-id 38 --primary Blue-Gear --collab Blue-Blade`

3) Attendance parser helper:
- `python3 skills/public/openclaw-telegram-topics-router/scripts/parse_attendance_command.py --text "#call Blue-Blade Oracle"`
- `python3 ... --text "#council all"`

1) Initialize (one-time):
- `python3 skills/public/openclaw-telegram-topics-router/scripts/init_workstream_ssot.py --chat-id telegram:-100...`

2) Set name (repeat per thread):
- `python3 skills/public/openclaw-telegram-topics-router/scripts/set_workstream.py --thread-id 68 --name "Ralph Loop / WIP" --slug ralph-loop`

3) Parser helper (for higher-level automation):
- `python3 skills/public/openclaw-telegram-topics-router/scripts/parse_workstream_command.py --text "이 토픽을 'Ralph Loop' 작업 스레드로 고정"`

## When you need deeper customization
- Edit topic taxonomy/rules in:
  - `context/telegram_topics/TOPICS_DEFINITION_V0_1.md`
- Add more slugs and thread IDs in:
  - `context/telegram_topics/thread_topic_map.json`
