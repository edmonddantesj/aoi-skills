#!/usr/bin/env python3
"""Topic-aware inbound execution layer prototype for Telegram topics.

Builds on existing router helpers:
- resolve_primary_agent.py
- delegation_decider.py
- delegation_state.py

Given a minimal inbound payload, produce a single execution decision with:
- mode: single | dual | silent
- owner
- secondary
- reason
- confidence
- delegate.should_delegate
- delegate.skip_reason / trigger_reason
- cooldown state

This script is deterministic and local-only. It does not call Telegram/OpenClaw APIs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path


NIGHT_START_HOUR = 23
NIGHT_END_HOUR = 8
EXPLICIT_MULTI_PATTERNS = [
    "둘이 논의해",
    "둘이 얘기해",
    "둘 다 봐",
    "둘 다 의견",
    "둘 다",
    "같이 봐",
    "보안도 같이",
]
STRATEGIC_KEYWORDS = [
    "전략",
    "방향",
    "장기",
    "수익",
    "수익화",
    "사업",
    "구조",
    "포지셔닝",
    "큰 그림",
    "왜",
    "맞나",
]
EXECUTION_KEYWORDS = [
    "실행",
    "운영",
    "정리",
    "우선순위",
    "적용",
    "도입",
    "진행",
    "구현",
    "체크",
    "테스트",
    "복구",
    "해줘",
    "다음",
    "이어",
]
LOW_VALUE_RE = re.compile(r"^(?:[\s\W]*)(?:ㅇㅋ|ok|ㅋㅋ+|굿|굳|thx|thanks|nice|알겠어|확인)(?:[\s\W]*)$", re.IGNORECASE)
BOT_NAMES = ["청묘", "흑묘", "청검", "청비", "청기", "청성", "청안", "청령", "청정", "청섬", "청뇌"]


def _find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "context" / "telegram_topics").exists():
            return parent
    return here.parents[4]


ROOT = _find_root()
TOPICS_DIR = ROOT / "context" / "telegram_topics"
TOPIC_MAP_PATH = TOPICS_DIR / "thread_topic_map.json"
AGENT_MAP_PATH = TOPICS_DIR / "thread_agent_map.json"
RUNTIME_DIR = TOPICS_DIR / "runtime" / "inbound_execution_layer"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_payload(arg: str | None) -> dict:
    if arg:
        return json.loads(arg)
    raw = sys.stdin.read()
    return json.loads(raw) if raw.strip() else {}


def _slug_for_thread(thread_id: int | None) -> str | None:
    if thread_id is None or not TOPIC_MAP_PATH.exists():
        return None
    data = _load_json(TOPIC_MAP_PATH)
    for slug, mapped in data.items():
        if str(mapped) == str(thread_id):
            return slug
    return None


def _agent_entry(slug: str | None) -> dict:
    if not slug or not AGENT_MAP_PATH.exists():
        return {}
    data = _load_json(AGENT_MAP_PATH)
    entry = data.get(slug)
    return entry if isinstance(entry, dict) else {}


def _is_night(hour: int | None) -> bool:
    if hour is None:
        return False
    return hour >= NIGHT_START_HOUR or hour < NIGHT_END_HOUR


def _contains_any(text: str, keywords: list[str]) -> bool:
    low = text.lower()
    return any(kw.lower() in low for kw in keywords)


def _detect_direct_tag(text: str) -> str | None:
    for name in BOT_NAMES:
        if name in text:
            return name
    return None


def _detect_explicit_multi(text: str) -> bool:
    return _contains_any(text, EXPLICIT_MULTI_PATTERNS)


def _classify_text(text: str) -> tuple[bool, bool]:
    strategic = _contains_any(text, STRATEGIC_KEYWORDS)
    execution = _contains_any(text, EXECUTION_KEYWORDS)
    return strategic, execution


def _confidence(base: float) -> float:
    return max(0.0, min(0.99, round(base, 2)))


def decide(payload: dict) -> dict:
    text = (payload.get("text") or "").strip()
    text_norm = re.sub(r"\s+", " ", text)
    thread_id = payload.get("message_thread_id")
    reply_target = payload.get("reply_target_agent")
    hour = payload.get("local_hour")
    now = int(time.time())

    slug = _slug_for_thread(thread_id)
    entry = _agent_entry(slug)
    primary = entry.get("primary")
    collaborators = entry.get("collaborators", [])
    night = _is_night(hour)

    decision = {
        "ok": True,
        "schema": "openclaw.telegram.inbound_execution_decision.v0_1",
        "timestamp": now,
        "thread_id": thread_id,
        "slug": slug,
        "text_norm": text_norm,
        "mode": None,
        "owner": None,
        "secondary": None,
        "reason": None,
        "confidence": None,
        "delegate": {
            "should_delegate": False,
            "trigger_reason": None,
            "skip_reason": None,
        },
        "context": {
            "primary": primary,
            "collaborators": collaborators,
            "reply_target_agent": reply_target,
            "night": night,
        },
    }

    if not text_norm:
        decision["mode"] = "silent"
        decision["reason"] = "empty_message"
        decision["confidence"] = _confidence(0.99)
        decision["delegate"]["skip_reason"] = "empty_message"
        return decision

    if LOW_VALUE_RE.match(text_norm):
        decision["mode"] = "silent"
        decision["reason"] = "low_value_reaction"
        decision["confidence"] = _confidence(0.97)
        decision["delegate"]["skip_reason"] = "low_value_reaction"
        return decision

    tagged = _detect_direct_tag(text_norm)
    if tagged:
        decision["mode"] = "single"
        decision["owner"] = tagged
        decision["reason"] = "direct_tag"
        decision["confidence"] = _confidence(0.98)
        decision["delegate"]["should_delegate"] = tagged == primary or tagged in collaborators
        decision["delegate"]["trigger_reason"] = "direct_tag"
        return decision

    if reply_target:
        decision["mode"] = "single"
        decision["owner"] = reply_target
        decision["reason"] = "reply_target"
        decision["confidence"] = _confidence(0.97)
        decision["delegate"]["should_delegate"] = True
        decision["delegate"]["trigger_reason"] = "reply_target"
        return decision

    strategic, execution = _classify_text(text_norm)

    if _detect_explicit_multi(text_norm):
        owner = "흑묘" if strategic and not execution else (primary or "청묘")
        secondary = (primary or "청묘") if owner == "흑묘" else ("흑묘" if "흑묘" in collaborators else None)
        if night and not strategic and not execution:
            decision["mode"] = "single"
            decision["owner"] = primary or owner
            decision["reason"] = "night_single_bias_on_explicit_multi"
            decision["confidence"] = _confidence(0.74)
        else:
            decision["mode"] = "dual"
            decision["owner"] = owner
            decision["secondary"] = secondary
            decision["reason"] = "explicit_multi_call"
            decision["confidence"] = _confidence(0.93 if not night else 0.86)
        decision["delegate"]["should_delegate"] = True
        decision["delegate"]["trigger_reason"] = "explicit_multi_call"
        return decision

    if strategic and execution:
        if night:
            decision["mode"] = "single"
            decision["owner"] = primary or "청묘"
            decision["reason"] = "mixed_intent_night_single_bias"
            decision["confidence"] = _confidence(0.72)
        else:
            decision["mode"] = "dual"
            decision["owner"] = "흑묘" if "흑묘" in collaborators else (primary or "청묘")
            decision["secondary"] = primary or "청묘"
            decision["reason"] = "mixed_intent_dual"
            decision["confidence"] = _confidence(0.84)
        decision["delegate"]["should_delegate"] = True
        decision["delegate"]["trigger_reason"] = decision["reason"]
        return decision

    if execution:
        decision["mode"] = "single"
        decision["owner"] = primary or "청묘"
        decision["reason"] = "execution_weighted_single_owner"
        decision["confidence"] = _confidence(0.88)
        decision["delegate"]["should_delegate"] = True
        decision["delegate"]["trigger_reason"] = "execution_keyword"
        return decision

    if strategic:
        decision["mode"] = "single"
        decision["owner"] = "흑묘" if "흑묘" in collaborators else (primary or "청묘")
        decision["reason"] = "strategic_weighted_single_owner"
        decision["confidence"] = _confidence(0.87)
        decision["delegate"]["should_delegate"] = True
        decision["delegate"]["trigger_reason"] = "strategic_keyword"
        return decision

    if night:
        decision["mode"] = "silent"
        decision["reason"] = "night_low_signal_silent"
        decision["confidence"] = _confidence(0.8)
        decision["delegate"]["skip_reason"] = "night_low_signal_silent"
        return decision

    decision["mode"] = "single"
    decision["owner"] = primary or "청묘"
    decision["reason"] = "default_primary_fallback"
    decision["confidence"] = _confidence(0.61)
    decision["delegate"]["should_delegate"] = "?" in text_norm or len(text_norm) >= 12
    if decision["delegate"]["should_delegate"]:
        decision["delegate"]["trigger_reason"] = "default_primary_fallback"
    else:
        decision["delegate"]["skip_reason"] = "low_signal_fallback"
    return decision


def persist_decision(decision: dict, chat_id: str | None) -> Path:
    thread_id = decision.get("thread_id") or "unknown"
    thread_dir = RUNTIME_DIR / f"thread_{thread_id}"
    latest_dir = thread_dir / "latest"
    runs_dir = thread_dir / "runs"
    run_key = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(decision["timestamp"]))
    run_dir = runs_dir / run_key
    run_dir.mkdir(parents=True, exist_ok=True)
    latest_dir.mkdir(parents=True, exist_ok=True)

    enriched = dict(decision)
    enriched["chat_id"] = chat_id
    enriched["run_key"] = run_key
    data = json.dumps(enriched, indent=2, ensure_ascii=False) + "\n"
    (run_dir / "decision.json").write_text(data, encoding="utf-8")
    (latest_dir / "decision.json").write_text(data, encoding="utf-8")
    return run_dir / "decision.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="Inbound JSON payload")
    ap.add_argument("--persist", action="store_true", help="Persist decision artifact under runtime/")
    args = ap.parse_args()

    payload = _load_payload(args.json)
    decision = decide(payload)
    if args.persist:
        decision_path = persist_decision(decision, payload.get("chat_id"))
        decision["decision_path"] = str(decision_path)
    print(json.dumps(decision, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
