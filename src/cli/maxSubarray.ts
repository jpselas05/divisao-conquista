import { maxSubarrayBrute } from '../maxSubarray/bruteForce.ts';
import { maxSubarrayDivideConquer } from '../maxSubarray/divideConquer.ts';
import { maxSubarrayDivideConquerLinear } from '../maxSubarray/divideConquerLinear.ts';
import { maxSubarrayKadane } from '../maxSubarray/kadane.ts';
import type { MaxSubarrayAlgorithm } from '../maxSubarray/types.ts';
import { OUTPUT_INDEX_BASE, readAlgorithmName, readValues, runCli } from './input.ts';

const ALGORITHMS: Record<string, MaxSubarrayAlgorithm> = {
  'forca-bruta': maxSubarrayBrute,
  dc: maxSubarrayDivideConquer,
  'dc-linear': maxSubarrayDivideConquerLinear,
  kadane: maxSubarrayKadane,
};

runCli(() => {
  const name = readAlgorithmName('dc');
  const algorithm = ALGORITHMS[name];
  if (!algorithm) throw new Error(`Algoritmo desconhecido: ${name}`);

  const { values } = readValues(1);
  const { sum, start, end } = algorithm(values);
  return `${sum} ${start + OUTPUT_INDEX_BASE} ${end + OUTPUT_INDEX_BASE}`;
});
