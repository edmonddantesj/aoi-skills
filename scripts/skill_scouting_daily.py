#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
TZ = dt.timezone(dt.timedelta(hours=9))
NOW = dt.datetime.now(TZ)
DAY = NOW.strftime("%Y-%m-%d")
REPORT_DIR = ROOT / "ops" / "reports" / "skill_scouting" / "daily"
DECISION_DIR = ROOT / "context" / "skill_scouting" / "decisions"
INBOX_DIR = ROOT / "context" / "skill_scouting" / "inbox"
ART_DIR = ROOT / "artifacts" / "skill_scouting"

CHAT_ID = "-1003732040608"
THREAD_ID = "77"

UTILITY_KEYWORDS = {
    "ops": 4,
    "monitor": 4,
    "monitoring": 4,
    "alert": 4,
    "automation": 5,
    "workflow": 4,
    "sync": 3,
    "dashboard": 3,
    "research": 4,
    "market": 4,
    "finance": 4,
    "stock": 3,
    "crypto": 3,
    "memory": 4,
    "knowledge": 4,
    "mcp": 5,
    "browser": 3,
    "scrape": 2,
    "search": 3,
    "data": 4,
    "api": 3,
    "proof": 3,
    "kanban": 3,
    "quality": 3,
    "security": 4,
}

RISK_KEYWORDS = {
    "wallet": 4,
    "onchain": 5,
    "sign": 4,
    "swap": 5,
    "bridge": 5,
    "bet": 5,
    "trade": 4,
    "trading": 4,
    "deploy": 3,
    "delete": 4,
    "publish": 3,
    "exec": 2,
    "shell": 2,
    "token": 2,
    "secret": 3,
}


