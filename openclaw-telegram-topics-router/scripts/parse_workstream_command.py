#!/usr/bin/env python3
"""Parse a chat command that declares a topic as a named workstream.

This does NOT talk to Telegram. It's a deterministic parser you can embed in higher-level automations.

Supported patterns (Korean + shorthand):
- 이 토픽을 "<name>" 작업 스레드로 고정/명명하고 진행
- 이 토픽을 '<name>' 작업 스레드로 고정
- #workstream <name>
- #ws <name>

Outputs JSON to stdout:
  {"ok": true, "name": "..."}
or
  {"ok": false}
"""

from __future__ import annotations

import argparse
import json
import re


def extract(text: str) -> str | None:
    t = text.strip()

    # Shorthand hashtags
    m = re.search(r"(?im)^#(?:workstream|ws)\s+(.+?)\s*$", t)
    if m:
        return m.group(1).strip().strip('"\'')

    # Korean sentence with quotes
    m = re.search(
        r"이\s*토픽을\s*[\"'](.+?)[\"']\s*작업\s*스레드로\s*(?:고정|명명).*",
        t,
    )
    if m:
        return m.group(1).strip()

    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    args = ap.parse_args()

    name = extract(args.text)
    payload = {"ok": bool(name), "name": name}
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
