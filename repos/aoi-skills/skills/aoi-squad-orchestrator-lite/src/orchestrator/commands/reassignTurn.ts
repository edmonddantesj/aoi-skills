import { CommandContext, TransitionResult, runCommand } from "./runCommand";
import { OrchestratorError } from "../errors";
import { AgentId, EventRecord } from "../types";
import { makeEventId } from "../utils/ids";

export interface ReassignTurnInput {
  actor: AgentId;
  expectedRevision: number;
  expectedTurnId: string;
  from?: AgentId | null;
  to: AgentId;
  reason: string;
  force?: boolean;
}

export async function reassignTurn(
  ctx: CommandContext,
  input: ReassignTurnInput
): Promise<TransitionResult> {
  return runCommand(ctx, async (state) => {
    if (!state.currentTurn) throw new OrchestratorError("INVALID_TRANSITION", "No current turn");
    if (input.actor !== "planner" && !input.force) throw new OrchestratorError("INVALID_OWNER", "Only planner can reassign turns");
    if (state.revision !== input.expectedRevision) throw new OrchestratorError("REVISION_MISMATCH", "Revision mismatch", true);
    if (state.currentTurn.turnId !== input.expectedTurnId) throw new OrchestratorError("TURN_ID_MISMATCH", "Turn mismatch");
    if (input.from && state.currentTurn.owner !== input.from) throw new OrchestratorError("INVALID_OWNER", "Current owner mismatch");

    const now = new Date().toISOString();
    const previousOwner = state.currentTurn.owner;
    const next = structuredClone(state);
    next.revision += 1;
    next.updatedAt = now;
    next.currentTurn.owner = input.to;
    next.currentTurn.status = input.to === "planner" ? "needs_replan" : "in_progress";
    next.currentTurn.lastProgressAt = now;
    next.currentTurn.deadlineAt = null;
    next.currentTurn.leaseVersion += 1;

    next.agents[previousOwner].status = "idle";
    next.agents[previousOwner].lastSeenAt = now;
    next.agents[previousOwner].lastTurnId = next.currentTurn.turnId;
    next.agents[input.to].status = "active";
    next.agents[input.to].lastSeenAt = now;
    next.agents[input.to].lastTurnId = next.currentTurn.turnId;

    next.flags.blocked = false;
    next.flags.softTimedOut = false;
    if (input.to !== "reviewer") next.flags.needsReview = false;

    next.lastDecision = {
      selectedAgent: input.to,
      reason: input.reason,
      at: now,
    };

    const event: EventRecord = {
      eventId: makeEventId("reassign"),
      type: "turn_reassigned",
      at: now,
      runId: next.runId,
      commandId: ctx.commandId,
      actor: input.actor,
      turnId: next.currentTurn.turnId,
      revision: next.revision,
      severity: "warn",
      data: {
        from: previousOwner,
        to: input.to,
        reason: input.reason,
        force: input.force ?? false,
        leaseVersionAfter: next.currentTurn.leaseVersion,
      },
    };

    return { next, events: [event] };
  });
}
