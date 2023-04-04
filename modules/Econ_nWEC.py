# Collection of Power distribution and Cost analysis modules
import numpy as np

#import pandas as pd

# Incoming internal variables:
# Power vs frequency ouput from WEC array elements
def distance(x1,x2,y1,y2):
    dis = np.sqrt((x2-x1)**2+(y2-y1)**2)
    return dis


def power_module(P_signal,bodies,OEE):#AC to DC conversion at power bank
    xx = {body:[] for body in bodies}
    yy = {body:[] for body in bodies}
    for body in bodies:
        name = body.name
        splitname=name.split('_')
        xx[body].append(float(splitname[0]))
        yy[body].append(float(splitname[1]))
    xxm = [x[0] for x in xx.values()]
    yym = [y[0] for y in yy.values()]
    xm=np.mean(xxm)
    ym=np.mean(yym)
    d={body:[] for body in bodies}
    #integrate power of voltage produced at WEC and distribute to power bank, return max power available for distribution
    R_eff=5*10**-3 #ohm/meter
    V_lines=500 # Volts 
    P_substation=0
    for body in bodies:
        d[body].append(distance(xx[body][0],xm,yy[body][0],ym))
        i_lines=P_signal[body][0]/V_lines
        P_line_loss=(i_lines**2)*R_eff*d[body][0]
        #P_line_loss = 0
        #print(f"This is psignal now {P_signal[body][0]}")
        P_substation=P_substation+(P_signal[body][0]-P_line_loss)
    dist_shore=10000 # 10km
    V_trans=10000 # 10 kV
    P_trans_loss=(P_substation/V_trans)**2*R_eff*dist_shore
    #P_trans_loss = 0
    #print(P_trans_loss)
    OEE=0.9
    power_out=(P_substation-P_trans_loss)*OEE
    #print(f"Power out is {power_out}")
    #TODO: add losses at volatage step up and transmission to shore.
    p_sig = [p_sig[0] for p_sig in P_signal.values()]
    eff=power_out/(np.sum(p_sig))
    return power_out, eff


def cost_module(n_WEC,size,eff):
    a=0.0*10**3 #$/m2
    b=1.0*10**4 #$/m
    c=1.0*10**5 #$
    finance_rate=0.07
    risk_free_rate=0.04
    tax_rate=0.21
    power_system_cost=10000*n_WEC
    cost_WEC=a*size**2+b*size+c # this can be some polynomial to approximate how WEC cost scales
    cap_cost_WEC=(n_WEC*(cost_WEC+power_system_cost))*(risk_free_rate+finance_rate)*(1-tax_rate) #annualized cost of capital
    var_cost_WEC = n_WEC*10000/eff # need simple relations for how maint costs scale.
    return cap_cost_WEC, var_cost_WEC

# Core Econ function to call from main

def run(size,Power,bodies): 
    #print('Running Econ module')
    # Unpack variables: this will need to be editied to match order from main 
    n_WEC=len(bodies)
    lifetime=10#years
    OEE=0.9
    power_out,eff=power_module(Power,bodies,OEE)
    cap_costs_WEC, var_costs_WEC =cost_module(n_WEC,size,eff) #income from power generated
    LCOE=((var_costs_WEC*lifetime)+cap_costs_WEC)/(power_out/(10**3)*8760*OEE*lifetime)
    # Cost of capital and LCOE
    return power_out, eff, LCOE