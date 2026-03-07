# acp PLAYBOOK V0.2 (SSOT)

- **Purpose:** Topic 50(ACP)에서의 모든 운영을 “증빙/승인/자동화” 기준으로 지속가능하게 굴리기 위한 규칙/반복업무/체크리스트 SSOT.
- **Scope:** ACP offer 운영, 팀원 지갑/키 운영, Dispatch(Bought & Analyzed) 발행, 증빙 축적.
- **Last updated:** 2026-03-08

## 0) Hard rules (절대규칙)
1. **Topic 50 = ACP 전용 워룸**
   - ACP 관련 요청/결과물/증빙/링크는 전부 Topic 50에만 쌓는다.
2. **시크릿 금지:** API key / Privy auth key / seed / 개인키 / 토큰 등 시크릿은 **채팅/Notion/Git에 절대 저장하지 않는다.**
   - SSOT에는 “포인터/경로/라벨”만 저장.
3. **승인 게이트:** 구매/결제/온체인 전송/offer 등록/외부 게시(홍보 포함)는 **사전 승인 없이는 실행하지 않는다.**
4. **Proof-first:** 중요한 주장/상태는 URL/스크린샷/로그/파일경로 등 **증빙을 남기는 것을 우선**한다.

## 1) Offering 운영 원칙
- Offering(판매 오퍼)은 **팀원 개별 ACP 계정/에이전트 단위**로 올린다.
- “12명 = 12개 offer”를 목표로 하되, **긴급개발(P0) > ACP offer 운영** 우선순위를 고정.
- 이번 주 ACTIVE는 2~3개로 제한(운영 방해 금지 모드).

## 2) Dispatch 운영 (Bought & Analyzed)
- 기본 주기: **주 1회 투고** (과도한 빈도는 금지)
- 차별점: 팀원들이 직접 구매 & 분석한 결과를 **머신-리더블 우선**으로 묶는다.
- 운영 플로우(요약):
  1) (청묘) 후보 shortlist 제시
  2) (팀원) 구매/분석 수행 + 증빙 제출
  3) (청묘) 합본/편집 + 최종 투고

## 3) 지갑/키 운영 (SSOT)
- 주소 매핑 SSOT: `context/acp/ACP_WALLET_REGISTRY_V0_1.md`
- 원칙: SSOT에는 주소만, **키는 로컬 git-ignored 파일/보안 저장소**로만.
- 마이크로 운영 워터마크 정책(초기값):
  - LOW(바닥): **1 USDC**
  - TARGET(채움): **3 USDC**
  - 방식: 부족하면 TARGET까지 보충(단, 자동 전송은 승인 필요)

## 4) 반복업무 (Recurring tasks)
### Weekly
- Dispatch 투고 리마인더 (주 1회)
- “Bought & Analyzed” 제출 수집 리마인더

### Daily/Ad-hoc
- 에이전트 지갑 잔고/활동 상태 점검(필요 시)
- offer runtime/serve 상태 점검(필요 시)

## 5) 기록 위치 (SSOT 구조)
- **진행중 작업:** `context/handoff/HF_*.md` (Handoff Index에 연결)
- **ACP 공통 규칙/체크리스트:** 이 Playbook
- **주소 매핑:** `context/acp/ACP_WALLET_REGISTRY_V0_1.md`

## 6) Automation plan (launchd / Ralph Loop)
### launchd (1차: 리마인더)
- 주간 Dispatch 리마인더
- 주간 Wallet/Ops 점검 리마인더

### Ralph Loop (2차: 실행 루프)
- shortlist → 구매/분석 → 합본 → 투고까지를 `ralph-loop` 라벨로 태스크화하고,
  루프 상태(이번주 후보/미제출/완료/보류)를 HF에 누적.
