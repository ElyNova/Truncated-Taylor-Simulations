import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import inv
import math
from cmath import exp

I = sp.csr_matrix([[1,0],[0,1]])
H = sp.csr_matrix([[1, 1],[1, -1]])*1/math.sqrt(2)
X = sp.csr_matrix([[0, 1],[1, 0]])
Z = sp.csr_matrix([[1, 0],[0, -1]])

def tensorProd(opList):
    '''create tensor product of ordered list on single qubit ops on different qubits'''
    prod = 1;
    for j in range(len(opList)):
        prod = sp.kron(prod, opList[j])
    return prod

def control(nq, op):
    '''n qubit matrix in which most significant n-1 bits control operation on qubit n'''
    C = np.identity(2**nq, dtype = complex)
    C[-op.shape[0]:, -op.shape[1]:] = op.todense()
    return sp.csr_matrix(C)

def swap(M, pos1, pos2):
    nq = int(math.log(M.shape[0],2))
    a = np.zeros([2**nq,nq], dtype = int)
    scale = (2*np.ones([1,nq], dtype = int))**np.array(range(nq-1,-1,-1))
    S = np.zeros(M.shape, dtype = int)
    for i in range(0,a.shape[0]):
        for j in range(0,a.shape[1]):
            if math.floor( (i) / 2**(j) )%2 == 1:
                a[i, nq-j-1] = 1
    b = np.copy(a)
    for i in range(0,a.shape[0]):
        b[i,pos1-1] = a[i,pos2-1]
        b[i,pos2-1] = a[i,pos1-1]
        x = np.dot(a[i,:],scale.T)
        y = np.dot(b[i,:],scale.T)
        S[x,y] = 1;
    S = sp.csr_matrix(S)
    return S*M*S

def Bgate(K,t, a, b):
    B = sp.eye(2**(3*K+2))
    for n in range(1,K+1):
        T = 0;
        for k in range(n-1,K+1):
            T += t**k/math.factorial(k)
        #print('Numerator: ',t**(n-1)/math.factorial(n-1))
        #print('Denominator: ',T)
        cost = math.sqrt(t**(n-1)/math.factorial(n-1)/T)
        theta = math.acos(cost)
        crot = rot(theta)
        #The first rotation on k register happens unconditionally
        #This is also where l registers are put into superpos dictated by a and b
        if n == 1:
            theta = math.acos(math.sqrt(2*a/(2*a + b)))
            D1 = sp.kron(rot(theta),I)
            D2 = sp.kron(X,I) * control(2,H) * sp.kron(X,I)
            for i in range(2,K+1):
                crot = sp.kron(crot,I)
            #Need to change the 2 in the loop below to ceil log(L)
            for i in range(K+1, 3*K+1, 2):
                crot = sp.kron(crot, D2*D1)
            crot = tensorProd([crot, I, I])
        #Rotations on qubits after k=1 are controlled on preceding qubit
        #all other qubits are untouched
        else:
            crot = control(2, crot)
            for i in range(1, 3*K+2+1):
                if i < (n-1):
                    crot = sp.kron(I,crot)
                if i > n:
                    crot = sp.kron(crot, I)
        B = crot * B
    return B

def selectV(K):
    '''Builds the select(V) matrix for H = X1 + X2 + ZZ'''
    L = 2
    nq = (1+L)*K+2
    S = sp.eye(2**nq)
    #Build the CX, iX, and iZZ gates
    CXI = control(2,X)
    X1 = control(4, 1j*X)
    ZZ = control(5, sp.kron(1j*Z,Z))
    for q in range(1, nq+1):
        if q < K:
            CXI = sp.kron(I, CXI)
            X1 = sp.kron(I, X1)
        if q < nq-4:
            ZZ = sp.kron(I, ZZ)
        if q > K+1:
            CXI = sp.kron(CXI,I)
        if q > K + 3:
            X1 = sp.kron(X1, I)
    CXI = swap(CXI, 1, K)
    CIX = swap(CXI,K+1, K+2)

    X1 = swap(X1, 1, K)
    X1 = swap(X1, K+3, nq-1)
    X2 = swap(X1, nq-1, nq)

    ZZ = swap(ZZ, nq-2, K+2)
    ZZ = swap(ZZ, nq-3, K+1)
    ZZ = swap(ZZ, nq-4, 1)

    subSV = CXI*X2*CIX*X1*CXI*ZZ*CIX;

    for k in range(1,K+1):
        S = subSV*S
        if k < K:
            subSV = swap(subSV, k, k+1)
            subSV = swap(subSV, K+(k-1)*L + 1, K+k*L+1)
            subSV = swap(subSV, K+(k-1)*L + 2, K+k*L+2)

    return S

def rot(theta):
    return sp.csr_matrix([[math.cos(theta), math.sin(theta)],[math.sin(theta), -math.cos(theta)]])

def R(K):
    '''Operation to reflect the state with all zero ancilla'''
    R1 = sp.kron(I,I)
    for i in range(3*K):
        R1 = sp.kron(X, R1)
    R2 = swap(control(3*K, Z), 1, 3*K)
    R2 = tensorProd([R2, I, I])
    return R1*R2*R1

def getHamiltonian(num_qubits):
    '''Hard coding for now'''
    if num_qubits == 2:
        return sp.kron(1.00001*X, I) + sp.kron(I,X) + sp.kron(Z,Z)
    else:
        print('Hey buddy, you didn\'t write the code for n<2 yet')

def decomposeState(Hamiltonian, initState, t):
    E, vecs = np.linalg.eig(Hamiltonian.todense())
    evolvedPsi = np.zeros([len(vecs),1], dtype = complex)
    for i in range(len(vecs)):
        c_n = (float(vecs[:,i].H * initState))
        evolvedPsi += c_n * exp(-1j*E[i]*t) * vecs[:,i]
    print('Up-Up:\t\t',  round(float(abs(evolvedPsi[0]**2)),2))
    print('Up-Down:\t',  round(float(abs(evolvedPsi[1]**2)),2))
    print('Down-Up:\t',  round(float(abs(evolvedPsi[2]**2)),2))
    print('Down-Down:\t',  round(float(abs(evolvedPsi[3]**2)),2))
