import modules.Econ_nWEC as Econ
import modules.geometry as geom
from modules.wec_dyn import wec_dyn as wec_dyn
from modules.time_avg_power import time_avg_power as time_avg_power
from numpy import pi as pi
import numpy as np
import modules.pwa.pwaFUNC as pwa
import modules.hydrostatics as hydrostatics

# x = [radius all wecs, x location, y location, pto damping, ... other wecs x y and d]
# p = [Wave Frequency, Wave Amplitude, density of WEC material, number of WECs]

def run(x,p):
    nWEC = p[3]
  
    # Unpack Design Variables
    wec_radius = x[0]
    wecx = np.zeros(nWEC)
    wecy = np.zeros(nWEC)
    damp = np.zeros(nWEC)
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
    bodies,xyzees = geom.run(wec_radius,wecx,wecy)      #   Get bodies
    pwa_results = pwa.run(bodies,xyzees,rho_wec,omega)  #   PWSLAY
    FK,Cs = hydrostatics.run(bodies,omega)            #   Hydrostatic Restoring Coefficients

    pwaF = {body:[] for body in bodies}
    As = {body:[] for body in bodies}
    Bs = {body:[] for body in bodies}
    for body in bodies:
        pwaF[body].append(pwa_results[body][0]['Heave'])
        As[body].append(pwa_results[body][1]['added_mass'])
        Bs[body].append(pwa_results[body][2]['damping'])


    dampy = {body:[] for body in bodies}
    i = 0
    for body in bodies:
        dampy[body] = damp[i]
        i = i + 1
    
    # Dynamics and Controls Modules
    power_indv = {body:[] for body in bodies} #   Each WEC's power out
    for body in bodies:
        A = As[body][0]
        B = Bs[body][0]
        C = Cs[body][0]
        F = FK[body][0] + pwaF[body][0]
        XI,stif = wec_dyn(omega,F,A,B,C,m,dampy[body])    #   Heave motion RAO   
        power_indv[body].append(time_avg_power(XI,dampy[body],omega,wave_amp))    #   Time Average Power captured

    # Power Transmission and Economics Module
    Power_out,efficiency,LCOE = Econ.run(wec_radius,power_indv,bodies)

    return Power_out,efficiency,LCOE