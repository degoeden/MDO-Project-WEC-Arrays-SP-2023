# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import A3_interface as A3

# Initial WEC design
r = 8                               #   WEC Radius
space = 3                           #   WEC spacing multiplier (multiplies by the radius to give spacing)
d1 = 300                            #   PTO damping
d2 = 300    
k1 = 300                            #   PTO stiffness
k2 = 300
x0 = [r,space,d1,k1,d2,k2]
bnds=[[2.5,15],[2,10],[10,500],[0,500],[10,500],[0,500]]    #   Set bounds for design variables

# Parameters
omega = 1.047                       #   Wave Frequency
A = 1.5                             #   Wave Amplitude
rho_wec = 850                       #   Density of WEC material
n_wec = 2                           #   Number of WEC's - will be in x soon                                 
p = [omega,A,rho_wec,n_wec] 

# ================================================================================ #
# Run Optimization
best = A3.heuristic_method(p,bnds)          #   Heuristic Optimization
#opt={'xatol': 1e-2, 'disp': True}           #   Options: for gradient only
#best = A3.gradient_method(x0,p,bnds,opt)    #   Gradient Optimization
# ================================================================================ #
# Print Best
print(best)