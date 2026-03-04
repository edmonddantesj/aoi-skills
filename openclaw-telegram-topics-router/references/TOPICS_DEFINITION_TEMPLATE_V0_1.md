# Telegram Forum Topics — Definition v0.1 (Template)

Goal: Topic별 대화/저장/자동화 룰을 가볍게 고정해서, 멘션 없이(always-on) 대화해도 자동 분류 + 올바른 행동을 하게 한다.

## Global rules (applies to all topics)
- Session routing key: `chat_id + message_thread_id`
- Storage: SSOT는 그대로 유지. 모든 레코드에 `topic=<topic_slug>` 태그 추가.
- Proof-first: 작업 결과는 가능한 한 파일 경로/로그/링크로 증빙.

---

## announcements
- 목적: 공지/결정/고정 링크.

## ops
- 목적: 서버/크론/게이트웨이/장애 대응.

## maintenance
- 목적: 리그레션/정리/의존성 업데이트/잡다한 수리.

## adp
- 목적: ADP 대시보드(UI/데이터/배포) 관련.

## acp
- 목적: ACP 연동/잡 실행/마켓플레이스 에이전트.

## bazaar
- 목적: NEXUS Bazaar / The Archive 상품화/리스트/스캔/레지스트리.

## github
- 목적: 외부 GitHub 소스 인입 → 분석 → ‘도입해줘’ 루트 전환.

## longform
- 목적: 장문/문서/PDF/DOCX/대화 덤프 인입.

## ralph-loop
- 목적: WIP 제한 기반의 실행 루프(작은 작업 빠르게 Done).

## hackathons
- 목적: 해커톤/대회 인입/트래킹/제출 패키징(SOP).

## inbox-dev
- 목적: 개발 인입/이관/트리아지 허브. 어디 토픽인지 애매하면 일단 여기.

## handoff
- 목적: 결정/컨텍스트/다음 액션 박제(토픽 이동 시 끊김 방지).

## random
- 목적: 애매한 대화/임시 메모/잡담.

---

## Calibration procedure (one-time)
- 각 토픽에서 1회: `ping` 같은 아무 메시지나 전송
- 그 메시지의 `message_thread_id`(=topic_id)를 확인해 `thread_topic_map.json`에 등록
