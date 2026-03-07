#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

msg="[$TS] ACP Wallet/Ops reminder: 주소 매핑 SSOT 확인 + (필요 시) LOW=1 / TARGET=3 USDC 정책으로 보충 계획 수립(승인 후). Registry: $ROOT/context/acp/ACP_WALLET_REGISTRY_V0_1.md"

mkdir -p "$ROOT/logs"
echo "$msg" | tee -a "$ROOT/logs/acp_wallet_ops_reminder.log"
