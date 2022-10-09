#!/usr/bin/env python3

import numpy
from dataclasses import dataclass, field
from typing import TypeAlias

@dataclass
class Resistor:
    '''Representa um ramo com resistor'''
    identificacao: str
    no1: int
    no2: int
    valor: float

@dataclass
class Indutor:
    '''Representa um ramo com indutor'''
    identificacao: str
    no1: int
    no2: int
    valor: float
    condicaoInicial: float

@dataclass
class Capacitor:
    '''Representa um ramo com capacitor'''
    identificacao: str
    no1: int
    no2: int
    valor: float
    condicaoInicial: float

@dataclass
class Transformador:
    '''Representa um ramo com um transformador'''
    identificacao: str
    no1: int
    no2: int
    no3: int
    no4: int
    valorIndutancia1: float
    valorIndutancia2: float
    valorIndutanciaMutua: float

@dataclass
class FonteDeCorrenteSenoidal:
    '''Representa um ramo com fonte de corrente senoidal'''
    identificacao: str
    no1: int
    no2: int
    valor: float
    amplitude: float
    frequenciaHZ: float
    faseGraus: float

@dataclass
class FonteDeCorrenteControladaPorTensao:
    '''Representa um ramo com fonte de corrente controlada por tensão'''
    identificacao: str
    no1: int
    no2: int
    no3: int
    no4: int
    valor: float

@dataclass
class Circuito:
    '''Representa quais são os componentes de um circuito elétrico'''
    resistores: list[Resistor] = field(default_factory=list)
    indutores: list[Indutor] = field(default_factory=list)
    capacitores: list[Capacitor] = field(default_factory=list)
    transformadores: list[Transformador] = field(default_factory=list)
    fontesDeCorrenteSenoidal: list[FonteDeCorrenteSenoidal] = field(default_factory=list)
    fontesDeCorrenteControladaPorTensao: list[FonteDeCorrenteControladaPorTensao] = field(default_factory=list)
    frequencia: float = 0

MatrizCondutancia: TypeAlias = numpy.ndarray
VetorDeFontes: TypeAlias = numpy.ndarray

def lerArquivo(arquivo: str) -> Circuito:
    '''Ele faz a leitura de um arquivo do tipo netlist e retorna o circuito gerado
    por ela'''
    arquivp = open(arquivo,"r")
    linhas = arquivp.readlines()
    circuito = Circuito()

    for linha in linhas:
        if len(linha.strip()) == 0 or linha[0] == "*":
            continue

        componente = linha.split()

        if componente[0][0] == "R":
            identificacao = componente[0][1:]
            no1 = int(componente[1])
            no2 = int(componente[2])
            valor = float(componente[3])

            circuito.resistores.append(Resistor(identificacao, no1, no2, valor))

        elif componente[0][0] == "L":
            identificacao = componente[0][1:]
            no1 = int(componente[1])
            no2 = int(componente[2])
            valor = float(componente[3])
            inicial = float(componente[4])

            circuito.indutores.append(
                Indutor(identificacao, no1, no2, valor, inicial)
            )

        elif componente[0][0] == "C":
            identificacao = componente[0][1:]
            no1 = int(componente[1])
            no2 = int(componente[2])
            valor = float(componente[3])
            inicial = float(componente[4])

            circuito.capacitores.append(
                Capacitor(identificacao, no1, no2, valor, inicial)
            )

        elif componente[0][0] == "K":
            identificacao = componente[0][1:]
            no1 = int(componente[1])
            no2 = int(componente[2])
            no3 = int(componente[3])
            no4 = int(componente[4])
            l1 = float(componente[5])
            l2 = float(componente[6])
            m = float(componente[7])

            circuito.transformadores.append(
                Transformador(identificacao, no1, no2, no3, no4, l1, l2, m)
            )

        elif componente[0][0] == "G":
            identificacao = componente[0][1:]
            no1 = int(componente[1])
            no2 = int(componente[2])
            no3 = int(componente[3])
            no4 = int(componente[4])
            valor = float(componente[5])

            circuito.fontesDeCorrenteControladaPorTensao.append(
                FonteDeCorrenteControladaPorTensao(
                    identificacao, no1, no2, no3, no4, valor
                )
            )

        elif componente[0][0] == "I":
            identificacao = componente[0][1:]
            no1 = int(componente[1])
            no2 = int(componente[2])
            valor = float(componente[4])
            amplitude = float(componente[5])
            frequencia = float(componente[6])
            fase = float(componente[7])

            circuito.fontesDeCorrenteSenoidal.append(
                FonteDeCorrenteSenoidal(
                    identificacao, no1, no2, valor, amplitude, frequencia, fase
                )
            )

            circuito.frequencia = frequencia * 2 * numpy.pi

        else:
            print(f"Não foi possível ler a linha: '{linha}'")


    return circuito


