"""Texto do relatório. Números de medição vêm sempre de Dados, nunca digitados à mão."""
from dados import TAMANHOS

NOMES = "João Pedro Sales Melo | 2510426 e Igor Roberto Freitas Barbosa | 2510420"
REPOSITORIO = "https://github.com/jpselas05/divisao-conquista"


def br(valor, casas=2):
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def inteiro(valor):
    return f"{valor:,}".replace(",", ".")


def por_cento(valor):
    return f"{valor * 100:.0f}%"


def celula(dados, etapa, algoritmo, n):
    media = dados.media(etapa, algoritmo, n)
    desvio = dados.desvio(etapa, algoritmo, n)
    casas = 4 if media < 0.1 else 3 if media < 1 else 2 if media < 100 else 1
    return f"{br(media, casas)} ± {br(desvio, casas)}"


def tabela_tempos(dados):
    colunas = [("etapa1", "forca-bruta"), ("etapa1", "dc"), ("etapa1", "dc-linear"),
               ("etapa1", "kadane"), ("etapa2", "forca-bruta"), ("etapa2", "dc")]
    corpo = [[inteiro(n)] + [celula(dados, e, a, n) for e, a in colunas] for n in TAMANHOS]
    expoentes = ["Expoente"] + [br(dados.expoente(e, a)) for e, a in colunas]
    cabecalho1 = ["", "Etapa 1 (ms)", "", "", "", "Etapa 2 (ms)", ""]
    cabecalho2 = ["n", "Força bruta", "D&C", "D&C O(n)", "Kadane", "Força bruta", "D&C"]
    return [cabecalho1, cabecalho2, *corpo, expoentes]


def tabela_limiar(dados):
    limiares = [2, 4, 8, 16, 32, 64, 128, 256]
    linhas = [["Limiar"] + [str(limiar) for limiar in limiares]]
    for n in (6400, 25600):
        linhas.append([f"n = {inteiro(n)}"] + [br(dados.limiar_medio(n, limiar)) for limiar in limiares])
    return linhas


CASOS_DE_BORDA = [
    ["Etapa", "Situação", "Por que está na bateria"],
    ["1", "Somente negativos", "A resposta é o maior valor isolado, nunca um intervalo vazio de soma 0."],
    ["1", "Tamanho 1 (positivo, negativo e zero)", "Exercita o caso base da recursão."],
    ["1", "Empates (disjuntos, entre negativos, com prefixo ou sufixo de soma 0, todos zeros)",
     "Revelam diferenças entre as versões; pegam recomeço indevido quando a soma parcial é 0."],
    ["1", "Resposta à esquerda, à direita e cruzando o meio", "Cobrem os três candidatos da combinação."],
    ["1", "Soma acima de 2³¹", "Revelaria somas limitadas a 32 bits."],
    ["2", "Dois pontos e um único ponto", "Menor entrada válida e entrada sem par, que deve gerar erro."],
    ["2", "Pontos duplicados", "A distância 0 esvazia a faixa."],
    ["2", "Todos com o mesmo x ou o mesmo y", "A divisão e a ordenação por y ficam totalmente empatadas."],
    ["2", "Par em lados opostos da linha", "Só a verificação da faixa encontra a resposta."],
    ["2", "Quadrado e grades 3×3 e 6×6", "Geram empates e o arranjo denso que justifica as 7 comparações."],
    ["2", "Coordenadas negativas e decimais", "Confirmam a ordenação numérica e a entrada não inteira."],
]


