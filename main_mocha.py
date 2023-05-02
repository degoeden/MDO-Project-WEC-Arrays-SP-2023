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
limits = {'r':[1,10], 'd':[0,6], 'x':[-500,500], 'y':[-500,500]}
# ================================================================================= #
#                               Optimization Code                                   #
# ================================================================================= #
# Run Optimization
start_time = time.time()
X,F,H = GA.MOCHA(p,limits)      #   Heuristic Optimization
end_time = time.time()
print(f"This took this long: {end_time-start_time}")
# ================================================================================= #
#                                 Save Pareto                                       #
# ================================================================================= #
# save nondominated
F2table = {F[i,0]:F[i,1] for i in range(len(F[:,0]))}
Xtable = {F[i,0]:X[i,:] for i in range(len(F[:,0]))}
F1 = np.sort(F[:,0])
F2 = [F2table[i] for i in F1]
X = [Xtable[i] for i in F1]
with open(f'paretos/domF@{end_time}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in range(len(F)):
        writer.writerow([F1[i],F2[i]])

with open(f'paretos/domX@{end_time}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in range(len(X)):
        writer.writerow(X[i])
