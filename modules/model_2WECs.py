import Econ as Econ
import hydro as hydro
from wec_dyn import wec_dyn as wec_dyn
from time_avg_power import time_avg_power as time_avg_power
from numpy import pi as pi
import numpy as np

# x = [radius all wecs, spacing, damping wec 1, stiffness wec 1, damping 2, stiffness 2]
# p = [Wave Frequency, Wave Amplitude, density of WEC material]
def run(x,p):
    nWEC = 2    # There are two WECs
    # Initialize some Vectors
    power_indv = np.zeros(nWEC) #   Each WEC's power out
    XI = np.zeros(nWEC)         #   Each WEC's heave motion RAO
    damp = np.zeros(nWEC)       #   Each WEC's pto damping
    stif = np.zeros(nWEC)       #   Each WEC's pto stiffness

    # Unpack Design Variables
    wec_radius = x[0]
    wec_spacing = x[1]
    for i in range(nWEC):
        damp[i] = x[2+2*i]
        stif[i] = x[3+2*i]
    
    # Unpack Parameters
    omega = p[0]
    wave_amp = p[1]
    rho_wec = p[2]

    # Mass Calculation
    m = rho_wec*4*pi/3*wec_radius**3

    # Hydro Module
    hydro_results = hydro.run(wec_radius,wec_spacing)
        # hydro_results = [Exciting Force RAO, Added mass, Wave damping, Hydrostatic restoring] for each WEC

    # Dynamics and Controls Modules
    for i in range(nWEC):
        F,A,B,C = hydro_results[i]  #   [Exciting Force RAO, Added mass, Wave damping, Hydrostatic restoring]
        XI[i] = wec_dyn(omega,F,A,B,C,m,damp[i],stif[i])    #   Heave motion RAO   
        power_indv[i] = time_avg_power(XI[i],damp[i],omega,wave_amp)    #   Time Average Power captured
    power = sum(power_indv) #   sum power outs

    # Power Transmission and Economics Module
    Power_out,efficiency,LCOE = Econ.run([nWEC,wec_radius,wec_spacing],power)

    return Power_out,efficiency,LCOE