# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import optimization_interfaces.A3_interface as A3
import numpy as np
import matplotlib.pyplot as plt
import random as randy
# ================================================================================= #
#                                   Set-Up                                          #
# ================================================================================= #
nwec = 4
# Initial Design Vector
r = 5
wecx = [0, randy.random()*200-100, randy.random()*200-100, randy.random()*200-100]
wecy = [0, randy.random()*200-100, randy.random()*200-100, randy.random()*200-100]
#wecx = [0, 40, 80, -20]
#wecy = [0, 0, 0, 0]
d0 = 3
damp = [d0, d0, d0, d0]
x0 = np.zeros(3*nwec-2)
#x0[0] = r
x0[0] = damp[0]
for i in range(nwec-1):
    x0[1+i*3] = wecx[i+1]
    x0[2+i*3] = wecy[i+1]
    x0[3+i*3] = damp[i+1]
bnds = [#[2,8],   # radius
        [0,5], # wec 1
        [-100,100],[-100,100],[0,5],   # wec 2
        [-100,100],[-100,100],[0,5],   # wec 3
        [-100,100],[-100,100],[0,5]]   # wec 4
# Parameters
omega = 1.047
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,nwec,r]
opt={'xatol': 1e-5, 'disp': True}  
fig = plt.figure(1)
plt.plot(wecx,wecy,linestyle='none',marker = 'o',markersize = r*2,color='y')
# ================================================================================= #
#                               Optimization Code                                   #
# ================================================================================= #
# Run Optimization
best = A3.gradient_method(x0,p,bnds,opt)    #   Gradient Optimization
# ================================================================================= #
print(best)
damp[0] = 10**best[0]
for i in range(nwec-1):
    wecx[i+1] = best[1+i*3]
    wecy[i+1] = best[2+i*3]
    damp[i+1] = 10**best[3+i*3]
print(damp)
plt.plot(wecx,wecy,linestyle = 'none',marker = 'o',markersize = r*2,color='m')
plt.show()