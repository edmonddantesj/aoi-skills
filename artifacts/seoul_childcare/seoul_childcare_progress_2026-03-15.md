# Seoul Childcare / Kids Activity DB Progress — 2026-03-15

## 이번 턴에서 한 일
- 초기에는 워크스페이스 내 기존 `seoul_kidscafe_list.csv`, `seoul_kidscafe_priority.json` 원본을 찾지 못해, 우선 **PDF 후보군으로 언급된 시설 중 공식 사이트에서 예약/신청 흐름이 보이는 곳**을 대상으로 1차 라벨링 초안을 생성함.
- 이후 prewipe 백업(`/Volumes/Aoineco/macmini-prewipe-backup-2026-03-15-094159`)에서 원본을 찾아 복구함.
- 결과 파일 생성:
  - `artifacts/seoul_childcare/seoul_childcare_integrated_candidates_draft_2026-03-15.csv`
  - `artifacts/seoul_childcare/childplay_integrated_db_draft_2026-03-15.csv`
  - `artifacts/seoul_childcare/childplay_integrated_db_draft_2026-03-15.json`

## 현재 상태
- 서울형 키즈카페 원본: **복구 완료**
- PDF 후보군 기반 통합 초안: **생성 완료**
- childplay용 통합 DB 초안: **생성 완료**
- 라벨링 기준
  - `예약가능`: 공식 사이트에서 관람/입장/체험 예약 페이지 확인
  - `신청가능`: 교육/프로그램/행사 단위 신청 페이지 중심
  - `단순안내`: 일반 안내 중심, 상시 예약형 시설로 보기 어려움

## 1차 통합 후보(공식 웹 검증)
- 국립중앙박물관 어린이박물관 — 예약가능
- 서울역사 어린이박물관 — 예약가능
- 국립민속박물관 어린이박물관 — 예약가능
- 국립어린이과학관 — 예약가능
- 서울상상나라 — 예약가능
- 광나루안전체험관 — 예약가능
- 보라매안전체험관 — 예약가능
- 서울식물원 — 단순안내

## 다음 우선순위
1. 서울형 키즈카페 116개 원본 복구 또는 재수집
2. 기존 키즈카페 목록과 이번 후보군 CSV 병합
3. 각 예약 URL alive check (HTTP 상태 / 로그인 필요 / 실제 예약 가능 여부)
4. `예약가능/신청가능/단순안내` 외에 `서울형키즈카페/박물관/과학관/안전체험관` 서브카테고리 정규화
5. childplay.aoineco.ai에서 바로 쓸 수 있도록 JSON API용 포맷 추가 생성

## 비고
- 이번 초안은 **운영/제품 설계용 가설 DB**에 가깝고, 실제 공개 전에는 링크 유효성/휴관/대상연령을 재검증해야 함.


## 업데이트 — 원본 복구 후 통합 DB 생성
- `seoul_kidscafe_list.csv` 복구본과 PDF 후보군 초안을 병합해 `childplay_integrated_db_draft_2026-03-15.csv/json` 생성
- 현재 총 항목 수: 129
- 그룹별
  - 서울형키즈카페: 121
  - 서울 어린이 체험시설: 8
- 라벨별: {'예약가능': 124, '단순안내': 5}
