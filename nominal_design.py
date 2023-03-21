import doe
from modules.wec_dyn import wec_dyn as wec_dyn
from modules.time_avg_power import time_avg_power as time_avg_power
import modules.Econ as Econ
import modules.capy.notfinalbutworks as nfbw
import modules.capy.geometry
import modules.capy.hydrodyno
import modules.capy.hydrostatics
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
results = nfbw.run(r,L)
hydro=results[0]
XI = wec_dyn(omega,hydro[0],hydro[1],hydro[2],hydro[3],rho*4/3*np.pi*r**3,d1,k1)
P = time_avg_power(XI,d1,omega,A)
Power_out,efficiency,LCOE = doe.evaluate(x,0,omega,rho,A)
print("--------------------------------------")
print("Power out: ", Power_out)
print("Efficiency: ", efficiency)
print("LCOE: ", LCOE)
print("--------------------------------------")
print("thing for nate: ", hydro[0])
print("--------------------------------------")
print("A33: ", hydro[1])
print("B33: ", hydro[2])
print("C33: ", hydro[3])
print("F3/A: ", abs(hydro[0]))
print("XI: ", XI)
print("P_WEC: ", P)