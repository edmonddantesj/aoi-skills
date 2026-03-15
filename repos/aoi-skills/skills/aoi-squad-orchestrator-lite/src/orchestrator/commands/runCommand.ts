import { randomUUID } from "node:crypto";
import { DEFAULT_LOCK_TTL_MS } from "../constants";
import { OrchestratorError } from "../errors";
import { appendEvent } from "../state/events";
import { acquireLock, releaseLock } from "../state/lock";
import { readState, writeStateAtomic } from "../state/repository";
import { EventActor, EventRecord, OrchestratorState } from "../types";

export interface CommandContext {
  rootDir: string;
  actor: EventActor;
  commandId: string;
  issuedAt: string;
  runId: string;
}

export interface TransitionResult {
  ok: boolean;
  state?: OrchestratorState;
  events?: EventRecord[];
  error?: {
    code: string;
    message: string;
    retryable: boolean;
  };
}

export async function runCommand(
  ctx: CommandContext,
  handler: (state: OrchestratorState) => Promise<{ next: OrchestratorState; events: EventRecord[] }>
): Promise<TransitionResult> {
  const lockToken = randomUUID();

  try {
    await acquireLock(ctx.rootDir, {
      owner: ctx.actor,
      pid: process.pid,
      runId: ctx.runId,
      acquiredAt: ctx.issuedAt,
      expiresAt: new Date(Date.now() + DEFAULT_LOCK_TTL_MS).toISOString(),
      token: lockToken,
    });

    const state = await readState(ctx.rootDir);
    const { next, events } = await handler(state);

    await writeStateAtomic(ctx.rootDir, next);
    for (const event of events) {
      await appendEvent(ctx.rootDir, event);
    }

    return { ok: true, state: next, events };
  } catch (err) {
    if (err instanceof OrchestratorError) {
      return {
        ok: false,
        error: { code: err.code, message: err.message, retryable: err.retryable },
      };
    }

    return {
      ok: false,
      error: {
        code: "INTERNAL",
        message: err instanceof Error ? err.message : "Unknown error",
        retryable: false,
      },
    };
  } finally {
    await releaseLock(ctx.rootDir, lockToken).catch(() => {});
  }
}
