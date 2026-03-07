# HF: AOI PRO Lite 평생권($0.01) — 스펙/가드레일 숫자 확정

- **Status:** ACTIVE
- **Owner:** 청묘
- **Last updated:** 2026-03-08 06:40 KST
- **Where:** Telegram topic 81 (Random)

## Goal
- AOI PRO Lite 평생권(한정기간, $0.01) 판매 설계의 **조건/가드레일/숫자**를 확정
- 시빌/지원부하 방지 조건을 SSOT로 고정

## Current state (what works / what’s broken)
- Random SSOT에 “아이디어/방향”만 존재
- 1그룹 제한/룰 제한/기간/레이트/업셀 트리거 등 숫자/정책이 미확정

## Decisions made
- x402 결제 기반 실험은 L3(돈) → 승인 전 LIVE 집행 금지

## Next actions (ordered)
1. 판매 기간/한정 수량/대상(테스터 전용 등) 확정
2. 시빌 방지: 결제/계정/그룹/디바이스/레이트 리밋 정책 설계
3. 지원 부하 방지: 지원 채널/응답 SLA/범위(무상 지원 범위) 명시
4. Lite 제한(기능/수량) + Pro 업셀 트리거 정의
5. SSOT 문서 1장으로 박제 + 실행 체크리스트(HF) 연결

## Commands / paths / proofs
- PROOF: file=context/telegram_topics/TOPIC81_RANDOM_CONTEXT_SSOT_V0_1.md

## Risks / blockers
- 가격/결제(돈) 관련이라 승인 프로세스가 필요
