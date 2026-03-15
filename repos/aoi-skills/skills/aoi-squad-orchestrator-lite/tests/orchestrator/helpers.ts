import os from "node:os";
import path from "node:path";
import { promises as fs } from "node:fs";
import { createInitialState } from "../../src/orchestrator/state/validate";
import { writeStateAtomic, readState } from "../../src/orchestrator/state/repository";
import { CurrentTurn, OrchestratorState } from "../../src/orchestrator/types";

export async function makeTempRoot(): Promise<string> {
  return await fs.mkdtemp(path.join(os.tmpdir(), "orchestrator-test-"));
}

export function makeTurn(overrides: Partial<CurrentTurn> = {}): CurrentTurn {
  return {
    turnId: "turn_1",
    owner: "planner",
    status: "in_progress",
    startedAt: "2026-03-12T00:00:00.000Z",
    lastProgressAt: "2026-03-12T00:00:00.000Z",
    deadlineAt: "2026-03-12T00:05:00.000Z",
    leaseVersion: 1,
    ...overrides,
  };
}

export function makeState(overrides: Partial<OrchestratorState> = {}): OrchestratorState {
  const base = createInitialState("2026-03-12T00:00:00.000Z", "run_test");
  return {
    ...base,
    ...overrides,
    sharedContext: { ...base.sharedContext, ...(overrides.sharedContext ?? {}) },
    agents: { ...base.agents, ...(overrides.agents ?? {}) },
    allocation: { ...base.allocation, ...(overrides.allocation ?? {}) },
    flags: { ...base.flags, ...(overrides.flags ?? {}) },
    currentTurn: overrides.currentTurn === undefined ? base.currentTurn : overrides.currentTurn,
  };
}

export async function writeInitialState(rootDir: string, state?: OrchestratorState) {
  const initial = state ?? createInitialState("2026-03-12T00:00:00.000Z", "run_test");
  await writeStateAtomic(rootDir, initial);
  return initial;
}

export async function readSavedState(rootDir: string) {
  return await readState(rootDir);
}
