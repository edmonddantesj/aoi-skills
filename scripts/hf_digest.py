#!/usr/bin/env python3
"""Generate a compact digest of ACTIVE HF docs.

Writes:
- context/ops/digests/HF_ACTIVE_DIGEST_LATEST.md

Design goal: low-risk, file-only automation (no outbound messaging).
"""

from __future__ import annotations

import datetime as dt
import os
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "context/handoff/INDEX.md"
OUT_DIR = ROOT / "context/ops/digests"
OUT = OUT_DIR / "HF_ACTIVE_DIGEST_LATEST.md"

ACTIVE_RE = re.compile(r"^\- `(?P<file>HF_[^`]+\.md)`\s+—\s+(?P<title>.*)$")


def read_active(index_text: str):
    in_active = False
    items = []
    for line in index_text.splitlines():
        if line.strip() == "## ACTIVE":
            in_active = True
            continue
        if in_active and line.startswith("## "):
            break
        if in_active:
            m = ACTIVE_RE.match(line.strip())
            if m:
                items.append((m.group("file"), m.group("title")))
    return items


def head_sections(hf_text: str):
    # very small heuristic extraction
    def grab(section: str):
        m = re.search(rf"^## {re.escape(section)}\n(?P<body>(?:.*\n)*?)(?=^## |\Z)", hf_text, re.M)
        if not m:
            return []
        body = m.group("body").strip("\n")
        lines = [l.strip() for l in body.splitlines() if l.strip()]
        return lines[:8]

    meta = []
    for k in ["Status", "Owner", "Last updated", "Where"]:
        mm = re.search(rf"^\- \*\*{k}:\*\*\s*(.*)$", hf_text, re.M)
        if mm:
            meta.append(f"- {k}: {mm.group(1).strip()}")

    goal = grab("Goal")
    nexts = grab("Next actions (ordered)")
    blockers = grab("Risks / blockers")
    return meta, goal, nexts, blockers


def main():
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
    if not INDEX.exists():
        raise SystemExit(f"Missing index: {INDEX}")

    index_text = INDEX.read_text(encoding="utf-8")
    actives = read_active(index_text)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append(f"# HF ACTIVE Digest (latest)\n")
    lines.append(f"- Generated: {now.strftime('%Y-%m-%d %H:%M KST')}\n")
    lines.append(f"- Source: context/handoff/INDEX.md\n")

    if not actives:
        lines.append("## ACTIVE\n\n- (none)\n")
    else:
        lines.append("## ACTIVE\n")
        for fname, title in actives:
            path = ROOT / "context/handoff" / fname
            lines.append(f"### {fname} — {title}\n")
            if not path.exists():
                lines.append("- BLOCKED: file missing\n")
                continue
            hf_text = path.read_text(encoding="utf-8", errors="ignore")
            meta, goal, nexts, blockers = head_sections(hf_text)
            if meta:
                lines.extend(meta)
            if goal:
                lines.append("- Goal:")
                lines.extend([f"  - {g.lstrip('- ').strip()}" for g in goal])
            if nexts:
                lines.append("- Next:")
                # keep only first 3 next actions
                cleaned = []
                for n in nexts:
                    n = re.sub(r"^\d+\.\s*", "", n)
                    if n.startswith("-"):
                        n = n.lstrip("- ")
                    if n:
                        cleaned.append(n)
                for n in cleaned[:3]:
                    lines.append(f"  - {n}")
            if blockers:
                lines.append("- Blockers/Risks:")
                lines.extend([f"  - {b.lstrip('- ').strip()}" for b in blockers[:3]])
            lines.append("")

    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
