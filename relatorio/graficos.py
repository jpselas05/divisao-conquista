"""Gera os gráficos do relatório em relatorio/figuras/ a partir dos CSVs."""
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, NullFormatter, NullLocator

from dados import TAMANHOS, Dados

FIGURAS = Path(__file__).resolve().parent / "figuras"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
GRADE = "#e6e5e1"
SUPERFICIE = "#ffffff"

# Cada algoritmo mantém cor e marcador em todas as figuras, inclusive impressas em P&B.
ESTILO = {
    "forca-bruta": dict(color="#2a78d6", marker="o", label="Força bruta"),
    "dc": dict(color="#eb6834", marker="s", label="D&C"),
    "dc-linear": dict(color="#1baf7a", marker="^", label="D&C O(n)"),
    "kadane": dict(color="#eda100", marker="D", label="Kadane"),
}

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": GRADE,
    "axes.labelcolor": TINTA_2, "xtick.color": TINTA_2, "ytick.color": TINTA_2,
    "text.color": TINTA, "axes.grid": True, "grid.color": GRADE, "grid.linewidth": 0.6,
    "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False,
    "xtick.major.size": 0, "ytick.major.size": 0, "legend.frameon": False,
    "axes.titlesize": 8.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
})


def numero_br(valor, _=None):
    if valor >= 1:
        return f"{valor:,.0f}".replace(",", ".")
    return f"{valor:g}".replace(".", ",")


def linha(eixo, xs, ys, algoritmo):
    eixo.plot(xs, ys, linewidth=1.6, markersize=4.5, markeredgecolor=SUPERFICIE,
              markeredgewidth=0.7, **ESTILO[algoritmo])


def eixo_n(eixo, ticks):
    eixo.set_xscale("log", base=2)
    eixo.xaxis.set_major_locator(matplotlib.ticker.FixedLocator(ticks))
    eixo.xaxis.set_major_formatter(FuncFormatter(numero_br))
    eixo.xaxis.set_minor_locator(NullLocator())
    eixo.xaxis.set_minor_formatter(NullFormatter())


def legenda(eixo, colunas=2):
    eixo.legend(loc="upper left", ncol=colunas, fontsize=7.5, handlelength=2,
                columnspacing=1.2, borderaxespad=0.2)


def salvar(figura, nome):
    FIGURAS.mkdir(exist_ok=True)
    figura.savefig(FIGURAS / nome, dpi=220, facecolor=SUPERFICIE, bbox_inches="tight")
    plt.close(figura)


def figura_tempos(dados):
    figura, eixos = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    grupos = [("etapa1", list(ESTILO), "Etapa 1: subarranjo de soma máxima"),
              ("etapa2", ["forca-bruta", "dc"], "Etapa 2: par de pontos mais próximos")]
    ticks = [100, 400, 1600, 6400, 25600]
    for eixo, (etapa, algoritmos, titulo) in zip(eixos, grupos):
        for algoritmo in algoritmos:
            linha(eixo, TAMANHOS, dados.serie(etapa, algoritmo), algoritmo)
        eixo_n(eixo, ticks)
        eixo.set_yscale("log")
        eixo.yaxis.set_major_formatter(FuncFormatter(numero_br))
        eixo.yaxis.set_minor_locator(NullLocator())
        eixo.set_title(titulo)
        eixo.set_xlabel("Tamanho da entrada (n)")
        eixo.set_ylim(top=dados.media("etapa2", "forca-bruta", 25600) * 30)
        legenda(eixo)
    eixos[0].set_ylabel("Tempo médio (ms, escala log)")
    salvar(figura, "tempos.png")


