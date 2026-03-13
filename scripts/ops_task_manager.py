#!/usr/bin/env python3
"""Ops Task Manager (hygiene)

v0.2 goals:
- scan ops/items/*.md
- summarize actionable hygiene signals, not just status totals
- suppress no-change report churn by comparing against the latest prior summary
- emit WARN/ALERT when something needs attention

Notes:
- read-only detector; does not mutate task files
- "proof" is inferred from an Evidence section or source/link-like lines
- "stale" is inferred from `status: open` + old `updated:` timestamp (default 14 days)
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

STATUS_RE = re.compile(r"^\s*status\s*:\s*([a-zA-Z0-9_-]+)\s*$", re.IGNORECASE)
UPDATED_RE = re.compile(r"^\s*updated\s*:\s*(.+?)\s*$", re.IGNORECASE)
ASSIGNEE_RE = re.compile(r"^\s*assignee\s*:\s*(.+?)\s*$", re.IGNORECASE)
DUE_RE = re.compile(r"^\s*due\s*:\s*(.+?)\s*$", re.IGNORECASE)
REPORT_RE = re.compile(r"^REPORT_\d{4}-\d{2}-\d{2}_\d{4}\.md$")
SUMMARY_START = "<!-- SUMMARY_JSON_START -->"
SUMMARY_END = "<!-- SUMMARY_JSON_END -->"


@dataclass
class TaskRecord:
    path: str
    status: str
    updated: datetime | None
    assignee: str | None
    due: datetime | None
    has_evidence: bool


@dataclass
class Summary:
    total: int
    counts: dict[str, int]
    warnings: dict[str, int]
    severity: str

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "counts": dict(sorted(self.counts.items())),
            "warnings": dict(sorted(self.warnings.items())),
            "severity": self.severity,
        }


def parse_dt(value: str) -> datetime | None:
    value = value.strip()
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def has_evidence(lines: Iterable[str]) -> bool:
    in_evidence = False
    evidence_lines = 0
    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("## "):
            in_evidence = stripped.lower() == "## evidence"
            continue
        if in_evidence and stripped:
            evidence_lines += 1
            if evidence_lines >= 1:
                return True
        if not in_evidence:
            lower = stripped.lower()
            if "http://" in lower or "https://" in lower or lower.startswith("source:"):
                return True
    return False


def parse_task(path: str) -> TaskRecord:
    status = "missing"
    updated = None
    assignee = None
    due = None
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if status == "missing":
            m = STATUS_RE.match(line)
            if m:
                status = m.group(1).lower()
                continue
        if updated is None:
            m = UPDATED_RE.match(line)
            if m:
                updated = parse_dt(m.group(1))
                continue
        if assignee is None:
            m = ASSIGNEE_RE.match(line)
            if m:
                value = m.group(1).strip()
                assignee = value if value else None
                continue
        if due is None:
            m = DUE_RE.match(line)
            if m:
                due = parse_dt(m.group(1))
                continue

    return TaskRecord(
        path=path,
        status=status,
        updated=updated,
        assignee=assignee,
        due=due,
        has_evidence=has_evidence(lines),
    )


def compute_summary(records: list[TaskRecord], stale_days: int, now: datetime) -> tuple[Summary, dict[str, list[str]]]:
    counts = Counter()
    warnings = Counter()
    details: dict[str, list[str]] = {
        "overdue": [],
        "stale": [],
        "missing_assignee": [],
        "missing_evidence": [],
        "missing_status": [],
    }

    stale_cutoff = now - timedelta(days=stale_days)

    for rec in records:
        counts[rec.status] += 1
        if rec.status == "missing":
            warnings["missing_status"] += 1
            details["missing_status"].append(os.path.basename(rec.path))
        if not rec.assignee:
            warnings["missing_assignee"] += 1
            details["missing_assignee"].append(os.path.basename(rec.path))
        if not rec.has_evidence:
            warnings["missing_evidence"] += 1
            details["missing_evidence"].append(os.path.basename(rec.path))
        if rec.due and rec.due < now and rec.status not in {"done", "closed", "cancelled"}:
            warnings["overdue"] += 1
            details["overdue"].append(os.path.basename(rec.path))
        if rec.status == "open" and (rec.updated is None or rec.updated < stale_cutoff):
            warnings["stale_candidate"] += 1
            details["stale"].append(os.path.basename(rec.path))

    severity = "INFO"
    if warnings["missing_status"] > 0 or warnings["overdue"] > 0:
        severity = "ALERT"
    elif warnings["missing_assignee"] > 0 or warnings["missing_evidence"] > 0 or warnings["stale_candidate"] > 0:
        severity = "WARN"

    return Summary(total=len(records), counts=dict(counts), warnings=dict(warnings), severity=severity), details


def find_previous_summary(outdir: str) -> dict | None:
    report_dir = Path(outdir)
    candidates = sorted(
        p for p in report_dir.glob("REPORT_*.md") if REPORT_RE.match(p.name)
    )
    for path in reversed(candidates):
        text = path.read_text(encoding="utf-8")
        start = text.find(SUMMARY_START)
        end = text.find(SUMMARY_END)
        if start == -1 or end == -1 or end < start:
            continue
        payload = text[start + len(SUMMARY_START):end].strip()
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            continue
    return None


def render_report(summary: Summary, details: dict[str, list[str]], stamp: str, changed: bool, stale_days: int) -> str:
    lines = [
        f"# Ops Task Manager Report — {stamp} (UTC)",
        "",
        f"- total: {summary.total}",
        f"- changed since last run: {'yes' if changed else 'no'}",
        f"- severity: {summary.severity}",
        "",
        "## Actionable warnings",
        f"- missing status: {summary.warnings.get('missing_status', 0)}",
        f"- missing assignee: {summary.warnings.get('missing_assignee', 0)}",
        f"- missing evidence: {summary.warnings.get('missing_evidence', 0)}",
        f"- overdue: {summary.warnings.get('overdue', 0)}",
        f"- stale candidates (>{stale_days}d): {summary.warnings.get('stale_candidate', 0)}",
        "",
        "## Counts by status",
    ]
    for k in sorted(summary.counts.keys()):
        lines.append(f"- {k}: {summary.counts[k]}")

    detail_order = [
        ("overdue", "Overdue tasks"),
        ("stale", "Stale candidate tasks"),
        ("missing_assignee", "Missing assignee"),
        ("missing_evidence", "Missing evidence"),
        ("missing_status", "Missing status"),
    ]
    for key, title in detail_order:
        if details[key]:
            lines += ["", f"## {title}"]
            for name in details[key][:20]:
                lines.append(f"- {name}")
            if len(details[key]) > 20:
                lines.append(f"- ... and {len(details[key]) - 20} more")

    lines += [
        "",
        SUMMARY_START,
        json.dumps(summary.to_dict(), ensure_ascii=False, sort_keys=True, indent=2),
        SUMMARY_END,
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", default="ops/items/*.md")
    ap.add_argument("--outdir", default="ops/reports/task_manager")
    ap.add_argument("--stale-days", type=int, default=14)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    files = sorted(glob.glob(args.items))
    now = datetime.now(timezone.utc)
    records = [parse_task(p) for p in files]
    summary, details = compute_summary(records, stale_days=args.stale_days, now=now)
    previous = find_previous_summary(args.outdir)
    current = summary.to_dict()
    changed = previous != current

    should_write = changed or summary.severity in {"WARN", "ALERT"}
    if not should_write:
        print("NO_CHANGE")
        return 0

    stamp = now.strftime("%Y-%m-%d_%H%M")
    report_path = os.path.join(args.outdir, f"REPORT_{stamp}.md")
    content = render_report(summary, details, stamp=stamp, changed=changed, stale_days=args.stale_days)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(report_path)
    print(f"SEVERITY={summary.severity}")
    print(f"CHANGED={'yes' if changed else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
