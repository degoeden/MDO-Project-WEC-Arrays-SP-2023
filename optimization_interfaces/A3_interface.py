# Contains Functions to complets A3b
import scipy.optimize as scipy_opt
import numpy as np

# import model for what you want to do...
import modules.model_4WECs as model

def objective(x,*args):         #   Calculates LCOE
    p = args
    Power_out,efficiency,LCOE = model.run(x,p)  #   runs the model
    print(LCOE)
    return LCOE

def objective1(x,args):         #   Calculates LCOE
    p = args
    Power_out,efficiency,LCOE = model.run(x,p)  #   runs the model
    print(LCOE)
    return LCOE

def gradient_method(x0,p,bnds,opt):     #   Gradient Method Search Algorithm
    res = scipy_opt.minimize(objective1, x0, method='nelder-mead', args=p, bounds=bnds, options=opt)
    return res.x

def heuristic_method(p,bnds,opt):       #   GA method search algorithm
    res = scipy_opt.differential_evolution(objective, bounds=bnds, args=p)
    return res.x