#!/usr/bin/env python3
"""Initialize SSOT for workstream (topic) lock tracking.

Creates (if missing):
- context/telegram_topics/workstream_lock_map.json

Purpose
- Prevent overlapping work across Telegram topics by tracking exclusive locks on shared resources
  (files, pipelines, or subsystems). This is a lightweight coordination SSOT meant to pair with a
  task ledger (e.g., Ralph Loop ledger) but can be used standalone.

Notes
- A lock is exclusive: one lock_key -> one active claim.
- Use claim_workstream_lock.py / release_workstream_lock.py.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Overwrite existing file")
    ap.add_argument("--chat-id", default=None, help="Optional chat_id, e.g. telegram:-100...")
    args = ap.parse_args()

    ctx_dir = ROOT / "context" / "telegram_topics"
    ctx_dir.mkdir(parents=True, exist_ok=True)

    path = ctx_dir / "workstream_lock_map.json"

    if path.exists() and not args.force:
        print("STATUS: skipped (exists)")
        print(f"PROOF: file={path.relative_to(ROOT)}")
        return 0

    payload = {
        "schema": "openclaw.telegram.workstream_lock_map.v0_1",
        "chat_id": args.chat_id,
        "notes": "Exclusive lock registry to prevent duplicated/conflicting work across Telegram topic workstreams.",
        "locks": {}
    }

    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("STATUS: done")
    print(f"PROOF: file={path.relative_to(ROOT)}")
    print("NEXT: claim locks with claim_workstream_lock.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
