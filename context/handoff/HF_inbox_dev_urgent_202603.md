# HF: Inbox-dev 긴급개발 (Topic 585) — DB/State loss + BaseBatches 데모

- **Status:** DONE ✅ 2026-03-17
- **Owner:** 청묘 (+ 관련팀: 청령/oracle, 청섬/builder)
- **Last updated:** 2026-03-08 05:47 KST
- **Where:** Telegram group topic **inbox-dev=585** (참조: topic map `context/telegram_topics/thread_topic_map.json`)

## Goal
- (1) DB/State 손실 이후 **반드시 다시 만들어야 하는 것들**을 우선순위로 복구/개발.
- (2) **Base Batches (3/9)** 데드라인: Vercel URL + 데모 영상 + repo 제출.

## Current state (what works / what’s broken)
- `gh`로 private repo 접근이 간헐 실패했는데 원인이 확인됨:
  - 환경변수 `GITHUB_TOKEN`(fine-grained PAT)이 `gh` keyring 토큰을 덮어써서 권한 에러 유발.
  - 워크어라운드: `env -u GITHUB_TOKEN gh ...`
  - 근본해결: 해당 PAT에 필요한 repo 권한 부여.
- Private repo `edmonddantesj/aoi-state-saves` 확인:
  - release `state_snapshot__20260306_211137` 존재, asset 다운로드 + sha256 검증 완료.

## Decisions made
- “긴급개발”은 Ralph Loop/RSL 스터디가 아니라 **실제 빌드/제출 우선**.
- 재현/복구는 두 갈래로 취급: (A) 로컬 DB/상태 (B) 태스크/문서 DB.

## Next actions (ordered)
1) (P0) **Base Batches 데모 패키지 확정**
   - 목표(3/9): Vercel URL + demo video + repo `https://github.com/edmonddantesj/aoi-basebatches-demo`
   - 데모 핵심: Base Sepolia에서 **실제 서명 1 tx** + proof bundle + `/verified` history 뷰.
   - 도메인 구매 불필요(Vercel *.vercel.app OK).
2) (P0) 지갑/서명 권한 복구 체크
   - 데모용 지갑 주소 컨텍스트는 존재하나(로그), **서명 권한 복구 가능성은 자격증명 존재 여부**에 달림.
   - 채팅에 시크릿 공유 금지.
3) (P1) State snapshot 기반 SSOT 복구 계속
   - 필요 문서/프로토콜을 snapshot 릴리즈에서 확인하고, 작업 디렉토리 `context/`로 승격.

## Commands / paths / proofs
- Workaround: `env -u GITHUB_TOKEN gh repo view ...`
- Snapshot:
  - created+uploaded: `state_snapshot__20260307_051207`
  - created+uploaded: `state_snapshot__20260307_145614`
- Phase2 SDNA 프로토콜(업그레이드 산출물): `context/opus_phases/PHASE_2_SDNA_PROTOCOL_V0_2.md`

## Related work (same timeframe)
- Nexus Bazaar / The Archive 프런트 UX 마무리(3/7):
  - `nexus-bazaar-webapp/src/App.css`
  - `src/pages/AdminReceiptsPage.tsx`
  - `src/pages/ReceiptPage.tsx`
  - `src/components/QuickActionBar.tsx`

## Risks / blockers
- Base Batches 제출까지 시간이 짧음(3/9). 영상/배포/tx proof가 병목.
- GitHub 토큰 권한 설정이 꼬이면 자동화/복구가 계속 막힐 수 있음.