def blocos(dados):
    """Sequência de blocos: (tipo, conteúdo), interpretada por gerar.py."""
    maq = dados.maquina
    e1_ultimo, e1_prox = dados.virada_pequenos("etapa1")
    e2_ultimo, e2_prox = dados.virada_principal("etapa2")
    ord_1600 = dados.parcela_ordenacao(1600)
    ord_25600 = dados.parcela_ordenacao(25600)
    bruta_e1 = dados.media("etapa1", "forca-bruta", 25600)
    dc_e1 = dados.media("etapa1", "dc", 25600)
    kadane_e1 = dados.media("etapa1", "kadane", 25600)
    bruta_e2 = dados.media("etapa2", "forca-bruta", 25600)
    dc_e2 = dados.media("etapa2", "dc", 25600)

    return [
        ("h1", "1. Introdução"),
        ("p", "Este relatório descreve a implementação, em TypeScript, de dois problemas resolvidos por "
              "divisão e conquista (D&amp;C), o subarranjo de soma máxima e o par de pontos mais próximos, "
              "ambos comparados a uma solução de força bruta. O objetivo é verificar se o tempo medido segue "
              "a complexidade prevista pela recorrência de cada algoritmo. O código, os casos de teste e as "
              f"medições brutas estão no repositório: {REPOSITORIO}."),
        ("h2", "Premissas adotadas"),
        ("p", "O enunciado deixa alguns pontos em aberto. As decisões tomadas foram:"),
        ("lista", [
            "<b>Índices:</b> a saída numera as posições a partir de 0.",
            "<b>Empates na Etapa 1:</b> vale o menor início e, depois, o menor fim. As quatro versões devolvem "
            "exatamente o mesmo intervalo.",
            "<b>Empates na Etapa 2:</b> qualquer par com a distância mínima é aceito.",
            "<b>Formato da Etapa 2:</b> a entrada é n seguido de n pares x y; a saída é a distância e os índices "
            "das duas estações.",
            "<b>Versão O(n):</b> a “questão desafio” citada nos critérios não é definida no enunciado. Foi "
            "interpretada como uma versão linear da Etapa 1, implementada de duas formas: o algoritmo de "
            "Kadane e uma D&amp;C com combinação em tempo constante.",
            "<b>Limiar:</b> foi interpretado como o tamanho em que a recursão da Etapa 2 passa a usar força bruta.",
            "<b>Medição de tamanhos:</b> a Etapa 3 fala em “dígitos” para a Etapa 2; os valores foram tratados "
            "como número de pontos.",
        ]),

        ("h1", "2. Etapa 1: subarranjo de soma máxima"),
        ("p", "Dado um vetor de n inteiros, procura-se o intervalo contínuo de maior soma."),
        ("p", "<b>Força bruta.</b> Para cada início, percorre todos os fins possíveis, reaproveitando a soma "
              "parcial. O número de intervalos é n(n + 1)/2, logo T(n) = Θ(n²)."),
        ("p", "<b>Divisão e conquista.</b> O vetor é dividido ao meio, e a resposta é a maior entre a melhor da "
              "esquerda, a melhor da direita e a melhor que cruza o meio. A última sai de duas varreduras a "
              "partir do meio, em Θ(n):"),
        ("eq", "T(1) = Θ(1)      T(n) = 2T(n/2) + Θ(n)"),
        ("p", "Pelo Teorema Mestre, com a = 2, b = 2 e f(n) = Θ(n) = Θ(n<super>log₂2</super>), vale o caso 2, e "
              "T(n) = Θ(n log n). A árvore de recursão mostra o mesmo: são log₂ n níveis, cada um com custo "
              "total Θ(n)."),
        ("p", "<b>D&amp;C com combinação constante.</b> Cada chamada devolve quatro valores do seu trecho: a soma "
              "total, o melhor prefixo, o melhor sufixo e o melhor intervalo. Com eles, as duas metades são "
              "combinadas sem varrer o vetor:"),
        ("eq", "T(1) = Θ(1)      T(n) = 2T(n/2) + Θ(1)"),
        ("p", "Como f(n) = Θ(1) = O(n<super>1−ε</super>), vale o caso 1 do Teorema Mestre, e T(n) = Θ(n)."),
        ("p", "<b>Kadane.</b> Não usa divisão e conquista: guarda a melhor soma que termina em cada posição e "
              "recomeça somente quando a soma acumulada fica negativa. Assim, T(n) = T(n − 1) + Θ(1) = Θ(n)."),

        ("h1", "3. Etapa 2: par de pontos mais próximos"),
        ("p", "<b>Força bruta.</b> Compara os n(n − 1)/2 pares, logo T(n) = Θ(n²). As comparações usam a distância "
              "ao quadrado, e a raiz só é calculada na resposta."),
        ("p", "<b>Divisão e conquista.</b> Os pontos são ordenados por x e por y uma única vez, com a função da "
              "biblioteca padrão, em Θ(n log n). A recursão divide na mediana de x e preserva a ordem por y ao "
              "separar a lista de cada lado, em Θ(n), sem ordenar de novo. Após resolver os dois lados e obter "
              "δ, percorre a faixa de largura 2δ em ordem de y. Abaixo do limiar L, usa força bruta:"),
        ("eq", "T(n) = Θ(1) para n ≤ L      T(n) = 2T(n/2) + Θ(n) para n > L"),
        ("p", "Vale novamente o caso 2 do Teorema Mestre, com total Θ(n log n), somado à ordenação inicial, de "
              "mesma ordem. Para L fixo, o custo detalhado é Θ(n log(n/L) + nL): há cerca de log₂(n/L) níveis de "
              "combinação e cerca de n/L folhas de custo Θ(L²). O primeiro termo diminui com L e o segundo cresce, "
              "o que motiva a busca por um limiar intermediário (seção 6.3)."),
        ("h2", "Por que bastam 7 comparações por ponto"),
        ("p", "Seja δ a menor distância encontrada nos dois lados. Um par melhor, com um ponto em cada lado, precisa "
              "estar na faixa e ter diferença de y menor que δ. Fixado um ponto p da faixa, os candidatos seguintes "
              "em ordem de y estão em um retângulo de largura 2δ e altura δ, centrado na linha divisória."),
        ("p", "Divida o retângulo em 8 quadrados de lado δ/2, 4 em cada lado da linha. Dois pontos do mesmo lado têm "
              "distância de pelo menos δ, mas dois pontos no mesmo quadrado estariam a no máximo δ/√2 &lt; δ. Portanto, "
              "cada quadrado guarda no máximo um ponto do seu lado, e o retângulo guarda no máximo 8 pontos. Como p "
              "é um deles, restam no máximo 7 candidatos. Isso limita a combinação a Θ(n), e a implementação ainda "
              "interrompe a busca assim que a diferença de y alcança δ."),

        ("h1", "4. Testes"),
        ("p", "A bateria é executada por <font face='Mono'>npm test</font>. Ela tem 26 casos com entrada, saída "
              "esperada e justificativa (15 da Etapa 1 e 11 da Etapa 2), passados pelos programas reais com a "
              "entrada padrão em cada versão, o que resulta em 82 verificações. Depois, compara a técnica com a força "
              "bruta em 3.000 entradas aleatórias por etapa, em 27.000 comparações. A Etapa 1 usa valores em faixa "
              "pequena para forçar empates; a Etapa 2 usa grades que forçam duplicatas e x repetidos e testa vários "
              "limiares. Todas as 27.082 verificações foram aprovadas."),
        ("tabela_casos", CASOS_DE_BORDA),
        ("p", "Para confirmar que a bateria detecta erros, cinco defeitos foram introduzidos de propósito, um por vez: "
              "a faixa com 1 vizinho, a retirada da faixa, o recomeço do Kadane com soma zero, o desempate errado no "
              "cruzamento e a D&amp;C linear sem o cruzamento. Todos foram detectados."),

        ("h1", "5. Metodologia experimental"),
        ("p", f"As medições usaram um processador {maq['cpu']}, com {maq['memoria_gb']} GB de memória, Windows 11 e "
              f"Node.js {maq['node'].lstrip('v')} (V8), na tomada e com outros programas abertos. Os tamanhos vão de 100 a 25.600, "
              "indo além dos sugeridos no enunciado. Cada tamanho teve 20 execuções, com entradas aleatórias de semente "
              "fixa, iguais para todos os algoritmos. Antes de medir, o código é executado várias vezes, e esse tempo é "
              "descartado, para que o compilador JIT do V8 otimize o código. A Etapa 1 usa inteiros em [−1.000, 1.000], "
              "e a Etapa 2, pontos uniformes em um plano de lado 10⁶."),
        ("p", "<b>Ameaça à validade corrigida.</b> A primeira versão forçava a coleta de lixo antes de cada medição, o "
              "que criou tempos em dois patamares: entradas iguais levavam de 5 a 16 ms, contra cerca de 4 ms sem a "
              "coleta forçada. Por isso, ela foi removida, e o custo normal de memória faz parte do tempo medido. Os "
              "tempos muito pequenos, abaixo de 0,1 ms, seguem mais sujeitos a ruído e ao JIT."),

        ("h1", "6. Resultados e discussão"),
        ("h2", "6.1. Crescimento observado e previsto"),
        ("p", "A Tabela 1 traz a média e o desvio padrão. A última linha estima o expoente k de T(n) ≈ c·n<super>k</super> "
              "entre n = 1.600 e n = 25.600: o previsto é 2 para a força bruta, pouco acima de 1 para Θ(n log n) e 1 para "
              "Θ(n)."),
        ("tabela_tempos", ("Tabela 1. Tempo médio ± desvio padrão, em ms, com 20 execuções por tamanho.", tabela_tempos(dados))),
        ("figura", ("tempos.png", "Figura 1. Tempo médio por tamanho de entrada, em escalas logarítmicas.")),
        ("p", f"Na Figura 1, as retas confirmam o previsto. Em n = 25.600, a força bruta da Etapa 1 levou {br(bruta_e1, 1)} ms, "
              f"contra {br(dc_e1)} ms da D&amp;C e {br(kadane_e1, 3)} ms do Kadane. Na Etapa 2, foram {br(bruta_e2, 1)} ms "
              f"contra {br(dc_e2, 1)} ms. Os expoentes da força bruta foram {br(dados.expoente('etapa1', 'forca-bruta'))} e "
              f"{br(dados.expoente('etapa2', 'forca-bruta'))}, próximos de 2. O valor da Etapa 2 "
              "vem principalmente do último salto, de n = 12.800 para 25.600, compatível com efeitos de cache, que não foram "
              "medidos diretamente."),
        ("figura", ("normalizado.png", "Figura 2. Tempo dividido pelo crescimento previsto (n², n log n ou n), com 1 em n = 25.600. "
                                       "Uma linha plana indica concordância com a análise.")),
        ("p", "A Figura 2 divide cada tempo pelo crescimento previsto; uma curva plana concorda com a análise. A força bruta e a "
              "D&amp;C da Etapa 1 são as mais estáveis. As curvas de Θ(n) variam mais, pois seus tempos são muito curtos; isso "
              f"explica o expoente {br(dados.expoente('etapa1', 'kadane'))} do Kadane, abaixo do valor teórico de 1. "
              f"Há uma anomalia: em n = 6.400, a D&amp;C O(n) ({br(dados.media('etapa1', 'dc-linear', 6400), 3)} ms) quase empata com a "
              f"D&amp;C Θ(n log n) ({br(dados.media('etapa1', 'dc', 6400), 3)} ms), apesar de ter complexidade menor. A D&amp;C O(n) cria "
              "um objeto por chamada, e seu custo depende da memória e do JIT, de modo que a ordem assintótica só aparece com "
              f"entradas maiores. Em n = 25.600, ela já é mais rápida ({br(dados.media('etapa1', 'dc-linear', 25600))} ms contra "
              f"{br(dc_e1)} ms). O Kadane, sem recursão nem alocação, é o mais rápido em todos os tamanhos."),

        ("h2", "6.2. Quando a força bruta vence e quando a técnica vence"),
        ("figura", ("cruzamento.png", "Figura 3. Comparação perto do ponto de virada. Na Etapa 1, cada medição é um lote de chamadas.")),
        ("p", "Para n pequeno, a constante pesa mais que a ordem de crescimento. A força bruta tem laços simples, sem chamadas nem "
              f"alocações. Na Etapa 1, ela vence até n = {e1_ultimo}, e a D&amp;C passa a vencer em n = {e1_prox}. Como a D&amp;C "
              "gasta pouco em cada chamada, a virada chega cedo."),
        ("p", f"Na Etapa 2, a virada é bem mais tardia: a força bruta vence até n = {inteiro(e2_ultimo)}, e a D&amp;C vence a partir de "
              f"n = {inteiro(e2_prox)}. O motivo é que a D&amp;C paga duas ordenações com comparador e aloca listas a cada nível. As "
              f"ordenações, sozinhas, consomem {por_cento(ord_1600[2])} do tempo total em n = 1.600 e {por_cento(ord_25600[2])} em "
              "n = 25.600. Depois da virada, a diferença entre as ordens de crescimento domina: ao dobrar n, o tempo da força bruta "
              "fica cerca de 4 vezes maior, e o da D&amp;C, pouco mais de 2 vezes."),

        ("h2", "6.3. Escolha do limiar da Etapa 2"),
        ("tabela_limiar", ("Tabela 2. Tempo médio, em ms, da D&C da Etapa 2 para alguns limiares, com 20 execuções.", tabela_limiar(dados))),
        ("figura", ("limiar.png", "Figura 4. Efeito do limiar. A área destacada marca a faixa de valores praticamente empatados.")),
        ("p", "O resultado tem a forma de U prevista por Θ(n log(n/L) + nL). Limiares muito baixos fazem mais chamadas e alocações, "
              "enquanto limiares muito altos deixam folhas quadráticas grandes. Entre 16 e 96, porém, as diferenças ficam dentro do "
              "ruído, e o melhor valor exato mudou entre rodadas repetidas. Não existe, portanto, um único limiar ótimo "
              "nessas medições. O valor adotado foi <b>L = 32</b>, por estar no meio dessa faixa, longe das duas extremidades ruins."),
        ("p", "A baixa sensibilidade tem uma explicação: as ordenações iniciais, que dominam o tempo total, não dependem do limiar. "
              f"Note também que L = 32 é muito menor que a virada do algoritmo completo, entre {inteiro(e2_ultimo)} e {inteiro(e2_prox)} pontos: "
              "na folha, a força bruta compete só com a recursão, sem custo adicional de ordenação."),

        ("h1", "7. Conclusão"),
        ("p", "Os experimentos confirmaram as complexidades previstas: tempo quadrático nas forças brutas, crescimento próximo "
              "de n log n nas versões de divisão e conquista e linear nas versões O(n). Mesmo assim, a análise assintótica não "
              "conta a história inteira. As constantes definem quem vence em entradas pequenas, adiam a virada da Etapa 2 para "
              "perto de mil pontos e explicam por que uma versão O(n) pode empatar com outra Θ(n log n). A medição também "
              "exigiu cuidado: a coleta de lixo forçada chegou a distorcer os resultados."),
        ("p", "Como limitação, as medições foram feitas com outros programas abertos, e os tempos muito curtos têm mais ruído. "
              "Além disso, os resultados são de uma única máquina, embora os CSVs brutos e as sementes fixas permitam "
              "repetir todo o experimento."),
    ]
