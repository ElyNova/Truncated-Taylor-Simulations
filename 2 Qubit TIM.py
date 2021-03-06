from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError
from qiskit import available_backends, execute, register, get_backend
from qiskit.tools.visualization import plot_histogram, circuit_drawer
from math import pi
import math
from numpy import log

#Import the config file (Qconfig.py) to retrieve the API token and API url
try:
    import sys
    sys.path.append('../') #Parent directory
    import Qconfig
    qx_config = {
        'APItoken': Qconfig.APItoken,
        'url': Qconfig.config['url']}
except Exception as e:
    print(e)
    qx_config = {
        'APItoken':'YOUR_TOKEN_HERE',
        'url':'https://quantumexperience.ng.bluemix.net/api'}

#Setup API
register(qx_config['APItoken'], qx_config['url'])

t = 1
K = int(input("Enter an order for the approximation: "))
a = 1
b = 1
r = (a + b)*t/log(2)
phi_1 = 2*math.acos(math.sqrt((a+b)/(2*a+b)))
phi_2 = 2*math.acos(math.sqrt(b/(a+b)))

#anci = QuantumRegister(3)
#cont = QuantumRegister(2)
#psi = QuantumRegister(2)
#qc = QuantumCircuit(anci, cont, psi)

ord = QuantumRegister(K)
ell = QuantumRegister(2*K)
helper = QuantumRegister(max(2, 3*K-2))
psi = QuantumRegister(2)
cr = ClassicalRegister(2)
qc = QuantumCircuit(ord, ell, helper, psi)

#Defining Select(V)
def selectV(K, qc, ord, ell, helper, psi):
    for k in range(0,K):
        qc.cx(ord[k], ell[2*k+1])
        #Controlled-Controlled -iX Gate on psi[0]
        qc.ccx(ord[k], ell[2*k], helper[0])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.cu3(pi, pi/2, pi, helper[1], psi[0])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.ccx(ord[k], ell[2*k], helper[0])

        qc.cx(ord[k], ell[2*k])
        #Controlled-Controlled -iZZ Gate on psi[0], psi[1]
        qc.ccx(ord[k], ell[2*k], helper[0])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.crz(pi, helper[1], psi[0])
        qc.cz(helper[1], psi[1])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.ccx(ord[k], ell[2*k], helper[0])

        qc.cx(ord[k], ell[2*k+1])
        #Controlled-Controlled -iX Gate on psi[1]
        qc.ccx(ord[k], ell[2*k], helper[0])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.cu3(pi, pi/2, pi, helper[1], psi[1])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.ccx(ord[k], ell[2*k], helper[0])

        qc.cx(ord[k], ell[2*k])

#Defining Select(V)dagger
def selectVdag(K, qc, ord, ell, helper, psi):
    for k in reversed(range(0,K)):
        qc.cx(ord[k], ell[2*k])
        qc.ccx(ord[k], ell[2*k], helper[0])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.cu3(pi, pi/2, pi, helper[1], psi[1])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.ccx(ord[k], ell[2*k], helper[0])
        qc.cx(ord[k], ell[2*k+1])
        qc.ccx(ord[k], ell[2*k], helper[0])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.crz(pi, helper[1], psi[0])
        qc.cz(helper[1], psi[1])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.ccx(ord[k], ell[2*k], helper[0])
        qc.cx(ord[k], ell[2*k])
        qc.ccx(ord[k], ell[2*k], helper[0])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.cu3(pi, pi/2, pi, helper[1], psi[0])
        qc.ccx(ell[2*k+1], helper[0], helper[1])
        qc.ccx(ord[k], ell[2*k], helper[0])
        qc.cx(ord[k], ell[2*k+1])

