# pylint: disable=too-many-lines, disable=line-too-long
"""Resolução do trabalho 4 de Circuitos Elétricos II."""
from dataclasses import dataclass
from dataclasses import field
from math import cos
from math import exp
from math import inf
from math import pi
from typing import List
from typing import Tuple
from typing import TypeAlias

import numpy
from matplotlib import pyplot


@dataclass
class Resitor:
    """Representa um ramo com resitor."""

    identificacao: str
    no1: int
    no2: int
    valor: float


@dataclass
class FonteDeCorrenteDC:
    """Representa um ramo com fonte de corrente DC."""

    identificacao: str
    no1: int
    no2: int
    valor: float


@dataclass
class FonteDeTensaoDC:
    """Representa um ramo com fonte de tensão DC."""

    identificacao: str
    no1: int
    no2: int
    valor: float
    posicao_variavel_de_corrente: int


@dataclass
class FonteDeCorrenteSenoidal:
    """Representa um ramo com fonte de corrente senoidal."""

    identificacao: str
    no1: int
    no2: int
    valor: float
    amplitude: float
    frequencia_hz: float
    fase_graus: float


@dataclass
# pylint: disable-next=too-many-instance-attributes
class FonteDeTensaoSenoidal:
    """Representa um ramo com fonte de tensão senoidal."""

    identificacao: str
    no1: int
    no2: int
    valor: float
    amplitude: float
    frequencia_hz: float
    fase_graus: float
    posicao_variavel_de_corrente: int


@dataclass
# pylint: disable-next=too-many-instance-attributes
class FonteDeCorrentePulso:
    """Representa um ramo com fonte de corrente de pulso."""

    identificacao: str
    no1: int
    no2: int
    valor1: float
    valor2: float
    delay: float
    tempo_subida: float
    tempo_descida: float
    tempo_v2: float
    periodo: float


@dataclass
# pylint: disable-next=too-many-instance-attributes
class FonteDeTensaoPulso:
    """Representa um ramo com fonte de tensão de pulso."""

    identificacao: str
    no1: int
    no2: int
    valor1: float
    valor2: float
    delay: float
    tempo_subida: float
    tempo_descida: float
    tempo_v2: float
    periodo: float
    posicao_variavel_de_corrente: int


@dataclass
class FonteDeCorrenteDCControladaPorTensao:
    """Representa um ramo com fonte de corrente controlada por tensão."""

    identificacao: str
    no1: int
    no2: int
    no3: int
    no4: int
    valor: float


@dataclass
class FonteDeCorrenteControladaPorCorrente:
    """Representa um ramo com fonte de corrente controlada por corrente."""

    identificacao: str
    no1: int
    no2: int
    no3: int
    no4: int
    valor: float
    posicao_variavel_de_corrente: int


@dataclass
class FonteDeTensaoControladaPorTensao:
    """Representa um ramo com fonte de tensão controlada por tensão."""

    identificacao: str
    no1: int
    no2: int
    no3: int
    no4: int
    valor: float
    posicao_variavel_de_corrente: int


@dataclass
# pylint: disable-next=too-many-instance-attributes
class FonteDeTensaoControladaPorCorrente:
    """Representa um ramo com fonte de te controlada por corrente."""

    identificacao: str
    no1: int
    no2: int
    no3: int
    no4: int
    valor: float
    posicao_variavel_de_corrente1: int
    posicao_variavel_de_corrente2: int


@dataclass
class Diodo:
    """Representa um ramo com diodo."""

    identificacao: str
    no1: int
    no2: int
    i_s: float
    nvt: float


@dataclass
class Capacitor:
    """Representa um ramo com capacitor."""

    identificacao: str
    no1: int
    no2: int
    valor: float
    condicao_inicial: float


@dataclass
class Indutor:
    """Representa um ramo com indutor."""

    identificacao: str
    no1: int
    no2: int
    valor: float
    condicao_inicial: float
    posicao_variavel_de_corrente: int


@dataclass
# pylint: disable-next=too-many-instance-attributes
class Transformador:
    """Representa um ramo com transformador."""

    identificacao: str
    no1: int
    no2: int
    no3: int
    no4: int
    valor1: float
    valor2: float
    valor_mutuo: float
    posicao_variavel_de_corrente1: int
    posicao_variavel_de_corrente2: int


@dataclass
# pylint: disable-next=too-many-instance-attributes
class Circuito:
    """Representa quais são os componentes de um circuito elétrico."""

    resitores: list[Resitor] = field(default_factory=list)
    fontes_de_corrente_dc: list[FonteDeCorrenteDC] = field(
        default_factory=list
    )
    fontes_de_tensao_dc: list[FonteDeTensaoDC] = field(default_factory=list)
    fontes_de_corrente_senoidal: list[FonteDeCorrenteSenoidal] = field(
        default_factory=list
    )
    fontes_de_tensao_senoidal: list[FonteDeTensaoSenoidal] = field(
        default_factory=list
    )
    fontes_de_corrente_pulso: list[FonteDeCorrentePulso] = field(
        default_factory=list
    )
    fontes_de_tensao_pulso: list[FonteDeTensaoPulso] = field(
        default_factory=list
    )
    fontes_de_corrente_controlada_por_tensao: list[FonteDeCorrenteDCControladaPorTensao] = field(
        default_factory=list
    )
    fontes_de_corrente_controlada_por_corrente: list[FonteDeCorrenteControladaPorCorrente] = field(
        default_factory=list
    )
    fontes_de_tensao_controlada_por_tensao: list[FonteDeTensaoControladaPorTensao] = field(
        default_factory=list
    )
    fontes_de_tensao_controlada_por_corrente: list[FonteDeTensaoControladaPorCorrente] = field(
        default_factory=list
    )
    diodos: list[Diodo] = field(default_factory=list)
    capacitores: list[Capacitor] = field(default_factory=list)
    indutores: list[Indutor] = field(default_factory=list)
    transformadores: list[Transformador] = field(default_factory=list)
    quantidade_de_variaveis_de_corrente: int = 0


