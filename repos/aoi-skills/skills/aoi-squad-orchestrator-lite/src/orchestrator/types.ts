export type AgentId = "planner" | "executor" | "reviewer";
export type EventActor = AgentId | "system";

export type TurnStatus =
  | "pending"
  | "in_progress"
  | "blocked"
  | "in_review"
  | "done"
  | "needs_replan";

export type EventSeverity = "info" | "warn" | "error";

export interface CurrentTurn {
  turnId: string;
  owner: AgentId;
  status: TurnStatus;
  startedAt: string;
  lastProgressAt: string | null;
  deadlineAt: string | null;
  leaseVersion: number;
}

export interface AgentState {
  status: "idle" | "active" | "blocked" | "offline";
  lastSeenAt: string | null;
  lastTurnId: string | null;
}

export interface SharedContext {
  goal: string;
  constraints: string[];
  inputs: string[];
  artifacts: string[];
}

export interface FlagsState {
  blocked: boolean;
  needsReview: boolean;
  handoffRequested: boolean;
  recovered?: boolean;
  softTimedOut?: boolean;
}

export interface LastDecision {
  selectedAgent: AgentId;
  reason: string;
  at: string;
}

export interface RecoveryState {
  needed?: boolean;
  reason?: string;
  startedAt?: string;
  recoveredFrom?: string;
  confidence?: "low" | "medium" | "high";
  lastRecoveredAt?: string;
}

export interface WatchdogState {
  enabled: boolean;
  lastCheckedAt: string | null;
  lastOutcome: string | null;
}

export interface AllocationState {
  strategy: "single-owner-per-turn";
  override: AgentId | null;
}

export interface OrchestratorState {
  version: number;
  revision: number;
  updatedAt: string;
  runId: string;
  mode: "active" | "idle" | "recovering" | "degraded";
  currentTurn: CurrentTurn | null;
  sharedContext: SharedContext;
  agents: Record<AgentId, AgentState>;
  allocation: AllocationState;
  flags: FlagsState;
  lastDecision: LastDecision | null;
  recovery?: RecoveryState;
  watchdog?: WatchdogState;
}

export interface EventRecord<T = Record<string, unknown>> {
  eventId: string;
  type: string;
  at: string;
  runId: string;
  commandId?: string;
  actor: EventActor;
  turnId?: string;
  revision: number;
  severity: EventSeverity;
  data: T;
  meta?: Record<string, unknown>;
}
