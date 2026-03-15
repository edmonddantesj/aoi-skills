import { readState } from "../state/repository";

export async function getCurrentTurn(rootDir: string) {
  const state = await readState(rootDir);
  return state.currentTurn;
}
