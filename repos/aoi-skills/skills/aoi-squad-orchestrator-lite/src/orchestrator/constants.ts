export const ORCHESTRATOR_DIR = "runtime/orchestrator";

export const STATE_FILE = `${ORCHESTRATOR_DIR}/state.json`;
export const TEMP_STATE_FILE = `${ORCHESTRATOR_DIR}/state.tmp`;
export const LOCK_FILE = `${ORCHESTRATOR_DIR}/state.lock`;
export const EVENTS_FILE = `${ORCHESTRATOR_DIR}/events.jsonl`;
export const CHECKPOINT_DIR = `${ORCHESTRATOR_DIR}/checkpoints`;

export const DEFAULT_LOCK_TTL_MS = 15_000;
export const DEFAULT_LOCK_WAIT_MS = 3_000;
export const DEFAULT_LOCK_RETRY_MS = 150;

export const WATCHDOG_INTERVAL_MS = 60_000;
export const WATCHDOG_GRACE_MS = 30_000;

export const STATE_VERSION = 1;
