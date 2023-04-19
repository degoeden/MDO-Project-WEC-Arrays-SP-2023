# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import optimization_interfaces.A3_interface as A3
import numpy as np
# ================================================================================= #
#                                   Set-Up                                          #
# ================================================================================= #
nwec = 4
# Initial Design Vector
r = 5
wecy = [0, 10*r, 20*r, 30*r]
wecx = [0, 0, 0, 0]
d0 = 1e4
damp = [d0, d0, d0, d0]
x0 = np.zeros(1+3*nwec)
x0[0] = r
for i in range(nwec):
    x0[1+i*3] = wecx[i]
    x0[2+i*3] = wecy[i]
    x0[3+i*3] = damp[i]
bnds = [[2,8],   # radius
        [0,0],[0,0],[0,1e7], # wec 1
        [-100*r,100*r],[-100*r,100*r],[0,1e7],   # wec 2
        [-100*r,100*r],[-100*r,100*r],[0,1e7],   # wec 3
        [-100*r,100*r],[-100*r,100*r],[0,1e7]]   # wec 4
# Parameters
omega = 0.785
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,nwec]
opt={'xatol': 1e-3, 'disp': True}  
# ================================================================================= #
#                               Optimization Code                                   #
# ================================================================================= #
# Run Optimization
best = A3.gradient_method(x0,p,bnds,opt)    #   Gradient Optimization
# ================================================================================= #
print(best)