MatrizCondutancia: TypeAlias = numpy.ndarray
VetorDeFontes: TypeAlias = numpy.ndarray
VetorDeTensoes: TypeAlias = numpy.ndarray


# pylint: disable-next=too-many-statements,too-many-branches,too-many-locals
def ler_linha(linha: str, circuito: Circuito):
    """Adiciona uma linha da netlist no Circuito."""
    componente = linha.split()

    if componente[0][0] == "R":
        identificacao = componente[0][1:]
        no1 = int(componente[1])
        no2 = int(componente[2])
        valor = float(componente[3])

        circuito.resitores.append(Resitor(identificacao, no1, no2, valor))

    elif componente[0][0] == "G":
        identificacao = componente[0][1:]
        no1 = int(componente[1])
        no2 = int(componente[2])
        no3 = int(componente[3])
        no4 = int(componente[4])
        valor = float(componente[5])

        circuito.fontes_de_corrente_controlada_por_tensao.append(
            FonteDeCorrenteDCControladaPorTensao(
                identificacao, no1, no2, no3, no4, valor
            )
        )

    elif componente[0][0] == "F":
        identificacao = componente[0][1:]
        no1 = int(componente[1])
        no2 = int(componente[2])
        no3 = int(componente[3])
        no4 = int(componente[4])
        valor = float(componente[5])
        posicao = circuito.quantidade_de_variaveis_de_corrente + 1

        circuito.fontes_de_corrente_controlada_por_corrente.append(
            FonteDeCorrenteControladaPorCorrente(
                identificacao, no1, no2, no3, no4, valor, posicao
            )
        )
        circuito.quantidade_de_variaveis_de_corrente += 1

    elif componente[0][0] == "E":
        identificacao = componente[0][1:]
        no1 = int(componente[1])
        no2 = int(componente[2])
        no3 = int(componente[3])
        no4 = int(componente[4])
        valor = float(componente[5])
        posicao = circuito.quantidade_de_variaveis_de_corrente + 1

        circuito.fontes_de_tensao_controlada_por_tensao.append(
            FonteDeTensaoControladaPorTensao(
                identificacao, no1, no2, no3, no4, valor, posicao
            )
        )
        circuito.quantidade_de_variaveis_de_corrente += 1

    elif componente[0][0] == "H":
        identificacao = componente[0][1:]
        no1 = int(componente[1])
        no2 = int(componente[2])
        no3 = int(componente[3])
        no4 = int(componente[4])
        valor = float(componente[5])
        posicao1 = circuito.quantidade_de_variaveis_de_corrente + 1
        posicao2 = posicao1 + 1

        circuito.fontes_de_tensao_controlada_por_corrente.append(
            FonteDeTensaoControladaPorCorrente(
                identificacao, no1, no2, no3, no4, valor, posicao1, posicao2
            )
        )
        circuito.quantidade_de_variaveis_de_corrente += 2

    elif componente[0][0] == "I":
        identificacao = componente[0][1:]
        no1 = int(componente[1])
        no2 = int(componente[2])
        tipo = componente[3]

        if tipo == "DC":
            valor = float(componente[4])

            circuito.fontes_de_corrente_dc.append(
                FonteDeCorrenteDC(identificacao, no1, no2, valor)
            )

        elif tipo == "SIN":
            valor = float(componente[4])
            amplitude = float(componente[5])
            frequencia = float(componente[6])
            fase = float(componente[7])

            circuito.fontes_de_corrente_senoidal.append(
                FonteDeCorrenteSenoidal(
                    identificacao, no1, no2, valor, amplitude, frequencia, fase
                )
            )

        elif tipo == "PULSE":
            valor1 = float(componente[4])
            valor2 = float(componente[5])
            delay = float(componente[6])
            tempo_subida = float(componente[7])
            tempo_descida = float(componente[8])
            tempo_v2 = float(componente[9])
            periodo = float(componente[10])

            circuito.fontes_de_corrente_pulso.append(
                FonteDeCorrentePulso(
                    identificacao,
                    no1,
                    no2,
                    valor1,
                    valor2,
                    delay,
                    tempo_subida,
                    tempo_descida,
                    tempo_v2,
                    periodo,
                )
            )

    elif componente[0][0] == "V":
        identificacao = componente[0][1:]
        no1 = int(componente[1])
        no2 = int(componente[2])
        tipo = componente[3]
        posicao = circuito.quantidade_de_variaveis_de_corrente + 1

        if tipo == "DC":
            valor = float(componente[4])

            circuito.fontes_de_tensao_dc.append(
                FonteDeTensaoDC(identificacao, no1, no2, valor, posicao)
            )

        elif tipo == "SIN":
            valor = float(componente[4])
            amplitude = float(componente[5])
            frequencia = float(componente[6])
            fase = float(componente[7])

            circuito.fontes_de_tensao_senoidal.append(
                FonteDeTensaoSenoidal(
                    identificacao,
                    no1,
                    no2,
                    valor,
                    amplitude,
                    frequencia,
                    fase,
                    posicao
                )
            )

        elif tipo == "PULSE":
            valor1 = float(componente[4])
            valor2 = float(componente[5])
            delay = float(componente[6])
            tempo_subida = float(componente[7])
            tempo_descida = float(componente[8])
            tempo_v2 = float(componente[9])
            periodo = float(componente[10])

            circuito.fontes_de_tensao_pulso.append(
                FonteDeTensaoPulso(
                    identificacao,
                    no1,
                    no2,
                    valor1,
                    valor2,
                    delay,
                    tempo_subida,
                    tempo_descida,
                    tempo_v2,
                    periodo,
                    posicao
                )
            )

        circuito.quantidade_de_variaveis_de_corrente += 1

    elif componente[0][0] == "D":
        identificacao = componente[0][1:]
        no1 = int(componente[1])
        no2 = int(componente[2])
        i_s = float(componente[3])
        nvt = float(componente[4])

        circuito.diodos.append(Diodo(identificacao, no1, no2, i_s, nvt))

    elif componente[0][0] == "C":
        identificacao = componente[0][1:]
        no1 = int(componente[1])
        no2 = int(componente[2])
        valor = float(componente[3])
        condicao_inicial = float(componente[4])

        circuito.capacitores.append(
            Capacitor(identificacao, no1, no2, valor, condicao_inicial)
        )

    elif componente[0][0] == "L":
        identificacao = componente[0][1:]
        no1 = int(componente[1])
        no2 = int(componente[2])
        valor = float(componente[3])
        condicao_inicial = float(componente[4])
        posicao = circuito.quantidade_de_variaveis_de_corrente + 1

        circuito.indutores.append(
            Indutor(identificacao, no1, no2, valor, condicao_inicial, posicao)
        )

        circuito.quantidade_de_variaveis_de_corrente += 1

    elif componente[0][0] == "K":
        identificacao = componente[0][1:]
        no1 = int(componente[1])
        no2 = int(componente[2])
        no3 = int(componente[3])
        no4 = int(componente[4])
        valor1 = float(componente[5])
        valor2 = float(componente[6])
        valor_mutuo = float(componente[7])
        posicao1 = circuito.quantidade_de_variaveis_de_corrente + 1
        posicao2 = posicao1 + 1

        circuito.transformadores.append(
            Transformador(
                identificacao,
                no1,
                no2,
                no3,
                no4,
                valor1,
                valor2,
                valor_mutuo,
                posicao1,
                posicao2
            )
        )

        circuito.quantidade_de_variaveis_de_corrente += 2


