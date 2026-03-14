#!/usr/bin/env python3
"""Pick daily Writer/Reviewers for Moltbook with weekly non-overlap.

- Random pick from member pool
- Constraint: same person shouldn't be assigned twice in the same ISO week
- Output JSON to stdout

State file (SSOT):
  context/state/moltbook_rotation.state.json

NOTE: members list must be filled with stable identifiers (e.g., telegram @handle or canonical team id).
"""

from __future__ import annotations

import datetime as dt
import json
import random
from pathlib import Path

STATE_PATH = Path("/Users/silkroadcat/.openclaw/workspace/context/state/moltbook_rotation.state.json")
SEED_PATH = Path("/Users/silkroadcat/.openclaw/workspace/context/state/moltbook_writer_profiles.seed.json")


def iso_week_key(now_kst: dt.datetime) -> str:
    y, w, _ = now_kst.isocalendar()
    return f"{y}-W{w:02d}"


def load_seed_members() -> list[dict]:
    if not SEED_PATH.exists():
        return []
    data = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    return data.get("members", [])


def alias_map() -> dict[str, str]:
    return {
        "main": "청묘",
        "oracle": "청령",
        "comms": "청음",
        "security": "청검",
        "record": "청비",
        "builder": "청섬",
        "research": "청안",
        "analyzer": "청뇌",
        "devops": "청기",
        "growth": "청성",
        "maintainer": "청정",
        "risk": "청약",
    }


def normalize_member(name: str) -> str:
    return alias_map().get(name, name)


def load_state() -> dict:
    if not STATE_PATH.exists():
        seed_members = [m["member"] for m in load_seed_members() if m.get("externalSafe") and m.get("rotationStatus") == "available"]
        return {"version": "0.2", "weekStart": "Mon", "members": seed_members, "history": {}}
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if not state.get("members"):
        state["members"] = [m["member"] for m in load_seed_members() if m.get("externalSafe") and m.get("rotationStatus") == "available"]
    state["members"] = [normalize_member(m) for m in state.get("members", [])]
    for week_data in state.get("history", {}).values():
        for a in week_data.get("assignments", []):
            if a.get("writer"):
                a["writer"] = normalize_member(a["writer"])
            if a.get("reviewers"):
                a["reviewers"] = [normalize_member(x) for x in a.get("reviewers", [])]
    return state


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
    today = now.strftime("%Y-%m-%d")
    week = iso_week_key(now)

    state = load_state()
    members: list[str] = state.get("members") or []
    if len(members) < 3:
        raise SystemExit("moltbook_rotation.state.json: members must have >=3 entries")

    hist = state.setdefault("history", {})
    week_hist = hist.setdefault(week, {"assignments": []})
    used = set()
    for a in week_hist.get("assignments", []):
        used.update([a.get("writer"), *a.get("reviewers", [])])

    available = [m for m in members if m not in used]
    if len(available) < 3:
        # reset weekly used if pool exhausted (still deterministic rule, but avoids deadlock)
        used = set()
        available = list(members)

    random.shuffle(available)
    writer = available[0]
    reviewers = available[1:3]

    assignment = {"date": today, "writer": writer, "reviewers": reviewers}
    week_hist.setdefault("assignments", []).append(assignment)
    save_state(state)

    print(json.dumps({"week": week, **assignment}, ensure_ascii=False))


if __name__ == "__main__":
    main()
