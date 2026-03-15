import { describe, expect, it } from "vitest";
import { readEvents } from "../../../src/orchestrator/state/events";
import { watchdogTick } from "../../../src/orchestrator/watchdog/watchdogTick";
import { makeState, makeTempRoot, makeTurn, readSavedState, writeInitialState } from "../helpers";

describe("integration/timeout-watchdog", () => {
  it("records soft timeout without reassigning owner", async () => {
    const root = await makeTempRoot();
    await writeInitialState(root, makeState({
      revision: 200,
      mode: "active",
      flags: { blocked: false, needsReview: false, handoffRequested: false, softTimedOut: false },
      currentTurn: makeTurn({ turnId: "turn_timeout_soft", owner: "executor", status: "in_progress", leaseVersion: 2, startedAt: "2020-03-12T00:00:00.000Z", lastProgressAt: "2020-03-12T00:00:00.000Z", deadlineAt: "2099-01-01T00:00:00.000Z" }),
      agents: {
        planner: { status: "idle", lastSeenAt: null, lastTurnId: null },
        executor: { status: "active", lastSeenAt: null, lastTurnId: "turn_timeout_soft" },
        reviewer: { status: "idle", lastSeenAt: null, lastTurnId: null },
      },
    }));
    await watchdogTick(root);
    const saved = await readSavedState(root);
    expect(saved.flags.softTimedOut).toBe(true);
    expect(saved.currentTurn?.owner).toBe("executor");
    const events = await readEvents(root);
    expect(events[0]?.type).toBe("timeout_detected");
  });

  it("preempts to planner on hard timeout", async () => {
    const root = await makeTempRoot();
    await writeInitialState(root, makeState({
      revision: 300,
      mode: "active",
      flags: { blocked: false, needsReview: false, handoffRequested: false, softTimedOut: false },
      currentTurn: makeTurn({ turnId: "turn_timeout_hard", owner: "executor", status: "in_progress", leaseVersion: 4, startedAt: "2020-03-12T00:00:00.000Z", lastProgressAt: "2020-03-12T00:00:00.000Z", deadlineAt: "2020-01-01T00:00:00.000Z" }),
      agents: {
        planner: { status: "idle", lastSeenAt: null, lastTurnId: null },
        executor: { status: "active", lastSeenAt: null, lastTurnId: "turn_timeout_hard" },
        reviewer: { status: "idle", lastSeenAt: null, lastTurnId: null },
      },
    }));
    await watchdogTick(root);
    const saved = await readSavedState(root);
    expect(saved.currentTurn?.owner).toBe("planner");
    expect(saved.currentTurn?.status).toBe("needs_replan");
    expect(saved.agents.executor.status).toBe("idle");
    expect(saved.agents.planner.status).toBe("active");
    const events = await readEvents(root);
    expect(events[0]?.type).toBe("turn_preempted");
    expect(events[0]?.data).toMatchObject({ from: "executor", to: "planner", reason: "hard_timeout" });
  });
});
