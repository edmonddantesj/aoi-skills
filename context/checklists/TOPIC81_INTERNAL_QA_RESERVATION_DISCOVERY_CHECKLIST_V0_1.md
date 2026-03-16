# Topic81 Internal QA — Reservation Discovery Checklist V0.1

Status: ACTIVE
Owner: 청묘(Aoineco)
Last updated: 2026-03-16 11:29 KST
Related HF: `context/handoff/HF_topic81_internal_qa_reservation_discovery_202603.md`

## Purpose
외부 테스트 전에 내부 품질 기준을 통과했는지 판단하기 위한 체크리스트.

## Pass gate
아래 5개 축이 모두 최소 기준을 충족해야 외부 테스트 가능 판정:
1. 링크 생존성
2. 필터 정확성
3. 추천 일관성
4. 데이터 청결도
5. 수동 spot QA 결과

## Checklist

### 1) 실예약 링크 alive check
- [ ] 샘플 후보 n건에 대해 링크 응답 성공/실패 기록
- [ ] dead redirect / 404 / 로그인 강제 / 예약불가 패턴 분류
- [ ] 최종 결과를 alive / degraded / dead 로 구분
- Proof:
  - file=
  - url=
  - cmd=

### 2) 구/연령/카테고리 필터 정교화
- [ ] 구 필터가 실제 지역값과 충돌 없이 작동
- [ ] 연령 필터가 누락/모호값 처리 기준을 가짐
- [ ] 카테고리 필터가 중복 taxonomy 없이 동작
- [ ] edge case(다중 카테고리/미상/빈값) 처리 규칙 기록
- Proof:
  - file=
  - sample=
  - rule=

### 3) 추천 로직 다듬기
- [ ] 추천 기준(우선순위 신호) 1차 명시
- [ ] 최소 5건 샘플에 대해 추천 결과 검토
- [ ] 사람이 봐도 이상한 추천 패턴 있는지 기록
- [ ] 보수적 fallback 규칙 존재
- Proof:
  - file=
  - sample=
  - diff=

### 4) 이상 항목/중복/가짜 예약가능 정리
- [ ] 중복 항목 정의 고정
- [ ] 가짜 예약가능 정의 고정
- [ ] 이상 항목 유형별 분류표 생성
- [ ] 제거/숨김/보류 처리 규칙 기록
- Proof:
  - file=
  - count=
  - examples=

### 5) 내부 QA verdict
- [ ] 외부 테스트 가능 / 조건부 가능 / 불가 중 하나로 판정
- [ ] 남은 blocker 명시
- [ ] 다음 액션 1~3개 고정
- Proof:
  - verdict=
  - blocker=
  - next=

## Reporting format
- STATUS:
- PROOF:
- NEXT: 또는 BLOCKED:

## Notes
- “진행중” 단독 사용 금지
- proof 없는 완료 표현 금지
- random 본문에는 긴 로그 대신 pointer만 남긴다
