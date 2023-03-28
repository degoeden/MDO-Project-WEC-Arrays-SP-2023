# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import A3_interface as A3

# Initial WEC design
r = 8
space = 3
d1 = 300
d2 = 300
k1 = 300
k2 = 300
x0 = [r,space,d1,k1,d2,k2]

# Parameters
omega = 1.047
A = 1.5
rho_wec = 850
n_wec = 2
p = [omega,A,rho_wec,n_wec]

bnds=[[2.5,15],[2,10],[10,500],[0,500],[10,500],[0,500]]    #   Set bounds for design variables
opt={'xatol': 1e-2, 'disp': True}                           #   Options: for gradient only

#best = A3.gradient_method(x0,p,bnds,opt)                    #   Gradient Optimization
best = A3.heuristic_method(p,bnds)                          #   Heuristic Optimization
print(best)                                                 #   Print Best Set-up