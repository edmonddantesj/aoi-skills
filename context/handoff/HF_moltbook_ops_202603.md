# HF: moltbook ops (rebuild + daily loop) — 2026-03 (ACTIVE)

- **Owner/Primary:** (TBD)
- **Scope:** moltbook topic(1114) 운영 복구 + Daily/Weekly 반복업무 자동화 고정
- **Last updated:** 2026-03-08

## Status (now)
- **STATE:** ACTIVE
- **Current mode:** 복구 모드 (키/스크립트/SSOT 재구축 전제)

## Decisions (SSOT)
1) **토픽 고정:** `moltbook` 운영 토픽 = **thread_id 1114**
2) **운영 정책(강화 모드/B):**
   - Daily: **Moltbook(EN) 1포스트/일** (초안 패키지 생산 포함)
   - Weekly: **봇마당(KR) 1포스트/주**
   - **업로드/댓글/대댓글 등 대외 게시 = L3 → 의장 Yes/No 승인 필수 (fail-closed)**
3) **API 기술 포인트:** 대댓글(reply) 작성 시 부모 댓글 필드 = `parent_id` (NOT `parent_comment_id`)

## Evidence / References
- (근거) 2026-03-08 대화 백업(telegram export) — moltbook 토픽(1114)
- 대표 글 링크(기준 샘플): https://www.moltbook.com/post/b55f3459-f842-4d60-a09d-e2ea4cc73aa3

## Next actions (ordered)
### A. 복구(내부) — 최소 동작 세트
- [ ] Moltbook Developers: 키 재발급/복구 루트 확정 (apply → create app → key)
- [ ] 키 저장 SSOT 확정 (OpenClaw secrets vs `~/.config/moltbook/credentials.json`)
- [ ] read-only health check: `/api/v1/posts?...` 및 `/api/v1/posts/{post_id}/comments` 접근성 재확인
- [ ] write path(POST) 가능 여부 확정 (글/댓글/대댓글) + 승인 게이트 플로우 문서화

### B. 운영(외부) — Daily/Weekly loop
- [ ] Daily: Moltbook(EN) 초안 패키지 자동 생성(스캔→후보→초안)
- [ ] Daily/Weekly 게시(실제 업로드)는 “YES 승인” 받은 후에만 실행
- [ ] 게시 후 증빙 번들: (1) 최종 URL (2) API response id/스크린샷 (3) 실행 커밋/스크립트 해시

## Log (append-only)
- 2026-03-08: 대화 백업 기반으로 SSOT 재정리 시작. Playbook/HF 분리 + launchd 자동화 착수.
- 2026-03-08: Attribution/Originality 규칙 추가(벤치마크 링크 묶음 + Our take + 팀 글 표기). "읽지 않은 링크/허위 집단토론" 금지.
