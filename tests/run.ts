import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { closestPairBrute } from '../src/closestPair/bruteForce.ts';
import { closestPairDivideConquer } from '../src/closestPair/divideConquer.ts';
import { createRandom, randomGridPoints, randomIntegers, randomPoints } from '../src/benchmark/generators.ts';
import { maxSubarrayBrute } from '../src/maxSubarray/bruteForce.ts';
import { maxSubarrayDivideConquer } from '../src/maxSubarray/divideConquer.ts';
import { maxSubarrayDivideConquerLinear } from '../src/maxSubarray/divideConquerLinear.ts';
import { maxSubarrayKadane } from '../src/maxSubarray/kadane.ts';

/** Bateria do trabalho: casos em tests/ pelos programas reais, depois força bruta x técnica. */
const root = join(import.meta.dirname, '..');
const EPSILON = 1e-9;
let passed = 0;
const failures: string[] = [];

function check(ok: boolean, label: string): void {
  if (ok) passed++;
  else failures.push(label);
}

function runProgram(file: string, algorithm: string, input: string) {
  const args = ['--disable-warning=ExperimentalWarning', join(root, 'src', 'cli', file), '--algo', algorithm];
  const result = spawnSync(process.execPath, args, { input, encoding: 'utf8' });
  return { status: result.status, output: result.stdout.trim() };
}

function loadCases<T>(file: string): T[] {
  return JSON.parse(readFileSync(join(root, 'tests', file), 'utf8'));
}

interface SubarrayCase {
  nome: string;
  valores: number[];
  esperado: { soma: number; inicio: number; fim: number };
}

for (const item of loadCases<SubarrayCase>('casos-etapa1.json')) {
  const input = `${item.valores.length}\n${item.valores.join(' ')}\n`;
  const { soma, inicio, fim } = item.esperado;
  for (const algorithm of ['forca-bruta', 'dc', 'dc-linear', 'kadane']) {
    const { output } = runProgram('maxSubarray.ts', algorithm, input);
    check(output === `${soma} ${inicio} ${fim}`, `etapa 1 / ${item.nome} / ${algorithm}: ${output}`);
  }
}

interface PairCase {
  nome: string;
  pontos: [number, number][];
  esperado: { distancia?: number; pares?: [number, number][]; erro?: boolean };
}

for (const item of loadCases<PairCase>('casos-etapa2.json')) {
  const lines = item.pontos.map(([x, y]) => `${x} ${y}`).join('\n');
  const input = `${item.pontos.length}\n${lines}\n`;

  for (const algorithm of ['forca-bruta', 'dc']) {
    const label = `etapa 2 / ${item.nome} / ${algorithm}`;
    const { status, output } = runProgram('closestPair.ts', algorithm, input);
    if (item.esperado.erro) {
      check(status === 1 && output === '', `${label}: deveria falhar`);
      continue;
    }

    const [distance, first, second] = output.split(' ').map(Number);
    const [ax, ay] = item.pontos[first];
    const [bx, by] = item.pontos[second];
    const realDistance = Math.hypot(ax - bx, ay - by);
    const pairAccepted = item.esperado.pares?.some(([a, b]) => a === first && b === second) ?? true;
    const ok = first < second
      && Math.abs(distance - item.esperado.distancia!) < EPSILON
      && Math.abs(realDistance - distance) < EPSILON
      && pairAccepted;
    check(ok, `${label}: ${output}`);
  }
}

const cliChecks = passed + failures.length;

// Valores em faixa pequena forçam empates; as quatro versões devem dar o mesmo intervalo.
const subarrayAlgorithms = [maxSubarrayDivideConquer, maxSubarrayDivideConquerLinear, maxSubarrayKadane];
for (let seed = 1; seed <= 3000; seed++) {
  const random = createRandom(seed);
  const n = 1 + Math.floor(random() * 60);
  const values = randomIntegers(n, seed % 2 === 0 ? 2 : 50, random);
  const expected = JSON.stringify(maxSubarrayBrute(values));
  for (const algorithm of subarrayAlgorithms) {
    const answer = JSON.stringify(algorithm(values));
    check(answer === expected, `etapa 1 / semente ${seed} / ${algorithm.name}: ${answer} x ${expected}`);
  }
}

// Empates de par são válidos, então só a distância precisa coincidir.
const thresholds = [2, 3, 8, 16, 32, 64];
for (let seed = 1; seed <= 3000; seed++) {
  const random = createRandom(seed);
  const n = 2 + Math.floor(random() * 300);
  const points = seed % 2 === 0
    ? randomGridPoints(n, 5 + (seed % 40), random)
    : randomPoints(n, 1000, random);
  const expected = closestPairBrute(points).distance;
  for (const threshold of thresholds) {
    const answer = closestPairDivideConquer(points, threshold);
    const { x: ax, y: ay } = points[answer.first];
    const { x: bx, y: by } = points[answer.second];
    const consistent = Math.abs(Math.hypot(ax - bx, ay - by) - answer.distance) < EPSILON;
    const ok = consistent && Math.abs(answer.distance - expected) < EPSILON;
    check(ok, `etapa 2 / semente ${seed} / limiar ${threshold}: ${answer.distance} x ${expected}`);
  }
}

for (const failure of failures.slice(0, 20)) console.error(`FALHOU ${failure}`);
const total = passed + failures.length;
console.log(`Programas reais: ${cliChecks} verificações. Comparações com força bruta: ${total - cliChecks}.`);
console.log(`${passed}/${total} aprovadas.`);
process.exitCode = failures.length === 0 ? 0 : 1;
