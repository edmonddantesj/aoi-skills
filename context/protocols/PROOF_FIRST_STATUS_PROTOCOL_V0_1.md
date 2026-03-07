# Proof-first Status Protocol V0.1 (SSOT)

목적: 에이전트/팀의 상태 업데이트가 “말”이 아니라 **재현 가능한 증빙(PROOF)** 으로 남도록 강제한다.

> 슬로건: **No proof = didn’t happen.**

---

## 0) 적용 범위
- 텔레그램/노션/깃헙/문서 어디든 **상태 업데이트**를 남길 때 전부 적용
- 특히: 배포/빌드/크론/자동화/릴리즈/운영 복구/온보딩 디버그

---

## 1) 금지 규칙 (BAN)
아래 표현을 **단독으로** 쓰는 것을 금지한다.
- “done / 완료”
- “working on it / 진행중 / 처리중 / 하고있음”
- “ok / 확인함” (증빙 없이)

허용되는 최소 조건: 아래 **표준 포맷**을 따르며 `PROOF:`가 1개 이상 포함되어야 한다.

---

## 2) 표준 포맷 (필수)
상태 업데이트는 항상 다음 중 하나의 형태로 남긴다.

- `STATUS:` starting | in_progress | review | done | blocked
- `PROOF:` file= | url= | cmd= | pid= | sha= | tx= (최소 1개)
- `NEXT:` 다음 액션 1줄 **또는** `BLOCKED:` 막힌 이유 1줄

### PROOF 예시
- `PROOF: file=context/handoff/HF_xxx.md`
- `PROOF: url=https://github.com/.../pull/123`
- `PROOF: cmd="openclaw status" -> "gateway: running"`
- `PROOF: sha=abc1234`
- `PROOF: tx=0x...`

---

## 3) DONE의 정의
`done`은 “기분”이 아니라 조건이다.
- **재현 가능**하고
- **증빙이 남아** 있고
- **SSOT(context/)에 기록**되어 있어야 한다.

---

## 4) L3(비가역/외부) 추가 거버넌스
다음은 **PROOF가 있어도 사전 승인 없이는 실행 금지**.
- 돈(결제/송금), 지갑/키/시드
- 온체인 트랜잭션
- 외부 게시/배포(공개 릴리즈/트윗/홍보)
- 파괴적 명령(대량 삭제/권한 변경/서비스 중단 등)

표기:
- `L3: <무엇>` 라벨을 먼저 붙이고, 승인자/승인 시각을 기록한다.

---

## 5) 최소 템플릿(복붙용)

### 진행 업데이트
- STATUS: in_progress
- PROOF: cmd="..." -> "..."
- NEXT: ...

### 완료 업데이트
- STATUS: done
- PROOF: file=... (또는 url/sha)
- NEXT: (후속이 없으면) "NEXT: none" 또는 체크리스트 마감

### 막힘 업데이트
- STATUS: blocked
- PROOF: url=... (또는 file/cmd)
- BLOCKED: ...
