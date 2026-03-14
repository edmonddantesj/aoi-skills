# Post-Restart Resume Notice Templates V0.1

## Purpose
When the server/gateway/agent dies and later resumes, use these short templates to notify topics that work may have been interrupted and can now resume from durable state.

---

## 1) Generic short template
재개 공지다냥.

중간에 서버/에이전트가 죽었다가 복귀한 정황이 확인됐다.
이 토픽 작업도 일부 중단/누락 가능성이 있어 durable state 기준으로 재개를 건다.

- current known state:
- what may have been interrupted:
- what resumes automatically:
- blocker / human gate:
- next:

기억 추정이 아니라 playbook / handoff / topic-state / proof 기준으로 이어간다냥.

---

## 2) Technical topic template (inbox-dev / ops / v6-invest / bazaar etc.)
재개 공지다냥.

중간에 서버/에이전트가 죽었다가 복귀한 정황이 확인됐다.
이 토픽은 기술/운영 성격이 있어 아래 기준으로 재개한다.

- current known state:
- affected scope:
- possible missed job / interrupted run:
- failure mode (if known):
- what resumes automatically:
- blocker / human gate:
- next:

durable source:
- playbook:
- handoff/HF:
- topic-state/proof:

---

## 3) Submission / external-output topic template (hackathons / moltbook etc.)
재개 공지다냥.

중간에 서버/에이전트가 죽었다가 복귀한 정황이 확인됐다.
초안/정리/리서치 작업은 재개 가능하지만, 최종 제출/외부 반영은 계속 human gate 유지다냥.

- current known state:
- interrupted support/draft work:
- what resumes automatically:
- what still needs human approval:
- next:

durable source:
- playbook:
- handoff/HF:
- proof/artifacts:

---

## 4) Ops incident template
재개 공지다냥.

중간 다운타임/재시작이 있었고 현재는 복귀 상태다.
원인 파악은 ops에서 맡고, main/각 토픽은 L1/L2 범위 복구와 중단 미션 재개에 집중한다.

- current known state:
- incident owner:
- possible missed jobs/topics:
- controllable recovery already done:
- blocker / human gate:
- next:

---

## Rule
- Do not pretend uninterrupted uptime.
- Prefer short factual notices over vague reassurance.
- Resume from durable state, not memory guesswork.
- Keep human gate explicit for risky/external actions.
