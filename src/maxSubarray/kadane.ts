import { assertNotEmpty } from './types.ts';
import type { SubarrayResult } from './types.ts';

export function maxSubarrayKadane(values: readonly number[]): SubarrayResult {
  assertNotEmpty(values);
  let bestSum = values[0];
  let bestStart = 0;
  let bestEnd = 0;
  let current = values[0];
  let currentStart = 0;

  for (let i = 1; i < values.length; i++) {
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
