# Contains Functions to complets A3b
import scipy.optimize as scipy_opt
import modules.model_2WECs as model
import numpy as np
from platypus import NSGAII

def outofbounds(x,p):       #   Checks if any x's are out of bounds
    are_we = False
    if x[0] < 2.5:          #   Minimum WEC radius is 2.5 meters
        are_we = True
    if x[0] > 15:           #   MAX WEC radius is 15 meters
        are_we = True
    if x[1] < 2*x[0]:       #   Min WEC spacing is the diameter of the WECs
        are_we = True
    if x[1] > 5*2*x[0]:     #   MAX WEC spacing is 5 times the diameter of the WECs
        are_we = True
    for i in range(p[3]):
        if x[2+i*2] < 0:    #   No negative pto damping
            are_we = True
        if x[2+i*2] > 500:  #   may need a more concrete number
            are_we = True
        if x[3+i*2] < 0:    #   No negative pto stiffness
            are_we = True
        if x[3+i*2] > 500:  #   may need a more concrete number
            are_we = True
    
    return are_we

def objective(x,p):         #   Calculates LCOE
    Power_out,efficiency,LCOE = model.run(x,p)  #   runs the model
    #if Power_out < 1000:        #   Checks constraint on Power out
    #    LCOE = np.inf
    #if outofbounds(x,p):        #   Checks if any design variables are out of bounds
    #    LCOE = np.inf
    #    print(x)
    print(LCOE)
    return LCOE

def gradient_method(x0,p,bnds,opt):     #   Gradient Method Search Algorithm
    res = scipy_opt.minimize(objective, x0, method='nelder-mead', args = p, bounds=bnds, options=opt)
    return res.x

def GA_method(x0,p,bnds):   #   GA method search algorithm
    