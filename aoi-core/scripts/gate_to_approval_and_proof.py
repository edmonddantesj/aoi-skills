#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert gate_report.json into Approval Request + Proof bundle (v0.1)")
    ap.add_argument("--gate", required=True, help="path to gate_report.json")
    ap.add_argument("--policy", required=True, help="path to acp_automation_policy_v0_1.json")
    ap.add_argument("--approvals-dir", default="aoi-core/state/approvals", help="approvals dir")
    ap.add_argument("--proofs-dir", default="aoi-core/state/proofs", help="proof bundle root dir")
    ap.add_argument("--id", required=True, help="approval/proof id (e.g., acp-20260220-0007)")
    ap.add_argument("--action", default="skill_update", help="action label")
    ap.add_argument("--provider", default="local", help="provider label")
    args = ap.parse_args()

    gate_path = Path(args.gate).resolve()
    policy_path = Path(args.policy).resolve()
    approvals_dir = Path(args.approvals_dir).resolve()
    proofs_dir = Path(args.proofs_dir).resolve() / args.id

    gate = read_json(gate_path)
    policy = read_json(policy_path)

    signal = (gate.get("result") or {}).get("signal")
    score = (gate.get("result") or {}).get("score")
    max_sev = (gate.get("result") or {}).get("max_severity")

    risk_level = "LOW"
    if signal == "yellow":
        risk_level = "MED"
    elif signal == "red":
        risk_level = "HIGH"

    status = "PENDING_APPROVAL"
    if signal == "red":
        status = "BLOCKED"

    # Build approval request (simple, compatible with our template)
    approval = {
        "id": args.id,
        "created_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "status": status,
        "action": args.action,
        "provider": args.provider,
        "action_mode": "queue_for_approval",
        "why_now": "Gate report generated; approval required to proceed.",
        "risk_level": risk_level,
        "cost_estimate": {"usd": 0, "fees_usd": 0, "slippage_bps": None},
        "required_inputs": {"account": "", "wallet": "", "params": {"gate_signal": signal, "gate_score": score}},
        "proof_plan": {
            "logs": "aoi-core/state/proofs/<id>/",
            "txhash": None,
            "screenshots": [],
            "sha256": None,
        },
        "dry_run_result": {"gate": {"signal": signal, "score": score, "max_severity": max_sev}},
        "operator_notes": "auto-generated from gate_report.json",
    }

    # Write proof bundle
    proofs_dir.mkdir(parents=True, exist_ok=True)
    (proofs_dir / "gate_report.json").write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
    (proofs_dir / "policy_snapshot.json").write_text(
        json.dumps(policy, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    inputs = {
        "created_at": utc_now_iso(),
        "gate_path": str(gate_path),
        "policy_path": str(policy_path),
        "action": args.action,
        "provider": args.provider,
    }
    (proofs_dir / "inputs.json").write_text(json.dumps(inputs, ensure_ascii=False, indent=2), encoding="utf-8")

    # Compute sha256 over the bundle files (deterministic order)
    hashes: dict[str, str] = {}
    for name in ["gate_report.json", "policy_snapshot.json", "inputs.json"]:
        b = (proofs_dir / name).read_bytes()
        hashes[name] = sha256_bytes(b)
    (proofs_dir / "sha256.json").write_text(json.dumps(hashes, ensure_ascii=False, indent=2), encoding="utf-8")

    approval["proof_plan"]["sha256"] = hashes

    approvals_dir.mkdir(parents=True, exist_ok=True)
    out_approval = approvals_dir / f"{args.id}.json"
    out_approval.write_text(json.dumps(approval, ensure_ascii=False, indent=2), encoding="utf-8")

    print("✅ wrote approval + proof")
    print("- approval:", out_approval)
    print("- proofs:", proofs_dir)
    print("- gate_signal:", signal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
