import { join } from 'node:path';
import { closestPairDivideConquer } from '../closestPair/divideConquer.ts';
import { createRandom, randomPoints } from './generators.ts';
import { assertGcEnabled, keepSink, timeOnce, warmUp, writeCsv } from './measure.ts';
import { PLANE_SIZE } from './suites.ts';

/** Mede a divisão e conquista da Etapa 2 com vários limiares de corte da recursão. */
const THRESHOLDS = [2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 256];
const SIZES = [6400, 25600];
const RUNS = 20;
const RESULTS_DIR = join(import.meta.dirname, '..', '..', 'results');

assertGcEnabled();
const rows: (string | number)[][] = [];

for (const n of SIZES) {
  const warmUpPoints = randomPoints(n, PLANE_SIZE, createRandom(n));
  for (const threshold of THRESHOLDS) {
    warmUp(() => closestPairDivideConquer(warmUpPoints, threshold).distance, 5);
  }

  for (let run = 1; run <= RUNS; run++) {
    const points = randomPoints(n, PLANE_SIZE, createRandom(n * 7000 + run));
    // Alterna a ordem dos limiares para o tempo não depender da posição na fila.
    const order = run % 2 === 0 ? THRESHOLDS : [...THRESHOLDS].reverse();
    for (const threshold of order) {
      const time = timeOnce(() => closestPairDivideConquer(points, threshold).distance);
      rows.push([n, threshold, run, time.toFixed(6)]);
    }
  }
  console.log(`limiar: n = ${n} concluído`);
}

writeCsv(join(RESULTS_DIR, 'limiar.csv'), ['n', 'limiar', 'execucao', 'tempo_ms'], rows);
console.log(`Linhas gravadas: ${rows.length} (controle ${keepSink().toFixed(0)})`);
