/** Intervalo contínuo [start, end], com índices inclusivos, e a soma dos seus valores. */
export interface SubarrayResult {
  sum: number;
  start: number;
  end: number;
}

export type MaxSubarrayAlgorithm = (values: readonly number[]) => SubarrayResult;

/**
 * Critério de desempate usado por todas as versões: maior soma, depois menor
 * início, depois menor fim. Assim, os algoritmos devolvem sempre o mesmo intervalo.
 */
export function isBetter(a: SubarrayResult, b: SubarrayResult): boolean {
  if (a.sum !== b.sum) return a.sum > b.sum;
  if (a.start !== b.start) return a.start < b.start;
  return a.end < b.end;
}

export function assertNotEmpty(values: readonly number[]): void {
  if (values.length === 0) throw new Error('O vetor precisa ter pelo menos um valor.');
}
