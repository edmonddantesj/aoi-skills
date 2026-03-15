import { watchdogCheck } from "../commands/watchdogCheck";
import { readState } from "../state/repository";
import { isHardTimeout, isSoftTimeout } from "./timeout";

export async function watchdogTick(rootDir: string): Promise<void> {
  const state = await readState(rootDir);
  if (!state.watchdog?.enabled) return;
  if (!state.currentTurn) return;
  if (state.mode === "recovering") return;
  if (!isHardTimeout(state.currentTurn) && !isSoftTimeout(state.currentTurn)) return;

  await watchdogCheck(
    {
      rootDir,
      actor: "system",
      commandId: `cmd_watchdog_${Date.now()}`,
      issuedAt: new Date().toISOString(),
      runId: state.runId,
    },
    { expectedRevision: state.revision }
  );
}
