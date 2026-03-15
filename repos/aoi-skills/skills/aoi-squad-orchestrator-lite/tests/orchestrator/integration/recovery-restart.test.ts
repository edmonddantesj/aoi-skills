import path from "node:path";
import { promises as fs } from "node:fs";
import { describe, expect, it } from "vitest";
import { LOCK_FILE, STATE_FILE, TEMP_STATE_FILE } from "../../../src/orchestrator/constants";
import { readEvents } from "../../../src/orchestrator/state/events";
import { recoverState } from "../../../src/orchestrator/state/recovery";
import { makeState, makeTempRoot, writeInitialState } from "../helpers";

describe("integration/recovery-restart", () => {
  it("loads valid state without rewrite by default", async () => {
    const root = await makeTempRoot();
    await writeInitialState(root, makeState({ revision: 70, runId: "old_run_id", mode: "active" }));
    const recovered = await recoverState(root);
    expect(recovered.revision).toBe(70);
    expect(recovered.runId).toBe("old_run_id");
    const events = await readEvents(root);
    expect(events).toHaveLength(0);
  });

  it("falls back to degraded initial state when state.json is corrupted", async () => {
    const root = await makeTempRoot();
    const statePath = path.join(root, STATE_FILE);
    await fs.mkdir(path.dirname(statePath), { recursive: true });
    await fs.writeFile(statePath, "{ this is not valid json", "utf8");
    const recovered = await recoverState(root);
    expect(recovered.mode).toBe("degraded");
    expect(recovered.flags.recovered).toBe(true);
    const events = await readEvents(root);
    expect(events[0]?.type).toBe("state_recovered");
  });

  it("removes leftover lock and temp files during fallback recovery", async () => {
    const root = await makeTempRoot();
    const statePath = path.join(root, STATE_FILE);
    const lockPath = path.join(root, LOCK_FILE);
    const tempPath = path.join(root, TEMP_STATE_FILE);
    await fs.mkdir(path.dirname(statePath), { recursive: true });
    await fs.writeFile(statePath, "broken json", "utf8");
    await fs.writeFile(lockPath, JSON.stringify({ token: "old_lock" }), "utf8");
    await fs.writeFile(tempPath, JSON.stringify({ partial: true }), "utf8");
    await recoverState(root);
    await expect(fs.access(lockPath)).rejects.toBeTruthy();
    await expect(fs.access(tempPath)).rejects.toBeTruthy();
  });
});
