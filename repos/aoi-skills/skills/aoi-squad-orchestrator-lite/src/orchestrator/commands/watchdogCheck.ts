import { CommandContext, TransitionResult, runCommand } from "./runCommand";
import { EventRecord } from "../types";
import { isHardTimeout, isSoftTimeout } from "../watchdog/timeout";
import { makeEventId } from "../utils/ids";

export interface WatchdogCheckInput {
  expectedRevision: number;
}

export async function watchdogCheck(
  ctx: CommandContext,
  input: WatchdogCheckInput
): Promise<TransitionResult> {
  return runCommand(ctx, async (state) => {
    if (!state.watchdog?.enabled || !state.currentTurn || state.mode === "recovering") {
      return { next: state, events: [] };
    }
    if (state.revision !== input.expectedRevision) {
      return { next: state, events: [] };
    }

    const nowIso = new Date().toISOString();
    const nowTs = Date.now();
    const turn = state.currentTurn;
    const next = structuredClone(state);
    const events: EventRecord[] = [];

    if (isHardTimeout(turn, nowTs)) {
      const previousOwner = turn.owner;
      next.revision += 1;
      next.updatedAt = nowIso;
      next.currentTurn.owner = "planner";
      next.currentTurn.status = "needs_replan";
      next.currentTurn.lastProgressAt = nowIso;
      next.currentTurn.deadlineAt = null;
      next.currentTurn.leaseVersion += 1;
      next.flags.blocked = false;
      next.flags.softTimedOut = false;
      next.agents[previousOwner].status = "idle";
      next.agents[previousOwner].lastSeenAt = nowIso;
      next.agents[previousOwner].lastTurnId = turn.turnId;
      next.agents.planner.status = "active";
      next.agents.planner.lastSeenAt = nowIso;
      next.agents.planner.lastTurnId = turn.turnId;
      next.lastDecision = {
        selectedAgent: "planner",
        reason: "hard_timeout",
        at: nowIso,
      };
      next.watchdog = {
        ...(next.watchdog ?? { enabled: true, lastCheckedAt: null, lastOutcome: null }),
        lastCheckedAt: nowIso,
        lastOutcome: "hard_timeout",
      };
      events.push({
        eventId: makeEventId("hard_timeout"),
        type: "turn_preempted",
        at: nowIso,
        runId: next.runId,
        commandId: ctx.commandId,
        actor: "system",
        turnId: turn.turnId,
        revision: next.revision,
        severity: "warn",
        data: {
          from: previousOwner,
          to: "planner",
          reason: "hard_timeout",
          previousDeadlineAt: turn.deadlineAt,
        },
      });
      return { next, events };
    }

    if (isSoftTimeout(turn, nowTs) && !state.flags.softTimedOut) {
      next.revision += 1;
      next.updatedAt = nowIso;
      next.flags.softTimedOut = true;
      next.watchdog = {
        ...(next.watchdog ?? { enabled: true, lastCheckedAt: null, lastOutcome: null }),
        lastCheckedAt: nowIso,
        lastOutcome: "soft_timeout",
      };
      events.push({
        eventId: makeEventId("soft_timeout"),
        type: "timeout_detected",
        at: nowIso,
        runId: next.runId,
        commandId: ctx.commandId,
        actor: "system",
        turnId: turn.turnId,
        revision: next.revision,
        severity: "warn",
        data: {
          level: "soft",
          owner: turn.owner,
          lastProgressAt: turn.lastProgressAt,
          deadlineAt: turn.deadlineAt,
          reason: "no_progress_within_soft_window",
        },
      });
      return { next, events };
    }

    return { next: state, events: [] };
  });
}
