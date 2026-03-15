import { describe, expect, it } from "vitest";
import { appendEvent, readEvents } from "../../../src/orchestrator/state/events";
import { EVENTS_FILE } from "../../../src/orchestrator/constants";
import { makeTempRoot } from "../helpers";
import path from "node:path";
import { promises as fs } from "node:fs";

describe("state/events", () => {
  it("appends and reads a single event", async () => {
    const root = await makeTempRoot();

    await appendEvent(root, {
      eventId: "evt_1",
      type: "turn_handoff",
      at: "2026-03-12T00:00:00.000Z",
      runId: "run_events_1",
      actor: "planner",
      turnId: "turn_1",
      revision: 1,
      severity: "info",
      data: { from: "planner", to: "executor" },
    });

    const events = await readEvents(root);
    expect(events).toHaveLength(1);
    expect(events[0]?.eventId).toBe("evt_1");
  });

  it("appends multiple events in order", async () => {
    const root = await makeTempRoot();

    await appendEvent(root, {
      eventId: "evt_1",
      type: "turn_handoff",
      at: "2026-03-12T00:00:00.000Z",
      runId: "run_events_2",
      actor: "planner",
      turnId: "turn_1",
      revision: 1,
      severity: "info",
      data: { step: 1 },
    });

    await appendEvent(root, {
      eventId: "evt_2",
      type: "turn_closed",
      at: "2026-03-12T00:01:00.000Z",
      runId: "run_events_2",
      actor: "reviewer",
      turnId: "turn_1",
      revision: 2,
      severity: "info",
      data: { step: 2 },
    });

    const events = await readEvents(root);
    expect(events).toHaveLength(2);
    expect(events[0]?.eventId).toBe("evt_1");
    expect(events[1]?.eventId).toBe("evt_2");
  });

  it("returns empty array when events file does not exist", async () => {
    const root = await makeTempRoot();
    const events = await readEvents(root);
    expect(events).toEqual([]);
  });

  it("tolerates malformed last line and keeps earlier events", async () => {
    const root = await makeTempRoot();
    const file = path.join(root, EVENTS_FILE);
    await fs.mkdir(path.dirname(file), { recursive: true });
    await fs.writeFile(
      file,
      [
        JSON.stringify({
          eventId: "evt_ok",
          type: "turn_handoff",
          at: "2026-03-12T00:00:00.000Z",
          runId: "run_events_3",
          actor: "planner",
          turnId: "turn_1",
          revision: 1,
          severity: "info",
          data: { ok: true },
        }),
        '{"eventId":"evt_broken"',
      ].join("\n") + "\n",
      "utf8"
    );

    const events = await readEvents(root);
    expect(events).toHaveLength(1);
    expect(events[0]?.eventId).toBe("evt_ok");
  });
});
