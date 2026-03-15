import { CommandContext, TransitionResult, runCommand } from "./runCommand";
import { OrchestratorError } from "../errors";
import { AgentId, EventRecord } from "../types";
import { makeEventId } from "../utils/ids";

export interface CloseTurnInput {
  agent: AgentId;
  expectedRevision: number;
  expectedTurnId: string;
  expectedLeaseVersion: number;
  outcome: "approved" | "completed" | "cancelled";
  summary: string;
}

export async function closeTurn(
  ctx: CommandContext,
  input: CloseTurnInput
): Promise<TransitionResult> {
  return runCommand(ctx, async (state) => {
    if (!state.currentTurn) throw new OrchestratorError("INVALID_TRANSITION", "No current turn");
    if (state.revision !== input.expectedRevision) throw new OrchestratorError("REVISION_MISMATCH", "Revision mismatch", true);
    if (state.currentTurn.owner !== input.agent) throw new OrchestratorError("INVALID_OWNER", "Only owner can close");
    if (state.currentTurn.turnId !== input.expectedTurnId) throw new OrchestratorError("TURN_ID_MISMATCH", "Turn mismatch");
    if (state.currentTurn.leaseVersion !== input.expectedLeaseVersion) throw new OrchestratorError("LEASE_MISMATCH", "Lease mismatch", true);

    const now = new Date().toISOString();
    const turnId = state.currentTurn.turnId;
    const next = structuredClone(state);
    next.revision += 1;
    next.updatedAt = now;
    next.mode = "idle";
    next.flags.blocked = false;
    next.flags.needsReview = false;
    next.flags.handoffRequested = false;
    next.flags.softTimedOut = false;
    next.agents[input.agent].status = "idle";
    next.agents[input.agent].lastSeenAt = now;
    next.agents[input.agent].lastTurnId = turnId;
    next.lastDecision = {
      selectedAgent: input.agent,
      reason: `turn_closed:${input.outcome}`,
      at: now,
    };

    const event: EventRecord = {
      eventId: makeEventId("closed"),
      type: "turn_closed",
      at: now,
      runId: next.runId,
      commandId: ctx.commandId,
      actor: input.agent,
      turnId,
      revision: next.revision,
      severity: "info",
      data: {
        outcome: input.outcome,
        summary: input.summary,
      },
    };

    next.currentTurn = null;
    return { next, events: [event] };
  });
}
