import { describe, expect, it } from "vitest";
import { closeTurn } from "../../../src/orchestrator/commands/closeTurn";
import { handoffTurn } from "../../../src/orchestrator/commands/handoffTurn";
import { readEvents } from "../../../src/orchestrator/state/events";
import { makeState, makeTempRoot, makeTurn, readSavedState, writeInitialState } from "../helpers";

describe("integration/happy-path", () => {
  it("completes planner -> executor -> reviewer -> close flow", async () => {
    const root = await makeTempRoot();
    await writeInitialState(root, makeState({
      revision: 100,
      mode: "active",
      currentTurn: makeTurn({ turnId: "turn_happy_1", owner: "planner", status: "in_progress", leaseVersion: 1 }),
      agents: {
        planner: { status: "active", lastSeenAt: null, lastTurnId: "turn_happy_1" },
        executor: { status: "idle", lastSeenAt: null, lastTurnId: null },
        reviewer: { status: "idle", lastSeenAt: null, lastTurnId: null },
      },
    }));

    const h1 = await handoffTurn({ rootDir: root, actor: "planner", commandId: "cmd_happy_1", issuedAt: "2026-03-12T00:05:00.000Z", runId: "run_test" }, { from: "planner", to: "executor", expectedRevision: 100, expectedTurnId: "turn_happy_1", expectedLeaseVersion: 1, reason: "spec_ready" });
    expect(h1.ok).toBe(true);
    const h2 = await handoffTurn({ rootDir: root, actor: "executor", commandId: "cmd_happy_2", issuedAt: "2026-03-12T00:06:00.000Z", runId: "run_test" }, { from: "executor", to: "reviewer", expectedRevision: h1.state!.revision, expectedTurnId: "turn_happy_1", expectedLeaseVersion: h1.state!.currentTurn!.leaseVersion, reason: "implementation_done" });
    expect(h2.ok).toBe(true);
    const closed = await closeTurn({ rootDir: root, actor: "reviewer", commandId: "cmd_happy_3", issuedAt: "2026-03-12T00:07:00.000Z", runId: "run_test" }, { agent: "reviewer", expectedRevision: h2.state!.revision, expectedTurnId: "turn_happy_1", expectedLeaseVersion: h2.state!.currentTurn!.leaseVersion, outcome: "approved", summary: "all good" });
    expect(closed.ok).toBe(true);
    const saved = await readSavedState(root);
    expect(saved.currentTurn).toBeNull();
    const events = await readEvents(root);
    expect(events.map((e) => e.type)).toEqual(["turn_handoff", "turn_handoff", "turn_closed"]);
  });
});
