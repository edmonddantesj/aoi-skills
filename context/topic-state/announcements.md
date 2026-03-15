# Topic State — announcements

- Topic: `announcements`
- Telegram topic id: `32`
- Status: PAUSED
- Last saved: 2026-03-16 08:29 KST

## Current objective
- 외부 공지/발행성 작업의 승인 게이트와 산출 흐름을 추후 재개 가능하게 보관한다.

## Latest checkpoint
- 2026-03-16: 청뇌 에스컬레이션을 받아, 승인된 L1/L2 작업을 `원하면`식 문장으로 되돌리거나 STATUS 뒤 실제 실행/아티팩트 없이 멈추는 패턴을 전사 운영 위반으로 고정하는 공지 초안을 작성했다.
- Canonical policy drafted: `context/ops/EXECUTION_CONTINUITY_AND_NO_RESPONSIBILITY_BOUNCE_POLICY_V0_1.md`
- Announcement draft created: `context/telegram_topics/ANNOUNCEMENTS_DRAFT_2026-03-16_EXECUTION_CONTINUITY_AND_NO_RESPONSIBILITY_BOUNCE.md`
- 커뮤니티 Auto-Archive의 Live-Sync 원칙상, 게시 후 최종 URL을 활동 로그에 남기는 것이 장기 규칙이다. Source: MEMORY.md#L28-L31

## Decisions locked
- 외부 게시/공지성 작업은 기본적으로 승인 전제.
- 최종 게시 후 URL 증빙을 남긴다.
- paused 토픽은 재개 조건을 명확히 적는다.

## Next actions
1. announcements 발행면에 위 공지 초안 게시.
2. 재발 패턴이 나온 topic은 playbook/state/handoff 중 최소 1곳에 위반 로그와 재발방지 조치를 기록.
3. escalation intake lane 사용을 시작하고 ACTIVE 항목 triage 루틴을 정한다.

## Key files
- Playbook: `context/topics/announcements_PLAYBOOK_V0_1.md`
- Handoff: (없음)
- Topic map: `context/telegram_topics/thread_topic_map.json`

## Restore instructions
- 먼저 이 파일을 읽고, 실제 내용이 얇으면 Playbook과 관련 HF를 최소만 추가로 읽는다.
- 복구 응답은 `현재 목표 / 마지막 체크포인트 / 다음 액션` 순서로 짧게 재구성한다.

## Notes
- announcements는 비활성이어도 승인/증빙 규칙만은 잊지 않게 남겨두는 토픽이다.
