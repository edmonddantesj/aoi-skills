#!/usr/bin/env python3
"""
support-flow watcher v0.2
Scans canonical request paths for OPEN requests and reports them.

Usage:
  python3 watcher.py --lane inbox-dev
  python3 watcher.py --all
  python3 watcher.py --root /path/to/context --all

Exit codes:
  0 = no open requests found
  1 = open requests found (useful for cron alerting)
"""

import argparse
import sys
from pathlib import Path
import re


# Default context root (relative to repo root, or override with --root)
DEFAULT_CONTEXT_ROOT = "context"

# Known lanes (add more as needed)
KNOWN_LANES = [
    "inbox-dev",
    "github",
    "longform",
    "v6-invest",
    "moltbook",
    "ops",
    "hackathons",
    "acp",
    "bazaar",
    "adp",
    "ralph-loop",
    "x-post",
    "random",
    "maintenance",
    "handoff",
]

# Subdirs to scan for requests (v0.2 structure + legacy flat)
REQUEST_SUBDIRS = ["support/requests", "requests"]


def extract_frontmatter(content: str) -> dict:
    """Extract YAML-style frontmatter from markdown."""
    result = {}
    lines = content.splitlines()
    in_fm = False
    for line in lines:
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                break
        if in_fm:
            m = re.match(r'^(\w+):\s*(.+)$', line)
            if m:
                result[m.group(1)] = m.group(2).strip()
    return result


def scan_lane(context_root: Path, lane: str) -> list[dict]:
    """Scan a single lane for OPEN requests."""
    found = []
    for subdir in REQUEST_SUBDIRS:
        req_dir = context_root / lane / subdir
        if not req_dir.exists():
            continue
        for f in sorted(req_dir.glob("TASK-*.md")):
            content = f.read_text(encoding="utf-8")
            fm = extract_frontmatter(content)
            state = fm.get("state", "").strip()
            if state in ("OPEN", "WORKING"):
                found.append({
                    "lane": lane,
                    "file": str(f),
                    "request_id": fm.get("request_id", f.stem),
                    "state": state,
                    "priority": fm.get("priority", "?"),
                    "requester": fm.get("requester", "?"),
                    "date": fm.get("date", "?"),
                })
    return found


def main():
    parser = argparse.ArgumentParser(description="support-flow watcher")
    parser.add_argument("--lane", help="Scan a specific lane")
    parser.add_argument("--all", action="store_true", help="Scan all known lanes")
    parser.add_argument("--root", default=None, help="Context root path (default: auto-detect)")
    parser.add_argument("--quiet", action="store_true", help="Only print if OPEN requests exist")
    args = parser.parse_args()

    # Resolve context root
    if args.root:
        context_root = Path(args.root)
    else:
        # Try to find context/ relative to script location or cwd
        candidates = [
            Path(__file__).parent.parent.parent.parent / "context",  # repo root
            Path.cwd() / "context",
            Path.cwd(),
        ]
        context_root = next((c for c in candidates if c.exists()), Path("context"))

    if not args.lane and not args.all:
        parser.print_help()
        sys.exit(0)

    lanes = KNOWN_LANES if args.all else [args.lane]

    all_open = []
    for lane in lanes:
        all_open.extend(scan_lane(context_root, lane))

    if not all_open:
        if not args.quiet:
            print("✅ No OPEN requests found.")
        sys.exit(0)

    # Print results
    print(f"\n⚠️  {len(all_open)} OPEN request(s) found:\n")
    for r in all_open:
        priority_icon = {"P0": "🔴", "P1": "🟡", "P2": "🟢"}.get(r["priority"], "⚪")
        state_label = "🔄 WORKING" if r["state"] == "WORKING" else "📥 OPEN"
        print(f"  {priority_icon} [{r['priority']}] {state_label}  {r['request_id']}")
        print(f"     Lane: {r['lane']} | From: {r['requester']} | Date: {r['date']}")
        print(f"     File: {r['file']}")
        print()

    sys.exit(1)


if __name__ == "__main__":
    main()
