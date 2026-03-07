#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

msg="[$TS] ACP Weekly Dispatch reminder: 후보 shortlist 올리고 Bought&Analyzed 제출 수집 시작. SSOT: $ROOT/context/topics/acp_PLAYBOOK_V0_2.md / HF: $ROOT/context/handoff/HF_acp_ops_202603.md"

mkdir -p "$ROOT/logs"
echo "$msg" | tee -a "$ROOT/logs/acp_weekly_dispatch_reminder.log"
