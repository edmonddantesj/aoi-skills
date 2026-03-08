#!/usr/bin/env python3
"""Set a per-topic workstream label for a Telegram thread.

Examples:
  python3 .../set_workstream.py --thread-id 68 --name "Ralph Loop / WIP Sweep"
  python3 .../set_workstream.py --thread-id 45 --name "ADP UI: Pixel Office"

SSOT:
  context/telegram_topics/thread_workstream_map.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PATH = ROOT / "context" / "telegram_topics" / "thread_workstream_map.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--thread-id", required=True, type=int, help="Telegram message_thread_id")
    ap.add_argument("--name", required=True, help="Workstream name/label")
    ap.add_argument("--slug", default=None, help="Optional topic slug hint")
    args = ap.parse_args()

    if not PATH.exists():
        raise SystemExit(f"Missing SSOT: {PATH}. Run init_workstream_ssot.py first.")

    data = json.loads(PATH.read_text(encoding="utf-8"))
    threads = data.setdefault("threads", {})

    entry = threads.get(str(args.thread_id), {})
    entry["name"] = args.name
    if args.slug:
        entry["slug"] = args.slug
    threads[str(args.thread_id)] = entry

    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("STATUS: done")
    print(f"PROOF: file={PATH.relative_to(ROOT)}")
    print(f"PROOF: thread_id={args.thread_id} name={args.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
