import pandas as pd
import numpy as np
from modularity import modularity
import math
import random
import matplotlib.pyplot as plt

np.random.seed(45678)
net = pd.read_csv('data/Zachary_Karate_club.txt', sep=' ', header=None)

vertices = sorted(set(list(net[0]) + list(net[1])))
n = len(vertices)

modularityVEC=[]
nsim = 500
for i in range(0, nsim):
    sol = list(np.random.choice([1,2],n))
    modularityVEC.append(modularity(net=net, solC=sol))

dis=[]
for i in range(0, nsim-1):
    for j in range(i+1, nsim):
        disttemp = abs(modularityVEC[i]-modularityVEC[j])
        dis.append(disttemp)

mm = np.mean(dis)
T0 = 100*mm
Tf = mm/100
nsim = 30000
A = T0
B = math.log(Tf/A)/nsim
Temp = A*np.exp(B*np.arange(1,nsim+1))

modularityPROC = []
sol = list(np.random.choice([1,2],n))
solNEW = sol
modularityBEST = modularity(net=net, solC=solNEW)
for t in range(0, nsim):
    nodeRAN = (int)(np.random.choice(vertices, 1)) - 1
    solNEW[nodeRAN] = 2 if sol[nodeRAN] == 1 else 1
    modularityNEW = modularity(net=net, solC=solNEW)
    if (modularityNEW >= modularityBEST):
        sol = solNEW
        modularityBEST = modularityNEW
    else:
        diff = modularityBEST-modularityNEW
        p = math.exp(-diff/Temp[t])
        ran = random.uniform(0, 1)
        if (ran <= p):
            sol = solNEW
            modularityBEST = modularityNEW

    modularityPROC.append(modularityBEST)

print(sol)

# for i in range(0, len(sol)):
#     print(f"({i+1}, {sol[i]})")

# print(modularityBEST)
