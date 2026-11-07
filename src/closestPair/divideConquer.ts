import { assertHasPair, toResult } from './types.ts';
import type { ClosestPairResult, Point } from './types.ts';

/** Tamanho a partir do qual a recursão passa para a força bruta. Ver results/limiar.csv. */
export const DEFAULT_THRESHOLD = 32;

/** Quantos vizinhos seguintes, em ordem de y, cada ponto da faixa compara. */
const MAX_STRIP_NEIGHBORS = 7;

interface PairCandidate {
  squared: number;
  a: number;
  b: number;
}

/** T(n) = 2T(n/2) + O(n) = O(n log n), além da ordenação inicial O(n log n). */
export function closestPairDivideConquer(
  points: readonly Point[],
  threshold: number = DEFAULT_THRESHOLD,
): ClosestPairResult {
  assertHasPair(points);
  const n = points.length;
  const xs = Float64Array.from(points, (p) => p.x);
  const ys = Float64Array.from(points, (p) => p.y);

  const byX = Int32Array.from({ length: n }, (_, i) => i)
    .sort((a, b) => xs[a] - xs[b] || ys[a] - ys[b]);
  const initialByY = Int32Array.from(byX).sort((a, b) => ys[a] - ys[b] || xs[a] - xs[b]);

  const isLeft = new Uint8Array(n);
  const strip = new Int32Array(n);

  function bruteRange(lo: number, hi: number): PairCandidate {
    const best: PairCandidate = { squared: Infinity, a: -1, b: -1 };
    for (let i = lo; i < hi; i++) {
      for (let j = i + 1; j < hi; j++) {
        const dx = xs[byX[i]] - xs[byX[j]];
        const dy = ys[byX[i]] - ys[byX[j]];
        const squared = dx * dx + dy * dy;
        if (squared < best.squared) {
          best.squared = squared;
          best.a = byX[i];
          best.b = byX[j];
        }
      }
    }
    return best;
  }

  /** Separa byY entre os lados em O(n), preservando a ordem por y. */
  function splitByY(byY: Int32Array, lo: number, mid: number): [Int32Array, Int32Array] {
    for (let i = lo; i < lo + byY.length; i++) isLeft[byX[i]] = i < mid ? 1 : 0;
    const left = new Int32Array(mid - lo);
    const right = new Int32Array(byY.length - (mid - lo));
    let l = 0;
    let r = 0;
    for (let i = 0; i < byY.length; i++) {
      if (isLeft[byY[i]] === 1) left[l++] = byY[i];
      else right[r++] = byY[i];
    }
    return [left, right];
  }

  /** Procura pares que cruzam a linha x = lineX e sejam melhores que best. */
  function searchStrip(byY: Int32Array, lineX: number, best: PairCandidate): PairCandidate {
    let size = 0;
    for (let i = 0; i < byY.length; i++) {
      const dx = xs[byY[i]] - lineX;
      if (dx * dx < best.squared) strip[size++] = byY[i];
    }
    for (let i = 0; i < size; i++) {
      const last = Math.min(i + MAX_STRIP_NEIGHBORS, size - 1);
      for (let j = i + 1; j <= last; j++) {
        const dy = ys[strip[j]] - ys[strip[i]];
        if (dy * dy >= best.squared) break;
        const dx = xs[strip[j]] - xs[strip[i]];
        const squared = dx * dx + dy * dy;
        if (squared < best.squared) best = { squared, a: strip[i], b: strip[j] };
      }
    }
    return best;
  }

  function solve(lo: number, hi: number, byY: Int32Array): PairCandidate {
    if (hi - lo <= threshold) return bruteRange(lo, hi);

    const mid = (lo + hi) >>> 1;
    const lineX = xs[byX[mid]];
    const [leftByY, rightByY] = splitByY(byY, lo, mid);

    const left = solve(lo, mid, leftByY);
    const right = solve(mid, hi, rightByY);
    return searchStrip(byY, lineX, left.squared <= right.squared ? left : right);
  }

  const best = solve(0, n, initialByY);
  return toResult(best.squared, best.a, best.b);
}
