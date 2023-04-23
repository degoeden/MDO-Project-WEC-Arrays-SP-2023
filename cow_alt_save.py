# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import optimization_interfaces.GA_interface as GA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
xNames=['radius','d1','x2','y2','d2','x3','y3','d3','x4','y4','d4']
Xdf=pd.DataFrame(X,columns=xNames)
fNames=['LCOE','Max Spacing']
Fdf=pd.DataFrame(F,columns=fNames)
pd.concat([Xdf,Fdf],axis=1).to_csv('paretos/domXF@'+hex(int(end_time))[2:]+'.csv')

