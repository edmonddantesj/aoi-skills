# Docs Recovery Status Audit — 2026-03-12

**Status:** SSOT audit snapshot  
**Scope:** inbox-dev / AOI docs recovery  
**Classification:** INTERNAL  
**Method:** Workspace + `repos/aoi-ssot` 실물 파일 기준 존재 여부/완성도 점검

---

## TL;DR

현재 문서 복구 상태는 **"완전 미복구"가 아니라, 영역별로 `정본 일부 완료 / 초안 존재 / 골격만 존재`가 혼재한 상태**다.

- **Brandbook 패키지:** 정본 초안 세트 존재
- **Tokenomics:** SSOT v0.1 + reconstructed v0.2 존재
- **Whitepaper / One-pager:** 생존본 + public one-pager 존재
- **OPUS 7 Phases:** 1~7 문서 파일은 전부 존재하지만, **실질 완성도는 Phase별 편차 큼**
- **Master Spec / V6 Ops-Spec:** 존재하지만 아직 전면 완성본으로 보긴 어려움

---

## 1. Whitepaper / One-pager

### 1.1 Surviving technical whitepaper
- **Path:** `repos/aoi-ssot/strategy/AOI_Tech_Whitepaper_v1.0.md`
- **Status:** **생존본 존재 (기준점 확보)**
- **Assessment:** 복구의 기준 원본 역할 가능. 현재 감사 턴에서는 내용 전문 검토는 미실시.

### 1.2 Public one-pager
- **Path:** `context/recovery/AOI_WHITEPAPER_ONEPAGER_PUBLIC_V0_2.md`
- **Status:** **초안 이상 / 사용 가능 수준**
- **Assessment:** 외부 공개 안전한 서술로 정리되어 있으며, AOI Core / DB-less architecture / governance 요약이 채워져 있음.
- **Caveat:** `Status: SSOT` 헤더는 없음. 현재 표현상 "public-safe summary"에 가까움.

---

## 2. Tokenomics

### 2.1 VC-inclusive tokenomics SSOT
- **Path:** `context/tokenomics/AOI_TOKENOMICS_V2_1_VC_INCLUSIVE_ARCHITECTURE_SSOT_V0_1.md`
- **Status:** **정본 후보 존재**
- **Assessment:** 공급량/배분표/SCFP 모델 등 핵심 섹션이 실제로 채워져 있음.
- **Caveat:** 헤더가 `Status: DRAFT`라서 "정본 SSOT 완결"로 잠그려면 추가 승격 필요.

### 2.2 Reconstructed TOP_SECRET tokenomics
- **Path:** `context/recovery/TOKENOMICS_TOP_SECRET_RECONSTRUCTED_V0_2.md`
- **Status:** **복구 초안 존재**
- **Assessment:** 유실 문서 복원 레일의 결과물로 보관 중. 근거 엄수용 복구문서 성격.

---

## 3. Brandbook package

### 3.1 Brandbook
- **Path:** `context/brandbook/BRANDBOOK_V0_1.md`
- **Status:** **초안 세트 존재**
- **Assessment:** 정체성/원칙/분류체계(OPEN/TEASER/STEALTH/TOP_SECRET) 포함.
- **Caveat:** `Status: DRAFT v0.1`

### 3.2 Naming System
- **Path:** `context/brandbook/NAMING_SYSTEM_V0_1.md`
- **Status:** **존재**

### 3.3 Voice & Tone
- **Path:** `context/brandbook/VOICE_AND_TONE_V0_1.md`
- **Status:** **존재**

### 3.4 Visual Spec
- **Path:** `context/brandbook/VISUAL_SPEC_V0_1.md`
- **Status:** **존재**

### Brandbook package summary
- **Overall status:** **패키지 파일 4종 실존 확인**
- **Assessment:** "브랜드북이 없다"가 아니라, **패키지 초안 세트가 이미 있는 상태**
- **Next step:** tone/visual/naming을 실제 브랜드 운영 정본으로 승격 필요

---

## 4. OPUS Phases 1–7

### 4.1 Master spec
- **Path:** `context/opus_phases/OPUS_PHASES_1_TO_7_MASTER_SPEC_V0_1.md`
- **Status:** **존재 / 요약형 master spec**
- **Assessment:** 각 phase의 intent/evidence를 정리한 통합 인덱스 역할은 가능.
- **Caveat:** fully expanded spec은 아님.

