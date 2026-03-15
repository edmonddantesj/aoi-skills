import { describe, expect, it } from "vitest";
import { OrchestratorError } from "../../../src/orchestrator/errors";
import { acquireLock, readLock, releaseLock } from "../../../src/orchestrator/state/lock";
import { makeTempRoot } from "../helpers";

describe("state/lock", () => {
  it("acquires a lock successfully", async () => {
    const root = await makeTempRoot();
    const lock = await acquireLock(root, {
      owner: "planner",
      pid: 12345,
      runId: "run_test",
      acquiredAt: "2026-03-12T00:00:00.000Z",
      expiresAt: "2099-03-12T00:00:15.000Z",
      token: "token_1",
    });
    expect(lock.token).toBe("token_1");
    const saved = await readLock(root);
    expect(saved?.owner).toBe("planner");
    expect(saved?.token).toBe("token_1");
  });

  it("throws LOCK_BUSY on second acquire", async () => {
    const root = await makeTempRoot();
    await acquireLock(root, {
      owner: "planner",
      pid: 12345,
      runId: "run_test",
      acquiredAt: "2026-03-12T00:00:00.000Z",
      expiresAt: "2099-03-12T00:00:15.000Z",
      token: "token_1",
    });
    await expect(
      acquireLock(root, {
        owner: "executor",
        pid: 99999,
        runId: "run_test_2",
        acquiredAt: "2026-03-12T00:00:01.000Z",
        expiresAt: "2099-03-12T00:00:16.000Z",
        token: "token_2",
      })
    ).rejects.toMatchObject<Partial<OrchestratorError>>({ code: "LOCK_BUSY" });
  });

  it("releases the lock when token matches", async () => {
    const root = await makeTempRoot();
    await acquireLock(root, {
      owner: "planner",
      pid: 12345,
      runId: "run_test",
      acquiredAt: "2026-03-12T00:00:00.000Z",
      expiresAt: "2099-03-12T00:00:15.000Z",
      token: "token_1",
    });
    await releaseLock(root, "token_1");
    const saved = await readLock(root);
    expect(saved).toBeNull();
  });
});
