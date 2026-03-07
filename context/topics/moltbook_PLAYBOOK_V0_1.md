# moltbook PLAYBOOK V0.1

- **Purpose:** Moltbook(EN) 커뮤니티 운영(글/댓글/대댓글) + Daily/Weekly 콘텐츠 루프를 “승인 게이트 + 증빙”으로 굴리기
- **Topic:** moltbook (thread_id=1114)
- **Last updated:** 2026-03-08

## SSOT / Canon
- 진행중 작업(복구/운영): `context/handoff/HF_moltbook_ops_202603.md`
- 공통 승인/권한(L1/L2/L3): `context/telegram_topics/ANNOUNCEMENTS_CANONICAL_V0_1.md`

## Operating rules (always)
- **외부 게시/댓글/대댓글/삭제 등 대외영향 = L3 → 의장 Yes/No 승인 필수 (fail-closed)**
- 승인 없이 가능한 것: 스캔/리서치/초안/내부 정리(L1/L2)
- 게시 후에는 반드시 **증빙 번들** 남기기:
  1) 최종 URL
  2) (가능하면) response id 또는 스샷 1장
  3) 사용한 스크립트/커밋 해시(재현용)

## Recurring tasks (must not forget)
### Daily (EN)
- [ ] Moltbook 신규/인기글 스캔 → **글감 후보 3개**
- [ ] **Moltbook EN 글 1편 ‘초안 패키지’ 생성** (제목/요약/본문/CTA/태그 후보)
- [ ] 업로드는 승인 YES 받은 경우에만 실행

### Weekly (KR)
- [ ] 봇마당(KR) 1편/주: 초안 패키지 생성 → 승인 → 게시

## Technical notes (API)
- 댓글/대댓글(reply) 작성 시 부모 댓글 필드: `parent_id` (NOT `parent_comment_id`)
- read-only 확인용 엔드포인트(공개 여부에 따라 동작):
  - `GET https://www.moltbook.com/api/v1/posts?sort=new&limit=N`
  - `GET https://moltbook.com/api/v1/posts/{post_id}/comments`

## Automation (launchd)
- Launchd job: `context/automation/launchd/ai.aoi.moltbook.daily.plist`
- 실행 스크립트: `scripts/moltbook_daily_tick.sh`
- 결과 산출물(초안 패키지): `artifacts/moltbook/daily/YYYY-MM-DD.md`

## Where to record
- 진행중 작업/결정/리스크/Next: **HF에 누적** (`context/handoff/HF_moltbook_ops_202603.md`)
- 반복업무/규칙/체크리스트: 이 Playbook
