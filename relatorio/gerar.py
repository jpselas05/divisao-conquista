"""Monta relatorio/relatorio.pdf: gráficos, texto e tabelas a partir de results/."""
from pathlib import Path

import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, ListFlowable, ListItem, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

import graficos
from dados import Dados
from secoes import NOMES, blocos

PASTA = Path(__file__).resolve().parent
LARGURA = A4[0] - 4 * cm
TINTA = colors.HexColor("#0b0b0b")
TINTA_2 = colors.HexColor("#52514e")
GRADE = colors.HexColor("#d9d8d3")
FUNDO = colors.HexColor("#f3f2ef")

fontes = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
pdfmetrics.registerFont(TTFont("Corpo", str(fontes / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("Corpo-B", str(fontes / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Corpo-I", str(fontes / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("Corpo-BI", str(fontes / "DejaVuSans-BoldOblique.ttf")))
pdfmetrics.registerFont(TTFont("Mono", str(fontes / "DejaVuSansMono.ttf")))
pdfmetrics.registerFontFamily("Corpo", normal="Corpo", bold="Corpo-B", italic="Corpo-I", boldItalic="Corpo-BI")

P = ParagraphStyle("p", fontName="Corpo", fontSize=9, leading=13.2, textColor=TINTA,
                   alignment=TA_JUSTIFY, spaceAfter=5, allowWidows=0, allowOrphans=0)
H1 = ParagraphStyle("h1", parent=P, fontName="Corpo-B", fontSize=12.5, leading=16, spaceBefore=9,
                    spaceAfter=4, alignment=0, keepWithNext=1)
H2 = ParagraphStyle("h2", parent=H1, fontSize=10, leading=13, spaceBefore=6, spaceAfter=3)
EQ = ParagraphStyle("eq", parent=P, alignment=TA_CENTER, spaceBefore=1, spaceAfter=6)
LEGENDA = ParagraphStyle("legenda", parent=P, fontSize=7.8, leading=10.5, textColor=TINTA_2,
                         alignment=0, spaceBefore=2, spaceAfter=7)
CEL = ParagraphStyle("cel", parent=P, fontSize=7.8, leading=10, alignment=0, spaceAfter=0)
CEL_B = ParagraphStyle("celb", parent=CEL, fontName="Corpo-B")
TITULO = ParagraphStyle("titulo", parent=P, fontName="Corpo-B", fontSize=18, leading=23, alignment=0, spaceAfter=3)
SUB = ParagraphStyle("sub", parent=P, fontSize=9.5, textColor=TINTA_2, alignment=0, spaceAfter=10)


def figura(nome, legenda):
    caminho = PASTA / "figuras" / nome
    largura, altura = ImageReader(str(caminho)).getSize()
    imagem = Image(str(caminho), width=LARGURA, height=LARGURA * altura / largura)
    return KeepTogether([imagem, Paragraph(legenda.replace("&", "&amp;"), LEGENDA)])


def estilo_tabela(extra=()):
    return TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Corpo"), ("FONTSIZE", (0, 0), (-1, -1), 7.2),
        ("TEXTCOLOR", (0, 0), (-1, -1), TINTA), ("LINEBELOW", (0, 0), (-1, -1), 0.3, GRADE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.8), ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3), *extra,
    ])


def tabela_tempos(legenda, linhas):
    larguras = [1.3 * cm, 2.75 * cm, 2.45 * cm, 2.45 * cm, 2.3 * cm, 2.45 * cm, 2.3 * cm]
    tabela = Table(linhas, colWidths=larguras, repeatRows=2)
    tabela.setStyle(estilo_tabela([
        ("SPAN", (1, 0), (4, 0)), ("SPAN", (5, 0), (6, 0)), ("BACKGROUND", (0, 0), (-1, 1), FUNDO),
        ("FONTNAME", (0, 0), (-1, 1), "Corpo-B"), ("FONTNAME", (0, -1), (-1, -1), "Corpo-B"),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("ALIGN", (1, 0), (4, 0), "CENTER"),
        ("ALIGN", (5, 0), (6, 0), "CENTER"), ("LINEABOVE", (0, -1), (-1, -1), 0.7, TINTA_2),
    ]))
    return KeepTogether([tabela, Paragraph(legenda.replace("&", "&amp;"), LEGENDA)])


def tabela_limiar(legenda, linhas):
    larguras = [2.6 * cm] + [(LARGURA - 2.6 * cm) / (len(linhas[0]) - 1)] * (len(linhas[0]) - 1)
    tabela = Table(linhas, colWidths=larguras)
    tabela.setStyle(estilo_tabela([("BACKGROUND", (0, 0), (-1, 0), FUNDO), ("FONTNAME", (0, 0), (-1, 0), "Corpo-B"),
                                   ("ALIGN", (1, 0), (-1, -1), "RIGHT")]))
    return KeepTogether([tabela, Paragraph(legenda.replace("&", "&amp;"), LEGENDA)])


def tabela_casos(linhas):
    corpo = [[Paragraph(c.replace("&", "&amp;"), CEL_B if i == 0 else CEL) for c in linha] for i, linha in enumerate(linhas)]
    tabela = Table(corpo, colWidths=[1.1 * cm, 6.3 * cm, LARGURA - 7.4 * cm], repeatRows=1)
    tabela.setStyle(estilo_tabela([("BACKGROUND", (0, 0), (-1, 0), FUNDO), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return tabela


def lista(itens):
    return ListFlowable([ListItem(Paragraph(item, P), leftIndent=12) for item in itens],
                        bulletType="bullet", start="•", bulletFontName="Corpo", bulletFontSize=8,
                        leftIndent=12)


def rodape(canvas, doc):
    canvas.setFont("Corpo", 7.5)
    canvas.setFillColor(TINTA_2)
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, str(doc.page))


def montar():
    dados = Dados()
    graficos.gerar(dados)
    historia = [Paragraph("Trabalho Prático: Divisão e Conquista", TITULO),
                Paragraph(f"{NOMES} · Novembro de 2026", SUB)]
    for tipo, conteudo in blocos(dados):
        if tipo == "h1":
            historia.append(Paragraph(conteudo, H1))
        elif tipo == "h2":
            historia.append(Paragraph(conteudo, H2))
        elif tipo == "p":
            historia.append(Paragraph(conteudo, P))
        elif tipo == "eq":
            historia.append(Paragraph(conteudo.replace("      ", "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"), EQ))
        elif tipo == "lista":
            historia.extend([lista(conteudo), Spacer(1, 4)])
        elif tipo == "tabela_casos":
            historia.extend([tabela_casos(conteudo), Spacer(1, 7)])
        elif tipo == "tabela_tempos":
            historia.append(tabela_tempos(*conteudo))
        elif tipo == "tabela_limiar":
            historia.append(tabela_limiar(*conteudo))
        elif tipo == "figura":
            historia.append(figura(*conteudo))

    doc = SimpleDocTemplate(str(PASTA / "relatorio.pdf"), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=1.8 * cm, bottomMargin=1.8 * cm, title="Trabalho Prático: Divisão e Conquista",
                            author=NOMES)
    doc.build(historia, onFirstPage=rodape, onLaterPages=rodape)
    print(f"Relatório gerado com {doc.page} páginas.")


if __name__ == "__main__":
    montar()