def ler_arquivo(nome_arquivo: str) -> Circuito:
    """Ele faz a leitura de um arquivo do tipo netlist e retorna o circuito gerado por ela."""
    circuito = Circuito()
    with open(nome_arquivo, "r", encoding="utf-8") as linhas:
        for linha in linhas:
            linha = linha.strip()
            if len(linha) == 0 or linha[0] == "*":
                continue

            ler_linha(linha, circuito)

    return circuito


elemento_2_nos = Resitor | FonteDeTensaoDC | FonteDeCorrenteDC |\
    FonteDeCorrenteSenoidal | FonteDeTensaoSenoidal |\
    FonteDeCorrentePulso | FonteDeTensaoPulso | Diodo |\
    Capacitor | Indutor


def maior_de_2_nos(
    componente: elemento_2_nos,
    no_atual: int
) -> int:
    """Retorna o maior no de um componete com 2 nós e um nó atual."""
    if componente.no1 > no_atual:
        return componente.no1

    if componente.no2 > no_atual:
        return componente.no2

    return no_atual


elemento_4_nos = FonteDeCorrenteDCControladaPorTensao | FonteDeCorrenteControladaPorCorrente |\
    FonteDeTensaoControladaPorCorrente | FonteDeTensaoControladaPorTensao | Transformador


def maior_de_4_nos(
    componente: elemento_4_nos,
    no_atual: int
) -> int:
    """Retorna o maior no de um componete com 2 nós e um nó atual."""
    if componente.no1 > no_atual:
        return componente.no1

    if componente.no2 > no_atual:
        return componente.no2

    if componente.no3 > no_atual:
        return componente.no1

    if componente.no4 > no_atual:
        return componente.no4

    return no_atual


