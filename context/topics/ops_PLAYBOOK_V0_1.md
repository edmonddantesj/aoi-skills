# ops PLAYBOOK V0.1

- **Purpose:** Mac mini/OpenClaw 운영(게이트웨이/launchd/cron/백업/드리프트) + 운영 규칙을 SSOT로 고정
- **Last updated:** 2026-03-08

## Imported from DM export (Shadow Ingest)
> Proof-first. 아래 항목은 DM export에서 확인된 반복 패턴/요청을 토픽 운영 SSOT로 승격한 초안.

### Recurring tasks (Top N)
1) **Notion에 “장기적으로 잊으면 안 되는 것” 기록(학습/복구 목적)**
- Rule: 중요한 원칙/결정/장기 메모리성 정보는 Notion에 기록해서, 이후 필요할 때만 조회(토큰 절약).
- Proof: DM export `messages.html` msgId=26

2) **Daily Report / Digest 주기작업(토큰 사용량 측정 포함) — 먼저 1회 테스트 후 정기화**
- Rule: 새 주기 작업은 먼저 1회 테스트로 토큰/효율 검증 후 고정 스케줄 결정.
- Proof: DM export `messages.html` msgId=28~29 ("Daily Report Cron… 토큰 사용량")

3) **Gateway 상태/성능 저하 감지 → 선보고 후조치**
- Rule: 느려짐/불안정 징후 시 원인 분석 시작, 재시작/모델전환 필요하면 먼저 승인 요청.
- Proof: DM export `messages.html` msgId=123747

4) **Notion 연동 장애 대응(권한 OK인데 반영 안 됨 / 유령 DB / env 불일치 등)**
- Rule: ‘성공했다고 말만’ 하지 말고, DB ID/워크스페이스/실행 컨텍스트 env를 증빙으로 맞춘 뒤 조치.
- Proof: DM export `messages.html` msgId=163, 266 (장애 사후 분석/게이트웨이 재시작 루프)

5) **"현재를 저장" (SAVE NOW) 스냅샷 루틴 상시 유지**
- Rule: 큰 변경/불안정 조치 후에는 스냅샷으로 상태를 박제.
- Proof: 현 세션에서 SAVE NOW 실행 + GitHub release 증빙 다수(별도 SSOT: `context/ops/SAVE_NOW_PROTOCOL_V0_1.md`)

### Automation candidates (ops)
- Daily/3h digest류는 launchd(plist)로 고정 주기 운영, 실패 시 알림.
- 대량 백로그 처리/triage류는 Ralph Loop로 라우팅.
- 재시작/장애 후 복귀 시에는 death-aware recovery scan을 통해 중단된 토픽 미션 및 누락 공지를 확인.

## Where to record
- 진행중 작업: `context/handoff/INDEX.md` + 개별 HF
- 운영 규칙/반복업무: 이 Playbook + `context/ops/*` SSOT

## Heukmyo support routing
- 운영 체크리스트 초안, 장애 triage 정리, 복구/점검 문서화가 필요할 때는 `context/heukmyo-squad/CHEONGMYO_HEUKMYO_SUPPORT_PROTOCOL_ONEPAGE_V0_1.md` 기준으로 요청을 구조화한다.
- Canonical policy source lives in `context/heukmyo-squad/playbook/` (GitHub canonical docs).
- Workspace-local operating references for ops are:
  - `context/heukmyo-squad/CHEONGMYO_HEUKMYO_SUPPORT_PROTOCOL_ONEPAGE_V0_1.md`
  - `context/heukmyo-squad/CHEONGMYO_HEUKMYO_SUPPORT_PROTOCOL_EXAMPLES_V0_1.md`
- For technical/ops requests, add optional extension fields when useful:
  - `Affected scope`
  - `Failure mode`
- 재시작/모델 전환/서비스 변경은 human gate로 남긴다.
UKMYO_SUPPORT_PROTOCOL_ONEPAGE_V0_1.md`
  - `context/heukmyo-squad/CHEONGMYO_HEUKMYO_SUPPORT_PROTOCOL_EXAMPLES_V0_1.md`
- For technical/ops requests, add optional extension fields when useful:
  - `Affected scope`
  - `Failure mode`
- 재시작/모델 전환/서비스 변경은 human gate로 남긴다.
