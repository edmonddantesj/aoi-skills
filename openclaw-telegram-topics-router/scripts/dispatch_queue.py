#!/usr/bin/env python3
"""Dispatch queued tasks with priority + locks + WIP limit.

Reads/Writes:
- context/ops/task_queue.json
- context/telegram_topics/workstream_lock_map.json (if present)

Algorithm (v0.1):
- Compute WIP = count(status==in_progress)
- Select up to N tasks from queued sorted by priority (P0..P3) then created_at
- For each candidate: if locks conflict -> mark blocked(lock-conflict)
- If policy_level==L3 requires approval_ref; otherwise blocked(policy)
- If --execute and exec_cmd present, run it; else just mark in_progress

Exit codes:
- 0 ok
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
QUEUE_PATH = ROOT / "context" / "ops" / "task_queue.json"
LOCKS_PATH = ROOT / "context" / "telegram_topics" / "workstream_lock_map.json"

PRIO_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def locks_load() -> dict:
    if not LOCKS_PATH.exists():
        return {"locks": {}}
    return load_json(LOCKS_PATH)


def locks_save(obj: dict) -> None:
    LOCKS_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_json(LOCKS_PATH, obj)


def can_claim(lock_key: str, locks_obj: dict) -> bool:
    return lock_key not in (locks_obj.get("locks") or {})


def claim(lock_key: str, entry: dict, locks_obj: dict) -> None:
    locks = locks_obj.setdefault("locks", {})
    locks[lock_key] = {
        "ledger_id": entry.get("ledger_id"),
        "queue_id": entry.get("queue_id"),
        "thread_id": (entry.get("target") or {}).get("thread_id"),
        "owner": entry.get("owner"),
        "claimed_at": now_iso(),
        "updated_at": now_iso(),
    }


def run_exec(cmd: str) -> tuple[int, str]:
    # run in shell to support simple one-liners. No sudo.
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out, _ = p.communicate()
    return int(p.returncode or 0), (out or "").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=None, help="Override max concurrency for this run")
    ap.add_argument("--execute", action="store_true", help="Run exec_cmd for dispatched tasks")
    args = ap.parse_args()

    if not QUEUE_PATH.exists():
        print(f"ERROR: missing SSOT file: {QUEUE_PATH.relative_to(ROOT)}")
        return 0

    q = load_json(QUEUE_PATH)
    defaults = q.get("defaults") or {}
    max_c = int(args.max or defaults.get("max_concurrency") or 1)

    items: list[dict] = list(q.get("items") or [])

    in_prog = [x for x in items if x.get("status") == "in_progress"]
    capacity = max(0, max_c - len(in_prog))

    if capacity <= 0:
        print("STATUS: idle")
        print(f"REASON: wip_full ({len(in_prog)}/{max_c})")
        return 0

    queued = [x for x in items if x.get("status") == "queued"]
    queued.sort(key=lambda x: (PRIO_ORDER.get(x.get("priority", "P3"), 9), x.get("created_at", "")))

    locks_obj = locks_load()

    dispatched = 0
    for entry in queued:
        if dispatched >= capacity:
            break

        policy = entry.get("policy_level")
        if policy == "L3" and not entry.get("approval_ref"):
            entry["status"] = "blocked"
            entry["last_error"] = "policy: L3 requires approval_ref"
            entry["updated_at"] = now_iso()
            continue

        lock_keys = entry.get("locks") or []
        conflict = next((k for k in lock_keys if not can_claim(k, locks_obj)), None)
        if conflict:
            entry["status"] = "blocked"
            entry["last_error"] = f"lock-conflict: {conflict}"
            entry["updated_at"] = now_iso()
            continue

        # claim locks (if lock registry exists or if locks requested)
        for k in lock_keys:
            claim(k, entry, locks_obj)

        entry["status"] = "in_progress"
        entry["attempts"] = int(entry.get("attempts") or 0) + 1
        entry["updated_at"] = now_iso()

        exec_cmd = entry.get("exec_cmd")
        if args.execute and exec_cmd:
            rc, out = run_exec(exec_cmd)
            # store short output; keep small
            entry["exec_rc"] = rc
            entry["exec_out_head"] = "\n".join(out.splitlines()[:20])
            if rc == 0:
                entry["status"] = "done"
                entry["done_at"] = now_iso()
            else:
                entry["status"] = "blocked"
                entry["last_error"] = f"exec failed rc={rc}"

        dispatched += 1
        print(f"DISPATCH: queue_id={entry.get('queue_id')} ledger_id={entry.get('ledger_id')} priority={entry.get('priority')} target_thread={((entry.get('target') or {}).get('thread_id'))}")

    # persist
    q["items"] = items
    q["generated_at"] = now_iso()
    save_json(QUEUE_PATH, q)
    if (entry.get("locks") for entry in queued):
        # only write if lock file exists or any locks were claimed
        if LOCKS_PATH.exists() or any((e.get("locks") for e in items)):
            locks_save(locks_obj)

    print("STATUS: ok")
    print(f"DISPATCHED: {dispatched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