# pylint: disable-next=too-many-branches,too-many-locals
def pegar_maior_no(circuito: Circuito) -> int:  # noqa: C901
    """Retorna qual é o maior nó do circuito."""
    maior_no = 0

    for resitor in circuito.resitores:
        maior_no = maior_de_2_nos(resitor, maior_no)

    for fonte_corrente_dc in circuito.fontes_de_corrente_dc:
        maior_no = maior_de_2_nos(fonte_corrente_dc, maior_no)

    for fonte_tensao_dc in circuito.fontes_de_tensao_dc:
        maior_no = maior_de_2_nos(fonte_tensao_dc, maior_no)

    for fonte_corrente_senoidal in circuito.fontes_de_corrente_senoidal:
        maior_no = maior_de_2_nos(fonte_corrente_senoidal, maior_no)

    for fonte_tensao_senoidal in circuito.fontes_de_tensao_senoidal:
        maior_no = maior_de_2_nos(fonte_tensao_senoidal, maior_no)

    for fonte_corrente_pulse in circuito.fontes_de_corrente_pulso:
        maior_no = maior_de_2_nos(fonte_corrente_pulse, maior_no)

    for fonte_tensao_pulse in circuito.fontes_de_tensao_pulso:
        maior_no = maior_de_2_nos(fonte_tensao_pulse, maior_no)

    for fonte_corrente_tensao in circuito.fontes_de_corrente_controlada_por_tensao:
        maior_no = maior_de_4_nos(fonte_corrente_tensao, maior_no)

    for fonte_corrente_corrente in circuito.fontes_de_corrente_controlada_por_corrente:
        maior_no = maior_de_4_nos(fonte_corrente_corrente, maior_no)

    for fonte_tensao_tensao in circuito.fontes_de_tensao_controlada_por_tensao:
        maior_no = maior_de_4_nos(fonte_tensao_tensao, maior_no)

    for fonte_tensao_corrente in circuito.fontes_de_tensao_controlada_por_corrente:
        maior_no = maior_de_4_nos(fonte_tensao_corrente, maior_no)

    for diodo in circuito.diodos:
        maior_no = maior_de_2_nos(diodo, maior_no)

    for capacitor in circuito.capacitores:
        maior_no = maior_de_2_nos(capacitor, maior_no)

    for indutor in circuito.indutores:
        maior_no = maior_de_2_nos(indutor, maior_no)

    for transfomador in circuito.transformadores:
        maior_no = maior_de_4_nos(transfomador, maior_no)

    return maior_no


def adicionar_resitor(
    matriz: MatrizCondutancia,
    resitor: Resitor
) -> MatrizCondutancia:
    """Ela adiciona um resitor na matriz de condutância do circuito."""
    matriz[resitor.no1][resitor.no1] += 1 / resitor.valor
    matriz[resitor.no1][resitor.no2] -= 1 / resitor.valor
    matriz[resitor.no2][resitor.no1] -= 1 / resitor.valor
    matriz[resitor.no2][resitor.no2] += 1 / resitor.valor

    return matriz


def adicionar_fonte_de_corrente_dc_controlada_tensao(
    matriz: MatrizCondutancia,
    fonte: FonteDeCorrenteDCControladaPorTensao
) -> MatrizCondutancia:
    """Ela adiciona uma fonte de corrente DC controlada por tensão na matriz de condutância do circuito."""
    matriz[fonte.no1][fonte.no3] += fonte.valor
    matriz[fonte.no1][fonte.no4] -= fonte.valor
    matriz[fonte.no2][fonte.no3] -= fonte.valor
    matriz[fonte.no2][fonte.no4] += fonte.valor

    return matriz


def adicionar_fonte_de_corrente_dc_controlada_corrente(
    matriz: MatrizCondutancia,
    fonte: FonteDeCorrenteControladaPorCorrente,
    maior_no: int
) -> MatrizCondutancia:
    """Adiciona uma fonte de corrente DC controlada por corrente na matriz de condutância do circuito."""
    posicao = maior_no + fonte.posicao_variavel_de_corrente

    matriz[fonte.no1][posicao] += fonte.valor
    matriz[fonte.no2][posicao] -= fonte.valor
    matriz[fonte.no3][posicao] += 1
    matriz[fonte.no4][posicao] -= 1
    matriz[posicao][fonte.no3] -= 1
    matriz[posicao][fonte.no4] += 1

    return matriz


def adicionar_conte_de_tensao_dc_controlada_tensao(
    matriz: MatrizCondutancia,
    fonte: FonteDeTensaoControladaPorTensao,
    maior_no: int
) -> MatrizCondutancia:
    """Ela adiciona uma fonte de tensão DC controlada por tensão na matriz de condutância do circuito."""
    posicao = maior_no + fonte.posicao_variavel_de_corrente

    matriz[fonte.no1][posicao] += 1
    matriz[fonte.no2][posicao] -= 1
    matriz[posicao][fonte.no1] -= 1
    matriz[posicao][fonte.no2] += 1
    matriz[posicao][fonte.no3] += fonte.valor
    matriz[posicao][fonte.no4] -= fonte.valor

    return matriz


