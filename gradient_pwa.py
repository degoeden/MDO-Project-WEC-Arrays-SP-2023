# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import optimization_interfaces.A3_interface as A3
import numpy as np
import matplotlib.pyplot as plt
# ================================================================================= #
#                                   Set-Up                                          #
# ================================================================================= #
nwec = 4
# Initial Design Vector
r = 5
wecx = [0, 10*r, 20*r, 30*r]
wecy = [0, 0, 0, 0]
wecy = wecx
#wecx = [0, 0, 0, 0]
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
fig = plt.figure(1)
plt.plot(wecx,wecy,linestyle='none',marker = 'o',markersize = r*2,color='y')
# ================================================================================= #
#                               Optimization Code                                   #
# ================================================================================= #
# Run Optimization
best = A3.gradient_method(x0,p,bnds,opt)    #   Gradient Optimization
# ================================================================================= #
print(best)
r = best[0]
for i in range(nwec):
    wecx[i] = best[1+i*3]
    wecy[i] = best[2+i*3]
plt.plot(wecx,wecy,linestyle = 'none',marker = 'o',markersize = r*2,color='m')
plt.show()