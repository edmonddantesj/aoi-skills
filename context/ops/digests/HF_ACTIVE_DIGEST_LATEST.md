# HF ACTIVE Digest (latest)

- Generated: 2026-03-08 06:40 KST

- Source: context/handoff/INDEX.md

## ACTIVE

### HF_inbox_dev_urgent_202603.md — Inbox-dev(585) 긴급개발: DB/State loss 복구 + Base Batches(3/9) 데모

- Status: ACTIVE
- Owner: 청묘 (+ 관련팀: 청령/oracle, 청섬/builder)
- Last updated: 2026-03-08 05:47 KST
- Where: Telegram group topic **inbox-dev=585** (참조: topic map `context/telegram_topics/thread_topic_map.json`)
- Goal:
  - (1) DB/State 손실 이후 **반드시 다시 만들어야 하는 것들**을 우선순위로 복구/개발.
  - (2) **Base Batches (3/9)** 데드라인: Vercel URL + 데모 영상 + repo 제출.
- Next:
  - 1) (P0) **Base Batches 데모 패키지 확정**
  - 목표(3/9): Vercel URL + demo video + repo `https://github.com/edmonddantesj/aoi-basebatches-demo`
  - 데모 핵심: Base Sepolia에서 **실제 서명 1 tx** + proof bundle + `/verified` history 뷰.
- Blockers/Risks:
  - Base Batches 제출까지 시간이 짧음(3/9). 영상/배포/tx proof가 병목.
  - GitHub 토큰 권한 설정이 꼬이면 자동화/복구가 계속 막힐 수 있음.

### HF_handoff_compact_reminder_202603.md — handoff(586): DAILY COMPACT 스냅샷 리마인더 자동화(09:30 KST)

- Owner: 청비/record

### HF_v6_invest_live_restart_202603.md — v6-invest(1029): 실투 재개발/운영 복구 SSOT 및 반복업무 자동화

- Status: ACTIVE
- Owner: 청뇌
- Last updated: 2026-03-08 07:03 KST
- Where: Telegram topic **v6-invest=1029**
- Goal:
  - `/openclaw` 삭제/DB 부재 상태에서도 v6 투자 운영의 연속성을 복원.
  - 이전 대화에서 확정된 규칙/실패 교정 지점을 SSOT화.
  - V6 실투 엔진은 현재는 **재개발 전제**로 처리하고, 새 개발 포인트를 받으면 즉시 라이브 붙임.
- Next:
  - 1) inbox-dev에서 전달될 새 V6 개발 공지 수신 후 즉시 통합:
  - 실행 루틴 매핑(실행 명령, env, approval)
  - 라이브/DRY_RUN 분기별 재확인

### HF_x-post.md — x-post(956): 브라우저 기반 후보발굴/본문추출 파이프라인 안정화 + 3회/일 산출 루틴 고정

- Status: ACTIVE
- Owner: 청묘 / growth / 메르세데스
- Last updated: 2026-03-08 06:40 KST
- Where: Telegram topic 956 (x-post), SSOT: `context/topics/x-post_PLAYBOOK_V0_1.md`
- Goal:
  - 매일 3회(08:10/12:10/18:10 KST) **후보3 + 선정1(C톤 20~35줄 + AOI 증빙 + 인용박스)** 산출을 안정적으로 만든다.
  - **자동 게시 금지** 원칙은 유지한다(산출물만 제공).
- Next:
  - 1) (운영) 3회 스케줄에 맞춘 **산출물 생성 루틴**을 자동 트리거(launchd or Ralph Loop)로 고정
  - 2) (기술) 발굴 엔진 1개 확정
  - A) OpenClaw 브라우저 릴레이 기반(탭 attach 필요)
- Blockers/Risks:
  - X UI/DOM 변경, 로그인/제한/캡차에 의한 중단
  - 브라우저 자동화 시 계정 리스크(가드레일 준수 필수)
  - 메모리/리소스 압박으로 인한 추출 불안정

### HF_moltbook_ops_202603.md — moltbook(1114): 운영 복구(키/스크립트/SSOT) + Daily/Weekly 루프 자동화

