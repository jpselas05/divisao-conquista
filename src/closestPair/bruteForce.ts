import { assertHasPair, toResult } from './types.ts';
import type { ClosestPairResult, Point } from './types.ts';

/** Compara todos os pares. Tempo: O(n²). */
export function closestPairBrute(points: readonly Point[]): ClosestPairResult {
  assertHasPair(points);
  let best = Infinity;
  let first = 0;
  let second = 1;

  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      const dx = points[i].x - points[j].x;
      const dy = points[i].y - points[j].y;
      const squared = dx * dx + dy * dy;
      if (squared < best) {
        best = squared;
        first = i;
        second = j;
      }
    }
  }
  return toResult(best, first, second);
}
