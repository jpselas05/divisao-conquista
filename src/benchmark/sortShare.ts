import { join } from 'node:path';
import { closestPairDivideConquer } from '../closestPair/divideConquer.ts';
import { createRandom, randomPoints } from './generators.ts';
import { keepSink, timeOnce, warmUp, writeCsv } from './measure.ts';
import { PLANE_SIZE } from './suites.ts';

const SIZES = [1600, 6400, 25600];
const RUNS = 20;
const RESULTS_DIR = join(import.meta.dirname, '..', '..', 'results');

function initialSorts(xs: Float64Array, ys: Float64Array): number {
  const byX = Int32Array.from({ length: xs.length }, (_, i) => i)
    .sort((a, b) => xs[a] - xs[b] || ys[a] - ys[b]);
  const byY = Int32Array.from(byX).sort((a, b) => ys[a] - ys[b] || xs[a] - xs[b]);
  return byX[0] + byY[0];
}

const rows: (string | number)[][] = [];

for (const n of SIZES) {
  for (let run = 1; run <= RUNS; run++) {
    const points = randomPoints(n, PLANE_SIZE, createRandom(n * 3000 + run));
    const xs = Float64Array.from(points, (p) => p.x);
    const ys = Float64Array.from(points, (p) => p.y);
    if (run === 1) {
      warmUp(() => initialSorts(xs, ys), 10);
      warmUp(() => closestPairDivideConquer(points).distance, 10);
    }
    const sorting = timeOnce(() => initialSorts(xs, ys));
    const total = timeOnce(() => closestPairDivideConquer(points).distance);
    rows.push([n, run, sorting.toFixed(6), total.toFixed(6)]);
  }
}

writeCsv(join(RESULTS_DIR, 'ordenacao.csv'), ['n', 'execucao', 'ordenacao_ms', 'total_ms'], rows);
console.log(`Linhas gravadas: ${rows.length} (controle ${keepSink().toFixed(0)})`);
