#!/usr/bin/env python3
"""Audit workstream naming coverage.

Checks:
- thread_topic_map.json: list all known threads
- thread_workstream_map.json: which threads have a friendly workstream name

Outputs missing thread ids.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TOPIC_MAP = ROOT / "context" / "telegram_topics" / "thread_topic_map.json"
WS_MAP = ROOT / "context" / "telegram_topics" / "thread_workstream_map.json"


def main() -> int:
    if not TOPIC_MAP.exists():
        raise SystemExit(f"Missing: {TOPIC_MAP}")

    topic_data = json.loads(TOPIC_MAP.read_text(encoding="utf-8"))
    topics = topic_data.get("topics") or topic_data.get("map") or {}

    ws_threads = {}
    if WS_MAP.exists():
        ws_data = json.loads(WS_MAP.read_text(encoding="utf-8"))
        ws_threads = ws_data.get("threads", {})

    missing = []
    for slug, tid in topics.items():
        if tid is None:
            continue
        if str(tid) not in ws_threads or not ws_threads[str(tid)].get("name"):
            missing.append({"slug": slug, "thread_id": tid})

    print("STATUS: ok" if not missing else "STATUS: missing")
    print(json.dumps({"missing": missing}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
