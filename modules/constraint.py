import numpy as np

def run(x,p):
    if len(p)==4:
        nwec = p[3]
        r = x[0]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec-1):
            wecx[i+1] = x[2+i*3]
            wecy[i+1] = x[3+i*3]
    else:
        nwec = p[3]
        r = p[4]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec-1):
            wecx[i+1] = x[1+i*3]
            wecy[i+1] = x[2+i*3]
    d = []
    for i in range(nwec):
        for j in range(i+1,nwec):
            d.append(((wecx[i]-wecx[j])**2 + (wecy[i]-wecy[j])**2)**(1/2))
    mind = min(d)
    print(f"The mind is {3*r -mind} <<0 ???!!!!")
    return (r*3 - mind)