def adicionar_fonte_de_tensao_dc_controlada_corrente(
    matriz: MatrizCondutancia,
    fonte: FonteDeTensaoControladaPorCorrente,
    maior_no: int
) -> MatrizCondutancia:
    """Ela adiciona uma fonte de tensão DC controlada por corrente na matriz de condutância do circuito."""
    posicao1 = maior_no + fonte.posicao_variavel_de_corrente1
    posicao2 = maior_no + fonte.posicao_variavel_de_corrente2

    matriz[fonte.no1][posicao2] += 1
    matriz[fonte.no2][posicao2] -= 1
    matriz[fonte.no3][posicao1] += 1
    matriz[fonte.no4][posicao1] -= 1
    matriz[posicao1][fonte.no3] -= 1
    matriz[posicao1][fonte.no4] += 1
    matriz[posicao2][fonte.no1] -= 1
    matriz[posicao2][fonte.no2] += 1
    matriz[posicao2][posicao1] += fonte.valor

    return matriz


def adicionar_fonte_de_corrente_dc(
    vetor: VetorDeFontes,
    fonte: FonteDeCorrenteDC
) -> VetorDeFontes:
    """Ela adiciona uma fonte de corrente DC no vetor de fontes do circuito."""
    vetor[fonte.no1] -= fonte.valor
    vetor[fonte.no2] += fonte.valor

    return vetor


def adicionar_fonte_de_corrente_senoidal(
    vetor: VetorDeFontes,
    fonte: FonteDeCorrenteSenoidal,
    tempo_atual: float
) -> VetorDeFontes:
    """Ela adiciona uma fonte de corrente senoidal no vetor de fontes do circuito."""
    tempo = 2 * pi * fonte.frequencia_hz * tempo_atual
    fase = fonte.fase_graus * (pi / 180)
    valor = (fonte.amplitude * cos(tempo + fase)) + fonte.valor

    fonte_dc = FonteDeCorrenteDC(
        fonte.identificacao,
        fonte.no1,
        fonte.no2,
        valor
    )

    return adicionar_fonte_de_corrente_dc(vetor, fonte_dc)


def adicionar_fonte_de_corrente_pulso(
    vetor: VetorDeFontes,
    fonte: FonteDeCorrentePulso,
    tempo_atual: float
) -> VetorDeFontes:
    """Ela adiciona uma fonte de corrente senoidal no vetor de fontes do circuito."""
    if fonte.delay >= tempo_atual:
        fonte_dc = FonteDeCorrenteDC(
            fonte.identificacao,
            fonte.no1,
            fonte.no2,
            fonte.valor1
        )

        return adicionar_fonte_de_corrente_dc(vetor, fonte_dc)

    tempo = (tempo_atual - fonte.delay) % fonte.periodo
    v_min, v_max = fonte.valor1, fonte.valor2
    t_subida, t_descida, t_on = fonte.tempo_subida, fonte.tempo_descida, fonte.tempo_v2

    if tempo <= t_subida:
        valor = v_min + (((v_min - v_max) * tempo) / t_subida)
    elif tempo <= (t_subida + t_on):
        valor = v_max
    elif tempo <= (t_subida + t_on + t_descida):
        valor = v_max - \
            (((v_max - v_min) * (tempo - t_on - t_subida)) / t_descida)
    else:
        valor = v_min

    fonte_dc = FonteDeCorrenteDC(
        fonte.identificacao,
        fonte.no1,
        fonte.no2,
        valor
    )

    return adicionar_fonte_de_corrente_dc(vetor, fonte_dc)


def adicionar_fonte_de_tensao_dc(
    matriz: MatrizCondutancia,
    vetor: VetorDeFontes,
    fonte: FonteDeTensaoDC,
    maior_no: int
) -> Tuple[MatrizCondutancia, VetorDeFontes]:
    """Ela adiciona uma fonte de tensão DC na matriz de continue e no vetor de fontes do circuito."""
    posicao = maior_no + fonte.posicao_variavel_de_corrente

    vetor[posicao] -= fonte.valor

    matriz[fonte.no1][posicao] += 1
    matriz[fonte.no2][posicao] -= 1
    matriz[posicao][fonte.no1] -= 1
    matriz[posicao][fonte.no2] += 1

    return matriz, vetor


def adicionar_fonte_de_tensao_senoidal(
    matriz: MatrizCondutancia,
    vetor: VetorDeFontes,
    fonte: FonteDeTensaoSenoidal,
    maior_no: int,
    tempo_atual: float
) -> Tuple[MatrizCondutancia, VetorDeFontes]:
    """Ela adiciona uma fonte de corrente senoidal no vetor de fontes do circuito."""
    tempo = 2 * pi * fonte.frequencia_hz * tempo_atual
    fase = fonte.fase_graus * (pi / 180)
    valor = (fonte.amplitude * cos(tempo + fase)) + fonte.valor

    fonte_dc = FonteDeTensaoDC(
        fonte.identificacao,
        fonte.no1,
        fonte.no2,
        valor,
        fonte.posicao_variavel_de_corrente
    )

    return adicionar_fonte_de_tensao_dc(matriz, vetor, fonte_dc, maior_no)


