# Playbook — Repeatable Rules V0.1 (SSOT)

이 문서는 Random(토픽 81) 대화 백업을 기준으로, **반복되는 업무/규칙을 영구 규격화**한 Playbook이다.

---

## 1) Topic 81(Random)의 역할
- Purpose: **잡담/실험/임시 논의/미분류 버퍼**
- Do: 테스트, 임시 아이디어, 짧은 Q&A, 설치/온보딩 디버그, 임시 링크/스크린샷
- Don’t: 확정 결정/장기 로드맵/배포 결론/L3 승인·집행
- SSOT: `context/telegram_topics/TOPIC81_RANDOM_CONTEXT_SSOT_V0_1.md`

---

## 2) Proof-first Status Protocol (전사 공통)
- SSOT: `context/protocols/PROOF_FIRST_STATUS_PROTOCOL_V0_1.md`
- 요약:
  - 금지: done/진행중 단독 사용
  - 필수: STATUS + PROOF + NEXT(or BLOCKED)
  - L3는 사전 승인 없이는 실행 금지

---

## 3) Handoff(HF)로 “진행중 작업” 분리 규칙
- 정책: `context/handoff/HANDOFF_POLICY_V0_1.md`
- 인덱스: `context/handoff/INDEX.md`
- 규칙:
  - 큰 작업/긴급건/여러날 가는 일 = **HF 1장** 생성 후 누적
  - 멈추기 전 `Next actions (ordered)` 최소 3개 남기기

---

## 4) Windows 베타테스터 온보딩(설치) 표준 분기
### 증상: bash 환경 부재/설치 스크립트 중단
- 루트 A(추천): **WSL2** 설치 후 Ubuntu에서 실행
- 루트 B(대안): **Git Bash**로 `curl | bash` 실행

### 운영 룰
- 설치가 “되었다”고 말하기 전에, 반드시 아래 중 1개 PROOF 확보:
  - `PROOF: cmd="openclaw status" -> ...`
  - `PROOF: file=<설치로그 경로>`
  - `PROOF: url=<스크린샷/로그 공유 링크>`

---

## 5) Render 502(Verified) 대응 표준
- 단발 오류는 ‘서버 성격’일 수 있음 → **재시도(백오프) + 타임아웃**으로 “최종 성공률”을 목표로 잡는다.
- 재현/판별 기준을 HF에 남긴다:
  - 언제/빈도/요청 경로/응답 코드/재시도 후 성공 여부

---

## 6) AOI PRO에서 LITE 폴백 발생 시 표준 흐름
- 결론: 무조건 재설치가 아니라 **진단 → 복구 → 재실행**이 기본
- 폴백은 `STATUS: blocked`에 준하는 사건으로 보고, 원인(환경/파일/검증 경로)을 증빙과 함께 남긴다.

---

## 7) x402(결제 기반 API) 실험의 안전장치
- 원칙: LIVE 결제는 L3(돈) → **명시 승인 없이는 실행 금지**
- 기본 진행: `DRY_RUN=true` (402 챌린지/terms 디코드까지)
- 필수 캡(예시): max $/day, max $/tx, allowlist endpoints
