import type { Point } from '../closestPair/types.ts';

export type Random = () => number;

/** Gerador mulberry32: mesma semente, mesma sequência, para reproduzir as medições. */
export function createRandom(seed: number): Random {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Inteiros uniformes em [-limit, limit]. */
export function randomIntegers(n: number, limit: number, random: Random): number[] {
  return Array.from({ length: n }, () => Math.floor(random() * (2 * limit + 1)) - limit);
}

/** Pontos com coordenadas reais uniformes em [0, size). */
export function randomPoints(n: number, size: number, random: Random): Point[] {
  return Array.from({ length: n }, () => ({ x: random() * size, y: random() * size }));
}

/** Pontos em grade inteira pequena, que força empates, duplicatas e x repetidos. */
export function randomGridPoints(n: number, size: number, random: Random): Point[] {
  return Array.from({ length: n }, () => ({
    x: Math.floor(random() * size),
    y: Math.floor(random() * size),
  }));
}
