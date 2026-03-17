# Announcements Draft — Topic 71 postmortem → proof-first / yellow-lane / fatigue-handoff lock (2026-03-17)

이번 Topic 71 Archive UI Agent 해커톤 시도는 제출 자체는 실패했지만, 실패 원인이 충분히 선명하게 드러난 케이스라 전사 운영 규칙으로 승격한다.

핵심 판단은 다음과 같다.
- 이번 실패의 본질은 Gemini 자체가 아니라 **page-context fidelity + proof discipline failure**였다.
- unstable live path를 main lane에 너무 오래 남긴 것이 제출 전환 실패를 키웠다.
- docs/설명/브랜딩/포장이 proof보다 앞서면 안 된다.
- 피로 누적 상태에서 handoff discipline 없이 계속 미는 방식은 deadline 국면에서 위험하다.

이에 따라 아래 규칙을 canonical로 고정한다.
1. **proof before polish**
2. **yellow lane must be locked before final stretch**
3. **known blocker 발견 시 noncritical work는 병목 주위로 collapse**
4. **fatigue 징후 누적 시 freeze + 4-line handoff packet**
5. **모든 해커톤 push는 최소 1개 reusable company asset package를 남길 것**

추가로 future agent demo는 deeper automation이 흔들려도 최소 아래 triad가 살아남아야 한다.
- 무엇을 읽었는지
- 무엇을 추론했는지
- 다음으로 무엇을 추천하는지

Canonical policy:
- `context/ops/PROOF_FIRST_YELLOW_LANE_AND_FATIGUE_HANDOFF_POLICY_V0_1.md`

Affected lane updates:
- `context/topics/hackathons_PLAYBOOK_V0_1.md`
- `context/topic-state/hackathons.md`
- `context/handoff/HF_hackathons_ralph_transfer_20260314.md`
