# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic method
import A3_interface as A3

# Initial WEC design
r = 8
L = 20
d1 = 500
d2 = 500
k1 = 500
k2 = 500
x0 = [r,L,d1,k1,d2,k2]

# Parameters
omega = 1.047
A = 1.5
rho_wec = 850
n_wec = 2
p = [omega,A,rho_wec,n_wec]

bnds=[[2.5,15],[30,100],[10,500],[0,500],[10,500],[0,500]]
opt={'xatol': 1e-2, 'disp': True}

A3.gradient_method(x0,p,bnds,opt)