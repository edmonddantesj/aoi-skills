#!/usr/bin/env python3
"""Ralph Loop WIP sweep

Scans ops/items/*.md and counts tasks by status.
Outputs one-line summary compatible with historical logs:
  WIP_SWEEP wip=<n>/<limit> stale=<n> sla_h=<sla>

Heuristics:
- status is extracted from a line like: `status: in-progress`
- updated timestamp is extracted from `updated:` (ISO8601 or `YYYY-MM-DD HH:MM`)
- if missing timestamps, stale detection is skipped for that file

This script is intentionally dependency-free.
"""

from __future__ import annotations

import argparse
import glob
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS_RE = re.compile(r"^\s*status\s*:\s*([a-zA-Z0-9_-]+)\s*$", re.IGNORECASE)
UPDATED_RE = re.compile(r"^\s*(updated|last_update|last-updated)\s*:\s*(.+?)\s*$", re.IGNORECASE)


def parse_dt(s: str) -> datetime | None:
    s = s.strip()
    fmts = [
        "%Y-%m-%d %H:%M %Z",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ]
    for fmt in fmts:
        try:
            dt = datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


@dataclass
class SweepResult:
    wip: int
    stale: int
    limit: int
    sla_h: int


def sweep(items_glob: str, limit: int, sla_h: int, now: datetime) -> SweepResult:
    wip = 0
    stale = 0

    for path in glob.glob(items_glob):
        if not os.path.isfile(path):
            continue
        status = None
        updated = None
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if status is None:
                        m = STATUS_RE.match(line)
                        if m:
                            status = m.group(1).lower()
                            continue
                    if updated is None:
                        m = UPDATED_RE.match(line)
                        if m:
                            updated = parse_dt(m.group(2))
                            continue
        except Exception:
            continue

        if status == "in-progress":
            wip += 1
            if updated is not None:
                age = now - updated.astimezone(now.tzinfo)
                if age > timedelta(hours=sla_h):
                    stale += 1

    return SweepResult(wip=wip, stale=stale, limit=limit, sla_h=sla_h)


def normalize_items_glob(pattern: str) -> str:
    if os.path.isabs(pattern):
        return pattern
    return os.path.join(ROOT, pattern)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--items",
        default=None,
        help="Glob for task files. Defaults to both context/ops/items and ops/items for backward compatibility.",
    )
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--sla-h", type=int, default=24)
    args = ap.parse_args()

    now = datetime.now(timezone.utc)

    if args.items:
        globs = [normalize_items_glob(args.items)]
    else:
        globs = [
            os.path.join(ROOT, "context/ops/items/*.md"),
            os.path.join(ROOT, "ops/items/*.md"),
        ]

    wip = 0
    stale = 0
    for g in globs:
        r = sweep(g, args.limit, args.sla_h, now)
        wip += r.wip
        stale += r.stale

    print(f"WIP_SWEEP wip={wip}/{args.limit} stale={stale} sla_h={args.sla_h}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
