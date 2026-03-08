# x-post PLAYBOOK V0.1 (Topic 956)

- **Purpose:** X(트위터)에서 ‘터질 각’ 콘텐츠를 선별해 **후보 3 + 선정 1(C톤 중장문)** 을 만들어, 메르세데스가 **수동 복붙 게시**하도록 지원한다. (자동 게시 금지)
- **Last updated:** 2026-03-08

## SSOT (what is fixed)
### Workstream identity
- Telegram topic: **956 = `x-post`**
- Canonical topic map: `context/telegram_topics/thread_topic_map.json`

### Execution rhythm (KST)
- **Daily 3 runs:** 08:10 / 12:10 / 18:10

### Candidate selection rule
- Goal: **좋아요 500+ 중심 후보 3개**
- If 500+ 부족하면 폴백 컷라인: **300 → 150** (단계 하향)

### Anti-dup filter (KR re-viral removal)
- 목적: “국내에서 이미 요약/번역으로 한 번 뜬 글” 재발굴을 피하고, **해외 원문을 국내에 빠르게 소개**하는 발굴로 맞춘다.
- 제외:
  - 한국어 요약/번역 계정이 인용(quote)해서 이미 조회수/RT를 먹고 있는 케이스
  - 한국어 본문/스레드로 이미 확산된 ‘2차 유통본’
- 빠른 검증(가볍게): 후보 URL에 대해 X에서 `url:<tweet_url>` 또는 원문 작성자+키워드로 검색 → 한국어 인용이 과도하면 제외
+
### Topic weighting (Mercedes preference)
- Priority: **A > B > C**
  - A) 실전 생산성(바로 써먹는 팁/워크플로)
  - B) 신규 런치/오픈소스 릴리즈
  - C) 에이전트 프레임워크/인프라(하드코어)

### Output contract — x-post
1) **후보 3개**
- 링크
- 좋아요(또는 RT) 수치
- “왜 터질 각인지” 1줄

2) **선정 1개**
- **C톤(Edmond 서사 + AOI 증빙)** 중장문 초안 **20~35줄**
- **AOI 증빙**: 체크리스트 5개 또는 미니표 1개
- **인용 복붙 박스 포함**
  - 원문 문장 1~3줄 + 링크(가능하면)
  - 커뮤니티 반응/2차 인용 1줄

### Style base (shared)
- 게시글은 **친절한 존대**
- 공통 컨셉 베이스: **귀여운 바닷가재가 모험을 떠나는 RPG** (상황/메타포만 활용, 과도한 설정 설명은 최소)
- 글에 어울리는 이미지 1장도 함께 생성(가능하면)

### Posting policy (hard)
- **자동 게시 금지**
- 메르세데스가 최종 검토 후 **직접 복붙 게시**

## Engines (discovery vs reading)
### Discovery (find candidates)
우선순위(운영 현실 기준):
1) **브라우저 기반(로그인 세션) Following / X Lists 스캔**
2) (대안) X API 기반 검색(x-research) — 비용 정책 필요

### Guardrails (account safety)
- **읽기 전용** (좋아요/팔로우/포스팅/DM 등 자동화 금지)
- **1탭**, 저속 스크롤 + 랜덤 딜레이
- 실행당 **최대 4분**
- **캡차/재로그인/제한 징후 뜨면 즉시 중단** (그 회차 스킵)
- (권장) 장기적으로 관측용 서브계정 분리

### Reading fallback (extract quote text)
- 1차: `https://r.jina.ai/https://<tweet_url>` (읽기 실패 시 본문 텍스트 추출)
- (선택) Scrapling: “발굴”이 아니라 **URL 본문 추출 보조 레일**로만 채택

## Recurring tasks (must not forget)
1) 매 회차 산출: **후보3 + 초안1 + 인용박스**
2) 실패 시에도 증빙 남기기: (무엇이 막혔는지 / 캡차 여부 / 어느 단계에서 실패)
3) 룰 변경 시 즉시 SSOT 업데이트
- 컷라인/시간창/소스(Following vs Lists)/가드레일 변경은 이 Playbook이 정본

## Where to record
- **반복업무/규칙:** 이 Playbook
- **진행중 큰 작업/긴급건:** `context/handoff/HF_x-post.md`
- **자동화/스케줄링:** `context/topics/maintenance_PLAYBOOK_V0_1.md` + 관련 launchd/loop spec

## KPIs (minimum)
- Runs/day: 3 (target)
- Success rate: (후보3+초안1 완성 회차 / 전체 회차)
- 평균 소요시간: 회차당 4분 이내 목표
