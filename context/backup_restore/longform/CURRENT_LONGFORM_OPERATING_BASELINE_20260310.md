# CURRENT_LONGFORM_OPERATING_BASELINE_20260310

status: current-operating-baseline
basis: live local SSOT + restore decision consolidation
updated: 2026-03-10
owner: 청비

## purpose
이 문서는 longform 운영에 대한 **현행 기준선(single-page baseline)** 이다.
과거 transcript/restore 메모에 나온 주장과, 현재 워크스페이스에서 실제로 살아있는 SSOT 경로를 분리해서 정리한다.

핵심 원칙:
1. A = current-topic truth
2. B = upstream-context proposal-only
3. live SSOT = 현재 경로/현재 존재 여부의 최종 판정자

---

## current canonical facts

### 1) topic routing
- `longform = 65`
- live path: `context/telegram_topics/thread_topic_map.json`

### 2) lane meaning
- `longform = longform ingest + summary + SSOT packaging`
- live path: `context/telegram_topics/TOPICS_DEFINITION_V0_1.md`

### 3) ownership
- `longform.primary = 청비`
- collaborators: `청안`
- live path: `context/telegram_topics/thread_agent_map.json`

### 4) canonical notion destination
- canonical DB: `📥 Reference Inbox (PDF/Longform)`
- datasource id: `1efd4236-bb3f-4b99-86e1-10a766213439`
- live path: `context/notion/NOTION_DB_ROUTING_AND_PAGE_TEMPLATE_POLICY_V0_1.md`

### 5) required longform page fill
longform row/page는 아래 내용을 채우는 방향으로 운영한다.
- Source
- One-liner
- Why it matters to AOI
- SSOT links
- Artifacts
- Next actions

live path:
- `context/notion/NOTION_DB_ROUTING_AND_PAGE_TEMPLATE_POLICY_V0_1.md`

### 6) storage strength / retention
- longform 저장 강도는 `S/A/B/C` triage를 따른다.
- 요약:
  - `S/A`: local fulltext 유지 + Notion은 summary + source
  - `B`: local fulltext 없이 thick-bullet summary
  - `C`: 필요 시 link only

live path:
- `context/notion/NOTION_DB_ROUTING_AND_PAGE_TEMPLATE_POLICY_V0_1.md`

### 7) restore / promotion safety
복원/승격은 아래 원칙을 따른다.
- proof-first
- no overwrite in phase A
- patch-only promotion
- explicit conflict marking

live path:
- `context/ops/DM_EXPORT_SHADOW_INGEST_AND_SAFE_PROMOTION_POLICY_V0_1.md`

### 8) external posting rule
- 외부 포스팅/대외 발행은 approval-gated로 취급한다.
- 이 원칙 자체는 운영 기준으로 유지하되, 이를 직접 규정하던 과거 runbook 파일 경로는 현재 live 검증이 안 된 것도 있다.

---

## practical operating baseline

현재 기준으로 longform 운영을 한 줄씩 풀면 이렇게 읽는다.

1. `longform` 토픽은 65번이다.
2. 역할은 `longform ingest + summary + SSOT packaging` 이다.
3. canonical DB는 `📥 Reference Inbox (PDF/Longform)` 이다.
4. longform row/page는 source / one-liner / why it matters / SSOT links / artifacts / next actions 를 채운다.
5. 저장 강도는 `S/A/B/C` triage를 따른다.
6. 복원/승격은 proof-first / no-overwrite / patch-only / explicit-conflict 로 처리한다.
7. historical naming보다 현재 살아있는 SSOT 경로를 우선한다.

---

## deprecated or non-live historical paths
아래 파일명들은 transcript/restore 문맥에 등장했지만, **2026-03-10 live check 기준 현재 워크스페이스에서 존재가 확인되지 않았다.**
따라서 “예전에 이런 이름이 있었다”와 “지금도 현행 SSOT다”를 분리해서 취급해야 한다.

### missing in current workspace
- `context/PDF_LONGFORM_INGEST_SOP_V0_1.md`
- `context/CONTENT_INGEST_TO_POST_APPROVAL_SOP_V0_1.md`
- `context/PLATFORM_POSTING_RUNBOOK.md`

### handling rule for those paths
- historical reference로는 보존 가능
- current SSOT로 자동 승격하지 않음
- 동일 규칙이 살아있다면 **현재 존재하는 파일 경로**에 매핑해서 복원
- old filename을 아무 근거 없이 “계속 살아있던 canonical”처럼 취급하지 않음

---

## restore mapping rule
historical rule이 transcript에는 강하게 남아 있어도, 복원 시에는 아래 순서를 따른다.

1. 현재 live SSOT 파일이 있는지 확인
2. 있으면 그 경로를 canonical로 채택
3. 없으면 proposal-only 또는 verify-then-promote 로 유지
4. 충돌 시 `CONFLICT/CHOICE` 로 명시

예시:
- 과거의 `PDF_LONGFORM_INGEST_SOP_V0_1.md` 주장은,
  현재는 아래 live 문서 조합으로 대체 해석한다.
  - `context/notion/NOTION_DB_ROUTING_AND_PAGE_TEMPLATE_POLICY_V0_1.md`
  - `context/telegram_topics/TOPICS_DEFINITION_V0_1.md`
  - `context/telegram_topics/thread_topic_map.json`
  - `context/ops/DM_EXPORT_SHADOW_INGEST_AND_SAFE_PROMOTION_POLICY_V0_1.md`

---

## verify-then-promote list
아직 추가 검증이 필요한 포인트:
- 옛 `PDF_LONGFORM_INGEST_SOP_V0_1.md` 를 완전히 대체하는 surviving current doc가 더 있는지
- surviving platform posting runbook/script/proof bundle tooling 이 실제로 남아 있는지
- current Notion DB 의 historical longform row/page 품질이 기대 수준인지
- longform → inbox-dev / ralph-loop 라우팅이 자동화인지 정책 레벨인지
- attribution/title/tone 관련 세부 규칙이 현행 runbook에 살아 있는지

---

## source set
- `context/backup_restore/longform/LIVE_SSOT_COMPARE_LONGFORM_20260310.md`
- `context/backup_restore/longform/RESTORE_DECISION_LONGFORM_20260310.md`
- `context/telegram_topics/thread_topic_map.json`
- `context/telegram_topics/TOPICS_DEFINITION_V0_1.md`
- `context/telegram_topics/thread_agent_map.json`
- `context/notion/NOTION_DB_ROUTING_AND_PAGE_TEMPLATE_POLICY_V0_1.md`
- `context/ops/DM_EXPORT_SHADOW_INGEST_AND_SAFE_PROMOTION_POLICY_V0_1.md`

---

## one-line summary
이제 longform은 “무엇을 복원할지”보다, **무엇을 현행 기준으로 인정할지**가 정리된 상태다.