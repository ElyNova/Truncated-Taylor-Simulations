#IMPORTS
from qiskit import ClassicalRegister, QuantumRegister
from qiskit import QuantumCircuit, execute
from qiskit.tools.visualization import plot_histogram, circuit_drawer
import math

#CONSTANTS
t = 1
K = int(input("Enter an order for the approximation: "))
a = 1
b = 1
phi = 2*math.acos(math.sqrt(a/(a+b)))

ord = QuantumRegister(2*K)
#l = QuantumRegister(K)
helper = QuantumRegister(2*K-1)
psi = QuantumRegister(1)
qc = QuantumCircuit(ord, helper, psi)

#defining the B subcircuit
def B(K, t, phi, qc, q):
    top = 0;
    for k in range(1, K+1):
        top = top + t**k
    bottom = top + 1
    for n in range(1, K+1):
        #x = math.sqrt((t**(n-1)/math.gamma(n))/bottom)
        y = math.sqrt(top/bottom)
        bottom = top
        top = top - t**(n+1)/math.gamma(n+2)
        theta = 2*math.asin(y)
        if n == 1:
            qc.ry(theta, ord[n-1])
        else:
            qc.cu3(theta,0,0, ord[n-2], ord[n-1])
        qc.ry(phi, ord[K+n-1])

def Bdag(K, t, phi, qc, ord):
    top = math.sqrt(t**K/math.gamma(K+1))
    bottom = top + math.sqrt(t**(K-1)/math.gamma(K))
    for n in range(K, 0, -1):
        y = math.sqrt(top/bottom)
        top = bottom
        bottom = bottom + math.sqrt(t**(n-1)/math.gamma(n))
        theta = 2*math.asin(y)
        if n==1:
            qc.ry(theta, ord[n-1])
        else:
            qc.cu3(theta, 0, 0, ord[n-2], ord[n-1])
        qc.ry(phi, ord[K+n-1])


#defining the select(v) subcircuit
def selectV(K, qc, ord, helper, psi):
    for k in range(0,K):
        qc.ccx(ord[k], ord[K+k], helper[0])
        qc.cy(helper[0], psi)
        qc.cx(helper[0], psi)
        qc.reset(helper[0])
        qc.cx(ord[k], ord[K+k])
        qc.ccx(ord[k], ord[K+k], helper[0])
        qc.cz(helper[0], psi)
        qc.cy(helper[0], psi)
        qc.reset(helper[0])

#defining the select(v) conjugate subcircuit
def selectVdag(K, qc, ord, helper, psi):
    for k in range(K-1,-1,-1):
        qc.ccx(ord[k], ord[K+k], helper[0])
        qc.cz(helper[0], psi)
        qc.cy(helper[0], psi)
        qc.reset(helper[0])
        qc.cx(ord[k], ord[K+k])
        qc.ccx(ord[k], ord[K+k], helper[0])
        qc.cy(helper[0], psi)
        qc.cx(helper[0], psi)
        qc.reset(helper[0])

#defining R circuit
def R(K, qc, ord, helper):
    for k in range(0, 2*K):
        qc.x(ord[k])
    if K==1:
        qc.cz(ord[1], ord[0])
    else:
        qc.ccx(ord[1], ord[2], helper[0])
        for k in range(3, 2*K):
            qc.ccx(ord[k], helper[k-3], helper[k-2])
        qc.cz(helper[2*K-2], ord[0])
        for k in range(2*K-1, 2, -1):
            qc.ccx(ord[k], helper[k-3], helper[k-2])
        qc.ccx(ord[1], ord[2], helper[0])
    for k in range(2*K, 0, -1):
        qc.x(ord[k-1])





#A = WRW*RW = B select(v) B* R B* select(v)* B R B select(v) B*
B(K, t, phi, qc, ord)
selectV(K, qc, ord, helper, psi)
Bdag(K, t, phi, qc, ord)
R(K, qc, ord, helper)
Bdag(K, t, phi, qc, ord)
selectVdag(K, qc, ord, helper, psi)
B(K, t, phi, qc, ord)
R(K, qc, ord, helper)
B(K, t, phi, qc, ord)
selectV(K, qc, ord, helper, psi)
Bdag(K, t, phi, qc, ord)

c = circuit_drawer(qc)
pic = circuit_drawer(qc)
pic.save('WRWRW3.png', 'png')