#Defining the circuit B
def B(K, t, phi_1, phi_2, qc):
    for n in range(1, K+1):
        top = 0
        for k in range(n, K+1):
            top = top + (t/r)**k/math.gamma(k+1)
        bottom = top + (t/r)**(n-1)/math.gamma(n)
        #x = math.sqrt((t**(n-1)/math.gamma(n))/bottom)
        y = math.sqrt(top/bottom)
        #bottom = top
        #top = top - t**(n+1)/math.gamma(n+2)
        theta = 2*math.asin(y)
        if n == 1:
            qc.ry(theta, ord[n-1])
        else:
            qc.cu3(theta,0,0, ord[n-2], ord[n-1])
        qc.ry(phi_1, ell[2*(n-1)])
        qc.ry(phi_2, ell[2*(n-1)+1])
        qc.cu3(phi_2, 0, 0, ell[2*(n-1)], ell[2*(n-1)+1])

#Defining the circuit Bdagger
def Bdag(K, t, phi_1, phi_2, qc):
    for n in reversed(range(1, K+1)):
        top = 0
        for k in range(n, K+1):
            top = top + (t/r)**k/math.gamma(k+1)
        bottom = top + (t/r)**(n-1)/math.gamma(n)
        #x = math.sqrt((t**(n-1)/math.gamma(n))/bottom)
        y = math.sqrt(top/bottom)
        #bottom = top
        #top = top - t**(n+1)/math.gamma(n+2)
        theta = 2*math.asin(y)
        if n == 1:
            qc.ry(theta, ord[n-1])
        else:
            qc.cu3(theta,0,0, ord[n-2], ord[n-1])
        qc.cu3(phi_2, 0, 0, ell[2*(n-1)], ell[2*(n-1)+1])
        qc.ry(phi_2, ell[2*(n-1)+1])
        qc.ry(phi_1, ell[2*(n-1)])

#Defining the R circuit
def R(K, qc, ord, ell, helper):
    for k in range(0, K):
        qc.x(ord[k])
    for k in range(0,2*K):
        qc.x(ell[k])
    if K==1:
        qc.ccx(ell[0], ell[1], helper[0])
        qc.cz(helper[0], ord[0])
        qc.ccx(ell[0], ell[1], helper[0])
    elif K==2:
        qc.ccx(ord[1], ell[0], helper[0])
        for k in range(0,2*K-1):
            qc.ccx(ell[k+1], helper[k], helper[k+1])
        qc.cz(helper[2*K-1], ord[0])
        for k in reversed(range(0,2*K-1)):
            qc.ccx(ell[k+1], helper[k], helper[k+1])
        qc.ccx(ord[1], ell[0], helper[0])
    else:
        qc.ccx(ord[1], ord[2], helper[0])
        for k in range(2,K-1):
            qc.ccx(ord[k+1], helper[k-2], helper[k-1])
        for k in range(0,2*K):
            qc.ccx(ell[k], helper[k+K-3], helper[k+K-2])
        qc.cz(helper[3*K-3], ord[0])
        for k in reversed(range(0,2*K)):
            qc.ccx(ell[k], helper[k+K-3], helper[k+K-2])
        for k in reversed(range(2,K-1)):
            qc.ccx(ord[k+1], helper[k-2], helper[k-1])
        qc.ccx(ord[1], ord[2], helper[0])
    for k in range(0, K):
        qc.x(ord[k])
    for k in range(0,2*K):
        qc.x(ell[k])

def W(B, selectV, Bdag):
    B(K, t, phi_1, phi_2, qc)
    selectV(K, qc, ord, ell, helper, psi)
    Bdag(K, t, phi_1, phi_2, qc)

def Wdag(B, selecVdag, Bdag):
    B(K, t, phi_1, phi_2, qc)
    selecVdag(K, qc, ord, ell, helper, psi)
    Bdag(K, t, phi_1, phi_2, qc)

W(B, selectV, Bdag)
R(K, qc, ord, ell, helper)
Wdag(B, selectVdag, Bdag)
R(K, qc, ord, ell, helper)
W(B, selectV, Bdag)
qc.z(psi[0])
qc.x(psi[0])
qc.z(psi[0])
qc.x(psi[0])

pic = circuit_drawer(qc)
pic.show()
