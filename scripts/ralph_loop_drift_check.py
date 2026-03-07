#!/usr/bin/env python3
"""ralph-loop drift integrity check + (optional) auto-repair.

Design goals:
- Deterministic, local-only.
- Snapshot-first, rollback-on-fail.
- Scope is SSOT-driven: context/ralph_loop/DRIFT_CANONICAL_SCOPE_V0_1.md

Current implementation (v0.1):
- Computes SHA256 checksums for canonical directories.
- Stores them under context/state/ralph_loop_drift.checksums.json
- Detects drift by comparing against previous checksums.
- Auto-repair is conservative: if a file is missing but has a snapshot copy,
  restore it; if checksum mismatch, do not overwrite automatically (report only)
  unless --aggressive is passed.

This is intentionally cautious even in "auto" mode.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE_MD = ROOT / "context/ralph_loop/DRIFT_CANONICAL_SCOPE_V0_1.md"
STATE_DIR = ROOT / "context/state"
CHECKSUMS_PATH = STATE_DIR / "ralph_loop_drift.checksums.json"

CANONICAL_DIRS = [
    ROOT / "context/state",
    ROOT / "context/ops/reports",
    ROOT / "context/ops/items",
]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def list_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    out: list[Path] = []
    for p in base.rglob("*"):
        if p.is_file():
            # ignore transient/large dirs if any
            if "/.git/" in str(p):
                continue
            # avoid self-referential drift: the checksum file changes when written
            if p.resolve() == CHECKSUMS_PATH.resolve():
                continue
            out.append(p)
    return sorted(out)


def snapshot_dir(ts: str) -> Path:
    snap = ROOT / "artifacts/state_saves" / ts
    snap.mkdir(parents=True, exist_ok=True)
    return snap


def copy_to_snapshot(ts: str, files: list[Path]) -> Path:
    snap = snapshot_dir(ts)
    for p in files:
        rel = p.relative_to(ROOT)
        dst = snap / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
    return snap


def load_prev() -> dict:
    if CHECKSUMS_PATH.exists():
        d = json.loads(CHECKSUMS_PATH.read_text(encoding="utf-8"))
        # Migration guard: older baselines may have included the checksum file itself.
        try:
            files = d.get("files", {}) if isinstance(d, dict) else {}
            if isinstance(files, dict):
                files.pop(str(CHECKSUMS_PATH.relative_to(ROOT)), None)
        except Exception:
            pass
        return d
    return {}


def save_now(data: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CHECKSUMS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="attempt auto-repair where safe")
    ap.add_argument("--aggressive", action="store_true", help="allow overwriting checksum-mismatched files from snapshot if available")
    ap.add_argument("--snapshot", action="store_true", help="force snapshot creation")
    args = ap.parse_args()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

    files: list[Path] = []
    for d in CANONICAL_DIRS:
        files.extend(list_files(d))

    # Always snapshot if applying
    did_snapshot = False
    snap_path: Path | None = None
    if args.apply or args.snapshot:
        snap_path = copy_to_snapshot(ts, files)
        did_snapshot = True

    pre = {
        "schema": "ralph-loop.drift.checksums.v0.1",
        "generated_at": ts,
        "scope": {
            "md": str(SCOPE_MD.relative_to(ROOT)),
            "dirs": [str(d.relative_to(ROOT)) for d in CANONICAL_DIRS],
        },
        "files": {str(p.relative_to(ROOT)): sha256_file(p) for p in files},
    }

    prev = load_prev()
    prev_files: dict = prev.get("files", {}) if isinstance(prev, dict) else {}

    missing_in_current = []  # existed before, missing now
    changed = []
    new_files = []

    cur_files = pre["files"]

    for path, old_hash in prev_files.items():
        if path not in cur_files:
            missing_in_current.append(path)
        elif cur_files[path] != old_hash:
            changed.append(path)

    for path in cur_files.keys():
        if path not in prev_files:
            new_files.append(path)

    drift = {
        "missing": missing_in_current,
        "changed": changed,
        "new": new_files,
    }

    repaired = {"restored": [], "overwritten": []}

    if args.apply:
        # restore missing files only if snapshot contains them
        if snap_path is None:
            snap_path = snapshot_dir(ts)
        for rel in missing_in_current:
            src = snap_path / rel
            dst = ROOT / rel
            if src.exists() and not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                repaired["restored"].append(rel)

        if args.aggressive:
            # overwrite changed files from snapshot (best-effort)
            for rel in changed:
                src = snap_path / rel
                dst = ROOT / rel
                if src.exists() and dst.exists():
                    shutil.copy2(src, dst)
                    repaired["overwritten"].append(rel)

    # Save POST-repair state as new baseline (important: if we repaired files,
    # the baseline must reflect the repaired content, not the pre-repair hashes).
    post_files: list[Path] = []
    for d in CANONICAL_DIRS:
        post_files.extend(list_files(d))

    post = {
        "schema": "ralph-loop.drift.checksums.v0.1",
        "generated_at": ts,
        "scope": pre["scope"],
        "files": {str(p.relative_to(ROOT)): sha256_file(p) for p in post_files},
    }

    save_now(post)

    out = {
        "ok": (len(missing_in_current) == 0 and len(changed) == 0),
        "snapshot": str(snap_path.relative_to(ROOT)) if did_snapshot and snap_path else None,
        "drift": drift,
        "repaired": repaired,
        "checksums": str(CHECKSUMS_PATH.relative_to(ROOT)),
    }

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