def figura_normalizada(dados):
    previsto = {
        "forca-bruta": lambda n: n * n,
        "dc": lambda n: n * math.log2(n),
        "dc-linear": lambda n: n,
        "kadane": lambda n: n,
    }
    figura, eixos = plt.subplots(1, 2, figsize=(7.2, 2.5), sharey=True)
    tamanhos = [n for n in TAMANHOS if n >= 800]
    grupos = [("etapa1", list(ESTILO), "Etapa 1"), ("etapa2", ["forca-bruta", "dc"], "Etapa 2")]
    for eixo, (etapa, algoritmos, titulo) in zip(eixos, grupos):
        eixo.axhline(1, color=TINTA_2, linewidth=0.9, linestyle="--")
        for algoritmo in algoritmos:
            bruto = [t / previsto[algoritmo](n) for t, n in zip(dados.serie(etapa, algoritmo, tamanhos), tamanhos)]
            linha(eixo, tamanhos, [valor / bruto[-1] for valor in bruto], algoritmo)
        eixo_n(eixo, [800, 1600, 3200, 6400, 12800, 25600])
        eixo.set_title(titulo)
        eixo.set_xlabel("Tamanho da entrada (n)")
        eixo.set_ylim(0, 2.6)
        eixo.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ",")))
        legenda(eixo)
    eixos[0].set_ylabel("T(n) / previsto (1 = n = 25.600)")
    salvar(figura, "normalizado.png")


def figura_cruzamento(dados):
    figura, eixos = plt.subplots(1, 2, figsize=(7.2, 2.6))
    pequenos = [2, 4, 8, 16, 32, 64, 128, 256, 512]
    for algoritmo in ("forca-bruta", "dc"):
        ys = [dados.cruzamento_medio("etapa1", algoritmo, n) for n in pequenos]
        linha(eixos[0], pequenos, ys, algoritmo)
    tamanhos = [100, 200, 400, 800, 1600, 3200]
    for algoritmo in ("forca-bruta", "dc"):
        linha(eixos[1], tamanhos, dados.serie("etapa2", algoritmo, tamanhos), algoritmo)

    eixo_n(eixos[0], [2, 8, 32, 128, 512])
    eixo_n(eixos[1], tamanhos)
    eixos[0].set_title("Etapa 1: entradas pequenas")
    eixos[1].set_title("Etapa 2: entradas até 3.200")
    eixos[0].set_ylabel("Tempo médio por chamada (µs, log)")
    eixos[1].set_ylabel("Tempo médio (ms, log)")
    for eixo in eixos:
        eixo.set_yscale("log")
        eixo.yaxis.set_major_formatter(FuncFormatter(numero_br))
        eixo.yaxis.set_minor_locator(NullLocator())
        eixo.set_xlabel("Tamanho da entrada (n)")
        legenda(eixo, colunas=1)
    salvar(figura, "cruzamento.png")


def figura_limiar(dados):
    figura, eixos = plt.subplots(1, 2, figsize=(7.2, 2.4))
    limiares = dados.lista_limiares()
    for eixo, n in zip(eixos, (6400, 25600)):
        ys = [dados.limiar_medio(n, limiar) for limiar in limiares]
        eixo.axvspan(16, 96, color="#2a78d6", alpha=0.08, linewidth=0)
        eixo.axvline(32, color=TINTA_2, linewidth=0.9, linestyle="--")
        linha(eixo, limiares, ys, "dc")
        eixo.annotate("limiar 32", (32, max(ys)), xytext=(4, -2), textcoords="offset points",
                      fontsize=7.5, color=TINTA_2, va="top")
        eixo_n(eixo, [2, 4, 8, 16, 32, 64, 128, 256])
        eixo.set_title(f"n = {numero_br(n)}")
        eixo.set_xlabel("Limiar de corte da recursão")
        eixo.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ",")))
    eixos[0].set_ylabel("Tempo médio (ms)")
    salvar(figura, "limiar.png")


def gerar(dados=None):
    dados = dados or Dados()
    figura_tempos(dados)
    figura_normalizada(dados)
    figura_cruzamento(dados)
    figura_limiar(dados)


if __name__ == "__main__":
    gerar()
