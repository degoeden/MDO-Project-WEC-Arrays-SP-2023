# Calculates the distance between the closest two WECs
import numpy as np

def run(x,p):
    nwec = p[3]                 # Number of WECs
    wecx = np.zeros(nwec)       # Stores x's
    wecy = np.zeros(nwec)       # Stores y's
    for i in range(nwec-1):
        wecx[i+1] = x[2+i*3]
        wecy[i+1] = x[3+i*3]
    d = [] 
    for i in range(nwec):
        for j in range(i+1,nwec):
            d.append(((wecx[i]-wecx[j])**2 + (wecy[i]-wecy[j])**2)**(1/2))      # Compute the distance
    mind = min(d)               # What is the shortest distance?
    return (mind)