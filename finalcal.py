import numpy as np
from Node import Node
from Rod import Rod
from Digitalize import SetBasicData, SetNodes, SetRods, SetForces

def finalcal(basicdata,x,y,ihl,ihr,loadnum,force,theta):
    n = basicdata[0]
    m = basicdata[1]
    nc = basicdata[2]
    nLoad = basicdata[3]

    x = x.split()
    y = y.split()
    ihl = ihl.split()
    ihr = ihr.split()
    loadnum = loadnum.split()
    force = force.split()
    theta = theta.split()

    for i in range(n):
        x[i] = float(x[i])
        y[i] = float(y[i])
    for i in range(m):
        ihl[i] = int(ihl[i])
        ihr[i] = int(ihr[i])
    for i in range(nLoad):
        loadnum[i] = int(loadnum[i])
        force[i] = float(force[i])
        theta[i] = float(theta[i])

    nn = 2*(n-nc)

    node = []
    for i in range(n):
        X = x[i]
        Y = y[i]
        node.append(SetNodes(X, Y))

    for i in range(nLoad):
        F = force[i]
        Theta = theta[i]
        nodenum = loadnum[i]
        SetForces(F, Theta, node[nodenum])
        # print(node[nodenum].GetLoadX())
        # node[nodenum].AddLoad(F, theta)
    for i in range(n):
        node[i].SetNumber(i)
# for i in range(n):
#     node[i].PrintNode()

    rod = []
    for i in range(m):
        left = ihl[i]
        right = ihr[i]
        rod.append(SetRods(node[left],node[right]))
    for i in range(m):
        rod[i].SetNum(i)
        # rod[i].PrintRod()

    print("\nReady to calculate...\n")

    r = []
    P = []
    for i in range(nn):
        r.append([])
        P.append(0)
        for j in range(nn):
            r[i].append(0)
    r = np.array(r, dtype=float)
    P = np.array(P, dtype=float)
    # print("r = \n", r, "\nP = \n", P)
    print("Initialize complete...\n")

    # Total stiffness matrix r[nn][nn]
    for k in range(m):
        i0 = rod[k].Cali0j0(nc)
        c = rod[k].CalStif()
        # print(i0)
        # print(c)
        # print("\n\n")
        if i0[0]>=0:
            # topleft
            for i in range(i0[0]+1, i0[0]+3):
                for j in range(i0[0]+1, i0[0]+3):
                    r[i-1][j-1] += c[i-i0[0]-1][j-i0[0]-1]
                for j in range(i0[1]+1, i0[1]+3):
                    r[i-1][j-1] -= c[i-i0[0]-1][j-i0[1]-1]
                    r[j-1][i-1] = r[i-1][j-1]
        if i0[1]>=0:
            # bottomright
            for i in range(i0[1]+1, i0[1]+3):
                for j in range(i0[1]+1, i0[1]+3):
                    r[i-1][j-1] += c[i-i0[1]-1][j-i0[1]-1]

    # Load vector P[nn]
    for i in range(0,n):
        if node[i].GetNum()-nc>=0:
            P[2*(node[i].GetNum()-nc)] += node[i].GetLoadX()
            P[2*(node[i].GetNum()-nc)+1] += node[i].GetLoadY();

    print("\nStiffness Matrix:")
    print(r)
    print("\nLoad Vector:")
    print(P)

    U = np.linalg.solve(r, P)
    print("\nDisplacement=")
    print(U)

    S = []
    for i in range(m):
        S.append(0.0)
    S = np.array(S)
    for k in range(m):
        i0 = rod[k].Cali0j0(nc)
        # print("i0=", i0)
        c = rod[k].CalStif()
        # print("c=", c)
        v = np.array([0.0, 0.0])
        for i in range(2):
            if i0[0]<0 and i0[1]>=0:
                v[i] = U[i0[1]+i]
            if i0[0]>=0 and i0[1]>=0:
                v[i] = U[i0[1]+i] - U[i0[0]+i]
            if i0[0]<0 and i0[1]<0:
                v[i] = 0
        # print("v=", v)
        t = np.array([0.0, 0.0])
        t[0] = rod[k].CalCos()
        t[1] = rod[k].CalSin()
        for i in range(2):
            S[k] = S[k]+t[i]*v[i]*rod[k].Calrd();
    print("\nInternal Force=")
    print(S)
    print("________________________________")
    return U,S



