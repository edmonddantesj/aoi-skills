import { promises as fs } from "node:fs";
import path from "node:path";
import { STATE_FILE, TEMP_STATE_FILE } from "../constants";
import { OrchestratorState } from "../types";
import { assertValidState } from "./validate";

export async function readState(rootDir: string): Promise<OrchestratorState> {
  const file = path.join(rootDir, STATE_FILE);
  const raw = await fs.readFile(file, "utf8");
  const parsed = JSON.parse(raw);
  assertValidState(parsed);
  return parsed;
}

export async function stateExists(rootDir: string): Promise<boolean> {
  const file = path.join(rootDir, STATE_FILE);
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
}

export async function writeStateAtomic(rootDir: string, state: OrchestratorState): Promise<void> {
  const target = path.join(rootDir, STATE_FILE);
  const temp = path.join(rootDir, TEMP_STATE_FILE);
  await fs.mkdir(path.dirname(target), { recursive: true });
  await fs.writeFile(temp, JSON.stringify(state, null, 2), "utf8");
  await fs.rename(temp, target);
}
