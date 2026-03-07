#!/usr/bin/env python3
"""Moltbook daily scan → draft-package seed.

Goal:
- Produce a daily draft package file (markdown) from publicly available signals.
- NO posting. NO secrets. Safe to run unattended.

Output:
- artifacts/moltbook/daily/YYYY-MM-DD.md

Notes:
- If Moltbook endpoints change / require auth, we still produce a skeleton file
  with TODOs rather than failing hard.
"""

from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
from typing import Any

import urllib.request


WORKSPACE = Path("/Users/silkroadcat/.openclaw/workspace")
OUT_DIR = WORKSPACE / "artifacts" / "moltbook" / "daily"


def http_get_json(url: str, timeout: int = 20) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": "openclaw-moltbook-scan/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return json.loads(raw)


def safe_posts_new(limit: int = 10) -> list[dict[str, Any]]:
    # Some deployments use www. prefix; keep it flexible.
    urls = [
        f"https://www.moltbook.com/api/v1/posts?sort=new&limit={limit}",
        f"https://moltbook.com/api/v1/posts?sort=new&limit={limit}",
    ]
    last_err = None
    for u in urls:
        try:
            data = http_get_json(u)
            if isinstance(data, dict) and "posts" in data and isinstance(data["posts"], list):
                return data["posts"]
            if isinstance(data, list):
                return data
            # Unknown shape; still return something useful.
            return [{"_raw": data}]
        except Exception as e:  # noqa: BLE001
            last_err = e
    raise RuntimeError(f"failed to fetch posts (tried {len(urls)} urls): {last_err}")


def render_md(today: str, posts: list[dict[str, Any]] | None, err: str | None) -> str:
    lines: list[str] = []
    lines.append(f"# Moltbook Daily Draft Package — {today}")
    lines.append("")
    lines.append("## 0) Constraints")
    lines.append("- External posting/commenting is **L3 (fail-closed)**: require explicit YES/NO approval.")
    lines.append("- This file is a draft package seed (scan → ideas → outline).")
    lines.append("")

    lines.append("## 1) Scan results (new posts)")
    if err:
        lines.append(f"- Scan error: `{err}`")
        lines.append("- Fallback: manually scan Moltbook TOP/New and fill below.")
    elif not posts:
        lines.append("- (no posts returned)")
    else:
        for i, p in enumerate(posts[:10], 1):
            title = str(p.get("title") or p.get("name") or p.get("subject") or "(no title)")
            pid = p.get("id") or p.get("post_id") or p.get("uuid") or ""
            url = p.get("url")
            if not url and pid:
                url = f"https://www.moltbook.com/post/{pid}"
            stats = []
            for k in ("likes", "like_count", "comments", "comment_count"):
                if k in p and p[k] is not None:
                    stats.append(f"{k}={p[k]}")
            stat_s = (" (" + ", ".join(stats) + ")") if stats else ""
            lines.append(f"{i}. {title}{stat_s}")
            if url:
                lines.append(f"   - {url}")
    lines.append("")

    lines.append("## 2) Candidate angles (pick 1)")
    lines.append("- A) Tooling deep dive (what we learned this week)")
    lines.append("- B) Proof-first / execution receipts (case study)")
    lines.append("- C) Ralph Loop (small routines → compounding)")
    lines.append("- D) Response to a Moltbook thread (quote + takeaways)")
    lines.append("")

    lines.append("## 3) Draft")
    lines.append("### Title")
    lines.append("- ")
    lines.append("### TL;DR (3 bullets)")
    lines.append("- ")
    lines.append("- ")
    lines.append("- ")
    lines.append("### Body outline")
    lines.append("1. ")
    lines.append("2. ")
    lines.append("3. ")
    lines.append("### CTA")
    lines.append("- ")
    lines.append("")

    lines.append("## 4) Approval gate")
    lines.append("- Chair decision: YES / NO")
    lines.append("- If YES: proceed to post via API/script and attach proof bundle in moltbook topic.")

    return "\n".join(lines) + "\n"


def main() -> None:
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime("%Y-%m-%d")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{today}.md"

    posts = None
    err = None
    try:
        posts = safe_posts_new(limit=10)
    except Exception as e:  # noqa: BLE001
        err = str(e)

    out_path.write_text(render_md(today, posts, err), encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()
