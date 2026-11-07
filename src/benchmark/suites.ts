import { closestPairBrute } from '../closestPair/bruteForce.ts';
import { closestPairDivideConquer } from '../closestPair/divideConquer.ts';
import { maxSubarrayBrute } from '../maxSubarray/bruteForce.ts';
import { maxSubarrayDivideConquer } from '../maxSubarray/divideConquer.ts';
import { maxSubarrayDivideConquerLinear } from '../maxSubarray/divideConquerLinear.ts';
import { maxSubarrayKadane } from '../maxSubarray/kadane.ts';
import { randomIntegers, randomPoints } from './generators.ts';
import type { Random } from './generators.ts';

export interface Suite {
  stage: string;
  algorithms: string[];
  prepare(n: number, random: Random): Record<string, () => number>;
}

export const MAX_VALUE = 1000;
export const PLANE_SIZE = 1_000_000;

export const maxSubarraySuite: Suite = {
  stage: 'etapa1',
  algorithms: ['forca-bruta', 'dc', 'dc-linear', 'kadane'],
  prepare(n, random) {
    const values = randomIntegers(n, MAX_VALUE, random);
    return {
      'forca-bruta': () => maxSubarrayBrute(values).sum,
      dc: () => maxSubarrayDivideConquer(values).sum,
      'dc-linear': () => maxSubarrayDivideConquerLinear(values).sum,
      kadane: () => maxSubarrayKadane(values).sum,
    };
  },
};

export const closestPairSuite: Suite = {
  stage: 'etapa2',
  algorithms: ['forca-bruta', 'dc'],
  prepare(n, random) {
    const points = randomPoints(n, PLANE_SIZE, random);
    return {
      'forca-bruta': () => closestPairBrute(points).distance,
      dc: () => closestPairDivideConquer(points).distance,
    };
  },
};

export const SUITES = [maxSubarraySuite, closestPairSuite];
