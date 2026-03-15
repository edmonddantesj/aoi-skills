import { promises as fs } from "node:fs";
import path from "node:path";
import { EVENTS_FILE } from "../constants";
import { EventRecord } from "../types";

export async function appendEvent(rootDir: string, event: EventRecord): Promise<void> {
  const file = path.join(rootDir, EVENTS_FILE);
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.appendFile(file, JSON.stringify(event) + "\n", "utf8");
}

export async function readEvents(rootDir: string): Promise<EventRecord[]> {
  const file = path.join(rootDir, EVENTS_FILE);

  try {
    const raw = await fs.readFile(file, "utf8");
    const lines = raw.split("\n").map((line) => line.trim()).filter(Boolean);
    const events: EventRecord[] = [];

    for (let i = 0; i < lines.length; i += 1) {
      const line = lines[i]!;
      try {
        events.push(JSON.parse(line) as EventRecord);
      } catch (err) {
        const isLastLine = i === lines.length - 1;
        if (isLastLine) break;
        throw err;
      }
    }

    return events;
  } catch (err: any) {
    if (err?.code === "ENOENT") {
      return [];
    }
    throw err;
  }
}
