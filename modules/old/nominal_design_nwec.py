import modules.model_nWECs as model
import numpy as np
nwec = 4
# Design Vector
r = 4.4
wecx = [0, 0, 0, 0]
wecy = [0, 51.125, 99.64, 147.72]
d0 = 1e4
damp = [d0, d0, d0, d0]
x = np.zeros(1+3*nwec)
x[0] = r
for i in range(nwec):
    x[1+i*3] = wecx[i]
    x[2+i*3] = wecy[i]
    x[3+i*3] = damp[i]
# Parameters
x = [4.40176867e+00, 0.00000000e+00, 0.00000000e+00, 1.00000001e+04, -8.20054418e-05, 5.12528358e+01, 1.00000000e+04, -5.74797483e-01, 9.96404646e+01, 1.00000000e+04, -1.94898682e-02, 1.49719833e+02, 1.00000000e+04]
omega = 1.047
omega = 1
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,nwec]
Power_out,LCOE = model.run(x,p)
print("Power out: ", Power_out)
print("LCOE: ", LCOE)
