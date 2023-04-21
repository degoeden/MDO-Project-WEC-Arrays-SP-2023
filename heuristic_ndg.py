# NDG x vector has 5 basic shapes and two spacing variables, as well as radius and all 4 pto dampers
# x = [shape, L1, L2, r, d1, d2, d3, d4]
# p = [freq, Amplitude, wec density, number of wecs]
import optimization_interfaces.A3_nate as A3

is_it_int = [True, False, False, False, False, False, False, False]
bnds = [[1,5],[0,100],[0,100],[2,8],[0,6],[0,6],[0,6]]

# Parameters
nwec = 4
omega = 1.047
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,nwec]

opt={'xatol': 1e-3, 'disp': True}  
# ================================================================================= #
#                               Optimization Code                                   #
# ================================================================================= #
# Run Optimization
best = A3.heuristic_method(p,bnds,is_it_int,opt)      #   Heuristic Optimization
print(best)
