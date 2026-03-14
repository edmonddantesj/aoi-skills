# moltbook PLAYBOOK V0.1

- **Purpose:** Moltbook(EN) 커뮤니티 운영(글/댓글/대댓글) + Daily/Weekly 콘텐츠 루프를 “승인 게이트 + 증빙”으로 굴리기
- **Topic:** moltbook (thread_id=1114)
- **Last updated:** 2026-03-08

## SSOT / Canon
- 진행중 작업(복구/운영): `context/handoff/HF_moltbook_ops_202603.md`
- 공통 승인/권한(L1/L2/L3): `context/telegram_topics/ANNOUNCEMENTS_CANONICAL_V0_1.md`
- 게시물 끝 블록/출처/작성자 표기 형식: `context/protocols/MOLTBOOK_POSTING_FORMAT_V0_1.md`

## Operating rules (always)
- **외부 게시/댓글/대댓글/삭제 등 대외영향 = L3 → 의장 Yes/No 승인 필수 (fail-closed)**
- 승인 없이 가능한 것: 스캔/리서치/초안/내부 정리(L1/L2)
- 게시 후에는 반드시 **증빙 번들** 남기기:
  1) 최종 URL
  2) (가능하면) response id 또는 스샷 1장
  3) 사용한 스크립트/커밋 해시(재현용)

### Attribution / Originality (must)
- 글 끝 형식은 `context/protocols/MOLTBOOK_POSTING_FORMAT_V0_1.md`를 canonical로 따른다.
- 글 하단은 아래 두 형식 중 하나만 사용:
  - **Benchmark bundle + Our take** (타 글 참고/확장 글)
  - **Original (Aoineco & Co.)** (우리 경험/토론 기반 오리지널 글)
- 팀 글 표기:
  - `This post reflects an internal discussion within Aoineco & Co. (not an individual’s personal opinion).`
- 작성/검토 표기:
  - `Written by: <English name>`
  - `Reviewed by: <English name 1>, <English name 2>`
- 내부 한글명(`청검`, `청비`, `청령`)을 외부 게시물 끝 표기에 쓰지 않는다.
- 금지: 실제로 읽지 않은 링크를 벤치마크로 나열 / 실제 토론 없는데 “12명이 토론” 같은 과장 / `Attribution line:` 같은 메타 라벨 추가

### Benchmark bundle template
- **Benchmark bundle (what we read):** 링크 3~7개
- **Our take (what we add):** 동의/반박/확장 1~2개 (짧고 단호하게)

## Recurring tasks (must not forget)
### Daily (EN)
- [ ] Moltbook 신규/인기글 스캔 → **글감 후보 3개**
- [ ] **Moltbook EN 글 1편 ‘상세 초안 패키지’ 생성**
  - 최소 포함: 제목 variants / picked title / TL;DR / near-post-ready full body / CTA / benchmark bundle candidates
  - **초안 단계부터 canonical end matter를 완성형으로 포함**: `Original (Aoineco & Co.)` 또는 `Benchmark bundle + Our take` 중 하나를 실제로 붙이고, `This post reflects an internal discussion within Aoineco & Co. (not an individual’s personal opinion).` + `Written by:` + `Reviewed by:`까지 채운다
  - 원칙: **주제 씨앗만 던지지 말고, 업로드 직전까지 검토 가능한 수준으로 작성**
  - 가능하면 **전날 밤 운영 지시 / HF 메모 / 최근 topic 요구사항**을 반영
- [ ] **Writer/Reviewers 로테이션 할당** (랜덤 + 주간 중복 방지)
- [ ] 업로드는 승인 YES 받은 경우에만 실행
- [ ] 게시 후 **첫 10분 댓글 창** 운영: 초반 10분 내 달린 댓글에는 가능한 한 모두 대댓글한다
  - 원칙: early engagement window는 게시물 운영의 일부로 본다
  - 단, 너무 빠른 연속 작성으로 spam/rate-limit 처리되지 않도록 순차적으로 템포 조절
  - verification / publish 상태까지 확인하고, 필요시 짧은 간격으로 나눠 응답

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

## Delegation / review gate (team rotation)
- Writer/Reviewers 로테이션을 “12 에이전트”로 실제 운영(토론 로그 생성)하려면, **subagent 스폰 allowlist**가 필요.
- 본 건(몰트북 포스팅 업무분배)에 한해: **청령 검토 후 허락받고 진행**

## Where to record
- 진행중 작업/결정/리스크/Next: **HF에 누적** (`context/handoff/HF_moltbook_ops_202603.md`)
- 반복업무/규칙/체크리스트: 이 Playbook
