# Antigravity Team Operating Status & Protocol V0.1

Status: DRAFT-OPERABLE
Scope: Aoineco & Co. internal use of Google Antigravity as shared auxiliary IDE / code workbench
Last updated: 2026-03-16

## Goal
전 팀원이 Google Antigravity를 **안전하고 실용적인 공용 보조 작업대/협업 IDE**로 활용할 수 있게 하고,
OpenClaw와 병행하는 운영 체계를 고정한다.

## Current status check
### Confirmed working signals
- Antigravity app is installed and running on macOS host.
- Local user-data directories exist:
  - `~/.antigravity`
  - `~/Library/Application Support/Antigravity`
- OAuth/login flow completed at least once:
  - auth localhost server started/stopped
  - OAuth refresh hook executed
  - authenticated state stored in Antigravity local DB
- Browser onboarding server starts successfully.
- Dedicated browser surface is active through Chrome profile:
  - `~/.gemini/antigravity-browser-profile`
  - remote debugging enabled on `9222`
- Workspace/playground traces exist:
  - `~/.gemini/antigravity/playground/cryo-plasma`
  - `~/.gemini/antigravity/playground/interstellar-granule`
- Agent/interactive editor surfaces initialized.

### Confirmed instability / risk signals
- main log shows uncaught `BigInt` serialization error.
- shared process log shows repeated `fireEvent` undefined exceptions during extension installs.
- agent manager window log shows `Window not found` errors.
- remote tunneling is unavailable in current build/config.
- ptyhost log shows one temp-path sticky-bit error.

## Operational verdict
### Current rating
**보조 작업대 권장**

### Interpretation
Antigravity is beyond pure experiment stage, because login/auth/browser/workspace traces are all real.
A repo-local mini task loop was also validated end-to-end: repo open → agent review → safe task proposal → dependency install → file edit → structured report.
However, it is not yet safe to classify as primary mission-critical dependency due to multiple runtime exceptions.

So current operating interpretation is:
- usable for real work
- suitable for active auxiliary team use
- useful for IDE-local execution loops
- should not yet be the sole critical path for business-critical delivery

## Role split: OpenClaw vs Antigravity
### Keep in OpenClaw
- SSOT / memory / durable documentation
- approvals / risk gates / human gate handling
- task routing / team allocation / escalation
- multi-system workflows
- final operating judgment

### Send to Antigravity
- IDE-local code edits
- repetitive refactor loops
- lint / type / test / build loops
- codebase-local implementation iterations
- hackathon / submission polishing near deadlines

## Standard workflow
1. OpenClaw locks scope, constraints, approval boundary, and team allocation.
2. Antigravity performs implementation/test/refactor loop.
3. Results come back to OpenClaw.
4. OpenClaw writes durable outputs to SSOT / handoff / report / memory.

## Team onboarding interpretation
HQ roster/naming must be used.
Do not guess names or roles when assigning Antigravity work.

### Suggested Antigravity-friendly roles
- 청령(Oracle): workload routing / dispatch / bottleneck relief
- 청섬(Blue-Flash): implementation / prototype / deadline coding
- 청기(Blue-Gear): environment / infra / build / runtime stabilization
- 청정(Blue-Maintainer): smoke test / regression triage / cleanup loops
- 청검(Blue-Blade): safety review / guardrails for risky changes
- 청비(Blue-Record): artifact capture / result packaging / traceability
- 청뇌(Blue-Brain): strategic implementation prioritization
- 청안(Blue-Eye): tool/library option scan and alternatives research

## Hackathon / submission use
Recommended pattern:
1. OpenClaw: scope lock / checklist / approval boundary
2. Antigravity: implementation / debugging / polishing
3. OpenClaw: final assembly / handoff / submission packaging / proof bundle

## Immediate next actions
1. Validate live browser onboarding usability from UI perspective.
2. Validate workspace-open / agent-manager actual task loop with one small repo-local task.
3. Record stable kickoff prompt/rules for Antigravity sessions.
4. If a clean mini-loop succeeds, promote from "보조 작업대 권장" to "보조 작업대 적극 활용".

## One-line operating rule
Use Antigravity as the hands-on IDE workbench; keep OpenClaw as the SSOT/ops/governance brain.
