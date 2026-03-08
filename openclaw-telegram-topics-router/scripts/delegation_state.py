#!/usr/bin/env python3
"""Delegation runtime state (cooldown + buffering) helper.

Stores a small local JSON state file under:
  context/telegram_topics/runtime/delegation_state.json

This is a building block for an execution layer. It does not call Telegram.

Commands:
- check: determine if a thread is in cooldown
- record: record that delegation just happened (set cooldown_until)

Example:
  python3 .../delegation_state.py check --chat-id telegram:-100... --thread-id 38
  python3 .../delegation_state.py record --chat-id telegram:-100... --thread-id 38 --cooldown-sec 180
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
STATE_DIR = ROOT / "context" / "telegram_topics" / "runtime"
STATE_PATH = STATE_DIR / "delegation_state.json"


def _load() -> dict:
    if not STATE_PATH.exists():
        return {"schema": "openclaw.telegram.delegation_state.v0_1", "threads": {}}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def _save(data: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_check = sub.add_parser("check")
    ap_check.add_argument("--chat-id", required=True)
    ap_check.add_argument("--thread-id", required=True, type=int)

    ap_record = sub.add_parser("record")
    ap_record.add_argument("--chat-id", required=True)
    ap_record.add_argument("--thread-id", required=True, type=int)
    ap_record.add_argument("--cooldown-sec", type=int, default=180)

    args = ap.parse_args()

    key = f"{args.chat_id}:{args.thread_id}"
    now = int(time.time())

    data = _load()
    threads = data.setdefault("threads", {})
    entry = threads.get(key, {})

    if args.cmd == "check":
        cooldown_until = int(entry.get("cooldown_until", 0) or 0)
        in_cooldown = now < cooldown_until
        out = {
            "ok": True,
            "key": key,
            "now": now,
            "cooldown_until": cooldown_until,
            "in_cooldown": in_cooldown,
        }
        print(json.dumps(out, ensure_ascii=False))
        return 0

    if args.cmd == "record":
        entry["cooldown_until"] = now + int(args.cooldown_sec)
        entry["last_recorded_at"] = now
        threads[key] = entry
        _save(data)
        out = {"ok": True, "key": key, "cooldown_until": entry["cooldown_until"]}
        print(json.dumps(out, ensure_ascii=False))
        return 0

    raise SystemExit("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
