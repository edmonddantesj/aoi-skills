#!/usr/bin/env python3
"""Enqueue a task for cross-topic handoff.

Updates:
- context/ops/task_queue.json

This script is intentionally simple:
- It records routing metadata (source/target threads, slug)
- It records scheduling metadata (priority, policy level)
- It optionally records locks[] and exec_cmd (for auto-dispatch)

Exit codes:
- 0 success
- 2 missing SSOT
"""

from __future__ import annotations

import argparse
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
QUEUE_PATH = ROOT / "context" / "ops" / "task_queue.json"
MAP_PATH = ROOT / "context" / "telegram_topics" / "thread_topic_map.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_slug_to_thread_id(slug: str) -> str | None:
    if not MAP_PATH.exists():
        return None
    data = load_json(MAP_PATH)
    m = (data.get("map") or {})
    for tid, s in m.items():
        if s == slug:
            return str(tid)
    return None


def parse_csv(s: str | None) -> list[str]:
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--ledger-id", default=None, help="Stable task id (recommended). If omitted, a Q- id is generated.")
    ap.add_argument("--priority", default="P1", choices=["P0", "P1", "P2", "P3"])
    ap.add_argument("--policy", default="L2", choices=["L1", "L2", "L3"])
    ap.add_argument("--approval-ref", default=None, help="Required when policy=L3")

    ap.add_argument("--source-thread-id", default=None)
    ap.add_argument("--target-thread-id", default=None)
    ap.add_argument("--target-slug", default=None, help="If provided, will resolve to target_thread_id using thread_topic_map.json")

    ap.add_argument("--owner", default=None)
    ap.add_argument("--locks", default=None, help="Comma-separated lock keys")
    ap.add_argument("--exec", default=None, help="Optional command to run on dispatch (single string).")

    args = ap.parse_args()

    if not QUEUE_PATH.exists():
        print(f"ERROR: missing SSOT file: {QUEUE_PATH.relative_to(ROOT)}")
        print("NEXT: run init_task_queue_ssot.py")
        return 2

    if args.policy == "L3" and not args.approval_ref:
        print("ERROR: policy=L3 requires --approval-ref")
        return 2

    target_thread_id = args.target_thread_id
    if not target_thread_id and args.target_slug:
        target_thread_id = resolve_slug_to_thread_id(args.target_slug)
        if not target_thread_id:
            print("ERROR: could not resolve target slug to thread_id")
            print("HINT: ensure context/telegram_topics/thread_topic_map.json is initialized and contains the slug")
            return 2

    q = load_json(QUEUE_PATH)
    items = q.setdefault("items", [])

    ledger_id = args.ledger_id or f"Q-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(3)}"

    entry = {
        "queue_id": f"TQ-{secrets.token_hex(4)}",
        "ledger_id": ledger_id,
        "title": args.title,
        "priority": args.priority,
        "policy_level": args.policy,
        "approval_ref": args.approval_ref,
        "status": "queued",
        "source": {
            "thread_id": args.source_thread_id,
        },
        "target": {
            "thread_id": target_thread_id,
            "slug": args.target_slug,
        },
        "owner": args.owner,
        "locks": parse_csv(args.locks),
        "exec_cmd": args.exec,
        "attempts": 0,
        "last_error": None,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }

    items.append(entry)
    q["generated_at"] = now_iso()
    save_json(QUEUE_PATH, q)

    print("STATUS: enqueued")
    print(f"PROOF: file={QUEUE_PATH.relative_to(ROOT)}")
    print(f"QUEUE_ID: {entry['queue_id']}")
    print(f"LEDGER_ID: {entry['ledger_id']}")
    print(f"TARGET_THREAD: {target_thread_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
