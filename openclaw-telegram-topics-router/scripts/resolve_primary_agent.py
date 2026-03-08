#!/usr/bin/env python3
"""Resolve primary agent for a Telegram thread_id using SSOT.

Reads:
- context/telegram_topics/thread_agent_map.json

Example:
  python3 .../resolve_primary_agent.py --thread-id 38

Output:
  {"ok":true,"thread_id":38,"primary":"Blue-Gear","collaborators":[...]}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MAP_PATH = ROOT / "context" / "telegram_topics" / "thread_agent_map.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--thread-id", required=True, type=int)
    args = ap.parse_args()

    if not MAP_PATH.exists():
        raise SystemExit(f"Missing SSOT: {MAP_PATH}")

    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    threads = data.get("threads", {})
    entry = threads.get(str(args.thread_id))

    if not entry:
        print(json.dumps({"ok": False, "error": "NOT_FOUND", "thread_id": args.thread_id}, ensure_ascii=False))
        return 0

    out = {
        "ok": True,
        "thread_id": args.thread_id,
        "primary": entry.get("primary"),
        "collaborators": entry.get("collaborators", []),
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
