#Main Code

#Our Modules
import modules.wec_dyn as wec_dyn
import modules.time_avg_power 
import Econ
import capy.notfinalbutworks as nfbw
import capy.geometry
import capy.hydrodyno
import capy.hydrostatics
#import capy1 

#Other packages:
import numpy as np


# Variables and Parameters:
#K_p = 100 #N/m : Proportional gain
#K_I = 10 #N/m.s : Integral Gain
#L = 100 #m : WEC spacing
#d = 0.36 #m : WEC diameter
#S= 0 # Spectral density function or array?
#k = 1000 # N/m : spring constant
#s = 10 #MPa : Nominal stiffness
#b = 10 #N.s/m : nominal damping

# Constraints --unused
#P_min = 10000 #W : minimum power Watts
#LCOE_max = 200 #$/MWhr

# Define design vector
#x=[L,d,k,s]
# Define parameters
p=[]
# Should some of these be internal variables determined during optimization? 
#...ex: control tuning parameters

#link modules together
def evaluate(x,p):
    #out1 = wec_dyn(x,p)
    #out2 = capy(x,p,out1)
    #out3 = time_avg_power(x,p,out2)
    rao1,rao2=nfbw.run(x[0],x[1])

    power=10**5 #100kW
    n_wec=2
    Power_out,efficiency,LCOE = Econ.run([n_wec,x[0],x[1]],p,power)
    # Define order of modules. connect inputs and outputs
    return Power_out,efficiency,LCOE

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

results = {'r_doe': [],
            'L_doe' : [], 'k_doe' : [],'s_doe' : [],'power':[],'efficiency':[],'LCOE':[]}


for i in range(np.size(x1)):
    x[i]=[r_doe[x1[i]+1],L_doe[x2[i]+1],k_doe[x3[i]+1],s_doe[x4[i]+1]]
    Power_out,efficiency,LCOE=evaluate(x[i],p)
    results['r_doe'].append(r_doe[x1[i]+1])
    results['L_doe'].append(L_doe[x2[i]+1])
    results['k_doe'].append(L_doe[x3[i]+1])
    results['s_doe'].append(L_doe[x4[i]+1])
    results['power'].append(Power_out)
    results['efficiency'].append(efficiency)
    results['LCOE'].append(LCOE)



data = pd.Dataframe.from_dict(results)
data.to_csv("data.csv")

