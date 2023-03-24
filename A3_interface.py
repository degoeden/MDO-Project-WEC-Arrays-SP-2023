# Contains Functions to complets A3b
import scipy.optimize as scipy_opt
import modules.model_2WECs as model

def gradient_objective(x,p):
    Power_out,efficiency,LCOE = model.run(x,p)
    if LCOE > 10:
        Power_out = 0
    return Power_out

def gradient_method(x0,p):
    scipy_opt.minimize(gradient_objective, x0, method='nelder-mead', options={'xatol': 1e-8, 'disp': True})
    return x_best