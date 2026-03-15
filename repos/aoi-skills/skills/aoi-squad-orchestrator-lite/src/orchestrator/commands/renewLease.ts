import { CommandContext, TransitionResult, runCommand } from "./runCommand";
import { OrchestratorError } from "../errors";
import { AgentId, EventRecord } from "../types";
import { makeEventId } from "../utils/ids";

export interface RenewLeaseInput {
  agent: AgentId;
  expectedRevision: number;
  expectedTurnId: string;
  expectedLeaseVersion: number;
  extendMs?: number;
  progressNote?: string;
}

export async function renewLease(
  ctx: CommandContext,
  input: RenewLeaseInput
): Promise<TransitionResult> {
  return runCommand(ctx, async (state) => {
    if (!state.currentTurn) throw new OrchestratorError("INVALID_TRANSITION", "No current turn");
    if (state.revision !== input.expectedRevision) throw new OrchestratorError("REVISION_MISMATCH", "Revision mismatch", true);
    if (state.currentTurn.owner !== input.agent) throw new OrchestratorError("INVALID_OWNER", "Only owner can renew lease");
    if (state.currentTurn.turnId !== input.expectedTurnId) throw new OrchestratorError("TURN_ID_MISMATCH", "Turn mismatch");
    if (state.currentTurn.leaseVersion !== input.expectedLeaseVersion) throw new OrchestratorError("LEASE_MISMATCH", "Lease mismatch", true);

    const now = new Date().toISOString();
    const extendMs = input.extendMs ?? 15 * 60 * 1000;
    const next = structuredClone(state);
    next.revision += 1;
    next.updatedAt = now;
    next.currentTurn.lastProgressAt = now;
    next.currentTurn.deadlineAt = new Date(Date.now() + extendMs).toISOString();
    next.agents[input.agent].lastSeenAt = now;
    next.agents[input.agent].lastTurnId = next.currentTurn.turnId;
    next.flags.softTimedOut = false;

    const event: EventRecord = {
      eventId: makeEventId("lease"),
      type: "lease_renewed",
      at: now,
      runId: next.runId,
      commandId: ctx.commandId,
      actor: input.agent,
      turnId: next.currentTurn.turnId,
      revision: next.revision,
      severity: "info",
      data: {
        extendMs,
        progressNote: input.progressNote ?? null,
      },
    };

    return { next, events: [event] };
  });
}
