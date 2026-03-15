import { promises as fs } from "node:fs";
import path from "node:path";
import { LOCK_FILE } from "../constants";
import { OrchestratorError } from "../errors";

export interface LockPayload {
  owner: string;
  pid: number;
  runId: string;
  acquiredAt: string;
  expiresAt: string;
  token: string;
}

export async function readLock(rootDir: string): Promise<LockPayload | null> {
  const file = path.join(rootDir, LOCK_FILE);
  try {
    const raw = await fs.readFile(file, "utf8");
    return JSON.parse(raw) as LockPayload;
  } catch (err: any) {
    if (err?.code === "ENOENT") return null;
    throw err;
  }
}

export async function acquireLock(rootDir: string, payload: LockPayload): Promise<LockPayload> {
  const file = path.join(rootDir, LOCK_FILE);
  await fs.mkdir(path.dirname(file), { recursive: true });

  try {
    const handle = await fs.open(file, "wx");
    await handle.writeFile(JSON.stringify(payload, null, 2), "utf8");
    await handle.close();
    return payload;
  } catch (err: any) {
    if (err?.code === "EEXIST") {
      const current = await readLock(rootDir);
      const expired =
        current?.expiresAt != null &&
        new Date(current.expiresAt).getTime() < Date.now();

      if (expired) {
        await fs.rm(file, { force: true });
        const retryHandle = await fs.open(file, "wx");
        await retryHandle.writeFile(JSON.stringify(payload, null, 2), "utf8");
        await retryHandle.close();
        return payload;
      }

      throw new OrchestratorError("LOCK_BUSY", "Lock file already exists", true);
    }
    throw err;
  }
}

export async function releaseLock(rootDir: string, token: string): Promise<void> {
  const file = path.join(rootDir, LOCK_FILE);
  const current = await readLock(rootDir);
  if (!current) return;
  if (current.token !== token) {
    throw new OrchestratorError("LOCK_NOT_OWNED", "Lock token mismatch");
  }
  await fs.rm(file, { force: true });
}
