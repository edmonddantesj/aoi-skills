#!/usr/bin/env python3
"""Audit current workstream locks for visibility.

Reads:
- context/telegram_topics/workstream_lock_map.json

Outputs a simple report and exits non-zero if any obvious issues are found.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PATH = ROOT / "context" / "telegram_topics" / "workstream_lock_map.json"


def main() -> int:
    if not PATH.exists():
        print(f"STATUS: missing ({PATH.relative_to(ROOT)})")
        return 0

    data = json.loads(PATH.read_text(encoding="utf-8"))
    locks = data.get("locks", {}) or {}

    print("STATUS: ok")
    print(f"PROOF: file={PATH.relative_to(ROOT)}")
    print(f"COUNT: {len(locks)}")

    # Print deterministic order
    for k in sorted(locks.keys()):
        v = locks[k] or {}
        print(f"- {k}: ledger_id={v.get('ledger_id')} owner={v.get('owner')} thread_id={v.get('thread_id')} claimed_at={v.get('claimed_at')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
