import { readFileSync } from 'node:fs';

/** Primeiro índice usado na saída. Trocar para 1 se o professor exigir índices a partir de 1. */
export const OUTPUT_INDEX_BASE = 0;

/** Lê da entrada padrão: n seguido de n * itemSize números, separados por espaços ou linhas. */
export function readValues(itemSize: number): { n: number; values: number[] } {
  const tokens = readFileSync(0, 'utf8').trim().split(/\s+/).filter(Boolean);
  if (tokens.length === 0) throw new Error('Entrada vazia.');

  const numbers = tokens.map(Number);
  if (numbers.some((value) => !Number.isFinite(value))) {
    throw new Error('A entrada só pode conter números.');
  }

  const n = numbers[0];
  if (!Number.isInteger(n) || n < 0) throw new Error('n precisa ser um inteiro não negativo.');

  const values = numbers.slice(1);
  if (values.length !== n * itemSize) {
    throw new Error(`Esperados ${n * itemSize} valores depois de n, mas vieram ${values.length}.`);
  }
  return { n, values };
}

/** Lê o valor de --algo, ou devolve o padrão. */
export function readAlgorithmName(fallback: string): string {
  const position = process.argv.indexOf('--algo');
  return position === -1 ? fallback : (process.argv[position + 1] ?? '');
}

/** Executa o programa e transforma erros de entrada em mensagem e código de saída 1. */
export function runCli(main: () => string): void {
  try {
    console.log(main());
  } catch (error) {
    console.error(`Erro: ${error instanceof Error ? error.message : String(error)}`);
    process.exitCode = 1;
  }
}
