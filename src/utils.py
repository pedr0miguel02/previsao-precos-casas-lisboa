"""
Configuração e funções partilhadas por todos os notebooks.

PORQUÊ ESTE FICHEIRO?
Vários notebooks precisam das mesmas coisas: os caminhos das pastas, a lista
de variáveis do modelo, as cores dos gráficos... Em vez de repetir isso em
cada notebook (e arriscar que fiquem diferentes), definimos tudo aqui UMA vez.
Cada notebook "importa" o que precisa com:

    from src.utils import NOME_DA_COISA

Se quisermos mudar algo (ex.: o limite de preço), mudamos só aqui.
"""

# --- Bibliotecas ------------------------------------------------------------
# pathlib.Path: forma moderna de trabalhar com caminhos de ficheiros/pastas,
#               que funciona igual em Windows, Mac e Linux.
from pathlib import Path

import numpy as np                       # cálculos numéricos (ex.: logaritmos)
import matplotlib.pyplot as plt          # gráficos
from matplotlib.ticker import FuncFormatter  # para formatar os eixos (ex.: "500 mil €")


# ===========================================================================
# 1. PASTAS DO PROJETO
# ===========================================================================
# __file__ é o caminho deste ficheiro (src/utils.py).
# .resolve() transforma-o num caminho completo; .parent sobe uma pasta.
# Subindo duas vezes (src/utils.py → src → raiz) chegamos à pasta do projeto.
RAIZ = Path(__file__).resolve().parent.parent

# O operador "/" junta pedaços de caminho: RAIZ / "data" / "raw" = <raiz>/data/raw
DADOS_RAW = RAIZ / "data" / "raw"                 # exportações originais (não publicadas)
DADOS_PROCESSADOS = RAIZ / "data" / "processed"   # dados limpos (não publicados)
FICHEIRO_LIMPO = DADOS_PROCESSADOS / "dados_limpos.csv"
MODELOS = RAIZ / "models"
FICHEIRO_MODELO = MODELOS / "modelo_final.joblib"
RELATORIOS = RAIZ / "reports"
FIGURAS = RELATORIOS / "figures"


# ===========================================================================
# 2. PARÂMETROS GERAIS
# ===========================================================================
# SEMENTE: muitos passos usam "acaso" (ex.: baralhar as casas antes de as
# dividir). Fixar a semente faz com que o "acaso" seja sempre o mesmo, e por
# isso quem correr os notebooks obtém exatamente os mesmos resultados.
SEMENTE = 42

# Âmbito do modelo: só apartamentos até este preço (mercado "normal").
# O "_" é só para facilitar a leitura do número (2_500_000 = 2500000).
PRECO_MAX = 2_500_000


# ===========================================================================
# 3. VARIÁVEIS USADAS PELO MODELO
# ===========================================================================
# Estão divididas em 3 grupos porque cada grupo é preparado de forma diferente
# antes de entrar no modelo (ver notebook 03).

# Números "a sério" (contínuos ou contagens)
NUMERICAS = ["area_m2", "log_area", "quartos", "casas_banho", "andar",
             "latitude", "longitude"]

# Variáveis sim/não, guardadas como 1 (sim), 0 (não) ou vazio (não sabemos)
SIM_NAO = ["elevador", "empreendimento_novo", "terraco", "piscina", "jardim",
           "ar_condicionado", "arrecadacao", "estacionamento"]

# Categorias em texto (não têm ordem numérica)
CATEGORIAS = ["freguesia", "estado", "tipo"]

# Lista completa: o "+" junta as três listas numa só
VARIAVEIS = NUMERICAS + SIM_NAO + CATEGORIAS

# Nomes legíveis para usar nos gráficos.
# Um dicionário ({chave: valor}) funciona como uma tabela de tradução.
NOMES_BONITOS = {
    "area_m2": "Área", "log_area": "Área (log)", "quartos": "Quartos",
    "casas_banho": "Casas de banho", "andar": "Andar", "latitude": "Latitude",
    "longitude": "Longitude", "elevador": "Elevador",
    "empreendimento_novo": "Empreend. novo", "terraco": "Terraço",
    "piscina": "Piscina", "jardim": "Jardim", "ar_condicionado": "Ar condicionado",
    "arrecadacao": "Arrecadação", "estacionamento": "Estacionamento",
    "freguesia": "Freguesia", "estado": "Estado", "tipo": "Tipo",
}

