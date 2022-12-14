#!/usr/bin/env python3

import numpy
from dataclasses import dataclass, field
from typing import TypeAlias

@dataclass
class Resitor:
    '''Representa um ramo com resitor'''
    identificacao: str
    no1: int
    no2: int
    valor: float

@dataclass
class FonteDeCorrenteDC:
    '''Representa um ramo com fonte de corrente DC'''
    identificacao: str
    no1: int
    no2: int
    valor: float

@dataclass
class FonteDeCorrenteDCControladaPorTensao:
    '''Representa um ramo com fonte de corrente DC controlada por tensão'''
    identificacao: str
    no1: int
    no2: int
    no3: int
    no4: int
    valor: float

@dataclass
class Circuito:
    '''Representa quais são os componentes de um circuito elétrico'''
    resitores: list[Resitor] = field(default_factory=list)
    fontesDeCorrenteDC: list[FonteDeCorrenteDC] = field(default_factory=list)
    fontesDeCorrenteDCControladaPorTensao: list[FonteDeCorrenteDCControladaPorTensao] = field(default_factory=list)

MatrizCondutancia: TypeAlias = numpy.ndarray
VetorDeFontes: TypeAlias = numpy.ndarray

def lerArquivo(arquivo: str) -> Circuito:
    '''Ele faz a leitura de um arquivo do tipo netlist e retorna o circuito gerado por ela
    '''
    arquivp = open(arquivo,"r")
    linhas = arquivp.readlines()
    circuito = Circuito()

    for linha in linhas:
        if not len(linha.strip()) == 0 and not linha[0] == "*":
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

                circuito.fontesDeCorrenteDCControladaPorTensao.append(
                    FonteDeCorrenteDCControladaPorTensao(
                        identificacao, no1, no2, no3, no4, valor
                    )
                )

            elif componente[0][0] == "I":
                identificacao = componente[0][1:]
                no1 = int(componente[1])
                no2 = int(componente[2])
                valor = float(componente[4])

                circuito.fontesDeCorrenteDC.append(
                    FonteDeCorrenteDC(identificacao, no1, no2, valor)
                )

    return circuito


def pegarMaiorNo(circuito: Circuito) -> int:
    '''Retorna qual é o maior nó do circuito'''
    no = 0

    for resitor in circuito.resitores:
        if resitor.no1 > no: 
            no = resitor.no1

        if resitor.no2 > no: 
            no = resitor.no2

    for fonte in circuito.fontesDeCorrenteDC:
        if fonte.no1 > no: 
            no = fonte.no1

        if fonte.no2 > no: 
            no = fonte.no2

    for fonte in circuito.fontesDeCorrenteDCControladaPorTensao:
        if fonte.no1 > no: 
            no = fonte.no1

        if fonte.no2 > no: 
            no = fonte.no2

        if fonte.no3 > no: 
            no = fonte.no3

        if fonte.no4 > no: 
            no = fonte.no4

    return no

def adicionarResitor(matriz: MatrizCondutancia, resitor: Resitor) -> MatrizCondutancia:
    '''Ela adiciona um resitor na matriz de condutância do circuito'''
    matriz[resitor.no1][resitor.no1] += 1/resitor.valor
    matriz[resitor.no1][resitor.no2] -= 1/resitor.valor
    matriz[resitor.no2][resitor.no1] -= 1/resitor.valor
    matriz[resitor.no2][resitor.no2] += 1/resitor.valor

    return matriz

def adicionarFonteDeCorrenteDCControladaTensao(
        matriz: MatrizCondutancia, fonte: FonteDeCorrenteDCControladaPorTensao
) -> MatrizCondutancia:
    '''Ela adiciona uma fonte de corrente DC controlada por tensão na matriz de 
    condutância do circuito'''
    matriz[fonte.no1][fonte.no3] += fonte.valor
    matriz[fonte.no1][fonte.no4] -= fonte.valor
    matriz[fonte.no2][fonte.no3] -= fonte.valor
    matriz[fonte.no2][fonte.no4] += fonte.valor

    return matriz

def adicionarFonteDeDCCorrente(vetor: VetorDeFontes, fonte: FonteDeCorrenteDC) -> VetorDeFontes:
    '''Ela adiciona uma fonte de corrente DC no vetor de fontes do circuito'''
    vetor[fonte.no1] -= fonte.valor
    vetor[fonte.no2] += fonte.valor

    return vetor


def main(arquivo: str) -> numpy.ndarray:
    '''Função principal onde ele ler um arquivo do formato de uma netlist, faz a solução
    do circuito e retorna ela'''

    circuito = lerArquivo(arquivo)
    maiorNo = pegarMaiorNo(circuito)
    matriz = numpy.zeros((maiorNo+1, maiorNo+1), dtype=float)
    vetor = numpy.zeros((maiorNo+1), dtype=float)

    for resitor in circuito.resitores:
        matriz = adicionarResitor(matriz, resitor)

    for fonte in circuito.fontesDeCorrenteDCControladaPorTensao:
        matriz = adicionarFonteDeCorrenteDCControladaTensao(matriz, fonte)

    for fonte in circuito.fontesDeCorrenteDC:
        vetor = adicionarFonteDeDCCorrente(vetor, fonte)

    return numpy.linalg.solve(matriz[1:, 1:], vetor[1: ])

if __name__ == "__main__":
    arquivos = ["netlist0.txt", "netlist1.txt", "netlist2.txt", "netlist3.txt"]

    for arquivo in arquivos:
        print(main(arquivo))
