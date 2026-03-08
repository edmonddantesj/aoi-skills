#!/usr/bin/env python3
"""Generate a 23:00 KST integrated maintenance report for the ralph-loop.

Output: prints markdown to stdout.
Designed to be used in OpenClaw cron with --announce to maintenance topic.

Sources:
- Daily scan report: context/ops/reports/ralph_loop_daily/REPORT_YYYY-MM-DD.md
- Tasks: context/ops/items/TASK-*.md

This intentionally stays lightweight and deterministic.
"""

from __future__ import annotations

import glob
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Task:
    id: str
    priority: str | None
    status: str | None
    assignee: str | None
    updated: str | None
    path: Path


def parse_task(p: Path) -> Task:
    lines = p.read_text(encoding="utf-8").splitlines()
    tid = (lines[0].lstrip("# ").strip() if lines else p.stem)

    priority = status = assignee = updated = None
    for line in lines[:40]:
        k = line.split(":", 1)[0].strip().lower()
        if k == "priority":
            priority = line.split(":", 1)[1].strip()
        elif k == "status":
            status = line.split(":", 1)[1].strip()
        elif k == "assignee":
            assignee = line.split(":", 1)[1].strip()
        elif k == "updated":
            updated = line.split(":", 1)[1].strip()

    return Task(id=tid, priority=priority, status=status, assignee=assignee, updated=updated, path=p)


def prio_key(p: str | None) -> int:
    return {"P0": 0, "P1": 1, "P2": 2, "P3": 3}.get((p or "").upper(), 9)


def status_key(s: str | None) -> int:
    s = (s or "").lower()
    return {"in-progress": 0, "blocked": 1, "review": 2, "todo": 3, "done": 9}.get(s, 8)


def latest_daily_report() -> Path | None:
    paths = sorted(glob.glob(str(ROOT / "context/ops/reports/ralph_loop_daily/REPORT_*.md")))
    return Path(paths[-1]) if paths else None


def main() -> int:
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    day = now.strftime("%Y-%m-%d")

    report = latest_daily_report()
    report_line = "(none)"
    if report and report.exists():
        report_line = str(report.relative_to(ROOT))

    tasks = [parse_task(Path(p)) for p in sorted(glob.glob(str(ROOT / "context/ops/items/TASK-*.md")))]

    wip = [t for t in tasks if (t.status or "").lower() == "in-progress"]
    todo = [t for t in tasks if (t.status or "").lower() == "todo"]
    blocked = [t for t in tasks if (t.status or "").lower() == "blocked"]
    done = [t for t in tasks if (t.status or "").lower() == "done"]

    wip_sorted = sorted(wip, key=lambda t: (prio_key(t.priority), status_key(t.status), t.id))

    lines = []
    lines.append(f"# [ralph-loop] 23:00 통합 업무보고 — {day}")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Daily scan report: `{report_line}`")
    lines.append(f"- WIP: {len(wip)}/5 | blocked: {len(blocked)} | todo: {len(todo)} | done: {len(done)}")
    lines.append("")

    lines.append("## WIP (assignee 기준)")
    if not wip_sorted:
        lines.append("- (none)")
    else:
        for t in wip_sorted:
            lines.append(
                f"- [{t.priority}] {t.id} — assignee: {t.assignee or 'TBD'} | updated: {t.updated or 'TBD'} | status: {t.status}"
            )

    lines.append("")
    lines.append("## Done today")
    lines.append("- (자동 집계는 아직 미구현: status=done + updated가 오늘인 항목으로 확장 예정)")

    lines.append("")
    lines.append("## Next (내일 아침 우선순위)")
    lines.append("- WIP 5개 중 1개를 done으로 보내는 게 1순위 (WIP ceiling 해제)")
    lines.append("- WIP 항목이 24h 넘으면 stale로 분해/blocked 전환")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
