# Contains Functions to complets A3b
import scipy.optimize as scipy_opt
import numpy as np
import matplotlib.pyplot as plt
import modules.model_nWECs as model
import modules.model_nWECs_fixr as model_fixr

def distance_check(wecx,wecy,r):
    n = len(wecx)
    d = []
    for i in range(n):
        for j in range(i+1,n):
            d.append(((wecx[i]-wecx[j])**2 + (wecy[i]-wecy[j])**2)**(1/2))
    mind = min(d)
    if mind<10*r:
        return 10000*(10*r - mind)**2     
    return 0

def objective(x,*args):         #   Calculates LCOE
    p = args
    if len(p)==4:
        nwec = p[3]
        r = x[0]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec):
            wecx[i] = x[1+i*3]
            wecy[i] = x[2+i*3]

        Power_out,LCOE = model.run(x,p)  #   runs the model
    else:
        nwec = p[3]
        r = p[4]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec-1):
            wecx[i+1] = x[1+i*3]
            wecy[i+1] = x[2+i*3]

        Power_out,LCOE = model_fixr.run(x,p)  #   runs the model
    LCOE = LCOE + distance_check(wecx,wecy,r)
    print(f"This is LCOE {LCOE}")
    return LCOE

def objective1(x,args):         #   Calculates LCOE
    p = args
    if len(p)==4:
        nwec = p[3]
        r = x[0]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec):
            wecx[i] = x[1+i*3]
            wecy[i] = x[2+i*3]

        Power_out,LCOE = model.run(x,p)  #   runs the model
    else:
        nwec = p[3]
        r = p[4]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec-1):
            wecx[i+1] = x[1+i*3]
            wecy[i+1] = x[2+i*3]

        Power_out,LCOE = model_fixr.run(x,p)  #   runs the model
    LCOE = LCOE + distance_check(wecx,wecy,r)
    print(f"This is LCOE {LCOE}")
    return LCOE

def maximumD(wecx,wecy):
    n = len(wecx)
    d = []
    for i in range(n):
        for j in range(i+1,n):
            d.append(((wecx[i]-wecx[j])**2 + (wecy[i]-wecy[j])**2)**(1/2))
    maxd = max(d)    
    return maxd

def objective2(x,args):         #   Calculates LCOE
    p = args
    if len(p)==4:
        nwec = p[3]
        r = x[0]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec):
            wecx[i] = x[1+i*3]
            wecy[i] = x[2+i*3]

        Power_out,LCOE = model.run(x,p)  #   runs the model
    else:
        nwec = p[3]
        r = p[4]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec-1):
            wecx[i+1] = x[1+i*3]
            wecy[i+1] = x[2+i*3]
    maxd = maximumD(wecx,wecy)
    maxd = maxd + distance_check(wecx,wecy,r)
    return maxd

def objective3(x,args): # multi objective 
    J1 = objective1(x,args)
    J2 = objective2(x,args)
    J3 = 0.5*J1/0.02 + 0.5*J2/100
    return J3

def gradient_method(x0,p,bnds,opt):     #   Gradient Method Search Algorithm
    history = []
    def callback(x,p):
        fobj = objective1(x,p)
        history.append(fobj)
    res = scipy_opt.minimize(objective1, x0, method='slsqp', args=p, bounds=bnds, options=opt)
    print("The values at each iteration")
    return res.x

def heuristic_method(p,bnds,opt):       #   GA method search algorithm
    res = scipy_opt.differential_evolution(objective, bounds=bnds, args=p)
    return res.x