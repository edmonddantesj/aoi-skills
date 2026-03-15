import { OrchestratorError } from "../errors";
import { STATE_VERSION } from "../constants";
import { AgentId, OrchestratorState } from "../types";

const AGENTS: AgentId[] = ["planner", "executor", "reviewer"];

export function createInitialState(now: string, runId: string): OrchestratorState {
  return {
    version: STATE_VERSION,
    revision: 1,
    updatedAt: now,
    runId,
    mode: "idle",
    currentTurn: null,
    sharedContext: {
      goal: "",
      constraints: [],
      inputs: [],
      artifacts: [],
    },
    agents: {
      planner: { status: "idle", lastSeenAt: null, lastTurnId: null },
      executor: { status: "idle", lastSeenAt: null, lastTurnId: null },
      reviewer: { status: "idle", lastSeenAt: null, lastTurnId: null },
    },
    allocation: {
      strategy: "single-owner-per-turn",
      override: null,
    },
    flags: {
      blocked: false,
      needsReview: false,
      handoffRequested: false,
    },
    lastDecision: null,
    recovery: {
      needed: false,
      lastRecoveredAt: now,
    },
    watchdog: {
      enabled: true,
      lastCheckedAt: null,
      lastOutcome: null,
    },
  };
}

export function assertValidState(state: unknown): asserts state is OrchestratorState {
  if (!state || typeof state !== "object") {
    throw new OrchestratorError("STATE_CORRUPTED", "State is not an object");
  }

  const s = state as Partial<OrchestratorState>;

  if (typeof s.version !== "number") {
    throw new OrchestratorError("STATE_CORRUPTED", "Missing or invalid version");
  }
  if (typeof s.revision !== "number") {
    throw new OrchestratorError("STATE_CORRUPTED", "Missing or invalid revision");
  }
  if (typeof s.updatedAt !== "string") {
    throw new OrchestratorError("STATE_CORRUPTED", "Missing or invalid updatedAt");
  }
  if (typeof s.runId !== "string") {
    throw new OrchestratorError("STATE_CORRUPTED", "Missing or invalid runId");
  }
  if (!s.sharedContext || typeof s.sharedContext !== "object") {
    throw new OrchestratorError("STATE_CORRUPTED", "Missing sharedContext");
  }
  if (!s.agents || typeof s.agents !== "object") {
    throw new OrchestratorError("STATE_CORRUPTED", "Missing agents");
  }
  for (const agent of AGENTS) {
    if (!s.agents[agent]) {
      throw new OrchestratorError("STATE_CORRUPTED", `Missing agent state for ${agent}`);
    }
  }
  if (!s.flags || typeof s.flags !== "object") {
    throw new OrchestratorError("STATE_CORRUPTED", "Missing flags");
  }
  if (!s.allocation || typeof s.allocation !== "object") {
    throw new OrchestratorError("STATE_CORRUPTED", "Missing allocation");
  }

  if (s.currentTurn != null) {
    if (typeof s.currentTurn !== "object") {
      throw new OrchestratorError("STATE_CORRUPTED", "Invalid currentTurn");
    }
    if (typeof s.currentTurn.turnId !== "string") {
      throw new OrchestratorError("STATE_CORRUPTED", "Invalid currentTurn.turnId");
    }
    if (!AGENTS.includes(s.currentTurn.owner as AgentId)) {
      throw new OrchestratorError("STATE_CORRUPTED", "Invalid currentTurn.owner");
    }
    if (typeof s.currentTurn.leaseVersion !== "number") {
      throw new OrchestratorError("STATE_CORRUPTED", "Invalid currentTurn.leaseVersion");
    }
  }
}
