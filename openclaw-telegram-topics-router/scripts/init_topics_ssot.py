#!/usr/bin/env python3
"""Initialize Telegram Topics SSOT files.

Creates (if missing):
- context/telegram_topics/TOPICS_DEFINITION_V0_1.md
- context/telegram_topics/thread_topic_map.json

Safe: does not overwrite existing files unless --force.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # workspace


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = ap.parse_args()

    ctx_dir = ROOT / "context" / "telegram_topics"
    ctx_dir.mkdir(parents=True, exist_ok=True)

    topics_def = ctx_dir / "TOPICS_DEFINITION_V0_1.md"
    map_path = ctx_dir / "thread_topic_map.json"

    template = (ROOT / "repos" / "openclaw-telegram-topics-router" / "openclaw-telegram-topics-router" / "references" / "TOPICS_DEFINITION_TEMPLATE_V0_1.md").read_text(
        encoding="utf-8"
    )

    if not topics_def.exists() or args.force:
        topics_def.write_text(template + "\n", encoding="utf-8")

    if not map_path.exists() or args.force:
        payload = {
            "schema": "openclaw.telegram.thread_topic_map.v0_1",
            "chat_id": None,
            "notes": "Map Telegram forum message_thread_id (topic_id) -> topic slug.",
            "topics": {
                "announcements": None,
                "ops": None,
                "maintenance": None,
                "adp": None,
                "acp": None,
                "bazaar": None,
                "github": None,
                "longform": None,
                "ralph-loop": None,
                "hackathons": None,
                "inbox-dev": None,
                "handoff": None,
                "random": None
            }
        }
        map_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print("STATUS: done")
    print(f"PROOF: file={topics_def.relative_to(ROOT)}")
    print(f"PROOF: file={map_path.relative_to(ROOT)}")
    print("NEXT: set thread IDs with add_mapping.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
