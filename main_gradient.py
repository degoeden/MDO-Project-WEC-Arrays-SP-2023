import optimization_interfaces.Grad_interface as grad
import time
import numpy as np
import matplotlib.pyplot as plt

# ================================================================================= #
#                                   Set-Up                                          #
# ================================================================================= #
# Initial Design Vector
x0 = [2,3,-5,25,3,-5,-1,3,-10,25,3]

# Parameters
nwec = 4
omega = 1.047
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,nwec]
limits = {'r':[1,10], 'd':[0,6], 'x':[-100,100], 'y':[-100,100]}
# ================================================================================= #
#                               Optimization Code                                   #
# ================================================================================= #
# Run Optimization
start_time = time.time()
X= grad.gradient_method(x0, p,limits)      #   Heuristic Optimization
end_time = time.time()
print(f"This took this long: {end_time-start_time}")
# ================================================================================= #
print(X)
damp = np.zeros(nwec)
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
#plt.xlim([-100,100])
#plt.ylim([-100,100])

plt.show()