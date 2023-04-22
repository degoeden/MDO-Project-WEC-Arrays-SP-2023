# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import optimization_interfaces.GA_interface as GA
import numpy as np
import matplotlib.pyplot as plt
# ================================================================================= #
#                                   Set-Up                                          #
# ================================================================================= #
# Parameters
nwec = 4
omega = 1.047
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,nwec]
# ================================================================================= #
#                               Optimization Code                                   #
# ================================================================================= #
# Run Optimization
X,F = GA.MOCHA(p)      #   Heuristic Optimization
# ================================================================================= #
print(f"The x is {X}")
print(F)
'''damp = np.zeros(nwec)
wecx = np.zeros(nwec)
wecy = np.zeros(nwec)
r = X[0]
damp[0] = 10**X[1]
for i in range(nwec-1):
    wecx[i+1] = X[2+i*3]
    wecy[i+1] = X[3+i*3]
    damp[i+1] = 10**X[4+i*3]
print(damp)
fig, ax = plt.subplots()
for i in range(nwec):
    circles = plt.Circle((wecx[i],wecy[i]),r,color='m')
    ax.add_patch(circles)
ax.axis('equal')
plt.xlim([-100,100])
plt.ylim([-100,100])

plt.show()'''