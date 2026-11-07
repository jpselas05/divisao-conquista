"""Leitura dos CSVs de results/ e estatísticas usadas no relatório."""
import csv
import json
import math
from pathlib import Path
from statistics import mean, stdev

RESULTS = Path(__file__).resolve().parent.parent / "results"
TAMANHOS = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]


def _ler(nome):
    with open(RESULTS / nome, newline="", encoding="utf-8") as arquivo:
        return list(csv.DictReader(arquivo))


class Dados:
    def __init__(self):
        self.maquina = json.loads((RESULTS / "maquina.json").read_text(encoding="utf-8"))
        self.tempos = {}
        for linha in _ler("medicoes.csv"):
            chave = (linha["etapa"], linha["algoritmo"], int(linha["n"]))
            self.tempos.setdefault(chave, []).append(float(linha["tempo_ms"]))

        self.limiares = {}
        for linha in _ler("limiar.csv"):
            chave = (int(linha["n"]), int(linha["limiar"]))
            self.limiares.setdefault(chave, []).append(float(linha["tempo_ms"]))

        self.cruzamento = {}
        for linha in _ler("cruzamento.csv"):
            chave = (linha["etapa"], linha["algoritmo"], int(linha["n"]))
            self.cruzamento.setdefault(chave, []).append(float(linha["tempo_us_por_chamada"]))

        self.ordenacao = {}
        for linha in _ler("ordenacao.csv"):
            parcial = self.ordenacao.setdefault(int(linha["n"]), ([], []))
            parcial[0].append(float(linha["ordenacao_ms"]))
            parcial[1].append(float(linha["total_ms"]))

    def media(self, etapa, algoritmo, n):
        return mean(self.tempos[(etapa, algoritmo, n)])

    def desvio(self, etapa, algoritmo, n):
        return stdev(self.tempos[(etapa, algoritmo, n)])

    def serie(self, etapa, algoritmo, tamanhos=TAMANHOS):
        return [self.media(etapa, algoritmo, n) for n in tamanhos]

    def expoente(self, etapa, algoritmo, inicio=1600, fim=25600):
        """Inclinação em escala log-log: aproxima k em T(n) proporcional a n^k."""
        razao = self.media(etapa, algoritmo, fim) / self.media(etapa, algoritmo, inicio)
        return math.log(razao) / math.log(fim / inicio)

    def limiar_medio(self, n, limiar):
        return mean(self.limiares[(n, limiar)])

    def lista_limiares(self):
        return sorted({limiar for _, limiar in self.limiares})

    def cruzamento_medio(self, etapa, algoritmo, n):
        return mean(self.cruzamento[(etapa, algoritmo, n)])

    def parcela_ordenacao(self, n):
        ordenacao, total = self.ordenacao[n]
        return mean(ordenacao), mean(total), mean(ordenacao) / mean(total)

    def virada_pequenos(self, etapa):
        """Maior n em que a força bruta vence e o seguinte, nos lotes de entradas pequenas."""
        tamanhos = sorted({n for e, a, n in self.cruzamento if e == etapa and a == "dc"})
        ultimo = None
        for n in tamanhos:
            if self.cruzamento_medio(etapa, "forca-bruta", n) < self.cruzamento_medio(etapa, "dc", n):
                ultimo = n
        proximo = next((n for n in tamanhos if ultimo is not None and n > ultimo), None)
        return ultimo, proximo

    def virada_principal(self, etapa):
        ultimo = None
        for n in TAMANHOS:
            if self.media(etapa, "forca-bruta", n) < self.media(etapa, "dc", n):
                ultimo = n
        proximo = next((n for n in TAMANHOS if ultimo is not None and n > ultimo), None)
        return ultimo, proximo
