# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import optimization_interfaces.A3_interface as A3
import numpy as np
# ================================================================================= #
#                                   Set-Up                                          #
# ================================================================================= #
r = 5
bnds = [[2,8],   # radius
        [0,0],[0,0],[0,1e7], # wec 1
        [-100*r,100*r],[-100*r,100*r],[0,1e7],   # wec 2
        [-100*r,100*r],[-100*r,100*r],[0,1e7],   # wec 3
        [-100*r,100*r],[-100*r,100*r],[0,1e7]]   # wec 4
# Parameters
nwec = 4
omega = 1.047
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,nwec]
opt={'xatol': 1e-3, 'disp': True}  
# ================================================================================= #
#                               Optimization Code                                   #
# ================================================================================= #
# Run Optimization
best = A3.heuristic_method(p,bnds,opt)      #   Heuristic Optimization
# ================================================================================= #
print(best)
