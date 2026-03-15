import { WATCHDOG_GRACE_MS } from "../constants";
import { AgentId, CurrentTurn } from "../types";

export function softTimeoutMs(owner: AgentId): number {
  if (owner === "planner") return 2 * 60 * 1000;
  if (owner === "reviewer") return 3 * 60 * 1000;
  return 5 * 60 * 1000;
}

export function hardTimeoutMs(owner: AgentId): number {
  if (owner === "planner") return 5 * 60 * 1000;
  if (owner === "reviewer") return 10 * 60 * 1000;
  return 15 * 60 * 1000;
}

export function defaultLeaseMs(owner: AgentId): number {
  return hardTimeoutMs(owner);
}

export function isSoftTimeout(turn: CurrentTurn, now = Date.now()): boolean {
  if (!turn.lastProgressAt) return false;
  return now - new Date(turn.lastProgressAt).getTime() > softTimeoutMs(turn.owner);
}

export function isHardTimeout(turn: CurrentTurn, now = Date.now()): boolean {
  if (turn.deadlineAt) {
    return now > new Date(turn.deadlineAt).getTime() + WATCHDOG_GRACE_MS;
  }
  return now - new Date(turn.startedAt).getTime() > hardTimeoutMs(turn.owner);
}
