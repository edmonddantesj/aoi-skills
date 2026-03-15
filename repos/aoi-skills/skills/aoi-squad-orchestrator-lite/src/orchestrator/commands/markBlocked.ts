import { CommandContext, TransitionResult, runCommand } from "./runCommand";
import { OrchestratorError } from "../errors";
import { AgentId, EventRecord } from "../types";
import { makeEventId } from "../utils/ids";

export interface MarkBlockedInput {
  agent: AgentId;
  expectedRevision: number;
  expectedTurnId: string;
  expectedLeaseVersion: number;
  reason: string;
  details?: string;
  blockerType?: "dependency" | "ambiguity" | "resource" | "policy" | "system";
}

export async function markBlocked(
  ctx: CommandContext,
  input: MarkBlockedInput
): Promise<TransitionResult> {
  return runCommand(ctx, async (state) => {
    if (!state.currentTurn) throw new OrchestratorError("INVALID_TRANSITION", "No current turn");
    if (state.revision !== input.expectedRevision) throw new OrchestratorError("REVISION_MISMATCH", "Revision mismatch", true);
    if (state.currentTurn.owner !== input.agent) throw new OrchestratorError("INVALID_OWNER", "Only owner can mark blocked");
    if (state.currentTurn.turnId !== input.expectedTurnId) throw new OrchestratorError("TURN_ID_MISMATCH", "Turn mismatch");
    if (state.currentTurn.leaseVersion !== input.expectedLeaseVersion) throw new OrchestratorError("LEASE_MISMATCH", "Lease mismatch", true);

    const now = new Date().toISOString();
    const next = structuredClone(state);
    next.revision += 1;
    next.updatedAt = now;
    next.currentTurn.status = "blocked";
    next.currentTurn.lastProgressAt = now;
    next.flags.blocked = true;
    next.agents[input.agent].status = "blocked";
    next.agents[input.agent].lastSeenAt = now;
    next.agents[input.agent].lastTurnId = next.currentTurn.turnId;
    next.lastDecision = {
      selectedAgent: "planner",
      reason: input.reason,
      at: now,
    };

    const event: EventRecord = {
      eventId: makeEventId("blocked"),
      type: "turn_blocked",
      at: now,
      runId: next.runId,
      commandId: ctx.commandId,
      actor: input.agent,
      turnId: next.currentTurn.turnId,
      revision: next.revision,
      severity: "warn",
      data: {
        reason: input.reason,
        details: input.details ?? null,
        blockerType: input.blockerType ?? null,
      },
    };

    return { next, events: [event] };
  });
}
