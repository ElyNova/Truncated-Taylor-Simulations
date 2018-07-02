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
qc.u3(theta, 0, math.pi,qr(1))

#select(v) subcircuit - super not correct yet
#Need to figure out double-controlled pauli gates
#Also, david, did you figure out how to do -i multiplier? do we use the general u3 gate?
#I know what I am writing is not remotely correct, I just wanna test that circuit_drawer still works
qc.cz(qr(2), qr(3))
qc.cx(qr(1), qr(2))
qc.cx(qr(2), qr(3))

#B dagger
qc.u3(theta, 0, math.pi, qr(1))

circuit_drawer(qc)
