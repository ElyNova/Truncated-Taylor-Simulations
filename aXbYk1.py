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
#First Apply W = B select(v) B*
#Rotation U1 of B circuit
theta = math.acos(math.sqrt(1/(1+math.sqrt(t))))
qc.u3(theta, 0, math.pi,1)





#select(v)


