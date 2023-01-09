import numpy as np

def adicionarResistor(G,no1,no2,R):
    G[no1,no1] = G[no1,no1] + 1/R
    G[no1,no2] = G[no1,no2] - 1/R
    G[no2,no1] = G[no2,no1] - 1/R
    G[no2,no2] = G[no2,no2] + 1/R
    return G

def adicionarFonteCorrente(I,no1,no2,iin):
    I[no1] = I[no1] - iin
    I[no2] = I[no2] + iin
    return I

def adicionarResistorQuadratico(G,I,no1,no2,e):
    e = np.concatenate((np.array([0]),e))
    G0 = 2*(e[no1]-e[no2])
    I0 = (e[no1]-e[no2])**2 - G0*(e[no1]-e[no2])
    G = adicionarResistor(G,no1,no2,1/G0)
    I = adicionarFonteCorrente(I,no1,no2,I0)
    return G,I

def adicionarTrancondutor(G,no1,no2,no3,no4,Gm):
    G[no1,no3] = G[no1,no3] + Gm
    G[no1,no4] = G[no1,no4] - Gm
    G[no2,no3] = G[no2,no3] - Gm
    G[no2,no4] = G[no2,no4] + Gm
    return G

def adicionarFonteInversa(G,I,no1,no2,no3,no4,e):
    e = np.concatenate((np.array([0]),e))
    Gm = -1/((e[no3]-e[no4])**2)
    If = 1/(e[no3]-e[no4]) - Gm*(e[no3]-e[no4])

    G = adicionarTrancondutor(G,no1,no2,no3,no4,Gm)
    
    I = adicionarFonteCorrente(I,no1,no2,If)
    
    return G,I
    

k = 100

eit0 = np.array([1.5,0])
epsilon = 0.001

Gref = np.zeros([3,3])
Iref = np.zeros(3)
Gref = adicionarResistor(Gref,1,2,2)
Iref = adicionarFonteCorrente(Iref,0,1,2)

while k > 0:

    G = np.copy(Gref)
    I = np.copy(Iref)
    
    G,I = adicionarResistorQuadratico(G,I,1,0,eit0)

    G,I = adicionarFonteInversa(G,I,2,0,1,2,eit0)


    G = G[1:,1:]
    I = I[1:]
    eitn = np.linalg.inv(G).dot(I)

    d = np.max(np.abs(eitn-eit0))
    if d < epsilon:
        break

    print(eitn)
    eit0 = eitn
    
    k = k-1

print(eitn)
print(100-k)

