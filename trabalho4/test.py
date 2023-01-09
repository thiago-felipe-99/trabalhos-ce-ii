import numpy as np
from matplotlib import pyplot

#################################################
# Valores validos para todas as simulacoes
deltaT = 1e-3

tFinal = 20e-3

nPontos = int(tFinal/deltaT)

Iin = np.ones(nPontos)*10
pontosSubida = 10

Iin[0:pontosSubida] = np.linspace(0,10,pontosSubida)

tempo = np.arange(0,nPontos)*deltaT

# Plot da entrada:
pyplot.plot(tempo*1e3,Iin)
#################################################

#################################################
# Backward Euler
vc = np.zeros(nPontos)
R = 1
C = 2e-3

G = np.array([[1/R + C/deltaT]])

for i in range(1,len(Iin)):
    I = np.array(Iin[i]+(C/deltaT)*vc[i-1])
    vc[i] = np.linalg.inv(G).dot(I)

pyplot.plot(tempo*1e3,vc)
#################################################

#################################################
# Forward Euler
vc = np.zeros(nPontos)
ic = np.zeros(nPontos)

R = 1
C = 2e-3

G = np.array([[1/R, 1],[-1, 0]])

for i in range(1,len(Iin)):
    I = np.array([Iin[i-1],-(vc[i-1]+(deltaT/C)*ic[i-1])])
    e = np.linalg.inv(G).dot(I)
    vc[i] = e[0]
    ic[i] = e[1]

pyplot.plot(tempo*1e3,vc,'--')
#################################################

#################################################
# Trapezios - 1
vc = np.zeros(nPontos)

R = 1
C = 2e-3

G = np.array([[1/R+2*C/deltaT]])
it0 = 0

for i in range(1,len(Iin)):
    I = np.array([Iin[i-1]+(2*C/deltaT)*vc[i-1]+it0])
    e = np.linalg.inv(G).dot(I)
    vc[i] = e[0]
    it0 = 2*C/deltaT*vc[i]-(2*C/deltaT)*vc[i-1]-it0

pyplot.plot(tempo*1e3,vc,'-.')
vc1=vc
#################################################

#################################################
# Trapezios - 2 - usando analise nodal modificada
vc = np.zeros(nPontos)
ic = np.zeros(nPontos)

R = 1
C = 2e-3

G = np.array([[1/R, 1],\
              [-1, deltaT/(2*C)]])

for i in range(1,len(Iin)):
    I = np.array([Iin[i-1],-(vc[i-1]+(deltaT/(2*C))*ic[i-1])])
    e = np.linalg.inv(G).dot(I)
    vc[i] = e[0]
    ic[i] = e[1]

pyplot.plot(tempo*1e3,vc,'.')
#################################################
pyplot.show()
pyplot.close()
