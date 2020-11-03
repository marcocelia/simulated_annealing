import pandas as pd
import numpy as np
from modularity import modularity
import math

net = pd.read_csv('data/Zachary_Karate_club.txt', sep=' ', header=None)

vertices = sorted(set(list(net[0]) + list(net[1])))
n = len(vertices)

modularityVEC=[]
nsim = 200
for i in range(0,nsim):
    np.random.seed(123+i)
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
nsim = 10000
A = T0
B = math.log(Tf/A)/nsim
Temp = A**(B*np.arange(1,nsim+1))

modularityPROC = []