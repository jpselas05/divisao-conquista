import { join } from 'node:path';
import { createRandom } from './generators.ts';
import { keepSink, timeOnce, warmUp, writeCsv, writeMachineInfo } from './measure.ts';
import { SUITES } from './suites.ts';

/** Inclui os tamanhos sugeridos no enunciado e vai além para evidenciar o crescimento. */
const SIZES = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600];
const RUNS = 20;
const WARM_UP_SIZE = 1000;
const WARM_UP_REPETITIONS = 200;
const RESULTS_DIR = join(import.meta.dirname, '..', '..', 'results');

const rows: (string | number)[][] = [];

for (const suite of SUITES) {
  const warmUpCalls = suite.prepare(WARM_UP_SIZE, createRandom(1));
  for (const name of suite.algorithms) warmUp(warmUpCalls[name], WARM_UP_REPETITIONS);

  for (const n of SIZES) {
    for (let run = 1; run <= RUNS; run++) {
      // Por execução, todos os algoritmos recebem a mesma entrada.
      const calls = suite.prepare(n, createRandom(n * 1000 + run));
      for (const name of suite.algorithms) {
        rows.push([suite.stage, name, n, run, timeOnce(calls[name]).toFixed(6)]);
      }
    }
    console.log(`${suite.stage}: n = ${n} concluído`);
  }
}

writeCsv(join(RESULTS_DIR, 'medicoes.csv'), ['etapa', 'algoritmo', 'n', 'execucao', 'tempo_ms'], rows);
writeMachineInfo(join(RESULTS_DIR, 'maquina.json'));
console.log(`Linhas gravadas: ${rows.length} (controle ${keepSink().toFixed(0)})`);
