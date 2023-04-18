# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import optimization_interfaces.A3_interface as A3
import numpy as np
# ================================================================================= #
#                                   Set-Up                                          #
# ================================================================================= #
nwec = 4
# Initial Design Vector
r = 5
wecx = [0, 0, 0, 0]
wecy = [0, 10*r, 20*r, 30*r]
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
        [-100*r,100*r],[0*r,100*r],[0,1e7],   # wec 2
        [-100*r,100*r],[0*r,100*r],[0,1e7],   # wec 3
        [-100*r,100*r],[0*r,100*r],[0,1e7]]   # wec 4
# Parameters
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
#best = A3.gradient_method(x0,p,bnds,opt)    #   Gradient Optimization
# ================================================================================= #
print(best)

'''********************************OLD CODE**************************************** #
# ================================================================================= #
#                                   2 WECs                                          # 
# ================================================================================= #
# Initial WEC design
r = 8                               #   WEC Radius
space = 3                           #   WEC spacing multiplier (multiplies by the radius to give spacing)
d1 = 1e5                            #   PTO damping
d2 = 1e5    
x0 = [r,space,d1,d2]
bnds=[[2.5,15],[4,20],[10,10**7],[10,10**7]]    #   Set bounds for design variables

# Parameters
omega = 1.047                       #   Wave Frequency
A = 1.5                             #   Wave Amplitude
rho_wec = 850                       #   Density of WEC material
n_wec = 2                           #   Number of WEC's - will be in x soon                                 
p = [omega,A,rho_wec,n_wec] 
opt={'xatol': 1e-3, 'disp': True}  
# ================================================================================= #
# Run Optimization
#best = A3.heuristic_method2(p,bnds,opt)      #   Heuristic Optimization
best = A3.gradient_method2(x0,p,bnds,opt)    #   Gradient Optimization
# ================================================================================= #
# Print Best
print(best)'''