- Last updated: 2026-03-08
- Next:
  - ### A. 복구(내부) — 최소 동작 세트
  - [ ] Moltbook Developers: 키 재발급/복구 루트 확정 (apply → create app → key)
  - [ ] 키 저장 SSOT 확정 (OpenClaw secrets vs `~/.config/moltbook/credentials.json`)

### HF_topic81_basebatches_submission_package_202603.md — topic81: Base Batches 제출 패키지(500 words + 인터뷰 + 데모) SSOT 합본

- Status: ACTIVE
- Owner: 청묘
- Last updated: 2026-03-08 06:40 KST
- Where: Telegram topic 81 (Random) → SSOT로 승격
- Goal:
  - Base Batches 제출 폼 요구사항(특히 500 words) 원문 확보
  - 제출 패키지 1장(SSOT)로 합본: 핵심 문구 + 링크 + 데모/증빙 번들
- Next:
  - Base Batches 공식 제출 폼 질문(원문) 확보 (URL/스크린샷/텍스트)
  - 500 words 초안 작성(버전관리) + 검증 체크리스트 정의
  - 데모/증빙(Receipt/Proof bundle) 최소 세트 확정 및 링크 수집
- Blockers/Risks:
  - 제출 폼 원문을 아직 확보하지 못함(외부 링크/스크린샷 필요)

### HF_aoi_pro_install_quickstart_preflight_202603.md — aoi-pro: 설치/퀵스타트 Preflight(노드/경로/라이선스)로 성공률 개선

- Status: ACTIVE
- Owner: 청묘
- Last updated: 2026-03-08 06:40 KST
- Where: Telegram topic 81 (Random) + 베타테스터 온보딩
- Goal:
  - 설치/실행 전에 “사전 점검(Preflight)”을 넣어 **폴백=BLOCKED+가이드**로 전환
  - 테스터가 겪는 반복 병목(Windows bash/권한/Defender/프록시/터미널 혼동)을 표준 분기로 흡수
- Next:
  - Preflight 체크리스트(노드 설치/가동, 경로, 라이선스/모드, 권한/네트워크) SSOT 문서화
  - Windows 분기(WSL2 vs Git Bash) 복붙 안내문 템플릿 고정
  - 실패 시 표준 리포트 포맷(STATUS/PROOF/BLOCKED/NEXT) 템플릿 배포
- Blockers/Risks:
  - 제품/리포 구조(설치 스크립트/퀵스타트 문서 위치)에 대한 최신 SSOT가 필요

### HF_render_502_warmup_retry_policy_202603.md — render: 502 워밍업/재시도 정책 SSOT 확정

- Status: ACTIVE
- Owner: 청묘
- Last updated: 2026-03-08 06:40 KST
- Where: Telegram topic 81 (Random)
- Goal:
  - 간헐적 `502 Bad Gateway`를 “운영적으로 해결”하기 위한 표준 정책 확정
  - 기준: 단발 회피가 아니라 **최종 성공률 확보** (retry/backoff/timeout)
- Next:
  - 대상 엔드포인트/컴포넌트 식별(어떤 요청에서 502가 나는지)
  - retry 정책(최대 횟수/백오프/타임아웃/서킷브레이커) SSOT로 고정
  - 워밍업(`/health`) 실행 여부 및 위치(클라이언트/서버) 결정
- Blockers/Risks:
  - 실제 운영 스택/레포 경로를 먼저 특정해야 함

### HF_aoi_pro_lite_lifetime_spec_202603.md — aoi-pro: Lite 평생권($0.01) 스펙/가드레일 숫자 확정

- Status: ACTIVE
- Owner: 청묘
- Last updated: 2026-03-08 06:40 KST
- Where: Telegram topic 81 (Random)
- Goal:
  - AOI PRO Lite 평생권(한정기간, $0.01) 판매 설계의 **조건/가드레일/숫자**를 확정
  - 시빌/지원부하 방지 조건을 SSOT로 고정
- Next:
  - 판매 기간/한정 수량/대상(테스터 전용 등) 확정
  - 시빌 방지: 결제/계정/그룹/디바이스/레이트 리밋 정책 설계
  - 지원 부하 방지: 지원 채널/응답 SLA/범위(무상 지원 범위) 명시
- Blockers/Risks:
  - 가격/결제(돈) 관련이라 승인 프로세스가 필요
