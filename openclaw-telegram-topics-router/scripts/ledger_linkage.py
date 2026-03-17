#!/usr/bin/env python3
"""Ledger linkage for combined_runner traces.

Links a combined_runner run trace to the ralph_loop ledger:
- Appends a lightweight "run_ref" proof entry into the matching ledger item
  (matched by slug → topic label, or by --ledger-id override)
- If no matching item found, writes a standalone linkage record instead
- Non-destructive: only appends to acceptance.proof[], never modifies other fields

Usage:
  python3 openclaw-telegram-topics-router/scripts/ledger_linkage.py \
    --thread-id 6062 \
    [--run-key 20260317T043022Z]   # defaults to latest
    [--ledger-id RL-20260306-001]  # override auto-match
    [--dry-run]

Output:
  - updates context/ralph_loop/ledger.json (in-place, proof append only)
  - writes context/telegram_topics/runtime/combined_runner/thread_<id>/latest/ledger_link.json
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def _find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "context" / "telegram_topics").exists():
            return parent
    return here.parents[4]


ROOT = _find_root()
COMBINED_RUNTIME_DIR = ROOT / "context" / "telegram_topics" / "runtime" / "combined_runner"
LEDGER_PATH = ROOT / "context" / "ralph_loop" / "ledger.json"

# Slug → ledger label keywords for auto-matching
SLUG_LABEL_HINTS: dict[str, list[str]] = {
    "cat-strategic": ["router", "orchestrat", "dispatch", "inbound", "delegation"],
    "acp": ["acp", "dispatch"],
    "ops": ["ops", "devops", "infra"],
    "adp": ["adp", "ops-task", "task-manager"],
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_trace(thread_id: int, run_key: str | None) -> tuple[dict, Path]:
    thread_dir = COMBINED_RUNTIME_DIR / f"thread_{thread_id}"
    if run_key:
        trace_path = thread_dir / "runs" / run_key / "trace.json"
    else:
        trace_path = thread_dir / "latest" / "trace.json"
    if not trace_path.exists():
        raise FileNotFoundError(f"Trace not found: {trace_path}")
    return _load_json(trace_path), trace_path


def _find_ledger_item(ledger: dict, slug: str | None, ledger_id: str | None) -> dict | None:
    items = ledger.get("items", [])
    if ledger_id:
        return next((i for i in items if i.get("id") == ledger_id), None)
    if not slug:
        return None
    hints = SLUG_LABEL_HINTS.get(slug, [])
    for item in items:
        labels = [str(l).lower() for l in item.get("labels", [])]
        title = item.get("title", "").lower()
        notes = item.get("notes", "").lower()
        for hint in hints:
            if any(hint in l for l in labels) or hint in title or hint in notes:
                return item
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--thread-id", type=int, required=True)
    ap.add_argument("--run-key", default=None)
    ap.add_argument("--ledger-id", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    trace, trace_path = _load_trace(args.thread_id, args.run_key)
    d = trace.get("decision", {})
    o = trace.get("orchestrator", {})

    proof_entry = {
        "type": "combined_runner_run",
        "run_key": trace.get("run_key"),
        "thread_id": args.thread_id,
        "slug": trace.get("slug"),
        "mode": d.get("mode"),
        "owner": d.get("owner"),
        "reason": d.get("reason"),
        "confidence": d.get("confidence"),
        "pipeline_complete": trace.get("pipeline_complete"),
        "orch_ok": o.get("ok"),
        "orch_skipped": o.get("skipped"),
        "trace_path": str(trace_path),
        "linked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    ledger_link = {
        "schema": "openclaw.telegram.ledger_linkage.v0_1",
        "thread_id": args.thread_id,
        "run_key": trace.get("run_key"),
        "slug": trace.get("slug"),
        "proof_entry": proof_entry,
        "ledger_item_id": None,
        "matched": False,
        "dry_run": args.dry_run,
    }

    if LEDGER_PATH.exists():
        ledger = _load_json(LEDGER_PATH)
        item = _find_ledger_item(ledger, trace.get("slug"), args.ledger_id)
        if item:
            ledger_link["ledger_item_id"] = item.get("id")
            ledger_link["matched"] = True
            if not args.dry_run:
                proof_list = item.setdefault("acceptance", {}).setdefault("proof", [])
                proof_list.append(proof_entry)
                item["updated_at"] = proof_entry["linked_at"]
                ledger_path_str = json.dumps(ledger, indent=2, ensure_ascii=False) + "\n"
                LEDGER_PATH.write_text(ledger_path_str, encoding="utf-8")
        else:
            ledger_link["matched"] = False
            ledger_link["note"] = "No matching ledger item found for slug. Standalone linkage record only."
    else:
        ledger_link["note"] = "ledger.json not found — standalone linkage record only."

    # Write linkage record into latest/
    latest_dir = COMBINED_RUNTIME_DIR / f"thread_{args.thread_id}" / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)
    link_data = json.dumps(ledger_link, indent=2, ensure_ascii=False) + "\n"
    (latest_dir / "ledger_link.json").write_text(link_data, encoding="utf-8")

    print(link_data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
