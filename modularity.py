import numpy as np
import pandas as pd

def modularity(*,net,solC):
    unlist_net = list(net[0]) + list(net[1])
    vertices = sorted(set(unlist_net))
    n = len(vertices)
    L = len(net)
    Ki = [ unlist_net.count(i) for i in vertices ]

    linksCOM = [ (solC[net.loc[i,0]-1], solC[net.loc[i,1]-1]) for i in range(0,len(net)) ]
    linksCOM = pd.DataFrame(linksCOM, columns=['COM1','COM2'])

    e=[]
    for i in range(1,3):
        mask = (linksCOM['COM1'] == i) & (linksCOM['COM2'] == i)
        subi = linksCOM[mask]
        e.append(len(subi))

    er=np.array(e)/L

    matrCOMK = pd.DataFrame(list(zip(solC, Ki)), columns=['COM','K'])
    a=[]
    for i in range(1,3):
        mask = (matrCOMK['COM'] == i)
        subi = matrCOMK[mask]
        a.append(sum(subi['K']))

    ar = np.array(a)/(2*L)
    ar2 = ar**2
    return sum(er-ar2)
