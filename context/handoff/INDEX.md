# Handoff Index (SSOT)

목적: 시간이 지나 다시 물어봐도, 현재 진행중인 작업을 **끊김없이 즉시 재구성**하기 위한 작업 현황 SSOT.

규칙:
- 새 작업/에픽 시작 시: `context/handoff/HF_<slug>.md` 생성
- 작업 진행/결정/막힌점/다음 액션은 해당 HF 문서에 누적
- 완료 시: 상태를 DONE으로 바꾸고, 산출물/링크/후속 액션을 기록

템플릿: `context/handoff/_TEMPLATE.md`

## ACTIVE
- `HF_inbox_dev_urgent_202603.md` — Inbox-dev(585) 긴급개발: DB/State loss 복구 + Base Batches(3/9) 데모
- `HF_handoff_compact_reminder_202603.md` — handoff(586): DAILY COMPACT 스냅샷 리마인더 자동화(09:30 KST)
- `HF_v6_invest_live_restart_202603.md` — v6-invest(1029): 실투 재개발/운영 복구 SSOT 및 반복업무 자동화
- `HF_x-post.md` — x-post(956): 브라우저 기반 후보발굴/본문추출 파이프라인 안정화 + 3회/일 산출 루틴 고정
