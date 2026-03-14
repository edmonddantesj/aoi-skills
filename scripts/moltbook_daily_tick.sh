#!/usr/bin/env bash
set -euo pipefail

# Moltbook daily loop tick:
# 1) Run scan → generate detailed daily draft package markdown
# 2) Post a short note into moltbook topic(thread_id=1114)
#
# Posting is only the internal report to Telegram; it does NOT publish to Moltbook.

OPENCLAW_BIN="${OPENCLAW_BIN:-/opt/homebrew/bin/openclaw}"
OPENCLAW_NODE="${OPENCLAW_NODE:-/opt/homebrew/bin/node}"
CHAT_ID="${CHAT_ID:--1003732040608}"
THREAD_ID="${THREAD_ID:-1114}"

OUT_PATH="$((python3 /Users/silkroadcat/.openclaw/workspace/scripts/moltbook_daily_scan.py) | tail -n 1)"

TODAY_KST="$(python3 - <<'PY'
import datetime as dt
print(dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime('%Y-%m-%d'))
PY
)"

MSG=$'📝 [MOLTBOOK DAILY DRAFT] '"$TODAY_KST"$'\n\n상세 초안 패키지 생성 완료.\n- 파일: '"$OUT_PATH"$'\n\n포함 사항:\n- 최신 Moltbook 스캔 반영\n- local HF/운영 지시사항 반영\n- 제목/요약/본문/CTA까지 near-post-ready draft\n\n다음: (의장) 초안 검토 → 수정지시 or YES면 업로드 진행(L3).\n(규칙/체크리스트: context/topics/moltbook_PLAYBOOK_V0_1.md)'

DRY_RUN_FLAG=""
if [[ "${DRY_RUN:-}" == "1" ]]; then
  DRY_RUN_FLAG="--dry-run"
fi

"$OPENCLAW_NODE" "$OPENCLAW_BIN" message send \
  --channel telegram \
  --target "$CHAT_ID" \
  --thread-id "$THREAD_ID" \
  --silent \
  $DRY_RUN_FLAG \
  --message "$MSG" \
  --json
