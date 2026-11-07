# Trabalho Prático: Divisão e Conquista

Subarranjo de soma máxima e par de pontos mais próximos em TypeScript, cada um comparado com a força bruta.

## Requisitos

Node.js 24 ou superior, que roda TypeScript diretamente, sem build. Os programas e as medições não têm dependências; `npm install` só é necessário para `npm run typecheck`.

## Como executar

Os dois programas leem da entrada padrão.

### Etapa 1

Entrada: `n` seguido de `n` inteiros. Saída: `soma inicio fim`.

```bash
echo "9  -2 1 -3 4 -1 2 1 -5 4" | node src/cli/maxSubarray.ts --algo dc
# 6 3 6
```

`--algo` aceita `forca-bruta`, `dc` (padrão), `dc-linear` e `kadane`.

### Etapa 2

Entrada: `n` seguido de `n` pares `x y`. Saída: `distancia i j`, com `i < j`.

```bash
echo "3  0 0  3 4  10 10" | node src/cli/closestPair.ts --algo dc
# 5 0 1
```

`--algo` aceita `forca-bruta` e `dc` (padrão).

## Decisões a confirmar

O enunciado não define estes pontos:

- **Índices:** começam em 0. Para mudar, altere `OUTPUT_INDEX_BASE` em `src/cli/input.ts`.
- **Empates na Etapa 1:** vale o menor início e, depois, o menor fim. As quatro versões devolvem o mesmo intervalo.
- **Empates na Etapa 2:** qualquer par com a distância mínima é aceito.
- **Formato da Etapa 2:** a entrada e a saída acima são uma escolha deste projeto.
- **Questão desafio:** a "versão O(n)" foi interpretada de duas formas, ambas implementadas: Kadane (`kadane`) e divisão e conquista com combinação O(1) (`dc-linear`).
- **Limiar:** interpretado como o tamanho em que a recursão da Etapa 2 passa para a força bruta (`DEFAULT_THRESHOLD`).

## Testes

```bash
npm test
```

O script `tests/run.ts` passa os casos de `tests/` pelos programas reais e compara a técnica com a força bruta em entradas aleatórias. Cada caso traz entrada, saída esperada e justificativa.

## Medições

```bash
npm run bench             # results/medicoes.csv e results/maquina.json
npm run bench:limiar      # results/limiar.csv
npm run bench:cruzamento  # results/cruzamento.csv
npm run bench:ordenacao  # results/ordenacao.csv
npm run bench:resumo      # results/resumo.csv
```

Cada tamanho tem 20 execuções, com entradas de semente fixa. O código é aquecido antes de medir, e as entradas de cada execução são iguais para todos os algoritmos.

A coleta de lixo não é forçada entre as medições: chamar `gc()` antes de cada uma criava dois patamares de tempo, de cerca de 5 ms e 11 ms, numa chamada que leva cerca de 4 ms sem isso. O custo normal de memória faz parte do tempo medido.


## Relatório

O relatório está em `relatorio/relatorio.pdf`.
