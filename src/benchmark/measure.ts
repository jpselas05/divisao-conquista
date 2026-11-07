import { writeFileSync, mkdirSync } from 'node:fs';
import { cpus, platform, release, totalmem } from 'node:os';
import { dirname } from 'node:path';

declare const gc: undefined | (() => void);

/** Acumula os resultados para o JIT não eliminar as chamadas medidas. */
let sink = 0;

/** Tempo, em milissegundos, de uma chamada de task. */
export function timeOnce(task: () => number): number {
  if (typeof gc === 'function') gc();
  const start = performance.now();
  sink += task();
  return performance.now() - start;
}

/** Roda task antes da medição para o V8 otimizar o código; o tempo é descartado. */
export function warmUp(task: () => number, repetitions: number): void {
  for (let i = 0; i < repetitions; i++) sink += task();
}

export function assertGcEnabled(): void {
  if (typeof gc !== 'function') throw new Error('Rode com node --expose-gc (use os scripts do npm).');
}

export function writeCsv(path: string, header: string[], rows: (string | number)[][]): void {
  mkdirSync(dirname(path), { recursive: true });
  const lines = [header, ...rows].map((row) => row.join(','));
  writeFileSync(path, `${lines.join('\n')}\n`);
}

export function writeMachineInfo(path: string): void {
  const info = {
    cpu: cpus()[0]?.model.trim(),
    nucleos_logicos: cpus().length,
    memoria_gb: Math.round(totalmem() / 1024 ** 3),
    sistema: `${platform()} ${release()}`,
    node: process.version,
    v8: process.versions.v8,
  };
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(info, null, 2)}\n`);
}

export function keepSink(): number {
  return sink;
}
