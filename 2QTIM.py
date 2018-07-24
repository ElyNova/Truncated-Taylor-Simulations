from TIMdefs import *
L = 3
t = math.log(2)/3
a = 1
b = 1
#K = 3
for K in range(2,3):
    nq = (math.ceil(math.log(L,2))+1)*K+2;
    psi = np.zeros([2**nq, 1], dtype = complex)
    psi[0] = 1;
    B = Bgate(K,t,a,b)
    psi = B*psi
    print('B')
    SV = selectV(K)
    psi = SV*psi
    print('S')
    Bdag = inv(B.tocsc())
    psi = Bdag*psi
    print('B*')

    Re = R(K)
    psi = Re*psi
    print('R')
    psi = B*psi
    print('B')
    SVdag = inv(SV.tocsc())
    psi = SVdag*psi;
    print('S*')
    psi = Bdag*psi
    print('B*')
    psi = Re*psi
    print('R')
    psi = B*psi
    print('B')
    psi = SV*psi
    print('S')
    psi = Bdag*psi
    print('B*')

    up_up = 0
    up_down = 0;
    down_up = 0;
    down_down = 0;
    psi = abs(psi*psi)
    normal = sum(psi)
    print('\nNormal:', bool(normal.round(0)))
    for i in range(len(psi)):
        if i%4==0:
            up_up += psi[i]
        elif i%4 == 1:
            up_down += psi[i]
        elif i%4 == 2:
            down_up += psi[i]
        else:
            down_down += psi[i]
    print('\n\nFAT TROTTER REUSLTS, K = ', K)
    print('\nUp-Up:\t\t', float(up_up.round(2)))
    print('Up-Down:\t', float(up_down.round(2)))
    print('Down-Up:\t', float(down_up.round(2)))
    print('Down-Down:\t', float(down_down.round(2)))
    #print(sp.csr_matrix(psi.round(5)))

print('\n\nSPECTRAL RESULTS')
nq = 2
psi2 = np.zeros([2**nq,1])
psi2[0] = 1;
H = getHamiltonian(nq)
decomposeState(H, psi2,t)
