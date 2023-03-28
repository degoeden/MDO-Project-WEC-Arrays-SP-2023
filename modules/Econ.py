# Collection of Power distribution and Cost analysis modules
import numpy as np

#import pandas as pd

# Incoming internal variables:
# Power vs frequency ouput from WEC array elements

def power_module(P_signal,L,OEE):#AC to DC conversion at power bank
    #integrate power of voltage produced at WEC and distribute to power bank, return max power available for distribution
    R_eff=5*10**-3 #ohm/meter
    V_lines=500 # Volts 
    P1=np.abs(np.sum(P_signal)) #power into capacitor bank
    #print(P1)
    i_lines=P1/V_lines
    P_line_loss=i_lines**2*R_eff*L
    #print(P_line_loss)
    power_substation=(P1-P_line_loss)
    dist_shore=10000 # 10km
    V_trans=10000 # 10 kV
    P_trans_loss=(power_substation/V_trans)**2*R_eff*dist_shore
    #print(P_trans_loss)
    OEE=0.9
    power_out=(power_substation-P_trans_loss)*OEE
    #TODO: add losses at volatage step up and transmission to shore.
    eff=power_out/(P1)
    return power_out, eff


def cost_module(n_WEC,size,dist,eff):
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
    dist=x[2]
    lifetime=10#years
    OEE=0.9
    power_out,eff=power_module(Power,dist,OEE)
    cap_costs_WEC, var_costs_WEC =cost_module(n_WEC,size,dist,eff) #income from power generated
    LCOE=((var_costs_WEC*lifetime)+cap_costs_WEC)/(power_out/(10**3)*8760*OEE*lifetime)
    # Cost of capital and LCOE
    return power_out, eff, LCOE