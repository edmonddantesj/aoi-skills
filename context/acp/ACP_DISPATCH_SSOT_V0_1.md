# ACP Dispatch SSOT V0.1

목적: ACP Dispatch 운영이 “기억/대화”가 아니라 **재현 가능한 SSOT(폴더/파일/규칙/게이트)**로 고정되도록 한다.

## 0) Canonical Spec Repo
- Repo (source of truth): `repos/aoineco-acp-dispatch-spec`
- Dispatch issues live under:
  - `repos/aoineco-acp-dispatch-spec/dispatch/`

## 1) Issue #001 (2026-02-25) — 구조(포맷) SSOT
SSOT: `repos/aoineco-acp-dispatch-spec/dispatch/ACP_DISPATCH_001_2026-02-25/README.md`

### 필수 산출물
- One-pager (EN)
- One-pager (KR)
- Preface
- Per-role reports (역할별 리포트 파일)

### #001의 핵심 의도
- “12-role experiences”를 **1페이지로 압축**하고, 각 항목은 **proof-first(영수증/tx/job id)**로 확장 가능해야 함.

### #001에서 관측된 포인트(요약)
- Verifiable action(증빙 가능한 실행)이 설득 비용이 가장 낮음
- Bait → trust loop(저가/초소액 실행→영수증 표준화)이 작동
- Distribution primitive(채널 생성 등)이 레버리지

## 2) Issue #002 (2026-03-07) — 방향(스펙상)
SSOT: `repos/aoineco-acp-dispatch-spec/dispatch/ACP_DISPATCH_002_2026-03-07/README.md`

### #002 포커스
- One-pager 파일명이 명시적으로 **bought_and_analyzed** 트랙임:
  - `ACP_DISPATCH_002__onepager__bought_and_analyzed__AOINECO_$NECO.md`

### 운영 규칙(스펙에 명시)
- Posting/publishing은 **L3** (explicit approval 필수)
- Author name은 **Aoineco**만 사용(assistant persona명 사용 금지)
- secrets/internal-only/stealth/top-secret 내용 금지

### 최신 백업에서 확정된 #002 운영 메커니즘(추가 SSOT)
- 채널: **Moltbook**
- 방식: 12명 전원 **자율 선택/자율 구매/각자 분석**
- 분산 운영: **4/4/4 배치**로 스킬 탐색→구매→분석 진행
- 전제: “출범/신규 프로그램”이 아니라 **001부터 이어오던 방식**을 002에 그대로 적용

## 3) 운영 원칙(Topic 50 합의분, SSOT로 고정)
- Dispatch의 강력한 차별점은 **Bought & Analyzed(직접 구매 + 분석)**
- 단, **구매=돈(L3)** 이므로 “분석 자동화”와 “구매 실행 승인”을 분리한다.
- Public/Internal 2-레일:
  - Public은 public-safe + 증빙 중심
  - Internal은 더 자세한 로그/회고를 담되 시크릿 금지

### Wallet 운영(Dispatch 품질을 올리는 기반)
- 마이크로 운영 워터마크(확정): **LOW=1 USDC / TARGET=3 USDC**
- 잔고 부족 시 알림: Privy/회사 treasury 둘 다 부족하면 메르세데스에게 알림
- 주기: Dispatch가 주 1회라 잔고점검도 과도하게 자주 돌릴 필요 없음(주간 단위면 충분)

Proof (chat export pointers):
- `_inbox/telegram_export/ChatExport_2026-03-08_aoineco/ChatExport_2026-03-08 (16)/messages17.html` 내
  - “001 포맷/저장방식/프리플라이트 인지” 대화 블록
  - “Bought & Analyzed + L3 구매 게이트” 합의 블록

## 4) Working doc / Handoff
- 진행(오늘/이번 주) 작업은 HF에 누적:
  - `context/handoff/HF_acp_dispatch_002_202603.md`

## 5) Next (운영 체크리스트)
1) Dispatch #002는 **spec repo의 폴더/네이밍을 정본으로** 한다.
2) 준비 단계에서 필요한 것:
   - 엔트리(스킬)별: URL/가격/실행 로그/증빙 포인터(tx/job id)
   - 리스크: 시크릿/승인게이트/재현성
3) 투고 전 preflight(가드):
   - Aoineco only
   - L3 승인 확인
   - 금칙어/시크릿 스캔

(※ preflight 스크립트가 과거 별도 drafts repo에 존재했다는 언급이 있으나, 현재 워크스페이스 기준으로는 spec repo가 정본이므로 “필요 시” workspace 스크립트로 재구축한다.)
