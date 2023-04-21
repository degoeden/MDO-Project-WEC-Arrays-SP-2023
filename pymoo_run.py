# To run A3b code, import the A3 interface and run the desired A3 function: gradient_method or heuristic_method
import optimization_interfaces.A3_interface as A3
import numpy as np
import matplotlib.pyplot as plt
import random as randy
import modules.model_nWECs as model
import modules.model_nWECs_fixr as model_fixr

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.termination.default import DefaultMultiObjectiveTermination
import scipy.optimize as scipy_opt


# ================================================================================= #
#                                   Set-Up                                          #
# ================================================================================= #
nwec = 4
# Initial Design Vector
r = 5
wecx = [0, randy.random()*200-100, randy.random()*200-100, randy.random()*200-100]
wecy = [0, randy.random()*200-100, randy.random()*200-100, randy.random()*200-100]
#wecx = [0, 40, 80, -20]
#wecy = [0, 0, 0, 0]
d0 = 3
damp = [d0, d0, d0, d0]
x0 = np.zeros(3*nwec-2)
x0[0] = r
x0[1] = damp[0]
for i in range(nwec-1):
    x0[1+i*3] = wecx[i+1]
    x0[2+i*3] = wecy[i+1]
    x0[3+i*3] = damp[i+1]

# Parameters
omega = 1.047
A = 1
rho_wec = 850
p = [omega,A,rho_wec,nwec]
opt={'xatol': 1e-5, 'disp': True}  
fig = plt.figure(1)
plt.plot(wecx,wecy,linestyle='none',marker = 'o',markersize = r*2,color='y')
# ================================================================================== #
from pymoo.core.problem import ElementwiseProblem

class MDO_Problem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=11,
                         n_obj=2,
                         n_ieq_constr=7,
                         xl=np.array([2,0,-1000,-1000,0,-1000,-1000,0,-1000,-1000,0]),
                         xu=np.array([100,10*8,1000,1000,10*8,1000,1000,10*8,1000,1000,10*8]))
    def _evaluate(self, x, out, *args, **kwargs):
        f1,f2 = model.run(x,p)
        g1 = -x[0]+2 # r min is 2m
        g2 = 2*x[0]-np.sqrt((x[2])**2+(x[3])**2) # r2
        g3 = 2*x[0]-np.sqrt((x[5])**2+(x[6])**2) # r3
        g4 = 2*x[0]-np.sqrt((x[8])**2+(x[9])**2) # r4
        g5 = 2*x[0]-np.sqrt((x[2]-x[5])**2+(x[3]-x[6])**2) # r2-r3
        g6 = 2*x[0]-np.sqrt((x[2]-x[8])**2+(x[3]-x[9])**2) # r2-r4
        g7 = 2*x[0]-np.sqrt((x[5]-x[8])**2+(x[6]-x[9])**2) # r3-r4
        # (n-1)! distance constraints, hard code for now
        out["F"] = [-f1, f2]
        out["G"] = [g1,g2,g3,g4,g5,g6,g7]


problem=MDO_Problem()


termination = DefaultMultiObjectiveTermination(
    xtol=1e-8,
    cvtol=1e-6,
    ftol=0.0025,
    period=30,
    n_max_gen=15,
    n_max_evals=1000
)

# ================================================================================= #
#                               Optimization Code                                   #
# ================================================================================= #
# Run Optimization

algorithm = NSGA2(pop_size=5)

res = minimize(problem,
               algorithm,
               termination,
               ('n_gen', 15),
               seed=1,
               verbose=False)

plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolor="red")
plot.show()
