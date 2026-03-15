import { CommandContext, TransitionResult, runCommand } from "./runCommand";
import { OrchestratorError } from "../errors";
import { AgentId, EventRecord } from "../types";
import { defaultLeaseMs } from "../watchdog/timeout";
import { makeEventId } from "../utils/ids";

export interface HandoffTurnInput {
  from: AgentId;
  to: AgentId;
  expectedRevision: number;
  expectedTurnId: string;
  expectedLeaseVersion: number;
  reason: string;
  artifacts?: string[];
  summary?: string;
}

export async function handoffTurn(
  ctx: CommandContext,
  input: HandoffTurnInput
): Promise<TransitionResult> {
  return runCommand(ctx, async (state) => {
    if (!state.currentTurn) throw new OrchestratorError("INVALID_TRANSITION", "No current turn");
    if (input.from === input.to) throw new OrchestratorError("INVALID_TRANSITION", "Cannot handoff to the same owner");
    if (state.revision !== input.expectedRevision) throw new OrchestratorError("REVISION_MISMATCH", "Revision mismatch", true);
    if (state.currentTurn.turnId !== input.expectedTurnId) throw new OrchestratorError("TURN_ID_MISMATCH", "Turn ID mismatch");
    if (state.currentTurn.owner !== input.from) throw new OrchestratorError("INVALID_OWNER", "Current owner mismatch");
    if (state.currentTurn.leaseVersion !== input.expectedLeaseVersion) throw new OrchestratorError("LEASE_MISMATCH", "Lease mismatch", true);

    const now = new Date().toISOString();
    const next = structuredClone(state);
    const leaseMs = defaultLeaseMs(input.to);

    next.revision += 1;
    next.updatedAt = now;
    next.mode = "active";
    next.currentTurn.owner = input.to;
    next.currentTurn.leaseVersion += 1;
    next.currentTurn.lastProgressAt = now;
    next.currentTurn.deadlineAt = new Date(Date.now() + leaseMs).toISOString();
    next.currentTurn.status = input.to === "reviewer" ? "in_review" : "in_progress";

    next.agents[input.from].status = "idle";
    next.agents[input.from].lastSeenAt = now;
    next.agents[input.from].lastTurnId = next.currentTurn.turnId;
    next.agents[input.to].status = "active";
    next.agents[input.to].lastSeenAt = now;
    next.agents[input.to].lastTurnId = next.currentTurn.turnId;

    next.flags.handoffRequested = false;
    next.flags.softTimedOut = false;
    next.flags.blocked = false;
    next.flags.needsReview = input.to === "reviewer";

    next.lastDecision = {
      selectedAgent: input.to,
      reason: input.reason,
      at: now,
    };

    const event: EventRecord = {
      eventId: makeEventId("handoff"),
      type: "turn_handoff",
      at: now,
      runId: next.runId,
      commandId: ctx.commandId,
      actor: input.from,
      turnId: next.currentTurn.turnId,
      revision: next.revision,
      severity: "info",
      data: {
        from: input.from,
        to: input.to,
        reason: input.reason,
        artifacts: input.artifacts ?? [],
        summary: input.summary ?? null,
        leaseMs,
        leaseVersionBefore: input.expectedLeaseVersion,
        leaseVersionAfter: next.currentTurn.leaseVersion,
      },
    };

    return { next, events: [event] };
  });
}
