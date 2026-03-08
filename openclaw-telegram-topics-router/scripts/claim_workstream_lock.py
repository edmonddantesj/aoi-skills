#!/usr/bin/env python3
"""Claim an exclusive workstream lock.

Updates:
- context/telegram_topics/workstream_lock_map.json

Exit codes:
- 0 success
- 2 lock already claimed (and not forced)
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PATH = ROOT / "context" / "telegram_topics" / "workstream_lock_map.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lock", required=True, help="Lock key, e.g. scripts/notion_mirror_sync.py or pipeline:notion-mirror")
    ap.add_argument("--ledger-id", required=True, help="Task id, e.g. RL-20260306-026")
    ap.add_argument("--thread-id", default=None, help="Telegram message_thread_id (topic) where this work runs")
    ap.add_argument("--owner", default=None, help="Human/agent owner label")
    ap.add_argument("--notes", default=None)
    ap.add_argument("--force", action="store_true", help="Steal lock (overwrites existing claim)")
    args = ap.parse_args()

    if not PATH.exists():
        raise SystemExit(f"ERROR: missing SSOT file: {PATH}. Run init_workstream_locks_ssot.py first.")

    data = json.loads(PATH.read_text(encoding="utf-8"))
    locks = data.setdefault("locks", {})

    existing = locks.get(args.lock)
    if existing and not args.force:
        print("STATUS: blocked")
        print("REASON: lock already claimed")
        print(f"LOCK: {args.lock}")
        print(f"CLAIMED_BY: ledger_id={existing.get('ledger_id')} owner={existing.get('owner')} thread_id={existing.get('thread_id')} claimed_at={existing.get('claimed_at')}")
        return 2

    locks[args.lock] = {
        "ledger_id": args.ledger_id,
        "thread_id": args.thread_id,
        "owner": args.owner,
        "notes": args.notes,
        "claimed_at": now_iso(),
        "updated_at": now_iso(),
    }

    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("STATUS: claimed")
    print(f"PROOF: file={PATH.relative_to(ROOT)}")
    print(f"LOCK: {args.lock}")
    print(f"CLAIM: ledger_id={args.ledger_id} owner={args.owner} thread_id={args.thread_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
