#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/silkroadcat/.openclaw/workspace"
OUT_DIR="$ROOT/artifacts/blackcat_migration"
STAMP="$(date +%Y%m%d_%H%M%S)"
BUNDLE_DIR="$OUT_DIR/blackcat_bundle_$STAMP"
mkdir -p "$BUNDLE_DIR/context/topic-state" "$BUNDLE_DIR/context/topics" "$BUNDLE_DIR/context/telegram_topics" "$BUNDLE_DIR/agents/strategist" "$BUNDLE_DIR/scripts"

cp "$ROOT/agents/strategist/AGENTS.md" "$BUNDLE_DIR/agents/strategist/AGENTS.md"
cp "$ROOT/agents/strategist/SOUL.md" "$BUNDLE_DIR/agents/strategist/SOUL.md"
cp "$ROOT/agents/strategist/USER.md" "$BUNDLE_DIR/agents/strategist/USER.md"
cp "$ROOT/context/topic-state/cat-strategic.md" "$BUNDLE_DIR/context/topic-state/cat-strategic.md"
cp "$ROOT/context/topics/cat-strategic_PLAYBOOK_V0_1.md" "$BUNDLE_DIR/context/topics/cat-strategic_PLAYBOOK_V0_1.md"
cp "$ROOT/context/AOINECO_ROUTER_SPEC_V0_1.md" "$BUNDLE_DIR/context/telegram_topics/AOINECO_ROUTER_SPEC_V0_1.md"
cp "$ROOT/context/AOINECO_ROUTER_OWNER_SELECTION_LOGIC_V0_1.md" "$BUNDLE_DIR/context/telegram_topics/AOINECO_ROUTER_OWNER_SELECTION_LOGIC_V0_1.md"
cp "$ROOT/context/AOINECO_AGENT_TO_AGENT_DIALOGUE_RUNTIME_V0_1.md" "$BUNDLE_DIR/context/telegram_topics/AOINECO_AGENT_TO_AGENT_DIALOGUE_RUNTIME_V0_1.md"
cp "$ROOT/context/CAT_STRATEGIC_ROUTER_CHECKLIST_V0_1.md" "$BUNDLE_DIR/context/telegram_topics/CAT_STRATEGIC_ROUTER_CHECKLIST_V0_1.md"
cp "$ROOT/context/telegram_topics/DISTRIBUTED_BLACKCAT_MIGRATION_PLAN_V0_1.md" "$BUNDLE_DIR/context/telegram_topics/DISTRIBUTED_BLACKCAT_MIGRATION_PLAN_V0_1.md"
cp "$ROOT/scripts/cat_strategic_router.py" "$BUNDLE_DIR/scripts/cat_strategic_router.py"

cat > "$BUNDLE_DIR/README.md" <<'MD'
# Blackcat Remote Migration Bundle

## Purpose
Move strategist/흑묘 to a separate OpenClaw server while preserving cat-strategic (topic 6062) behavior.

## Required on target server
1. OpenClaw installed and gateway healthy
2. Telegram bot token for @Mercedes_cyrano_3_bot configured on target only
3. strategist agent workspace present
4. Binding for telegram topic 6062 -> strategist

## Minimal target config shape
- telegram account: heukmyo (or target default if dedicated server)
- peer binding: group:-1003732040608:topic:6062 -> strategist
- privacy mode already disabled in BotFather
- do not run same token on multiple hosts simultaneously

## Next step after copying files
Use the accompanying handoff document in `context/telegram_topics/DISTRIBUTED_BLACKCAT_MIGRATION_PLAN_V0_1.md`.
MD

TAR_PATH="$OUT_DIR/blackcat_bundle_$STAMP.tar.gz"
tar -czf "$TAR_PATH" -C "$OUT_DIR" "blackcat_bundle_$STAMP"
printf '%s\n' "$TAR_PATH"
