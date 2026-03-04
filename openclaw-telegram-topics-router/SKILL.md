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

## Operating rule (recommended)
- In chat, never claim a topic mapping exists without proof.
- For operational reporting, combine this with Proof-first:
  - `context/protocols/PROOF_FIRST_STATUS_PROTOCOL_V0_1.md`

## When you need deeper customization
- Edit topic taxonomy/rules in:
  - `context/telegram_topics/TOPICS_DEFINITION_V0_1.md`
- Add more slugs and thread IDs in:
  - `context/telegram_topics/thread_topic_map.json`
