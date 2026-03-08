#!/usr/bin/env python3
"""Parse attendance commands for multi-agent participation.

Supported:
- #call <Role1> <Role2> ...
- #council all (alias of #all-hands)
- #all-hands (12요원 전원 의견 요청일 때만)
- #council core
- #council market

Outputs JSON:
  {"kind":"call","roles":[...]}  OR  {"kind":"council","group":"all|core|market"} OR {"kind":"none"}
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

    if re.search(r"(?im)^#all-hands\b", t) or re.search(r"(?im)^#council\s+all\b", t):
        print(json.dumps({"kind": "council", "group": "all"}, ensure_ascii=False))
        return 0

    m = re.search(r"(?im)^#council\s+(core|market)\b", t)
    if m:
        print(json.dumps({"kind": "council", "group": m.group(1)}, ensure_ascii=False))
        return 0

    m = re.search(r"(?im)^#call\s+(.+)$", t)
    if m:
        roles = [r for r in re.split(r"\s+", m.group(1).strip()) if r]
        print(json.dumps({"kind": "call", "roles": roles}, ensure_ascii=False))
        return 0

    print(json.dumps({"kind": "none"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
