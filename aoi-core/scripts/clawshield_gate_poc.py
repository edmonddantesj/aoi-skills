#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Ensure workspace root is importable when running from aoi-core/scripts
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from aoi_core.acp.clawshield_gate import make_report, scan_repo_snapshot


def git_verify_commit(repo: Path, commit: str) -> None:
    # local-only; no network. just verify the commit exists (quiet).
    subprocess.check_output(["git", "-C", str(repo), "rev-parse", "--verify", commit], stderr=subprocess.STDOUT)


def main() -> int:
    ap = argparse.ArgumentParser(description="ClawShield-style commit gate (PoC)")
    ap.add_argument("--repo", required=True, help="path to git repo")
    ap.add_argument("--commit", required=True, help="commit sha (must exist locally)")
    ap.add_argument("--out", required=True, help="output json path")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        raise SystemExit(f"Not a git repo: {repo}")

    git_verify_commit(repo, args.commit)

    # Safety note: we DO NOT checkout or modify working tree in this PoC.
    findings = scan_repo_snapshot(repo)
    report = make_report(repo=str(repo), commit=args.commit, findings=findings)

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("✅ clawshield_gate_poc: wrote")
    print(f"- out: {out}")
    print(f"- signal: {report['result']['signal']} (score {report['result']['score']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