def sh(cmd: list[str], timeout: int = 60) -> tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def norm_slug(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9._-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-._")
    return s[:80] or "item"


def score_text(text: str) -> tuple[int, int, list[str], list[str]]:
    t = text.lower()
    util = 0
    risk = 0
    util_hits: list[str] = []
    risk_hits: list[str] = []
    for k, v in UTILITY_KEYWORDS.items():
        if k in t:
            util += v
            util_hits.append(k)
    for k, v in RISK_KEYWORDS.items():
        if k in t:
            risk += v
            risk_hits.append(k)
    return util, risk, util_hits[:5], risk_hits[:5]


def _extract_json(text: str) -> Any:
    start = text.find('{')
    if start == -1:
        raise ValueError('json payload not found')
    return json.loads(text[start:])


def clawhub_explore(sort: str, limit: int = 25) -> list[dict[str, Any]]:
    rc, out, err = sh(["clawhub", "explore", "--sort", sort, "--limit", str(limit), "--json"], timeout=90)
    if rc != 0:
        raise RuntimeError(f"clawhub explore {sort} failed: {err.strip()}")
    data = _extract_json(out)
    if isinstance(data, dict) and isinstance(data.get('items'), list):
        return data['items']
    if isinstance(data, list):
        return data
    return []


def gh_search(query: str, limit: int = 20) -> list[dict[str, Any]]:
    cmd = [
        "gh", "search", "repos", query,
        "--limit", str(limit),
        "--json", "name,owner,description,url,updatedAt,stargazersCount"
    ]
    rc, out, err = sh(cmd, timeout=90)
    if rc != 0:
        raise RuntimeError(f"gh search failed: {err.strip()}")
    return json.loads(out)


def build_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []

    for sort in ("trending", "newest"):
        for row in clawhub_explore(sort, 20):
            text = f"{row.get('displayName','')} {row.get('summary','')} {' '.join(row.get('tags',{}).keys())}"
            util, risk, util_hits, risk_hits = score_text(text)
            candidates.append({
                "source": f"clawhub:{sort}",
                "slug": row.get("slug"),
                "name": row.get("displayName") or row.get("slug"),
                "summary": row.get("summary", ""),
                "url": f"https://clawhub.com/skills/{row.get('slug')}",
                "install": f"clawhub install {row.get('slug')}",
                "utility": util + min(int((row.get("stats") or {}).get("downloads", 0) / 100), 3),
                "risk": risk,
                "util_hits": util_hits,
                "risk_hits": risk_hits,
            })

    gh_queries = [
        'openclaw agent automation OR mcp in:name,description,readme pushed:>2026-02-01',
        'agent workflow monitoring dashboard proof in:name,description,readme pushed:>2026-02-01',
    ]
    for q in gh_queries:
        for row in gh_search(q, 15):
            text = f"{row.get('name','')} {row.get('description','')}"
            util, risk, util_hits, risk_hits = score_text(text)
            owner = (row.get("owner") or {}).get("login") or "owner"
            candidates.append({
                "source": "github",
                "slug": norm_slug(f"{owner}-{row.get('name','repo')}"),
                "name": f"{owner}/{row.get('name')}",
                "summary": row.get("description") or "",
                "url": row.get("url"),
                "install": f"gh repo clone {owner}/{row.get('name')}",
                "utility": util + min(int((row.get("stargazersCount") or 0) / 50), 4),
                "risk": risk,
                "util_hits": util_hits,
                "risk_hits": risk_hits,
            })
    return candidates


def route(item: dict[str, Any]) -> str:
    # Safe-ish default: ADOPT only when clearly useful and not obviously risky.
    if item["risk"] >= 7:
        return "HOLD"
    if item["utility"] >= 10 and item["risk"] <= 3:
        return "ADOPT"
    if item["utility"] >= 8:
        return "REBUILD"
    return "HOLD"


def choose_top(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dedup: dict[str, dict[str, Any]] = {}
    for c in candidates:
        key = c["url"] or c["name"]
        if key not in dedup or (c["utility"] - c["risk"]) > (dedup[key]["utility"] - dedup[key]["risk"]):
            dedup[key] = c
    pool = list(dedup.values())
    for c in pool:
        c["route"] = route(c)
        c["score"] = c["utility"] - c["risk"]
    pool.sort(key=lambda x: (x["score"], x["utility"]), reverse=True)

    top: list[dict[str, Any]] = []
    have_github = 0
    have_clawhub = 0
    for c in pool:
        if len(top) >= 5:
            break
        if c["source"].startswith("clawhub") and have_clawhub >= 3:
            continue
        if c["source"] == "github" and have_github >= 2:
            continue
        top.append(c)
        have_github += int(c["source"] == "github")
        have_clawhub += int(c["source"].startswith("clawhub"))
    return top


def ensure_pack(item: dict[str, Any]) -> pathlib.Path:
    slug = norm_slug(item["slug"])
    pack = ROOT / "context" / "adoption" / f"{DAY}_{slug}_ADOPTION_PACK_V0_1"
    pack.mkdir(parents=True, exist_ok=True)

    (pack / "00_intake.json").write_text(json.dumps({
        "date": DAY,
        "slug": slug,
        "source": item["source"],
        "name": item["name"],
        "url": item["url"],
        "install_hint": item["install"],
        "auto_started_by": "skill_scouting_daily.py",
        "route": item["route"],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    files = {
        "10_license_and_security.md": f"# license + security\n\n- status: STARTED\n- source: {item['url']}\n- route: {item['route']}\n- initial utility/risk: {item['utility']}/{item['risk']}\n- utility hits: {', '.join(item['util_hits']) or '(none)'}\n- risk hits: {', '.join(item['risk_hits']) or '(none)'}\n",
        "20_creator_contact.md": f"# creator contact\n\n- source url: {item['url']}\n- status: TBD (auto-created by scout loop)\n",
        "30_rebuild_plan.md": f"# rebuild plan\n\n- route: {item['route']}\n- why: {item['summary']}\n- initial plan: local review -> guardrails -> adoption decision\n",
        "40_install_proof.md": "# install proof\n\n- status: NOT_STARTED\n- note: daily scout only started the adoption pack; installation is a later step after review.\n",
    }
    for name, body in files.items():
        p = pack / name
        if not p.exists():
            p.write_text(body, encoding="utf-8")
    return pack


def write_decision(item: dict[str, Any], pack: pathlib.Path | None) -> pathlib.Path:
    DECISION_DIR.mkdir(parents=True, exist_ok=True)
    p = DECISION_DIR / f"{DAY}_{norm_slug(item['slug'])}_DECISION.md"
    body = [
        f"# {item['name']} — {item['route']}",
        "",
        f"- date: {DAY}",
        f"- source: {item['source']}",
        f"- url: {item['url']}",
        f"- utility: {item['utility']}",
        f"- risk: {item['risk']}",
        f"- install hint: `{item['install']}`",
        "",
        "## Why",
        f"- {item['summary']}",
        f"- business fit hits: {', '.join(item['util_hits']) or '(none)'}",
        f"- risk hits: {', '.join(item['risk_hits']) or '(none)'}",
        "",
        "## Next",
        f"- route = {item['route']}",
    ]
    if pack:
        body.append(f"- adoption pack started: `{pack.relative_to(ROOT)}`")
    p.write_text("\n".join(body) + "\n", encoding="utf-8")
    return p


def render_report(top: list[dict[str, Any]], evidence: list[str], packs: dict[str, pathlib.Path]) -> pathlib.Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ART_DIR.mkdir(parents=True, exist_ok=True)
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    report = REPORT_DIR / f"REPORT_{DAY}.md"
    lines = [
        f"# Daily Skill Scouting Report — {DAY}",
        "",
        f"- generated: {NOW.strftime('%Y-%m-%d %H:%M KST')}",
        "- scope: morning ClawHub + GitHub scouting, Top 5 only",
        "- policy: maintainers auto-review L1/L2 candidates; L3/obvious-risk stays HOLD",
        "",
        "## Evidence from Telegram export (why this loop exists)",
    ]
    lines += [f"- {e}" for e in evidence]
    lines.append("")
    lines.append("## Top 5")
    lines.append("")
    for i, item in enumerate(top, 1):
        lines += [
            f"### {i}. {item['name']} [{item['route']}]"
        ]
        lines += [
            f"- source: {item['source']}",
            f"- summary: {item['summary']}",
            f"- url: {item['url']}",
            f"- install/ref: `{item['install']}`",
            f"- utility/risk/score: {item['utility']}/{item['risk']}/{item['score']}",
            f"- business-fit hits: {', '.join(item['util_hits']) or '(none)'}",
            f"- risk hits: {', '.join(item['risk_hits']) or '(none)'}",
        ]
        if item['route'] in ('ADOPT', 'REBUILD') and item['slug'] in packs:
            lines.append(f"- adoption pack: `{packs[item['slug']].relative_to(ROOT)}`")
        lines.append("")

    report.write_text("\n".join(lines), encoding="utf-8")
    return report


def send_summary(top: list[dict[str, Any]], report: pathlib.Path) -> None:
    parts = [f"Daily skill scouting — {DAY} ({NOW.strftime('%H:%M KST')})", "", "Top 5"]
    for i, item in enumerate(top, 1):
        parts.append(f"{i}. {item['name']} — {item['route']} — {item['summary'][:110]}")
        parts.append(f"   ref: {item['install']}")
    parts += ["", f"Proof: {report}"]
    msg = "\n".join(parts)
    sh([
        "openclaw", "message", "send",
        "--channel", "telegram",
        "--target", CHAT_ID,
        "--thread-id", THREAD_ID,
        "--message", msg,
        "--silent",
    ], timeout=60)


def main() -> int:
    evidence = [
        "messages10.html:12209 / 12225 — 오전 ClawHub 순찰 결과 5개를 ‘사업적 엣지 + 설치 힌트’ 형식으로 보고",
        "messages14.html:12363 — ‘클로헙 정찰 결과 바로 쓸만한 후보 5개’ 패턴 확인",
        "messages15.html:22827 — ‘ClawHub 리서치 결과 5개’ + 설치 커맨드 요약 패턴 확인",
        "messages11.html:5731 / 5763 — 정찰 후보는 내부검토 후 Adopt/Rebuild/Reject 결론으로 자동 착수 정책 확인",
    ]

    candidates = build_candidates()
    top = choose_top(candidates)
    if not top:
        print("No candidates found")
        return 2

    packs: dict[str, pathlib.Path] = {}
    for item in top:
        pack = None
        if item["route"] in ("ADOPT", "REBUILD"):
            pack = ensure_pack(item)
            packs[item['slug']] = pack
        write_decision(item, pack)

    report = render_report(top, evidence, packs)
    send_summary(top, report)
    print(str(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
