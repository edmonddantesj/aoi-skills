# HF: ACP 운영/자동화 SSOT (2026-03)

- **Status:** ACTIVE
- **Owner:** 청묘 / 메르세데스
- **Last updated:** 2026-03-08 06:55 KST
- **Where:** Telegram Topic 50 (ACP), `context/topics/acp_PLAYBOOK_V0_1.md`, Notion 🛒 ACP Offers Registry (Squad, v0.1)

## Goal
- Topic 50(ACP) 백업을 기준으로:
  1) 반복업무/규칙을 Playbook에 영구 기록
  2) 진행중 작업을 HF로 분리하여 끊김 없이 운영
  3) 반복업무를 launchd 또는 Ralph Loop로 자동화까지 완료

## Current state (what works / what’s broken)
- 워룸 규칙/보안 원칙/지갑 매핑(주소 SSOT)은 대화상으로 확정되어 있음.
- 다만 SSOT가 “대화”에 많이 존재 → 파일/자동화로 고정이 필요.
- 자동화(launchd/Ralph)로 굴러가는 루틴은 아직 ‘정식 설치/운영’로 확정되지 않음.

## Decisions made (SSOT로 고정할 것)
- Topic 50 = **ACP 전용 워룸** (ACP 관련 요청/결과물/증빙/링크는 여기)
- Offering(판매 오퍼)은 **팀원 개별 ACP 계정/에이전트 단위**로 올린다.
- **구매/결제/등록/외부게시 등 돈/온체인/공개 액션은 사전 승인** 없이는 진행하지 않는다.
- 시크릿(API 키/Privy auth key/seed 등)은 **채팅/Notion/Git에 절대 저장 금지**
- Dispatch 운영은 **Bought & Analyzed 중심** + (원칙적으로) **주 1회 투고**
- 에이전트 지갑 운영은 Low/Target 워터마크 정책을 두고 마이크로 운영으로 시작

## Next actions (ordered)
1. `context/topics/acp_PLAYBOOK_V0_1.md`에 반복업무/규칙/체크리스트를 정리해 SSOT 고정
2. 진행중 작업을 HF로 추가 분리(필요 시 아래 슬러그로 추가 생성)
   - `HF_acp_dispatch_002.md` (Dispatch #002 운영)
   - `HF_acp_offer_registry.md` (12명 오퍼 레지스트리/활성화 2~3개)
   - `HF_acp_wallet_ops.md` (지갑 매칭/충전/잔고점검/증빙)
3. 자동화: launchd로 “주간 Dispatch 리마인더 + 월렛 점검 리마인더” 1차 설치(로컬)
4. Ralph Loop: “후보 shortlist → 팀원 Bought&Analyzed 제출 → 합본/투고” 루프를 태스크 라벨링(`ralph-loop`)로 운영안 고정

## Commands / paths / proofs
- Wallet SSOT: `context/acp/ACP_WALLET_REGISTRY_V0_1.md`
- Handoff policy: `context/handoff/HANDOFF_POLICY_V0_1.md`
- Handoff index: `context/handoff/INDEX.md`
- ACP Playbook: `context/topics/acp_PLAYBOOK_V0_1.md`

## Risks / blockers
- Notion/ACP/Privy 관련 시크릿 취급 실수(채팅 노출) 리스크
- 자동화가 ‘리마인더’ 수준을 넘어 실제 체결/전송으로 확장될 때 승인 게이트 필요
