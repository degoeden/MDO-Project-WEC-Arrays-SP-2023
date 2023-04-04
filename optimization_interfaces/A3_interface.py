# Contains Functions to complets A3b
import scipy.optimize as scipy_opt
import modules.n2.model_2WECs as model
import numpy as np

# ================================================================================= #
#                                   2 WECs                                          # 
# ================================================================================= #
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

def objective2(x,*args):         #   Calculates LCOE
    p = args
    Power_out,efficiency,LCOE,stif = model.run(x,p)  #   runs the model
    print(LCOE)
    return LCOE

def objective12(x,args):         #   Calculates LCOE
    p = args
    Power_out,efficiency,LCOE,stif = model.run(x,p)  #   runs the model
    print(LCOE)
    return LCOE

def gradient_method2(x0,p,bnds,opt):     #   Gradient Method Search Algorithm
    res = scipy_opt.minimize(objective12, x0, method='nelder-mead', args=p, bounds=bnds, options=opt)
    return res.x

def heuristic_method2(p,bnds,opt):       #   GA method search algorithm
    res = scipy_opt.differential_evolution(objective2, bounds=bnds, args=p)
    return res.x


# ================================================================================= #
#                                   4 WECs                                          # 
# ================================================================================= #