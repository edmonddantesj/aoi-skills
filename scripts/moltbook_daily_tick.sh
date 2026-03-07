#!/usr/bin/env bash
set -euo pipefail

# Moltbook daily loop tick:
# 1) Run scan → generate daily draft package markdown
# 2) Post a short note into moltbook topic(thread_id=1114)
#
# Posting is just a reminder + path; it does NOT publish to Moltbook.

OPENCLAW_BIN="${OPENCLAW_BIN:-/opt/homebrew/bin/openclaw}"
CHAT_ID="${CHAT_ID:--1003732040608}"
THREAD_ID="${THREAD_ID:-1114}"

OUT_PATH="$((python3 /Users/silkroadcat/.openclaw/workspace/scripts/moltbook_daily_scan.py) | tail -n 1)"

TODAY_KST="$(python3 - <<'PY'
import datetime as dt
print(dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime('%Y-%m-%d'))
PY
)"

MSG=$'📝 [MOLTBOOK DAILY DRAFT] '\"$TODAY_KST\"$'\n\n초안 패키지 생성 완료.\n- 파일: '\"$OUT_PATH\"$'\n\n다음: (의장) 오늘 EN 1포스트 주제/방향 선택 → YES면 업로드 진행(L3).\n(규칙/체크리스트: context/topics/moltbook_PLAYBOOK_V0_1.md)'

DRY_RUN_FLAG=""
if [[ "${DRY_RUN:-}" == "1" ]]; then
  DRY_RUN_FLAG="--dry-run"
fi

"$OPENCLAW_BIN" message send \
  --channel telegram \
  --target "$CHAT_ID" \
  --thread-id "$THREAD_ID" \
  --silent \
  $DRY_RUN_FLAG \
  --message "$MSG" \
  --json
