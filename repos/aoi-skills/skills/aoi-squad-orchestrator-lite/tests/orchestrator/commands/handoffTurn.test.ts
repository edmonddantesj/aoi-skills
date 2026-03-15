import { describe, expect, it } from "vitest";
import { handoffTurn } from "../../../src/orchestrator/commands/handoffTurn";
import { readEvents } from "../../../src/orchestrator/state/events";
import { makeState, makeTempRoot, makeTurn, readSavedState, writeInitialState } from "../helpers";

describe("commands/handoffTurn", () => {
  it("hands off from planner to executor", async () => {
    const root = await makeTempRoot();
    await writeInitialState(root, makeState({
      revision: 10,
      mode: "active",
      currentTurn: makeTurn({ turnId: "turn_1", owner: "planner", status: "in_progress", leaseVersion: 2 }),
      agents: {
        planner: { status: "active", lastSeenAt: null, lastTurnId: "turn_1" },
        executor: { status: "idle", lastSeenAt: null, lastTurnId: null },
        reviewer: { status: "idle", lastSeenAt: null, lastTurnId: null },
      },
    }));

    const result = await handoffTurn({
      rootDir: root,
      actor: "planner",
      commandId: "cmd_handoff_1",
      issuedAt: "2026-03-12T00:01:00.000Z",
      runId: "run_test",
    }, {
      from: "planner",
      to: "executor",
      expectedRevision: 10,
      expectedTurnId: "turn_1",
      expectedLeaseVersion: 2,
      reason: "spec_ready",
    });

    expect(result.ok).toBe(true);
    expect(result.state?.revision).toBe(11);
    expect(result.state?.currentTurn?.owner).toBe("executor");
    expect(result.state?.currentTurn?.leaseVersion).toBe(3);
    const saved = await readSavedState(root);
    expect(saved.currentTurn?.owner).toBe("executor");
    const events = await readEvents(root);
    expect(events).toHaveLength(1);
    expect(events[0]?.type).toBe("turn_handoff");
  });
});
