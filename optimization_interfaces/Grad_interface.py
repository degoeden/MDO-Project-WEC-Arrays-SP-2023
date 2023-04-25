import scipy.optimize as scipy_opt
import modules.model_nWECs as model
import numpy as np
import optimization_interfaces.google_translate as translate
# ================================================================================= #
#                               Unscaled / Normal                                   #
# ================================================================================= #
def objective(x,args):
    LCOE = model.run(x,args)
    return LCOE

def gradient_method(x0,p,limits):
    opt={'disp': True}
    nwec = p[3]
    n_var=3*(nwec-1)+2
    xl = np.zeros(n_var)            #   Lower bnds
    xu = np.zeros(n_var)            #   Upper bnds
    xl[0] = limits['r'][0]
    xu[0] = limits['r'][1]
    xl[1] = limits['d'][0]
    xu[1] = limits['d'][1]
    for i in range(nwec-1):
        xl[i*3+2] = limits['x'][0]
        xu[i*3+2] = limits['x'][1]
        xl[i*3+3] = limits['y'][0]
        xu[i*3+3] = limits['y'][1]
        xl[i*3+4] = limits['d'][0]
        xu[i*3+4] = limits['d'][1]
    bnds = [[l,u] for l,u in zip(xl,xu)]    #   zip bnds together
    res = scipy_opt.minimize(objective,x0,p,'slsqp',bounds=bnds,options = opt,tol = 1e-3, )
    X = res.x
    return X

# ================================================================================= #
#                                     Scaled                                        #
# ================================================================================= #
def objective_scaled(x,args):
    x = translate.scaled2normal(x)
    LCOE = model.run(x,args)
    return LCOE

def gradient_method_scaled(x0,p,limits):
    x0 = translate.normal2scaled(x0)
    opt={'disp': True}
    nwec = p[3]
    n_var=3*(nwec-1)+2
    xl = np.zeros(n_var)
    xu = np.zeros(n_var)
    xl[0] = limits['r'][0]
    xu[0] = limits['r'][1]
    xl[1] = limits['d'][0]
    xu[1] = limits['d'][1]
    for i in range(nwec-1):
        xl[i*3+2] = limits['x'][0]
        xu[i*3+2] = limits['x'][1]
        xl[i*3+3] = limits['y'][0]
        xu[i*3+3] = limits['y'][1]
        xl[i*3+4] = limits['d'][0]
        xu[i*3+4] = limits['d'][1]
    xl = translate.normal2scaled(xl)
    xu = translate.normal2scaled(xu)
    bnds = [[l,u] for l,u in zip(xl,xu)]
    res = scipy_opt.minimize(objective_scaled,x0,p,'slsqp',bounds=bnds,options = opt,tol = 1e-3, )
    X = translate.scaled2normal(res.x)
    return X