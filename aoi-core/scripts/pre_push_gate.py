#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def kst_timestamp() -> str:
    # Asia/Seoul is UTC+9 (no DST)
    return datetime.now(timezone.utc).astimezone(timezone.utc).isoformat()


def new_approval_id() -> str:
    # acp-YYYYMMDD-HHMMSS
    now = datetime.now(timezone.utc).astimezone()
    return now.strftime("acp-%Y%m%d-%H%M%S")


def main() -> int:
    ap = argparse.ArgumentParser(description="Pre-push security gate: Gate -> Approval -> Proof (fail-closed)")
    ap.add_argument("--repo", default=".", help="git repo path")
    ap.add_argument("--commit", default="HEAD", help="commit/ref to scan")
    ap.add_argument("--policy", default="aoi-core/state/acp_automation_policy_v0_1.json", help="policy path")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        print(f"[pre-push] Not a git repo: {repo}")
        return 2

    # Run gate
    gate_out = Path("/tmp") / "clawshield_pre_push_gate_report.json"
    cmd_gate = [
        "python3",
        str(repo / "aoi-core" / "scripts" / "clawshield_gate_poc.py"),
        "--repo",
        str(repo),
        "--commit",
        args.commit,
        "--out",
        str(gate_out),
    ]
    res = subprocess.run(cmd_gate, capture_output=True, text=True)
    print(res.stdout.rstrip())
    if res.returncode != 0:
        print(res.stderr.rstrip())
        print("[pre-push] Gate execution failed. Blocking push.")
        return 1

    # Convert to approval+proof
    approval_id = new_approval_id()
    cmd_conv = [
        "python3",
        str(repo / "aoi-core" / "scripts" / "gate_to_approval_and_proof.py"),
        "--gate",
        str(gate_out),
        "--policy",
        str(repo / args.policy),
        "--id",
        approval_id,
        "--action",
        "git_push",
        "--provider",
        "pre_push_gate",
    ]
    res2 = subprocess.run(cmd_conv, capture_output=True, text=True, cwd=str(repo))
    print(res2.stdout.rstrip())
    if res2.returncode != 0:
        print(res2.stderr.rstrip())
        print("[pre-push] Failed to write approval/proof. Blocking push.")
        return 1

    # Parse signal from gate report by grepping stdout line OR reading file quickly (no json dependency)
    try:
        import json

        gate = json.loads(gate_out.read_text(encoding="utf-8"))
        signal = (gate.get("result") or {}).get("signal")
        score = (gate.get("result") or {}).get("score")
    except Exception:
        signal = None
        score = None

    if signal == "red":
        print(f"[pre-push] ❌ BLOCKED: gate signal=red (score={score}).")
        print(f"[pre-push] Approval created: {approval_id} (see aoi-core/state/approvals)")
        return 1

    if signal == "yellow":
        print(f"[pre-push] ⚠️ WARN: gate signal=yellow (score={score}). Proceeding with push.")
        print(f"[pre-push] Approval created: {approval_id} (for audit trail)")
        return 0

    print(f"[pre-push] ✅ OK: gate signal={signal} (score={score}).")
    print(f"[pre-push] Approval created: {approval_id} (for audit trail)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
