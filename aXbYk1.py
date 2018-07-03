#CONSTANTS
t = 1

#IMPORTS
from qiskit import ClassicalRegister, QuantumRegister
from qiskit import QuantumCircuit, execute
from qiskit.tools.visualization import plot_histogram, circuit_drawer
import math

#Ancillary Qubits = K + K*Log(L) = 2
#Plus one additional qubit to hold |Psi>

#qr(1) = |k>    qr(2) = |l>    qr(3) = |psi>
anci = QuantumRegister(2)
cont = QuantumRegister(1)
psi = QuantumRegister(1)
qc = QuantumCircuit(anci, cont, psi)

#-WRW*RW|0>|psi> = |0>U|psi>

#THE W CIRCUIT: W = B select(v) B*
#Rotation U1 of B subcircuit
theta = math.acos(math.sqrt(1/(1+math.sqrt(t))))
qc.u3(theta, 0, math.pi,anci[0])

#select(v) subcircuit - super not correct yet
#Need to figure out double-controlled pauli gates
#Also, david, did you figure out how to do -i multiplier? do we use the general u3 gate?
#The -iX gate can be done by a rotation around the x-axis. qc.rx(pi, qr[q])
#The -iZ gate can be done by a rotation around the z-axis. qc.rz(pi, qr[q])
#I know what I am writing is not remotely correct, I just wanna test that circuit_drawer still works

#double controlled iz gate
qc.ccx(anci[0], anci[1], cont[0])
qc.cy(cont[0], psi[0])
qc.cx(cont[0], psi[0])
qc.ccx(anci[0], anci[1], cont[0])

qc.cx(anci[0], anci[1])

qc.ccx(anci[0], anci[1], cont[0])
qc.cz(cont[0], psi[0])
qc.cy(cont[0], psi[0])
qc.ccx(anci[0], anci[1], cont[0])

#B dagger
qc.u3(theta, 0, math.pi, anci[0])

#R subcircuit
qc.x(anci[0])
qc.x(anci[1])
qc.cz(anci[1], anci[0])
qc.x(anci[0])
qc.x(anci[1])

#W dagger
qc.u3(theta, 0, math.pi,anci[0])

qc.ccx(anci[0], anci[1], cont[0])
qc.cz(cont[0], psi[0])
qc.cy(cont[0], psi[0])
qc.ccx(anci[0], anci[1], cont[0])

qc.cx(anci[0], anci[1])

qc.ccx(anci[0], anci[1], cont[0])
qc.cy(cont[0], psi[0])
qc.cx(cont[0], psi[0])
qc.ccx(anci[0], anci[1], cont[0])

qc.u3(theta, 0, math.pi, anci[0])

#R subcircuit
qc.x(anci[0])
qc.x(anci[1])
qc.cz(anci[1], anci[0])
qc.x(anci[0])
qc.x(anci[1])


#W
qc.u3(theta, 0, math.pi,anci[0])

qc.ccx(anci[0], anci[1], cont[0])
qc.cy(cont[0], psi[0])
qc.cx(cont[0], psi[0])
qc.ccx(anci[0], anci[1], cont[0])

qc.cx(anci[0], anci[1])

qc.ccx(anci[0], anci[1], cont[0])
qc.cz(cont[0], psi[0])
qc.cy(cont[0], psi[0])
qc.ccx(anci[0], anci[1], cont[0])

qc.u3(theta, 0, math.pi, anci[0])
pic = circuit_drawer(qc)
#from PIL import Image
pic.save('WRWRW', 'png')
#pic.show()

#import BackendSetup
#BackendSetup.signIn()
#backend = BackendSetup.bestBackend()
