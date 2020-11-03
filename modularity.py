import numpy as np
import pandas as pd

def modularity(*,net,solC):
    np.random.seed(123)

    vertices = sorted(set(list(net[0]) + list(net[1])))
    n = len(vertices)
    L = len(net)
    Ki = [(list(net[0]) + list(net[1])).count(i) for i in vertices]

    linksCOM = [ (solC[net.loc[i,0]-1], solC[net.loc[i,1]-1]) for i in range(0,len(net)) ]
    linksCOM = pd.DataFrame(linksCOM, columns=['A','B'])

    e=[]
    for i in range(1,3):
        mask = (linksCOM['A'] == i) & (linksCOM['B'] == i)
        subi = linksCOM[mask]
        e.append(len(subi))

    er=np.array(e)/L
    matrCOMK = pd.DataFrame(list(zip(solC, Ki)), columns=['solC','Ki'])

    a=[]
    for i in range(1,3):
        mask = (matrCOMK['solC'] == i)
        subi = matrCOMK[mask]
        a.append(sum(subi['Ki']))
    ar = np.array(a)/(2*L)
    ar2 = ar**2
    return sum(er-ar2)
