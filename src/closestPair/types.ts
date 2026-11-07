export interface Point {
  x: number;
  y: number;
}

export interface ClosestPairResult {
  distance: number;
  first: number;
  second: number;
}

export type ClosestPairAlgorithm = (points: readonly Point[]) => ClosestPairResult;

export function assertHasPair(points: readonly Point[]): void {
  if (points.length < 2) throw new Error('São necessários pelo menos dois pontos.');
}

export function toResult(squaredDistance: number, a: number, b: number): ClosestPairResult {
  return {
    distance: Math.sqrt(squaredDistance),
    first: Math.min(a, b),
    second: Math.max(a, b),
  };
}