def adicionar_fonte_de_tensao_pulso(
    matriz: MatrizCondutancia,
    vetor: VetorDeFontes,
    fonte: FonteDeTensaoPulso,
    maior_no: int,
    tempo_atual: float
) -> Tuple[MatrizCondutancia, VetorDeFontes]:
    """Ela adiciona uma fonte de corrente senoidal no vetor de fontes do circuito."""
    if fonte.delay >= tempo_atual:
        fonte_dc = FonteDeTensaoDC(
            fonte.identificacao,
            fonte.no1,
            fonte.no2,
            fonte.valor1,
            fonte.posicao_variavel_de_corrente
        )

        return adicionar_fonte_de_tensao_dc(matriz, vetor, fonte_dc, maior_no)

    tempo = (tempo_atual - fonte.delay) % fonte.periodo
    v_min, v_max = fonte.valor1, fonte.valor2
    t_subida, t_descida, t_on = fonte.tempo_subida, fonte.tempo_descida, fonte.tempo_v2

    if tempo <= t_subida:
        valor = v_min + (((v_min - v_max) * tempo) / t_subida)
    elif tempo <= (t_subida + t_on):
        valor = v_max
    elif tempo <= (t_subida + t_on + t_descida):
        valor = v_max - \
            (((v_max - v_min) * (tempo - t_on - t_subida)) / t_descida)
    else:
        valor = v_min

    fonte_dc = FonteDeTensaoDC(
        fonte.identificacao,
        fonte.no1,
        fonte.no2,
        valor,
        fonte.posicao_variavel_de_corrente
    )

    return adicionar_fonte_de_tensao_dc(matriz, vetor, fonte_dc, maior_no)


def adicionar_diodo(
    matriz: MatrizCondutancia,
    vetor: VetorDeFontes,
    diodo: Diodo,
    tensoes_anteriores: VetorDeTensoes
) -> Tuple[MatrizCondutancia, VetorDeFontes]:
    """Adiciona um diodo na matriz de condutancia e no vetor de fontes."""
    tensao_no = tensoes_anteriores[diodo.no1] - tensoes_anteriores[diodo.no2]
    i_s = diodo.i_s * exp(tensao_no / diodo.nvt)
    conduntancia = i_s / diodo.nvt
    corrente = i_s - diodo.i_s - (conduntancia * tensao_no)

    if conduntancia == 0:
        resitencia = inf
    else:
        resitencia = 1.0 / conduntancia

    resitor = Resitor(
        diodo.identificacao,
        diodo.no1,
        diodo.no2,
        resitencia
    )

    fonte = FonteDeCorrenteDC(
        diodo.identificacao,
        diodo.no1,
        diodo.no2,
        corrente
    )

    matriz = adicionar_resitor(matriz, resitor)
    fonte = adicionar_fonte_de_corrente_dc(vetor, fonte)

    return matriz, vetor


def adicionar_capacitor(
    matriz: MatrizCondutancia,
    vetor: VetorDeFontes,
    capacitor: Capacitor,
    tensoes_anteriores: VetorDeTensoes,
    intervalo: float
) -> Tuple[MatrizCondutancia, VetorDeFontes]:
    """Adiciona um capacitor na matriz de condutancia e no vetor de fontes."""
    no1, no2 = capacitor.no1, capacitor.no2
    resistencia = capacitor.valor / intervalo
    corrente = resistencia * \
        (tensoes_anteriores[no1] - tensoes_anteriores[no2])

    resitor = Resitor(capacitor.identificacao, no1, no2, resistencia)
    fonte = FonteDeCorrenteDC(capacitor.identificacao, no1, no2, corrente)

    matriz = adicionar_resitor(matriz, resitor)
    vetor = adicionar_fonte_de_corrente_dc(vetor, fonte)

    return matriz, vetor


# pylint: disable-next=too-many-arguments
def adicionar_indutor(
    matriz: MatrizCondutancia,
    vetor: VetorDeFontes,
    indutor: Indutor,
    tensoes_anteriores: VetorDeTensoes,
    intervalo: float,
    maior_no: int
) -> Tuple[MatrizCondutancia, VetorDeFontes]:
    """Adiciona um capacitor na matriz de condutancia e no vetor de fontes."""
    no1, no2 = indutor.no1, indutor.no2
    no_indutor = maior_no + indutor.posicao_variavel_de_corrente
    resistencia = indutor.valor / intervalo
    tensao = resistencia * (tensoes_anteriores[no_indutor])

    fonte = FonteDeTensaoDC(
        indutor.identificacao, no2, no1, tensao, indutor.posicao_variavel_de_corrente
    )

    matriz, vetor = adicionar_fonte_de_tensao_dc(
        matriz, vetor, fonte, maior_no)
    matriz[no_indutor][no_indutor] += resistencia

    return matriz, vetor


