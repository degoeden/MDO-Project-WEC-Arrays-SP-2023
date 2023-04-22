# Collection of Power distribution and Cost analysis modules
import numpy as np

# Core Econ function to call from main

def run(size,Power,bodies): 
    t=10    # Lifetime : years
    nWEC=len(bodies)
    rWEC=size
    Vol_WEC=nWEC*np.pi*rWEC**3*4/3
    vol_cost=10**4 # $10k per m3 of WEC volume
    Cbase = 10*10**6+(Vol_WEC)*vol_cost #capital cost will scale with WEC volume
    CA=0.1 # $/W cost per capacity to construct
    DA=2*10**6 # cost to decomission
    MA = 5*10**5 # Base Maint cost / year
    MV=10 #  variable Maint cost / power / year  : $M/MWhr/yr 
    r=0.08 # discount rate %
    hr=8760 # hr/yr
    OEE=0.7 # Uptime
    p_sig = [p_sig[0] for p_sig in Power.values()]
    P = np.sum(p_sig)
    print(f'Power is: {P/1e6} MW')
    cap=(Cbase+MA+(MV*np.log10(P)))/(1+r)**(1) # year one CapEx
    for i in range(t-1):
        cap = cap + ((MA+MV*np.log10(P))/((1+r)**(i+2))) #subsequent year discounted CapEx sum over lifetime

    comish=CA*P
    decomish=DA/(1+r)**t # decomish cost discounted to final year
    cap=cap+comish+decomish

    transmission_efficiency = 0.8
    motor_efficiency = 0.6

    Enet=P*t*hr*OEE*transmission_efficiency*motor_efficiency*0.001 # $/kWhr
    LCOE=cap/Enet # $/kW.hr
    return Enet, LCOE