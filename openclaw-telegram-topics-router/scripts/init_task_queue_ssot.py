#!/usr/bin/env python3
"""Initialize SSOT for a cross-topic task queue.

Creates (if missing):
- context/ops/task_queue.json

This SSOT is meant to coordinate handoffs across Telegram forum topics.
It is intentionally lightweight and works best when each queue entry references a stable ledger/task id.

Safe by default: does not overwrite unless --force.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Overwrite existing file")
    ap.add_argument("--chat-id", default=None, help="Optional chat_id, e.g. telegram:-100...")
    args = ap.parse_args()

    ctx_dir = ROOT / "context" / "ops"
    ctx_dir.mkdir(parents=True, exist_ok=True)

    path = ctx_dir / "task_queue.json"

    if path.exists() and not args.force:
        print("STATUS: skipped (exists)")
        print(f"PROOF: file={path.relative_to(ROOT)}")
        return 0

    payload = {
        "schema": "openclaw.ops.task_queue.v0_1",
        "chat_id": args.chat_id,
        "notes": "Cross-topic task queue SSOT (handoff → prioritize → dispatch).",
        "defaults": {
            "max_concurrency": 3,
            "policy": {"auto_levels": ["L1", "L2"], "require_approval_for": ["L3"]},
        },
        "items": [],
        "generated_at": now_iso(),
    }

    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("STATUS: done")
    print(f"PROOF: file={path.relative_to(ROOT)}")
    print("NEXT: enqueue tasks with enqueue_task.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
