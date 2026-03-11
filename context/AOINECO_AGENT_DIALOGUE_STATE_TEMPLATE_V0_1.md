# AOINECO_AGENT_DIALOGUE_STATE_TEMPLATE_V0.1

agent-to-agent dialogue session에서 공유할 최소 상태 템플릿.

```yaml
dialogue_id: DLG-YYYYMMDD-XX
topic_id: 6062
question: ""
participants:
  - 청묘
  - 흑묘
mode: open
turn_count: 0
max_turns: 2
current_turn_owner: null
last_speaker: null
last_message_summary: ""
current_position_cheongmyo: ""
current_position_heukmyo: ""
provisional_conclusion: ""
status: open
night_mode: true
started_at_kst: "YYYY-MM-DD HH:MM"
ended_at_kst: null
```

## Notes
- `last_message_summary`는 1~3줄 요약만
- `current_position_*`은 각 에이전트 현재 입장 한 줄 요약
- `provisional_conclusion`은 잠정 합의/정리
- 밤에는 `max_turns: 2` 권장
