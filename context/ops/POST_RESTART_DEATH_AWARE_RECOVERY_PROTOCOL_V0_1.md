# Post-Restart / Death-Aware Recovery Protocol V0.1

## Purpose
OpenClaw or the host may die and come back. When the assistant resumes after an unexpected outage/restart, it should not behave as if nothing happened.
This protocol defines the minimum recovery behavior after a detected restart/outage.

## Trigger condition
Treat the situation as a restart/outage recovery case if one or more are true:
- the agent/session was interrupted unexpectedly
- the host/gateway died and later came back
- there is a visible gap suggesting the assistant was unavailable during expected work
- the user explicitly says the server/agent died
- cron/topic work that should have happened appears missing or interrupted

## Core behavior after restart
When recovery mode is triggered, do the following in order.

### 1) Acknowledge death/restart state
Do not pretend continuous uptime.
If relevant, explicitly recognize that the system died/restarted and resumed.

### 2) Check whether ops already owns root-cause analysis
- If ops already has the incident, do not duplicate the investigation from main.
- If no ops handling exists and there is a meaningful risk/incident, request root-cause analysis in ops.

### 3) L1/L2 controllable recovery
If the situation is controllable within L1/L2 bounds, perform recovery-safe actions such as:
- state/status checks
- gateway/node health checks
- verifying whether scheduled jobs resumed
- restoring durable context from playbooks/handoff/topic-state
- asking for human approval before restart/model-switch/config changes when required

Do not cross human-gate boundaries automatically.

### 4) Sweep interrupted missions across topics
Check active/important topics and determine whether work may have been interrupted.
Priority topics should include at minimum:
- ops
- inbox-dev
- hackathons
- adp
- bazaar
- v6-invest
- moltbook
- any topic explicitly active in recent handoff/state

For each topic, determine:
- what was expected to continue
- whether a cron/automation/report may have been missed
- whether a human-facing announcement or restart note is needed
- whether there is enough durable state to resume safely

### 5) Resume-notice behavior
If a topic likely had interrupted work, post a short recovery/resume notice so work can restart without guessing.
Preferred content:
- restart/outage was recognized
- current known state / whether interruption may have happened
- what will resume automatically vs what needs human input
- any blocker / human gate

### 6) Prefer durable resumption over memory guessing
Use:
- playbooks
- handoff/HF
- topic-state
- proof artifacts
- saved outputs
Do not guess continuity from vibes or partial memory.

## Ops escalation rule
Request/route root-cause analysis to ops when:
- server death cause is unknown
- gateway/process instability may recur
- scheduled jobs may be silently failing
- restart loops or repeated downtime are suspected
- there may be data loss / drift / corruption

Suggested support request shape:
- Topic: ops
- Priority: P0/P1
- Current state: agent/server died and resumed
- Goal: determine root cause and propose containment/fix
- Needed support: incident triage / logs / recovery checklist / prevention plan
- Expected output type: checklist / incident memo / ops runbook update
- Affected scope: gateway / node / launchd / cron / host
- Failure mode: downtime / restart / missed jobs / possible drift

## Human gate boundaries
Remain fail-closed for:
- restart/model-switch/config changes outside L1/L2
- service install/remove
- firewall/network/remote access changes
- destructive cleanup
- external/public actions not already approved

## Desired end state
After a restart/outage:
1. the outage is recognized
2. ops owns root-cause analysis if needed
3. controllable recovery is handled within L1/L2 bounds
4. interrupted topic missions are scanned
5. restart/resume notices are posted where needed
6. work restarts from durable state, not guesswork
