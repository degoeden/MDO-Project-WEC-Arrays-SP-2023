# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import optimization_interfaces.GA_interface as GA
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
# ================================================================================= #
#                                   Set-Up                                          #
# ================================================================================= #
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
X,F,H = GA.MOCHA(p,limits)      #   Heuristic Optimization
end_time = time.time()
print(f"This took this long: {end_time-start_time}")
# ================================================================================= #
'''print(X)
print(F)
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

plt.show()'''

# save nondominated
F2table = {F[i,0]:F[i,1] for i in range(len(F[:,0]))}
Xtable = {F[i,0]:X[i,:] for i in range(len(F[:,0]))}
F1 = np.sort(F[:,0])
F2 = [F2table[i] for i in F1]
X = [Xtable[i] for i in F1]
with open(f'domF@{end_time}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in range(len(F)):
        writer.writerow([F1[i],F2[i]])

with open(f'domX@{end_time}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in range(len(X)):
        writer.writerow(X[i])

# all points
'''with open(f'allF@{end_time}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in range(len(H.F)):
        writer.writerow(H.F[i])

with open(f'allX@{end_time}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in range(len(H.X)):
        writer.writerow(H.X[i])'''