### 4.2 Phase-by-phase file existence
- `PHASE_1_SURVIVAL_2_1_V0_1.md` → 존재
- `PHASE_2_SDNA_PROTOCOL_V0_1.md` → 존재
- `PHASE_2_SDNA_PROTOCOL_V0_2.md` → 존재
- `PHASE_3_NEXUS_ORACLE_OMEGA_V0_1.md` → 존재
- `PHASE_4_NINE_SKILLS_LINEUP_V0_1.md` → 존재
- `PHASE_5_GUARDIAN_SENTRY_V0_1.md` → 존재
- `PHASE_6_NEXUS_BAZAAR_V0_1.md` → 존재
- `PHASE_7_STEALTH_STRATEGY_V0_1.md` → 존재

### 4.3 Quality snapshot
- **Phase 1:** 과거 로그상 complete 보고 있었으나, 이번 턴 실물 본문 점검은 미실시
- **Phase 2:** V0.2까지 존재 → 현재 7개 중 가장 진척된 축으로 판단
- **Phase 3:** 실물 확인 결과 **template 수준** (`Status: SSOT (draft)`, 항목 다수 비어 있음)
- **Phase 4~7:** 이번 턴에서는 존재만 확인, 완성도 본문 감사는 미실시

### OPUS phases summary
- **Overall status:** **"7개 전부 미복구" 아님**
- 더 정확히는: **파일 세트는 복구되어 있고, Phase 2는 비교적 진척, 나머지는 일부 skeleton/초안 가능성 높음**

---

## 5. Limitless / Alpha Oracle V6

### 5.1 Ops spec
- **Path:** `context/limitless/LIMITLESS_V6_OPS_SPEC_V0_1.md`
- **Status:** **존재**
- **Assessment:** V6 운영 스펙 트랙이 완전 유실된 상태는 아님.
- **Caveat:** 본문 완성도는 별도 심층 감사 필요.

---

## 6. Repo-side SSOT traces (`repos/aoi-ssot`)

실물 확인된 주요 파일:
- `repos/aoi-ssot/context/aoi_core/AOI_MISSION_MANIFESTO_V0_1.md`
- `repos/aoi-ssot/context/guild/GUILD_OPERATING_REGULATIONS_V0_1.md`
- `repos/aoi-ssot/context/tokenomics/AOI_TOKENOMICS_V2_1_VC_INCLUSIVE_ARCHITECTURE_SSOT_V0_1.md`
- `repos/aoi-ssot/context/NEXUS_BAZAAR_DEMO_ONEPAGER_V0_1.md`

**Assessment:** 적어도 일부 문서는 로컬 임시 초안이 아니라, `aoi-ssot` 경로에도 살아 있음.

---

## 7. Final status matrix

| Domain | Current status | Notes |
|---|---|---|
| Whitepaper (surviving base) | 기준점 확보 | `AOI_Tech_Whitepaper_v1.0.md` 생존 |
| Public One-pager | 초안 이상 | 공개 안전 요약본 존재 |
| Tokenomics SSOT | 초안/정본 후보 | v2.1 문서 실존, 다만 DRAFT |
| Tokenomics reconstructed | 복구 초안 존재 | v0.2 존재 |
| Brandbook package | 4종 패키지 존재 | 전부 존재, 승격 필요 |
| OPUS Master Spec | 존재 | 요약형 master spec |
| OPUS Phase 1–7 | 파일 전부 존재 | 완성도 편차 큼, Phase 3는 skeleton 확인 |
| Limitless V6 Ops-Spec | 존재 | 심층 완성도 감사 필요 |

---

## 8. Operational conclusion

이번 감사 기준 결론:

1. **문서 복구는 이미 시작됐고, 적지 않은 파일이 실존한다.**
2. 문제는 "없음"보다 **"있지만 draft/skeleton/partial completion 상태"** 인 항목이 많다는 점이다.
3. 따라서 다음 실행은 새로 발명하는 게 아니라:
   - 실존 문서를 기준점으로 삼고
   - evidence bundle을 보강하고
   - `DRAFT → SSOT (Complete)` 승격 순서로 가는 게 맞다.

---

## 9. Next action lock

다음 우선순위는 아래 순서로 잠근다.

1. **OPUS Phase 1~7 완성도 감사** (특히 3~7)
2. **Whitepaper / One-pager / Tokenomics 문장/근거 승격**
3. **Brandbook 패키지 DRAFT → 운영정본 승격**
4. **결과를 `aoi-ssot` 정본 repo 기준으로 재정렬**