def pegarMaiorNo(circuito: Circuito) -> int:
    '''Retorna qual é o maior nó do circuito'''
    no = 0

    for resistor in circuito.resistores:
        if resistor.no1 > no: 
            no = resistor.no1

        if resistor.no2 > no: 
            no = resistor.no2

    for indutor in circuito.indutores:
        if indutor.no1 > no: 
            no = indutor.no1

        if indutor.no2 > no: 
            no = indutor.no2

    for capacitor in circuito.capacitores:
        if capacitor.no1 > no: 
            no = capacitor.no1

        if capacitor.no2 > no: 
            no = capacitor.no2

    for transformador in circuito.transformadores:
        if transformador.no1 > no: 
            no = transformador.no1

        if transformador.no2 > no: 
            no = transformador.no2

        if transformador.no3 > no: 
            no = transformador.no3

        if transformador.no4 > no: 
            no = transformador.no4

    for fonte in circuito.fontesDeCorrenteSenoidal:
        if fonte.no1 > no: 
            no = fonte.no1

        if fonte.no2 > no: 
            no = fonte.no2

    for fonte in circuito.fontesDeCorrenteControladaPorTensao:
        if fonte.no1 > no: 
            no = fonte.no1

        if fonte.no2 > no: 
            no = fonte.no2

        if fonte.no3 > no: 
            no = fonte.no3

        if fonte.no4 > no: 
            no = fonte.no4

    return no

def adicionarResistor(matriz: MatrizCondutancia, resistor: Resistor) -> MatrizCondutancia:
    '''Ela adiciona um resistor na matriz de condutância do circuito'''
    matriz[resistor.no1][resistor.no1] += 1/resistor.valor
    matriz[resistor.no1][resistor.no2] -= 1/resistor.valor
    matriz[resistor.no2][resistor.no1] -= 1/resistor.valor
    matriz[resistor.no2][resistor.no2] += 1/resistor.valor

    return matriz

def adicionarIndutor(
        matriz: MatrizCondutancia, indutor: Indutor, frequencia: float      
) -> MatrizCondutancia:
    '''Ela adiciona um indutor na matriz de condutância do circuito'''
    matriz[indutor.no1][indutor.no1] += 1/(indutor.valor * 1j * frequencia)
    matriz[indutor.no1][indutor.no2] -= 1/(indutor.valor * 1j * frequencia)
    matriz[indutor.no2][indutor.no1] -= 1/(indutor.valor * 1j * frequencia)
    matriz[indutor.no2][indutor.no2] += 1/(indutor.valor * 1j * frequencia)

    return matriz

def adicionarCapacitor(
        matriz: MatrizCondutancia, capacitor: Capacitor, frequencia: float
) -> MatrizCondutancia:
    '''Ela adiciona um capacitor na matriz de condutância do circuito'''
    matriz[capacitor.no1][capacitor.no1] += capacitor.valor * 1j * frequencia
    matriz[capacitor.no1][capacitor.no2] -= capacitor.valor * 1j * frequencia
    matriz[capacitor.no2][capacitor.no1] -= capacitor.valor * 1j * frequencia
    matriz[capacitor.no2][capacitor.no2] += capacitor.valor * 1j * frequencia

    return matriz

