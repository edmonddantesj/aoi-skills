#!/usr/bin/env python3
"""Delegation decider (execution layer building block).

Given an inbound message payload (minimal fields), decide whether to auto-delegate
under Delegation Policy v0.1 (MODE B).

This script is deterministic and does NOT talk to Telegram/OpenClaw directly.
It is intended to be embedded into a higher-level router that receives inbound updates.

Input (JSON via --json or stdin):
  {
    "chat_id": "telegram:-100...",
    "message_thread_id": 38,
    "message_id": 123,
    "text": "..."
  }

Output:
  {
    "ok": true,
    "should_delegate": true|false,
    "reason": "trigger:question_mark"|"skip:reaction"|...,
    "thread_id": 38,
    "text_norm": "..."
  }
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass


REACTION_ONLY = re.compile(r"^(?:[\s\W]*)(?:ㅇㅋ|ok|ㅋㅋ+|굿|굳|thx|thanks|nice)(?:[\s\W]*)$", re.IGNORECASE)

TRIGGER_KEYWORDS = [
    # Korean
    "어떻게",
    "왜",
    "가능",
    "해줘",
    "도와",
    "해결",
    "결정",
    "해야",
    "오류",
    "에러",
    "로그",
    # English
    "todo",
    "next",
    "fix",
    "implement",
    "debug",
    "error",
    "stack",
    "trace",
    "fail",
    "exception",
]


@dataclass
class Decision:
    should_delegate: bool
    reason: str
    text_norm: str


def decide(text: str) -> Decision:
    t = (text or "").strip()
    t_norm = re.sub(r"\s+", " ", t)

    if not t_norm:
        return Decision(False, "skip:empty", t_norm)

    if REACTION_ONLY.match(t_norm):
        return Decision(False, "skip:reaction_only", t_norm)

    # Hard triggers
    if "?" in t_norm:
        return Decision(True, "trigger:question_mark", t_norm)

    # Link trigger
    if re.search(r"https?://", t_norm):
        return Decision(True, "trigger:link", t_norm)

    # Code fence
    if "```" in t_norm:
        return Decision(True, "trigger:code_fence", t_norm)

    low = t_norm.lower()
    for kw in TRIGGER_KEYWORDS:
        if kw.lower() in low:
            return Decision(True, f"trigger:keyword:{kw}", t_norm)

    return Decision(False, "skip:no_signal", t_norm)


def _load_json(arg: str | None) -> dict:
    if arg:
        return json.loads(arg)
    raw = sys.stdin.read()
    return json.loads(raw) if raw.strip() else {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="Inbound JSON payload")
    args = ap.parse_args()

    payload = _load_json(args.json)
    text = payload.get("text", "")
    d = decide(text)

    out = {
        "ok": True,
        "should_delegate": d.should_delegate,
        "reason": d.reason,
        "thread_id": payload.get("message_thread_id"),
        "text_norm": d.text_norm,
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
