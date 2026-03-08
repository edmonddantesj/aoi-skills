#!/usr/bin/env python3
"""Audit thread_topic_map.json for missing thread ids."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MAP_PATH = ROOT / "context" / "telegram_topics" / "thread_topic_map.json"


def main() -> int:
    if not MAP_PATH.exists():
        print("STATUS: blocked")
        print(f"BLOCKED: missing {MAP_PATH.relative_to(ROOT)}; run init_topics_ssot.py")
        return 2

    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    topics = data.get("topics", {})
    missing = [k for k, v in topics.items() if v in (None, "", 0)]

    if missing:
        print("STATUS: blocked")
        print(f"PROOF: file={MAP_PATH.relative_to(ROOT)}")
        print("BLOCKED: missing thread_id for slugs: " + ", ".join(missing))
        return 1

    print("STATUS: done")
    print(f"PROOF: file={MAP_PATH.relative_to(ROOT)}")
    print("NEXT: integrate routing into your agent/cron delivery")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