# Tradução dos valores da coluna "estado" (os dados originais vêm em inglês)
NOMES_ESTADO = {"good": "Bom estado", "renew": "Para recuperar",
                "newdevelopment": "Empreendimento novo", "desconhecido": "Desconhecido"}


def preparar_variaveis(df):
    """Acrescenta as variáveis derivadas de que o modelo precisa.

    É usada tanto no treino (notebook 03) como nas previsões (notebook 04),
    para garantir que uma casa nova é preparada EXATAMENTE como as do treino.

    - log_area: logaritmo da área. Ajuda sobretudo a regressão linear, porque
      o preço cresce de forma proporcional à área (não em linha reta).
    - estado: quando falta, passa a 'desconhecido' (uma categoria própria).
    """
    df = df.copy()                                       # cópia, para não alterar a tabela original
    df["log_area"] = np.log(df["area_m2"])               # nova coluna com o logaritmo da área
    df["estado"] = df["estado"].fillna("desconhecido")   # fillna = "preencher os vazios com..."
    return df


# ===========================================================================
# 4. ESTILO DOS GRÁFICOS
# ===========================================================================
# Cores em código hexadecimal (#RRGGBB)
AZUL = "#2a78d6"
TEXTO = "#0b0b0b"      # texto principal (quase preto)
TEXTO_2 = "#52514e"    # texto secundário (cinzento)
GRELHA = "#e6e5e1"     # linhas de grelha (cinzento claro)


def aplicar_estilo():
    """Define o aspeto de todos os gráficos (fundo, cores, grelha, títulos).

    plt.rcParams é o "painel de configurações" do matplotlib: o que mudarmos
    aqui passa a valer para todos os gráficos seguintes.
    """
    plt.rcParams.update({
        "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.edgecolor": GRELHA, "axes.labelcolor": TEXTO_2,
        "xtick.color": TEXTO_2, "ytick.color": TEXTO_2,
        "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlecolor": TEXTO,
        "axes.titlelocation": "left",                             # título alinhado à esquerda
        "axes.spines.top": False, "axes.spines.right": False,     # sem moldura em cima e à direita
        "axes.grid": True, "grid.color": GRELHA, "axes.axisbelow": True,
        "font.size": 10, "figure.dpi": 110,
    })


def _fmt_euros_curto(x, _=None):
    """Formata valores grandes de forma curta: 500000 → '500 mil €', 1500000 → '1,5 M€'."""
    if x == 0:
        return "0 €"
    if x >= 1e6:                                       # 1e6 = 1 000 000
        return f"{x/1e6:g} M€".replace(".", ",")      # :g remove zeros desnecessários
    return f"{x/1000:.0f} mil €"                       # :.0f = sem casas decimais


# FuncFormatter "liga" uma função de formatação a um eixo de um gráfico
euros_curto = FuncFormatter(_fmt_euros_curto)                                # 500 mil € / 1,5 M€
euros = FuncFormatter(lambda x, _=None: f"{x:,.0f} €".replace(",", " "))   # 6 500 €
sem_rotulo = FuncFormatter(lambda x, _=None: "")                            # esconde rótulos


def formatar_euros(valor):
    """Formata um número como euros, com espaço nos milhares: 585000 → '585 000 €'.

    f"{valor:,.0f}" escreve o número com vírgulas nos milhares (585,000);
    depois trocamos as vírgulas por espaços (estilo português).
    """
    return f"{valor:,.0f} €".replace(",", " ")


def num_pt(valor, casas=1):
    """Escreve um número com vírgula decimal, à portuguesa: num_pt(2.5) → '2,5'.

    casas = nº de casas decimais. Ex.: num_pt(0.8312, 2) → '0,83'.
    """
    return f"{valor:.{casas}f}".replace(".", ",")


# Formatador de eixo com vírgula decimal (ex.: 0,05 em vez de 0.05)
decimal_pt = FuncFormatter(lambda x, _=None: f"{x:.2f}".replace(".", ","))


def guardar_figura(fig, nome):
    """Grava o gráfico em reports/figures/ (usado no README do GitHub)."""
    FIGURAS.mkdir(parents=True, exist_ok=True)               # cria a pasta se não existir
    fig.savefig(FIGURAS / nome, dpi=150, bbox_inches="tight")  # dpi = resolução da imagem
