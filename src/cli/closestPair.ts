import { closestPairBrute } from '../closestPair/bruteForce.ts';
import { closestPairDivideConquer } from '../closestPair/divideConquer.ts';
import type { ClosestPairAlgorithm, Point } from '../closestPair/types.ts';
import { OUTPUT_INDEX_BASE, readAlgorithmName, readValues, runCli } from './input.ts';

const ALGORITHMS: Record<string, ClosestPairAlgorithm> = {
  'forca-bruta': closestPairBrute,
  dc: (points) => closestPairDivideConquer(points),
};

runCli(() => {
  const name = readAlgorithmName('dc');
  const algorithm = ALGORITHMS[name];
  if (!algorithm) throw new Error(`Algoritmo desconhecido: ${name}`);

  const { n, values } = readValues(2);
  const points: Point[] = Array.from({ length: n }, (_, i) => ({
    x: values[2 * i],
    y: values[2 * i + 1],
  }));

  const { distance, first, second } = algorithm(points);
  return `${distance} ${first + OUTPUT_INDEX_BASE} ${second + OUTPUT_INDEX_BASE}`;
});
