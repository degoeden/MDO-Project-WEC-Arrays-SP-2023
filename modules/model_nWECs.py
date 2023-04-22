import modules.ECON as Econ
from modules.wec_dyn import wec_dyn as wec_dyn
from modules.time_avg_power import time_avg_power as time_avg_power
from numpy import pi as pi
import numpy as np
import modules.hydrostuff as hydro

# x = [radius all wecs, x location, y location, pto damping, ... other wecs x y and d]
# p = [Wave Frequency, Wave Amplitude, density of WEC material, number of WECs]

def run(x,p):
    nWEC = p[3]
      
    # Unpack Design Variables
    wec_radius = x[0]
    wecx = np.zeros(nWEC)
    wecy = np.zeros(nWEC)
    damp = np.zeros(nWEC)
    damp[0] = 10**x[1]
    for i in range(nWEC-1):
        wecx[i+1] = x[2+i*3]
        wecy[i+1] = x[3+i*3]
        damp[i+1] = 10**x[4+i*3]
    
    # Unpack Parameters
    omega = p[0]
    wave_amp = p[1]
    rho_wec = p[2]

    # Mass Calculation
    m = rho_wec*4*pi/3*wec_radius**3
    
    # Hydro Module
    beta = 0
    A,B,C,F = hydro.run(wec_radius,beta,omega,wecx,wecy)
    
    # Dynamics and Controls Modules
    power_indv = np.zeros(nWEC)
    for i in range(nWEC):
        XI,stif = wec_dyn(omega,F[i],A[i],B[i],C[i],m,damp[i])    #   Heave motion RAO  
        power_indv[i] = time_avg_power(XI,damp[i],omega,wave_amp) #   Time Average Power captured

    # Power Transmission and Economics Module
    Power_out,LCOE = Econ.run(wec_radius,power_indv)

    return LCOE
