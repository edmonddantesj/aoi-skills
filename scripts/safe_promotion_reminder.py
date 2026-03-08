#!/usr/bin/env python3
"""Safe Promotion reply reminder (24h cooldown).

Reads sprint backlog SSOT and reminds pending ADOPT/HOLD/CONFLICT replies.

- Source: context/ralph_loop/SPRINT_LOOP_BACKLOG_V0_1.md
- Topic ids: context/telegram_topics/thread_topic_map.json
- Cooldown state: context/state/safe_promotion_reminder.state.json

Delivery is handled by OpenClaw cron --announce to the maintenance topic.
This script only prints markdown to stdout.

Assumptions:
- Telegram internal group id for deep links is 3732040608 (from existing SSOT links).
- Backlog contains lines like: "Safe Promotion msgs: ops=3190, github=3191, ..."

Usage:
  python3 scripts/safe_promotion_reminder.py [--apply] [--cooldown-h 24]
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "context/ralph_loop/SPRINT_LOOP_BACKLOG_V0_1.md"
TOPIC_MAP = ROOT / "context/telegram_topics/thread_topic_map.json"
STATE_PATH = ROOT / "context/state/safe_promotion_reminder.state.json"

TELEGRAM_INTERNAL_GROUP_ID = "3732040608"  # derived from existing t.me/c links in SSOT

SAFE_PROMO_RE = re.compile(r"Safe Promotion msgs\s*:\s*(.+)$", re.I)
PAIR_RE = re.compile(r"\b([a-zA-Z0-9_-]+)\s*=\s*(\d+)\b")


@dataclass
class Pending:
    sprint: str
    slug: str
    msg_id: int


def load_topic_map() -> dict[str, int]:
    if TOPIC_MAP.exists():
        return json.loads(TOPIC_MAP.read_text(encoding="utf-8"))
    return {}


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"schema": "safe_promo_reminder.state.v0.1", "last": {}}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_backlog() -> list[Pending]:
    txt = BACKLOG.read_text(encoding="utf-8")
    out: list[Pending] = []

    current_sprint = None
    sprint_status_line = ""

    for line in txt.splitlines():
        if line.startswith("### Sprint "):
            current_sprint = line.strip("# ")
            sprint_status_line = line
            continue

        m = SAFE_PROMO_RE.search(line)
        if not m or not current_sprint:
            continue

        # Only remind when the sprint is still awaiting replies
        if "awaiting" not in sprint_status_line.lower() and "회신 대기" not in sprint_status_line:
            continue

        pairs = PAIR_RE.findall(m.group(1))
        for slug, mid in pairs:
            out.append(Pending(sprint=current_sprint, slug=slug, msg_id=int(mid)))

    return out


def deep_link(topic_id: int, msg_id: int) -> str:
    # Forum topic deep link format observed: https://t.me/c/<internal>/<topic>/<msg>
    return f"https://t.me/c/{TELEGRAM_INTERNAL_GROUP_ID}/{topic_id}/{msg_id}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="update reminder state (record last reminded timestamps)")
    ap.add_argument("--cooldown-h", type=int, default=24)
    args = ap.parse_args()

    now = datetime.now(ZoneInfo("Asia/Seoul"))
    now_iso = now.isoformat(timespec="seconds")

    topic_map = load_topic_map()
    state = load_state()
    last: dict = state.get("last", {}) if isinstance(state, dict) else {}

    pending = parse_backlog()

    due: list[Pending] = []
    for p in pending:
        key = f"{p.sprint}::{p.slug}::{p.msg_id}"
        prev = last.get(key)
        if prev:
            dt = None
            try:
                dt = datetime.fromisoformat(prev)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=ZoneInfo("Asia/Seoul"))
            except Exception:
                dt = None
            if dt is not None and (now - dt) < timedelta(hours=args.cooldown_h):
                continue
        due.append(p)

    lines: list[str] = []
    lines.append(f"# [Safe Promotion] 회신 리마인더 — {now.strftime('%Y-%m-%d %H:%M KST')}")
    lines.append("")

    if not due:
        lines.append("- pending replies: 0 (cooldown 내이거나 모두 처리됨)")
        print("\n".join(lines))
        return 0

    lines.append(f"- pending replies (due): {len(due)}")
    lines.append("- 요청: 각 토픽 Primary는 아래 패치에 **ADOPT/HOLD/CONFLICT** 중 1개로 회신")
    lines.append("")

    for p in due:
        tid = topic_map.get(p.slug)
        link = f"(topic id unknown for slug={p.slug})"
        if tid is not None:
            link = deep_link(tid, p.msg_id)
        lines.append(f"- {p.sprint} / {p.slug}: msgId={p.msg_id} → {link}")

    if args.apply:
        for p in due:
            key = f"{p.sprint}::{p.slug}::{p.msg_id}"
            last[key] = now_iso
        state["last"] = last
        state["updated_at"] = now_iso
        save_state(state)

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
