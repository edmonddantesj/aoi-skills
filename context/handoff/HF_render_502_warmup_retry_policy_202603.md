# HF: Render 502(Verified) — 워밍업/재시도 정책 SSOT 확정

- **Status:** ACTIVE
- **Owner:** 청묘
- **Last updated:** 2026-03-08 06:40 KST
- **Where:** Telegram topic 81 (Random)

## Goal
- 간헐적 `502 Bad Gateway`를 “운영적으로 해결”하기 위한 표준 정책 확정
- 기준: 단발 회피가 아니라 **최종 성공률 확보** (retry/backoff/timeout)

## Current state (what works / what’s broken)
- Random SSOT에 운영적 해결 방향만 존재(재시도/백오프/타임아웃)
- 실제 파이프라인에 적용된 리트라이 규격/헬스체크(`/health` 워밍업) 여부는 아직 불명

## Decisions made
- 502는 서버 콜드스타트/일시 장애 성격일 수 있음 → retry/backoff를 표준으로 채택

## Next actions (ordered)
1. 대상 엔드포인트/컴포넌트 식별(어떤 요청에서 502가 나는지)
2. retry 정책(최대 횟수/백오프/타임아웃/서킷브레이커) SSOT로 고정
3. 워밍업(`/health`) 실행 여부 및 위치(클라이언트/서버) 결정
4. 적용 후 PROOF(로그/커맨드 출력/테스트 결과) 첨부

## Commands / paths / proofs
- PROOF: file=context/telegram_topics/TOPIC81_RANDOM_CONTEXT_SSOT_V0_1.md

## Risks / blockers
- 실제 운영 스택/레포 경로를 먼저 특정해야 함