# pylint: disable-next=too-many-arguments,too-many-locals
def adicionar_transformador(
    matriz: MatrizCondutancia,
    vetor: VetorDeFontes,
    transformador: Transformador,
    tensoes_anteriores: VetorDeTensoes,
    intervalo: float,
    maior_no: int
) -> Tuple[MatrizCondutancia, VetorDeFontes]:
    """Adiciona um capacitor na matriz de condutancia e no vetor de fontes."""
    no1, no2 = transformador.no1, transformador.no2
    no3, no4 = transformador.no3, transformador.no4
    no_indutor1 = maior_no + transformador.posicao_variavel_de_corrente1
    no_indutor2 = maior_no + transformador.posicao_variavel_de_corrente2

    indutor1 = transformador.valor1 / intervalo
    indutor2 = transformador.valor2 / intervalo
    indutorm = transformador.valor_mutuo / intervalo

    fonte1 = (indutor1 * tensoes_anteriores[no_indutor1]) + \
        (indutorm * tensoes_anteriores[no_indutor2])
    fonte2 = (indutor2 * tensoes_anteriores[no_indutor2]) + \
        (indutorm * tensoes_anteriores[no_indutor1])

    matriz[no1][no_indutor1] += 1
    matriz[no2][no_indutor1] -= 1
    matriz[no3][no_indutor2] += 1
    matriz[no4][no_indutor2] -= 1
    matriz[no_indutor1][no1] -= 1
    matriz[no_indutor2][no1] += 1
    matriz[no_indutor1][no3] -= 1
    matriz[no_indutor2][no4] += 1
    matriz[no_indutor1][no_indutor1] = indutor1
    matriz[no_indutor2][no_indutor1] = indutorm
    matriz[no_indutor1][no_indutor2] = indutorm
    matriz[no_indutor1][no_indutor2] = indutor1

    vetor[no_indutor1] = fonte1
    vetor[no_indutor2] = fonte2

    return matriz, vetor


def criar_matriz_e_vetor_de_elementos_constantes(
    circuito: Circuito,
    maior_no: int,
) -> Tuple[MatrizCondutancia, VetorDeFontes]:
    """Cria a matriz de condutancia e vetor de fontes de elementos constantes."""
    dimensao = maior_no + circuito.quantidade_de_variaveis_de_corrente + 1
    matriz = numpy.zeros((dimensao, dimensao), dtype=float)
    vetor = numpy.zeros((dimensao), dtype=float)

    for resitor in circuito.resitores:
        matriz = adicionar_resitor(matriz, resitor)

    for fonte_corrente_tensao in circuito.fontes_de_corrente_controlada_por_tensao:
        matriz = adicionar_fonte_de_corrente_dc_controlada_tensao(
            matriz,
            fonte_corrente_tensao
        )

    for fonte_corrente_corrente in circuito.fontes_de_corrente_controlada_por_corrente:
        matriz = adicionar_fonte_de_corrente_dc_controlada_corrente(
            matriz,
            fonte_corrente_corrente,
            maior_no
        )

    for fonte_tensao_tensao in circuito.fontes_de_tensao_controlada_por_tensao:
        matriz = adicionar_conte_de_tensao_dc_controlada_tensao(
            matriz,
            fonte_tensao_tensao,
            maior_no
        )

    for fonte_tensao_corrente in circuito.fontes_de_tensao_controlada_por_corrente:
        matriz = adicionar_fonte_de_tensao_dc_controlada_corrente(
            matriz,
            fonte_tensao_corrente,
            maior_no
        )

    for fonte_corrente in circuito.fontes_de_corrente_dc:
        vetor = adicionar_fonte_de_corrente_dc(vetor, fonte_corrente)

    for fonte_tensao in circuito.fontes_de_tensao_dc:
        matriz, vetor = adicionar_fonte_de_tensao_dc(
            matriz,
            vetor,
            fonte_tensao,
            maior_no
        )

    return matriz, vetor


# pylint: disable-next=too-many-arguments
def adicionar_elementos_temporais(
    circuito: Circuito,
    matriz: MatrizCondutancia,
    vetor: VetorDeFontes,
    maior_no: int,
    tempo_atual: float,
    intervalo: float,
    tensoes_anteriores: VetorDeTensoes
) -> Tuple[MatrizCondutancia, VetorDeFontes]:
    """Função resolve um circuito em um dado momento a partir da matriz e vetores de elementos constantes."""
    for fonte_corrente_senoidal in circuito.fontes_de_corrente_senoidal:
        vetor = adicionar_fonte_de_corrente_senoidal(
            vetor,
            fonte_corrente_senoidal,
            tempo_atual
        )

    for fonte_tensao_senoidal in circuito.fontes_de_tensao_senoidal:
        matriz, vetor = adicionar_fonte_de_tensao_senoidal(
            matriz,
            vetor,
            fonte_tensao_senoidal,
            maior_no,
            tempo_atual
        )

    for fonte_corrente_pulso in circuito.fontes_de_corrente_pulso:
        vetor = adicionar_fonte_de_corrente_pulso(
            vetor,
            fonte_corrente_pulso,
            tempo_atual
        )

    for fonte_tensao_pulso in circuito.fontes_de_tensao_pulso:
        matriz, vetor = adicionar_fonte_de_tensao_pulso(
            matriz,
            vetor,
            fonte_tensao_pulso,
            maior_no,
            tempo_atual
        )

    for capacitor in circuito.capacitores:
        matriz, vetor = adicionar_capacitor(
            matriz,
            vetor,
            capacitor,
            tensoes_anteriores,
            intervalo
        )

    for indutor in circuito.indutores:
        matriz, vetor = adicionar_indutor(
            matriz,
            vetor,
            indutor,
            tensoes_atuais,
            intervalo,
            maior_no
        )

    for transformador in circuito.transformadores:
        matriz, vetor = adicionar_transformador(
            matriz,
            vetor,
            transformador,
            tensoes_atuais,
            intervalo,
            maior_no
        )

    return matriz, vetor


