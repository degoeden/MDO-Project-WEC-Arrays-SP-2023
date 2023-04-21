# Contains Functions to complets A3b
import scipy.optimize as scipy_opt
import numpy as np
import matplotlib.pyplot as plt
import modules.model_nWECs as model
import modules.model_nWECs_fixr as model_fixr
import modules.translate_nate as google_translate
import optimization_interfaces.A3_interface as real_A3

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

def nate_objective(x,*args):
    p = args
    x,p = google_translate.nate2english(x,p)
    LCOE = real_A3.objective1(x,p)
    return LCOE


def heuristic_method(p,bnds,is_it_int,opt):
    res = scipy_opt.differential_evolution(nate_objective, bounds=bnds, args=p, integrality=is_it_int)
    return res.x