#!/usr/bin/env python3
"""Initialize SSOT for per-topic workstream naming.

Creates (if missing):
- context/telegram_topics/thread_workstream_map.json

This is optional but recommended when you want to "name" a topic thread as a dedicated workstream.
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

    path = ctx_dir / "thread_workstream_map.json"

    if path.exists() and not args.force:
        print("STATUS: skipped (exists)")
        print(f"PROOF: file={path.relative_to(ROOT)}")
        return 0

    payload = {
        "schema": "openclaw.telegram.thread_workstream_map.v0_1",
        "chat_id": args.chat_id,
        "notes": "Map Telegram message_thread_id -> workstream name/label for that topic.",
        "threads": {}
    }

    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("STATUS: done")
    print(f"PROOF: file={path.relative_to(ROOT)}")
    print("NEXT: set names with set_workstream.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
