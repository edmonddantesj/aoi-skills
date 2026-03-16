# HF: topic81 내부 QA — 예약 링크/필터/추천 로직 정제

- **Status:** ACTIVE
- **Owner:** 청묘(Aoineco)
- **Last updated:** 2026-03-16 11:29 KST
- **Where:** Telegram topic 81 (Random)

## Goal
- 외부 테스트(소띠 아빠방) 전에 내부 QA 단계로서 아래 5가지를 tracked execution 상태로 전환한다.
- 대상:
  1. 실예약 링크 alive check
  2. 구/연령/카테고리 필터 정교화
  3. 추천 로직 다듬기
  4. 이상 항목/중복/가짜 예약가능 정리
  5. 내부 QA 후 외부 테스트 가능/불가 판정

## Current state (what works / what’s broken)
- 2026-03-16 오전 대화에서 위 작업을 “진행중”처럼 말했으나, 실제 workspace 기준 tracked artifact/HF/checklist/proof가 없어서 운영상 **미진행 / 미기록** 상태였음.
- 현재 이 HF 생성으로 해당 작업을 처음으로 durable tracked state에 올림.
- 아직 실제 서비스/데이터/레포 경로가 이 HF에 연결되지 않아, 1차로는 범위/체크리스트/증빙 규격을 고정하는 단계.

## Decisions made
- 이 작업은 random 본문에 계속 쌓지 않고 HF로 추적한다.
- 외부 테스트 전 단계는 반드시 **내부 QA 완료 + proof 남김** 기준으로만 통과 판정한다.
- 상태 표현은 가능/추천형이 아니라 proof-first로 남긴다.
- 이름/역할 표기는 HQ roster 기준 canonical 형식을 따른다.

## Next actions (ordered)
1. 관련 서비스/레포/데이터 경로 식별 및 이 HF에 연결
2. QA 체크리스트 문서 생성 및 통과 기준 고정
3. 각 항목별 결과를 proof와 함께 누적
4. 외부 테스트 가능/불가를 one-line verdict로 기록

## Commands / paths / proofs
- HF created: `context/handoff/HF_topic81_internal_qa_reservation_discovery_202603.md`
- Checklist path: `context/checklists/TOPIC81_INTERNAL_QA_RESERVATION_DISCOVERY_CHECKLIST_V0_1.md`
- Related topic state: `context/topic-state/random.md`
- Related playbook: `context/topics/random_PLAYBOOK_V0_1.md`

## Risks / blockers
- 실제 QA 대상 서비스/레포/데이터 위치가 아직 이 HF에 매핑되지 않음
- 링크 alive check는 네트워크/서비스 접근 상태에 따라 추가 증빙이 필요할 수 있음
- 추천/필터 품질 평가는 샘플 데이터셋 또는 운영 기준이 없으면 주관화될 수 있음
