# ACP Tailscale 구성 — ADP 히스토리 기반 복제 플랜 (V0.1)

목적: ADP에서 이미 검증된 “Tailscale로 원격에서 항상 상태 파악” 구성을 ACP에도 동일하게 적용한다.

> 주의: 이 문서는 **접속/관측 채널**만 다룬다. buy/onchain/publish 등 위험 액션은 별도 **승인 게이트(FAIL-CLOSED)** 정책을 따른다.

## 1) ADP 히스토리에서 확인된 증빙(발췌)
- ADP dev endpoint(3010)가 Tailscale 도메인으로 접근 가능:
  - `curl http://choi-macmini.tailc63c7c.ts.net/ → 200`
- 운영 작업 항목에 `tailscale serve 런북`이 별도 태스크로 잡혀 있었음(백로그):
  - `TASK-20260303-ADPDEVSTAB-03 (tailscale serve 런북)`

Source: `tmp/0305_ADP.txt` (Telegram topic45 ADP export → docx→txt 변환)

## 2) ACP에 적용할 추천 구조(ADP 방식 복제)
### A. Access (접속)
- ACP 운영 노드(현재 Mac mini)를 tailnet에 조인
- 외부에서 공인 IP/포트포워딩은 금지

### B. Observe (관측)
- 원격 상태 확인은 “tailnet 내부에서만” 제공
- 두 가지 방식 중 하나를 택하되, 1차는 B가 더 안전:

**B1) Tailscale SSH + 포트포워딩 (권장/안전)**
- PixelOffice control plane(예: 4100), ADP dev server(예: 3010) 등은 localhost 유지
- 필요 시 `ssh -L`로 로컬처럼 접속

**B2) Tailscale Serve (편의)**
- tailnet 도메인(`*.ts.net`)으로 내부 노출
- 예: ADP에서 확인된 `choi-macmini.tailc63c7c.ts.net`

### C. Approve (승인)
- buy/onchain/publish는 PixelOffice 승인 큐(`awaiting`)로 올리고, 기본 deny/hold(FAIL-CLOSED)

## 3) ACP 체크리스트(복제 절차)
1. (운영 노드) tailscale 로그인/조인 확인
2. (DNS) `*.ts.net` 도메인 동작 확인(옵션)
3. (관측) PixelOffice control plane을 tailnet 내부에서만 접근 가능하도록 설정
   - port-forward 방식 또는 serve 방식 선택
4. (보안) 승인 게이트 정책이 없는 엔드포인트는 read-only로만

## 4) Open Questions (추가 백업 분석 필요)
- ADP에서 실제로 `tailscale serve`를 실행해 고정했는지(런북/명령/ACL/태그)
- tailnet ACL/SSH policy (누가 어떤 노드에 접근 가능한지)
- exit node / funnel 사용 여부

다음: 통합 백업(전체 export)에서 `tailscale serve` 실제 실행 로그/명령이 나오면 V0.2로 업데이트.
