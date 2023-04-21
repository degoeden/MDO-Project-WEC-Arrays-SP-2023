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
    #print(f"The numbe rof WEC is {nWEC}")
  
    # Unpack Design Variables
    wec_radius = x[0]
    wecx = np.zeros(nWEC)
    wecy = np.zeros(nWEC)
    damp = np.zeros(nWEC)
    for i in range(nWEC-1):
        wecx[i] = x[2+i*3]
        wecy[i] = x[3+i*3]
        damp[i] = x[1+i*3]
    
    # Unpack Parameters
    omega = p[0]
    wave_amp = p[1]
    rho_wec = p[2]

    # Mass Calculation
    m = rho_wec*4*pi/3*wec_radius**3
    
    # Geometry and Hydro Modules
    bodies,xyzees = geom.run(wec_radius,wecx,wecy)      #   Get bodies
    #print("after geometry")
    beta = 0
    pwa_results = pwa.run(bodies,xyzees,1023.0,omega,beta)  #   PWSLAY
    #np.savetxt('pwa_results.txt',pwa_results)
    FK,hydro_restore = hydrostatics.run(bodies,omega,beta)   #   Hydrostatic Restoring Coefficients and Froude-Krylov Force

    # Put PTO damping into body array format
    dampy = {body:[] for body in bodies}
    i = 0
    for body in bodies:
        dampy[body] = damp[i]
        i = i + 1
    
    # Dynamics and Controls Modules
    power_indv = {body:[] for body in bodies}   #   Each WEC's power out
    for body in bodies:
        # None of these trigger
        A = pwa_results[body][1]['added_mass']  # Added mass from PWA
        #print(f"The added mass is {A}")
        '''if A > 5e5:
            A = (5e6)
            print('added mass TOO BIG')'''
        B = pwa_results[body][2]['damping']     # Damping from PWA
        '''if B > 5e6:
            B = (5e6)
            print('damping TOO BIG')'''
        C = hydro_restore[body][0]              # Hydrostatic Resoring Coefficient from hydro statics module
        '''if C > 1e7:
            C = (1e7)**(1/2)
            print('stiffness TOO BIG')'''
        F = FK[body][0] + pwa_results[body][0]['Heave'] # Total force: Foude Krylov from hydro statics, others from PWA
        
        #print(f"For body {body}")
        #print(f"Added mass {A} & Damp {B} & Force {F} & Stif {C}")
        XI,stif = wec_dyn(omega,F,A,B,C,m,dampy[body])    #   Heave motion RAO   
        power_indv[body].append(time_avg_power(XI,dampy[body],omega,wave_amp))    #   Time Average Power captured

    # Power Transmission and Economics Module
    Power_out,LCOE = Econ.run(wec_radius,power_indv,bodies)

    return Power_out,LCOE
