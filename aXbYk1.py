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
qr = QuantumRegister(3)
cr = ClassicalRegister(3)
qc = QuantumCircuit(qr, cr)

#-WRW*RW|0>|psi> = |0>U|psi>

#THE W CIRCUIT: W = B select(v) B*
#Rotation U1 of B subcircuit
theta = math.acos(math.sqrt(1/(1+math.sqrt(t))))
qc.u3(theta, 0, math.pi,qr[0])

#select(v) subcircuit - super not correct yet
#Need to figure out double-controlled pauli gates
#Also, david, did you figure out how to do -i multiplier? do we use the general u3 gate?
#The -iX gate can be done by a rotation around the x-axis. qc.rx(pi, qr[q])
#The -iZ gate can be done by a rotation around the z-axis. qc.rz(pi, qr[q])
#I know what I am writing is not remotely correct, I just wanna test that circuit_drawer still works
qc.cz(qr[1], qr[2])
qc.cx(qr[0], qr[1])
qc.cx(qr[1], qr[2])

#B dagger
qc.u3(theta, 0, math.pi, qr[0])

pic = circuit_drawer(qc)

import BackendSetup
BackendSetup.signIn()
backend = BackendSetup.bestBackend()
