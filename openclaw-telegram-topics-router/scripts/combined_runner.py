#!/usr/bin/env python3
"""Combined inbound execution runner.

Connects the full pipeline in one call:
  1. inbound_execution_layer.decide()  → execution decision
  2. If delegate.should_delegate:
       mock_orchestrator_dispatch logic → orchestrator run
  3. Both artifacts written under a shared run_pointer (same run_key + thread_dir)
  4. Unified trace emitted to runtime/combined_runner/

Usage:
  python3 openclaw-telegram-topics-router/scripts/combined_runner.py \
    --chat-id telegram:-1003732040608 \
    --thread-id 6062 \
    --message "이어서 해야지" \
    [--local-hour 13] \
    [--preset planner-builder-reviewer] \
    [--dry-run]

  # or pipe JSON payload:
  echo '{"chat_id":"telegram:-1003732040608","message_thread_id":6062,"text":"이어서 해야지","local_hour":13}' \
    | python3 openclaw-telegram-topics-router/scripts/combined_runner.py --from-stdin
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Root / path helpers
# ---------------------------------------------------------------------------

def _find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "context" / "telegram_topics").exists():
            return parent
    return here.parents[4]


ROOT = _find_root()
SCRIPTS_DIR = ROOT / "openclaw-telegram-topics-router" / "scripts"
TOPICS_DIR = ROOT / "context" / "telegram_topics"
COMBINED_RUNTIME_DIR = TOPICS_DIR / "runtime" / "combined_runner"
SKILL_DIR = ROOT / "repos" / "aoi-skills" / "skills" / "aoi-squad-orchestrator-lite"
SKILL_JS = SKILL_DIR / "skill.js"


# ---------------------------------------------------------------------------
# Inbound decision (inline import)
# ---------------------------------------------------------------------------

def _run_inbound_decision(payload: dict) -> dict:
    """Import and call decide() from inbound_execution_layer."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "inbound_execution_layer",
        str(SCRIPTS_DIR / "inbound_execution_layer.py"),
    )
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod.decide(payload)


# ---------------------------------------------------------------------------
# Orchestrator dispatch (inline, mirrors mock_orchestrator_dispatch logic)
# ---------------------------------------------------------------------------

def _run_orchestrator(
    chat_id: str,
    thread_id: int,
    message: str,
    preset: str,
    run_dir: Path,
    latest_dir: Path,
    run_key: str,
    dry_run: bool,
) -> dict:
    """Run orchestrator skill and write artifacts into shared run_dir."""
    import importlib.util
    # Load thread/agent maps for slug + agent resolution
    thread_topic_map = TOPICS_DIR / "thread_topic_map.json"
    thread_agent_map = TOPICS_DIR / "thread_agent_map.json"

    def _load(p: Path) -> dict:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

    topic_data = _load(thread_topic_map)
    agent_data = _load(thread_agent_map)

    slug = next(
        (s for s, tid in topic_data.items() if str(tid) == str(thread_id)),
        None,
    )
    agent_entry = agent_data.get(slug, {}) if slug else {}
    primary = agent_entry.get("primary") if isinstance(agent_entry, dict) else None
    collaborators = agent_entry.get("collaborators", []) if isinstance(agent_entry, dict) else []

    created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    dispatch_record = {
        "schema": "openclaw.telegram.orchestrator_alpha_dispatch.v0_1",
        "chat_id": chat_id,
        "thread_id": thread_id,
        "slug": slug,
        "primary": primary,
        "collaborators": collaborators,
        "preset": preset,
        "message": message,
        "created_at": created_at,
        "run_key": run_key,
        "via": "combined_runner",
    }
    dispatch_json = json.dumps(dispatch_record, indent=2, ensure_ascii=False) + "\n"
    (run_dir / "orchestrator_dispatch.json").write_text(dispatch_json, encoding="utf-8")
    (latest_dir / "orchestrator_dispatch.json").write_text(dispatch_json, encoding="utf-8")

    if dry_run or not SKILL_JS.exists():
        stdout_out = json.dumps({"dry_run": True, "skipped": not SKILL_JS.exists()}, ensure_ascii=False)
        stderr_out = ""
        returncode = 0
    else:
        cmd = ["node", str(SKILL_JS), "run", "--preset", preset, "--task", message]
        proc = subprocess.run(cmd, cwd=str(SKILL_DIR), capture_output=True, text=True)
        stdout_out = proc.stdout
        stderr_out = proc.stderr or ""
        returncode = proc.returncode

    (run_dir / "orchestrator_stdout.json").write_text(stdout_out, encoding="utf-8")
    (run_dir / "orchestrator_stderr.log").write_text(stderr_out, encoding="utf-8")
    (latest_dir / "orchestrator_stdout.json").write_text(stdout_out, encoding="utf-8")
    (latest_dir / "orchestrator_stderr.log").write_text(stderr_out, encoding="utf-8")

    return {
        "ok": returncode == 0,
        "slug": slug,
        "primary": primary,
        "collaborators": collaborators,
        "dispatch_path": str(run_dir / "orchestrator_dispatch.json"),
        "stdout_path": str(run_dir / "orchestrator_stdout.json"),
        "stderr_path": str(run_dir / "orchestrator_stderr.log"),
        "returncode": returncode,
        "dry_run": dry_run or not SKILL_JS.exists(),
    }


