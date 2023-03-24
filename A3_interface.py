# Contains Functions to complets A3b
import scipy.optimize as scipy_opt
import modules.model_2WECs as model

def gradient_objective(x,p):
    Power_out,efficiency,LCOE = model.run(x,p)
    if LCOE > 10:
        Power_out = 0
    if x[0] < 2.5:
        Power_out = 0
    if x[0] > 15:
        Power_out = 0
    if x[1] < 2*x[0]:
        Power_out = 0
    if x[1] > 5*x[0]:
        Power_out = 0
    for i in range(p[3]):
        if x[2+i*2] < 0:
            Power_out = 0
        if x[3+i*2] < 0:
            Power_out = 0
        if x[2+i*2] > 500:  # may need a more concrete number
            Power_out = 0
        if x[3+i*2] > 500:  # may need a more concrete number
            Power_out = 0
    
    return -1*Power_out

def gradient_method(x0,p):
    res = scipy_opt.minimize(gradient_objective, x0, method='nelder-mead', args = p, options={'xatol': 1e-8, 'disp': True})
    return res.x