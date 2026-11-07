import { join } from 'node:path';
import { createRandom } from './generators.ts';
import { keepSink, timeOnce, warmUp, writeCsv } from './measure.ts';
import { SUITES } from './suites.ts';

const SIZES = [2, 4, 8, 16, 32, 64, 128, 256, 512];
const RUNS = 5;
const BATCH_ELEMENTS = 20_000;
const RESULTS_DIR = join(import.meta.dirname, '..', '..', 'results');

const rows: (string | number)[][] = [];

for (const suite of SUITES) {
  for (const n of SIZES) {
    const batchSize = Math.ceil(BATCH_ELEMENTS / n);
    const random = createRandom(n * 13);
    const inputs = Array.from({ length: batchSize }, () => suite.prepare(n, random));

    for (const name of suite.algorithms) {
      const batch = (): number => inputs.reduce((total, calls) => total + calls[name](), 0);
      warmUp(batch, 3);
      for (let run = 1; run <= RUNS; run++) {
        const perCall = (timeOnce(batch) * 1000) / batchSize;
        rows.push([suite.stage, name, n, run, batchSize, perCall.toFixed(4)]);
      }
    }
  }
  console.log(`${suite.stage}: concluído`);
}

const header = ['etapa', 'algoritmo', 'n', 'execucao', 'chamadas_no_lote', 'tempo_us_por_chamada'];
writeCsv(join(RESULTS_DIR, 'cruzamento.csv'), header, rows);
console.log(`Linhas gravadas: ${rows.length} (controle ${keepSink().toFixed(0)})`);
