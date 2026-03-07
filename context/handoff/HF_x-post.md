# HF: x-post(956) — 브라우저 기반 후보발굴/본문추출 파이프라인 안정화

- **Status:** ACTIVE
- **Owner:** 청묘 / growth / 메르세데스
- **Last updated:** 2026-03-08 06:40 KST
- **Where:** Telegram topic 956 (x-post), SSOT: `context/topics/x-post_PLAYBOOK_V0_1.md`

## Goal
- 매일 3회(08:10/12:10/18:10 KST) **후보3 + 선정1(C톤 20~35줄 + AOI 증빙 + 인용박스)** 산출을 안정적으로 만든다.
- **자동 게시 금지** 원칙은 유지한다(산출물만 제공).

## Current state (what works / what’s broken)
- Playbook(규칙/포맷/가드레일)은 `context/topics/x-post_PLAYBOOK_V0_1.md`에 정리 완료.
- 발굴 엔진은 “브라우저 기반(로그인 세션) Following / Lists 스캔”이 기본 방향.
- 본문 추출은 `r.jina.ai` fallback을 1차 레일로 사용.
- (과거 대화 기준) openchrome/openclaw 릴레이 등 구현 시도는 있었으나, E2E로 Following에서 후보3개를 안정적으로 뽑는 성공 로그를 고정해두지 못했음(세션 유지/DOM 파싱/가상스크롤/메모리 압박 이슈).

## Decisions made
- Topic 956은 workstream `x-post`로 운영.
- 실행 리듬: 08:10 / 12:10 / 18:10 KST.
- 컷라인: 500 기본, 없으면 300→150 폴백.
- 안전: 읽기전용/1탭/4분 제한/저속 스크롤/캡차·재로그인 즉시 중단.
- r.jina.ai는 ‘발굴’이 아니라 ‘읽기/본문추출’ 폴백.

## Next actions (ordered)
1) (운영) 3회 스케줄에 맞춘 **산출물 생성 루틴**을 자동 트리거(launchd or Ralph Loop)로 고정
2) (기술) 발굴 엔진 1개 확정
   - A) OpenClaw 브라우저 릴레이 기반(탭 attach 필요)
   - B) openchrome 기반(세션 유지 러너 필요)
3) (증빙) 성공/실패 각각에 대해 Evidence Pack 남기기
   - 성공: 후보3 링크+지표+선정 초안+인용박스
   - 실패: 스크린샷/에러 로그/중단 사유(캡차/재로그인/DOM 미탐색)

## Commands / paths / proofs
- Playbook(정본): `context/topics/x-post_PLAYBOOK_V0_1.md`
- Handoff index: `context/handoff/INDEX.md`
- Automation stub(초안): `scripts/xpost_tick.sh` + `context/automation/launchd/com.aoineco.xpost.tick.plist`
- Proof(예정): `artifacts/x-post/<timestamp>/` (회차별 산출물)

## Risks / blockers
- X UI/DOM 변경, 로그인/제한/캡차에 의한 중단
- 브라우저 자동화 시 계정 리스크(가드레일 준수 필수)
- 메모리/리소스 압박으로 인한 추출 불안정
