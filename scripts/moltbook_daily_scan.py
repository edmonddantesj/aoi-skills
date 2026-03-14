#!/usr/bin/env python3
"""Moltbook daily scan → detailed draft package.

Goal:
- Produce a near-post-ready daily draft package from publicly available signals
  plus local moltbook handoff instructions.
- NO posting. NO secrets. Safe to run unattended.

Output:
- artifacts/moltbook/daily/YYYY-MM-DD.md

Behavior:
- Pull recent Moltbook new posts when available.
- Pull current operator directives from HF / playbook notes.
- Generate a recommended angle, title variants, summary, full draft,
  CTA, end-matter placeholders, and approval checklist.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

import urllib.request


WORKSPACE = Path("/Users/silkroadcat/.openclaw/workspace")
OUT_DIR = WORKSPACE / "artifacts" / "moltbook" / "daily"
HF_PATH = WORKSPACE / "context" / "handoff" / "HF_moltbook_ops_202603.md"
PLAYBOOK_PATH = WORKSPACE / "context" / "topics" / "moltbook_PLAYBOOK_V0_1.md"


def http_get_json(url: str, timeout: int = 20) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": "openclaw-moltbook-scan/0.2"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return json.loads(raw)


def safe_posts_new(limit: int = 10) -> list[dict[str, Any]]:
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
            return [{"_raw": data}]
        except Exception as e:  # noqa: BLE001
            last_err = e
    raise RuntimeError(f"failed to fetch posts (tried {len(urls)} urls): {last_err}")


def _normalize(text: str) -> str:
    return " ".join((text or "").lower().replace("-", " ").replace("_", " ").split())


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        return ""


def extract_operator_directives() -> list[str]:
    text = read_text(HF_PATH)
    bullets: list[str] = []
    allow = ["daily", "draft", "upload", "comment", "reply", "writer", "review", "approval", "posted", "proof bundle"]
    deny = ["scope:", "owner/primary", "근거", "대표 글 링크", "thread_id", "evidence", "reference"]
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("- [ ]") or s.startswith("- "):
            body = re.sub(r"^- \[.\] ?", "", s)
            body = re.sub(r"^- ", "", body)
            low = body.lower()
            if any(d in low for d in deny):
                continue
            if any(k in low for k in allow):
                bullets.append(body)
    seen = []
    for b in bullets:
        if b not in seen:
            seen.append(b)
    return seen[:6]


def build_candidate_angles(posts: list[dict[str, Any]] | None) -> list[dict[str, str]]:
    defaults = [
        {
            "key": "constraints_before_memory",
            "label": "Clearer constraints before bigger memory",
            "thesis": "Most agent inconsistency is a contract failure before it becomes a memory failure.",
        },
        {
            "key": "proof_first",
            "label": "Proof-first / execution receipts",
            "thesis": "Reliable agent operations depend on visible receipts, not just confident claims.",
        },
        {
            "key": "creator_mechanics",
            "label": "Creator mechanics from live comment threads",
            "thesis": "Distribution quality often depends on how a post invites response and how quickly the author joins the thread.",
        },
        {
            "key": "ops_loop",
            "label": "Ralph Loop / small routines compound",
            "thesis": "Small repeatable operating loops compound into trust, quality, and recoverability.",
        },
    ]
    if not posts:
        return defaults

    joined = " ".join(
        _normalize(str(p.get("title") or p.get("name") or p.get("subject") or ""))
        for p in posts[:10]
    )
    scored: list[tuple[int, dict[str, str]]] = []
    for item in defaults:
        key = item["key"]
        score = 0
        if key == "constraints_before_memory":
            score += sum(1 for kw in ["agent", "memory", "identity", "trust", "workflow", "constraint"] if kw in joined)
        elif key == "proof_first":
            score += sum(1 for kw in ["proof", "verify", "receipt", "audit", "signal"] if kw in joined)
        elif key == "creator_mechanics":
            score += sum(1 for kw in ["comment", "thread", "creator", "post", "audience"] if kw in joined)
            score += sum(1 for p in posts[:10] if (p.get("comment_count") or 0) >= 3)
        elif key == "ops_loop":
            score += sum(1 for kw in ["daily", "routine", "system", "process", "tooling"] if kw in joined)
        scored.append((score, item))
    scored.sort(key=lambda x: -x[0])
    return [item for _, item in scored]


def choose_primary(posts: list[dict[str, Any]] | None) -> dict[str, str]:
    return build_candidate_angles(posts)[0]


def title_variants(primary: dict[str, str]) -> list[str]:
    if primary["key"] == "constraints_before_memory":
        return [
            "Stop Treating Agent Memory Like a Scrap Pile",
            "Most Agent Failures Are Contract Failures First",
            "Before Bigger Memory, Give Agents Clearer Commitments",
        ]
    if primary["key"] == "proof_first":
        return [
            "Reliable Agents Need Receipts, Not Just Confidence",
            "Execution Receipts Are Becoming the Real Agent UX",
            "If You Can’t Show the Receipt, Don’t Call It Automation",
        ]
    if primary["key"] == "creator_mechanics":
        return [
            "Threads Don’t Grow by Themselves",
            "Good Posts Invite Replies. Good Operators Show Up Fast.",
            "Distribution Is Often a Comment-Speed Problem",
        ]
    return [
        "Small Loops Compound Faster Than Grand Strategies",
        "The Boring Agent Routine That Actually Scales",
        "Why Repeatable Ops Matter More Than Heroic Bursts",
    ]


def select_reference_posts(posts: list[dict[str, Any]] | None, limit: int = 3) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    if not posts:
        return refs
    for p in posts[:10]:
        title = str(p.get("title") or p.get("name") or p.get("subject") or "(no title)")
        pid = p.get("id") or p.get("post_id") or p.get("uuid") or ""
        url = p.get("url") or (f"https://www.moltbook.com/post/{pid}" if pid else "")
        refs.append({"title": title, "url": url})
        if len(refs) >= limit:
            break
    return refs


def build_body(primary: dict[str, str], refs: list[dict[str, str]], directives: list[str]) -> str:
    title_hint = refs[0]["title"] if refs else "recent threads"
    directive_hint = directives[0] if directives else "post, then actively work the early reply window instead of treating publication as the endpoint"

    if primary["key"] == "constraints_before_memory":
        paras = [
            "A lot of teams still talk about agent reliability as if the core problem were memory size. Bigger windows, more retrieval, more context, more persistence. That matters. But in live workflows, the first failure is often more boring: the agent does not have a stable contract.",
            "If role, boundaries, escalation rules, and handoff format are fuzzy, memory just stores more ambiguity. The system remembers fragments, but it still does not know what must remain stable. That is why an agent can look informed and still feel inconsistent.",
            "The more useful framing is this: before asking how to make an agent remember more, ask what it is allowed to do without approval, what it must escalate, what artifacts it should write back to, and what other humans or agents can safely assume will remain true across sessions.",
            f"That is also why threads like \"{title_hint}\" tend to resonate. People are not only asking for smarter outputs. They are asking for systems they can route work through without guessing where the invisible edges are.",
            f"Our own operating bias is simple: {directive_hint}. In practice that means we care less about sounding universally capable and more about making commitments visible. A visible limit is not weakness. It is an interface.",
            "When constraints are explicit, continuity improves, handoffs get cleaner, approvals become cheaper, and trust stops depending on trial and error. Bigger memory can help later. But clearer commitments usually help first.",
        ]
    elif primary["key"] == "proof_first":
        paras = [
            "Agent systems accumulate hidden risk whenever they substitute narrative confidence for execution evidence. A good answer is useful. A receipt is operational.",
            "Proof-first operations do not require perfect observability. They require a habit: every meaningful action should leave behind something another operator can inspect. A URL. A response id. A diff. A screenshot. A trace. A timestamped artifact.",
            "This matters because modern agent workflows are multi-step and multi-actor. One agent drafts, another reviews, a human approves, a cron retries, a tool mutates state. Without receipts, every failure becomes a memory contest. With receipts, it becomes a debugging problem.",
            f"That is why recent signals like \"{title_hint}\" are interesting. The community keeps circling the same trust question from different angles: not just whether an agent can act, but whether we can inspect what it actually did.",
            "Receipts also improve behavior upstream. When an action must produce evidence, teams naturally define boundaries better, reduce vague side effects, and think harder about replayability. Proof is not paperwork after the fact. It is architecture pressure during design.",
            "The result is not glamorous. But boring evidence often scales better than impressive demos.",
        ]
    elif primary["key"] == "creator_mechanics":
        paras = [
            "A lot of distribution advice still treats posting like a one-shot publishing event. Write the post. Hit publish. Hope the feed does the rest. In practice, thread quality often depends on what happens in the first few minutes after publication.",
            "A strong post does not just communicate a thought. It creates a clean place for response. The title frames the disagreement. The lead gives readers a hook. The CTA makes participation low-friction. Then the operator has to actually show up.",
            "That last part is underrated. Fast, relevant replies in early comments do more than boost engagement metrics. They tell the audience the thread is alive, clarify the post’s center of gravity, and convert vague reactions into specific discussion.",
            f"We see that pattern in threads like \"{title_hint}\". The difference between a quiet post and a durable discussion is often not the idea alone. It is whether the thread has enough structure and enough operator presence to keep attention coherent.",
            f"That is why our operating rule is converging toward this: {directive_hint}. The post is only half the object. The early comment loop is the other half.",
            "Good distribution is not just writing. It is thread stewardship.",
        ]
    else:
        paras = [
            "Most operating systems fail quietly before they fail dramatically. The pattern is familiar: no one updates the checklist, no one writes the artifact, no one closes the loop, and eventually the entire workflow depends on memory and goodwill.",
            "That is why small routines matter more than they look. A repeated scan. A daily draft. A visible handoff. A proof bundle after execution. None of these are exciting alone. Together, they turn vague intention into a system people can rely on.",
            "The value is not only throughput. It is continuity. Small loops reduce reset costs, make delegation less fragile, and preserve context in forms other people can inspect later.",
            f"Recent Moltbook signals like \"{title_hint}\" are a reminder that people are hungry for systems thinking, not just isolated clever takes. The community notices when work is part of a repeatable loop instead of an occasional burst.",
            f"Our own bias is simple: {directive_hint}. That sounds procedural because it is. Compounding usually comes from boring things done on schedule.",
            "A strong loop does not need to feel magical. It needs to keep making the next good action easier.",
        ]
    return "\n\n".join(paras)


def render_md(today: str, posts: list[dict[str, Any]] | None, err: str | None) -> str:
    directives = extract_operator_directives()
    primary = choose_primary(posts)
    refs = select_reference_posts(posts)
    titles = title_variants(primary)
    body = build_body(primary, refs, directives)

    lines: list[str] = []
    lines.append(f"# Moltbook Daily Draft Package — {today}")
    lines.append("")
    lines.append("## 0) Run intent")
    lines.append("- Goal: prepare a near-post-ready Moltbook EN draft before upload approval.")
    lines.append("- Output mode: detailed draft package (not topic seed only).")
    lines.append("- Posting remains **L3 / fail-closed**: explicit YES required.")
    lines.append("")

    lines.append("## 1) Operator directives carried forward")
    if directives:
        for d in directives:
            lines.append(f"- {d}")
    else:
        lines.append("- (no local directives found; fallback to playbook default daily EN draft)")
    lines.append("")

    lines.append("## 2) Scan results (new posts)")
    if err:
        lines.append(f"- Scan error: `{err}`")
        lines.append("- Fallback: continue with local operating thesis + previous handoff notes.")
    elif not posts:
        lines.append("- (no posts returned)")
    else:
        for i, p in enumerate(posts[:8], 1):
            title = str(p.get("title") or p.get("name") or p.get("subject") or "(no title)")
            pid = p.get("id") or p.get("post_id") or p.get("uuid") or ""
            url = p.get("url") or (f"https://www.moltbook.com/post/{pid}" if pid else "")
            cc = p.get("comment_count")
            extra = f" (comments={cc})" if cc is not None else ""
            lines.append(f"{i}. {title}{extra}")
            if url:
                lines.append(f"   - {url}")
    lines.append("")

    lines.append("## 3) Recommended angle")
    lines.append(f"- Primary angle: **{primary['label']}**")
    lines.append(f"- Working thesis: {primary['thesis']}")
    lines.append("- Why this one: strongest overlap between current feed signals and current operating directives.")
    lines.append("")

    lines.append("## 4) Title variants")
    for t in titles:
        lines.append(f"- {t}")
    lines.append("")

    lines.append("## 5) Picked title")
    lines.append(f"- {titles[0]}")
    lines.append("")

    lines.append("## 6) TL;DR (ready to paste)")
    lines.append(f"- {primary['thesis']}")
    lines.append("- Reliability comes more from explicit operating boundaries and repeatable handoffs than from raw context accumulation alone.")
    lines.append("- Trust grows when commitments, escalation points, and follow-up behavior are visible in the workflow.")
    lines.append("")

    lines.append("## 7) Full draft (near-post-ready)")
    lines.append(body)
    lines.append("")

    lines.append("## 8) CTA variants")
    if primary["key"] == "constraints_before_memory":
        lines.append("- Which matters more in your workflows right now: larger memory, or clearer operating boundaries?")
        lines.append("- What is one constraint your agents should publish but currently hide?")
    elif primary["key"] == "proof_first":
        lines.append("- What is the smallest receipt that would make you trust an agent action more?")
        lines.append("- Which actions in your stack still rely on confidence instead of evidence?")
    elif primary["key"] == "creator_mechanics":
        lines.append("- How much of post performance is really decided in the first reply window?")
        lines.append("- Do you treat comment operations as part of publishing, or as an afterthought?")
    else:
        lines.append("- Which boring routine in your workflow has produced the most compounding value?")
        lines.append("- What loop would you automate first if continuity mattered more than speed?")
    lines.append("")

    lines.append("## 9) End matter")
    lines.append("- This post reflects an internal discussion within Aoineco & Co. (not an individual’s personal opinion).")
    lines.append("- Written by: <English name>")
    lines.append("- Reviewed by: <English name 1>, <English name 2>")
    lines.append("")

    lines.append("## 10) Benchmark bundle candidates")
    if refs:
        for r in refs:
            lines.append(f"- {r['title']} — {r['url']}")
    else:
        lines.append("- (none fetched; add manually if needed)")
    lines.append("")

    lines.append("## 11) Pre-upload checklist")
    lines.append("- [ ] Title locked")
    lines.append("- [ ] CTA locked")
    lines.append("- [ ] Writer / reviewers assigned")
    lines.append("- [ ] End matter filled")
    lines.append("- [ ] Chair approval YES received")
    lines.append("- [ ] If posted: proof bundle reported back to topic 1114")

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
