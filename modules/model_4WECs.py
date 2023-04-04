import modules.Econ_nWEC as Econ
import modules.geometry as geom
from modules.wec_dyn import wec_dyn as wec_dyn
from modules.time_avg_power import time_avg_power as time_avg_power
from numpy import pi as pi
import numpy as np
import modules.pwa.pwaFUNC as pwa

# x = [radius all wecs, x location, y location, pto damping, ... other wecs x y and d]
# p = [Wave Frequency, Wave Amplitude, density of WEC material, number of WECs]

def run(x,p):
    nWEC = p[3]
    # Initialize some Vectors
    power_indv = np.zeros(nWEC) #   Each WEC's power out
    wecx = np.zeros(nWEC)       #   Each WEC's x location
    wecy = np.zeros(nWEC)       #   Each WEC's y location
    damp = np.zeros(nWEC)       #   Each WEC's pto damping
    stif = np.zeros(nWEC)       #   Each WEC's pto stiffness

    # Unpack Design Variables
    wec_radius = x[0]
    for i in range(nWEC):
        wecx[i] = x[1+i*3]
        wecy[i] = x[2+i*3]
        damp[i] = x[3+i*3]
    
    # Unpack Parameters
    omega = p[0]
    wave_amp = p[1]
    rho_wec = p[2]

    # Mass Calculation
    m = rho_wec*4*pi/3*wec_radius**3

    # Geometry and Hydro Modules
    bodies = geom.run(wec_radius,wecx,wecy)
    pwa_results = pwa.run(bodies)
        # hydro_results = [Exciting Force RAO, Added mass, Wave damping, Hydrostatic restoring] for each WEC

    # Dynamics and Controls Modules
    for i in range(nWEC):
        F,A,B,C = hydro_results[i]  #   [Exciting Force RAO, Added mass, Wave damping, Hydrostatic restoring]
        XI,stif[i] = wec_dyn(omega,F,A,B,C,m,damp[i])    #   Heave motion RAO   
        power_indv[i] = time_avg_power(XI,damp[i],omega,wave_amp)    #   Time Average Power captured

    # Power Transmission and Economics Module
    # We need a new econ module that can account for different spacings
    Power_out,efficiency,LCOE = Econ.run([nWEC,wec_radius,wecx,wecy],power_indv)

    return Power_out,efficiency,LCOE,stif