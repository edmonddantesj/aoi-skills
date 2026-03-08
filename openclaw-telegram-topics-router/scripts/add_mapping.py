#!/usr/bin/env python3
"""Add/update a mapping: topic_slug -> Telegram thread_id.

Example:
  python3 .../add_mapping.py --slug ops --thread-id 38
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MAP_PATH = ROOT / "context" / "telegram_topics" / "thread_topic_map.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="Topic slug, e.g. ops")
    ap.add_argument("--thread-id", required=True, type=int, help="Telegram message_thread_id")
    args = ap.parse_args()

    if not MAP_PATH.exists():
        raise SystemExit(f"Missing SSOT: {MAP_PATH}. Run init_topics_ssot.py first.")

    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    topics = data.setdefault("topics", {})
    topics[args.slug] = args.thread_id

    MAP_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    print("STATUS: done")
    print(f"PROOF: file={MAP_PATH.relative_to(ROOT)}")
    print(f"NEXT: send a ping in that topic and verify routing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
