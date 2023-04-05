# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import optimization_interfaces.A3_interface as A3
import numpy as np

# ================================================================================= #
#                                   2 WECs                                          # 
# ================================================================================= #
# Initial WEC design
r = 3                               #   WEC Radius
space = 4                           #   WEC spacing multiplier (multiplies by the radius to give spacing)
d1 = 1e6                            #   PTO damping
d2 = 1e6    
x0 = [r,space,d1,d2]
x0 = [8, 3, 1e5, 1e5]
bnds=[[2.5,15],[2,20],[10,10**7],[10,10**7]]    #   Set bounds for design variables

# Parameters
omega = 1.047                       #   Wave Frequency
A = 1.5                             #   Wave Amplitude
rho_wec = 850                       #   Density of WEC material
n_wec = 2                           #   Number of WEC's - will be in x soon                                 
p = [omega,A,rho_wec,n_wec] 
opt={'xatol': 1e-3, 'disp': True}  
# ================================================================================= #
# Run Optimization
#best = A3.heuristic_method(p,bnds,opt)      #   Heuristic Optimization
best = A3.gradient_method(x0,p,bnds,opt)    #   Gradient Optimization
# ================================================================================= #
# Print Best
print(best)