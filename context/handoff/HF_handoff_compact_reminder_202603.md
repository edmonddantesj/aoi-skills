# HF: handoff(586) — Daily Compact 스냅샷 리마인더 자동화

- **Status:** ACTIVE
- **Owner:** 청비/record
- **Last updated:** 2026-03-17 13:33 KST
- **Where:** Telegram topic **handoff=586**

## Goal
매일 09:30 KST에 현재 ACTIVE HF 목록 + 긴급 항목을 자동으로 요약해 handoff(586)에 올린다.

## Spec
- 타이밍: 09:30 KST daily
- 출력 대상: topic 586 (handoff)
- 내용 구성:
  1. ACTIVE HF 목록 (slug + 1줄 요약)
  2. 오늘 마감/긴급 항목 (있으면)
  3. 어젯밤 이후 새로 추가/완료된 HF (있으면)
- 출력 형태: 5~10줄 이하, 짧고 날카롭게

## Current state
- 자동화 미구현 (launchd plist 없음)
- 수동 compact는 이 토픽에서 `이 토픽 저장` / `복구해줘` 명령으로 대체 중

## Decisions made
- 자동화 구현 전까지는 09:30 KST 하트비트 또는 handoff 토픽 진입 시 수동 compact로 대체.
- launchd 방식으로 구현 시 `context/automation/launchd/` 아래에 plist 배치.

## Next actions
1. [ ] launchd plist 초안 작성 (`ai.aoi.handoff-compact-daily.plist`)
2. [ ] compact 스크립트 작성 — `context/handoff/INDEX.md` ACTIVE 섹션 읽고 요약 생성 후 topic 586에 전송
3. [ ] 테스트 후 설치 (L2) / 활성화 승인 (L3)

## Commands / paths
- Handoff index: `context/handoff/INDEX.md`
- Topic-state: `context/topic-state/handoff.md`
- Automation dir: `context/automation/launchd/`
