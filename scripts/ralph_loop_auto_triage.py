#!/usr/bin/env python3
"""ralph-loop 자동 병목 분석/해결안 제안 + (선택) 자동 조치.

목표
- WIP(in-progress) 항목이 SLA(기본 24h)를 넘어서 "빨리 넘어가지" 않으면
  자동으로 원인분석 프롬프트/해결방안을 태스크에 누적하고,
  필요한 최소 조치(예: blocked 전환, Next Actions 보강)를 수행한다.

안전 가드
- 기본은 report-only (--apply 없으면 파일 수정 없음)
- 같은 태스크에 대해 반복적으로 덮어쓰지 않도록 cooldown 마커 사용

입력
- context/ops/items/TASK-*.md

출력
- stdout markdown (cron announce용)
"""

from __future__ import annotations

import argparse
import glob
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ITEMS_GLOB = str(ROOT / "context/ops/items/TASK-*.md")

STATUS_RE = re.compile(r"^\s*status\s*:\s*(.+?)\s*$", re.I)
PRIO_RE = re.compile(r"^\s*priority\s*:\s*(.+?)\s*$", re.I)
ASSIGNEE_RE = re.compile(r"^\s*assignee\s*:\s*(.+?)\s*$", re.I)
UPDATED_RE = re.compile(r"^\s*updated\s*:\s*(.+?)\s*$", re.I)

AUTO_MARK = "AUTO_TRIAGE_V0_1"
AUTO_LAST_RE = re.compile(r"^\s*auto_triage_last\s*:\s*(.+?)\s*$", re.I)


def parse_dt(s: str) -> datetime | None:
    s = s.strip()
    fmts = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M%z",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d",
    ]
    for fmt in fmts:
        try:
            dt = datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=ZoneInfo("Asia/Seoul"))
            return dt
        except ValueError:
            continue
    return None


@dataclass
class Task:
    path: Path
    title: str
    priority: str | None
    status: str | None
    assignee: str | None
    updated: datetime | None
    auto_last: datetime | None


def load_task(p: Path) -> Task:
    lines = p.read_text(encoding="utf-8").splitlines()
    title = (lines[0].lstrip("# ").strip() if lines else p.stem)

    priority = status = assignee = None
    updated = None
    auto_last = None

    for line in lines[:60]:
        m = PRIO_RE.match(line)
        if m:
            priority = m.group(1).strip()
        m = STATUS_RE.match(line)
        if m:
            status = m.group(1).strip()
        m = ASSIGNEE_RE.match(line)
        if m:
            assignee = m.group(1).strip()
        m = UPDATED_RE.match(line)
        if m:
            updated = parse_dt(m.group(1))
        m = AUTO_LAST_RE.match(line)
        if m:
            auto_last = parse_dt(m.group(1))

    return Task(path=p, title=title, priority=priority, status=status, assignee=assignee, updated=updated, auto_last=auto_last)


def update_frontmatter(text: str, key: str, value: str) -> str:
    # Replace first matching "key:" line, else insert after title line.
    lines = text.splitlines()
    key_re = re.compile(rf"^\s*{re.escape(key)}\s*:\s*.*$", re.I)
    for i, line in enumerate(lines[:80]):
        if key_re.match(line):
            lines[i] = f"{key}: {value}"
            return "\n".join(lines) + ("\n" if not text.endswith("\n") else "")
    # insert after metadata block if present; simplest: after title line and blank
    insert_at = 1
    while insert_at < len(lines) and lines[insert_at].strip() == "":
        insert_at += 1
    lines.insert(insert_at, f"{key}: {value}")
    return "\n".join(lines) + ("\n" if not text.endswith("\n") else "")


def append_auto_block(text: str, now_iso: str, sla_h: int) -> str:
    block = f"""\n\n---\n\n## {AUTO_MARK} (stale triage)\n\nauto_triage_last: {now_iso}\n\n### Detected\n- stale trigger: in-progress + updated older than {sla_h}h\n\n### Fast diagnosis (fill 1 line each)\n- blocker kind: (dependency/spec/unknown/infra/approval/other)\n- real next action: (one concrete command/file/edit)\n- owner to unblock: (name/role)\n\n### Suggested actions\n- If dependency/approval: set `status: blocked` + write blocker + ping owner\n- If too big: split into 2 child tasks (keep this as parent)\n- If unclear: write 5-line spec in this task, then proceed\n"""
    if AUTO_MARK in text:
        # already has; just update auto_triage_last
        text = update_frontmatter(text, "auto_triage_last", now_iso)
        return text
    return text.rstrip() + block + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sla-h", type=int, default=24)
    ap.add_argument("--cooldown-h", type=int, default=12)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    now = datetime.now(ZoneInfo("Asia/Seoul"))
    now_iso = now.isoformat(timespec="seconds")

    tasks = [load_task(Path(p)) for p in glob.glob(ITEMS_GLOB)]

    stale: list[tuple[Task, timedelta]] = []
    for t in tasks:
        if (t.status or "").lower() != "in-progress":
            continue
        if t.updated is None:
            continue
        age = now - t.updated.astimezone(now.tzinfo)
        if age > timedelta(hours=args.sla_h):
            stale.append((t, age))

    lines: list[str] = []
    lines.append(f"# [ralph-loop] stale triage report — {now.strftime('%Y-%m-%d %H:%M KST')}")
    lines.append("")
    lines.append(f"- SLA: {args.sla_h}h | cooldown: {args.cooldown_h}h | apply: {args.apply}")
    lines.append(f"- stale(in-progress): {len(stale)}")

    if not stale:
        print("\n".join(lines))
        return 0

    lines.append("")
    lines.append("## Stale items")

    for t, age in sorted(stale, key=lambda x: (-x[1].total_seconds(), x[0].title)):
        lines.append(f"- [{t.priority}] {t.title} — assignee: {t.assignee or 'TBD'} — age: {int(age.total_seconds()//3600)}h")

        # Apply changes if requested and not in cooldown
        if args.apply:
            if t.auto_last is not None:
                since = now - t.auto_last.astimezone(now.tzinfo)
                if since < timedelta(hours=args.cooldown_h):
                    continue
            raw = t.path.read_text(encoding="utf-8")
            new = append_auto_block(raw, now_iso, args.sla_h)
            # If not already blocked, set status to blocked to force attention.
            if re.search(r"^\s*status\s*:\s*in-progress\s*$", new, re.I | re.M):
                new = re.sub(r"^\s*status\s*:\s*in-progress\s*$", "status: blocked", new, flags=re.I | re.M)
            # Update updated timestamp (since we touched it)
            new = update_frontmatter(new, "updated", now_iso)
            t.path.write_text(new, encoding="utf-8")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
