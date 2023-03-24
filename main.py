# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic method
import A3_interface as A3

# Initial WEC design
r = 5
L = 20
d1 = 100
d2 = 100
k1 = 300
k2 = 300
x0 = [r,L,d1,k1,d2,k2]

# Parameters
omega = 1.047
A = 1.5
rho_wec = 850
n_wec = 2
p = [omega,A,rho_wec,n_wec]

A3.gradient_method(x0,p)