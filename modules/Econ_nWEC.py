# Collection of Power distribution and Cost analysis modules
import numpy as np

#import pandas as pd

# Incoming internal variables:
# Power vs frequency ouput from WEC array elements
def distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2+(y2-y1)**2)


def power_module(P_signal,xx,yy,OEE):#AC to DC conversion at power bank
    xm=np.mean(xx)
    ym=np.mean(yy)
    d=np.zeros(len(xx))
    #integrate power of voltage produced at WEC and distribute to power bank, return max power available for distribution
    R_eff=5*10**-3 #ohm/meter
    V_lines=500 # Volts 
    P_substation=0
    for k in range(len(xx)):
        d[k]=distance(xx[k],xm,yy[k],ym)
        i_lines=P_signal[k]/V_lines
        P_line_loss=i_lines**2*R_eff*d[k]
        P_substation=P_substation+(P_signal[k]-P_line_loss)
    dist_shore=10000 # 10km
    V_trans=10000 # 10 kV
    P_trans_loss=(power_substation/V_trans)**2*R_eff*dist_shore
    #print(P_trans_loss)
    OEE=0.9
    power_out=(power_substation-P_trans_loss)*OEE
    #TODO: add losses at volatage step up and transmission to shore.
    eff=power_out/(np.sum(P_signal))
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

def run(x,Power): 
    #print('Running Econ module')
    # Unpack variables: this will need to be editied to match order from main 
    n_WEC=x[0]
    size=x[1]
    xx=x[2]
    yy=x[3]
    lifetime=10#years
    OEE=0.9
    power_out,eff=power_module(Power,xx,yy,OEE)
    cap_costs_WEC, var_costs_WEC =cost_module(n_WEC,size,eff) #income from power generated
    LCOE=((var_costs_WEC*lifetime)+cap_costs_WEC)/(power_out/(10**3)*8760*OEE*lifetime)
    # Cost of capital and LCOE
    return power_out, eff, LCOE