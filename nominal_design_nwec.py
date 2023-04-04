import modules.model_4WECs as model

# Design Vector
r = 5
wecx = [0, 10*r, 20*r, 30*r]
wecy = [0, 0, 0, 0]
d = [1e5, 1e5, 1e5, 1e5]
x = [r,wecx,wecy,d]

# Parameters
omega = 1.047
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,4]
model.run(x,p)
