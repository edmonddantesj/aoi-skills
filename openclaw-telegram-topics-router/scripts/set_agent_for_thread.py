#!/usr/bin/env python3
"""Set primary agent (and optional collaborators) for a Telegram thread.

Example:
  python3 .../set_agent_for_thread.py --thread-id 38 --primary Blue-Gear --collab Blue-Blade --collab Oracle

SSOT:
  context/telegram_topics/thread_agent_map.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PATH = ROOT / "context" / "telegram_topics" / "thread_agent_map.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--thread-id", required=True, type=int)
    ap.add_argument("--primary", required=True)
    ap.add_argument("--collab", action="append", default=[], help="Repeatable collaborator role")
    ap.add_argument("--notes", default=None)
    args = ap.parse_args()

    if not PATH.exists():
        raise SystemExit(f"Missing SSOT: {PATH}. Run init_agent_map_ssot.py first.")

    data = json.loads(PATH.read_text(encoding="utf-8"))
    threads = data.setdefault("threads", {})

    entry = threads.get(str(args.thread_id), {})
    entry["primary"] = args.primary
    entry["collaborators"] = sorted(set(args.collab))
    if args.notes:
        entry["notes"] = args.notes

    threads[str(args.thread_id)] = entry
    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("STATUS: done")
    print(f"PROOF: file={PATH.relative_to(ROOT)}")
    print(f"PROOF: thread_id={args.thread_id} primary={args.primary} collab={entry['collaborators']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
