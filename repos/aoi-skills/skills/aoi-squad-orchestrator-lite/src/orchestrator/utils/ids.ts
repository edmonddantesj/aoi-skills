export function makeEventId(suffix: string): string {
  return `evt_${Date.now()}_${suffix}`;
}

export function makeRunId(): string {
  return `run_${Date.now()}`;
}
