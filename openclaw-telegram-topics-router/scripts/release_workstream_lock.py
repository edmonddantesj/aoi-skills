#!/usr/bin/env python3
"""Release an exclusive workstream lock.

Updates:
- context/telegram_topics/workstream_lock_map.json

Exit codes:
- 0 success
- 2 lock not claimed / cannot release (guard)
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
    ap.add_argument("--lock", required=True)
    ap.add_argument("--ledger-id", default=None, help="If provided, only release when current claim matches")
    ap.add_argument("--force", action="store_true", help="Release even if ledger-id mismatch")
    args = ap.parse_args()

    if not PATH.exists():
        raise SystemExit(f"ERROR: missing SSOT file: {PATH}. Run init_workstream_locks_ssot.py first.")

    data = json.loads(PATH.read_text(encoding="utf-8"))
    locks = data.setdefault("locks", {})

    existing = locks.get(args.lock)
    if not existing:
        print("STATUS: blocked")
        print("REASON: lock not claimed")
        print(f"LOCK: {args.lock}")
        return 2

    if args.ledger_id and (existing.get("ledger_id") != args.ledger_id) and not args.force:
        print("STATUS: blocked")
        print("REASON: ledger-id mismatch")
        print(f"LOCK: {args.lock}")
        print(f"CLAIMED_BY: ledger_id={existing.get('ledger_id')} owner={existing.get('owner')} thread_id={existing.get('thread_id')} claimed_at={existing.get('claimed_at')}")
        return 2

    del locks[args.lock]
    data["updated_at"] = now_iso()

    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("STATUS: released")
    print(f"PROOF: file={PATH.relative_to(ROOT)}")
    print(f"LOCK: {args.lock}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
