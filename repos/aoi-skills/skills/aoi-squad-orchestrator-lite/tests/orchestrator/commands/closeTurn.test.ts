import { describe, expect, it } from "vitest";
import { closeTurn } from "../../../src/orchestrator/commands/closeTurn";
import { readEvents } from "../../../src/orchestrator/state/events";
import { makeState, makeTempRoot, makeTurn, readSavedState, writeInitialState } from "../helpers";

describe("commands/closeTurn", () => {
  it("closes the current turn and clears state", async () => {
    const root = await makeTempRoot();
    await writeInitialState(root, makeState({
      revision: 20,
      mode: "active",
      flags: { blocked: false, needsReview: true, handoffRequested: true, softTimedOut: true },
      currentTurn: makeTurn({ turnId: "turn_9", owner: "reviewer", status: "in_review", leaseVersion: 4 }),
      agents: {
        planner: { status: "idle", lastSeenAt: null, lastTurnId: null },
        executor: { status: "idle", lastSeenAt: null, lastTurnId: "turn_9" },
        reviewer: { status: "active", lastSeenAt: null, lastTurnId: "turn_9" },
      },
    }));

    const result = await closeTurn({
      rootDir: root,
      actor: "reviewer",
      commandId: "cmd_close_1",
      issuedAt: "2026-03-12T00:02:00.000Z",
      runId: "run_test",
    }, {
      agent: "reviewer",
      expectedRevision: 20,
      expectedTurnId: "turn_9",
      expectedLeaseVersion: 4,
      outcome: "approved",
      summary: "looks good",
    });

    expect(result.ok).toBe(true);
    expect(result.state?.currentTurn).toBeNull();
    const saved = await readSavedState(root);
    expect(saved.currentTurn).toBeNull();
    const events = await readEvents(root);
    expect(events[0]?.type).toBe("turn_closed");
  });
});
