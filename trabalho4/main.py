"""Resolução do trabalho 4 de Circuitos Elétricos II."""
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Tuple
from typing import TypeAlias

import numpy


# pylint: disable=line-too-long


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
# pylint: disable-next=too-many-instance-attributes
class Circuito:
    """Representa quais são os componentes de um circuito elétrico."""

    resitores: list[Resitor] = field(default_factory=list)
    fontes_de_corrente_dc: list[FonteDeCorrenteDC] = field(
        default_factory=list)
    fontes_de_tensao_dc: list[FonteDeTensaoDC] = field(default_factory=list)
    fontes_de_corrente_senoidal: list[FonteDeCorrenteSenoidal] = field(
        default_factory=list)
    fontes_de_tensao_senoidal: list[FonteDeTensaoSenoidal] = field(
        default_factory=list)
    fontes_de_corrente_pulso: list[FonteDeCorrentePulso] = field(
        default_factory=list)
    fontes_de_tensao_pulso: list[FonteDeTensaoPulso] = field(
        default_factory=list)
    fontes_de_corrente_controlada_por_tensao: list[FonteDeCorrenteDCControladaPorTensao] = field(
        default_factory=list)
    fontes_de_corrente_controlada_por_corrente: list[FonteDeCorrenteControladaPorCorrente] = field(
        default_factory=list)
    fontes_de_tensao_controlada_por_tensao: list[FonteDeTensaoControladaPorTensao] = field(
        default_factory=list)
    fontes_de_tensao_controlada_por_corrente: list[FonteDeTensaoControladaPorCorrente] = field(
        default_factory=list)
    quantidade_de_variaveis_de_corrente: int = 0


MatrizCondutancia: TypeAlias = numpy.ndarray
VetorDeFontes: TypeAlias = numpy.ndarray


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
    FonteDeCorrentePulso | FonteDeTensaoPulso


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
    FonteDeTensaoControladaPorCorrente | FonteDeTensaoControladaPorTensao


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


# pylint: disable-next=too-many-arguments,too-many-locals
def main(
        nome_arquivo: str,
        duracao: float,
        passo: float,
        tolerancia: float,
        tensoes_inciais: List[float],
        nos_desejados: List[int]
) -> numpy.ndarray:
    """Função principal onde ele ler um arquivo do formato de uma netlist, faz a solução do circuito e retorna ela."""
    circuito = ler_arquivo(nome_arquivo)
    maior_no = pegar_maior_no(circuito)
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

    return numpy.linalg.solve(matriz[1:, 1:], vetor[1:])


if __name__ == "__main__":
    arquivos = ["netlist1.txt", "netlist2.txt", "netlist3.txt", "netlist4.txt"]

    with numpy.printoptions(formatter={'float': '{: 0.3f}'.format}):
        print(main("netlist1.txt", 1e-3, 0.2e-3, 1e-4, [1, 0.5], [1, 2]))
        print(main("netlist2.txt", 1e-3, 0.2e-3, 1e-4, [1, 0], [1, 2]))
        print(main("netlist3.txt", 1e-3, 0.2e-3, 1e-4, [10, 0], [1, 2]))
        print(main("netlist4.txt", 1e-3, 0.2e-3, 1e-4, [10, 0], [1, 2]))
