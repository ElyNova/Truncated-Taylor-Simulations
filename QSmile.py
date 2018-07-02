from qiskit import ClassicalRegister, QuantumRegister
from qiskit import QuantumCircuit, execute
from qiskit.tools.visualization import plot_histogram, circuit_drawer


qr = QuantumRegister(16)
cr = ClassicalRegister(16)
qc = QuantumCircuit(qr,cr)

qc.x(qr[0])
qc.x(qr[3])
qc.x(qr[5])

qc.h(qr[9])
qc.cx(qr[9], qr[8])
qc.x(qr[11])
qc.x(qr[12])
qc.x(qr[13])

for j in range(16):
    qc.measure(qr[j],cr[j])
print("Done\n")

#Sign onto IBM UE

from qiskit import register, available_backends, get_backend
#import Qconfig and set APIToken and API url
try:
    import sys 
    sys.path.append("../") #go to parent directory
    import Qconfig
    qx_config = {
        "APIToken": Qconfig.APIToken,
        "url": Qconfig.config['url']
    }
    
except Exception as e:
    print(e)
    qx_config = {
        "APIToken": "b2b686d61de1af50d8ae7cb4fe85fb8dc61279a888b47e290ffe2f1f87d692a7dc65ab295ec957b7c54a24497c2c5138a72f6dbbf93d96d0db8e1018c8418563",
        "url":"https://quantumexperience.ng.bluemix.net/api"
    }

#set api
register(qx_config['APIToken'], qx_config['url'])

#Plot dat shit
backend = "ibmq_qasm_simulator"
shots_sim = 128

job_sim = execute(qc, backend, shots = shots_sim)
stats_sim = job_sim.result().get_counts()

plot_histogram(stats_sim)

#Grphic

import matplotlib.pyplot as plt
#%matplotlib inline
plt.rc('font', family = 'monospace')

def plot_smiley (stats, shots):
    for bitString in stats:
        char = chr(int(bitString[0:8], 2)) #convert leftmost 8 bits into ascii character
        char +=chr(int(bitString[8:16], 2)) #convert next 8 bits into ascii and append to first character
        prob = stats[bitString]/shots
        #create plot overlaying characters with transparancy dictated by prob
        plt.annotate( char, (0.5,0.5), va="center", ha="center", color = (0,0,0, prob ), size = 300)
        if(prob > .05):
            print(str(prob)+"\t"+char)
    plt.axis('off')
    plt.show()
    
plot_smiley(stats_sim, shots_sim)
circuit_drawer(qc)

