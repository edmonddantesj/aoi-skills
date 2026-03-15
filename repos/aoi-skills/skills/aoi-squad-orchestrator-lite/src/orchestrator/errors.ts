export type ErrorCode =
  | "LOCK_BUSY"
  | "LOCK_NOT_OWNED"
  | "REVISION_MISMATCH"
  | "TURN_ID_MISMATCH"
  | "LEASE_MISMATCH"
  | "INVALID_OWNER"
  | "INVALID_STATUS"
  | "INVALID_TRANSITION"
  | "ALREADY_PROCESSED"
  | "ARTIFACT_MISSING"
  | "BLOCKED"
  | "RECOVERY_REQUIRED"
  | "STATE_CORRUPTED"
  | "NOT_FOUND"
  | "INTERNAL";

export class OrchestratorError extends Error {
  constructor(
    public code: ErrorCode,
    message: string,
    public retryable = false
  ) {
    super(message);
    this.name = "OrchestratorError";
  }
}
