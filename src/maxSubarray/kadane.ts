import { assertNotEmpty } from './types.ts';
import type { SubarrayResult } from './types.ts';

/** Varredura única guardando a melhor soma que termina em cada posição. Tempo: O(n). */
export function maxSubarrayKadane(values: readonly number[]): SubarrayResult {
  assertNotEmpty(values);
  let bestSum = values[0];
  let bestStart = 0;
  let bestEnd = 0;
  let current = values[0];
  let currentStart = 0;

  for (let i = 1; i < values.length; i++) {
    // Só recomeça com soma negativa: com soma zero, estender mantém o início menor.
    if (current < 0) {
      current = values[i];
      currentStart = i;
    } else {
      current += values[i];
    }
    if (current > bestSum) {
      bestSum = current;
      bestStart = currentStart;
      bestEnd = i;
    }
  }
  return { sum: bestSum, start: bestStart, end: bestEnd };
}
