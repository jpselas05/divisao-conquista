import { assertNotEmpty } from './types.ts';
import type { SubarrayResult } from './types.ts';

export function maxSubarrayBrute(values: readonly number[]): SubarrayResult {
  assertNotEmpty(values);
  let bestSum = -Infinity;
  let bestStart = 0;
  let bestEnd = 0;

  for (let start = 0; start < values.length; start++) {
    let sum = 0;
    for (let end = start; end < values.length; end++) {
      sum += values[end];
      if (sum > bestSum) {
        bestSum = sum;
        bestStart = start;
        bestEnd = end;
      }
    }
  }
  return { sum: bestSum, start: bestStart, end: bestEnd };
}
