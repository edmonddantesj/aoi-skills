#!/usr/bin/env bash
# handoff_compact_daily.sh
# 매일 09:30 KST — ACTIVE HF 다이제스트 생성 후 handoff(586) 토픽에 전송
# Owner: 청비/record
# Last updated: 2026-03-17

set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$WORKSPACE/logs/launchd"
LOG="$LOG_DIR/handoff-compact-daily.log"
mkdir -p "$LOG_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] handoff_compact_daily.sh start" >> "$LOG"

# 1. HF digest 생성
cd "$WORKSPACE"
python3 scripts/hf_digest.py >> "$LOG" 2>&1

DIGEST="$WORKSPACE/context/ops/digests/HF_ACTIVE_DIGEST_LATEST.md"

if [ ! -f "$DIGEST" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] ERROR: digest not found at $DIGEST" >> "$LOG"
  exit 1
fi

# 2. 다이제스트를 handoff(586) 토픽에 전송
# openclaw send: channel=telegram, topic_id=586
ACTIVE_COUNT=$(grep -c "^### HF_" "$DIGEST" || true)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M KST')

MESSAGE="📋 *Daily HF Compact* — ${TIMESTAMP}

ACTIVE HF: ${ACTIVE_COUNT}개

$(grep "^### HF_\|^- Goal:\|^  - " "$DIGEST" | head -40 | sed 's/^### /🔹 /; s/^- Goal:/   Goal:/; s/^  - /      /')"

openclaw message send \
  --channel telegram \
  --target "-1003732040608" \
  --thread-id 586 \
  --message "$MESSAGE" >> "$LOG" 2>&1 || {
  echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] WARN: openclaw send failed (non-fatal)" >> "$LOG"
}

echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] handoff_compact_daily.sh done" >> "$LOG"
