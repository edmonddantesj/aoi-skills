# HF: AOI PRO 설치/퀵스타트 Preflight(노드/경로/라이선스)로 성공률 개선

- **Status:** ACTIVE
- **Owner:** 청묘
- **Last updated:** 2026-03-08 06:40 KST
- **Where:** Telegram topic 81 (Random) + 베타테스터 온보딩

## Goal
- 설치/실행 전에 “사전 점검(Preflight)”을 넣어 **폴백=BLOCKED+가이드**로 전환
- 테스터가 겪는 반복 병목(Windows bash/권한/Defender/프록시/터미널 혼동)을 표준 분기로 흡수

## Current state (what works / what’s broken)
- 반복 병목 패턴이 Random SSOT에 요약되어 있으나(토픽81 SSOT 섹션 B), 실제 “Preflight 체크리스트/메시지 템플릿/자동 진단”이 아직 SSOT/자동화로 고정되지 않음

## Decisions made
- 설치 완료/성공은 “말”이 아니라 PROOF로만 인정(Proof-first 적용)

## Next actions (ordered)
1. Preflight 체크리스트(노드 설치/가동, 경로, 라이선스/모드, 권한/네트워크) SSOT 문서화
2. Windows 분기(WSL2 vs Git Bash) 복붙 안내문 템플릿 고정
3. 실패 시 표준 리포트 포맷(STATUS/PROOF/BLOCKED/NEXT) 템플릿 배포
4. 가능하면 `openclaw doctor` 같은 진단 스크립트(또는 최소 커맨드 묶음) 정의

## Commands / paths / proofs
- PROOF: file=context/telegram_topics/TOPIC81_RANDOM_CONTEXT_SSOT_V0_1.md
- 참고 규칙: file=context/protocols/PROOF_FIRST_STATUS_PROTOCOL_V0_1.md

## Risks / blockers
- 제품/리포 구조(설치 스크립트/퀵스타트 문서 위치)에 대한 최신 SSOT가 필요
