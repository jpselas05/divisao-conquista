import { assertNotEmpty, isBetter } from './types.ts';
import type { SubarrayResult } from './types.ts';

function maxCrossing(values: readonly number[], lo: number, mid: number, hi: number): SubarrayResult {
  let leftBest = -Infinity;
  let start = mid;
  let sum = 0;
  for (let i = mid; i >= lo; i--) {
    sum += values[i];
    if (sum >= leftBest) {
      leftBest = sum;
      start = i;
    }
  }

  let rightBest = -Infinity;
  let end = mid + 1;
  sum = 0;
  for (let j = mid + 1; j <= hi; j++) {
    sum += values[j];
    if (sum > rightBest) {
      rightBest = sum;
      end = j;
    }
  }
  return { sum: leftBest + rightBest, start, end };
}

function solve(values: readonly number[], lo: number, hi: number): SubarrayResult {
  if (lo === hi) return { sum: values[lo], start: lo, end: lo };

  const mid = (lo + hi) >>> 1;
  const left = solve(values, lo, mid);
  const right = solve(values, mid + 1, hi);
  const crossing = maxCrossing(values, lo, mid, hi);

  const best = isBetter(right, left) ? right : left;
  return isBetter(crossing, best) ? crossing : best;
}

export function maxSubarrayDivideConquer(values: readonly number[]): SubarrayResult {
  assertNotEmpty(values);
  return solve(values, 0, values.length - 1);
}
