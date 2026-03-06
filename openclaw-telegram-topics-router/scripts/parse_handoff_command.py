#!/usr/bin/env python3
"""Parse a simple handoff command.

Supported:
- #handoff <slug> <P0|P1|P2|P3> <title...>
- #handoff <slug> <title...>   (priority defaults to P1)

Outputs JSON to stdout.
"""

from __future__ import annotations

import argparse
import json
import re


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    args = ap.parse_args()

    t = args.text.strip()

    m = re.match(r"^#handoff\s+(?P<slug>[a-zA-Z0-9_-]+)\s+(?:(?P<prio>P[0-3])\s+)?(?P<title>.+)$", t)
    if not m:
        print(json.dumps({"ok": False, "reason": "no_match"}, ensure_ascii=False))
        return 0

    slug = m.group("slug")
    prio = m.group("prio") or "P1"
    title = m.group("title").strip()

    print(json.dumps({"ok": True, "target_slug": slug, "priority": prio, "title": title}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
