import expiriments.doe as doe
from modules.wec_dyn import wec_dyn as wec_dyn
from modules.time_avg_power import time_avg_power as time_avg_power
import modules.n2.Econ_2WEC as Econ_2WEC
import modules.n2.hydro2 as hydro2

import pandas as pd
import numpy as np
# Initial WEC design
r = 2
L = 20
d1 = 100
d2 = 100
k1 = 300
k2 = 300

# Parameter
omega = 1.047
A = 1.5
rho = 850


x = [r,L,d1,k1,d2,k2]
results = hydro2.run(r,L)
hydro2=results[0]
XI = wec_dyn(omega,hydro2[0],hydro2[1],hydro2[2],hydro2[3],rho*4/3*np.pi*r**3,d1,k1)
P = time_avg_power(XI,d1,omega,A)
Power_out,efficiency,LCOE = doe.evaluate(x,0,omega,rho,A)
print("--------------------------------------")
print("Power out: ", Power_out)
print("Efficiency: ", efficiency)
print("LCOE: ", LCOE)
print("--------------------------------------")
print("thing for nate: ", hydro2[0])
print("--------------------------------------")
print("A33: ", hydro2[1])
print("B33: ", hydro2[2])
print("C33: ", hydro2[3])
print("F3/A: ", abs(hydro2[0]))
print("XI: ", XI)
print("P_WEC: ", P)