import modules.model_nWECs as model
import numpy as np
nwec = 4
# Design Vector
r = 5
wecy = [0, 0, 0, 0]
wecx = [0, 10*r, 20*r, 30*r]
d0 = 1e4
damp = [d0, d0, d0, d0]
x = np.zeros(1+3*nwec)
x[0] = r
for i in range(nwec):
    x[1+i*3] = wecx[i]
    x[2+i*3] = wecy[i]
    x[3+i*3] = damp[i]
# Parameters
omega = 1.047
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,nwec]
Power_out,LCOE = model.run(x,p)
print("Power out: ", Power_out)
print("LCOE: ", LCOE)
