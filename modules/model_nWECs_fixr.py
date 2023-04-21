import modules.ECON as Econ
import modules.geometry as geom
from modules.wec_dyn import wec_dyn as wec_dyn
from modules.time_avg_power import time_avg_power as time_avg_power
from numpy import pi as pi
import numpy as np
import modules.pwa.pwaFUNC as pwa
import modules.hydrostatics as hydrostatics
import modules.mdoplsworkfuck as slay

# x = [radius all wecs, x location, y location, pto damping, ... other wecs x y and d]
# p = [Wave Frequency, Wave Amplitude, density of WEC material, number of WECs]

def run(x,p):
    nWEC = p[3]
    #print(f"The numbe rof WEC is {nWEC}")
  
    # Unpack Design Variables
    wec_radius = p[4]
    wecx = np.zeros(nWEC)
    wecy = np.zeros(nWEC)
    damp = np.zeros(nWEC)
    damp[0] = 10**x[0]
    for i in range(nWEC-1):
        wecx[i+1] = x[1+i*3]
        wecy[i+1] = x[2+i*3]
        damp[i+1] = 10**x[3+i*3]
    print(f"Nate Look Here: {damp}")
    # Unpack Parameters
    omega = p[0]
    wave_amp = p[1]
    rho_wec = p[2]

    # Mass Calculation
    m = rho_wec*4*pi/3*wec_radius**3
    
    # Geometry and Hydro Modules
    beta = np.pi/2
    bodies,xyzees = geom.run(wec_radius,wecx,wecy)      #   Get bodies
    #print("after geometry")
    '''pwa_results = pwa.run(bodies,xyzees,1023.0,omega,beta)  #   PWSLAY
    #np.savetxt('pwa_results.txt',pwa_results)
    FK,hydro_restore = hydrostatics.run(bodies,omega,beta)   #   Hydrostatic Restoring Coefficients and Froude-Krylov Force'''
    Aarray,Barray,Carray,Farray = slay.run(wec_radius,beta,omega,wecx,wecy)

    # Put Stuff into body array format
    dampy = {body:[] for body in bodies}
    As = {body:[] for body in bodies}
    Bs = {body:[] for body in bodies}
    Cs = {body:[] for body in bodies}
    Fs = {body:[] for body in bodies}
    i = 0
    for body in bodies:
        dampy[body] = damp[i]
        As[body] = Aarray[i]
        Bs[body] = Barray[i]
        Cs[body] = Carray[i]
        Fs[body] = Farray[i]
        i = i + 1
    
    # Dynamics and Controls Modules
    power_indv = {body:[] for body in bodies}   #   Each WEC's power out
    for body in bodies:
        # None of these trigger
        #A = pwa_results[body][1]['added_mass']  # Added mass from PWA
        A = As[body][0]
        #print(f"The added mass is {A}")
        '''if A > 5e5:
            A = (5e6)
            print('added mass TOO BIG')'''
        #B = pwa_results[body][2]['damping']     # Damping from PWA
        B = Bs[body][0]
        '''if B > 5e6:
            B = (5e6)
            print('damping TOO BIG')'''
        #C = hydro_restore[body][0]              # Hydrostatic Resoring Coefficient from hydro statics module
        C = Cs[body][0]
        '''if C > 1e7:
            C = (1e7)**(1/2)
            print('stiffness TOO BIG')'''
        #F = FK[body][0] + pwa_results[body][0]['Heave'] # Total force: Foude Krylov from hydro statics, others from PWA
        F = Fs[body]
        print(f"The force is: {F}")
        #print(f"For body {body}")
        #print(f"Added mass {A} & Damp {B} & Force {F} & Stif {C}")
        print(f"NO NATE LOOK AT THIS: {dampy[body]}")
        XI,stif = wec_dyn(omega,F,A,B,C,m,dampy[body])    #   Heave motion RAO  
        print(f"the mag is: {abs(XI)}") 
        power_indv[body].append(time_avg_power(XI,dampy[body],omega,wave_amp))    #   Time Average Power captured

    # Power Transmission and Economics Module
    Power_out,LCOE = Econ.run(wec_radius,power_indv,bodies)

    return LCOE
