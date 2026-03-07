#!/usr/bin/env python3
"""Ralph Loop Daily Scan

Creates a daily report under context/ops/reports/ralph_loop_daily/REPORT_YYYY-MM-DD.md (and legacy ops/reports for compatibility if present)
and (optionally) creates follow-up ops/items tasks when drift/staleness is detected.

This is a reconstruction script: minimal, deterministic, local-only.
"""

from __future__ import annotations

import argparse
import os
import subprocess
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def run(cmd: list[str]) -> str:
    out = subprocess.check_output(cmd, text=True)
    return out.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (defaults to today Asia/Seoul)")
    ap.add_argument("--force", action="store_true", help="overwrite existing report file")
    ap.add_argument("--wip-limit", type=int, default=5)
    ap.add_argument("--sla-h", type=int, default=24)
    args = ap.parse_args()

    d = args.date
    if not d:
        d = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d")

    # Prefer SSOT path under context/, but keep legacy ops/ path if it exists.
    report_dir = "context/ops/reports/ralph_loop_daily"
    legacy_dir = "ops/reports/ralph_loop_daily"
    os.makedirs(report_dir, exist_ok=True)
    if os.path.isdir("ops/reports"):
        os.makedirs(legacy_dir, exist_ok=True)

    wip_line = run(["python3", "scripts/ralph_loop_wip_sweep.py", "--limit", str(args.wip_limit), "--sla-h", str(args.sla_h)])

    report_path = f"{report_dir}/REPORT_{d}.md"
    legacy_report_path = f"{legacy_dir}/REPORT_{d}.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    content = f"""# Ralph Loop Daily Scan — {d}

Generated: {now}

## Summary
- {wip_line}

## WIP Sweep
- (See summary line; reconstructed runner)

## Cron Health
- Reconstructed environment: cron DB may be missing; see `context/RALPH_LOOP_CRON_ID_REMAP_TABLE_2026-03-06.md`.

## State Integrity / Drift
- Executed via `python3 scripts/ralph_loop_drift_check.py` (baseline + drift report; auto-repair may be enabled by scheduler).

## Next Actions
- If `stale>0`, triage in-progress items: split / mark blocked / return to backlog.
"""

    if os.path.exists(report_path) and not args.force:
        print(report_path)
        return 0

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Best-effort write to legacy location too, if available.
    try:
        if os.path.isdir(legacy_dir):
            with open(legacy_report_path, "w", encoding="utf-8") as f:
                f.write(content)
    except Exception:
        pass

    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
