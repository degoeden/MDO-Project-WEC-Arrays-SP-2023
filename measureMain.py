# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import optimization_interfaces.A3_interface as A3
import numpy as np
import time

# ================================================================================= #
#                                   2 WECs                                          # 
# ================================================================================= #
# Initial WEC design
r = 8                               #   WEC Radius
space = 3                           #   WEC spacing multiplier (multiplies by the radius to give spacing)
d1 = 1e5                            #   PTO damping
d2 = 1e5    
x0 = [r,space,d1,d2]
bnds=[[2.5,15],[2,20],[10,10**7],[10,10**7]]    #   Set bounds for design variables

# Parameters
omega = 1.047                       #   Wave Frequency
A = 1.5                             #   Wave Amplitude
rho_wec = 850                       #   Density of WEC material
n_wec = 2                           #   Number of WEC's - will be in x soon                                 
p = [omega,A,rho_wec,n_wec] 
opt={'xatol': 1e-3, 'disp': True} 


popSize = [15,100]
mutation = [(0.5,1),(0.4,1)]
recombination = [0.8,0.9]

measured = {'x':1}

for pops,muts,recombs in zip(popSize,mutation,recombination):
	opts = {'popsize':pops,'mutation':muts,'recombination':recombs}
	starttime = time.time()
	best = A3.heuristic_method(p,bnds,opts) 
	end = time.time()
	measured['time'] = end-starttime
	measured['recom'] = (pops,muts,recombs)
	measured['LCOE'] = best

opts = {'popsize':15,'mutation':(0.5,1),'recombination':0.8}
#popsize=15, tol=0.01, mutation=(0.5, 1), recombination=0.7
# ================================================================================= #
# Run Optimization

#best = A3.gradient_method(x0,p,bnds,opt)    #   Gradient Optimization
# ================================================================================= #
# Print Best
print("THE TABLES HERE IT IS")
print(measured)