# ---------------------------------------------------------------------------
# Combined trace writer
# ---------------------------------------------------------------------------

def _write_trace(
    run_dir: Path,
    latest_dir: Path,
    decision: dict,
    orch_result: dict | None,
    run_key: str,
    chat_id: str,
) -> dict:
    trace = {
        "schema": "openclaw.telegram.combined_runner_trace.v0_1",
        "run_key": run_key,
        "chat_id": chat_id,
        "thread_id": decision.get("thread_id"),
        "slug": decision.get("slug"),
        "decision": decision,
        "orchestrator": orch_result,
        "pipeline_complete": orch_result is not None and orch_result.get("ok", False),
    }
    data = json.dumps(trace, indent=2, ensure_ascii=False) + "\n"
    (run_dir / "trace.json").write_text(data, encoding="utf-8")
    (latest_dir / "trace.json").write_text(data, encoding="utf-8")
    return trace


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Combined inbound + orchestrator runner")
    ap.add_argument("--chat-id", default="telegram:-1003732040608")
    ap.add_argument("--thread-id", type=int, default=None)
    ap.add_argument("--message", default=None)
    ap.add_argument("--local-hour", type=int, default=None)
    ap.add_argument("--reply-target", default=None)
    ap.add_argument("--preset", default="planner-builder-reviewer")
    ap.add_argument("--dry-run", action="store_true", help="Skip actual orchestrator node call")
    ap.add_argument("--from-stdin", action="store_true", help="Read full JSON payload from stdin")
    args = ap.parse_args()

    # Build inbound payload
    if args.from_stdin:
        raw = sys.stdin.read().strip()
        payload = json.loads(raw) if raw else {}
    else:
        if not args.message:
            ap.error("--message is required (or use --from-stdin)")
        payload = {
            "chat_id": args.chat_id,
            "message_thread_id": args.thread_id,
            "text": args.message,
        }
        if args.local_hour is not None:
            payload["local_hour"] = args.local_hour
        if args.reply_target:
            payload["reply_target_agent"] = args.reply_target

    chat_id = payload.get("chat_id") or args.chat_id
    thread_id = payload.get("message_thread_id") or args.thread_id
    message = payload.get("text") or args.message or ""

    # Shared run_key and dirs
    run_ts = int(time.time())
    run_key = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(run_ts))
    thread_dir = COMBINED_RUNTIME_DIR / f"thread_{thread_id}"
    run_dir = thread_dir / "runs" / run_key
    latest_dir = thread_dir / "latest"
    run_dir.mkdir(parents=True, exist_ok=True)
    latest_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: inbound decision
    decision = _run_inbound_decision(payload)
    decision["run_key"] = run_key
    decision_json = json.dumps(decision, indent=2, ensure_ascii=False) + "\n"
    (run_dir / "decision.json").write_text(decision_json, encoding="utf-8")
    (latest_dir / "decision.json").write_text(decision_json, encoding="utf-8")

    # Step 2: orchestrator (only if delegate.should_delegate)
    orch_result = None
    should_delegate = decision.get("delegate", {}).get("should_delegate", False)
    if should_delegate:
        orch_result = _run_orchestrator(
            chat_id=chat_id,
            thread_id=thread_id,
            message=message,
            preset=args.preset,
            run_dir=run_dir,
            latest_dir=latest_dir,
            run_key=run_key,
            dry_run=args.dry_run,
        )
    else:
        skip_reason = decision.get("delegate", {}).get("skip_reason", "not_delegated")
        orch_result = {"ok": True, "skipped": True, "skip_reason": skip_reason}
        skip_json = json.dumps(orch_result, indent=2, ensure_ascii=False) + "\n"
        (run_dir / "orchestrator_skipped.json").write_text(skip_json, encoding="utf-8")
        (latest_dir / "orchestrator_skipped.json").write_text(skip_json, encoding="utf-8")

    # Step 3: unified trace
    trace = _write_trace(run_dir, latest_dir, decision, orch_result, run_key, chat_id)

    output = {
        "ok": trace["pipeline_complete"] or orch_result.get("skipped", False),
        "run_key": run_key,
        "thread_id": thread_id,
        "slug": decision.get("slug"),
        "mode": decision.get("mode"),
        "owner": decision.get("owner"),
        "reason": decision.get("reason"),
        "confidence": decision.get("confidence"),
        "should_delegate": should_delegate,
        "orchestrator": orch_result,
        "trace_path": str(run_dir / "trace.json"),
        "latest_trace_path": str(latest_dir / "trace.json"),
        "run_dir": str(run_dir),
    }
    print(json.dumps(output, ensure_ascii=False))
    return 0 if output["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