def calcula_circuito_nao_linear(
    circuito: Circuito,
    matriz_temporal: MatrizCondutancia,
    vetor_temporal: VetorDeFontes,
    tensoes_anteriores: VetorDeTensoes,
    tolerancia: float
) -> numpy.ndarray:
    """Calcula a solução de um circuito com elementos não lineares."""
    maxima_interacoes = 1000

    matriz, vetor = numpy.copy(matriz_temporal), numpy.copy(vetor_temporal)
    while maxima_interacoes > 0:
        for diodo in circuito.diodos:
            matriz, vetor = adicionar_diodo(
                matriz, vetor, diodo, tensoes_anteriores
            )

        resultado_parcial = numpy.linalg.solve(matriz[1:, 1:], vetor[1:])

        max_diff = numpy.max(
            numpy.abs(tensoes_anteriores[1:] - resultado_parcial))

        if max_diff < tolerancia:
            break

        tensoes_anteriores = numpy.concatenate(([0], resultado_parcial))
        maxima_interacoes = maxima_interacoes - 1
        matriz, vetor = numpy.copy(matriz_temporal), numpy.copy(vetor_temporal)

    return numpy.linalg.solve(matriz[1:, 1:], vetor[1:])


# pylint: disable-next=too-many-arguments,too-many-locals
def main(
    nome_arquivo: str,
    duracao: float,
    intervalo: float,
    tolerancia: float,
    tensoes_iniciais: List[float],
    nos_desejados: List[int]
):  # -> numpy.ndarray:
    """Função principal onde ele ler um arquivo do formato de uma netlist, faz a solução do circuito e retorna ela."""
    circuito = ler_arquivo(nome_arquivo)
    maior_no = pegar_maior_no(circuito)
    matriz_inicial, vetor_inicial = criar_matriz_e_vetor_de_elementos_constantes(
        circuito, maior_no
    )

    quantidade_pontos = int(duracao / intervalo) + 1

    tempo = numpy.arange(0, quantidade_pontos) * intervalo

    dimensao = maior_no + circuito.quantidade_de_variaveis_de_corrente
    resultados = numpy.zeros((quantidade_pontos, dimensao), dtype=float)

    tensoes_anteriores = numpy.array(tensoes_iniciais.copy())
    tensoes_anteriores = numpy.pad(
        tensoes_anteriores,
        (0, circuito.quantidade_de_variaveis_de_corrente),
        mode='constant',
        constant_values=0
    )

    for index, tempo_atual in enumerate(tempo):
        tensoes_anteriores = numpy.concatenate(([0], tensoes_anteriores))

        matriz_temporal = numpy.copy(matriz_inicial)
        vetor_temporal = numpy.copy(vetor_inicial)

        matriz_temporal, vetor_temporal = adicionar_elementos_temporais(
            circuito,
            matriz_temporal,
            vetor_temporal,
            maior_no,
            tempo_atual,
            intervalo,
            tensoes_anteriores
        )

        if len(circuito.diodos) <= 0:
            resultados[index] = numpy.linalg.solve(
                matriz_temporal[1:, 1:],
                vetor_temporal[1:]
            )
        else:
            resultados[index] = calcula_circuito_nao_linear(
                circuito,
                matriz_temporal,
                vetor_temporal,
                tensoes_anteriores,
                tolerancia
            )

        tensoes_anteriores = resultados[index]

    resultados = resultados.transpose()
    nos_desejados = list(map(lambda x: x - 1, nos_desejados))

    print(resultados)
    return resultados[nos_desejados]


if __name__ == "__main__":
    arquivos = ["netlist1.txt", "netlist2.txt", "netlist3.txt", "netlist4.txt"]

    with numpy.printoptions(formatter={'float': '{: 0.8f}'.format}):
        DELLTA_T = 0.2e-3
        N_PONTOS = 2 / DELLTA_T + 1
        figures, axis = pyplot.subplots(2, 2)

        tempo_total = numpy.arange(0, N_PONTOS) * DELLTA_T
        print(main("netlist1.txt", 1e-3, 0.2e-3, 1e-4, [1, 0.5], [1, 2]))
        resultado1 = main("netlist1.txt", 2, 0.2e-3, 1e-4, [1, 0.5], [1, 2])
        axis[0][0].plot(tempo_total, resultado1[0], tempo_total, resultado1[1])
        print()
        print(main("netlist2.txt", 1e-3, 0.2e-3, 1e-4, [1, 0], [1, 2]))
        resultado2 = main("netlist2.txt", 2, 0.2e-3, 1e-4, [1, 0], [1, 2])
        axis[0][1].plot(tempo_total, resultado2[0], tempo_total, resultado2[1])
        print()
        print(main("netlist3.txt", 1e-3, 0.2e-3, 1e-4, [10, 0], [1, 2]))
        resultado3 = main("netlist3.txt", 2, 0.2e-3, 1e-4, [10, 0], [1, 2])
        axis[1][0].plot(tempo_total, resultado3[0], tempo_total, resultado3[1])
        print()
        print(main("netlist4.txt", 1e-3, 0.2e-3, 1e-4, [10, 0], [1, 2]))
        resultado4 = main("netlist4.txt", 2, 0.2e-3, 1e-4, [10, 0], [1, 2])
        axis[1][1].plot(tempo_total, resultado3[0], tempo_total, resultado3[1])
        pyplot.show()
        pyplot.close()
