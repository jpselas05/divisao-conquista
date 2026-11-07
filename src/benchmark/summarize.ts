import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { writeCsv } from './measure.ts';

const RESULTS_DIR = join(import.meta.dirname, '..', '..', 'results');

function median(sorted: number[]): number {
  const mid = sorted.length >> 1;
  return sorted.length % 2 === 1 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

const lines = readFileSync(join(RESULTS_DIR, 'medicoes.csv'), 'utf8').trim().split(/\r?\n/).slice(1);
const groups = new Map<string, number[]>();

for (const line of lines) {
  const [stage, algorithm, n, , time] = line.split(',');
  const key = `${stage},${algorithm},${n}`;
  groups.set(key, [...(groups.get(key) ?? []), Number(time)]);
}

const rows: (string | number)[][] = [];
const previousMedian = new Map<string, number>();

for (const [key, times] of groups) {
  const [stage, algorithm, n] = key.split(',');
  const sorted = [...times].sort((a, b) => a - b);
  const mean = times.reduce((sum, time) => sum + time, 0) / times.length;
  const variance = times.reduce((sum, time) => sum + (time - mean) ** 2, 0) / (times.length - 1);
  const center = median(sorted);

  const series = `${stage},${algorithm}`;
  const previous = previousMedian.get(series);
  previousMedian.set(series, center);

  rows.push([
    stage,
    algorithm,
    n,
    times.length,
    mean.toFixed(4),
    center.toFixed(4),
    Math.sqrt(variance).toFixed(4),
    sorted[0].toFixed(4),
    previous === undefined ? '' : (center / previous).toFixed(2),
  ]);
}

const header = ['etapa', 'algoritmo', 'n', 'execucoes', 'media_ms', 'mediana_ms', 'desvio_ms', 'minimo_ms', 'razao_ao_dobrar_n'];
writeCsv(join(RESULTS_DIR, 'resumo.csv'), header, rows);
console.log(`Resumo gravado com ${rows.length} linhas.`);
