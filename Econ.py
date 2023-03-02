# Paceholder data
import numpy as np
#import pandas as pd


x0=np.array([0,1,2,3,4,5])# power in [units]
f0=np.array([1,2,3,4,5,6]) # Frequency in [units]
# Incoming internal variables:
# Power vs frequency ouput from WEC array elements
def func_init(): # __main__ goes somewhere... revisit.
    return print('This is the main function')

def sub_func_acdc1(p,cap):#AC to DC conversion at power bank
    #integrate power of voltage produced at WEC and distribute to power bank, return max power available for distribution
    return print('test')

def sub_func_dcac1(p_in,r):#DC to AC conversion step up to transmission voltage
    #implement losses during power conversion.. need relevent parameters
    p_out=np.mean(p_in*r)# some calculation of losses
    eff=np.mean(p_out/p_in) #some calculation of efficiency, with weighting or using net energy 
    return p_out,eff

def cost_module(p_out):
    mean_rate=1# placeholder for variable rates.
    revenue=p_out*mean_rate
    return revenue
# Design Parameters incoming:
# Cost of capital, lifetime costs, assumptions based on energy demand and rates

# Process

# convert power to high voltage AC at 60Hz
# feed power to grid
# compute revenue metrics