#Main Code

#Our Modules
import modules.wec_dyn as wec_dyn
import modules.time_avg_power 
import Econ
import capy.notfinalbutworks as nf
import capy.geometry
import capy.hydrodyno
import capy.hydrostatics
#import capy1

#Other packages:
import numpy as np


# Variables and Parameters:
K_p = 100 #N/m : Proportional gain
K_I = 10 #N/m.s : Integral Gain
L = 100 #m : WEC spacing
d = 0.36 #m : WEC diameter
S= 0 # Spectral density function or array?
k = 1000 # N/m : spring constant
s = 10 #MPa : Nominal stiffness
b = 10 #N.s/m : nominal damping

# Constraints
P_min = 10000 #W : minimum power Watts
LCOE_max = 200 #$/MWhr

# Define design vector
x=[L,d,k,s]
# Define parameters
p=[]
# Should some of these be internal variables determined during optimization? 
#...ex: control tuning parameters

#link modules together
def evaluate(x,p):
    out1 = wec_dyn(x,p)
    out2 = capy(x,p,out1)
    out3 = time_avg_power(x,p,out2)
    out4 = econ(x,p,out3)
    y = out4
    # Define order of modules. connect inputs and outputs
    
    return y

# Build DoE input vectors
x1=[0,0,0,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1]
x2=[0,1,-1,0,0,-1,1,-1,1,1,-1,-1,1,1,-1,1,-1]
x3=[0,1,-1,1,1,0,0,-1,1,-1,1,1,-1,-1,1,1,-1]
x4=[0,1,-1,1,1,1,-1,0,0,-1,1,-1,1,1,-1,-1,1]
x=np.zeros([17,4])
r_doe=[2,3,4]
L_doe=[200,300,400]
k_doe=[100,200,300]
s_doe=[10,20,30]
print('DoE Conditions: ')
for i in range(np.size(x1)):
    x[i]=[r_doe[x1[i]+1],L_doe[x2[i]+1],k_doe[x3[i]+1],s_doe[x4[i]+1]]
    print(x[i])

