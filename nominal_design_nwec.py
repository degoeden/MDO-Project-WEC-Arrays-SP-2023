import modules.model_nWECs as model
import numpy as np
import time as time
nwec = 4
# Design Vector
r = 3
wecx = [0, 0, 0, 0]
wecy = [0, 20, 40, 60]
d0 = 3
damp = [d0, d0, d0, d0]
x = np.zeros(2+3*(nwec-1))
x[0] = r
x[1] = damp[0]
for i in range(nwec-1):
    x[2+i*3] = wecx[i+1]
    x[3+i*3] = wecy[i+1]
    x[4+i*3] = damp[i+1]
x = [  6.16508689,   5.19148179, 176.55289471,  51.43802826,   5.25181387,
  33.13876137, -43.56398604,  5.17949576, 178.02307292,  26.23344913,
   5.28842795]
# Parameters
omega = 1.047
omega = 1
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,nwec]
start_time = time.time()
LCOE = model.run(x,p)
end_time = time.time()
print(f"This took this long: {end_time-start_time}")
print("LCOE: ", LCOE)
print(x)