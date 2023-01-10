import numpy as np
from math import exp


def adicionarResistor(G, no1, no2, R):
    G[no1, no1] = G[no1, no1] + 1 / R
    G[no1, no2] = G[no1, no2] - 1 / R
    G[no2, no1] = G[no2, no1] - 1 / R
    G[no2, no2] = G[no2, no2] + 1 / R

    return G


def adicionarFonteCorrente(I, no1, no2, iin):
    I[no1] = I[no1] - iin
    I[no2] = I[no2] + iin

    return I


def adicionarFonteTensao(G, I, no1, no2, vin, posicao):
    I[posicao] -= vin

    G[no1][posicao] += 1
    G[no2][posicao] -= 1
    G[posicao][no1] -= 1
    G[posicao][no2] += 1

    return G, I


def adicionarResistorQuadratico(G, I, no1, no2, e):
    e = np.concatenate((np.array([0]), e))
    G0 = 2 * (e[no1] - e[no2])
    I0 = (e[no1] - e[no2])**2 - G0 * (e[no1] - e[no2])
    G = adicionarResistor(G, no1, no2, 1 / G0)
    I = adicionarFonteCorrente(I, no1, no2, I0)

    return G, I


def adicionarTrancondutor(G, no1, no2, no3, no4, Gm):
    G[no1, no3] = G[no1, no3] + Gm
    G[no1, no4] = G[no1, no4] - Gm
    G[no2, no3] = G[no2, no3] - Gm
    G[no2, no4] = G[no2, no4] + Gm

    return G

def adicionarFonteInversa(G, I, no1, no2, no3, no4, e):

    e = np.concatenate((np.array([0]), e))
    Gm = -1/((e[no3]-e[no4])**2)
    If = 1/(e[no3]-e[no4]) - Gm*(e[no3]-e[no4])

    G = adicionarTrancondutor(G, no1, no2, no3, no4, Gm)

    I = adicionarFonteCorrente(I, no1, no2, If)

    return G, I


def adicionarDiodo(G, I, no1, no2, isv, nvt, eit0):
    vn = eit0[no1 - 1] - eit0[no2 - 1]
    conduntancia = (isv * exp(vn / nvt)) / nvt
    corrente = (isv * (exp(vn / nvt) - 1)) - (conduntancia * vn)

    G = adicionarResistor(G, no1, no2, 1.0 / conduntancia)
    I = adicionarFonteCorrente(I, no1, no2, corrente)

    return G, I


k = 1000

eit0 = np.array([1, 0.5, 0])
epsilon = 1e-4

Gref = np.zeros([4, 4])
Iref = np.zeros(4)
Gref = adicionarResistor(Gref, 0, 2, 1e3)
Gref, Iref = adicionarFonteTensao(Gref, Iref, 1, 0, 1, 3)

while k > 0:

    G = np.copy(Gref)
    I = np.copy(Iref)

    G, I = adicionarDiodo(G, I, 1, 2, 50e-15, 22.5e-3, eit0)

    G = G[1:, 1:]
    I = I[1:]
    eitn = np.linalg.inv(G).dot(I)

    d = np.max(np.abs(eitn - eit0))
    if d < epsilon:
        break

    print(eitn)
    eit0 = eitn
    k = k - 1

print(eitn)
print(1000 - k)

