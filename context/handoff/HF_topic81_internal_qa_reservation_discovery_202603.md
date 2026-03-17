# HF: topic81 내부 QA — 예약 링크/필터/추천 로직 정제

- **Status:** DONE ✅
- **Owner:** 청묘(Aoineco)
- **Last updated:** 2026-03-17 16:10 KST
- **Where:** Telegram topic 81 (Random)

## Goal (완료)
- 외부 테스트 전 내부 QA 5개 항목 전부 완료

## 완료 항목
1. ✅ 실예약 링크 alive check (132개 → 124개 정상, 8개 URL 수작업 보완)
2. ✅ 구/연령/카테고리 필터 정교화 (age_min/max 파싱, category_tag 5개 통합)
3. ✅ 추천 로직 v2 (연령적합도/수용인원/URL품질/카테고리 다양성 4기준 종합)
4. ✅ 이상항목/중복/가짜 예약가능 정리 (rank=128 EXCLUDE, rank=131 DEMOTE)
5. ✅ 데이터 확장:
   - B-1: seoulfuture365 URL 35개 보완, 11개 단순안내→예약가능 업그레이드
   - B-2: yeyak API 전량 수집 (서울 열린데이터광장 API 키 발급) → 239개 추가
   - 최종 DB: **132 → 378개**

## 산출물
- `artifacts/seoul_childcare/childplay_reservable_focus_2026-03-15.json` (378개, score_v2 전체)
- `artifacts/seoul_childcare/link_alive_check_2026-03-17.json`
- `artifacts/seoul_childcare/yeyak_child_full_2026-03-17.json` (API 전량 원본)
- `artifacts/seoul_childcare/childplay_top_picks_v3_2026-03-17.md` (최종 픽스)
- `artifacts/seoul_childcare/seoulfuture365_expanded_candidates_2026-03-15.json` (URL 보완됨)

## 최종 데이터 요약 (378개 확정)
- **Top 5 (5세 기준):** 1~5위 서울형 키즈카페 (공공 직링크 + 연령 적합 조합 최강)
- **특색시설 Top 5:** 광나루한강 생태공원, 공평도시유적전시관, 여의샛강생태체험관, 중랑캠핑숲, 암사생태공원
- **지역별 분포:** 동작구(31) > 양천구(25) > 종로구(22) > 광진구(21) > 중구(19)
- **분석:** 서울형 키즈카페가 공공 예약 시스템과의 연동성이 가장 우수하며, 생태공원/박물관 체험시설이 주말 가족 단위 예약의 핵심 자산임.

## 서비스명 확정
- 내부 코드명: `childplay`
- **서비스 도메인: `playground.aoineco.ai`** (에드몽 확정)
- 서울 열린데이터광장 API 키: `~/.zshrc`의 `SEOUL_API_KEY`

## 다음 재개 포인트
1. playground.aoineco.ai 사이트 구축 (청섬 or Antigravity)
2. 378개 DB → API 엔드포인트 연결
3. 구/연령/카테고리 필터 UI 구현
4. 에드몽 직접 테스트 후 소띠 아빠방 외부 배포

## Commits (오늘)
- `5fe03ef` — URL 수작업 보완 8개
- `7b46d9f` — 필터 정교화
- `6a8d61a` — score_v2
- `ee76481` — QA pass
- `0ad523c` — B-1 seoulfuture365 URL enrich
- `6bbf4dc` — B-2 신규 7개
- `d06b631` — B-2 yeyak API 239개 추가
- `87b2f2f` — v3 재계산
