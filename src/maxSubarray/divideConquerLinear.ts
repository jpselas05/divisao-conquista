import { assertNotEmpty, isBetter } from './types.ts';
import type { SubarrayResult } from './types.ts';

interface Segment {
  total: number;
  prefixSum: number;
  prefixEnd: number;
  suffixSum: number;
  suffixStart: number;
  best: SubarrayResult;
}

function leaf(value: number, index: number): Segment {
  return {
    total: value,
    prefixSum: value,
    prefixEnd: index,
    suffixSum: value,
    suffixStart: index,
    best: { sum: value, start: index, end: index },
  };
}

function merge(left: Segment, right: Segment): Segment {
  const extendedPrefix = left.total + right.prefixSum;
  const keepPrefix = left.prefixSum >= extendedPrefix;
  const extendedSuffix = right.total + left.suffixSum;
  const extendSuffix = extendedSuffix >= right.suffixSum;

  const crossing: SubarrayResult = {
    sum: left.suffixSum + right.prefixSum,
    start: left.suffixStart,
    end: right.prefixEnd,
  };
  const sideBest = isBetter(right.best, left.best) ? right.best : left.best;

  return {
    total: left.total + right.total,
    prefixSum: keepPrefix ? left.prefixSum : extendedPrefix,
    prefixEnd: keepPrefix ? left.prefixEnd : right.prefixEnd,
    suffixSum: extendSuffix ? extendedSuffix : right.suffixSum,
    suffixStart: extendSuffix ? left.suffixStart : right.suffixStart,
    best: isBetter(crossing, sideBest) ? crossing : sideBest,
  };
}

function solve(values: readonly number[], lo: number, hi: number): Segment {
  if (lo === hi) return leaf(values[lo], lo);
  const mid = (lo + hi) >>> 1;
  return merge(solve(values, lo, mid), solve(values, mid + 1, hi));
}

export function maxSubarrayDivideConquerLinear(values: readonly number[]): SubarrayResult {
  assertNotEmpty(values);
  return solve(values, 0, values.length - 1).best;
}
