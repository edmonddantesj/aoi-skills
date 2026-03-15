import { promises as fs } from "node:fs";
import path from "node:path";
import { LOCK_FILE, TEMP_STATE_FILE } from "../constants";
import { makeEventId, makeRunId } from "../utils/ids";
import { appendEvent } from "./events";
import { readState, writeStateAtomic } from "./repository";
import { createInitialState } from "./validate";

export interface RecoverStateOptions {
  rotateRunId?: boolean;
}

export async function recoverState(
  rootDir: string,
  options: RecoverStateOptions = {}
) {
  const now = new Date().toISOString();
  const runId = makeRunId();

  try {
    const state = await readState(rootDir);

    if (!options.rotateRunId) {
      return state;
    }

    const next = structuredClone(state);
    next.runId = runId;
    next.updatedAt = now;
    next.recovery = {
      needed: false,
      lastRecoveredAt: now,
      recoveredFrom: "state_json",
      confidence: "high",
    };

    await writeStateAtomic(rootDir, next);
    await appendEvent(rootDir, {
      eventId: makeEventId("recovery_completed"),
      type: "recovery_completed",
      at: now,
      runId: next.runId,
      actor: "system",
      revision: next.revision,
      severity: "info",
      data: {
        source: "state_json",
        mode: next.mode,
        confidence: "high",
      },
    });

    return next;
  } catch {
    const recovered = createInitialState(now, runId);
    recovered.mode = "degraded";
    recovered.flags.recovered = true;
    recovered.recovery = {
      needed: false,
      reason: "state_read_failed",
      startedAt: now,
      recoveredFrom: "initial_fallback",
      confidence: "medium",
      lastRecoveredAt: now,
    };
    recovered.lastDecision = {
      selectedAgent: "planner",
      reason: "recovery_fallback",
      at: now,
    };

    const lockPath = path.join(rootDir, LOCK_FILE);
    const tempPath = path.join(rootDir, TEMP_STATE_FILE);
    await fs.rm(lockPath, { force: true }).catch(() => {});
    await fs.rm(tempPath, { force: true }).catch(() => {});
    await writeStateAtomic(rootDir, recovered);
    await appendEvent(rootDir, {
      eventId: makeEventId("recovery_fallback"),
      type: "state_recovered",
      at: now,
      runId: recovered.runId,
      actor: "system",
      revision: recovered.revision,
      severity: "warn",
      data: {
        source: "initial_fallback",
        reason: "state_read_failed",
        mode: recovered.mode,
      },
    });

    return recovered;
  }
}