def adicionarTransformador(
        matriz: MatrizCondutancia, transformador: Transformador, frequencia: float
) -> MatrizCondutancia:
    '''Ela adiciona um transformador na matriz de admitância do circuito'''
    l1l2 = transformador.valorIndutancia1 * transformador.valorIndutancia2
    gama1 = transformador.valorIndutancia2/(l1l2 - transformador.valorIndutanciaMutua**2)
    gama12 = -transformador.valorIndutanciaMutua/(l1l2 - transformador.valorIndutanciaMutua**2)
    gama2 = transformador.valorIndutancia1/(l1l2 - transformador.valorIndutanciaMutua**2)

    matriz[transformador.no1][transformador.no1] += gama1  / (1j * frequencia) 
    matriz[transformador.no1][transformador.no2] -= gama1  / (1j * frequencia) 
    matriz[transformador.no1][transformador.no3] += gama12 / (1j * frequencia) 
    matriz[transformador.no1][transformador.no4] -= gama12 / (1j * frequencia) 

    matriz[transformador.no2][transformador.no1] -= gama1  / (1j * frequencia) 
    matriz[transformador.no2][transformador.no2] += gama1  / (1j * frequencia) 
    matriz[transformador.no2][transformador.no3] -= gama12 / (1j * frequencia) 
    matriz[transformador.no2][transformador.no4] += gama12 / (1j * frequencia) 

    matriz[transformador.no3][transformador.no1] += gama12 / (1j * frequencia) 
    matriz[transformador.no3][transformador.no2] -= gama12 / (1j * frequencia) 
    matriz[transformador.no3][transformador.no3] += gama2  / (1j * frequencia) 
    matriz[transformador.no3][transformador.no4] -= gama2  / (1j * frequencia) 

    matriz[transformador.no4][transformador.no1] -= gama12 / (1j * frequencia) 
    matriz[transformador.no4][transformador.no2] += gama12 / (1j * frequencia) 
    matriz[transformador.no4][transformador.no3] -= gama2  / (1j * frequencia) 
    matriz[transformador.no4][transformador.no4] += gama2  / (1j * frequencia) 

    return matriz

def adicionarFonteDeCorrenteControladaTensao(
        matriz: MatrizCondutancia, fonte: FonteDeCorrenteControladaPorTensao
) -> MatrizCondutancia:
    '''Ela adiciona uma fonte de corrente controlada por tensão na matriz de 
    condutância do circuito'''
    matriz[fonte.no1][fonte.no3] += fonte.valor
    matriz[fonte.no1][fonte.no4] -= fonte.valor
    matriz[fonte.no2][fonte.no3] -= fonte.valor
    matriz[fonte.no2][fonte.no4] += fonte.valor

    return matriz

def adicionarFonteDeCorrenteSenoidal(
        vetor: VetorDeFontes, fonte: FonteDeCorrenteSenoidal
) -> VetorDeFontes:
    '''Ela adiciona uma fonte de corrente senoidal com a seguinte foŕmula
    i(t) = <amplitude> * cos ( 2*pi*<frequencia>*t + <fase>*pi/180 ) no vetor de 
    fontes do circuito'''

    valor = fonte.amplitude * (numpy.cos((fonte.faseGraus*numpy.pi)/180) + 
                               numpy.sin((fonte.faseGraus*numpy.pi)/180)*1j)
    vetor[fonte.no1] -= valor
    vetor[fonte.no2] += valor

    return vetor

def main(arquivo: str) -> numpy.ndarray:
    '''Função principal onde ele ler um arquivo do formato de uma netlist, faz a 
    solução do circuito e retorna ela'''
    circuito = lerArquivo(arquivo)
    maiorNo = pegarMaiorNo(circuito)
    matriz = numpy.zeros((maiorNo+1, maiorNo+1), dtype=complex)
    vetor = numpy.zeros((maiorNo+1), dtype=complex)

    for resistor in circuito.resistores:
        matriz = adicionarResistor(matriz, resistor)

    for indutor in circuito.indutores:
        matriz = adicionarIndutor(matriz, indutor, circuito.frequencia)

    for capacitor in circuito.capacitores:
        matriz = adicionarCapacitor(matriz, capacitor, circuito.frequencia)

    for transformador in circuito.transformadores:
        matriz = adicionarTransformador(matriz, transformador, circuito.frequencia)

    for fonte in circuito.fontesDeCorrenteControladaPorTensao:
        matriz = adicionarFonteDeCorrenteControladaTensao(matriz, fonte)

    for fonte in circuito.fontesDeCorrenteSenoidal:
        vetor = adicionarFonteDeCorrenteSenoidal(vetor, fonte)

    return numpy.linalg.solve(matriz[1:, 1:], vetor[1: ])

if __name__ == "__main__":
    arquivos = [ "teste1.txt", "teste2.txt", "teste3.txt", "teste4.txt"]

    for arquivo in arquivos:
        print(arquivo)
        print("Solução do sistema:", list(map('{:.3f}'.format,main(arquivo))))
        print()
