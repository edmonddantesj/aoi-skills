#!/usr/bin/env python3
"""Topic-local runtime trace summarizer.

Reads all combined_runner run traces for a given thread and emits a
consistent per-topic runtime log: last N runs, pipeline status, owner,
confidence, reason — in a single JSON summary file.

Usage:
  python3 openclaw-telegram-topics-router/scripts/topic_trace_summary.py \
    --thread-id 6062 [--limit 10]

Output:
  context/telegram_topics/runtime/combined_runner/thread_<id>/summary.json
  (also printed to stdout)
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


def load_runs(thread_id: int, limit: int) -> list[dict]:
    runs_dir = COMBINED_RUNTIME_DIR / f"thread_{thread_id}" / "runs"
    if not runs_dir.exists():
        return []
    run_keys = sorted(runs_dir.iterdir(), key=lambda p: p.name, reverse=True)[:limit]
    results = []
    for rk in run_keys:
        trace_path = rk / "trace.json"
        if not trace_path.exists():
            continue
        try:
            trace = json.loads(trace_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        d = trace.get("decision", {})
        o = trace.get("orchestrator", {})
        results.append({
            "run_key": trace.get("run_key"),
            "slug": trace.get("slug"),
            "mode": d.get("mode"),
            "owner": d.get("owner"),
            "reason": d.get("reason"),
            "confidence": d.get("confidence"),
            "text_norm": d.get("text_norm", "")[:80],
            "pipeline_complete": trace.get("pipeline_complete"),
            "orch_ok": o.get("ok"),
            "orch_skipped": o.get("skipped"),
            "orch_skip_reason": o.get("skip_reason"),
        })
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--thread-id", type=int, required=True)
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    runs = load_runs(args.thread_id, args.limit)

    thread_dir = COMBINED_RUNTIME_DIR / f"thread_{args.thread_id}"
    latest_dir = thread_dir / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "schema": "openclaw.telegram.topic_trace_summary.v0_1",
        "thread_id": args.thread_id,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "run_count": len(runs),
        "runs": runs,
    }
    data = json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    (latest_dir / "summary.json").write_text(data, encoding="utf-8")

    print(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
